from pathlib import Path
from urllib.parse import urlparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]

SERVICES = [
    {
        "it": "consulenza-90g.html",
        "en": "en/kitchen-consultation.html",
        "url": "/en/kitchen-consultation.html",
        "name": "90G Kitchen Consultation",
        "price": "79",
        "days": "1 working day",
        "id": "S90G-01",
    },
    {
        "it": "analisi-preventivo-cucina.html",
        "en": "en/kitchen-quote-order-review.html",
        "url": "/en/kitchen-quote-order-review.html",
        "name": "90G Quote & Order Review",
        "price": "129",
        "days": "2 working days",
        "id": "S90G-02",
    },
    {
        "it": "verifica-90g.html",
        "en": "en/kitchen-review.html",
        "url": "/en/kitchen-review.html",
        "name": "90G Kitchen Review",
        "price": "149",
        "days": "2 working days",
        "id": "S90G-03",
    },
    {
        "it": "progetto-cucina-sistema90g.html",
        "en": "en/kitchen-design.html",
        "url": "/en/kitchen-design.html",
        "name": "90G Kitchen Design",
        "price": "299",
        "days": "3 working days",
        "id": "S90G-04",
    },
    {
        "it": "controllo-pre-montaggio-cucina.html",
        "en": "en/pre-installation-check.html",
        "url": "/en/pre-installation-check.html",
        "name": "90G Pre-installation Check",
        "price": "179",
        "days": "2 working days",
        "id": "S90G-05",
    },
    {
        "it": "analisi-problema-cucina.html",
        "en": "en/kitchen-problem-analysis.html",
        "url": "/en/kitchen-problem-analysis.html",
        "name": "90G Kitchen Problem Analysis",
        "price": "149",
        "days": "2 working days",
        "id": "S90G-06",
    },
]

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

services_page = (
    ROOT
    / "en"
    / "services.html"
).read_text(
    encoding="utf-8",
)

for item in SERVICES:
    it = (
        ROOT
        / item["it"]
    ).read_text(
        encoding="utf-8",
    )

    en_path = (
        ROOT
        / item["en"]
    )

    require(
        en_path.exists(),
        f"English service page missing: {item['en']}",
    )

    en = en_path.read_text(
        encoding="utf-8",
    )

    require(
        '<html lang="en-GB">'
        in en,
        f"en-GB lang missing: {item['en']}",
    )

    expected_url = (
        "https://sistema90g.it"
        + item["url"]
    )

    require(
        f'href="{expected_url}"'
        in en,
        f"self canonical missing: {item['en']}",
    )

    for lang in [
        "it-IT",
        "en-GB",
        "x-default",
    ]:
        require(
            f'hreflang="{lang}"'
            in en,
            f"{lang} missing: {item['en']}",
        )

        require(
            f'hreflang="{lang}"'
            in it,
            f"Italian pair {lang} missing: {item['it']}",
        )

    require(
        f'href="{item["url"]}"'
        in it,
        f"Italian EN switch missing: {item['it']}",
    )

    require(
        item["name"]
        in en,
        f"service name missing: {item['en']}",
    )

    require(
        f'€{item["price"]}'
        in en,
        f"EUR price missing: {item['en']}",
    )

    require(
        item["days"]
        in en,
        f"delivery time missing: {item['en']}",
    )

    require(
        '/en/how-it-works.html#submit'
        in en,
        f"Free Entry route missing: {item['en']}",
    )

    require(
        "portale.sistema90g.it"
        not in en,
        f"direct Portal bypass: {item['en']}",
    )

    require(
        "privacy-consent.js"
        not in en,
        f"Italian runtime loaded: {item['en']}",
    )

    require(
        "navigation-conversion.js"
        not in en,
        f"Italian navigation runtime loaded: {item['en']}",
    )

    require(
        "/s90g-site-en-gb-v1.js"
        in en,
        f"English runtime missing: {item['en']}",
    )

    require(
        'src="images/'
        not in en,
        f"non-root-relative image: {item['en']}",
    )

    require(
        'href="s90g-'
        not in en
        and 'href="sistema90g-'
        not in en,
        f"non-root-relative stylesheet: {item['en']}",
    )

    require(
        "£" not in en
        and "GBP" not in en,
        f"GBP leaked into EUR V1: {item['en']}",
    )

    require(
        "€349" not in en
        and "349 €" not in en,
        f"unmapped Project & Quote leaked: {item['en']}",
    )

    require(
        "€39" not in en
        and "39 €" not in en,
        f"unmapped render add-on leaked: {item['en']}",
    )

    require(
        "progetto-preventivo-cucina-90g"
        not in en,
        f"unmapped Italian commercial extension leaked: {item['en']}",
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
            f"US terminology {us_term}: {item['en']}",
        )

    for italian_marker in [
        "Mostra gratuitamente",
        "Prima valutazione gratuita",
        "Cosa ricevi",
        "Cosa non comprende",
        "Tempi",
        "Prezzo",
        "Partita IVA",
    ]:
        require(
            italian_marker
            not in en,
            f"Italian copy remains ({italian_marker}): {item['en']}",
        )

    schema_blocks = re.findall(
        r'<script\s+type="application/ld\+json">(.*?)</script>',
        en,
        re.I | re.S,
    )

    require(
        len(schema_blocks) == 1,
        f"expected one schema block: {item['en']}",
    )

    schema = json.loads(
        schema_blocks[0],
    )

    require(
        schema.get("@type") == "Service",
        f"schema type: {item['en']}",
    )

    require(
        schema.get("name")
        == item["name"],
        f"schema service name: {item['en']}",
    )

    require(
        schema.get("identifier")
        == item["id"],
        f"schema identifier: {item['en']}",
    )

    require(
        schema.get("url")
        == expected_url,
        f"schema URL: {item['en']}",
    )

    require(
        schema.get("inLanguage")
        == "en-GB",
        f"schema language: {item['en']}",
    )

    offer = schema.get(
        "offers",
        {},
    )

    require(
        offer.get("price")
        == item["price"],
        f"schema price: {item['en']}",
    )

    require(
        offer.get("priceCurrency")
        == "EUR",
        f"schema currency: {item['en']}",
    )

    area = schema.get(
        "areaServed",
        {},
    )

    require(
        area.get("name")
        == "United Kingdom",
        f"schema areaServed: {item['en']}",
    )

    require(
        f'href="{item["url"]}"'
        in services_page,
        f"services index does not link page: {item['en']}",
    )

require(
    '/en/kitchen-design-example.html'
    in (
        ROOT
        / "en"
        / "kitchen-design.html"
    ).read_text(
        encoding="utf-8",
    ),
    "English design example link missing",
)

for required_phrase, page in [
    (
        "A consultation must not become a hidden full review or design project.",
        "en/kitchen-consultation.html",
    ),
    (
        "The review does not determine whether a price is objectively correct",
        "en/kitchen-quote-order-review.html",
    ),
    (
        "The 90G Kitchen Review does not include development of a new solution",
        "en/kitchen-review.html",
    ),
    (
        "It does not include an executive measured survey",
        "en/kitchen-design.html",
    ),
    (
        "This check does not replace the final measured survey",
        "en/pre-installation-check.html",
    ),
    (
        "is not a legal expert report",
        "en/kitchen-problem-analysis.html",
    ),
]:
    source = (
        ROOT
        / page
    ).read_text(
        encoding="utf-8",
    )

    require(
        collapse_ws(required_phrase)
        in collapse_ws(source),
        f"service boundary missing: {page}",
    )

print(
    "PASS — six en-GB service detail pages exist"
)

print(
    "PASS — six reciprocal IT / en-GB pairs"
)

print(
    "PASS — six canonical service names"
)

print(
    "PASS — six canonical EUR prices"
)

print(
    "PASS — six canonical delivery times"
)

print(
    "PASS — six service scope boundaries preserved"
)

print(
    "PASS — six Service schema contracts"
)

print(
    "PASS — United Kingdom areaServed"
)

print(
    "PASS — no direct Portal bypass"
)

print(
    "PASS — Free Entry remains website-first"
)

print(
    "PASS — English safe runtime only"
)

print(
    "PASS — UK terminology guard"
)

print(
    "PASS — unmapped commercial extensions excluded"
)

print(
    "PASS — services index now has six real local targets"
)

print(
    "PASS — design example URL reserved for mapped launch page"
)

print(
    "SITE I18N SERVICE DETAILS V1: PASS"
)
