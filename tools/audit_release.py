#!/usr/bin/env python3
from __future__ import annotations

import html.parser
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SKIP_ASSETS = os.environ.get('S90G_SKIP_ASSET_CHECK') == '1'
SITE_ORIGIN = 'https://sistema90g.it'
SITE_HOSTS = {'sistema90g.it', 'www.sistema90g.it'}
NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
SKIP_SCHEMES = {'mailto', 'tel', 'javascript', 'data'}

CANONICAL_OFFER = [
    'Consulenza 90G · 97 €',
    'Verifica 90G · 127 €',
    'Progetto Cucina 90G · 145 €',
    '+117 € ciascuno',
    'Render fotorealistici · 57 € / vista',
]
LEGACY_PUBLIC_TERMS = [
    '#percorso',
    '#livelli-seconda-opinione',
    'Seconda Opinione · dubbio preciso',
    'Seconda Opinione · controllo completo',
    'Controllo mirato',
    'Analisi completa',
    'Acquisto Assistito · 290 €',
    '€347', '€ 347', '347 €', '€797', '€ 797', '797 €',
    'Check-up Progetto',
    'Portale sicuro in attivazione',
    'L’invio della pratica non è ancora disponibile',
    'sistema90g-console.sistema90g.workers.dev',
    'sistema90g-public-requests.sistema90g.workers.dev',
    'sistema90g-portale.simply-winspace.it',
]
PUBLIC_RUNTIME_FILES = [
    'navigation-conversion.js',
    'privacy-consent.js',
]


def attrs_dict(attrs):
    return {key.lower(): (value or '') for key, value in attrs}


@dataclass
class PageData:
    lang: str = ''
    title_parts: list[str] = field(default_factory=list)
    h1_parts: list[list[str]] = field(default_factory=list)
    canonical: str = ''
    robots: str = ''
    links: list[dict[str, str]] = field(default_factory=list)
    images: list[dict[str, str]] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)
    stylesheets: list[str] = field(default_factory=list)
    ids: list[str] = field(default_factory=list)
    has_nav: bool = False
    has_footer: bool = False

    @property
    def title(self):
        return ' '.join(self.title_parts).strip()

    @property
    def h1_texts(self):
        return [' '.join(parts).strip() for parts in self.h1_parts]


class PageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.data = PageData()
        self.in_title = False
        self.current_h1 = None
        self.current_anchor = None
        self.current_anchor_text = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        a = attrs_dict(attrs)
        if 'id' in a:
            self.data.ids.append(a['id'])
        if tag == 'html':
            self.data.lang = a.get('lang', '')
        elif tag == 'title':
            self.in_title = True
        elif tag == 'h1':
            self.current_h1 = []
            self.data.h1_parts.append(self.current_h1)
        elif tag == 'link':
            rel = {token.lower() for token in a.get('rel', '').split()}
            href = a.get('href', '')
            if 'canonical' in rel:
                self.data.canonical = href
            if 'stylesheet' in rel and href:
                self.data.stylesheets.append(href)
        elif tag == 'meta' and a.get('name', '').lower() == 'robots':
            self.data.robots = a.get('content', '')
        elif tag == 'nav' and 's90g-nav' in a.get('class', '').split():
            self.data.has_nav = True
        elif tag == 'footer' and 's90g-footer' in a.get('class', '').split():
            self.data.has_footer = True
        elif tag == 'a':
            self.current_anchor = {
                'href': a.get('href', ''),
                'data_start_path': 'data-start-path' in a,
            }
            self.current_anchor_text = []
        elif tag == 'img':
            self.data.images.append(a)
        elif tag == 'script' and a.get('src'):
            self.data.scripts.append(a['src'])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == 'title':
            self.in_title = False
        elif tag == 'h1':
            self.current_h1 = None
        elif tag == 'a' and self.current_anchor is not None:
            self.data.links.append({
                **self.current_anchor,
                'text': ' '.join(self.current_anchor_text).strip(),
            })
            self.current_anchor = None
            self.current_anchor_text = []

    def handle_data(self, data):
        text = re.sub(r'\s+', ' ', data).strip()
        if not text:
            return
        if self.in_title:
            self.data.title_parts.append(text)
        if self.current_h1 is not None:
            self.current_h1.append(text)
        if self.current_anchor is not None:
            self.current_anchor_text.append(text)


def parse_page(raw):
    parser = PageParser()
    parser.feed(raw)
    parser.close()
    return parser.data


def sitemap_entries():
    entries = []
    tree = ET.parse(ROOT / 'sitemap.xml')
    for loc in tree.findall('.//sm:loc', NS):
        if not loc.text:
            continue
        url = loc.text.strip()
        parsed = urlparse(url)
        if parsed.netloc not in SITE_HOSTS:
            continue
        rel = unquote(parsed.path).lstrip('/') or 'index.html'
        if rel.endswith('/'):
            rel += 'index.html'
        entries.append((url, rel))
    return entries


def local_target(page: Path, value: str):
    value = value.strip()
    if not value or value.startswith('#') or value.startswith('//'):
        return None
    parsed = urlparse(value)
    if parsed.scheme.lower() in SKIP_SCHEMES:
        return None
    if parsed.netloc and parsed.netloc not in SITE_HOSTS:
        return None
    clean = unquote(parsed.path)
    if not clean:
        return None
    target = (ROOT / clean.lstrip('/')) if (clean.startswith('/') or parsed.netloc) else (page.parent / clean)
    if clean.endswith('/'):
        target = target / 'index.html'
    return target.resolve()


def check_local_reference(page_rel, page, value, kind, issues):
    if SKIP_ASSETS:
        return
    target = local_target(page, value)
    if target is not None and not target.exists():
        issues.append((page_rel, f'missing local {kind}', value))


def canonical_expected(rel):
    return f'{SITE_ORIGIN}/' if rel == 'index.html' else f'{SITE_ORIGIN}/{rel}'


def audit():
    issues = []
    entries = sitemap_entries()
    sitemap_urls = [url for url, _ in entries]
    if len(sitemap_urls) != len(set(sitemap_urls)):
        issues.append(('sitemap.xml', 'duplicate URL'))

    pages = {}
    for url, rel in entries:
        path = ROOT / rel
        if not path.exists():
            issues.append((rel, 'sitemap file missing'))
            continue
        raw = path.read_text('utf-8', errors='replace')
        page = parse_page(raw)
        pages[rel] = (page, raw)

        if page.lang != 'it':
            issues.append((rel, 'html lang missing/not it', page.lang))
        if len(page.h1_texts) != 1:
            issues.append((rel, 'expected one H1', len(page.h1_texts)))
        if not page.title:
            issues.append((rel, 'missing title'))
        expected = canonical_expected(rel)
        if page.canonical != expected:
            issues.append((rel, 'canonical mismatch', page.canonical, expected))
        if not page.has_nav:
            issues.append((rel, 'missing navigation'))
        if not page.has_footer:
            issues.append((rel, 'missing footer'))

        for token in LEGACY_PUBLIC_TERMS:
            if token.lower() in raw.lower():
                issues.append((rel, 'legacy public term', token))
        if '®' in raw:
            issues.append((rel, 'registered symbol must not be used'))

        for link in page.links:
            if link['data_start_path'] and '#richiedi' not in link['href']:
                issues.append((rel, 'Free Entry CTA wrong target', link['href']))
            check_local_reference(rel, path, link['href'], 'link', issues)
        for image in page.images:
            if 'alt' not in image:
                issues.append((rel, 'image missing alt', image.get('src', '')))
            if not image.get('width') or not image.get('height'):
                issues.append((rel, 'image missing intrinsic dimensions', image.get('src', '')))
            check_local_reference(rel, path, image.get('src', ''), 'image', issues)
        for source in page.scripts:
            check_local_reference(rel, path, source, 'script', issues)
        for stylesheet in page.stylesheets:
            check_local_reference(rel, path, stylesheet, 'stylesheet', issues)

    # Contratto dell'offerta pubblica.
    services = (ROOT / 'servizi.html').read_text('utf-8', errors='replace')
    for token in CANONICAL_OFFER:
        if token not in services:
            issues.append(('servizi.html', 'canonical offer missing', token))

    intake = (ROOT / 'analisi-preventiva.html').read_text('utf-8', errors='replace')
    if 'id="richiedi"' not in intake:
        issues.append(('analisi-preventiva.html', 'Free Entry #richiedi missing'))
    portal_links = re.findall(r'https://portale\.sistema90g\.it/portal\.html\?[^\"\']+', intake)
    if len(portal_links) < 7:
        issues.append(('analisi-preventiva.html', 'expected role-based Free Entry links', len(portal_links)))
    for href in portal_links:
        if 'service=valutazione-iniziale' not in href:
            issues.append(('analisi-preventiva.html', 'portal link not Free Entry', href))
        if 'service_price=' in href:
            issues.append(('analisi-preventiva.html', 'Free Entry link transmits price', href))

    # I runtime pubblici non devono poter reintrodurre il vecchio funnel.
    for filename in PUBLIC_RUNTIME_FILES:
        raw = (ROOT / filename).read_text('utf-8', errors='replace')
        for token in ['#percorso', '#livelli-seconda-opinione', 'controllo-mirato', 'analisi-completa']:
            if token in raw:
                issues.append((filename, 'legacy runtime token', token))

    # Il vecchio catalogo può restare nel repository solo come materiale storico,
    # ma il build deve esplicitamente impedirne la pubblicazione.
    build = (ROOT / 'tools/build_cloudflare.sh').read_text('utf-8', errors='replace')
    for token in ['role-case-path.js', 'role-case-path.css']:
        if token not in build:
            issues.append(('tools/build_cloudflare.sh', 'legacy catalog exclusion missing', token))

    for xml_name in ['sitemap.xml', 'guide-cucina-sitemap.xml', 'image-sitemap.xml']:
        try:
            ET.parse(ROOT / xml_name)
        except Exception as exc:
            issues.append((xml_name, 'invalid XML', str(exc)))

    print(f'Public sitemap pages checked: {len(entries)}')
    print(f'Issues: {len(issues)}')
    for issue in issues:
        print(' -', issue)
    if issues:
        return 1
    print('RELEASE AUDIT: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(audit())
