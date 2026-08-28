#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

HUBS = {
    'progettazione': ('progettare-cucina-guide.html', [
        'progetto-cucina-planner-online-prima-ordine.html', 'errori-progetto-cucina.html',
        'isola-cucina-distanze-passaggi.html', 'misure-passaggi-cucina.html',
        'cucina-piccola-come-progettarla.html', 'cucina-open-space-tavolo-passaggi.html',
        'tavolo-vicino-cucina-spazi-sedute.html', 'penisola-cucina-distanze-passaggi.html',
        'lavello-sotto-finestra-cucina.html', 'profondita-cucina-75-cm.html',
        'cucina-ad-angolo-guida.html', 'piano-lavoro-colonne-cucina.html',
        'illuminazione-cucina-progetto.html', 'progettare-cucina-prima-impianti.html',
        'vincoli-verticali-cucina-pensili-colonne-finestre.html',
        'lavello-una-o-due-vasche-gocciolatoio.html',
    ]),
    'preventivo-acquisto': ('preventivo-acquisto-cucina-guide.html', [
        'rilievo-misure-cucina-prima-ordine.html', 'montaggio-allacciamenti-cucina-cosa-chiarire.html',
        'preventivo-cucina-guida.html', 'confrontare-due-preventivi-cucina.html',
        'prima-di-firmare-ordine-cucina.html', 'voci-escluse-preventivo-cucina.html',
        'sconto-cucina-valore-reale.html', 'quando-verifica-indipendente-cucina.html',
        'pareti-fuori-squadra-cucina.html',
    ]),
    'elettrodomestici-impianti': ('elettrodomestici-impianti-cucina-guide.html', [
        'frigorifero-cucina-vicino-parete.html', 'lavastoviglie-cucina-aperture-passaggi.html',
        'piano-induzione-cucina.html', 'colonna-forno-microonde-cucina.html',
        'elettrodomestici-incasso-misure-cucina.html', 'cappa-aspirazione-cucina.html',
        'prese-impianti-cucina.html', 'altezza-pensili-spazio-top-cucina.html',
        'elettrodomestici-rivenditore-o-acquisto-separato.html',
        'frigorifero-incasso-o-libera-installazione.html',
        'piano-induzione-aspirazione-integrata-o-cappa.html',
    ]),
    'materiali-finiture': ('materiali-finiture-cucina-guide.html', [
        'top-cucina-materiali-guida.html', 'ante-cucina-materiali-manutenzione.html',
        'finiture-opache-lucide-cucina.html', 'cucina-chiara-scura-luce.html',
        'abbinare-cucina-pavimento.html',
    ]),
}

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


all_guides: list[str] = []
for hub_key, (hub_file, guides) in HUBS.items():
    hub_path = root / hub_file
    if not hub_path.is_file():
        issues.append(f'{hub_key}: hub mancante: {hub_file}')
        continue
    hub_text = hub_path.read_text('utf-8', errors='strict')
    for guide in guides:
        all_guides.append(guide)
        guide_path = root / guide
        if not guide_path.is_file():
            issues.append(f'{hub_key}: guida mancante: {guide}')
            continue
        if f'href="{url(guide)}"' not in hub_text:
            issues.append(f'{hub_file}: non collega {guide}')
        guide_text = guide_path.read_text('utf-8', errors='strict')
        pilot = next((name for name, values in CLUSTERS.items() if values[1] == guide), None)
        if pilot:
            marker = f'data-s90g-cluster-path="guide:{pilot}"'
        else:
            marker = f'data-s90g-guide-hub="{hub_key}"'
        if guide_text.count(marker) != 1:
            issues.append(f'{guide}: marker hub canonico duplicato o mancante')
        if f'href="{url(hub_file)}"' not in guide_text:
            issues.append(f'{guide}: non collega il proprio hub {hub_file}')

if len(all_guides) != len(set(all_guides)):
    issues.append('una o piu guide sono assegnate a piu hub canonici')
if len(all_guides) != 41:
    issues.append(f'attese 41 guide specifiche, trovate {len(all_guides)} nella mappa')

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
        if f'href="{url(case_file)}"' not in text:
            issues.append(f'{guide_file}: non collega il caso reale {case_file}')
        if text.count(marker) != 1:
            issues.append(f'{guide_file}: marker cluster guide duplicato o mancante')

sitemap = root / 'guide-cucina-sitemap.xml'
if not sitemap.is_file():
    issues.append('guide-cucina-sitemap.xml mancante')
else:
    text = sitemap.read_text('utf-8', errors='strict')
    locs = re.findall(r'<loc>https://sistema90g\.it([^<]+)</loc>', text)
    expected = {url(hub_file) for hub_file, _ in HUBS.values()} | {url(guide) for guide in all_guides}
    actual = set(locs)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing:
            issues.append('sitemap guide: URL mancanti: ' + ', '.join(missing))
        if extra:
            issues.append('sitemap guide: URL inattesi: ' + ', '.join(extra))

if issues:
    print('ERRORE: contratto cluster contenuti non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print('OK public content clusters contract: 4 hub + 41 guide + 6 casi reali, sitemap editoriale completa')
