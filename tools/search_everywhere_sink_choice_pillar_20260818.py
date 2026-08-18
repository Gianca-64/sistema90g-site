from pathlib import Path

NEW = Path('lavello-una-o-due-vasche-gocciolatoio.html')
if not NEW.exists():
    NEW.write_text('''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lavello cucina: una o due vasche e gocciolatoio? | Sistema 90G</title><meta name="description" content="Lavello cucina a una o due vasche, vasca e mezza e gocciolatoio: come scegliere in base a lavastoviglie, pentole, base disponibile, piano di lavoro e abitudini reali."><link rel="canonical" href="https://sistema90g.it/lavello-una-o-due-vasche-gocciolatoio.html"><link rel="stylesheet" href="sistema90g-visual-2026.css?v=20260730a"></head><body class="s90g-visual"><main><section class="s90g-section"><div class="s90g-shell"><p class="s90g-eyebrow">Guida cucina · zona lavaggio</p><h1>Lavello cucina: una vasca, due vasche o gocciolatoio? Scegliere in base all uso reale</h1><p class="s90g-lead">Non esiste una configurazione migliore in assoluto. La scelta dipende da come lavi e prepari, dalla presenza della lavastoviglie, dalle pentole che usi, dalla base disponibile e da quanto piano di lavoro vuoi conservare.</p><section class="s90g-callout"><h2>Meglio lavello cucina a una vasca o due vasche?</h2><p>Una vasca grande può essere più comoda con pentole, teglie e oggetti ingombranti e può lasciare più libertà al piano. Due vasche permettono invece di separare operazioni contemporanee. La scelta va fatta sul modo in cui la cucina viene realmente usata, non soltanto sull abitudine o sull estetica.</p></section><div class="s90g-prose"><h2>Quando conviene un lavello a una vasca e mezza?</h2><p>Può essere un compromesso quando si vuole mantenere una vasca principale abbastanza ampia e avere un secondo spazio più piccolo per scolare, risciacquare o separare alcune operazioni. Va però verificato che la divisione non renda la vasca principale troppo piccola per le esigenze reali.</p><h2>Serve davvero il gocciolatoio nel lavello cucina?</h2><p>Dipende dalle abitudini. Se molti oggetti vengono lavati a mano e lasciati sgocciolare, può essere utile. Se la lavastoviglie assorbe gran parte del lavaggio e il piano di lavoro è scarso, rinunciarvi può liberare una superficie preziosa. Esistono anche accessori mobili da usare sopra la vasca quando servono.</p><h2>Con la lavastoviglie servono ancora due vasche?</h2><p>Non necessariamente. La lavastoviglie può ridurre il bisogno di separare lavaggio e risciacquo nel lavello, ma non elimina automaticamente l utilità di una seconda vasca. Conta cosa viene ancora lavato a mano, come si preparano gli alimenti e quante attività devono convivere nella zona lavaggio.</p><h2>Meglio rinunciare al gocciolatoio per avere più piano di lavoro?</h2><p>Nelle cucine con poco piano utile può essere una scelta efficace, soprattutto se il gocciolatoio sarebbe usato poco. Il confronto corretto non è tra due lavelli isolati: bisogna valutare quanto spazio operativo resta tra lavello, cottura e piccoli elettrodomestici.</p><h2>Una vasca grande è più comoda per pentole e teglie?</h2><p>Spesso sì, perché una vasca unica ampia evita la separazione centrale e facilita l inserimento di oggetti grandi. Prima di sceglierla vanno comunque controllate dimensioni interne effettive, profondità, posizione del miscelatore e compatibilità con il mobile sottostante.</p><h2>Quanto incide la dimensione della base lavello sulla scelta?</h2><p>Incide direttamente. Ogni modello richiede un mobile minimo compatibile e il sottolavello deve convivere con vasca, scarico, sifone, raccolta differenziata e altri eventuali accessori. Un lavello desiderato può quindi richiedere una base più larga e modificare la distribuzione delle basi vicine.</p><h2>Come scegliere il lavello in base a uso reale e abitudini?</h2><p>Conviene partire dalle attività: quanto lavi a mano, quali oggetti sono più ingombranti, se usi molto la lavastoviglie, se prepari alimenti nel lavello, se lasci stoviglie ad asciugare e quanto piano libero ti serve. Solo dopo ha senso confrontare una vasca, due vasche, vasca e mezza e gocciolatoio.</p><h2>La verifica prima dell ordine</h2><p>Controlla modello reale, misure del foro e della vasca, base minima richiesta, ingombri sotto il piano, posizione di scarico e miscelatore, rapporto con lavastoviglie e quantità di piano di lavoro che rimane. Una scelta apparentemente piccola può modificare l intera zona lavaggio.</p><p><a href="/lavastoviglie-cucina-aperture-passaggi.html">Lavastoviglie: posizione, aperture e zona lavaggio →</a></p><p><a href="/piano-lavoro-colonne-cucina.html">Piano di lavoro: quanto spazio conservare →</a></p><p><a href="/lavello-sotto-finestra-cucina.html">Lavello sotto finestra: cosa verificare →</a></p><p>Se il dubbio riguarda il lavello all interno di un progetto già ricevuto, puoi usare la <a href="/seconda-opinione-cucina.html#livelli-seconda-opinione">Seconda Opinione · dubbio preciso</a>; se la scelta modifica basi, lavastoviglie e piano di lavoro, è più utile leggere insieme l intera composizione.</p></div></div></section></main></body></html>''', encoding='utf-8')
    print('OK lavello-una-o-due-vasche-gocciolatoio.html')
else:
    print('SKIP nuova pagina: già presente')

hub = Path('progettare-cucina-guide.html')
s = hub.read_text(encoding='utf-8')
link = '/lavello-una-o-due-vasche-gocciolatoio.html'
if link not in s:
    marker = '<a href="/lavello-sotto-finestra-cucina.html">Lavello sotto finestra →</a>'
    if marker not in s:
        raise SystemExit('Marker hub lavello non trovato')
    s = s.replace(marker, marker + '<a href="/lavello-una-o-due-vasche-gocciolatoio.html">Lavello: una o due vasche e gocciolatoio →</a>', 1)
    hub.write_text(s, encoding='utf-8')
    print('OK progettare-cucina-guide.html')
else:
    print('SKIP hub: link già presente')

old = Path('lavello-sotto-finestra-cucina.html')
s = old.read_text(encoding='utf-8')
if link not in s:
    marker = '</main>'
    if marker not in s:
        raise SystemExit('Marker pagina lavello non trovato')
    s = s.replace(marker, '<section class="s90g-section"><div class="s90g-shell"><p><a href="/lavello-una-o-due-vasche-gocciolatoio.html">Una vasca, due vasche o gocciolatoio: come scegliere →</a></p></div></section>'+marker, 1)
    old.write_text(s, encoding='utf-8')
    print('OK lavello-sotto-finestra-cucina.html')
else:
    print('SKIP pagina lavello: link già presente')

site = Path('sitemap.xml')
s = site.read_text(encoding='utf-8')
url = 'https://sistema90g.it/lavello-una-o-due-vasche-gocciolatoio.html'
if url not in s:
    marker = '</urlset>'
    if marker not in s:
        raise SystemExit('Marker sitemap non trovato')
    s = s.replace(marker, '  <url><loc>'+url+'</loc><lastmod>2026-08-18</lastmod></url>\n'+marker, 1)
    site.write_text(s, encoding='utf-8')
    print('OK sitemap.xml')
else:
    print('SKIP sitemap: URL già presente')

print('Search Everywhere: pilastro scelta lavello creato e collegato.')
