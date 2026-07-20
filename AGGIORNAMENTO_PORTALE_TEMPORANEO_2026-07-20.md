# Pubblicazione sito con portale temporaneamente sospeso

Data: 20 luglio 2026

## Decisione applicata

Il sito pubblico può essere pubblicato prima dell'attivazione del portale. Il percorso guidato resta operativo fino al terzo passaggio, dove mostra servizio, prezzo, tempi e limiti. L'invio di dati personali, immagini e PDF resta disabilitato.

## Hosting di prova

L'indirizzo configurato, ma non ancora attivo, è:

`https://sistema90g-portale.simply-winspace.it/`

È l'hostname scelto per il periodo di prova di 30 giorni dell'hosting Register.it.

## Attivazione futura

La configurazione è centralizzata in `portal-config.js`. Quando il portale sarà pronto e verificato in HTTPS, sarà sufficiente impostare `enabled: true`. Al termine della prova l'URL potrà essere sostituito con il sottodominio definitivo senza modificare le pagine del sito.

## Protezioni temporanee

- nessun collegamento al vecchio Worker;
- nessun modulo alternativo provvisorio;
- nessuna raccolta di dati o allegati nella pagina statica;
- avviso visibile prima del percorso e al pulsante finale;
- tracciamento del clic verso il portale disattivato finché il portale non è attivo.
