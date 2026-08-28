#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

CLUSTERS = {
    'isola': {
        'case': 'caso-isola-passaggi-cucina.html',
        'guide': 'isola-cucina-distanze-passaggi.html',
        'guide_label': 'Guida isola: distanze, passaggi e aperture',
        'hub': 'progettare-cucina-guide.html',
        'hub_label': 'Hub progettazione cucina',
    },
    'lavastoviglie': {
        'case': 'caso-lavastoviglie-passaggio-cucina.html',
        'guide': 'lavastoviglie-cucina-aperture-passaggi.html',
        'guide_label': 'Guida lavastoviglie: aperture e passaggi',
        'hub': 'elettrodomestici-impianti-cucina-guide.html',
        'hub_label': 'Hub elettrodomestici e impianti',
    },
    'lavello-finestra': {
        'case': 'caso-lavello-sotto-finestra-aperture.html',
        'guide': 'lavello-sotto-finestra-cucina.html',
        'guide_label': 'Guida lavello sotto finestra',
        'hub': 'progettare-cucina-guide.html',
        'hub_label': 'Hub progettazione cucina',
    },
    'cucina-piccola': {
        'case': 'caso-cucina-piccola-tre-lati.html',
        'guide': 'cucina-piccola-come-progettarla.html',
        'guide_label': 'Guida cucina piccola',
        'hub': 'progettare-cucina-guide.html',
        'hub_label': 'Hub progettazione cucina',
    },
    'profondita-75': {
        'case': 'caso-cucina-profondita-75-angolo.html',
        'guide': 'profondita-cucina-75-cm.html',
        'guide_label': 'Guida profondità cucina 75 cm',
        'hub': 'progettare-cucina-guide.html',
        'hub_label': 'Hub progettazione cucina',
    },
    'preventivo-sconto': {
        'case': 'caso-preventivo-cucina-sconto-valore.html',
        'guide': 'sconto-cucina-valore-reale.html',
        'guide_label': 'Guida sconto e valore reale',
        'hub': 'preventivo-acquisto-cucina-guide.html',
        'hub_label': 'Hub preventivo e acquisto cucina',
    },
}

changed: list[str] = []


def public_url(filename: str) -> str:
    if not filename.endswith('.html'):
        raise ValueError(filename)
    return '/' + filename[:-5]


def inject(path: Path, block: str, marker: str) -> None:
    text = path.read_text('utf-8', errors='strict')
    if marker in text:
        return
    if '</main>' not in text:
        raise SystemExit(f'ERRORE: </main> non trovato in {path.name}')
    path.write_text(text.replace('</main>', block + '</main>', 1), 'utf-8')
    changed.append(path.name)


for cluster, data in CLUSTERS.items():
    case_path = root / data['case']
    guide_path = root / data['guide']
    hub_path = root / data['hub']
    for path in (case_path, guide_path, hub_path):
        if not path.is_file():
            raise SystemExit(f'ERRORE: pagina cluster mancante: {path.name}')

    case_marker = f'data-s90g-cluster-path="case:{cluster}"'
    case_block = (
        f'<p class="s90g-trust" {case_marker}><strong>Percorso tematico:</strong> '
        f'<a href="{public_url(data["guide"])}">{data["guide_label"]}</a> · '
        f'<a href="{public_url(data["hub"])}">{data["hub_label"]}</a></p>'
    )
    inject(case_path, case_block, case_marker)

    guide_marker = f'data-s90g-cluster-path="guide:{cluster}"'
    guide_block = (
        f'<p class="s90g-trust" {guide_marker}><strong>Percorso tematico:</strong> '
        f'<a href="{public_url(data["hub"])}">{data["hub_label"]}</a> · '
        f'<a href="{public_url(data["case"])}">Caso reale correlato</a></p>'
    )
    inject(guide_path, guide_block, guide_marker)

print('Cluster contenuti pubblici integrati: ' + (', '.join(changed) if changed else 'gia presenti'))
