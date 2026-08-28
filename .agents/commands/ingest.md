---
description: 入库/迁文档到知识库（llm-wiki ingest）
---

调用 llm-wiki skill 的 **ingest** 流程：先读 `.agents/skills/llm-wiki/SKILL.md` 路由，再按 `ingest.md` + `references/okf.md` + `references/index-log.md` 执行。若用户给的是公司 wiki 链接或要求刷新，走 `ingest.md` §公司 wiki + `references/source-wiki-cli.md`。写入后按 index-log 更新 index/log 并跑 lint。

用户的入库内容或来源：$ARGUMENTS
