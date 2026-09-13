from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]

PAIRS = [
    (
        "metodo-sistema90g.html",
        "en/method.html",
        "/en/method.html",
        "/metodo-sistema90g.html",
    ),
    (
        "chi-e-sistema90g.html",
        "en/about.html",
        "/en/about.html",
        "/chi-e-sistema90g.html",
    ),
    (
        "contatti.html",
        "en/contact.html",
        "/en/contact.html",
        "/contatti.html",
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

for (
    it_file,
    en_file,
    en_path,
    it_path,
) in PAIRS:
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
        f'href="{it_path}"'
        in en,
        f"EN IT switch missing: {en_file}",
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
        f"Free Entry route missing: {en_file}",
    )

    require(
        'src="images/'
        not in en,
        f"non-root-relative image: {en_file}",
    )

method = (
    ROOT
    / "en"
    / "method.html"
).read_text(
    encoding="utf-8",
)

about = (
    ROOT
    / "en"
    / "about.html"
).read_text(
    encoding="utf-8",
)

contact = (
    ROOT
    / "en"
    / "contact.html"
).read_text(
    encoding="utf-8",
)

for label in [
    "OBSERVE",
    "GATHER",
    "DISTINGUISH",
    "VERIFY",
    "ASSESS",
    "DEFINE THE NEXT STEP",
]:
    require(
        label in method,
        f"method step missing: {label}",
    )

for label in [
    "VERIFIED",
    "TO BE VERIFIED",
    "NOT DETERMINABLE",
]:
    require(
        label in method,
        f"certainty level missing: {label}",
    )

require(
    "Missing information is declared,"
    in method
    and "not completed with invented data."
    in method,
    "no-invented-data boundary missing",
)

require(
    "Final review and assessment remain human."
    in method,
    "human final-review boundary missing",
)

require(
    "Technology helps."
    in method
    and "It does not make the final decision."
    in method,
    "AI / technology boundary missing",
)

require(
    "The service comes after"
    in method
    and "understanding the problem."
    in method,
    "problem-before-service principle missing",
)

require(
    "retailer or manufacturer"
    in method,
    "retailer/manufacturer confirmation boundary missing",
)

require(
    "competent professional"
    in method,
    "competent-professional boundary missing",
)

for marker in [
    "Gian Carlo Primo",
    "founder of Sistema 90G",
    "design, sales, installation",
    "after-sales",
    "does not sell furniture",
    "does not represent brands",
    "does not receive commission",
    "Final review and assessment remain human.",
]:
    require(
        marker.lower()
        in about.lower(),
        f"about invariant missing: {marker}",
    )

require(
    "Sistema 90G does not replace"
    in about,
    "about competence boundary missing",
)

require(
    "does not certify"
    in about,
    "about no-certification boundary missing",
)

require(
    "production order"
    in about,
    "about production-order boundary missing",
)

for marker in [
    "info@sistema90g.it",
    "Sending the case is only used",
    "the service and price are stated",
    "before work begins",
]:
    require(
        marker
        in contact,
        f"contact invariant missing: {marker}",
    )

require(
    contact.count(
        "mailto:info@sistema90g.it"
    )
    >= 2,
    "public email actions missing",
)

def schemas(
    source,
):
    blocks = re.findall(
        r'<script\s+type="application/ld\+json">(.*?)</script>',
        source,
        re.I | re.S,
    )

    return [
        json.loads(
            block
        )
        for block in blocks
    ]

about_blocks = schemas(
    about
)

require(
    len(about_blocks) == 1,
    "about schema count",
)

about_graph = about_blocks[0].get(
    "@graph",
    [],
)

about_people = [
    item
    for item in about_graph
    if isinstance(
        item,
        dict,
    )
    and item.get(
        "@type"
    )
    == "Person"
]

require(
    len(about_people) == 1,
    "about Person schema missing",
)

require(
    about_people[0].get(
        "jobTitle"
    )
    == "Founder of Sistema 90G",
    "about jobTitle overclaim or mismatch",
)

contact_blocks = schemas(
    contact
)

require(
    len(contact_blocks) == 1,
    "contact schema count",
)

contact_graph = contact_blocks[0].get(
    "@graph",
    [],
)

organisations = [
    item
    for item in contact_graph
    if isinstance(
        item,
        dict,
    )
    and item.get(
        "@type"
    )
    == "Organization"
]

people = [
    item
    for item in contact_graph
    if isinstance(
        item,
        dict,
    )
    and item.get(
        "@type"
    )
    == "Person"
]

pages = [
    item
    for item in contact_graph
    if isinstance(
        item,
        dict,
    )
    and item.get(
        "@type"
    )
    == "ContactPage"
]

require(
    len(organisations) == 1,
    "contact Organization schema missing",
)

require(
    len(people) == 1,
    "contact Person schema missing",
)

require(
    len(pages) == 1,
    "ContactPage schema missing",
)

org = organisations[0]

area = org.get(
    "areaServed",
    {},
)

require(
    isinstance(
        area,
        dict,
    )
    and area.get(
        "@type"
    )
    == "Country"
    and area.get(
        "name"
    )
    == "United Kingdom",
    "contact areaServed must be United Kingdom",
)

require(
    org.get(
        "email"
    )
    == "info@sistema90g.it",
    "contact email schema mismatch",
)

require(
    people[0].get(
        "jobTitle"
    )
    == "Founder of Sistema 90G",
    "contact professional-title overclaim",
)

require(
    pages[0].get(
        "inLanguage"
    )
    == "en-GB",
    "ContactPage language mismatch",
)

combined = (
    method
    + about
    + contact
)

for forbidden in [
    "Independent kitchen technician",
    "Kitchen technician",
    "architect",
    "chartered",
    "engineer",
]:
    require(
        forbidden.lower()
        not in combined.lower(),
        f"professional-title overclaim: {forbidden}",
    )

require(
    '"name": "Italia"'
    not in contact,
    "Italian areaServed leaked into English contact schema",
)

require(
    "Progettazione e analisi indipendente"
    not in contact,
    "Italian activity-description schema leaked",
)

for forbidden in [
    "£",
    "GBP",
]:
    require(
        forbidden.lower()
        not in combined.lower(),
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
        not in combined.lower(),
        f"US terminology leaked: {forbidden}",
    )

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

        attrs = dict(
            attrs
        )

        href = attrs.get(
            "href"
        )

        if href:
            self.hrefs.append(
                href
            )

allowed_it = {
    "/metodo-sistema90g.html",
    "/chi-e-sistema90g.html",
    "/contatti.html",
}

for filename, source in [
    (
        "method",
        method,
    ),
    (
        "about",
        about,
    ),
    (
        "contact",
        contact,
    ),
]:
    parser = LinkParser()
    parser.feed(
        source
    )

    for href in parser.hrefs:
        if href.startswith(
            "mailto:"
        ):
            continue

        if href.startswith(
            "#"
        ):
            continue

        route = urlsplit(
            href
        ).path

        if not route.endswith(
            ".html"
        ):
            continue

        if route.startswith(
            "/en/"
        ):
            continue

        require(
            route
            in allowed_it,
            f"untranslated Italian route leaked in {filename}: {href}",
        )

print("PASS — three reciprocal IT / en-GB pairs")
print("PASS — six-step method preserved")
print("PASS — VERIFIED / TO BE VERIFIED / NOT DETERMINABLE")
print("PASS — no-invented-data boundary")
print("PASS — human final-review boundary")
print("PASS — technology / AI boundary")
print("PASS — problem-before-service principle")
print("PASS — founder identity preserved")
print("PASS — design / sales / installation / after-sales experience")
print("PASS — independence / no brand / no commission claims")
print("PASS — specialist competence limits preserved")
print("PASS — no certification or production-order overclaim")
print("PASS — public email preserved")
print("PASS — UK areaServed")
print("PASS — Founder-only jobTitle")
print("PASS — no professional-title inflation")
print("PASS — no Italy areaServed leakage")
print("PASS — no invented measurements")
print("PASS — no GBP")
print("PASS — UK terminology guard")
print("PASS — no direct Portale bypass")
print("PASS — Free Entry remains website-first")
print("PASS — English safe runtime only")
print("SITE I18N METHOD + ABOUT + CONTACT V1: PASS")
