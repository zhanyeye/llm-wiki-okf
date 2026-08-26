# query

**只读本文件与 `wiki/`。** 不要通读 `AGENTS.md`；不要读 `raw/`；不要一次 Glob/Read 整库；不要读 `ingest.md` / `references/`；不要把仓根 `index.md` / `README.md` / `script/` / `tools/` 当正文。

## 流程

1. 读 `wiki/index.md`（不是仓库根 `index.md`）。
2. 按问题打开分组 index：
   - **现象不明** → `wiki/故障排查/index.md`
   - **已知系统** → 对应分组（如 `wiki/系统与架构/`）
   - **入口 / 负责人 / 日志路径** → `wiki/资源注册表/`
3. 打开相关正文（通常 2–5 篇；没有相关页不要凑数）。看 frontmatter：已过 `stale_after`、或没有 `verified` → 回答里标明「可能过期 / 未经人工确认」。
4. 仍不够：在 `wiki/` 下搜 `title` / `tags` / `services` / `domain`。

## 输出标准

- 引用所用页面路径（对话中用仓根相对路径，如 `wiki/操作手册/页.md`）。
- 命令、主机名、集群名、地址**只来自已打开的页**；页内占位符保持原样，不要替换成臆造值。
- 故障排查 index 中该项为「待入库」、或没有正文 → 回答「没有成文步骤」；可指出最接近的已有页，不要补全内网命令或主机名。
- wiki 里没有的事实 → 说「wiki 里没有」，建议按 [ingest.md](ingest.md) 补；不要编。
- 有价值的排查树 / 对比表：问是否回写成新页（[ingest.md](ingest.md)）。

## Archive（可选）

用户明确要求把对话答案存档进 wiki 时：

1. 按 [references/okf.md](references/okf.md) 选 type/目录写新页；`sources` 链到被引用的 wiki 页（bundle 路径），不写 raw。
2. 始终新建页，不合并进已有概念页。
3. 更新分组 index 与 `wiki/log.md`（见 [references/index-log.md](references/index-log.md)）。
