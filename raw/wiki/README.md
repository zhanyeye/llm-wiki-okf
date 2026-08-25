# raw/wiki — 公司 wiki 来源

与仓根 [`wiki/`](../../wiki/)（OKF 知识面）不是同一目录。这里只放 **wiki 链接与导出快照**。

## 上手（人只要做这些）

**方式 A — 对话里贴链接：**

```text
把这些入库：
https://wiki.example.com/pages/viewpage.action?pageId=12001
https://wiki.example.com/pages/viewpage.action?pageId=12002
```

**方式 B — 一次丢很多：** 把 URL 一行一个写进 [`inbox.md`](inbox.md)，再说「把 inbox 入库」。

不要改 [`catalog.yaml`](catalog.yaml)（Agent 账本）。不要每个 URL 单独建文件。

## 目录

| 路径 | 谁写 | 说明 |
|------|------|------|
| `inbox.md` | 人 | 一行一个 URL；`#` 开头是注释 |
| `catalog.yaml` | Agent | 去重与 pending/compiled/skipped/failed |
| `snapshots/<id>/` | Agent（经 wiki-cli） | 导出正文与图片；写出后当原文，不润色 |

查询知识仍只读仓根 `wiki/`，不读本目录。
