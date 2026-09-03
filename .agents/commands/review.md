---
description: 审核知识页（llm-wiki review）
---

调用 llm-wiki skill 的 **Lint** 审核段：读 `.agents/skills/llm-wiki/SKILL.md` 中 `### 4. Lint / Maintain (lint)` 的审核说明，列 `draft` / 无 `verified` / 已过期页。只有人明确确认并给出身份后才写 `verified.by: human:<id>` 和 `status: stable`。Agent 不得自行标 verified。

用户补充：$ARGUMENTS
