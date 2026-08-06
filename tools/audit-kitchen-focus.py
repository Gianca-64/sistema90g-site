#!/usr/bin/env python3
"""Audit statico del percorso commerciale cucina.

Controlla coerenza minima tra pagine, servizi, prezzi, collegamenti locali,
ID HTML, sitemap e separazione tra contenuti pubblici e note operative interne.
Non sostituisce il collaudo visivo o il test end-to-end.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

HTML_FILES = [
    "index.html",
    "servizi.html",
    "analisi-preventiva.html",
    "controllo-mirato.html",
    "analisi-completa.html",
    "acquisto-assistito-cucina.html",
    "scelta-finiture-casa.html",
    "restyling-cucina-esistente.html",
    "analisi-preventivo-cucina.html",
    "problemi-errori-cucina.html",
    "casi-cucina.html",
]

SERVICES = {
    "controllo-mirato": {
        "code": "S90G-K01",
        "price": "127",
        "page": "controllo-mirato.html",
    },
    "analisi-completa": {
        "code": "S90G-K02",
        "price": "253",
        "page": "analisi-completa.html",
    },
    "acquisto-assistito-cucina": {
        "code": "S90G-K03",
        "price": "290",
        "page": "acquisto-assistito-cucina.html",
    },
    "scelta-finiture-cucina": {
        "code": "S90G-K11",
        "price": "47",
        "page": "scelta-finiture-casa.html",
    },
    "restyling-cucina-esistente": {
        "code": "S90G-K12",
        "price": "79",
        "page": "restyling-cucina-esistente.html",
    },
}

REQUIRED_NAV_LINKS = {
    "/servizi.html",
    "/analisi-completa.html",
    "/analisi-preventivo-cucina.html",
    "/acquisto-assistito-cucina.html",
    "/problemi-errori-cucina.html",
    "/casi-cucina.html",
    "/analisi-preventiva.html",
}

SITEMAP_REQUIRED = {
    "https://sistema90g.it/",
    "https://sistema90g.it/servizi.html",
    "https://sistema90g.it/analisi-preventiva.html",
    "https://sistema90g.it/controllo-mirato.html",
    "https://sistema90g.it/analisi-completa.html",
    "https://sistema90g.it/acquisto-assistito-cucina.html",
    "https://sistema90g.it/scelta-finiture-casa.html",
    "https://sistema90g.it/restyling-cucina-esistente.html",
    "https://sistema90g.it/analisi-preventivo-cucina.html",
    "https://sistema90g.it/problemi-errori-cucina.html",
    "https://sistema90g.it/casi-cucina.html",
}

SITEMAP_FORBIDDEN = {
    "https://sistema90g.it/interesse-professionale.html",
    "https://sistema90g.it/controllo-progetto-cucina.html",
    "https://sistema90g.it/professionisti.html",
    "https://sistema90g.it/rivenditori-cucine.html",
}

FORBIDDEN_PUBLIC_PHRASES = {
    "sottoposto al collaudo operativo",
    "sottoposti al collaudo operativo",
    "numero standard dei render resta",
    "prezzo attuale",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.nav_href_sets: list[set[str]] = []
        self._in_nav = False
        self._current_nav: set[str] | None = None
        self.title_count = 0
        self.h1_count = 0
        self.canonical_count = 0
        self.description_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if data.get("id"):
            self.ids.append(data["id"])
        if tag == "a" and data.get("href"):
            self.hrefs.append(data["href"])
            if self._in_nav and self._current_nav is not None:
                self._current_nav.add(data["href"])
        if tag == "nav":
            self._in_nav = True
            self._current_nav = set()
            self.nav_href_sets.append(self._current_nav)
        if tag == "title":
            self.title_count += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical_count += 1
        if tag == "meta" and data.get("name") == "description":
            self.description_count += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "nav":
            self._in_nav = False
            self._current_nav = None


def local_target_exists(href: str) -> bool:
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return True
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        return True
    path = parsed.path
    if not path or path == "/":
        path = "/index.html"
    target = ROOT / path.lstrip("/")
    return target.exists()


def audit_page(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    try:
        parser.feed(text)
    except Exception as exc:  # pragma: no cover - diagnostic path
        return [f"{path.name}: parsing HTML fallito: {exc}"]

    duplicates = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
    if duplicates:
        errors.append(f"{path.name}: ID duplicati: {', '.join(duplicates)}")
    if parser.title_count != 1:
        errors.append(f"{path.name}: deve contenere un solo <title>, trovati {parser.title_count}")
    if parser.h1_count != 1:
        errors.append(f"{path.name}: deve contenere un solo <h1>, trovati {parser.h1_count}")
    if parser.canonical_count != 1:
        errors.append(f"{path.name}: canonical assente o duplicato ({parser.canonical_count})")
    if parser.description_count != 1:
        errors.append(f"{path.name}: meta description assente o duplicata ({parser.description_count})")

    for href in parser.hrefs:
        if not local_target_exists(href):
            errors.append(f"{path.name}: collegamento locale inesistente: {href}")

    main_nav = max(parser.nav_href_sets, key=len, default=set())
    missing_nav = sorted(REQUIRED_NAV_LINKS - main_nav)
    if missing_nav:
        errors.append(f"{path.name}: navigazione cucina incompleta: {', '.join(missing_nav)}")

    if "casa e cucina" in text.lower() or "studio preliminare degli spazi" in text.lower():
        errors.append(f"{path.name}: contiene linguaggio generalista sospeso")
    return errors


def audit_services() -> list[str]:
    errors: list[str] = []
    js = (ROOT / "role-case-path.js").read_text(encoding="utf-8")
    services_page = (ROOT / "servizi.html").read_text(encoding="utf-8")

    for slug, expected in SERVICES.items():
        service_page = (ROOT / expected["page"]).read_text(encoding="utf-8")

        if slug not in js:
            errors.append(f"role-case-path.js: servizio assente: {slug}")
        if expected["code"] not in js:
            errors.append(f"role-case-path.js: codice assente: {expected['code']}")
        if not re.search(rf"price\s*:\s*{re.escape(expected['price'])}\b", js):
            errors.append(f"role-case-path.js: prezzo non coerente per {slug}")

        if expected["code"] not in services_page:
            errors.append(f"servizi.html: codice assente: {expected['code']}")
        if f"€{expected['price']}" not in services_page and f"€ {expected['price']}" not in services_page:
            errors.append(f"servizi.html: prezzo assente per {slug}: €{expected['price']}")

        if expected["code"] not in service_page:
            errors.append(f"{expected['page']}: codice assente: {expected['code']}")
        if f"€{expected['price']}" not in service_page and f"€ {expected['price']}" not in service_page:
            errors.append(f"{expected['page']}: prezzo pubblico assente: €{expected['price']}")
        if f'data-service="{slug}"' not in service_page:
            errors.append(f"{expected['page']}: CTA senza servizio canonico locale {slug}")

    for context_key in ("source_page", "content_type", "cta_position"):
        if f"source.searchParams.get('{context_key}')" not in js:
            errors.append(f"role-case-path.js: contesto di origine non conservato: {context_key}")

    for preserved_key in ("utm_source", "utm_medium", "utm_campaign", "case_id"):
        if f"'{preserved_key}'" not in js:
            errors.append(f"role-case-path.js: parametro non conservato: {preserved_key}")

    return errors


def audit_public_boundaries() -> list[str]:
    errors: list[str] = []
    page = (ROOT / "acquisto-assistito-cucina.html").read_text(encoding="utf-8")
    lowered = page.lower()

    for phrase in FORBIDDEN_PUBLIC_PHRASES:
        if phrase in lowered:
            errors.append(
                "acquisto-assistito-cucina.html: nota operativa interna esposta: "
                + phrase
            )

    for required in ("cinque render", "una vista della variante di finitura"):
        if required not in lowered:
            errors.append(
                "acquisto-assistito-cucina.html: promessa pubblica incompleta: "
                + required
            )

    return errors


def audit_sitemap() -> list[str]:
    errors: list[str] = []
    text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    urls = set(re.findall(r"<loc>(.*?)</loc>", text))

    missing = sorted(SITEMAP_REQUIRED - urls)
    if missing:
        errors.append("sitemap.xml: URL obbligatori assenti: " + ", ".join(missing))

    forbidden = sorted(SITEMAP_FORBIDDEN & urls)
    if forbidden:
        errors.append(
            "sitemap.xml: percorsi professionali non ancora attivi presenti: "
            + ", ".join(forbidden)
        )

    if "index.html" in text:
        errors.append("sitemap.xml: la home canonica non deve usare /index.html")
    return errors


def main() -> int:
    errors: list[str] = []
    for filename in HTML_FILES:
        path = ROOT / filename
        if not path.exists():
            errors.append(f"File obbligatorio assente: {filename}")
            continue
        errors.extend(audit_page(path))

    errors.extend(audit_services())
    errors.extend(audit_public_boundaries())
    errors.extend(audit_sitemap())

    if errors:
        print("AUDIT CUCINA: FALLITO")
        for error in errors:
            print(f"- {error}")
        return 1

    print("AUDIT CUCINA: SUPERATO")
    print(f"Pagine controllate: {len(HTML_FILES)}")
    print(f"Servizi controllati: {len(SERVICES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())