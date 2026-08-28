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
        'Se la cucina è ancora in fase di definizione, il <a href="/progetto-cucina-sistema90g">Progetto Cucina 90G</a> permette di leggere il top insieme a composizione e funzioni; l’add-on <a href="/scelta-finiture-cucina">Finiture e materiali</a> approfondisce il confronto tra alternative.': 'Se il dubbio riguarda il tuo progetto o due materiali concreti, puoi partire dalla valutazione iniziale: prima leggiamo il problema e poi ti diciamo se basta un chiarimento o se serve un approfondimento sulle finiture.',
    },
    'ante-cucina-materiali-manutenzione.html': {
        'La prima valutazione serve a capire se il dubbio è leggibile dal materiale e se basta una Consulenza 90G o se ha senso approfondire la scelta nel progetto.': 'La prima valutazione serve a capire se il dubbio è leggibile dal materiale, se basta chiarire il confronto oppure se la scelta richiede un approfondimento nel progetto.',
    },
    'cucina-piccola-come-progettarla.html': {
        'Se hai già un progetto, puoi partire da una prima valutazione gratuita: non serve decidere in anticipo se il dubbio riguarda un solo punto o l\'intera composizione. Se invece la cucina deve ancora essere impostata, puoi approfondire il <a href="/progetto-cucina-sistema90g">Progetto Cucina 90G</a>.': 'Se hai già un progetto, o se la cucina deve ancora essere impostata, puoi partire da una prima valutazione gratuita: non serve decidere in anticipo se il dubbio riguarda un solo punto o l\'intera composizione. Prima leggiamo il problema e poi ti diciamo se serve davvero un approfondimento.',
    },
    'errori-progetto-cucina.html': {
        "se serve un'analisi professionale, ricevi prima indicazione del servizio appropriato e del prezzo.": "se serve un'analisi professionale, prima ti diciamo quale lavoro è utile e quanto costa.",
        'Se uno di questi errori riguarda una cucina già disegnata o un preventivo già ricevuto, la verifica più utile è quella fatta sul materiale reale: misure disponibili, composizione proposta, aperture, impianti ed eventuali vincoli dell’ambiente. In quel caso può essere appropriata <a href="/servizi">Verifica 90G</a>. Se invece la cucina deve ancora essere definita, può essere più adatto il <a href="/progetto-cucina-sistema90g">Progetto Cucina 90G</a>. La valutazione gratuita serve proprio a stabilirlo prima di qualsiasi acquisto.': 'Se uno di questi errori riguarda una cucina già disegnata, un preventivo già ricevuto o una cucina ancora da definire, la lettura più utile parte dal materiale reale: misure disponibili, composizione, aperture, impianti ed eventuali vincoli dell’ambiente. La valutazione iniziale serve a capire se il dubbio è circoscritto oppure se richiede un lavoro più ampio, senza che tu debba scegliere in anticipo il servizio.',
        '<a href="/analisi-preventiva#richiedi"><strong>Sottoponi gratuitamente il tuo caso →</strong></a>': '',
    },
    'index.html': {
        '<a class="s90g-link" href="/servizi">Scopri il Progetto →</a>': '<a class="s90g-link" href="/servizi#progetto">Scopri il Progetto →</a>',
        '<a class="s90g-link" href="/servizi">Scopri la Verifica →</a>': '<a class="s90g-link" href="/servizi#verifica">Scopri la Verifica →</a>',
        '<a class="s90g-link" href="/servizi">Scopri la Consulenza →</a>': '<a class="s90g-link" href="/servizi#consulenza">Scopri la Consulenza →</a>',
    },
    'servizi.html': {
        '<section class="s90g-section" id="servizi">': '<section class="s90g-section" id="consulenza">',
        '<section class="s90g-dark-band"><div class="s90g-shell"><p class="s90g-eyebrow">Hai già progetto o preventivo</p>': '<section class="s90g-dark-band" id="verifica"><div class="s90g-shell"><p class="s90g-eyebrow">Hai già progetto o preventivo</p>',
        '<section class="s90g-section"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">La cucina è ancora da impostare</p>': '<section class="s90g-section" id="progetto"><div class="s90g-shell"><div class="s90g-section-head"><div><p class="s90g-eyebrow">La cucina è ancora da impostare</p>',
        'href="#servizi"><span>Vedi servizi e prezzi</span>': 'href="#consulenza"><span>Vedi servizi e prezzi</span>',
    },
    'casi-analizzati.html': {
        'Sistema 90G valuta pertinenza e tipo di bisogno; solo se serve un approfondimento viene indicato il servizio professionale con il relativo prezzo.': 'Sistema 90G legge il materiale per capire che cosa merita davvero attenzione; solo se serve un approfondimento ti diciamo quale lavoro è utile e quanto costa.',
        'Se il caso richiede un lavoro professionale, percorso, contenuti e prezzo vengono indicati prima di iniziare.': 'Se il caso richiede un lavoro professionale, prima di iniziare sai che cosa verrà fatto e quanto costa.',
    },
    'rinnovare-cucina-senza-cambiarla.html': {
        'href="/servizi#servizi"': 'href="/servizi#consulenza"',
    },
    'professionisti-progetto-cucina.html': {
        "Il supporto resta circoscritto alla cucina e al perimetro concordato.": "Il supporto resta circoscritto alla cucina e al problema concordato.",
        '1. Definisci il dubbio o il perimetro': '1. Definisci il dubbio o ciò che vuoi approfondire',
        'Ti diciamo se il caso è pertinente, quale servizio è eventualmente appropriato e quali informazioni servono. Solo dopo, con contenuti e prezzo chiari, decidi se procedere con l\'approfondimento professionale.': 'Ti diciamo se dal materiale possiamo aiutarti, quali informazioni servono e, solo se occorre un approfondimento, quale lavoro è utile e quanto costa. Poi decidi se procedere.',
        'Se serve un approfondimento, servizio, contenuti e prezzo vengono indicati prima di iniziare.': 'Se serve un approfondimento, prima di iniziare sai che cosa verrà fatto e quanto costa.',
    },
}

changed: list[str] = []
for filename, replacements in REPLACEMENTS.items():
    path = root / filename
    if not path.is_file():
        raise SystemExit(f'ERRORE: pagina editoriale mancante: {filename}')
    text = path.read_text('utf-8', errors='strict')
    original = text
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, 'utf-8')
        changed.append(filename)

print('Copy editoriale normalizzato: ' + (', '.join(changed) if changed else 'gia pulito'))
