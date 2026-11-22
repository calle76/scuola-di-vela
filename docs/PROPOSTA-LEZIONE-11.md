# Proposta: rifare la lezione 11 («I salti di vento»)

*Fermata 1, 22 novembre 2026 sera (Opus). Nessun codice finché non arriva il via di Ale.*

## Da dove viene

Ale, 22 nov, dopo la sua «Regata nei salti di vento» delle 16:17 (1.3.42): «forse non ho capito come virare, come leggere scarso o buono e come vedere se il vento è persistente: sono io che non ho proprio capito le basi!». In quella regata il vento girava **sempre a destra** (da 0° a 18° in 170 s); la riga diceva scarso 5°, 7°, 10°, 12° sulla stessa mura e Ale ha virato a 12° come col vento che oscilla: fra 2:04 e 3:04 la rotta ottimale gli ha preso 84 m. Già il 20 nov Ale aveva detto che la lezione su scarso e buono va migliorata (`DECISIONI.md`).

## Cosa non va nella lezione di oggi (`LB5`, js/contenuti.js)

1. **Il vento persistente sta in una riga** («Due eccezioni…») e nel riepilogo: nessun esercizio, nessun modo di vederlo.
2. **Non insegna a riconoscere i due venti.** Dice cosa fare se oscilla e cosa fare se gira sempre, ma non come capire quale dei due è.
3. **L'esercizio insegna un riflesso solo:** «quando sei scarso di 7°, vira» (con il suggerimento in basso «vira adesso»). È proprio il riflesso che nella regata di Ale ha sbagliato.
4. **Il conto si fa con la Prua e una media a mente**; dalla 1.3.42 in regata c'è la riga «scarso / buono» sopra la bussola, che la lezione non mostra mai.

## Cosa dice la fonte (F41, Dellenbaugh, la sola: rivista, allenatore)

Di bolina prima si capisce se il vento oscilla o gira sempre dalla stessa parte. Se oscilla: si vira sugli scarsi e si resta sulle mure buone; la media si fa con la bussola prima del via. Se gira sempre dalla stessa parte: non si vira sugli scarsi, **si va verso il salto**. Vicino alla boa, quando resta un salto solo, lo si gioca come persistente; stare lontani dalle layline.

**Cosa la fonte non dice** e la lezione dirà come regola del gioco, dichiarata: «come si vede dal numero» (che sale e scende, o cresce sempre sulla stessa mura). È una conseguenza diretta delle due definizioni, non un dato.
**Prima del codice si cerca una seconda fonte** (libro o federazione: per esempio i manuali di regata FIV, RYA o US Sailing) per il passo «riconoscere il persistente»; se non si trova, il testo lo dice come oggi («una sola fonte»).

## La lezione nuova (modello più semplice)

Sette passi; i primi tre restano quasi come oggi (teoria e esempio), cambia il resto.

| # | Passo | Tipo | Cosa cambia |
| --- | --- | --- | --- |
| 1 | Il vento gira | teoria | come oggi |
| 2 | Scarso e buono | teoria | come oggi «Un esempio», più una riga: «nel gioco lo vedi anche scritto sopra la bussola» |
| 3 | **Due venti diversi** | teoria, nuovo | oscilla (va e torna) o persistente (gira sempre dalla stessa parte); le due regole **opposte**; come si vede dal numero: «scarso 8, poi media, poi buono 6, poi scarso 9: oscilla»; «scarso 5, 7, 10, 12 sulla stessa mura: persistente» (l'esempio è la regata di Ale) |
| 4 | Vira sugli scarsi | pratica, oscillante | come l'esercizio di oggi (due virate da scarsi, mai da buoni), ma **la riga sopra la bussola al posto del suggerimento «vira adesso»** |
| 5 | **Vai verso il salto** | pratica, persistente, nuovo | vedi sotto |
| 6 | **Vicino alla boa** | teoria, nuovo | un salto solo resta: si gioca come persistente; la layline gira col vento (rimando alla lezione delle layline) |
| 7 | Riepilogo | navigazione | testo nuovo in tre righe: riconosci, poi oscilla → vira sugli scarsi, persistente → vai verso il salto |

**Passo 5, «Vai verso il salto».** Vento medio da nord che gira sempre dalla stessa parte, una boa 200 m sopravento con le sue due layline disegnate. Si parte sulle mure che vanno **verso** il salto, quindi scarse e sempre più scarse. Consegna: «Il numero cresce: il vento è persistente. Non virare: tieni queste mure fino alla layline, poi vira e vai alla boa». Riuscito se la barca arriva alla boa (entro 15 m) con **al più 2 virate** e **nessuna virata da scarso prima della layline** (più di 20 m prima). Se si vira prima, il passo ricomincia con una frase che spiega perché.

**Quiz della lezione:** tre domande nuove sul riconoscere («scarso 5, 7, 10, 12 sulla stessa mura: che vento è?»; «il numero sale e scende ogni minuto: che cosa fai quando sei scarso?»; «vento persistente verso destra: da che parte vai?»), le altre restano.

## Costanti nuove (ipotesi nostre, nessuna fonte)

- **Rotazione del passo 5: 0,12 °/s** (in 150 s circa 18°), oscillazione sopra di 3° (come `SALTI2.persAmp` in basso). Nelle regate il persistente gira 0,05-0,10 °/s (`SALTI2.persRate`): nella lezione un po' più in fretta, perché il passo duri 2-3 minuti e non 5. Va scritto nel testo («qui il vento gira più in fretta che in mare»).
- Soglie del passo 5: boa entro 15 m, al più 2 virate, layline con 20 m di tolleranza.
- Nessun'altra: 7° e 3° restano quelle della lezione e della riga (1.3.42).

## Criteri (soglie: attese nostre)

| # | Criterio | Soglia |
| --- | --- | --- |
| L1 | **Il passo 5 premia la regola giusta e boccia quella sbagliata.** Tre piloti, 10 semi di scelta (2101-2110) e 10 di conferma (2111-2120): A «giusto» (tiene le mure fino alla layline), B «da oscillante» (vira a ogni scarso ≥ 7°), C «a caso» (vira ogni 30-60 s) | A riesce in ≥ 9 su 10 dei semi di conferma; B in ≤ 1 su 10; C in ≤ 2 su 10 |
| L2 | **La regola giusta è davvero più veloce** (il metro non è il passo): stessi semi, tempo fino alla boa | A più veloce di B in ≥ 8 su 10 dei semi di conferma |
| L3 | **Il passo 4 resta valido** con la riga al posto del suggerimento: come oggi in `collaudo_pilota_lezioni` | stessi esiti di oggi |
| L4 | **La riga nelle lezioni** solo nei passi 4 e 5 della lezione 11 (non nelle altre lezioni né negli altri passi): 0 fuori posto, numero uguale al conto (come S2 della 1.3.42) | 0 |
| L5 | **Spazio:** testi della lezione nel pannello senza scorrere (`collaudo_pannello_lezioni`), 0 px a 1360x650 | 0 px |
| L6 | **Il resto non cambia:** le altre lezioni, le regate e il torneo identici al bit; `polare`, `raffiche_e_virate`, `impronta1b` identici; quiz ed esame della lezione 11 coerenti col testo nuovo (`collaudo_quiz`, `collaudo_esame`) | 0 differenze |

Chromium e Firefox, uno per volta col freno.

## Rischi

- **Una sola fonte** per tutta la lezione, come oggi: se la seconda fonte non si trova, lo si dice nel testo.
- **Il passo 5 potrebbe essere troppo facile** (basta non virare): L1 lo controlla col pilota «a caso»; se C passa troppo spesso, si alza la richiesta (per esempio partire sulle mure sbagliate e dover virare prima verso il salto).
- **Lezione più lunga** (da 6 a 7 passi, un passo pratico in più di 2-3 minuti).
- **Medaglie e progressi della lezione 11:** chi l'ha già fatta la ritrova cambiata; i progressi restano (si aggiunge un passo, non si toglie).
- La riga che entra nella lezione cambia S3e del collaudo della 1.3.42 («0 scritte nella lezione 11»): il collaudo va aggiornato insieme, dicendolo.

## Lavoro stimato

Testi e passi in `js/contenuti.js` (lezione e quiz), il passo 5 (vento persistente con rotazione propria, boa con layline, condizione di riuscita) e la riga nelle lezioni in `js/gioco.js` e `js/disegno.js`, un collaudo nuovo (`collaudo_lezione_salti.py`, L1-L4). Una versione (1.3.43). Modello: Opus (il passo 5 e i piloti), i testi si possono rileggere con Sonnet.
