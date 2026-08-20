# ingest

把 `raw/` 或对话里的故障结论变成 wiki 页。

1. 读 `raw/` 里对应材料（若有）。**不要修改 raw。**
2. 按 [`AGENTS.md`](../../../AGENTS.md) 的 type 表选目录。操作手册：流程用 `Runbook`，配位置用 `Configuration`。
3. 套 [`templates/`](../../../templates/) 同名模板（小写文件名，如 `runbook.md`）。
4. 一篇来源可以改多页：注册表、架构页、手册、`故障排查/index.md` 的待入库行。
5. 交叉链接用 bundle 绝对路径。
6. 更新被改目录的 `index.md`；新分组条目再改根 `index.md`。
7. 在 [`wiki/log.md`](../../../wiki/log.md) 最新日期下追加 `**Creation**` 或 `**Update**`。日期 `YYYY-MM-DD`，最新日在上。
8. `generated.by`：人写用 `human:<id>`；Agent 写用 `agent/<model>`。新页 `status: draft`。`stale_after` 默认 180 天后。

可复用的步骤从 Incident 抽到 Runbook 或 Playbook，不要只停在复盘页。
