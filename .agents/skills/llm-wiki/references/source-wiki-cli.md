# 公司 Wiki 来源（wiki_export.py + wiki-cli）

`raw/wiki/` 是来源通道，与仓根 `wiki/`（知识面）不是同一目录。

**禁止**用 WebFetch / Defuddle 抓内网 wiki。必须用 **wiki_export.py** 脚本（内部调用 wiki CLI）。

## 触发

| 用户意图 | 走 |
|----------|-----|
| 对话贴 wiki 链接并说入库 | §0–5（入库流程）|
| 「把 inbox 入库」 | §0–5（入库流程）|
| 「继续下一批 / 重试失败项」 | §0–5（入库流程）|
| 「刷新某 url」 | §0–5，该 URL 无视 `sources:` 去重 |
| **「增量刷新 / 刷新 wiki / 检查更新」** | **§增量刷新** |

人可贴对话链接，或编辑 [`raw/wiki/inbox.md`](../../../../raw/wiki/inbox.md)。`inbox.md` 是增量登记册，不是会排空的队列。

Agent 对 `raw/` **只允许**：

1. 把本对话里尚未出现在 inbox 的 URL **追加**到 `inbox.md` 末尾（精确匹配去重）；不删行、不改已有行。
2. 通过 `wiki_export.py` 写 `raw/wiki/archive/<docKey>/`（导出落盘）。

## 0. 前置检查（每会话首次入库前）

1. 检查脚本与 wiki CLI：

```bash
python tools/wiki-export/wiki_export.py check
```

   如果 check 不通过 → 停；告诉用户先安装配置；本批标 `failed` 并写 `wiki/log.md`，不要空编存档。

2. 全部 wiki CLI 交互**串行**执行；`wiki_export.py` 已内部串行调用 wiki CLI，Agent 无需再逐条手动调用。

## 1. 收集与追加 inbox

`inbox.md` 当前为**表格格式**，每行含 URL、标题、最近更新时间、docKey：

```markdown
| # | URL | 标题 | 最近更新 | docKey |
|---|-----|------|---------|--------|
| 1 | https://wiki.huawei.com/.../WIKI... | 页面标题 | 2026-08-20 | WIKI... |
```

1. 收集 URL：当前对话链接 + `inbox.md` 表格中的 URL 列。`wiki_export.py` 的 `parse_inbox()` 已兼容表格格式（从 `|` 分隔行提取 http URL）。
2. 对话里有、且 inbox 中尚未出现的 URL（**url 精确匹配**）→ **追加到 `inbox.md` 末尾为新表格行**（需填 #、URL、标题、最近更新、docKey）。标题和更新时间可通过 `wiki doc get` 获取，或用 `python tools/wiki-export/wiki_inbox_meta.py fetch && generate` 批量刷新后重写 inbox。
3. 「重试失败项」：从 `wiki/log.md` 读标记为 `ingest failed` 的 URL，纳入待处理。
4. 「刷新某 url」：该 URL 无视已有 `sources:`，用 `re-export` 模式重导后再编译。

不要 Glob 整个 `raw/` 或整库 `wiki/`。

## 2. 取本批

按 inbox 从上到下（含刚追加的），过滤掉：

- 已在某知识页 frontmatter `sources[].resource` 中出现过的 URL（精确匹配），除非用户点名「刷新该 url」
- `wiki/log.md` 里已记为 `ingest skipped` / `ingest failed` 的 URL，除非用户说重试或刷新

默认取最多 **15** 条；用户指定本批条数则按指定。批处理导出无 token 瓶颈，但编译（triage → 蒸馏 → 写页）每条约需 1 轮对话，过大批次易超上下文，建议 10–20 条。

## 3. 批量导出（用 wiki_export.py）

将本批 URL 交给脚本一次性导出，**不要逐条手动调用 wiki CLI**：

```bash
python tools/wiki-export/wiki_export.py export <url1> <url2> ...
```

脚本会自动：
- 从 URL 提取 docKey
- 调用 `wiki doc get` 获取正文
- 解析所有图片 URL 并下载到 `images/`（用 hash 命名，避免 `image.png` 覆盖）
- 改写 `{标题}.md` 中的图片链接为本地路径
- 串行调用 wiki CLI（无需 Agent 逐条等待）

### 刷新模式

需要重导某个已归档的 docKey：

```bash
python tools/wiki-export/wiki_export.py re-export <docKey>
```

### 导出结果验收

脚本输出每个文档的状态。对成功的条目，验收目录结构：

```
raw/wiki/archive/<docKey>/
  {标题}.md
  images/
```

不满足 → `failed`，不编译。

## 4. 编译（必须串行；质量门）

对每条导出并验收成功的条目，**一条一条**编译（index/log 是共享状态）。「同批」本身不是关联依据；**内容确有关联时可以互链**。禁止默认「1 URL = 1 新页」。

### 4.1 过滤

非运维知识 → `skipped`，写 log（原因），不写知识页。

### 4.2 Triage（与一般摄入相同）

以本条 `archive/<docKey>/{标题}.md` 为主；在 `wiki/` 按标题/实体/同义词搜已有页，判定：

- **Update** — 合并进已有页（补 `sources` 写本条原始 wiki URL）
- **New** — 才新建；一篇来源可拆成多种 type（例如手册 + 注册表）
- **No material** — 无新增知识；只记 log，不强行写页

需要判断与本批其它条是否相关时，可对照其标题/摘要，不要为凑链通读全文硬凑。

### 4.3 蒸馏验收

按 [okf.md](okf.md) 选 type/目录与固定 `##`；写页当时按 §4.3.0 **对照来源核对清单**逐项自检，不通过 → `failed` + log note，不要凑空壳页：

- 按 type 固定 `##` 写满；来源没有的小节写「来源未写」，**禁止**用训练数据补集群名、地址、命令
- 正文自洽，值班打开这一页就能做；不要「详见 raw/archive」
- 命令进代码块；密钥/token 剥离；占位符用 `<cluster>`、`<namespace>`、`<path>`
- 只拷对操作有用的图到知识页同目录 `attachments/`，正文 `![](./attachments/<文件名>)`（见 okf.md）；raw 侧仍用 `images/`
- **交叉引用**：按 [okf.md](okf.md)「按内容关联」——确有依赖/互补/上下游 → 可链；仅因同批 → 不链
- `status: draft`；**不替人写** `verified`
- `sources` **只写本条原始 wiki URL**；禁止写 `raw/wiki/archive/...`

可选：按 [obsidian.md](obsidian.md) 用 `obsidian-cli` 创建/更新笔记；失败则回退普通 Write。

### 4.3.0 蒸馏核对清单（对照原文逐项过）

写页后**对照 `archive/<docKey>/{标题}.md` 原文逐项核对**，不通过 → `failed` + log note，不要凑空壳页：

- **步骤可执行**：每个步骤必须有命令 / 链接 / 参数等可执行内容；只有一句话标题的步骤不合格
- **关键外链保留**：来源正文中的 MR / commit / codehub / 3ms 等关键引用链接，保留进对应小节（可追溯）；`sources` 仍只写 wiki URL
- **数据保留**：数字、表格、命令原样保留，不缩写、不丢行
- **遗留项保留**：来源的「待确认 / 遗留问题 / 下一步」逐条照搬（含链接）
- **空壳标注**：来源没有的小节写「来源未写」，禁止留空标题
- **正文自洽**：值班打开这一页就能做，不依赖 raw

### 4.3.1 实体注册（资源注册表同步）

按 [ingest.md](../ingest.md) 一般摄入「实体注册」步执行。**写完概念页后立即做，不要等用户提醒。** 本通道 `sources` **只写本条原始 wiki URL**，禁止 `raw/wiki/archive/...`。没有可注册实体、或本条是 skipped / failed / no material → 跳过，不强行建页。交叉引用仍按 [okf.md](okf.md)「按内容关联」，链到 Registry 时放在该 type 的固定相关章节。

### 4.4 index / log

按 [index-log.md](index-log.md) 更新分组 index（无则创建）与 `wiki/log.md`。公司 wiki 结果用固定句式（便于下次过滤）：

- `* **Update**: ingest compiled https://... → [标题](/wiki/操作手册/页.md)。`
- `* **Update**: ingest skipped https://... — 非运维知识。`
- `* **Update**: ingest failed https://... — wiki-cli 失败：…`
- `* **Update**: ingest no material: https://...`

新建概念页仍可另写一条 `**Creation**`（见 index-log.md）。

## 5. 本批结束

汇报：compiled / skipped / failed / no material（各列 url 或 docKey）；inbox 中尚未出现在 `sources:` 且未记 skipped/failed 的剩余大约数量；问是否继续。

列出本批新页/改页路径，并说：「以上为 draft，请抽看；要标 verified 再说一声。」

然后跑 `python tools/okf-lint/okf_lint.py`，先修 error。

存档路径为 `raw/wiki/archive/<docKey>/`。不自动刷新已编译 URL（除非用户点名）。蒸馏编译，不要把 wiki 全文当 OKF 页粘贴。

---

## 增量刷新

**默认刷新模式**：仅编译 wiki 有更新的条目，跳过未变化的条目。全量刷新需用户明确说「全量刷新」。

### 流程

```
Step 1: 刷新元数据    wiki_inbox_meta.py fetch + generate
Step 2: Diff          wiki_refresh.py diff
Step 3: Re-export     wiki_export.py re-export <受影响 docKey...>
Step 4: 编译          同 §4（串行 Triage → 蒸馏 → 写页 → log）
Step 5: 收尾          同 §5
```

### Step 1：刷新 inbox 元数据

拉取所有 URL 的最新标题和更新时间，同步到 `inbox.md` 和 `inbox_meta.json`：

```bash
python tools/wiki-export/wiki_inbox_meta.py fetch && python tools/wiki-export/wiki_inbox_meta.py generate
```

- `fetch`：串行调用 `wiki doc get` 获取每条 URL 的 `title` + `last_update_time`，缓存到 `raw/wiki/inbox_meta.json`
- `generate`：从缓存重写 `inbox.md` 为表格格式（含标题、最近更新、docKey），原文件备份为 `.bak`

### Step 2：Diff（判断哪些需要重编译）

```bash
python tools/wiki-export/wiki_refresh.py diff
```

脚本自动：
1. 读 `inbox_meta.json`（每条 URL 的 wiki `last_update_time`）
2. 读 `wiki/log.md`（每条 URL 最近一次 `ingest compiled` 的日期）
3. 对比：**wiki `last_update_time` > 编译日期** 的条目标记为 **NEEDS REFRESH**
4. 输出四类：
   - **NEEDS REFRESH** — wiki 有更新，需重编译
   - **NO COMPILE DATE** — inbox 中有 URL 但从未编译过（新条目）
   - **UP TO DATE** — wiki 未更新，可跳过
   - **SKIPPED / FAILED** — log 标记为 skipped/failed 的条目

**判断规则**：按日期粒度比较（YYYY-MM-DD），同日视为无更新。

### Step 3：Re-export 受影响条目

仅 re-export Step 2 标记为 NEEDS REFRESH 的 docKey：

```bash
python tools/wiki-export/wiki_export.py re-export <docKey1> <docKey2> ...
```

或用快捷命令（脚本内部调 diff 后只 re-export 有变化的）：

```bash
python tools/wiki-export/wiki_refresh.py re-export-changed
```

### Step 4：编译变更条目

按 §4 串行编译每条 re-export 成功的条目。**关键差异**：

| | 首次入库 | 增量刷新 |
|---|---------|---------|
| Triage | New / Update | **一定是 Update**（已有页） |
| 编译动作 | 写新页或合并进已有页 | **读 raw 源 + 读现有 OKF 页 → diff → 合并新增内容** |
| 不变处理 | N/A | wiki 源无新增知识 → `no material`，不强行改页 |

增量刷新编译时的具体操作：
1. 读 raw 源文件 `archive/<docKey>/{标题}.md`
2. 读现有 OKF 页（从 `sources` 反查到对应页）
3. 对比：
   - raw 有、OKF 无 → 合并
   - raw 有变化（步骤/命令/参数更正）→ 更新
   - raw 无变化 → `no material`
4. 写页 + 更新 index/log

### Step 5：收尾

同 §5。额外汇报：
- 本轮 diff 结果中 **NEEDS REFRESH 数** vs **实际 compiled 数**
- 仍为 UP TO DATE 的条目数量和概览

### 特殊场景

| 场景 | 处理 |
|------|------|
| 用户说「全量刷新」 | `wiki_export.py re-export --all`，然后全量走 §4 编译 |
| 新 URL 加入了 inbox | Step 2 会标为 NO COMPILE DATE，走首次入库流程（§0–5） |
| wiki 更新但编译后发现无新增知识 | 记 `no material`，写 log；不强行改页 |
| skipped/failed 条目有更新 | 不自动重试；汇报给用户，由用户决定 |
| 多条 URL 贡献给同一个 OKF 页 | 合并处理；任一条有更新都触发该页重编译 |

---

## 辅助工具

| 工具 | 用途 |
|------|------|
| `python tools/wiki-export/wiki_inbox_meta.py fetch` | 批量获取 inbox 所有 URL 的标题+更新时间，缓存到 `raw/wiki/inbox_meta.json` |
| `python tools/wiki-export/wiki_inbox_meta.py generate` | 从缓存重写 `inbox.md` 为表格格式（含标题、最近更新、docKey） |
| `python tools/wiki-export/wiki_refresh.py diff` | 对比 wiki 更新时间与编译时间，列出需重编译条目 |
| `python tools/wiki-export/wiki_refresh.py re-export-changed` | 仅 re-export 有更新的条目 |
