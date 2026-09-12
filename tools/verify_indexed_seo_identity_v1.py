#!/usr/bin/env python3

from pathlib import Path
from urllib.parse import urlparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

OLD_JOB = (
    "Tecnico indipendente per analisi preventiva "
    "di progetti casa e cucina"
)

OLD_SITE = (
    "Analisi preventiva indipendente per progetti, "
    "spazi, preventivi e cucine."
)

CANONICAL_JOB = "Fondatore di Sistema 90G"

CANONICAL_SITE = (
    "Sistema 90G aiuta a individuare problemi, "
    "incongruenze e decisioni rischiose sulla cucina "
    "prima che diventino costosi o difficili da correggere."
)

CANONICAL_ORG = (
    "Sistema dedicato a problemi, verifiche "
    "e decisioni sulla cucina."
)

CASES = [
    "caso-cucina-piccola-tre-lati.html",
    "caso-cucina-profondita-75-angolo.html",
    "caso-isola-passaggi-cucina.html",
    "caso-lavastoviglie-passaggio-cucina.html",
    "caso-lavello-sotto-finestra-aperture.html",
    "caso-preventivo-cucina-sconto-valore.html",
]

errors = []

sitemap = (
    ROOT / "sitemap.xml"
).read_text(errors="replace")

urls = re.findall(
    r"<loc>\s*(.*?)\s*</loc>",
    sitemap,
    re.I
)

pages = []

for url in urls:
    path = urlparse(url).path.lstrip("/")

    if not path:
        path = "index.html"

    if path.endswith(".html"):
        pages.append(path)

# ----------------------------------------------------------
# No indexed JSON-LD may keep the exact retired global identity.
# ----------------------------------------------------------

for filename in pages:

    p = ROOT / filename

    if not p.exists():
        errors.append(
            f"sitemap file missing: {filename}"
        )
        continue

    html = p.read_text(errors="replace")

    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>'
        r'([\s\S]*?)</script>',
        html,
        re.I
    )

    joined = "\n".join(blocks)

    if OLD_JOB in joined:
        errors.append(
            f"retired Person identity in indexed JSON-LD: {filename}"
        )

    if OLD_SITE in joined:
        errors.append(
            f"retired WebSite identity in indexed JSON-LD: {filename}"
        )

# ----------------------------------------------------------
# Six canonical cases must carry the new identity statically.
# ----------------------------------------------------------

for filename in CASES:

    html = (
        ROOT / filename
    ).read_text(errors="replace")

    if CANONICAL_JOB not in html:
        errors.append(
            f"canonical Person identity missing: {filename}"
        )

    if CANONICAL_SITE not in html:
        errors.append(
            f"canonical WebSite identity missing: {filename}"
        )

    if "progetti casa e cucina" in html:
        errors.append(
            f"old house scope remains in canonical case: {filename}"
        )

# ----------------------------------------------------------
# Generator must not be able to reintroduce the legacy schema.
# ----------------------------------------------------------

generator = (
    ROOT / "tools/apply_ai_search_conformity.py"
).read_text(errors="replace")

if OLD_JOB in generator:
    errors.append(
        "structured-data generator still owns retired jobTitle"
    )

if OLD_SITE in generator:
    errors.append(
        "structured-data generator still owns retired website description"
    )

if CANONICAL_JOB not in generator:
    errors.append(
        "canonical Person identity missing from generator"
    )

if CANONICAL_SITE not in generator:
    errors.append(
        "canonical WebSite identity missing from generator"
    )

# ----------------------------------------------------------
# Runtime fallback must use the same public identity direction.
# ----------------------------------------------------------

privacy = (
    ROOT / "privacy-consent.js"
).read_text(errors="replace")

if OLD_JOB in privacy:
    errors.append(
        "runtime fallback still owns retired jobTitle"
    )

if CANONICAL_JOB not in privacy:
    errors.append(
        "canonical Person identity missing from runtime fallback"
    )

if CANONICAL_ORG not in privacy:
    errors.append(
        "canonical Organization identity missing from runtime fallback"
    )

# ----------------------------------------------------------

if errors:

    print("INDEXED SEO IDENTITY V1: FAIL")

    for error in errors:
        print("FAIL —", error)

    sys.exit(1)

print("PASS — indexed JSON-LD has no retired global Person identity")
print("PASS — indexed JSON-LD has no retired global WebSite identity")
print("PASS — six canonical cases carry new identity statically")
print("PASS — old house scope removed from canonical case schema")
print("PASS — schema generator cannot reintroduce retired identity")
print("PASS — runtime fallback uses canonical Person identity")
print("PASS — runtime fallback uses canonical Organization direction")
print("INDEXED SEO IDENTITY V1: PASS")
