#!/usr/bin/env python3

from pathlib import Path
from urllib.parse import urlparse
from collections import defaultdict
import posixpath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

errors = []

EXPECTED_EDGES = {
    "index.html":
        "/domande-cucina-faq.html",

    "elettrodomestici-impianti-cucina-guide.html":
        "/innovazioni.html",

    "sostituire-elettrodomestici-cucina-esistente.html":
        "/analisi-problema-cucina.html",

    "montaggio-allacciamenti-cucina-cosa-chiarire.html":
        "/controllo-pre-montaggio-cucina.html",

    "prima-di-firmare-ordine-cucina.html":
        "/progetto-cucina-planner-online-prima-ordine.html",

    "progetto-cucina-sistema90g.html":
        "/progetto-preventivo-cucina-90g.html",

    "progettare-cucina-guide.html":
        "/rinnovare-cucina-senza-cambiarla.html",

    "confrontare-due-preventivi-cucina.html":
        "/sconto-cucina-valore-reale.html",
}

TARGET_MIN_INLINKS = {
    "domande-cucina-faq.html": 1,
    "innovazioni.html": 4,
    "analisi-problema-cucina.html": 2,
    "controllo-pre-montaggio-cucina.html": 2,
    "progetto-cucina-planner-online-prima-ordine.html": 2,
    "progetto-preventivo-cucina-90g.html": 2,
    "rinnovare-cucina-senza-cambiarla.html": 2,
    "sconto-cucina-valore-reale.html": 2,
}

GENERIC = {
    "clicca qui",
    "qui",
    "leggi",
    "scopri",
    "approfondisci",
    "continua",
}


xml = (
    ROOT / "sitemap.xml"
).read_text(
    errors="replace"
)

urls = re.findall(
    r"<loc>\s*(.*?)\s*</loc>",
    xml,
    re.I
)

pages = []

for url in urls:

    path = urlparse(
        url
    ).path.lstrip("/")

    if not path:
        path = "index.html"

    if path.endswith(".html"):
        pages.append(path)

if len(pages) != 76:
    errors.append(
        f"expected 76 indexed pages, found {len(pages)}"
    )

known = set(pages)
incoming = defaultdict(set)


def resolve(source, href):

    parsed = urlparse(href)

    if (
        parsed.scheme
        or href.startswith(
            (
                "mailto:",
                "tel:",
                "#",
            )
        )
    ):
        return None

    path = parsed.path

    if not path:
        return None

    if path == "/":
        return "index.html"

    if path.startswith("/"):
        target = path.lstrip("/")

    else:
        target = posixpath.normpath(
            posixpath.join(
                posixpath.dirname(source),
                path,
            )
        )

    return (
        target
        if target in known
        else None
    )


for page in pages:

    html = (
        ROOT / page
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
            f"{page}: main missing"
        )
        continue

    body = main.group(1)

    for href, inner in re.findall(
        r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>'
        r'([\s\S]*?)</a>',
        body,
        re.I
    ):

        anchor = " ".join(
            re.sub(
                r"<[^>]+>",
                " ",
                inner
            ).split()
        ).lower()

        if anchor in GENERIC:
            errors.append(
                f"{page}: generic anchor {anchor!r}"
            )

        target = resolve(
            page,
            href
        )

        if (
            target
            and target != page
        ):
            incoming[target].add(
                page
            )


for source, href in EXPECTED_EDGES.items():

    html = (
        ROOT / source
    ).read_text(
        errors="replace"
    )

    main = re.search(
        r"<main\b[^>]*>([\s\S]*?)</main>",
        html,
        re.I
    )

    if not main:
        continue

    count = len(
        re.findall(
            rf'href=["\']{re.escape(href)}["\']',
            main.group(1),
            re.I
        )
    )

    if count != 1:
        errors.append(
            f"{source} -> {href}: "
            f"expected 1, found {count}"
        )


for target, minimum in TARGET_MIN_INLINKS.items():

    count = len(
        incoming[target]
    )

    if count < minimum:
        errors.append(
            f"{target}: "
            f"expected >= {minimum} main-content inlinks, "
            f"found {count}"
        )


if errors:

    print(
        "CONTEXTUAL INTERNAL LINKS V1: FAIL"
    )

    for error in errors:
        print(
            "FAIL —",
            error
        )

    sys.exit(1)


for target in TARGET_MIN_INLINKS:

    print(
        f"PASS — {target}: "
        f"{len(incoming[target])} main-content inlinks"
    )

print("PASS — exact eight contextual edges")
print("PASS — no generic low-value anchors")
print("CONTEXTUAL INTERNAL LINKS V1: PASS")
