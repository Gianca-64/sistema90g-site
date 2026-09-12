#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

services_path = ROOT / "servizi.html"
detail_path = ROOT / "progetto-preventivo-cucina-90g.html"
css_path = ROOT / "s90g-services-acquisition-v1.css"

errors = []

for path in (services_path, detail_path, css_path):
    if not path.exists():
        errors.append(f"missing file: {path.name}")

if errors:
    for error in errors:
        print("FAIL —", error)
    sys.exit(1)

html = services_path.read_text()
detail = detail_path.read_text()
css = css_path.read_text()

required = [
    "Non partire dal servizio.",
    "Parti da dove sei.",
    "Sei momenti. Sei problemi diversi.",
    "Non devi scegliere il servizio da solo.",
    "Mostra gratuitamente il tuo caso",
    'data-s90g-nav-managed="page"',
    "VEDERE IL PROBLEMA PRIMA",
]

for marker in required:
    if marker not in html:
        errors.append(
            f"services acquisition marker missing: {marker}"
        )

services = [
    ("Consulenza 90G", "79 €", "1 giorno lavorativo"),
    (
        "Analisi Preventivo &amp; Ordine 90G",
        "129 €",
        "2 giorni lavorativi",
    ),
    (
        "Verifica Cucina 90G",
        "149 €",
        "2 giorni lavorativi",
    ),
    (
        "Progetto Cucina 90G",
        "299 €",
        "3 giorni lavorativi",
    ),
    (
        "Controllo Pre-Montaggio 90G",
        "179 €",
        "2 giorni lavorativi",
    ),
    (
        "Analisi Problema 90G",
        "149 €",
        "2 giorni lavorativi",
    ),
]

for name, price, time in services:
    for marker in (name, price, time):
        if marker not in html:
            errors.append(
                f"canonical service fact missing: {marker}"
            )

extension_markers = [
    "Progetto &amp; Preventivo 90G",
    "349 €",
    "Tempo Sistema 90G:",
    "tempi del rivenditore",
    "Solo dopo la tua approvazione esplicita",
    "Il pagamento del servizio",
    "non costituisce autorizzazione all'invio",
    "identificare univocamente la richiesta",
    "NESSUN DATO SENSIBILE",
    "I dati sensibili non vengono trasmessi",
    "riferimento di pratica",
    "estranei alla richiesta commerciale",
]

for marker in extension_markers:
    if marker not in html:
        errors.append(
            f"services extension contract missing: {marker}"
        )

detail_markers = [
    "La richiesta parte solo dopo la tua approvazione.",
    "approvazione esplicita",
    "autorizzazione alla trasmissione",
    "Il pagamento del servizio non costituisce",
    "identificare",
    "univocamente la richiesta",
    "riferimento di pratica",
    "Non vengono trasmessi dati sensibili",
    "Non vengono trasmessi dati sensibili",
    "I tempi necessari al rivenditore",
    "non sono controllati da Sistema 90G",
]

for marker in detail_markers:
    if marker not in detail:
        errors.append(
            f"detail approval/privacy contract missing: {marker}"
        )

ids = re.findall(
    r'<article[^>]+class="s90g-svc-route"[^>]+id="([^"]+)"',
    html,
    re.I
)

expected_ids = [
    "scelta",
    "preventivo",
    "verifica",
    "progetto",
    "premontaggio",
    "problema",
]

if ids != expected_ids:
    errors.append(
        f"service journey ids/order incorrect: {ids}"
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
        f"services page must have exactly one H1, found {parser.h1}"
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
            f"retired visible services language: {forbidden}"
        )

if "prefers-reduced-motion" not in css:
    errors.append(
        "services reduced-motion support missing"
    )

if ":focus-visible" not in css:
    errors.append(
        "services focus-visible support missing"
    )

if errors:
    print("SERVICES ACQUISITION V1: FAIL")

    for error in errors:
        print("FAIL —", error)

    sys.exit(1)

print("PASS — services start from customer situations")
print("PASS — six canonical service routes present")
print("PASS — canonical prices preserved")
print("PASS — canonical delivery times preserved")
print("PASS — Project & Preventivo remains an extension")
print("PASS — retailer timing is separated from Sistema 90G timing")
print("PASS — retailer send requires explicit customer approval")
print("PASS — payment is not treated as send authorization")
print("PASS — retailer data minimization is explicit")
print("PASS — Free Entry remains the default when uncertain")
print("PASS — public language is customer-direct")
print("PASS — accessibility contracts present")
print("SERVICES ACQUISITION V1: PASS")
