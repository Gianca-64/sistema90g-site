# Verifica pubblicazione con portale sospeso

Data: 20 luglio 2026

## Stato

Il sito pubblico è pronto per essere pubblicato mentre il portale resta in fase di attivazione.

Il percorso guidato consente di:

1. scegliere il ruolo;
2. scegliere la situazione;
3. vedere servizio, prezzo, tempo e condizioni.

Il passaggio successivo è disabilitato. La pagina non raccoglie dati personali, immagini o PDF.

## Configurazione del portale

File unico: `portal-config.js`

Stato attuale:

```js
enabled: false
url: 'https://sistema90g-portale.simply-winspace.it/'
```

L'URL è quello scelto per il periodo di prova di 30 giorni dell'hosting Register.it.

## Attivazione futura

Dopo avere verificato HTTPS, modulo, allegati, registrazione nella Console e approvazione manuale, modificare soltanto:

```js
enabled: true
```

Non è necessario modificare le CTA o le pagine HTML.

## Comportamento durante la sospensione

- avviso visibile all'inizio del percorso;
- servizio e prezzo restano consultabili;
- il pulsante finale mostra lo stato di attivazione;
- nessun dato viene inviato;
- nessun collegamento viene aperto verso un portale non operativo;
- nessun modulo provvisorio alternativo è stato introdotto.

## Pulizia eseguita

- rimosso il vecchio endpoint della Console Cloudflare;
- rimosso il vecchio endpoint pubblico Cloudflare;
- eliminato `public-request-form.js`, non utilizzato da alcuna pagina e collegato al backend obsoleto;
- adeguate Privacy Policy e Cookie Policy allo stato temporaneo;
- aggiornato il tracciamento per non registrare aperture del portale finché è disabilitato.

## Test

- `RELEASE AUDIT: PASS`
- `GUIDED PRICING TEST: PASS`
- 75 file HTML controllati;
- 57 pagine indicizzabili;
- 168 CTA guidate complete;
- nessun collegamento interno rotto;
- nessun asset locale mancante;
- nessun endpoint obsoleto nei file operativi;
- una sola configurazione dell'URL del portale.

## Verifica visiva

La verifica strutturale, sintattica e automatica è completa. Il tentativo di rendering con Chromium headless non è terminato nell'ambiente di esecuzione; prima della pubblicazione definitiva è quindi consigliato aprire localmente `analisi-preventiva.html` su desktop e smartphone e provare i tre passaggi.
