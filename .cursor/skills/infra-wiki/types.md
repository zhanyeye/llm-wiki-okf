# 选 type 与目录

同一内容只放一个目录，其它地方用链接。

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

文件名短 kebab 英文；中文只在 `title`。模板：`templates/<type 小写>.md`（如 `runbook.md`）。
