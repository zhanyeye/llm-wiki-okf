# ingest

把 `raw/`、对话里的故障结论、或要迁入的旧文档写成 wiki 页。

**分流：** 对话贴了公司 wiki 链接要入库，或 `raw/wiki/inbox.md` 非空，或用户要求继续下一批 / 重试失败项 → **停读本文件**，改走 [ingest-wiki.md](ingest-wiki.md)。其它来源继续下面步骤。

1. 有 raw 就读；**不要改 raw**（`raw/wiki/` 例外见 ingest-wiki）。密钥、token、kubeconfig 不要抄进 wiki。步骤、入口、命令写进知识页正文，使页可脱离 raw 阅读。
2. 读 [types.md](types.md) 选 type/目录与固定标题；按 types 填 frontmatter。工单/纪要等 `sources` 用仓内路径（如 `raw/tickets/...`）。
3. **故障关闭**：事实写入 `Incident`；以后还能复用的步骤写入或更新 `Playbook` / `Runbook`。把 `wiki/故障排查/index.md` 里对应「待入库」改成链接。
4. **迁旧文档**：按内容选 type，补 frontmatter（`status: draft`），链到已有 Architecture / Registry，不要另建平行副本。
5. 一篇来源可以改多页；保持交叉引用一致。链接规则见 types.md。
6. 按 [index-log.md](index-log.md) 更新被改目录的 `index.md`、必要时 `wiki/index.md` 与 `故障排查/index.md`，并追加 `wiki/log.md`。
7. 跑 `python tools/okf-lint/okf_lint.py`，先修 error；对 warning 决定补页、改链，或保留尚未写的断链。再看矛盾陈述、孤儿页、故障排查 index 仍为「待入库」但已有正文的项。
