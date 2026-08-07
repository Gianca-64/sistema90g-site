#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap.xml"

CANONICAL_NAV = (
    '<nav class="s90g-nav" aria-label="Navigazione principale">'
    '<a href="/servizi.html">Servizi cucina</a>'
    '<a href="/analisi-completa.html">Verifica progetto</a>'
    '<a href="/analisi-preventivo-cucina.html">Verifica preventivo</a>'
    '<a href="/acquisto-assistito-cucina.html">Acquisto assistito</a>'
    '<a href="/problemi-errori-cucina.html">Problemi ed errori</a>'
    '<a href="/casi-cucina.html">Casi reali</a>'
    '<a href="/analisi-preventiva.html">Come funziona</a>'
    '</nav>'
)

CANONICAL_FOOTER = (
    '<footer class="s90g-footer"><div class="s90g-shell"><div class="s90g-footer-inner"><div>'
    '<strong>Sistema 90G</strong><br/><span>Verifica indipendente della cucina · Partita IVA IT02844900221</span>'
    '</div><div class="s90g-footer-links">'
    '<a href="/servizi.html">Servizi cucina</a>'
    '<a href="/problemi-errori-cucina.html">Problemi ed errori</a>'
    '<a href="/casi-cucina.html">Casi reali</a>'
    '<a href="/analisi-preventiva.html">Come funziona</a>'
    '<a href="/chi-e-sistema90g.html">Chi sono</a>'
    '<a href="/contatti.html">Contatti</a>'
    '<a href="/privacy-policy.html">Privacy</a>'
    '<a href="/cookie-policy.html">Cookie</a>'
    '<a href="/proprieta-intellettuale.html">Proprietà intellettuale</a>'
    '<a data-cookie-settings href="#">Gestisci cookie</a>'
    '<a href="mailto:info@sistema90g.it">info@sistema90g.it</a>'
    '</div></div><p class="s90g-footer-notice">Le verifiche documentali non sostituiscono rilievi, calcoli, certificazioni o controlli riservati ai professionisti competenti.</p></div></footer>'
)

NAV_RE = re.compile(r'<nav\b(?=[^>]*\bs90g-nav\b)[^>]*>.*?</nav>', re.I | re.S)
FOOTER_RE = re.compile(r'<footer\b(?=[^>]*\bs90g-footer\b)[^>]*>.*?</footer>', re.I | re.S)
LOGO_SMALL_RE = re.compile(r'(<a\b(?=[^>]*\bs90g-logo\b)[^>]*>.*?<small>).*?(</small>)', re.I | re.S)
HEADER_CTA_TEXT_RE = re.compile(r'(<a\b(?=[^>]*\bs90g-header-cta\b)[^>]*>\s*<span>).*?(</span>)', re.I | re.S)


def sitemap_pages() -> list[Path]:
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(SITEMAP)
    pages: list[Path] = []
    for loc in tree.findall(".//sm:loc", ns):
        if not loc.text:
            continue
        parsed = urlparse(loc.text.strip())
        if parsed.netloc not in {"sistema90g.it", "www.sistema90g.it"}:
            continue
        pages.append(ROOT / (parsed.path.lstrip("/") or "index.html"))
    return pages


def normalize(text: str) -> str:
    text, nav_count = NAV_RE.subn(CANONICAL_NAV, text, count=1)
    text, footer_count = FOOTER_RE.subn(CANONICAL_FOOTER, text, count=1)
    text = LOGO_SMALL_RE.sub(r'\1VERIFICA INDIPENDENTE CUCINA\2', text, count=1)
    text = HEADER_CTA_TEXT_RE.sub(r'\1RICHIEDI LA VERIFICA\2', text, count=1)
    if nav_count != 1:
        raise ValueError(f"navigazione principale trovata {nav_count} volte")
    if footer_count != 1:
        raise ValueError(f"footer standard trovato {footer_count} volte")
    return text


def main() -> int:
    changed: list[str] = []
    errors: list[str] = []
    for page in sitemap_pages():
        rel = page.relative_to(ROOT).as_posix()
        if not page.exists():
            errors.append(f"{rel}: file assente")
            continue
        original = page.read_text(encoding="utf-8")
        try:
            updated = normalize(original)
        except ValueError as exc:
            errors.append(f"{rel}: {exc}")
            continue
        if updated != original:
            page.write_text(updated, encoding="utf-8")
            changed.append(rel)

    print(f"Pagine aggiornate: {len(changed)}")
    for rel in changed:
        print(f"- {rel}")
    if errors:
        print("ERRORI:")
        for error in errors:
            print(f"- {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
