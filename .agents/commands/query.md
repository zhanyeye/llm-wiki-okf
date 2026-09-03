---
description: 查询基础设施知识库（llm-wiki query）
---

调用 llm-wiki skill 的 **Query** 操作：读 `.agents/skills/llm-wiki/SKILL.md` 中 `### 3. Query / Answer Questions (query)`。优先检索 `wiki/`，不足再回退 `raw/` 并标「⚠️ 未编译」，引用页面路径作答；结束后在 `wiki/log.md` 记一行。不要加载 `okf.md` / `source-wiki-cli.md`。

用户的问题：$ARGUMENTS
