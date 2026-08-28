#!/usr/bin/env python3

from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")
if not root.is_dir():
    raise SystemExit(f"ERRORE: directory pubblica non trovata: {root}")

attr_re = re.compile(r'''(?:src|href)\s*=\s*["']([^"']+)["']''', re.IGNORECASE)
issues: list[str] = []
checked = 0

for html in sorted(root.rglob("*.html")):
    text = html.read_text("utf-8", errors="ignore")
    for match in attr_re.finditer(text):
        raw = match.group(1).strip()
        if not raw or raw.startswith(("http://", "https://", "//", "data:", "mailto:", "tel:", "#", "javascript:")):
            continue

        parsed = urlsplit(raw)
        if Path(parsed.path).suffix.lower() not in {".css", ".js"}:
            continue

        checked += 1
        versions = parse_qs(parsed.query).get("v", [])
        if len(versions) != 1 or not re.fullmatch(r"[0-9a-f]{12}", versions[0]):
            issues.append(f"{html.relative_to(root)} -> {raw}")

if issues:
    print("ERRORE: CSS/JS pubblici senza versione contenuto valida:")
    for issue in issues:
        print(f" - {issue}")
    raise SystemExit(1)

print(f"OK public static asset versioning: {checked} riferimenti CSS/JS con hash contenuto")
