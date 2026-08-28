#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

items = [
    ('/servizi', 'Servizi'),
    ('/analisi-preventiva', 'Come funziona'),
    ('/domande-cucina-faq', 'Domande'),
    ('/casi-analizzati', 'Casi reali'),
    ('/professionisti', 'Professionisti'),
    ('/rivenditori-cucine', 'Rivenditori'),
    ('/metodo-sistema90g', 'Metodo e AI'),
    ('/innovazioni', 'Innovazioni'),
    ('/chi-e-sistema90g', 'Chi sono'),
    ('/contatti', 'Contatti'),
]

current_by_file = {
    'servizi.html': '/servizi',
    'analisi-preventiva.html': '/analisi-preventiva',
    'domande-cucina-faq.html': '/domande-cucina-faq',
    'casi-analizzati.html': '/casi-analizzati',
    'professionisti.html': '/professionisti',
    'rivenditori-cucine.html': '/rivenditori-cucine',
    'metodo-sistema90g.html': '/metodo-sistema90g',
    'innovazioni.html': '/innovazioni',
    'chi-e-sistema90g.html': '/chi-e-sistema90g',
    'contatti.html': '/contatti',
    'index.html': None,
}

pattern = re.compile(r'<nav\b[^>]*class="[^"]*\bs90g-nav\b[^"]*"[^>]*>.*?</nav>', re.S)
changed: list[str] = []

for rel, current in current_by_file.items():
    path = root / rel
    if not path.is_file():
        raise SystemExit(f'ERRORE: pagina strategica mancante: {rel}')
    links = []
    for href, label in items:
        current_attr = ' aria-current="page"' if href == current else ''
        links.append(f'<a{current_attr} href="{href}">{label}</a>')
    nav = '<nav class="s90g-nav" aria-label="Navigazione principale">' + ''.join(links) + '</nav>'
    text = path.read_text('utf-8', errors='ignore')
    match = pattern.search(text)
    if not match:
        raise SystemExit(f'ERRORE: navigazione primaria non trovata in {rel}')
    if match.group(0) == nav:
        continue
    path.write_text(text[:match.start()] + nav + text[match.end():], 'utf-8')
    changed.append(rel)

print('Navigazione primaria normalizzata: ' + (', '.join(changed) if changed else 'gia coerente'))
