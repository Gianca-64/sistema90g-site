# Audit visuale profondo — Sistema 90G

Data: 4 luglio 2026

## Perché le immagini e il layout non hanno funzionato in modo stabile

1. **Tre livelli CSS sovrapposti**
   - `style.css` conteneva il vecchio impianto a riquadri.
   - `sistema90g-refresh.css` aggiungeva altri pannelli, bordi, radius e ombre con `!important`.
   - `sistema90g-final-images.css` correggeva soltanto le immagini, senza eliminare i contenitori che continuavano a farle sembrare incorniciate.

2. **Le immagini venivano modificate anche via JavaScript**
   - `site-ui-clean.js` reinseriva o sostituiva alcune hero e card dopo il caricamento della pagina.
   - Una modifica corretta nell'HTML poteva quindi essere sovrascritta nel browser.

3. **Cache non invalidata in modo coerente**
   - Molte pagine caricavano gli stessi file CSS e JS con versioni vecchie nella query string.
   - Safari poteva continuare a mostrare regole o immagini precedenti anche dopo un nuovo commit.

4. **Pagine costruite con strutture HTML diverse**
   - Alcune hero avevano già `<figure class="premium-image">`.
   - Altre avevano soltanto il testo e nessun contenitore immagine.
   - Altre ancora usavano classi storiche differenti.
   - Una singola regola non poteva quindi correggere tutte le pagine nello stesso modo.

5. **Rimozione e reinserimento non coordinati**
   - Alcuni script hanno eliminato immagini mancanti o vecchie.
   - Script successivi le hanno riassegnate tramite mappe automatiche, talvolta usando file generici o duplicati.

6. **Controllo tecnico diverso dal controllo editoriale**
   - Verificare che 15 file avessero 15 nomi diversi non garantiva che le scene fossero davvero differenti o coerenti con il caso.
   - Alcuni doppioni erano concettuali, non nominali.

7. **SVG non affidabile in una hero specifica**
   - La pagina “Progetto da zero” mostrava un'immagine non caricata in Safari.
   - La hero è stata riportata a un JPEG già presente e compatibile.

## Correzioni applicate

- Eliminati bordi, radius, fondi bianchi e ombre dalle hero.
- Trasformate le card in colonne editoriali aperte, separate da una linea superiore sottile.
- Rimossi i fondi e i bordi dalle immagini interne.
- Trasformate le etichette da pillole a microtitoli editoriali.
- Rimosse le scatole da CTA, risposte rapide, note e FAQ.
- Mantenute soltanto le sezioni scure a tutta larghezza come pausa visiva.
- Aggiunte hero alle pagine che risultavano vuote:
  - Render fotorealistici
  - Agenzie immobiliari
  - Controllo mirato
  - Analisi completa
  - Progetto da zero
- Forzato un nuovo caricamento dello script che assegna le hero.

## Regola stabile da mantenere

Ogni futura modifica visuale deve intervenire in un solo livello principale. Non devono essere aggiunti nuovi script che sostituiscono immagini senza aggiornare anche la mappa editoriale e la versione cache. Ogni nuova immagine deve essere verificata per:

- contesto corretto;
- unicità visiva e concettuale;
- assenza di ritaglio;
- compatibilità Safari;
- comportamento desktop e smartphone;
- assenza di fondi o riquadri non intenzionali.
