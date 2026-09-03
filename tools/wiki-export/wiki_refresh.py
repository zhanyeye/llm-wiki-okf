#!/usr/bin/env python3
"""
wiki_refresh.py — Incremental refresh: compare wiki last_update_time with
local compile timestamp to determine which docs need re-compile.

Usage:
    python wiki_refresh.py diff           # Show which docs need re-compile
    python wiki_refresh.py re-export-changed   # Re-export only changed docs
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INBOX_META = REPO_ROOT / "raw" / "wiki" / "inbox_meta.json"
ARCHIVE_DIR = REPO_ROOT / "raw" / "wiki" / "archive"
WIKI_DIR = REPO_ROOT / "wiki"
LOG_FILE = WIKI_DIR / "log.md"

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


def load_inbox_meta():
    """Load inbox metadata cache."""
    if INBOX_META.exists():
        return json.loads(INBOX_META.read_text(encoding="utf-8"))
    return {}


def get_compile_dates():
    """Extract compile dates for each wiki URL from log.md.

    Returns dict: url -> latest compile date string (YYYY-MM-DD).
    """
    compile_dates = {}
    if not LOG_FILE.exists():
        return compile_dates

    content = LOG_FILE.read_text(encoding="utf-8")
    # Find all date headers and ingest compiled lines
    current_date = None
    for line in content.splitlines():
        # Date header: ## 2026-08-28
        m = re.match(r"^## (\d{4}-\d{2}-\d{2})", line)
        if m:
            current_date = m.group(1)
            continue
        # Ingest compiled line:
        # * **Update**: ingest compiled https://... → [标题](/wiki/...).
        m = re.match(r"\* \*\*Update\*\*: ingest compiled (https?://\S+?)(?:\s|→)", line)
        if m and current_date:
            url = m.group(1)
            # Keep the latest compile date
            if url not in compile_dates or current_date > compile_dates[url]:
                compile_dates[url] = current_date

    return compile_dates


def get_skipped_failed_urls():
    """Get URLs that were marked as skipped or failed in log.md."""
    result = {"skipped": set(), "failed": set()}
    if not LOG_FILE.exists():
        return result

    content = LOG_FILE.read_text(encoding="utf-8")
    for line in content.splitlines():
        m = re.match(r"\* \*\*Update\*\*: ingest skipped (https?://\S+?)(?:\s|—)", line)
        if m:
            result["skipped"].add(m.group(1))
        m = re.match(r"\* \*\*Update\*\*: ingest failed (https?://\S+?)(?:\s|—)", line)
        if m:
            result["failed"].add(m.group(1))

    return result


def cmd_diff(args):
    """Show which docs need re-compile based on update time vs compile time."""
    meta = load_inbox_meta()
    compile_dates = get_compile_dates()
    skipped_failed = get_skipped_failed_urls()

    if not meta:
        print("No inbox metadata found. Run wiki_inbox_meta.py fetch first.")
        return 1

    needs_refresh = []
    up_to_date = []
    skipped = []
    failed = []
    no_compile_date = []

    all_urls = set()
    for url, info in meta.items():
        if info.get("status") != "ok":
            failed.append((url, info.get("error", "unknown")))
            continue
        all_urls.add(url)

    for url in sorted(all_urls):
        info = meta[url]
        last_update = info.get("last_update_time", "")[:10]
        title = info.get("title", "")
        dk = info.get("doc_key", "")

        if url in skipped_failed["skipped"]:
            skipped.append((url, title, last_update, "skipped"))
            continue
        if url in skipped_failed["failed"]:
            skipped.append((url, title, last_update, "failed"))
            continue

        compile_date = compile_dates.get(url)
        if not compile_date:
            no_compile_date.append((url, title, last_update, dk))
            continue

        if last_update > compile_date:
            needs_refresh.append((url, title, last_update, compile_date, dk))
        else:
            up_to_date.append((url, title, last_update, compile_date, dk))

    # Print results
    if needs_refresh:
        print(f"\n=== NEEDS REFRESH ({len(needs_refresh)}) ===")
        print(f"{'docKey':<30} {'标题':<30} {'更新':<12} {'编译':<12}")
        print("-" * 84)
        for url, title, upd, comp, dk in needs_refresh:
            print(f"{dk:<30} {title[:28]:<30} {upd:<12} {comp:<12}")

    if no_compile_date:
        print(f"\n=== NO COMPILE DATE ({len(no_compile_date)}) ===")
        for url, title, upd, dk in no_compile_date:
            print(f"  {dk}: {title[:40]} (updated {upd})")

    if up_to_date:
        print(f"\n=== UP TO DATE ({len(up_to_date)}) ===")
        for url, title, upd, comp, dk in up_to_date:
            print(f"  {dk}: {title[:30]} (updated {upd}, compiled {comp})")

    if skipped:
        print(f"\n=== SKIPPED / FAILED ({len(skipped)}) ===")
        for url, title, upd, reason in skipped:
            print(f"  {extract_doc_key(url)}: {reason} — {title[:30]}")

    print(f"\n总计: {len(needs_refresh)} 需刷新, {len(up_to_date)} 最新, "
          f"{len(no_compile_date)} 无编译记录, {len(skipped)} skipped/failed")

    return 0


def cmd_reexport_changed(args):
    """Re-export only docs whose last_update_time > compile date."""
    meta = load_inbox_meta()
    compile_dates = get_compile_dates()
    skipped_failed = get_skipped_failed_urls()

    needs_refresh = []
    for url, info in meta.items():
        if info.get("status") != "ok":
            continue
        if url in skipped_failed["skipped"] or url in skipped_failed["failed"]:
            continue
        last_update = info.get("last_update_time", "")[:10]
        compile_date = compile_dates.get(url)
        if not compile_date or last_update > compile_date:
            needs_refresh.append(url)

    if not needs_refresh:
        print("All docs are up to date. Nothing to re-export.")
        return 0

    print(f"Re-exporting {len(needs_refresh)} changed doc(s)...")
    for i, url in enumerate(needs_refresh, 1):
        dk = extract_doc_key(url) or url
        print(f"[{i}/{len(needs_refresh)}] {dk}")

    # Use wiki_export.py for the actual re-export
    result = run([
        sys.executable,
        str(REPO_ROOT / "tools" / "wiki-export" / "wiki_export.py"),
        "re-export",
    ] + [extract_doc_key(u) for u in needs_refresh], check=False)

    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Wiki incremental refresh helper")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("diff", help="Show which docs need re-compile")
    sub.add_parser("re-export-changed", help="Re-export only changed docs")

    args = parser.parse_args()
    if args.command == "diff":
        return cmd_diff(args)
    elif args.command == "re-export-changed":
        return cmd_reexport_changed(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
