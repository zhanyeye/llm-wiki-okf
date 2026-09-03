# okf-lint

体检 `wiki/` 是否符合本仓 OKF 约定（stdlib，无第三方依赖）。

## 何时用

入库、改页、改 index/log 之后，或对话里说「体检一下 wiki」时。

## 怎么跑

在仓库根执行：

```bash
python tools/okf-lint/okf_lint.py
```

先修 error（type/目录、Foundation/Registry schema、wikilink 目标、coverage manifest、`verified.by`），再看 warning（Registry 画像缺口、孤儿 Foundation、L2 缺下层链接、Markdown 断链、过期和 index 等）。

验证隔离示例库：

```bash
python tools/okf-lint/okf_lint.py --root examples/network-pilot
```

## 扫什么

扫描 `wiki/index.md`、`wiki/log.md`、9 个知识类型目录（含 `基础知识/`、`资源目录/` 子目录）与 `wiki/_meta/ingest/*.yaml`。不把 `_meta` 当知识正文，也不扫描仓根框架文件和 raw。
