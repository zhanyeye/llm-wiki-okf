from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "okf_lint.py"
SPEC = importlib.util.spec_from_file_location("okf_lint", MODULE_PATH)
assert SPEC and SPEC.loader
OKF_LINT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = OKF_LINT
SPEC.loader.exec_module(OKF_LINT)


class LayeredLintTests(unittest.TestCase):
    def make_repo(self) -> Path:
        root = Path(tempfile.mkdtemp())
        wiki = root / "wiki"
        wiki.mkdir()
        for dirname in OKF_LINT.TYPE_DIR.values():
            (wiki / dirname).mkdir()
        (wiki / "_meta" / "ingest").mkdir(parents=True)
        (wiki / "index.md").write_text(
            '---\nokf_version: "0.2"\n---\n\n# 测试知识库\n', encoding="utf-8"
        )
        (wiki / "log.md").write_text(
            "# 更新日志\n\n## 2026-09-02\n\n* **Initialization**: 测试。\n",
            encoding="utf-8",
        )
        return root

    def add_valid_graph(self, root: Path) -> None:
        wiki = root / "wiki"
        source = "https://wiki.example.invalid/WIKI-DEMO"
        (wiki / "原子知识" / "网络规则.md").write_text(
            f"""---
type: Atomic
id: atomic:network:zone-rule
layer: atomic
kind: policy
title: 网络区域规则
description: 虚构网络区域的稳定约束。
domain: network
status: draft
sources:
  - {source}
---

## 定义

这是虚构规则。

## 职责与边界

只描述网络边界。

## 公司内使用方式

示例环境使用统一出口。

## 稳定约束

绿色区域必须通过统一代理访问外部网络。 ^green-egress-rule

## 关系

来源未写。
""",
            encoding="utf-8",
        )
        (wiki / "资源注册表" / "示例代理.md").write_text(
            f"""---
type: Registry
id: asset:network:demo-proxy
layer: registry
title: 示例出口代理
description: 虚构出口代理资产。
domain: network
asset_kind: network
name: demo-proxy
environment: demo
owner: demo-team
technology:
  - "[[网络规则#^green-egress-rule]]"
entries:
  console: https://proxy.example.invalid
status: draft
sources:
  - {source}
---

## 资产

虚构资产。

## 位置与环境

demo。

## 入口

见 frontmatter。

## 负责人

demo-team。

## 依赖

[[网络规则#^green-egress-rule]]

## 观测与告警

来源未写。

## 生命周期

来源未写。

## 凭证怎么申请

不适用。
""",
            encoding="utf-8",
        )
        (wiki / "_meta" / "ingest" / "WIKI-DEMO.yaml").write_text(
            f"""source_id: WIKI-DEMO
source: {source}
status: compiled
entities:
  - id: zone-rule
    target: "[[网络规则]]"
items:
  - id: fact-001
    kind: fact
    summary: 绿色区域使用统一出口
    disposition: compiled
    target: "[[网络规则#^green-egress-rule]]"
outputs:
  - "[[网络规则]]"
  - "[[示例代理]]"
validated_at: 2026-09-02T09:00:00Z
""",
            encoding="utf-8",
        )

    def test_valid_layered_graph_has_no_errors(self) -> None:
        root = self.make_repo()
        self.add_valid_graph(root)
        errors, _warnings = OKF_LINT.run(root)
        self.assertEqual([], errors)

    def test_missing_block_target_is_error(self) -> None:
        root = self.make_repo()
        self.add_valid_graph(root)
        registry = root / "wiki" / "资源注册表" / "示例代理.md"
        registry.write_text(
            registry.read_text(encoding="utf-8").replace(
                "^green-egress-rule", "^missing-rule"
            ),
            encoding="utf-8",
        )
        errors, _warnings = OKF_LINT.run(root)
        self.assertTrue(any("missing block" in error for error in errors))

    def test_duplicate_stable_id_is_error(self) -> None:
        root = self.make_repo()
        self.add_valid_graph(root)
        atomic = root / "wiki" / "原子知识" / "网络规则.md"
        duplicate = root / "wiki" / "原子知识" / "重复规则.md"
        duplicate.write_text(atomic.read_text(encoding="utf-8"), encoding="utf-8")
        errors, _warnings = OKF_LINT.run(root)
        self.assertTrue(any("duplicate id" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
