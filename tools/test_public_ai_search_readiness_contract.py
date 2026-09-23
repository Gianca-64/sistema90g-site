#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

RETIRED_REDIRECTS = {
    "/professionisti": "/servizi",
    "/professionisti.html": "/servizi",
    "/professionisti-progetto-cucina": "/progetto-cucina-sistema90g",
    "/professionisti-progetto-cucina.html": "/progetto-cucina-sistema90g",
    "/agenzie-immobiliari-cucina": "/analisi-preventiva",
    "/agenzie-immobiliari-cucina.html": "/analisi-preventiva",
    "/rivenditori-cucine": "/metodo-sistema90g",
    "/rivenditori-cucine.html": "/metodo-sistema90g",
    "/rivenditori-veneta-cucine": "/metodo-sistema90g",
    "/rivenditori-veneta-cucine.html": "/metodo-sistema90g",
    "/controllo-progetto-cucina": "/verifica-90g",
    "/controllo-progetto-cucina.html": "/verifica-90g",
    "/seconda-opinione-cucina": "/verifica-90g",
    "/seconda-opinione-cucina.html": "/verifica-90g",
    "/controllo-mirato": "/verifica-90g",
    "/controllo-mirato.html": "/verifica-90g",
    "/analisi-completa": "/verifica-90g",
    "/analisi-completa.html": "/verifica-90g",
    "/sviluppo-avanzato-progetto-cucina": "/progetto-cucina-sistema90g",
    "/sviluppo-avanzato-progetto-cucina.html": "/progetto-cucina-sistema90g",
    "/acquisto-assistito-cucina": "/progetto-preventivo-cucina-90g",
    "/acquisto-assistito-cucina.html": "/progetto-preventivo-cucina-90g",
    "/scelta-finiture-cucina": "/consulenza-90g",
    "/scelta-finiture-cucina.html": "/consulenza-90g",
    "/restyling-cucina-esistente": "/analisi-preventiva#richiedi",
    "/restyling-cucina-esistente.html": "/analisi-preventiva#richiedi",
    "/esempio-fascicolo-cucina": "/esempio-progetto-cucina-90g",
    "/esempio-fascicolo-cucina.html": "/esempio-progetto-cucina-90g",
}

OBSOLETE_PUBLIC_TOKENS = (
    "Progetto Cucina 90G · 145 €",
    "Verifica 90G · 127 €",
    "Progetto & Preventivo Cucina 90G · 185 €",
    "Progetto & Preventivo 90G · 185 €",
    "Sviluppo avanzato · +117 €",
    "Sviluppo avanzato · +145 €",
    "Acquisto Assistito · 290 €",
    "Verifica professionale progetto cucina · 150 €",
    "<title>Supporto cucina per professionisti",
    "Per rivenditori e showroom",
)

SITEMAPS = (
    "sitemap.xml",
    "guide-cucina-sitemap.xml",
    "en-sitemap.xml",
)


def parse_redirects(path: Path) -> dict[str, tuple[str, str]]:
    rules: dict[str, tuple[str, str]] = {}

    for raw in path.read_text("utf-8").splitlines():
        stripped = raw.strip()

        if not stripped or stripped.startswith("#"):
            continue

        parts = stripped.split()

        if len(parts) < 3:
            continue

        source, target, status = parts[:3]

        if source in rules:
            raise RuntimeError(
                f"redirect duplicato per {source}"
            )

        rules[source] = (target, status)

    return rules


def source_for_url(url: str) -> Path:
    parsed = urlparse(url)

    if parsed.scheme != "https" or parsed.netloc not in {
        "sistema90g.it",
        "www.sistema90g.it",
    }:
        raise ValueError(f"URL fuori dominio: {url}")

    public_path = unquote(parsed.path)

    if public_path in ("", "/"):
        relative = Path("index.html")
    else:
        relative_text = public_path.lstrip("/").rstrip("/")

        if not relative_text:
            relative = Path("index.html")
        elif Path(relative_text).suffix:
            relative = Path(relative_text)
        else:
            relative = Path(relative_text + ".html")

    source = ROOT / relative

    if not source.is_file():
        raise FileNotFoundError(
            f"nessun sorgente per {url}: atteso {relative}"
        )

    return source


def git_last_modified(source: Path) -> str:
    relative = source.relative_to(ROOT)
    completed = subprocess.run(
        [
            "git",
            "log",
            "-1",
            "--format=%cs",
            "--",
            str(relative),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    value = completed.stdout.strip()

    if not value:
        raise RuntimeError(
            f"data Git assente per {relative}"
        )

    return value


errors: list[str] = []

if not TARGET.is_dir():
    raise SystemExit(
        f"ERRORE: directory pubblica non trovata: {TARGET}"
    )

robots = TARGET / "robots.txt"

if not robots.is_file():
    errors.append("robots.txt mancante")
else:
    text = robots.read_text("utf-8")

    if not re.search(
        r"(?ms)^User-agent:\s*OAI-SearchBot\s*$.*?^Allow:\s*/\s*$",
        text,
    ):
        errors.append(
            "robots.txt: OAI-SearchBot non esplicitamente consentito"
        )

    for sitemap_url in (
        "https://sistema90g.it/sitemap.xml",
        "https://sistema90g.it/guide-cucina-sitemap.xml",
        "https://sistema90g.it/en-sitemap.xml",
        "https://sistema90g.it/image-sitemap.xml",
    ):
        if f"Sitemap: {sitemap_url}" not in text:
            errors.append(
                f"robots.txt: sitemap non dichiarata {sitemap_url}"
            )

redirects = TARGET / "_redirects"

if not redirects.is_file():
    errors.append("_redirects mancante")
else:
    try:
        rules = parse_redirects(redirects)
    except RuntimeError as exc:
        errors.append(str(exc))
        rules = {}

    for source, expected_target in RETIRED_REDIRECTS.items():
        actual = rules.get(source)

        if actual is None:
            errors.append(
                f"_redirects: manca ritiro legacy {source}"
            )
            continue

        target, status = actual

        if target != expected_target or status != "301":
            errors.append(
                f"_redirects: {source} -> {target} {status}; "
                f"atteso {expected_target} 301"
            )

for source in RETIRED_REDIRECTS:
    if not source.endswith(".html"):
        continue

    public_file = TARGET / source.lstrip("/")

    if public_file.exists():
        errors.append(
            f"landing legacy ancora presente nel dist: {public_file.name}"
        )

for html in TARGET.rglob("*.html"):
    text = html.read_text("utf-8", errors="strict")

    for token in OBSOLETE_PUBLIC_TOKENS:
        if token in text:
            errors.append(
                f"{html.relative_to(TARGET)}: residuo legacy {token!r}"
            )

for sitemap_name in SITEMAPS:
    path = TARGET / sitemap_name

    if not path.is_file():
        errors.append(
            f"{sitemap_name}: sitemap mancante"
        )
        continue

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        errors.append(
            f"{sitemap_name}: XML non valido: {exc}"
        )
        continue

    for url_node in tree.getroot().findall(
        f"{{{SITEMAP_NS}}}url"
    ):
        loc_node = url_node.find(
            f"{{{SITEMAP_NS}}}loc"
        )
        lastmod_node = url_node.find(
            f"{{{SITEMAP_NS}}}lastmod"
        )

        if loc_node is None or not (loc_node.text or "").strip():
            errors.append(
                f"{sitemap_name}: <url> senza <loc>"
            )
            continue

        url = (loc_node.text or "").strip()

        for retired in RETIRED_REDIRECTS:
            retired_clean = retired.removesuffix(".html")
            if urlparse(url).path.rstrip("/") == retired_clean:
                errors.append(
                    f"{sitemap_name}: URL legacy presente {url}"
                )

        if lastmod_node is None or not (
            lastmod_node.text or ""
        ).strip():
            errors.append(
                f"{sitemap_name}: lastmod mancante per {url}"
            )
            continue

        actual_lastmod = (
            lastmod_node.text or ""
        ).strip()

        try:
            parsed_lastmod = date.fromisoformat(
                actual_lastmod
            )
        except ValueError:
            errors.append(
                f"{sitemap_name}: lastmod non ISO per "
                f"{url}: {actual_lastmod}"
            )
            continue

        if parsed_lastmod > date.today():
            errors.append(
                f"{sitemap_name}: lastmod futuro per "
                f"{url}: {actual_lastmod}"
            )

        try:
            source = source_for_url(url)
            expected_lastmod = git_last_modified(source)
        except (
            FileNotFoundError,
            RuntimeError,
            ValueError,
            subprocess.CalledProcessError,
        ) as exc:
            errors.append(
                f"{sitemap_name}: freshness non verificabile "
                f"per {url}: {exc}"
            )
            continue

        if actual_lastmod != expected_lastmod:
            errors.append(
                f"{sitemap_name}: lastmod stale per {url}: "
                f"{actual_lastmod}, atteso {expected_lastmod}"
            )

if errors:
    print("AI SEARCH READINESS CONTRACT: FAIL")

    for error in errors:
        print("FAIL —", error)

    raise SystemExit(1)

print("PASS — OAI-SearchBot e sitemap dichiarati")
print("PASS — landing B2B/offer legacy ritirate con 301")
print("PASS — vecchi prezzi e messaggi commerciali assenti dal dist")
print("PASS — sitemap prive di URL legacy")
print("PASS — lastmod sitemap sincronizzati con la storia Git")
print("AI SEARCH READINESS CONTRACT: PASS")
