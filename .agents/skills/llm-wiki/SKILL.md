---
name: llm-wiki
description: >-
  基于 LLM 的知识库管理。在用户要建设、维护或查询 wiki 风格知识库时使用——包括初始化、
  入库文档、检索问答、体检维护。适合个人笔记、研究、项目文档及持续积累知识的场景。
---

# LLM Wiki Skill

用于构建和维护持久、可累积的知识库。

本 Skill 实现 wiki 模式：LLM 在你与原始来源之间增量构建并维护结构化 wiki——知识编译一次并保持更新，而不是每次查询从头推导。

## 核心理念

- **Wiki 是持久的**：交叉引用已存在，矛盾会被标出，综合反映你已读过的全部内容
- **LLM 负责记账**：摘要、交叉引用、归档与维护——人容易放弃的琐事
- **人负责思考**：筛选来源、指导分析、提出好问题、解释含义

## 推荐目录结构

```
wiki-root/                # 以 wiki 为根目录（raw/ 下不分子目录）
├── CLAUDE.md             # Schema：结构、约定、工作流
├── raw/sources/          # 扁平存放：把文件丢进来即可
│   ├── article-1.md      # 不分子目录——由 LLM 通过 index 管理分类
│   └── ...
├── wiki/
│   ├── index.md          # 内容目录（按类型 + 时间戳组织）
│   ├── log.md            # 活动日志
│   ├── entities/         # 实体页
│   ├── concepts/         # 概念页
│   └── source-summaries/ # 来源摘要页
└── .git/                 # 版本历史（git 仓自带）
```

**关键设计决策：**
- **以 wiki 为根**：管理更简单，与根目录 `CLAUDE.md` 配合
- **扁平 `raw/sources/`**：无需手工维护目录——丢文件即可，LLM 通过 `index.md` 分类
- **wiki 内容分离**：来源摘要、实体、概念放在 `wiki/` 子目录

## 关键文件

- **`CLAUDE.md`** — 定义本 wiki 结构、约定与工作流的 Schema。LLM 维护此库时必读。
- **`wiki/index.md`** — 内容目录。按类别（实体、概念、来源）组织，每条含链接 + 一句话摘要 + 更新时间戳。每次 ingest 由 LLM 更新。
- **`wiki/log.md`** — 按时间顺序的活动日志。格式：`## [2026-04-05] ingest | 标题`。

---

## 操作

### 1. 初始化 Wiki（init）

从零创建新 wiki。

**何时：** 用户说「初始化」「创建知识库」「start wiki」

**流程：**
1. 询问用户：wiki 名称/用途、存放位置、初始来源（如有）
2. 创建目录结构：
   ```
   wiki-root/                # 以 wiki 为根目录
   ├── CLAUDE.md             # Schema：结构、约定、工作流
   ├── raw/sources/          # 扁平存放：把文件丢进来即可
   │   ├── article-1.md
   │   └── ...
   ├── wiki/
   │   ├── index.md          # 内容目录（按类型 + 时间戳组织）
   │   ├── log.md            # 活动日志
   │   ├── entities/         # 实体页
   │   ├── concepts/         # 概念页
   │   └── source-summaries/ # 来源摘要页
   ```
3. 创建初始 `index.md` 与 `log.md`
4. 创建 `CLAUDE.md`，写入 wiki 约定（结构、工作流、用户偏好）
5. 若已有来源，执行 ingest

---

### 2. 入库来源（ingest）

处理新来源并整合进 wiki。

**何时：** 用户说「ingest」「入库」「add to wiki」「处理这份文档」

**流程：**
1. **采集时间戳信息：**
   - 获取文件最后修改时间（file_modified）
   - 提取内容日期（content_date）：新闻发布日、日记日期、会议日期等
   - 若两者不一致，在 frontmatter 中注明

2. 仔细阅读来源
3. 与用户讨论关键要点
4. 写/更新 wiki 页：
   - 摘要页：关键点
   - 实体页：人物、地点、组织
   - 概念页：主题、理论、想法
   - 交叉引用：链到相关页
5. 更新 `index.md` 新条目（含 `updated` 时间戳）
6. 追加 `log.md`
7. 标出与既有内容的矛盾

**提示：** 一次处理一条来源，并让用户参与。一起审阅摘要。

---

### 3. 查询 / 回答问题（query）

以 wiki 为知识来源回答问题。

**何时：** 用户问「关于 X 我们知道什么」「总结 Y 的笔记」「对比 A 和 B」

**流程：**
1. 读 `index.md` 找相关页
2. 阅读相关页
3. 综合回答并给出引用
4. 提议把有价值的答案存回 wiki 成新页
5. 在 `log.md` 记录本次查询

**输出形态：** Markdown 页、对比表、幻灯片（Marp）、图表（matplotlib）

---

### 4. 体检 / 维护（lint）

检查 wiki 健康状况，含内容新鲜度与 schema 健康。

**何时：** 用户说「检查 wiki 健康」「lint wiki」「清理知识库」——建议定期（如每季度）做

**流程：**
1. **基础健康检查：**
   - 跨页矛盾
   - 被更新来源取代的过时内容
   - 孤儿页（无入链）
   - 缺页（重要概念被提及但无独立页）
   - 断链
   - 可用网络搜索填补的数据缺口

2. **内容新鲜度检查：**
   - 扫描 `raw/sources/` 下全部文档
   - 对每份：取 file_modified，从正文提取 content_date
   - 对比：文件日期与内容日期不一致则标出
   - 识别过时内容：旧 raw 对应过时 wiki 页
   - 按来源新鲜度优先级生成报告

3. **CLAUDE.md 健康检查：**
   - 确认根目录存在 `CLAUDE.md`
   - 检查约定是否仍然有效（询问用户）
   - 若工作流已演变，建议更新
   - 确保 CLAUDE.md 反映当前 wiki 结构

4. 向用户汇报发现
5. 提议修复问题
6. 更新 `log.md`

---

### 5. 搜索（search）

对 wiki 做全文检索。

**何时：** 用户说「搜索 X」「找出所有关于 Y 的内容」

**流程：**
1. 若有 qmd 可用则用（BM25/向量混合检索）
2. 否则 grep 遍历 wiki 文件
3. 给出带上下文的结果
4. 提议打开相关页

---

## Wiki 结构约定

### index.md 格式

```markdown
# Wiki Index

## Entities
- [[Person: Name]] - Brief (sources: 2, updated: 2026-04-07)

## Concepts
- [[Concept: Topic]] - Brief (sources: 3, updated: 2026-04-07)

## Sources
- [[Source: Doc Title]] - Source latest: 2026-04-01

## Recent Updates (newest first)
- [[Page: Name]] - Updated: 2026-04-07

## Stale Content
- [[Page: Name]] - 90 days stale, last updated: 2026-01-07
```

**要点：** 每条 index 条目应带 `updated` 时间戳。查询时优先较新内容。

---

### log.md 格式

```markdown
# Wiki Log

## [2026-04-07] ingest | Article Title
- Summary: Key finding
- Updated: entity page, concept page
- Notes: User emphasis noted

## [2026-04-06] query | What is X?
- Answered with 3 sources
- Saved as: comparison-x-vs-y.md
```

---

### 页面格式

```markdown
---
title: Page Title
type: entity | concept | source-summary | synthesis
tags: [tag1, tag2]  # 例：[entity, tool]、[concept]、[source-summary, ai]
source: "Original title"
author: "Author name"
date: "2026-04-07"  # 原始文档日期（对新鲜度至关重要）
url: "Original URL"  # 若为网页内容
created: 2026-04-07
updated: 2026-04-07
source_timestamps:
  - source: raw/sources/document.md
    file_modified: "2026-04-01"  # 文件系统修改时间
    content_date: "2026-03-25"   # 文档正文中的日期
    note: "Event mentioned occurred on 2026-03-25"
---

# Page Title

## Summary
Brief overview.

## Key Details
- Point 1
- Point 2

## Related
- [[Concept: Related Topic]]
- [[Entity: Related Entity]]

## Sources
1. [[Source: Source Name]] - Excerpt (source date: 2026-04-01)
```

**Frontmatter 字段：**
- `type`：页面类型 — `entity`、`concept`、`source-summary`、`synthesis`
- `tags`：分类用数组
- `source`：原始文档标题
- `author`：文档作者
- `date`：原始文档日期（对新鲜度至关重要）
- `url`：原始链接（若为网页）
- `created` / `updated`：wiki 页时间戳
- `source_timestamps`：raw 文档时间信息

**重要：** 原始文档时间戳对判断内容新鲜度至关重要。入库时务必提取日期信息。

---

## 用户交互模式

### 个人知识
- 询问目标、挑战、关注领域
- 组织为：日记条目、洞察、行动项

### 研究
- 询问研究问题/论点
- 仔细追踪引用

### 项目文档
- 询问项目结构、决策
- 在合适处链到代码

### 业务 / 团队 Wiki
- 明确 LLM 与人工审核的职责边界
- 工作流：LLM 起草 → 人批准 → LLM 发布

---

## 最佳实践

1. **始终记日志** — 每次 ingest / query / lint 都写入 `log.md`
2. **维护 index** — 保持 `index.md` 最新
3. **积极双链** — 每个概念提及都链到对应页
4. **标出矛盾** — 不要静默覆盖，展示给用户
5. **保存有价值输出** — 好的查询答案应变成 wiki 页
6. **尊重来源** — raw 文档不可变
7. **建议，勿臆断** — 改动前先与用户确认

---

## 交叉引用原则

1. **每页底部**：包含「Sources」节，链到来源摘要
2. **新来源更新旧页**：入库时检查既有页是否需更新
3. **概念网络**：摘要页末列出「Related Concepts」
4. **跨来源连接**：标出不同来源的共用主题

**格式：** 内部链接使用 `[[Page Name]]`（Obsidian 风格）。

### 知识关联发现

处理第 2+ 条来源时，重点关注：

- **共同主题**：标出跨来源重复出现的观点
- **矛盾观点**：显式标冲突——不要静默覆盖
- **互补**：新来源为已有概念补充例子？则更新已有页
- **概念演进**：同一概念在不同来源侧重点不同——加以综合

---

## 典型入库规模

一篇中等文章（约 2000–3000 字）通常：
- 新建 2–4 页（1 个摘要 + 1–3 个实体/概念）
- 更新 2–4 个已有页
- 合计触碰约 5–8 个文件

这是正常现象——知识库在互联中生长。

---

## 工具

- **Read/Write/Edit**：读写 wiki 文件
- **Glob/Grep**：搜索与导航
- **WebSearch/WebFetch**：填补缺口（需许可）
- **qmd**：混合检索（若可用）
- **Marp**：演示文稿（若需要）
- **Dataview**：查询 frontmatter（若使用 Obsidian）

---

## 快速开始

当用户第一次提到想要 wiki 时：

1. 简短说明模式
2. 询问想追踪什么：个人 / 研究 / 项目 / 其他
3. 询问存放位置
4. 提议初始化

根据其回答决定优先执行哪些操作。
