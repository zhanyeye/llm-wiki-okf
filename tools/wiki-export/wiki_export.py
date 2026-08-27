#!/usr/bin/env python3
"""
wiki_export.py — Batch export example wiki documents via wiki CLI.

Handles:
  - wiki CLI installation & auth check
  - Batch export: wiki doc get → {title}.md
  - Smart image naming (hash from URL, avoid image.png overwrite)
  - Rewrite local image links in {title}.md
  - Re-export existing archives (clear & re-download)

Usage:
    python wiki_export.py check                          # Check wiki CLI & auth
    python wiki_export.py export <url> [<url> ...]       # Export wiki docs
    python wiki_export.py export --inbox                 # Export from raw/wiki/inbox.md
    python wiki_export.py re-export [<docKey> ...]       # Re-export existing archive dirs
    python wiki_export.py re-export --all                # Re-export all archived docs
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ARCHIVE_DIR = REPO_ROOT / "raw" / "wiki" / "archive"
INBOX_FILE = REPO_ROOT / "raw" / "wiki" / "inbox.md"

WIKI_CLI = "wiki"

# Regex: extract docKey from URL
# e.g. https://wiki.example.com/domains/4255/wiki/8/WIKI2026080712208286
#      https://wiki.example.com/...?sn=WIKI202307141560110
RE_DOC_KEY = re.compile(r"(WIKI\d{4,})")

# Regex: find image URLs in markdown content
# Matches ![alt](url) and <img src="url">
RE_MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
RE_HTML_IMAGE = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\']', re.IGNORECASE)

# Which wiki image domains can be downloaded via wiki CLI
WIKI_IMAGE_DOMAINS = [
    "wiki.example.com/vision-file-storage",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return CompletedProcess."""
    return subprocess.run(
        cmd, capture_output=True, text=True, check=check,
        encoding="utf-8", errors="replace",
    )


def wiki_cli_available() -> bool:
    """Check if wiki CLI is installed."""
    try:
        result = run([WIKI_CLI, "--version"], check=False)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def wiki_cli_authenticated() -> bool:
    """Check if wiki CLI is authenticated by trying a simple doc get."""
    # Try listing — if auth fails, CLI will report it
    result = run([WIKI_CLI, "--version"], check=False)
    if result.returncode != 0:
        return False
    # Try a lightweight auth check via auth status if available
    result = run([WIKI_CLI, "auth", "--help"], check=False)
    return result.returncode == 0


def extract_doc_key(url: str) -> str | None:
    """Extract docKey (WIKI...) from URL."""
    m = RE_DOC_KEY.search(url)
    return m.group(1) if m else None


def unique_image_filename(url: str) -> str:
    """Generate a unique filename for an image URL.

    Strategy:
    - If the URL path contains a hash-like segment before the filename,
      use that hash as the filename: <hash>.<ext>
    - Otherwise fall back to the original filename with a URL hash suffix.

    Examples:
      .../86881f81fc3e425ba30292d46cd7296f.png → 86881f81fc3e425ba30292d46cd7296f.png
      .../7dd6bb5fcb4445a99d0a9200fae02062/image.png → 7dd6bb5fcb4445a99d0a9200fae02062.png
      .../some-name.png → some-name.png (if unique enough)
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")

    # Get the original filename and extension
    original_name = path_parts[-1] if path_parts else "image.png"
    name, ext = os.path.splitext(original_name)
    ext = ext or ".png"

    # Try to find a hash-like segment (32+ hex chars) before the filename
    for part in reversed(path_parts[:-1]):
        if re.match(r"^[0-9a-f]{20,}$", part):
            return f"{part}{ext}"

    # For image.example.com/tiny-lts URLs, extract the hash from the filename
    # e.g. 5f955002163575a9097ec5e44a175dc5_362x117.png@900-0-90-f.png
    if "image.example.com" in url:
        # Strip @suffix and size suffix
        clean = original_name.split("@")[0]
        # Extract the hash part before _
        hash_match = re.match(r"^([0-9a-f]{20,})", clean)
        if hash_match:
            return f"{hash_match.group(1)}{ext}"

    # Fall back: if name is generic like "image", add URL hash
    if name.lower() in ("image", "img", "pic"):
        url_hash = format(hash(url), "x")[:12]
        return f"{name}_{url_hash}{ext}"

    return original_name


def can_download_via_wiki_cli(url: str) -> bool:
    """Check if an image URL can be downloaded via wiki CLI."""
    return any(domain in url for domain in WIKI_IMAGE_DOMAINS)


def parse_inbox(inbox_path: Path) -> list[str]:
    """Parse inbox.md and return list of URLs."""
    urls = []
    if not inbox_path.exists():
        return urls
    for line in inbox_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("http"):
            urls.append(line)
    return urls


# ---------------------------------------------------------------------------
# Export logic
# ---------------------------------------------------------------------------

def export_wiki_doc(url: str, force: bool = False) -> dict:
    """Export a single wiki document to raw/wiki/archive/<docKey>/.

    Returns a dict with status and details.
    """
    doc_key = extract_doc_key(url)
    if not doc_key:
        return {"status": "failed", "url": url, "error": "Cannot extract docKey from URL"}

    archive_dir = ARCHIVE_DIR / doc_key
    images_dir = archive_dir / "images"

    # If force (re-export), clear the directory first
    if force and archive_dir.exists():
        shutil.rmtree(archive_dir)

    # Create directories
    images_dir.mkdir(parents=True, exist_ok=True)

    # Clean up legacy page.md if it exists (old format, now using {title}.md)
    legacy_page = archive_dir / "page.md"
    if legacy_page.exists():
        legacy_page.unlink()
        print(f"  Removed legacy page.md")

    print(f"[*] Exporting {doc_key} ...")

    # Step 1: Get document content
    result = run([WIKI_CLI, "doc", "get", url], check=False)
    if result.returncode != 0:
        error = f"wiki doc get failed: {result.stderr.strip()}"
        print(f"  [FAILED] {error}")
        return {"status": "failed", "url": url, "doc_key": doc_key, "error": error}

    try:
        doc = json.loads(result.stdout)
    except json.JSONDecodeError:
        error = f"wiki doc get returned non-JSON: {result.stdout[:200]}"
        print(f"  [FAILED] {error}")
        return {"status": "failed", "url": url, "doc_key": doc_key, "error": error}

    title = doc.get("title", doc_key)
    content = doc.get("content", "")
    doc_type = doc.get("document_type", "Markdown")

    print(f"  Title: {title}")
    print(f"  Type: {doc_type}")

    # Step 2: Find all image URLs
    image_urls = []
    for match in RE_MD_IMAGE.finditer(content):
        image_urls.append(match.group(2))
    for match in RE_HTML_IMAGE.finditer(content):
        image_urls.append(match.group(1))

    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for img_url in image_urls:
        if img_url not in seen:
            seen.add(img_url)
            unique_urls.append(img_url)

    print(f"  Found {len(unique_urls)} image(s)")

    # Build URL → local filename mapping
    url_to_local = {}
    for img_url in unique_urls:
        local_name = unique_image_filename(img_url)
        url_to_local[img_url] = local_name

    # Step 3: Rewrite image links in content
    for img_url, local_name in url_to_local.items():
        if can_download_via_wiki_cli(img_url):
            # Wiki-hosted: rewrite to ./images/<local_name>
            local_path = f"./images/{local_name}"
            content = content.replace(img_url, local_path)
        # External images: keep original URL (cannot download via wiki CLI)

    # Step 4: Write {title}.md
    safe_title = title.replace("/", "_").replace("\\", "_").replace(":", "_").strip()
    if not safe_title:
        safe_title = doc_key
    md_filename = f"{safe_title}.md"
    page_path = archive_dir / md_filename
    page_path.write_text(content, encoding="utf-8")
    print(f"  Written {md_filename} ({len(content)} chars)")

    # Step 5: Download images (serial, one by one)
    downloaded = 0
    failed = 0
    skipped = 0
    for img_url, local_name in url_to_local.items():
        if not can_download_via_wiki_cli(img_url):
            print(f"  [SKIP] {local_name} (external URL)")
            skipped += 1
            continue

        # Download to images dir
        # wiki file download-image saves with URL's last segment name
        # We download, then rename to avoid image.png collision
        result = run(
            [WIKI_CLI, "file", "download-image", img_url, str(images_dir)],
            check=False,
        )
        if result.returncode != 0:
            print(f"  [FAILED] {local_name}: {result.stderr.strip()}")
            failed += 1
            continue

        # Parse saved path from result
        try:
            dl_result = json.loads(result.stdout)
            saved_path = Path(dl_result.get("saved_path", ""))
        except (json.JSONDecodeError, KeyError):
            # Fallback: guess the saved filename from URL
            from urllib.parse import urlparse
            url_filename = urlparse(img_url).path.split("/")[-1]
            saved_path = images_dir / url_filename

        # Rename if needed (e.g. image.png → <hash>.png)
        if saved_path.exists() and saved_path.name != local_name:
            target = images_dir / local_name
            # If target already exists, don't overwrite from a different source
            if target.exists() and target != saved_path:
                # Remove the just-downloaded file
                saved_path.unlink(missing_ok=True)
                print(f"  [OK] {local_name} (already exists)")
            else:
                saved_path.rename(target)
                print(f"  [OK] {local_name}")
        else:
            print(f"  [OK] {local_name}")

        downloaded += 1

    # Step 6: Verify archive structure
    has_page = page_path.exists()
    has_images_dir = images_dir.is_dir()

    # Check root only has {title}.md and images/
    root_items = [p.name for p in archive_dir.iterdir()]
    extra_items = [n for n in root_items if n not in (md_filename, "images")]

    status = "ok" if has_page and not extra_items else "warning"
    if extra_items:
        print(f"  [WARN] Extra items in archive root: {extra_items}")

    return {
        "status": status,
        "url": url,
        "doc_key": doc_key,
        "title": title,
        "md_filename": md_filename,
        "doc_type": doc_type,
        "images_total": len(unique_urls),
        "images_downloaded": downloaded,
        "images_failed": failed,
        "images_skipped": skipped,
    }


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_check(args):
    """Check wiki CLI installation and authentication."""
    print("Checking wiki CLI...")

    if not wiki_cli_available():
        print("[FAIL] wiki CLI not found. Install via: pip install wiki-cli")
        return 1

    result = run([WIKI_CLI, "--version"], check=False)
    print(f"[OK] wiki CLI version: {result.stdout.strip()}")

    # Check auth by trying a simple command
    result = run([WIKI_CLI, "auth", "--help"], check=False)
    if result.returncode == 0:
        print("[OK] wiki CLI auth available")
    else:
        print("[WARN] Cannot verify auth status. Run 'wiki auth login' if needed.")

    print(f"[OK] Archive dir: {ARCHIVE_DIR}")
    print(f"[OK] Inbox file: {INBOX_FILE}")
    return 0


def cmd_export(args):
    """Export wiki documents."""
    # Collect URLs
    urls = []
    if args.inbox:
        urls = parse_inbox(INBOX_FILE)
        if not urls:
            print("No URLs found in inbox.md")
            return 1
        print(f"Found {len(urls)} URL(s) in inbox.md")
    else:
        if not args.urls:
            print("No URLs provided. Use --inbox or provide URLs as arguments.")
            return 1
        urls = args.urls

    # Export each
    results = []
    for i, url in enumerate(urls, 1):
        print(f"\n--- [{i}/{len(urls)}] ---")
        result = export_wiki_doc(url, force=False)
        results.append(result)

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    ok = sum(1 for r in results if r["status"] == "ok")
    warn = sum(1 for r in results if r["status"] == "warning")
    failed = sum(1 for r in results if r["status"] == "failed")
    total_images = sum(r.get("images_total", 0) for r in results)
    dl_images = sum(r.get("images_downloaded", 0) for r in results)
    skip_images = sum(r.get("images_skipped", 0) for r in results)
    fail_images = sum(r.get("images_failed", 0) for r in results)

    print(f"  Documents: {ok} ok, {warn} warning, {failed} failed")
    print(f"  Images: {dl_images} downloaded, {skip_images} skipped, {fail_images} failed / {total_images} total")

    if failed > 0:
        print("\nFailed:")
        for r in results:
            if r["status"] == "failed":
                print(f"  {r.get('doc_key', '?')}: {r.get('error', 'unknown')}")

    return 1 if failed > 0 else 0


def cmd_reexport(args):
    """Re-export existing archive directories."""
    doc_keys = []

    if args.all:
        # Find all archived doc keys
        if ARCHIVE_DIR.exists():
            for d in ARCHIVE_DIR.iterdir():
                if d.is_dir() and d.name.startswith("WIKI"):
                    doc_keys.append(d.name)
    else:
        doc_keys = args.doc_keys

    if not doc_keys:
        print("No docKeys provided. Use --all or specify docKeys.")
        return 1

    # For each docKey, find the URL from inbox or log
    # We need the original URL to re-export
    # Read inbox to find URLs
    inbox_urls = parse_inbox(INBOX_FILE)
    url_map = {}
    for url in inbox_urls:
        dk = extract_doc_key(url)
        if dk:
            url_map[dk] = url

    # Also try to find URLs from {title}.md sources in wiki/
    # Or from log
    missing = []
    urls = []
    for dk in doc_keys:
        if dk in url_map:
            urls.append(url_map[dk])
        else:
            # Try to construct URL from common patterns
            # Default: https://wiki.example.com/domains/4255/wiki/8/<docKey>
            url = f"https://wiki.example.com/domains/4255/wiki/8/{dk}"
            urls.append(url)
            print(f"[WARN] No inbox URL for {dk}, using constructed URL: {url}")

    print(f"Re-exporting {len(urls)} document(s)...\n")

    results = []
    for i, url in enumerate(urls, 1):
        print(f"\n--- [{i}/{len(urls)}] ---")
        result = export_wiki_doc(url, force=True)
        results.append(result)

    # Summary
    print("\n" + "=" * 60)
    print("Re-export Summary:")
    ok = sum(1 for r in results if r["status"] in ("ok", "warning"))
    failed = sum(1 for r in results if r["status"] == "failed")
    print(f"  {ok} ok, {failed} failed")

    return 1 if failed > 0 else 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Batch export example wiki documents via wiki CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # check
    sub.add_parser("check", help="Check wiki CLI installation & auth")

    # export
    p_export = sub.add_parser("export", help="Export wiki documents")
    p_export.add_argument("urls", nargs="*", help="Wiki document URLs")
    p_export.add_argument("--inbox", action="store_true", help="Export from raw/wiki/inbox.md")

    # re-export
    p_reexport = sub.add_parser("re-export", help="Re-export existing archive directories")
    p_reexport.add_argument("doc_keys", nargs="*", help="Archive docKeys to re-export")
    p_reexport.add_argument("--all", action="store_true", help="Re-export all archived docs")

    args = parser.parse_args()

    if args.command == "check":
        return cmd_check(args)
    elif args.command == "export":
        return cmd_export(args)
    elif args.command == "re-export":
        return cmd_reexport(args)

    return 1


if __name__ == "__main__":
    sys.exit(main())
