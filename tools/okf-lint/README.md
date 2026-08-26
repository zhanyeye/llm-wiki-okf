# okf-lint

体检 `wiki/` 是否符合本仓 OKF 约定（stdlib，无第三方依赖）。

## 何时用

入库、改页、改 index/log 之后，或对话里说「体检一下 wiki」时。

## 怎么跑

在仓库根执行：

```bash
python tools/okf-lint/okf_lint.py
```

先修 error，再看 warning（断链、过期 `stale_after`、`title`/文件名不含中文等）。

## 扫什么

只扫 `wiki/index.md`、`wiki/log.md` 与各分组目录（以 `wiki/index.md` 为准）。不扫仓根 `index.md`、`README.md`、`raw/`、`script/`、`tools/`。
