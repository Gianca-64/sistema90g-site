from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

pairs = [
    (
        "casi-analizzati.html",
        "en/real-kitchen-cases.html",
        "/en/real-kitchen-cases.html",
    ),
    (
        "caso-lavastoviglie-passaggio-cucina.html",
        "en/case-dishwasher-passage.html",
        "/en/case-dishwasher-passage.html",
    ),
    (
        "caso-isola-passaggi-cucina.html",
        "en/case-kitchen-island-clearances.html",
        "/en/case-kitchen-island-clearances.html",
    ),
    (
        "caso-preventivo-cucina-sconto-valore.html",
        "en/case-kitchen-quote-discount-value.html",
        "/en/case-kitchen-quote-discount-value.html",
    ),
]

def require(condition, message):
    if not condition:
        raise SystemExit(
            f"FAIL — {message}"
        )

def collapse(value):
    return " ".join(
        value.split()
    )

for it_file, en_file, en_url in pairs:
    it = (
        ROOT / it_file
    ).read_text(
        encoding="utf-8",
    )

    en = (
        ROOT / en_file
    ).read_text(
        encoding="utf-8",
    )

    require(
        '<html lang="en-GB">'
        in en,
        f"en-GB lang missing: {en_file}",
    )

    for lang in [
        "it-IT",
        "en-GB",
        "x-default",
    ]:
        require(
            f'hreflang="{lang}"'
            in en,
            f"EN hreflang {lang}: {en_file}",
        )

        require(
            f'hreflang="{lang}"'
            in it,
            f"IT hreflang {lang}: {it_file}",
        )

    require(
        f'href="{en_url}"'
        in it,
        f"IT EN switch missing: {it_file}",
    )

    require(
        "/s90g-site-en-gb-v1.js"
        in en,
        f"English runtime missing: {en_file}",
    )

    require(
        "privacy-consent.js"
        not in en,
        f"Italian runtime leaked: {en_file}",
    )

    require(
        "portale.sistema90g.it"
        not in en,
        f"direct Portal bypass: {en_file}",
    )

    require(
        '/en/how-it-works.html#submit'
        in en,
        f"Free Entry missing: {en_file}",
    )

    require(
        'src="images/'
        not in en,
        f"non-root-relative image: {en_file}",
    )

index = (
    ROOT
    / "en"
    / "real-kitchen-cases.html"
).read_text(
    encoding="utf-8",
)

expected_cases = [
    "/en/case-dishwasher-passage.html",
    "/en/case-kitchen-island-clearances.html",
    "/en/case-kitchen-quote-discount-value.html",
]

for target in expected_cases:
    require(
        f'href="{target}"'
        in index,
        f"index target missing: {target}",
    )

for forbidden in [
    "caso-lavello-sotto-finestra-aperture",
    "caso-cucina-piccola-tre-lati",
    "caso-cucina-profondita-75-angolo",
    "/confrontare-due-preventivi-cucina.html",
]:
    require(
        forbidden not in index,
        f"untranslated route leaked in EN index: {forbidden}",
    )

require(
    "Three selected cases"
    in index,
    "English index must not claim six translated cases",
)

schema_match = re.search(
    r'<script\s+type="application/ld\+json">(.*?)</script>',
    index,
    re.I | re.S,
)

require(
    schema_match is not None,
    "index JSON-LD missing",
)

schema = json.loads(
    schema_match.group(1)
)

graph = schema.get(
    "@graph",
    [],
)

lists = [
    item
    for item in graph
    if isinstance(item, dict)
    and item.get("@type") == "ItemList"
]

require(
    len(lists) == 1,
    "index ItemList missing",
)

items = lists[0].get(
    "itemListElement",
    [],
)

require(
    len(items) == 3,
    "English ItemList must contain exactly three mapped cases",
)

dishwasher = (
    ROOT
    / "en"
    / "case-dishwasher-passage.html"
).read_text(
    encoding="utf-8",
)

island = (
    ROOT
    / "en"
    / "case-kitchen-island-clearances.html"
).read_text(
    encoding="utf-8",
)

quote = (
    ROOT
    / "en"
    / "case-kitchen-quote-discount-value.html"
).read_text(
    encoding="utf-8",
)

require(
    collapse(
        "without final room measurements, "
        "the actual depth of the appliance "
        "and the precise position of the cabinet fronts, "
        "it is not possible to state a numerically safe passage."
    )
    in collapse(dishwasher),
    "dishwasher uncertainty boundary changed",
)

require(
    collapse(
        "without final measurements, "
        "actual depths, seating dimensions "
        "and full opening dimensions, "
        "it is not possible to state that the passages are safe."
    )
    in collapse(island),
    "island uncertainty boundary changed",
)

require(
    collapse(
        "without the complete quote, "
        "product data sheets "
        "and the final kitchen design, "
        "it is not possible to establish "
        "the economic value of the supply."
    )
    in collapse(quote),
    "quote uncertainty boundary changed",
)

for page, name in [
    (dishwasher, "dishwasher"),
    (island, "island"),
    (quote, "quote"),
]:
    require(
        not re.search(
            r"\b\d+(?:[.,]\d+)?\s?(?:mm|cm|metres?|meters?)\b",
            page,
            re.I,
        ),
        f"invented numeric measurement: {name}",
    )

    require(
        "£" not in page
        and "GBP" not in page,
        f"GBP leakage: {name}",
    )

for forbidden in [
    "countertop",
    "cooktop",
    "wall cabinet",
    "faucet",
    "range hood",
    "toe-kick",
]:
    require(
        forbidden.lower()
        not in (
            index
            + dishwasher
            + island
            + quote
        ).lower(),
        f"US terminology leaked: {forbidden}",
    )

require(
    "worktop"
    in quote.lower(),
    "UK worktop terminology missing",
)

for page, expected_related in [
    (
        dishwasher,
        {
            "/en/case-kitchen-island-clearances.html",
            "/en/case-kitchen-quote-discount-value.html",
        },
    ),
    (
        island,
        {
            "/en/case-dishwasher-passage.html",
            "/en/case-kitchen-quote-discount-value.html",
        },
    ),
    (
        quote,
        {
            "/en/case-dishwasher-passage.html",
            "/en/case-kitchen-island-clearances.html",
        },
    ),
]:
    for target in expected_related:
        require(
            f'href="{target}"'
            in page,
            f"related mapped case missing: {target}",
        )

    for forbidden in [
        "caso-cucina-piccola-tre-lati",
        "caso-cucina-profondita-75-angolo",
        "caso-lavello-sotto-finestra-aperture",
        "confrontare-due-preventivi-cucina",
    ]:
        require(
            forbidden not in page,
            f"untranslated related route leaked: {forbidden}",
        )

print("PASS — four reciprocal IT / en-GB case pairs")
print("PASS — English index contains exactly three mapped cases")
print("PASS — no untranslated Italian case links")
print("PASS — no untranslated quote-guide link")
print("PASS — dishwasher uncertainty preserved")
print("PASS — island uncertainty preserved")
print("PASS — quote economic uncertainty preserved")
print("PASS — no invented numeric measurements")
print("PASS — no GBP")
print("PASS — UK terminology guard")
print("PASS — mapped related-case graph only")
print("PASS — no direct Portal bypass")
print("PASS — Free Entry remains website-first")
print("PASS — English safe runtime only")
print("SITE I18N REAL CASES V1: PASS")
