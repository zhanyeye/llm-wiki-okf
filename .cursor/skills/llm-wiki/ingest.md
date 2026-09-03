# ingest

把来源或对话结论编译进 `wiki/` OKF 页。来源：本地 raw Markdown、公司 wiki URL、粘贴内容、故障结案、迁旧文档。

写入前必读 [references/compile.md](references/compile.md)、[references/okf.md](references/okf.md) 与 [references/index-log.md](references/index-log.md)。

## 分流

| 触发 | 走 |
|------|-----|
| 对话贴了公司 wiki 链接要入库；或 `raw/wiki/inbox.md` 非空；或「继续下一批 / 重试失败项 / 刷新某 url」 | §公司 wiki → [references/source-wiki-cli.md](references/source-wiki-cli.md) |
| 「增量刷新 / 刷新 wiki / 检查更新」 | §公司 wiki → [references/source-wiki-cli.md](references/source-wiki-cli.md) **§增量刷新** |
| 公网文档 URL（非公司 wiki）要入库 | §一般摄入：先用 `defuddle` 落 raw，再按分层写入（见 [references/obsidian.md](references/obsidian.md)） |
| 本地 raw Markdown、工单、纪要、故障结案、迁文档、从零写页 | §一般摄入 |
| 用户指出已有页内容错误 / 过期 / 与环境不符 | §用户更正 |
| 「把这个答案存进 wiki」/ 查询后同意回写成新页 | §对话存档 |

编译时可按 [references/obsidian.md](references/obsidian.md) 使用 `obsidian-cli` / `obsidian-markdown` / `obsidian-bases` / `json-canvas` / `defuddle`；工具不可用则普通读写。

## 写入分组（可选）

用户用 [`wiki/index.md`](../../../wiki/index.md) 中的**分组名**声明本次写入范围；**不要**要求用户说 L0/L1。未指定 = 全部（现有全层拆分）。

**分组名 = 写入范围**，不是「把整篇硬塞进这一页」。Extract/Plan 仍按知识性质拆条；只有目标分组落在用户指定范围内的条目才 Compose；范围外标 `deferred` 并在汇报中列出。

### 解析

权威名单以 `wiki/index.md` 为准（与 [references/okf.md](references/okf.md) type↔目录一致）：

| 用户说法 | 写入范围 |
|----------|----------|
| 基础知识 | `wiki/基础知识/**`（Atomic） |
| OS镜像 / 镜像制作 / 构建资源管理 / 网络管理 / 应用服务 / 资源调度 | `wiki/基础知识/<该能力域>/` |
| 资源目录 | `wiki/资源目录/**`（Registry） |
| 集群 / 数据库 / 存储 / 中间件 / 可观测 | `wiki/资源目录/<该资产类>/` |
| 操作手册 / 常见问题 / 架构决策记录 / 案例与复盘 | 对应顶层分组 |

- 解析优先级：先匹配子分组名，再匹配顶层。
- 同义词可接受（如「手册」→操作手册、「注册表」/「资源注册表」→资源目录）；不确定时**先问用户一句**再写。
- 可指定多个分组（如「网络管理」+「操作手册」）。
- 内部映射到 type 见 okf.md；用户无感。

### 缺下层依赖（默认 link-only）

用户只指定上层分组（如操作手册）时：

- **默认**：能 Resolve 到已有基础知识/资源目录页就双链；缺则该项标 `gap`（「缺 [[某概念]]」），**不自动新建**空下层页。
- 仅当用户明确说「缺的概念也建一下」时，才为依赖建最小 stub（`status: draft`，固定标题骨架，`tags` 含 `stub`）。

禁止因指定「操作手册」就把概念定义、实例 IP 全写进同一本手册。

### 公司 wiki 批量

同一套分组范围适用（「本批只进网络管理」）。若写 coverage YAML，增加：

```yaml
scope:
  groups: [网络管理]
```

一般 raw / 小改不强制写 YAML。

## 一般摄入

**禁止默认一来源一页。** 一篇「网络边界」材料要先拆成黄绿区、证书、DNS 等基础知识页，再登记实例，再写手册/FAQ/ADR。

1. **Fetch**：有 raw 就读对应文件；**不要改 raw**（`raw/wiki/` 例外见 source-wiki-cli：可追加 inbox、写 archive）。公网 URL 用 `defuddle parse <url> --md` 写入 `raw/` 再读。无来源时按对话/已知事实写。密钥、token、kubeconfig 不要抄进 wiki。
2. **Extract**：按 [references/compile.md](references/compile.md) 列出实体、事实、资产、步骤、FAQ、决策、症状和事件。命令/数字/错误原文保真；限制、遗留项和不确定性不得丢失。
3. **Resolve**：用名称、别名、职责和环境搜索 `wiki/`。同一实体更新已有页，同名异物分配不同稳定 `id`；未知项标 `gap`。Registry 的 `technology` 必须解析到基础知识页（Atomic）。
4. **Plan**：写文件前确定每条提取项的目标分组与页。定义/规则 → 基础知识（或能力域子目录）；实例/入口 → 资源目录；任务 → 操作手册；短问答与按症状排查 → 常见问题；决策 → 架构决策记录；事件 → 案例与复盘。跨实体拓扑/链路事实写入相关基础知识页或 ADR，不单开系统与架构分组。允许一来源多页、多来源一页。
5. **按用户指定分组过滤**：若用户声明了写入分组（见 §写入分组），目标分组不在范围内的 Plan 项标 `deferred`（原因如 `out_of_scope`），不进入 Compose。未指定则不过滤。
6. **Compose（先下层再上层）**：只对范围内条目按 [references/okf.md](references/okf.md) 的 type/目录/固定标题写入。新页 `status: draft`，不替人写 `verified`。上层用双链引用下层，不复制近似文本。正文自洽；来源缺失项写「来源未写」或「不适用」，禁止训练数据补内网事实。缺下层按 §写入分组 的 link-only（或用户要求的 stub）处理。
   - **资产注册**在本步完成（若范围包含资源目录或其资产类），不是写完文档后的附加项。没有可注册实体则跳过。按 `asset_kind` 放入对应子目录。`technology` 至少一条 `[[双链]]` 到基础知识页。
   - **脚本提取**（若有独立可运行脚本 ≥5 行）在 Compose 内、Validate 前完成：写入 `script/<功能名>/` + `README.md`；wiki 正文完整保留脚本并加 `automation` 块（见 okf.md）。不提取单条命令或需交互的片段。
7. **Link**：为 `technology`、`depends_on`、`operates_on`、`answers_about`、`decides_for` 建双链。只维护有来源的有向边；基础知识页不反向依赖 Runbook；反向关系用 backlinks。禁止仅因同批互链。
8. **Coverage manifest（可选）**：仅公司 wiki 批量建议写 `wiki/_meta/ingest/<docKey>.yaml`（可含 `scope.groups`）。一般 raw / 小改不强制。清单不含凭证，不进导航。
9. **Validate**：范围内目标页必须存在；每个操作步骤可执行；关键外链、数字、命令、限制与遗留项均有去向（`deferred`/`gap` 须在汇报中可见）。Registry 链到基础知识页且满足 `asset_kind` 画像。未通过先修复，不得记 `ingest compiled`。
10. **故障关闭**：事实写入 `Incident`；可复用步骤写入或更新常见问题（FAQ）/ 操作手册（Runbook）；稳定根因回写基础知识；把常见问题 index 的「待入库」改成链接。若用户限定了分组，只写入范围内类型。
11. **迁旧文档**：按分层重写，不得只补 frontmatter 或把旧目录映射到新目录。
12. **可选可视化**：复杂拓扑或排查树确需示意 → `json-canvas`；资产/type/domain/status 聚合 → `obsidian-bases`。视图不复制事实。
13. 按 [references/index-log.md](references/index-log.md) 更新涉及目录的 index 与 `wiki/log.md`；只有 Validate 通过才记录 compiled。log 可记 `ingest scope: <分组名> → …`。
14. 跑 `python tools/okf-lint/okf_lint.py`，先修 error。再按 [review.md](review.md) 请人审核 draft；人明确确认后才标 `verified`。
15. **汇报**：按下方模板输出本次写入分组、已写入、延后、缺口（指定了分组或存在 deferred/gap 时必出）。

## 用户更正

用户指出已有页内容错误、过期或与本环境不符时，按 Update 流程修改该页：用户更正写进 `sources` 或正文；页面改回 `status: draft` 并清除 `verified`；描述受影响时同步分组 index，并追加 `wiki/log.md`，跑 lint。

## 对话存档

查询对话中产生值得沉淀的答案（用户明确要求存档，或同意把排查树、跨页对比、raw/ 综合结论回写）时：

1. 对综合答案照常执行 Extract → Resolve → Plan；若用户指定了写入分组则先过滤；基础事实更新基础知识页，综合操作/对比再进入对应 Runbook/FAQ/ADR。
2. `sources` 链到被引用的 wiki 页。公司 wiki 批量以外不必写 coverage YAML。
3. 完成 Link/Validate 后更新分组 index 与 `wiki/log.md`，并按模板汇报。

## 公司 wiki

完整流程见 [references/source-wiki-cli.md](references/source-wiki-cli.md)。摘要：

1. 收集对话链接 + `inbox.md`；把对话里尚未出现的 URL **追加**到 inbox 末尾（不删行）。
2. 按 `sources:` 与 `wiki/log.md` 里 ingest skipped/failed 过滤；每批默认最多 15 条未处理项（批处理导出无瓶颈，编译每条约 1 轮对话，10–20 条为宜）。
3. 用 **`python tools/wiki-export/wiki_export.py export`** 批量导出到 `raw/wiki/archive/<docKey>/`（`{标题}.md` + `images/`）。脚本内部串行调用 wiki CLI，Agent 无需逐条手动调用。
4. **串行编译**：过滤非运维 → Extract → Resolve → Plan → **按用户指定分组过滤** → Compose（范围内）→ Link → Validate → 更新 index/log。每个 docKey **建议**写 `wiki/_meta/ingest/<docKey>.yaml`（可含 `scope.groups`；刷新用，不进导航）。内网导出**不要**用 Defuddle。禁止把 wiki 全文当一页粘贴。
5. 关系必须有语义与目标标题/块；同批不是关联依据。
6. 知识页 `sources` **只写原始 wiki URL**；禁止写 `raw/wiki/archive/...`。有用图片拷到知识页同目录 `attachments/`，正文 `![](./attachments/...)`。
7. 本批结束汇报 compiled/skipped/failed/no material、deferred、coverage gap 与产出路径；跑 lint 后请人按 review.md 审核 draft。

## Post-Ingest

### 汇报模板

指定了写入分组，或存在 deferred/gap 时，对话末尾必须输出：

```markdown
### 本次写入分组
网络管理

### 已写入
- wiki/基础知识/网络管理/企业 DNS.md

### 延后（不在本次分组）
- 资源目录「xx DNS」— 建议下次指定「资源目录」或「集群」
- 操作手册「申请白名单」— 建议下次指定「操作手册」

### 缺口
- 操作手册依赖的 [[黄绿区]] 不存在（未建 stub）
```

未指定分组且无 deferred/gap 时，可省略该块，仍须汇报产出路径。续写延后项：用户再开一轮 `/ingest` 并指定对应分组（不做自动状态机）。

### log 示例

`wiki/log.md` 追加示例：

```markdown
## 2026-08-26

* **Creation**: 写入 [标题](/wiki/操作手册/页.md)。
* **Update**: 合并来源 raw/tickets/disk-full.md 到 [磁盘满排查](/wiki/常见问题/磁盘满.md)。
* **Update**: ingest scope: 网络管理 → [企业 DNS](/wiki/基础知识/网络管理/企业 DNS.md)。
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
