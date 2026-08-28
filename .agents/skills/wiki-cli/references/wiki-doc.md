# wiki doc — 文档管理

文档管理命令组：`get` / `create` / `update` / `list` / `search`。

---

## get — 查询文档

```bash
wiki doc get "https://wki.test.com/domains/59/wiki/3334/WIKI2021032500053"
```

### 返回结构

```json
{
  "document_type": "Markdown | 富文本",
  "title": "文档标题",
  "create_time": "2024-01-01 12:00:00",
  "document_owner_name": "责任人姓名",
  "document_owner_account": "l30028681",
  "last_update_time": "2024-07-17 10:00:00",
  "last_updated_by_name": "最后更新人姓名",
  "last_updated_by_account": "wwx899480",
  "content": "Markdown 正文（富文本文档返回纯文本提取结果）"
}
```

---

## create — 新建文档

```bash
# 在某文档下新建子文档
wiki doc create "https://wki.test.com/.../WIKI2021032500053" \
  --type 新建子文档 \
  --title "新文档标题" \
  --content "文档内容"

# 在某文档同级新建
wiki doc create "参考URL" --type 新建同级文档 --title "兄弟文档"
```

### 参数

| 参数 | 必填 | 说明 |
|-|-|-|
| `URL` | 是 | 参考文档 URL，用于解析 domain_id / kanban_id / parent_id，**不等于新文档 URL** |
| `--type, -t` | 是 | `新建子文档` 或 `新建同级文档` |
| `--title` | 是 | 文档标题 |
| `--content, -c` | 否 | Markdown 正文，空字符串创建空文档 |

### 返回

```json
{ "created_document_url": "https://wki.test.com/.../WIKI2026071711899999" }
```

### 注意

- `--content` 必须是 Markdown 格式
- 新文档默认是 Markdown 类型，不支持新建富文本

---

## update — 更新文档

**两种模式互斥**：全量覆盖 vs 局部替换。

### 模式 1：全量覆盖（`--content`）

```bash
wiki doc update "文档URL" --content "# 全新的正文"
wiki doc update "文档URL" --title "新标题"                    # 只改标题
wiki doc update "文档URL" --title "新标题" --content "..."    # 同时改
```

**语义**：`--content` 完全替换原文，不保留任何原内容。需保留原内容时务必先 `doc get` 取回 `content` 字段再拼接修改。

### 模式 2：局部替换（`--replace P --with N`）

**语义**：
- 在当前正文中匹配 `--replace` pattern
- **匹配到唯一一处**时替换为 `--with` 的内容
- 匹配 0 处 → 报错退出（请检查 pattern）
- 匹配 >1 处 → 报错退出（请提供更精确的 pattern）
- `--with` 中包含原匹配串 → 实现"插入"语义

### 参数冲突校验

| 冲突 | 报错 |
|-|-|
| `--replace` + `--content` 同用 | "参数冲突：--replace 与 --content 不可同时使用" |
| `--replace` 无 `--with` | "--replace 需配合 --with 使用" |
| `--with` 无 `--replace` | "--with 仅在 --replace 模式下有效" |

### 文档类型限制

| 类型 | `--title` | `--content` | `--replace` |
|-|-|-|-|
| Markdown | ✅ | ✅ | ✅ |
| 富文本 | ✅ | ❌ "当前文档类型为富文本，仅支持更新标题" | ❌ "局部替换仅支持 Markdown 类型文档" |

### 决策树（选哪种模式）

1. **只改标题** → `--title X`（不带 `--content` / `--replace`）
2. **改一两处局部，原文大体保留** → `--replace P --with N`
3. **重写整篇或大段重写** → `--content` 全量覆盖（务必先 `get` 取原文再拼接）

`--replace` 风险低（不碰其他内容），但 pattern 必须精确唯一；`--content` 简单粗暴，但容易丢失原文中应保留的部分。**改动范围不确定时优先 `--replace`**，pattern 难以唯一时退回 `--content`。

### `--replace` 常见场景

执行前务必先 `wiki doc get` 获取当前文档内容，确保 pattern 来自原文。核心模式：把原文片段放入 `--replace`，把"替换内容"放入 `--with`：

```bash
# 在指定内容前插入
wiki doc update "文档URL" --replace "指定内容" --with "插入的内容...指定内容"

# 在指定内容后追加
wiki doc update "文档URL" --replace "指定内容" --with "指定内容...追加的内容"

# 局部内容替换
wiki doc update "文档URL" --replace "局部的内容" --with "新的内容"
```

> 大范围多处更新见决策树第 3 项（`--content` 全量覆盖）。

### 返回

```json
{ "document_url": "https://wki.test.com/.../WIKI2021032500053" }
```

---

## list — 查询文档列表

```bash
# 列出某类目下的全部文档
wiki doc list "文档URL" --range 类目

# 列出某文档的子文档（仅首层）
wiki doc list "文档URL" --range 子文档 --type 首层文档

# 按标题模糊 + 责任人 + 时间区间过滤
wiki doc list "文档URL" --range 子文档 \
  --title "设计" \
  --owner l30028681 \
  --create-start 2026-01-01 --create-end 2026-07-17 \
  --update-start 2026-06-01 \
  --page 1 --page-size 100
```

### 参数

| 参数 | 必填 | 说明                                             |
|-|-|------------------------------------------------|
| `URL` | 是 | 用于解析 domain_id / kanban_id / wiki_id 的参考文档 URL |
| `--range, -r` | 是 | `类目`（kanban 下所有）或 `子文档`（当前文档下所有）               |
| `--type, -t` | 否 | `全部文档`（默认）或 `首层文档`（不展开嵌套）                      |
| `--title` | 否 | 标题模糊搜索                                         |
| `--owner` | 否 | 责任人工号，如 `l30028681`                            |
| `--create-start` / `--create-end` | 否 | 创建时间区间 YYYY-MM-DD，单边可省                         |
| `--update-start` / `--update-end` | 否 | 更新时间区间 YYYY-MM-DD，单边可省                         |
| `--page, -p` | 否 | 页码，默认 1                                        |
| `--page-size, -s` | 否 | 每页条数，默认 100，且最大支持100                           |

### 返回

```json
{
  "total_records": 1,
  "page": 1,
  "page_size": 100,
  "records": [
    {
      "title": "子文档标题",
      "url": "https://wki.test.com/.../WIKI2021032500053",
      "owner_name": "责任人姓名",
      "owner_account": "l30028681",
      "create_time": "2024-01-01 12:00:00",
      "last_update_time": "2024-07-17 10:00:00",
      "document_type": "Markdown | 富文本"
    }
  ]
}
```

---

## search — 关键词搜索

```bash
# 在当前文档及子文档范围内搜
wiki doc search "文档URL" --range 当前文档及子文档 "部署指南"

# 在整个类目内搜
wiki doc search "文档URL" --range 类目 "架构"

# 在整个知识库内搜（最广）
wiki doc search "文档URL" --range 知识库 "AI Agent"
```

### 参数

| 参数 | 必填 | 说明                                            |
|-|-|-----------------------------------------------|
| `URL` | 是 | 参考文档 URL，用于解析 domain_id / kanban_id / wiki_sn |
| `--range, -r` | 是 | `知识库` / `类目` / `当前文档及子文档`，范围递减                |
| `关键词` | 是 | 位置参数，搜索关键词                                    |
| `--page, -p` / `--page-size, -s` | 否 | 分页，默认 1 / 100，page-size最大支持100                |

### 返回

```json
{
  "total_records": 1,
  "page": 1,
  "page_size": 100,
  "records": [
    {
      "title": "匹配文档标题",
      "url": "https://wki.test.com/.../WIKI2021032500053",
      "content_match_snippets": ["正文匹配片段1", "片段2"]
    }
  ]
}
```

结果按相关度降序排列

### 决策点（选 `--range`）

| 用户意图 | `--range` |
|-|-|
| "在 XX 文档及子文档里找" | `当前文档及子文档`（最窄，最快） |
| "在 XX 类目下找" | `类目` |
| "在整个知识库里找" | `知识库`（最广，结果最多） |
