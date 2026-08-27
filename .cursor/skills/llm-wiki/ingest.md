# ingest

把来源或对话结论编译进 `wiki/` OKF 页。来源：本地 raw Markdown、公司 wiki URL、粘贴内容、故障结案、迁旧文档。

写入前必读 [references/okf.md](references/okf.md) 与 [references/index-log.md](references/index-log.md)。

## 分流

| 触发 | 走 |
|------|-----|
| 对话贴了公司 wiki 链接要入库；或 `raw/wiki/inbox.md` 非空；或「继续下一批 / 重试失败项 / 刷新某 url」 | §公司 wiki → [references/source-wiki-cli.md](references/source-wiki-cli.md) |
| 本地 raw Markdown、工单、纪要、故障结案、迁文档、从零写页 | §一般摄入 |

## 一般摄入

1. **Fetch**：有 raw 就读对应文件；**不要改 raw**（`raw/wiki/` 例外见 source-wiki-cli：可追加 inbox、写 archive）。无来源时按对话/已知事实写。密钥、token、kubeconfig 不要抄进 wiki。
2. **Triage**：在 `wiki/` 搜来源关键实体与同义词，判定：
   - **New** — 新建一页或多页
   - **Update** — 合并进已有页
   - **No material** — 无新增知识；只记 log，不强行写页
3. **Compile**：按 [references/okf.md](references/okf.md) 选 type/目录与固定标题；填 frontmatter（`status: draft`）；`sources` 写仓内路径（如 `raw/tickets/...`）或原始 wiki URL。图片进同目录 `attachments/`（见 okf.md）。来源没有的小节写「来源未写」，**禁止**用训练数据补集群名、地址、命令。不替人写 `verified`。
4. **交叉引用**：按内容关联决定是否互链（见 okf.md）。同批多来源不因「同批」自动互链；**确有依赖/互补时可以互链**。
5. **故障关闭**：事实写入 `Incident`；可复用步骤写入或更新 `Playbook` / `Runbook`；把 `wiki/故障排查/index.md` 里对应「待入库」改成链接。
6. **迁旧文档**：按内容选 type，补 frontmatter，链到已有 Architecture / Registry，不要另建平行副本。
7. 一篇来源可改多页；**仅当该来源触及的概念确需交叉引用时**保持链接一致。命令放可复制代码块；占位符用 `<cluster>`、`<namespace>`、`<path>`。
8. 可选：按 [references/obsidian.md](references/obsidian.md) 用 `obsidian-cli` 辅助写页/查重（Obsidian 未开则用普通 Write）。
9. 按 [references/index-log.md](references/index-log.md) 更新被改目录的 index（**若该分组尚无 `index.md`，写入第一篇时创建**）、必要时 `wiki/index.md` 与 `故障排查/index.md`，并追加 `wiki/log.md`。
10. 跑 `python tools/okf-lint/okf_lint.py`，先修 error。汇报新页/改页路径，请人抽看 draft；要标 `verified` 需人确认。

## 公司 wiki

完整流程见 [references/source-wiki-cli.md](references/source-wiki-cli.md)。摘要：

1. 收集对话链接 + `inbox.md`；把对话里尚未出现的 URL **追加**到 inbox 末尾（不删行）。
2. 按 `sources:` 与 `wiki/log.md` 里 ingest skipped/failed 过滤；每批默认最多 15 条未处理项（批处理导出无瓶颈，编译每条约 1 轮对话，10–20 条为宜）。
3. 用 **`python tools/wiki-export/wiki_export.py export`** 批量导出到 `raw/wiki/archive/<docKey>/`（`{标题}.md` + `images/`）。脚本内部串行调用 wiki CLI，Agent 无需逐条手动调用。
4. **串行编译**（与一般摄入共用 Triage）：过滤非运维 → Triage（Update / New / No material）→ 蒸馏验收 → 写 OKF 页 → 更新 index/log（不用 catalog）。
5. 交叉引用按**内容是否确有关联**决定；同批不是关联依据，但同批页之间若确有依赖/互补 → **可以**互链。
6. 知识页 `sources` **只写原始 wiki URL**；禁止写 `raw/wiki/archive/...`。有用图片拷到知识页同目录 `attachments/`，正文 `![](./attachments/...)`。
7. 本批结束汇报 compiled/skipped/failed/no material；列出路径并请人抽看 draft；问是否继续；再跑 lint。

## Post-Ingest

`wiki/log.md` 追加示例：

```markdown
## 2026-08-26

* **Creation**: 写入 [标题](/wiki/操作手册/页.md)。
* **Update**: 合并来源 raw/tickets/disk-full.md 到 [磁盘满排查](/wiki/故障排查/磁盘满.md)。
* **Update**: ingest compiled https://wiki.example.com/pages/viewpage.action?pageId=12001 → [标题](/wiki/操作手册/页.md)。
* **Update**: ingest skipped https://wiki.example.com/pages/viewpage.action?pageId=12002 — 非运维知识。
* **Update**: ingest failed https://wiki.example.com/pages/viewpage.action?pageId=12003 — wiki-cli 失败：…。
```

No material 时：

```markdown
## 2026-08-26

* **Update**: ingest no material: raw/tickets/duplicate.md
* **Update**: ingest no material: https://wiki.example.com/pages/viewpage.action?pageId=12004
```
