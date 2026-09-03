---
description: 入库/迁文档到知识库（llm-wiki ingest）
---

调用 llm-wiki skill 的 **Ingest** 操作：读 `.agents/skills/llm-wiki/SKILL.md` §Ingest。禁止一来源一页：先拆基础知识（Foundation），再长资源目录 / 手册 / FAQ / ADR，语义关系用双链。写页时读 `references/okf.md`。公司 wiki 链接或刷新另读 `references/source-wiki-cli.md`。Validate 通过后更新 index/log 并跑 lint。

用户可用 `wiki/index.md` 分组名限制写入范围（如「网络管理」「操作手册」）；未指定则全层拆分。

用户的入库内容或来源：$ARGUMENTS
