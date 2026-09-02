# llm-wiki-okf

本仓是基础设施 OKF 知识库。约定见 [AGENTS.md](AGENTS.md)，人读总览见 [README.md](README.md)。

技能实体在 [`.agents/skills/`](.agents/skills/)。[`.claude/skills`](.claude/skills) 是指向该目录的软链接，因此可以使用 **`/llm-wiki`**。

处理运维知识、值班排查、文档入库或知识库体检时，使用 Skill **llm-wiki**：先读 [`.agents/skills/llm-wiki/SKILL.md`](.agents/skills/llm-wiki/SKILL.md)，按意图只读对应文件（默认 `query.md`）。

- 查询 / 排障：`query.md`
- 入库 / 迁文档 / 从零写页：`ingest.md` + `references/compile.md` + `references/okf.md` + `references/index-log.md`
- 公司 wiki 链接：另读 `references/source-wiki-cli.md` 与 Skill `wiki-cli`（`/wiki-cli`）
- 体检：`lint.md`
- 审核：`review.md` + `references/compile.md`

知识按 L0 基础知识 → L1 Registry → Runbook/FAQ/ADR 编译；禁止把来源缩写后平铺成一页，也不要用训练数据填补 wiki 里没有的集群名、地址、凭证、步骤。L0 目录是 `wiki/基础知识/`。
