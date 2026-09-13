from pathlib import Path
from urllib.parse import urlparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT
    / "tools"
    / "site-i18n-en-gb-manifest.json"
)

def fail(message):
    print(f"FAIL — {message}")
    raise SystemExit(1)

data = json.loads(
    MANIFEST.read_text(
        encoding="utf-8",
    )
)

if data.get("defaultLanguage") != "it":
    fail("default language must remain it")

if data.get("defaultLocale") != "it-IT":
    fail("default locale must remain it-IT")

if data.get("pilotLanguage") != "en":
    fail("pilot language must be en")

if data.get("pilotLocale") != "en-GB":
    fail("pilot locale must be en-GB")

if data.get("pilotMarket") != "GB":
    fail("pilot market must be GB")

if data.get("currency") != "EUR":
    fail("V1 currency must remain EUR")

if data.get("englishPrefix") != "/en/":
    fail("English website must live under /en/")

portal = data.get("portal") or {}

expected_portal = {
    "origin":
        "https://portale.sistema90g.it",
    "language":
        "en",
    "locale":
        "en-GB",
    "requesterRole":
        "private",
    "freeEntryService":
        "valutazione-iniziale",
}

for key, expected in expected_portal.items():
    if portal.get(key) != expected:
        fail(
            f"portal contract mismatch: "
            f"{key}"
        )

sitemap_path = ROOT / "sitemap.xml"

sitemap = sitemap_path.read_text(
    encoding="utf-8",
    errors="ignore",
)

public_urls = {
    value.strip()
    for value in re.findall(
        r"<loc>(.*?)</loc>",
        sitemap,
        re.I | re.S,
    )
}

pages = data.get("pages") or []

if not pages:
    fail("page manifest is empty")

ids = set()
it_paths = set()
en_paths = set()
en_urls = set()

for page in pages:
    page_id = page.get("id")
    it_path = page.get("it")
    en_path = page.get("en")
    en_url = page.get("enUrl")

    if not page_id:
        fail("page without id")

    if page_id in ids:
        fail(
            f"duplicate page id: {page_id}"
        )

    ids.add(page_id)

    if not it_path:
        fail(
            f"{page_id}: missing Italian source"
        )

    if it_path in it_paths:
        fail(
            f"duplicate Italian source: "
            f"{it_path}"
        )

    it_paths.add(it_path)

    if not (
        ROOT / it_path
    ).is_file():
        fail(
            f"{page_id}: Italian source "
            f"does not exist: {it_path}"
        )

    if it_path == "index.html":
        canonical_it = (
            "https://sistema90g.it/"
        )
    else:
        canonical_it = (
            "https://sistema90g.it/"
            + it_path
        )

    if canonical_it not in public_urls:
        fail(
            f"{page_id}: Italian source "
            f"is not canonical sitemap scope: "
            f"{canonical_it}"
        )

    if not en_path:
        fail(
            f"{page_id}: missing English target"
        )

    if not en_path.startswith("en/"):
        fail(
            f"{page_id}: English target "
            f"must live under en/"
        )

    if en_path in en_paths:
        fail(
            f"duplicate English path: "
            f"{en_path}"
        )

    en_paths.add(en_path)

    if not en_url:
        fail(
            f"{page_id}: missing English URL"
        )

    if not en_url.startswith("/en/"):
        fail(
            f"{page_id}: English URL "
            f"must live under /en/"
        )

    if en_url in en_urls:
        fail(
            f"duplicate English URL: "
            f"{en_url}"
        )

    en_urls.add(en_url)

required_ids = {
    "home",
    "how-it-works",
    "services",
    "consultation",
    "quote-order-review",
    "kitchen-review",
    "kitchen-design",
    "pre-installation-check",
    "problem-analysis",
    "real-cases",
    "guides",
    "faq",
    "method",
    "about",
    "contact",
    "privacy",
    "cookie",
    "intellectual-property",
}

missing = (
    required_ids - ids
)

if missing:
    fail(
        "required launch pages missing: "
        + ", ".join(sorted(missing))
    )

service_sources = {
    "consultation":
        "consulenza-90g.html",
    "quote-order-review":
        "analisi-preventivo-cucina.html",
    "kitchen-review":
        "verifica-90g.html",
    "kitchen-design":
        "progetto-cucina-sistema90g.html",
    "pre-installation-check":
        "controllo-pre-montaggio-cucina.html",
    "problem-analysis":
        "analisi-problema-cucina.html",
}

by_id = {
    page["id"]: page
    for page in pages
}

for page_id, source in service_sources.items():
    actual = (
        by_id
        .get(page_id, {})
        .get("it")
    )

    if actual != source:
        fail(
            f"{page_id}: unexpected "
            f"service source {actual!r}"
        )

seo = data.get("seo") or {}

if seo.get("selfCanonical") is not True:
    fail("self canonical policy missing")

if seo.get("pairedHreflang") != [
    "it-IT",
    "en-GB",
]:
    fail("paired hreflang contract invalid")

if seo.get(
    "automaticLanguageRedirect"
) is not False:
    fail(
        "automatic language redirect "
        "must be disabled"
    )

blockers = set(
    data.get("releaseBlockers")
    or []
)

for blocker in {
    "english-commercial-terms",
    "english-consumer-cancellation-information",
    "paired-hreflang",
    "english-sitemap",
    "language-switcher",
    "portal-en-gb-release",
    "bilingual-e2e",
}:
    if blocker not in blockers:
        fail(
            f"release blocker not recorded: "
            f"{blocker}"
        )

print(
    "PASS — locale contract "
    "it-IT / en-GB"
)

print(
    "PASS — /en/ URL architecture"
)

print(
    "PASS — EUR-only V1 contract"
)

print(
    "PASS — English Portale entry contract"
)

print(
    "PASS — all Italian launch "
    "sources exist"
)

print(
    "PASS — all Italian launch "
    "sources are current sitemap URLs"
)

print(
    "PASS — six canonical service "
    "sources mapped"
)

print(
    "PASS — no duplicate English "
    "targets"
)

print(
    "PASS — legal and bilingual "
    "release blockers recorded"
)

print(
    f"SITE I18N ARCHITECTURE V1: PASS "
    f"({len(pages)} mapped pages)"
)
