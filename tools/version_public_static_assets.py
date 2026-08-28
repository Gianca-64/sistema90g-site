#!/usr/bin/env python3

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")
if not root.is_dir():
    raise SystemExit(f"ERRORE: directory pubblica non trovata: {root}")

ATTR_RE = re.compile(r'''(?P<prefix>(?:src|href)\s*=\s*["'])(?P<url>[^"']+)(?P<suffix>["'])''', re.IGNORECASE)
ASSET_EXTS = {".css", ".js"}


def resolve_asset(source: Path, raw_path: str) -> Path | None:
    if raw_path.startswith("/"):
        candidate = root / raw_path.lstrip("/")
    else:
        candidate = source.parent / raw_path

    try:
        candidate = candidate.resolve()
        public_root = root.resolve()
        candidate.relative_to(public_root)
    except (OSError, ValueError):
        return None

    return candidate if candidate.is_file() else None


def content_version(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()[:12]


changed_files = 0
rewritten_refs = 0
missing_assets: list[str] = []

for html in sorted(root.rglob("*.html")):
    text = html.read_text("utf-8", errors="ignore")

    def replace(match: re.Match[str]) -> str:
        nonlocal_rewritten = 0
        raw = match.group("url").strip()

        if not raw or raw.startswith(("http://", "https://", "//", "data:", "mailto:", "tel:", "#", "javascript:")):
            return match.group(0)

        parsed = urlsplit(raw)
        if Path(parsed.path).suffix.lower() not in ASSET_EXTS:
            return match.group(0)

        asset = resolve_asset(html, parsed.path)
        if asset is None:
            missing_assets.append(f"{html.relative_to(root)} -> {raw}")
            return match.group(0)

        version = content_version(asset)
        query = f"v={version}"
        updated = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query, parsed.fragment))

        if updated == raw:
            return match.group(0)

        replace.changed += 1
        return f'{match.group("prefix")}{updated}{match.group("suffix")}'

    replace.changed = 0
    updated_text = ATTR_RE.sub(replace, text)

    if replace.changed:
        html.write_text(updated_text, "utf-8")
        changed_files += 1
        rewritten_refs += replace.changed

if missing_assets:
    print("ERRORE: riferimenti CSS/JS locali senza file pubblico corrispondente:", file=sys.stderr)
    for item in missing_assets:
        print(f" - {item}", file=sys.stderr)
    raise SystemExit(1)

print(
    f"Versionamento static assets: {rewritten_refs} riferimenti CSS/JS riscritti "
    f"in {changed_files} file HTML"
)
