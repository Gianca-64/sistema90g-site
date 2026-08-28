#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

cases = [
    'caso-lavastoviglie-passaggio-cucina.html',
    'caso-isola-passaggi-cucina.html',
    'caso-lavello-sotto-finestra-aperture.html',
    'caso-cucina-piccola-tre-lati.html',
    'caso-cucina-profondita-75-angolo.html',
    'caso-preventivo-cucina-sconto-valore.html',
]
issues: list[str] = []
for rel in cases:
    path = root / rel
    if not path.is_file():
        issues.append(f'{rel}: pagina mancante')
        continue
    text = path.read_text('utf-8', errors='ignore')
    if 'Caso reale anonimizzato' not in text:
        issues.append(f'{rel}: manca indicazione caso reale anonimizzato')
    if "Limite dell'analisi pubblica:" not in text:
        issues.append(f'{rel}: manca limite dell analisi pubblica')
    if '/analisi-preventiva' not in text:
        issues.append(f'{rel}: manca percorso alla valutazione iniziale')

hub = root / 'casi-analizzati.html'
if not hub.is_file():
    issues.append('casi-analizzati.html: pagina mancante')
else:
    text = hub.read_text('utf-8', errors='ignore')
    required = [
        'Problemi reali, pubblicati in forma anonima',
        'data-s90g-case-proof-boundary="true"',
        'il caso mostra il criterio che ha fatto emergere il problema',
        'non sostituisce la verifica del progetto, delle misure o del preventivo specifico',
    ]
    for token in required:
        if token not in text:
            issues.append(f'casi-analizzati.html: manca {token}')
    if text.count('data-s90g-case-proof-boundary="true"') != 1:
        issues.append('casi-analizzati.html: confine prova duplicato o mancante')

if issues:
    print('ERRORE: contratto prova casi pubblici non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public case proof contract: 6 casi reali anonimizzati + limiti pubblici + confine prova')
