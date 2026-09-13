from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]

PAIRS = [
    (
        "progettare-cucina-guide.html",
        "en/kitchen-guides.html",
        "/en/kitchen-guides.html",
    ),
    (
        "domande-cucina-faq.html",
        "en/kitchen-faq.html",
        "/en/kitchen-faq.html",
    ),
]

def require(
    condition,
    message,
):
    if not condition:
        raise SystemExit(
            f"FAIL — {message}"
        )

for it_file, en_file, en_path in PAIRS:
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
        f"lang missing: {en_file}",
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
        f'href="{en_path}"'
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
        f"direct Portale bypass: {en_file}",
    )

    require(
        "/en/how-it-works.html#submit"
        in en,
        f"Free Entry missing: {en_file}",
    )

    require(
        'src="images/'
        not in en,
        f"non-root-relative image: {en_file}",
    )

guides = (
    ROOT
    / "en"
    / "kitchen-guides.html"
).read_text(
    encoding="utf-8",
)

faq = (
    ROOT
    / "en"
    / "kitchen-faq.html"
).read_text(
    encoding="utf-8",
)

required_guide_links = {
    "/en/kitchen-design.html",
    "/en/kitchen-design-example.html",
    "/en/kitchen-review.html",
    "/en/kitchen-quote-order-review.html",
    "/en/real-kitchen-cases.html",
    "/en/case-dishwasher-passage.html",
    "/en/case-kitchen-island-clearances.html",
    "/en/case-kitchen-quote-discount-value.html",
    "/en/kitchen-faq.html",
    "/en/services.html",
    "/en/how-it-works.html#submit",
}

for target in required_guide_links:
    require(
        f'href="{target}"'
        in guides,
        f"guide launch link missing: {target}",
    )

italian_pair_routes = {
    "/progettare-cucina-guide.html",
    "/domande-cucina-faq.html",
}

class LinkParser(
    HTMLParser
):
    def __init__(self):
        super().__init__(
            convert_charrefs=True
        )

        self.hrefs = []

    def handle_starttag(
        self,
        tag,
        attrs,
    ):
        if tag != "a":
            return

        attrs = dict(attrs)

        href = attrs.get(
            "href"
        )

        if href:
            self.hrefs.append(
                href
            )

for name, source in [
    ("guides", guides),
    ("faq", faq),
]:
    parser = LinkParser()
    parser.feed(source)

    for href in parser.hrefs:
        path = urlsplit(
            href
        ).path

        if not path.endswith(
            ".html"
        ):
            continue

        if path.startswith(
            "/en/"
        ):
            continue

        require(
            path
            in italian_pair_routes,
            f"untranslated Italian route leaked in {name}: {href}",
        )

for forbidden in [
    "cucina-piccola-come-progettarla",
    "piano-lavoro-colonne-cucina",
    "errori-progetto-cucina",
    "illuminazione-cucina-progetto",
    "vincoli-verticali-cucina",
    "progettare-cucina-prima-impianti",
    "misure-passaggi-cucina",
    "cucina-ad-angolo-guida",
    "profondita-cucina-75-cm",
    "lavello-sotto-finestra-cucina",
    "lavello-una-o-due-vasche",
    "isola-cucina-distanze-passaggi",
    "penisola-cucina-distanze-passaggi",
    "cucina-open-space-tavolo-passaggi",
    "tavolo-vicino-cucina",
    "progetto-cucina-planner-online",
    "preventivo-acquisto-cucina-guide",
    "preventivo-cucina-guida",
    "rinnovare-cucina-senza-cambiarla",
    "elettrodomestici-impianti-cucina-guide",
    "materiali-finiture-cucina-guide",
    "confrontare-due-preventivi-cucina",
    "prima-di-firmare-ordine-cucina",
    "voci-escluse-preventivo-cucina",
]:
    require(
        forbidden not in guides,
        f"untranslated guide leaked: {forbidden}",
    )

    require(
        forbidden not in faq,
        f"untranslated FAQ link leaked: {forbidden}",
    )

guide_questions = [
    "Where do you start when planning a kitchen?",
    "Can I plan the kitchen before choosing a retailer?",
    "How can I tell whether a kitchen layout is functional?",
    "Should the kitchen layout or the utility positions be defined first?",
]

for question in guide_questions:
    require(
        question in guides,
        f"guide FAQ missing: {question}",
    )

faq_questions = [
    "Can I plan the kitchen before choosing a retailer?",
    "How can I tell whether a kitchen design is good?",
    "How do I compare two kitchen quotes?",
    "What should I check before signing a kitchen order?",
    "Should kitchen utility positions be decided before or after the design?",
    "Is a matt or gloss kitchen better?",
    "When is an independent kitchen review useful?",
]

for question in faq_questions:
    require(
        question in faq,
        f"visible FAQ missing: {question}",
    )

require(
    faq.count(
        "data-faq-question"
    )
    == 7,
    "FAQ must expose exactly seven visible questions",
)

def jsonld_blocks(source):
    return [
        json.loads(raw)
        for raw in re.findall(
            r'<script\s+type="application/ld\+json">(.*?)</script>',
            source,
            re.I | re.S,
        )
    ]

faq_schemas = jsonld_blocks(
    faq
)

require(
    len(faq_schemas) == 1,
    "FAQ JSON-LD block count",
)

graph = faq_schemas[0].get(
    "@graph",
    [],
)

faq_pages = [
    item
    for item in graph
    if isinstance(
        item,
        dict,
    )
    and item.get(
        "@type"
    )
    == "FAQPage"
]

require(
    len(faq_pages) == 1,
    "FAQPage schema missing",
)

entities = faq_pages[0].get(
    "mainEntity",
    [],
)

require(
    len(entities) == 7,
    "FAQ schema must contain seven questions",
)

schema_questions = {
    item.get(
        "name"
    )
    for item in entities
}

require(
    schema_questions
    == set(
        faq_questions
    ),
    "visible / schema FAQ question contract mismatch",
)

guides_schemas = jsonld_blocks(
    guides
)

require(
    len(guides_schemas) == 1,
    "guide JSON-LD block count",
)

guide_graph = guides_schemas[0].get(
    "@graph",
    [],
)

guide_faq = [
    item
    for item in guide_graph
    if isinstance(
        item,
        dict,
    )
    and item.get(
        "@type"
    )
    == "FAQPage"
]

require(
    len(guide_faq) == 1,
    "guide FAQPage schema missing",
)

require(
    len(
        guide_faq[0].get(
            "mainEntity",
            [],
        )
    )
    == 4,
    "guide FAQ schema must contain four source questions",
)

combined = (
    guides
    + faq
).lower()

for forbidden in [
    "countertop",
    "cooktop",
    "wall cabinet",
    "faucet",
    "range hood",
    "toe-kick",
]:
    require(
        forbidden
        not in combined,
        f"US terminology leaked: {forbidden}",
    )

require(
    "worktop"
    in combined,
    "UK worktop terminology missing",
)

for forbidden in [
    "£",
    "gbp",
]:
    require(
        forbidden.lower()
        not in combined,
        f"GBP leakage: {forbidden}",
    )

require(
    not re.search(
        r"\b\d+(?:[.,]\d+)?\s?(?:mm|cm|metres?|meters?)\b",
        combined,
        re.I,
    ),
    "numeric measurement introduced",
)

require(
    "final technical verification remains specific"
    in combined,
    "site-specific technical boundary missing",
)

print("PASS — reciprocal guides + FAQ pairs")
print("PASS — curated English guide hub")
print("PASS — no untranslated Italian guide routes")
print("PASS — guide hub links only launch English resources")
print("PASS — four source guide questions preserved")
print("PASS — seven canonical FAQ questions visible")
print("PASS — seven-question FAQPage schema matches visible content")
print("PASS — site-specific technical verification boundary")
print("PASS — no invented measurements")
print("PASS — no GBP")
print("PASS — UK terminology guard")
print("PASS — no direct Portale bypass")
print("PASS — Free Entry remains website-first")
print("PASS — English safe runtime only")
print("SITE I18N GUIDES + FAQ V1: PASS")
