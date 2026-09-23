#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys


ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")

PAIRS = (
    ("index.html", "en/index.html", "https://sistema90g.it/", "https://sistema90g.it/en/"),
    ("chi-e-sistema90g.html", "en/about.html", "https://sistema90g.it/chi-e-sistema90g", "https://sistema90g.it/en/about"),
    ("analisi-preventiva.html", "en/how-it-works.html", "https://sistema90g.it/analisi-preventiva", "https://sistema90g.it/en/how-it-works"),
    ("servizi.html", "en/services.html", "https://sistema90g.it/servizi", "https://sistema90g.it/en/services"),
    ("metodo-sistema90g.html", "en/method.html", "https://sistema90g.it/metodo-sistema90g", "https://sistema90g.it/en/method"),
    ("contatti.html", "en/contact.html", "https://sistema90g.it/contatti", "https://sistema90g.it/en/contact"),
    ("progettare-cucina-guide.html", "en/kitchen-guides.html", "https://sistema90g.it/progettare-cucina-guide", "https://sistema90g.it/en/kitchen-guides"),
    ("domande-cucina-faq.html", "en/kitchen-faq.html", "https://sistema90g.it/domande-cucina-faq", "https://sistema90g.it/en/kitchen-faq"),
    ("casi-analizzati.html", "en/real-kitchen-cases.html", "https://sistema90g.it/casi-analizzati", "https://sistema90g.it/en/real-kitchen-cases"),
    ("caso-lavastoviglie-passaggio-cucina.html", "en/case-dishwasher-passage.html", "https://sistema90g.it/caso-lavastoviglie-passaggio-cucina", "https://sistema90g.it/en/case-dishwasher-passage"),
    ("caso-isola-passaggi-cucina.html", "en/case-kitchen-island-clearances.html", "https://sistema90g.it/caso-isola-passaggi-cucina", "https://sistema90g.it/en/case-kitchen-island-clearances"),
    ("caso-preventivo-cucina-sconto-valore.html", "en/case-kitchen-quote-discount-value.html", "https://sistema90g.it/caso-preventivo-cucina-sconto-valore", "https://sistema90g.it/en/case-kitchen-quote-discount-value"),
    ("consulenza-90g.html", "en/kitchen-consultation.html", "https://sistema90g.it/consulenza-90g", "https://sistema90g.it/en/kitchen-consultation"),
    ("analisi-preventivo-cucina.html", "en/kitchen-quote-order-review.html", "https://sistema90g.it/analisi-preventivo-cucina", "https://sistema90g.it/en/kitchen-quote-order-review"),
    ("verifica-90g.html", "en/kitchen-review.html", "https://sistema90g.it/verifica-90g", "https://sistema90g.it/en/kitchen-review"),
    ("progetto-cucina-sistema90g.html", "en/kitchen-design.html", "https://sistema90g.it/progetto-cucina-sistema90g", "https://sistema90g.it/en/kitchen-design"),
    ("controllo-pre-montaggio-cucina.html", "en/pre-installation-check.html", "https://sistema90g.it/controllo-pre-montaggio-cucina", "https://sistema90g.it/en/pre-installation-check"),
    ("analisi-problema-cucina.html", "en/kitchen-problem-analysis.html", "https://sistema90g.it/analisi-problema-cucina", "https://sistema90g.it/en/kitchen-problem-analysis"),
    ("esempio-progetto-cucina-90g.html", "en/kitchen-design-example.html", "https://sistema90g.it/esempio-progetto-cucina-90g", "https://sistema90g.it/en/kitchen-design-example"),
    ("esempio-verifica-cucina-90g.html", "en/kitchen-review-example.html", "https://sistema90g.it/esempio-verifica-cucina-90g", "https://sistema90g.it/en/kitchen-review-example"),
)


class AlternateParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.alternates: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() != "link":
            return

        data = {str(k).lower(): v for k, v in attrs}

        if str(data.get("rel", "")).lower() != "alternate":
            return

        lang = data.get("hreflang")
        href = data.get("href")

        if lang and href:
            self.alternates[str(lang)] = str(href)


def alternates(path: Path) -> dict[str, str]:
    parser = AlternateParser()
    parser.feed(path.read_text("utf-8", errors="strict"))
    return parser.alternates


errors: list[str] = []

if not ROOT.is_dir():
    raise SystemExit(
        f"ERRORE: directory pubblica non trovata: {ROOT}"
    )

for it_file, en_file, it_url, en_url in PAIRS:
    it_path = ROOT / it_file
    en_path = ROOT / en_file

    if not it_path.is_file():
        errors.append(f"{it_file}: pagina IT mancante")
        continue

    if not en_path.is_file():
        errors.append(f"{en_file}: pagina EN mancante")
        continue

    it_alts = alternates(it_path)
    en_alts = alternates(en_path)

    expected = {
        "it-IT": it_url,
        "en-GB": en_url,
        "x-default": it_url,
    }

    for lang, url in expected.items():
        if it_alts.get(lang) != url:
            errors.append(
                f"{it_file}: hreflang {lang}="
                f"{it_alts.get(lang)!r}, atteso {url!r}"
            )

        if en_alts.get(lang) != url:
            errors.append(
                f"{en_file}: hreflang {lang}="
                f"{en_alts.get(lang)!r}, atteso {url!r}"
            )

if errors:
    print("HREFLANG CONTRACT: FAIL")

    for error in errors:
        print("FAIL —", error)

    raise SystemExit(1)

print("PASS — 20 coppie IT/EN hanno hreflang reciproco")
print("PASS — x-default resta sulla versione italiana")
print("HREFLANG CONTRACT: PASS")
