# Proposta: avversari in bolina, virare sugli scarsi (10 novembre 2026, notte)

Seconda correzione della `PROPOSTA-AVVERSARI-ROTTA.md`, §1. Ordine deciso da Ale il 9 novembre: poppa, poi bolina, poi cono d'ombra. Via in anticipo («vai avanti senza chiedere»): proposta e soglie committate **prima** di misurare.

## 1. Cosa succede (diagnosi del §1 della proposta della rotta)

- **Peso:** la bolina vale il 64% del tempo perso dagli avversari rispetto alla rotta ottimale, 24,8 s in mediana per lato (29%).
- **Il quarto peggiore** perde 49,8 s con 4,7 virate, contro le 2,5 della rotta ottimale.
- **Come decidono oggi** (`js/regate.js`, guida generale): virano quando scade il bordo, a durata sorteggiata (25-60 s i principianti, 35-90 s gli esperti), o negli ultimi 30 m. Del vento guardano solo l'angolo per tenere la bolina: **non virano sugli scarsi**.
- **La rotta ottimale invece** vira sugli scarsi (lo dice il motivo «virata sullo scarso» nella 1.2.22).

**Fonte, F41** (Dellenbaugh, «Windshift Rules of Thumb»):
- se il vento oscilla, si vira sugli scarsi e si resta sulle mure buone;
- lo scarso si misura rispetto alla prua media: nell'esempio, 10° sotto la media si vira;
- si sta lontani dalle layline;
- se il vento gira sempre dalla stessa parte, si va verso il salto.

## 2. Modello più semplice

Ogni avversario tiene la **media del vento che sente**: direzione del vento reale nel suo punto, media mobile su `T_MEDIA` = 60 s. È un'ipotesi nostra: l'oscillazione dei salti dura circa due minuti per mezzo giro.

In bolina, con le mure `s`, il vento è **scarso** di `d` gradi quando gira contro le mure (`s · (twd − media) ≤ −d`, la stessa convenzione della rotta ottimale).

- **Si vira sullo scarso:** se lo scarso arriva almeno a `SCARSO_AI` gradi e il bordo dura da almeno `BORDO_MIN_AI` = 10 s (ipotesi nostra, per non virare a raffica), si vira.
- **I bordi a tempo restano** come rete di sicurezza, ma lunghi il doppio di oggi: gli avversari non stanno per sempre su un bordo.
- **Gli ultimi 30 m e la boa non cambiano:** restano le regole di oggi.
- **Persistente:** niente di speciale. Con la rotazione sempre dalla stessa parte, la media resta indietro e si vira comunque verso il lato buono. È una semplificazione, da dichiarare.
- **Principianti ed esperti:** i principianti vedono gli scarsi solo da `SCARSO_AI + 4°`, quindi giocano peggio i salti. Ipotesi nostra, per lasciare la differenza fra livelli.

**Costante da scegliere:** `SCARSO_AI` ∈ {6, 8, 10}°. Il 10° è l'esempio di F41; 6° è lo `SCARSO` della rotta ottimale. `null` è spento, come oggi.

**Cosa non si tocca:** la fisica, chi cede, la partenza (solo dopo il via, `b.leg` ≥ 1), la poppa, i giri di boa, il giocatore.

**Rischi:**
- Le raffiche girano già il vento di qualche grado: se la media è corta gli avversari virano troppo spesso. Lo controlla B3.
- Più virate in mezzo al gruppo: lo controlla B4.

## 3. Criteri (soglie nostre, scritte prima di misurare)

`tests/misura_avversari_rotta.py`, contro il gioco di prima sugli stessi semi (con la poppa della 1.2.24 se adottata). Scelta di `SCARSO_AI` sui **semi 1191-1220**, conferma sui **semi 1221-1250**, mai usati.

- **B1, bolina:** secondi persi sul lato di bolina, mediana, almeno −15%.
- **B2, arrivo mediano degli avversari:** non peggiora.
- **B3, virate per lato di bolina:** media non oltre +0,5.
- **B4, contatti dopo il via:** al massimo +10%.
- **B5, boe:** boa toccata al massimo il più grande fra +10% e +5; sbagliate al massimo +2; non arrivate non aumentano.
- **B6, Scuola:** `collaudo_regate.py` 6 0, 6 1 e `--lungo`, nessuna «BLOCCATA».
- **B7, non-regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.

Fra i valori che passano si sceglie quello che perde meno in bolina (B1). A parità, quello con meno virate. Se nessuno passa, gli avversari restano come sono e lo si riporta.

## 4. Esito della scelta (semi 1191-1220, 240 regate del torneo sulla 1.2.24): nessuno passa B1

| `SCARSO_AI` | B1 bolina, persi mediana | B2 arrivo | B3 virate per lato | B4 contatti | B5 boa toccata / sbagliate / non arrivate |
| --- | --- | --- | --- | --- | --- |
| spento | 23,4 s | 198,1 s | 3,72 | 165 | 61 / 0 / 0 |
| 6° | 20,0 s (**−14,6%** ✗) | 197,4 s | 3,14 | 138 | 33 / 0 / 0 |
| 8° | 20,2 s (−13,7% ✗) | 197,8 s | 3,13 | 144 | 51 / 0 / 0 |
| 10° | 21,7 s (−7,3% ✗) | 199,3 s ✗ | 3,08 | 143 | 56 / 0 / 0 |

- **Soglie:** B1 ≤19,9 s (−15%), B2 ≤198,1 s.
- **6° e 8°** migliorano tutti gli altri numeri: arrivo, virate, contatti, boa toccata. Mancano la soglia B1 di 0,4 e 1,3 punti. La soglia non si cambia: **non adottato**. Il codice resta spento (`SCARSO_AI` null).

## 5. Seconda prova, dichiarata prima di misurare (10 novembre, notte)

**Una sola prova in più.** Come la seconda prova della boa (`PROPOSTA-BOA-PIANTATA.md` §8), si cambia una cosa sola: la durata della media del vento.
- **Perché:** con 60 s la media sta indietro di circa mezza oscillazione dei salti.
- **`T_MEDIA` ∈ {30, 120}** s, con `SCARSO_AI` 6° (il migliore del §4).
- **Criteri:** gli stessi B1-B7, soglie uguali.
- **Semi nuovi:** scelta **1251-1280**, conferma **1281-1310**. Il riferimento è il gioco della 1.2.24 sugli stessi semi.

Se nessuna delle due passa, la bolina degli avversari resta com'è e lo si riporta, senza altre prove questa notte.

## 6. Esito della seconda prova (semi 1251-1280): non passa, stop

| `T_MEDIA` (con `SCARSO_AI` 6°) | B1 bolina, persi mediana | B2 arrivo | B3 virate per lato | B4 contatti | B5 boa toccata / sbagliate / non arrivate |
| --- | --- | --- | --- | --- | --- |
| spento (1.2.24) | 22,7 s | 197,5 s | 3,79 | 106 | 51 / 0 / 0 |
| 30 s | 21,5 s (−5,2% ✗) | 198,0 s ✗ | 3,17 | **143** (+35% ✗) | 55 / 0 / 0 |
| 120 s | 22,1 s (−2,5% ✗) | 198,8 s ✗ | 3,38 | **163** (+54% ✗) | 37 / 0 / 0 |

**Non passa niente.** Come scritto nel §5, la bolina degli avversari resta quella della 1.2.24. Il codice non è nel gioco: sta in `sperimentale/avversari-bolina-scarsi/scarsi.patch` (si applica sulla 1.2.24).

**Cosa si è imparato:**
- **Virare sugli scarsi aiuta ma poco:** −14,6% al meglio, e solo con la media di 60 s. Con 30 o 120 s quasi niente. Il resto della perdita in bolina sta altrove:
  - le virate vicino alla boa (`PROPOSTA-LAYLINE.md` §5, osservazione 113);
  - l'angolo di bolina dei principianti, 49-54° di prua contro i 45-46° della polare;
  - la regolazione della vela (`ai.trim`, sbagliata a caso di ±2-6°).
- **I contatti di riferimento cambiano molto da un gruppo di semi all'altro:** 165 sui semi 1191-1220, 106 sui 1251-1280. Il +35% e il +54% vanno letti con questo in mente, ma restano sopra soglia.

**Prossimo passo proposto:** misurare quanto pesa ognuna delle tre cause sopra, togliendone una alla volta a mano, prima di proporre altro. È una diagnosi, non una correzione.

## 7. Diagnosi delle cause in bolina (10 novembre, mattina; Ale: «parti dalla diagnosi della bolina senza chiedere»)

Non è una correzione: il gioco non cambia. Nello strumento (`misura_avversari_rotta.py`) si toglie **una causa alla volta**, solo durante la misura, e si guarda quanto cala il tempo perso in bolina rispetto alla rotta ottimale.

Il tempo perso è diviso in due:
- **ultimi 40 m:** dall'ingresso nel cerchio di 40 m dalla boa 1 al giro, contro la rotta ottimale da quel punto;
- **il resto della bolina.**

Semi **1311-1340**, mai usati, le 4 regate del torneo, principianti ed esperti, gioco della 1.2.24.

| Prova | Cosa si toglie |
| --- | --- |
| riferimento | niente |
| `DIAGUP=45` | angolo di bolina: tutti a 45° di prua, circa la bolina della polare con lo scarroccio (oggi esperti 45-48°, principianti 49-54°) |
| `DIAGTRIM=0` | errore di regolazione della vela: `ai.trim` a 0 (oggi ±2° gli esperti, ±6° i principianti) |
| tutte e due | i due insieme |

Le virate vicino alla boa e i bordi a tempo non si possono togliere senza cambiare la guida. Il loro peso si legge dalla parte «ultimi 40 m» e da quello che resta nelle prove sopra.

## 8. Esito della diagnosi (semi 1311-1340, 240 regate del torneo, 1.2.24)

| Prova | Bolina, persi media (mediana) | Principianti / esperti, mediana | Ultimi 40 m dalla boa 1: persi media (mediana), virate | Quota degli ultimi 40 m sulla prima bolina |
| --- | --- | --- | --- | --- |
| riferimento | 28,0 s (23,6) | 29,6 / 18,0 s | 11,4 s (6,9), 1,68 | 41% |
| angolo 45° | 26,4 s (21,0) | 23,9 / 18,3 s | 10,7 s (6,4), 1,61 | 41% |
| vela regolata | 26,6 s (22,5) | 24,4 / 21,9 s | 11,8 s (6,6), 1,73 | 44% |
| tutte e due | 22,9 s (20,3) | 19,6 / 21,1 s | 8,8 s (5,7), 1,44 | 38% |

**Cosa vuol dire:**
- **Ultimi 40 m prima della boa 1: il pezzo più grosso.** Lì gli avversari perdono 11,4 s a passaggio in media, con 1,7 virate. È il 41% di quello che perdono nella prima bolina: è la confusione dell'osservazione 113.
- **Angolo e regolazione insieme valgono il 18%** (−5,1 s), ma soprattutto per i principianti, che arrivano al livello degli esperti. È la **differenza fra livelli**, voluta (`aiParams`): non si corregge.
- **Il resto, circa il 40%,** sta in mezzo alla bolina: bordi a tempo e salti non giocati. La prova «sugli scarsi» (§4-6) ne ha preso solo una parte.

**Quindi la correzione da provare è l'avvicinamento alla boa.**

## 9. Correzione: avvicinamento alla boa con il giro diretto da più lontano (scritta prima di misurare)

**Modello.** Il giro diretto della 1.2.20 (`PROPOSTA-BOA-PIANTATA.md` §8) scatta solo entro `R_DIR` = 15 m dalla boa. Chi è mure a dritta, a destra della boa, e di bolina passa sopra la boa di almeno 3 m, va oltre la boa tenendo la bolina, invece di puntare prima il punto di passaggio a destra della boa.

Da più lontano lo stesso vale **sulla layline**: chi ci arriva mure a dritta non ha bisogno del punto di passaggio. Oggi lo punta, ci gira intorno negli ultimi 30 m e vira due volte.

Si allarga solo `R_DIR`; nient'altro cambia.

**Costante:** `R_DIR` ∈ {40, 80} m (oggi 15). Ipotesi nostra: 40 m è il raggio della misura, 80 m è metà della bolina del torneo.

**Criteri** (soglie nostre, `misura_avversari_rotta.py` con `RDIR`, contro la 1.2.24 sugli stessi semi). Scelta sui **semi 1341-1370**, conferma sui **semi 1371-1400**, mai usati.
- **A1, ultimi 40 m:** secondi persi in media almeno −25%.
- **A2, arrivo mediano degli avversari:** non peggiora.
- **A3, virate negli ultimi 40 m:** non aumentano.
- **A4, contatti dopo il via:** al massimo +10%.
- **A5, boe:** boa toccata al massimo il più grande fra +10% e +5; sbagliate al massimo +2; non arrivate non aumentano.
- **A6, Scuola:** `collaudo_regate.py` 6 0, 6 1 e `--lungo`, nessuna «BLOCCATA».
- **A7, non-regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.

Fra i valori che passano si sceglie quello che perde meno negli ultimi 40 m. Se nessuno passa, `R_DIR` resta 15.
