# 选 type 与目录

同一内容只放一个目录，其它地方用链接。frontmatter 见 `AGENTS.md`。文件名短 kebab 英文；中文只在 `title`。占位符用 `<cluster>`、`<namespace>`、`<path>`，不要编造内网主机名或密钥。

| 情况 | type | 目录 |
|------|------|------|
| 可重复的变更/部署/扩缩容/回滚，或改配置项、参数表、reload | `Runbook` | `wiki/操作手册/` |
| 按症状排查、止损、升级 | `Playbook` | `wiki/故障排查/` |
| 就这一次故障/变更/演练 | `Incident` | `wiki/案例与复盘/` |
| 入口、负责人、告警、东西在哪 | `Registry` | `wiki/资源注册表/` |
| 系统职责、拓扑、数据流 | `Architecture` | `wiki/系统与架构/` |
| 选型、放弃项、以后不能轻易改的前提 | `Decision` | `wiki/架构决策记录/` |
| 三五句问答、报错释义 | `FAQ` | `wiki/常见问题/` |
| 必须/禁止、门禁规范 | `Policy` | `wiki/规范与约束/` |
| 能力项、学习路径 | `Curriculum` | `wiki/技能地图/` |
| 接手清单、首周任务 | `Onboarding` | `wiki/新人上手/` |
| 脚本参数、权限、风险 | `Automation` | `wiki/自动化脚本/` |

`domain`：`landscape` `images` `k8s` `cicd` `network` `database` `storage` `middleware` `troubleshooting`。

正文用该 type 的固定 `#` 标题（按序，勿改名）。命令放代码块。`Registry` 不写密码、token、密钥。

| type | 标题 |
|------|------|
| `Runbook` | 触发条件；何时用 / 何时不用；前置检查；步骤；验证；回滚；相关系统 |
| `Playbook` | 症状；影响；排查 / 止损路径；常见根因；升级条件；相关文档 |
| `Incident` | 时间线；根因；修复；行动项 |
| `Registry` | 资源；环境；入口；负责人；依赖；告警；凭证怎么申请 |
| `Architecture` | 职责与边界；拓扑 / 请求路径 / 数据流；依赖；相关文档 |
| `Decision` | 背景；决策与放弃项；影响与约束；落地手册 |
| `FAQ` | 问题；答案 |
| `Policy` | 适用范围；必须 / 禁止；检查方式；例外 |
| `Curriculum` | 能力项 |
| `Onboarding` | 权限申请；第 1 周清单；必读 |
| `Automation` | 做什么；权限；参数；怎么跑；输入输出；风险 |
