from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path, old, new, count=1):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    found = text.count(old)
    if found < count:
        raise SystemExit(f'ERRORE {path}: atteso almeno {count} match, trovati {found}: {old[:90]!r}')
    text = text.replace(old, new, count)
    p.write_text(text, encoding='utf-8')
    print(f'OK {path}: {old[:55]} -> {new[:55]}')

# HOME: le tre porte principali devono essere le tre situazioni commerciali reali.
replace('index.html',
        'Il servizio cambia in base al punto in cui si trova la tua cucina.',
        'Tre situazioni, tre percorsi chiari.')
replace('index.html',
        '<p class="s90g-eyebrow">Non sai quale servizio serve</p><h3>Percorso guidato</h3><p>Indica la situazione: il sito ti mostra il servizio pertinente, il prezzo e il tempo prima dell\'invio dei dati personali.</p><a class="s90g-link" href="/analisi-preventiva.html#percorso">Valuta la tua cucina →</a>',
        '<p class="s90g-eyebrow">Hai già una cucina</p><h3>Restyling cucina esistente · €79</h3><p>Rinnova ciò che hai già, decidendo cosa mantenere, cosa modificare e quali verifiche affidare al fornitore.</p><a class="s90g-link" href="/restyling-cucina-esistente.html">Scopri il Restyling →</a>')

# SERVIZI: la Seconda Opinione è un percorso con due livelli, non due prodotti concorrenti.
replace('servizi.html', '<h3>Controllo mirato · 127 €</h3>', '<h3>Seconda Opinione · dubbio preciso · 127 €</h3>')
replace('servizi.html', '<a class="s90g-link" href="/controllo-mirato.html">Vedi il controllo mirato →</a>', '<a class="s90g-link" href="/seconda-opinione-cucina.html">Approfondisci la Seconda Opinione →</a>')
replace('servizi.html', '<h3>Analisi completa · 253 €</h3>', '<h3>Seconda Opinione · controllo completo · 253 €</h3>')
replace('servizi.html', '<a class="s90g-link" href="/analisi-completa.html">Vedi l\'analisi completa →</a>', '<a class="s90g-link" href="/seconda-opinione-cucina.html">Approfondisci la Seconda Opinione →</a>')

# PROGETTO: quando esiste già una proposta, si passa al percorso Seconda Opinione.
replace('progetto-cucina-sistema90g.html', '<h3>Un dubbio preciso · 127 €</h3>', '<h3>Seconda Opinione · dubbio preciso · 127 €</h3>')
replace('progetto-cucina-sistema90g.html', '<a class="s90g-link" href="/controllo-mirato.html">Controllo mirato →</a>', '<a class="s90g-link" href="/seconda-opinione-cucina.html">Vai alla Seconda Opinione →</a>')
replace('progetto-cucina-sistema90g.html', '<h3>Controllo completo · 253 €</h3>', '<h3>Seconda Opinione · controllo completo · 253 €</h3>')
replace('progetto-cucina-sistema90g.html', '<a class="s90g-link" href="/analisi-completa.html">Analisi completa →</a>', '<a class="s90g-link" href="/seconda-opinione-cucina.html">Vai alla Seconda Opinione →</a>')

# COME FUNZIONA: il visitatore sceglie una situazione, non un catalogo di servizi.
replace('analisi-preventiva.html',
        'Percorso guidato Sistema 90G: descrivi la tua situazione cucina e scopri servizio, prezzo e tempi prima di inviare la richiesta.',
        'Percorso guidato Sistema 90G: descrivi la tua situazione cucina e scopri percorso, prezzo e tempi prima di inviare la richiesta.')
replace('analisi-preventiva.html',
        'Come funziona Sistema 90G | Trova il servizio cucina adatto',
        'Come funziona Sistema 90G | Trova il percorso cucina adatto', 2)
replace('analisi-preventiva.html',
        'Percorso guidato per individuare il servizio cucina indipendente, il prezzo e le condizioni prima dell\'invio della richiesta.',
        'Percorso guidato per individuare il percorso cucina indipendente, il prezzo e le condizioni prima dell\'invio della richiesta.')
replace('analisi-preventiva.html', 'Non devi conoscere il nome del servizio', 'Non devi conoscere il nome dell\'offerta')
replace('analisi-preventiva.html',
        'Devi ancora progettare la cucina? Hai già un progetto o un preventivo? Vuoi chiarire un solo dubbio? In tre passaggi individui il servizio pertinente prima di inserire dati personali o avviare una richiesta.',
        'Devi ancora progettare la cucina? Hai già un progetto o un preventivo? Vuoi rinnovare una cucina esistente? In tre passaggi individui il percorso pertinente prima di inserire dati personali o avviare una richiesta.')
replace('analisi-preventiva.html', '<span>Vedi tutti i servizi</span>', '<span>Vedi i tre percorsi</span>')
replace('analisi-preventiva.html', 'Prima la situazione, poi il servizio.', 'Prima la situazione, poi il percorso.')
replace('analisi-preventiva.html',
        'Indica chi presenta la richiesta e cosa deve essere fatto sulla cucina. Il percorso distingue progettazione, controllo di una proposta esistente, confronto di scelte e aggiornamento di una cucina già installata.',
        'Indica chi presenta la richiesta e a che punto si trova la cucina. Il percorso distingue progettazione, Seconda Opinione su una proposta esistente e Restyling di una cucina già installata.')
replace('analisi-preventiva.html', 'Chi richiede, situazione cucina, servizio e prezzo.', 'Chi richiede, situazione cucina, percorso e prezzo.')
replace('analisi-preventiva.html', '<span data-progress="3">3. Servizio e prezzo</span>', '<span data-progress="3">3. Percorso e prezzo</span>')
replace('analisi-preventiva.html', '<span>Mostra servizio e prezzo</span>', '<span>Mostra percorso e prezzo</span>')

# PERCORSO GUIDATO: rinomina i livelli della Seconda Opinione e riduce il linguaggio da catalogo.
replace('role-case-path.js',
        "const basePrivate={relationship:'La valutazione riguarda direttamente la cucina del richiedente. Il servizio viene confermato dopo il controllo del materiale.'};",
        "const basePrivate={relationship:'La valutazione riguarda direttamente la cucina del richiedente. Il percorso viene confermato dopo il controllo del materiale.'};")
replace('role-case-path.js', "title:'Controllo mirato cucina'", "title:'Seconda Opinione · dubbio preciso'", 2)
replace('role-case-path.js', "title:'Analisi completa cucina'", "title:'Seconda Opinione · controllo completo'", 2)
replace('role-case-path.js',
        "deliverables:['base progettuale indipendente','elaborati e visualizzazioni previsti dal servizio','priorità e punti da verificare con il rivenditore','add-on opzionali selezionabili nel portale']",
        "deliverables:['base progettuale indipendente','elaborati e visualizzazioni previsti dal progetto base','priorità e punti da verificare con il rivenditore','add-on opzionali selezionabili nel portale']")
replace('role-case-path.js',
        "const calculatePrice=s=>({price:s.price,priceText:euro(s.price),priceNote:s.id==='progetto-cucina-sistema90g'?'Prezzo base. Gli add-on opzionali si scelgono nel portale.':'Il prezzo viene confermato dopo il controllo del materiale.'});",
        "const calculatePrice=s=>({price:s.price,priceText:euro(s.price),priceNote:s.id==='progetto-cucina-sistema90g'?'Prezzo base. Gli add-on opzionali si scelgono nel portale.':'Il prezzo viene confermato dopo il controllo del materiale.'});")
replace('role-case-path.js', 'Tutti i servizi sono limitati alla cucina.', 'Tutti i percorsi sono limitati alla cucina.')

print('\nRiallineamento architettura offerta completato.')
