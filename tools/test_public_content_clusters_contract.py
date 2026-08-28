#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

CLUSTERS = {
    'isola': ('caso-isola-passaggi-cucina.html', 'isola-cucina-distanze-passaggi.html', 'progettare-cucina-guide.html'),
    'lavastoviglie': ('caso-lavastoviglie-passaggio-cucina.html', 'lavastoviglie-cucina-aperture-passaggi.html', 'elettrodomestici-impianti-cucina-guide.html'),
    'lavello-finestra': ('caso-lavello-sotto-finestra-aperture.html', 'lavello-sotto-finestra-cucina.html', 'progettare-cucina-guide.html'),
    'cucina-piccola': ('caso-cucina-piccola-tre-lati.html', 'cucina-piccola-come-progettarla.html', 'progettare-cucina-guide.html'),
    'profondita-75': ('caso-cucina-profondita-75-angolo.html', 'profondita-cucina-75-cm.html', 'progettare-cucina-guide.html'),
    'preventivo-sconto': ('caso-preventivo-cucina-sconto-valore.html', 'sconto-cucina-valore-reale.html', 'preventivo-acquisto-cucina-guide.html'),
}

issues: list[str] = []


def url(filename: str) -> str:
    return '/' + filename[:-5]


for cluster, (case_file, guide_file, hub_file) in CLUSTERS.items():
    case_path = root / case_file
    guide_path = root / guide_file
    hub_path = root / hub_file
    for path in (case_path, guide_path, hub_path):
        if not path.is_file():
            issues.append(f'{cluster}: pagina mancante: {path.name}')

    if case_path.is_file():
        text = case_path.read_text('utf-8', errors='strict')
        marker = f'data-s90g-cluster-path="case:{cluster}"'
        for token in (marker, f'href="{url(guide_file)}"', f'href="{url(hub_file)}"'):
            if token not in text:
                issues.append(f'{case_file}: manca {token}')
        if text.count(marker) != 1:
            issues.append(f'{case_file}: marker cluster case duplicato o mancante')

    if guide_path.is_file():
        text = guide_path.read_text('utf-8', errors='strict')
        marker = f'data-s90g-cluster-path="guide:{cluster}"'
        for token in (marker, f'href="{url(hub_file)}"', f'href="{url(case_file)}"'):
            if token not in text:
                issues.append(f'{guide_file}: manca {token}')
        if text.count(marker) != 1:
            issues.append(f'{guide_file}: marker cluster guide duplicato o mancante')

    if hub_path.is_file():
        text = hub_path.read_text('utf-8', errors='strict')
        if f'href="{url(guide_file)}"' not in text:
            issues.append(f'{hub_file}: non collega la guida {guide_file}')

if issues:
    print('ERRORE: contratto cluster contenuti non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public content clusters contract: 6 casi + 6 guide collegate ai rispettivi hub')
