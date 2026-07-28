#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
version = "20260728e"
errors = []
css = (root / "sistema90g-visual-2026.css").read_text(encoding="utf-8", errors="replace")
required = [
    "SEZIONE C — responsive hardening 2026-07-28",
    "overflow-x: clip",
    "grid-template-columns: minmax(0, 1fr) auto",
    "grid-template-columns: minmax(0, 1fr);",
    "@media (max-width: 560px)",
    "@media (max-width: 360px)",
    '.s90g-header-cta span[aria-hidden="true"]',
]
for token in required:
    if token not in css:
        errors.append(f"regola responsive mancante: {token}")
pattern = re.compile(r"sistema90g-visual-2026\.css\?v=([^\"']+)")
checked = 0
visual = 0
for path in sorted(root.rglob("*.html")):
    if ".git" in path.parts or path.name.startswith("._"):
        continue
    raw = path.read_text(encoding="utf-8", errors="replace")
    checked += 1
    if "sistema90g-visual-2026.css" not in raw:
        continue
    visual += 1
    if 'name="viewport"' not in raw and "name='viewport'" not in raw:
        errors.append(f"{path.name}: meta viewport mancante")
    expected = f"sistema90g-visual-2026.css?v={version}"
    if expected not in raw:
        errors.append(f"{path.name}: versione CSS non aggiornata")
    versions = pattern.findall(raw)
    if versions and any(item != version for item in versions):
        errors.append(f"{path.name}: versione CSS incoerente {versions}")
if visual < 50:
    errors.append(f"numero anomalo di pagine visuali: {visual}")
print(f"HTML checked: {checked}")
print(f"Visual pages checked: {visual}")
print(f"Issues: {len(errors)}")
if errors:
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)
print("RESPONSIVE CONTRACT TEST: PASS")
