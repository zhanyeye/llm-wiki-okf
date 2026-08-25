# ingest-wiki

公司 wiki 增量入库。`raw/wiki/` 是**来源类型**，与仓根 `wiki/`（OKF 知识面）不是同一目录。

触发：对话贴了 wiki 链接并说入库；或「把 inbox 入库」；或「再来 5 个 / 重试 failed / 刷新某 url」。

人**不要**改 [`raw/wiki/catalog.yaml`](../../../raw/wiki/catalog.yaml)。人只贴对话链接，或编辑 [`raw/wiki/inbox.md`](../../../raw/wiki/inbox.md)。

本流程走完后，知识页编译仍遵守 [types.md](types.md) 与 [index-log.md](index-log.md)。查询路径**永不**读本文件或 wiki-cli。

wiki-cli 负责下载；导出后若文件不是「`page.md` + `images/`」，按 §3 整理，验收通过再编译。

## 0. 绑定 wiki-cli（每会话首次导出前必做）

本仓**不** vendor CLI。导出依赖本机已有的 **`wiki` CLI** 与 **`wiki-cli` Skill**。

1. 读 wiki-cli Skill（常见路径：`~/.cursor/skills/wiki-cli/SKILL.md`、项目/用户 skills 下同名目录）。找不到就 `wiki --help` / `wiki-cli --help`。
2. 用 Skill / help 里**真实存在**的「导出页面 + 下载鉴权图片」命令；**禁止虚构 flags**。
3. 导出目标：`raw/wiki/archive/<pageId>/`（`<pageId>` = url 里文档 id 的**完整字符串**，见 §3）。若 CLI 默认写到别处，导出后挪到该路径，或让 CLI 的 output 参数指向该路径。
4. CLI / Skill 都找不到 → **停**，告诉用户先安装/配置 wiki-cli，本批标 `failed` 并写 `note`，不要空编存档。

把本会话实际采用的命令记在回复里一行即可（便于下次对齐），**不要**把私有 CLI 文档抄进本仓。

## 1. 入队（合并 URL）

1. 收集 URL：当前对话里的链接 + [`raw/wiki/inbox.md`](../../../raw/wiki/inbox.md) 非注释行（`#` 开头忽略）。
2. 读 [`raw/wiki/catalog.yaml`](../../../raw/wiki/catalog.yaml)。按 **url 精确匹配** 去重：
   - 新 url → 追加 `{ url, status: pending }`（**不要**写 `id`）
   - 已有 url → 不重复追加（除非用户明确「刷新该 url」：将该条改回 `pending`，可清 `note`）
3. 从 `inbox.md` **删除已入队的 URL 行**；文件只留注释说明「一行一个链接」。
4. 「重试 failed」：把对应条目（按 url）`status` 改为 `pending`，再进入第 2 步。

**不要** Glob 整个 `raw/` 或整库仓根 `wiki/`。

## 2. 取本批

- 默认取 catalog 中最多 **5** 条 `status: pending`（按文件中出现顺序）。
- 用户说「只入这一条」→ 1 条；「再来 N 个」→ N 条。
- **禁止**一轮扫完全部 pending。

## 3. 导出与整理（可并行）

对每条本批 URL：

1. 从 url 取出文档标识参数的**完整取值**（常见参数名 `pageId` / `docId` 等，以实际 URL 为准），用作 `archive/` 下目录名。**原样使用，不要改写**：不要剥前缀、不要只留数字、不要再映射成另一套 id。取不到 → 该条 `status: failed`，`note` 写「url 无文档 id，请换成带 pageId 的链接」，**继续下一条**。不要用标题造 slug，不要在 catalog 写 `id`。
2. 目标目录：`raw/wiki/archive/<pageId>/`（`<pageId>` = 上一步取出的完整取值）。刷新或重导：先**清空**该目录再写，避免旧图残留。
3. 按 §0 调用 wiki-cli 导出正文 + 图片到该目录（或导出到别处后挪入）。失败则该条 `status: failed`，`note` 写原因，**继续下一条**，不整批回滚。
4. 导出后检查布局。目标：

```
raw/wiki/archive/<pageId>/
  page.md          # 仅此一个 markdown
  images/          # 全部图片只在这里
```

   若已是上述结构，跳过整理。否则：
   1. 找到导出的主 markdown，重命名为 `page.md`。
   2. 建 `images/`。把该目录根下（不含 `images/` 自身）所有 `.png` `.jpg` `.jpeg` `.gif` `.webp` `.svg` **移入** `images/`，不要留在 `page.md` 旁边。
   3. 改写 `page.md` 里的本地图链为 `./images/<文件名>`；**禁止**把鉴权 URL 留在 `page.md`。
   4. **验收**：`archive/<pageId>/` 根下只有 `page.md` 和 `images/`。不满足 → 该条 `failed`，`note` 写「存档布局未整理好」，不要进入编译。

5. 整理后的 `page.md` **不润色**；进知识页前剥离密钥。

## 4. 编译（必须串行）

对每条导出并整理成功的条目，**一条一条**编译（`index.md` / `log.md` 是共享状态）：

1. **只读本条** `archive/<pageId>/page.md` 与 `images/`。
2. 非运维知识（人事、行政等）→ `status: skipped`，`note` 写原因，不写知识页。
3. 否则按 [types.md](types.md) 选 type/目录；文件名与 `title` **中文**；固定中文章节；`status: draft`。
4. `sources`：**只写原始 wiki URL**（可多条 URL）。**禁止**写 `raw/wiki/archive/...`。正文须自洽，查询不读 raw。
5. **图片**：鉴权 URL **禁止**写进仓根 `wiki/` 正文。Agent 看 `archive/<pageId>/images/`；对理解有用的图拷到知识页旁（如 `wiki/操作手册/磁盘满处理.md` + `wiki/操作手册/磁盘满处理/topology.png`），正文用 `![](./磁盘满处理/topology.png)`。
6. 按 [index-log.md](index-log.md) 更新分组 index 与 `wiki/log.md`（一篇一链）。
7. 回写 catalog：`status: compiled`，`compiled_at: YYYY-MM-DD`，`title`，`wiki_pages: [相对仓根 wiki/ 的路径，如 操作手册/磁盘满处理.md]`。一篇来源可对应多页。**不要**写 `id`。
8. 编译失败：该条 `failed` + `note`，继续下一条。

密钥、token、kubeconfig 不要抄进知识页。

## 5. 本批结束（必须停）

汇报：

- 本批：compiled / skipped / failed（各列 url 或 pageId）
- catalog 剩余 `pending` 数量
- 问是否继续（「再来 5 个」）

然后跑 `python tools/okf-lint/okf_lint.py`，先修 error。

## catalog 字段（Agent 写）

| 字段 | 说明 |
|------|------|
| `url` | wiki 链接；**不改、不删条目**；去重与刷新都按它 |
| `title` | 来源标题（可中文） |
| `status` | `pending` \| `compiled` \| `skipped` \| `failed` |
| `compiled_at` | `YYYY-MM-DD` |
| `wiki_pages` | 相对仓根 `wiki/` 的路径列表 |
| `note` | 跳过/失败原因 |

**不要**写 `id`。存档路径为 `raw/wiki/archive/<pageId>/`，`<pageId>` = url 文档 id 参数的完整取值原样，不必记在 catalog。

## 硬规则摘要

- 人：对话或 `inbox.md`；不改 catalog。
- Agent 可写：`catalog.yaml`、`archive/`、清理 inbox；其它 raw 仍只读。
- 每个 URL 只留一份存档；刷新覆盖同一 `archive/<pageId>/`。
- 图必须在 `images/`，不得与 `page.md` 同级。
- 知识页 `sources` 只写 wiki URL。
- batch 默认 5；导出可并行，编译串行；批末必停。
- 不自动刷新已 `compiled`（除非用户点名刷新）。
- 不把 wiki 全文当 OKF 页粘贴；蒸馏编译。
- 不把 wiki-cli 实现拷进本仓。
