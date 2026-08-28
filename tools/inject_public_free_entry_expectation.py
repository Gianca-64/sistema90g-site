#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

path = root / 'analisi-preventiva.html'
if not path.is_file():
    raise SystemExit('ERRORE: analisi-preventiva.html non trovato nella dist')

marker = 'data-s90g-free-entry-expectation="true"'
anchor = '<section class="s90g-section" id="richiedi">'
block = '''<section class="s90g-section" data-s90g-free-entry-expectation="true"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">Dopo l'invio</p><h2>Prima leggiamo il caso. Solo dopo capiamo se serve altro.</h2><p>Nel portale descrivi il dubbio e alleghi il materiale che possiedi già. La richiesta entra come valutazione iniziale gratuita: non stai acquistando un servizio e non devi scegliere in anticipo quale potrebbe servirti.</p></div></div><div class="s90g-route-grid"><article class="s90g-route-card"><p class="s90g-eyebrow">1</p><h3>Invii problema e materiale</h3><p>Racconti cosa vuoi capire e alleghi foto, progetto, preventivo, planimetria o misure se li hai già.</p></article><article class="s90g-route-card"><p class="s90g-eyebrow">2</p><h3>Facciamo la prima lettura</h3><p>Mettiamo a fuoco ciò che è già chiaro, ciò che manca e il punto che merita davvero attenzione.</p></article><article class="s90g-route-card"><p class="s90g-eyebrow">3</p><h3>Il passo successivo dipende dal caso</h3><p>Può bastare un chiarimento o un dato da recuperare. Se invece serve un lavoro professionale, prima di attivarlo sai cosa comprende e quanto costa.</p></article></div><p class="s90g-trust">La valutazione iniziale resta gratuita e non comporta alcun acquisto automatico.</p></div></section>'''

text = path.read_text('utf-8', errors='ignore')
if marker in text:
    print('Aspettativa Free Entry: gia presente')
    raise SystemExit(0)
if anchor not in text:
    raise SystemExit('ERRORE: punto #richiedi non trovato per aspettativa Free Entry')
path.write_text(text.replace(anchor, block + anchor, 1), 'utf-8')
print('Aspettativa Free Entry integrata: analisi-preventiva.html')
