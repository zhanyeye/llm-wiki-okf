# llm-wiki Skill 演进方案

基于四个参考项目的调研结论，为 `.agents/skills/llm-wiki/` 与配套框架制定的后续优化建议与设计。
状态：**提案**（未实施）。日期：2026-08-29。

## 输入项目与各自的可借鉴点

| 项目 | 定位 | 对本仓的价值 |
|------|------|--------------|
| [Karpathy gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | 思想源头（raw/wiki/schema 三层 + ingest/query/lint） | 本仓已继承；再借鉴"查询结论回写复利"与"index.md 在中等规模出人意料地好用" |
| [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)（2.1k★） | 生产验证（94 页/13 分组）后的通用 Skill | 最有价值的是**拒绝清单**：明确不做 source-hash、置信度、访问衰减、向量检索（grep 在 5–10 万 token 内够用）、typed ontology；且明确放弃 OKF（规范未成熟） |
| [lewislulu/llm-wiki-skill](https://github.com/lewislulu/llm-wiki-skill)（650★） | Skill + 人→LLM 反馈工具链 | **log/ 按天目录**（多人协作）、**audit 人工纠错文件**、scaffold/lint 脚本化；Web 查看器与 Obsidian 插件不搬 |
| [tobi/qmd](https://github.com/tobi/qmd)（29k★） | 全本地 CLI 检索引擎 | 中文语料需要 Qwen3-Embedding-0.6B（640MB）；`vsearch` 档位够用；项目内索引 + MCP 常驻；内网需离线装模型 |

## 设计原则（从四项目提炼，后续增删功能先对照）

1. **编译复利**（Karpathy）：每次 ingest/query/lint 都要让库比之前更好——查询结论回写、未命中留痕，禁止结论只留在聊天窗口。
2. **边界先行**（Astro-Han）：每个新功能先问"它是否在拒绝清单里"。清单见 §明确不做。
3. **人进回路**（lewislulu）：值班场景必须有人工纠错的低成本通道，且通道本身必须是纯 markdown（不依赖平台）。
4. **工具按证据引入**（Karpathy + Astro-Han + qmd）：80 篇内 grep + index 够用；检索加速等 query-miss 证据出现再上。
5. **单一权威**：每类约定只在一处文件维护（本方案 P0-3 专门收敛现状的三处重复路由表）。

## 现状差距

| 能力 | 本仓现状 | 差距动作 |
|------|----------|----------|
| ingest/query/lint 三操作 + index/log 闭环 | ✅ 比 Astro-Han 更强（OKF type 体系、固定标题） | — |
| 公司 wiki 增量通道（inbox + wiki_export.py） | ✅ 四项目中独有 | — |
| log 并发友好 | ❌ 单文件 `wiki/log.md` 顶部插入，多会话/多人必冲突 | **P0-1 目录化** |
| 人工纠错回路 | ❌ 页面错了只能人改或等 lint | **P0-2 audit 通道** |
| 约定单点维护 | ❌ 路由/必读清单在 AGENTS.md、SKILL.md、ingest.md 三处重复 | **P0-3 收敛** |
| 刷新入口 | ❌ 增量刷新是高频操作但无命令 | **P1-1 `/refresh`** |
| 批量建页工具 | ❌ Phase 2 迁 80 篇全靠 agent 手写 | **P1-2 scaffold** |
| 中文语义检索 | ❌ 只有 grep/关键词 | **P2-1 qmd（证据门控）** |
| 未命中留痕 | ❌ | **P2-2 QueryMiss** |

---

## P0-1 log 目录化（借鉴 lewislulu）

**动机**：单文件 + 最新日在上 + 当天条目顶部插入 = 多人/多会话每次写 log 必冲突；文件无限膨胀，agent 每次写要加载全量。

**设计**：

- `wiki/log/` 目录，一天一文件，文件名 `YYYYMMDD.md`（lint 校验 regex `^\d{8}\.md$`，目录内禁止其它文件）。
- 文件内：H1 为 ISO 日期（`# 2026-08-29`）；条目沿用现有格式 `* **动词**: 说明，并链 [标题](/wiki/...)`；**新条目追加在文件末尾**（append-only，同日多会话各追加不同行，git 大多可自动合并）。
- 动词表不变（Creation/Update/Deprecation/Initialization + ingest 固定句式），P2-2 会新增 `QueryMiss`。
- 全局时间线靠 grep：`grep -rh "^\* \*\*" wiki/log/`；按 URL 过滤已处理项的现有用法不受影响（`grep -rh "pageId=12003" wiki/log/`）。
- 迁移：现有 `wiki/log.md` 按日拆成 `log/2026082*.md`，原文件删除（git 历史即存档）。
- `wiki/log/` 不是知识分组：不建 `index.md`、不进 `wiki/index.md`。

**改动面**：`references/index-log.md` §log.md 重写、`lint.md`、`tools/okf-lint/okf_lint.py`（log 校验规则）、`ingest.md`/`query.md` 中对 log 的引用、`AGENTS.md` 一处提及、迁移现有 log.md。

**验收**：lint 通过；两个会话同日各写一条互不冲突；`grep -rh` 时间线可用；查询"某 URL 是否已 ingest"与现状等效。

## P0-2 audit 人工纠错通道（借鉴 lewislulu，纯 markdown 化）

**动机**：值班时发现页面错误/过期，高频场景是"没空当场改，但必须记下来"。目前没有这个通道，错误只能靠人肉记住或等 lint 碰运气。lewislulu 的 audit 文件模式（锚定原文 + 严重级 + open/resolved）用纯 markdown 即可实现，不依赖它的 Obsidian 插件。

**设计**：

- 目录：`wiki/audit/open/` 与 `wiki/audit/resolved/`（目录即状态）。
- 文件名：`YYYYMMDD-HHMMSS-<slug>.md`。
- frontmatter：`target`（被质疑页的仓根绝对路径）、`anchor`（引用的错误原文片段，供精确定位）、`severity`（`block` / `warn` / `note`）、`reporter`、`date`。正文 ≤5 行：问题 + 建议改法（可空）。
- 产生途径（三条，都不强制装任何东西）：
  1. 人直接在 Obsidian/编辑器里建文件；
  2. 对 agent 说"这条答案不对" → agent 按格式建 audit 文件（写入 `ingest.md` 或 `query.md` 各一句）；
  3. lint 发现 stale 但无法自动修时，可降级为建 warn 级 audit 而不是硬改。
- 消化途径：`lint.md` 新增第 0 步"先列 open audit"；处理 = 修页 → 文件移入 `resolved/` → log 写一条 `**Update**`。okf-lint 报告 open 总数与 block 数。
- 边界：audit 文件不是知识页——不进任何 index、不算概念页、不参与交叉引用；`resolved/` 保留作为决策痕迹（文件极小，不清理）。

**改动面**：新增 `.agents/commands/audit.md`、`lint.md` 增节、`okf_lint.py` 校验 audit 文件 frontmatter 完整性、`okf.md` 或 `index-log.md` 加一小节格式定义（建议放 index-log.md，与 log 同属"记账类"）。

**验收**：从"人指出错误"到"页被修正"全程留痕；值班中建一条 audit ≤30 秒；lint 能报出未处理数。

## P0-3 约定单点收敛（本次自检发现）

**动机**：必读文件清单目前维护在 `AGENTS.md` 表、`SKILL.md` 路由表、`ingest.md` 分流表三处，公司 wiki 行在两处各列 4–5 个文件。加一种意图要同步三处，已经发生过漂移风险。

**设计**：

- `SKILL.md` 路由表为**唯一权威**；
- `ingest.md` 分流表只保留"触发 → 走本文件哪一节 + 哪个 reference"，删除重复的必读清单（表头注明"必读组合以 SKILL.md 路由为准"）；
- `AGENTS.md` 表保留（人读索引的职责），但表下加一行：*"明细以 SKILL.md 路由表为准，两处不一致时按 SKILL.md 执行"*。

**验收**：新增一个意图只改 SKILL.md + 新意图文件两处。

## P1-1 命令层补全（半天）

已有 `/query` `/ingest` `/lint`，补两个对应现有高频意图的：

- `.agents/commands/refresh.md` → 公司 wiki 增量刷新（source-wiki-cli §增量刷新）。这是日常最高频操作，现在没有命令入口。
- `.agents/commands/audit.md` → 列出并处理 open audit（随 P0-2 一起做）。

## P1-2 scaffold 工具（一天，服务 Phase 2）

**动机**：Phase 2 要迁约 80 篇，逐篇手写 frontmatter + 8 种固定标题骨架 + index 条目，格式错误全靠 lint 事后抓。lewislulu 的 `scaffold.py` 证明这一步可以脚本化。

**设计**：`tools/okf-scaffold/scaffold.py`（遵循"一个工具一个子目录"约定）：

- 输入：`--type Runbook --title "重置 xx 密码" [--dir wiki/操作手册]`；type→目录映射直接读 `references/okf.md` 的表（避免硬编码两份）；
- 产出：骨架页（frontmatter `status: draft` + 该 type 固定 `##` 标题，正文一律"来源未写"）+ 对应分组 index 追加条目 + 提示 agent 补 log 条目；
- agent 在 ingest.md Compile 步可选用；批量迁移时先 scaffold 后填肉。

**验收**：一条命令产出的骨架页 `okf_lint.py` 零 error；type→目录与 okf.md 无第二份硬编码。

---

## P2-1 qmd 检索层（证据门控，Phase 4 或提前触发）

**动机**：中文语料下 grep/FTS5 召回弱（分词问题）；但 Astro-Han 的生产结论是 grep 在 5–10 万 token 内够用，Karpathy 也把 qmd 定位为"index.md 不再够用时"的可选项。所以**不预设上线时间，由证据触发**：

- 触发条件（满足其一）：`wiki/` 概念页 > 100 篇；或 P2-2 的 QueryMiss 记录显示月未命中 ≥ 10 次；或用户主动要求语义搜索。

**设计**：

- 地位：可选加速器，与 `references/obsidian.md` 同级——新增 `references/search-qmd.md`；权威顺序：OKF 规则 > llm-wiki 流程 > qmd 加速；不可用即回退 grep，不阻塞。
- 配置收敛到最小：
  - 只装一个模型：`QMD_EMBED_MODEL` 指向 Qwen3-Embedding-0.6B-Q8_0（640MB，119 语言）；**内网在外网下载 GGUF 后配本地文件路径**，不依赖运行时连 HuggingFace；
  - 只用 `qmd search`（BM25，零模型兜底）+ `qmd vsearch`（语义）；**不装** expansion 1.7B 与 reranker 0.6B，不用 `query` 命令；
  - 项目内索引：`qmd init` → `.qmd/index.yml` **提交进仓**；`.qmd/index.sqlite` **gitignore**（含机器绝对路径的二进制），同事 clone 后 `qmd update && qmd embed` 重建（几十秒）；
  - 环境要求写进 search-qmd.md：Node ≥ 22；Windows 用 CPU 或 Vulkan 后端（CUDA 并发有崩溃前科，`QMD_EMBED_PARALLELISM` 默认 1）。
- `query.md` §导航与召回改造：qmd 可用时 `vsearch` 优先 → 命中页照常走"打开 2–5 篇作答"；不可用时现有 grep 流程原样保留。
- 与 lint / ingest 完全解耦：qmd 坏了不影响写入闭环。

**成本**（已核实）：磁盘 +640MB + 索引几 MB；CLI 模式静止时零占用，单次查询热态约 1 秒（含模型加载）；嫌慢切 `qmd mcp` 常驻（会话期亚秒，空闲 5 分钟自动卸载推理上下文）。

**验收**：同义改写类查询（如"容器拉起"命中写的是"重启 pod"的页）能命中 grep 搜不到的页；断网 + 无 HF 环境下可完整重建索引。

## P2-2 QueryMiss 留痕（Karpathy 复利原则，随 P0-1 顺带做）

**动机**：查询未命中有双重价值——内容缺口 backlog（指导下一批入库）+ P2-1 的门控证据。目前"未检索到"说完就蒸发。

**设计**：

- `index-log.md` 动词表新增一行：`**QueryMiss**: 纯查询未命中（不链页），写检索词与改写过的变体`；
- `query.md` §流程末尾加一句：返回"未在 wiki 中检索到"前，在当日 log 追加 QueryMiss 条目；
- lint 报告输出"近 30 天 QueryMiss 数与高频词"，作为 Phase 2 入库优先级与 P2-1 触发判断的输入。

**验收**：未命中可被 grep 汇总；QueryMiss 高发词出现在 lint 报告里。

---

## 明确不做（拒绝清单，增功能前先读）

继承 Astro-Han 的生产结论 + 本仓自身判断：

1. **source-hash 追踪、行号级引用、数值置信度、逐篇 review 日期、访问衰减**——"常被问到"不等于"正确"，这些元数据维护成本高于价值；
2. **自建向量库/图数据库**——检索加速只经 qmd 一个入口，且由 P2-1 证据门控；qmd 之外不引入任何检索基础设施；
3. **typed ontology / 结构化数据库**——OKF 子集已是上限，不再加 type 字段；
4. **lewislulu 的 Web 查看器与 audit Obsidian 插件**——浏览归 Phase 4 的 Obsidian；audit 保持纯 markdown；
5. **OKF 全量合规**——只跟 v0.2 子集（okf.md 已文档化）；上游 spec 变更不自动跟升，Astro-Han 弃用 OKF 的理由（规范未成熟）视为持续有效的风险提示；
6. **多 agent 并发写同一页**——不引入锁机制，靠 git 纪律 + P0-1 的按天 log 把冲突面压到最小。

## 路线映射与实施顺序

对齐 AGENTS.md 现有 Phase 0–4，不重排路线图：

| 现有阶段 | 本方案项 | 量级 |
|----------|----------|------|
| Phase 0（框架，当前） | P0-1 log 目录化、P0-2 audit、P0-3 收敛、P1-1 命令、P2-2 QueryMiss | 合计 2–3 天，可拆成多个独立 PR |
| Phase 1（按痛点补） | P0-2 audit 在值班实战中打磨格式 | 0（使用中迭代） |
| Phase 2（迁 80 篇） | P1-2 scaffold 投产；期间积累 QueryMiss 数据 | 1 天 + 迁移期观察 |
| Phase 3 | 不变 | — |
| Phase 4（浏览与搜索） | P2-1 qmd 接入（或被证据提前触发） | 1 天（含 search-qmd.md 与配置） |

**建议首个 PR**：P0-1 + P0-3 + P2-2（都是改 index-log.md / lint / skill 文本，互相耦合最小、一起验收）；P0-2 + P1-1 作第二个 PR；P1-2、P2-1 各自独立排期。
