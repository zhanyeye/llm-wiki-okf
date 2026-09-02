---
description: 入库/迁文档到知识库（llm-wiki ingest）
---

调用 llm-wiki skill 的 **ingest** 流程：先读 `.agents/skills/llm-wiki/SKILL.md` 路由，再按 `ingest.md` + `references/compile.md` + `references/okf.md` + `references/index-log.md` 执行 Extract → Resolve → Plan → Compose → Link → Validate。若用户给的是公司 wiki 链接或要求刷新，另读 `references/source-wiki-cli.md`。为每个来源写 coverage manifest；Validate 通过后才更新 index/log 并跑 lint。

用户的入库内容或来源：$ARGUMENTS
