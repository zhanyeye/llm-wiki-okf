# 更新日志

## 2026-08-27

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
