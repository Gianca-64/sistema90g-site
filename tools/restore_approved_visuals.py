from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260703-approved2"

MAIN_HEROES = {
    "index.html": "homepage-approvata.svg",
    "controllo-progetto-cucina.html": "hero-cucina-conflitto-90g.jpg",
    "verifica-planimetria-distribuzione-casa.html": "hero-planimetria-90g.jpg",
    "analisi-preventivo-cucina.html": "hero-preventivo-90g.jpg",
    "casi-analizzati.html": "hero-analisi-90g.jpg",
    "chi-e-sistema90g.html": "hero-casa90g.jpg",
}

CASE_VISUALS = {
    "caso-lavastoviglie-passaggio-cucina.html": "hero-cucina-conflitto-90g.jpg",
    "caso-ingresso-tavolo-living.html": "hero-open-space-90g.jpg",
    "caso-cucina-piccola-tre-lati.html": "hero-progetto-zero-90g.jpg",
    "caso-preventivo-cucina-sconto-valore.html": "hero-preventivo-90g.jpg",
    "caso-isola-passaggi-cucina.html": "hero-cucina-conflitto-90g.jpg",
    "caso-secondo-bagno-impianti-spazio.html": "hero-casa90g.jpg",
    "caso-open-space-tv-divano-passaggi.html": "hero-open-space-90g.jpg",
    "caso-lavello-sotto-finestra-aperture.html": "hero-finiture-90g.jpg",
    "caso-scala-interna-terrazzo-planimetria.html": "hero-planimetria-90g.jpg",
    "caso-open-space-percorso-centrale.html": "hero-analisi-90g.jpg",
    "caso-terza-camera-zona-giorno.html": "hero-planimetria-90g.jpg",
    "caso-cucina-profondita-75-angolo.html": "hero-progetto-zero-90g.jpg",
    "caso-bagno-lavatrice-dieci-centimetri.html": "hero-casa90g.jpg",
    "caso-cabina-armadio-camera-irregolare.html": "hero-livelli-90g.jpg",
    "caso-divano-letto-soggiorno-tre-persone.html": "hero-open-space-90g.jpg",
}

for image in set(MAIN_HEROES.values()) | set(CASE_VISUALS.values()):
    path = ROOT / "images" / image
    if not path.exists():
        raise RuntimeError(f"Immagine approvata mancante: {path}")


def replace_first_hero(html: str, image: str) -> str:
    replacement = f'images/{image}?v={VERSION}'
    pattern = re.compile(
        r'(<section class="premium-hero">.*?<figure class="premium-image">\s*<img\s+src=")[^"]+',
        re.S,
    )
    html, count = pattern.subn(rf'\1{replacement}', html, count=1)
    if count != 1:
        raise RuntimeError("Hero principale non trovata")
    return html


for page_name, image in {**MAIN_HEROES, **CASE_VISUALS}.items():
    page = ROOT / page_name
    if not page.exists():
        continue
    html = page.read_text(encoding="utf-8")
    html = replace_first_hero(html, image)
    html = re.sub(
        r'(<meta property="og:image" content=")[^"]+',
        rf'\1https://sistema90g.it/images/{image}?v={VERSION}',
        html,
        count=1,
    )
    page.write_text(html, encoding="utf-8")

collection = ROOT / "casi-analizzati.html"
html = collection.read_text(encoding="utf-8")
for target, image in CASE_VISUALS.items():
    article = re.compile(
        r'(<article>.*?<a class="text-link" href="' + re.escape(target) + r'">.*?</a></article>)',
        re.S,
    )
    match = article.search(html)
    if not match:
        raise RuntimeError(f"Card non trovata: {target}")
    block = match.group(1)
    block, count = re.subn(
        r'(<img class="case-card-image" src=")[^"]+',
        rf'\1images/{image}?v={VERSION}',
        block,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"Immagine card non trovata: {target}")
    html = html[:match.start(1)] + block + html[match.end(1):]
collection.write_text(html, encoding="utf-8")

# Rimuove il codice che sostituiva nuovamente le immagini con i file schematici 2026.
site_ui = ROOT / "site-ui.js"
js = site_ui.read_text(encoding="utf-8")
marker = "  const visualVersion = '20260703-visual4';"
if marker in js:
    js = js.split(marker, 1)[0].rstrip() + "\n})();\n"
site_ui.write_text(js, encoding="utf-8")

# Verifica: nessun file schematico 2026 deve restare richiamato nell'HTML o nel JS.
problems = []
for page in ROOT.glob("*.html"):
    text = page.read_text(encoding="utf-8")
    if re.search(r'images/(?:hero|caso)-[^"\']+-2026\.jpg', text):
        problems.append(page.name)

if "-2026.jpg" in site_ui.read_text(encoding="utf-8"):
    problems.append("site-ui.js")

if problems:
    raise RuntimeError("Restano immagini schematiche richiamate in: " + ", ".join(problems))

print("Visual schematici rimossi; immagini approvate ripristinate.")
