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
    if text.count('data-s90g-wow-visual-proof="true"') != 1:
        issues.append('index.html: prova visuale WOW mancante o duplicata')
    required = [
        'Guarda cosa vede Sistema 90G',
        'images/caso-lavastoviglie-passaggio-cucina.jpg',
        'images/caso-isola-passaggi-cucina.jpg',
        'Apertura reale', 'Passaggio residuo', 'Sedute in uso', 'Percorso operativo',
        'Conseguenza da verificare:',
        'href="/caso-lavastoviglie-passaggio-cucina"',
        'href="/caso-isola-passaggi-cucina"',
        'href="/analisi-preventiva#richiedi"',
        's90g-wow-visual-proof.css',
    ]
    for token in required:
        if token not in text:
            issues.append(f'index.html: elemento prova WOW mancante: {token}')
    forbidden = [
        'passaggio sicuro di', 'distanza minima di', 'soluzione definitiva',
        'service=progetto', 'service=verifica', 'service=consulenza',
    ]
    for token in forbidden:
        if token in text:
            issues.append(f'index.html: prova WOW troppo prescrittiva/commerciale: {token}')
    if text.count('class="s90g-wow-proof-card"') != 2:
        issues.append('index.html: attese esattamente 2 prove visuali')

css = root / 's90g-wow-visual-proof.css'
if not css.is_file():
    issues.append('s90g-wow-visual-proof.css: asset mancante')

if issues:
    print('ERRORE: contratto WOW visual proof non rispettato:')
    for issue in issues:
        print(' -', issue)
    raise SystemExit(1)

print('OK public WOW visual proof: 2 casi reali, 4 evidenze qualitative, CTA Free Entry, no soluzione completa')
