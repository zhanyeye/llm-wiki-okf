# Obsidian 与周边 Skill（编译增强）

本仓常作为 Obsidian vault（vault 根 = 仓根）。编译 / 整理 `wiki/` 时，在合适场景**主动**使用下列项目 Skill；未开 Obsidian 或工具失败时回退普通 Read/Write，**不要**阻塞 ingest。

权威顺序：**OKF 规则 > llm-wiki ingest > Obsidian 便利**。

## 用哪个

| 场景 | Skill | 怎么用 |
|------|-------|--------|
| Triage 查重、写/改页、设 frontmatter | `obsidian-cli` | Obsidian 已打开时：先读该 Skill → `obsidian help`；`search` / `backlinks` 查重；`create` / `append` / `property:set` 写 `wiki/...`（`path=` 相对仓根） |
| 正文里 callout / embed 等 Obsidian 语法 | `obsidian-markdown` | 需要 callout、embed 时读该 Skill。**链接仍按 okf.md**：同目录 `./页.md`，跨目录 `/wiki/分组/页.md`；不要默认改成 `[[wikilink]]` |
| Architecture / 复杂排查树要画示意 | `json-canvas` | 可选同目录或分组下 `.canvas`；**不**替代概念页，**不**把可操作步骤只写在画布上 |
| 按 type / domain / tags / status 做视图 | `obsidian-bases` | 可选 `.base`（如 draft 总览、按 domain）；用户要视图或整理浏览时再做，**不要**每篇入库新建一个 base |
| 用户给了**公网**文档 URL 要入库 | `defuddle` | `defuddle parse <url> --md` 落 `raw/` 再走 ingest。**禁止**用于公司内网 wiki（走 [source-wiki-cli.md](source-wiki-cli.md)） |

## 编译时建议顺序

1. **取源**：公网 URL → `defuddle`；公司 wiki → `wiki_export.py`；已有 raw → 只读。
2. **Triage**：优先 `obsidian search`（可用时）；否则 Grep / 读分组 index。判定 New / Update / No material。
3. **写页**：内容符合 [okf.md](okf.md)。可用 `obsidian-cli` 写入；语法细节用 `obsidian-markdown`。图片仍 `./attachments/`。
4. **可选可视化 / 视图**：用户要拓扑或值班表，或 Architecture 确需示意 → `json-canvas` / `obsidian-bases`；否则跳过。
5. **失败回退**：CLI 报错、vault 未开 → 立刻 Write/StrReplace，继续 index/log + lint。

## 边界

- Query / Lint 默认仍读 Markdown；Obsidian 是加速，不是唯一入口。
- Canvas / Bases 不是知识正文；结论写回 OKF 概念页。
- `raw/` 默认只读；公司 wiki 存档只经 source-wiki-cli。
