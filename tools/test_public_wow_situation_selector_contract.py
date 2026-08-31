#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlsplit
import re
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
        'images/05_HOME_CASO_1.jpg',
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

    if proof.count('class="s90g-wow-proof-card"') != 2:
        issues.append('index.html: attese esattamente 2 prove visuali')

    # La Home deve conservare il medesimo risultato finale ma senza applicare
    # audit-fix dopo DOMContentLoaded: visual -> offer -> WOW -> audit-fix.
    href_re = re.compile(r'href=["\']([^"\']+)["\']', re.I)
    href_paths = [Path(urlsplit(m.group(1)).path).name for m in href_re.finditer(text)]
    bundle_name = 's90g-home-critical.css'
    css_sources = [
        'sistema90g-visual-2026.css',
        's90g-offer-2026.css',
        's90g-wow-visual-proof.css',
        'sistema90g-audit-fix-20260707.css',
    ]
    if href_paths.count(bundle_name) != 1:
        issues.append(f'index.html: atteso 1 riferimento a {bundle_name}, trovati {href_paths.count(bundle_name)}')
    for name in css_sources:
        if href_paths.count(name) != 0:
            issues.append(f'index.html: {name} deve essere assorbito nel bundle Home')
    if href_paths.count('consent-ui.css') != 1:
        issues.append('index.html: consent-ui.css deve restare separato')
    if text.find(bundle_name) > text.find('consent-ui.css'):
        issues.append('index.html: bundle Home deve precedere consent-ui.css')
    if 'data-s90g-home-critical' not in text:
        issues.append('index.html: marker bundle Home mancante')
    if 'data-s90g-audit-fix' not in text:
        issues.append('index.html: marker audit-fix iniziale mancante')

    bundle = root / bundle_name
    if not bundle.is_file():
        issues.append(f'{bundle_name}: asset generato mancante')
    else:
        expected_parts = []
        for name in css_sources:
            css_path = root / name
            if not css_path.is_file():
                issues.append(f'{name}: asset sorgente mancante')
                continue
            expected_parts.append(f'/* bundled: {name} */\n{css_path.read_text("utf-8", errors="strict").rstrip()}')
        if len(expected_parts) == len(css_sources):
            expected = '\n\n'.join(expected_parts) + '\n'
            actual = bundle.read_text('utf-8', errors='strict')
            if actual != expected:
                issues.append(f'{bundle_name}: ordine o contenuto diverso dalla cascata canonica')
            for token in ('.s90g-chat-widget', '.s90g-hero-grid', '.s90g-hero-media img'):
                if token not in actual:
                    issues.append(f'{bundle_name}: regola audit-fix necessaria mancante: {token}')

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
    issues.append('s90g-wow-visual-proof.css: asset sorgente mancante')

audit_css = root / 'sistema90g-audit-fix-20260707.css'
if not audit_css.is_file():
    issues.append('sistema90g-audit-fix-20260707.css: asset sorgente mancante')

if issues:
    print('ERRORE: contratto WOW Home non rispettato:')
    for issue in issues:
        print(' -', issue)
    raise SystemExit(1)

print('OK public WOW Home: 6 situazioni + 2 casi + bundle CSS Home con audit-fix iniziale e cascata invariata')
