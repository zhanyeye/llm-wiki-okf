# index.md 与 log.md

常规查询不改这两类文件；**新建或改概念页之后必须更新**。唯一例外：execute.md 的执行记录（见下）。

分组列表以 [`wiki/index.md`](../../../../wiki/index.md) 为权威来源；本文件只规定格式，不硬编码分组名。

## index.md（渐进式索引）

`index.md` 是目录 TOC，不是概念页。总入口先按 L0 Atomic、L1 Registry、L2 Operational 导航；分组内可继续按领域或资产种类建子目录。

| 位置 | frontmatter | 列什么 |
|------|-------------|--------|
| `wiki/index.md` | 仅允许 `okf_version: "0.2"` | 各分组目录（读该文件，不假设固定数量） |
| `wiki/<分组>/index.md` | **禁止** frontmatter | 本目录概念页 |
| 仓根 `index.md` | **禁止** frontmatter | 只链 `wiki/` / `raw/` / `script/` / `tools/`（仓地图，lint 不扫） |

`wiki/index.md` **只在增删/改名分组时**改。日常入库只改被写入的那个分组 `index.md`；故障相关再看 `wiki/故障排查/index.md`。

### 何时需要分组 index.md

| 状态 | 是否需要 `wiki/<分组>/index.md` |
|------|--------------------------------|
| 分组尚无概念页 | **不需要**。不要为占位单独建空 index；目录可用 `.gitkeep` 保留 |
| 写入第一篇概念页 | **必须创建** index.md，并列入该页 |
| 已有 index | 有页必有条目；删页或改 `title`/`description` 时同步改 |

嵌套目录同样遵守“有概念页才建 index”：例如 `wiki/资源注册表/数据库/index.md` 列数据库资产，`wiki/资源注册表/index.md` 链到 `./数据库/`。不要在父 index 复制列出所有子目录资产。

例外：`wiki/故障排查/index.md` 可在尚无正文时存在，用于列「待入库」症状清单（值班入口）。

### 结构

```markdown
# 目录标题

一句话说明本目录放什么。

## 分组名

* [中文 title](./页名.md) - 该页 description 的短摘要
* [子目录](./subdir/) - 该子目录一句话
```

- 标题用 `#`；内容分组用 `##`。
- 条目格式：`* [标题](链接) - 短描述`（空格、连字符、空格）。描述取自目标页 `title` / `description`。
- 同目录概念：`./页名.md`。同目录子文件夹：`./资源注册表/`（目录链接，不要写成 `index.md`）。跨目录：仓根绝对路径 `/wiki/资源注册表/页.md`。
- 不要把 schema、domain 列表、Skill 说明写进 index。
- index 只做导航；资产聚合视图可由 Obsidian Base 生成，不能成为第二份事实源。

### 故障排查/index.md

按症状列。已有正文 → 链接；没有 → `* 待入库：<症状>`。入库后把「待入库」换成链接，不要两条并存。

## log.md（变更日志）

仅 `wiki/log.md`。无 frontmatter。追加式，**不要改写或删除**旧条目。

```markdown
# 更新日志

## 2026-08-26

* **Update**: 说明，并链到 [标题](/wiki/操作手册/file.md)。
* **Creation**: 写入 [标题](/wiki/操作手册/file.md)。

## 2026-08-25

* **Initialization**: 建立分组结构。
```

- 日期标题 `## YYYY-MM-DD`，**最新日在上**。当天已有该日期则在该节**顶部**插入新行。
- 日期标题与第一条之间空一行。
- 一条一事、一篇一链。
- 动词（英文，加粗）后接 **ASCII 冒号 `:`**（不要用 `：`）：

| 动词 | 何时 |
|------|------|
| `**Creation**` | 新建概念页 |
| `**Update**` | 改已有页（含改 index 条目、把待入库换成链接、公司 wiki ingest 结果） |
| `**Deprecation**` | 废弃一页 |
| `**Initialization**` | 建目录结构（一般只出现一次） |
| `**Execution**` | Agent 按 execute.md 跑脚本后记录结果（不改知识页） |

- 链接用仓根绝对路径：`[标题](/wiki/操作手册/file.md)`。
- 纯查询、只跑 lint 且未改页 → 不写 log（执行记录见 `**Execution**`，如：
  `* **Execution**: ran [磁盘满处理](/wiki/操作手册/磁盘满处理.md) — exit 0，水位恢复正常。`

### 公司 wiki ingest 行（固定句式）

便于下次按 URL 过滤已处理项；与 `inbox.md`（只追加）配合：

```markdown
* **Update**: ingest compiled https://wiki.example.com/pages/viewpage.action?pageId=12001 → [标题](/wiki/操作手册/页.md)。
* **Update**: ingest skipped https://wiki.example.com/pages/viewpage.action?pageId=12002 — 非运维知识。
* **Update**: ingest failed https://wiki.example.com/pages/viewpage.action?pageId=12003 — wiki-cli 失败：…。
* **Update**: ingest no material: https://wiki.example.com/pages/viewpage.action?pageId=12004
```

- `ingest compiled`：URL 已编进知识页（也可用 `sources` 数组判断已处理）。
- `ingest skipped` / `ingest failed`：默认不再进本批，除非用户说重试或刷新。
- 新建概念页仍可另写一条 `**Creation**`。
