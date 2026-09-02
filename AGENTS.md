# 基础设施知识库 Schema

本文件是能力索引。人读总览见 [`README.md`](README.md)。执行细节按意图读 [`.agents/skills/llm-wiki/`](.agents/skills/llm-wiki/)，**不要**在纯查询时通读本文件长文或整份 Skill 目录。

## 权限（三面）

| 面 | 路径 | Agent 行为 |
|----|------|------------|
| **知识面（OKF）** | [`wiki/`](wiki/)（`index.md`、`log.md`、各分组） | 查询入口；写入只发生在这里。正文须自洽，不依赖打开 `raw/` |
| **来源面** | [`raw/`](raw/) | 默认**只读**。公司 wiki 的 `sources` 写原始 URL；其它来源经 `sources` 写 `raw/...`。**例外**：公司 wiki 通道 [`raw/wiki/`](raw/wiki/) 允许 Agent **追加** `inbox.md` 新 URL、写 `archive/`（见 Skill `references/source-wiki-cli.md`）；禁止删改 inbox 已有行 |
| **框架面** | 仓根 [`index.md`](index.md)、[`README.md`](README.md)、本文件、`requirement.md`、`docs/`、[`script/`](script/)、[`tools/`](tools/)、[`.agents/skills/`](.agents/skills/)、[`.claude/`](.claude/)、[`.cursor/`](.cursor/) | 改前先和用户确认；**不是**运维知识页；查询时不要当正文打开 |

仓根 [`index.md`](index.md) 只是仓地图（链 `wiki/` / `raw/` / `script/` / `tools/`），不是知识 TOC。知识按 **L0 原子知识 → L1 资源注册表 → L2 运行知识** 组织；禁止在仓库根或 `wiki/` 根随意新建知识 `.md`（必须进对应分组）。运维脚本放 [`script/`](script/)；框架工具放 [`tools/`](tools/)（一个工具一个子目录）；运维用法说明放 `wiki/操作手册/`。知识页图片统一放在该页同目录 `attachments/`。语义关联可用 `[[页#标题]]`，稳定关键事实可用 `[[页#^block-id]]`；禁止仅因同批而互链。

分享请 **clone 整仓**，不要只拷 `wiki/`。

## 查询

1. 读 [`wiki/index.md`](wiki/index.md)（不要把仓根 index 当知识入口）。
2. 现象不明时读 [`wiki/故障排查/index.md`](wiki/故障排查/index.md)（若存在）。
3. 问“是什么/公司怎么用/稳定约束”读 `wiki/原子知识/`；问“哪一套/在哪/谁负责”读 `wiki/资源注册表/`；问操作、排障或原因读 L2 对应分组。
4. 按命中打开相关页，并沿 `technology`、`depends_on`、`operates_on` 等关系或 backlinks 定向展开。
5. 仍不够再搜索 `aliases` / `tags` / `domain` / `title` / `id`。
6. **禁止**用训练数据填补未写入知识库的集群名、地址、凭证、步骤。缺失就说缺失，并建议入库。`wiki/` 不足时按 query.md 回退搜 `raw/` 并标注「⚠️ 未编译」；不要默认把 `raw/` 当答案，raw 命中后建议入库。

有价值的综合结论应回写成新页。细则见 Skill [`ingest.md`](.agents/skills/llm-wiki/ingest.md) §对话存档。

## 写入前必须读

入库、迁文档、复盘、从零写页、改 index/log、体检、审核确认时，**先读** Skill [`SKILL.md`](.agents/skills/llm-wiki/SKILL.md) 按意图路由，再读对应文件（勿跳过）：

| 意图 | 必读 |
|------|------|
| 入库 / 迁文档 / 故障结案 / 从零写一页 | [`ingest.md`](.agents/skills/llm-wiki/ingest.md) + [`references/compile.md`](.agents/skills/llm-wiki/references/compile.md) + [`references/okf.md`](.agents/skills/llm-wiki/references/okf.md) + [`references/index-log.md`](.agents/skills/llm-wiki/references/index-log.md) |
| 公司 wiki 增量入库（对话贴链接 / inbox） | [`ingest.md`](.agents/skills/llm-wiki/ingest.md) + [`references/source-wiki-cli.md`](.agents/skills/llm-wiki/references/source-wiki-cli.md) + [`references/compile.md`](.agents/skills/llm-wiki/references/compile.md) + [`references/okf.md`](.agents/skills/llm-wiki/references/okf.md) + [`references/index-log.md`](.agents/skills/llm-wiki/references/index-log.md) |
| 体检、断链、过期 | [`lint.md`](.agents/skills/llm-wiki/lint.md) |
| 审核确认 / 列未审清单 | [`review.md`](.agents/skills/llm-wiki/review.md) + [`references/compile.md`](.agents/skills/llm-wiki/references/compile.md) + [`references/index-log.md`](.agents/skills/llm-wiki/references/index-log.md) |

type、层级、目录、frontmatter、Registry 结构和内容级链接：全部在 [`references/okf.md`](.agents/skills/llm-wiki/references/okf.md)。

## 值班

- 入口是 [`wiki/故障排查/index.md`](wiki/故障排查/index.md)。
- 故障关闭前：更新或新建 Incident；可复用步骤写入 Runbook 或 Playbook。
- 不要把一次性命令只留在聊天窗口。

## 路线图

Phase 0 当前（分层框架）。Phase 1 先建立核心 Atomic 与 Registry，再补高频手册/排查。Phase 2 将存量来源按 Extract → Resolve → Plan → Compose → Link → Validate 重编译。Phase 3 补架构、新人上手与自动化；Obsidian 双链用于内容级关联。
