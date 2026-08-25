# author

从零写一页：

1. 用 [types.md](types.md) 选 type 与目录。不要把排查写进操作手册，也不要把复盘当手册。
2. 文件名短 kebab 英文；`title` / `description` / 正文固定标题必须中文。frontmatter 与固定标题见 [types.md](types.md)。
3. 填齐 `type`、`title`、`description`、`domain`、`generated`、`stale_after`。`title` 写给人看的中文，不要抄英文 slug。
4. **用 types.md 里该 type 的固定标题**；命令放可复制代码块；写清何时用 / 何时不用。
5. 占位符用 `<cluster>`、`<namespace>`、`<path>`。不要编造内网主机名或密钥。
6. `Registry`：只写申请途径和找谁。`Automation`：说明对应 `script/` 里的文件，不要把 `.py` 正文塞进 wiki。
7. 按 [index-log.md](index-log.md) 更新分组 `index.md` 与 `wiki/log.md`，再跑 lint。
