# OKF Profile（本仓）

本仓 wiki/ 采用 [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 子集。分组目录以 [`wiki/index.md`](../../../../wiki/index.md) 为准；下表是当前默认映射，增删分组时同步改此表与 wiki/index.md。

占位符用 `<cluster>`、`<namespace>`、`<path>`，不要编造内网主机名或密钥。

## 分层模型

知识按依赖方向分三层，**不按来源文档分层**，禁止把一篇来源平铺成一页：

1. **L0 基础知识**（`type: Foundation`，目录 `wiki/基础知识/<能力域>/`）：内网特有概念、平台与规则。回答“它是什么、公司如何使用、有哪些稳定约束”。不写某套生产实例的 IP/入口。开源组件通用原理不进本层，除非是公司定制用法。
2. **L1 资源目录**：稳定、可独立定位和运维的真实部署实例。回答“哪一套、在哪、谁负责、入口和告警是什么”。`technology` 必须 `[[双链]]` 到 L0。
3. **运维与设计**：Runbook、FAQ（含短问答与按症状排查）、ADR、Incident。回答“怎么做、怎么查、为什么”。引用 L0/L1，也可以互相双链；不复制下层定义。跨实体拓扑/职责说明写入相关基础知识页或 ADR，不单开「系统与架构」分组。

一页 Foundation 对应一个内部概念或平台（如黄绿区、ROMA、EulerOS）；页内 `##`/`###` 对应可复用知识单元，只有需要被精确复用的稳定事实才加 `^block-id`。不要一条句子建一页，也不要把一篇来源机械变成一页。

L0 能力域（子目录，增删时同步 `wiki/index.md`）：`OS镜像`、`镜像制作`、`构建资源管理`、`网络管理`、`应用服务`、`资源调度`。

L1 资产类（子目录）：`集群`、`数据库`、`存储`、`中间件`、`可观测`。样例库还可使用 `网络`、`域名`、`证书`。

## 命名与语言


| 位置                                  | 语言                  |
| ----------------------------------- | ------------------- |
| 分组目录名                               | **中文**              |
| 文件名                                 | **中文**（可夹专名）        |
| frontmatter `title` / `description` | **中文**              |
| 分组 index 链接文字                       | 该页中文 `title`        |
| 正文章节                                | 下表固定 **中文** `##` 标题 |


页面标题只在 `title`。正文从该 type 的固定 `##` 开始；不要再套一层英文 H1。

## type / 目录 / 固定标题


| type         | 目录                      | 何时选                                      | 固定标题（按序，勿改名）                                                      |
| ------------ | ----------------------- | ---------------------------------------- | ----------------------------------------------------------------- |
| `Foundation` | `wiki/基础知识/`（按能力域分子目录）  | 内网特有概念、平台、规则                             | 定义；职责与边界；公司内使用方式；稳定约束；关系                                          |
| `Registry`   | `wiki/资源目录/`（按资产种类分子目录） | 稳定资产、部署实例、入口、负责人、告警                      | 资产；位置与环境；入口；负责人；依赖；观测与告警；生命周期；凭证怎么申请                              |
| `Runbook`    | `wiki/操作手册/`            | 可重复变更/部署/扩缩容/回滚、改配置，或说明 `script/` 里脚本怎么跑 | 触发条件；何时用 / 何时不用；前置检查；步骤；验证；回滚；相关系统                                |
| `Incident`   | `wiki/案例与复盘/`           | 就这一次故障/变更/演练                             | 时间线；根因；修复；行动项                                                     |
| `ADR`   | `wiki/架构决策记录/`          | 选型、放弃项、长期前提                              | 背景；决策与放弃项；影响与约束；落地手册                                              |
| `FAQ`        | `wiki/常见问题/`            | 短问答、报错释义、按症状排查与止损（值班入口）                  | 短页：问题；答案。长页（排查）：症状；影响；排查 / 止损路径；常见根因；升级条件；相关文档（二选一形态，勿两套标题混用当全必填） |


- 保留项：`wiki/index.md`、`wiki/log.md`（不加 `type`），以及 `wiki/_meta/ingest/*.yaml` 编译清单（不属于知识正文、不进导航）。`wiki/index.md` 可有 `okf_version: "0.2"`。
- 概念页必须放在上表对应分组，不要写在仓库根或 `wiki/` 根。
- 每个概念 `.md` 必须有可解析 YAML frontmatter，且含非空 `type`。
- `Foundation` 的 `kind` 必须是 `concept`、`component`、`platform`、`policy`、`capability` 之一。
- `Registry` 的 `asset_kind` 必填；正式库子目录对应：`cluster`→集群、`database`→数据库、`storage`→存储、`middleware`→中间件、`observability`→可观测。亦支持 `namespace`、`application`、`domain`、`certificate`、`bucket`、`dashboard`、`alert`、`network`。
- Registry 只登记稳定运维对象。Pod、临时 IP、一次性排查主机等短生命周期对象不入表。
- `Registry` 不写密码、token、密钥；只写申请途径和找谁。
- 不要把 `.py` 正文塞进 wiki；脚本用法写 `Runbook`，可执行文件在 `script/`。

### 检索标签：`tags`

| 字段 | 用途 | 写法 |
|------|------|------|
| `tags` | 可搜标签 | 自由列表：场景、专名、服务/系统名、别名、报错码、症状词（如 `NFS`、`支付网关`、`503`、`上传失败`） |

面向查询编写：

- `title` 写人会查找的主题；`description` 同时说明适用场景与页面能解决什么。
- `tags` 补正文主题的中文/英文名、产品别名或缩写、稳定的错误码/报错短语、常见症状与操作动词。
- 只写来源支持且对召回有区分度的词；不要罗列整句问法、通用虚词、未在来源中确认的内网别名。
- 标签不能替代正文。查询会同时搜 frontmatter 与正文全文（见 [SKILL.md](../SKILL.md) §Query）。

## Frontmatter

```yaml
---
type: Runbook
title: 示例操作手册
description: 一句话说明适用场景与结果。
tags: [NFS]
status: draft
owner: 张三
updated: 2026-09-03
sources:
  - https://wiki.example.com/WIKI…
---
```

### 字段说明

| 字段 | 要求 |
|------|------|
| `type` | **必填**：`Foundation` \| `Registry` \| `Runbook` \| `FAQ` \| `ADR` \| `Incident` |
| `title` | 推荐；中文 |
| `description` | 推荐；index 摘要 + 适用场景 |
| `tags` | 推荐；检索用（见上） |
| `status` | `draft` \| `stable` \| `deprecated`；新页用 `draft` |
| `owner` | 推荐；本页维护人 |
| `updated` | 推荐；本页最近更新日期（`YYYY-MM-DD`） |
| `sources` | 溯源 URL 或 `raw/...` 路径（见下） |

按 type 另加：`Foundation` 要 `kind`；`Registry` 要 `asset_kind` + `technology`（双链基础知识）。`verified`（人工确认）、`automation` 按需，见下文。

### Registry frontmatter

Registry 用 Markdown + frontmatter 记资产事实；`asset_kind` 区分资产种类（`type` 已留给 OKF）。

```yaml
---
type: Registry
title: ClickHouse 生产实例 01
description: 位置、入口、依赖与观测入口。
asset_kind: database
technology:
  - "[[ClickHouse#定义]]"
status: draft
owner: 李四
updated: 2026-09-03
sources:
  - raw/examples/registry.md
---
```

环境、负责人、入口等写在正文固定标题下。`technology` 必须双链到基础知识页。

### automation（可选）

仅当 Runbook 抽了可执行脚本到 `script/` 时才写：`ready`、`script_ref`；参数与退出码按需。默认不写。

### sources

- 字符串数组；每个元素是一个 URL 或仓内相对路径
- 公司 wiki：**只写原始 wiki URL**。禁止写 `raw/wiki/archive/...`。
- 本地 raw：写仓内相对路径（如 `raw/tickets/disk-full.md`）。
- Obsidian 会自动将 HTTP 链接渲染为可点击链接，方便追溯。
- `sources` 只做溯源；正文须自洽，查询默认无需读 raw（`wiki/` 不足时按 SKILL.md §Query 回退搜 raw 并标注「⚠️ 未编译」）。

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


| 规则  | 说明                                                                                       |
| --- | ---------------------------------------------------------------------------------------- |
| 路径  | `./attachments/<文件名>`；禁止 `./页名/`、`./images/`、页旁随意子目录                                     |
| 来源  | 公司 wiki：从 `raw/wiki/archive/<docKey>/images/` **拷贝**到目标 `attachments/`（raw 仍用 `images/`） |
| 命名  | 尽量保留原名；同目录重名时加页名前缀（如 `磁盘满-xxx.png`）                                                      |
| 鉴权  | 禁止把鉴权 URL 写进 `wiki/` 正文                                                                  |
| 空目录 | 无图则不要建空 `attachments/`                                                                   |
| 离线  | 知识页须离线可读                                                                                 |


## 链接规则

语义关系**必须**用 Obsidian 双链（领导要求知识相关联，禁止平铺后互不引用）。


| 场景         | 规则                                                                              |
| ---------- | ------------------------------------------------------------------------------- |
| 普通导航/来源引用  | 同目录 `./页名.md`；跨目录 `/wiki/操作手册/页.md`                                             |
| 语义关系、标题级引用 | `[[页名]]` 或 `[[页名#标题]]`；重名时用 `[[wiki/分组/页名#标题]]`                                 |
| 关键事实块引用    | `[[页名#^block-id]]`；块 ID 只用小写 ASCII、数字和连字符                                       |
| 嵌入下层内容     | `![[页名#标题]]` 或 `![[页名#^block-id]]`，仅在确需展示原文时使用                                  |
| 对话输出引用     | 仓根相对路径 `wiki/操作手册/页.md`                                                         |
| 禁止         | 不带 `/wiki/` 前缀的 `/操作手册/页.md` 形式；指向不存在 raw 的「去 raw 看步骤」；L0 基础知识页反向依赖 Runbook/FAQ |


链接原则：

- 上层页用双链或嵌入引用下层定义/约束，不复制改写同一事实。
- 标题重命名前先查 backlinks 并同步修改引用；块 ID 一经被引用不得随意改变。
- frontmatter 中的关系值必须写为带引号的 wikilink，如 `- "[[ClickHouse#定义]]"`。
- 关系字段只维护有来源的有向边，反向关系由 backlinks/查询派生，避免双写漂移。
- Registry 的 `technology`、Runbook 的 `operates_on`、FAQ 的 `answers_about`（排查长页也可用 `operates_on`）、ADR 的 `decides_for` 在适用时必须填写双链。

### 交叉引用（按内容关联，禁止瞎链）

交叉链接很重要，但**只在内容上确有关系时**才写：


| 可以链                        | 不可以链                 |
| -------------------------- | -------------------- |
| 正文提到的系统 / Registry / 上游依赖  | 只因「同一批入库」或同一次对话      |
| 同一故障链、同一手册步骤互相引用 | 主题无关、仅同目录或同批 |
| 来源正文里已有的外链对应仓内页            | 为「相关文档」凑条数而互链        |
| **同批**多条来源：内容确有依赖/互补/上下游关系 | 无实质关系却因同批互相塞进「相关文档」  |


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

