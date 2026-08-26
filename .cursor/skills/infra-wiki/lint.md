# lint

1. 运行：

```bash
python tools/okf-lint/okf_lint.py
```

2. 先修 error（缺 frontmatter、缺 `type`、`type` 与目录不符）。
3. warning：断链、过期 `stale_after`、`title` 或文件名不含中文。尚未写的页可以保持断链，不要为消警告编造正文。英文 `title`/文件名改成中文，并同步分组 index。
4. 对照 [references/index-log.md](references/index-log.md)：分组 index 有页必有条目；log 最新日在上、一条一事、动词后用 ASCII `:`；故障排查 index 中已有正文的项不要再写「待入库」。
5. 再看：两页矛盾、没有任何入链的概念页。
