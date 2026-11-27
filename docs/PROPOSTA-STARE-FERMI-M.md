# Proposta: «Stare fermi» con la barca M (voce 89; fermata 1, 27 novembre 2026, Opus)

**Il difetto** (`PROPOSTA-RIPARTENZA.md` §Esito, `collaudo_stare_fermi` F2 rosso dalla 1.3.59): con la barca M, ferma a 45° con la vela tutta lascata, la barca non esce dal cerchio di 8 m in 30 s, quindi il passo si supera senza toccare la scotta.

## 1. Cosa fa la barca M (misurato col motore della 1.3.61, banco in node, prua libera, barra al centro)

Vela tutta lascata, barca ferma all'inizio. Velocità dopo 30 s (meno = indietro) e quando esce dal cerchio di 8 m:

| prua | 6 nodi | 10 nodi | 14 nodi | barca 1b (13 nov), 10 nodi, 60 s |
| --- | --- | --- | --- | --- |
| 40° | −0,11, mai | −0,26, a 50 s | −0,35, a 31 s | −1,08 |
| 45° | **+0,13**, mai | **+0,26**, a 50 s | +0,29, a 31 s | −0,86 |
| 50° | +0,19, mai | +0,43, a 42 s | +0,52, a 30 s | −0,58 |
| 60° | +0,20, mai | +0,44, a 43 s | +0,56, a 31 s | +0,49 |

**Con M la vela tutta lascata a 45° spinge la barca avanti**, piano. Il testo della lezione («lasciata a sé, la barca va indietro e sottovento») oggi è falso nel gioco.

**La causa** (letta nel codice, `vela84` in `js/motore.js`): una vela libera (boma non tenuto dalla scotta) nel motore sta sempre a 2° dal vento apparente (`boom = A − 2`). La vela di M comincia a portare da 0° (`V84.a0 = 0`, rampa di 10°: ipotesi della voce 84 da Newman e Low), quindi a 2° ha ancora il 20% della portanza e la barca va avanti. Una vela che sbatte libera non porta.

## 2. Le fonti

- Lucio (13 nov, dal vero, `PROPOSTA-LEZIONE-STARE-FERMI.md`): se non fai niente, la barca va indietro.
- F87 (Chapin): se la barca comincia ad andare indietro si cazza un poco. F25 (WindCheck): stare quasi fermi con la vela che sbatte.
- Nessuna fonte dà la velocità all'indietro: le due cose sicure sono il verso (indietro) e che con la scotta si può tenere la barca ferma.

## 3. Proposta: la vela libera non porta (una costante del motore)

**`V84.a0` da 0 a 2°**: la vela comincia a portare dai 2° in su, cioè solo quando la scotta la tiene. **Ipotesi nostra** (TARATURA, dichiarata come le altre della 84): sceglie il valore più piccolo che fa sbattere la vela libera. Con 2 o 3 i numeri sono identici (provati tutti e due).

Prova su una copia (gioco invariato):

| | 1.3.61 | con a0 = 2 |
| --- | --- | --- |
| 45°, 10 nodi, vela lascata, 30 s | +0,26 nodi, 4,3 m | **−1,33 nodi, 16,4 m** (esce a 18 s) |
| 50° / 55° / 60°, 10 nodi | +0,43 / +0,36 / +0,44 | −0,89 / −0,37 / +0,33 |
| 45°, 6 / 14 nodi | +0,13 / +0,29 | −0,77 / −1,86 (esce a 29 s / 13 s) |
| pilota coi soli tasti della scotta (45°, 50°, 55°; 6, 10, 14 nodi; 20 semi ciascuno) | 160 su 180 (14 nodi a 50°: 0 su 20) | **180 su 180** |
| `polare.js`, `costo_manovre.js`, `virata1b.js`, `scarroccio1b.js` | | **identici** |
| `raffiche_e_virate.js` | | raffica «lascando» −1° di sbandamento, «senza reagire col boma a 21°» +2-3°; virata da 1,9 nodi 6,8 → 6,9 s |
| `impronta1b.js` | | 12 corse su 25 diverse (al bit: andature, virate, raffica lascando, ferma nel vento, indietro) |

La forma è quella della barca 1b (indietro fino a 55°, avanti a 60°), un po' più forte all'indietro (−1,33 contro −0,86 a 45°).

**Non cambia l'angolo morto R4** (a 25° la barca da ferma avanza: 0,62-0,73 nodi, identico): è un'altra causa.

**La lezione non cambia** se la barca torna ad andare indietro. A 55° con 6 nodi si supera ancora senza scotta (era il punto debole già noto della 1.3.58, F2 è scritto a 45°).

## 4. Criteri (soglie nostre, scritte prima di toccare il gioco)

- **S1** `polare.js` identico; `rotta-dati.js` rigenerato identico (se no, si rigenera e si dice).
- **S2** `collaudo_stare_fermi`: F1 almeno 18 su 20 (semi 1-20 e 21-40), F2 rosso → verde, F4, F5; in Chromium e Firefox.
- **S3** banco: a 45° con 6, 10, 14 nodi la barca lascata va indietro dopo 30 s; il pilota della scotta almeno 18 su 20 in ogni caso della tabella.
- **S4** non peggiorano: lezioni col pilota (veloce), 6.3, partenza da ferma (R1, R3 della 1.3.60), medaglie (tempi del pilota, prove 2-6); `raffiche_e_virate.txt` e `impronta1b.txt` riscritti (cambio voluto).
- **S5** `collaudo_esercizi_regata` C2 (lezione 19, fermi fino al via) verde.

## 5. Rischi

- È un cambio della barca: lista di `cambio-barca` (rotta-dati, banchi, barca da ferma, vento forte, angolo morto). La polare non si muove, quindi rotta, rivali e medaglie dovrebbero restare uguali; si misura.
- In partenza i rivali aspettano con la vela lascata: con a0 = 2 andranno indietro più di oggi. Da guardare nelle regate (contatti al via, `misura_rivali_lunghe` della voce 2 da rifare se cambia).
- −1,3 nodi all'indietro con 10 nodi può essere troppo: nessuna fonte numerica.

## 6. Cosa serve da Ale

Il via ad a0 = 2 nel motore (1.3.62), oppure no e si cambia solo il testo della lezione (la barca resta quella che avanza piano: il passo andrebbe ripensato da capo).

## Esito (1.3.63, 27 novembre 2026, Opus)

Fatto con **a0 = 1°** invece di 2° (scelto dopo aver visto la bolina a 22 nodi: −7,4% con 2°, −3,6% con 1°). Passano S2, S3, S5; S1 solo per la polare (`rotta-dati.js` cambia fra 17 e 20 nodi); **S4 non passa per la lezione 6.3** (guidando 16 su 99 non completate, prima 8 su 97). Numeri in `CHANGELOG.md` 1.3.63.
