#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

html_path = ROOT / "index.html"
en_html_path = ROOT / "en" / "index.html"
en_method_path = ROOT / "en" / "method.html"
css_path = ROOT / "s90g-home-acquisition-v1.css"
js_path = ROOT / "s90g-home-acquisition-v1.js"

errors = []

for path in (
    html_path,
    en_html_path,
    en_method_path,
    css_path,
    js_path,
):
    if not path.exists():
        errors.append(f"missing file: {path.name}")

if errors:
    for error in errors:
        print("FAIL —", error)
    sys.exit(1)

html = html_path.read_text()
en_html = en_html_path.read_text()
en_method = en_method_path.read_text()
css = css_path.read_text()
js = js_path.read_text()

required_html = [
    "La cucina può sembrare perfetta.",
    "Finché non inizi a usarla.",
    "Vista 90G",
    "Qual è il problema che stai cercando di risolvere?",
    "Sembrava tutto corretto.",
    "Non dobbiamo venderti una cucina.",
    "9 domande che farei sulla tua cucina.",
    "Mostra gratuitamente il tuo caso",
    'href="s90g-home-acquisition-v1.css?v=',
    'src="s90g-home-acquisition-v1.js?v=',
    'data-s90g-nav-managed="page"',
    'TAVOLA 90G · USO REALE',
    'Una risposta utile deve dire',
    'quanto è certa.',
    'VERIFICATO',
    'DA VERIFICARE',
    'NON DETERMINABILE',
    'data-evidence-state="verified"',
    'data-evidence-state="to-check"',
    'data-evidence-state="not-determinable"',
    'href="/metodo-sistema90g.html"',
    'href="/esempio-verifica-cucina-90g.html"',
]

for marker in required_html:
    if marker not in html:
        errors.append(f"missing homepage marker: {marker}")

for marker in (
    "VERIFIED",
    "TO CHECK",
    "NOT DETERMINABLE",
    'href="/en/method.html"',
    'href="/en/kitchen-review-example.html"',
):
    if marker not in en_html:
        errors.append(
            f"English P1 Home alignment missing: {marker}"
        )

for marker in (
    "VERIFIED",
    "TO CHECK",
    "NOT DETERMINABLE",
):
    if marker not in en_method:
        errors.append(
            f"English P1 Method certainty state missing: {marker}"
        )

if "TO BE VERIFIED" in en_method:
    errors.append(
        "retired English certainty label remains: TO BE VERIFIED"
    )

if "“to be verified”" in en_method:
    errors.append(
        "retired English certainty wording remains in Method example"
    )

if en_method.count("TO CHECK") != 2:
    errors.append(
        "English Method must expose canonical TO CHECK exactly twice "
        "(state label + explanatory example)"
    )

for forbidden in (
    r"\bprivato\b",
    r"\bprivati\b",
    r"\brichiedente\b",
    r"\brichiedenti\b",
    r"PROGETTAZIONE INDIPENDENTE CUCINE",
):
    if re.search(forbidden, html, re.I):
        errors.append(
            f"forbidden public-home language: {forbidden}"
        )

if len(re.findall(r"data-vista-hotspot", html)) != 4:
    errors.append("Vista 90G must expose exactly 4 hotspots")

if len(re.findall(r"data-problem=", html)) != 6:
    errors.append("homepage must expose exactly 6 problem routes")

if len(re.findall(r"data-evidence-state=", html)) != 3:
    errors.append(
        "homepage must expose exactly 3 evidence states"
    )

for evidence_state in (
    "verified",
    "to-check",
    "not-determinable",
):
    if html.count(
        f'data-evidence-state="{evidence_state}"'
    ) != 1:
        errors.append(
            f"homepage evidence state must exist exactly once: {evidence_state}"
        )

if len(re.findall(r"data-checklist-item", html)) != 9:
    errors.append("homepage checklist must contain 9 questions")

if "prefers-reduced-motion" not in css:
    errors.append("reduced-motion support missing")

if ":focus-visible" not in css:
    errors.append("focus-visible styling missing")

for event in (
    "vista90g_open",
    "vista90g_hotspot",
    "problem_selected",
    "free_entry_click",
):
    if event not in js:
        errors.append(f"analytics event missing: {event}")

if re.search(r"\bon(?:click|load|change)\s*=", html, re.I):
    errors.append("inline event handler found")

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.main = 0
        self.buttons = 0

    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            self.h1 += 1
        elif tag == "main":
            self.main += 1
        elif tag == "button":
            self.buttons += 1

parser = Parser()
parser.feed(html)

if parser.h1 != 1:
    errors.append(
        f"homepage must have exactly one H1, found {parser.h1}"
    )

if parser.main != 1:
    errors.append(
        f"homepage must have exactly one main, found {parser.main}"
    )

if parser.buttons < 5:
    errors.append(
        "expected Vista toggle + hotspot buttons"
    )

if errors:
    print("HOME ACQUISITION V1: FAIL")
    for error in errors:
        print("FAIL —", error)
    sys.exit(1)

print("PASS — memorable customer-first hero present")
print("PASS — Vista 90G structure present")
print("PASS — three evidence-certainty states visible")
print("PASS — direct illustrative proof link visible IT + EN")
print("PASS — canonical EN certainty vocabulary aligned")
print("PASS — six problem-first entry routes present")
print("PASS — three proof cases integrated")
print("PASS — independence positioning present")
print("PASS — nine-question shareable checklist present")
print("PASS — public home language is customer-direct")
print("PASS — focus and reduced-motion contracts present")
print("PASS — acquisition analytics hooks present")
# A3-R3 — Vista 90G reveal contract
for marker in (
    "02_HOME_SCENA_PULITA.jpg",
    "data-vista-90g-clean-src=",
    "data-vista-90g-analysed-src=",
):
    if marker not in html:
        errors.append(
            f"Vista 90G reveal HTML marker missing: {marker}"
        )

for marker in (
    "initVista90GReveal",
    "Lettura 90G attiva",
    "[data-vista-hotspot]",
):
    if marker not in js:
        errors.append(
            f"Vista 90G runtime marker missing: {marker}"
        )

for marker in (
    'class="s90g-vista-clean-layer"',
    'class="s90g-vista-analysed-layer"',
):
    if marker not in html:
        errors.append(
            f"Vista 90G visual layer missing: {marker}"
        )

if len(re.findall(r"\bdata-vista-hotspot\b", html)) != 4:
    errors.append(
        "Vista 90G must expose exactly four canonical hotspots"
    )

if "A3-R3.3 — CANONICAL VISTA 90G REVEAL" not in css:
    errors.append(
        "canonical Vista 90G reveal CSS missing"
    )

if js.count("function initVista90GReveal") != 1:
    errors.append(
        "Vista 90G reveal runtime must exist exactly once"
    )

if errors:
    print("HOME ACQUISITION V1: FAIL")
    for error in errors:
        print("FAIL —", error)
    sys.exit(1)

# A3-R3.1 — Vista activation ownership
for marker in (
    "event.stopImmediatePropagation()",
    "activating Vista 90G must never move the viewport",
):
    if marker not in js:
        print(
            "HOME ACQUISITION V1: FAIL"
        )
        print(
            f"FAIL — Vista activation ownership missing: {marker}"
        )
        sys.exit(1)

# A3-R4 — canonical hotspot semantics
for marker in (
    'data-vista-id="colonna-forno"',
    'data-vista-id="passaggio-isola"',
    'data-vista-id="interferenze-uso"',
    'data-vista-id="planimetria-uso"',
    'data-title="Colonna forno e quote"',
    'data-title="Passaggio intorno all’isola"',
    'data-title="Interferenze nell’uso reale"',
    'data-title="Planimetria e spazio vissuto"',
):
    if marker not in html:
        errors.append(
            f"canonical Vista hotspot missing: {marker}"
        )

if errors:
    print("HOME ACQUISITION V1: FAIL")
    for error in errors:
        print("FAIL —", error)
    sys.exit(1)

print("HOME ACQUISITION V1: PASS")
