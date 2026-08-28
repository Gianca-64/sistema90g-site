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
    'index.html': None,
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
}
pattern = re.compile(r'<nav\b[^>]*class="[^"]*\bs90g-nav\b[^"]*"[^>]*>(.*?)</nav>', re.S)
link_pattern = re.compile(r'<a([^>]*) href="([^"]+)">([^<]+)</a>')
issues: list[str] = []

for rel, current in current_by_file.items():
    path = root / rel
    if not path.is_file():
        issues.append(f'{rel}: pagina mancante')
        continue
    text = path.read_text('utf-8', errors='ignore')
    match = pattern.search(text)
    if not match:
        issues.append(f'{rel}: navigazione primaria mancante')
        continue
    links = [(href, label, attrs) for attrs, href, label in link_pattern.findall(match.group(1))]
    got = [(href, label) for href, label, _ in links]
    if got != items:
        issues.append(f'{rel}: sequenza menu diversa dal contratto canonico')
    currents = [href for href, _, attrs in links if 'aria-current="page"' in attrs]
    expected_currents = [] if current is None else [current]
    if currents != expected_currents:
        issues.append(f'{rel}: aria-current errato: {currents}, atteso {expected_currents}')
    if 'aria-label="Navigazione principale"' not in match.group(0):
        issues.append(f'{rel}: manca aria-label della navigazione principale')

if issues:
    print('ERRORE: contratto navigazione primaria non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public primary navigation contract: 11 pagine strategiche con menu canonico coerente')
