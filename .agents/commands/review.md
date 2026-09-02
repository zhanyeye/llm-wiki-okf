---
description: 审核分层知识编译结果（llm-wiki review）
---

调用 llm-wiki skill 的 **review** 流程：读取 `.agents/skills/llm-wiki/review.md`、`references/compile.md` 与 `references/index-log.md`，按来源 manifest 聚合 Atomic、Registry 和 L2 产出，核对来源覆盖、原子边界、关系与可运维性。只有人明确确认后才写 `verified.by: human:<id>` 和 `status: stable`。

用户指定的页面、来源或审核意见：$ARGUMENTS
