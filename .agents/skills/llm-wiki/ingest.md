# ingest

把来源或对话结论编译进 `wiki/` OKF 页。来源：本地 raw Markdown、公司 wiki URL、粘贴内容、故障结案、迁旧文档。

写入前必读 [references/okf.md](references/okf.md) 与 [references/index-log.md](references/index-log.md)。

## 分流

| 触发 | 走 |
|------|-----|
| 对话贴了公司 wiki 链接要入库；或 `raw/wiki/inbox.md` 非空；或「继续下一批 / 重试失败项 / 刷新某 url」 | §公司 wiki → [references/source-wiki-cli.md](references/source-wiki-cli.md) |
| 「增量刷新 / 刷新 wiki / 检查更新」 | §公司 wiki → [references/source-wiki-cli.md](references/source-wiki-cli.md) **§增量刷新** |
| 公网文档 URL（非公司 wiki）要入库 | §一般摄入：先用 `defuddle` 落 raw，再 Compile（见 [references/obsidian.md](references/obsidian.md)） |
| 本地 raw Markdown、工单、纪要、故障结案、迁文档、从零写页 | §一般摄入 |

编译时可按 [references/obsidian.md](references/obsidian.md) 使用 `obsidian-cli` / `obsidian-markdown` / `obsidian-bases` / `json-canvas` / `defuddle`；工具不可用则普通读写。

## 一般摄入

1. **Fetch**：有 raw 就读对应文件；**不要改 raw**（`raw/wiki/` 例外见 source-wiki-cli：可追加 inbox、写 archive）。公网 URL 用 `defuddle parse <url> --md` 写入 `raw/` 再读。无来源时按对话/已知事实写。密钥、token、kubeconfig 不要抄进 wiki。
2. **Triage**：先从来源提取关键实体、中文/英文名、明显别名、报错码/报错短语、症状词和操作动词；用这些词在 `wiki/` 的 frontmatter 与正文中搜索（Obsidian 可用时优先 `obsidian search`），判定：
   - **New** — 新建一页或多页
   - **Update** — 合并进已有页
   - **No material** — 无新增知识；只记 log，不强行写页
3. **Compile**：按 [references/okf.md](references/okf.md) 选 type/目录与固定标题；填 frontmatter（`status: draft`）；`sources` 写字符串数组（原始 URL 或仓内相对路径）。`title` 用人会查找的主题，`description` 说明适用场景/症状与结果，`tags` 收录有区分度的别名、报错码和症状词；只写来源支持的词，不堆整句问法或臆造内网别名。图片进同目录 `attachments/`（见 okf.md）。来源没有的小节写「来源未写」，**禁止**用训练数据补集群名、地址、命令。不替人写 `verified`。可用 `obsidian-cli` 写页；需要 callout/embed 时读 `obsidian-markdown`（链接风格仍按 okf.md）。
4. **脚本提取**（Compile 后、实体注册前）：若正文含**独立可运行脚本**（≥5 行 bash/python，含 shebang 或可保存为文件直接执行），按以下流程提取：
   - 在 `script/<功能名>/` 下创建脚本文件（去掉 markdown 代码围栏，补 shebang 和 `set -euo pipefail` 如缺失）
   - 同目录创建 `README.md`（含：用途、参数说明、用法、退出码、相关 wiki 页链接）
   - wiki 正文**完整保留**脚本（离线可用），在脚本代码块上方加一行 `> 可执行版本：[script/<功能名>/<文件>](/script/<功能名>/<文件>)`
   - wiki 页 frontmatter 加 `automation:` 块（`ready: true`、`script_ref`、`params`、`exit_codes`），见 okf.md
   - 正文中自动化段落用 `<!-- okf:auto:script -->` / `<!-- okf:auto:verify -->` / `<!-- okf:auto:rollback -->` 标记
   - **不提取**：单条命令（`df -h`、`kubectl get pods`）、验证/排查片段、需要人工交互的命令序列——这些仅加 `automation.ready: partial` + `params`
   - **script/ 命名**：按功能名（如 `disk-manager`、`bisheng-install`），不用 wiki 分组名
   - 更新 `script/README.md` 索引
4. **实体注册（资源注册表同步）**：写完概念页后**立即做**，不要等用户提醒。从来源提取值班会反复用到的入口（平台控制台、集群 dashboard/API、镜像仓、DNS/代理、制品库等）。本条是 No material / skipped / failed 则跳过。
   - **不要登记**：一次性排查 IP、临时跳板、个人机器、正文里未当作入口的外链。密钥/token/kubeconfig 仍禁止写入（见 okf.md）。
   - **没有可注册实体**：跳过，不强行建 Registry 页。
   - 在 `wiki/资源注册表/` 按实体名与同义词查找，按序处理：
     1. **已有该实体** → 补缺失入口/地址，追 `sources`，不要重复建页。
     2. **没有该实体，但已有合适领域页**（如「CI-CD平台与制品仓」「基础设施平台入口」）→ 归入该页。
     3. **没有合适领域页** → 才新建 Registry 页。按领域/职能成页（一页是一类入口的目录），**不要一 URL 一页**，也不要建成超大杂页。
   - `sources`：公司 wiki 写原始 URL；本地 raw / 工单写仓内路径（见 okf.md）。一个平台入口只注册一次；多篇来源可充实同一 Registry 页。
5. **交叉引用**：按内容关联决定是否互链（见 okf.md）。同批多来源不因「同批」自动互链；**确有依赖/互补时可以互链**。概念页提到已注册的平台/资源且内容确有依赖时，在该 type 的固定相关章节链到对应 Registry 页（Runbook「相关系统」；Playbook / Architecture「相关文档」；Registry「依赖」）。
6. **故障关闭**：事实写入 `Incident`；可复用步骤写入或更新 `Playbook` / `Runbook`；把 `wiki/故障排查/index.md` 里对应「待入库」改成链接。
7. **迁旧文档**：按内容选 type，补 frontmatter，链到已有 Architecture / Registry，不要另建平行副本。
8. 一篇来源可改多页；**仅当该来源触及的概念确需交叉引用时**保持链接一致。命令放可复制代码块；占位符用 `<cluster>`、`<namespace>`、`<path>`。
9. **可选可视化**：Architecture / 复杂排查树且用户需要或内容确需示意 → `json-canvas`；用户要按 type/domain/status 浏览 → `obsidian-bases`。不要每篇默认建 canvas/base。
10. 按 [references/index-log.md](references/index-log.md) 更新被改目录的 index（**若该分组尚无 `index.md`，写入第一篇时创建**）、必要时 `wiki/index.md` 与 `故障排查/index.md`，并追加 `wiki/log.md`。
11. 跑 `python tools/okf-lint/okf_lint.py`，先修 error。汇报新页/改页路径，请人抽看 draft；要标 `verified` 需人确认。

## 公司 wiki

完整流程见 [references/source-wiki-cli.md](references/source-wiki-cli.md)。摘要：

1. 收集对话链接 + `inbox.md`；把对话里尚未出现的 URL **追加**到 inbox 末尾（不删行）。
2. 按 `sources:` 与 `wiki/log.md` 里 ingest skipped/failed 过滤；每批默认最多 15 条未处理项（批处理导出无瓶颈，编译每条约 1 轮对话，10–20 条为宜）。
3. 用 **`python tools/wiki-export/wiki_export.py export`** 批量导出到 `raw/wiki/archive/<docKey>/`（`{标题}.md` + `images/`）。脚本内部串行调用 wiki CLI，Agent 无需逐条手动调用。
4. **串行编译**（与一般摄入共用 Triage）：过滤非运维 → Triage（可用时 `obsidian search`）→ 蒸馏验收 → 写 OKF 页（可用 `obsidian-cli`）→ **实体注册**（上节第 4 步）→ 更新 index/log。内网导出**不要**用 Defuddle。
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
