# raw

来源面：工单摘录、会议纪要、截图说明、公司 wiki 链接与存档等。

放入后告诉 Agent 入库。分享知识库请 clone 整仓（含本目录与仓根 `wiki/`）。

## 一般来源

工单、纪要等：人放入本目录对应子目录。Agent **只读、不改、不删**，把知识写进仓根 `wiki/` 对应分组。知识页 `sources` 写仓内路径，例如 `raw/tickets/disk-full.md`。

## 公司 wiki（例外）

路径：[`raw/wiki/`](wiki/)。**不是**仓根 `wiki/`。规范出处是公司 wiki **URL**；每个 URL 只留一份本地存档。

```
raw/wiki/
  inbox.md                 # 增量 URL 清单：人可写；对话入库时 Agent 只追加新 URL，不删行
  archive/
    <pageId>/              # 一份存档；刷新整目录覆盖
      page.md
      images/              # 全部图片只在这里
```

- **人**：对话贴链接，或编辑 [`raw/wiki/inbox.md`](wiki/inbox.md)（一行一个 URL，只追加）。`#` 开头整行是注释。
- **Agent 允许写**：把对话里尚未出现的 URL **追加**到 `inbox.md` 末尾；写 `archive/`。禁止删改 inbox 已有行。其它 raw 仍只读。
- 已编译与否看知识页 `sources:`；skipped/failed 记在 `wiki/log.md`（无 catalog）。
- 知识页 `sources` **只写原始 wiki URL**，不写 `archive/` 路径。
- 存档目录名 = URL 里文档 id 参数的**完整取值原样**（不要剥前缀、不要只留数字）；图必须在 `images/`，不得与 `page.md` 同级。
- 编译进 `wiki/` 后：有用图片拷到知识页同目录 `attachments/`（不是 `images/`）。

细则见 Skill [`.cursor/skills/llm-wiki/references/source-wiki-cli.md`](../.cursor/skills/llm-wiki/references/source-wiki-cli.md)。
