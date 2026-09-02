---
name: llm-wiki
description: >-
  Build and maintain an OKF knowledge base under wiki/ using Karpathy-style
  ingest / query / lint. Sources are raw Markdown and company wiki URLs
  (via wiki-cli). Use for 基础设施、知识库、值班、排查、入库、迁文档、复盘、
  playbook、runbook；以及 Rancher、MinIO、Helm、Harbor、NFS、px、yum、镜像、
  域名、DNS、证书、防火墙、openGauss、流水线、微服务重启、时延、磁盘满、
  绿区代理。Triggers: ingest, query, lint, add to wiki, company wiki links,
  raw/wiki/inbox.md.
---

# llm-wiki

维护 `wiki/` 知识库。对话不是知识库；有价值的值班结论与综合要写回页面。

基于 [Karpathy LLM Wiki](https://github.com/Astro-Han/karpathy-llm-wiki) 三操作：**Ingest**、**Query**、**Lint**。编译结果用 [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 格式。
  
## 优先级

1. **安全**：不写密钥；不编造集群名、地址、步骤。
2. **接地**：查询只根据已打开的 `wiki/` 页作答；缺页就说缺页。
3. **分面**：知识只写 `wiki/`；`raw/` 默认只读（公司 wiki 通道例外：可追加 `inbox.md`、写 `archive/`，见 [references/source-wiki-cli.md](references/source-wiki-cli.md)）；框架面（仓根 `index.md` / `README.md` / `AGENTS.md` / `script/` / `tools/`）不是知识正文。
4. **按意图只读对应文件**；写入再读 schema，并完成 index/log + lint。

## 路由

| 用户意图 | 读 |
|----------|-----|
| 查、排障、东西在哪、怎么做 | [query.md](query.md) |
| 入库、迁文档、故障关闭、从零写一页、粘贴内容 | [ingest.md](ingest.md) + [references/compile.md](references/compile.md) + [references/okf.md](references/okf.md) + [references/index-log.md](references/index-log.md)；合适时再读 [references/obsidian.md](references/obsidian.md) |
| 公司 wiki 链接 / inbox / 继续下一批 / 重试失败项 | [ingest.md](ingest.md) §公司 wiki + [references/source-wiki-cli.md](references/source-wiki-cli.md) + [references/compile.md](references/compile.md) + [references/okf.md](references/okf.md) + [references/index-log.md](references/index-log.md) + `tools/wiki-export/wiki_export.py`；合适时再读 [references/obsidian.md](references/obsidian.md) |
| 增量刷新 / 刷新 wiki / 检查更新 | [ingest.md](ingest.md) §公司 wiki + [references/source-wiki-cli.md](references/source-wiki-cli.md) §增量刷新 |
| 执行操作 / 跑脚本 / 自动化执行 | [query.md](query.md) §自动化执行 |
| 只改 index / log | [references/index-log.md](references/index-log.md) |
| 体检、过期、断链 | [lint.md](lint.md) |
| 审核确认、列未审清单 | [review.md](review.md) + [references/compile.md](references/compile.md) + [references/index-log.md](references/index-log.md) |
| Obsidian 浏览 / Bases / Canvas / 公网 Defuddle | [references/obsidian.md](references/obsidian.md) |

默认走 query。查询**不要**先通读 `AGENTS.md`，不要读 `raw/`，不要一次加载整库，不要读写入用 references。

## 不变量

- **分面**：概念页只在 `wiki/` 对应分组（分组以 [`wiki/index.md`](../../../wiki/index.md) 为准，不在 skill 中硬编码）。
- **接地**：wiki 里没有的事实不要补；答案与命令只来自已读页面。
- **一页一概念**：每篇概念 `.md` 有 YAML frontmatter 与非空 `type`（见 [references/okf.md](references/okf.md)）。L0 在 `wiki/基础知识/<能力域>/`。
- **写入闭环**：禁止一来源一页。先拆基础知识 → Registry（双链 L0）→ Runbook/FAQ/ADR → 正文自洽 → 按 index-log.md 更新 index/log → 跑 lint。
- **公司 wiki**：禁止 WebFetch 内网 wiki；批量导出用 `tools/wiki-export/wiki_export.py`（内部串行调用 wiki CLI），编译仍由 Agent 按分层拆页。**增量刷新为默认模式**：只编译 wiki 有更新的条目；全量刷新需用户明确要求。
- **链接**：导航/来源用 Markdown 链接；语义关系必须用 `[[页]]` / `[[页#标题]]`，关键事实可用 `[[页#^block-id]]`。交叉引用按内容关系，禁止仅因同批互链；L0 不反向依赖 Runbook（见 okf.md）。
- **附件**：知识页图片统一 `./attachments/`（md 同目录）；raw 存档仍用 `images/`。
- **自动化**：正文含独立可运行脚本（≥5 行）时，提取到 `script/<功能名>/`（含脚本文件 + `README.md`），wiki 正文完整保留 + frontmatter 加 `automation` 块。Agent 执行操作时优先用 `script_ref`。详见 okf.md 和 ingest.md。
- **Obsidian 增强**：本仓常作 vault。编译/整理 wiki 时，在合适场景**主动**用项目内 Skill：`obsidian-cli`、`obsidian-markdown`、`obsidian-bases`、`json-canvas`、`defuddle`（细则 [references/obsidian.md](references/obsidian.md)）。权威顺序：**OKF > ingest 流程 > Obsidian 便利**；CLI/工具失败则回退普通 Read/Write，勿阻塞整批。

## 目录结构（可演进）

当前分组见 [`wiki/index.md`](../../../wiki/index.md)。未来增删分组时只改该文件与各分组 index，并同步更新 [references/okf.md](references/okf.md) 中的 type→目录映射表。

```
raw/          ← 来源（默认只读；raw/wiki/ 仅可追加 inbox、写 archive）
wiki/         ← OKF 编译结果（index.md、log.md、各分组）
```
