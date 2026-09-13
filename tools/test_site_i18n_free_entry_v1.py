from pathlib import Path
from urllib.parse import (
    parse_qs,
    urlparse,
)
import json
import re

ROOT = Path(__file__).resolve().parents[1]

IT = (
    ROOT
    / "analisi-preventiva.html"
).read_text(
    encoding="utf-8",
)

EN = (
    ROOT
    / "en"
    / "how-it-works.html"
).read_text(
    encoding="utf-8",
)

RUNTIME = (
    ROOT
    / "s90g-site-en-gb-v1.js"
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

require(
    '<html lang="en-GB">'
    in EN,
    "English Free Entry lang",
)

require(
    'href="https://sistema90g.it/en/how-it-works.html"'
    in EN,
    "English Free Entry self canonical",
)

for value in [
    'hreflang="it-IT"',
    'hreflang="en-GB"',
    'hreflang="x-default"',
]:
    require(
        value in EN,
        f"English Free Entry missing {value}",
    )

require(
    'id="submit"'
    in EN,
    "English #submit anchor missing",
)

require(
    'id="what-we-check"'
    in EN,
    "English #what-we-check anchor missing",
)

require(
    "Free initial assessment"
    in EN,
    "free assessment promise missing",
)

require(
    "You are not buying a service"
    in EN,
    "no-purchase message missing",
)

require(
    "no obligation to continue"
    in EN.lower(),
    "no-obligation message missing",
)

require(
    "Not every question needs to become a paid service."
    in EN,
    "customer-first independence message missing",
)

require(
    "service_price="
    not in EN,
    "Free Entry must not pass a service price",
)

for forbidden in [
    "technician",
    "interior",
    "company",
    "agency",
    "retailer",
]:
    require(
        f"requester_role={forbidden}"
        not in EN,
        f"B2B role leaked into English Free Entry: {forbidden}",
    )

portal_hrefs = re.findall(
    r'href="(https://portale\.sistema90g\.it/portal\.html\?[^"]+)"',
    EN,
    re.I,
)

require(
    len(portal_hrefs) == 2,
    f"expected exactly 2 English Portal CTAs, found {len(portal_hrefs)}",
)

positions = set()

for raw in portal_hrefs:
    raw = raw.replace(
        "&amp;",
        "&",
    )

    parsed = urlparse(raw)

    query = parse_qs(
        parsed.query,
    )

    def one(key):
        values = query.get(
            key,
            [],
        )

        require(
            len(values) == 1,
            f"{key} must have exactly one value",
        )

        return values[0]

    require(
        one("requester_role")
        == "private",
        "English Free Entry requester role",
    )

    require(
        one("service")
        == "valutazione-iniziale",
        "English Free Entry service",
    )

    require(
        one("source_page")
        == "en-how-it-works",
        "English Free Entry source page",
    )

    require(
        one("content_type")
        == "free_evaluation",
        "English Free Entry content type",
    )

    require(
        one("lang")
        == "en",
        "English Free Entry language handoff",
    )

    require(
        one("locale")
        == "en-GB",
        "English Free Entry locale handoff",
    )

    positions.add(
        one("cta_position")
    )

require(
    positions
    == {
        "hero",
        "final",
    },
    f"unexpected CTA positions: {sorted(positions)}",
)

require(
    '/s90g-site-en-gb-v1.js'
    in EN,
    "English locale-safe runtime missing",
)

require(
    'privacy-consent.js'
    not in EN,
    "Italian runtime must not load on English Free Entry",
)

require(
    'navigation-conversion.js'
    not in EN,
    "Italian navigation runtime must not load on English Free Entry",
)

for marker in [
    "Mostra gratuitamente",
    "Prima valutazione gratuita",
    "Non stai acquistando",
    "Come funziona",
    "Cosa guardiamo",
    "Il tuo caso",
    "Partita IVA",
]:
    require(
        marker not in EN,
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
    "target.searchParams.set(\n            'lang',\n            'en',"
    in RUNTIME,
    "runtime language enforcement missing",
)

require(
    "target.searchParams.set(\n            'locale',\n            'en-GB',"
    in RUNTIME,
    "runtime locale enforcement missing",
)

for value in [
    'hreflang="it-IT"',
    'hreflang="en-GB"',
    'hreflang="x-default"',
]:
    require(
        value in IT,
        f"Italian Free Entry missing {value}",
    )

require(
    'href="/en/how-it-works.html"'
    in IT,
    "Italian Free Entry EN switch missing",
)

scripts = re.findall(
    r'<script\s+type="application/ld\+json">(.*?)</script>',
    EN,
    re.I | re.S,
)

require(
    len(scripts) == 1,
    "expected one English JSON-LD block",
)

schema = json.loads(
    scripts[0],
)

require(
    schema.get("@type")
    == "WebPage",
    "English Free Entry schema type",
)

require(
    schema.get("url")
    == "https://sistema90g.it/en/how-it-works.html",
    "English Free Entry schema URL",
)

require(
    schema.get("inLanguage")
    == "en-GB",
    "English Free Entry schema language",
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

print(
    "PASS — English Free Entry lang + canonical"
)

print(
    "PASS — Free Entry paired hreflang"
)

print(
    "PASS — English #submit and #what-we-check anchors"
)

print(
    "PASS — customer-first Free Entry copy"
)

print(
    "PASS — no service price or B2B role leakage"
)

print(
    "PASS — exactly two controlled Portal CTAs"
)

print(
    "PASS — Portal requester_role=private"
)

print(
    "PASS — Portal service=valutazione-iniziale"
)

print(
    "PASS — Portal lang=en + locale=en-GB"
)

print(
    "PASS — hero/final attribution preserved"
)

print(
    "PASS — English safe runtime only"
)

print(
    "PASS — UK terminology guard"
)

print(
    "PASS — English structured data"
)

print(
    "PASS — Italian Free Entry EN switch"
)

print(
    "SITE I18N FREE ENTRY V1: PASS"
)
