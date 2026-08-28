#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')


def replace_exact(path: Path, old: str, new: str, label: str) -> bool:
    text = path.read_text('utf-8', errors='strict')
    if old not in text:
        raise SystemExit(f'ERRORE: conversion path non trovato ({label}) in {path.name}')
    updated = text.replace(old, new, 1)
    path.write_text(updated, 'utf-8')
    return updated != text


home = root / 'index.html'
servizi = root / 'servizi.html'
casi = root / 'casi-analizzati.html'
for path in (home, servizi, casi):
    if not path.is_file():
        raise SystemExit(f'ERRORE: pagina conversione mancante: {path.name}')

changes: list[str] = []

home_replacements = (
    ('<a class="s90g-link" href="/servizi">Scopri il Progetto →</a>',
     '<a class="s90g-link" href="/servizi#progetto">Scopri il Progetto →</a>', 'home progetto'),
    ('<a class="s90g-link" href="/servizi">Scopri la Verifica →</a>',
     '<a class="s90g-link" href="/servizi#verifica">Scopri la Verifica →</a>', 'home verifica'),
    ('<a class="s90g-link" href="/servizi">Scopri la Consulenza →</a>',
     '<a class="s90g-link" href="/servizi#consulenza">Scopri la Consulenza →</a>', 'home consulenza'),
)
for old, new, label in home_replacements:
    if replace_exact(home, old, new, label):
        changes.append(label)

service_replacements = (
    ('<section class="s90g-section" id="servizi">',
     '<section class="s90g-section" id="consulenza">', 'servizi consulenza'),
    ('<section class="s90g-dark-band"><div class="s90g-shell"><p class="s90g-eyebrow">Hai già progetto o preventivo</p>',
     '<section class="s90g-dark-band" id="verifica"><div class="s90g-shell"><p class="s90g-eyebrow">Hai già progetto o preventivo</p>', 'servizi verifica'),
    ('<section class="s90g-section"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">La cucina è ancora da impostare</p>',
     '<section class="s90g-section" id="progetto"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">La cucina è ancora da impostare</p>', 'servizi progetto'),
    ('href="#servizi"><span>Vedi servizi e prezzi</span>',
     'href="#consulenza"><span>Vedi servizi e prezzi</span>', 'servizi hero anchor'),
)
for old, new, label in service_replacements:
    if replace_exact(servizi, old, new, label):
        changes.append(label)

case_replacements = (
    ('Sistema 90G valuta pertinenza e tipo di bisogno; solo se serve un approfondimento viene indicato il servizio professionale con il relativo prezzo.',
     'Sistema 90G legge il materiale per capire che cosa merita davvero attenzione; solo se serve un approfondimento ti diciamo quale lavoro è utile e quanto costa.', 'casi bisogno'),
    ('Se il caso richiede un lavoro professionale, percorso, contenuti e prezzo vengono indicati prima di iniziare.',
     'Se il caso richiede un lavoro professionale, prima di iniziare sai che cosa verrà fatto e quanto costa.', 'casi finale'),
)
for old, new, label in case_replacements:
    if replace_exact(casi, old, new, label):
        changes.append(label)

print('Conversione pubblica normalizzata: ' + ', '.join(changes))
