#!/usr/bin/env python3
"""
wiki_inbox_meta.py — Fetch metadata (title, last_update_time) for all inbox URLs
and generate an enhanced inbox.md with structured entries.

Usage:
    python wiki_inbox_meta.py fetch          # Fetch metadata and print JSON
    python wiki_inbox_meta.py generate       # Generate enhanced inbox.md
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INBOX_FILE = REPO_ROOT / "raw" / "wiki" / "inbox.md"
ARCHIVE_DIR = REPO_ROOT / "raw" / "wiki" / "archive"
META_CACHE = REPO_ROOT / "raw" / "wiki" / "inbox_meta.json"

RE_DOC_KEY = re.compile(r"(WIKI\d{4,})")
WIKI_CLI = "wiki"


def run(cmd, check=True):
    return subprocess.run(
        cmd, capture_output=True, text=True, check=check,
        encoding="utf-8", errors="replace",
    )


def extract_doc_key(url):
    m = RE_DOC_KEY.search(url)
    return m.group(1) if m else None


def parse_inbox(inbox_path):
    """Parse inbox.md, return list of URLs.

    Supports both plain URL format (one URL per line) and table format
    (| # | URL | 标题 | 最近更新 | docKey |), consistent with wiki_export.py.
    """
    urls = []
    seen = set()
    if not inbox_path.exists():
        return urls
    for line in inbox_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("http"):
            if line not in seen:
                urls.append(line)
                seen.add(line)
            continue
        if line.startswith("|"):
            for match in re.finditer(r"(https?://\S+?)(?:\s*\||$)", line):
                url = match.group(1).rstrip("|").strip()
                if url and url not in seen:
                    urls.append(url)
                    seen.add(url)
    return urls


def fetch_url_metadata(url):
    """Fetch metadata for a single URL using wiki CLI fetch_wiki_content equivalent."""
    try:
        result = run(["wiki", "doc", "get", url], check=False)
        if result.returncode != 0:
            return {"url": url, "status": "failed", "error": result.stderr.strip()[:200]}
        doc = json.loads(result.stdout)
        return {
            "url": url,
            "doc_key": extract_doc_key(url),
            "title": doc.get("title", ""),
            "last_update_time": doc.get("last_update_time", ""),
            "document_type": doc.get("document_type", ""),
            "status": "ok",
        }
    except Exception as e:
        return {"url": url, "status": "failed", "error": str(e)[:200]}


def load_existing_meta():
    """Load existing metadata cache if available."""
    if META_CACHE.exists():
        try:
            return json.loads(META_CACHE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, KeyError):
            return {}
    return {}


def cmd_fetch(args):
    """Fetch metadata for all inbox URLs."""
    urls = parse_inbox(INBOX_FILE)
    if not urls:
        print("No URLs found in inbox.md")
        return 1

    existing = load_existing_meta()

    results = []
    for i, url in enumerate(urls, 1):
        dk = extract_doc_key(url)
        print(f"[{i}/{len(urls)}] Fetching {dk or url}...", end=" ", flush=True)
        meta = fetch_url_metadata(url)
        if meta["status"] == "ok":
            print(f"OK — {meta['title'][:40]} (updated: {meta['last_update_time'][:10]})")
        else:
            print(f"FAILED — {meta.get('error', 'unknown')[:80]}")
        results.append(meta)

    # Save cache
    cache = {r["url"]: r for r in results if r["status"] == "ok"}
    META_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nMetadata cached to {META_CACHE}")

    ok = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] == "failed")
    print(f"Summary: {ok} ok, {failed} failed / {len(urls)} total")

    return 1 if failed > 0 else 0


def cmd_generate(args):
    """Generate enhanced inbox.md from metadata cache."""
    urls = parse_inbox(INBOX_FILE)
    cache = load_existing_meta()

    if not cache:
        print("No metadata cache found. Run 'fetch' first.")
        return 1

    lines = [
        "# Wiki 来源登记册",
        "",
        "格式：| URL | 标题 | 最近更新 | docKey |",
        "增量刷新：对比「最近更新」与上次编译时间判断是否需要重编译。",
        "",
    ]

    # Table header
    lines.append("| # | URL | 标题 | 最近更新 | docKey |")
    lines.append("|---|-----|------|---------|--------|")

    for i, url in enumerate(urls, 1):
        dk = extract_doc_key(url) or ""
        meta = cache.get(url, {})
        title = meta.get("title", "") if meta else ""
        last_update = meta.get("last_update_time", "")[:10] if meta else ""

        if not title or not last_update:
            # Mark as metadata missing
            title = title or "(未获取)"
            last_update = last_update or "(未知)"

        # Escape pipe chars in title
        title_safe = title.replace("|", "\\|")
        lines.append(f"| {i} | {url} | {title_safe} | {last_update} | {dk} |")

    lines.append("")
    content = "\n".join(lines)

    # Backup original inbox.md
    backup = INBOX_FILE.with_suffix(".md.bak")
    if INBOX_FILE.exists():
        backup.write_text(INBOX_FILE.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Original inbox.md backed up to {backup}")

    INBOX_FILE.write_text(content, encoding="utf-8")
    print(f"Enhanced inbox.md written to {INBOX_FILE}")

    return 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Inbox metadata helper")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("fetch", help="Fetch metadata for all inbox URLs")
    sub.add_parser("generate", help="Generate enhanced inbox.md from cache")

    args = parser.parse_args()
    if args.command == "fetch":
        return cmd_fetch(args)
    elif args.command == "generate":
        return cmd_generate(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
