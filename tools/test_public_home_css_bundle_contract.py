#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
page = root / 'index.html'
bundle_name = 's90g-home-critical.css'
sources = [
    'sistema90g-visual-2026.css',
    's90g-offer-2026.css',
    's90g-wow-visual-proof.css',
]
issues: list[str] = []

if not page.is_file():
    issues.append('index.html: pagina mancante')
else:
    text = page.read_text('utf-8', errors='strict')
    href_re = re.compile(r'href=["\']([^"\']+)["\']', re.I)
    href_paths = [Path(urlsplit(m.group(1)).path).name for m in href_re.finditer(text)]

    if href_paths.count(bundle_name) != 1:
        issues.append(f'index.html: atteso 1 riferimento a {bundle_name}, trovati {href_paths.count(bundle_name)}')
    for name in sources:
        count = href_paths.count(name)
        if count != 0:
            issues.append(f'index.html: {name} deve essere assorbito nel bundle, trovati {count} riferimenti')
    if href_paths.count('consent-ui.css') != 1:
        issues.append('index.html: consent-ui.css deve restare separato e immediato')

    bundle_pos = text.find(bundle_name)
    consent_pos = text.find('consent-ui.css')
    if bundle_pos < 0 or consent_pos < 0 or bundle_pos > consent_pos:
        issues.append('index.html: bundle Home deve precedere consent-ui.css')

bundle = root / bundle_name
if not bundle.is_file():
    issues.append(f'{bundle_name}: asset generato mancante')
else:
    expected_parts = []
    for name in sources:
        path = root / name
        if not path.is_file():
            issues.append(f'{name}: sorgente CSS mancante')
            continue
        expected_parts.append(f'/* bundled: {name} */\n{path.read_text("utf-8", errors="strict").rstrip()}')
    if len(expected_parts) == len(sources):
        expected = '\n\n'.join(expected_parts) + '\n'
        actual = bundle.read_text('utf-8', errors='strict')
        if actual != expected:
            issues.append(f'{bundle_name}: contenuto o ordine cascata diverso dalle tre sorgenti canoniche')

# Il bundle e specifico della Home: nessun'altra pagina deve dipenderne.
for html in sorted(root.rglob('*.html')):
    if html == page:
        continue
    if bundle_name in html.read_text('utf-8', errors='ignore'):
        issues.append(f'{html.relative_to(root)}: riferimento inatteso al bundle CSS Home')

if issues:
    print('ERRORE: contratto bundle CSS Home non rispettato:')
    for issue in issues:
        print(' -', issue)
    raise SystemExit(1)

print('OK public Home CSS bundle: 3 fogli -> 1 richiesta, cascata invariata, Consent CSS separato')
