#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")
MAX_IMAGE_BYTES = 1_000_000
SITE_HOSTS = {"sistema90g.it", "www.sistema90g.it"}
RASTER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif"}

if not root.is_dir():
    raise SystemExit(f"ERRORE: directory pubblica non trovata: {root}")


class ImageRefs(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[str] = []
        self.images: list[dict[str, str]] = []

    @staticmethod
    def attrs_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key.lower(): (value or "") for key, value in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = self.attrs_dict(attrs)
        tag = tag.lower()
        if tag == "img" and data.get("src"):
            self.refs.append(data["src"])
            self.images.append(data)
        elif tag == "meta":
            prop = data.get("property", "").lower()
            name = data.get("name", "").lower()
            if (prop == "og:image" or name == "twitter:image") and data.get("content"):
                self.refs.append(data["content"])

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def resolve_ref(page: Path, value: str) -> Path | None:
    value = value.strip()
    if not value or value.startswith(("data:", "//")):
        return None

    parsed = urlparse(value)
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return None
    if parsed.netloc and parsed.netloc not in SITE_HOSTS:
        return None

    clean_path = unquote(parsed.path)
    if not clean_path:
        return None

    if clean_path.startswith("/") or parsed.netloc:
        candidate = root / clean_path.lstrip("/")
    else:
        candidate = page.parent / clean_path

    try:
        resolved = candidate.resolve()
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


issues: list[str] = []
checked_refs = 0
unique_assets: dict[Path, int] = {}

for page in sorted(root.rglob("*.html")):
    parser = ImageRefs()
    parser.feed(page.read_text("utf-8", errors="ignore"))
    parser.close()

    for ref in parser.refs:
        asset = resolve_ref(page, ref)
        if asset is None or asset.suffix.lower() not in RASTER_EXTENSIONS:
            continue
        checked_refs += 1
        if not asset.is_file():
            continue

        size = asset.stat().st_size
        unique_assets[asset] = size
        if size > MAX_IMAGE_BYTES:
            rel_page = page.relative_to(root)
            rel_asset = asset.relative_to(root)
            issues.append(
                f"{rel_page} -> {rel_asset}: {size:,} byte "
                f"(limite {MAX_IMAGE_BYTES:,})"
            )

# P1 Home: solo l'immagine hero può partecipare al caricamento eager iniziale.
# Tutte le immagini successive devono usare il scheduling nativo lazy/async.
home = root / "index.html"
if home.is_file():
    home_parser = ImageRefs()
    home_parser.feed(home.read_text("utf-8", errors="ignore"))
    home_parser.close()

    hero_count = 0
    deferred_count = 0
    for image in home_parser.images:
        src = image.get("src", "")
        name = Path(urlparse(src).path).name
        if name == "01_HOME_HERO.jpg":
            hero_count += 1
            if image.get("loading", "").lower() == "lazy":
                issues.append("index.html: immagine hero non deve essere loading=lazy")
            continue

        deferred_count += 1
        if image.get("loading", "").lower() != "lazy":
            issues.append(f"index.html: immagine sotto-fold senza loading=lazy: {src}")
        if image.get("decoding", "").lower() != "async":
            issues.append(f"index.html: immagine sotto-fold senza decoding=async: {src}")

    if hero_count != 1:
        issues.append(f"index.html: attesa 1 immagine hero 01_HOME_HERO.jpg, trovate {hero_count}")
    if deferred_count == 0:
        issues.append("index.html: nessuna immagine sotto-fold trovata per il controllo scheduling")
else:
    issues.append("index.html: Home mancante per il controllo immagini")

if issues:
    print("ERRORE: contratto immagini pubbliche non rispettato:")
    for issue in issues:
        print(f" - {issue}")
    raise SystemExit(1)

largest = max(unique_assets.items(), key=lambda item: item[1], default=None)
if largest:
    rel_asset = largest[0].relative_to(root)
    largest_label = f"{rel_asset} ({largest[1]:,} byte)"
else:
    largest_label = "nessuna immagine raster locale"

print(
    "OK public image performance contract: "
    f"{checked_refs} riferimenti raster, {len(unique_assets)} asset unici; "
    f"Home hero eager + {deferred_count} immagini sotto-fold lazy/async; "
    f"massimo {largest_label}"
)
