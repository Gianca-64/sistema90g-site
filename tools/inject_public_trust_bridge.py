#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

HOME_BLOCK = '''<section class="s90g-section" data-s90g-trust-bridge="home"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">Perché fidarti</p><h2>Dietro Sistema 90G ci sono esperienza, un metodo e casi che puoi verificare.</h2><p>Il sito non ti chiede di fidarti di una promessa generica: puoi controllare come vengono letti i problemi, quali limiti vengono dichiarati e quali casi sono già stati analizzati.</p></div></div><div class="s90g-route-grid"><article class="s90g-route-card"><h3>Esperienza applicata alla cucina</h3><p>Sistema 90G nasce da esperienza diretta tra progettazione, vendita, montaggio e post-vendita nel settore arredamento, oggi concentrata esclusivamente sulla cucina.</p><a class="s90g-link" href="/chi-e-sistema90g.html">Scopri chi c'è dietro Sistema 90G →</a></article><article class="s90g-route-card"><h3>Indipendenza verificabile</h3><p>Sistema 90G non vende cucine, non rappresenta marchi e non riceve provvigioni sulla vendita. Il rivenditore resta il soggetto che rende la soluzione definitiva e ordinabile.</p><a class="s90g-link" href="/metodo-sistema90g.html">Leggi metodo e limiti →</a></article><article class="s90g-route-card"><h3>Problemi reali, non solo promesse</h3><p>Passaggi, aperture, isole, elettrodomestici e preventivi sono mostrati attraverso casi anonimizzati che permettono di vedere quali criteri vengono applicati.</p><a class="s90g-link" href="/casi-analizzati.html">Guarda i casi analizzati →</a></article></div></div></section>'''

FREE_ENTRY_BLOCK = '''<section class="s90g-dark-band" data-s90g-trust-bridge="free-entry"><div class="s90g-shell"><p class="s90g-eyebrow">Prima di mostrare il tuo caso</p><h2>Puoi verificare chi c'è dietro Sistema 90G prima di inviare materiale.</h2><p>Sistema 90G è fondato da Gian Carlo Primo. L'esperienza maturata tra progettazione, vendita, montaggio e post-vendita viene oggi applicata esclusivamente alle cucine. Il sito rende consultabili anche casi reali anonimizzati, metodo di lavoro e limiti del ruolo.</p><div class="s90g-actions"><a class="s90g-button" href="/chi-e-sistema90g.html"><span>Chi c'è dietro Sistema 90G</span><span>→</span></a><a class="s90g-button" href="/casi-analizzati.html"><span>Guarda casi reali</span><span>→</span></a></div></div></section>'''

CASE_LABELS = {
    'caso-lavastoviglie-passaggio-cucina.html': ('Caso pratico cucina', 'Caso reale anonimizzato · cucina'),
    'caso-isola-passaggi-cucina.html': ('Caso pratico cucina', 'Caso reale anonimizzato · cucina'),
    'caso-lavello-sotto-finestra-aperture.html': ('Caso pratico cucina', 'Caso reale anonimizzato · cucina'),
    'caso-cucina-piccola-tre-lati.html': ('Caso pratico cucina', 'Caso reale anonimizzato · cucina'),
    'caso-cucina-profondita-75-angolo.html': ('Caso pratico cucina', 'Caso reale anonimizzato · cucina'),
    'caso-preventivo-cucina-sconto-valore.html': ('Caso pratico preventivo', 'Caso reale anonimizzato · preventivo cucina'),
}


def inject_once(path: Path, marker: str, anchor: str, block: str, before: bool) -> bool:
    text = path.read_text('utf-8', errors='ignore')
    if marker in text:
        return False
    if anchor not in text:
        raise SystemExit(f'ERRORE: anchor trust bridge non trovato in {path.name}: {anchor}')
    replacement = block + anchor if before else anchor + block
    path.write_text(text.replace(anchor, replacement, 1), 'utf-8')
    return True

changed = []

home = root / 'index.html'
if not home.is_file():
    raise SystemExit('ERRORE: index.html non trovato nella dist')
if inject_once(home, 'data-s90g-trust-bridge="home"', '<section class="s90g-section"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">Prima il problema</p>', HOME_BLOCK, True):
    changed.append('index.html')

free_entry = root / 'analisi-preventiva.html'
if not free_entry.is_file():
    raise SystemExit('ERRORE: analisi-preventiva.html non trovato nella dist')
if inject_once(free_entry, 'data-s90g-trust-bridge="free-entry"', '<section class="s90g-section" id="richiedi">', FREE_ENTRY_BLOCK, True):
    changed.append('analisi-preventiva.html')

for rel, (old_label, new_label) in CASE_LABELS.items():
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

print('Trust e prova pubblica integrati: ' + (', '.join(changed) if changed else 'gia presenti'))
