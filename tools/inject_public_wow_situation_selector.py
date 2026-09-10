#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlsplit
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
page = root / 'index.html'
if not page.is_file():
    raise SystemExit('ERRORE: index.html mancante')

text = page.read_text('utf-8', errors='strict')
journey_marker = '<!-- S90G-CUSTOMER-JOURNEY-V1 -->'
selector_marker = 'data-s90g-wow-situation-selector="true"'

# La customer journey commerciale è ora parte del sorgente canonico della Home.
# La build non deve più iniettare un secondo selettore.
if journey_marker not in text and selector_marker not in text:
    raise SystemExit('ERRORE: customer journey V1 Home non trovata')

changed = []

if selector_marker not in text:
    journey_pos = text.find(journey_marker)
    section_start = text.find('<section', journey_pos)

    if section_start == -1:
        raise SystemExit('ERRORE: sezione customer journey V1 non trovata')

    section_end = text.find('>', section_start)

    if section_end == -1:
        raise SystemExit('ERRORE: tag customer journey V1 non valido')

    section_tag = text[section_start:section_end + 1]

    if 'id="servizi"' not in section_tag:
        raise SystemExit('ERRORE: customer journey V1 senza id servizi')

    marked_tag = (
        section_tag[:-1]
        + ' data-s90g-wow-situation-selector="true">'
    )

    text = (
        text[:section_start]
        + marked_tag
        + text[section_end + 1:]
    )

    changed.append('customer journey V1 riconosciuta')

if 'data-s90g-wow-visual-proof="true"' not in text:
    selector_anchor = '<section class="s90g-section" id="servizi" data-s90g-wow-situation-selector="true">'
    if selector_anchor not in text:
        raise SystemExit('ERRORE: selettore situazione WOW non trovato in Home')
    if 's90g-wow-visual-proof.css' not in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="s90g-wow-visual-proof.css"></head>', 1)
    proof = '''<section class="s90g-section" data-s90g-wow-visual-proof="true"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">Guarda cosa vede Sistema 90G</p><h2>Una cucina può sembrare corretta finché non la guardi durante l'uso.</h2><p>Non mostriamo soltanto la cucina: evidenziamo il dato, la situazione d'uso e la criticità che può sfuggire prima che diventi un errore difficile o costoso da correggere.</p></div></div><div class="s90g-wow-proof-grid"><article class="s90g-wow-proof-card"><figure class="s90g-wow-proof-figure"><img src="images/05_HOME_CASO_1.jpg" width="1400" height="933" loading="lazy" alt="Caso reale di cucina con lavastoviglie e passaggio da verificare"><span class="s90g-wow-proof-marker a" aria-hidden="true">Apertura reale</span><span class="s90g-wow-proof-marker b" aria-hidden="true">Passaggio residuo</span></figure><div class="s90g-wow-proof-copy"><p class="s90g-eyebrow">90G Focus · caso reale anonimizzato</p><h3>Il corridoio sembra sufficiente. Poi si apre la lavastoviglie.</h3><p>La misura letta con i fronti chiusi non racconta tutto: conta cosa resta quando l'elettrodomestico è in uso e qualcuno deve attraversare la cucina.</p><div class="s90g-wow-proof-lens" aria-label="Lettura Sistema 90G"><div class="s90g-wow-proof-step"><span>Dato</span><strong>Passaggio nominale</strong></div><div class="s90g-wow-proof-step"><span>Uso reale</span><strong>Lavastoviglie aperta</strong></div><div class="s90g-wow-proof-step"><span>Criticità</span><strong>Spazio residuo da verificare</strong></div></div><p class="s90g-wow-proof-consequence"><strong>Conseguenza da verificare:</strong> un passaggio quotidiano può trasformarsi in un punto di blocco.</p><a class="s90g-link" href="/caso-lavastoviglie-passaggio-cucina">Guarda il caso completo →</a></div></article><article class="s90g-wow-proof-card"><figure class="s90g-wow-proof-figure"><img src="images/caso-isola-passaggi-cucina.jpg" width="1400" height="933" loading="lazy" alt="Caso reale di cucina con isola, sedute e percorsi da verificare"><span class="s90g-wow-proof-marker a" aria-hidden="true">Sedute in uso</span><span class="s90g-wow-proof-marker b" aria-hidden="true">Percorso operativo</span></figure><div class="s90g-wow-proof-copy"><p class="s90g-eyebrow">90G Conflict · caso reale anonimizzato</p><h3>L'isola entra nella stanza. Ma cosa succede quando la cucina viene vissuta?</h3><p>La presenza di sgabelli, ante aperte e persone in movimento può cambiare completamente lo spazio che sulla pianta sembrava libero.</p><div class="s90g-wow-proof-lens" aria-label="Lettura Sistema 90G"><div class="s90g-wow-proof-step"><span>Dato</span><strong>Ingombro dell'isola</strong></div><div class="s90g-wow-proof-step"><span>Uso reale</span><strong>Sedute, ante e persone</strong></div><div class="s90g-wow-proof-step"><span>Criticità</span><strong>Percorsi che si sovrappongono</strong></div></div><p class="s90g-wow-proof-consequence"><strong>Conseguenza da verificare:</strong> l'isola può comprimere passaggi e funzioni anche se entra nelle misure.</p><a class="s90g-link" href="/caso-isola-passaggi-cucina">Guarda il caso completo →</a></div></article></div><div class="s90g-center-link"><a class="s90g-button primary" data-content-type="wow-visual-proof" data-cta-position="wow-proof" data-start-path="true" href="/analisi-preventiva#richiedi"><span>Vuoi sapere cosa emerge nel tuo progetto?</span><span>→</span></a></div><p class="s90g-trust">Gli esempi pubblici mostrano il criterio di attenzione e la conseguenza possibile, non sostituiscono una verifica sul materiale reale del tuo caso.</p></div></section>'''
    text = text.replace(selector_anchor, proof + selector_anchor, 1)
    changed.append('prova visuale')

# P1 performance Home: tutti questi fogli determinano il layout finale della Home.
# Li applichiamo nella stessa cascata fin dal primo render, evitando che audit-fix
# arrivi dopo DOMContentLoaded e costringa la hero a un secondo layout.
css_sources = [
    'sistema90g-visual-2026.css',
    's90g-offer-2026.css',
    's90g-wow-visual-proof.css',
    'sistema90g-audit-fix-20260707.css',
]
bundle_name = 's90g-home-critical.css'
for name in css_sources:
    if not (root / name).is_file():
        raise SystemExit(f'ERRORE: CSS Home sorgente mancante: {name}')

parts = []
for name in css_sources:
    css = (root / name).read_text('utf-8', errors='strict').rstrip()
    parts.append(f'/* bundled: {name} */\n{css}')
(root / bundle_name).write_text('\n\n'.join(parts) + '\n', 'utf-8')

link_re = re.compile(r'<link\b[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\'][^>]*>', re.I)
initial_sources = css_sources[:3]
source_tags = {name: [] for name in initial_sources}
for match in link_re.finditer(text):
    name = Path(urlsplit(match.group(1)).path).name
    if name in source_tags:
        source_tags[name].append(match.group(0))

bad = [name for name, tags in source_tags.items() if len(tags) != 1]
if bad:
    detail = ', '.join(f'{name}={len(source_tags[name])}' for name in bad)
    raise SystemExit(f'ERRORE: riferimenti CSS Home inattesi: {detail}')

# data-s90g-audit-fix fa sì che privacy-consent.js riconosca che sulla Home le
# correzioni audit sono già presenti e non aggiunga un secondo stylesheet a runtime.
text = text.replace(
    source_tags[initial_sources[0]][0],
    f'<link rel="stylesheet" href="/{bundle_name}" data-s90g-home-critical data-s90g-audit-fix>',
    1,
)
for name in initial_sources[1:]:
    text = text.replace(source_tags[name][0], '', 1)

# P1 performance immagini Home: la sola immagine hero resta eager. Tutte le altre
# immagini della Home sono sotto la prima viewport e non devono competere sulla rete
# iniziale; manteniamo dimensioni/markup e aggiungiamo soltanto scheduling nativo.
img_re = re.compile(r'<img\b[^>]*>', re.I)
src_re = re.compile(r'\bsrc=["\']([^"\']+)["\']', re.I)

def schedule_home_image(match: re.Match[str]) -> str:
    tag = match.group(0)
    src_match = src_re.search(tag)
    if not src_match:
        return tag
    name = Path(urlsplit(src_match.group(1)).path).name
    if name == '01_HOME_HERO.jpg':
        return tag
    if not re.search(r'\bloading\s*=', tag, re.I):
        tag = tag[:-1] + ' loading="lazy">'
    if not re.search(r'\bdecoding\s*=', tag, re.I):
        tag = tag[:-1] + ' decoding="async">'
    return tag

text = img_re.sub(schedule_home_image, text)
changed.append('immagini sotto-fold differite')

page.write_text(text, 'utf-8')
print('WOW Home integrata: ' + (', '.join(changed) if changed else 'gia completa') + '; CSS Home + audit-fix consolidati')
