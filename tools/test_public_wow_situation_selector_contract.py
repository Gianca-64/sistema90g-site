#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
page = root / 'index.html'
issues = []

if not page.is_file():
    issues.append('index.html: pagina mancante')
else:
    text = page.read_text('utf-8', errors='strict')
    if text.count('data-s90g-wow-situation-selector="true"') != 1:
        issues.append('index.html: selettore WOW mancante o duplicato')
    selector_required = [
        'Cosa stai cercando di capire?',
        'Ho già un progetto o un preventivo',
        'Sto valutando isola o penisola',
        'Devo confrontare due preventivi',
        'Devo scegliere materiali o finiture',
        'La cucina è già montata',
        'Non so come definire il problema',
        'href="/analisi-preventiva#richiedi"',
    ]
    for token in selector_required:
        if token not in text:
            issues.append(f'index.html: elemento selettore mancante: {token}')

    if text.count('data-s90g-wow-visual-proof="true"') != 1:
        issues.append('index.html: prova visuale WOW mancante o duplicata')
    proof_required = [
        'Guarda cosa vede Sistema 90G',
        'images/caso-lavastoviglie-passaggio-cucina.jpg',
        'images/caso-isola-passaggi-cucina.jpg',
        'Apertura reale', 'Passaggio residuo', 'Sedute in uso', 'Percorso operativo',
        'Conseguenza da verificare:',
        'href="/caso-lavastoviglie-passaggio-cucina"',
        'href="/caso-isola-passaggi-cucina"',
        's90g-wow-visual-proof.css',
    ]
    for token in proof_required:
        if token not in text:
            issues.append(f'index.html: elemento prova WOW mancante: {token}')
    if text.count('class="s90g-wow-proof-card"') != 2:
        issues.append('index.html: attese esattamente 2 prove visuali')

    forbidden = [
        'Scegli il servizio', 'Quale servizio vuoi',
        'service=progetto', 'service=verifica', 'service=consulenza',
        'passaggio sicuro di', 'distanza minima di', 'soluzione definitiva',
    ]
    for token in forbidden:
        if token in text:
            issues.append(f'index.html: componente WOW troppo prescrittivo/commerciale: {token}')

css = root / 's90g-wow-visual-proof.css'
if not css.is_file():
    issues.append('s90g-wow-visual-proof.css: asset mancante')

if issues:
    print('ERRORE: contratto WOW Home non rispettato:')
    for issue in issues:
        print(' -', issue)
    raise SystemExit(1)

print('OK public WOW Home: 6 situazioni problem-first + 2 casi visuali + 4 evidenze qualitative, no scelta servizio/soluzione completa')
