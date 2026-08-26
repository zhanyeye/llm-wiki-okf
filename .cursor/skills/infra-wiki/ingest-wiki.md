# ingest-wiki

公司 wiki 增量入库。`raw/wiki/` 是来源通道，与仓根 `wiki/`（知识面）不是同一目录。

触发：对话贴了 wiki 链接并说入库；或「把 inbox 入库」；或要求继续下一批 / 重试失败项 / 刷新某 url。

人只贴对话链接，或编辑 [`raw/wiki/inbox.md`](../../../raw/wiki/inbox.md)。人不要改 [`raw/wiki/catalog.yaml`](../../../raw/wiki/catalog.yaml)。

编译仍遵守 [types.md](types.md) 与 [index-log.md](index-log.md)。查询路径永不读本文件。

## 0. 绑定 wiki-cli（每会话首次导出前）

本仓不 vendor CLI。依赖本机 **`wiki` CLI** 与 **`wiki-cli` Skill**。

1. 读 wiki-cli Skill（常见：`~/.cursor/skills/wiki-cli/SKILL.md` 等）；找不到则 `wiki --help` / `wiki-cli --help`。
2. 只用 Skill / help 里**真实存在**的「导出页面 + 下载鉴权图片」命令；不要虚构 flags，不要把私有 CLI 文档写入本仓。
3. 导出目标：`raw/wiki/archive/<docKey>/`（`<docKey>` 见 §3）。若 CLI 写到别处，导出后挪入，或让 output 参数指向该路径。
4. CLI / Skill 都找不到 → 停；告诉用户先安装配置；本批标 `failed` 并写 `note`，不要空编存档。

会话实际采用的命令记在回复里一行即可。

## 1. 入队（按 url 精确合并）

1. 收集 URL：当前对话链接 + `inbox.md` 非注释行（`#` 开头忽略）。
2. 读 `catalog.yaml`。按 **url 精确匹配** 去重：
   - 新 url → 追加 `{ url, status: pending }`
   - 已有 url → 不重复追加（用户明确「刷新该 url」除外：改回 `pending`，可清 `note`）
3. 从 `inbox.md` 删除已入队的 URL 行；文件只留注释说明。
4. 「重试失败项」：把对应条目 `status` 改为 `pending`，再进入第 2 步。

不要 Glob 整个 `raw/` 或整库 `wiki/`。

## 2. 取本批

- 默认取最多 **5** 条 `status: pending`（按文件出现顺序）。
- 用户指定本批条数则按指定；未指定不要一轮抽干全部 pending。

## 3. 导出与整理（可并行）

对每条本批 URL：

1. 从 url 取出文档标识参数的**完整取值**（常见名如 `pageId` / `docId`，以实际 URL 为准），记为 `<docKey>`。**原样使用**：不要改写、不要另造第三套 id。取不到 → 该条 `failed`，`note` 说明原因，继续下一条。不要用标题造 slug。
2. 目标：`raw/wiki/archive/<docKey>/`。刷新或重导：先清空该目录再写。
3. 按 §0 导出正文 + 图片。失败 → 该条 `failed` + `note`，继续下一条，不整批回滚。
4. 本仓布局合同（不跟 CLI 默认）：

```
raw/wiki/archive/<docKey>/
  page.md
  images/
```

   已是上述结构则跳过整理。否则：把主 markdown 重命名为 `page.md`；把该目录根下所有图片移入 `images/`；改写 `page.md` 本地图链为 `./images/<文件名>`；禁止把鉴权 URL 留在 `page.md`。
5. **验收**：根下只有 `page.md` 与 `images/`。不满足 → `failed`，不要进入编译。
6. 整理后的 `page.md` 不润色；进知识页前剥离密钥。

## 4. 编译（必须串行）

对每条导出并验收成功的条目，一条一条编译（`index.md` / `log.md` 是共享状态）：

1. 只读本条 `archive/<docKey>/page.md` 与 `images/`。
2. 非运维知识 → `status: skipped`，`note` 写原因，不写知识页。
3. 否则按 [types.md](types.md) 选 type/目录；`status: draft`；`sources` **只写原始 wiki URL**（可多条）。禁止写 `raw/wiki/archive/...`。正文须自洽。
4. 图片：鉴权 URL 禁止写进 `wiki/`。有用的图拷到知识页旁目录，正文用仓内相对路径引用。
5. 按 [index-log.md](index-log.md) 更新分组 index 与 `wiki/log.md`。
6. 回写 catalog：`status: compiled`，`compiled_at: YYYY-MM-DD`，`title`，`wiki_pages: [相对仓根 wiki/ 的路径]`。一篇来源可对应多页。
7. 编译失败：该条 `failed` + `note`，继续下一条。

密钥不要抄进知识页。

## 5. 本批结束（必须停）

汇报：本批 compiled / skipped / failed（各列 url 或 docKey）；catalog 剩余 `pending` 数量；问是否继续。

然后跑 `python tools/okf-lint/okf_lint.py`，先修 error。

## catalog 字段（Agent 写）

| 字段 | 说明 |
|------|------|
| `url` | wiki 链接；身份键；不改、不删条目；去重与刷新都按它 |
| `title` | 来源标题 |
| `status` | `pending` \| `compiled` \| `skipped` \| `failed` |
| `compiled_at` | `YYYY-MM-DD` |
| `wiki_pages` | 相对仓根 `wiki/` 的路径列表 |
| `note` | 跳过/失败原因 |

存档路径为 `raw/wiki/archive/<docKey>/`；`<docKey>` 不必记在 catalog。不自动刷新已 `compiled`（除非用户点名）。蒸馏编译，不要把 wiki 全文当 OKF 页粘贴。
