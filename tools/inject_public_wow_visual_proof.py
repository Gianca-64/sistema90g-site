#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
page = root / 'index.html'
if not page.is_file():
    raise SystemExit('ERRORE: index.html mancante')

text = page.read_text('utf-8', errors='strict')
if 'data-s90g-wow-visual-proof="true"' in text:
    print('WOW visual proof gia presente')
    raise SystemExit(0)

selector_anchor = '<section class="s90g-section" data-s90g-wow-situation-selector="true">'
if selector_anchor not in text:
    raise SystemExit('ERRORE: selettore situazione WOW non trovato in Home')

if 's90g-wow-visual-proof.css' not in text:
    text = text.replace('</head>', '<link rel="stylesheet" href="s90g-wow-visual-proof.css"></head>', 1)

section = '''<section class="s90g-section" data-s90g-wow-visual-proof="true"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">Guarda cosa vede Sistema 90G</p><h2>Una cucina può sembrare corretta finché non la guardi durante l'uso.</h2><p>Questi due casi reali mostrano il tipo di attenzione che applichiamo: non la soluzione completa, ma il punto che merita verifica e la conseguenza pratica da non ignorare.</p></div></div><div class="s90g-wow-proof-grid"><article class="s90g-wow-proof-card"><figure class="s90g-wow-proof-figure"><img src="images/caso-lavastoviglie-passaggio-cucina.jpg" width="1400" height="933" loading="lazy" alt="Caso reale di cucina con lavastoviglie e passaggio da verificare"><span class="s90g-wow-proof-marker a" aria-hidden="true">Apertura reale</span><span class="s90g-wow-proof-marker b" aria-hidden="true">Passaggio residuo</span></figure><div class="s90g-wow-proof-copy"><p class="s90g-eyebrow">Caso reale anonimizzato</p><h3>Il corridoio sembra sufficiente. Poi si apre la lavastoviglie.</h3><p>La misura letta con i fronti chiusi non racconta tutto: conta cosa resta quando l'elettrodomestico è in uso e qualcuno deve attraversare la cucina.</p><p class="s90g-wow-proof-consequence"><strong>Conseguenza da verificare:</strong> un passaggio quotidiano può trasformarsi in un punto di blocco.</p><a class="s90g-link" href="/caso-lavastoviglie-passaggio-cucina">Guarda il caso completo →</a></div></article><article class="s90g-wow-proof-card"><figure class="s90g-wow-proof-figure"><img src="images/caso-isola-passaggi-cucina.jpg" width="1400" height="933" loading="lazy" alt="Caso reale di cucina con isola, sedute e percorsi da verificare"><span class="s90g-wow-proof-marker a" aria-hidden="true">Sedute in uso</span><span class="s90g-wow-proof-marker b" aria-hidden="true">Percorso operativo</span></figure><div class="s90g-wow-proof-copy"><p class="s90g-eyebrow">Caso reale anonimizzato</p><h3>L'isola entra nella stanza. Ma cosa succede quando la cucina viene vissuta?</h3><p>La presenza di sgabelli, ante aperte e persone in movimento può cambiare completamente lo spazio che sulla pianta sembrava libero.</p><p class="s90g-wow-proof-consequence"><strong>Conseguenza da verificare:</strong> l'isola può comprimere passaggi e funzioni anche se entra nelle misure.</p><a class="s90g-link" href="/caso-isola-passaggi-cucina">Guarda il caso completo →</a></div></article></div><div class="s90g-center-link"><a class="s90g-button primary" data-content-type="wow-visual-proof" data-cta-position="wow-proof" data-start-path="true" href="/analisi-preventiva#richiedi"><span>Vuoi sapere cosa emerge nel tuo progetto?</span><span>→</span></a></div><p class="s90g-trust">Gli esempi pubblici mostrano il criterio di attenzione e la conseguenza possibile, non sostituiscono una verifica sul materiale reale del tuo caso.</p></div></section>'''

page.write_text(text.replace(selector_anchor, section + selector_anchor, 1), 'utf-8')
print('WOW visual proof integrata: Home, 2 casi reali')
