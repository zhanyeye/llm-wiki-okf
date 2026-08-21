# 基础设施知识库 Schema

本文件约束 Agent 如何维护 [`wiki/`](wiki/)。人读总览见 [`README.md`](README.md)。执行细节见 [`.cursor/skills/infra-wiki/`](.cursor/skills/infra-wiki/)。

## 权限

- [`raw/`](raw/)：**只读**。不要改、不要删。
- [`wiki/`](wiki/)：查、写、更新 `index.md` 与 `log.md`。
- 改本文件或 Skill 前先和用户确认。

`wiki/` 只写运维知识。不要把格式规范解说写进 wiki 正文。

## 目录与 type

| type | 目录 | 放什么 |
|------|------|--------|
| `Registry` | `wiki/资源注册表/` | 资源、入口、环境、负责人、依赖、告警。不存凭证，只写申请途径和找谁 |
| `Architecture` | `wiki/系统与架构/` | 系统说明、拓扑、请求/数据链路、依赖关系 |
| `Runbook` | `wiki/操作手册/` | 申请、部署、变更、扩缩容、回滚 |
| `Configuration` | `wiki/操作手册/` | 网关、DNS、证书、防火墙等配置说明 |
| `Playbook` | `wiki/故障排查/` | 按症状的排查、止损、升级路径 |
| `Decision` | `wiki/架构决策记录/` | 选型背景、方案权衡、影响与约束 |
| `FAQ` | `wiki/常见问题/` | 短问答、工具速查、报错释义 |
| `Policy` | `wiki/规范与约束/` | 命名、权限、变更、安全、CI 适配规范 |
| `Incident` | `wiki/案例与复盘/` | 故障、变更、演练的复盘与行动项 |
| `Curriculum` | `wiki/技能地图/` | 能力范围、学习路径、技能矩阵 |
| `Onboarding` | `wiki/新人上手/` | 接手清单、权限申请、首周任务 |
| `Automation` | `wiki/自动化脚本/` | 脚本说明、参数、权限、输入输出与风险 |

- wiki 根只有 `index.md` 和 `log.md`。它们是保留名，不加 `type`。根 `index.md` 可有 `okf_version: "0.2"`。写法见 [`.cursor/skills/infra-wiki/index-log.md`](.cursor/skills/infra-wiki/index-log.md)。
- 每个非保留 `.md` 必须有可解析的 YAML frontmatter，且含非空 `type`，与上表一致。
- 链接：跨目录用 bundle 绝对路径 `[MinIO](/系统与架构/minio.md)`；同目录 index 条目用 `./file.md`。
- 文件名短 kebab：`disk-full.md`。中文只在 `title`。
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
sources: []
---
```

- Actor：`human:<id>` / `<agent>/<model>` / `process:<name>`。人工确认必须用 `human:`。
- 新页用 `status: draft`；过目后改 `stable`。缺省视为 `stable`。
- `stale_after` 默认生成日后 180 天。
- 无 `verified` ⇒ unverified。不要假装已人工确认。
- `Registry` 页不写密码、token、密钥。
- 允许额外 key；不要删除你不认识的字段。

模板在 [`templates/`](templates/)，按 type 各一份。正文用模板里的固定标题。占位符用 `<cluster>`、`<namespace>`、`<path>`；不要编造看起来真实的内网主机名或密钥。

## 查询

1. 读 [`wiki/index.md`](wiki/index.md)。
2. 现象不明时读 [`wiki/故障排查/index.md`](wiki/故障排查/index.md)。
3. 已知系统读 `wiki/系统与架构/<name>.md`；找入口/负责人读 `wiki/资源注册表/`。
4. 打开 2–5 篇作答，引用路径。
5. 仍不够再搜索 `tags` / `domain` / `services` / `title`。
6. **禁止**用训练数据填补未写入 wiki 的集群名、地址、凭证、步骤。缺失就说缺失，并建议入库。

有价值的综合结论应回写成新页。

## 入库

1. 阅读 `raw/` 中对应材料（若有）；不要修改 raw。
2. 选 type 与目录；套对应模板。
3. 一篇来源可以改多页。保持交叉引用一致。
4. 按 Skill [`index-log.md`](.cursor/skills/infra-wiki/index-log.md) 更新所在目录 `index.md`、必要时根 `index.md` 与 `故障排查/index.md`。
5. 在 [`wiki/log.md`](wiki/log.md) 当日 `## YYYY-MM-DD` 节顶部追加一条：`* **Creation**:` 或 `* **Update**:`（ASCII 冒号，一篇一链，最新日在上）。

## 体检

1. 跑 `python scripts/okf_lint.py`。
2. 处理 error；对 warning 决定是补页、改链，还是保留尚未写的断链。
3. 再看：矛盾陈述、孤儿页、故障排查 index 仍为「待入库」但已有正文的项。

## 值班

- 入口是 [`wiki/故障排查/index.md`](wiki/故障排查/index.md)。
- 故障关闭前：更新或新建 Incident；可复用步骤写入 Runbook 或 Playbook。
- 不要把一次性命令只留在聊天窗口。

## 路线图

Phase 0 当前（框架与示例）。Phase 1 按痛点补手册/排查/注册表。Phase 2 迁约 80 篇。Phase 3 补架构、技能地图、新人上手、脚本。Phase 4 可选浏览与搜索。
