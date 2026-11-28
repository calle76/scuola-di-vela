# Proposta: chi supera da dietro sottovento (regole 17 e 14), voce 98

28 novembre 2026. Fermata 1: solo proposta, `js/` non toccato. Nasce dall'oss. 154 (regata di Lucio del 28/11 00:05, 1.3.77).

## Il caso (letto nel file, secondo per secondo)

Lasco, mure a dritta, verso la boa 3 (stimata dai passaggi a circa (416, 235)). La Blu arriva da dietro, sottovento a Lucio, più veloce di 0,1-0,5 nodi. Fra 308 e 320 s Lucio poggia (prua 53-56°) e la distanza di lato scende da 12 a 7 m; poi la Blu tiene 61° contro i 58-60° di Lucio e chiude piano (da 5 a 1,2 m di lato in 25 s). A 339 s la guida della Blu segna «cede a Tu» (regola 12, giusto); verso 340-342 s si affiancano (la prua della Blu passa la poppa di Lucio, barca lunga 4,2 m) e la precedenza passa alla Blu (regola 11). Contatto a 351,9 s, colpa a Lucio per la 11: **giusta**, anche per la 15 (il contatto è 10 s dopo l'affiancamento, oltre la finestra del gioco di 5,2 s).

- **Regola 17 (F15, parafrasata):** chi da dietro si affianca sottovento entro due lunghezze, con le stesse mure, non può andare più all'orza della sua rotta propria finché restano affiancate entro quella distanza (salvo passare subito di poppa all'altra). Rotta propria (definizione F15): la rotta che terrebbe per finire il lato al più presto se le altre barche non ci fossero; prima del via non c'è. **Nel gioco la 17 non c'è.** In questo caso però la Blu andava verso la boa: dalla Blu, la boa stava a 59° e la sua prua era 60-61°. **La 17 qui non avrebbe cambiato quasi niente.**
- **Regola 14 (F15, parafrasata):** se è ragionevolmente possibile, ogni barca evita il contatto; chi ha la precedenza deve agire solo quando è chiaro che l'altra non sta cedendo. **Questo è il punto debole.** La guida dei rivali, quando ha la precedenza, a meno di 1,5 lunghezze (`ULTIMO`, 6,3 m fra i centri) prova degli scarti (`cedeAvv1b`, `js/regate.js:524`). Qui la Blu è rimasta entro 4,6 m per 10 s senza girare di un grado. **Perché non lo faccia non si capisce dal file:** va riprodotto (passo A).

## Cosa si propone

**A. Prima la causa (solo collaudo, nessun cambio):** una scena costruita apposta, `tests/collaudo_regola17.py`. Il pilota dei collaudi tiene una rotta fissa al lasco. Un rivale parte 8 m dietro e 10 m sottovento, un po' più veloce, verso una boa che lo porta a convergere di 2-3°. Variazioni: 20, con semi fissi (vento 8/12/16 nodi, distanza di lato 6-14 m, convergenza 0-5°). Si conta in quante c'è un contatto e si legge, nella guida, quale ramo di `cedeAvv1b` decide la prua negli ultimi 10 s. La correzione B si scrive solo dopo la causa trovata, e si riporta qui prima del codice.

**B. Regola 14 per chi ha la precedenza (la correzione vera):** quando la guida ha la precedenza, l'altra è a meno di `ULTIMO` lunghezze e la distanza non cresce, lo scarto deve davvero allontanare (prima la prua che si allontana, poi quella che passa più lontano); se nessuno scarto «passa», si prende comunque quello che allontana di più invece di tenere la rotta. Solo nelle regate di Deriva e dopo lo sparo (la Scuola resta invariata).

**C. Regola 17 (in due pezzi, il secondo solo se A mostra casi):**
- *Guida:* un rivale che si è affiancato da dietro sottovento entro 2 lunghezze, finché resta così, non orza più di `G17` sopra la sua rotta verso la boa (quella che la guida vuole senza le altre barche).
- *Penalità:* contatto in quella situazione con il rivale sopravento della sua rotta di più di `G17` → colpa al rivale «per la regola 17». **Semplificazione dichiarata:** per il giocatore la rotta propria non si conosce (non la sceglie il gioco), quindi la 17 non si applica al giocatore: se è lui a superare da sottovento, vale solo la 11 com'è oggi.

## Costanti

- 2 lunghezze: dal regolamento.
- `G17` = 5° (ipotesi nostra, scelta da Claude: più grande delle oscillazioni della guida in rotta libera, 1-3° in questo file; uguale alla G147 dell'oss. 147).
- Nessun'altra costante nuova in B (usa `ULTIMO` e `SCARTI` di oggi).

## Criteri (soglie nostre, scritte ora, prima di ogni misura)

1. **Scena (A, poi B):** con la correzione, contatti nella scena al massimo 2 su 20 e almeno il 50% in meno del gioco di oggi. Se il gioco di oggi ne ha meno di 4 su 20, la scena non distingue: si dichiara e si ripensa la scena prima di cambiare il gioco.
2. **Torneo, giro «Misura», 450 regate per gruppo** (scelta sui semi 2261-2410, conferma sui semi 2411-2560, mai guardati con la prova): contatti in tutto al massimo +5% (atteso: in calo); contatti con colpa del giocatore pilota invariati o in calo; arrivo mediano dei rivali al massimo +2 s; bolina degli esperti barca per barca, mediana al massimo +2 s; coppie dopo il via al massimo +20%; partenze anticipate al massimo +10%.
3. **Casi 80-83 di `collaudo_avversari_deriva.py`:** almeno 9 su 10 ciascuno (oggi 10 su 10).
4. **Scuola invariata:** `impronta1b.js` «25 corse identiche», `polare.js` e `raffiche_e_virate.js` uguali carattere per carattere.
5. Strumento: prima della prova si controlla che lo strumento veda i casi (contatti fra stesse mure con la barca sottovento arrivata da dietro nei 30 s prima): se nel gioco sono meno di 10 su 450 regate, i criteri 2 sui contatti non distinguono e si dichiara.

## Rischi

- Rivali più timidi quando hanno la precedenza: il giocatore impara che può «stringere» un rivale sottovento senza pagare. Coperto in parte dalla regola: la colpa resta al giocatore sopravento; cambia solo che il rivale prova a evitare.
- Scarti a 1-2 lunghezze in lasco: poggiare per allontanarsi può portare in poppa o in strambata vicino a un'altra barca (oss. 80: chi scende non torna verso la bolina). I criteri 2 sulle coppie e i contatti lo misurano.
- La parte C sulla penalità cambia la colpa in pochi casi; senza la parte guida, i rivali prenderebbero penalità nuove.

## Collaudi da toccare

Il nuovo `collaudo_regola17.py` (Chromium e Firefox). Se B cambia la guida: i 7 confronti al bit passano alla versione nuova (`RIF` in `collaudo_regola18`, `regole_15_16`, `freccia`, `storico_rivali`, `scotta_automatica`, `riquadro_bandiere`, `coach`). Giro completo su GitHub a fine lavoro.

## Fonti

F15 (World Sailing, RRS 2025-2028): regole 11, 12, 14, 15, 17 e definizione di rotta propria, lette nella copia locale il 28 novembre 2026.

## Esito (28 novembre 2026, via di Ale del mattino: «vai in autonomia»)

- **Passo A, causa:** non erano gli scarti a fallire. In `cedeAvv1b` un'altra barca conta solo se il momento dei centri più vicini cade entro `T_CEDE` = 15 s. Lucio e la Blu, quasi paralleli e alla stessa velocità, avevano quel momento a 18-37 s, e gli scafi si toccano prima (centri a 3,2 m). La Blu non vedeva Lucio. Dettagli in `sperimentale/regola-17/LEGGIMI.md`.
- **Criterio 1 e la scena:** la scena scritta qui («dietro») dava 1 contatto su 20 col gioco di oggi, cioè non distingueva. Aggiunta una scena «affiancata»; la velocità del giocatore è legata a quella del rivale e il seme si fissa prima di aprire la regata (scelte fatte dopo aver visto i numeri, dichiarate nel LEGGIMI). Vento solo 10 nodi (il collaudo non può cambiarlo, semplificazione dichiarata).
- **B adottata nella 1.3.78, solo per chi ha la precedenza di base (B2):** criteri 1-5 tutti passati, sui semi di scelta e su quelli di conferma. La prima prova (B1, anche per chi cede) non passava l'arrivo mediano (+2,3 s) e le coppie in conferma (+26,9%). Numeri in `CHANGELOG.md` 1.3.78.
- **C (regola 17) non fatta:** in questo caso era rispettata e la scena non ha mostrato casi in cui serva.
- **1.3.79 (dopo il giro completo sulla 1.3.78):** la regola vale solo lasciata la linea e a più di 40 m dalla boa da girare. In partenza una Blu finiva in poppa e non partiva; alla boa tre rivali insieme non giravano. Criteri ripassati rispetto alla 1.3.77. Nel torneo l'effetto sui contatti dopo un sorpasso da sottovento non è chiaro (71 → 55, 53 → 54).
