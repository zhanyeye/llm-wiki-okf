---
description: 体检知识库（llm-wiki lint）
---

调用 llm-wiki skill 的 **Lint** 操作：读 `.agents/skills/llm-wiki/SKILL.md` §Lint，运行 `python tools/okf-lint/okf_lint.py`，先修 error 再做内容/新鲜度/schema 检查，结果写入 `wiki/log.md`。结束后汇报体检结果与已修/待办清单。

用户补充：$ARGUMENTS
