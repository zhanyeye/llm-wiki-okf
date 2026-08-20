# ingest

把 `raw/`、对话里的故障结论、或要迁入的旧文档写成 wiki 页。

1. 有 raw 就读；**不要改 raw。** 密钥、token、kubeconfig 不要抄进 wiki。
2. 读 [types.md](types.md) 选 type/目录，套 `templates/` 对应文件。
3. **故障结论：** 必写 `Incident`。步骤以后还能用 → 再写或改 `Playbook` / `Runbook`。把 `wiki/故障排查/index.md` 里对应「待入库」改成链接。
4. **迁旧文档：** 按标题选 type，补 frontmatter（`status: draft`），链到已有 Architecture / Registry，不要另建平行副本。
5. 一篇来源可以改多页。链接用 `/系统与架构/minio.md` 这种 bundle 路径。
6. 更新被改目录的 `index.md`；新分组条目才改根 `wiki/index.md`。
7. `wiki/log.md` 顶部日期下追加 `**Creation**` 或 `**Update**`（`YYYY-MM-DD`，最新日在上）。
8. `generated.by`：人 `human:<id>`；Agent `agent/<model>`。`stale_after` 默认 180 天后。
9. 跑 `python scripts/okf_lint.py`，先修 error。
