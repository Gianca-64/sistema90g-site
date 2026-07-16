# Audit approfondito immagini — Sistema 90G

Data: 4 luglio 2026

## Causa principale dei difetti

I problemi non derivavano da un solo file CSS. Nel sito convivevano tre famiglie di immagini:

1. immagini 2026 coerenti e già raccolte nel manifest ufficiale;
2. immagini legacy con testo incorporato, sfondi diversi e ritagli interni;
3. immagini della cartella `images/final/` con composizioni diverse da quelle 2026.

Lo script `site-ui-clean.js` continuava inoltre ad assegnare alcune immagini legacy alle pagine principali dopo il caricamento, annullando le sostituzioni fatte nell'HTML.

## Problemi riscontrati

- sfondo beige o bianco incorporato nei pixel del JPG;
- testo promozionale storico già tagliato dentro il file;
- immagini con proporzioni non adatte alla hero;
- immagini differenti tra card e pagina del caso;
- uso contemporaneo delle cartelle `images/`, `images/final/` e di vecchi SVG;
- fallback automatico che riproponeva una hero generica anche quando il file non era adatto;
- cache CSS e JavaScript non aggiornata in modo uniforme.

## Correzioni applicate

### Immagini approvate e mantenute

Sono state mantenute e collegate solo le immagini elencate in `images/VISUAL-MANIFEST-2026.txt`:

- 6 hero principali;
- 15 immagini caso;
- 1 immagine dedicata alla pagina Chi sono.

Le 15 card caso e le relative 15 pagine ora usano la stessa immagine 2026.

### Immagini legacy rimosse dall'uso pubblico

Le seguenti pagine non usano più immagini legacy non conformi:

- Render fotorealistici;
- Agenzie immobiliari;
- Controllo mirato;
- Analisi completa;
- Progetto da zero.

Finché non viene prodotta una hero nuova e approvata per ciascuna pagina, queste pagine vengono mostrate con una hero testuale pulita, senza riquadri vuoti e senza immagini storiche tagliate.

### Integrazione visiva

- `object-fit: contain` su tutte le immagini;
- nessun ritaglio `cover`;
- nessun bordo, radius o ombra;
- fusione del fondo chiaro mediante `mix-blend-mode: multiply`;
- sfumatura leggera ai bordi del JPG per evitare il rettangolo netto;
- rimozione automatica del contenitore se il file non viene caricato;
- layout a colonna singola sulle pagine prive di hero approvata;
- nuova versione cache per CSS e JavaScript.

## Regola operativa definitiva

Una nuova immagine può essere pubblicata solo se:

- deriva dallo stile visivo ufficiale Sistema 90G;
- non contiene testi promozionali incorporati o tagliati;
- ha una composizione adatta alla posizione in cui verrà usata;
- è diversa dalle altre immagini del sito;
- la stessa immagine viene usata nella card e nella pagina del caso;
- è verificata su desktop e smartphone;
- non richiede `object-fit: cover` per apparire correttamente.
