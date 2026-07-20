# Aggiornamento percorso interattivo e prezzi — 20 luglio 2026

## Decisione applicata

I prezzi non sono più esposti in homepage, nella pagina Servizi, nelle schede dei servizi, nelle pagine professionali, nei metadati o nei dati strutturati.

Il visitatore li vede soltanto al terzo passaggio del percorso:

1. scelta del ruolo;
2. scelta della situazione;
3. servizio suggerito, prezzo, tempo, contenuto e limiti.

Solo dopo il terzo passaggio può aprire il portale e inserire dati personali, immagini e PDF.

## Prezzi applicati

### Privati

- Scelta Finiture cucina: €47
- Restyling cucina esistente: €79
- Controllo mirato: €127
- Analisi completa: €253
- Acquisto Assistito Cucina 90G: €290
- Studio preliminare degli spazi: €560

### Professionisti dell’immobile

Per agenzie immobiliari, imprese di costruzioni, interior designer, architetti e geometri:

- Verifica preliminare dell’immobile: €149
- Analisi di più unità o varianti: €110 per unità, minimo 3

### Rivenditori di cucine

- Verifica professionale progetto cucina: €150

## Pagine e funzioni aggiornate

- `analisi-preventiva.html`: nuovo percorso guidato in tre passaggi.
- `servizi.html`: descrizione di sei servizi privati e tre servizi professionali, senza listino.
- `professionisti.html`: tre perimetri professionali e tutela del rapporto con il cliente.
- `controllo-progetto-cucina.html`: evoluta in Verifica professionale progetto cucina.
- `verifica-planimetria-distribuzione-casa.html`: evoluta in Verifica preliminare dell’immobile.
- `analisi-unita-varianti.html`: nuova pagina per unità o varianti collegate.
- sei schede private: prezzi rimossi e CTA instradate al percorso guidato.
- homepage, casi e altre pagine: accessi al portale instradati al percorso guidato.
- `richiesta.html`: vecchio collegamento compatibile reindirizzato al percorso guidato.
- `role-case-path.js`: matrice ruolo/situazione/servizio/prezzo e calcolo delle unità.
- `role-case-path.css`: interfaccia accessibile e responsive.
- `privacy-consent.js`: conservazione della provenienza e tracciamento dopo consenso.

## Regole professionali comunicate

- Il cliente finale resta associato al professionista o al rivenditore.
- Sistema 90G non contatta autonomamente il cliente.
- Destinatari e modalità di contatto devono essere autorizzati.
- Il prezzo standard richiede materiale organizzato, un referente e un perimetro definito.
- I casi non compatibili con i percorsi standard vengono qualificati prima di formulare un prezzo.

## Dipendenza dalla Console

Il sito trasmette al portale parametri non sensibili, fra cui:

- `requester_role`
- `case_context`
- `service`
- `units`, quando applicabile
- `source_page`
- `content_type`
- `cta_position`
- parametri campagna e identificativo del caso, quando presenti

La Console e il portale devono ancora essere adeguati, nella relativa chat di sviluppo, per registrare e utilizzare questi campi nel nuovo modulo dinamico.
