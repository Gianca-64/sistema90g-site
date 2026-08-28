#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin, urlparse
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")
script_path = root / "privacy-consent.js"
if not script_path.is_file():
    raise SystemExit(f"ERRORE: runtime pubblico non trovato: {script_path}")

raw = script_path.read_text("utf-8", errors="ignore")

required_literals = {
    "/sistema90g-audit-fix-20260707.css?v=20260708am",
    "/images/19_CASI_CUCINA.jpg?v=20260715a",
    "/analisi-preventiva.html#richiedi",
}
missing = sorted(value for value in required_literals if value not in raw)
if missing:
    print("ERRORE: mancano URL runtime root-relative attesi:")
    for value in missing:
        print(f" - {value}")
    raise SystemExit(1)

forbidden_patterns = {
    r"(?<!/)sistema90g-audit-fix-20260707\.css\?v=20260708am": "CSS audit runtime relativo",
    r"(?<!/)images/19_CASI_CUCINA\.jpg\?v=20260715a": "fallback immagine relativo",
    r"(?<!/)analisi-preventiva\.html#richiedi": "CTA valutazione relativa",
}
issues: list[str] = []
for pattern, label in forbidden_patterns.items():
    if re.search(pattern, raw):
        issues.append(label)

# Simula la risoluzione browser da una pagina annidata: tutti i percorsi locali
# runtime devono restare sulla radice pubblica, non sotto /approfondimenti/.
nested_page = "https://sistema90g.it/approfondimenti/esempio.html"
for value in sorted(required_literals):
    resolved = urljoin(nested_page, value)
    path = urlparse(resolved).path
    if path.startswith("/approfondimenti/"):
        issues.append(f"{value} si risolve sotto /approfondimenti/: {resolved}")

if issues:
    print("ERRORE: contratto URL runtime root-safe non rispettato:")
    for issue in issues:
        print(f" - {issue}")
    raise SystemExit(1)

print("OK public runtime root paths: CSS, fallback immagini e CTA chat root-safe")
