#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

page = root / 'index.html'
if not page.is_file():
    raise SystemExit('ERRORE: index.html mancante')

sources = [
    'sistema90g-visual-2026.css',
    's90g-offer-2026.css',
    's90g-wow-visual-proof.css',
]
bundle_name = 's90g-home-critical.css'
bundle = root / bundle_name

for name in sources:
    if not (root / name).is_file():
        raise SystemExit(f'ERRORE: CSS Home sorgente mancante: {name}')

# Manteniamo esattamente l'ordine di cascata gia usato dalla Home:
# visual -> offer -> WOW. Nessun caricamento asincrono e nessun cambio di timing
# degli stili: riduciamo soltanto tre richieste CSS a una.
parts = []
for name in sources:
    css = (root / name).read_text('utf-8', errors='strict').rstrip()
    parts.append(f'/* bundled: {name} */\n{css}')
bundle.write_text('\n\n'.join(parts) + '\n', 'utf-8')

text = page.read_text('utf-8', errors='strict')
link_re = re.compile(r'<link\b[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\'][^>]*>', re.I)
matches = list(link_re.finditer(text))
source_matches: dict[str, list[re.Match[str]]] = {name: [] for name in sources}

for match in matches:
    path = Path(urlsplit(match.group(1)).path).name
    if path in source_matches:
        source_matches[path].append(match)

issues = [name for name, found in source_matches.items() if len(found) != 1]
if issues:
    detail = ', '.join(f'{name}={len(source_matches[name])}' for name in issues)
    raise SystemExit(f'ERRORE: riferimenti CSS Home inattesi: {detail}')

first_tag = source_matches[sources[0]][0].group(0)
bundle_tag = f'<link rel="stylesheet" href="/{bundle_name}" data-s90g-home-critical>'
text = text.replace(first_tag, bundle_tag, 1)
for name in sources[1:]:
    text = text.replace(source_matches[name][0].group(0), '', 1)

page.write_text(text, 'utf-8')
print('CSS Home consolidato: visual + offer + WOW -> s90g-home-critical.css')
