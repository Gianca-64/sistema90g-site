# Sistema 90G — pagamento rapido tramite Payment Links

Data: 2026-08-16

## Obiettivo

Ridurre il passaggio tra conferma del servizio e pagamento senza costruire ora un e-commerce completo.

## Impostazione proposta

Usare link di pagamento distinti per i servizi a prezzo fisso già presenti nel catalogo pubblico. Il link viene inviato solo dopo il controllo del materiale e la conferma che il servizio selezionato è corretto.

Servizi da predisporre:

- Scelta Finiture cucina — 47 euro
- Restyling cucina esistente — 79 euro
- Controllo mirato cucina — 127 euro
- Analisi completa cucina — 253 euro
- Acquisto Assistito Cucina 90G — 290 euro
- Analisi progetto cucina per rivenditori — 150 euro

## Flusso operativo iniziale

1. Il cliente entra dal sito o da un contatto diretto.
2. Il percorso guidato identifica il servizio e mostra il prezzo.
3. La richiesta arriva al portale/Console.
4. Sistema 90G controlla che materiale e servizio siano coerenti.
5. Viene inviato il link di pagamento relativo al servizio confermato.
6. Dopo l'esito positivo il caso passa allo stato pagato e parte il tempo di consegna.

## Perché non inserire subito il pagamento prima del controllo

Il catalogo prevede che il servizio sia confermato dopo il controllo del materiale. Far pagare prima rischierebbe rimborsi, richieste fuori perimetro o acquisti del livello sbagliato. Il Payment Link elimina attrito mantenendo questo controllo.

## Dati da registrare nella Console

- servizio acquistato;
- importo;
- valuta;
- data pagamento;
- provider;
- identificativo pagamento;
- stato pagamento;
- cliente associato;
- dati necessari alla fatturazione.

## Attivazione

Non inserire URL fittizi nel sito. I link reali devono essere creati nell'account del provider e poi configurati nel sistema. Fino a quel momento il portale continua a raccogliere la richiesta iniziale e il pagamento viene gestito separatamente.
