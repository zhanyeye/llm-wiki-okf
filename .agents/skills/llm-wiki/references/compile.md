# 分层知识编译

目标不是摘要或改写原文，而是：**先拆内网特有概念，再长出 Registry / Runbook / FAQ / ADR，并用双链引用**。禁止把一篇来源平铺成一页。

日常小改：直接改对应层的页 + 更新 index/log + lint。不必写覆盖 YAML。

新来源或公司 wiki 批量按下面做。公司 wiki 批量可把处置清单写到 `wiki/_meta/ingest/<docKey>.yaml`（不进导航）；一般 raw 不强制。

## 按知识性质分配

- 内部概念、平台「是什么」、公司用法、稳定规则 → L0 [`wiki/基础知识/<能力域>/`](../../../../wiki/基础知识/)（`type: Atomic`）
- 部署实例、入口、负责人、告警 → L1 Registry，且 `technology` 必须 `[[双链]]` 到 L0
- 可重复任务 → Runbook；按症状排查 → Playbook
- 短问答 → FAQ；决策与权衡 → ADR（Decision）
- 跨实体拓扑 → Architecture；一次性事件 → Incident

一篇来源可以更新多页；多篇来源也可汇入同一页。不得规定「一个 URL 一页」。

能力域：OS镜像、镜像制作、构建资源管理、网络管理、应用服务、资源调度。  
资产类：集群、数据库、存储、中间件、可观测。

## 顺序

1. **Extract**：列出实体、事实、资产、步骤、问答、决策、症状。命令/数字/错误原文保真；限制和不确定不得丢失。
2. **Resolve**：按名称、别名、环境搜已有页。同一实体更新；同名异物用不同 `id`。Registry 的 `technology` 必须解析到已有或将写的 L0 页。
3. **Plan**：每条提取项给出目标层和页。没有分层计划不得写文件。
4. **Compose**：先 L0，再 L1，再 Runbook/FAQ/ADR。上层不复制下层定义。来源没有的小节写「来源未写」。脚本提取（若有）在这一步做完。
5. **Link**：语义关系用 `[[页]]` / `[[页#标题]]` / `[[页#^block-id]]`。L0 不反向依赖 Runbook。反向关系用 backlinks。
6. **Validate**：步骤可执行；数字、命令、限制有去向；Registry 链到 L0；lint 无 error。未通过不得记 `ingest compiled`。

## 发布

- 新页 `status: draft`，不替人写 `verified`。
- lint 只保证结构；语义质量按 [review.md](../review.md) 由人确认后才标 `stable`。
