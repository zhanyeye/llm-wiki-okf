# raw

来源面：工单摘录、会议纪要、截图说明、公司 wiki 导出等。

放入后告诉 Agent 入库。分享知识库请 clone 整仓（含本目录与仓根 `wiki/`）。

## 一般来源

工单、纪要等：人放入本目录对应子目录。Agent **只读、不改、不删**，把知识写进仓根 `wiki/` 对应分组。

## 公司 wiki（例外）

路径：[`raw/wiki/`](wiki/)。**不是**仓根 `wiki/`。

- **人**：对话贴链接，或编辑 [`raw/wiki/inbox.md`](wiki/inbox.md)（一行一个 URL）。不要改 `catalog.yaml`。
- **Agent 允许写**：`catalog.yaml`、`snapshots/`、清理 `inbox.md` 里已入队的行。其它 raw 仍只读。

细则见 Skill [`.cursor/skills/infra-wiki/ingest-wiki.md`](../.cursor/skills/infra-wiki/ingest-wiki.md)。
