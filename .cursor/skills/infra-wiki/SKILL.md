---
name: infra-wiki
description: >-
  Queries and maintains the team infrastructure wiki under wiki/ (Markdown
  with YAML frontmatter; OKF knowledge surface). Use for 基础设施、知识库、值班、
  排查、入库、迁文档、复盘、playbook、runbook；以及 Rancher、MinIO、Helm、Harbor、
  NFS、px、yum、镜像、域名、DNS、证书、防火墙、openGauss、流水线、微服务重启、
  时延、磁盘满、绿区代理。Use when closing an incident, migrating an old doc
  into wiki/, linting wiki pages, or incremental ingest from company wiki
  links / raw/wiki/inbox.md via wiki-cli.
---

# infra-wiki

维护 `wiki/` 知识库。对话不是知识库；有价值的值班结论与综合要写回页面。

## 优先级

1. **安全**：不写密钥；不编造集群名、地址、步骤。
2. **接地**：只根据已打开的 `wiki/` 页作答；缺页就说缺页。
3. **分面**：知识只写 `wiki/`；`raw/` 默认只读（公司 wiki 通道例外见下）；框架面（仓根 `index.md` / `README.md` / `AGENTS.md` / `script/` / `tools/`）不是知识正文。
4. **按意图只读对应文件**；写入再读 schema，并完成 index/log + lint。

## 路由

| 用户意图 | 读 |
|----------|-----|
| 查、排障、东西在哪、怎么做 | [query.md](query.md) |
| type / 目录 / frontmatter / 固定标题 | [types.md](types.md) |
| 工单、纪要、迁文档、故障关闭 | [ingest.md](ingest.md) + [types.md](types.md) + [index-log.md](index-log.md) |
| 公司 wiki 链接 / inbox / 继续下一批 / 重试失败项 | [ingest-wiki.md](ingest-wiki.md) + [types.md](types.md) + [index-log.md](index-log.md) |
| 从零写一页 | [author.md](author.md) + [types.md](types.md) + [index-log.md](index-log.md) |
| 只改 index / log | [index-log.md](index-log.md) |
| 体检、过期、断链 | [lint.md](lint.md) |

默认走 query。查询**不要**先通读 `AGENTS.md`，不要读 `raw/`，不要一次加载整库，不要读写入用文件。

## 不变量

- **分面**：概念页只在 `wiki/` 对应分组。`raw/` 默认只读；例外：公司 wiki 通道可写 `raw/wiki/catalog.yaml`、`raw/wiki/archive/`、清理 `raw/wiki/inbox.md`（见 [ingest-wiki.md](ingest-wiki.md)）。
- **接地**：wiki 里没有的事实不要补；答案与命令只来自已读页面。
- **一页一概念**：每篇概念 `.md` 有 YAML frontmatter 与非空 `type`（见 [types.md](types.md)）。
- **写入闭环**：按 [types.md](types.md) 写页 → 正文自洽（查询不依赖打开 `raw/`）→ 按 [index-log.md](index-log.md) 更新 index/log → 跑 lint。
