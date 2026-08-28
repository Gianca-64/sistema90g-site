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
    'sviluppo-avanzato-progetto-cucina.html': [
        'Sviluppo avanzato',
        '+117 €',
        'https://sistema90g.it/sviluppo-avanzato-progetto-cucina',
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

legacy_page = DIST / 'acquisto-assistito-cucina.html'
if legacy_page.exists():
    errors.append('acquisto-assistito-cucina.html: vecchia landing ancora pubblicata')

sitemap = DIST / 'sitemap.xml'
if not sitemap.is_file():
    errors.append('sitemap.xml: mancante')
else:
    sitemap_text = sitemap.read_text('utf-8', errors='replace')
    if 'https://sistema90g.it/sviluppo-avanzato-progetto-cucina' not in sitemap_text:
        errors.append('sitemap.xml: nuova landing Sviluppo avanzato mancante')
    if 'acquisto-assistito-cucina' in sitemap_text:
        errors.append('sitemap.xml: vecchio slug acquisto-assistito ancora indicizzato')

redirects = DIST / '_redirects'
if not redirects.is_file():
    errors.append('_redirects: mancante')
else:
    redirects_text = redirects.read_text('utf-8', errors='replace')
    for source in ('/acquisto-assistito-cucina ', '/acquisto-assistito-cucina.html '):
        expected = f'{source}/sviluppo-avanzato-progetto-cucina 301'
        if expected not in redirects_text:
            errors.append(f'_redirects: regola legacy mancante {expected!r}')

for runtime_name in ('navigation-conversion.js', 'privacy-consent.js'):
    runtime = DIST / runtime_name
    if runtime.is_file():
        text = runtime.read_text('utf-8', errors='replace')
        if 'acquisto-assistito-cucina' in text:
            errors.append(f'{runtime_name}: classificazione runtime usa ancora il vecchio slug')
        if 'sviluppo-avanzato-progetto-cucina' not in text:
            errors.append(f'{runtime_name}: nuova landing non classificata come servizio')

if errors:
    print('ERRORE public commercial contract:')
    for error in errors:
        print(' -', error)
    raise SystemExit(1)

print('OK public commercial contract: Verifica 90G 127 € + Sviluppo avanzato su URL canonica coerente')
