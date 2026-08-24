# Sistema 90G — Audit testi sito

Data: 2026-08-23
Branch: `strategy/free-entry-organic-20260823`

## Obiettivo

Verificare i testi del sito con due obiettivi principali: aumentare la comprensione e la fiducia del visitatore, e aumentare la probabilità che una visita qualificata diventi una richiesta reale. L'audit non riguarda solo grammatica o stile: valuta chiarezza, posizionamento, naturalezza, ripetizioni, coerenza commerciale, valore percepito, SEO e qualità delle CTA.

Le verifiche applicano anche le linee editoriali del sito: evitare formule seriali, CTA identiche, linguaggio artificiale, strutture ripetitive e testi costruiti solo per SEO.

## Criteri di controllo

Per ogni pagina verificare:

1. se titolo e primo paragrafo fanno capire subito il problema risolto;
2. se il testo parla prima del bisogno dell'utente e solo dopo del servizio;
3. se il linguaggio è naturale e comprensibile a un privato non tecnico;
4. se vengono usati troppo spesso termini interni come `percorso`, `perimetro`, `qualificare il caso`, `decisione specialistica circoscritta`;
5. se il valore dell'indipendenza è chiaro senza diventare una difesa ripetitiva contro rivenditori o marchi;
6. se la parte gratuita è presentata come ingresso utile e non come slogan ripetuto;
7. se prezzo, contenuti e nomi dei servizi sono coerenti tra tutte le pagine;
8. se una CTA nasce dal problema della pagina e non da una formula standard;
9. se esistono ripetizioni o sovrapposizioni tra pagine che possono ridurre chiarezza o autorevolezza;
10. se il contenuto dimostra competenza senza pubblicare procedure interne proprietarie.

# Blocco 1 — Home e pagine commerciali principali

Pagine analizzate:

- `index.html`
- `servizi.html`
- `analisi-preventiva.html`
- `progetto-cucina-sistema90g.html`
- `seconda-opinione-cucina.html`
- `professionisti.html`
- `rivenditori-cucine.html`
- `contatti.html`

## Valutazione generale

La struttura commerciale è molto più chiara rispetto alla versione precedente. Sono leggibili i tre bisogni fondamentali — progettare, verificare, scegliere — e la valutazione gratuita riduce il rischio che il visitatore debba interpretare da solo l'offerta.

Il problema principale non è più la mancanza di informazioni. È quasi l'opposto: alcuni concetti vengono spiegati troppe volte e con formule troppo simili. La ripetizione di `prima`, `valutazione gratuita`, `percorso`, `non devi scegliere il servizio`, `prima dell'acquisto` e `indipendente` rischia di far percepire il sito come costruito attorno al funnel anziché attorno ai problemi reali della cucina.

La revisione editoriale deve quindi togliere ripetizioni senza indebolire il Free Entry.

## P0 — incoerenza commerciale da risolvere prima della revisione finale

### Rivenditori: 150 € oppure Verifica 90G 127 €?

La pagina `servizi.html` dichiara che il catalogo è unico e che il servizio dipende dal lavoro necessario, non dalla professione di chi lo richiede. `professionisti.html` ripete lo stesso principio e mostra Verifica 90G a 127 €.

`rivenditori-cucine.html`, invece, presenta ancora un servizio distinto `Verifica professionale progetto cucina · 150 €`, con structured data e CTA specifica a 150 €.

Questa non è una semplice questione di copy: è una contraddizione dell'offerta. Prima di riscrivere definitivamente la pagina rivenditori bisogna stabilire quale delle due regole è canonica:

- catalogo unico anche per rivenditori → Verifica 90G 127 €;
- servizio B2B realmente diverso → mantenere 150 €, ma allora va spiegata l'eccezione anche in `servizi.html` e `professionisti.html`.

Non correggere il prezzo solo per uniformità linguistica finché la regola commerciale non è confermata.

## P1 — Home

### Cosa funziona

- `Prima di spendere, verifica cosa ti serve davvero.` è un'apertura forte, semplice e coerente con il posizionamento.
- Il triplice bisogno progettare/verificare/scegliere permette di capire rapidamente l'offerta.
- La frase `Sistema 90G non vende cucine, non rappresenta marchi e non riceve provvigioni` rende concreta l'indipendenza.
- I casi reali sono un elemento di fiducia più forte di molte dichiarazioni autoreferenziali.

### Cosa migliorare

1. `progettare, verificare o scegliere sulla cucina` è una costruzione poco naturale. Meglio `progettare la cucina, verificare una proposta o prendere una decisione specifica`.
2. La Home ripete numerose volte `prima`, `rivenditore`, `indipendente`, `valutazione gratuita`. Il concetto è corretto, ma va compresso.
3. Due intere sezioni spiegano la differenza tra Sistema 90G e rivenditore. Una delle due può essere accorciata oppure trasformata in prova concreta attraverso un esempio.
4. `Scopri cosa facciamo` è una CTA generica rispetto alla precisione del resto della pagina.
5. La Home mostra immediatamente tutti e tre i prezzi, poi di nuovo il prezzo del Progetto. Può essere utile, ma la gerarchia deve evitare l'effetto listino prima che il visitatore abbia capito il valore.

### Direzione di riscrittura

Mantenere l'hero e ridurre il testo difensivo. Far emergere più rapidamente un messaggio pratico: `portaci il problema, non devi sapere già quale servizio ti serve` una sola volta, poi mostrare prove/casi.

## P1 — Servizi

### Cosa funziona

La pagina distingue chiaramente Consulenza, Verifica e Progetto con prezzi e confini leggibili.

### Cosa migliorare

- `decisione specialistica circoscritta`, `perimetro`, `insieme coerente di decisioni già formulate` sono espressioni corrette internamente ma poco spontanee per un cliente.
- Le tre schede spiegano molto bene ciò che non rientra nei servizi, ma il tono può diventare amministrativo.
- `Il percorso lo individuiamo noi sulla base del problema reale` è chiaro, ma la parola `percorso` compare troppe volte nel sito.

### Direzione di riscrittura

Usare esempi concreti al posto di definizioni astratte. Per esempio: `Hai già scelto due top e vuoi capire quale è più adatto? Consulenza.`; `Hai un progetto e vuoi controllare passaggi e preventivo? Verifica.`; `La cucina è ancora da impostare? Progetto.`

## P1 — Valutazione iniziale gratuita

### Cosa funziona

La pagina spiega chiaramente cosa è gratuito e cosa non lo è. Il fatto che l'invio non attivi un acquisto riduce una frizione reale.

### Cosa migliorare

- La parola `gratuita` è ripetuta molto frequentemente nello stesso viewport.
- La pagina ripete ancora una volta l'intero catalogo dei servizi, già presente nella pagina Servizi.
- `Raccontaci il dubbio. Al servizio pensiamo dopo.` è naturale e può diventare il centro della pagina; molte frasi attorno possono essere accorciate.
- `qualificare il caso`, `pertinenza e bisogno`, `percorso appropriato` sono termini da back-office, non da relazione con il cliente.

### Direzione di riscrittura

Più semplice: `Raccontaci cosa stai cercando di decidere e allega ciò che hai. Ti diciamo se possiamo essere utili e, solo se serve un lavoro professionale, quale servizio è adatto e quanto costa.`

## P1 — Progetto Cucina 90G

### Cosa funziona

- Prezzo e contenuto base sono trasparenti.
- È chiarito bene che il progetto non sostituisce il rilievo e l'esecutivo del rivenditore.
- La frase `Il progetto base deve essere utile da solo` è un buon principio di fiducia.

### Cosa migliorare

- `base progettuale indipendente`, `soluzione progettuale principale completa nel proprio perimetro`, `posizionamento indicativo` e `resa realistica/illustrata o schizzata coerente con il sistema` rendono il servizio più difficile da immaginare.
- La descrizione delle `2/3 viste stile 90G realistiche/illustrate non fotorealistiche` è tecnicamente prudente ma poco elegante e può creare più dubbi di quanti ne risolva.
- Gli add-on sono chiari come prezzi, meno chiari come beneficio concreto per il cliente.

### Direzione di riscrittura

Descrivere prima cosa può fare il cliente con ciò che riceve. Esempio: `vedere una disposizione concreta, capire come sono organizzate le funzioni e arrivare dal rivenditore sapendo quali aspetti non vuole perdere`.

## P1 — Verifica / seconda opinione

### Cosa funziona

La pagina conserva una query SEO utile (`seconda opinione cucina`) ma presenta correttamente il servizio come Verifica 90G.

### Cosa migliorare

- `non devi scegliere tra fidarti alla cieca o rifare tutto` è una formula troppo drammatica e può sembrare implicitamente critica verso il rivenditore.
- La pagina usa molte formule prudenti (`ciò che appare coerente`, `ciò che merita una domanda`, `ciò che deve essere verificato`) che, sommate, rallentano il messaggio.
- La sezione `Il punto non è trovare un errore` è utile, ma lo stesso concetto è già presente in varie altre pagine.

### Direzione di riscrittura

Posizionare la Verifica come chiarezza prima della firma, non come sospetto: `Hai già una proposta e vuoi essere sicuro di averla capita bene?`.

## P1 — Professionisti

### Cosa funziona

È chiaro che Sistema 90G non sottrae il cliente e non sostituisce responsabilità professionali.

### Cosa migliorare

- Il testo è molto difensivo. `non un ruolo sostitutivo`, `mantiene la regia`, `responsabilità di competenza`, `non assume incarichi`, `non usa il supporto per acquisire autonomamente il cliente` occupano molto spazio prima di spiegare il vantaggio operativo.
- Il beneficio per il professionista dovrebbe arrivare prima: risparmio di tempo, approfondimento verticale, possibilità di delegare un sotto-problema cucina senza ampliare l'incarico generale.
- `Catalogo unico` è una definizione interna; non serve necessariamente al cliente.

### Direzione di riscrittura

Aprire dal vantaggio: `Quando la cucina richiede più tempo o dettaglio di quanto conviene assorbire nell'incarico principale, puoi affiancare una competenza verticale mantenendo tu il rapporto con il cliente.` Poi una sola sezione chiara sui confini.

## P0/P1 — Rivenditori

### Cosa funziona

La pagina evita un posizionamento antagonista e parla di dubbi che rallentano la vendita, un problema concreto per lo showroom.

### Cosa migliorare

- Prima va risolta l'incoerenza 150 €/127 €.
- `Una seconda lettura quando un dubbio rischia di allungare la vendita` è una buona promessa B2B.
- La pagina ripete molto `non sostituisce`, `non alternativa`, `non antagonista`, `senza entrare nella vendita`, `nessuna interferenza commerciale`.
- Serve più concretezza su quando il rivenditore guadagna tempo e meno rassicurazioni ripetute sul fatto che Sistema 90G non vende cucine.

## P1 — Contatti

### Cosa funziona

La pagina distingue correttamente richiesta di un caso da informazioni generali via email.

### Cosa migliorare

- È molto sovrapposta a `analisi-preventiva.html`: spiega nuovamente valutazione gratuita, tre famiglie di servizi, gratuità, cosa succede dopo e prezzo.
- Questa duplicazione può indebolire entrambe le pagine e rende il sito più verboso.
- La pagina Contatti dovrebbe essere più breve e funzionale: `caso cucina → valutazione`, `informazioni/collaborazioni → email`, eventuali dati del professionista.

### Direzione di riscrittura

Ridurre sensibilmente la pagina. La spiegazione completa del Free Entry deve restare su `analisi-preventiva.html`; Contatti deve indirizzare correttamente la persona senza duplicare il funnel.

# Pattern trasversali emersi

## 1. Eccesso di linguaggio da processo interno

Parole da ridurre nel sito pubblico:

- percorso
- perimetro
- qualificare / qualifica
- pertinenza
- decisione specialistica circoscritta
- proposta a pagamento
- materiale compatibile con il servizio
- insieme coerente di decisioni

Non sono errate, ma ripetute rendono la voce più burocratica e meno umana.

## 2. Eccesso di frasi negative

Il sito usa molto spesso `non vende`, `non sostituisce`, `non comprende`, `non attiva`, `non devi`, `non rappresenta`, `non assume`, `non viene proposto`.

I confini sono necessari, ma conviene concentrare le negazioni in pochi punti e usare nel resto del testo formulazioni positive: cosa fa Sistema 90G, cosa riceve il cliente e quale decisione riesce a prendere meglio.

## 3. Ripetizione della valutazione gratuita

Il Free Entry è strategicamente corretto, ma non deve diventare il tema dominante di ogni sezione. La gratuità va usata come riduzione della frizione, non come promessa ripetuta fino a sembrare promozionale.

Regola proposta: una CTA primaria gratuita per pagina, più eventuali richiami contestuali dove realmente utili. Evitare di ripetere la parola `gratuita` in ogni titolo, card e chiusura.

## 4. Più problemi reali, meno definizioni dell'offerta

Le pagine migliori del sito sono quelle che mostrano casi concreti: lavastoviglie, passaggi, isola, preventivo, lavello/finestra. La revisione testuale dovrebbe portare questo stile anche nelle pagine commerciali: esempi comprensibili al posto di categorie astratte.

# Priorità operativa

1. Risolvere la regola commerciale rivenditori 150 €/127 €.
2. Riscrivere Home riducendo ripetizioni e linguaggio difensivo senza cambiare il posizionamento.
3. Semplificare `analisi-preventiva.html` e `contatti.html` eliminando duplicazioni.
4. Rendere `servizi.html` più concreta con esempi di problemi reali.
5. Rendere Progetto e Verifica più facili da immaginare attraverso benefici e risultati, meno attraverso definizioni di perimetro.
6. Riscrivere Professionisti e Rivenditori mettendo il vantaggio operativo prima delle rassicurazioni sui confini.
7. Proseguire l'audit su hub, guide SEO, casi reali, FAQ e pagine istituzionali.

# Regola durante l'audit

Non creare nuove pagine solo per risolvere un problema di testo. Prima consolidare e migliorare le pagine esistenti. Non applicare sostituzioni seriali cieche: ogni modifica deve rispettare il ruolo specifico della pagina.
