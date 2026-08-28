---
description: 知识库体检（llm-wiki lint）
---

调用 llm-wiki skill 的 **lint** 流程：先读 `.agents/skills/llm-wiki/lint.md`，运行 `python tools/okf-lint/okf_lint.py`，先修 error 再处理 warning（Safe Fixes + 机械报告，人工判断项只报告不强改）。结束后汇报体检结果与已修/待办清单。

用户的附加要求（可选）：$ARGUMENTS
