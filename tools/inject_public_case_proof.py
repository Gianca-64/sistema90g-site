#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

cases = {
    'caso-lavastoviglie-passaggio-cucina.html': ('Caso pratico cucina', 'Caso reale anonimizzato · cucina'),
    'caso-isola-passaggi-cucina.html': ('Caso pratico cucina', 'Caso reale anonimizzato · cucina'),
    'caso-lavello-sotto-finestra-aperture.html': ('Caso pratico cucina', 'Caso reale anonimizzato · cucina'),
    'caso-cucina-piccola-tre-lati.html': ('Caso pratico cucina', 'Caso reale anonimizzato · cucina'),
    'caso-cucina-profondita-75-angolo.html': ('Caso pratico cucina', 'Caso reale anonimizzato · cucina'),
    'caso-preventivo-cucina-sconto-valore.html': ('Caso pratico preventivo', 'Caso reale anonimizzato · preventivo cucina'),
}

changed: list[str] = []
for rel, (old_label, new_label) in cases.items():
    path = root / rel
    if not path.is_file():
        raise SystemExit(f'ERRORE: caso pubblico mancante: {rel}')
    text = path.read_text('utf-8', errors='ignore')
    if new_label in text:
        continue
    old = f'<p class="s90g-kicker">{old_label}</p>'
    new = f'<p class="s90g-kicker">{new_label}</p>'
    if old not in text:
        raise SystemExit(f'ERRORE: etichetta caso non trovata in {rel}: {old_label}')
    path.write_text(text.replace(old, new, 1), 'utf-8')
    changed.append(rel)

hub = root / 'casi-analizzati.html'
if not hub.is_file():
    raise SystemExit('ERRORE: casi-analizzati.html non trovato nella dist')
text = hub.read_text('utf-8', errors='ignore')
marker = 'data-s90g-case-proof-boundary="true"'
if marker not in text:
    anchor = '<p>I contenuti sono pubblicati in forma anonima e servono a rendere comprensibili i criteri di lettura. Non vengono utilizzati per mettere in discussione rivenditori o professionisti coinvolti nei singoli progetti.</p>'
    addition = anchor + '<p data-s90g-case-proof-boundary="true"><strong>Confine della prova pubblica:</strong> il caso mostra il criterio che ha fatto emergere il problema, ma non sostituisce la verifica del progetto, delle misure o del preventivo specifico della persona.</p>'
    if anchor not in text:
        raise SystemExit('ERRORE: punto di inserimento confine prova non trovato in casi-analizzati.html')
    hub.write_text(text.replace(anchor, addition, 1), 'utf-8')
    changed.append('casi-analizzati.html')

print('Prova casi pubblici integrata: ' + (', '.join(changed) if changed else 'gia presente'))
