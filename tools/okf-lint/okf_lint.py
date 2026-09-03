#!/usr/bin/env python3
"""Lint the OKF knowledge surface under wiki/. Stdlib only. UTF-8 paths.

Scans only wiki/index.md, wiki/log.md and the 8 type directories (allowlist).
Does not treat repo-root index.md, README.md, AGENTS.md, raw/, script/,
tools/, etc. as concept pages.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "wiki"

RESERVED = {"index.md", "log.md"}

TYPE_DIR = {
    "Foundation": "基础知识",
    "Registry": "资源目录",
    "Runbook": "操作手册",
    "FAQ": "常见问题",
    "ADR": "架构决策记录",
    "Incident": "案例与复盘",
}

# 固定小节（okf.md：按 type 固定 ## 标题，按序写满，来源没有写「来源未写」）
FIXED_HEADINGS = {
    "Foundation": ["定义", "职责与边界", "公司内使用方式", "稳定约束", "关系"],
    "Registry": ["资产", "位置与环境", "入口", "负责人", "依赖", "观测与告警", "生命周期", "凭证怎么申请"],
    "Runbook": ["触发条件", "何时用 / 何时不用", "前置检查", "步骤", "验证", "回滚", "相关系统"],
    "Incident": ["时间线", "根因", "修复", "行动项"],
    "ADR": ["背景", "决策与放弃项", "影响与约束", "落地手册"],
    "FAQ": ["问题", "答案"],
}

KNOWLEDGE_DIRS = frozenset(TYPE_DIR.values())

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# Obsidian wikilinks: [[target]], [[target#heading]], [[target#^block-id]], ![[target#heading]]
# Captures only the target (before #), for resolution against file stems.
WIKILINK_RE = re.compile(r"!?\[\[([^\]#]+)(?:#[^\]]*)?\]\]")
# Template placeholders in index.md / docs that look like wikilinks but aren't real links.
WIKILINK_PLACEHOLDERS = frozenset({"双链", "页", "页名", "X", "相关页", "Y"})
TYPE_RE = re.compile(r"^type:\s*[\"']?([A-Za-z][A-Za-z0-9]*)[\"']?\s*$", re.M)
TITLE_RE = re.compile(r"^title:\s*(.*)$", re.M)
DESCRIPTION_RE = re.compile(r"^description:\s*\S", re.M)
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
STALE_RE = re.compile(r"^stale_after:\s*[\"']?(\d{4}-\d{2}-\d{2})[\"']?\s*$", re.M)
LOG_DATE_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$", re.M)
LOG_ENTRY_RE = re.compile(
    r"^\* \*\*(Creation|Update|Deprecation|Initialization)\*\*: "
)
LOG_BAD_COLON_RE = re.compile(
    r"^\* \*\*(Creation|Update|Deprecation|Initialization)\*\*："
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMG_LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
RAW_REF_RE = re.compile(r"raw/(?:wiki/)?archive|详见\s*raw|去\s*raw")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME)\b|待补充")
# Inline backticks that carry a real command (has args or is a known CLI verb);
# these count as executable content, unlike plain config-file names.
INLINE_CMD_RE = re.compile(r"`[^`]*[A-Za-z0-9_./-]+\s+[^`]*`|`(?:kubectl|docker|git|python|curl|ssh|scp|systemctl|helm|minio|mc|yum|pip|gradle|go|sh|bash|cd|rm|ls|df|ping|openssl|mysql|clickhouse|virsh)[^\s`]*`")


def parse_title(fm: str) -> str | None:
    m = TITLE_RE.search(fm)
    if not m:
        return None
    raw = m.group(1).strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        raw = raw[1:-1]
    return raw.strip() or None


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    rest = text[3:]
    if rest.startswith("\r\n"):
        rest = rest[2:]
    elif rest.startswith("\n"):
        rest = rest[1:]
    else:
        return None, text
    end = rest.find("\n---")
    if end < 0:
        return None, text
    return rest[:end], rest[end + 4 :]


def iter_md(bundle: Path) -> list[Path]:
    """Only wiki index/log and files under the 8 knowledge directories."""
    out: list[Path] = []
    for name in RESERVED:
        p = bundle / name
        if p.is_file():
            out.append(p)
    for dirname in sorted(KNOWLEDGE_DIRS):
        d = bundle / dirname
        if not d.is_dir():
            continue
        out.extend(sorted(p for p in d.rglob("*.md") if p.is_file()))
    return out


def rel_posix(path: Path) -> str:
    return path.relative_to(BUNDLE).as_posix()


def collect_wiki_stems(bundle: Path) -> tuple[set[str], set[str]]:
    """Return (stems, posix_paths) of all concept .md files for wikilink resolution.

    stems:      basenames without .md (for short-form [[页名]])
    posix_paths: repo-root-relative paths without .md (for path-form [[wiki/分组/页名]])
    """
    stems: set[str] = set()
    posix_paths: set[str] = set()
    for dirname in sorted(KNOWLEDGE_DIRS):
        base = bundle / dirname
        if not base.is_dir():
            continue
        for p in base.rglob("*.md"):
            if p.is_file() and p.name not in RESERVED:
                stems.add(p.stem)
                posix_paths.add(p.resolve().relative_to(ROOT).with_suffix("").as_posix())
    return stems, posix_paths


def check_wikilinks(
    rel: str,
    text: str,
    stems: set[str],
    posix_paths: set[str],
    errors: list[str],
) -> None:
    """Validate that every [[target]] resolves to an existing .md file.

    Obsidian resolves wikilinks by filename (basename without .md), not by
    frontmatter title. A mismatch (e.g. file ``harbor镜像仓.md`` linked as
    ``[[Harbor 镜像仓]]``) produces a silent broken link in Obsidian.
    """
    for m in WIKILINK_RE.finditer(text):
        target = m.group(1).strip()
        if target in WIKILINK_PLACEHOLDERS:
            continue
        if target in stems or target in posix_paths:
            continue
        errors.append(
            f"{rel}: wikilink 断链 [[{target}]]——目标文件不存在"
            f"（wikilink 须用文件名而非 title，注意大小写与空格）"
        )


def resolve_link(src: Path, href: str) -> Path | None:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "http://", "https://")):
        return None
    href = href.split("#", 1)[0]
    if not href:
        return None
    if href.startswith("/"):
        # Repo-root absolute path, e.g. /wiki/操作手册/页.md or /script/foo.sh
        target = ROOT / href.lstrip("/")
    else:
        target = (src.parent / href).resolve()
        try:
            target.relative_to(BUNDLE.resolve())
        except ValueError:
            return target
    if target.is_dir():
        # Directory TOC link (./分组/): valid if the directory exists.
        # Group index.md is optional until the first concept page is written.
        return target
    return target


def collect_headings(body: str) -> list[tuple[int, str, int]]:
    """(level, title, raw_line_index) for headings outside code fences.
    Line indices match body.splitlines(), so heading_spans() can index raw
    lines and still count code-block content as section content."""
    headings: list[tuple[int, str, int]] = []
    in_fence = False
    for i, line in enumerate(body.splitlines()):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            m = HEADING_RE.match(line)
            if m:
                headings.append((len(m.group(1)), m.group(2).strip(), i))
    return headings


def heading_spans(body: str) -> list[tuple[int, str, list[str]]]:
    """(level, title, content_lines) per heading; content excludes nested
    headings but keeps code lines, so a section holding only a code block
    still counts as having content."""
    lines = body.splitlines()
    headings = collect_headings(body)
    spans: list[tuple[int, str, list[str]]] = []
    for idx, (level, title, start) in enumerate(headings):
        end = len(lines)
        for j in range(idx + 1, len(headings)):
            if headings[j][0] <= level:
                end = headings[j][2]
                break
        block = [l for l in lines[start + 1 : end] if not HEADING_RE.match(l)]
        spans.append((level, title, block))
    return spans


def is_marker_line(line: str) -> bool:
    s = line.strip()
    return s in ("（无）", "无", "来源未写", "（待补充）")


def empty_sections(body: str) -> list[str]:
    """Headings whose whole subtree has no body content at all."""
    return [t for _, t, block in heading_spans(body) if not any(l.strip() for l in block)]


def hollow_sections(body: str) -> list[str]:
    """Sub-steps (### and deeper) whose body is only 1-3 short lines with no
    code block, link, table or list — i.e. a step heading standing in for
    executable content. Fixed ## sections (触发条件/影响/验证/回滚…) may
    legitimately be one line, so only levels >= 3 are considered."""
    bad: list[str] = []
    for level, title, block in heading_spans(body):
        if level < 3:
            continue
        content = [l.strip() for l in block if l.strip()]
        if not content or all(is_marker_line(l) for l in content):
            continue
        joined = "".join(content)
        if (
            len(content) <= 3
            and len(joined) < 40
            and "```" not in joined
            and "http" not in joined
            and "](" not in joined
            and "|" not in joined
            and not any(
                l.startswith(("- ", "* ", "> ")) or re.match(r"^\d+\.", l) for l in content
            )
            and not INLINE_CMD_RE.search(joined)
        ):
            bad.append(title)
    return bad


def check_fixed_headings(rel: str, typ: str, body: str, warnings: list[str]) -> None:
    expected = {h.replace(" ", "") for h in FIXED_HEADINGS.get(typ, [])}
    if not expected:
        return
    actual = {h.replace(" ", "") for _, h, _ in collect_headings(body)}
    for want in sorted(expected - actual):
        warnings.append(
            f"{rel}: type {typ} 缺少固定小节「{want}」（okf.md 要求按序写满，来源没有写「来源未写」）"
        )


def check_images(
    rel: str, path: Path, body: str, errors: list[str], warnings: list[str]
) -> None:
    for raw_href in IMG_LINK_RE.findall(body):
        href = raw_href.strip()
        if not href or href.startswith(("http://", "https://", "data:")):
            continue
        if "_attachments" in href:
            errors.append(
                f"{rel}: 图片目录违规 {raw_href!r}（禁止 filename_attachments，应放 ./attachments/）"
            )
            continue
        if href.startswith(("./images/", "images/")):
            errors.append(
                f"{rel}: 图片目录违规 {raw_href!r}（知识页应放 ./attachments/，raw 才用 images/）"
            )
            continue
        if href.startswith("./attachments/"):
            target = (path.parent / href[2:]).resolve()
            if not target.exists():
                errors.append(f"{rel}: 图片引用断链 {raw_href!r}")
            continue
        if not href.startswith("/"):
            warnings.append(f"{rel}: 图片未放 ./attachments/：{raw_href!r}")


def check_raw_refs(rel: str, body: str, warnings: list[str]) -> None:
    for m in RAW_REF_RE.finditer(body):
        warnings.append(
            f"{rel}: 正文引用 raw 存档（{m.group(0)!r}）——知识页须自洽，不要指向 raw"
        )


def check_placeholders(rel: str, body: str, warnings: list[str]) -> None:
    for m in PLACEHOLDER_RE.finditer(body):
        warnings.append(f"{rel}: 残留占位符 {m.group(0)!r}")


def lint_log(rel: str, text: str, fm: str | None, errors: list[str], warnings: list[str]) -> None:
    if fm is not None:
        errors.append(f"{rel}: log.md must not have frontmatter")
    dates = LOG_DATE_RE.findall(text)
    if not dates:
        errors.append(f"{rel}: needs ## YYYY-MM-DD headings")
    elif dates != sorted(dates, reverse=True):
        errors.append(f"{rel}: date headings must be newest first")
    for line in text.splitlines():
        if LOG_BAD_COLON_RE.match(line):
            errors.append(f"{rel}: use ASCII colon after **Verb**, not fullwidth ：")
        elif line.startswith("* **") and not LOG_ENTRY_RE.match(line):
            warnings.append(
                f"{rel}: entry should be '* **Creation**: ...' ({line[:60]})"
            )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    today = dt.date.today()

    if not BUNDLE.is_dir():
        print("error: wiki/ not found", file=sys.stderr)
        return 2

    root_index = BUNDLE / "index.md"
    if not root_index.is_file():
        print("error: wiki/index.md not found", file=sys.stderr)
        return 2

    for dirname in sorted(KNOWLEDGE_DIRS):
        if not (BUNDLE / dirname).is_dir():
            errors.append(f"missing knowledge directory: wiki/{dirname}/")

    md_files = iter_md(BUNDLE)
    existing = {p.resolve() for p in md_files}
    wiki_stems, wiki_posix_paths = collect_wiki_stems(BUNDLE)
    dir_indexes: dict[Path, str] = {}
    concepts: list[Path] = []

    for path in md_files:
        text = path.read_text(encoding="utf-8")
        rel = rel_posix(path)
        name = path.name
        fm, _body = split_frontmatter(text)

        if name == "log.md":
            if path.parent != BUNDLE:
                errors.append(f"{rel}: log.md must live at wiki/")
            lint_log(rel, text, fm, errors, warnings)
            continue

        if name == "index.md":
            dir_indexes[path.parent.resolve()] = text
            if path.parent == BUNDLE:
                if fm is None or "okf_version:" not in fm:
                    errors.append(f"{rel}: wiki/index.md needs okf_version in frontmatter")
            elif fm is not None:
                errors.append(f"{rel}: directory index.md must not have frontmatter")
        else:
            concepts.append(path)
            if fm is None:
                errors.append(f"{rel}: missing YAML frontmatter")
                continue
            m = TYPE_RE.search(fm)
            if not m:
                errors.append(f"{rel}: frontmatter missing type")
                continue
            typ = m.group(1)
            expected_dir = TYPE_DIR.get(typ)
            if expected_dir is None:
                errors.append(f"{rel}: unknown type {typ!r}")
            else:
                parent = path.parent.relative_to(BUNDLE).as_posix()
                if parent != expected_dir and not parent.startswith(expected_dir + "/"):
                    errors.append(
                        f"{rel}: type {typ} should live under wiki/{expected_dir}/"
                    )
            title = parse_title(fm)
            if title is None:
                warnings.append(f"{rel}: frontmatter missing Chinese title")
            elif not CJK_RE.search(title):
                warnings.append(f"{rel}: title must be Chinese, got {title!r}")
            stem = path.stem
            if stem not in RESERVED and not CJK_RE.search(stem):
                warnings.append(
                    f"{rel}: filename should be Chinese, got {path.name!r}"
                )
            sm = STALE_RE.search(fm)
            if sm:
                stale = dt.date.fromisoformat(sm.group(1))
                if today >= stale:
                    warnings.append(f"{rel}: stale_after {stale.isoformat()} (today {today})")

            if typ in TYPE_DIR:
                if DESCRIPTION_RE.search(fm) is None:
                    warnings.append(f"{rel}: frontmatter missing description")
                check_fixed_headings(rel, typ, _body, warnings)
                for h in empty_sections(_body):
                    errors.append(f"{rel}: 空壳小节「{h}」——无任何正文内容")
                for h in hollow_sections(_body):
                    warnings.append(f"{rel}: 疑似空壳小节「{h}」——仅短句无命令/链接/表格")
                check_images(rel, path, _body, errors, warnings)
                check_raw_refs(rel, _body, warnings)
                check_placeholders(rel, _body, warnings)

        for raw_href in LINK_RE.findall(text):
            target = resolve_link(path, raw_href)
            if target is None:
                continue
            resolved = target.resolve() if target.exists() else target
            if not target.exists():
                warnings.append(f"{rel}: broken link ({raw_href})")
            elif target.suffix == ".md" and resolved not in existing and not target.exists():
                warnings.append(f"{rel}: broken link ({raw_href})")

        # Obsidian wikilink validation: [[target]] must match a real filename
        check_wikilinks(rel, text, wiki_stems, wiki_posix_paths, errors)

    for concept in concepts:
        idx_text = dir_indexes.get(concept.parent.resolve())
        idx_rel = rel_posix(concept.parent / "index.md")
        if idx_text is None:
            warnings.append(f"{rel_posix(concept)}: directory missing index.md")
            continue
        if concept.name not in idx_text:
            warnings.append(f"{idx_rel}: missing entry for {concept.name}")

    for line in errors:
        print(f"error: {line}")
    for line in warnings:
        print(f"warning: {line}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
