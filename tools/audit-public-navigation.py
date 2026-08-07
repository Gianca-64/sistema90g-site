#!/usr/bin/env python3
from __future__ import annotations

import html.parser
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

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


class NavParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_main_nav = False
        self.current_href: str | None = None
        self.current_text: list[str] = []
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k: (v or "") for k, v in attrs}
        if tag == "nav" and "s90g-nav" in data.get("class", "").split():
            self.in_main_nav = True
        elif tag == "a" and self.in_main_nav:
            self.current_href = data.get("href", "")
            self.current_text = []

    def handle_data(self, data: str) -> None:
        if self.current_href is not None:
            text = " ".join(data.split())
            if text:
                self.current_text.append(text)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.current_href is not None:
            self.links.append((self.current_href, " ".join(self.current_text).strip()))
            self.current_href = None
            self.current_text = []
        elif tag == "nav" and self.in_main_nav:
            self.in_main_nav = False


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
        rel = parsed.path.lstrip("/") or "index.html"
        pages.append(ROOT / rel)
    return pages


def main() -> int:
    errors: list[str] = []
    checked = 0
    for page in sitemap_pages():
        rel = page.relative_to(ROOT).as_posix()
        if not page.exists():
            errors.append(f"{rel}: pagina in sitemap assente")
            continue
        parser = NavParser()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        checked += 1
        if parser.links != CANONICAL_NAV:
            errors.append(
                f"{rel}: navigazione non canonica\n"
                f"  trovata: {parser.links}\n"
                f"  attesa:  {CANONICAL_NAV}"
            )

    print(f"Pagine sitemap controllate: {checked}")
    print(f"Navigazioni non canoniche: {len(errors)}")
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1
    print("PUBLIC NAVIGATION AUDIT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
