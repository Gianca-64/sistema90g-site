#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

HUBS = {
    'progettazione': {
        'file': 'progettare-cucina-guide.html',
        'label': 'Hub progettazione cucina',
        'guides': [
            'progetto-cucina-planner-online-prima-ordine.html', 'errori-progetto-cucina.html',
            'isola-cucina-distanze-passaggi.html', 'misure-passaggi-cucina.html',
            'cucina-piccola-come-progettarla.html', 'cucina-open-space-tavolo-passaggi.html',
            'tavolo-vicino-cucina-spazi-sedute.html', 'penisola-cucina-distanze-passaggi.html',
            'lavello-sotto-finestra-cucina.html', 'profondita-cucina-75-cm.html',
            'cucina-ad-angolo-guida.html', 'piano-lavoro-colonne-cucina.html',
            'illuminazione-cucina-progetto.html', 'progettare-cucina-prima-impianti.html',
            'vincoli-verticali-cucina-pensili-colonne-finestre.html',
            'lavello-una-o-due-vasche-gocciolatoio.html',
        ],
    },
    'preventivo-acquisto': {
        'file': 'preventivo-acquisto-cucina-guide.html',
        'label': 'Hub preventivo e acquisto cucina',
        'guides': [
            'rilievo-misure-cucina-prima-ordine.html', 'montaggio-allacciamenti-cucina-cosa-chiarire.html',
            'preventivo-cucina-guida.html', 'confrontare-due-preventivi-cucina.html',
            'prima-di-firmare-ordine-cucina.html', 'voci-escluse-preventivo-cucina.html',
            'sconto-cucina-valore-reale.html', 'quando-verifica-indipendente-cucina.html',
            'pareti-fuori-squadra-cucina.html',
        ],
    },
    'elettrodomestici-impianti': {
        'file': 'elettrodomestici-impianti-cucina-guide.html',
        'label': 'Hub elettrodomestici e impianti',
        'guides': [
            'frigorifero-cucina-vicino-parete.html', 'lavastoviglie-cucina-aperture-passaggi.html',
            'piano-induzione-cucina.html', 'colonna-forno-microonde-cucina.html',
            'elettrodomestici-incasso-misure-cucina.html', 'cappa-aspirazione-cucina.html',
            'prese-impianti-cucina.html', 'altezza-pensili-spazio-top-cucina.html',
            'elettrodomestici-rivenditore-o-acquisto-separato.html',
            'frigorifero-incasso-o-libera-installazione.html',
            'piano-induzione-aspirazione-integrata-o-cappa.html',
        ],
    },
    'materiali-finiture': {
        'file': 'materiali-finiture-cucina-guide.html',
        'label': 'Hub materiali e finiture cucina',
        'guides': [
            'top-cucina-materiali-guida.html', 'ante-cucina-materiali-manutenzione.html',
            'finiture-opache-lucide-cucina.html', 'cucina-chiara-scura-luce.html',
            'abbinare-cucina-pavimento.html',
        ],
    },
}

CLUSTERS = {
    'isola': ('caso-isola-passaggi-cucina.html', 'isola-cucina-distanze-passaggi.html', 'Guida isola: distanze, passaggi e aperture', 'progettare-cucina-guide.html', 'Hub progettazione cucina'),
    'lavastoviglie': ('caso-lavastoviglie-passaggio-cucina.html', 'lavastoviglie-cucina-aperture-passaggi.html', 'Guida lavastoviglie: aperture e passaggi', 'elettrodomestici-impianti-cucina-guide.html', 'Hub elettrodomestici e impianti'),
    'lavello-finestra': ('caso-lavello-sotto-finestra-aperture.html', 'lavello-sotto-finestra-cucina.html', 'Guida lavello sotto finestra', 'progettare-cucina-guide.html', 'Hub progettazione cucina'),
    'cucina-piccola': ('caso-cucina-piccola-tre-lati.html', 'cucina-piccola-come-progettarla.html', 'Guida cucina piccola', 'progettare-cucina-guide.html', 'Hub progettazione cucina'),
    'profondita-75': ('caso-cucina-profondita-75-angolo.html', 'profondita-cucina-75-cm.html', 'Guida profondità cucina 75 cm', 'progettare-cucina-guide.html', 'Hub progettazione cucina'),
    'preventivo-sconto': ('caso-preventivo-cucina-sconto-valore.html', 'sconto-cucina-valore-reale.html', 'Guida sconto e valore reale', 'preventivo-acquisto-cucina-guide.html', 'Hub preventivo e acquisto cucina'),
}

changed: list[str] = []


def public_url(filename: str) -> str:
    return '/' + filename[:-5]


def inject(path: Path, block: str, marker: str) -> None:
    text = path.read_text('utf-8', errors='strict')
    if marker in text:
        return
    if '</main>' not in text:
        raise SystemExit(f'ERRORE: </main> non trovato in {path.name}')
    path.write_text(text.replace('</main>', block + '</main>', 1), 'utf-8')
    changed.append(path.name)


def ensure_hub_link(path: Path, key: str, guide: str) -> None:
    text = path.read_text('utf-8', errors='strict')
    if f'href="{public_url(guide)}"' in text:
        return
    marker = f'data-s90g-cluster-hub-link="{key}"'
    label = guide[:-5].replace('-', ' ')
    inject(path, f'<p class="s90g-trust" {marker}><strong>Approfondimento del cluster:</strong> <a href="{public_url(guide)}">{label}</a></p>', marker)


pilot_guides = {values[1] for values in CLUSTERS.values()}

for hub_key, hub in HUBS.items():
    hub_path = root / hub['file']
    if not hub_path.is_file():
        raise SystemExit(f'ERRORE: hub editoriale mancante: {hub_path.name}')
    for guide in hub['guides']:
        guide_path = root / guide
        if not guide_path.is_file():
            raise SystemExit(f'ERRORE: guida editoriale mancante: {guide_path.name}')
        ensure_hub_link(hub_path, f'{hub_key}:{guide[:-5]}', guide)
        if guide not in pilot_guides:
            marker = f'data-s90g-guide-hub="{hub_key}"'
            block = f'<p class="s90g-trust" {marker}><strong>Percorso tematico:</strong> <a href="{public_url(hub["file"])}">{hub["label"]}</a></p>'
            inject(guide_path, block, marker)

for cluster, (case_file, guide_file, guide_label, hub_file, hub_label) in CLUSTERS.items():
    case_path, guide_path, hub_path = root / case_file, root / guide_file, root / hub_file
    for path in (case_path, guide_path, hub_path):
        if not path.is_file():
            raise SystemExit(f'ERRORE: pagina cluster mancante: {path.name}')

    case_marker = f'data-s90g-cluster-path="case:{cluster}"'
    inject(case_path, f'<p class="s90g-trust" {case_marker}><strong>Percorso tematico:</strong> <a href="{public_url(guide_file)}">{guide_label}</a> · <a href="{public_url(hub_file)}">{hub_label}</a></p>', case_marker)

    guide_marker = f'data-s90g-cluster-path="guide:{cluster}"'
    inject(guide_path, f'<p class="s90g-trust" {guide_marker}><strong>Percorso tematico:</strong> <a href="{public_url(hub_file)}">{hub_label}</a> · <a href="{public_url(case_file)}">Caso reale correlato</a></p>', guide_marker)

print('Cluster contenuti pubblici integrati: ' + (', '.join(dict.fromkeys(changed)) if changed else 'gia presenti'))
