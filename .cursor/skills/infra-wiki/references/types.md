# 选 type、目录与 frontmatter

同一内容只放一个目录，其它地方用链接。占位符用 `<cluster>`、`<namespace>`、`<path>`，不要编造内网主机名或密钥。

## 命名与语言

| 位置 | 语言 |
|------|------|
| 分组目录名 | **中文**（与人读名称相同，见下表） |
| 文件名 | **中文**（可夹专名） |
| frontmatter `title` / `description` | **中文** |
| 分组 index 链接文字 | 该页中文 `title`（或分组人读名称） |
| 正文章节 | 下表固定 **中文** `##` 标题 |

页面标题只在 `title`。正文从该 type 的固定 `##` 开始；不要再套一层英文 H1。不要把英文来源标题直接当文件名或 `title`。若必须写 H1，须与 `title` 相同且为中文。

## type / 目录 / 何时选 / 固定标题

| type | 目录 | 何时选 | 固定标题（按序，勿改名） |
|------|------|--------|--------------------------|
| `Registry` | `wiki/资源注册表/` | 入口、负责人、告警、东西在哪 | 资源；环境；入口；负责人；依赖；告警；凭证怎么申请 |
| `Architecture` | `wiki/系统与架构/` | 系统职责、拓扑、数据流 | 职责与边界；拓扑 / 请求路径 / 数据流；依赖；相关文档 |
| `Runbook` | `wiki/操作手册/` | 可重复变更/部署/扩缩容/回滚、改配置，或说明 `script/` 里脚本怎么跑 | 触发条件；何时用 / 何时不用；前置检查；步骤；验证；回滚；相关系统 |
| `Playbook` | `wiki/故障排查/` | 按症状排查、止损、升级（场景预案） | 症状；影响；排查 / 止损路径；常见根因；升级条件；相关文档 |
| `Incident` | `wiki/案例与复盘/` | 就这一次故障/变更/演练 | 时间线；根因；修复；行动项 |
| `Decision` | `wiki/架构决策记录/` | 选型、放弃项、长期前提 | 背景；决策与放弃项；影响与约束；落地手册 |
| `FAQ` | `wiki/常见问题/` | 短问答、报错释义 | 问题；答案 |
| `Onboarding` | `wiki/新人上手/` | 接手清单、首周任务、能力与学习路径 | 权限申请；第 1 周清单；必读 |

- 保留名：`wiki/index.md`、`wiki/log.md`（不加 `type`）。`wiki/index.md` 可有 `okf_version: "0.2"`。仓根 `index.md` 是仓地图，不是知识 TOC。写法见 [index-log.md](index-log.md)。
- 概念页必须放在上表对应分组，不要写在仓库根或 `wiki/` 根。
- 每个概念 `.md` 必须有可解析 YAML frontmatter，且含非空 `type`，与上表一致。
- 链接：跨目录用相对 wiki 根的路径 `[标题](/操作手册/页.md)`（不要 `/wiki/...`）；同目录 index 条目用 `./页.md`。
- `sources`：公司 wiki 用原始 URL；工单/纪要等用仓内路径 `raw/...`。正文须自洽；查询不读 raw。
- 断链允许暂时存在（尚未写的知识）；lint 会警告。
- `Registry` 不写密码、token、密钥；只写申请途径和找谁。
- 不要把 `.py` 正文塞进 wiki；脚本用法写 `Runbook`，可执行文件在 `script/`。
- 不再单开 `Policy` / `Curriculum` / `Automation`：必须/禁止写进相关 Architecture「职责与边界」或 Runbook「何时用 / 何时不用」（规范页多了再加 `wiki/规范与约束/`）；能力项写进 Onboarding「必读」。

`domain`：`landscape` | `images` | `k8s` | `cicd` | `network` | `database` | `storage` | `middleware` | `troubleshooting`。

## Frontmatter

```yaml
---
type: Runbook
title: 示例操作手册
description: 一句话说明适用场景与结果。
domain: storage
tags: [oncall]
status: draft
owner: infra
scope: [prod]
services: []
generated: { by: human:name-or-agent/model, at: 2026-08-21T00:00:00Z }
verified: { by: human:name, at: 2026-08-21T00:00:00Z }
stale_after: 2027-02-17
sources:
  - resource: https://wiki.example.com/pages/viewpage.action?pageId=12001
---
```

- `sources` 只做溯源，不要写「去 raw 里看步骤」。
  - 公司 wiki：只写原始 wiki URL（可多条）。禁止写 `raw/wiki/archive/...`。
  - 工单 / 纪要等：仓内路径 `raw/tickets/...`。
- **图片（wiki 导出）**：鉴权图链禁止写进正文。有用的图从 `raw/wiki/archive/<docKey>/images/` 拷到知识页旁目录，正文用相对路径引用（如 `![](./页名/图.png)`）。知识页须离线可读。
- Actor：`human:<id>` / `agent/<model>` / `process:<name>`。人工确认必须用 `human:`。
- 新页用 `status: draft`；过目后改 `stable`。缺省视为 `stable`。
- `stale_after` 默认生成日后 180 天。
- 无 `verified` ⇒ unverified。不要假装已人工确认。
- 允许额外 key；不要删除你不认识的字段。

## 正文

命令放代码块。按上表该 type 的固定标题写（`##`，按序，勿改名）。
