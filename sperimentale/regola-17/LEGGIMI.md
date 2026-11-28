# Voce 98: chi supera da sottovento (regole 17 e 14), oss. 154

28 novembre 2026. Proposta: `docs/PROPOSTA-REGOLA-17.md`. Via di Ale il 28 nov mattina («vai in autonomia»).

## Passo A: la causa

**Letta nel file della regata di Lucio (28/11 00:05) e confermata con una copia del gioco segnata (righe di traccia in `cedeAvv1b`, fuori dal repo).** Fra 325 e 351,9 s la guida della Blu trova un'altra barca da guardare solo a 339,25 s (un istante, «cede a Tu»). Per il resto risponde «nessuna barca»: in `cedeAvv1b` una barca conta solo se il momento in cui i centri sono più vicini cade entro `T_CEDE` = 15 s. Lucio e la Blu andavano quasi paralleli (2-3° di differenza) e quasi alla stessa velocità, e quel momento era a 18-37 s nel futuro (conto sulle righe del file: a 330 s 37 s, a 345 s 18 s). Il contatto fra gli scafi però arriva prima: a 351,9 s i centri erano ancora a 3,2 m. La Blu quindi non ha mai provato a scostarsi: non erano gli scarti a fallire (come ipotizzava la proposta), è che la guida non vedeva Lucio.

La scena di diagnosi (copia segnata, Chromium) lo riproduce: rivale con la precedenza, affiancato, stessa velocità, «nessuna» per 40 s fino al contatto.

## Il collaudo: `tests/collaudo_regola17.py`

Due scene da 20 varianti, semi fissi (0-19 scelta, 20-39 conferma), regata nei salti (Deriva) senza salti, vento 10 nodi. Il collaudo non può cambiare il vento: la proposta diceva 8/12/16 nodi, semplificazione dichiarata. Il giocatore tiene una prua fissa che converge verso il rivale di `conv` gradi.

- **dietro** (la scena della proposta): il rivale parte 8 m dietro e 6-14 m sottovento, convergenza 0-5°.
- **affiancata** (aggiunta dopo il passo A, dichiarata): già affiancati, convergenza 1-5°.

**Cambi fatti dopo aver visto i numeri, dichiarati:**

1. La scena «dietro» con la scotta fissa dava 1 contatto su 20: sotto la soglia di 4 del criterio 1, quindi non distingue. Da qui la scena «affiancata».
2. Con la scotta fissa i rivali sorteggiati erano diversi fra Chromium e Firefox (4 contatti su 20 contro 0). Il seme ora si fissa anche prima di aprire la regata.
3. La velocità del giocatore ora è legata a quella del rivale: nella scena «dietro» il giocatore va al 90-97% della velocità del rivale, nella «affiancata» al 99-101%. Con il 97-100% il rivale passava davanti e i contatti venivano solo sopra il 99,6% (3 su 20).

| Contatti su 20 | gioco 1.3.77 | prova B1 | prova B2 |
| --- | --- | --- | --- |
| dietro, varianti 0-19 | 1 | 0 | 0 |
| dietro, varianti 20-39 | 4 | 0 | 0 |
| affiancata, varianti 0-19 | 14 | 0 | 0 |
| affiancata, varianti 20-39 | 11 | 0 | 0 |

Chromium; Firefox, varianti 0-19: gioco 1 e 14, B1 0 e 0 (gli stessi numeri).

## Le prove

- **B1 (`v98.patch`):** nelle regate di Deriva, dopo lo sparo, una barca a meno di `ULTIMO` lunghezze (6,3 m fra i centri) che si avvicina conta subito, come se il momento più vicino fosse adesso. Vale per tutte e due le barche, chi cede e chi ha la precedenza. Nessuna costante nuova; `V98 = false` torna alla 1.3.77.
- **B2 (`v98-precedenza.patch`):** come B1, ma solo per chi ha la precedenza di base (regole 10-13, `chiCede`, che non scrive niente; `chiCede1516` scrive la memoria della regola 16 e lì non si può chiamare). È la parte B della proposta com'era scritta.

Casi 80-83 di `collaudo_avversari_deriva.py` con B1: 10, 10, 10, 10 su 10.

## Misura grande (giro «Misura», Chromium, `misura_r17.py --conf m4 --lungo`, 450 regate per gruppo)

`leggi.py` legge le uscite. L'arrivo mediano è la mediana delle mediane dei pezzi (approssimazione dichiarata, come per l'oss. 147). «Sorpassi da sottovento» (lo strumento del criterio 5): contatti dopo il via con le stesse mure e la barca sottovento arrivata da dietro (tutta dietro la poppa dell'altra) nei 30 s prima.

**B1 (run 46116629890 e 46116632305):**

| | Scelta 2261-2410 | Conferma 2411-2560 | Soglia |
| --- | --- | --- | --- |
| contatti | 574 → 511 (−11,0%) | 498 → 452 (−9,2%) | +5% |
| colpa del pilota | 175 → 151 | 148 → 131 | non in aumento |
| arrivo mediano | 587,0 → 589,3 (+2,3 s) | 586,0 → 588,2 (+2,2 s) | **+2 s: no** |
| bolina esperti, barca per barca | mediana +0,0 s (media +0,20) | +0,0 s (+0,37) | +2 s |
| coppie dopo il via | 35 → 26 | 26 → 33 (+26,9%) | **+20%: no in conferma** |
| fuori linea allo sparo | 231 → 234 (+1,3%) | 194 → 199 (+2,6%) | +10% |
| strumento: sorpassi con contatto | 71 → 51 | 53 → 42 | almeno 10 nel gioco: sì |

B1 non passa (arrivo +2,2/+2,3 s contro +2; coppie +26,9% in conferma).

**B2 (run 46118874329 e 46118876680; il gioco di oggi ha dato le stesse uscite, al byte, dei giri di B1: misura ripetibile):**

| | Scelta 2261-2410 | Conferma 2411-2560 | Soglia |
| --- | --- | --- | --- |
| contatti | 574 → 511 (−11,0%) | 498 → 472 (−5,2%) | +5% |
| colpa del pilota | 175 → 146 | 148 → 137 | non in aumento |
| arrivo mediano | 587,0 → 588,7 (+1,7 s) | 586,0 → 587,5 (+1,5 s) | +2 s |
| bolina esperti, barca per barca | mediana +0,0 s (media +0,73) | +0,0 s (+0,98) | +2 s |
| coppie dopo il via | 35 → 26 | 26 → 24 | +20% |
| fuori linea allo sparo | 231 → 233 (+0,9%) | 194 → 194 | +10% |
| strumento: sorpassi con contatto | 71 → 50 | 53 → 47 | almeno 10 nel gioco: sì |

Casi 80-83 con B2: 10, 10, 10, 10 su 10. Scuola: `impronta1b.js` 25 corse identiche, `polare.js` e `raffiche_e_virate.js` identiche alla 1.3.77 carattere per carattere. **B2 passa tutti i criteri ed è nella 1.3.78.**

**Cosa resta:** i contatti dopo un sorpasso da sottovento calano (71 → 50, 53 → 47) ma non spariscono. Nel torneo il giocatore pilota non tiene una prua fissa, e chi supera da dietro (regola 12, prima di affiancarsi) non usa ancora la regola nuova: con B1 la usava, ma costava tempo e coppie. La regola 17 (rotta propria di chi supera da sottovento) non è entrata: nell'oss. 154 era rispettata e la scena non mostra casi in cui serva.

## 1.3.79: la regola solo lontano da linea e boe (`v98-1379.patch`, sopra la 1.3.78)

Il giro completo sulla 1.3.78 (run 46120775438) ha dato due rossi nuovi in Chromium, tutti e due causati dalla 1.3.78 (confronto con la 1.3.77 sugli stessi semi):

- `collaudo_non_partite` salti, seme 11, principianti, 5 minuti: la Blu non parte entro 60 s. Traccia: cede alla Rossa (prua 246°), poi ha la precedenza e lo scarto parte dalla prua già poggiata (232°, 128° dal vento). La regola della poppa (oss. 85, `GYBE_MIN`) vede una strambata che non c'è e per 10 s la tiene a 172° dal vento.
- `collaudo_avversari1b` scenario 5 (tre rivali alla boa): 10 → 8 su 10.

La regola ora vale solo con `leg >= 1` e a più di 40 m dalla boa da girare; lo scarto parte dalla rotta voluta. Misure contro la 1.3.77 (run 46126322329 e 46126325088): tutti i criteri passano (numeri in `CHANGELOG.md` 1.3.79). **Effetto nel torneo non chiaro:** contatti dopo un sorpasso da sottovento 71 → 55 (scelta) e 53 → 54 (conferma). La scena lo mostra (14 e 11 → 0 su 20), il torneo no: lì molti di quei contatti sono vicino alla linea o alle boe, dove ora la regola non vale, oppure il colpevole è il pilota che stringe.

## 1.3.80: solo stesse mure, non verso chi sconta, lontano anche dalla linea (`v98-1380.patch`, sopra la 1.3.79)

Dal giro sulla 1.3.79 (cinque pezzi su otto; gli altri li ha annullati il giro programmato) due rossi nuovi in Firefox, causati dalla regola (confronto con la 1.3.77 sul PC, seme 405):

- `collaudo_giri` D2: la Blu mure a dritta, con la precedenza su due barche mure a sinistra, si scostava; due contatti nuovi (27,2 e 28,4 s). Fra mure diverse chi ha la precedenza tiene la rotta (regola 16). → solo stesse mure.
- `collaudo_regola21` K4: la storia si separava già a 10-15 m dalla linea, subito dopo il via; il giocatore non arrivava a scontare. → anche a 40 m o più dalla linea. In più la regola non vale verso chi sconta o torna dietro la linea (regola 21); da sola questa parte non bastava per il seme 405.

Misure contro la 1.3.77 (run 46136864120 e 46136866725): tutti i criteri passano. Contatti dopo un sorpasso da sottovento 71 → 66 e 53 → 50: nel torneo l'effetto è piccolo; la scena resta 14 e 11 → 0.

**In tutto, quattro versioni:** B1 (anche chi cede: arrivo e coppie fuori soglia), B2 = 1.3.78 (giro: non partite e boa), 1.3.79 (giro: D2 e K4), 1.3.80. Ogni limite viene da un caso visto nel giro, con la causa letta nella traccia.
