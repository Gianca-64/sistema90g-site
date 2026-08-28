#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

strategic = [
    'index.html',
    'servizi.html',
    'analisi-preventiva.html',
    'domande-cucina-faq.html',
    'casi-analizzati.html',
    'professionisti.html',
    'rivenditori-cucine.html',
    'metodo-sistema90g.html',
    'innovazioni.html',
    'chi-e-sistema90g.html',
    'contatti.html',
]

script_re = re.compile(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
title_re = re.compile(r'<title>(.*?)</title>', re.I | re.S)
desc_re = re.compile(r'<meta\b[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\'][^>]*>', re.I | re.S)
desc_alt_re = re.compile(r'<meta\b[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']description["\'][^>]*>', re.I | re.S)
canonical_re = re.compile(r'<link\b[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\'][^>]*>', re.I | re.S)
canonical_alt_re = re.compile(r'<link\b[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\'][^>]*>', re.I | re.S)

issues: list[str] = []
jsonld_count = 0

for path in root.rglob('*.html'):
    text = path.read_text('utf-8', errors='strict')
    if 'FAQPage' in text:
        issues.append(f'{path.relative_to(root)}: markup FAQPage obsoleto ancora presente')
    for raw in script_re.findall(text):
        jsonld_count += 1
        try:
            json.loads(raw.strip())
        except json.JSONDecodeError as exc:
            issues.append(f'{path.relative_to(root)}: JSON-LD non valido: {exc.msg}')

for rel in strategic:
    path = root / rel
    if not path.is_file():
        issues.append(f'{rel}: pagina strategica mancante')
        continue
    text = path.read_text('utf-8', errors='strict')
    titles = [x.strip() for x in title_re.findall(text) if x.strip()]
    descs = desc_re.findall(text) + desc_alt_re.findall(text)
    canonicals = canonical_re.findall(text) + canonical_alt_re.findall(text)
    if len(titles) != 1:
        issues.append(f'{rel}: atteso 1 title, trovati {len(titles)}')
    if len(descs) != 1 or not descs[0].strip():
        issues.append(f'{rel}: meta description mancante o duplicata')
    if len(canonicals) != 1:
        issues.append(f'{rel}: canonical mancante o duplicato')
    else:
        expected = 'https://sistema90g.it/' if rel == 'index.html' else 'https://sistema90g.it/' + rel[:-5]
        if canonicals[0] != expected:
            issues.append(f'{rel}: canonical {canonicals[0]} diverso da {expected}')

sitemap = root / 'sitemap.xml'
if not sitemap.is_file():
    issues.append('sitemap.xml: file mancante')
else:
    text = sitemap.read_text('utf-8', errors='strict')
    if re.search(r'<loc>https://sistema90g\.it/[^<]*\.html(?:[?#][^<]*)?</loc>', text):
        issues.append('sitemap.xml: contiene ancora URL .html')
    if '<loc>https://sistema90g.it/</loc>' not in text:
        issues.append('sitemap.xml: home canonica mancante')

if issues:
    print('ERRORE: contratto semantica ricerca non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print(f'OK public search semantics contract: 11 pagine strategiche + {jsonld_count} blocchi JSON-LD validi + sitemap canonica + no FAQPage')
