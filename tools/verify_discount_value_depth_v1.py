#!/usr/bin/env python3

from pathlib import Path
from html import unescape
import re
import sys


ROOT = Path(__file__).resolve().parents[1]

PAGE = ROOT / "sconto-cucina-valore-reale.html"

errors = []

html = PAGE.read_text(
    errors="replace"
)

main = re.search(
    r"<main\b[^>]*>([\s\S]*?)</main>",
    html,
    re.I
)

if not main:

    print(
        "DISCOUNT VALUE DEPTH V1: FAIL"
    )

    print(
        "FAIL — main missing"
    )

    sys.exit(1)


text = " ".join(
    unescape(
        re.sub(
            r"<[^>]+>",
            " ",
            main.group(1)
        )
    ).split()
)

words = re.findall(
    r"\b[\wÀ-ÿ’'-]+\b",
    text
)


if len(words) < 330:
    errors.append(
        f"content depth too low: {len(words)} words"
    )


required = [
    "Prima rendi leggibile la proposta",
    "Quattro domande prima di giudicare lo sconto",
    "prezzo finale",
    "Che cosa comprende?",
    "Che cosa resta fuori?",
    "Il progetto è coerente con le tue priorità?",
    "uso reale della cucina",
]

for marker in required:

    if marker.lower() not in text.lower():
        errors.append(
            f"missing concept: {marker!r}"
        )


# Preserve the page's role:
# reading the value of one proposal, not ranking retailers.
for marker in (
    "lo sconto sia “vero” o “falso”",
    "che cosa stai acquistando",
    "quale valore ha per il tuo caso",
):

    if marker.lower() not in text.lower():
        errors.append(
            f"decision framing missing: {marker!r}"
        )


# The existing contextual links must remain.
links_required = [
    "/caso-preventivo-cucina-sconto-valore.html",
    "/confrontare-due-preventivi-cucina.html",
    "/analisi-preventiva.html",
]

for href in links_required:

    if not re.search(
        rf'href=["\']{re.escape(href)}(?:#[^"\']*)?["\']',
        main.group(1),
        re.I
    ):
        errors.append(
            f"required link missing: {href}"
        )


if errors:

    print(
        "DISCOUNT VALUE DEPTH V1: FAIL"
    )

    for error in errors:
        print(
            "FAIL —",
            error
        )

    sys.exit(1)


print(
    f"PASS — decision content depth: {len(words)} words"
)

print(
    "PASS — price, scope, exclusions and project coherence are separated"
)

print(
    "PASS — discount is framed as a decision input, not a verdict"
)

print(
    "PASS — case, comparison guide and Free Entry links preserved"
)

print(
    "DISCOUNT VALUE DEPTH V1: PASS"
)
