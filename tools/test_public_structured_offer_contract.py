#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import sys


ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")

EXPECTED = {
    "consulenza-90g.html": ("79", "EUR", "79 €"),
    "analisi-preventivo-cucina.html": ("129", "EUR", "129 €"),
    "verifica-90g.html": ("149", "EUR", "149 €"),
    "progetto-cucina-sistema90g.html": ("299", "EUR", "299 €"),
    "controllo-pre-montaggio-cucina.html": ("179", "EUR", "179 €"),
    "analisi-problema-cucina.html": ("149", "EUR", "149 €"),
    "progetto-preventivo-cucina-90g.html": ("349", "EUR", "349 €"),
    "en/kitchen-consultation.html": ("79", "EUR", "€79"),
    "en/kitchen-quote-order-review.html": ("129", "EUR", "€129"),
    "en/kitchen-review.html": ("149", "EUR", "€149"),
    "en/kitchen-design.html": ("299", "EUR", "€299"),
    "en/pre-installation-check.html": ("179", "EUR", "€179"),
    "en/kitchen-problem-analysis.html": ("149", "EUR", "€149"),
}

SCRIPT_RE = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>'
    r'(.*?)</script>',
    re.I | re.S,
)


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def offers(path: Path) -> list[dict]:
    text = path.read_text("utf-8", errors="strict")
    found: list[dict] = []

    for raw in SCRIPT_RE.findall(text):
        data = json.loads(raw.strip())

        for node in walk(data):
            node_type = node.get("@type")

            if node_type == "Offer" or (
                isinstance(node_type, list)
                and "Offer" in node_type
            ):
                found.append(node)

    return found


errors: list[str] = []

if not ROOT.is_dir():
    raise SystemExit(
        f"ERRORE: directory pubblica non trovata: {ROOT}"
    )

for filename, (price, currency, visible_price) in EXPECTED.items():
    path = ROOT / filename

    if not path.is_file():
        errors.append(f"{filename}: pagina servizio mancante")
        continue

    text = path.read_text("utf-8", errors="strict")

    if visible_price not in text:
        errors.append(
            f"{filename}: prezzo visibile atteso "
            f"{visible_price!r} assente"
        )

    try:
        page_offers = offers(path)
    except json.JSONDecodeError as exc:
        errors.append(
            f"{filename}: JSON-LD non valido: {exc}"
        )
        continue

    exact = [
        offer
        for offer in page_offers
        if str(offer.get("price")) == price
        and offer.get("priceCurrency") == currency
    ]

    if len(exact) != 1:
        errors.append(
            f"{filename}: attesa una sola Offer "
            f"{price} {currency}, trovate {len(exact)}"
        )

    conflicting = [
        offer
        for offer in page_offers
        if "price" in offer
        and (
            str(offer.get("price")) != price
            or offer.get("priceCurrency") != currency
        )
    ]

    if conflicting:
        errors.append(
            f"{filename}: Offer con prezzo/valuta "
            "in conflitto con il listino canonico"
        )

if errors:
    print("STRUCTURED OFFER CONTRACT: FAIL")

    for error in errors:
        print("FAIL —", error)

    raise SystemExit(1)

print("PASS — 13 servizi IT/EN hanno prezzo visibile canonico")
print("PASS — Offer JSON-LD coincide con prezzo e valuta visibili")
print("PASS — nessuna Offer confliggente nelle pagine servizio")
print("STRUCTURED OFFER CONTRACT: PASS")
