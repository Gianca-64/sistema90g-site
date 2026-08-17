from pathlib import Path


def replace_once(path, old, new):
    p = Path(path)
    s = p.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit(f'Marker non trovato in {path}')
    s = s.replace(old, new, 1)
    p.write_text(s, encoding='utf-8')
    print(f'OK {path}')


# 1) Preventivo: collega voce commerciale e modello tecnico reale.
path = 'preventivo-cucina-guida.html'
old = '<li>marca e modello degli elettrodomestici;</li><li>lavello, miscelatore e accessori;</li>'
new = '<li>marca e modello degli elettrodomestici;</li><li>lavello, miscelatore e accessori;</li>'
replace_once(path, old, new)

old = '<h2>Il prezzo va letto insieme al progetto</h2><p>Due preventivi sono confrontabili solo se descrivono forniture equivalenti. Inoltre un prezzo corretto non rende automaticamente corretto il progetto: passaggi, aperture, ergonomia e misure vanno verificati separatamente.</p>'
new = '<h2>Elettrodomestici: non basta leggere “forno 60 cm”</h2><p>Nel preventivo è utile che ogni elettrodomestico sia identificato almeno per marca e modello. La misura commerciale non descrive sempre il vano necessario, la profondità effettiva, la ventilazione, i collegamenti o lo spazio di apertura. Prima dell’ordine conviene quindi verificare che il modello indicato nel preventivo sia lo stesso considerato nel progetto e che la relativa scheda tecnica sia compatibile con il mobile previsto.</p><p><a href="/elettrodomestici-incasso-misure-cucina.html">Misure reali degli elettrodomestici da incasso →</a></p><h2>Il prezzo va letto insieme al progetto</h2><p>Due preventivi sono confrontabili solo se descrivono forniture equivalenti. Inoltre un prezzo corretto non rende automaticamente corretto il progetto: passaggi, aperture, ergonomia e misure vanno verificati separatamente.</p>'
replace_once(path, old, new)

# 2) Guida incasso: collega esplicitamente preventivo, progetto e verifica indipendente.
path = 'elettrodomestici-incasso-misure-cucina.html'
old = '<h2>Perché la scheda tecnica conta</h2><p>Un forno dichiarato da 60 cm, un frigorifero integrato o una lavastoviglie da incasso possono richiedere vani e distanze precise. Verificare il modello reale prima dell\'ordine riduce il rischio di modifiche in cantiere o compromessi nella composizione.</p>'
new = '<h2>Perché la scheda tecnica conta</h2><p>Un forno dichiarato da 60 cm, un frigorifero integrato o una lavastoviglie da incasso possono richiedere vani e distanze precise. Verificare il modello reale prima dell\'ordine riduce il rischio di modifiche in cantiere o compromessi nella composizione.</p><h2>Preventivo e progetto devono indicare lo stesso elettrodomestico</h2><p>Se nel preventivo compare un modello preciso, è utile controllare che sia quello realmente previsto nel progetto. Una sostituzione di marca o modello può cambiare quote di incasso, ventilazione, apertura, posizione dei collegamenti o compatibilità con il mobile. Quando preventivo, progetto e scheda tecnica non coincidono, il punto da chiarire è prima dell’ordine, non durante il montaggio.</p><p><a href="/preventivo-cucina-guida.html">Come leggere gli elettrodomestici nel preventivo →</a></p>'
replace_once(path, old, new)

print('Search Everywhere: cluster elettrodomestici/preventivo rafforzato.')
