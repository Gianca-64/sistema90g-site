#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from collections import defaultdict, Counter
import argparse
import json
import xml.etree.ElementTree as ET

SITE_HOSTS = {'sistema90g.it', 'www.sistema90g.it'}
SITEMAP_NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
GENERIC_LABELS = {
    'clicca qui', 'scopri', 'scopri di più', 'approfondisci',
    'contattami', 'richiedi informazioni'
}


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self._a = None
        self._text = []
        self.robots = ''
        self.ids = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d:
            self.ids.append(d['id'])
        if tag == 'meta' and d.get('name', '').lower() == 'robots':
            self.robots = d.get('content', '')
        if tag == 'a':
            self._a = d
            self._text = []

    def handle_data(self, data):
        if self._a is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == 'a' and self._a is not None:
            self.links.append((
                self._a.get('href', ''),
                ' '.join(''.join(self._text).split()),
                self._a,
            ))
            self._a = None
            self._text = []


def sitemap_pages(root: Path):
    sitemap = root / 'sitemap.xml'
    tree = ET.parse(sitemap)
    pages = set()
    for loc in tree.findall('.//sm:loc', SITEMAP_NS):
        if not loc.text:
            continue
        u = urlsplit(loc.text.strip())
        if u.netloc not in SITE_HOSTS:
            continue
        path = unquote(u.path).lstrip('/') or 'index.html'
        if path.endswith('/'):
            path += 'index.html'
        if path.endswith('.html') or path == 'index.html':
            pages.add(path)
    return pages


def redirect_sources(root: Path):
    sources = set()
    redirects = root / '_redirects'
    if not redirects.exists():
        return sources
    for raw in redirects.read_text(encoding='utf-8', errors='ignore').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        source = line.split()[0]
        if '*' in source or ':' in source:
            continue
        path = source.split('#', 1)[0].split('?', 1)[0].lstrip('/')
        if path:
            sources.add(path)
    return sources


def normalize_internal_target(root: Path, page: Path, href: str):
    if not href or href.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return None
    u = urlsplit(href)
    if u.scheme and u.netloc and u.netloc not in SITE_HOSTS:
        return None
    path = unquote(u.path)
    if not path:
        return None
    base = root if path.startswith('/') or (u.scheme and u.netloc) else page.parent
    clean = path.lstrip('/') or 'index.html'
    target = (base / clean).resolve()
    try:
        rel = target.relative_to(root).as_posix()
    except ValueError:
        return None
    if rel.endswith('/'):
        rel += 'index.html'
    return rel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', nargs='?', default='.')
    ap.add_argument('--out')
    args = ap.parse_args()
    root = Path(args.root).resolve()

    public_pages = sitemap_pages(root)
    redirects = redirect_sources(root)
    missing_public_files = sorted(p for p in public_pages if not (root / p).exists())
    files = [root / rel for rel in sorted(public_pages) if (root / rel).exists()]

    incoming = defaultdict(list)
    missing = []
    generic = []
    duplicates = []
    legacy_anchors = []
    records = {}

    for p in files:
        rel = p.relative_to(root).as_posix()
        raw = p.read_text(encoding='utf-8', errors='ignore')
        parser = Parser()
        parser.feed(raw)
        records[rel] = parser

        dup = [x for x, c in Counter(parser.ids).items() if c > 1]
        if dup:
            duplicates.append({'page': rel, 'ids': dup})

        if '#percorso' in raw or '#livelli-seconda-opinione' in raw:
            legacy_anchors.append(rel)

        for href, text, attrs in parser.links:
            low = text.lower().replace('→', '').strip()
            if low in GENERIC_LABELS or low.startswith('parliamo del caso'):
                generic.append({'page': rel, 'text': text, 'href': href})

            target = normalize_internal_target(root, p, href)
            if not target:
                continue

            if target.endswith('.html') or target == 'index.html':
                incoming[target].append({'from': rel, 'text': text, 'href': href})
                # Un link interno è valido se punta a una pagina pubblica, a un URL
                # mantenuto tramite redirect oppure a un file statico realmente presente.
                if target not in public_pages and target not in redirects and not (root / target).exists():
                    missing.append({'page': rel, 'href': href, 'target': target})

    orphans = []
    for rel, parser in records.items():
        if rel in {'index.html', '404.html'}:
            continue
        if 'noindex' in parser.robots.lower():
            continue
        if not incoming.get(rel):
            orphans.append(rel)

    summary = {
        'public_html_pages': len(files),
        'sitemap_missing_files': len(missing_public_files),
        'missing_internal_targets': len(missing),
        'indexable_orphans': len(orphans),
        'generic_cta_labels': len(generic),
        'duplicate_ids': len(duplicates),
        'legacy_anchors': len(legacy_anchors),
    }

    if args.out:
        out = Path(args.out).resolve()
        out.mkdir(parents=True, exist_ok=True)
        payloads = [
            ('summary.json', summary),
            ('sitemap-missing-files.json', missing_public_files),
            ('orphans.json', orphans),
            ('missing-links.json', missing),
            ('generic-labels.json', generic),
            ('duplicate-ids.json', duplicates),
            ('legacy-anchors.json', legacy_anchors),
        ]
        for name, data in payloads:
            (out / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if missing_public_files:
        print('Sitemap URLs without local file:')
        for rel in missing_public_files:
            print(f' - {rel}')
    if orphans:
        print('Indexable public orphans:')
        for rel in orphans:
            print(f' - {rel}')
    if missing:
        print('Missing internal targets:')
        for item in missing:
            print(f" - {item['page']}: {item['href']} -> {item['target']}")
    if generic:
        print('Generic CTA labels:')
        for item in generic:
            print(f" - {item['page']}: {item['text']} -> {item['href']}")
    if duplicates:
        print('Duplicate IDs:')
        for item in duplicates:
            print(f" - {item['page']}: {', '.join(item['ids'])}")
    if legacy_anchors:
        print('Legacy anchors:')
        for rel in legacy_anchors:
            print(f' - {rel}')

    if missing_public_files or missing or orphans or generic or duplicates or legacy_anchors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
