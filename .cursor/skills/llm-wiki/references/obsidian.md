# Obsidian 适配层

Obsidian **不是**必需依赖。本机未开 Obsidian / 无 `obsidian` CLI 时，ingest 用普通 Read/Write 即可。

当用户把本仓当 vault，且 Obsidian 正在运行时，Code Agent **可以**在编译 wiki 时使用相关 skill 辅助。

## 何时用哪个 Skill

| 场景 | Skill | 说明 |
|------|-------|------|
| 创建/更新/搜索 vault 内笔记、设 property | `obsidian-cli` | 需 Obsidian 已打开；`path=` 用相对 vault 根路径（如 `wiki/操作手册/页.md`） |
| 编辑 wikilinks、callouts、embeds | `obsidian-markdown` | frontmatter 仍按 [okf.md](okf.md)；跨目录链接优先 OKF `/分组/页.md` |
| 系统拓扑 / 排查树可视化 | `json-canvas` | 可选 `.canvas`，不替代 OKF 概念页、不承载可操作步骤 |
| 按 type/domain/tags 做值班视图 | `obsidian-bases` | 可选 `.base`，从 frontmatter 聚合 |
| 抓取**公网**文档进 raw | `defuddle` | **禁止**用于公司内网 wiki（走 [source-wiki-cli.md](source-wiki-cli.md)） |

## 编译 wiki 时如何用（可选）

在 [ingest.md](../ingest.md) / 公司 wiki 编译阶段，若 Obsidian 可用：

1. **先读**项目或全局 `obsidian-cli` Skill，再跑 `obsidian help`（不要臆造子命令）。
2. **查重**：`obsidian search` 找是否已有同名/同主题页，避免平行副本。
3. **写页**：可用 `obsidian create` / `append` / `property:set` 写入 `wiki/...`；内容仍须符合 [okf.md](okf.md)（`type`、固定标题、`sources`、`attachments/`）。
4. **附件**：图片仍落在知识页同目录 `attachments/`；CLI 不能替代拷贝二进制时，用 Shell/文件系统拷贝后再改 markdown 图链。
5. **失败回退**：CLI 报错、vault 未打开、路径不对 → 立即改用普通 Write/StrReplace，不要卡住整批 ingest。

权威顺序：**OKF 规则 > llm-wiki ingest 流程 > Obsidian 便利性**。

## 边界

- Query / Lint 默认仍读 Markdown 文件；Obsidian 是加速，不是查询唯一入口。
- 禁止为了用 Obsidian 而改写链接风格（不要默认改成 `[[wikilink]]`，除非用户明确要求且 lint 仍可通过）。
- `raw/` 默认不要当可编辑笔记区；公司 wiki 存档只经 source-wiki-cli 通道写入。
- Canvas / Bases 产出不是知识正文；值班结论仍须写回 OKF 概念页。

## 推荐工作流

1. Clone 整仓 → Obsidian 打开为 vault（vault 根 = 仓根）。
2. Agent 用 llm-wiki 做 ingest/query/lint；有 CLI 时按上表辅助写页。
3. 人用 Obsidian 阅读、批注；确认后更新 `verified`。
4. 可选 Bases / Canvas 做视图，不重复写事实。
