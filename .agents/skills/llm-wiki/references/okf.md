# OKF Profile（本仓）

本仓 wiki/ 采用 [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 子集。分组目录以 [`wiki/index.md`](../../../../wiki/index.md) 为准；下表是当前默认映射，增删分组时同步改此表与 wiki/index.md。

占位符用 `<cluster>`、`<namespace>`、`<path>`，不要编造内网主机名或密钥。

## 分层模型

知识按依赖方向分三层，不按来源文档分层：

1. **L0 Atomic**：内部概念、组件、平台、规则与能力。回答“它是什么、公司如何使用、有哪些稳定约束”。
2. **L1 Registry**：稳定、可独立定位和运维的真实资产或部署实例。回答“哪一套、在哪、谁负责、入口和告警是什么”。
3. **L2 Operational**：Runbook、Playbook、FAQ、Decision、Architecture、Incident、Onboarding。回答“怎么做、怎么查、为什么、如何学习”，并引用 L0/L1。

一页 Atomic 对应一个稳定实体或概念；页内 `##`/`###` 对应可复用知识单元，只有需要被精确复用的稳定事实才加 `^block-id`。不要一条句子建一页，也不要把一篇来源机械变成一页。

## 命名与语言

| 位置 | 语言 |
|------|------|
| 分组目录名 | **中文** |
| 文件名 | **中文**（可夹专名） |
| frontmatter `title` / `description` | **中文** |
| 分组 index 链接文字 | 该页中文 `title` |
| 正文章节 | 下表固定 **中文** `##` 标题 |

页面标题只在 `title`。正文从该 type 的固定 `##` 开始；不要再套一层英文 H1。

## type / 目录 / 固定标题

| type | 目录 | 何时选 | 固定标题（按序，勿改名） |
|------|------|--------|--------------------------|
| `Atomic` | `wiki/原子知识/` | 内部概念、组件、平台、规则、能力 | 定义；职责与边界；公司内使用方式；稳定约束；关系 |
| `Registry` | `wiki/资源注册表/`（允许按资产种类建子目录） | 稳定资产、部署实例、入口、负责人、告警 | 资产；位置与环境；入口；负责人；依赖；观测与告警；生命周期；凭证怎么申请 |
| `Architecture` | `wiki/系统与架构/` | 系统职责、拓扑、数据流 | 职责与边界；拓扑 / 请求路径 / 数据流；依赖；相关文档 |
| `Runbook` | `wiki/操作手册/` | 可重复变更/部署/扩缩容/回滚、改配置，或说明 `script/` 里脚本怎么跑 | 触发条件；何时用 / 何时不用；前置检查；步骤；验证；回滚；相关系统 |
| `Playbook` | `wiki/故障排查/` | 按症状排查、止损、升级（场景预案） | 症状；影响；排查 / 止损路径；常见根因；升级条件；相关文档 |
| `Incident` | `wiki/案例与复盘/` | 就这一次故障/变更/演练 | 时间线；根因；修复；行动项 |
| `Decision` | `wiki/架构决策记录/` | 选型、放弃项、长期前提 | 背景；决策与放弃项；影响与约束；落地手册 |
| `FAQ` | `wiki/常见问题/` | 短问答、报错释义 | 问题；答案 |
| `Onboarding` | `wiki/新人上手/` | 接手清单、首周任务、学习路径 | 权限申请；第 1 周清单；必读 |

- 保留项：`wiki/index.md`、`wiki/log.md`（不加 `type`），以及 `wiki/_meta/ingest/*.yaml` 编译清单（不属于知识正文、不进导航）。`wiki/index.md` 可有 `okf_version: "0.2"`。
- 概念页必须放在上表对应分组，不要写在仓库根或 `wiki/` 根。
- 每个概念 `.md` 必须有可解析 YAML frontmatter，且含非空 `type`。
- `Atomic` 的 `kind` 必须是 `concept`、`component`、`platform`、`policy`、`capability` 之一。
- `Registry` 的 `asset_kind` 必填；至少支持 `cluster`、`namespace`、`application`、`database`、`middleware`、`domain`、`certificate`、`bucket`、`dashboard`、`alert`、`network`、`storage`。
- Registry 只登记稳定运维对象。Pod、临时 IP、一次性排查主机等短生命周期对象不入表。
- `Registry` 不写密码、token、密钥；只写申请途径和找谁。
- 不要把 `.py` 正文塞进 wiki；脚本用法写 `Runbook`，可执行文件在 `script/`。

### 检索标签：`domain` + `tags`

| 字段 | 用途 | 写法 |
|------|------|------|
| `domain` | 固定业务/技术大类 | 只从枚举选：`landscape` \| `os` \| `images` \| `platform` \| `k8s` \| `cicd` \| `network` \| `database` \| `storage` \| `middleware` \| `observability` \| `troubleshooting` |
| `tags` | 其余可搜标签 | 自由列表：场景、专名、服务/系统名、别名、报错码、症状词（如 `oncall`、`NFS-prod`、`支付网关`、`503`、`上传失败`） |

面向查询编写：

- `title` 写人会查找的主题；`description` 同时说明适用场景/症状与页面能解决什么。
- `tags` 补正文主题的中文/英文名、产品别名或缩写、稳定的错误码/报错短语、常见症状与操作动词。
- 只写来源支持且对召回有区分度的词；不要罗列整句问法、通用虚词、未在来源中确认的内网别名，也不要重复 `domain`。
- 标签不能替代正文。查询会同时搜 frontmatter 与正文全文（见 [query.md](../query.md)）。

## Frontmatter

```yaml
---
type: Runbook
id: runbook:storage:disk-manager
layer: operational
title: 示例操作手册
description: 一句话说明适用场景与结果。
domain: storage
tags: [oncall, NFS-prod]
status: draft
generated:
  by: agent/cursor
  at: 2026-08-26T04:00:00Z
verified:
  by: human:reviewer
  at: 2026-08-26T06:00:00Z
stale_after: 2027-02-22T00:00:00Z
sources:
  - https://wiki.example.com/pages/viewpage.action?pageId=12001
  - raw/tickets/disk-full.md
automation:
  ready: true
  script_ref: script/disk-manager/disk-manager.sh
  params:
    - name: TARGET_DIRS
      type: string
      default: "/data"
      required: true
      description: 目标目录列表，冒号分隔
    - name: FILE_SIZE
      type: string
      default: "1G"
      required: false
  exit_codes:
    0: 成功
    1: 参数错误
---
```

### 字段说明

| 字段 | 要求 |
|------|------|
| `type` | **必填**（OKF 唯一 always-required） |
| `id` | **必填**；仓内唯一稳定 ID，推荐 `<type>:<domain>:<slug>`，改文件名时不改 ID |
| `layer` | **必填**；`atomic` \| `registry` \| `operational`，必须与 type 一致 |
| `title` | 推荐；中文 |
| `description` | 推荐；用于 index 摘要，并说明适用场景/症状与页面能解决什么 |
| `domain` | 推荐；固定枚举大类（见上） |
| `tags` | 推荐；场景、专名、服务/系统名、别名、报错码、症状词（见上） |
| `status` | `draft` \| `stable` \| `deprecated`；新页用 `draft` |
| `owner` | 可选；本页文档维护人。系统/资源负责人写在 `Registry` 正文「负责人」 |
| `generated` | `{ by, at }`；`by` 用 `human:<id>` / `agent/<model>` / `process:<name>` |
| `verified` | 可选；人工确认须 `human:`；Agent 不替人写 |
| `stale_after` | ISO 8601；默认生成日后 180 天 |
| `sources` | 溯源；见下 |
| `automation` | 可选；自动化元数据（见下） |
| `kind` | Atomic 必填；概念种类 |
| `asset_kind` | Registry 必填；资产种类 |
| `aliases` | 可选；来源明确的中文名、英文名、缩写，不臆造 |
| `technology` | Registry 必填；至少一个指向 Atomic 标题或块的 wikilink |
| `depends_on` | 可选；当前页依赖的 Atomic/Registry wikilink 列表 |
| `operates_on` | Runbook/Playbook 可选；所操作资产或概念的 wikilink 列表 |
| `answers_about` | FAQ 可选；所回答主题的 wikilink列表 |
| `decides_for` | Decision 可选；决策约束对象的 wikilink 列表 |
| `source_of_truth` | Registry 可选；权威系统或资料来源 |
| `external_id` / `sync_mode` | Registry 可选；外部资产系统 ID 与 `manual`/`generated` |

### Registry frontmatter

Registry 使用 Markdown + frontmatter 作为唯一事实记录，index/Obsidian Base 只生成视图，不复制资产数据。原始设计中的组件 `type` 政名为 `asset_kind`，因为 `type` 已保留给 OKF。

```yaml
---
type: Registry
id: asset:database:clickhouse-prod-01
layer: registry
title: ClickHouse 生产实例 01
description: ClickHouse 生产实例的位置、入口、依赖、观测与运维链接。
domain: database
asset_kind: database
name: clickhouse-prod-01
environment: prod
owner: infra-team
technology:
  - "[[ClickHouse#定义]]"
depends_on:
  - "[[S3 备份桶]]"
runbooks:
  - "[[ClickHouse 扩容]]"
entries:
  console: https://clickhouse.example.invalid
  dashboard: https://grafana.example.invalid
source_of_truth: demo
sync_mode: manual
status: draft
sources:
  - raw/examples/registry.md
---
```

`used_by` 等反向关系优先从 backlinks 推导；只有来源直接陈述且反向对象尚无页面时才暂记。按 `asset_kind` 至少满足：

- `database`：环境、负责人、入口、备份/保留策略、监控或明确待补。
- `domain`：DNS、证书、请求路径或明确待补。
- `certificate`：覆盖域名、到期时间、续期 Runbook 或明确待补。
- `cluster`：环境、入口、告警、变更方式或明确待补。
- 其它资产：环境/位置、负责人、入口、依赖、观测、生命周期；不适用项写“不适用”，未知写“来源未写”。

### automation 块

标记本页是否可由 Agent 自动执行，以及脚本参数与退出码。

| 字段 | 类型 | 说明 |
|------|------|------|
| `ready` | `true` \| `partial` \| `false` | `true`=有独立可运行脚本；`partial`=有结构化命令但无独立脚本；`false`（默认）=纯文档 |
| `script_ref` | 仓内路径 | 指向 `script/<name>/<file>`；`ready: true` 时必填 |
| `params` | 列表 | 脚本/命令参数：`{ name, type, default, required, description }` |
| `exit_codes` | 映射 | 退出码含义：`{ 0: "成功", 1: "参数错误" }` |

**判定 ready 级别**：

| 级别 | 条件 | 示例 |
|------|------|------|
| `true` | 正文含独立可运行的完整脚本（≥5 行、可保存为 .sh/.py 直接执行）→ 已提取到 `script/` | disk-manager.sh、bisheng-install |
| `partial` | 有多步骤命令序列但不适合提取为独立脚本（需人工判断/交互） | Etcd 手动恢复、harbor GC 流程 |
| `false` | 仅单条验证命令、纯概念文档 | 架构页、Registry 页 |

**正文与脚本的关系**：

- 正文**完整保留**脚本内容（离线可用）
- `script_ref` 提供可直接执行的脚本路径（自动化入口）
- 两者内容相同，`script_ref` 是正文中脚本的提取版本（含 param 替换、exit 处理等增强）
- Agent 优先用 `script_ref` 执行；人读正文

### sources

- 字符串数组；每个元素是一个 URL 或仓内相对路径
- 公司 wiki：**只写原始 wiki URL**。禁止写 `raw/wiki/archive/...`。
- 本地 raw：写仓内相对路径（如 `raw/tickets/disk-full.md`）。
- Obsidian 会自动将 HTTP 链接渲染为可点击链接，方便追溯。
- `sources` 只做溯源；正文须自洽，查询默认无需读 raw（`wiki/` 不足时按 query.md 回退搜 raw 并标注「⚠️ 未编译」）。

### 图片（统一 attachments/）

知识页图片**一律**放在该 `.md` **所在目录**下的 `attachments/`：

```
wiki/操作手册/磁盘满处理.md
wiki/操作手册/attachments/磁盘满-dashboard.png
```

正文引用：

```markdown
![](./attachments/磁盘满-dashboard.png)
```

| 规则 | 说明 |
|------|------|
| 路径 | `./attachments/<文件名>`；禁止 `./页名/`、`./images/`、页旁随意子目录 |
| 来源 | 公司 wiki：从 `raw/wiki/archive/<docKey>/images/` **拷贝**到目标 `attachments/`（raw 仍用 `images/`） |
| 命名 | 尽量保留原名；同目录重名时加页名前缀（如 `磁盘满-xxx.png`） |
| 鉴权 | 禁止把鉴权 URL 写进 `wiki/` 正文 |
| 空目录 | 无图则不要建空 `attachments/` |
| 离线 | 知识页须离线可读 |

## 链接规则

| 场景 | 规则 |
|------|------|
| 普通导航/来源引用 | 同目录 `./页名.md`；跨目录 `/wiki/操作手册/页.md` |
| 语义关系、标题级引用 | `[[页名#标题]]`；重名时用 `[[wiki/分组/页名#标题]]` |
| 关键事实块引用 | `[[页名#^block-id]]`；块 ID 只用小写 ASCII、数字和连字符 |
| 嵌入下层内容 | `![[页名#标题]]` 或 `![[页名#^block-id]]`，仅在确需展示原文时使用 |
| 对话输出引用 | 仓根相对路径 `wiki/操作手册/页.md` |
| 禁止 | 不带 `/wiki/` 前缀的 `/操作手册/页.md` 形式；指向不存在 raw 的「去 raw 看步骤」 |

链接原则：

- 上层页用普通链接或嵌入引用下层定义/约束，不复制改写同一事实。
- 标题重命名前先查 backlinks 并同步修改引用；块 ID 一经被引用不得随意改变。
- frontmatter 中的关系值必须写为带引号的 wikilink，如 `- "[[ClickHouse#定义]]"`。
- 关系字段只维护有来源的有向边，反向关系由 backlinks/查询派生，避免双写漂移。

### 交叉引用（按内容关联，禁止瞎链）

交叉链接很重要，但**只在内容上确有关系时**才写：

| 可以链 | 不可以链 |
|--------|----------|
| 正文提到的系统 / Registry / 上游依赖 | 只因「同一批入库」或同一次对话 |
| 同一故障链、同一手册步骤互相引用 | 主题无关、仅同 domain / 同分组 |
| 来源正文里已有的外链对应仓内页 | 为「相关文档」凑条数而互链 |
| **同批**多条来源：内容确有依赖/互补/上下游关系 | 无实质关系却因同批互相塞进「相关文档」 |

判定顺序：先看本条正文与实体是否指向对方主题；有 → 可链（含本批刚写/将写的页）；无 → 不链。没有明确关系 → 省略该节链接，或只写「相关文档：无」。

## 正文

命令放代码块。按 type 固定 `##` 标题写（见上表）。

### Agent 可解析标记

正文中的自动化相关段落可用 HTML 注释标记，供 Agent 快速定位：

```markdown
<!-- okf:auto:script -->
脚本的完整内容（与 script_ref 指向的文件一致）
<!-- /okf:auto:script -->

<!-- okf:auto:verify -->
验证步骤的命令
<!-- /okf:auto:verify -->

<!-- okf:auto:rollback -->
回滚步骤的命令
<!-- /okf:auto:rollback -->
```

- 不是必须有标记；没有标记时 Agent 按固定标题（步骤/验证/回滚）定位。
- 有标记时 Agent 优先用标记区间提取内容。
- 标记内不放 `script_ref`；`script_ref` 只在 frontmatter。
