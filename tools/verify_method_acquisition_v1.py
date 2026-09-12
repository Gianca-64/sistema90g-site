#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

html_path = ROOT / "metodo-sistema90g.html"
css_path = ROOT / "s90g-method-acquisition-v1.css"

errors = []

for path in (html_path, css_path):
    if not path.exists():
        errors.append(
            f"missing file: {path.name}"
        )

if errors:
    for error in errors:
        print("FAIL —", error)
    sys.exit(1)

html = html_path.read_text()
css = css_path.read_text()

required = [
    "Metodo Sistema 90G",
    "Prima va capito.",
    "Il servizio viene dopo",
    "OBSERVARE",  # checked below with actual Italian marker
]

# use explicit actual markers
required = [
    "Metodo Sistema 90G",
    "Prima va capito.",
    "Il servizio viene dopo",
    "OSSERVARE",
    "RACCOGLIERE",
    "DISTINGUERE",
    "VERIFICARE",
    "VALUTARE",
    "INDICARE IL PASSO",
    "VERIFICATO",
    "DA VERIFICARE",
    "NON DETERMINABILE",
    "La tecnologia aiuta.",
    "La revisione e la valutazione finale",
    "Dichiarare un limite",
    "Mostra gratuitamente il tuo caso",
    'data-s90g-nav-managed="page"',
    "VEDERE IL PROBLEMA PRIMA",
]

for marker in required:
    if marker not in html:
        errors.append(
            f"method marker missing: {marker}"
        )

class VisibleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.h1 = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip += 1
            return

        if tag == "h1":
            self.h1 += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if self.skip:
            return

        value = " ".join(data.split())

        if value:
            self.text.append(value)

parser = VisibleParser()
parser.feed(html)

visible = " ".join(parser.text)

if parser.h1 != 1:
    errors.append(
        f"method page must have exactly one H1, found {parser.h1}"
    )

for forbidden in (
    r"PROGETTAZIONE INDIPENDENTE CUCINE",
    r"ANALISI INDIPENDENTE CUCINE",
    r"Metodo e AI",
):
    if re.search(forbidden, visible, re.I):
        errors.append(
            f"retired visible method identity: {forbidden}"
        )

# Innovations must not remain a primary Method navigation dependency.
nav_match = re.search(
    r'<nav\b[^>]*class=["\'][^"\']*\bs90g-nav\b[^"\']*["\'][^>]*>'
    r'([\s\S]*?)</nav>',
    html,
    re.I
)

if not nav_match:
    errors.append(
        "method acquisition navigation not parseable"
    )
else:
    nav = nav_match.group(1)

    if "innovazioni.html" in nav:
        errors.append(
            "Innovazioni remains in primary Method navigation"
        )

jsonld_blocks = re.findall(
    r'<script[^>]+type="application/ld\+json"[^>]*>'
    r'(.*?)</script>',
    html,
    re.I | re.S
)

if len(jsonld_blocks) != 1:
    errors.append(
        f"expected 1 JSON-LD block, found {len(jsonld_blocks)}"
    )
else:
    try:
        data = json.loads(jsonld_blocks[0])

        if data.get("name") != "Metodo Sistema 90G":
            errors.append(
                "Method JSON-LD still uses old identity"
            )

    except Exception as exc:
        errors.append(
            f"invalid Method JSON-LD: {exc}"
        )

if "prefers-reduced-motion" not in css:
    errors.append(
        "method reduced-motion support missing"
    )

if ":focus-visible" not in css:
    errors.append(
        "method focus-visible support missing"
    )

if errors:
    print("METHOD ACQUISITION V1: FAIL")

    for error in errors:
        print("FAIL —", error)

    sys.exit(1)

print("PASS — Method starts from the doubt, not the tool")
print("PASS — six verification steps are explicit")
print("PASS — facts / uncertainty / missing-data states are explicit")
print("PASS — technology remains subordinate")
print("PASS — human evaluation remains final")
print("PASS — professional boundaries remain explicit")
print("PASS — Innovazioni removed from primary Method navigation")
print("PASS — structured Method identity aligned")
print("PASS — accessibility contracts present")
print("METHOD ACQUISITION V1: PASS")
