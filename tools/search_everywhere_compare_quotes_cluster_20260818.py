from pathlib import Path

p = Path('confrontare-due-preventivi-cucina.html')
s = p.read_text()
old = '<h2>Come usare il confronto</h2><p>Il risultato dovrebbe aiutarti a tornare dai rivenditori con domande più precise e a capire meglio le differenze, non trasformare il confronto in una classifica assoluta tra punti vendita.</p>'
new = '''<h2>Un metodo pratico per confrontare due preventivi</h2><p>Metti le due offerte una accanto all'altra e confronta le voci nello stesso ordine. Se una voce esiste solo in una proposta, non confrontare ancora il totale: prima chiarisci se nell'altra è esclusa, compresa altrove o semplicemente non specificata.</p><ul><li><strong>Composizione:</strong> numero e misura di basi, pensili, colonne, pannelli e tamponamenti;</li><li><strong>Dotazioni:</strong> cassetti, cestoni, meccanismi, accessori interni e illuminazione;</li><li><strong>Materiali:</strong> ante, fianchi, schienali, top, spessori e lavorazioni;</li><li><strong>Elettrodomestici:</strong> marca e codice modello, non solo la categoria;</li><li><strong>Servizi:</strong> rilievo, trasporto, consegna, montaggio, posa e allacciamenti;</li><li><strong>Esclusioni:</strong> lavorazioni, opere e attività che dovrai organizzare o pagare separatamente.</li></ul><h2>Se i totali sono molto diversi</h2><p>Una differenza di prezzo importante non indica da sola quale proposta sia migliore. Può dipendere da materiali, modularità, accessori, elettrodomestici, servizi inclusi o da una composizione che sembra uguale ma non lo è. Il confronto diventa utile quando riesci a spiegare da dove nasce la differenza.</p><h2>Come usare il confronto</h2><p>Il risultato dovrebbe aiutarti a tornare dai rivenditori con domande più precise e a capire meglio le differenze, non trasformare il confronto in una classifica assoluta tra punti vendita.</p><p><a href="/elettrodomestici-incasso-misure-cucina.html">Controlla anche i modelli e le misure reali degli elettrodomestici →</a></p>'''
if old not in s:
    raise SystemExit('marker confronto non trovato')
s = s.replace(old, new, 1)
p.write_text(s)

p = Path('voci-escluse-preventivo-cucina.html')
s = p.read_text()
old = '<p><a href="/confrontare-due-preventivi-cucina.html">Confrontare due preventivi cucina →</a></p>'
new = '<p><a href="/confrontare-due-preventivi-cucina.html">Confrontare due preventivi voce per voce →</a></p>'
if old not in s:
    raise SystemExit('marker esclusioni non trovato')
s = s.replace(old, new, 1)
p.write_text(s)

print('OK confrontare-due-preventivi-cucina.html')
print('OK voci-escluse-preventivo-cucina.html')
print('Search Everywhere: confronto preventivi rafforzato.')
