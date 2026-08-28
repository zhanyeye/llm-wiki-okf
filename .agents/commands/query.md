---
description: 查询基础设施知识库（llm-wiki query）
---

调用 llm-wiki skill 的 **query** 流程，按 `.agents/skills/llm-wiki/query.md` 执行：优先检索 `wiki/`，不足再回退 `raw/`，引用页面路径作答；不要加载 ingest/lint 相关文件。

用户的问题：$ARGUMENTS
