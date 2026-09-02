# 分层知识编译流水线

本文件定义来源到知识图谱的强制编译过程。目标不是摘要或改写原文，而是保留全部有效技术知识，消除重复，并让上层知识精确引用下层事实。

## 六阶段

### 1. Extract

逐项提取，不直接写知识页：

- `entities`：名称、别名、种类、环境，以及来源中的定义位置。
- `facts`：可独立判断真假的事实、约束、版本、边界和参数。
- `assets`：稳定资源或部署实例；临时对象排除。
- `procedures`：目标、前置、步骤、验证、回滚。
- `questions`：来源明确回答的常见问题。
- `decisions`：背景、选择、备选、权衡和后续约束。
- `symptoms` / `incidents`：症状路径与一次性事件。

命令、数字、表格、错误原文保真；叙述内容提炼为自洽事实。不得丢弃限制条件、遗留项或来源中的“不确定”。

### 2. Resolve

用实体名、别名、职责和已有关系搜索 `wiki/`：

- 同一实体 → 更新已有 Atomic/Registry，不建平行页。
- 同名不同实体 → 用环境、职责或所属系统消歧，分别分配稳定 ID。
- 来源不足 → 标记 `gap`，写“来源未写/待确认”，禁止用训练数据补齐。
- Registry 的 `technology` 必须解析到 Atomic；若 Atomic 尚不存在且来源足够，先创建 Atomic。

### 3. Plan

先形成产出计划，再写文件。按知识性质分配：

- 定义、职责、公司内用法、稳定规则 → Atomic。
- 稳定资产、实例、入口、负责人、告警 → Registry。
- 可重复任务 → Runbook；按症状排查 → Playbook。
- 短问答 → FAQ；决策与权衡 → Decision。
- 跨实体拓扑/数据流 → Architecture；一次性事件 → Incident。

一篇来源可以更新多页，多篇来源也可汇入同一页。不得规定“一个 URL 一页”或“每个来源最少几页”；原子边界由稳定实体和独立更新边界决定。

### 4. Compose

按 L0 → L1 → L2 写入：

1. 先写/更新 Atomic，并给需要复用的标题或关键事实稳定块 ID。
2. 再写 Registry；结构化字段遵循 `okf.md` 的 `asset_kind` 画像，缺失项显式标记。
3. 最后写 Runbook/FAQ/Decision 等上层页。定义与稳定约束使用标题/块引用，不复制一份近似文本。

正文必须自洽。原始来源只做追溯，不能要求读者去 raw 才能完成操作。

### 5. Link

链接必须表达明确关系：

- `technology` / `instance_of`：资产属于哪个 Atomic 技术或平台。
- `depends_on`：本实体运行依赖什么。
- `operates_on`：Runbook/Playbook 操作或排查什么。
- `answers_about`：FAQ 回答什么。
- `decides_for`：ADR 约束什么。

普通导航用 Markdown 链接；语义关系用 `[[页#标题]]`，关键事实用 `[[页#^block-id]]`。只维护有来源的有向边，反向关系由 backlinks 派生。不得因同批、同目录或同 domain 自动互链。

### 6. Validate

写 index/log 前完成：

- 每条提取项都有 `compiled`、`duplicate`、`excluded` 或 `gap` 处置。
- `compiled` 指向存在的页、标题或块；`duplicate` 指向已有事实。
- `excluded` 必须写原因；`gap` 必须写缺少什么证据。
- Registry 解析到 Atomic，并满足对应 `asset_kind` 最小画像。
- 上层页在适用时链接 Atomic/Registry，且没有复制冲突定义。
- 数字、命令、限制、遗留项与来源核对无静默丢失。
- lint 无 error；失败项修复前不得记 `ingest compiled`。

## 编译清单

每个来源在 `wiki/_meta/ingest/<source-id>.yaml` 保存一份清单，用于增量刷新、覆盖验收和人工审核；它是编译元数据，不是知识正文，不进入导航。`source-id` 优先使用公司 wiki `docKey`，其它来源使用稳定短名；冲突时追加短 hash。

```yaml
source_id: WIKI2026000000001
source: https://wiki.example.invalid/WIKI2026000000001
status: compiled
entities:
  - id: clickhouse
    target: "[[ClickHouse]]"
items:
  - id: fact-001
    kind: fact
    summary: 生产实例使用统一监控入口
    disposition: compiled
    target: "[[ClickHouse 生产实例 01#观测与告警]]"
  - id: fact-002
    kind: fact
    summary: 备份周期在来源中未说明
    disposition: gap
    reason: 缺少备份周期
outputs:
  - "[[ClickHouse]]"
  - "[[ClickHouse 生产实例 01]]"
validated_at: 2026-09-02T09:00:00Z
```

清单不得抄入密码、token、kubeconfig。刷新来源时重跑 Extract → Validate，更新同一清单；不能只把 raw 新段落追加到旧页面。

## 发布门禁

- `draft` 表示已通过机械门禁但尚未人工确认，不表示可以低质量搬运。
- 机械门禁通过后，按 `review.md` 检查原子边界、来源覆盖、关系正确性和可执行性。
- 只有人明确确认后才写 `verified.by: human:<id>` 并改为 `stable`。
