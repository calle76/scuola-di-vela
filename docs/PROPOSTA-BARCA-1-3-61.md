# Proposta: la barca della 1.3.61 (dopo il controllo completo del 26 nov)

Via di Ale (27 nov, «ok»). Tre cose insieme, dal controllo `sperimentale/barca-84/controllo/CONTROLLO.md`:
1. **Angolo morto** (voce 90, `PROPOSTA-ANGOLO-MORTO-M.md`): la portanza della tabella ORC si spegne col vento apparente fra 19° e 26° (`a1` 19°, scelto da Claude con la regola «più simile alla realtà possibile»).
2. **Tetto alla resistenza indotta della deriva:** al massimo il 15% della forza laterale. Fisica: una deriva di allungamento circa 4 al massimo della portanza dà una resistenza indotta di circa il 7-15% della portanza (CL / (π · allungamento)); la formula di oggi a bassa velocità la fa crescere senza limite. **0,15 e 0,25 provati su una copia prima di scrivere questi criteri** (16 nodi, vela cazzata, da ferma: 3,7-4,3 nodi con 0,15; 0,8-4,2 con 0,25): si sceglie 0,15, il bordo alto della teoria.
3. **Tabella delle velocità `js/rotta-dati.js` rigenerata** (`tests/fisica/polare_tabella.js --scrivi`) sulla barca finale: era ancora della barca vecchia (rotta ottimale, Coach, layline, guida dei rivali in layline e in poppa).

## Criteri (attese nostre, scritti prima di misurare sul gioco)

| | Criterio | Soglia |
|---|---|---|
| T1 | Partenza da ferma col vento forte | vela cazzata, da ferma, 16 nodi, prua a 40 / 60 / 90°: almeno 2 nodi entro 20 s |
| T2 | R1 e R3 della 1.3.60 | 12 nodi vela cazzata 40-60°: almeno 3 nodi in 20 s; virata da 0,4 nodi fallisce |
| T3 | Bolina come prima | Day e Binns 9 nodi entro 0,5 punti dai valori di `a1` 19 da solo (`PROPOSTA-ANGOLO-MORTO-M.md`) |
| T4 | Tabella | `rotta-dati.js` uguale a quello che scrive `polare_tabella.js` sul motore nuovo; `collaudo_layline.py` e `collaudo_coach.py` verdi |
| T5 | Il resto | impronte riscritte (cambio voluto); medaglie (regola di `PROPOSTA-MEDAGLIE-E-NOMI.md`: se i tempi cambiano, bande ricalcolate e confermate); lezioni col pilota (veloce) e 6.3 non peggiorano; «Stare fermi» F2 si riporta (voce 89) |

## Esito (27 novembre 2026)

| | Esito | Numeri |
|---|---|---|
| T1 | ok | 16 nodi, vela cazzata, da ferma: 2 nodi in 3,1 / 6,2 / 3,3 s a 40 / 60 / 90° (1.3.60: mai, restava a 0,8-1,1 nodi) |
| T2 | ok | 12 nodi vela cazzata 4,9-5,2 nodi dopo 20 s; virata da 0,4 nodi fallisce (prua a 24°, 0,8 nodi) |
| T3 | ok | Day −4,0 / −3,2 / −2,8%, Binns 9 nodi −4,4 / −2,9 / −4,1 / −5,0%: uguali ad `a1` 19 da solo. Angolo morto: a 30° 45 / 52 / 65% della velocità a 45° (6 / 10 / 15 nodi; con 15 nodi il tetto lo alza da 54 a 65%), a 25° al massimo 0,86 nodi |
| T4 | ok, con un controllo da guardare | `rotta-dati.js` riscritto da `polare_tabella.js` (10 nodi: 45° 4,6 → 5,2, 90° 6,0 → 6,2, 180° 4,1 → 4,5); `collaudo_layline` verde. `collaudo_coach`: **K1 rosso per forza** (confronta con la 1.3.10, barca vecchia); **K5a 1 caso su 4 fuori** (45°: Coach 6,5 s contro stima 4,8, soglia ±25%): la stima del collaudo usa il vento del primo istante, il Coach quello che cambia con le raffiche; con la tabella nuova la velocità a 45° cambia di più col vento. Non è un difetto del gioco; il collaudo va rivisto |
| T5 | in parte | Medaglie: la barca perde 2-3 s di bolina; bande nuove con la regola (uguali in Chromium e Firefox): prova 3 [140, 175, 225], 4 [250, 315, 400], 6 [215, 270, 345]; conferma semi 101-130 OK nei due browser. Lezioni col pilota (veloce): solo il caso noto 2.5 (1 su 3 dopo un colpo lungo). **Lezione 6.3 peggiora rispetto alla 1.3.60:** guidando 28/30 (30/30), dopo un colpo lungo 4/30 (1/30); a mani ferme 0/30. «Stare fermi» F2 rosso come nella 1.3.59-1.3.60 (voce 89) |
