---
description: 入库/迁文档到知识库（llm-wiki ingest）
---

调用 llm-wiki skill 的 **ingest** 流程：先读 `.agents/skills/llm-wiki/SKILL.md` 路由，再按 `ingest.md` + `references/compile.md` + `references/okf.md` + `references/index-log.md` 执行。禁止一来源一页：先拆基础知识，再长 Registry/Runbook/FAQ/ADR，语义关系用双链。若用户给的是公司 wiki 链接或要求刷新，另读 `references/source-wiki-cli.md`。公司 wiki 批量可写 coverage manifest；Validate 通过后才更新 index/log 并跑 lint。

**写入范围（可选）**：用户用 [`wiki/index.md`](../../wiki/index.md) 里的**分组名**限制本次写入（不要求说 L0/L1）。未指定则全层拆分。指定分组 = 只 Compose 落在该分组的条目；其它性质条目标 deferred 并汇报，禁止把整篇硬塞进指定分组的一页。

示例：

```text
/ingest 这篇放进「网络管理」
/ingest 来源 xxx，只写「资源目录/集群」
/ingest 结案进「常见问题」和「案例与复盘」
/ingest 先只沉淀「基础知识」
```

可写顶层分组（基础知识、资源目录、操作手册…），也可写子分组（网络管理、集群…）。细则见 `ingest.md` §写入分组。

用户的入库内容或来源：$ARGUMENTS
