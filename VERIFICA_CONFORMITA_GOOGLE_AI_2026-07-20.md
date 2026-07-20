# Verifica di conformità Google Search e funzioni AI — 20 luglio 2026

## Esito

La copia di lavoro del sito pubblico Sistema 90G è stata riallineata alle indicazioni attuali di Google Search per AI Overviews e AI Mode.

Google non richiede file o marcature speciali per la ricerca con AI. La conformità dipende dalle normali basi SEO: contenuti originali e utili, struttura tecnica leggibile, pagine indicizzabili, collegamenti interni, immagini contestuali e dati strutturati coerenti con ciò che il visitatore vede.

Questa verifica riguarda la copia locale. L’idoneità definitiva dovrà essere controllata nuovamente sulla versione pubblicata attraverso Google Search Console, URL Inspection e Rich Results Test.

## Interventi completati

### Contenuti e architettura

- offerta statica unica a sei servizi;
- homepage organizzata per situazione del visitatore;
- pagina autonoma `servizi.html`;
- pagine servizio con confini, prezzo, tempo, risultati e limiti;
- Acquisto Assistito indipendente dai marchi e organizzato in due fasi;
- pagina rivenditori neutrale;
- pagina Professionisti per rivenditori, architetti, geometri e agenzie;
- archivio di 27 casi organizzato in cinque raccolte tematiche;
- collegamenti dai casi al servizio pertinente e a casi realmente correlati;
- contenuti commerciali principali presenti direttamente nell’HTML e non sostituiti via JavaScript.

### Indicizzazione e metadati

- 56 pagine indicizzabili;
- title, description, canonical e direttive robots presenti sulle pagine indicizzabili;
- Open Graph e Twitter Card completi;
- sitemap XML perfettamente allineata alle 56 canonical indicizzabili;
- image sitemap valida;
- nessun collegamento interno interrotto;
- nessun asset locale mancante.

### Dati strutturati JSON-LD

Ogni pagina indicizzabile contiene un solo blocco statico JSON-LD coerente con il contenuto visibile.

Sono presenti:

- `Organization` e `WebSite` per Sistema 90G;
- `Person` per Gian Carlo Primo;
- `Service` sulle sei pagine commerciali e sulle due pagine professionali pertinenti;
- `Article` sui 27 casi pubblici;
- `BreadcrumbList` sui casi e sulle raccolte tematiche;
- `CollectionPage` e `ItemList` sulle raccolte dei casi;
- `ItemList` sulla pagina Servizi;
- `AboutPage`, `ContactPage`, `CreativeWork` e `WebPage` dove appropriato.

Non sono stati aggiunti voti, recensioni, disponibilità o altre informazioni non realmente presenti nel sito.

### Immagini e stabilità visiva

- tutte le immagini hanno attributo `alt`, compreso `alt=""` per le icone decorative;
- tutte le immagini locali hanno larghezza e altezza intrinseche;
- prima immagine di contenuto caricata con priorità alta;
- immagini successive caricate in modo differito;
- archivio casi corretto per evitare il caricamento immediato di tutte le immagini;
- 0 riferimenti a immagini mancanti.

### Tracciamento e consenso

- 167 CTA verso il portale controllate;
- 167 CTA dotate di pagina, tipo contenuto, posizione e servizio/caso di provenienza;
- parametri di campagna conservati nel passaggio al portale;
- Google Analytics caricato soltanto dopo consenso positivo;
- nessun doppio blocco di dati strutturati generato dal JavaScript;
- formulazione del banner corretta in “misurazione statistica”, evitando l’affermazione non dimostrabile di anonimato completo.

## Audit automatico

È stato aggiunto:

`tools/audit_release.py`

Il controllo verifica:

- metadati;
- canonical;
- dati strutturati;
- nomi e prezzi dei servizi;
- vecchi termini commerciali vietati;
- riferimenti a Veneta Cucine;
- collegamenti e asset;
- menu;
- CTA e attribuzione;
- sitemap;
- immagini;
- rischio di duplicazione dinamica dei dati strutturati.

Esito finale:

- HTML controllati: 74;
- pagine indicizzabili: 56;
- varianti del menu: 1;
- CTA attribuite: 167 su 167;
- problemi bloccanti: 0;
- risultato: `RELEASE AUDIT: PASS`.

## Elementi volutamente non implementati nel sito statico

Queste funzioni appartengono al progetto separato Console/portale:

- salvataggio dei parametri di provenienza nella richiesta;
- filtro delle date e della capacità disponibile;
- registrazione di dati anagrafici, immagini e PDF nella Console;
- distinzione tra richiedente professionale e cliente finale;
- analisi automatica della richiesta;
- bozza da sottoporre all’approvazione dell’operatore;
- invio della risposta soltanto dopo approvazione;
- notifica email all’operatore;
- gestione privata degli allegati e dei tempi di conservazione.

## Controlli obbligatori dopo la pubblicazione

1. eseguire Rich Results Test almeno su homepage, una pagina servizio, un caso e una raccolta;
2. eseguire URL Inspection con Googlebot smartphone;
3. inviare o aggiornare la sitemap in Search Console;
4. verificare canonical e stato HTTP reali;
5. verificare il redirect permanente del vecchio URL rivenditori quando l’hosting lo consentirà;
6. controllare Core Web Vitals e prestazioni sulla versione pubblicata;
7. monitorare il nuovo rapporto Generative AI in Search Console;
8. verificare legalmente privacy, conservazione, fornitori e gestione degli allegati prima dell’attivazione delle nuove funzioni della Console.

## Pulizia futura prudenziale

L’audit immagini rileva file non utilizzati e alcuni duplicati binari storici. Non sono stati cancellati in questa fase perché potrebbero essere riferimenti di strumenti o versioni precedenti. La pulizia potrà essere affrontata dopo la pubblicazione e dopo un periodo di verifica, con un commit separato e reversibile.

## Fonti ufficiali Google utilizzate come riferimento

- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- https://developers.google.com/search/docs/appearance/structured-data/organization
- https://developers.google.com/search/docs/appearance/structured-data/article
- https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing
- https://developers.google.com/search/docs/appearance/google-images
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
