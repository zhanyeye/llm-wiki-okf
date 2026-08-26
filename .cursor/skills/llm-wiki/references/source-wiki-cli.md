# 公司 Wiki 来源（wiki-cli）

`raw/wiki/` 是来源通道，与仓根 `wiki/`（知识面）不是同一目录。

**禁止**用 WebFetch / Defuddle 抓内网 wiki。必须用 **wiki-cli** skill 与本机 **`wiki` CLI**。

## 触发

- 对话贴了 wiki 链接并说入库
- 「把 inbox 入库」
- 「继续下一批 / 重试失败项 / 刷新某 url」

人只贴对话链接，或编辑 [`raw/wiki/inbox.md`](../../../../raw/wiki/inbox.md)。人不要改 [`raw/wiki/catalog.yaml`](../../../../raw/wiki/catalog.yaml)。

## 0. 绑定 wiki-cli（每会话首次导出前）

1. **读取 wiki-cli Skill**：
   - 项目内：[`.cursor/skills/wiki-cli/SKILL.md`](../../../wiki-cli/SKILL.md)
   - 或用户全局：`~/.cursor/skills/wiki-cli/SKILL.md` 等
2. 按 wiki-cli Skill 要求，**先读对应 references**（如 `wiki-doc.md`、`wiki-file.md`）再执行命令。
3. **串行执行**：全部 wiki 命令必须等待上一条返回后再发下一条；禁止并行。
4. 只用 Skill / `wiki --help` 里**真实存在**的导出与图片下载命令；不要虚构 flags。
5. CLI / Skill 都找不到 → 停；告诉用户先安装配置；本批标 `failed` 并写 `note`，不要空编存档。

会话实际采用的命令记在回复里一行即可。

## 1. 入队（按 url 精确合并）

1. 收集 URL：当前对话链接 + `inbox.md` 非注释行（`#` 开头忽略）。
2. 读 `catalog.yaml`。按 **url 精确匹配** 去重：
   - 新 url → 追加 `{ url, status: pending }`
   - 已有 url → 不重复追加（用户明确「刷新该 url」除外：改回 `pending`，可清 `note`）
3. 从 `inbox.md` 删除已入队的 URL 行；文件只留注释说明。
4. 「重试失败项」：把对应条目 `status` 改为 `pending`，再进入 §2。

不要 Glob 整个 `raw/` 或整库 `wiki/`。

## 2. 取本批

- 默认取最多 **5** 条 `status: pending`（按文件出现顺序）。
- 用户指定本批条数则按指定；未指定不要一轮抽干全部 pending。

## 3. 导出与整理

对每条本批 URL：

1. 从 url 取出文档标识参数的**完整取值**（常见 `pageId` / `docId` / `sn=WIKI...`），记为 `<docKey>`。**原样使用**，不要改写。取不到 → `failed` + `note`。
2. 目标：`raw/wiki/archive/<docKey>/`。刷新：先清空该目录再写。
3. 按 §0 用 wiki-cli 导出正文 + 图片。失败 → `failed` + `note`，继续下一条。
4. 本仓布局合同：

```
raw/wiki/archive/<docKey>/
  page.md
  images/
```

   整理：主 markdown → `page.md`；图片 → `images/`；改写 `page.md` 本地图链为 `./images/<文件名>`；禁止鉴权 URL 留在 `page.md`。
5. **验收**：根下只有 `page.md` 与 `images/`。不满足 → `failed`，不编译。
6. `page.md` 不润色；进知识页前剥离密钥。

## 4. 编译（必须串行）

对每条导出并验收成功的条目，**一条一条**编译（index/log 是共享状态）。「同批」本身不是关联依据；**内容确有关联时可以互链**。

1. 以本条 `archive/<docKey>/page.md` 与 `images/` 为主；需要判断与本批其它条是否相关时，可对照其标题/摘要，不要为凑链通读全文硬凑。
2. 非运维知识 → catalog `status: skipped`，`note` 写原因，不写知识页。
3. 否则按 [okf.md](okf.md) 选 type/目录；`status: draft`；`sources` **只写本条原始 wiki URL**。正文须自洽。
4. **交叉引用**：按 [okf.md](okf.md)「按内容关联」——确有依赖/互补/上下游 → 可链已有页，也可链本批其它确相关页；仅因同批 → 不链。
5. **图片**：鉴权 URL 禁止写进 `wiki/`。有用的图从 `images/` 拷到知识页同目录 `attachments/`，正文用 `![](./attachments/<文件名>)`（见 okf.md）。raw 侧仍保持 `images/`。
6. 可选：按 [obsidian.md](obsidian.md) 用 `obsidian-cli` 创建/更新笔记；失败则回退普通 Write。
7. 按 [index-log.md](index-log.md) 更新分组 index（无则创建）与 `wiki/log.md`。
8. 回写 catalog：`status: compiled`，`compiled_at: YYYY-MM-DD`，`title`，`wiki_pages: [相对仓根 wiki/ 的路径]`。
9. 编译失败：`failed` + `note`，继续下一条。

## 5. 本批结束

汇报：compiled / skipped / failed（各列 url 或 docKey）；catalog 剩余 `pending` 数量；问是否继续。

然后跑 `python tools/okf-lint/okf_lint.py`，先修 error。

## catalog 字段

| 字段 | 说明 |
|------|------|
| `url` | wiki 链接；身份键；不改、不删条目 |
| `title` | 来源标题 |
| `status` | `pending` \| `compiled` \| `skipped` \| `failed` |
| `compiled_at` | `YYYY-MM-DD` |
| `wiki_pages` | 相对仓根 `wiki/` 的路径列表 |
| `note` | 跳过/失败原因 |

存档路径为 `raw/wiki/archive/<docKey>/`。不自动刷新已 `compiled`（除非用户点名）。蒸馏编译，不要把 wiki 全文当 OKF 页粘贴。
