#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
page = root / 'index.html'
issues = []

if not page.is_file():
    issues.append('index.html: pagina mancante')
else:
    text = page.read_text('utf-8', errors='strict')
    if text.count('data-s90g-wow-situation-selector="true"') != 1:
        issues.append('index.html: selettore WOW mancante o duplicato')
    required = [
        'Cosa stai cercando di capire?',
        'Ho già un progetto o un preventivo',
        'Sto valutando isola o penisola',
        'Devo confrontare due preventivi',
        'Devo scegliere materiali o finiture',
        'La cucina è già montata',
        'Non so come definire il problema',
        'href="/analisi-preventiva#richiedi"',
    ]
    for token in required:
        if token not in text:
            issues.append(f'index.html: elemento selettore mancante: {token}')
    forbidden = ['Scegli il servizio', 'Quale servizio vuoi', 'service=progetto', 'service=verifica', 'service=consulenza']
    for token in forbidden:
        if token in text:
            issues.append(f'index.html: il selettore anticipa la scelta servizio: {token}')

if issues:
    print('ERRORE: contratto WOW situation selector non rispettato:')
    for issue in issues:
        print(' -', issue)
    raise SystemExit(1)

print('OK public WOW situation selector: 6 situazioni problem-first, nessuna scelta servizio obbligatoria')
