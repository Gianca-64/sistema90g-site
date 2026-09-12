#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

CORE = {
    "index.html",
    "analisi-preventiva.html",
    "servizi.html",
    "casi-analizzati.html",
    "chi-e-sistema90g.html",
    "metodo-sistema90g.html",
}

EXPECTED_NAV = [
    "Problemi da evitare",
    "Casi reali",
    "Guide",
    "Come funziona",
    "Servizi e prezzi",
    "Chi sono",
]

EXPECTED_FOOTER = [
    "Home",
    "Casi",
    "Guide",
    "Come funziona",
    "Servizi e prezzi",
    "Metodo",
    "Chi sono",
    "Contatti",
    "Privacy",
    "Cookie",
    "Proprietà intellettuale",
]

RETIRED_DESCRIPTORS = {
    "PROGETTAZIONE INDIPENDENTE CUCINE",
    "ANALISI PREVENTIVA INDIPENDENTE",
    "ANALISI INDIPENDENTE CUCINE",
}

errors = []

xml = (
    ROOT / "sitemap.xml"
).read_text(errors="replace")

urls = re.findall(
    r"<loc>\s*(.*?)\s*</loc>",
    xml,
    re.I
)

pages = []

for url in urls:

    path = urlparse(url).path.lstrip("/")

    if not path:
        path = "index.html"

    if path.endswith(".html"):
        pages.append(path)

if len(pages) != 76:
    errors.append(
        f"expected 76 sitemap HTML pages, found {len(pages)}"
    )

shared = [
    page
    for page in pages
    if page not in CORE
]

if len(shared) != 70:
    errors.append(
        f"expected 70 shared indexed pages, found {len(shared)}"
    )


class ShellParser(HTMLParser):

    def __init__(self):

        super().__init__()

        self.logo_depth = 0
        self.logo_small = False

        self.in_nav = False
        self.in_footer_links = False
        self.in_header_cta = False
        self.in_a = False

        self.buf = []

        self.descriptors = []
        self.nav = []
        self.footer = []

        self.cta_text = None
        self.cta_href = None

    def handle_starttag(self, tag, attrs):

        attrs = dict(attrs)
        classes = attrs.get(
            "class",
            ""
        ).split()

        if (
            tag == "a"
            and "s90g-logo" in classes
        ):
            self.logo_depth = 1

        elif self.logo_depth:
            self.logo_depth += 1

        if (
            tag == "small"
            and self.logo_depth
        ):
            self.logo_small = True

        if (
            tag == "nav"
            and "s90g-nav" in classes
        ):
            self.in_nav = True

        if (
            tag == "div"
            and "s90g-footer-links" in classes
        ):
            self.in_footer_links = True

        if (
            tag == "a"
            and "s90g-header-cta" in classes
        ):
            self.in_header_cta = True
            self.cta_href = attrs.get(
                "href",
                ""
            )
            self.buf = []

        elif (
            tag == "a"
            and (
                self.in_nav
                or self.in_footer_links
            )
        ):
            self.in_a = True
            self.buf = []

    def handle_data(self, data):

        if self.logo_small:
            value = " ".join(
                data.split()
            )

            if value:
                self.descriptors.append(
                    value
                )

        if (
            self.in_a
            or self.in_header_cta
        ):
            self.buf.append(data)

    def handle_endtag(self, tag):

        if (
            tag == "small"
            and self.logo_small
        ):
            self.logo_small = False

        if tag == "a" and self.in_header_cta:

            self.cta_text = " ".join(
                " ".join(
                    self.buf
                ).split()
            )

            self.in_header_cta = False
            self.buf = []

        elif tag == "a" and self.in_a:

            text = " ".join(
                " ".join(
                    self.buf
                ).split()
            )

            if self.in_nav:
                self.nav.append(text)

            if self.in_footer_links:
                self.footer.append(text)

            self.in_a = False
            self.buf = []

        if (
            tag == "nav"
            and self.in_nav
        ):
            self.in_nav = False

        if (
            tag == "div"
            and self.in_footer_links
        ):
            self.in_footer_links = False

        if self.logo_depth:
            self.logo_depth -= 1


for filename in shared:

    p = ROOT / filename

    if not p.exists():
        errors.append(
            f"indexed shared page missing: {filename}"
        )
        continue

    html = p.read_text(
        errors="replace"
    )

    parser = ShellParser()
    parser.feed(html)

    if parser.descriptors != [
        "VEDERE IL PROBLEMA PRIMA"
    ]:
        errors.append(
            f"{filename}: descriptor={parser.descriptors}"
        )

    if parser.nav != EXPECTED_NAV:
        errors.append(
            f"{filename}: nav={' | '.join(parser.nav)}"
        )

    if parser.footer != EXPECTED_FOOTER:
        errors.append(
            f"{filename}: footer={' | '.join(parser.footer)}"
        )

    if not parser.cta_text:
        errors.append(
            f"{filename}: header CTA missing"
        )
    else:
        cta = (
            parser.cta_text
            .replace("→", "")
            .strip()
        )

        if cta != "MOSTRA IL TUO CASO":
            errors.append(
                f"{filename}: CTA={parser.cta_text}"
            )

    if (
        parser.cta_href
        != "/analisi-preventiva.html#richiedi"
    ):
        errors.append(
            f"{filename}: CTA href={parser.cta_href}"
        )

    if (
        'data-s90g-nav-managed="page"'
        in html
    ):
        errors.append(
            f"{filename}: shared page became page-managed"
        )

    for retired in RETIRED_DESCRIPTORS:

        if retired in html:
            errors.append(
                f"{filename}: retired descriptor remains: {retired}"
            )

    if "Metodo e AI" in re.search(
        r'<header\b[\s\S]*?</header>',
        html,
        re.I
    ).group(0):
        errors.append(
            f"{filename}: Metodo e AI remains in header"
        )

    script_matches = re.findall(
        r'<script\b[^>]*src=["\']'
        r'([^"\']*privacy-consent\.js[^"\']*)',
        html,
        re.I
    )

    if script_matches != [
        "/privacy-consent.js?v=20260912a"
    ]:
        errors.append(
            f"{filename}: privacy bootstrap={script_matches}"
        )


# Core pages remain intentionally page-managed.
for filename in CORE:

    html = (
        ROOT / filename
    ).read_text(errors="replace")

    if (
        'data-s90g-nav-managed="page"'
        not in html
    ):
        errors.append(
            f"{filename}: core page lost page-managed nav"
        )


if errors:

    print("INDEXED PUBLIC SHELL V1: FAIL")

    for error in errors[:120]:
        print("FAIL —", error)

    if len(errors) > 120:
        print(
            f"FAIL — plus {len(errors) - 120} more"
        )

    sys.exit(1)

print("PASS — 70 indexed shared pages use canonical descriptor")
print("PASS — 70 indexed shared pages use canonical static navigation")
print("PASS — 70 indexed shared pages carry canonical header CTA")
print("PASS — 70 indexed shared pages use canonical static footer")
print("PASS — retired shell identity absent from indexed shared source")
print("PASS — shared pages remain runtime-managed")
print("PASS — privacy bootstrap version normalized")
print("PASS — six core pages remain page-managed")
print("INDEXED PUBLIC SHELL V1: PASS")
