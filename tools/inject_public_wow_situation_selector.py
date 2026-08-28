#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
page = root / 'index.html'
if not page.is_file():
    raise SystemExit('ERRORE: index.html mancante')

text = page.read_text('utf-8', errors='strict')
if 'data-s90g-wow-situation-selector="true"' in text:
    print('WOW situation selector gia presente')
    raise SystemExit(0)

anchor = '<section class="s90g-section"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">Gli strumenti, se servono</p>'
if anchor not in text:
    raise SystemExit('ERRORE: punto di inserimento Home non trovato')

section = '''<section class="s90g-section" data-s90g-wow-situation-selector="true"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">Cosa stai cercando di capire?</p><h2>Parti dalla situazione, non dal nome del servizio.</h2><p>Scegli il dubbio che assomiglia di più al tuo. Se nessuno coincide, puoi comunque raccontare liberamente il problema nella valutazione iniziale gratuita.</p></div></div><div class="s90g-route-grid"><article class="s90g-route-card"><h3>Ho già un progetto o un preventivo</h3><p>Vuoi capire se passaggi, aperture, composizione o voci economiche meritano un controllo.</p><a class="s90g-link" href="/quando-verifica-indipendente-cucina">Vedi cosa controllare →</a></article><article class="s90g-route-card"><h3>Sto valutando isola o penisola</h3><p>Il dubbio riguarda distanze, sgabelli, aperture o spazio che resta durante l'uso.</p><a class="s90g-link" href="/isola-cucina-distanze-passaggi">Guarda i criteri →</a></article><article class="s90g-route-card"><h3>Devo confrontare due preventivi</h3><p>Vuoi rendere comparabili prodotti, lavorazioni, inclusioni ed esclusioni prima di decidere.</p><a class="s90g-link" href="/confrontare-due-preventivi-cucina">Come confrontarli →</a></article><article class="s90g-route-card"><h3>Devo scegliere materiali o finiture</h3><p>Il problema è decidere tra alternative concrete senza fermarsi solo all'effetto estetico.</p><a class="s90g-link" href="/materiali-finiture-cucina-guide">Esplora le scelte →</a></article><article class="s90g-route-card"><h3>La cucina è già montata</h3><p>Vuoi capire se conviene intervenire su finiture, componenti o elettrodomestici senza rifare tutto.</p><a class="s90g-link" href="/rinnovare-cucina-senza-cambiarla">Valuta il rinnovo →</a></article><article class="s90g-route-card"><h3>Non so come definire il problema</h3><p>Non serve classificarlo da solo: descrivi cosa non ti convince e allega ciò che hai.</p><a class="s90g-link" href="/analisi-preventiva#richiedi">Racconta il problema →</a></article></div></div></section>'''

text = text.replace(anchor, section + anchor, 1)
page.write_text(text, 'utf-8')
print('WOW situation selector integrato: Home')
