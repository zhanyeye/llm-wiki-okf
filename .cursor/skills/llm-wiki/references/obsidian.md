# Obsidian 适配层（可选 / 未来）

Obsidian 不是当前 ingest/query/lint 的必需依赖。仅在用户明确要求或 Phase 4 浏览场景时使用。

## 何时用哪个 Skill

| 场景 | Skill | 说明 |
|------|-------|------|
| 把本仓作为 Obsidian vault 浏览/编辑 | `obsidian-cli` | 读/写/搜索笔记；开发插件时用 reload/screenshot |
| 编辑 wiki 页 wikilinks、callouts、embeds | `obsidian-markdown` | 与 OKF 正文兼容；frontmatter 仍按 [okf.md](okf.md) |
| 可视化知识图、排查树 | `json-canvas` | 可选 `.canvas` 文件，不替代 OKF 概念页 |
| 表格视图、过滤、公式 | `obsidian-bases` | 可选 `.base` 文件，从 frontmatter 聚合 |
| 抓取**公网**文档进 raw | `defuddle` | **不用于**公司内网 wiki（内网 wiki 走 [source-wiki-cli.md](source-wiki-cli.md)） |

## 边界

- **Query / Lint 默认路径不变**：仍从 `wiki/index.md` 渐进式读 Markdown；Obsidian CLI 是可选加速，不是替代。
- **写入仍走 llm-wiki ingest**：Obsidian 里手改的页若需正式入库，仍应满足 OKF frontmatter 并跑 lint。
- **vault 根目录**：若整仓作 vault，`wiki/` 是 OKF bundle；`raw/` 可设为排除或只读文件夹（Obsidian 侧配置，不在 skill 中强制）。
- **链接**：OKF bundle 内跨目录链接用 `/分组/页.md`；Obsidian wikilinks `[[页]]` 仅在用户明确要求 Obsidian 风格时采用，且 lint 前须与 okf.md 链接规则一致。

## 推荐 Phase 4 工作流

1. Clone 整仓 → Obsidian 打开为 vault。
2. 日常仍用 Agent + llm-wiki skill 做 ingest/query/lint。
3. 人用 Obsidian 阅读、加注释；确认过的页更新 frontmatter `verified`。
4. 可选：用 Bases 做按 `type` / `domain` / `tags` 的值班视图；用 Canvas 画系统拓扑（引用 wiki 页，不重复写事实）。
