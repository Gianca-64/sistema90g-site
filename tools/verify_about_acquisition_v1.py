#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

html_path = ROOT / "chi-e-sistema90g.html"
css_path = ROOT / "s90g-about-acquisition-v1.css"

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
    "Sono Gian Carlo Primo.",
    "Il mio lavoro è capire",
    "progettazione, vendita, montaggio",
    "post-vendita",
    "Non vendo la cucina",
    "non rappresenta marchi",
    "non riceve provvigioni",
    "La tecnologia supporta.",
    "La revisione e la valutazione finale",
    "Limiti chiari",
    "Mostra il tuo caso",
    'data-s90g-nav-managed="page"',
    "VEDERE IL PROBLEMA PRIMA",
]

for marker in required:
    if marker not in html:
        errors.append(
            f"about acquisition marker missing: {marker}"
        )

stages = [
    "Progettazione",
    "Vendita",
    "Montaggio",
    "Post-vendita",
]

for stage in stages:
    if stage not in html:
        errors.append(
            f"experience stage missing: {stage}"
        )

nav_required = [
    "Problemi da evitare",
    "Casi reali",
    "Guide",
    "Come funziona",
    "Servizi e prezzi",
    "Chi sono",
]

for marker in nav_required:
    if marker not in html:
        errors.append(
            f"about navigation marker missing: {marker}"
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
        f"about page must have exactly one H1, found {parser.h1}"
    )

for forbidden in (
    r"PROGETTAZIONE INDIPENDENTE CUCINE",
    r"ANALISI INDIPENDENTE CUCINE",
    r"\bprivato\b",
    r"\bprivati\b",
    r"\butente\b",
    r"\butenti\b",
    r"\brichiedente\b",
    r"\brichiedenti\b",
):
    if re.search(forbidden, visible, re.I):
        errors.append(
            f"retired visible about language: {forbidden}"
        )

# AI must be subordinate, not a primary navigation or headline theme.
if "Metodo e AI" in visible:
    errors.append(
        "AI remains over-prominent in visible about-page navigation/content"
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
        graph = data.get("@graph", [])

        persons = [
            item for item in graph
            if item.get("@type") == "Person"
        ]

        orgs = [
            item for item in graph
            if item.get("@type") == "Organization"
        ]

        if len(persons) != 1:
            errors.append(
                "Person JSON-LD missing or duplicated"
            )

        if len(orgs) != 1:
            errors.append(
                "Organization JSON-LD missing or duplicated"
            )

        if persons:
            if persons[0].get("name") != "Gian Carlo Primo":
                errors.append(
                    "Person JSON-LD name changed"
                )

            if persons[0].get("jobTitle") != "Fondatore di Sistema 90G":
                errors.append(
                    "Person JSON-LD jobTitle not aligned"
                )

    except Exception as exc:
        errors.append(
            f"invalid about JSON-LD: {exc}"
        )

if "prefers-reduced-motion" not in css:
    errors.append(
        "about reduced-motion support missing"
    )

if ":focus-visible" not in css:
    errors.append(
        "about focus-visible support missing"
    )

if errors:
    print("ABOUT ACQUISITION V1: FAIL")

    for error in errors:
        print("FAIL —", error)

    sys.exit(1)

print("PASS — Chi sono starts from person and responsibility")
print("PASS — four experience stages preserved")
print("PASS — commercial independence explicit")
print("PASS — AI is subordinate to human evaluation")
print("PASS — professional limits remain explicit")
print("PASS — trust is supported by cases and public journey")
print("PASS — acquisition navigation aligned")
print("PASS — structured Person/Organization data aligned")
print("PASS — accessibility contracts present")
print("ABOUT ACQUISITION V1: PASS")
