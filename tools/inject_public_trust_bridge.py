#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

HOME_BLOCK = '''<section class="s90g-section" data-s90g-trust-bridge="home"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">Perché fidarti</p><h2>Dietro Sistema 90G ci sono una persona, un metodo e casi che puoi verificare.</h2><p>Il sito non ti chiede di fidarti di una promessa generica: puoi controllare chi c'è dietro il lavoro, come vengono letti i problemi e quali casi sono già stati analizzati.</p></div></div><div class="s90g-route-grid"><article class="s90g-route-card"><h3>Chi c'è dietro</h3><p>Sistema 90G è fondato da Gian Carlo Primo, con esperienza maturata tra progettazione, vendita, montaggio e post-vendita nel settore arredamento, oggi concentrata esclusivamente sulla cucina.</p><a class="s90g-link" href="/chi-e-sistema90g.html">Conosci chi c'è dietro Sistema 90G →</a></article><article class="s90g-route-card"><h3>Indipendenza verificabile</h3><p>Sistema 90G non vende cucine, non rappresenta marchi e non riceve provvigioni sulla vendita. Il rivenditore resta il soggetto che rende la soluzione definitiva e ordinabile.</p><a class="s90g-link" href="/metodo-sistema90g.html">Leggi metodo e limiti →</a></article><article class="s90g-route-card"><h3>Problemi reali, non solo promesse</h3><p>Passaggi, aperture, isole, elettrodomestici e preventivi sono mostrati attraverso casi anonimizzati che permettono di vedere quali criteri vengono applicati.</p><a class="s90g-link" href="/casi-analizzati.html">Guarda i casi analizzati →</a></article></div></div></section>'''

FREE_ENTRY_BLOCK = '''<section class="s90g-dark-band" data-s90g-trust-bridge="free-entry"><div class="s90g-shell"><p class="s90g-eyebrow">Prima di mostrare il tuo caso</p><h2>Puoi verificare chi c'è dietro Sistema 90G prima di inviare materiale.</h2><p>Sistema 90G è fondato da Gian Carlo Primo. L'esperienza maturata tra progettazione, vendita, montaggio e post-vendita viene oggi applicata esclusivamente alle cucine. Il sito rende consultabili anche casi reali anonimizzati, metodo di lavoro e limiti del ruolo.</p><div class="s90g-actions"><a class="s90g-button" href="/chi-e-sistema90g.html"><span>Chi c'è dietro Sistema 90G</span><span>→</span></a><a class="s90g-button" href="/casi-analizzati.html"><span>Guarda casi reali</span><span>→</span></a></div></div></section>'''


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

print('Trust bridge pubblico integrato: ' + (', '.join(changed) if changed else 'gia presente'))
