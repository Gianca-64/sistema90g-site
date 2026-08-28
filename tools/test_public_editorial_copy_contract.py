#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

FORBIDDEN = {
    'pareti-fuori-squadra-cucina.html': ['Seconda Opinione'],
    'frigorifero-incasso-o-libera-installazione.html': [
        'dell ordine', 'd aria', 'l allineamento', 'l angolo', 'l estrazione',
        'l integrazione', 'dell apparecchio',
    ],
    'lavello-una-o-due-vasche-gocciolatoio.html': [
        'all uso', 'sull abitudine', 'l utilità', 'l inserimento', 'dell ordine', 'l intera',
    ],
    'piano-induzione-aspirazione-integrata-o-cappa.html': [
        'dell isola', 'L aspirazione', 'l aspirazione', 'dell aria', 'un isola',
        'c è', 'dell ordine', 'dell acquisto',
    ],
    'confrontare-due-preventivi-cucina.html': [
        'percorso appropriato', 'Chiedi la valutazione gratuita →',
    ],
    'voci-escluse-preventivo-cucina.html': [
        'percorso complessivo', 'perimetro della propria offerta',
    ],
}

REQUIRED = {
    'pareti-fuori-squadra-cucina.html': ['Verifica 90G'],
    'frigorifero-incasso-o-libera-installazione.html': ["dell'ordine"],
    'lavello-una-o-due-vasche-gocciolatoio.html': ["all'uso"],
    'piano-induzione-aspirazione-integrata-o-cappa.html': ["L'aspirazione"],
    'confrontare-due-preventivi-cucina.html': [
        'quale lavoro è adatto e quanto costa', 'Sottoponi gratuitamente i preventivi →',
    ],
    'voci-escluse-preventivo-cucina.html': [
        "costo e sull'organizzazione complessiva", 'chiarire cosa comprende la propria offerta',
    ],
}

issues: list[str] = []
for filename, forbidden in FORBIDDEN.items():
    path = root / filename
    if not path.is_file():
        issues.append(f'{filename}: pagina mancante')
        continue
    text = path.read_text('utf-8', errors='strict')
    for token in forbidden:
        if token in text:
            issues.append(f'{filename}: residuo editoriale: {token}')
    for token in REQUIRED[filename]:
        if token not in text:
            issues.append(f'{filename}: correzione attesa mancante: {token}')

if issues:
    print('ERRORE: contratto copy editoriale non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public editorial copy contract: 6 guide senza residui legacy, tecnicismi interni o CTA duplicate')
