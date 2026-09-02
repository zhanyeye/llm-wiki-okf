# Obsidian 与周边 Skill（编译增强）

本仓常作为 Obsidian vault（vault 根 = 仓根）。编译 / 整理 `wiki/` 时，在合适场景**主动**使用下列项目 Skill；未开 Obsidian 或工具失败时回退普通 Read/Write，**不要**阻塞 ingest。

权威顺序：**OKF 规则 > llm-wiki ingest > Obsidian 便利**。

## 用哪个

| 场景 | Skill | 怎么用 |
|------|-------|--------|
| Resolve 消歧、写/改页、设 frontmatter | `obsidian-cli` | Obsidian 已打开时：先读该 Skill → `obsidian help`；`search` / `backlinks` 查重与查关系；`create` / `append` / `property:set` 写 `wiki/...`（`path=` 相对仓根） |
| 内容级语义关系、callout / embed | `obsidian-markdown` | 导航与来源仍用 Markdown 链接；语义关系按 okf.md 使用 `[[页#标题]]`，关键稳定事实使用 `[[页#^block-id]]` |
| Architecture / 复杂排查树要画示意 | `json-canvas` | 可选同目录或分组下 `.canvas`；**不**替代概念页，**不**把可操作步骤只写在画布上 |
| 按 type / domain / tags / status 做视图 | `obsidian-bases` | 可选 `.base`（如 draft 总览、按 domain）；用户要视图或整理浏览时再做，**不要**每篇入库新建一个 base |
| 用户给了**公网**文档 URL 要入库 | `defuddle` | `defuddle parse <url> --md` 落 `raw/` 再走 ingest。**禁止**用于公司内网 wiki（走 [source-wiki-cli.md](source-wiki-cli.md)） |

## 编译时建议顺序

1. **取源**：公网 URL → `defuddle`；公司 wiki → `wiki_export.py`；已有 raw → 只读。
2. **Resolve**：优先 `obsidian search` 查名称/别名，用 `backlinks` 查反向关系；否则用全文搜索。不得只按文件名判断同一实体。
3. **Compose**：按 L0 → L1 → L2 写页。可用 `obsidian-cli` 写入；图片仍 `./attachments/`。
4. **Link**：首次链接优先标题级；只有事实稳定且会被多处复用才添加块 ID。用 backlinks 检查上层影响面，反向关系不重复手写。
5. **Validate**：确认每个 wikilink 的页、标题或块存在；Obsidian 不可用时由 okf-lint 完成同类机械检查。
6. **可选可视化 / 视图**：Architecture 确需示意 → `json-canvas`；Registry/type/domain/status 聚合 → `obsidian-bases`。Base 不是第二份资产数据。
7. **失败回退**：CLI 报错、vault 未开 → 使用普通文件工具继续完整六阶段，不降低质量门。

## 边界

- Query / Lint 默认仍读 Markdown；Obsidian 是加速，不是唯一入口。
- Canvas / Bases 不是知识正文；结论写回 OKF 概念页。
- `raw/` 默认只读；公司 wiki 存档只经 source-wiki-cli。
- 不要求所有文本都变成 wikilink。导航、来源和外链保持 Markdown；只有有类型的知识关系使用双链。
