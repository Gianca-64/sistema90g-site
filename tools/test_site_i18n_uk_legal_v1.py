from pathlib import Path
from html.parser import HTMLParser
import json
import re

ROOT = Path(__file__).resolve().parents[1]

PAIRS = [
    (
        "privacy-policy.html",
        "en/privacy-policy.html",
        "/en/privacy-policy.html",
    ),
    (
        "cookie-policy.html",
        "en/cookie-policy.html",
        "/en/cookie-policy.html",
    ),
    (
        "proprieta-intellettuale.html",
        "en/intellectual-property.html",
        "/en/intellectual-property.html",
    ),
]

LEGAL = [
    "en/privacy-policy.html",
    "en/cookie-policy.html",
    "en/intellectual-property.html",
    "en/commercial-terms.html",
    "en/cancellation-information.html",
]

TRADER = [
    "Via Federico Vanga 9",
    "38061 Santa Margherita di Ala",
    "Italy",
    "info@sistema90g.it",
    "+39 327 547 8485",
    "IT02844900221",
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
        f"English lang missing: {en_file}",
    )

    for lang in [
        "it-IT",
        "en-GB",
        "x-default",
    ]:
        require(
            f'hreflang="{lang}"'
            in it,
            f"IT hreflang missing {lang}: {it_file}",
        )

    require(
        f'href="{en_path}"'
        in it,
        f"English switch missing: {it_file}",
    )

    for lang in [
        "it-IT",
        "en-GB",
        "x-default",
    ]:
        require(
            f'hreflang="{lang}"'
            in en,
            f"EN reciprocal hreflang missing {lang}: {en_file}",
        )

    require(
        f'href="https://sistema90g.it/{it_file}"'
        in en,
        f"EN reciprocal Italian alternate missing: {en_file}",
    )

    require(
        f'href="/{it_file}"'
        in en
        and 'hreflang="it-IT"'
        in en,
        f"visible IT switch missing: {en_file}",
    )

for filename in LEGAL:
    source = (
        ROOT / filename
    ).read_text(
        encoding="utf-8",
    )

    require(
        '<html lang="en-GB">'
        in source,
        f"lang missing: {filename}",
    )

    require(
        "/s90g-site-en-gb-v1.js"
        in source,
        f"safe EN runtime missing: {filename}",
    )

    require(
        "privacy-consent.js"
        not in source,
        f"Italian runtime leaked: {filename}",
    )

    require(
        "portale.sistema90g.it"
        not in source,
        f"direct Portale bypass: {filename}",
    )

    for href in [
        "/en/privacy-policy.html",
        "/en/cookie-policy.html",
        "/en/intellectual-property.html",
        "/en/commercial-terms.html",
        "/en/cancellation-information.html",
    ]:
        require(
            f'href="{href}"'
            in source,
            f"legal footer link missing {href}: {filename}",
        )

privacy = (
    ROOT
    / "en/privacy-policy.html"
).read_text(
    encoding="utf-8",
)

for marker in [
    "lawful basis",
    "performance of the contract",
    "legal obligation",
    "legitimate interests",
    "analytics",
    "SumUp",
    "Google",
    "international transfers",
    "UK adequacy regulations",
    "retention",
    "Information Commissioner's Office",
    "Final review and assessment remain human",
]:
    require(
        marker.lower()
        in privacy.lower(),
        f"privacy marker missing: {marker}",
    )

require(
    'name="robots"'
    in privacy
    and "noindex,nofollow"
    in privacy,
    "pre-launch privacy must be noindex",
)

require(
    'data-uk-release-blocker="uk-representative"'
    in privacy,
    "UK representative release blocker missing",
)

require(
    "pre-launch draft"
    in privacy.lower(),
    "privacy pre-launch warning missing",
)

cookie = (
    ROOT
    / "en/cookie-policy.html"
).read_text(
    encoding="utf-8",
)

for marker in [
    "local storage",
    "Google Analytics",
    "after you choose to accept analytics",
    "reject analytics",
    "Cookie settings",
    "SumUp",
]:
    require(
        marker.lower()
        in cookie.lower(),
        f"cookie marker missing: {marker}",
    )

ip = (
    ROOT
    / "en/intellectual-property.html"
).read_text(
    encoding="utf-8",
)

for marker in [
    "Original Sistema 90G content",
    "Permitted personal use",
    "Uses that require permission",
    "Customer material",
    "Customer cases",
    "Artificial intelligence",
    "Third-party brands",
]:
    require(
        marker.lower()
        in ip.lower(),
        f"IP marker missing: {marker}",
    )

terms = (
    ROOT
    / "en/commercial-terms.html"
).read_text(
    encoding="utf-8",
)

for marker in TRADER:
    require(
        marker.lower()
        in terms.lower(),
        f"trader identity missing from terms: {marker}",
    )

for marker in [
    "Free Entry",
    "paid contract is formed",
    "successfully completed",
    "verified",
    "EUR",
    "SumUp",
    "14 days",
    "expressly ask",
    "do not request early performance",
    "reasonable care and skill",
    "Complaints",
    "No subscription or automatic renewal",
]:
    require(
        marker.lower()
        in terms.lower(),
        f"terms marker missing: {marker}",
    )

require(
    "GBP"
    not in terms,
    "GBP must not replace EUR",
)

cancellation = (
    ROOT
    / "en/cancellation-information.html"
).read_text(
    encoding="utf-8",
)

for marker in TRADER[:5]:
    require(
        marker.lower()
        in cancellation.lower(),
        f"cancellation trader detail missing: {marker}",
    )

for marker in [
    "14 days",
    "day after the day",
    "without giving a reason",
    "expressly request",
    "proportionate",
    "fully completed",
    "lose the right to cancel",
    "do not request early performance",
    "Model cancellation form",
    "reasonable care and skill",
]:
    require(
        marker.lower()
        in cancellation.lower(),
        f"cancellation marker missing: {marker}",
    )

english_pages = sorted(
    (ROOT / "en").glob(
        "*.html"
    )
)

require(
    len(english_pages) >= 24,
    f"expected at least 24 English pages, got {len(english_pages)}",
)

for path in english_pages:
    source = path.read_text(
        encoding="utf-8",
    )

    for href in [
        "/en/privacy-policy.html",
        "/en/cookie-policy.html",
        "/en/intellectual-property.html",
        "/en/commercial-terms.html",
        "/en/cancellation-information.html",
    ]:
        require(
            f'href="{href}"'
            in source,
            f"{path}: legal footer target missing {href}",
        )

combined = "\n".join(
    (
        ROOT / filename
    ).read_text(
        encoding="utf-8",
    )
    for filename in LEGAL
)

for forbidden in [
    "£",
    "GBP",
    "UK office",
    "UK branch",
    "UK establishment",
]:
    require(
        forbidden.lower()
        not in combined.lower(),
        f"unsupported UK commercial claim: {forbidden}",
    )

for path in [
    ROOT / "en/commercial-terms.html",
    ROOT / "en/cancellation-information.html",
]:
    source = path.read_text(
        encoding="utf-8",
    )

    require(
        "info@sistema90g.it"
        in source,
        f"{path}: complaint/contact email missing",
    )

print("PASS — three reciprocal Italian / en-GB legal pairs")
print("PASS — five UK legal pages exist")
print("PASS — real trader address / email / telephone")
print("PASS — EUR-only commercial contract")
print("PASS — paid-contract formation described")
print("PASS — 14-day cancellation information")
print("PASS — optional early-performance path")
print("PASS — proportional-payment rule")
print("PASS — full-performance cancellation-loss boundary")
print("PASS — model cancellation form")
print("PASS — reasonable-care-and-skill boundary")
print("PASS — cookie analytics remains consent-first")
print("PASS — intellectual-property contract")
print("PASS — all English footers expose five legal targets")
print("PASS — UK representative remains explicit release blocker")
print("PASS — pre-launch UK privacy remains noindex")
print("PASS — no unsupported UK office / branch claim")
print("PASS — no direct Portale bypass")
print("SITE I18N UK LEGAL V1: PASS")
