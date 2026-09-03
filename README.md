# 基础设施知识库

团队基础设施知识库。人和 Agent 读同一套 Markdown。知识按 **L0 基础知识 → L1 资源目录 → 运维与设计（Runbook / FAQ / ADR）** 生长：先沉淀内网特有概念，再登记部署实例，手册与问答用双链引用下层。禁止把来源文档平铺成一页。

组织方式来自两处：

- [Karpathy LLM Wiki](https://github.com/Astro-Han/karpathy-llm-wiki) / [Karpathy gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)：`raw/` 与 `wiki/` 分离。人投放来源、提问；Agent 把知识编译进 wiki 并持续维护。wiki 是可复利的产物，对话不是。
- [Google Cloud Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)：用各层 `index.md` 做**渐进式索引**（progressive disclosure）。先读 `wiki/index.md` 看有哪些分组，再读分组 index，最后打开 2–5 篇正文。每页 YAML frontmatter（`type` 等）和 `tools/okf-lint/okf_lint.py` 是配套约定。[OKF — The Markdown Spec for Humans and AI Agents](https://okf.md/)

**分享请 clone 整仓**（含 `wiki/` 与 `raw/`），不要只拷 `wiki/`。知识页须自洽；`sources` 只做溯源。

## 目录结构

```
.
├── index.md                      # 仓地图：wiki / raw / script / tools
├── wiki/                         # OKF 知识图：Agent 维护
│   ├── index.md                  # 知识入口：按层和能力域
│   ├── log.md                    # 追加式变更日志
│   ├── _meta/ingest/             # 公司 wiki 批量可选的覆盖清单
│   ├── 基础知识/                   # L0：内网特有概念/平台（按能力域）
│   ├── 资源目录/                 # L1：部署实例（集群/数据库/存储/中间件/可观测）
│   ├── 操作手册/                   # Runbook：引用 L0/L1
│   ├── 常见问题/                   # FAQ：短问答与按症状排查；值班入口
│   ├── 架构决策记录/
│   └── 案例与复盘/
├── raw/                          # 人维护：只读来源
├── script/                       # 运维可执行脚本
├── tools/                        # 维护本仓的框架工具
│   ├── index.md                  # 工具总览
│   └── okf-lint/                 # wiki 体检
│       ├── README.md
│       └── okf_lint.py
├── AGENTS.md                     # 能力索引；细则在 Skill
├── CLAUDE.md                     # Claude Code 入口
├── .agents/skills/               # 技能实体（Cursor / Codex 扫描）
├── examples/network-pilot/       # 与正式 wiki 隔离的虚构分层试点
└── .claude/skills -> .agents/skills  # 软链接，供 Claude `/llm-wiki`
```

| 面 | 路径 | 谁维护 | 说明 |
| --- | --- | --- | --- |
| **知识面** | [`wiki/`](wiki/) | **Agent** | 编译后的知识。人读、提问、过目确认（`verified`）。 |
| **来源面** | [`raw/`](raw/) | **人** | 投放来源后告诉 Agent 入库。一般 raw Agent **只读**；公司 wiki 见 [`raw/wiki/`](raw/wiki/)（增量 `inbox.md` + `archive/`）。 |
| **框架面** | 仓根 [`index.md`](index.md)、[`AGENTS.md`](AGENTS.md)、[`README.md`](README.md)、[`script/`](script/)、[`tools/`](tools/)、[`.agents/skills/`](.agents/skills/) | 人（改前先确认） | 约定与工具；**不是**运维知识页。运维脚本在 `script/`，框架工具在 `tools/`，用法写在 `wiki/操作手册/`（运维）或 `tools/*/README.md`（框架）。 |

## 在 Code Agent 中使用

使用 **CodeAgent** 打开本仓库，在对话里提问或下命令即可。人投放来源、提问、过目确认；Agent 会读 [`AGENTS.md`](AGENTS.md) 和 Skill [`llm-wiki`](.agents/skills/llm-wiki/)，按查 / 入库 / 体检维护 `wiki/`。禁止脱离 wiki 臆造未写入的细节。

两种用法可以混：直接用自然语言，或打斜杠命令（定义在 [`.agents/commands/`](.agents/commands/)）。命令会把意图钉死，少绕路。

| 命令 | 做什么 | 示例 |
|------|--------|------|
| [`/query`](.agents/commands/query.md) | 查 wiki、排障 | `/query 磁盘满了怎么处理` |
| [`/ingest`](.agents/commands/ingest.md) | 入库、迁文档、结案写页 | `/ingest 把 raw/ 里这份工单入库` |
| [`/lint`](.agents/commands/lint.md) | 体检、断链、过期 | `/lint` |
| [`/review`](.agents/commands/review.md) | 列未确认页、人工审核标 `verified` | `/review` |

贴公司 wiki 链接时用 `/ingest`（也可以把 URL 直接丢进对话）。不记得命令就原话说，例如「把 inbox 入库」「体检一下 wiki」。下文四条操作各有一组可复制的说法。

### Ingest（摄入）

把来源编译进 `wiki/`。人先把工单、纪要、旧文档放进 [`raw/`](raw/)，再让 Agent 入库；一般来源 Agent **不改** `raw/`（公司 wiki：可追加 `inbox.md`、写 `archive/`）。**禁止一来源一页**：内部概念进 L0 基础知识（按能力域），部署实例进 Registry 并双链 L0，步骤/问答/决策再写 Runbook/FAQ/ADR。写入后会更新分组 `index.md` 和 [`wiki/log.md`](wiki/log.md)。

```text
把 raw/ 里这份工单入库。
这次故障结案，结论写进 wiki。
补一页绿区转发代理操作说明。
把这些 wiki 链接入库：
https://wiki.example.com/pages/viewpage.action?pageId=12001
把 inbox 入库。
```

公司 wiki：人对话贴链接，或写 [`raw/wiki/inbox.md`](raw/wiki/inbox.md)（只追加、入库不删行）。导出到 `raw/wiki/archive/<pageId>/` 后，先拆基础知识再长 Registry/Runbook/FAQ/ADR；导出工具只保存来源，不负责知识生成。知识页 `sources` 只写原始 URL。新页 `status: draft`，通过语义审核后再标 `verified`。公司 wiki 批量可写 `wiki/_meta/ingest/<docKey>.yaml`，该清单不进知识导航。

### Query（查询）

问 `wiki/` 里已有的知识。Agent 先读 [`wiki/index.md`](wiki/index.md)，按层选起点：是什么/内部概念走 [`基础知识`](wiki/基础知识/)；哪一套走 [`资源目录`](wiki/资源目录/)；怎么做走操作手册；为什么走 ADR；只知道现象或短问答时走 [`wiki/常见问题/`](wiki/常见问题/)。

```text
磁盘满了怎么处理？
某服务的入口和负责人在哪？
Helm 部署失败怎么排查？
```

### Lint（检查）

检查 frontmatter、`type` 与目录是否一致、断链、过期、index/log 是否跟上。Agent 对话里说「体检一下 wiki」，或本地执行：

```bash
python tools/okf-lint/okf_lint.py
```

### Review（审核）

编译产物的质量最终由人判断：机器管格式与断链（lint），"内容对不对"由人看完正文说了算。`/review` 列出所有未确认（`status: draft` 或无人工 `verified`）与待复审（`stale_after` 已过）的页面，逐篇请人过目；人说「这篇 OK」才写 `verified` 与 `status: stable`，说「不对」走 ingest 更正。

```text
哪些还没确认？
/review
第 2 篇 OK
```

## wiki 分组


| 目录 | `type` | 放什么 |
| --- | --- | --- |
| [`基础知识/`](wiki/基础知识/) | `Foundation` | 内网特有概念、平台、规则（按能力域分子目录）；上层用双链引用 |
| [`资源目录/`](wiki/资源目录/) | `Registry` | 部署实例：哪一套、入口、环境、负责人、依赖、告警。不存凭证 |
| [`操作手册/`](wiki/操作手册/) | `Runbook` | 标准操作、配置说明与脚本用法（`.py` 在 `script/`） |
| [`常见问题/`](wiki/常见问题/) | `FAQ` | 短问答、报错释义、按症状排查与止损（值班入口） |
| [`架构决策记录/`](wiki/架构决策记录/) | `Decision` | 选型、权衡、约束 |
| [`案例与复盘/`](wiki/案例与复盘/) | `Incident` | 故障/变更/演练复盘 |

业务域写在 frontmatter 的 `domain`。基础知识按能力域分子目录；Registry 按资产种类分子目录。语义关系必须使用 Obsidian `[[页]]` / `[[页#标题]]`，关键稳定事实可用 `[[页#^block-id]]`。type / frontmatter / Registry 画像见 Skill [`references/okf.md`](.agents/skills/llm-wiki/references/okf.md)。

## 路线图


| 阶段              | 做什么                           |
| --------------- | ----------------------------- |
| **Phase 0（当前）** | L0 基础知识能力域 + L1 资产类骨架、双链约定 |
| **Phase 1**     | 按痛点补 L0 概念页与 Registry 实例，再补高频 Runbook/FAQ/ADR |
| **Phase 2**     | 存量来源按「先拆基础知识再长上层」重编译，禁止平铺 |
| **Phase 3**     | 补齐架构、自动化与演练 |
| **Phase 4** | Obsidian/MkDocs 视图与持续质量治理 |
