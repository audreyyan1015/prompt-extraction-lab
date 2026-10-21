#!/usr/bin/env python3
"""Download the versioned experiment assets and check their SHA-256 hashes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(4 * 1024 * 1024):
            result.update(chunk)
    return result.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        default=Path(__file__).parent / "data" / "2026-10-21" / "download_manifest.json")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "artifacts")
    args = parser.parse_args()
    destination = args.output.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    assets = json.loads(args.manifest.read_text(encoding="utf-8"))
    for asset in assets:
        name = asset["filename"]
        if Path(name).name != name or name in ("", ".", ".."):
            raise ValueError(f"Invalid asset filename: {name!r}")
        target = destination / name
        if target.is_file() and target.stat().st_size == asset["size"] and digest(target) == asset["sha256"]:
            print(f"Verified existing asset: {name}", flush=True)
            continue
        if not asset["url"].startswith("https://"):
            raise ValueError(f"Asset URL must use HTTPS: {name}")
        temporary = destination / (name + ".part")
        print(f"Downloading {name} ({asset['size']:,} bytes)", flush=True)
        try:
            request = urllib.request.Request(asset["url"], headers={"User-Agent": "prompt-extraction-lab/1.0"})
            with urllib.request.urlopen(request, timeout=180) as response, temporary.open("wb") as output:
                while chunk := response.read(4 * 1024 * 1024):
                    output.write(chunk)
            if temporary.stat().st_size != asset["size"] or digest(temporary) != asset["sha256"]:
                raise RuntimeError(f"Size or SHA-256 mismatch for {name}")
            temporary.replace(target)
            print(f"Saved and verified: {target}", flush=True)
        finally:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
