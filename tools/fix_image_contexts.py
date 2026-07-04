from __future__ import annotations

from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260704-image-audit1"

# Una sola immagine, specifica per ciascun caso nella raccolta.
CASE_CARDS = {
    "caso-lavastoviglie-passaggio-cucina.html": "caso-lavastoviglie-passaggio-2026.jpg",
    "caso-ingresso-tavolo-living.html": "caso-ingresso-living-2026.jpg",
    "caso-cucina-piccola-tre-lati.html": "caso-cucina-tre-lati-2026.jpg",
    "caso-preventivo-cucina-sconto-valore.html": "caso-preventivo-valore-2026.jpg",
    "caso-isola-passaggi-cucina.html": "caso-isola-passaggi-2026.jpg",
    "caso-secondo-bagno-impianti-spazio.html": "caso-secondo-bagno-2026.jpg",
    "caso-open-space-tv-divano-passaggi.html": "caso-open-space-tv-2026.jpg",
    "caso-lavello-sotto-finestra-aperture.html": "caso-lavello-finestra-2026.jpg",
    "caso-scala-interna-terrazzo-planimetria.html": "caso-scala-planimetria-2026.jpg",
    "caso-open-space-percorso-centrale.html": "caso-percorso-centrale-2026.jpg",
    "caso-terza-camera-zona-giorno.html": "caso-terza-camera-2026.jpg",
    "caso-cucina-profondita-75-angolo.html": "caso-profondita-angolo-2026.jpg",
    "caso-bagno-lavatrice-dieci-centimetri.html": "caso-bagno-lavatrice-2026.jpg",
    "caso-cabina-armadio-camera-irregolare.html": "caso-cabina-armadio-2026.jpg",
    "caso-divano-letto-soggiorno-tre-persone.html": "caso-divano-letto-2026.jpg",
}

# Hero principali: ogni pagina usa il visual più vicino al contenuto dichiarato.
PAGE_HEROES = {
    "index.html": "homepage-approvata.svg",
    "analisi-preventiva.html": "hero-analisi-90g.jpg",
    "controllo-mirato.html": "90g-style-hero.svg",
    "analisi-completa.html": "90g-style-planimetria.svg",
    "progetto-da-zero.html": "hero-progetto-zero-90g.jpg",
    "chi-e-sistema90g.html": "hero-casa90g.jpg",
    "casi-analizzati.html": "hero-casi-90g-2026.jpg",
    "controllo-progetto-cucina.html": "hero-controllo-progetto-cucina.svg",
    "analisi-preventivo-cucina.html": "hero-analisi-preventivo-cucina.svg",
    "verifica-planimetria-distribuzione-casa.html": "hero-verifica-planimetria-casa.svg",
    "scelta-finiture-casa.html": "hero-scelta-finiture-casa.svg",
    "render-fotorealistici-interni.html": "90g-real-kitchen.svg",
    "agenzie-immobiliari.html": "hero-agenzie-90g.jpg",
    "caso-lavastoviglie-passaggio-cucina.html": "caso-lavastoviglie-passaggio.svg",
    "caso-ingresso-tavolo-living.html": "caso-ingresso-tavolo-living.svg",
    "caso-cucina-piccola-tre-lati.html": "caso-cucina-piccola-tre-lati.svg",
    "caso-preventivo-cucina-sconto-valore.html": "caso-preventivo-sconto-valore.svg",
    "caso-isola-passaggi-cucina.html": "caso-isola-passaggi-2026.jpg",
    "caso-secondo-bagno-impianti-spazio.html": "caso-secondo-bagno-2026.jpg",
    "caso-open-space-tv-divano-passaggi.html": "caso-open-space-tv-2026.jpg",
    "caso-lavello-sotto-finestra-aperture.html": "caso-lavello-finestra-2026.jpg",
    "caso-scala-interna-terrazzo-planimetria.html": "caso-scala-planimetria-2026.jpg",
    "caso-open-space-percorso-centrale.html": "caso-percorso-centrale-2026.jpg",
    "caso-terza-camera-zona-giorno.html": "caso-terza-camera-2026.jpg",
    "caso-cucina-profondita-75-angolo.html": "caso-profondita-angolo-2026.jpg",
    "caso-bagno-lavatrice-dieci-centimetri.html": "caso-bagno-lavatrice-10cm-90g.svg",
    "caso-cabina-armadio-camera-irregolare.html": "caso-cabina-armadio-camera-irregolare-90g.svg",
    "caso-divano-letto-soggiorno-tre-persone.html": "caso-divano-letto-soggiorno-tre-persone-90g.svg",
}

# Pagine che avevano due volte lo stesso visual: il secondo viene distinto e contestualizzato.
SECONDARY_IMAGES = {
    "index.html": ["90g-style-conflitto.svg"],
    "analisi-preventiva.html": ["90g-style-preventivo.svg"],
    "controllo-progetto-cucina.html": ["90g-style-conflitto.svg"],
    "analisi-preventivo-cucina.html": ["90g-real-preventivo.svg"],
    "verifica-planimetria-distribuzione-casa.html": ["hero-planimetria-90g.jpg"],
    "scelta-finiture-casa.html": ["90g-style-finiture.svg"],
    "render-fotorealistici-interni.html": ["hero-finiture-90g.jpg"],
    "agenzie-immobiliari.html": ["90g-style-agenzie.svg"],
    "professionisti.html": ["90g-style-planimetria.svg", "hero-verifica-planimetria-casa.svg"],
}


def image_src(asset: str) -> str:
    return f"images/{asset}?v={VERSION}"


def assert_asset(asset: str) -> None:
    if not (ROOT / "images" / asset).exists():
        raise RuntimeError(f"Immagine mancante: images/{asset}")


for asset in set(PAGE_HEROES.values()) | set(CASE_CARDS.values()):
    assert_asset(asset)
for assets in SECONDARY_IMAGES.values():
    for asset in assets:
        assert_asset(asset)


def replace_first_content_image(page: Path, asset: str) -> None:
    text = page.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(<main\b.*?<img\b[^>]*?\bsrc=["\'])[^"\']+(["\'])',
        re.I | re.S,
    )
    text, count = pattern.subn(rf'\1{image_src(asset)}\2', text, count=1)
    if count != 1:
        raise RuntimeError(f"Hero non trovata: {page.name}")
    text = re.sub(
        r'(<meta\s+property=["\']og:image["\']\s+content=["\'])[^"\']+(["\'])',
        rf'\1https://sistema90g.it/{image_src(asset)}\2',
        text,
        count=1,
        flags=re.I,
    )
    page.write_text(text, encoding="utf-8")


for page_name, asset in PAGE_HEROES.items():
    page = ROOT / page_name
    if page.exists():
        replace_first_content_image(page, asset)

# Corregge le quindici card senza riciclare alcun file nella stessa raccolta.
collection = ROOT / "casi-analizzati.html"
text = collection.read_text(encoding="utf-8")
for target, asset in CASE_CARDS.items():
    article_re = re.compile(
        r'<article>.*?<a\s+class=["\']text-link["\']\s+href=["\']' + re.escape(target) + r'["\']>.*?</a>\s*</article>',
        re.I | re.S,
    )
    match = article_re.search(text)
    if not match:
        raise RuntimeError(f"Card non trovata: {target}")
    block = match.group(0)
    block, count = re.subn(
        r'(<img\b[^>]*?\bclass=["\'][^"\']*case-card-image[^"\']*["\'][^>]*?\bsrc=["\'])[^"\']+',
        rf'\1{image_src(asset)}',
        block,
        count=1,
        flags=re.I | re.S,
    )
    if count != 1:
        # Gestisce anche l'ordine src prima di class.
        block, count = re.subn(
            r'(<img\b[^>]*?\bsrc=["\'])[^"\']+(["\'][^>]*?\bclass=["\'][^"\']*case-card-image)',
            rf'\1{image_src(asset)}\2',
            block,
            count=1,
            flags=re.I | re.S,
        )
    if count != 1:
        raise RuntimeError(f"Immagine card non trovata: {target}")
    text = text[:match.start()] + block + text[match.end():]
collection.write_text(text, encoding="utf-8")

# Sostituisce soltanto le immagini successive alla hero nelle pagine note.
img_re = re.compile(r'(<img\b[^>]*?\bsrc=["\'])[^"\']+(["\'])', re.I | re.S)
for page_name, assets in SECONDARY_IMAGES.items():
    page = ROOT / page_name
    if not page.exists():
        continue
    text = page.read_text(encoding="utf-8")
    matches = list(img_re.finditer(text))
    content_matches = [m for m in matches if "brand-mark" not in text[max(0, m.start()-180):m.start()]]
    # La prima immagine di contenuto è la hero, quindi si parte dalla seconda.
    for offset, asset in enumerate(assets, start=1):
        if offset >= len(content_matches):
            break
        m = content_matches[offset]
        text = text[:m.start(0)] + m.group(1) + image_src(asset) + m.group(2) + text[m.end(0):]
        # Ricalcola le posizioni dopo ogni sostituzione.
        matches = list(img_re.finditer(text))
        content_matches = [x for x in matches if "brand-mark" not in text[max(0, x.start()-180):x.start()]]
    page.write_text(text, encoding="utf-8")

# Elimina la vecchia sovrascrittura runtime: le immagini devono restare quelle dichiarate nell'HTML.
override = ROOT / "visual-reference-fix.js"
if override.exists():
    override.unlink()

# Verifica specifica raccolta: 15 card, 15 file distinti, target coerenti.
final_text = collection.read_text(encoding="utf-8")
seen: list[str] = []
for target, asset in CASE_CARDS.items():
    if final_text.count(image_src(asset)) != 1:
        raise RuntimeError(f"Riferimento non univoco nella raccolta: {asset}")
    seen.append(asset)
if len(seen) != len(set(seen)):
    raise RuntimeError("La mappa delle card contiene doppioni")

map_lines = [
    "# Mappa immagini pubblicate",
    "",
    "Ogni caso della raccolta usa un file distinto e collegato al problema descritto.",
    "",
    "| Caso | Immagine |",
    "|---|---|",
]
for target, asset in CASE_CARDS.items():
    map_lines.append(f"| `{target}` | `images/{asset}` |")
(ROOT / "IMAGE-MAP.md").write_text("\n".join(map_lines) + "\n", encoding="utf-8")

print("Abbinamento immagini completato: 15 card, 15 visual distinti.")
