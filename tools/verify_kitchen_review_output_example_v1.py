#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

IT_SERVICE = ROOT / "verifica-90g.html"
EN_SERVICE = ROOT / "en" / "kitchen-review.html"
IT_EXAMPLE = ROOT / "esempio-verifica-cucina-90g.html"
EN_EXAMPLE = ROOT / "en" / "kitchen-review-example.html"
SITEMAP = ROOT / "sitemap.xml"

errors = []

for path in (
    IT_SERVICE,
    EN_SERVICE,
    IT_EXAMPLE,
    EN_EXAMPLE,
    SITEMAP,
):
    if not path.is_file():
        errors.append(
            f"missing P1-D file: {path.relative_to(ROOT)}"
        )

if errors:
    for error in errors:
        print("FAIL —", error)
    sys.exit(1)

it_service = IT_SERVICE.read_text(encoding="utf-8")
en_service = EN_SERVICE.read_text(encoding="utf-8")
it = IT_EXAMPLE.read_text(encoding="utf-8")
en = EN_EXAMPLE.read_text(encoding="utf-8")
sitemap = SITEMAP.read_text(encoding="utf-8")


def require(condition, message):
    if not condition:
        errors.append(message)


for marker in (
    "Questo esempio è illustrativo e non rappresenta un caso reale.",
    "Non garantisce che una verifica trovi un errore",
    "VERIFICATO",
    "DA VERIFICARE",
    "NON DETERMINABILE",
    'data-evidence-state="verified"',
    'data-evidence-state="to-check"',
    'data-evidence-state="not-determinable"',
    "criticità individuate",
    "conseguenze possibili",
    "elementi coerenti",
    "dati mancanti",
    "Passo successivo",
    "non comprende una riprogettazione",
    "Non è una certificazione",
    "149 €",
    "Entro 2 giorni lavorativi",
):
    require(
        marker in it,
        f"Italian review example missing: {marker}",
    )

for marker in (
    "This is an illustrative example and does not represent a real client case.",
    "It does not guarantee that a review will find an error",
    "VERIFIED",
    "TO CHECK",
    "NOT DETERMINABLE",
    'data-evidence-state="verified"',
    'data-evidence-state="to-check"',
    'data-evidence-state="not-determinable"',
    "identified critical issues",
    "possible consequences",
    "consistent elements",
    "missing information",
    "Next step",
    "does not include redesign",
    "It is not a certification",
    "€149",
    "Within 2 working days",
):
    require(
        marker in en,
        f"English review example missing: {marker}",
    )

require(
    it.count('data-evidence-state=') == 3,
    "Italian example must expose exactly three evidence states",
)

require(
    en.count('data-evidence-state=') == 3,
    "English example must expose exactly three evidence states",
)

for state in (
    "verified",
    "to-check",
    "not-determinable",
):
    require(
        it.count(
            f'data-evidence-state="{state}"'
        ) == 1,
        f"Italian state must exist exactly once: {state}",
    )

    require(
        en.count(
            f'data-evidence-state="{state}"'
        ) == 1,
        f"English state must exist exactly once: {state}",
    )

require(
    'href="/esempio-verifica-cucina-90g.html"'
    in it_service,
    "Italian service does not link to review example",
)

require(
    'href="/en/kitchen-review-example.html"'
    in en_service,
    "English service does not link to review example",
)

require(
    'href="/verifica-90g.html"'
    in it,
    "Italian example does not link back to service",
)

require(
    'href="/en/kitchen-review.html"'
    in en,
    "English example does not link back to service",
)

for marker in (
    "Verifica Cucina 90G · 149 €",
    "entro 2 giorni lavorativi",
):
    require(
        marker in it_service,
        f"Italian service fact changed: {marker}",
    )

for marker in (
    "90G Kitchen Review · €149",
    "within 2 working days",
):
    require(
        marker in en_service,
        f"English service fact changed: {marker}",
    )

it_canonical = (
    '<link\n'
    '    rel="canonical"\n'
    '    href="https://sistema90g.it/esempio-verifica-cucina-90g.html">'
)

en_canonical = (
    '<link\n'
    '    rel="canonical"\n'
    '    href="https://sistema90g.it/en/kitchen-review-example.html">'
)

require(
    it_canonical in it,
    "Italian example canonical incorrect",
)

require(
    en_canonical in en,
    "English example canonical incorrect",
)

for text, label in (
    (it, "Italian"),
    (en, "English"),
):
    for marker in (
        'hreflang="it-IT"',
        'hreflang="en-GB"',
        'hreflang="x-default"',
    ):
        require(
            marker in text,
            f"{label} example missing {marker}",
        )

require(
    "https://sistema90g.it/esempio-verifica-cucina-90g.html"
    in sitemap,
    "Italian review example missing from sitemap",
)

require(
    "https://sistema90g.it/en/kitchen-review-example.html"
    not in sitemap,
    "P1-D must not introduce a lone EN URL into the current Italian-only sitemap",
)


class H1Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "h1":
            self.h1 += 1


for text, label in (
    (it, "Italian"),
    (en, "English"),
):
    parser = H1Parser()
    parser.feed(text)

    require(
        parser.h1 == 1,
        f"{label} example must have exactly one H1",
    )


script_re = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>'
    r'(.*?)</script>',
    re.I | re.S,
)

for text, label in (
    (it, "Italian"),
    (en, "English"),
):
    scripts = script_re.findall(text)

    require(
        len(scripts) == 1,
        f"{label} example must expose exactly one JSON-LD block",
    )

    if len(scripts) == 1:
        try:
            json.loads(scripts[0])
        except json.JSONDecodeError:
            errors.append(
                f"{label} example JSON-LD invalid"
            )


for forbidden, label in (
    (
        r"\btestimonianza\b|\btestimonial\b",
        "invented testimonial language",
    ),
    (
        r"risparmio garantito|guaranteed saving",
        "unsupported saving claim",
    ),
    (
        r"troviamo sempre un errore|always find an error",
        "guaranteed error discovery",
    ),
):
    require(
        not re.search(
            forbidden,
            it + "\n" + en,
            re.I,
        ),
        label,
    )


if errors:
    print("KITCHEN REVIEW OUTPUT EXAMPLE V1: FAIL")

    for error in errors:
        print("FAIL —", error)

    sys.exit(1)


print("PASS — Italian illustrative review example present")
print("PASS — English illustrative review example present")
print("PASS — explicit non-real-case disclosure")
print("PASS — exact three certainty states IT + EN")
print("PASS — critical / consequence / missing-data / next-step logic")
print("PASS — service <-> example links IT + EN")
print("PASS — canonical service price and delivery preserved")
print("PASS — no redesign or certification promise")
print("PASS — canonical + hreflang pairing")
print("PASS — Italian sitemap strategy preserved")
print("PASS — no unsupported testimonial/saving/error guarantee")
print("KITCHEN REVIEW OUTPUT EXAMPLE V1: PASS")
