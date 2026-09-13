from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]

IT = (
    ROOT
    / "servizi.html"
).read_text(
    encoding="utf-8",
)

EN = (
    ROOT
    / "en"
    / "services.html"
).read_text(
    encoding="utf-8",
)

def require(
    condition,
    message,
):
    if not condition:
        raise SystemExit(
            f"FAIL — {message}"
        )

def normalise(value):
    value = re.sub(
        r"<[^>]+>",
        " ",
        value,
    )

    return " ".join(
        html.unescape(
            value
        ).split()
    )

require(
    '<html lang="en-GB">'
    in EN,
    "English services lang",
)

require(
    'href="https://sistema90g.it/en/services.html"'
    in EN,
    "English services self canonical",
)

for value in [
    'hreflang="it-IT"',
    'hreflang="en-GB"',
    'hreflang="x-default"',
]:
    require(
        value in EN,
        f"English services missing {value}",
    )

require(
    'id="situations"'
    in EN,
    "English situations anchor missing",
)

require(
    "Do not start with the service."
    in EN,
    "situation-first hero missing",
)

require(
    "Start with where you are."
    in EN,
    "customer situation promise missing",
)

require(
    "All prices shown are in EUR."
    in EN,
    "EUR disclosure missing",
)

expected = [
    (
        "choice",
        "90G Kitchen Consultation",
        "€79",
        "within 1 working day",
        "/en/kitchen-consultation.html",
    ),
    (
        "quote",
        "90G Quote & Order Review",
        "€129",
        "within 2 working days",
        "/en/kitchen-quote-order-review.html",
    ),
    (
        "review",
        "90G Kitchen Review",
        "€149",
        "within 2 working days",
        "/en/kitchen-review.html",
    ),
    (
        "design",
        "90G Kitchen Design",
        "€299",
        "within 3 working days",
        "/en/kitchen-design.html",
    ),
    (
        "pre-installation",
        "90G Pre-installation Check",
        "€179",
        "within 2 working days",
        "/en/pre-installation-check.html",
    ),
    (
        "problem",
        "90G Kitchen Problem Analysis",
        "€149",
        "within 2 working days",
        "/en/kitchen-problem-analysis.html",
    ),
]

articles = [
    match.group(0)
    for match in re.finditer(
        r"<article\b[\s\S]*?</article>",
        EN,
        re.I,
    )
    if "s90g-svc-route"
    in match.group(0)
]

require(
    len(articles) == 6,
    f"expected six English canonical routes, found {len(articles)}",
)

for (
    route_id,
    name,
    price,
    delivery,
    href,
) in expected:
    block = next(
        (
            article
            for article in articles
            if f'id="{route_id}"'
            in article
        ),
        None,
    )

    require(
        block is not None,
        f"English route missing: {route_id}",
    )

    text = normalise(
        block
    )

    require(
        name in text,
        f"service name missing: {name}",
    )

    require(
        price in text,
        f"service price missing: {name}",
    )

    require(
        delivery in text,
        f"delivery time missing: {name}",
    )

    require(
        f'href="{href}"'
        in block,
        f"service detail URL missing: {name}",
    )

require(
    "£"
    not in EN,
    "GBP must not be displayed in V1",
)

require(
    "GBP"
    not in EN,
    "GBP must not be advertised in V1",
)

require(
    "349 €"
    not in EN
    and "€349"
    not in EN,
    "unmapped Project & Quote extension leaked into en-GB launch",
)

require(
    "39 €"
    not in EN
    and "€39"
    not in EN,
    "unmapped render extension leaked into en-GB launch",
)

require(
    "progetto-preventivo-cucina-90g"
    not in EN,
    "unmapped Italian extension link leaked into English page",
)

require(
    "portale.sistema90g.it"
    not in EN,
    "services page must route through English Free Entry, not directly to Portal",
)

free_entry_links = re.findall(
    r'href="(/en/how-it-works\.html#submit)"',
    EN,
)

require(
    len(free_entry_links) >= 3,
    "English services must expose Free Entry from header, hero/fallback and final journey",
)

for marker in [
    "Servizi e prezzi",
    "Non partire dal servizio",
    "A che punto sei?",
    "Ti riconosci qui?",
    "Cosa ricevi",
    "Mostra il tuo caso",
    "Partita IVA",
]:
    require(
        marker
        not in EN,
        f"Italian visible copy remains: {marker}",
    )

for term in [
    "countertop",
    "cooktop",
    "wall cabinet",
]:
    require(
        term.lower()
        not in EN.lower(),
        f"US terminology found: {term}",
    )

require(
    'privacy-consent.js'
    not in EN,
    "Italian consent runtime must not load",
)

require(
    'navigation-conversion.js'
    not in EN,
    "Italian navigation runtime must not load",
)

require(
    '/s90g-site-en-gb-v1.js'
    in EN,
    "English safe runtime missing",
)

require(
    'src="images/'
    not in EN,
    "English images must be root-relative",
)

require(
    'href="s90g-'
    not in EN,
    "English CSS must be root-relative",
)

for value in [
    'hreflang="it-IT"',
    'hreflang="en-GB"',
    'hreflang="x-default"',
]:
    require(
        value in IT,
        f"Italian services missing {value}",
    )

require(
    'href="/en/services.html"'
    in IT,
    "Italian services EN switch missing",
)

scripts = re.findall(
    r'<script\s+type="application/ld\+json">(.*?)</script>',
    EN,
    re.I | re.S,
)

require(
    len(scripts) == 1,
    "expected one English services JSON-LD block",
)

schema = json.loads(
    scripts[0],
)

require(
    schema.get("@type")
    == "ItemList",
    "English services schema type",
)

require(
    schema.get("inLanguage")
    == "en-GB",
    "English services schema language",
)

items = schema.get(
    "itemListElement",
    [],
)

require(
    len(items) == 6,
    "English services schema must contain six items",
)

expected_schema_urls = [
    "https://sistema90g.it/en/kitchen-consultation.html",
    "https://sistema90g.it/en/kitchen-quote-order-review.html",
    "https://sistema90g.it/en/kitchen-review.html",
    "https://sistema90g.it/en/kitchen-design.html",
    "https://sistema90g.it/en/pre-installation-check.html",
    "https://sistema90g.it/en/kitchen-problem-analysis.html",
]

require(
    [
        item.get("url")
        for item in items
    ]
    == expected_schema_urls,
    "English services schema URLs do not match canonical launch mapping",
)

print(
    "PASS — English services lang + canonical"
)

print(
    "PASS — services paired hreflang"
)

print(
    "PASS — situation-first customer journey"
)

print(
    "PASS — exactly six en-GB canonical services"
)

print(
    "PASS — six canonical EUR prices"
)

print(
    "PASS — six canonical delivery times"
)

print(
    "PASS — six mapped English detail URLs"
)

print(
    "PASS — EUR-only V1 / no GBP"
)

print(
    "PASS — unmapped extensions excluded"
)

print(
    "PASS — Free Entry stays inside English website journey"
)

print(
    "PASS — no direct Portal bypass"
)

print(
    "PASS — UK terminology guard"
)

print(
    "PASS — English safe runtime only"
)

print(
    "PASS — English ItemList structured data"
)

print(
    "PASS — Italian services EN switch"
)

print(
    "SITE I18N SERVICES V1: PASS"
)
