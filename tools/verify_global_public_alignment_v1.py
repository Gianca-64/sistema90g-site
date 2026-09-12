#!/usr/bin/env python3

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

nav_path = ROOT / "navigation-conversion.js"
privacy_path = ROOT / "privacy-consent.js"

nav = nav_path.read_text()
privacy = privacy_path.read_text()

errors = []

required_nav = [
    "['problems','Problemi da evitare','/#problemi']",
    "['cases','Casi reali','/casi-analizzati.html']",
    "['guides','Guide','/progettare-cucina-guide.html']",
    "['process','Come funziona','/analisi-preventiva.html']",
    "['services','Servizi e prezzi','/servizi.html']",
    "['about','Chi sono','/chi-e-sistema90g.html']",
    "VEDERE IL PROBLEMA PRIMA",
    "Mostra il tuo caso",
    "function normalizeHeaderCta()",
    "link.className='s90g-header-cta'",
    "inner.appendChild(link)",
    "/analisi-preventiva.html#richiedi",
    "MOSTRA IL TUO CASO",

    "const pageManaged=nav.dataset.s90gNavManaged==='page';",
]

for marker in required_nav:
    if marker not in nav:
        errors.append(
            f"shared navigation marker missing: {marker}"
        )

nav_block = re.search(
    r"const NAV_LINKS=\[(?:.|\n)*?\];",
    nav
)

if not nav_block:
    errors.append("NAV_LINKS block missing")
else:
    block = nav_block.group(0)

    for retired in (
        "Metodo 90G",
        "Innovazioni",
    ):
        if retired in block:
            errors.append(
                f"retired primary-nav item remains: {retired}"
            )

required_privacy = [
    "function s90gIntegrateMethodFooterLink()",
    "link.textContent='Metodo';",
]

for marker in required_privacy:
    if marker not in privacy:
        errors.append(
            f"shared footer marker missing: {marker}"
        )

for retired in (
    "s90gIntegrateAiTransparencyPage",
    "link.textContent='Metodo e AI';",
):
    if retired in privacy:
        errors.append(
            f"retired shared runtime behavior remains: {retired}"
        )

core_pages = [
    "index.html",
    "analisi-preventiva.html",
    "servizi.html",
    "casi-analizzati.html",
    "chi-e-sistema90g.html",
    "metodo-sistema90g.html",
]

for filename in core_pages:
    html = (ROOT / filename).read_text()

    if 'data-s90g-nav-managed="page"' not in html:
        errors.append(
            f"core page lost page-managed nav: {filename}"
        )

if errors:
    print("GLOBAL PUBLIC ALIGNMENT V1: FAIL")

    for error in errors:
        print("FAIL —", error)

    sys.exit(1)

print("PASS — canonical shared primary navigation defined")
print("PASS — Method and Innovazioni absent from primary shared nav")
print("PASS — Guide route exists in shared navigation")
print("PASS — canonical brand descriptor normalized at runtime")
print("PASS — customer-first CTA normalized at runtime")
print("PASS — Method remains accessible from footer")
print("PASS — old Metodo e AI runtime injection retired")
print("PASS — six core pages remain page-managed")
print("GLOBAL PUBLIC ALIGNMENT V1: PASS")
