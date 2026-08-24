# Sistema 90G — Sito pubblico — istruzioni per agenti

## Avvio obbligatorio di ogni nuova conversazione
Prima di qualsiasi attività leggere `docs/CHATGPT_CODEX_OPERATING_MANUAL.md`. Il manuale definisce apertura chat, divisione ChatGPT/Codex, delega delle attività locali, gestione delle working copy parallele, condizioni di stop e rapporto finale. Le sue regole operative sono vincolanti insieme a questo file.

## Ruoli permanenti

Questa divisione è vincolante anche per il Sito pubblico di Sistema 90G.

### ChatGPT = direzione
ChatGPT mantiene:
- ragionamento e decisioni;
- architettura e programmazione;
- UX e strategia;
- contenuti, posizionamento e linee editoriali;
- definizione delle modifiche;
- valutazione dei rischi;
- verifica finale.

### Codex locale = operatore tecnico
Codex esegue sul Mac le attività meccaniche già definite:
- Git e sincronizzazione del repository;
- ricerca e modifiche ripetitive autorizzate;
- audit e verifiche;
- build/package del sito;
- deploy Cloudflare con la procedura canonica;
- raccolta di log ed errori.

Codex non è una seconda regia. Non deve decidere autonomamente architettura, UX, strategia, testi pubblici, SEO, servizi o cambiamenti di comportamento. Se incontra una scelta non prevista, un conflitto, un working tree non pulito o un errore che richiede interpretazione, si ferma e riferisce.

### Operatore umano
Nell'uso quotidiano normale l'operatore lavora con ChatGPT e non deve usare Terminale, Git, build o deploy. Un intervento manuale sul Mac è ammesso solo in situazioni eccezionali realmente necessarie, per esempio autorizzazioni di sistema, autenticazioni o recuperi infrastrutturali.

## Separazione dei sistemi
Il Sito è indipendente da Console e Configuratore. Non usare branch, script, build, Worker o configurazioni degli altri repository.

Repository: `Gianca-64/sistema90g-site`
Branch canonico: `main`

## Contenuti pubblici
Per qualsiasi intervento che crei o modifichi testi pubblici, pagine, articoli, FAQ, CTA o contenuti SEO, leggere e applicare prima:

`docs/LINEE_EDITORIALI_SITO_SISTEMA90G.md`

Le linee editoriali sono un requisito del sito. Evitare template linguistici rigidi, CTA ripetute e strutture editoriali uniformi. La qualità e la naturalezza del testo prevalgono sulla ripetizione meccanica di pattern SEO.

Le procedure interne complete di Sistema 90G restano nel repository privato della Console e non devono essere copiate nel sito pubblico.

## Principio centrale: problema prima del servizio

Sistema 90G parte dai problemi delle persone e cerca il modo più utile per risolverli. Il sito pubblico, le risposte, i casi, le guide, le CTA e soprattutto il Free Entry devono riflettere questa gerarchia: persona -> problema -> comprensione -> primo aiuto -> soluzione -> eventuale servizio.

Il Free Entry non è un semplice filtro commerciale o un preventivatore. È una prima lettura gratuita del caso: deve aiutare a mettere a fuoco il problema, evidenziare quando possibile il punto che merita attenzione e indicare il passo utile successivo. Il servizio a pagamento viene proposto soltanto quando aggiunge realmente il lavoro necessario per arrivare a una soluzione affidabile.

Non trasformare ogni richiesta in una vendita. Se la cosa più utile è recuperare una misura, chiedere una conferma al rivenditore, verificare una scheda tecnica, rivolgersi a un professionista competente o non fare altro, questo deve poter essere detto chiaramente. Questa indipendenza concreta è parte del valore di Sistema 90G.

I testi pubblici non devono presentare il Free Entry principalmente come "scelta del servizio giusto". Devono far capire che Sistema 90G guarda davvero il problema e prova ad aiutare la persona a risolverlo, mantenendo chiaro il confine tra prima valutazione gratuita e lavoro professionale completo.

## Ruolo dell'AI

L'AI è uno strumento di supporto interno per aumentare velocità, completezza, ordine e coerenza del lavoro. Può aiutare a leggere materiali, estrarre informazioni, confrontare dati, preparare bozze e segnalare elementi da verificare.

L'AI non prende decisioni al posto di Sistema 90G e non deve essere presentata come il soggetto che risponde al cliente. Individuazione del problema rilevante, priorità, confine tra gratuito e servizio, scelta dell'approfondimento, valutazione finale e comunicazione al cliente restano sotto controllo umano.

Nel sito pubblico questa struttura deve essere percepibile senza esporre processi interni: prima viene il problema della persona, poi il metodo e gli strumenti usati per lavorare bene; l'AI non è il prodotto e non è il centro del posizionamento.

## Neutralità verso marchi terzi

Sistema 90G non deve costruire cluster SEO, landing page o contenuti con l'effetto principale di promuovere, rafforzare o fare pubblicità gratuita a un marchio terzo. La crescita organica deve partire dai problemi e dalle decisioni dell'utente, non dal nome del produttore.

I marchi possono essere citati solo quando sono realmente necessari per rispondere a un caso concreto, confrontare in modo indipendente una proposta o chiarire una compatibilità specifica. Le citazioni devono restare neutrali, proporzionate e subordinate al problema dell'utente; evitare pagine dedicate a un singolo marchio salvo una decisione strategica esplicita approvata nella conversazione principale.

## Regola Git
Prima di operazioni automatiche:
1. branch `main`;
2. working tree pulito;
3. `git fetch origin`;
4. solo fast-forward verso `origin/main`;
5. nessun reset, stash automatico, clean o force-push.

## Deploy
Il deploy ordinario deve usare esclusivamente la procedura locale verificata del repository. Non usare GitHub Actions come meccanismo ordinario di pubblicazione.
