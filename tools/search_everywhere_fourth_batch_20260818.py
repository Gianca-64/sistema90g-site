from pathlib import Path

# Quarto lotto Search Everywhere:
# 1) completa l'ultima guida tecnica sotto le 180 parole;
# 2) collega le guide materiali al Progetto Cucina + add-on Finiture senza forzare pagine B2B/istituzionali.

PATCHES = {
    "colonna-forno-microonde-cucina.html": {
        "marker": '<p class="s90g-lead">La posizione in colonna può migliorare l\'uso quotidiano, ma altezza, aperture e passaggi devono essere verificati nel progetto reale.</p>',
        "insert": '<div class="s90g-prose"><h2>In breve: a che altezza conviene mettere forno e microonde in colonna?</h2><p>Non esiste una quota unica valida per tutti. L’altezza corretta dipende dalla statura di chi usa la cucina, dal tipo di apertura degli apparecchi, dalla possibilità di vedere e raggiungere bene l’interno e dalla presenza di un piano di appoggio vicino. Anche ventilazione e istruzioni di incasso del modello scelto devono essere compatibili con il mobile.</p><h2>Cosa significa in pratica</h2><p>Prima di fissare le quote conviene simulare l’uso reale: estrarre una teglia calda, aprire il microonde, controllare il contenuto e verificare cosa accade nel passaggio quando le porte sono aperte. La colonna deve funzionare per la persona che la userà, non soltanto risultare ordinata nel prospetto.</p></div>',
    },
    "abbinare-cucina-pavimento.html": {
        "marker": '<p>Prima di scegliere conviene mettere in relazione pavimento, ante, top e pareti. Se tutti gli elementi hanno la stessa intensità e temperatura il risultato può appiattirsi; se i contrasti sono troppo forti, invece, l’ambiente può frammentarsi. L’obiettivo è costruire una gerarchia visiva coerente, non trovare due colori semplicemente “uguali”.</p>',
        "insert": '<p>Se la cucina deve ancora essere definita, il <a href="/progetto-cucina-sistema90g.html">Progetto Cucina 90G</a> può integrare queste scelte; con l’add-on <a href="/scelta-finiture-cucina.html">Finiture e materiali</a> il confronto viene approfondito sul contesto reale.</p>',
    },
    "ante-cucina-materiali-manutenzione.html": {
        "marker": '<p>Per confrontare due ante conviene guardare una scheda tecnica completa e un campione reale: superficie, bordo, supporto interno, spessore e modalità di manutenzione. Una finitura molto resistente ma delicata nei bordi o difficile da ripristinare può risultare meno adatta di una soluzione apparentemente più semplice.</p>',
        "insert": '<p>Nel <a href="/progetto-cucina-sistema90g.html">Progetto Cucina 90G</a> la scelta può essere letta insieme alla composizione; l’add-on <a href="/scelta-finiture-cucina.html">Finiture e materiali</a> serve quando vuoi approfondire il confronto tra alternative già selezionate.</p>',
    },
    "cucina-chiara-scura-luce.html": {
        "marker": '<p>La scelta tra chiaro e scuro va valutata sull’insieme della stanza. È utile osservare quanta luce naturale entra, in quali ore, quali superfici ricevono ombra e dove conviene creare contrasto. Il colore deve aiutare a leggere volumi e funzioni, non essere deciso separatamente dal progetto.</p>',
        "insert": '<p>Se la cucina è ancora da progettare, il <a href="/progetto-cucina-sistema90g.html">Progetto Cucina 90G</a> permette di valutare luce e volumi insieme alla disposizione; l’add-on <a href="/scelta-finiture-cucina.html">Finiture e materiali</a> approfondisce poi le alternative cromatiche.</p>',
    },
    "finiture-opache-lucide-cucina.html": {
        "marker": '<p>Prima di decidere conviene osservare campioni abbastanza grandi sotto luce naturale e artificiale e verificare la manutenzione prevista dal produttore. La stessa tonalità può cambiare sensibilmente tra opaco e lucido, soprattutto accanto a top, pavimento e pareti.</p>',
        "insert": '<p>Quando la cucina deve ancora essere definita, queste scelte possono entrare nel <a href="/progetto-cucina-sistema90g.html">Progetto Cucina 90G</a>; l’add-on <a href="/scelta-finiture-cucina.html">Finiture e materiali</a> è pensato per approfondire il confronto tra finiture nel loro contesto.</p>',
    },
    "top-cucina-materiali-guida.html": {
        "marker": '<p>La scelta va verificata sulla composizione reale: dimensioni delle lastre, posizione di lavello e piano cottura, fori, giunzioni, alzatine e spessori influenzano sia estetica sia fattibilità. Prima dell’ordine è utile controllare anche condizioni di garanzia, manutenzione e tolleranze di posa.</p>',
        "insert": '<p>Se la cucina è ancora in fase di definizione, il <a href="/progetto-cucina-sistema90g.html">Progetto Cucina 90G</a> permette di leggere il top insieme a composizione e funzioni; l’add-on <a href="/scelta-finiture-cucina.html">Finiture e materiali</a> approfondisce il confronto tra alternative.</p>',
    },
}

for filename, spec in PATCHES.items():
    path = Path(filename)
    text = path.read_text()
    if spec["insert"] in text:
        print(f"SKIP {filename}: già aggiornato")
        continue
    if spec["marker"] not in text:
        raise SystemExit(f"Marker non trovato in {filename}")
    text = text.replace(spec["marker"], spec["marker"] + spec["insert"], 1)
    path.write_text(text)
    print(f"OK {filename}")

print("Search Everywhere: quarto lotto completato.")
