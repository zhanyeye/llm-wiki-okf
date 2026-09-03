# 更新日志

## 2026-09-03

* **Update**: 页 `type` `Decision` 改名为 `ADR`（目录仍为 [架构决策记录](/wiki/架构决策记录/)）。
* **Update**: L0 页 `type` 由 `Atomic` 改为 `Foundation`（目录仍为 [基础知识](/wiki/基础知识/)，`layer: foundation`）。
* **Update**: L1 分组由「资源注册表」改名为 [资源目录](/wiki/资源目录/)（`type` 仍为 `Registry`）。
* **Update**: 去掉「系统与架构」分组（`Architecture`）；拓扑/链路写入基础知识或 ADR。基础设施侧后续另有承载。
* **Update**: 合并原「故障排查」进 [常见问题](/wiki/常见问题/)（`type: FAQ`，含短问答与按症状排查；值班入口）；去掉「新人上手」分组。
* **Update**: L0 目录改为 [基础知识](/wiki/基础知识/)，按能力域建 OS镜像 / 镜像制作 / 构建资源管理 / 网络管理 / 应用服务 / 资源调度；L1 [资源目录](/wiki/资源目录/) 按集群 / 数据库 / 存储 / 中间件 / 可观测分子目录。禁止来源平铺；上层用 Obsidian 双链引用下层。

## 2026-09-02

* **Update**: 知识模型改为 L0 基础知识、L1 资源目录、L2 运行知识，并加入内容级关系与来源覆盖清单。

## 2026-08-27

* **Update**: 编译 wiki 时按场景主动用 `obsidian-cli` / `obsidian-markdown` / `obsidian-bases` / `json-canvas` / `defuddle`（见 Skill `references/obsidian.md`）；内网 wiki 仍禁 Defuddle。
* **Update**: frontmatter 检索用 `domain` + `tags`；去掉 `scope`；`owner` 可选表示本页维护人。

## 2026-08-26

* **Update**: 去掉 `raw/wiki/catalog.yaml`；`inbox.md` 改为增量只追加（对话可代写新 URL）；去重与 skipped/failed 走 `sources:` 与本 log；公司 wiki 编译强制 Triage + 蒸馏验收。
* **Update**: ingest 约束：交叉引用按内容关联（同批确有关系可互链，禁止瞎链）；知识页图片统一 `attachments/`；编译可用可选 Obsidian CLI。
* **Update**: 空分组不再强制保留 `index.md`；有概念页时再由 Agent 创建。仅 `故障排查/index.md` 因待入库清单保留。
* **Update**: 8 个分组目录改回中文（与人读名称一致）；`type` 仍为英文。
* **Update**: 分组改为 8 个英文目录（registry、architecture、runbooks、playbooks、adr、faq、incidents、onboarding）；去掉规范与约束、技能地图、自动化脚本顶栏。人读名称不变。

## 2026-08-24

* **Update**: `okf_lint.py` 迁至 `tools/okf-lint/`；`tools/index.md` 作工具总览；`script/` 专放运维脚本。
* **Update**: 知识面收回 `wiki/`（`index.md`、`log.md`、11 个分组）；仓根另放极薄 `index.md` 作地图；`scripts/` 改名为 `script/`。
* **Update**: 去掉 `wiki/` 包装层；知识面曾平铺到仓库根（已回退）。

## 2026-08-21

* **Update**: 删除 Phase 0 示例概念页；知识面仅保留分组结构、空 index 与本日志，避免骨架页干扰后续入库。
* **Initialization**: 建立 11 个分组目录。
