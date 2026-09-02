# ingest

把来源或对话结论编译进 `wiki/` OKF 页。来源：本地 raw Markdown、公司 wiki URL、粘贴内容、故障结案、迁旧文档。

写入前必读 [references/compile.md](references/compile.md)、[references/okf.md](references/okf.md) 与 [references/index-log.md](references/index-log.md)。

## 分流

| 触发 | 走 |
|------|-----|
| 对话贴了公司 wiki 链接要入库；或 `raw/wiki/inbox.md` 非空；或「继续下一批 / 重试失败项 / 刷新某 url」 | §公司 wiki → [references/source-wiki-cli.md](references/source-wiki-cli.md) |
| 「增量刷新 / 刷新 wiki / 检查更新」 | §公司 wiki → [references/source-wiki-cli.md](references/source-wiki-cli.md) **§增量刷新** |
| 公网文档 URL（非公司 wiki）要入库 | §一般摄入：先用 `defuddle` 落 raw，再 Compile（见 [references/obsidian.md](references/obsidian.md)） |
| 本地 raw Markdown、工单、纪要、故障结案、迁文档、从零写页 | §一般摄入 |
| 用户指出已有页内容错误 / 过期 / 与环境不符 | §用户更正 |
| 「把这个答案存进 wiki」/ 查询后同意回写成新页 | §对话存档 |

编译时可按 [references/obsidian.md](references/obsidian.md) 使用 `obsidian-cli` / `obsidian-markdown` / `obsidian-bases` / `json-canvas` / `defuddle`；工具不可用则普通读写。

## 一般摄入

1. **Fetch**：有 raw 就读对应文件；**不要改 raw**（`raw/wiki/` 例外见 source-wiki-cli：可追加 inbox、写 archive）。公网 URL 用 `defuddle parse <url> --md` 写入 `raw/` 再读。无来源时按对话/已知事实写。密钥、token、kubeconfig 不要抄进 wiki。
2. **Extract**：按 [references/compile.md](references/compile.md) 逐项列出实体、事实、资产、步骤、FAQ、决策、症状和事件。命令/数字/错误原文保真，叙述提炼为可判断事实；限制、遗留项和不确定性不得丢失。
3. **Resolve**：用名称、别名、职责、环境和已有关系搜索 `wiki/`。同一实体更新已有页，同名异物分配不同稳定 `id`；未知项标 `gap`。Registry 的 `technology` 必须解析到 Atomic。
4. **Plan**：写文件前先确定每个提取项的处置与目标。定义/规则 → Atomic；实例/入口 → Registry；任务 → Runbook；症状 → Playbook；问答 → FAQ；决策 → Decision；拓扑 → Architecture；事件 → Incident。允许一来源多页、多来源一页，不设机械页数。
5. **Compose**：按 L0 → L1 → L2 写入，使用 [references/okf.md](references/okf.md) 的 type/目录/固定标题。新页 `status: draft`，不替人写 `verified`。上层定义与稳定约束链接到 Atomic/Registry，不复制近似文本。正文自洽；来源缺失项写「来源未写」或「不适用」，禁止训练数据补内网事实。
6. **Link**：为 `technology`、`depends_on`、`operates_on`、`answers_about`、`decides_for` 建内容级关系。语义关系使用 `[[页#标题]]` 或 `[[页#^block-id]]`；只维护有来源的有向边，反向关系用 backlinks。
7. **Coverage manifest**：在 `wiki/_meta/ingest/<source-id>.yaml` 记录来源、实体、每条提取项的 `compiled|duplicate|excluded|gap` 处置及目标。公司 wiki 用 docKey；其它来源用稳定短名，冲突时加短 hash。清单不含凭证。
8. **Validate**：逐项核对清单与来源；`compiled/duplicate` 目标必须存在，`excluded/gap` 必须有原因。每个操作步骤可执行；关键外链、数字、命令、限制与遗留项均有去向。Registry 满足 `asset_kind` 画像，上层在适用时链接下层。未通过先修复，不得记 `ingest compiled`。
9. **脚本提取**（Compose 后、Validate 前）：若正文含**独立可运行脚本**（≥5 行 bash/python，含 shebang 或可保存为文件直接执行），按以下流程提取：
   - 在 `script/<功能名>/` 下创建脚本文件（去掉 markdown 代码围栏，补 shebang 和 `set -euo pipefail` 如缺失）
   - 同目录创建 `README.md`（含：用途、参数说明、用法、退出码、相关 wiki 页链接）
   - wiki 正文**完整保留**脚本（离线可用），在脚本代码块上方加一行 `> 可执行版本：[script/<功能名>/<文件>](/script/<功能名>/<文件>)`
   - wiki 页 frontmatter 加 `automation:` 块（`ready: true`、`script_ref`、`params`、`exit_codes`），见 okf.md
   - 正文中自动化段落用 `<!-- okf:auto:script -->` / `<!-- okf:auto:verify -->` / `<!-- okf:auto:rollback -->` 标记
   - **不提取**：单条命令（`df -h`、`kubectl get pods`）、验证/排查片段、需要人工交互的命令序列——这些仅加 `automation.ready: partial` + `params`
   - **script/ 命名**：按功能名（如 `disk-manager`、`bisheng-install`），不用 wiki 分组名
   - 更新 `script/README.md` 索引
10. **资产注册（Registry）**：作为 Compose 的 L1 阶段处理，不再是写完文档后的可选附加项。从来源提取稳定资产与值班会反复用到的入口（平台控制台、集群 dashboard/API、镜像仓、DNS/代理、制品库等）。本条是 No material / skipped / failed 则跳过。
   - **不要登记**：一次性排查 IP、临时跳板、个人机器、正文里未当作入口的外链。密钥/token/kubeconfig 仍禁止写入（见 okf.md）。
   - **没有可注册实体**：跳过，不强行建 Registry 页。
   - 在 `wiki/资源注册表/` 按稳定 `id`、名称与别名查找：已有资产就补字段与来源；新的稳定资产才建页。一个可独立定位和运维的资产一页，按 `asset_kind` 放入子目录；聚合入口由 index/Base 生成，不建超大杂页。
   - `type: Registry`，组件类型写 `asset_kind`；`technology` 至少链接一个 Atomic。已有 CMDB/平台为权威源时记录 `source_of_truth`、`external_id`、`sync_mode`。
   - `sources`：公司 wiki 写原始 URL；本地 raw / 工单写仓内路径（见 okf.md）。一个平台入口只注册一次；多篇来源可充实同一 Registry 页。
11. **故障关闭**：事实写入 `Incident`；可复用步骤写入或更新 `Playbook` / `Runbook`；稳定根因知识回写 Atomic；把故障排查 index 的「待入库」改成链接。
12. **迁旧文档**：完整重跑 Extract → Validate，不得只补 frontmatter 或把旧目录映射到新目录。
13. **可选可视化**：Architecture / 复杂排查树确需示意 → `json-canvas`；资产/type/domain/status 聚合 → `obsidian-bases`。视图不复制事实。
14. 按 [references/index-log.md](references/index-log.md) 更新涉及目录的 index 与 `wiki/log.md`；只有 Validate 通过才记录 compiled。
15. 跑 `python tools/okf-lint/okf_lint.py`，先修 error。再按 [review.md](review.md) 请人审核 draft；人明确确认后才标 `verified`。

## 用户更正

用户指出已有页内容错误、过期或与本环境不符时，按 Update 流程修改该页：用户更正写进 `sources` 或正文；页面改回 `status: draft` 并清除 `verified`；描述受影响时同步分组 index，并追加 `wiki/log.md`，跑 lint。

## 对话存档

查询对话中产生值得沉淀的答案（用户明确要求存档，或同意把排查树、跨页对比、raw/ 综合结论回写）时：

1. 对综合答案照常执行 Extract → Resolve → Plan；基础事实更新 Atomic，综合操作/对比再进入对应 L2 页面。
2. `sources` 链到被引用的 wiki 页；为本次存档写 `wiki/_meta/ingest/conversation-<date>-<slug>.yaml` 覆盖清单。
3. 完成 Link/Validate 后更新分组 index 与 `wiki/log.md`。

## 公司 wiki

完整流程见 [references/source-wiki-cli.md](references/source-wiki-cli.md)。摘要：

1. 收集对话链接 + `inbox.md`；把对话里尚未出现的 URL **追加**到 inbox 末尾（不删行）。
2. 按 `sources:` 与 `wiki/log.md` 里 ingest skipped/failed 过滤；每批默认最多 15 条未处理项（批处理导出无瓶颈，编译每条约 1 轮对话，10–20 条为宜）。
3. 用 **`python tools/wiki-export/wiki_export.py export`** 批量导出到 `raw/wiki/archive/<docKey>/`（`{标题}.md` + `images/`）。脚本内部串行调用 wiki CLI，Agent 无需逐条手动调用。
4. **串行编译**：过滤非运维 → Extract → Resolve → Plan → Compose（L0/L1/L2）→ Link → Validate → 更新 index/log。每个 docKey 写 `wiki/_meta/ingest/<docKey>.yaml`。内网导出**不要**用 Defuddle。
5. 关系必须有语义与目标标题/块；同批不是关联依据。
6. 知识页 `sources` **只写原始 wiki URL**；禁止写 `raw/wiki/archive/...`。有用图片拷到知识页同目录 `attachments/`，正文 `![](./attachments/...)`。
7. 本批结束汇报 compiled/skipped/failed/no material、coverage gap 与产出路径；跑 lint 后请人按 review.md 审核 draft。

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
