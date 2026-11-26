# Proposta: la barca M che non riparte da ferma (1.3.60)

Scritta il 26 novembre 2026, sera. **Il difetto** (regata di Ale del 26 nov, 20:44, 1.3.59, `registrazioni/regata-20261126-2044-intera.txt`): da 20 s prima del via a 27 s dopo la barca resta a 0,2-0,4 nodi con la prua a 40-55° dal vento e la vela cazzata; poi strambata violenta, scuffia, partenza a 94 s. **Causa:** nella barca M lo smorzamento della resistenza indotta è 0,1 (Day fig. 11, barca in movimento) invece di 0,4; da ferma, con la vela cazzata, la resistenza indotta pareggia la spinta verso 0,5 nodi. Con 12 nodi la barca M non riparte con la vela cazzata (la 1.3.58 arrivava a 5 nodi in 20 s); con 20 nodi non riparte nemmeno con la scotta lascata al 30%. Il banco della voce 84 partiva sempre con la barca in movimento.

## Criteri (scritti dopo la prima prova di correzione, prima del via di Ale)

| | Criterio | Soglia |
|---|---|---|
| R1 | Partenza da ferma | 12 nodi, 40-60° dal vento, vela cazzata: almeno 3 nodi in 20 s; 20 nodi: almeno 3 nodi con la scotta migliore fra 10 e 30% |
| R2 | Barca in movimento | sopra i 3 nodi come M (polare sopra i 30°, medaglie) |
| R3 | Virata da ferma | partendo da 0,4 nodi fallisce (`raffiche_e_virate.js`) |
| R4 | Angolo morto | a 20-25° dal vento, prua tenuta dritta (polare): sotto 0,5 nodi |
| R5 | Lezioni | la 18 «Stare fermi», la 6.3 e le medaglie non peggiorano |

## Correzione (via di Ale, 26 nov: «ok via alla 1.3.60»)

Smorzamento 0,3 da fermo, che scende a 0,1 fra 0,3 e 1,5 m/s (0,6-2,9 nodi): **taratura** su R1 e R3, scelta in una griglia (da fermo 0,2 / 0,25 / 0,28 / 0,3 / 0,35 / 0,4; rampa fino a 0,9 o 1,5 m/s) come il valore più piccolo che passa R1 e R3. Con la rampa corta (fino a 0,9 m/s) R1 a 20 nodi non passa a nessun valore. Controllo su dati non usati per sceglierla: R2, R5, angolo morto della 84.

## Esito

| | Esito | Numeri |
|---|---|---|
| R1 | ok | 12 nodi vela cazzata 4,9-5,2 nodi dopo 20 s (1.3.59: 0,3-0,4); 20 nodi la scotta migliore 4,9 (1.3.59: 0,2-0,4) |
| R2 | ok | polare identica sopra i 30°, tranne 15 nodi a 30°: 0,2 → 3,2 (era bloccata dallo stesso difetto); medaglie: tempi del pilota identici alla 1.3.59, ESITO OK (Chromium, semi 101-130) |
| R3 | ok | virata da 0,4 nodi fallita (prua a 26°, 0,7 nodi) |
| R4 | **no** | 6 nodi a 25° 1,6 nodi, 10 nodi a 25° 1,4. **Non passava già con la 1.3.59** (6 nodi a 25° 1,3): è la vela di M che porta con poco vento apparente, non questo difetto. Il criterio della 84 (0-15° da ferma) passa |
| R5 | ok, con un difetto già nella 1.3.59 | 6.3 guidando 30/30, a mani ferme 0/30, dopo un colpo lungo 1/30 (1.3.59: 2 e 8); 41 passi col pilota, semi 1-3: niente da guardare. **«Stare fermi» F2 non passa né qui né nella 1.3.59**: con M la barca ferma con la vela lascata non scarroccia fuori dal cerchio, quindi il passo si completa senza toccare la scotta. Da rivedere la lezione (voce nuova in `DA-FARE.md`) |
