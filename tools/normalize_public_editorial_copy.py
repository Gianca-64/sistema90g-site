#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

REPLACEMENTS = {
    'pareti-fuori-squadra-cucina.html': {
        'Seconda Opinione': 'Verifica 90G',
    },
    'frigorifero-incasso-o-libera-installazione.html': {
        'dell ordine': "dell'ordine",
        'd aria': "d'aria",
        'l allineamento': "l'allineamento",
        'l angolo': "l'angolo",
        'l estrazione': "l'estrazione",
        'l integrazione': "l'integrazione",
        'dell apparecchio': "dell'apparecchio",
    },
    'lavello-una-o-due-vasche-gocciolatoio.html': {
        'all uso': "all'uso",
        'sull abitudine': "sull'abitudine",
        'l utilità': "l'utilità",
        'l inserimento': "l'inserimento",
        'dell ordine': "dell'ordine",
        'l intera': "l'intera",
    },
    'piano-induzione-aspirazione-integrata-o-cappa.html': {
        'dell isola': "dell'isola",
        'L aspirazione': "L'aspirazione",
        'l aspirazione': "l'aspirazione",
        'dell aria': "dell'aria",
        'un isola': "un'isola",
        'c è': "c'è",
        'dell ordine': "dell'ordine",
        'dell acquisto': "dell'acquisto",
    },
    'confrontare-due-preventivi-cucina.html': {
        "prima ricevi l'indicazione del percorso appropriato e del relativo prezzo.": "prima ti diciamo se serve davvero un approfondimento e, se sì, quale lavoro è adatto e quanto costa.",
        '<p><a href="/analisi-preventiva#richiedi"><strong>Chiedi la valutazione gratuita →</strong></a></p>': '',
    },
    'voci-escluse-preventivo-cucina.html': {
        'quanto incide sul percorso complessivo.': "quanto incide sul costo e sull'organizzazione complessiva.",
        'chiarire il perimetro della propria offerta.': 'chiarire cosa comprende la propria offerta.',
    },
    'top-cucina-materiali-guida.html': {
        'Se la cucina è ancora in fase di definizione, il <a href="/progetto-cucina-sistema90g.html">Progetto Cucina 90G</a> permette di leggere il top insieme a composizione e funzioni; l’add-on <a href="/scelta-finiture-cucina.html">Finiture e materiali</a> approfondisce il confronto tra alternative.': 'Se il dubbio riguarda il tuo progetto o due materiali concreti, puoi partire dalla valutazione iniziale: prima leggiamo il problema e poi ti diciamo se basta un chiarimento o se serve un approfondimento sulle finiture.',
    },
    'ante-cucina-materiali-manutenzione.html': {
        'La prima valutazione serve a capire se il dubbio è leggibile dal materiale e se basta una Consulenza 90G o se ha senso approfondire la scelta nel progetto.': 'La prima valutazione serve a capire se il dubbio è leggibile dal materiale, se basta chiarire il confronto oppure se la scelta richiede un approfondimento nel progetto.',
    },
    'cucina-piccola-come-progettarla.html': {
        'Se hai già un progetto, puoi partire da una prima valutazione gratuita: non serve decidere in anticipo se il dubbio riguarda un solo punto o l’intera composizione. Se invece la cucina deve ancora essere impostata, puoi approfondire il <a href="/progetto-cucina-sistema90g.html">Progetto Cucina 90G</a>.': 'Se hai già un progetto, o se la cucina deve ancora essere impostata, puoi partire da una prima valutazione gratuita: non serve decidere in anticipo se il dubbio riguarda un solo punto o l’intera composizione. Prima leggiamo il problema e poi ti diciamo se serve davvero un approfondimento.',
    },
    'errori-progetto-cucina.html': {
        "se serve un'analisi professionale, ricevi prima indicazione del servizio appropriato e del prezzo.": "se serve un'analisi professionale, prima ti diciamo quale lavoro è utile e quanto costa.",
        'Se uno di questi errori riguarda una cucina già disegnata o un preventivo già ricevuto, la verifica più utile è quella fatta sul materiale reale: misure disponibili, composizione proposta, aperture, impianti ed eventuali vincoli dell’ambiente. In quel caso può essere appropriata <a href="/servizi.html">Verifica 90G</a>. Se invece la cucina deve ancora essere definita, può essere più adatto il <a href="/progetto-cucina-sistema90g.html">Progetto Cucina 90G</a>. La valutazione gratuita serve proprio a stabilirlo prima di qualsiasi acquisto.': 'Se uno di questi errori riguarda una cucina già disegnata, un preventivo già ricevuto o una cucina ancora da definire, la lettura più utile parte dal materiale reale: misure disponibili, composizione, aperture, impianti ed eventuali vincoli dell’ambiente. La valutazione iniziale serve a capire se il dubbio è circoscritto oppure se richiede un lavoro più ampio, senza che tu debba scegliere in anticipo il servizio.',
        '<a href="/analisi-preventiva#richiedi"><strong>Sottoponi gratuitamente il tuo caso →</strong></a>': '',
    },
}

changed: list[str] = []
for filename, replacements in REPLACEMENTS.items():
    path = root / filename
    if not path.is_file():
        raise SystemExit(f'ERRORE: guida editoriale mancante: {filename}')
    text = path.read_text('utf-8', errors='strict')
    original = text
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, 'utf-8')
        changed.append(filename)

print('Copy editoriale normalizzato: ' + (', '.join(changed) if changed else 'gia pulito'))
