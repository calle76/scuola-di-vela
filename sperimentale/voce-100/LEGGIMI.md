# Voce 100: quanto pesa la regola 17 (conto prima della proposta)

28 novembre 2026. Richiesta di Ale: «prima conta quanto pesa la regola 17, poi dimmi se vale la pena farla». Niente cambi al gioco: solo misura.

## Cosa si conta (scritto prima di misurare)

La regola 17 (F15, parafrasata): una barca che da dietro si affianca sottovento a un'altra con le stesse mure, entro due lunghezze, finché restano affiancate così non deve andare sopra la sua rotta propria. Nel gioco oggi in quel caso la colpa di un contatto è della sopravento (regola 11).

**Caso 17** = contatto dopo il via, stesse mure (`st`), la sottovento era tutta dietro la sopravento in un momento dei 30 s prima (`dietro`), al primo campione affiancata la distanza di lato era al più 8,4 m (2 lunghezze, `lat0`), la sottovento è un rivale e sta più di 5° sopra la sua rotta propria (`sopra` > `G17`, la costante della proposta). La rotta propria è approssimata con la prua che la guida vuole prima di cedere (`b.dProp`, patch di sola misura `dprop.patch`): semplificazione dichiarata. Per il giocatore la rotta propria non si conosce: se è lui a superare da sottovento, il caso non si conta (come nella proposta).

Si riportano anche i limiti larghi: gli stessi contatti senza la condizione su `sopra` (tetto massimo).

**Soglia per «vale la pena» (scelta di Claude, dichiarata prima):** la parte «penalità» vale la pena se i casi 17 con colpa oggi al giocatore pilota sono almeno 1 ogni 30 regate lunghe (un torneo da 3 regate su 10); sotto, la regola cambierebbe la colpa così di rado che il giocatore non se ne accorgerebbe.

## Strumento

`misura_r100.py` (copia di `sperimentale/regola-17/misura_r17.py` con `lat0` e `sopra` nelle righe CONT), giro «Misura», `--conf m4 --lungo`, patch `sperimentale/voce-100/dprop.patch`, semi 2261-2560 (450 + 450 regate).
