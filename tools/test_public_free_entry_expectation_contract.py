#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
path = root / 'analisi-preventiva.html'
if not path.is_file():
    raise SystemExit('ERRORE: analisi-preventiva.html non trovato nella dist')

text = path.read_text('utf-8', errors='ignore')
required = [
    'data-s90g-free-entry-expectation="true"',
    "Dopo l'invio",
    'La richiesta entra come valutazione iniziale gratuita',
    'non stai acquistando un servizio',
    'prima di attivarlo sai cosa comprende e quanto costa',
    'La valutazione iniziale resta gratuita e non comporta alcun acquisto automatico.',
    'id="richiedi"',
]
issues: list[str] = []
for token in required:
    if token not in text:
        issues.append(f'manca: {token}')

if text.count('data-s90g-free-entry-expectation="true"') != 1:
    issues.append('blocco aspettativa Free Entry duplicato o mancante')

expectation_pos = text.find('data-s90g-free-entry-expectation="true"')
request_pos = text.find('id="richiedi"')
if expectation_pos < 0 or request_pos < 0 or expectation_pos > request_pos:
    issues.append('il blocco aspettativa deve precedere il punto #richiedi')

for forbidden in ('entro 24 ore', 'entro 48 ore', 'riceverai una email', 'risposta via email'):
    if forbidden.lower() in text.lower():
        issues.append(f'promessa operativa non verificata presente: {forbidden}')

if issues:
    print('ERRORE: contratto aspettativa Free Entry non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public Free Entry expectation contract: invio, prima lettura, nessun acquisto automatico')
