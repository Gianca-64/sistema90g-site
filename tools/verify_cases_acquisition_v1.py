#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

html_path = ROOT / "casi-analizzati.html"
css_path = ROOT / "s90g-cases-acquisition-v1.css"

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
    "Casi 90G · problemi reali",
    "Sembrava tutto a posto.",
    "Poi abbiamo guardato cosa succede davvero.",
    "Un Caso 90G non mostra",
    "Sei casi. Sei cose facili da non vedere.",
    "Mostriamo il ragionamento.",
    "Non esponiamo il cliente.",
    'data-s90g-nav-managed="page"',
    "VEDERE IL PROBLEMA PRIMA",
]

for marker in required:
    if marker not in html:
        errors.append(
            f"cases acquisition marker missing: {marker}"
        )

cases = [
    (
        "caso-01",
        "caso-lavastoviglie-passaggio-cucina.html",
        "La cucina sembra comoda.",
    ),
    (
        "caso-02",
        "caso-isola-passaggi-cucina.html",
        "L'isola entra nelle misure.",
    ),
    (
        "caso-03",
        "caso-lavello-sotto-finestra-aperture.html",
        "Il lavello sotto finestra funziona.",
    ),
    (
        "caso-04",
        "caso-cucina-piccola-tre-lati.html",
        "Più mobili su tre lati",
    ),
    (
        "caso-05",
        "caso-cucina-profondita-75-angolo.html",
        "Più profondità può dare più volume.",
    ),
    (
        "caso-06",
        "caso-preventivo-cucina-sconto-valore.html",
        "Lo sconto è evidente.",
    ),
]

for case_id, href, proof in cases:
    for marker in (
        f'id="{case_id}"',
        href,
        proof,
    ):
        if marker not in html:
            errors.append(
                f"canonical case marker missing: {marker}"
            )

if html.count("SEMBRAVA") != 6:
    errors.append(
        f"expected 6 SEMBRAVA markers, found {html.count('SEMBRAVA')}"
    )

if html.count("IL PUNTO") != 6:
    errors.append(
        f"expected 6 IL PUNTO markers, found {html.count('IL PUNTO')}"
    )

if html.count("DA VERIFICARE") != 6:
    errors.append(
        "expected 6 DA VERIFICARE markers, "
        f"found {html.count('DA VERIFICARE')}"
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
        f"cases page must have exactly one H1, found {parser.h1}"
    )

for forbidden in (
    r"ANALISI INDIPENDENTE CUCINE",
    r"PROGETTAZIONE INDIPENDENTE CUCINE",
    r"\bprivato\b",
    r"\bprivati\b",
    r"\butente\b",
    r"\butenti\b",
    r"\brichiedente\b",
    r"\brichiedenti\b",
):
    if re.search(forbidden, visible, re.I):
        errors.append(
            f"retired visible cases language: {forbidden}"
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
            f"cases navigation marker missing: {marker}"
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

        item_lists = [
            item
            for item in graph
            if item.get("@type") == "ItemList"
        ]

        if len(item_lists) != 1:
            errors.append(
                "canonical cases ItemList missing"
            )
        else:
            items = item_lists[0].get(
                "itemListElement",
                []
            )

            if len(items) != 6:
                errors.append(
                    f"expected 6 JSON-LD cases, found {len(items)}"
                )

    except Exception as exc:
        errors.append(
            f"invalid cases JSON-LD: {exc}"
        )

if "prefers-reduced-motion" not in css:
    errors.append(
        "cases reduced-motion support missing"
    )

if ":focus-visible" not in css:
    errors.append(
        "cases focus-visible support missing"
    )

if errors:
    print("CASES ACQUISITION V1: FAIL")

    for error in errors:
        print("FAIL —", error)

    sys.exit(1)

print("PASS — Casi 90G are presented as proof, not archive")
print("PASS — six canonical kitchen cases preserved")
print("PASS — each case exposes seemed / point / verify logic")
print("PASS — cases remain anonymous")
print("PASS — acquisition navigation aligned")
print("PASS — customer-direct public language")
print("PASS — structured data preserves six-case collection")
print("PASS — accessibility contracts present")
print("CASES ACQUISITION V1: PASS")
