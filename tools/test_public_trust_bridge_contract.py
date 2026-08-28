#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

checks = {
    'index.html': [
        'data-s90g-trust-bridge="home"',
        'Gian Carlo Primo',
        'progettazione, vendita, montaggio e post-vendita',
        'non vende cucine',
        '/chi-e-sistema90g',
        '/metodo-sistema90g',
        '/casi-analizzati',
    ],
    'analisi-preventiva.html': [
        'data-s90g-trust-bridge="free-entry"',
        'Gian Carlo Primo',
        'progettazione, vendita, montaggio e post-vendita',
        '/chi-e-sistema90g',
        '/casi-analizzati',
        'id="richiedi"',
    ],
}

issues: list[str] = []
for rel, tokens in checks.items():
    path = root / rel
    if not path.is_file():
        issues.append(f'{rel}: pagina pubblica mancante')
        continue
    text = path.read_text('utf-8', errors='ignore')
    for token in tokens:
        if token not in text:
            issues.append(f'{rel}: trust contract mancante: {token}')
    if text.count('data-s90g-trust-bridge=') != 1:
        issues.append(f'{rel}: trust bridge duplicato o mancante')

free_entry = (root / 'analisi-preventiva.html').read_text('utf-8', errors='ignore') if (root / 'analisi-preventiva.html').is_file() else ''
if free_entry:
    bridge_pos = free_entry.find('data-s90g-trust-bridge="free-entry"')
    request_pos = free_entry.find('id="richiedi"')
    if bridge_pos < 0 or request_pos < 0 or bridge_pos > request_pos:
        issues.append('analisi-preventiva.html: trust bridge deve precedere il punto di invio')

if issues:
    print('ERRORE: contratto trust bridge pubblico non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public trust bridge contract: Home + Free Entry con identita, indipendenza e prove verificabili')
