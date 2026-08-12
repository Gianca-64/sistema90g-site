#!/usr/bin/env python3
from __future__ import annotations

import html.parser
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SKIP_ASSETS = os.environ.get("S90G_SKIP_ASSET_CHECK") == "1"

EXPECTED_HEADINGS = {
    "studio-preliminare-spazi.html": "Studio preliminare degli spazi",
    "controllo-progetto-cucina.html": "Analisi progetto cucina",
    "verifica-planimetria-distribuzione-casa.html": "Verifica preliminare immobile",
    "proprieta-intellettuale.html": "Proprietà intellettuale e uso dei contenuti",
}

PRICE_MATRIX = {
    "scelta-finiture-cucina": 47,
    "restyling-cucina-esistente": 79,
    "controllo-mirato": 127,
    "analisi-completa": 253,
    "acquisto-assistito-cucina": 290,
    "studio-preliminare-spazi": 560,
    "verifica-preliminare-immobile": 149,
    "analisi-unita-varianti": 110,
    "verifica-progetto-cucina": 150,
}

REDIRECT_STUBS = {"progetto-da-zero.html"}
OLD_PUBLIC_TERMS = [
    "€347", "€ 347", "347 €", "€797", "€ 797", "797 €",
    "Check-up Progetto", "Portale sicuro in attivazione",
    "L’invio della pratica non è ancora disponibile",
    "sistema90g-console.sistema90g.workers.dev",
    "sistema90g-public-requests.sistema90g.workers.dev",
    "sistema90g-portale.simply-winspace.it",
]
SKIP_SCHEMES = {"mailto", "tel", "javascript", "data"}


def attrs_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
    return {key.lower(): (value or "") for key, value in attrs}


@dataclass
class PageData:
    lang: str = ""
    title_parts: list[str] = field(default_factory=list)
    h1_parts: list[list[str]] = field(default_factory=list)
    canonical: str = ""
    robots: str = ""
    links: list[dict[str, str]] = field(default_factory=list)
    images: list[dict[str, str]] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)
    stylesheets: list[str] = field(default_factory=list)
    nav_links: list[tuple[str, str]] = field(default_factory=list)
    footer_text: list[str] = field(default_factory=list)
    has_nav: bool = False
    has_footer: bool = False
    ip_link: bool = False

    @property
    def title(self) -> str:
        return " ".join(self.title_parts).strip()

    @property
    def h1_texts(self) -> list[str]:
        return [" ".join(parts).strip() for parts in self.h1_parts]


class PageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.data = PageData()
        self.in_title = False
        self.in_nav = False
        self.in_footer = False
        self.current_h1: list[str] | None = None
        self.current_anchor: dict[str, str] | None = None
        self.current_anchor_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = attrs_dict(attrs)
        if tag == "html":
            self.data.lang = attributes.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.current_h1 = []
            self.data.h1_parts.append(self.current_h1)
        elif tag == "link":
            rel_tokens = {token.lower() for token in attributes.get("rel", "").split()}
            href = attributes.get("href", "")
            if "canonical" in rel_tokens:
                self.data.canonical = href
            if "stylesheet" in rel_tokens and href:
                self.data.stylesheets.append(href)
        elif tag == "meta" and attributes.get("name", "").lower() == "robots":
            self.data.robots = attributes.get("content", "")
        elif tag == "nav" and "s90g-nav" in attributes.get("class", "").split():
            self.in_nav = True
            self.data.has_nav = True
        elif tag == "footer" and "s90g-footer" in attributes.get("class", "").split():
            self.in_footer = True
            self.data.has_footer = True
        elif tag == "a":
            href = attributes.get("href", "")
            self.current_anchor = {
                "href": href,
                "data_start_path": attributes.get("data-start-path", ""),
            }
            self.current_anchor_text = []
            if href == "/proprieta-intellettuale.html":
                self.data.ip_link = True
        elif tag == "img":
            self.data.images.append(attributes)
        elif tag == "script" and attributes.get("src"):
            self.data.scripts.append(attributes["src"])

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.current_h1 = None
        elif tag == "a" and self.current_anchor is not None:
            text = " ".join(self.current_anchor_text).strip()
            link = {**self.current_anchor, "text": text}
            self.data.links.append(link)
            if self.in_nav:
                self.data.nav_links.append((link["href"], text))
            self.current_anchor = None
            self.current_anchor_text = []
        elif tag == "nav":
            self.in_nav = False
        elif tag == "footer":
            self.in_footer = False

    def handle_data(self, data: str) -> None:
        text = re.sub(r"\s+", " ", data).strip()
        if not text:
            return
        if self.in_title:
            self.data.title_parts.append(text)
        if self.current_h1 is not None:
            self.current_h1.append(text)
        if self.current_anchor is not None:
            self.current_anchor_text.append(text)
        if self.in_footer:
            self.data.footer_text.append(text)


def parse_page(raw: str) -> PageData:
    parser = PageParser()
    parser.feed(raw)
    parser.close()
    return parser.data


def local_target(page: Path, value: str) -> Path | None:
    value = value.strip()
    if not value or value.startswith("#") or value.startswith("//"):
        return None
    parsed = urlparse(value)
    if parsed.scheme.lower() in SKIP_SCHEMES or parsed.netloc:
        return None
    clean = unquote(parsed.path)
    if not clean:
        return None
    target = ROOT / clean.lstrip("/") if clean.startswith("/") else page.parent / clean
    if clean.endswith("/"):
        target = target / "index.html"
    return target.resolve()


def check_local_reference(page_rel: str, page: Path, value: str, kind: str, issues: list[tuple]) -> None:
    if SKIP_ASSETS:
        return
    target = local_target(page, value)
    if target is not None and not target.exists():
        issues.append((page_rel, f"missing local {kind}", value))


def main() -> int:
    issues: list[tuple] = []
    canonicals: dict[str, str] = {}
    menus: Counter = Counter()
    footer_signatures: Counter = Counter()
    html_count = 0

    for path in sorted(ROOT.rglob("*.html")):
        if path.name.startswith("._") or ".git" in path.parts or "node_modules" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in REDIRECT_STUBS:
            continue
        raw = path.read_text("utf-8", errors="replace")
        page = parse_page(raw)
        html_count += 1

        if page.lang != "it":
            issues.append((rel, "html lang missing/not it"))

        indexable = "noindex" not in page.robots.lower()
        if not indexable:
            continue

        if len(page.h1_texts) != 1:
            issues.append((rel, "expected one H1", len(page.h1_texts)))
        if not page.title:
            issues.append((rel, "missing title"))
        if not page.canonical:
            issues.append((rel, "missing canonical"))
        elif page.canonical in canonicals:
            issues.append((rel, "duplicate canonical", page.canonical, canonicals[page.canonical]))
        else:
            canonicals[page.canonical] = rel

        lower_raw = raw.lower()
        for token in OLD_PUBLIC_TERMS:
            if token.lower() in lower_raw:
                issues.append((rel, "obsolete public term", token))
        if "®" in raw:
            issues.append((rel, "registered symbol must not be used"))
        if not page.ip_link:
            issues.append((rel, "missing intellectual-property link"))
        if not page.has_footer:
            issues.append((rel, "missing standard footer"))
        else:
            footer_signatures[re.sub(r"\s+", " ", " ".join(page.footer_text)).strip()] += 1
        if not page.has_nav:
            issues.append((rel, "missing navigation"))
        else:
            menus[tuple(page.nav_links)] += 1

        for link in page.links:
            if link["data_start_path"] and link["href"] != "/analisi-preventiva.html#percorso":
                issues.append((rel, "guided CTA wrong target", link["href"]))
            check_local_reference(rel, path, link["href"], "link", issues)
        for image in page.images:
            if "alt" not in image:
                issues.append((rel, "image missing alt", image.get("src", "")))
            if not image.get("width") or not image.get("height"):
                issues.append((rel, "image missing intrinsic dimensions", image.get("src", "")))
            check_local_reference(rel, path, image.get("src", ""), "image", issues)
        for source in page.scripts:
            check_local_reference(rel, path, source, "script", issues)
        for stylesheet in page.stylesheets:
            check_local_reference(rel, path, stylesheet, "stylesheet", issues)

    if len(menus) != 1:
        issues.append(("GLOBAL", "multiple navigation variants", len(menus)))
    if len(footer_signatures) != 1:
        issues.append(("GLOBAL", "multiple footer variants", len(footer_signatures)))

    for filename, heading in EXPECTED_HEADINGS.items():
        path = ROOT / filename
        if not path.exists():
            issues.append((filename, "required page missing"))
        else:
            page = parse_page(path.read_text("utf-8", errors="replace"))
            if heading not in page.h1_texts:
                issues.append((filename, "wrong/missing H1", heading, page.h1_texts))

    role_path = ROOT / "role-case-path.js"
    role = role_path.read_text("utf-8", errors="replace") if role_path.exists() else ""
    if not role:
        issues.append(("role-case-path.js", "required file missing"))
    for service_id, price in PRICE_MATRIX.items():
        if service_id not in role or not re.search(rf"(?:price|unitPrice):\s*{price}\b", role):
            issues.append(("role-case-path.js", "approved price missing/wrong", service_id, price))
    for token in [
        "requester_role", "case_context", "service", "service_title",
        "service_price", "service_time", "service_currency",
    ]:
        if token not in role:
            issues.append(("role-case-path.js", "portal parameter missing", token))
    if "Inizia la richiesta" not in role:
        issues.append(("role-case-path.js", "final CTA wording missing"))

    portal_path = ROOT / "portal-config.js"
    portal = portal_path.read_text("utf-8", errors="replace") if portal_path.exists() else ""
    if not portal:
        issues.append(("portal-config.js", "required file missing"))
    for token in ["attachments: false", "payments: false", "delivery: false"]:
        if token not in portal:
            issues.append(("portal-config.js", "capability/config missing", token))
    portal_active = all(token in portal for token in [
        "enabled: true", "status: 'active'", "initialRequest: true",
    ])
    portal_verification = all(token in portal for token in [
        "enabled: false", "status: 'verification'", "initialRequest: false",
    ])
    if not (portal_active or portal_verification):
        issues.append(("portal-config.js", "inconsistent portal state"))

    htaccess_path = ROOT / ".htaccess"
    htaccess = htaccess_path.read_text("utf-8", errors="replace") if htaccess_path.exists() else ""
    if not htaccess:
        issues.append((".htaccess", "required file missing"))
    for pattern in ["^index\\.html$", "^progetto-da-zero\\.html$", "^www\\.sistema90g\\.it$", "%{HTTPS} !=on"]:
        if pattern not in htaccess:
            issues.append((".htaccess", "redirect/canonical rule missing", pattern))

    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    try:
        sitemap_urls = {
            element.text.strip()
            for element in ET.parse(ROOT / "sitemap.xml").findall(".//sm:loc", namespace)
            if element.text
        }
    except Exception as exc:
        sitemap_urls = set()
        issues.append(("sitemap.xml", "invalid XML", str(exc)))
    if sitemap_urls != set(canonicals):
        issues.append(("sitemap.xml", "canonical parity mismatch", {
            "missing": sorted(set(canonicals) - sitemap_urls),
            "extra": sorted(sitemap_urls - set(canonicals)),
        }))
    try:
        ET.parse(ROOT / "image-sitemap.xml")
    except Exception as exc:
        issues.append(("image-sitemap.xml", "invalid XML", str(exc)))

    print(f"HTML checked: {html_count}")
    print(f"Indexable pages: {len(canonicals)}")
    print(f"Navigation variants: {len(menus)}")
    print(f"Footer variants: {len(footer_signatures)}")
    print(f"Issues: {len(issues)}")
    for issue in issues:
        print(" -", issue)
    if issues:
        return 1
    print("RELEASE AUDIT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
