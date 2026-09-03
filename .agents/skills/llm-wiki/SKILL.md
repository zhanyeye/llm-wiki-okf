---
name: llm-wiki
description: >-
  基于 LLM 的基础设施知识库管理。在用户要建设、维护或查询 wiki/ 时使用——包括初始化、
  入库文档、检索问答、搜索与体检。Triggers: ingest, query, lint, search, init,
  add to wiki, company wiki links, raw/wiki/inbox.md。
---

# LLM Wiki Skill

用于构建和维护持久、可累积的基础设施知识库。

本 Skill 实现 wiki 模式：LLM 在你与 `raw/` 来源之间增量编译并维护结构化 `wiki/`——知识编译一次并保持更新，而不是每次查询从头推导。对话不是知识库；有价值的综合结论要写回页面。

**默认只读本文件 + [`wiki/index.md`](../../../wiki/index.md)。** 写页再读 [references/okf.md](references/okf.md)；公司 wiki 再读 [references/source-wiki-cli.md](references/source-wiki-cli.md)。

## 核心理念

- **Wiki是持续积累的**：交叉引用已存在，矛盾会被标出，综合反映已入库内容
- **LLM负责整理维护**：摘要、交叉引用、归档与维护——人容易放弃的琐事
- **人负责思考**：筛选来源、指导分析、提出好问题、解释含义；人工审核后才 `verified`
- **安全与接地**：不写密钥；不编造集群名、地址、步骤；答案只来自已打开的 `wiki/` 页
- **禁止一来源一页**：先拆基础知识 → 资源目录（双链 L0）→ 操作手册 / 常见问题 / ADR / 案例

## 推荐目录结构

```
repo-root/
├── AGENTS.md             # Schema 索引：权限、查询入口、约定
├── raw/                  # 来源（默认只读；raw/wiki/ 可追加 inbox、写 archive）
│   ├── wiki/             # 公司 wiki 导出通道
│   └── ...
├── wiki/
│   ├── index.md          # 知识入口 TOC（分层）
│   ├── log.md            # 活动日志
│   ├── 基础知识/         # L0 Foundation（按能力域）
│   ├── 资源目录/         # L1 Registry（按资产类）
│   ├── 操作手册/         # Runbook
│   ├── 常见问题/         # FAQ（短问答与排查）
│   ├── 架构决策记录/     # ADR
│   └── 案例与复盘/       # Incident
├── script/               # 运维脚本（用法写在操作手册）
└── tools/                # 框架工具（okf-lint、wiki-export 等）
```

**关键设计决策：**
- **分层而非平铺**：知识按依赖生长（L0 → L1 → 运维），禁止把一篇来源缩成一页
- **`raw/` 与 `wiki/` 分离**：来源默认不可变；知识只写 `wiki/`
- **分组以 [`wiki/index.md`](../../../wiki/index.md) 为准**：有概念页才建分组 index（例外见 okf）

## 关键文件

- **`AGENTS.md`** — 仓能力索引与三面权限。查询时不要通读长文；操作以本 Skill 为准。
- **`wiki/index.md`** — 知识入口 TOC。可有 `okf_version: "0.2"`。只在增删/改名分组时改顶栏；日常入库更新**被写入分组**的 `index.md`。
- **`wiki/log.md`** — 追加式活动日志（无 frontmatter）。见下方约定。

---

## 操作

### 1. Initialize Wiki (init)

从零搭建或校验本仓骨架。

**何时：** 用户说「初始化」「创建知识库」「start wiki」；或明确要求补齐缺失分组骨架。

**流程：**
1. 若仓已存在：对照 `wiki/index.md` 校验分组与目录缺口，只补缺、不重建。
2. 若从零开始，询问用途后创建：
   ```
   AGENTS.md / README.md（若缺）
   raw/  wiki/index.md  wiki/log.md
   wiki/基础知识/（能力域子目录可写「待建」）
   wiki/资源目录/（资产类子目录可写「待建」）
   wiki/操作手册/  wiki/常见问题/  wiki/架构决策记录/  wiki/案例与复盘/
   ```
3. 写入初始 `wiki/index.md` 与 `wiki/log.md`（`**Initialization**`）。
4. 有初始来源则转入 ingest。

不要创建 entities/concepts/source-summaries 树。

---

### 2. Ingest Sources (ingest)

处理新来源并整合进 `wiki/`。

**何时：** 用户说「ingest」「入库」「add to wiki」「处理这份文档」；或贴公司 wiki 链接 / `inbox.md`。

写页前读 [references/okf.md](references/okf.md)。

**触发分流**

| 触发 | 走 | 工具 |
|------|-----|------|
| 公司 wiki 链接 / `inbox.md` / 继续下一批 / 增量刷新 | 本节 + [references/source-wiki-cli.md](references/source-wiki-cli.md) | `wiki_export.py` + `wiki` CLI |
| 公网 URL | `defuddle parse <url> --md` 落 `raw/` 后再编译 | Defuddle |
| raw / 对话存档 / 从零写页 | 本节一般流程 | Read |
| 用户指出页错误 | 改页 → `status: draft`、清 `verified` → 更新 index/log → lint | Edit |

**⚠️ 公司 wiki 关键约束（容易违反）：**
- **禁止**用 Read/Defuddle/WebFetch 读取公司 wiki URL — 这些工具无法访问内网
- **必须**使用 `tools/wiki-export/wiki_export.py` 脚本（内部调用 `wiki` CLI）
- 具体命令和流程见 [references/source-wiki-cli.md](references/source-wiki-cli.md)

**写入分组（可选）：** 用户用 `wiki/index.md` 里的**分组名**限制本次写入。未指定 = 全部。范围外标 `deferred`。缺下层默认 link-only（标 gap）；仅用户说「缺的也建」才 stub。

**流程：**

1. **读取来源内容（按来源类型选工具）：**

| 来源类型 | 读取工具 | 示例 |
|----------|----------|------|
| **公司 wiki 链接** | `python tools/wiki-export/wiki_export.py export <url>` | `python tools/wiki-export/wiki_export.py export "https://wiki.huawei.com/.../WIKI..."` |
| 公网 URL | `defuddle parse <url> --md` 落 `raw/` | - |
| 本地文件 | Read | - |

**⚠️ 公司 wiki 必须用 `wiki_export.py`（内部调用 `wiki` CLI），禁止用 Read/Defuddle/WebFetch。**

2. **采集时间戳信息：**
   - 文件最后修改时间（file_modified）
   - 正文/文档中的内容日期（content_date：发布日、变更日等）
   - 若不一致，记在 frontmatter 或汇报里
3. 仔细阅读来源（不抄密钥；不改 `raw/`，公司 wiki 例外见 source-wiki-cli）
4. 与用户讨论关键要点（大改或将新建 ≥3 页时先报 Plan）
5. 写/更新 wiki 页（禁止一来源一页）：
   - 定义 → `基础知识/`（`Foundation`）
   - 实例 → `资源目录/`（`Registry`，正文「依赖」节 `[[双链]]` L0）
   - 任务 → `操作手册/`；问答/排查 → `常见问题/`；决策 → ADR；事件 → 案例
   - 同实体更新；同名异物换 `id`；先 L0 再 L1 再运维层；新页 `status: draft`
   - 语义关系用 `[[页]]` / `[[页#标题]]`；禁止仅因同批互链
6. **交叉引用编织（强制，不可跳过，全部页写完后统一执行）：**
   **先写完本次全部页（步骤 5），再统一做这一轮编织**——不要逐页边写边链，否则先写的页看不到后写的页，会误判孤立。
   - **出链**：对每一页，在新页正文（「关系」节、「依赖」节或其他相关章节）中，用 `[[双链]]` 指向相关已有页（含本次同批写的页）。
   - **反向补全**：对每一页，Grep `[[本页名]]` 找引用方；同时 Grep 搜索 `wiki/` 中提及本页主题（系统名、概念名、专名、`tags`）的页面；在语义合理处补充 `[[本页名]]` 回链。**被引用必回链**（见步骤 9）。
   - **同批互链**：本次同时写的多页之间，若内容确有依赖/互补/上下游关系，互相双链（仍遵守「禁止仅因同批互链」）。
   - **链接方向（双向允许）**：上层链下层用**依赖/定义引用**（引用定义，不复制内容）；下层链上层用**指路链接**（如「相关操作步骤见 [[X]]」）。双向互链是目标，禁止把有关系的页写成孤立。
   - 判定标准见下方 [交叉引用原则](#交叉引用原则) 与 okf.md「交叉引用」表。没有明确关系 → 省略链接，不要硬凑。
7. 更新涉及分组的 `index.md` 与 `wiki/log.md`
8. 标出与既有内容的矛盾（不静默覆盖）
9. **链接完整性自检：**
   - **被链必回链**：对每个新页 Grep `[[本页名]]` 找引用方；被引用且语义合理 → 必须回链。例：Runbook 链了 Foundation，Foundation 的「关系」节必须回链该 Runbook（指路）。
   - 确认每个新页至少有 1 条出链（`[[页]]`），除非**确实孤立**
   - **「暂无关联」仅限真孤立**：只有 Grep 全库确认**没有任何页面**提及本页主题（含跨目录、同批页）时才允许写「暂无关联」；只要发现 1 个相关页就必须链，禁止用「暂无关联」逃避链接义务
   - 断链（指向不存在的页）必须修复或移除
10. `python tools/okf-lint/okf_lint.py`（先修 error）；人说 OK 才写 `verified`
11. 有 deferred/gap 或指定了分组时汇报：本次写入 / 延后 / 缺口

**公司 wiki 完整流程（详细版）：**
1. `python tools/wiki-export/wiki_export.py check` — 前置检查 wiki CLI
2. 追加 URL 到 `raw/wiki/inbox.md`（精确去重）
3. `python tools/wiki-export/wiki_export.py export <url1> <url2>...` — 批量导出到 `raw/wiki/archive/`
4. 分层编译：先拆 Foundation → Registry → Runbook/FAQ/ADR
5. 写页时读 [references/okf.md](references/okf.md) 确保格式正确
6. 详细流程见 [references/source-wiki-cli.md](references/source-wiki-cli.md) §0-5

---

### 3. Query / Answer Questions (query)

以 wiki 为知识来源回答问题。

**何时：** 用户问「X 是什么」「我们怎么用 Y」「对比 A 和 B」「总结关于 Z 的内容」

**只读知识页**；但仍写 `log.md`。不要通读 AGENTS，不要一次加载整库，不要读 okf / source-wiki-cli。

**流程：**
1. 读 `wiki/index.md`，按问法选起点再读分组 index：
   - 是什么 / 内部概念 → `基础知识/`
   - 哪一套 / 入口 / 负责人 → `资源目录/`
   - 怎么做 / 变更 / 回滚 → `操作手册/`
   - 为什么 / 选型 → `架构决策记录/`
   - 短问答 / 报错释义 / 排查 → `常见问题/`
   - 历史事件 / 案例 → `案例与复盘/`
2. 无命中或跨分组时，搜文件名、frontmatter（`title`/`aliases`/`tags`/`owner`）与正文；命中后再打开 2–5 篇；偏好 `updated` 较新的页
3. 沿正文 `[[双链]]` 或 Obsidian backlinks 最多两跳
4. `wiki/` 不足 → 搜 `raw/`，标注「⚠️ 未编译」；两边都没有 → 说未检索到并建议入库
5. 综合作答并引用仓根相对路径；末尾「源头链接」取 `sources`；命令/主机名只来自已打开页
6. 有价值的综合结论主动问是否回写（同意后走 Ingest）
7. 在 `wiki/log.md` 追加一行

**输出形态：** Markdown 页、对比表、幻灯片（Marp）、图表（有工具才用）

---

### 4. Lint / Maintain (lint)

检查 wiki 健康状况，含内容新鲜度与 schema 健康。

**何时：** 用户说「检查 wiki 健康」「lint wiki」「清理知识库」——建议定期做

**流程：**
1. **机械门禁 + 基础健康检查：**
   ```bash
   python tools/okf-lint/okf_lint.py
   ```
   先修 error。可自动修：index 与文件不一致、唯一可解析的断链。另查：跨页矛盾、过时内容、孤儿页、缺页、断链、可补缺口（公网搜索需许可；内网 wiki 不用 WebFetch）。

2. **内容新鲜度检查：**
   - 扫描 `raw/`（含 `raw/wiki/archive/`）：file_modified vs content_date
   - 标出旧 raw 对应的过时 wiki 页；按新鲜度优先级汇报

3. **Schema 健康检查：**
   - 确认 `AGENTS.md` 与 `wiki/index.md` 反映真实分组
   - 检查约定是否仍然有效（询问用户）
   - 若工作流已演变，建议更新 Skill / AGENTS

4. 向用户汇报发现
5. 提议修复问题
6. 更新 `log.md`

**审核：** 列 `draft` / 无 `verified` / 已过期页。人明确说通过并给出身份后才写 `verified.by: human:<id>` 与 `status: stable`。Agent 不得自行标 verified。

---

### 5. Search (search)

对 wiki 做全文检索。

**何时：** 用户说「搜索 X」「找出所有关于 Y 的内容」

**流程：**
1. 若有 qmd 可用则用（BM25/向量混合检索）
2. 否则 Grep/Glob 遍历 `wiki/`
3. 给出带上下文的结果
4. 提议打开相关页
5. 写 `log.md` 一行

---

## Wiki 结构约定

### index.md 格式

与现网一致（示意）：

```markdown
---
okf_version: "0.2"
---

# 基础设施知识库

## L0 基础知识

* [基础知识](./基础知识/index.md) - 内网特有概念与平台
  * [网络管理](./基础知识/网络管理/index.md) - 黄绿区、证书、DNS…

## L1 资源目录（部署实例）

* [资源目录](./资源目录/index.md) - 哪一套、在哪、谁负责
  * [集群](./资源目录/集群/index.md) - …

## 运维与设计

* [操作手册](./操作手册/index.md) - …
* [常见问题](./常见问题/index.md) - 短问答与排查
* [架构决策记录](./架构决策记录/index.md) - …
* [案例与复盘](./案例与复盘/index.md) - …
```

分组 `index.md` 条目：`* [中文 title](./页.md) - 短描述`。

**⚠️ 目录入口链接必须指向 `index.md`，禁止指向目录本身。** Obsidian 的链接解析只认文件，`(./目录名/)` 会显示「未创建」。正确写法：`* [分组名](./分组名/index.md)`。子分组同理：`* [子分组](./子分组/index.md)`。普通知识页仍用 `* [页名](./页名.md)`。

---

### log.md 格式

```markdown
# 更新日志

## 2026-09-03

* **Creation**: 新建 [黄绿区](/wiki/基础知识/网络管理/黄绿区.md)。
* **Update**: ingest compiled https://wiki.example/WIKI… → …
* **Update**: query | 绿区代理怎么配 — 引用 3 页。
```

| 动词 | 何时 |
|------|------|
| `**Creation**` | 新建概念页 |
| `**Update**` | 改页 / index / ingest / query / lint / search |
| `**Deprecation**` | 废弃一页 |
| `**Initialization**` | 建目录结构 |

动词后用 ASCII `:`。链接用仓根路径。公司 wiki：`ingest compiled|skipped|failed|no material` + URL。

---

### 页面格式

完整 type / 固定标题 / frontmatter 见 [references/okf.md](references/okf.md)。最小示意：

```markdown
---
type: Foundation   # 或 Registry | Runbook | FAQ | ADR | Incident
title: 黄绿区
description: 内网黄区/绿区划分与访问约束。
status: draft
owner: 张三
updated: 2026-09-03
sources:
  - https://wiki.example/WIKI…
---

## 定义

…

## 职责与边界

…

## 公司内使用方式

…

## 稳定约束

…

## 关系

- [[相关页]]
```

**type：** `Foundation` | `Registry` | `Runbook` | `FAQ` | `ADR` | `Incident`（目录与固定中文 `##` 见 okf；不要用 Summary/Key Details 模板）。

**重要：** 入库时采集来源日期（content_date / file_modified），供新鲜度判断。

---

## 用户交互模式

### 查询与综合
- 先读 index，再打开相关页；引用路径作答
- 有价值的综合结论提议写回 wiki

### 入库与更新
- 澄清写入范围（分组名）与是否「缺的也建」
- LLM 出 draft → 人审核 verified → `stable`

### 团队协作
- 明确 LLM 与人的职责：Agent 记账与起草，人把关事实与发布
- 大范围变更先 Plan 再写

---

## 最佳实践

1. **始终记日志** — 每次 ingest / query / search / lint 都写入 `wiki/log.md`
2. **维护 index** — 分组 index 与文件一致
3. **双链是写入义务** — 每页写完后必须：(a) 新页正文 `[[双链]]` 链向已有页；(b) 已有页回链新页（双向互链）。「暂无关联」**仅限全库确认无任何相关页**时使用，禁止用它逃避链接义务
4. **标出矛盾** — 不要静默覆盖，展示给用户
5. **保存有价值输出** — 好的查询综合应变知识页
6. **尊重来源** — `raw/` 默认不可变（公司 wiki 仅追加 inbox / 写 archive）
7. **建议，勿臆断** — 大改前与用户确认
8. **禁止一来源一页** — 先拆 L0 再长上层

---

## 交叉引用原则

1. 溯源写在 frontmatter `sources`（公司 wiki = 原始 URL）；正文自洽，查询默认不打开 `raw/`
2. 新来源优先**更新旧页**，而不是新建近似页
3. 基础知识页「关系」节与上层页正文 `[[双链]]` 形成网络
4. 跨来源主题要标出共用点

**格式：** 语义关联用 `[[页]]` / `[[页#标题]]` / `[[页#^block-id]]`。导航可用 Markdown 链接。

**⚠️ wikilink 目标必须与文件名精确匹配（含大小写与空格）。** Obsidian 按**文件名**（不含 `.md`）解析 `[[...]]`，而非按 frontmatter `title`。例如文件 `harbor镜像仓.md` 的 wikilink 是 `[[harbor镜像仓]]`，不能写成 `[[Harbor 镜像仓]]`（title 写法）——否则 Obsidian 找不到文件，产生断链。规则：
- `[[文件名]]`：文件名 = 去掉 `.md` 后的实际 basename（含大小写、空格）
- `[[文件名#标题]]`：`#` 前必须同上
- 建议文件名与 `title` 保持一致以减少歧义；若两者不同，wikilink 永远跟文件名

### 知识关联发现（操作清单）

处理每条来源时（含第 1 条），按以下清单逐项检查：

- [ ] **概念命中**：Grep `wiki/基础知识/` 中正文和 frontmatter `title`/`aliases`/`tags`，看是否有已入库的同概念页 → 有则更新，不新建近似页
- [ ] **资产命中**：Grep `wiki/资源目录/` 看是否有同技术栈的 Registry 页 → 有则更新其正文 `[[双链]]`
- [ ] **运维命中**：Grep `wiki/操作手册/` `wiki/常见问题/` 看是否已有同主题手册/FAQ → 新内容是补充还是替代？
- [ ] **矛盾扫描**：新事实是否与已有页冲突 → 显式标出，不静默覆盖
- [ ] **互补扫描**：新内容是否只是补步骤/补例子 → 更新已有页而非新建
- [ ] **概念演进**：同一概念侧重点变化 → 综合进 Foundation，上层引用新约束
- [ ] **跨来源收敛**：多条来源的重复点 → 收敛到基础知识或资源目录，不分散在多页

清单执行结果汇入 Ingest 步骤 6（交叉引用编织）。

---

## 典型入库规模

一篇中等公司 wiki / runbook（约 2000–3000 字）通常：
- 新建 2–4 页（1–2 基础知识 + 资源目录或手册/FAQ）
- 更新 2–4 个已有页
- 合计触碰约 5–8 个文件

这是正常现象——知识库在互联中生长。整篇缩成一页，或拆成十几页碎片，都要纠偏。

---

## 工具

### 读取来源内容

| 来源 | 工具 | 说明 |
|------|------|------|
| **公司 wiki URL** | `python tools/wiki-export/wiki_export.py export <url>` | 通过 `wiki` CLI 导出到 `raw/wiki/archive/`，含图片下载 |
| 公司 wiki 批量 | `python tools/wiki-export/wiki_export.py export <url1> <url2>...` | 一次导出多条，串行调用 wiki CLI |
| 公司 wiki 增量刷新 | `wiki_refresh.py diff` + `wiki_export.py re-export` | 见 source-wiki-cli §增量刷新 |
| 公司 wiki 元数据 | `wiki doc get <url>` | 直接调用 wiki CLI 获取标题/更新时间等 |
| 公网 URL | `defuddle parse <url> --md` | 落 `raw/` 后编译 |
| 本地文件 | Read | 直接读取 |

**其他工具：**
- **Read/Write/Edit**：读写 `wiki/` 知识库页面（及公司 wiki 允许的 `raw/wiki/`）
- **Glob/Grep**：搜索与导航
- **WebSearch/WebFetch**：补公网缺口（需许可）
- **okf-lint**：`python tools/okf-lint/okf_lint.py`
- **qmd / Marp / Dataview / Obsidian CLI**：可选；失败则普通 Read/Write，不阻塞

**⚠️ 禁止：** 用 Read/Defuddle/WebFetch 读取公司内网 wiki URL。

权威顺序：OKF > 本 Skill > Obsidian 便利

---

## 快速开始

本仓通常**已初始化**。用户第一次提到知识库时：

1. 简短说明分层（基础知识 → 资源目录 → 手册/FAQ/ADR/案例）
2. 问当前目标：查询 / 入库 / 体检 / 其他
3. 导向对应操作；仅明确要求从零建库时走 Init

根据其回答决定优先执行哪些操作。
