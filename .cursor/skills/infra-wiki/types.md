# 选 type、目录与 frontmatter

同一内容只放一个目录，其它地方用链接。文件名短 kebab 英文；中文只在 `title`。占位符用 `<cluster>`、`<namespace>`、`<path>`，不要编造内网主机名或密钥。

## 目录与 type

| type | 目录 | 放什么 |
|------|------|--------|
| `Registry` | `wiki/资源注册表/` | 资源、入口、环境、负责人、依赖、告警。不存凭证，只写申请途径和找谁 |
| `Architecture` | `wiki/系统与架构/` | 系统说明、拓扑、请求/数据链路、依赖关系 |
| `Runbook` | `wiki/操作手册/` | 申请、部署、变更、扩缩容、回滚；网关、DNS、证书、防火墙等配置说明 |
| `Playbook` | `wiki/故障排查/` | 按症状的排查、止损、升级路径 |
| `Decision` | `wiki/架构决策记录/` | 选型背景、方案权衡、影响与约束 |
| `FAQ` | `wiki/常见问题/` | 短问答、工具速查、报错释义 |
| `Policy` | `wiki/规范与约束/` | 命名、权限、变更、安全、CI 适配规范 |
| `Incident` | `wiki/案例与复盘/` | 故障、变更、演练的复盘与行动项 |
| `Curriculum` | `wiki/技能地图/` | 能力范围、学习路径、技能矩阵 |
| `Onboarding` | `wiki/新人上手/` | 接手清单、权限申请、首周任务 |
| `Automation` | `wiki/自动化脚本/` | 脚本说明、参数、权限、风险；可执行文件在 `script/`，不要把 `.py` 塞进 wiki |

按场景选 type：

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

- OKF 知识图根是 `wiki/`。保留名只有 `wiki/index.md` 和 `wiki/log.md`，不加 `type`。`wiki/index.md` 可有 `okf_version: "0.2"`。仓根 `index.md` 是仓地图，不是知识 TOC。写法见 [index-log.md](index-log.md)。
- 概念页必须放在上表对应 `wiki/` 分组，不要写在仓库根或 `wiki/` 根。
- 每个概念 `.md` 必须有可解析的 YAML frontmatter，且含非空 `type`，与上表一致。
- 链接：跨目录用相对 wiki 根的路径 `[MinIO](/系统与架构/minio.md)`（不要 `/wiki/...`）；同目录 index 条目用 `./file.md`。
- `sources` 用仓内路径，例如 `raw/tickets/foo.md`。正文须自洽；查询不读 raw。
- 断链允许暂时存在（尚未写的知识）；lint 会警告。

`domain` 取值：`landscape` | `images` | `k8s` | `cicd` | `network` | `database` | `storage` | `middleware` | `troubleshooting`。

## Frontmatter

```yaml
---
type: Runbook
title: 人类可读标题
description: 一句话摘要。
domain: storage
tags: [oncall, disk]
status: draft
owner: infra-storage
scope: [prod]
services: [minio]
generated: { by: human:name-or-agent/model, at: 2026-08-21T00:00:00Z }
verified: { by: human:name, at: 2026-08-21T00:00:00Z }
stale_after: 2027-02-17
sources:
  - resource: raw/example.md
---
```

- `sources`：仓内相对路径 `raw/...`；只做溯源，不要写「去 raw 里看步骤」。
- Actor：`human:<id>` / `<agent>/<model>` / `process:<name>`。人工确认必须用 `human:`。
- 新页用 `status: draft`；过目后改 `stable`。缺省视为 `stable`。
- `stale_after` 默认生成日后 180 天。
- 无 `verified` ⇒ unverified。不要假装已人工确认。
- `Registry` 页不写密码、token、密钥。
- 允许额外 key；不要删除你不认识的字段。

## 固定正文标题

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
