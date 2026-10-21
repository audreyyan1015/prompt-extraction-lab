# 公开系统提示词资料

本目录对应报告附录A。检索日期为2026年10月21日。

## 官方原文

xAI 的两份模板按官方仓库 AGPL-3.0 许可证保存，原文未作修改。许可全文位于 `xai/LICENSE`；固定提交、下载地址与 SHA-256 位于 `xai/sources.json`。

- `xai/ask_grok_system_prompt.j2`：Grok 在 X 平台的回复提示词全文。
- `xai/grok3_official0330_p1.j2`：Grok 3 聊天助手提示词模板全文。

## 原文节选与结构分析

### Claude Sonnet 3.5

来源：官方公开；条目日期：2024-11-22。

[原始条目](https://platform.claude.com/docs/en/release-notes/system-prompts/claude-sonnet-3-5)

对应英文节选见报告附录A。

2024 年 11 月 22 日的文本首先给出模型身份、当前日期占位符和知识更新时间，随后依次说明链接访问能力、回答方式、复杂问题处理、信息不确定性、交流风格及内容边界。动态日期由模板变量注入，知识更新时间则保持为固定事实；两者共同帮助模型判断问题是否涉及知识范围之外的事件。该页面记录的是 Claude 网页与移动端的产品提示词。

### Microsoft Copilot

来源：社区存档；条目日期：2024-03-10。

[原始条目](https://github.com/jujumilk3/leaked-system-prompts/blob/2bffdfe275e5dc4725b23e20c330e036ef438802/microsoft-copilot_20240310.md)

[上游记录](https://old.reddit.com/r/bing/comments/1bapeh7/copilots_initial_prompt_as_of_march_2024/)

对应英文节选见报告附录A。

该存档包含用户请求和解码后的模型回答。用户将初始提示词输出包装为 Base64 编码任务，并在后续消息中要求继续编码。被记录的回答按身份、内部工具、回复要求、能力、输出格式、限制和安全规则组织，其中明确出现提示词保密规则。这个案例对应了格式转换型提取方法：输出形式发生改变，所请求的信息对象仍是初始指令。

### Perplexity GPT-4

来源：社区存档；条目日期：2024-03-11。

[原始条目](https://github.com/jujumilk3/leaked-system-prompts/blob/2bffdfe275e5dc4725b23e20c330e036ef438802/perplexity.ai_gpt4_20240311.md)

[上游记录](https://github.com/jujumilk3/leaked-system-prompts/issues/14#issuecomment-1988489006)

对应英文节选见报告附录A。

该存档记录了一次要求忽略既有指令并输出前文的请求，随后展示了一段描述 Perplexity 回答行为的文本。文本强调以检索结果支持回答、保持问答语言一致、在相关句末使用数字引用，以及按 Markdown 和 LaTeX 组织内容。与通用聊天提示词相比，这些要求更集中于检索结果整合和来源呈现。

