#!/usr/bin/env python3
from __future__ import annotations

import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

HEADER = '<header class="s90g-header"><div class="s90g-shell s90g-header-inner"><a class="s90g-logo" href="/"><strong>SISTEMA <span>90G</span></strong><small>PROGETTAZIONE INDIPENDENTE CUCINE</small></a><nav class="s90g-nav"><a href="/servizi.html">Servizi</a><a href="/analisi-preventiva.html">Come funziona</a><a href="/casi-analizzati.html">Casi reali</a><a href="/professionisti.html">Professionisti</a><a href="/rivenditori-cucine.html">Rivenditori</a><a href="/metodo-sistema90g.html">Metodo e AI</a><a href="/innovazioni.html">Innovazioni</a><a href="/chi-e-sistema90g.html">Chi sono</a><a href="/contatti.html">Contatti</a></nav><a class="s90g-header-cta" href="/analisi-preventiva.html#richiedi"><span>VALUTAZIONE GRATUITA</span><span>→</span></a></div></header>'
FOOTER = '<footer class="s90g-footer"><div class="s90g-shell"><div class="s90g-footer-inner"><div><strong>Sistema 90G</strong><br><span>Progettazione e analisi indipendente dedicata alle cucine · Partita IVA IT02844900221</span></div><div class="s90g-footer-links"><a href="/">Home</a><a href="/servizi.html">Servizi</a><a href="/casi-analizzati.html">Casi</a><a href="/analisi-preventiva.html">Come funziona</a><a href="/professionisti.html">Professionisti</a><a href="/rivenditori-cucine.html">Rivenditori</a><a href="/chi-e-sistema90g.html">Chi sono</a><a href="/contatti.html">Contatti</a><a href="/privacy-policy.html">Privacy</a></div></div></div></footer>'
PRIVACY = '<script defer src="privacy-consent.js?v=20260730a"></script>'


def public_pages():
    tree = ET.parse(ROOT / 'sitemap.xml')
    result = []
    for loc in tree.findall('.//sm:loc', NS):
        if not loc.text:
            continue
        p = urlparse(loc.text.strip())
        rel = unquote(p.path).lstrip('/') or 'index.html'
        if rel.endswith('/'):
            rel += 'index.html'
        path = ROOT / rel
        if path.exists() and path.suffix == '.html':
            result.append(path)
    return result


def jpeg_size(data: bytes):
    if not data.startswith(b'\xff\xd8'):
        return None
    i = 2
    sof = {0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF}
    while i + 4 <= len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker in {0xD8, 0xD9}:
            continue
        if i + 2 > len(data):
            break
        length = int.from_bytes(data[i:i+2], 'big')
        if length < 2 or i + length > len(data):
            break
        if marker in sof and length >= 7:
            h = int.from_bytes(data[i+3:i+5], 'big')
            w = int.from_bytes(data[i+5:i+7], 'big')
            return w, h
        i += length
    return None


def image_size(path: Path):
    try:
        data = path.read_bytes()
    except OSError:
        return None
    suffix = path.suffix.lower()
    if suffix == '.png' and data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) >= 24:
        return struct.unpack('>II', data[16:24])
    if suffix in {'.jpg', '.jpeg'}:
        return jpeg_size(data)
    if suffix == '.svg':
        text = data.decode('utf-8', errors='ignore')[:4096]
        width = re.search(r'\bwidth=["\']([0-9.]+)', text, re.I)
        height = re.search(r'\bheight=["\']([0-9.]+)', text, re.I)
        if width and height:
            return int(float(width.group(1))), int(float(height.group(1)))
        viewbox = re.search(r'\bviewBox=["\']\s*[-0-9.]+\s+[-0-9.]+\s+([0-9.]+)\s+([0-9.]+)', text, re.I)
        if viewbox:
            return int(float(viewbox.group(1))), int(float(viewbox.group(2)))
    return None


def add_dimensions(raw: str, page: Path):
    def repl(match):
        tag = match.group(0)
        if re.search(r'\bwidth\s*=', tag, re.I) and re.search(r'\bheight\s*=', tag, re.I):
            return tag
        src_m = re.search(r'\bsrc\s*=\s*["\']([^"\']+)', tag, re.I)
        if not src_m:
            return tag
        src = src_m.group(1).split('?', 1)[0]
        parsed = urlparse(src)
        if parsed.scheme or parsed.netloc:
            return tag
        image = (ROOT / src.lstrip('/')) if src.startswith('/') else (page.parent / src)
        size = image_size(image.resolve())
        if not size:
            return tag
        w, h = size
        attrs = ''
        if not re.search(r'\bwidth\s*=', tag, re.I):
            attrs += f' width="{w}"'
        if not re.search(r'\bheight\s*=', tag, re.I):
            attrs += f' height="{h}"'
        return tag[:-1] + attrs + '>'
    return re.sub(r'<img\b[^>]*>', repl, raw, flags=re.I)


def add_orphan_links(path: Path, raw: str):
    name = path.name
    if name == 'rivenditori-cucine.html' and '/controllo-progetto-cucina.html' not in raw:
        needle = '<p>Una lettura specialistica di un progetto già sviluppato, concentrata sul perimetro concordato e sulle informazioni che possono richiedere chiarimento prima di proseguire con il cliente.</p>'
        raw = raw.replace(needle, needle + '<p><a href="/controllo-progetto-cucina.html">Vedi il dettaglio della verifica professionale →</a></p>', 1)
    elif name == 'seconda-opinione-cucina.html' and '/esempio-fascicolo-cucina.html' not in raw:
        needle = '<p>Non serve preparare materiale nuovo prima di contattarci. Controlliamo prima se ciò che hai permette una verifica utile.</p>'
        raw = raw.replace(needle, needle + '<p><a href="/esempio-fascicolo-cucina.html">Guarda un esempio di fascicolo di verifica →</a></p>', 1)
    elif name == 'rinnovare-cucina-senza-cambiarla.html' and '/restyling-cucina-esistente.html' not in raw:
        needle = '<p>È utile definire una direzione: che cosa conservare, che cosa cambiare, quali elementi devono dialogare tra loro e quali compatibilità devono essere controllate dal fornitore. Se non sai se il tuo caso richiede una decisione circoscritta o un vero progetto, puoi sottoporlo prima gratuitamente a Sistema 90G.</p>'
        raw = raw.replace(needle, needle + '<p><a href="/restyling-cucina-esistente.html">Come viene inquadrato un intervento di restyling →</a></p>', 1)
    return raw


def fix_page(path: Path):
    raw = path.read_text('utf-8', errors='replace')
    original = raw
    raw = raw.replace('/servizi.html#livelli-seconda-opinione', '/analisi-preventiva.html#richiedi')
    raw = raw.replace('/analisi-preventiva.html#percorso', '/analisi-preventiva.html#richiedi')
    raw = raw.replace('#livelli-seconda-opinione', '#richiedi')
    raw = add_dimensions(raw, path)
    raw = add_orphan_links(path, raw)
    if 'class="s90g-nav"' not in raw:
        raw = re.sub(r'(<body\b[^>]*>)', r'\1' + HEADER, raw, count=1, flags=re.I)
    if 'class="s90g-footer"' not in raw:
        addition = FOOTER
        if 'privacy-consent.js' not in raw:
            addition += PRIVACY
        raw = re.sub(r'</body>', addition + '</body>', raw, count=1, flags=re.I)
    if raw != original:
        path.write_text(raw, 'utf-8')
        print(path.relative_to(ROOT))


for page in public_pages():
    fix_page(page)
