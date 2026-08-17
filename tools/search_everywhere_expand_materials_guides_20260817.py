from pathlib import Path

PATCHES = {
    "abbinare-cucina-pavimento.html": {
        "marker": '<div class="s90g-prose">',
        "insert": '<div class="s90g-prose"><h2>In breve: come abbinare cucina e pavimento senza affidarsi solo al colore?</h2><p>Il risultato dipende soprattutto da temperatura cromatica, contrasto, quantità di luce e dimensione delle superfici. Due materiali che sembrano simili su un campione possono comportarsi diversamente quando occupano pareti, basi, colonne e pavimento. È quindi utile confrontarli insieme, nelle condizioni di luce reali o simulate.</p><h2>Cosa significa in pratica</h2><p>Prima di scegliere conviene mettere in relazione pavimento, ante, top e pareti. Se tutti gli elementi hanno la stessa intensità e temperatura il risultato può appiattirsi; se i contrasti sono troppo forti, invece, l’ambiente può frammentarsi. L’obiettivo è costruire una gerarchia visiva coerente, non trovare due colori semplicemente “uguali”.</p></div>',
    },
    "ante-cucina-materiali-manutenzione.html": {
        "marker": '<div class="s90g-prose">',
        "insert": '<div class="s90g-prose"><h2>In breve: quale materiale scegliere per le ante della cucina?</h2><p>Non esiste un materiale migliore in assoluto. La scelta va fatta considerando resistenza all’uso quotidiano, facilità di pulizia, sensibilità a calore e umidità, possibilità di riparazione e qualità della finitura. Anche bordi, supporto e lavorazioni incidono sulla durata più del solo nome commerciale del materiale.</p><h2>Cosa significa in pratica</h2><p>Per confrontare due ante conviene guardare una scheda tecnica completa e un campione reale: superficie, bordo, supporto interno, spessore e modalità di manutenzione. Una finitura molto resistente ma delicata nei bordi o difficile da ripristinare può risultare meno adatta di una soluzione apparentemente più semplice.</p></div>',
    },
    "cucina-chiara-scura-luce.html": {
        "marker": '<div class="s90g-prose">',
        "insert": '<div class="s90g-prose"><h2>In breve: una cucina chiara fa sempre sembrare lo spazio più grande?</h2><p>No. Le superfici chiare riflettono più luce, ma la percezione dello spazio dipende anche da contrasto, continuità visiva, quantità di colonne e pensili, pavimento e illuminazione. Una cucina scura ben progettata può risultare ordinata e profonda; una cucina tutta chiara ma molto frammentata può sembrare più pesante.</p><h2>Cosa significa in pratica</h2><p>La scelta tra chiaro e scuro va valutata sull’insieme della stanza. È utile osservare quanta luce naturale entra, in quali ore, quali superfici ricevono ombra e dove conviene creare contrasto. Il colore deve aiutare a leggere volumi e funzioni, non essere deciso separatamente dal progetto.</p></div>',
    },
    "finiture-opache-lucide-cucina.html": {
        "marker": '<div class="s90g-prose">',
        "insert": '<div class="s90g-prose"><h2>In breve: meglio una cucina opaca o lucida?</h2><p>Dipende dall’effetto visivo desiderato e dall’uso reale. Il lucido riflette maggiormente luce e ambiente, mentre l’opaco produce superfici più uniformi e meno specchianti. Impronte, micrograffi e facilità di pulizia variano però molto in base al materiale e al trattamento specifico, non soltanto alla categoria “opaco” o “lucido”.</p><h2>Cosa significa in pratica</h2><p>Prima di decidere conviene osservare campioni abbastanza grandi sotto luce naturale e artificiale e verificare la manutenzione prevista dal produttore. La stessa tonalità può cambiare sensibilmente tra opaco e lucido, soprattutto accanto a top, pavimento e pareti.</p></div>',
    },
    "top-cucina-materiali-guida.html": {
        "marker": '<p class="s90g-lead">Aspetto, resistenza e manutenzione contano, ma il risultato dipende anche da spessore, lavorazioni, giunzioni e inserimento di lavello e piano cottura.</p>',
        "insert": '<h2>In breve: come scegliere il materiale del top cucina?</h2><p>Il top va scelto in base a uso, manutenzione, resistenza, spessore possibile e lavorazioni richieste. Nessun materiale offre il massimo in ogni aspetto: alcuni sopportano meglio calore e graffi, altri permettono giunzioni o bordi più discreti, altri ancora richiedono maggiore attenzione alle macchie o agli urti.</p><h2>Cosa significa in pratica</h2><p>La scelta va verificata sulla composizione reale: dimensioni delle lastre, posizione di lavello e piano cottura, fori, giunzioni, alzatine e spessori influenzano sia estetica sia fattibilità. Prima dell’ordine è utile controllare anche condizioni di garanzia, manutenzione e tolleranze di posa.</p>',
    },
    "tavolo-vicino-cucina-spazi-sedute.html": {
        "marker": '<div class="s90g-prose">',
        "insert": '<div class="s90g-prose"><h2>In breve: quanto spazio serve tra tavolo e cucina?</h2><p>La distanza non va valutata soltanto a sedie chiuse. Bisogna considerare persone sedute, sedie arretrate, apertura di cassetti e lavastoviglie e il passaggio di chi usa la cucina. Lo spazio corretto dipende quindi da ciò che deve accadere contemporaneamente nella zona operativa.</p><h2>Cosa significa in pratica</h2><p>Una misura che sulla planimetria sembra sufficiente può diventare stretta nell’uso quotidiano. Conviene verificare il tavolo alla dimensione reale, la profondità delle sedute e le aperture degli elementi cucina più vicini, soprattutto in open space e ambienti compatti.</p></div>',
    },
}

for filename, spec in PATCHES.items():
    path = Path(filename)
    text = path.read_text()
    heading = spec["insert"].split("</h2>", 1)[0].split("<h2>", 1)[-1]
    if heading in text:
        print(f"SKIP {filename}: già aggiornato")
        continue
    if spec["marker"] not in text:
        raise SystemExit(f"Marker non trovato in {filename}")
    if filename == "top-cucina-materiali-guida.html":
        text = text.replace(spec["marker"], spec["marker"] + spec["insert"], 1)
    else:
        text = text.replace(spec["marker"], spec["insert"] + spec["marker"], 1)
    path.write_text(text)
    print(f"OK {filename}")

print("Search Everywhere: secondo lotto materiali, finiture e spazi ampliato e reso più citabile.")
