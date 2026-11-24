# Proposta: vela, braccio e rampa insieme (voce 81, seconda proposta)

*Fermata 1, 25 novembre 2026. Ale: «Si vai». Nessun codice nel motore finché non arriva il via. Parte da `PROPOSTA-BOLINA-POCO-VENTO.md` (ultime due parti).*

## Il difetto

Con 3-9 nodi la bolina del gioco è del 10-16% più lenta di Day, di Binns e delle misure in acqua di F109; la virata con 3,2 nodi perde 1,74 m invece di 0,67. La resistenza in acqua del gioco è vicina alla tesi F121; **manca la spinta della vela**.

## Modello più semplice (tre costanti, nessuna formula nuova)

| Costante | Oggi | Proposta | Da dove | Stato |
|---|---|---|---|---|
| `luffA0` (rampa della vela) | 22° | 15° | La tabella ORC usata da Day dà CL 1,35 a 28° e 1,16 a 12°: la vela porta già a 12°. 15° è una scelta nostra prudente; 9°, 15° e 18° danno la stessa velocità in linea retta | principio con fonte, **numero ipotesi** |
| `sailCL2` (resistenza della vela) | 0,08 (CD 0,34) | 0,042 (CD 0,27) | Day: ORC 0,20 più il timoniere, circa 0,07 (conto del 16 ottobre). Flay dà 0,27 **senza** timoniere, cioè 0,34 con: le due fonti non vanno d'accordo, Day sceglie ORC | con fonte, ma contesa |
| `zCE` (braccio sbandante) | 2,0 m | 2,4 m | Le fonti danno **3,0 m** (F121: centro velico 2,68 m sull'acqua, deriva al 43-45%). 2,4 è a metà strada: con 2,8-3,0 la barca non vira più bene a 16 nodi e le raffiche la rovesciano, perché il motore non ha lo svergolamento della vela | **compromesso dichiarato, senza fonte per il 2,4** |

`minBoom` resta 9. Alternative provate e scartate: braccio 3,0 (a 16 nodi la virata con la freccia fallisce o dura oltre 5 s), braccio 2,0 (12 nodi +4/+5%, 15 nodi +11%), svergolamento con il braccio che cala a vento forte (12 nodi ancora −1/−4%).

## Cosa dà sul banco (già visto: non è una prova alla cieca)

`sperimentale/bolina-81/esplora81.js`, `prua_imposta.js`, test fisici con le costanti cambiate in memoria.

| Criterio della prima proposta | Soglia | Oggi | Proposta | Esito |
|---|---|---|---|---|
| B1 Day 6 nodi | −5% | −16% | −9% | **no** |
| B2 Binns 9 nodi, 42-60° | ±5% | −15 −12 −14 −15 | −6 −7 −10 −11 | **no** |
| B3 Binns 12 nodi | ±3% | −2 … 0 | +2 0 0 0 +1 | passa |
| B4 Day 15 nodi | ≤ +7% | +6% | +6% | passa |
| B5 3,2 nodi a 45° (prua imposta; 1,05 m/s) | −8% | 0,88 (−16%) | 0,96 (−8,6%); scotta migliore 0,99 | **no, per 0,6 punti** |
| B6 virata 3,2 nodi, 10 s | −30% | −1,74 m | −1,24 m (−29%) | **no, per un punto** |
| B7 poppa e lasco | 0,03 nodi | 7,19 / 5,62 / 4,66 (90/135/180°, 12 nodi) | 7,50 / 5,57 / 4,62 | **no** |
| B8 una costante con fonte | sì | — | tre | **no** |

Tesi F121 (2, 3, 4, 5 nodi di barca, ottimista): −11 −12 −12 −5% oggi, −2 −4 −5 0% con la proposta.

**In breve:** lo scarto col poco vento si riduce circa della metà (meno a 55-60° con 9 nodi), i 12 e 15 nodi restano come oggi. **Due criteri su otto passano.** Con `luffA0` 9 la virata passa (−1,05 m, −40%), ma la barca avanza a 25° dal vento: l'angolo morto quasi sparisce.

## Cosa peggiora o cambia (misurato sul banco)

- **Raffiche:** da 10 a 16 nodi senza reagire 37° → 45° (lascando 19° → 23°); da 10 a 18: 52° → **61°, scuffia** (28° → 34°); da 10 a 20: 65° → 73° (38° → 46°). Gioco più difficile, lezioni «raffica» e «scuffia» da rivedere.
- **Virata:** `virata1b` criterio 1 fuori a 6 nodi (freccia 3,6 s e minima 63%) e a 12 nodi (2,4 s e minima 55%); a 16 nodi rientra (2,7 s, 44%).
- **Angolo morto:** con 6 nodi la barca fa 2,05 nodi a 30° (oggi 0,86) e 1,19 a 25° (oggi −0,11). La VMG migliore resta intorno ai 39-46°. Cambiano la lezione «Orzare e l'angolo morto», il messaggio «la vela sbatte» (scatta a `luffA0 + luffW/2`: 25,5° → 18,5°), i filetti e il suggerimento della scotta.
- **Traverso con 12 nodi:** +0,3 nodi (7,19 → 7,50), conseguenza della vela che frena meno.
- **Rivali, tempi, medaglie, record, stagione:** da rimisurare tutti.

## Criteri per la fermata 2 (scritti ora)

I numeri del banco sopra sono noti: i criteri nuovi sono **quelli non ancora visti**. Dichiaro una soglia diversa dalla prima proposta per B1, B2, B5, B6 e B7, **dopo averli visti**: la proposta non li passa.

| # | Cosa | Soglia |
|---|---|---|
| V1 | Polare, raffiche, impronta col riferimento **nuovo**: il cambio si limita a queste tre costanti | `git diff` di `js/motore.js` su 3 righe di costanti (e commenti); i riferimenti nuovi dichiarati nel `CHANGELOG.md` |
| V2 | Angolo morto: con vento 6, 10 e 14 nodi, barca ferma con prua a 0-20° per lato e vela cazzata | dopo 30 s di vela ferma, velocità sotto 0,3 nodi a 0-15°, 20 partenze su 20 per vento |
| V3 | Lezioni 1-25, pilota, semi 1-100 | nessun fallimento nuovo oltre ai casi noti, e nessuno in più di 2 su 100 per passo |
| V4 | Torneo: 40 tornei corti col pilota prima e dopo | contatti per regata non oltre +10%, non arrivati non oltre +2 punti, scuffie di rivali e pilota riportate |
| V5 | Guardiano degli avversari e rivali in bolina | rivali e pilota cambiano insieme: distacco medio dal primo entro ±15% |
| V6 | Raffiche in gara: 20 regate lunghe a 12-16 nodi | scuffie del pilota non oltre +50% sulla barca di oggi; **se oltre, si rivede `zCE` a 2,2 con un solo nuovo giro** |
| V7 | Prove a tempo, medaglie | fasce rifatte (già previsto dalle decisioni di Ale: record e medaglie azzerabili) |
| V8 | Pannello 0 px, 0 errori, Chromium e Firefox | come sempre |
| V9 | Ale e Lucio giocano: vento leggero e 14-16 nodi | giudizio «meglio / uguale / peggio»; peggio = si torna indietro |

## Costo e rischi

- Lavoro da Opus in più sessioni: motore (poco), fasce, lezioni, rivali, collaudi coi tempi; giro completo su GitHub.
- **La correzione non passa la maggioranza dei criteri scritti prima:** metà dello scarto a 6 nodi resta, e a 9 nodi oltre 46° non so perché.
- Il braccio 2,4 non ha fonte: è il valore che tiene giusti 12 e 15 nodi. La fonte dice 3,0; lo si può usare solo con lo svergolamento della vela, che è un'altra proposta, più grossa.
- Due fonti sulla resistenza della vela non concordano (0,27 e 0,34 col timoniere): se fosse giusta Flay, metà della correzione sparirebbe.
- Il gioco diventa più difficile con le raffiche.

## Alternative per Ale

1. **Fare questa** (consiglio se vuoi la barca più vera col poco vento, sapendo che non passa i criteri vecchi e che le raffiche si fanno più dure).
2. **Solo la rampa a 15°** (una costante): col poco vento −9 −11 −12 −5% sulla tesi (oggi −11 −12 −12 −5%), Day 6 nodi −15%: quasi niente da sola.
3. **Rampa e resistenza, braccio 2,0:** raffiche e virata più facili, ma 12 e 15 nodi troppo veloci (+4/+5%, +11%): sconsigliata.
4. **Non fare niente**, limite noto come a ottobre, ma con la causa trovata e scritta.
5. **Svergolamento della vela e braccio 3,0** (più grossa): l'unica strada per avere tutto giusto. Da studiare solo se si riprende la fisica a vento forte.
