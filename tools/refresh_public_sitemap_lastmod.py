#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
SITEMAPS = ("sitemap.xml", "guide-cucina-sitemap.xml", "en-sitemap.xml")
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

ET.register_namespace("", SITEMAP_NS)


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
    elif public_path.endswith("/"):
        relative = Path(public_path.lstrip("/")) / "index.html"
    else:
        relative_text = public_path.lstrip("/")

        if Path(relative_text).suffix:
            relative = Path(relative_text)
        else:
            relative = Path(relative_text + ".html")

    source = ROOT / relative

    if not source.is_file():
        raise FileNotFoundError(
            f"nessun file sorgente per {url}: atteso {relative}"
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
            f"nessuna data Git disponibile per {relative}"
        )

    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise RuntimeError(
            f"data Git non valida per {relative}: {value}"
        ) from exc

    if parsed > date.today():
        raise RuntimeError(
            f"data Git futura per {relative}: {value}"
        )

    return value


def refresh_sitemap(path: Path) -> tuple[int, int]:
    tree = ET.parse(path)
    root = tree.getroot()

    updated = 0
    total = 0

    for url_node in root.findall(f"{{{SITEMAP_NS}}}url"):
        loc_node = url_node.find(f"{{{SITEMAP_NS}}}loc")

        if loc_node is None or not (loc_node.text or "").strip():
            raise RuntimeError(
                f"{path.name}: elemento <url> senza <loc>"
            )

        url = (loc_node.text or "").strip()
        source = source_for_url(url)
        expected = git_last_modified(source)

        lastmod_node = url_node.find(f"{{{SITEMAP_NS}}}lastmod")

        if lastmod_node is None:
            lastmod_node = ET.SubElement(
                url_node,
                f"{{{SITEMAP_NS}}}lastmod",
            )

        previous = (lastmod_node.text or "").strip()

        if previous != expected:
            lastmod_node.text = expected
            updated += 1

        total += 1

    ET.indent(tree, space="  ")
    tree.write(
        path,
        encoding="utf-8",
        xml_declaration=True,
        short_empty_elements=True,
    )

    return total, updated


if not TARGET.is_dir():
    raise SystemExit(
        f"ERRORE: directory pubblica non trovata: {TARGET}"
    )

grand_total = 0
grand_updated = 0

for sitemap_name in SITEMAPS:
    sitemap_path = TARGET / sitemap_name

    if not sitemap_path.is_file():
        raise SystemExit(
            f"ERRORE: sitemap pubblica mancante: {sitemap_name}"
        )

    try:
        total, updated = refresh_sitemap(sitemap_path)
    except (
        FileNotFoundError,
        RuntimeError,
        ValueError,
        subprocess.CalledProcessError,
        ET.ParseError,
    ) as exc:
        raise SystemExit(
            f"ERRORE freshness sitemap {sitemap_name}: {exc}"
        ) from exc

    grand_total += total
    grand_updated += updated

    print(
        f"SITEMAP FRESHNESS: {sitemap_name}: "
        f"{total} URL, {updated} lastmod aggiornati"
    )

print(
    "SITEMAP FRESHNESS PASS — "
    f"{grand_total} URL verificati, "
    f"{grand_updated} lastmod sincronizzati con Git"
)
