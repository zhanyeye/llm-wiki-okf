# 基础设施知识库 Schema

本文件是能力索引。人读总览见 [`README.md`](README.md)。执行细节按意图读 [`.cursor/skills/infra-wiki/`](.cursor/skills/infra-wiki/)，**不要**在纯查询时通读本文件长文或整份 Skill 目录。

## 权限（三面）

| 面 | 路径 | Agent 行为 |
|----|------|------------|
| **知识面（OKF）** | 根 [`index.md`](index.md)、[`log.md`](log.md)、11 个分组目录 | 查询入口；写入只发生在这里 |
| **来源面** | [`raw/`](raw/) | **只读**。不要改、不要删。经 `sources` 引用 |
| **框架面** | [`README.md`](README.md)、本文件、`requirement.md`、`docs/`、`scripts/`、[`.cursor/`](.cursor/) | 改前先和用户确认；**不是**运维知识页；查询时不要当正文打开 |

知识面只写运维知识。不要把格式规范解说写进知识正文。禁止在仓库根随意新建知识 `.md`（必须进对应分组）。

## 查询

1. 读 [`index.md`](index.md)。
2. 现象不明时读 [`故障排查/index.md`](故障排查/index.md)。
3. 已知系统读 `系统与架构/<name>.md`；找入口/负责人读 `资源注册表/`。
4. 打开 2–5 篇作答，引用路径。
5. 仍不够再搜索 `tags` / `domain` / `services` / `title`。
6. **禁止**用训练数据填补未写入知识库的集群名、地址、凭证、步骤。缺失就说缺失，并建议入库。

有价值的综合结论应回写成新页。细则见 Skill [`query.md`](.cursor/skills/infra-wiki/query.md)。

## 写入前必须读

入库、迁文档、复盘、从零写页、改 index/log、体检时，**先读** Skill [`SKILL.md`](.cursor/skills/infra-wiki/SKILL.md) 按意图路由，再读对应文件（勿跳过）：

| 意图 | 必读 |
|------|------|
| 入库 / 迁文档 / 故障结案 | [`ingest.md`](.cursor/skills/infra-wiki/ingest.md) + [`types.md`](.cursor/skills/infra-wiki/types.md) + [`index-log.md`](.cursor/skills/infra-wiki/index-log.md) |
| 从零写一页 | [`author.md`](.cursor/skills/infra-wiki/author.md) + [`types.md`](.cursor/skills/infra-wiki/types.md) + [`index-log.md`](.cursor/skills/infra-wiki/index-log.md) |
| 体检、断链、过期 | [`lint.md`](.cursor/skills/infra-wiki/lint.md) |

type、目录、frontmatter、固定正文标题：全部在 [`types.md`](.cursor/skills/infra-wiki/types.md)。

## 值班

- 入口是 [`故障排查/index.md`](故障排查/index.md)。
- 故障关闭前：更新或新建 Incident；可复用步骤写入 Runbook 或 Playbook。
- 不要把一次性命令只留在聊天窗口。

## 路线图

Phase 0 当前（框架）。Phase 1 按痛点补手册/排查/注册表。Phase 2 迁约 80 篇。Phase 3 补架构、技能地图、新人上手、脚本。Phase 4 可选浏览与搜索。
