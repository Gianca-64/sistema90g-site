from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

IT_PATH = (
    ROOT
    / "esempio-progetto-cucina-90g.html"
)

EN_PATH = (
    ROOT
    / "en"
    / "kitchen-design-example.html"
)

DESIGN_PATH = (
    ROOT
    / "en"
    / "kitchen-design.html"
)

def require(
    condition,
    message,
):
    if not condition:
        raise SystemExit(
            f"FAIL — {message}"
        )

def collapse_ws(value):
    return " ".join(
        value.split()
    )

require(
    IT_PATH.exists(),
    "Italian design example missing",
)

require(
    EN_PATH.exists(),
    "English design example missing",
)

it = IT_PATH.read_text(
    encoding="utf-8",
)

en = EN_PATH.read_text(
    encoding="utf-8",
)

design = DESIGN_PATH.read_text(
    encoding="utf-8",
)

require(
    '<html lang="en-GB">'
    in en,
    "en-GB lang missing",
)

require(
    'rel="canonical"'
    in en
    and (
        "https://sistema90g.it/"
        "en/kitchen-design-example.html"
    )
    in en,
    "English self canonical missing",
)

for lang in [
    "it-IT",
    "en-GB",
    "x-default",
]:
    require(
        f'hreflang="{lang}"'
        in en,
        f"English hreflang missing: {lang}",
    )

    require(
        f'hreflang="{lang}"'
        in it,
        f"Italian hreflang missing: {lang}",
    )

require(
    'href="/en/kitchen-design-example.html"'
    in it,
    "Italian EN switch missing",
)

require(
    'href="/esempio-progetto-cucina-90g.html"'
    in en,
    "English IT switch missing",
)

required_meaning = [
    "This is an illustrative example, not a real customer project",
    "it does not promise a fixed number of drawings",
    "Three levels of information",
    "This is not the retailer's execution-ready design",
    "does not certify measurements",
    "€299 EUR",
]

collapsed = collapse_ws(en)

for phrase in required_meaning:
    require(
        collapse_ws(phrase)
        in collapsed,
        f"illustrative boundary missing: {phrase}",
    )

require(
    '/en/kitchen-design.html'
    in en,
    "design service route missing",
)

require(
    '/en/how-it-works.html#submit'
    in en,
    "Free Entry route missing",
)

require(
    "portale.sistema90g.it"
    not in en,
    "direct Portal bypass",
)

require(
    "privacy-consent.js"
    not in en,
    "Italian runtime loaded",
)

require(
    "navigation-conversion.js"
    not in en,
    "Italian navigation runtime loaded",
)

require(
    "/s90g-site-en-gb-v1.js"
    in en,
    "English runtime missing",
)

for forbidden in [
    "€39",
    "39 €",
    "€349",
    "349 €",
    "Project & Quote",
    "progetto-preventivo-cucina-90g",
    "GBP",
    "£",
]:
    require(
        forbidden not in en,
        f"forbidden commercial extension/currency: {forbidden}",
    )

for us_term in [
    "countertop",
    "cooktop",
    "wall cabinet",
    "faucet",
    "range hood",
    "toe-kick",
]:
    require(
        us_term.lower()
        not in en.lower(),
        f"US terminology leaked: {us_term}",
    )

for uk_term in [
    "worktop",
    "hob",
]:
    require(
        uk_term.lower()
        in en.lower(),
        f"expected UK terminology missing: {uk_term}",
    )

for italian_marker in [
    "Esempio illustrativo",
    "Cosa non devi aspettarti",
    "Vedi il servizio",
    "Chiedi la valutazione gratuita",
    "Partita IVA",
]:
    require(
        italian_marker
        not in en,
        f"Italian visible copy remains: {italian_marker}",
    )

require(
    'src="images/'
    not in en,
    "non-root-relative image",
)

require(
    'href="sistema90g-'
    not in en
    and 'href="s90g-'
    not in en,
    "non-root-relative stylesheet",
)

schema_blocks = re.findall(
    r'<script\s+type="application/ld\+json">(.*?)</script>',
    en,
    re.I | re.S,
)

require(
    len(schema_blocks) == 1,
    "expected one JSON-LD block",
)

schema = json.loads(
    schema_blocks[0],
)

require(
    schema.get("@type")
    == "CreativeWork",
    "schema type",
)

require(
    schema.get("inLanguage")
    == "en-GB",
    "schema language",
)

require(
    schema.get("url")
    == (
        "https://sistema90g.it/"
        "en/kitchen-design-example.html"
    ),
    "schema URL",
)

about = schema.get(
    "about",
    {},
)

require(
    about.get("@type")
    == "Service",
    "schema about type",
)

require(
    about.get("name")
    == "90G Kitchen Design",
    "schema about service",
)

require(
    about.get("url")
    == (
        "https://sistema90g.it/"
        "en/kitchen-design.html"
    ),
    "schema about URL",
)

require(
    '/en/kitchen-design-example.html'
    in design,
    "design detail page no longer links example",
)

print(
    "PASS — en-GB design example lang + canonical"
)

print(
    "PASS — reciprocal Italian / en-GB pair"
)

print(
    "PASS — illustrative-not-real boundary"
)

print(
    "PASS — no fixed drawing-count promise"
)

print(
    "PASS — non-executive retailer boundary"
)

print(
    "PASS — canonical €299 EUR service only"
)

print(
    "PASS — no render or Project & Quote extension"
)

print(
    "PASS — design service route"
)

print(
    "PASS — Free Entry website-first route"
)

print(
    "PASS — no direct Portal bypass"
)

print(
    "PASS — UK terminology"
)

print(
    "PASS — English safe runtime only"
)

print(
    "PASS — CreativeWork structured data"
)

print(
    "PASS — existing design page links real example target"
)

print(
    "SITE I18N DESIGN EXAMPLE V1: PASS"
)
