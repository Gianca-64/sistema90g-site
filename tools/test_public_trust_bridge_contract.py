#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

checks = {
    'index.html': [
        'data-s90g-trust-bridge="home"',
        'esperienza diretta tra progettazione, vendita, montaggio e post-vendita',
        'non vende cucine',
        'href="/chi-e-sistema90g"',
        'href="/metodo-sistema90g"',
        'href="/casi-analizzati"',
    ],
    'analisi-preventiva.html': [
        'data-s90g-trust-bridge="free-entry"',
        'Gian Carlo Primo',
        'progettazione, vendita, montaggio e post-vendita',
        'href="/chi-e-sistema90g"',
        'href="/casi-analizzati"',
        'id="richiedi"',
        's90g-free-entry-visual-v1.css',
        's90g-free-entry-visual-v1',
        'data-s90g-free-entry-stage="read"',
        'data-s90g-free-entry-stage="example"',
        'data-s90g-free-entry-stage="process"',
        'data-s90g-free-entry-stage="independence"',
        'data-s90g-free-entry-stage="deepen"',
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
    if '.html"' in home_bridge:
        issues.append('index.html: il trust bridge deve usare URL pubblici canonici senza .html')

free_entry = (root / 'analisi-preventiva.html').read_text('utf-8', errors='ignore') if (root / 'analisi-preventiva.html').is_file() else ''
if free_entry:
    bridge_pos = free_entry.find('data-s90g-trust-bridge="free-entry"')
    request_pos = free_entry.find('id="richiedi"')
    if bridge_pos < 0 or request_pos < 0 or bridge_pos > request_pos:
        issues.append('analisi-preventiva.html: trust bridge deve precedere il punto di invio')
    start = free_entry.find('data-s90g-trust-bridge="free-entry"')
    end = free_entry.find('</section>', start)
    free_bridge = free_entry[start:end] if start >= 0 and end >= 0 else ''
    if '.html"' in free_bridge:
        issues.append('analisi-preventiva.html: il trust bridge deve usare URL pubblici canonici senza .html')
    if free_entry.count('s90g-free-entry-visual-v1.css') != 1:
        issues.append('analisi-preventiva.html: stylesheet Free Entry visual duplicato o mancante')
    if free_entry.count('s90g-free-entry-visual-v1') != 2:
        issues.append('analisi-preventiva.html: marker Free Entry visual inatteso')
    for stage in ('read', 'example', 'process', 'independence', 'deepen'):
        if free_entry.count(f'data-s90g-free-entry-stage="{stage}"') != 1:
            issues.append(f'analisi-preventiva.html: stage Free Entry {stage} duplicato o mancante')

free_entry_css = root / 's90g-free-entry-visual-v1.css'
if not free_entry_css.is_file():
    issues.append('s90g-free-entry-visual-v1.css: stylesheet pubblico mancante')
else:
    css = free_entry_css.read_text('utf-8', errors='ignore')
    for token in ('90G Focus', '90G Next Step', '#richiedi', 's90g-free-entry-visual-v1'):
        if token not in css:
            issues.append(f's90g-free-entry-visual-v1.css: grammatica visuale mancante: {token}')

case_modes = {
    'caso-lavastoviglie-passaggio-cucina.html': 's90g-case-mode-use',
    'caso-isola-passaggi-cucina.html': 's90g-case-mode-conflict',
    'caso-lavello-sotto-finestra-aperture.html': 's90g-case-mode-conflict',
    'caso-cucina-piccola-tre-lati.html': 's90g-case-mode-use',
    'caso-cucina-profondita-75-angolo.html': 's90g-case-mode-check',
    'caso-preventivo-cucina-sconto-valore.html': 's90g-case-mode-compare',
}
for rel, mode_class in case_modes.items():
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
    if 's90g-case-visual-v2.css' not in text:
        issues.append(f'{rel}: manca stylesheet Case Visual V2')
    if 's90g-case-visual-v2' not in text:
        issues.append(f'{rel}: manca classe Case Visual V2')
    if mode_class not in text:
        issues.append(f'{rel}: manca modalità visuale specifica {mode_class}')

case_css = root / 's90g-case-visual-v2.css'
if not case_css.is_file():
    issues.append('s90g-case-visual-v2.css: stylesheet pubblico mancante')
else:
    css = case_css.read_text('utf-8', errors='ignore')
    for token in (
        '90G Check',
        '90G Use',
        '90G Conflict',
        '90G Compare',
        '90G Consequence',
        's90g-case-mode-conflict',
        's90g-case-mode-check',
        's90g-case-mode-compare',
    ):
        if token not in css:
            issues.append(f's90g-case-visual-v2.css: grammatica visuale mancante: {token}')

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

nav_items = [
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
nav_current = {
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
nav_pattern = re.compile(r'<nav\b[^>]*class="[^"]*\bs90g-nav\b[^"]*"[^>]*>(.*?)</nav>', re.S)
link_pattern = re.compile(r'<a([^>]*) href="([^"]+)">([^<]+)</a>')
for rel, current in nav_current.items():
    path = root / rel
    if not path.is_file():
        issues.append(f'{rel}: pagina strategica mancante')
        continue
    text = path.read_text('utf-8', errors='ignore')
    match = nav_pattern.search(text)
    if not match:
        issues.append(f'{rel}: navigazione primaria mancante')
        continue
    links = [(href, label, attrs) for attrs, href, label in link_pattern.findall(match.group(1))]
    if [(href, label) for href, label, _ in links] != nav_items:
        issues.append(f'{rel}: menu principale diverso dalla sequenza canonica')
    currents = [href for href, _, attrs in links if 'aria-current="page"' in attrs]
    expected = [] if current is None else [current]
    if currents != expected:
        issues.append(f'{rel}: aria-current errato: {currents}, atteso {expected}')
    if 'aria-label="Navigazione principale"' not in match.group(0):
        issues.append(f'{rel}: manca aria-label sulla navigazione principale')

if issues:
    print('ERRORE: contratto trust/prova/navigazione pubblico non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public trust bridge contract: trust + Free Entry Visual V1 + 6 casi reali Case V2 + 11 pagine con navigazione canonica')