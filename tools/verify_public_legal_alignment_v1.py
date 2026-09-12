#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

errors = []


class VisibleParser(HTMLParser):

    def __init__(self):
        super().__init__()

        self.ignore = 0
        self.main = 0

        self.visible_main = []
        self.description = ""

    def handle_starttag(self, tag, attrs):

        attrs = dict(attrs)

        if tag in (
            "script",
            "style",
            "noscript",
        ):
            self.ignore += 1
            return

        if tag == "main":
            self.main += 1

        if (
            tag == "meta"
            and attrs.get(
                "name",
                ""
            ).lower()
            == "description"
        ):
            self.description = attrs.get(
                "content",
                ""
            )

    def handle_endtag(self, tag):

        if tag in (
            "script",
            "style",
            "noscript",
        ):
            if self.ignore:
                self.ignore -= 1
            return

        if tag == "main" and self.main:
            self.main -= 1

    def handle_data(self, data):

        if self.ignore:
            return

        if self.main:

            value = " ".join(
                data.split()
            )

            if value:
                self.visible_main.append(
                    value
                )


def parse(filename):

    html = (
        ROOT / filename
    ).read_text(
        errors="replace"
    )

    parser = VisibleParser()
    parser.feed(html)

    return (
        html,
        " ".join(
            parser.visible_main
        ),
        parser.description,
    )


privacy_html, privacy_main, privacy_desc = parse(
    "privacy-policy.html"
)

cookie_html, cookie_main, cookie_desc = parse(
    "cookie-policy.html"
)

contacts_html, contacts_main, contacts_desc = parse(
    "contatti.html"
)


# ----------------------------------------------------------
# Privacy Policy
# ----------------------------------------------------------

retired_privacy = [
    "ruolo professionale",
    "Richieste professionali",
    "Per professionisti e rivenditori",
    "Il pagamento non viene attualmente gestito nel portale",
    "pagamento attraverso il canale disponibile",
]

for marker in retired_privacy:

    if marker.lower() in privacy_main.lower():
        errors.append(
            f"Privacy retains retired contract: {marker}"
        )


required_privacy = [
    "Pagamento",
    "SumUp",
    "stato, importo e riferimento della transazione",
    "I dati completi della carta",
    "non vengono ricevuti o conservati da Sistema 90G",
    "Dati di terzi nei materiali",
    "verifica del pagamento tramite SumUp",
]

for marker in required_privacy:

    if marker.lower() not in privacy_main.lower():
        errors.append(
            f"Privacy missing current contract: {marker}"
        )


if re.search(
    r'\bprofessionist[aioe]*\b',
    privacy_main,
    re.I
):
    errors.append(
        "Privacy still addresses professionals as a public target"
    )


# ----------------------------------------------------------
# Cookie Policy
# ----------------------------------------------------------

if "ruolo suggerito" in cookie_main.lower():
    errors.append(
        "Cookie Policy still exposes role-based acquisition language"
    )

for marker in (
    "pagina di origine",
    "tipo di contenuto",
    "posizione del pulsante",
    "servizio eventualmente suggerito",
    "caso consultato",
    "Gestisci cookie",
):

    if marker.lower() not in cookie_main.lower():
        errors.append(
            f"Cookie Policy missing current wording: {marker}"
        )


# ----------------------------------------------------------
# Contacts
# ----------------------------------------------------------

contacts_public = (
    contacts_main
    + " "
    + contacts_desc
)

for marker in (
    "collaborazioni",
    "professionist",
    "rivenditor",
    "agenzi",
):

    if marker.lower() in contacts_public.lower():
        errors.append(
            f"Contacts retains non-B2C public target: {marker}"
        )


if (
    "per informazioni generali puoi scrivere via email"
    not in contacts_desc.lower()
):
    errors.append(
        "Contacts description not aligned with customer-only positioning"
    )


# ----------------------------------------------------------

if errors:

    print(
        "PUBLIC LEGAL ALIGNMENT V1: FAIL"
    )

    for error in errors:
        print(
            "FAIL —",
            error
        )

    sys.exit(1)


print("PASS — Privacy no longer exposes retired B2B role model")
print("PASS — Privacy describes current SumUp payment boundary")
print("PASS — full card data remains outside Sistema 90G")
print("PASS — third-party material rule is customer-neutral")
print("PASS — Cookie Policy no longer exposes role-based acquisition")
print("PASS — Cookie Policy describes current path parameters")
print("PASS — Contacts no longer targets collaborations/B2B")
print("PUBLIC LEGAL ALIGNMENT V1: PASS")
