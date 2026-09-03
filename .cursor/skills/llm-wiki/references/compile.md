# 分层知识编译

目标不是摘要或改写原文，而是：**先拆内网特有概念，再长出 Registry / Runbook / FAQ / ADR，并用双链引用**。禁止把一篇来源平铺成一页。

日常小改：直接改对应层的页 + 更新 index/log + lint。不必写覆盖 YAML。

新来源或公司 wiki 批量按下面做。公司 wiki 批量可把处置清单写到 `wiki/_meta/ingest/<docKey>.yaml`（不进导航）；一般 raw 不强制。

## 按知识性质分配

- 内部概念、平台「是什么」、公司用法、稳定规则 → [`wiki/基础知识/<能力域>/`](../../../../wiki/基础知识/)（`type: Atomic`）
- 部署实例、入口、负责人、告警 → 资源目录（Registry），且 `technology` 必须 `[[双链]]` 到基础知识页
- 可重复任务 → 操作手册（Runbook）；短问答与按症状排查 → 常见问题（FAQ）
- 决策与权衡 → 架构决策记录（Decision）
- 一次性事件 → 案例与复盘（Incident）
- 跨实体拓扑/链路 → 写入相关基础知识页或 ADR（不单开「系统与架构」）

一篇来源可以更新多页；多篇来源也可汇入同一页。不得规定「一个 URL 一页」。

能力域：OS镜像、镜像制作、构建资源管理、网络管理、应用服务、资源调度。  
资产类：集群、数据库、存储、中间件、可观测。

## 用户指定写入分组

用户用 [`wiki/index.md`](../../../../wiki/index.md) 的**分组名**限制本次 Compose（如「网络管理」「操作手册」），不是层编号（L0/L1）。未指定 = 全部。

- 分组名 = 写入范围；仍按知识性质 Plan，禁止整篇硬塞进指定分组的一页。
- 目标分组不在范围内 → disposition `deferred`（原因如 `out_of_scope`），不写页，须在汇报中列出。
- 其它处置：`compiled` | `duplicate` | `excluded` | `gap` | `deferred`。
- 缺下层默认 link-only（标 `gap`，不自动建空页）；仅用户明确要求时才建 stub。细则见 [ingest.md](../ingest.md) §写入分组。

公司 wiki 批量若写 coverage YAML，可含：

```yaml
scope:
  groups: [网络管理]
```

## 顺序

1. **Extract**：列出实体、事实、资产、步骤、问答、决策、症状。命令/数字/错误原文保真；限制和不确定不得丢失。
2. **Resolve**：按名称、别名、环境搜已有页。同一实体更新；同名异物用不同 `id`。Registry 的 `technology` 必须解析到已有或将写的基础知识页。
3. **Plan**：每条提取项给出目标分组和页。没有分层计划不得写文件。
4. **按用户指定分组过滤**（若有）：范围外 → `deferred`；范围内才进入 Compose。
5. **Compose**：先基础知识，再资源目录，再操作手册/常见问题/ADR 等。上层不复制下层定义。来源没有的小节写「来源未写」。脚本提取（若有）在这一步做完。
6. **Link**：语义关系用 `[[页]]` / `[[页#标题]]` / `[[页#^block-id]]`。基础知识页不反向依赖 Runbook/FAQ。反向关系用 backlinks。
7. **Validate**：范围内步骤可执行；数字、命令、限制有去向；`deferred`/`gap` 已汇报；Registry 链到基础知识页；lint 无 error。未通过不得记 `ingest compiled`。

## 发布

- 新页 `status: draft`，不替人写 `verified`。
- lint 只保证结构；语义质量按 [review.md](../review.md) 由人确认后才标 `stable`。
