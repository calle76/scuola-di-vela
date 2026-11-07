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

## 5. Esiti (7 novembre 2026): **fermi prima dell'unione**, come previsto al §2

Ale: «vai». Giro su GitHub sul ramo `deriva` (8 zip delle 11:24): **12 falliti** contro 1 del giro di `main` della mattina. `main` non è stato toccato.

**P2-P5, P7 (qui):** P2 sì, cambiano solo le 7 regate con avversari (regate 1-3 principianti ed esperti, prima regata del torneo); lezioni, prove, menu e mare identici. P4 sì. P5 sì: «deriva» compare solo come nome della barca. P7: `scene_strane.py --prova` OK; il rigioco si rifà dopo l'unione. **P3** (pilota nelle due regate della Scuola, 320 regate per ramo): piazzamenti simili; contatti nelle regate da 294 a 249, fuori linea da 111 a 51; **boe dal lato sbagliato da 6 a 15**.

**Trovato e corretto, solo nel collaudo:** `collaudo_impronta.py` dava sempre «non valido» anche su `main`, perché chiedeva la barca «livello 2», che dalla 1.1.0 non c'è più. Ora accetta anche la barca unica; l'impronta di `deriva` rifatta è identica bit per bit.

**I 12 falliti di P1:**

| Collaudo | Cosa | Spiegazione | Da fare |
| --- | --- | --- | --- |
| `collaudo_suoni_si_sentono` (Chromium) | come al mattino | noto, non dipende dagli avversari | niente |
| `collaudo_torneo` C11 (Firefox, 2 pezzi) | chiusura a metà torneo | noto, osservazione 86 | niente |
| `collaudo_avversari1b` scenario 5 | Chromium da 7 a **9** su 10 (verde), Firefox da 7 a **8** | migliora | aggiornare la riga dei noti |
| `collaudo_partenze` | stessi criteri (1) e (2), numeri un po' diversi | stessa famiglia di prima | aggiornare la riga dei noti |
| `collaudo_competizione` C1 | piazzamenti diversi, un gruppo ora in fascia | la fascia va ritarata (previsto) | aggiornare la riga dei noti |
| `collaudo_giri_avversari` | G4 durata dei giri 20-21 s (soglia 12-30, ma su 8-11 casi contro i 15 chiesti); **G12 nuovo**: 1 giro su 32-41 nel verso sbagliato | da capire | guardare |
| `collaudo_contatto_vero` (Firefox) | **nuovo tipo**: un istante con scafi sovrapposti senza contatto | da capire | guardare |
| `collaudo_moviola` | il pilota **non arriva** in 1 regata del torneo su 12 (seme 5): due contatti con Rossa, poi chiude fuori tempo massimo a 299 s | la guida nuova; su `main` arriva | guardare insieme alle boe |
| `collaudo_registratore_barche` G4 costruito 8 | l'avversario fermato a mano era già lento prima | la guida nuova cambia la scena costruita | correggere la scena |
| `collaudo_registro` (Chromium) | la scena del contatto non tocca | qui passa 15 su 15: caso isolato | rilanciare |

**Difetti possibili della guida, prima di unire:** le boe dal lato sbagliato (P3), il pilota fuori tempo (moviola), G12 e il nuovo `contatto_vero`. Per la regola del §2 ci si ferma e si decide con Ale.
