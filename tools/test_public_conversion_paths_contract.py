#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

issues: list[str] = []

home = (root / 'index.html').read_text('utf-8', errors='strict')
servizi = (root / 'servizi.html').read_text('utf-8', errors='strict')
casi = (root / 'casi-analizzati.html').read_text('utf-8', errors='strict')

for href in ('/servizi#consulenza', '/servizi#verifica', '/servizi#progetto'):
    if f'href="{href}"' not in home:
        issues.append(f'Home: collegamento mancante {href}')

for section_id in ('consulenza', 'verifica', 'progetto'):
    if f'id="{section_id}"' not in servizi:
        issues.append(f'Servizi: ancora mancante #{section_id}')

for stale in (
    'Sistema 90G valuta pertinenza e tipo di bisogno',
    'percorso, contenuti e prezzo vengono indicati prima di iniziare',
):
    if stale in casi:
        issues.append(f'Casi: linguaggio interno residuo: {stale}')

for required in (
    'quale lavoro è utile e quanto costa',
    'prima di iniziare sai che cosa verrà fatto e quanto costa',
):
    if required not in casi:
        issues.append(f'Casi: copy cliente-centrico mancante: {required}')

if issues:
    print('ERRORE: contratto conversione pubblica non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public conversion paths contract: Home -> 3 sezioni servizio corrette + Casi senza linguaggio da processo')
