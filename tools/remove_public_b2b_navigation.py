#!/usr/bin/env python3

from pathlib import Path
import re
import sys

ROOT = (
    Path(sys.argv[1])
    if len(sys.argv) > 1
    else Path("dist")
)

if not ROOT.is_dir():
    raise SystemExit(
        f"ERRORE: directory pubblica non trovata: {ROOT}"
    )

B2B_PATHS = {
    "/professionisti",
    "/professionisti.html",
    "/professionisti-progetto-cucina",
    "/professionisti-progetto-cucina.html",
    "/agenzie-immobiliari-cucina",
    "/agenzie-immobiliari-cucina.html",
    "/rivenditori-cucine",
    "/rivenditori-cucine.html",
    "/controllo-progetto-cucina",
    "/controllo-progetto-cucina.html",
}

anchor_re = re.compile(
    r'<a\b[^>]*\bhref=(["\'])(.*?)\1[^>]*>.*?</a>',
    re.I | re.S,
)

nav_re = re.compile(
    r'<nav\b[^>]*>.*?</nav>',
    re.I | re.S,
)

footer_re = re.compile(
    r'<div\b[^>]*class=(["\'])'
    r'[^"\']*\bs90g-footer-links\b[^"\']*'
    r'\1[^>]*>.*?</div>',
    re.I | re.S,
)


def normalized_path(href: str) -> str:
    value = href.strip()

    if not value:
        return value

    value = value.split("#", 1)[0]
    value = value.split("?", 1)[0]

    return value.rstrip("/") or "/"


def clean_region(region: str):
    removed = []

    def repl(match):
        href = normalized_path(match.group(2))

        if href in B2B_PATHS:
            removed.append(href)
            return ""

        return match.group(0)

    return anchor_re.sub(repl, region), removed


changed = []
removed_total = 0

for page in sorted(ROOT.rglob("*.html")):
    text = page.read_text(
        "utf-8",
        errors="replace",
    )

    original = text
    page_removed = []

    def nav_clean(match):
        cleaned, removed = clean_region(match.group(0))
        page_removed.extend(removed)
        return cleaned

    def footer_clean(match):
        cleaned, removed = clean_region(match.group(0))
        page_removed.extend(removed)
        return cleaned

    text = nav_re.sub(nav_clean, text)
    text = footer_re.sub(footer_clean, text)

    if text != original:
        page.write_text(text, "utf-8")
        changed.append(page.relative_to(ROOT).as_posix())
        removed_total += len(page_removed)

print(
    "B2B navigation sanitizer:",
    f"{len(changed)} pagine aggiornate,",
    f"{removed_total} link rimossi",
)
