---
name: infra-wiki
description: >-
  Maintains and queries the team infrastructure knowledge wiki (Markdown +
  YAML frontmatter). Use when the user asks about 基础设施, 知识库, 值班,
  排查, 入库, playbook, runbook, Rancher, MinIO, Helm, 磁盘满, 证书,
  绿区代理, or when creating, updating, or linting wiki pages.
---

# infra-wiki

本仓库的 `wiki/` 是要持续维护的知识库，不是一次性检索。对话不是知识库；有价值的结论写回 `wiki/`。

先读 [`AGENTS.md`](../../../AGENTS.md) 里的目录/`type` 表。本 Skill 只补工作流。

## 路由

| 用户意图 | 读 |
|----------|-----|
| 查、排障、东西在哪、怎么做 | [query.md](query.md) |
| 工单/纪要/故障结论入库 | [ingest.md](ingest.md) |
| 从零写一页 | [author.md](author.md) |
| 体检、过期、断链 | [lint.md](lint.md) |

默认走 query。

## 硬规则

- [`raw/`](../../../raw/) 只读，禁止修改。
- 先读 `wiki/index.md` 和相关分组 `index.md`，再打开正文。不要一次加载整库。
- 每个概念一篇 `.md`，YAML frontmatter 必有 `type`，且与 AGENTS.md 表格一致。
- `index.md` / `log.md` 是保留名，不加 `type`。仅根 `wiki/index.md` 可有 `okf_version: "0.2"`。
- 链接写成 `[MinIO](/系统与架构/minio.md)`。
- 写入后更新所在目录与根 `index.md`（若新增分组条目），并在 `wiki/log.md` **顶部**追加当日条目。
- `generated` / `verified` / `status` / `stale_after` 按 AGENTS.md 填写。
- `Registry` 页不写密码、token、kubeconfig。
- 禁止用训练数据填补未写入 wiki 的集群名、地址、步骤。
