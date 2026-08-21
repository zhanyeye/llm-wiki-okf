#!/usr/bin/env python3
"""Lint wiki/ as an OKF-style markdown bundle. Stdlib only. UTF-8 paths."""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"

RESERVED = {"index.md", "log.md"}

TYPE_DIR = {
    "Registry": "资源注册表",
    "Architecture": "系统与架构",
    "Runbook": "操作手册",
    "Configuration": "操作手册",
    "Playbook": "故障排查",
    "Decision": "架构决策记录",
    "FAQ": "常见问题",
    "Policy": "规范与约束",
    "Incident": "案例与复盘",
    "Curriculum": "技能地图",
    "Onboarding": "新人上手",
    "Automation": "自动化脚本",
}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TYPE_RE = re.compile(r"^type:\s*[\"']?([A-Za-z][A-Za-z0-9]*)[\"']?\s*$", re.M)
STALE_RE = re.compile(r"^stale_after:\s*[\"']?(\d{4}-\d{2}-\d{2})[\"']?\s*$", re.M)
LOG_DATE_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$", re.M)
LOG_ENTRY_RE = re.compile(
    r"^\* \*\*(Creation|Update|Deprecation|Initialization)\*\*: "
)
LOG_BAD_COLON_RE = re.compile(
    r"^\* \*\*(Creation|Update|Deprecation|Initialization)\*\*："
)


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


def iter_md(wiki: Path) -> list[Path]:
    return sorted(p for p in wiki.rglob("*.md") if p.is_file())


def rel_posix(path: Path) -> str:
    return path.relative_to(WIKI).as_posix()


def resolve_link(src: Path, href: str) -> Path | None:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "http://", "https://")):
        return None
    href = href.split("#", 1)[0]
    if not href:
        return None
    if href.startswith("/"):
        target = WIKI / href.lstrip("/")
    else:
        target = (src.parent / href).resolve()
        try:
            target.relative_to(WIKI.resolve())
        except ValueError:
            return target
    if target.is_dir():
        return target / "index.md"
    return target


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

    if not WIKI.is_dir():
        print("error: wiki/ not found", file=sys.stderr)
        return 2

    md_files = iter_md(WIKI)
    existing = {p.resolve() for p in md_files}
    dir_indexes: dict[Path, str] = {}
    concepts: list[Path] = []

    for path in md_files:
        text = path.read_text(encoding="utf-8")
        rel = rel_posix(path)
        name = path.name
        fm, _body = split_frontmatter(text)

        if name == "log.md":
            lint_log(rel, text, fm, errors, warnings)
            continue

        if name == "index.md":
            dir_indexes[path.parent.resolve()] = text
            if path.parent == WIKI:
                if fm is None or "okf_version:" not in fm:
                    errors.append(f"{rel}: root index.md needs okf_version in frontmatter")
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
                parent = path.parent.relative_to(WIKI).as_posix()
                if parent != expected_dir:
                    errors.append(
                        f"{rel}: type {typ} should live under wiki/{expected_dir}/"
                    )
            sm = STALE_RE.search(fm)
            if sm:
                stale = dt.date.fromisoformat(sm.group(1))
                if today >= stale:
                    warnings.append(f"{rel}: stale_after {stale.isoformat()} (today {today})")

        for raw_href in LINK_RE.findall(text):
            target = resolve_link(path, raw_href)
            if target is None:
                continue
            resolved = target.resolve() if target.exists() else target
            if not target.exists():
                warnings.append(f"{rel}: broken link ({raw_href})")
            elif target.suffix == ".md" and resolved not in existing and not target.exists():
                warnings.append(f"{rel}: broken link ({raw_href})")

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
