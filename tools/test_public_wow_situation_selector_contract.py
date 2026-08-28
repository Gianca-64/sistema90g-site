#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
page = root / 'index.html'
issues = []


def extract_section(text: str, marker: str, next_marker: str | None = None) -> str:
    start = text.find(marker)
    if start == -1:
        return ''
    if next_marker:
        end = text.find(next_marker, start + len(marker))
        if end != -1:
            return text[start:end]
    end = text.find('</section>', start)
    return text[start:end + len('</section>')] if end != -1 else text[start:]


if not page.is_file():
    issues.append('index.html: pagina mancante')
else:
    text = page.read_text('utf-8', errors='strict')
    selector_marker = 'data-s90g-wow-situation-selector="true"'
    proof_marker = 'data-s90g-wow-visual-proof="true"'

    if text.count(selector_marker) != 1:
        issues.append('index.html: selettore WOW mancante o duplicato')
    if text.count(proof_marker) != 1:
        issues.append('index.html: prova visuale WOW mancante o duplicata')

    selector = extract_section(text, selector_marker)
    proof = extract_section(text, proof_marker, selector_marker)

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
        if token not in selector:
            issues.append(f'index.html: elemento selettore mancante: {token}')

    proof_required = [
        'Guarda cosa vede Sistema 90G',
        'images/caso-lavastoviglie-passaggio-cucina.jpg',
        'images/caso-isola-passaggi-cucina.jpg',
        'Apertura reale', 'Passaggio residuo', 'Sedute in uso', 'Percorso operativo',
        'Conseguenza da verificare:',
        'href="/caso-lavastoviglie-passaggio-cucina"',
        'href="/caso-isola-passaggi-cucina"',
        'href="/analisi-preventiva#richiedi"',
    ]
    for token in proof_required:
        if token not in proof:
            issues.append(f'index.html: elemento prova WOW mancante: {token}')

    if 's90g-wow-visual-proof.css' not in text:
        issues.append('index.html: stylesheet prova WOW mancante')
    if proof.count('class="s90g-wow-proof-card"') != 2:
        issues.append('index.html: attese esattamente 2 prove visuali')

    selector_forbidden = [
        'Scegli il servizio', 'Quale servizio vuoi',
        'service=progetto', 'service=verifica', 'service=consulenza',
    ]
    for token in selector_forbidden:
        if token in selector:
            issues.append(f'index.html: selettore WOW anticipa la scelta servizio: {token}')

    proof_forbidden = [
        'service=progetto', 'service=verifica', 'service=consulenza',
        'passaggio sicuro di', 'distanza minima di', 'soluzione definitiva',
    ]
    for token in proof_forbidden:
        if token in proof:
            issues.append(f'index.html: prova WOW troppo prescrittiva/commerciale: {token}')

css = root / 's90g-wow-visual-proof.css'
if not css.is_file():
    issues.append('s90g-wow-visual-proof.css: asset mancante')

if issues:
    print('ERRORE: contratto WOW Home non rispettato:')
    for issue in issues:
        print(' -', issue)
    raise SystemExit(1)

print('OK public WOW Home: 6 situazioni problem-first + 2 casi visuali + 4 evidenze qualitative, no scelta servizio/soluzione completa')
