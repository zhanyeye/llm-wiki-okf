#!/usr/bin/env python3
"""Lint the layered OKF knowledge graph. Stdlib only."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

RESERVED = {"index.md", "log.md"}
TYPE_DIR = {
    "Atomic": "基础知识",
    "Registry": "资源注册表",
    "Architecture": "系统与架构",
    "Runbook": "操作手册",
    "Playbook": "故障排查",
    "Decision": "架构决策记录",
    "FAQ": "常见问题",
    "Incident": "案例与复盘",
    "Onboarding": "新人上手",
}
TYPE_LAYER = {
    "Atomic": "atomic",
    "Registry": "registry",
    "Architecture": "operational",
    "Runbook": "operational",
    "Playbook": "operational",
    "Decision": "operational",
    "FAQ": "operational",
    "Incident": "operational",
    "Onboarding": "operational",
}
ATOMIC_KINDS = {"concept", "component", "platform", "policy", "capability"}
ASSET_KINDS = {
    "cluster",
    "namespace",
    "application",
    "database",
    "middleware",
    "domain",
    "certificate",
    "bucket",
    "dashboard",
    "alert",
    "network",
    "observability",
}
RELATION_FIELDS = {
    "technology",
    "instance_of",
    "depends_on",
    "operates_on",
    "answers_about",
    "decides_for",
    "runbooks",
    "playbooks",
    "used_by",
}
LOWER_LINK_TYPES = {"Atomic", "Registry"}
STATUS_VALUES = {"draft", "stable", "deprecated"}

MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.M)
BLOCK_RE = re.compile(r"(?:^|\s)\^([a-z0-9][a-z0-9-]*)\s*$", re.M)
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
LOG_DATE_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$", re.M)
LOG_ENTRY_RE = re.compile(
    r"^\* \*\*(Creation|Update|Deprecation|Initialization|Execution)\*\*: "
)
LOG_BAD_COLON_RE = re.compile(
    r"^\* \*\*(Creation|Update|Deprecation|Initialization|Execution)\*\*："
)


@dataclass
class Doc:
    path: Path
    rel: str
    text: str
    fm: str
    body: str
    typ: str
    title: str
    doc_id: str
    headings: set[str]
    blocks: set[str]


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not match:
        return None, text
    return match.group(1), text[match.end() :]


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def scalar(fm: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:[ \t]*(.*?)[ \t]*$", fm, re.M)
    return unquote(match.group(1)) if match else ""


def has_key(fm: str, key: str) -> bool:
    return re.search(rf"^{re.escape(key)}:", fm, re.M) is not None


def list_values(fm: str, key: str) -> list[str]:
    match = re.search(rf"^{re.escape(key)}:[ \t]*(.*?)[ \t]*$", fm, re.M)
    if not match:
        return []
    inline = match.group(1).strip()
    if inline.startswith("[") and inline.endswith("]"):
        return [
            unquote(item.strip())
            for item in inline[1:-1].split(",")
            if item.strip()
        ]
    values: list[str] = []
    lines = fm[match.end() :].splitlines()
    for line in lines:
        if not line.strip():
            continue
        item = re.match(r"^\s+-\s+(.*?)\s*$", line)
        if item:
            values.append(unquote(item.group(1)))
            continue
        if not line.startswith((" ", "\t")):
            break
    return values


def rel_posix(path: Path, bundle: Path) -> str:
    return path.relative_to(bundle).as_posix()


def iter_markdown(bundle: Path) -> list[Path]:
    paths = [p for p in (bundle / "index.md", bundle / "log.md") if p.is_file()]
    for dirname in TYPE_DIR.values():
        directory = bundle / dirname
        if directory.is_dir():
            paths.extend(sorted(p for p in directory.rglob("*.md") if p.is_file()))
    return paths


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
            errors.append(f"{rel}: use ASCII colon after **Verb**")
        elif line.startswith("* **") and not LOG_ENTRY_RE.match(line):
            warnings.append(f"{rel}: invalid log entry ({line[:60]})")


def normalize_wikilink(raw: str) -> tuple[str, str]:
    target = raw.split("|", 1)[0].strip()
    if "#" in target:
        page, anchor = target.split("#", 1)
    else:
        page, anchor = target, ""
    return page.strip(), anchor.strip()


def resolve_wikipage(
    page: str,
    source: Doc | None,
    bundle: Path,
    by_stem: dict[str, list[Doc]],
    by_path: dict[str, Doc],
) -> tuple[Doc | None, str]:
    if not page:
        return source, ""
    normalized = page.replace("\\", "/").strip("/")
    if normalized.startswith("wiki/"):
        normalized = normalized[5:]
    if normalized.endswith(".md"):
        normalized = normalized[:-3]
    if "/" in normalized:
        found = by_path.get(normalized) or by_path.get(normalized + ".md")
        return found, "" if found else "missing"
    matches = by_stem.get(Path(normalized).name.casefold(), [])
    if len(matches) == 1:
        return matches[0], ""
    if not matches:
        return None, "missing"
    return None, "ambiguous"


def resolve_wikilink(
    raw: str,
    source: Doc | None,
    bundle: Path,
    by_stem: dict[str, list[Doc]],
    by_path: dict[str, Doc],
) -> tuple[Doc | None, str]:
    page, anchor = normalize_wikilink(raw)
    target, problem = resolve_wikipage(page, source, bundle, by_stem, by_path)
    if problem or target is None:
        return None, problem or "missing"
    if anchor.startswith("^"):
        if anchor[1:] not in target.blocks:
            return None, "missing block"
    elif anchor and anchor not in target.headings:
        return None, "missing heading"
    return target, ""


def resolve_markdown_link(href: str, src: Path, root: Path, bundle: Path) -> Path | None:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "http://", "https://")):
        return None
    href = href.split("#", 1)[0]
    if not href:
        return None
    if href.startswith("/wiki/"):
        return root / href.lstrip("/")
    if href.startswith("/"):
        return bundle / href.lstrip("/")
    return (src.parent / href).resolve()


def manifest_items(text: str) -> list[dict[str, str]]:
    section = re.search(r"(?ms)^items:\s*\n(.*?)(?=^outputs:|\Z)", text)
    if not section:
        return []
    blocks = re.findall(
        r"(?ms)^  - id:[ \t]*(.*?)\n(.*?)(?=^  - id:|\Z)", section.group(1)
    )
    items: list[dict[str, str]] = []
    for item_id, block in blocks:
        item = {"id": unquote(item_id)}
        for key in ("kind", "summary", "disposition", "target", "reason"):
            match = re.search(
                rf"^[ \t]+{key}:[ \t]*(.*?)[ \t]*$", block, re.M
            )
            if match:
                item[key] = unquote(match.group(1))
        items.append(item)
    return items


def run(root: Path) -> tuple[list[str], list[str]]:
    bundle = root / "wiki"
    errors: list[str] = []
    warnings: list[str] = []
    if not bundle.is_dir():
        return [f"wiki/ not found under {root}"], warnings
    if not (bundle / "index.md").is_file():
        errors.append("wiki/index.md not found")
    for dirname in TYPE_DIR.values():
        if not (bundle / dirname).is_dir():
            errors.append(f"missing knowledge directory: wiki/{dirname}/")

    docs: list[Doc] = []
    dir_indexes: dict[Path, str] = {}
    markdown_files = iter_markdown(bundle)
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        rel = rel_posix(path, bundle)
        fm, body = split_frontmatter(text)
        if path.name == "log.md":
            lint_log(rel, text, fm, errors, warnings)
            continue
        if path.name == "index.md":
            dir_indexes[path.parent.resolve()] = text
            if path.parent == bundle:
                if fm is None or not has_key(fm, "okf_version"):
                    errors.append(f"{rel}: wiki/index.md needs okf_version")
            elif fm is not None:
                errors.append(f"{rel}: directory index.md must not have frontmatter")
            continue
        if fm is None:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue
        typ = scalar(fm, "type")
        title = scalar(fm, "title")
        doc_id = scalar(fm, "id")
        headings = {h.strip() for h in HEADING_RE.findall(body)}
        blocks = set(BLOCK_RE.findall(body))
        docs.append(Doc(path, rel, text, fm, body, typ, title, doc_id, headings, blocks))

    by_stem: dict[str, list[Doc]] = defaultdict(list)
    by_path: dict[str, Doc] = {}
    ids: dict[str, Doc] = {}
    block_owners: dict[str, list[Doc]] = defaultdict(list)
    inbound: dict[str, int] = defaultdict(int)
    manifest_sources: set[str] = set()

    for doc in docs:
        by_stem[doc.path.stem.casefold()].append(doc)
        relative = doc.path.relative_to(bundle).as_posix()
        by_path[relative] = doc
        by_path[relative.removesuffix(".md")] = doc
        if not doc.typ:
            errors.append(f"{doc.rel}: frontmatter missing type")
        elif doc.typ not in TYPE_DIR:
            errors.append(f"{doc.rel}: unknown type {doc.typ!r}")
        else:
            top = doc.path.relative_to(bundle).parts[0]
            if top != TYPE_DIR[doc.typ]:
                errors.append(f"{doc.rel}: type {doc.typ} should live under wiki/{TYPE_DIR[doc.typ]}/")
        if not doc.doc_id:
            errors.append(f"{doc.rel}: frontmatter missing stable id")
        elif doc.doc_id in ids:
            errors.append(f"{doc.rel}: duplicate id {doc.doc_id!r} (also {ids[doc.doc_id].rel})")
        else:
            ids[doc.doc_id] = doc
        expected_layer = TYPE_LAYER.get(doc.typ)
        layer = scalar(doc.fm, "layer")
        if layer and expected_layer and layer != expected_layer:
            errors.append(f"{doc.rel}: layer must be {expected_layer!r} for {doc.typ}")
        if not doc.title:
            warnings.append(f"{doc.rel}: frontmatter missing title")
        elif not CJK_RE.search(doc.title):
            warnings.append(f"{doc.rel}: title should contain Chinese")
        if not CJK_RE.search(doc.path.stem):
            warnings.append(f"{doc.rel}: filename should contain Chinese")
        status = scalar(doc.fm, "status")
        if status and status not in STATUS_VALUES:
            warnings.append(f"{doc.rel}: unknown status {status!r}")
        stale = scalar(doc.fm, "stale_after")
        if stale:
            try:
                if dt.date.today() >= dt.date.fromisoformat(stale[:10]):
                    warnings.append(f"{doc.rel}: stale_after {stale}")
            except ValueError:
                errors.append(f"{doc.rel}: invalid stale_after {stale!r}")
        verified_by = ""
        verified = re.search(r"^verified:\s*\n\s+by:\s*(.*?)\s*$", doc.fm, re.M)
        if verified:
            verified_by = unquote(verified.group(1))
        if verified_by and not verified_by.startswith("human:"):
            errors.append(f"{doc.rel}: verified.by must be human:<id>")
        if doc.typ == "Atomic":
            kind = scalar(doc.fm, "kind")
            if kind not in ATOMIC_KINDS:
                errors.append(f"{doc.rel}: Atomic kind must be one of {sorted(ATOMIC_KINDS)}")
        if doc.typ == "Registry":
            asset_kind = scalar(doc.fm, "asset_kind")
            if asset_kind not in ASSET_KINDS:
                errors.append(f"{doc.rel}: Registry asset_kind must be one of {sorted(ASSET_KINDS)}")
            if not list_values(doc.fm, "technology"):
                errors.append(f"{doc.rel}: Registry needs technology wikilink to Atomic")
            for key in ("name", "environment", "owner", "entries"):
                if not has_key(doc.fm, key):
                    warnings.append(f"{doc.rel}: Registry missing {key}")
            profile_fields = {
                "database": ("backup", "retention"),
                "domain": ("dns", "certificate"),
                "certificate": ("covered_domains", "expires_at", "runbooks"),
                "cluster": ("alerts", "runbooks"),
            }
            for key in profile_fields.get(asset_kind, ()):
                if not has_key(doc.fm, key) and key.replace("_", " ") not in doc.body.casefold():
                    warnings.append(f"{doc.rel}: {asset_kind} profile missing {key} or explicit gap")
        for block in doc.blocks:
            block_owners[block].append(doc)

    for block, owners in block_owners.items():
        if len(owners) > 1:
            warnings.append(f"duplicate block id ^{block}: {', '.join(d.rel for d in owners)}")

    for doc in docs:
        lower_links = 0
        for raw in WIKILINK_RE.findall(doc.text):
            target, problem = resolve_wikilink(raw, doc, bundle, by_stem, by_path)
            if problem:
                errors.append(f"{doc.rel}: invalid wikilink [[{raw}]] ({problem})")
            elif target:
                inbound[target.rel] += 1
                if target.typ in LOWER_LINK_TYPES:
                    lower_links += 1
        for field in RELATION_FIELDS:
            for value in list_values(doc.fm, field):
                if not WIKILINK_RE.fullmatch(value):
                    errors.append(f"{doc.rel}: {field} value must be a quoted wikilink ({value})")
        for href in MD_LINK_RE.findall(doc.text):
            target = resolve_markdown_link(href, doc.path, root, bundle)
            if target is not None and not target.exists():
                warnings.append(f"{doc.rel}: broken markdown link ({href})")
        if doc.typ in {"Runbook", "Playbook", "FAQ", "Decision", "Architecture"} and lower_links == 0:
            warnings.append(f"{doc.rel}: operational page has no Atomic/Registry content link")
        index_text = dir_indexes.get(doc.path.parent.resolve())
        if index_text is None:
            warnings.append(f"{doc.rel}: directory missing index.md")
        elif doc.path.name not in index_text:
            warnings.append(f"{rel_posix(doc.path.parent / 'index.md', bundle)}: missing entry for {doc.path.name}")

    for doc in docs:
        if doc.typ == "Atomic" and inbound[doc.rel] == 0:
            warnings.append(f"{doc.rel}: orphan Atomic page has no inbound content link")

    manifest_dir = bundle / "_meta" / "ingest"
    for path in sorted(manifest_dir.glob("*.yaml")) if manifest_dir.is_dir() else []:
        text = path.read_text(encoding="utf-8")
        rel = rel_posix(path, bundle)
        source = scalar(text, "source")
        if source:
            manifest_sources.add(source)
        status = scalar(text, "status")
        if status not in {"compiled", "no-material", "failed", "skipped"}:
            errors.append(f"{rel}: invalid manifest status {status!r}")
        items = manifest_items(text)
        if status == "compiled" and not items:
            errors.append(f"{rel}: compiled manifest has no items")
        for item in items:
            disposition = item.get("disposition", "")
            if disposition not in {"compiled", "duplicate", "excluded", "gap"}:
                errors.append(f"{rel}: item {item['id']} has invalid disposition {disposition!r}")
                continue
            if disposition in {"compiled", "duplicate"}:
                target_value = item.get("target", "")
                match = WIKILINK_RE.fullmatch(target_value)
                if not match:
                    errors.append(f"{rel}: item {item['id']} needs wikilink target")
                else:
                    _, problem = resolve_wikilink(match.group(1), None, bundle, by_stem, by_path)
                    if problem:
                        errors.append(f"{rel}: item {item['id']} target invalid ({problem})")
            elif not item.get("reason"):
                errors.append(f"{rel}: item {item['id']} {disposition} needs reason")

    for doc in docs:
        for source in list_values(doc.fm, "sources"):
            if source.startswith(("http://", "https://", "raw/")) and source not in manifest_sources:
                warnings.append(f"{doc.rel}: source has no coverage manifest ({source})")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repository root containing wiki/",
    )
    args = parser.parse_args(argv)
    errors, warnings = run(args.root.resolve())
    for line in errors:
        print(f"error: {line}")
    for line in warnings:
        print(f"warning: {line}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
