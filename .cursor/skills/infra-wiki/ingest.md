# ingest

把 `raw/`、对话里的故障结论、或要迁入的旧文档写成 wiki 页。

1. 有 raw 就读；**不要改 raw。** 密钥、token、kubeconfig 不要抄进 wiki。步骤、入口、命令写进知识页正文，使页可脱离 raw 阅读。
2. 读 [types.md](types.md) 选 type/目录，按该 type 的固定**中文**标题写正文；frontmatter 字段与示例也在 types.md。`title` / `description` **必须中文**（可含 MinIO 等专名），禁止把英文文件名或来源英文标题当 `title`。不要套 Karpathy 英文 `# Title` 正文头。`sources` 用仓内路径，例如 `raw/tickets/disk-full.md`。
3. **故障结论：** 必写 `Incident`。步骤以后还能用 → 再写或改 `Playbook` / `Runbook`。把 `wiki/故障排查/index.md` 里对应「待入库」改成链接。
4. **迁旧文档：** 按标题选 type，补 frontmatter（`status: draft`），链到已有 Architecture / Registry，不要另建平行副本。
5. 一篇来源可以改多页。保持交叉引用一致。链接用 `/系统与架构/minio.md` 这种相对 wiki 根的路径（不要 `/wiki/...`）。
6. 按 [index-log.md](index-log.md) 更新被改目录的 `index.md`、必要时 `wiki/index.md` 与 `故障排查/index.md`。
7. 按 [index-log.md](index-log.md) 在 `wiki/log.md` 当日节顶部追加一条（一篇一链，`**Creation**:` / `**Update**:`，ASCII 冒号，最新日在上）。
8. `generated.by`：人 `human:<id>`；Agent `agent/<model>`。`stale_after` 默认 180 天后。
9. 跑 `python tools/okf-lint/okf_lint.py`，先修 error；对 warning 决定是补页、改链，还是保留尚未写的断链。再看：矛盾陈述、孤儿页、故障排查 index 仍为「待入库」但已有正文的项。
