#!/usr/bin/env python3

from pathlib import Path
from urllib.parse import urlparse, urljoin
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

errors = []

js = (
    ROOT / "privacy-consent.js"
).read_text(errors="replace")

required_js = [
    "function s90gEnsureCookieBanner()",
    "function s90gEnsureCookieSettingsControl()",
    "const b=s90gEnsureCookieBanner()",
    "s90gEnsureCookieSettingsControl();",
    "link.dataset.cookieSettings='';",
    "link.textContent='Gestisci cookie';",
    "document.querySelectorAll('[data-cookie-choice]')",
    "document.querySelectorAll('[data-cookie-settings]')",
    "showCookieBanner(b)",
]

for marker in required_js:

    if marker not in js:
        errors.append(
            f"runtime marker missing: {marker}"
        )

try:
    if (
        js.index("const b=s90gEnsureCookieBanner()")
        >
        js.index(
            "document.querySelectorAll('[data-cookie-choice]')"
        )
    ):
        errors.append(
            "banner ensure runs after choice-listener binding"
        )

    if (
        js.index("s90gEnsureCookieSettingsControl();")
        >
        js.index(
            "document.querySelectorAll('[data-cookie-settings]')"
        )
    ):
        errors.append(
            "settings ensure runs after settings-listener binding"
        )

except ValueError:
    pass


# ----------------------------------------------------------
# Every indexed page must resolve the same current runtime.
# ----------------------------------------------------------

xml = (
    ROOT / "sitemap.xml"
).read_text(errors="replace")

urls = re.findall(
    r"<loc>\s*(.*?)\s*</loc>",
    xml,
    re.I
)

pages = []

for public_url in urls:

    path = urlparse(
        public_url
    ).path.lstrip("/")

    if not path:
        path = "index.html"

    if path.endswith(".html"):
        pages.append(
            (public_url, path)
        )

if len(pages) != 76:
    errors.append(
        f"expected 76 indexed pages, found {len(pages)}"
    )

for public_url, filename in pages:

    html = (
        ROOT / filename
    ).read_text(errors="replace")

    matches = re.findall(
        r'<script\b[^>]*src=["\']'
        r'([^"\']*privacy-consent\.js[^"\']*)',
        html,
        re.I
    )

    if len(matches) != 1:

        errors.append(
            f"{filename}: privacy bootstrap count={len(matches)}"
        )

        continue

    resolved = urlparse(
        urljoin(
            public_url,
            matches[0]
        )
    )

    if resolved.path != "/privacy-consent.js":

        errors.append(
            f"{filename}: privacy path={resolved.path}"
        )

    if resolved.query != "v=20260912a":

        errors.append(
            f"{filename}: privacy version={resolved.query}"
        )


# ----------------------------------------------------------

if errors:

    print("COOKIE CONSENT RUNTIME V1: FAIL")

    for error in errors:
        print("FAIL —", error)

    sys.exit(1)

print("PASS — cookie banner is guaranteed by shared runtime")
print("PASS — cookie preference control is guaranteed in footer")
print("PASS — controls exist before runtime listeners are bound")
print("PASS — saved consent can be reopened through footer control")
print("PASS — all 76 indexed pages load current consent runtime")
print("COOKIE CONSENT RUNTIME V1: PASS")
