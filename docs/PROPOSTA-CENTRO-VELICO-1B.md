# Proposta: altezza del centro velico della barca dell'1b

Stato: **chiusa con la scelta 1** (Ale, 23 ottobre 2026): `zCE` resta 2,0 m, limite dichiarato in `FISICA-E-TARATURE.md`; nessun codice. Nata dalla ricerca della 1.0.46 (`PROPOSTA-ORZIERA-1B.md`): `zCE` 2,0 m è senza fonte, le fonti indicano circa 2,6 m. Ultimo passo prima del congelamento della barca.

## Cosa dicono le fonti
- **F17** (Day 2017, VPP della nostra barca): centro velico al 36,4% dell'inferitura sopra il boma; **con vento forte il timoniere svergola la vela e lo scende al 32%**, e la portanza cala (depotenziamento, eq. 4 e sez. 2.2). Il suo momento raddrizzante (timoniere col baricentro fino a circa 0,52 volte la sua altezza dal centro, eq. 18) torna con il nostro: 75 kg a 1,0 m.
- Inferitura 5,13 m (due fonti secondarie sul web): centro velico 1,87 m sopra il boma (1,64 svergolata). Boma sull'acqua: non trovato, stima 0,6-0,9 m. **Totale circa 2,5-2,8 m** contro 2,0.

## Anteprima [banco fuori dal repository, solo barca dell'1b]

| | 2,0 m (oggi) | 2,6 m | 3,0 m |
|---|---|---|---|
| VMG di bolina 6 / 10 / 15 / 20 nodi | 2,13 / 3,08 / 3,84 / 4,16 | 2,13 / 3,08 / **3,66 / 3,82** | 2,13 / 3,08 / 3,54 / 3,64 |
| contro Day fig. 8 con 15 nodi (3,8) | +1% | **−4%** | −7% |
| timoniere tutto fuori di bolina | da circa 15 nodi | da circa 10-11 nodi | da 10 nodi |
| raffica di bolina da 10 a 16 / 18 nodi, senza reagire | 37° / 52° | 51° / **scuffia** | 59° / scuffia |
| virata con la freccia, 16 nodi (`virata1b.js`) | 2,9 s, minima 34% | **3,9 s, minima 18%** | non riesce |
| barca orziera, criterio 2 (14 nodi al traverso) | 1,06 °/s | 1,01 °/s | 1,64 °/s |

Fino a 10 nodi non cambia niente. Con vento forte la barca diventa più lenta di Day, scuffia prima e vira male.

## Il punto: nel gioco il timoniere non depotenzia la vela
Day ha il centro velico alto **e** la vela svergolata che lo abbassa e toglie portanza con vento forte. Il nostro motore non ha lo svergolamento: la vela porta sempre al massimo, e l'unico modo di scaricarla è lascare. Alzare solo `zCE` mette la parte della fonte che peggiora la barca senza quella che la salva. Con 2,0 m la VMG con 15 nodi coincide con Day (+1%): l'altezza più bassa fa, nei fatti, la parte del depotenziamento che manca.

## Decisione per Ale
1. **Lasciare 2,0 m e dichiararlo** (consiglio): «braccio sbandante più corto del vero (2,5-2,8 m), tiene conto in modo grezzo dello svergolamento della vela, che il motore non ha». Nessun codice, nessun collaudo.
2. **2,6 m solo nell'1b** (costante nuova, l'1a non cambia). Costi della tabella; la virata con 16 nodi esce dal criterio della 1.0.43.
3. **2,6 m più lo svergolamento come nel modello di Day.** È una novità grossa (un comando o un automatismo nuovo del timoniere): non prima del congelamento.

## Collaudi, se si sceglie la 2 (pochi, per risparmiare tempo)
Lancio io solo i banchi in Node (pochi secondi: `polare.js` e `raffiche_e_virate.js` per l'1a, poi `scarroccio1b.js`, `orziera1b.js`, `virata1b.js`) e nel browser soltanto `collaudo_torneo.py --veloce` e `collaudo_versione.py`. Il giro completo sul PC di Ale non serve per questo passo: basta quello che farà dopo il congelamento.

## Seconda misura (23 ottobre 2026, chiesta da Ale per togliersi il dubbio)
Banco fuori dal repository, barca dell'1b, VMG di bolina sulla rotta vera con la scotta migliore (cioè lascando quanto conviene, l'unico depotenziamento che il motore ha); raffica di bolina da 10 nodi senza reagire (scotta 0,1).

| `zCE` | VMG 12 / 15 / 18 / 20 nodi | scuffia con raffica da 10 a |
|---|---|---|
| 2,0 | 3,42 / 3,84 / 4,07 / 4,16 | 19,5 nodi |
| 2,2 | 3,42 / 3,77 / 3,97 / 4,04 | 18,5 |
| 2,4 | 3,40 / 3,72 / 3,86 / 3,92 | 18 |
| 2,6 | 3,40 / 3,66 / 3,77 / 3,82 | 17,5 |
| 2,8 | 3,36 / 3,59 / 3,69 / 3,73 | 17 |

Confronti: Day fig. 8 con 15 nodi 3,8 (VMG quasi piatta fra 10 e 15); F24, virate comprese, circa 4,0 oltre i 15 nodi (in linea retta quindi di più). **Con 2,6 m e oltre la barca sta sotto tutte e due le fonti con vento forte; con 2,0-2,2 m ci sta dentro.** Il dubbio si chiude per la scelta 1: l'altezza vera è probabilmente 2,5-2,8 m, ma nel nostro motore, senza svergolamento della vela, quella che riproduce le velocità delle fonti è 2,0-2,2 m. Non scelgo 2,2 per non tarare un numero sulle velocità: 2,0 è quello di sempre e sta già dentro.
