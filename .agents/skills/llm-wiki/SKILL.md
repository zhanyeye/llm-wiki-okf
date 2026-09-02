---
name: llm-wiki
description: >-
  基础设施知识库（OKF）的查询与维护入口，知识存于 wiki/，四种操作：查（query）、
  入库/迁文档/写页/存档/更正（ingest）、体检/断链/过期（lint）、执行 Runbook（execute）。
  适用场景：基础设施问答、故障排查、故障复盘、操作手册、runbook / playbook、
  迁文档、新人上手、找系统入口或负责人。
  适用领域：Rancher、MinIO、Helm、Harbor、NFS、px、yum、镜像、域名、DNS、证书、
  防火墙、openGauss、流水线；常见症状：微服务重启、时延高、磁盘满、绿区代理。
  Triggers: 查、怎么配、在哪、入库、迁文档、复盘、体检、add to wiki、
  贴公司 wiki 链接（WIKI+数字）、raw/wiki/inbox.md。
---

# llm-wiki

维护 `wiki/` 知识库。聊天记录随会话结束即失效，只留在对话里的结论等于没入库。凡对话中产生可复用的知识——排查结论、故障复盘、跨多篇综合出的结论、验证有效的命令——都要写成新页或更新既有页（流程见 [ingest.md](ingest.md)）。

四种操作：**Query** 查、**Ingest** 入库、**Execute** 执行、**Lint** 体检，按意图走下面的路由。

## 原则

任何操作都适用，按序优先：

1. **安全**：机密凭证不进知识库（如密码、密钥、token、kubeconfig）；需要引用时写占位符或申请途径。
2. **不编造**：答案与命令必须有页面依据——优先 `wiki/`，不够再搜 `raw/`；两边都没有才明说没有、建议入库，不要凭记忆或训练数据填空。
3. **知识只进 `wiki/`**：`raw/` 是来源存档，默认只读（公司 wiki 通道例外：可追加 `inbox.md`、写 `archive/`，见 [references/source-wiki-cli.md](references/source-wiki-cli.md)）；仓根 `index.md` / `README.md` / `AGENTS.md` / `script/` / `tools/` 是框架文件，不是知识页。
4. **按意图只读对应文件**（路由见下表）；写入时才读 schema 与流程文件。

## 路由

| 用户意图 | 读 |
|----------|-----|
| 查、排障、东西在哪、怎么做 | [query.md](query.md) |
| 入库、迁文档、故障关闭、从零写一页、粘贴内容、存档查询答案 / 回写 | [ingest.md](ingest.md) + [references/compile.md](references/compile.md) + [references/okf.md](references/okf.md) + [references/index-log.md](references/index-log.md)；合适时再读 [references/obsidian.md](references/obsidian.md) |
| 公司 wiki 链接 / inbox / 继续下一批 / 重试失败项 | [ingest.md](ingest.md) §公司 wiki + [references/source-wiki-cli.md](references/source-wiki-cli.md) + [references/compile.md](references/compile.md) + [references/okf.md](references/okf.md) + [references/index-log.md](references/index-log.md) + `tools/wiki-export/wiki_export.py`；合适时再读 [references/obsidian.md](references/obsidian.md) |
| 增量刷新 / 刷新 wiki / 检查更新 | [ingest.md](ingest.md) §公司 wiki + [references/source-wiki-cli.md](references/source-wiki-cli.md) §增量刷新 |
| 执行操作 / 跑脚本 / 自动化执行 | [execute.md](execute.md) |
| 只改 index / log | [references/index-log.md](references/index-log.md) |
| 体检、过期、断链 | [lint.md](lint.md) |
| 审核确认、列未审清单 | [review.md](review.md) + [references/compile.md](references/compile.md) + [references/index-log.md](references/index-log.md) |
| Obsidian 浏览 / Bases / Canvas / 公网 Defuddle | [references/obsidian.md](references/obsidian.md) |

默认走 query。查询细节以 [query.md](query.md) 为准（`AGENTS.md` 查询节只是摘要），不要一次加载整库，不要加载写入用的 `references/`（写入与执行场景按路由表加载）。

## 写入要求

每次写入或修改 `wiki/` 后必须成立（lint 按此体检）：

- **分层原子化**：来源先按 [references/compile.md](references/compile.md) Extract → Resolve → Plan，再按 L0 Atomic → L1 Registry → L2 Operational 写入；禁止默认一来源一页。
- **写入闭环**：维护 `wiki/_meta/ingest/<source-id>.yaml` 覆盖清单 → Compose → Link → Validate → 正文自洽 → 按 index-log.md 更新 index/log → 跑 lint → 人工 review。
- **公司 wiki**：禁止 WebFetch 内网 wiki；批量导出用 `tools/wiki-export/wiki_export.py`（内部串行调用 wiki CLI），语义编译仍由 Agent 执行完整六阶段。**增量刷新为默认**：只编译有更新/未处理的条目；全量刷新需用户明确要求。
- **链接**：导航/来源用 Markdown 链接；语义关系用 `[[页#标题]]`，关键事实用 `[[页#^block-id]]`。交叉引用按内容关系，禁止仅因同批互链（见 okf.md）。
- **附件**：知识页图片统一放该页同目录 `./attachments/`；raw 存档仍用 `images/`（细则见 okf.md）。
- **自动化**：正文含独立可运行脚本（≥5 行）时，提取到 `script/<功能名>/`（含脚本文件 + `README.md`），wiki 正文完整保留 + frontmatter 加 `automation` 块。Agent 执行操作时优先用 `script_ref`。详见 okf.md 和 ingest.md。
- **Obsidian 增强**：编译/整理时可在合适场景用项目内 Obsidian Skill 加速；细则与失败回退见 [references/obsidian.md](references/obsidian.md)。
