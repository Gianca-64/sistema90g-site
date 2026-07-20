# Verifica tecnica del percorso interattivo — 20 luglio 2026

## Esito

`RELEASE AUDIT: PASS`

`GUIDED PRICING TEST: PASS`

## Controlli superati

- 75 file HTML analizzati.
- 57 pagine indicizzabili.
- un’unica variante della navigazione.
- 168 CTA verso il percorso guidato, tutte complete di attribuzione.
- nessun prezzo numerico statico negli HTML.
- nessun prezzo nelle offerte dei dati strutturati.
- nessun collegamento interno interrotto.
- nessun asset locale mancante.
- sitemap allineata alle pagine indicizzabili.
- JavaScript valido secondo `node --check`.
- prezzi approvati presenti nella matrice dinamica.
- minimo di tre unità applicato automaticamente.
- parametri di instradamento verso Console presenti.

## Esempi di calcolo verificati

- Analisi completa: €253.
- Verifica professionale progetto cucina: €150.
- quattro unità: €440.
- una quantità inferiore al minimo viene ricondotta a tre unità: €330.

## SEO e ricerca Google con AI

- i prezzi non vengono duplicati nei dati strutturati delle pagine descrittive;
- le pagine servizio mantengono entità `Service` senza `Offer` pubblica;
- la pagina Servizi è una `CollectionPage` con l’elenco dei percorsi;
- la nuova pagina per più unità è inclusa in sitemap e image sitemap;
- canonical, metadati sociali, H1 e dati strutturati restano coerenti.

## Limite del collaudo locale

L’ambiente di esecuzione ha impedito il caricamento visuale completo del sito in Chromium per una policy amministrativa. Sono stati comunque eseguiti:

- controllo sintattico JavaScript;
- test automatico della matrice e dei calcoli;
- analisi strutturale di tutti gli HTML;
- controllo di link, immagini, schema e sitemap.

Dopo la pubblicazione restano raccomandati test reali mobile/desktop e verifica del flusso con il portale aggiornato.
