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

## 6. Correzioni prima dell'unione (Ale: «la 1»), criteri scritti prima

**Boe dal lato sbagliato.** Misura (`boe_sbagliate.py` nella cartella di lavoro, regate 0 e 1, principianti ed esperti, semi 1-40, 160 corse, Chromium): `main` 12 (pilota 3, avversari 9), `deriva` 19 (pilota 6, avversari 13). Casi del pilota riletti: in tutti la barca arriva **da sinistra della boa** e punta il punto 0 (a destra della boa, 3 m sopra): la retta la fa passare **sopra** la boa da sinistra a destra, cioè dal lato sbagliato. Il difetto c'era già su `main`; la guida nuova lo rende più frequente. **Correzione:** al primo lato (bastone), se la retta verso il punto 0 incrocia la verticale della boa a meno di 3 m sotto la boa (`PASSO_M`, già usato al §11), si va prima al punto 2 (sotto e a sinistra), che c'è già per ritentare. **Criteri:** B1 sui semi 1-40, boe sbagliate in tutto al massimo quanto `main` (12); conferma sui semi 41-80, al massimo quanto `main` sugli stessi semi. B2 `misura_avversari.py` (semi 361-380): non arrivate 0, boe sbagliate non più di prima, arrivo mediano al massimo +3%. B3 `collaudo_giro_boa.py` non peggiore di prima. B4 il seme 5 del torneo di `collaudo_moviola` si riguarda e si dice.

**Collaudi da sistemare, senza cambiare il gioco:** G12 di `collaudo_giri_avversari` (i due casi sono a 1,50 e 1,51 m/s, proprio sulla soglia di 1,5 della guida: il campione del collaudo e l'istante della scelta cadono ai due lati; si escludono i casi entro 0,05 m/s dalla soglia, come già si escludono quelli vicini alla poppa); G4 dello stesso collaudo (durate 20-21 s, dentro 12-30, ma su 8-11 casi contro i 15 chiesti: con meno contatti ci sono meno doppi giri; servono più regate); `collaudo_registratore_barche` G4 costruito; `collaudo_contatto_vero` in Firefox (un istante di 1/240 s, tre barche insieme: la spinta fra due fa sovrapporre per 4 mm la terza, che ha il contatto al passo dopo; da rendere noto con la spiegazione, dopo averlo verificato).

**Esiti della correzione delle boe** (codice congelato prima di guardare la conferma): B1 semi 1-40 da 19 a **2** (`main` 12); conferma semi 41-80 **2** (`main` 9). B2 (`misura_avversari.py`, 361-380, prima → dopo): non arrivate 0 → 0; boe sbagliate Chromium 1 → 2, Firefox 7 → 0; arrivi mediani entro ±2 s; penalità uguali ±1. B3 `collaudo_giro_boa.py` OK. **B4, seme 5 del torneo: non è la boa.** Il pilota naviga quasi parallelo a Rossa e «cede» per 60 s di fila, allontanandosi di 140 m dalla boa, poi chiude fuori tempo. Il limite di 25 s agli scarti (`SCARTO_MAX`) c'è, ma il suo orologio si azzera ogni volta che per un istante non c'è una barca in rotta di collisione: con due barche parallele succede di continuo.

**Correzione:** l'orologio dello scarto si azzera solo dopo **5 s** di via libera (ipotesi nostra). **Criteri:** M1 il seme 5 arriva, e i semi 1-12 del torneo di `collaudo_moviola` arrivano tutti (V1 e V3 verdi); M2 `misura_avversari.py` (361-380, due browser) non arrivate 0, penalità al massimo +10%, arrivo mediano al massimo +3%; M3 boe sbagliate (semi 1-40) non più di 2+2; M4 `collaudo_giro_boa.py` e `collaudo_avversari1b.py` verdi.

**Esiti dell'orologio dello scarto, prima prova:** M1 sì (i 12 semi del torneo arrivano, il seme 5 a 250 s); M3 sì (boe sbagliate 1); M4 sì. **M2 no in Firefox:** penalità da 158 a 214 (+35%), quasi tutte prima del via (da 109 a 154); Chromium da 171 a 182 (+6%). Prima del via le barche in attesa stanno spesso parallele, e smettere di cedere dopo 25 s le fa toccare. **Cambiato dopo aver visto i numeri, e lo dico:** la correzione vale solo dopo il via, dove era nato il difetto. Soglie invariate; M2 si rimisura sui semi 361-380 e si conferma sui semi 381-400, mai usati per questo.

**`collaudo_moviola` V1 (prua entro 5°):** il 50° viene dal seme 10, in cui la barca del pilota scuffia; alla raddrizzata la prua cambia di colpo e il confronto cade fra i due istanti. Non dipende dalla guida. Il collaudo non confronta più la prua delle barche scuffiate (la posizione sì).

**Esiti dell'orologio dello scarto, seconda prova (solo dopo il via): non superata, correzione tolta.** Penalità (`misura_avversari.py`, prima → dopo): semi 361-380 Chromium 171 → 181 (+6%), Firefox 158 → 179 (**+13%**); conferma semi 381-400 Chromium 143 → 165 (**+15%**), Firefox 161 → 167 (+4%) con **una barca non arrivata**. Il seme 5 arriva e la moviola è verde, ma M2 non è rispettato: smettere di cedere dopo 25 s fa toccare di più anche in regata. `js/regate.js` contiene solo la correzione delle boe. Il seme 5 del torneo in `collaudo_moviola` (V3, pilota fuori tempo per 60 s di scarto accanto a Rossa) resta un fallimento noto e spiegato; il difetto della guida (due barche parallele che non smettono di cedere) resta da proporre.
