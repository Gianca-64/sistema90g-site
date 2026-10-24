#!/usr/bin/env python3
"""Verify editorial identity, examples and navigation of the five priority guides.

Run against the public build: python3 tools/test_priority_guides_contract.py dist
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
PAGES = {
    'misure-passaggi-cucina': 'passaggio-esempio',
    'isola-cucina-distanze-passaggi': 'isola-confronto',
    'frigorifero-cucina-vicino-parete': None,
    'lavastoviglie-cucina-aperture-passaggi': None,
    'confrontare-due-preventivi-cucina': 'preventivi-esempio',
}

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.times, self.links, self.ids, self.headers = [], [], [], []
        self.schemas = []
        self.current_schema = None
        self.tables = self.captions = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'time':
            self.times.append(a.get('datetime'))
        if tag == 'a':
            self.links.append(a.get('href', ''))
        if tag == 'table':
            self.tables += 1
        if tag == 'caption':
            self.captions += 1
        if tag == 'th':
            self.headers.append(a.get('scope'))
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.current_schema = ''
    def handle_data(self, data):
        if self.current_schema is not None:
            self.current_schema += data
    def handle_endtag(self, tag):
        if tag == 'script' and self.current_schema is not None:
            data = json.loads(self.current_schema)
            self.schemas.extend(data.get('@graph', [data]))
            self.current_schema = None

errors = []
for slug, example_id in PAGES.items():
    path = ROOT / (slug + '.html')
    text = path.read_text(encoding='utf-8')
    page = Page()
    page.feed(text)
    articles = [s for s in page.schemas if s.get('@type') == 'Article']
    if len(articles) != 1:
        errors.append(f'{slug}: atteso un Article')
        continue
    article = articles[0]
    author = article.get('author', {})
    if author.get('@id') != 'https://sistema90g.it/chi-e-sistema90g#person':
        errors.append(f'{slug}: identità autore non collegata al profilo')
    if article.get('dateModified') not in page.times:
        errors.append(f'{slug}: data schema diversa dalla data visibile')
    if not any(href.startswith('/chi-e-sistema90g') for href in page.links):
        errors.append(f'{slug}: firma senza profilo')
    if len(page.ids) != len(set(page.ids)):
        errors.append(f'{slug}: ID duplicati')
    if example_id and example_id not in page.ids:
        errors.append(f'{slug}: esempio editoriale mancante')
    if page.tables and (page.captions != page.tables or any(s not in ('row', 'col') for s in page.headers)):
        errors.append(f'{slug}: tabella senza didascalia o intestazioni associate')
    service = '/analisi-preventivo-cucina' if slug.startswith('confrontare') else '/verifica-90g'
    if not any(href.removesuffix('.html') == service for href in page.links):
        errors.append(f'{slug}: servizio contestuale mancante')
    for href in page.links:
        if not href.startswith('/') or href.startswith('//'):
            continue
        route = href.split('#')[0].split('?')[0]
        candidates = [ROOT / route.lstrip('/'), ROOT / (route.lstrip('/') + '.html')]
        if route == '/':
            candidates.append(ROOT / 'index.html')
        if not any(p.is_file() for p in candidates):
            errors.append(f'{slug}: destinazione locale assente: {href}')
if errors:
    raise SystemExit('\n'.join(errors))
print('OK: 5 guide prioritarie — identità, date, esempi, tabelle e collegamenti')
