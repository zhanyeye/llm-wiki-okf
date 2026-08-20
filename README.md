# 基础设施知识库

团队内网知识库框架。人和 Agent 读同一套 Markdown。现有约 80 篇文档仍在内网；本仓库是框架、模板和示例页，不含内网原文。迁入时按模板补 frontmatter、改交叉链接即可。

## 怎么用

**查**

1. 打开 [`wiki/index.md`](wiki/index.md)。
2. 只知道现象时，打开 [`wiki/故障排查/index.md`](wiki/故障排查/index.md)。
3. 已知系统名 → [`wiki/系统与架构/`](wiki/系统与架构/)；找入口/负责人 → [`wiki/资源注册表/`](wiki/资源注册表/)。

在 Cursor 里直接提问；项目 Skill `infra-wiki` 按上述顺序检索，禁止脱离 wiki 臆造内网细节。

**写**

- 套 [`templates/`](templates/) 对应模板。
- 故障处理后把结论写入 wiki，不要只留在聊天里。
- 写入后更新相关 `index.md`，并在 [`wiki/log.md`](wiki/log.md) 追加一条。

**体检**

```bash
python scripts/okf_lint.py
```

## 三层

| 层 | 路径 | 说明 |
|---|---|---|
| 来源 | [`raw/`](raw/) | 只读。工单摘录、导出草稿。Agent 不修改。 |
| 知识 | [`wiki/`](wiki/) | 结构化、互相链接。查询与值班都读这里。 |
| 约定 | [`AGENTS.md`](AGENTS.md)、[`templates/`](templates/)、[`.cursor/skills/infra-wiki/`](.cursor/skills/infra-wiki/) | 目录、模板、查/写/入库/体检流程。 |

## wiki 分组

| 目录 | `type` | 放什么 |
|------|--------|--------|
| [`资源注册表/`](wiki/资源注册表/) | `Registry` | 资源、入口、环境、负责人、依赖、告警。不存凭证 |
| [`系统与架构/`](wiki/系统与架构/) | `Architecture` | 系统说明、拓扑、请求/数据链路 |
| [`操作手册/`](wiki/操作手册/) | `Runbook` / `Configuration` | 标准操作或配置说明 |
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

| 阶段 | 做什么 |
|------|--------|
| **Phase 0（当前）** | 框架、模板、schema、Skill、校验脚本、少量示例页 |
| **Phase 1** | 按痛点补操作手册、故障排查、资源注册表 |
| **Phase 2** | 内网约 80 篇落入 11 个目录、打 domain、互相链接 |
| **Phase 3** | 补齐系统与架构、技能地图、新人上手、自动化脚本 |
| **Phase 4（可选）** | Obsidian / MkDocs；再加本地搜索 |
