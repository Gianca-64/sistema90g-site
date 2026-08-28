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
        'esperienza diretta tra progettazione, vendita, montaggio e post-vendita',
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

home = (root / 'index.html').read_text('utf-8', errors='ignore') if (root / 'index.html').is_file() else ''
if home:
    start = home.find('data-s90g-trust-bridge="home"')
    end = home.find('</section>', start)
    home_bridge = home[start:end] if start >= 0 and end >= 0 else ''
    if 'Gian Carlo Primo' in home_bridge:
        issues.append('index.html: il trust bridge Home deve restare brand-first, senza nome personale')

free_entry = (root / 'analisi-preventiva.html').read_text('utf-8', errors='ignore') if (root / 'analisi-preventiva.html').is_file() else ''
if free_entry:
    bridge_pos = free_entry.find('data-s90g-trust-bridge="free-entry"')
    request_pos = free_entry.find('id="richiedi"')
    if bridge_pos < 0 or request_pos < 0 or bridge_pos > request_pos:
        issues.append('analisi-preventiva.html: trust bridge deve precedere il punto di invio')

case_pages = [
    'caso-lavastoviglie-passaggio-cucina.html',
    'caso-isola-passaggi-cucina.html',
    'caso-lavello-sotto-finestra-aperture.html',
    'caso-cucina-piccola-tre-lati.html',
    'caso-cucina-profondita-75-angolo.html',
    'caso-preventivo-cucina-sconto-valore.html',
]
for rel in case_pages:
    path = root / rel
    if not path.is_file():
        issues.append(f'{rel}: caso pubblico mancante')
        continue
    text = path.read_text('utf-8', errors='ignore')
    if 'Caso reale anonimizzato' not in text:
        issues.append(f'{rel}: manca indicazione di caso reale anonimizzato')
    if "Limite dell'analisi pubblica:" not in text:
        issues.append(f'{rel}: manca il limite dell analisi pubblica')
    if '/analisi-preventiva' not in text:
        issues.append(f'{rel}: manca il percorso alla valutazione iniziale')

hub = root / 'casi-analizzati.html'
if not hub.is_file():
    issues.append('casi-analizzati.html: pagina pubblica mancante')
else:
    text = hub.read_text('utf-8', errors='ignore')
    for token in (
        'Problemi reali, pubblicati in forma anonima',
        'data-s90g-case-proof-boundary="true"',
        'il caso mostra il criterio che ha fatto emergere il problema',
        'non sostituisce la verifica del progetto, delle misure o del preventivo specifico',
    ):
        if token not in text:
            issues.append(f'casi-analizzati.html: prova pubblica mancante: {token}')
    if text.count('data-s90g-case-proof-boundary="true"') != 1:
        issues.append('casi-analizzati.html: confine prova duplicato o mancante')

if issues:
    print('ERRORE: contratto trust/prova pubblico non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public trust bridge contract: Home brand-first + identita nel Free Entry + 6 casi reali anonimizzati con limiti')
