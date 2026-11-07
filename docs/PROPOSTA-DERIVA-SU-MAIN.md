# Proposta: portare il ramo `deriva` su `main`, cioè online (fermata 1)

**7 novembre 2026.** Ale: «la 1, fai la proposta dei controlli; non ti preoccupare se i progressi della carriera si cancellano». Scopo: giocare in due (Ale e Lucio) la stessa versione, con gli avversari nuovi, e avere più regate da misurare.

## 1. Cosa entra

Il ramo ha 18 commit dopo `main`, ma nel gioco cambiano solo tre file:

- **`js/regate.js` (83 righe):** la guida nuova degli avversari (`PROPOSTA-AVVERSARI-DERIVA.md` §10 e §11): scarto che guarda tutte le barche, niente ritorni di bolina, niente strambate a raffica, linea di partenza, giro di boa. Vale per tutte le regate, anche quelle della Scuola (decisione di Ale, 6 novembre).
- **`js/registratore.js` e `index.html`:** il pulsante «Scarica l'ultima regata», e il menu che non tiene più le regate chiuse subito.
- **Nessun livello Deriva visibile:** il ramo ha preso il nome dal livello, ma il livello non c'è. Lo controllo comunque (P5).

Il resto sono documenti e strumenti di misura (`tests/`). Su `main`, dopo la base comune, c'è un solo commit, solo documenti: `docs/DECISIONI.md` andrà unito a mano.

Diventa la versione **1.2.15** (`VERSIONE` e `CHANGELOG.md`). L'unione si fa con un merge, come per `pulizia` (decisione del 3 novembre). I salvataggi non cambiano formato; se qualcosa si perdesse, Ale ha detto che non importa.

## 2. I controlli (soglie nostre, scritte prima di misurare)

- **P1, giro completo su GitHub sul ramo `deriva`** (Chromium e Firefox, non veloce), confrontato con il giro di `main` del 7 novembre (138 OK, 1 fallito, 9 noti, 10 da controllare). Passa se ogni collaudo diverso da quel giro ha una spiegazione scritta: **guida nuova** (allora si guarda se il numero nuovo è accettabile e si aggiorna la riga dei fallimenti noti, dicendolo), oppure **difetto**, e allora si corregge prima dell'unione. Nessun collaudo nuovo rosso senza spiegazione.
- **P2, impronta:** `collaudo_impronta.py` rifatto. Passa se le differenze col riferimento di oggi stanno **solo nelle regate con avversari**; lezioni, prove e menu identici.
- **P3, punti di Competizione nella Scuola:** piazzamenti del pilota nelle due regate della Scuola (`collaudo_competizione.py`, misura) prima e dopo, Chromium. Nessuna soglia: il criterio C1 è già fuori fascia e va ritarato con le medaglie (lavoro previsto). Si riportano i numeri e si dice se un giocatore fa più fatica o meno a prendere i punti.
- **P4, barca invariata:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.
- **P5, niente di nascosto in vista:** nel testo del gioco (`index.html`, `js/`) nessuna parola «Deriva» che un giocatore possa vedere, e il menu uguale a oggi, salvo il pulsante del registratore.
- **P6, versione:** `collaudo_versione.py` verde; dopo il push Ale apre il sito e legge «1.2.15» nel menu (in Firefox, e lo fa provare a Lucio).
- **P7, i due strumenti nuovi sul nuovo `main`:** `scene_strane.py --prova` OK, e il rigioco della regata delle 18:33 dà gli stessi numeri del ramo.

Un numero fuori soglia si riporta com'è. Se P1 o P2 trovano un difetto, ci si ferma e lo si dice prima di unire.

## 3. Chi fa cosa

1. Ale lancia il giro su GitHub: Actions → Collaudi → Run workflow → ramo `deriva`, senza «veloce». Circa mezz'ora su 8 computer; il PC resta libero. Poi mette gli 8 zip nella cartella del repo, come oggi.
2. Io, nel frattempo, P2-P5 e P7 qui, e la voce 1.2.15 del `CHANGELOG.md` con i numeri.
3. Letti gli zip, se tutto è spiegato: merge in `main`, versione, commit. Ale fa il push e controlla P6.

## 4. Rischi

- **La Scuola cambia mentre Ale e Lucio la provano:** le regate e il torneo avranno gli avversari nuovi. Va detto a Lucio.
- **Fallimenti noti che cambiano firma:** alcuni noti (per esempio scenario 5 di `collaudo_avversari1b.py`, `collaudo_partenze.py`, `collaudo_competizione.py`) potrebbero fallire con numeri diversi o diventare verdi. Ogni cambio si scrive, non si nasconde.
- **I numeri della guida restano quelli del §10:** prima del via (V2) e le piantate fuori soglia. Si porta online sapendolo, per avere i dati che mancano.
