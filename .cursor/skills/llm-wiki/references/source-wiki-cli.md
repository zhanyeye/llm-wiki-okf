# 公司 Wiki 来源（wiki_export.py + wiki-cli）

`raw/wiki/` 是来源通道，与仓根 `wiki/`（知识面）不是同一目录。

**禁止**用 WebFetch / Defuddle 抓内网 wiki。必须用 **wiki_export.py** 脚本（内部调用 wiki CLI）。

## 触发

- 对话贴了 wiki 链接并说入库
- 「把 inbox 入库」
- 「继续下一批 / 重试失败项 / 刷新某 url」

人可贴对话链接，或编辑 [`raw/wiki/inbox.md`](../../../../raw/wiki/inbox.md)（一行一个 URL，只追加）。`inbox.md` 是增量登记册，不是会排空的队列。

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

1. 收集 URL：当前对话链接 + `inbox.md` 非注释行（`#` 开头整行忽略；空行忽略）。有效行 = 去掉首尾空白后整行就是 URL；**一行一个**，原样保留。
2. 对话里有、且 inbox 中尚未出现的 URL（**url 精确匹配**）→ **追加到 `inbox.md` 末尾**。不要删行、不要改已有行、不要写成 `[标题](url)`、不要加状态列。
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

按 [okf.md](okf.md) 选 type/目录与固定 `##`；写页当时自检，不通过 → `failed` + log note，不要凑空壳页：

- 按 type 固定 `##` 写满；来源没有的小节写「来源未写」，**禁止**用训练数据补集群名、地址、命令
- 正文自洽，值班打开这一页就能做；不要「详见 raw/archive」
- 命令进代码块；密钥/token 剥离；占位符用 `<cluster>`、`<namespace>`、`<path>`
- 只拷对操作有用的图到知识页同目录 `attachments/`，正文 `![](./attachments/<文件名>)`（见 okf.md）；raw 侧仍用 `images/`
- **交叉引用**：按 [okf.md](okf.md)「按内容关联」——确有依赖/互补/上下游 → 可链；仅因同批 → 不链
- `status: draft`；**不替人写** `verified`
- `sources` **只写本条原始 wiki URL**；禁止写 `raw/wiki/archive/...`

可选：按 [obsidian.md](obsidian.md) 用 `obsidian-cli` 创建/更新笔记；失败则回退普通 Write。

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
