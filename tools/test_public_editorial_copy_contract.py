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
    'top-cucina-materiali-guida.html': [
        'Progetto Cucina 90G', 'add-on', 'Finiture e materiali</a> approfondisce',
    ],
    'ante-cucina-materiali-manutenzione.html': [
        'basta una Consulenza 90G',
    ],
    'cucina-piccola-come-progettarla.html': [
        'puoi approfondire il <a href="/progetto-cucina-sistema90g">Progetto Cucina 90G</a>',
    ],
    'errori-progetto-cucina.html': [
        'servizio appropriato', 'può essere appropriata <a href="/servizi">Verifica 90G</a>',
        'può essere più adatto il <a href="/progetto-cucina-sistema90g">Progetto Cucina 90G</a>',
        'Sottoponi gratuitamente il tuo caso →',
    ],
    'casi-analizzati.html': [
        'valuta pertinenza e tipo di bisogno',
        'percorso, contenuti e prezzo vengono indicati prima di iniziare',
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
    'top-cucina-materiali-guida.html': [
        'prima leggiamo il problema', 'serve un approfondimento sulle finiture',
    ],
    'ante-cucina-materiali-manutenzione.html': [
        'se basta chiarire il confronto oppure se la scelta richiede un approfondimento nel progetto',
    ],
    'cucina-piccola-come-progettarla.html': [
        'Prima leggiamo il problema e poi ti diciamo se serve davvero un approfondimento',
    ],
    'errori-progetto-cucina.html': [
        'senza che tu debba scegliere in anticipo il servizio', 'prima ti diciamo quale lavoro è utile e quanto costa',
    ],
    'casi-analizzati.html': [
        'quale lavoro è utile e quanto costa',
        'prima di iniziare sai che cosa verrà fatto e quanto costa',
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

home = root / 'index.html'
servizi = root / 'servizi.html'
if not home.is_file():
    issues.append('index.html: pagina mancante')
else:
    home_text = home.read_text('utf-8', errors='strict')
    for href in ('/servizi#consulenza', '/servizi#verifica', '/servizi#progetto'):
        if f'href="{href}"' not in home_text:
            issues.append(f'index.html: collegamento servizio mancante {href}')

if not servizi.is_file():
    issues.append('servizi.html: pagina mancante')
else:
    servizi_text = servizi.read_text('utf-8', errors='strict')
    for section_id in ('consulenza', 'verifica', 'progetto'):
        if f'id="{section_id}"' not in servizi_text:
            issues.append(f'servizi.html: ancora mancante #{section_id}')

if issues:
    print('ERRORE: contratto copy/conversione editoriale non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public editorial copy contract: 11 pagine allineate + Home instradata alle 3 sezioni servizio corrette')
