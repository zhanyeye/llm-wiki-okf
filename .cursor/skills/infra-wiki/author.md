# author

从零写一页：

1. 用 [types.md](types.md) 选 type 与目录。不要把排查写进操作手册，也不要把复盘当手册。
2. 复制 `templates/` 对应文件到目标目录，文件名短 kebab 英文。
3. 填齐 `type`、`title`、`description`、`domain`、`generated`、`stale_after`。其它字段见 `AGENTS.md`。
4. **保留模板标题**；命令放可复制代码块；写清何时用 / 何时不用。
5. 占位符用 `<cluster>`、`<namespace>`、`<path>`。不要编造内网主机名或密钥。
6. `Registry`：只写申请途径和找谁。
7. 按 [ingest.md](ingest.md) 更新 index、log，并跑 lint。
