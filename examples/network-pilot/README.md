# network-pilot：完全虚构的 OKF 隔离试点

> **危险声明：本 mini repo 的全部系统、域名、URL、证书、负责人、实例名、命令参数和流程均为完全虚构内容，仅用于 `demo` 环境的 schema/lint 演示，严禁用于生产、联调或真实网络配置。**

本目录是独立的分层知识编译样例，不依赖父仓库 `wiki/` 正文。`raw/` 放置三篇故意混杂概念、资产、操作和决策的虚构来源；`wiki/` 是按 L0 Atomic → L1 Registry → L2 Operational 编译后的知识图谱；`wiki/_meta/ingest/` 记录逐来源覆盖。

## 结构

* `raw/`：完全虚构且故意混杂的原始资料。
* `wiki/原子知识/`：四个稳定概念。
* `wiki/资源注册表/`：三个 `demo` 资产实例。
* `wiki/操作手册/`、`wiki/常见问题/`、`wiki/架构决策记录/`：运行知识。
* 其余 OKF 类型目录以 `.gitkeep` 保留，明确展示完整九类型结构。
* [`ACCEPTANCE.md`](./ACCEPTANCE.md)：概念、资产、操作和 FAQ 四类查询的预期遍历与验收条件。

## 校验

从父仓库根目录运行：

```powershell
python tools/okf-lint/okf_lint.py --root examples/network-pilot
```

此命令只验证示例结构，不表示其中任何操作已获真实环境验证。
