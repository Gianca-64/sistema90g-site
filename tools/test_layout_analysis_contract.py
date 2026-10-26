#!/usr/bin/env python3
"""Public boundary: one fixed price, analysis deliverables, no new design."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.h1 = 0
        self.links = []
        self.ids = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1': self.h1 += 1
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'a': self.links.append(attrs.get('href', ''))

errors = []
for filename, listing, name, price, free_entry, required in [
    ('analisi-distributiva-90g.html', 'servizi.html', 'Analisi Distributiva 90G', '199 €',
     '/analisi-preventiva', ['planimetria commentata', 'relazione sintetica',
     'un chiarimento finale', 'indipendentemente dal numero e dal tipo di ambienti',
     'non comprende lo sviluppo di un nuovo progetto', 'varianti progettuali',
     'le misure mancanti non vengono inventate', 'tempi di consegna vengono confermati prima']),
    ('en/layout-analysis.html', 'en/services.html', '90G Layout Analysis', '€199',
     '/en/how-it-works', ['annotated floor plan', 'concise report',
     'one final clarification', 'regardless of the number or type of rooms',
     'does not include a new design', 'design alternatives',
     'missing measurements are not invented', 'delivery time are confirmed before']),
]:
    path = ROOT / filename
    if not path.is_file():
        errors.append(f'{filename}: service page missing'); continue
    text = path.read_text()
    plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', text)).lower()
    page = Page(text)
    if page.h1 != 1 or len(page.ids) != len(set(page.ids)):
        errors.append(f'{filename}: heading/ID structure invalid')
    if name not in text or price not in text:
        errors.append(f'{filename}: service name or fixed visible price missing')
    for token in required:
        if token not in plain:
            errors.append(f'{filename}: scope promise missing: {token}')
    if not any(href.startswith(free_entry) for href in page.links):
        errors.append(f'{filename}: canonical free assessment link missing')
    if any('portale.sistema90g.it' in href for href in page.links):
        errors.append(f'{filename}: must use free assessment, not a new direct Portal route')
    for raw in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S):
        data = json.loads(raw)
        if data.get('@type') == 'Service':
            if data.get('name') != name or data.get('offers', {}).get('price') != '199' or data.get('offers', {}).get('priceCurrency') != 'EUR':
                errors.append(f'{filename}: structured service price/name mismatch')
            break
    else:
        errors.append(f'{filename}: Service schema missing')
    index = (ROOT / listing).read_text()
    slug = '/' + filename.removesuffix('.html')
    if not any(href.removesuffix('.html') == slug for href in Page(index).links):
        errors.append(f'{listing}: service not reachable from listing')
    index_plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', index)).lower()
    if name.lower() not in index_plain or price.lower() not in index_plain:
        errors.append(f'{listing}: service/price not visible')

if errors:
    print('\n'.join('FAIL — ' + error for error in errors))
    raise SystemExit(1)
print('LAYOUT ANALYSIS CONTRACT: PASS — fixed €199, room-independent scope, deliverables, exclusions and canonical free entry in IT/EN')
