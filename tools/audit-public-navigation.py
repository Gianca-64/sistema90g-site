#!/usr/bin/env python3
from __future__ import annotations

import html.parser
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap.xml"

CANONICAL_NAV = [
    ("/servizi.html", "Servizi cucina"),
    ("/analisi-completa.html", "Verifica progetto"),
    ("/analisi-preventivo-cucina.html", "Verifica preventivo"),
    ("/acquisto-assistito-cucina.html", "Acquisto assistito"),
    ("/problemi-errori-cucina.html", "Problemi ed errori"),
    ("/casi-cucina.html", "Casi reali"),
    ("/analisi-preventiva.html", "Come funziona"),
]

CANONICAL_FOOTER_HREFS = [
    "/servizi.html",
    "/problemi-errori-cucina.html",
    "/casi-cucina.html",
    "/analisi-preventiva.html",
    "/chi-e-sistema90g.html",
    "/contatti.html",
    "/privacy-policy.html",
    "/cookie-policy.html",
    "/proprieta-intellettuale.html",
    "#",
    "mailto:info@sistema90g.it",
]


class PageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_main_nav = False
        self.in_footer = False
        self.current_nav_href: str | None = None
        self.current_nav_text: list[str] = []
        self.nav_links: list[tuple[str, str]] = []
        self.footer_hrefs: list[str] = []
        self.title_count = 0
        self.h1_count = 0
        self.description_count = 0
        self.canonical = ""
        self.robots = ""
        self.local_refs: list[tuple[str, str]] = []
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k.lower(): (v or "") for k, v in attrs}
        classes = data.get("class", "").split()
        if tag == "nav" and "s90g-nav" in classes:
            self.in_main_nav = True
        elif tag == "footer" and "s90g-footer" in classes:
            self.in_footer = True
        elif tag == "a":
            href = data.get("href", "")
            if self.in_main_nav:
                self.current_nav_href = href
                self.current_nav_text = []
            if self.in_footer:
                self.footer_hrefs.append(href)
            if href:
                self.local_refs.append(("link", href))
        elif tag == "title":
            self.title_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            name = data.get("name", "").lower()
            if name == "description":
                self.description_count += 1
            elif name == "robots":
                self.robots = data.get("content", "")
        elif tag == "link":
            rel = {item.lower() for item in data.get("rel", "").split()}
            href = data.get("href", "")
            if "canonical" in rel:
                self.canonical = href
            if "stylesheet" in rel and href:
                self.local_refs.append(("stylesheet", href))
        elif tag == "script" and data.get("src"):
            self.local_refs.append(("script", data["src"]))
        elif tag == "img":
            self.images.append(data)
            if data.get("src"):
                self.local_refs.append(("image", data["src"]))

    def handle_data(self, data: str) -> None:
        if self.current_nav_href is not None:
            text = " ".join(data.split())
            if text:
                self.current_nav_text.append(text)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.current_nav_href is not None:
            self.nav_links.append((self.current_nav_href, " ".join(self.current_nav_text).strip()))
            self.current_nav_href = None
            self.current_nav_text = []
        elif tag == "nav" and self.in_main_nav:
            self.in_main_nav = False
        elif tag == "footer" and self.in_footer:
            self.in_footer = False


def sitemap_pages() -> list[tuple[str, Path]]:
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(SITEMAP)
    pages: list[tuple[str, Path]] = []
    for loc in tree.findall(".//sm:loc", ns):
        if not loc.text:
            continue
        url = loc.text.strip()
        parsed = urlparse(url)
        if parsed.netloc not in {"sistema90g.it", "www.sistema90g.it"}:
            continue
        rel = parsed.path.lstrip("/") or "index.html"
        pages.append((url, ROOT / rel))
    return pages


def local_target(page: Path, value: str) -> Path | None:
    if not value or value.startswith("#"):
        return None
    parsed = urlparse(value)
    if parsed.scheme in {"mailto", "tel", "javascript", "data"}:
        return None
    if parsed.netloc and parsed.netloc not in {"sistema90g.it", "www.sistema90g.it"}:
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    if parsed.netloc or path.startswith("/"):
        target = ROOT / (path.lstrip("/") or "index.html")
    else:
        target = page.parent / path
    if path.endswith("/"):
        target = target / "index.html"
    return target.resolve()


def main() -> int:
    errors: list[str] = []
    checked = 0
    for expected_url, page in sitemap_pages():
        rel = page.relative_to(ROOT).as_posix()
        if not page.exists():
            errors.append(f"{rel}: pagina in sitemap assente")
            continue
        raw = page.read_text(encoding="utf-8", errors="replace")
        parser = PageParser()
        parser.feed(raw)
        checked += 1

        if parser.title_count != 1:
            errors.append(f"{rel}: atteso un solo title, trovati {parser.title_count}")
        if parser.h1_count != 1:
            errors.append(f"{rel}: atteso un solo H1, trovati {parser.h1_count}")
        if parser.description_count != 1:
            errors.append(f"{rel}: attesa una sola meta description, trovate {parser.description_count}")
        if parser.canonical != expected_url:
            errors.append(f"{rel}: canonical {parser.canonical!r} diverso da sitemap {expected_url!r}")
        if "noindex" in parser.robots.lower():
            errors.append(f"{rel}: pagina in sitemap marcata noindex")
        if parser.nav_links != CANONICAL_NAV:
            errors.append(f"{rel}: navigazione principale non canonica")
        if parser.footer_hrefs != CANONICAL_FOOTER_HREFS:
            errors.append(f"{rel}: footer non canonico")
        if "<small>VERIFICA INDIPENDENTE CUCINA</small>" not in raw:
            errors.append(f"{rel}: payoff header non canonico")
        if "<span>RICHIEDI LA VERIFICA</span>" not in raw:
            errors.append(f"{rel}: CTA header non canonica")

        for image in parser.images:
            if "alt" not in image:
                errors.append(f"{rel}: immagine senza alt: {image.get('src', '')}")
            if not image.get("width") or not image.get("height"):
                errors.append(f"{rel}: immagine senza dimensioni intrinseche: {image.get('src', '')}")

        for kind, value in parser.local_refs:
            target = local_target(page, value)
            if target is not None and not target.exists():
                errors.append(f"{rel}: {kind} locale inesistente: {value}")

    print(f"Pagine sitemap controllate: {checked}")
    print(f"Problemi trovati: {len(errors)}")
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1
    print("PUBLIC SITE QUALITY AUDIT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
