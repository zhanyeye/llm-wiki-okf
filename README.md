# 基础设施知识库

团队基础设施知识库。人和 Agent 读同一套 Markdown。本仓库是框架、模板和示例页。

组织方式来自两处：

- [Karpathy / llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)：`raw/` 与 `wiki/` 分离。人投放来源、提问；Agent 把知识编译进 wiki 并持续维护。wiki 是可复利的产物，对话不是。
- [Google Cloud Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)：用各层 `index.md` 做**渐进式索引**（progressive disclosure）。先读根 index 看有哪些分组，再读分组 index 看有哪些页，最后才打开 2–5 篇正文，不要一次加载整库。每页 YAML frontmatter（`type` 等）和 `scripts/okf_lint.py` 是配套约定，不是主轴。[OKF — The Markdown Spec for Humans and AI Agents](https://okf.md/)

## 目录结构

```
.
├── raw/                          # 人维护
├── wiki/                         # Agent 维护：结构化、互相链接的知识正文
│   ├── index.md                  # 根索引：只列分组（可有 okf_version）
│   ├── log.md                    # 追加式变更日志
│   ├── 资源注册表/index.md        # 分组索引：列本目录页面
│   ├── 系统与架构/                # 子分组，内也包含 index.md 进行索引
│   ├── 操作手册/
│   ├── 故障排查/                 
│   ├── 架构决策记录/
│   ├── 常见问题/
│   ├── 规范与约束/
│   ├── 案例与复盘/
│   ├── 技能地图/
│   ├── 新人上手/
│   └── 自动化脚本/
├── templates/                    # 按 OKF type 的正文模板
├── scripts/okf_lint.py           # wiki 体检
├── AGENTS.md                     # Agent 写 wiki 的 schema
└── .cursor/skills/infra-wiki/    # Ingest / Query / Lint
```


| 路径 | 谁维护 | 说明 |
| --- | --- | --- |
| [`raw/`](raw/) | **人** | 投放来源后告诉 Agent 入库。Agent **只读、不改、不删**。 |
| [`wiki/`](wiki/) | **Agent** | 编译后的知识。人读、提问、过目确认（`verified`）；不要把一次性结论只留在聊天里。 |
| [`AGENTS.md`](AGENTS.md)、[`templates/`](templates/)、[`.cursor/skills/infra-wiki/`](.cursor/skills/infra-wiki/) | 人（改前先确认） | 目录、模板、Ingest / Query / Lint 约定。 |




## 在 Code Agent 中使用

用 **Cursor** 或 **Claude Code** 打开本仓库，在 Agent 对话里用自然语言说话。人投放来源、提问、过目确认；Agent 按 Karpathy 的三条操作维护 `wiki/`。禁止脱离 wiki 臆造未写入的细节。

| 产品 | 会读什么 | 你怎么做 |
|------|----------|----------|
| [Cursor](https://cursor.com) | [`AGENTS.md`](AGENTS.md)、Rule [`.cursor/rules/infra-wiki.mdc`](.cursor/rules/infra-wiki.mdc)、Skill [`infra-wiki`](.cursor/skills/infra-wiki/) | 打开仓库 → Agent 聊天，直接问 |
| [Claude Code](https://code.claude.com/docs) | 根目录 [`AGENTS.md`](AGENTS.md) | 在仓库根运行 `claude`；需要更细路由时 `@.cursor/skills/infra-wiki/SKILL.md`，或把该目录拷到 `.claude/skills/infra-wiki/` |

### Ingest（摄入）

把来源编译进 `wiki/`。人先把工单、纪要、旧文档放进 [`raw/`](raw/)，再让 Agent 入库；Agent **不改** `raw/`。故障结论不要只留在聊天里。写入后会更新分组 `index.md` 和 [`wiki/log.md`](wiki/log.md)。

```text
把 raw/ 里这份工单入库。
这次故障结案，结论写进 wiki。
按模板补一页绿区转发代理操作说明。
```

### Query（查询）

问 `wiki/` 里已有的知识。Agent 先读 [`wiki/index.md`](wiki/index.md)，再打开分组 index，最后读 2–5 篇正文。只知道现象时走 [`wiki/故障排查/`](wiki/故障排查/)。

```text
磁盘满了怎么处理？
MinIO 的入口和负责人在哪？
Helm 部署失败怎么排查？
```

### Lint（检查）

检查 frontmatter、`type` 与目录是否一致、断链、过期、index/log 是否跟上。Agent 对话里说「体检一下 wiki」，或本地执行：

```bash
python scripts/okf_lint.py
```




## wiki 分组


| 目录 | `type` | 放什么 |
| --- | --- | --- |
| [`资源注册表/`](wiki/资源注册表/) | `Registry` | 资源、入口、环境、负责人、依赖、告警。不存凭证 |
| [`系统与架构/`](wiki/系统与架构/) | `Architecture` | 系统说明、拓扑、请求/数据链路 |
| [`操作手册/`](wiki/操作手册/) | `Runbook` | 标准操作或配置说明 |
| [`故障排查/`](wiki/故障排查/) | `Playbook` | 按症状排查、止损、升级 |
| [`架构决策记录/`](wiki/架构决策记录/) | `Decision` | 选型、权衡、约束 |
| [`常见问题/`](wiki/常见问题/) | `FAQ` | 短问答、工具速查、报错释义 |
| [`规范与约束/`](wiki/规范与约束/) | `Policy` | 命名、权限、变更、安全、CI 规范 |
| [`案例与复盘/`](wiki/案例与复盘/) | `Incident` | 故障/变更/演练复盘 |
| [`技能地图/`](wiki/技能地图/) | `Curriculum` | 能力范围、学习路径 |
| [`新人上手/`](wiki/新人上手/) | `Onboarding` | 接手清单、权限申请、首周任务 |
| [`自动化脚本/`](wiki/自动化脚本/) | `Automation` | 脚本说明、参数、权限、风险 |

业务域（原 00–08）写在 frontmatter 的 `domain`，不当目录。约定见 [`AGENTS.md`](AGENTS.md)。

## 路线图


| 阶段              | 做什么                           |
| --------------- | ----------------------------- |
| **Phase 0（当前）** | 框架、模板、schema、Skill、校验脚本、少量示例页 |
| **Phase 1**     | 按痛点补操作手册、故障排查、资源注册表           |
| **Phase 2**     | 存量文档落入 11 个目录、打 domain、互相链接   |
| **Phase 3**     | 补齐系统与架构、技能地图、新人上手、自动化脚本       |
| **Phase 4（可选）** | Obsidian / MkDocs；再加本地搜索      |


