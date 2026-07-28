# Sezione D — Navigazione, percorsi e conversione

Applicazione tecnica del 28 luglio 2026.

## Interventi

- menu principale governato e completo, con apertura accessibile su tablet e smartphone;
- eliminazione della dipendenza dallo scorrimento orizzontale del menu;
- collegamenti diretti a rivenditori, Metodo 90G e contatti;
- focus visibile, skip link, `aria-expanded`, `aria-controls`, chiusura con Escape;
- conservazione dei parametri UTM tra le pagine interne;
- `role_hint`, `service_hint`, provenienza e posizione CTA nel percorso guidato;
- cronologia avanti/indietro del percorso guidato;
- risultato in tre blocchi: controlli, consegna, limiti;
- continuità tra pagine servizio e casi reali;
- continuità dell’articolo Innovazioni;
- eliminazione delle CTA generiche individuate nella baseline;
- collegamenti statici alle pagine indicizzabili risultate realmente orfane.

## Vincoli preservati

- nessun nuovo cookie o strumento esterno;
- nessuna modifica al backend del portale;
- nessuna promessa di caricamento allegati, pagamento o consegna nel portale;
- catalogo e prezzi approvati invariati;
- nessun commit o deploy automatico nello script di applicazione.

## Correzione di revisione pre-commit

- separato il collegamento “Come funziona” dall’apertura del percorso guidato;
- impedita la visualizzazione di un risultato vuoto con query incomplete;
- aggiornate le versioni cache-busting di CSS e JavaScript modificati;
- rafforzati i test sul contratto runtime e sulle versioni degli asset.
