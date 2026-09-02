# lint

体检 `wiki/` OKF 知识库。分三类：可自动修、机械报告、人工判断。

## 1. 运行 okf-lint

```bash
python tools/okf-lint/okf_lint.py
```

先修 **error**：缺 frontmatter/type/id、type 与顶层目录不符、ID 重复、Atomic kind 非法、Registry 缺 asset_kind/technology、关系目标页/标题/块不存在、coverage manifest 处置不完整、`verified.by` 不是 `human:` 前缀。`layer` 若填写则必须与 type 一致。

**warning**：Markdown 断链、过期、Registry 画像字段缺口、L2 缺下层链接、孤儿 Atomic、重复块 ID、来源缺 manifest、index 不一致。不要为消警告编造事实；缺信息应明确写为 gap 并进入审核。

可对隔离示例库运行：

```bash
python tools/okf-lint/okf_lint.py --root examples/network-pilot
```

## 2. Safe Fixes（可自动修）

**Index 一致性** — 对照各分组 `index.md` 与实际概念 `.md` 文件：

- 尚无概念页 → 允许没有 `index.md`（不要为消警告建空 index）
- 有概念页但缺 `index.md` → **创建** index 并补条目
- 有页无条目 → 补条目（description 取自 frontmatter）
- 条目指向不存在文件 → 标 `[MISSING]`，不删条目
- 删页或改 title/description → 同步改 index

**内部链接** — wiki 正文与 frontmatter 中的 Markdown 链接和 wikilink：

- 目标不存在 → 在 `wiki/` 搜同名文件
  - 唯一匹配 → 修正路径
  - 零或多匹配 → 报告用户
- `[[页#标题]]` / `[[页#^block-id]]` 的页、标题或块不存在 → error；标题重命名前先查 backlinks

**故障排查 index** — 已有正文的项不得仍写「待入库」

**log.md** — 对照 [references/index-log.md](references/index-log.md)：最新日在上、一条一事、动词后用 ASCII `:`

## 3. Mechanical Reports（只报告）

- `sources` 中 `resource` 无法解析
- 过期 `stale_after` 未处理
- 概念页放在错误分组（type 与目录不符）
- Registry 的外部权威源不可访问或同步状态未知（工具只校验字段，实际状态人工确认）

## 4. Judgment Reports（只报告）

- 两页矛盾陈述
- 没有任何入链的孤儿页
- 故障相关「待入库」长期未补
- 明显缺失的交叉引用（建议，不静默添加）
- **乱关联**：仅因同批入库、内容无关却互链「相关文档」——报告并建议删链；内容确有关联的同批互链保留
- **原子边界不当**：一页混入多个可独立更新实体，或一条句子被拆成一页
- **搬运式入库**：来源段落仅换标题/目录，没有事实清单、消歧和上层/下层编排
- **来源覆盖**：manifest 虽完整但摘要与原文不符，或有效事实被错误标成 excluded
- **附件路径**：知识页图链不在 `./attachments/`（如 `./页名/`、`./images/`）——报告，入库修时应迁到 `attachments/`

## 5. Post-Lint

若改了 index 或页面，追加 `wiki/log.md`：

```markdown
## 2026-08-26

* **Update**: lint: 3 auto-fixed, 2 reported
```

纯查询、只跑 lint 且未改页 → 不写 log。
