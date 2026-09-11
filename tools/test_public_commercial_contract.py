#!/usr/bin/env python3

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT


CANONICAL_PAGES = {
    "consulenza-90g.html": [
        "Consulenza 90G",
        "79 €",
    ],
    "analisi-preventivo-cucina.html": [
        "Analisi Preventivo",
        "129 €",
    ],
    "verifica-90g.html": [
        "Verifica Cucina 90G",
        "149 €",
    ],
    "progetto-cucina-sistema90g.html": [
        "Progetto Cucina 90G",
        "299 €",
    ],
    "controllo-pre-montaggio-cucina.html": [
        "Controllo Pre-Montaggio 90G",
        "179 €",
    ],
    "analisi-problema-cucina.html": [
        "Analisi Problema 90G",
        "149 €",
    ],
    "progetto-preventivo-cucina-90g.html": [
        "Progetto &amp; Preventivo 90G",
        "349 €",
    ],
}


SITEMAP_URLS = [
    "https://sistema90g.it/consulenza-90g.html",
    "https://sistema90g.it/analisi-preventivo-cucina.html",
    "https://sistema90g.it/verifica-90g.html",
    "https://sistema90g.it/progetto-cucina-sistema90g.html",
    "https://sistema90g.it/controllo-pre-montaggio-cucina.html",
    "https://sistema90g.it/analisi-problema-cucina.html",
    "https://sistema90g.it/progetto-preventivo-cucina-90g.html",
]


SERVICE_OFFER_TOKENS = [
    "Consulenza 90G · 79 €",
    "Analisi Preventivo &amp; Ordine 90G · 129 €",
    "Verifica Cucina 90G · 149 €",
    "Progetto Cucina 90G · 299 €",
    "Controllo Pre-Montaggio 90G · 179 €",
    "Analisi Problema 90G · 149 €",
    "Progetto &amp; Preventivo 90G · 349 €",
    "Render fotorealistico aggiuntivo · 39 € / vista",
]


OBSOLETE_OFFER_TOKENS = [
    "Progetto Cucina 90G · 145 €",
    "Verifica 90G · 127 €",
    "Progetto &amp; Preventivo Cucina 90G · 185 €",
    "+117 € ciascuno",
    "Acquisto Assistito · 290 €",
    "Analisi progetto cucina · 150 €",
]


errors = []


for name, required in CANONICAL_PAGES.items():
    path = TARGET / name

    if not path.is_file():
        errors.append(f"{name}: pagina canonica mancante")
        continue

    text = path.read_text("utf-8", errors="replace")

    for token in required:
        if token not in text:
            errors.append(
                f"{name}: manca contenuto canonico {token!r}"
            )


services = TARGET / "servizi.html"

if not services.is_file():
    errors.append("servizi.html: mancante")
else:
    text = services.read_text("utf-8", errors="replace")

    for token in SERVICE_OFFER_TOKENS:
        if token not in text:
            errors.append(
                f"servizi.html: offerta canonica assente {token!r}"
            )

    for token in OBSOLETE_OFFER_TOKENS:
        if token in text:
            errors.append(
                f"servizi.html: residuo offerta obsoleta {token!r}"
            )

    free_entry_links = (
        "/analisi-preventiva.html#richiedi",
        "/analisi-preventiva#richiedi",
    )

    if not any(link in text for link in free_entry_links):
        errors.append(
            "servizi.html: accesso Free Entry mancante"
        )


sitemap = TARGET / "sitemap.xml"

if not sitemap.is_file():
    errors.append("sitemap.xml: mancante")
else:
    sitemap_text = sitemap.read_text(
        "utf-8",
        errors="replace",
    )

    is_dist = TARGET.name == "dist"

    for source_url in SITEMAP_URLS:
        expected_url = (
            source_url.removesuffix(".html")
            if is_dist
            else source_url
        )

        if sitemap_text.count(expected_url) != 1:
            errors.append(
                "sitemap.xml: URL canonico non unico "
                f"{expected_url!r}"
            )

        alternate_url = (
            source_url
            if is_dist
            else source_url.removesuffix(".html")
        )

        if alternate_url != expected_url:
            exact_alternate = (
                f"<loc>{alternate_url}</loc>"
            )

            if exact_alternate in sitemap_text:
                errors.append(
                    "sitemap.xml: forma URL non canonica "
                    f"{alternate_url!r}"
                )


redirects = TARGET / "_redirects"

if not redirects.is_file():
    errors.append("_redirects: mancante")
else:
    redirects_text = redirects.read_text(
        "utf-8",
        errors="replace",
    )

    obsolete_redirect = (
        "/analisi-preventivo-cucina.html "
        "/seconda-opinione-cucina.html 301"
    )

    if obsolete_redirect in redirects_text:
        errors.append(
            "_redirects: Analisi Preventivo viene ancora "
            "deviata verso Seconda Opinione"
        )


for runtime_name in (
    "navigation-conversion.js",
    "privacy-consent.js",
):
    runtime = TARGET / runtime_name

    if not runtime.is_file():
        errors.append(f"{runtime_name}: mancante")
        continue

    text = runtime.read_text(
        "utf-8",
        errors="replace",
    )

    for slug in [
        "consulenza-90g",
        "analisi-preventivo-cucina",
        "verifica-90g",
        "progetto-cucina-sistema90g",
        "controllo-pre-montaggio-cucina",
        "analisi-problema-cucina",
        "progetto-preventivo-cucina-90g",
    ]:
        if slug not in text:
            errors.append(
                f"{runtime_name}: servizio canonico "
                f"non classificato {slug!r}"
            )


if errors:
    print("ERRORE public B2C commercial contract:")

    for error in errors:
        print(" -", error)

    raise SystemExit(1)


print(
    "OK public B2C commercial contract: "
    "sette servizi canonici + Free Entry + routing/runtime coerenti"
)
