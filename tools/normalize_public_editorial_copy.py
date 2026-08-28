#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

REPLACEMENTS = {
    'pareti-fuori-squadra-cucina.html': {
        'Seconda Opinione': 'Verifica 90G',
    },
    'frigorifero-incasso-o-libera-installazione.html': {
        'dell ordine': "dell'ordine",
        'd aria': "d'aria",
        'l allineamento': "l'allineamento",
        'l angolo': "l'angolo",
        'l estrazione': "l'estrazione",
        'l integrazione': "l'integrazione",
        'dell apparecchio': "dell'apparecchio",
    },
    'lavello-una-o-due-vasche-gocciolatoio.html': {
        'all uso': "all'uso",
        'sull abitudine': "sull'abitudine",
        'l utilità': "l'utilità",
        'l inserimento': "l'inserimento",
        'dell ordine': "dell'ordine",
        'l intera': "l'intera",
    },
    'piano-induzione-aspirazione-integrata-o-cappa.html': {
        'dell isola': "dell'isola",
        'L aspirazione': "L'aspirazione",
        'l aspirazione': "l'aspirazione",
        'dell aria': "dell'aria",
        'un isola': "un'isola",
        'c è': "c'è",
        'dell ordine': "dell'ordine",
        'dell acquisto': "dell'acquisto",
    },
}

changed: list[str] = []
for filename, replacements in REPLACEMENTS.items():
    path = root / filename
    if not path.is_file():
        raise SystemExit(f'ERRORE: guida editoriale mancante: {filename}')
    text = path.read_text('utf-8', errors='strict')
    original = text
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, 'utf-8')
        changed.append(filename)

print('Copy editoriale normalizzato: ' + (', '.join(changed) if changed else 'gia pulito'))
