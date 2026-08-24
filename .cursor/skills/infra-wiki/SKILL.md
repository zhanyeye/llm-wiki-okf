---
name: infra-wiki
description: >-
  Queries and maintains the team infrastructure knowledge surface at repo root
  (Markdown with YAML frontmatter; OKF bundle). Use for 基础设施、知识库、值班、
  排查、入库、迁文档、复盘、playbook、runbook；以及 Rancher、MinIO、Helm、Harbor、
  NFS、px、yum、镜像、域名、DNS、证书、防火墙、openGauss、流水线、微服务重启、
  时延、磁盘满、绿区代理。Use when closing an incident, migrating an old doc
  into a knowledge group, or linting knowledge pages.
---

# infra-wiki

知识面（根 `index.md` / `log.md` + 11 个分组）是要持续维护的知识库。对话不是知识库；值班结论和有用的综合要写回页面。不要把 `README.md` / `AGENTS.md` 当知识正文。

查询只走 [query.md](query.md)，**不要**先通读 `AGENTS.md`，不要读 `raw/`，不要一次加载整库。选目录、写 frontmatter 时再读 [types.md](types.md)（含完整字段与固定标题）。写入后按 [index-log.md](index-log.md) 更新 `index.md` 与 `log.md`。

## 路由

| 用户意图 | 读 |
|----------|-----|
| 查、排障、东西在哪、怎么做 | [query.md](query.md) |
| 工单/纪要/故障结论入库 | [ingest.md](ingest.md) + [types.md](types.md) + [index-log.md](index-log.md) |
| 故障关闭、复盘、值班结束 | [ingest.md](ingest.md) + [types.md](types.md) + [index-log.md](index-log.md) |
| 把旧文档迁进知识库 | [ingest.md](ingest.md) + [types.md](types.md) + [index-log.md](index-log.md) |
| 从零写一页 | [author.md](author.md) + [types.md](types.md) + [index-log.md](index-log.md) |
| 更新 index / log | [index-log.md](index-log.md) |
| 体检、过期、断链 | [lint.md](lint.md) |

默认走 query。

## 硬规则

- `raw/` 只读，禁止修改。
- 先读根 `index.md` 和相关分组 `index.md`，再打开正文。不要一次加载整库。
- 每个概念一篇 `.md`，YAML frontmatter 必有 `type`，且与 [types.md](types.md) 一致。知识页必须放在对应分组目录，不要写在仓库根。
- `index.md` / `log.md` 是保留名，不加 `type`。格式见 [index-log.md](index-log.md)。仅根 `index.md` 可有 `okf_version: "0.2"`。
- 链接：同目录 `./file.md`；跨目录 `[MinIO](/系统与架构/minio.md)`（相对 bundle 根）。
- 写入后按 [index-log.md](index-log.md) 更新分组 `index.md` 与 `log.md`（新分组才改根 index）。禁止跳过。
- `Registry` 不写密码、token、kubeconfig。raw/对话里的密钥不要抄进知识页。
- 知识库里没有的集群名、地址、步骤不要编。
