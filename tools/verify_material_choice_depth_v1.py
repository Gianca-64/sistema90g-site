#!/usr/bin/env python3

from pathlib import Path
from html import unescape
import re
import sys


ROOT = Path(__file__).resolve().parents[1]

checks = {
    "abbinare-cucina-pavimento.html": {
        "required": [
            "Come fare un confronto utile",
            "luce naturale",
            "campioni reali",
            "colore, riflesso e texture",
        ],
        "min_words": 260,
    },

    "cucina-chiara-scura-luce.html": {
        "required": [
            "Valuta colore e volume insieme",
            "colonna scura",
            "luce naturale",
            "intera massa della composizione",
        ],
        "min_words": 260,
    },
}


errors = []


for filename, contract in checks.items():

    html = (
        ROOT / filename
    ).read_text(
        errors="replace"
    )

    main = re.search(
        r"<main\b[^>]*>([\s\S]*?)</main>",
        html,
        re.I
    )

    if not main:
        errors.append(
            f"{filename}: main missing"
        )
        continue

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

    if len(words) < contract["min_words"]:
        errors.append(
            f"{filename}: "
            f"{len(words)} words < {contract['min_words']}"
        )

    for marker in contract["required"]:

        if marker.lower() not in text.lower():
            errors.append(
                f"{filename}: missing {marker!r}"
            )

    if not re.search(
        r"\bluce naturale\b",
        text,
        re.I
    ):
        errors.append(
            f"{filename}: natural-light concept missing"
        )

    if not re.search(
        r"\bartificiale\b",
        text,
        re.I
    ):
        errors.append(
            f"{filename}: artificial-light concept missing"
        )


if errors:

    print(
        "MATERIAL CHOICE DEPTH V1: FAIL"
    )

    for error in errors:
        print(
            "FAIL —",
            error
        )

    sys.exit(1)


for filename in checks:

    print(
        f"PASS — {filename}: "
        "contextual comparison method present"
    )

print(
    "PASS — material guidance goes beyond isolated samples"
)

print(
    "MATERIAL CHOICE DEPTH V1: PASS"
)
