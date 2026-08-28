#!/usr/bin/env python3
from pathlib import Path
import sys

DIST = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'dist'

PAGES = {
    'rivenditori-cucine.html': [
        'Verifica 90G',
        '127 €',
        '"price":"127"',
    ],
    'controllo-progetto-cucina.html': [
        'Verifica 90G',
        '127 €',
        '"price":"127"',
    ],
}

errors = []
for name, required in PAGES.items():
    path = DIST / name
    if not path.is_file():
        errors.append(f'{name}: pagina pubblica mancante')
        continue
    text = path.read_text('utf-8', errors='replace')
    for token in required:
        if token not in text:
            errors.append(f'{name}: manca {token!r}')
    for legacy in ('150 €', '"price":"150"', 'Verifica professionale progetto cucina'):
        if legacy in text:
            errors.append(f'{name}: residuo commerciale obsoleto {legacy!r}')

if errors:
    print('ERRORE public commercial contract:')
    for error in errors:
        print(' -', error)
    raise SystemExit(1)

print('OK public commercial contract: Verifica 90G 127 € coerente per rivenditori')
