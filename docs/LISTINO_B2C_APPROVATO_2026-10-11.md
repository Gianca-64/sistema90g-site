# Sistema 90G — Listino B2C approvato 2026-10-11

Stato: **APPROVATO COME DECISIONE COMMERCIALE**. Decorrenza pubblica: **solo al rilascio coordinato e verificato** di Sito, Console e Portale, non al commit di questo documento.

## Sei servizi attivi e prezzi finali

| Codice offerta sito | Servizio | Prezzo in EUR |
| --- | --- | ---: |
| S90G-01 | Consulenza 90G | 99 |
| S90G-02 | Analisi Preventivo & Ordine 90G | 189 |
| S90G-03 | Verifica Cucina 90G | 229 |
| S90G-04 | Progetto Cucina 90G | 449 |
| S90G-05 | Controllo Pre-Montaggio 90G | 269 |
| S90G-06 | Analisi Problema 90G | 229 |

Add-on: render fotorealistico aggiuntivo **59 € per vista**, solo quando pertinente e chiaramente concordato. Valutazione iniziale: **0 €**.

Il Percorso Acquisto Cucina 90G continuativo rimane con proposta personalizzata: la precedente valutazione indicativa "da 890 €" **non è un prezzo fisso pubblicabile** finché non è approvato un perimetro contrattuale standard.

## Regola approvata per il Portale

1. **Primo contatto**: la Valutazione iniziale gratuita è reale e non equivale a un ordine o un preventivo automatico. Il cliente espone il proprio problema e fornisce gli elementi disponibili.
2. **Valutazione umana**: Sistema 90G esamina il caso, determina che cosa è verificabile e se basta un chiarimento gratuito. Solo se utile propone un servizio.
3. **Proposta**: Console → Portale invia la scelta umana revisionata: identificativo canonico del servizio, titolo, prezzo EUR finale, perimetro, inclusioni, esclusioni, eventuali add-on, condizioni e validità dell'offerta.
4. **Prezzo visibile**: il Portale presenta il prezzo approvato **quando il servizio adatto è stato definito**, prima di qualsiasi accettazione o richiesta di pagamento. Una bozza o richiesta gratuita non mostra un prezzo di servizio già deciso.
5. **Concordato e storico**: il prezzo accettato è uno snapshot immutabile associato alla proposta/caso, con versione del listino e data. Aggiornare il catalogo non deve ricalcolare prezzi di offerte accettate, ordini, pagamenti, fatture o casi esistenti.
6. **Fail closed**: servizio non mappato, prezzo non noto/non approvato, differenza Console/Portale/pagamento, valuta diversa da EUR, perimetro ambiguo o add-on non autorizzato impediscono emissione di una richiesta di pagamento e richiedono intervento umano.
7. **Controllo prezzi**: il front-end non deve inviare un importo considerato autorevole; il backend valida la proposta autenticata. Non costruire il prezzo a partire dal vecchio `PublicServiceCatalog` del Portale, che contiene servizi storici non equivalenti ai sei servizi B2C attivi.

## Gate di rilascio

- Pagina Servizi e sei dettagli IT, sei dettagli EN, metadata e Service Offer JSON-LD esattamente coerenti.
- Render a 59 € dove il servizio è effettivamente proposto; nessun add-on non mappato pubblicizzato nelle pagine EN.
- Suite completa Sito: verifica servizi, contratto commerciale, Offer JSON-LD, i18n servizi e dettagli, build Cloudflare, audit e accessibilità.
- Suite Console e Portale: offerta revisionata, accettazione, idempotenza, scadenza, importo coincidente con il link di pagamento, gestione dell'errore e snapshot storico.
- Nessun merge/deploy dei prezzi come variazione **operativa** prima del superamento di questi gate o di una scelta esplicita di rilascio scaglionato con controllo temporaneo delle discrepanze.
- Il deploy del sito usa soltanto la procedura locale canonica; non usare GitHub Actions come deploy ordinario.

Questo documento prevale **per le tariffe B2C attive** su offerte storiche datate 2026-08 e precedenti, senza cancellarne il valore archivistico.
