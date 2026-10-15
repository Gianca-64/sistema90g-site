# Home: leggibilità e accessibilità — 15 ottobre 2026

Base verificata: `8ddae6ebe4ee77cc69e36f1bb34f8b3893dbd88b` (`main`).

## Modifiche

- Home IT/EN: apertura più breve, sei situazioni subito dopo il blocco iniziale; spiegazione del valore spostata nelle sezioni di approfondimento già presenti. Prezzi, percorsi e attributi di tracciamento conservati.
- Vista 90G: pulsanti dei punti disabilitati quando invisibili, inizializzazione sicura e ripristino del focus al comando di attivazione quando necessario. Controlli disabilitati anche nell'HTML prima del caricamento dello script.
- Vista 90G: immagini sovrapposte conservano le proporzioni, così le coordinate dei punti si riferiscono allo stesso quadro senza ritaglio. Verifica visiva ancora necessaria.
- Chi sono IT/EN: sostituzione dell'etichetta interna “Free Entry” con una descrizione della valutazione gratuita.

## Verifiche eseguite

- Build canonica `bash tools/build_cloudflare.sh`: PASS prima e dopo le modifiche, 459 file pubblici.
- `node --check s90g-home-acquisition-v1.js`: PASS.
- `node --test tools/test_vista_keyboard_state.cjs`: 3 PASS. Esecuzione dello script in DOM simulato per IT/EN, ciclo iniziale/apertura/selezione/chiusura ripetuto e pagina senza Vista.
- `python tools/verify_about_acquisition_v1.py`: PASS.
- `python tools/test_responsive_contract.py`: PASS (controlli statici, non collaudo visuale).
- `git diff --check`: PASS.
- `python tools/test_site_i18n_home_v1.py`: PASS. Aggiornati due riferimenti a frasi superate: ora vengono controllati il messaggio visibile del lead e la descrizione per i motori di ricerca. Conservati i controlli su identità italiana, lingua, navigazione e immagini. Il primo errore era stato riprodotto anche sulla base originale.

## Verifiche ancora aperte

- Collaudo visuale desktop e mobile: proporzioni dei due livelli Vista, coordinate, pulsante e focus a 320/375/390/768 px; verifica tastiera nel browser e assenza di salti di pagina. Nessun collaudo nel browser della versione modificata eseguito in questa sessione.
- Portale live: verificato nel browser il collegamento dalla pagina Analisi preventiva al modulo. Caricamento completato, servizio “Valutazione iniziale gratuita”, totale 0 €, campi e pulsante di invio presenti. Il precedente 403 delle richieste automatiche e gli stati indicizzati non dimostrano un guasto. Restano da verificare invio/allegati/conferma nell’ambiente autorizzato del Portale; nessun invio di prova effettuato.
- Descrizione AI: da allineare solo dopo verifica del funzionamento definitivo della Console; nessun cambiamento in questa proposta.

## Pubblicazione

Proposta separata: nessun merge su main e nessun deploy. Il repository richiede `tools/deploy_verified_local.sh` nella copia canonica pulita, con credenziali Cloudflare disponibili. Non sostituire questa procedura con Sites o GitHub Actions.
