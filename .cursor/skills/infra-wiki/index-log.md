# index.md 与 log.md

对齐 [OKF Quickstart](https://okf.md/quickstart/) 与 SPEC §8 / §9。查询不改这两类文件；**新建或改概念页之后必须更新**。

## index.md（渐进式索引）

`index.md` 是目录 TOC，不是概念页。让人/Agent 先看见有什么，再打开正文。

| 位置 | frontmatter | 列什么 |
|------|-------------|--------|
| 根 `index.md` | 仅允许 `okf_version: "0.2"` | 11 个分组目录 |
| `<分组>/index.md` | **禁止** frontmatter | 本目录概念页 |

根 index **只在增删/改名分组时**改。日常入库只改被写入的那个分组 `index.md`；故障相关再看 `故障排查/index.md`。

### 结构（必须）

```markdown
# 目录标题

一句话说明本目录放什么。

## 分组名

* [概念 title](./file.md) - 该页 description 的短摘要
* [子目录](./subdir/) - 该子目录一句话
```

- 标题用 `#`；内容分组用 `##`，不要再用 `#` 当第二节。
- 条目格式：`* [标题](链接) - 短描述`（空格、连字符、空格）。描述取自目标页 `title` / `description`，不要另写一套。
- 同目录概念：`./disk-full.md`。同目录子文件夹：`./资源注册表/`（目录链接，不要写成 `index.md`）。跨目录：bundle 绝对路径 `/系统与架构/minio.md`。
- 有页必有一条；删页或改 `title`/`description` 时同步改条目。
- 尚无概念页：只保留 `# 标题` 和一句话；**第一篇写入时**再加 `## 页面` 和条目。
- 不要把 schema、domain 列表、Skill 说明写进 index（那是 README / Skill `types.md`）。

### 故障排查/index.md

按症状列。已有正文 → 链接；没有 → `* 待入库：<症状>`。入库后把「待入库」换成链接，不要两条并存。

## log.md（变更日志）

仅根 `log.md`。无 frontmatter。追加式，**不要改写或删除**旧条目。

```markdown
# 更新日志

## 2026-08-21

* **Update**: 说明，并链到 [标题](/分组/file.md)。
* **Creation**: 写入 [标题](/分组/file.md)。

## 2026-08-20

* **Initialization**: 建立分组结构。
```

- 日期标题 `## YYYY-MM-DD`，**最新日在上**。当天已有该日期则在该节**顶部**插入新行。
- 日期标题与第一条之间空一行。
- 一条一事、一篇一链。禁止把多页塞进同一颗 `*`。
- 动词（英文，加粗）后接 **ASCII 冒号 `:`**（不要用 `：`）：

  | 动词 | 何时 |
  |------|------|
  | `**Creation**` | 新建概念页 |
  | `**Update**` | 改已有页（含改 index 条目、把待入库换成链接） |
  | `**Deprecation**` | 废弃一页（正文标废弃，index 可保留并注明） |
  | `**Initialization**` | 建目录结构（一般只出现一次） |

- 链接用 bundle 绝对路径：`[MinIO](/系统与架构/minio.md)`。
- 纯查询、只跑 lint 且未改页 → 不写 log。
