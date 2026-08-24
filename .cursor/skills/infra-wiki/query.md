# query

**只读本文件与 wiki。** 查询时禁止：通读 `AGENTS.md`；读 `raw/`；`Glob`/`Read` 整个 `wiki/`；读 `ingest.md` / `types.md` / `index-log.md` / `author.md`（写入时再读）；把仓根 `index.md` / `README.md` / `script/` / `tools/` 当正文。

1. 读 `wiki/index.md`（不是仓库根 `index.md`）。
2. 只知道现象 → **必须**打开 `wiki/故障排查/index.md`。
3. 已知系统名 → 打开对应分组 `index.md`（如 `wiki/系统与架构/`）；找入口/负责人/日志路径 → `wiki/资源注册表/`。
4. 打开 **2–5** 篇正文。看 frontmatter：已过 `stale_after`、或没有 `verified`，回答里要说「可能过期 / 未经人工确认」。
5. 仍不够：`rg` 搜 `title` / `tags` / `services` / `domain`（wiki 下中文路径可用）。

**待入库：** `wiki/故障排查/index.md` 里该项是「待入库」→ 回答「没有成文步骤」。可指出最接近的已有页，**不要**补全内网命令或主机名。

**缺页：** 集群名、VIP、凭证、未写步骤 → 说「wiki 里没有」，建议按 [ingest.md](ingest.md) 补。不要编。

有价值的排查树/对比表：问是否回写成新页（[author.md](author.md)）。

**对：** 问磁盘满 → 先看 `wiki/故障排查/index.md`；若是「待入库」就说没有成文步骤。有手册页才引用其中的命令，占位符保持 `<mount>`。  
**错：** 编造主机名、清理目录；Glob 整库；把 `raw/` 当答案来源。
