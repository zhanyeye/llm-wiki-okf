# lint

1. 运行：

```bash
python scripts/okf_lint.py
```

2. 先修 error（缺 frontmatter、缺 `type`、`type` 与目录不符）。
3. warning：断链、过期 `stale_after`。尚未写的页可以保持断链，不要为消警告编造正文。
4. 刚入库过：打开 `wiki/故障排查/index.md`，已有正文的项不要再写「待入库」。
5. `index.md` / `log.md` 对照 [index-log.md](index-log.md)：分组 index 有页必有条目；log 最新日在上、一条一事、动词后用 ASCII `:`。
6. 再看：两页矛盾、没有任何入链的概念页。
