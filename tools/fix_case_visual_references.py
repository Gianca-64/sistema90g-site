from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260703-visual4"

case_page_map = {
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

collection = ROOT / "casi-analizzati.html"
text = collection.read_text(encoding="utf-8")

for page_name, image_name in case_page_map.items():
    article_pattern = re.compile(
        r'<article>.*?<a class="text-link" href="' + re.escape(page_name) + r'">.*?</a></article>',
        re.S,
    )
    match = article_pattern.search(text)
    if not match:
        raise RuntimeError(f"Articolo non trovato per {page_name}")

    block = match.group(0)
    replacement = f'images/{image_name}?v={VERSION}'
    block, count = re.subn(
        r'(<img class="case-card-image" src=")[^"]+',
        rf'\1{replacement}',
        block,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"Immagine card non trovata per {page_name}")

    text = text[:match.start()] + block + text[match.end():]

text = re.sub(
    r'(<meta property="og:image" content=")[^"]+',
    rf'\1https://sistema90g.it/images/hero-casi-90g-2026.jpg?v={VERSION}',
    text,
    count=1,
)
text = re.sub(
    r'(<figure class="premium-image"><img src=")[^"]+',
    rf'\1images/hero-casi-90g-2026.jpg?v={VERSION}',
    text,
    count=1,
)

for image_name in case_page_map.values():
    expected = f'images/{image_name}?v={VERSION}'
    if text.count(expected) != 1:
        raise RuntimeError(f"Riferimento non univoco: {expected}")

collection.write_text(text, encoding="utf-8")
print("Riferimenti dei 15 casi corretti e verificati.")
