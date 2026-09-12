#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

html_path = ROOT / "analisi-preventiva.html"
css_path = ROOT / "s90g-free-entry-acquisition-v1.css"

errors = []

for path in (html_path, css_path):
    if not path.exists():
        errors.append(f"missing file: {path.name}")

if errors:
    for error in errors:
        print("FAIL —", error)
    sys.exit(1)

html = html_path.read_text()
css = css_path.read_text()

required = [
    "Mostraci cosa non ti convince.",
    "Partiamo da lì.",
    "Non devi scegliere un servizio",
    "Prima capiamo cosa sta succedendo.",
    "Parti dal materiale che hai già.",
    "Se non serve altro, te lo diciamo.",
    "Cosa non ti convince della tua cucina?",
    'data-s90g-nav-managed="page"',
    "VEDERE IL PROBLEMA PRIMA",
    "images/22_CASI_PREVENTIVO.jpg?v=20260912a",
    'src="privacy-consent.js?v=20260912a"',
]

for marker in required:
    if marker not in html:
        errors.append(
            f"required Free Entry marker missing: {marker}"
        )

portal_contract = [
    "requester_role=private",
    "service=valutazione-iniziale",
    "source_page=analisi-preventiva",
    "content_type=free_evaluation",
]

for marker in portal_contract:
    if marker not in html:
        errors.append(
            f"Portale compatibility marker missing: {marker}"
        )

for position in ("hero", "final"):
    if f"cta_position={position}" not in html:
        errors.append(
            f"Free Entry CTA position missing: {position}"
        )

class VisibleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.text = []
        self.h1 = 0
        self.nav_text = []

        self.in_nav = False
        self.nav_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip += 1
            return

        attrs = dict(attrs)

        if tag == "h1":
            self.h1 += 1

        if (
            tag == "nav"
            and "s90g-nav"
            in attrs.get("class", "").split()
        ):
            self.in_nav = True
            self.nav_depth = 1
            return

        if self.in_nav:
            self.nav_depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.skip:
            self.skip -= 1
            return

        if self.in_nav:
            self.nav_depth -= 1

            if self.nav_depth == 0:
                self.in_nav = False

    def handle_data(self, data):
        if self.skip:
            return

        value = " ".join(data.split())

        if not value:
            return

        self.text.append(value)

        if self.in_nav:
            self.nav_text.append(value)

parser = VisibleParser()
parser.feed(html)

visible = " ".join(parser.text)
nav = " ".join(parser.nav_text)

if parser.h1 != 1:
    errors.append(
        f"Free Entry must have exactly one H1, found {parser.h1}"
    )

for forbidden in (
    r"\bprivato\b",
    r"\bprivati\b",
    r"\butente\b",
    r"\butenti\b",
    r"\brichiedente\b",
    r"\brichiedenti\b",
    r"PROGETTAZIONE INDIPENDENTE CUCINE",
):
    if re.search(forbidden, visible, re.I):
        errors.append(
            f"forbidden visible Free Entry language: {forbidden}"
        )

required_nav = [
    "Problemi da evitare",
    "Casi reali",
    "Guide",
    "Come funziona",
    "Servizi e prezzi",
    "Chi sono",
]

for label in required_nav:
    if label not in nav:
        errors.append(
            f"Free Entry acquisition nav missing: {label}"
        )

for legacy in (
    "Metodo e AI",
    "Innovazioni",
    "Contatti",
):
    if legacy in nav:
        errors.append(
            f"legacy Free Entry nav item present: {legacy}"
        )

if "prefers-reduced-motion" not in css:
    errors.append("Free Entry reduced-motion support missing")

if ":focus-visible" not in css:
    errors.append("Free Entry focus-visible support missing")

if errors:
    print("FREE ENTRY ACQUISITION V1: FAIL")

    for error in errors:
        print("FAIL —", error)

    sys.exit(1)

print("PASS — customer problem is the Free Entry starting point")
print("PASS — no public role classification language")
print("PASS — service selection is not required")
print("PASS — technical Portale compatibility preserved")
print("PASS — acquisition navigation aligned with home")
print("PASS — independence and no-sale logic preserved")
print("PASS — accessibility contracts present")
print("FREE ENTRY ACQUISITION V1: PASS")
