#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import sys


ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")

AUTHOR_IMAGE = (
    "https://sistema90g.it/images/"
    "18_CHI_SONO_GIANCARLO_METODO.jpg"
)

PROFILES = {
    "chi-e-sistema90g.html": {
        "author_id": "https://sistema90g.it/chi-e-sistema90g#person",
        "profile_id": "https://sistema90g.it/chi-e-sistema90g#webpage",
        "url": "https://sistema90g.it/chi-e-sistema90g",
        "name": "Gian Carlo Primo",
    },
    "en/about.html": {
        "author_id": "https://sistema90g.it/en/about#person",
        "profile_id": "https://sistema90g.it/en/about#webpage",
        "url": "https://sistema90g.it/en/about",
        "name": "Gian Carlo Primo",
    },
}

CASES = {
    "caso-cucina-piccola-tre-lati.html": (
        "Aggiornato l'8 luglio 2026",
        "2026-07-08",
        PROFILES["chi-e-sistema90g.html"]["author_id"],
    ),
    "caso-cucina-profondita-75-angolo.html": (
        "Aggiornato l'8 luglio 2026",
        "2026-07-08",
        PROFILES["chi-e-sistema90g.html"]["author_id"],
    ),
    "caso-isola-passaggi-cucina.html": (
        "Aggiornato l'8 luglio 2026",
        "2026-07-08",
        PROFILES["chi-e-sistema90g.html"]["author_id"],
    ),
    "caso-lavastoviglie-passaggio-cucina.html": (
        "Aggiornato l'8 luglio 2026",
        "2026-07-08",
        PROFILES["chi-e-sistema90g.html"]["author_id"],
    ),
    "caso-lavello-sotto-finestra-aperture.html": (
        "Aggiornato l'8 luglio 2026",
        "2026-07-08",
        PROFILES["chi-e-sistema90g.html"]["author_id"],
    ),
    "caso-preventivo-cucina-sconto-valore.html": (
        "Aggiornato il 7 luglio 2026",
        "2026-07-07",
        PROFILES["chi-e-sistema90g.html"]["author_id"],
    ),
    "en/case-dishwasher-passage.html": (
        "Updated 8 July 2026",
        "2026-07-08",
        PROFILES["en/about.html"]["author_id"],
    ),
    "en/case-kitchen-island-clearances.html": (
        "Updated 8 July 2026",
        "2026-07-08",
        PROFILES["en/about.html"]["author_id"],
    ),
    "en/case-kitchen-quote-discount-value.html": (
        "Updated 7 July 2026",
        "2026-07-07",
        PROFILES["en/about.html"]["author_id"],
    ),
}

SCRIPT_RE = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>'
    r'(.*?)</script>',
    re.I | re.S,
)


def jsonld_nodes(path: Path) -> list[dict]:
    text = path.read_text("utf-8", errors="strict")
    nodes: list[dict] = []

    for raw in SCRIPT_RE.findall(text):
        data = json.loads(raw.strip())

        if isinstance(data, dict) and isinstance(
            data.get("@graph"),
            list,
        ):
            nodes.extend(
                node
                for node in data["@graph"]
                if isinstance(node, dict)
            )
        elif isinstance(data, dict):
            nodes.append(data)

    return nodes


def first_type(nodes: list[dict], type_name: str) -> dict | None:
    for node in nodes:
        value = node.get("@type")

        if value == type_name:
            return node

        if isinstance(value, list) and type_name in value:
            return node

    return None


errors: list[str] = []

if not ROOT.is_dir():
    raise SystemExit(
        f"ERRORE: directory pubblica non trovata: {ROOT}"
    )

for filename, expected in PROFILES.items():
    path = ROOT / filename

    if not path.is_file():
        errors.append(f"{filename}: pagina autore mancante")
        continue

    try:
        nodes = jsonld_nodes(path)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        errors.append(
            f"{filename}: JSON-LD non valido: {exc}"
        )
        continue

    person = first_type(nodes, "Person")
    profile = first_type(nodes, "ProfilePage")

    if person is None:
        errors.append(f"{filename}: Person mancante")
    else:
        if person.get("@id") != expected["author_id"]:
            errors.append(
                f"{filename}: Person @id non canonico"
            )

        if person.get("name") != expected["name"]:
            errors.append(
                f"{filename}: nome autore non canonico"
            )

        if person.get("url") != expected["url"]:
            errors.append(
                f"{filename}: URL autore non canonico"
            )

        if person.get("image") != AUTHOR_IMAGE:
            errors.append(
                f"{filename}: immagine autore mancante "
                "o non canonica"
            )

    if profile is None:
        errors.append(f"{filename}: ProfilePage mancante")
    else:
        if profile.get("@id") != expected["profile_id"]:
            errors.append(
                f"{filename}: ProfilePage @id non canonico"
            )

        if profile.get("url") != expected["url"]:
            errors.append(
                f"{filename}: ProfilePage URL non canonico"
            )

        main_entity = profile.get("mainEntity")

        if not isinstance(main_entity, dict) or (
            main_entity.get("@id") != expected["author_id"]
        ):
            errors.append(
                f"{filename}: ProfilePage non collega "
                "la Person canonica"
            )

for filename, (visible_date, iso_date, author_id) in CASES.items():
    path = ROOT / filename

    if not path.is_file():
        errors.append(f"{filename}: caso pubblico mancante")
        continue

    text = path.read_text("utf-8", errors="strict")

    if visible_date not in text:
        errors.append(
            f"{filename}: data visibile attesa assente "
            f"{visible_date!r}"
        )

    try:
        nodes = jsonld_nodes(path)
    except json.JSONDecodeError as exc:
        errors.append(
            f"{filename}: JSON-LD non valido: {exc}"
        )
        continue

    article = first_type(nodes, "Article")

    if article is None:
        errors.append(f"{filename}: Article JSON-LD mancante")
        continue

    if article.get("dateModified") != iso_date:
        errors.append(
            f"{filename}: dateModified "
            f"{article.get('dateModified')!r}, atteso {iso_date!r}"
        )

    author = article.get("author")

    if not isinstance(author, dict) or author.get("@id") != author_id:
        errors.append(
            f"{filename}: Article non collega la Person canonica"
        )

if errors:
    print("SOURCE IDENTITY CONTRACT: FAIL")

    for error in errors:
        print("FAIL —", error)

    raise SystemExit(1)

print("PASS — ProfilePage IT + EN collegano Gian Carlo Primo")
print("PASS — immagine e URL autore sono espliciti in entrambe le lingue")
print("PASS — nove casi IT/EN collegano la Person canonica")
print("PASS — dateModified coincidono con le date visibili")
print("SOURCE IDENTITY CONTRACT: PASS")
