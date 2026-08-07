# Gate 3 — Sito cucina isolato

Stato: preparazione tecnica sul ramo `integrazione/cucina-professionisti-infomaniak-v1`.

## Scopo

Preparare un ambiente di collaudo isolato per verificare il percorso:

```text
sito cucina di test → portale-test.sistema90g.it → backend Gate 3 → Console privata di test
```

Il pacchetto non è destinato al dominio pubblico `sistema90g.it` e non modifica la configurazione pubblica presente nel repository.

## Vincoli

- nessun merge;
- nessun deploy automatico;
- nessuna pubblicazione sul dominio operativo;
- nessuna attivazione del percorso professionale;
- nessun uso di casi, contatti o richieste reali;
- esclusivamente richieste sintetiche chiaramente riconoscibili;
- collegamento soltanto a `https://portale-test.sistema90g.it/portal.html`;
- indicizzazione impedita mediante `robots.txt` e meta `noindex`.

## Contenuto del pacchetto

Il workflow `Gate 3 sito isolato` crea una copia separata del sito e:

1. esegue gli audit cucina già presenti;
2. lascia invariato `portal-config.js` nel ramo;
3. sostituisce `portal-config.js` soltanto dentro il pacchetto con la destinazione Gate 3;
4. esclude le pagine e gli asset del percorso professionale non ancora attivo;
5. sostituisce `robots.txt` con `Disallow: /`;
6. inserisce `noindex, nofollow, noarchive` in tutte le pagine HTML;
7. esegue uno smoke test HTTP locale;
8. genera manifesto SHA-256, archivio e checksum;
9. pubblica esclusivamente un artefatto GitHub temporaneo;
10. non apre connessioni verso Infomaniak.

## Verifica determinante prima dell’uso

Prima di utilizzare il pacchetto in un ambiente remoto devono risultare positivi:

- DNS e certificato di `portale-test.sistema90g.it`;
- backend Gate 3 installato in una directory separata;
- database `4u0514_s90g_gate3` vuoto e pronto;
- configurazione privata del backend fuori dalla directory pubblica;
- risposta HTTP del catalogo di test;
- assenza di collegamenti al portale operativo.

## Rollback

Il rollback consiste nel non utilizzare o eliminare il pacchetto Gate 3. Poiché la configurazione pubblica del ramo resta invariata, non è richiesta alcuna modifica al sito operativo.
