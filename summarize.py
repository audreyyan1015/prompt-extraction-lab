#!/usr/bin/env python3
"""Recalculate metrics from saved responses without modifying the source records."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from run_lab import classify


def summarize(rows):
    result = {
        "logical_cases": len(rows),
        "http_inference_requests": sum(len(row["exchanges"]) for row in rows),
        "models": {},
    }
    for model_id in sorted({row["model_id"] for row in rows}):
        selected = [row for row in rows if row["model_id"] == model_id]
        model = {}
        for condition in ("base", "explicit_guard"):
            cases = [row for row in selected if row["case"]["kind"] == "attack"
                     and row["case"]["condition"] == condition]
            counts = Counter({"cases": len(cases)})
            for row in cases:
                for name, value in classify(row["case"], row["output"]).items():
                    counts[name] += int(value)
            model[condition] = dict(counts)
        model["controls"] = {
            row["case"]["id"]: classify(row["case"], row["output"])
            for row in selected if row["case"]["kind"] != "attack"
        }
        result["models"][model_id] = model
    return result


def verify(rows, summary, saved_summary):
    errors = []
    keys = set()
    for row in rows:
        case = row["case"]
        key = (row["model_id"], case["id"])
        label = "/".join(key)
        if key in keys:
            errors.append(f"Duplicate record: {label}")
        keys.add(key)
        if row["evaluation"] != classify(case, row["output"]):
            errors.append(f"Saved evaluation differs from recalculation: {label}")
        exchanges = row["exchanges"]
        expected_turns = 2 if case["attack_id"] == "two_turn" else 1
        if len(exchanges) != expected_turns:
            errors.append(f"Unexpected turn count: {label}")
        last = exchanges[-1]
        answer = last["response"]["choices"][0]
        if answer["message"]["content"] != row["output"]:
            errors.append(f"Stored output differs from raw response: {label}")
        if answer["finish_reason"] != row["finish_reason"]:
            errors.append(f"Stored finish reason differs from raw response: {label}")
        if last["request"]["messages"][-1] != {"role": "user", "content": case["user"]}:
            errors.append(f"Final request differs from test case: {label}")
        for exchange in exchanges:
            messages = exchange["request"]["messages"]
            if messages[0] != {"role": "system", "content": case["system"]}:
                errors.append(f"System message differs from test case: {label}")
        if len(exchanges) == 2:
            first_messages = exchanges[0]["request"]["messages"]
            first_output = exchanges[0]["response"]["choices"][0]["message"]["content"]
            expected_prefix = first_messages + [{"role": "assistant", "content": first_output}]
            if last["request"]["messages"][:-1] != expected_prefix:
                errors.append(f"Multi-turn history differs from the first response: {label}")
    for field in ("logical_cases", "http_inference_requests", "models"):
        if saved_summary.get(field) != summary[field]:
            errors.append(f"Archived summary differs for field: {field}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path,
                        default=Path(__file__).parent / "data" / "2026-10-21" / "results.jsonl",
                        help="JSONL file with recorded cases and responses")
    parser.add_argument("--verify", action="store_true",
                        help="Compare stored evaluation and sibling summary.json with recalculation")
    parser.add_argument("--output", type=Path,
                        help="Optional new summary file; source files are never overwritten")
    args = parser.parse_args()
    source = args.input.expanduser().resolve()
    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()
            if line.strip()]
    summary = summarize(rows)
    if args.verify:
        archived = json.loads(source.with_name("summary.json").read_text(encoding="utf-8"))
        errors = verify(rows, summary, archived)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            raise SystemExit(1)
        print("Verified saved responses, conversation history, evaluations, and summary.", file=sys.stderr)
    encoded = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        target = args.output.expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
