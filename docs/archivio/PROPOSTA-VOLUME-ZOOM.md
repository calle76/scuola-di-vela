# Proposta: il volume dei suoni segue lo zoom, via il tasto del volume (voce 70)

*Fermata 1, 21 novembre 2026 (scritta nella notte, Ale assente: le scelte aperte hanno una mia raccomandazione, da confermare). Richiesta di Ale, 20 novembre: «togliere il tasto del volume dei suoni; si usa il volume del PC; coi tasti dello zoom si alza e abbassa il volume: zoom 100% volume 100%, e più ci si allontana più il volume si abbassa». Nessun codice finché non arriva il via.*

## Cosa c'è oggi (letto nel codice)

- **Volume generale** in `js/suoni.js`: impostazione «Suoni» con quattro livelli, `SUONI_LIV = { spento: 0, basso: 0.22, medio: 0.45, alto: 0.6 }` (di partenza «basso», salvato in `localStorage`, chiave `scuolaVelaSuoni`). Tutti i suoni passano da un solo nodo, `sMaster`.
- **Zoom** in `js/gioco.js` e `js/disegno.js`: `userZoom` va da `ZMIN = 0,1` a 3, si cambia con i tasti **1** (avvicina, ×1,25) e **2** (allontana, ÷1,25) e con la rotella. `zoomQ` è un altro zoom, automatico (il tasto vista): **non** c'entra con questa proposta.
- Misura del volume: `collaudo_suoni_si_sentono.py` (H4: ogni evento alza la banda 200-5.000 Hz di almeno 6 dB; H5: a «alto» strambata, contatto e gabbiano insieme hanno il picco al più −0,5 dB). Gira solo in Chromium, con `ffmpeg`.

## Il modello più semplice

1. **Un solo guadagno nuovo**, `zoomVol(userZoom)`, applicato a un nodo intermedio fra i suoni «del mondo» e `sMaster`: `1` a zoom 1 (e oltre), scende in modo **logaritmico** fino a `SUONI_MIN` a `ZMIN`: `v = SUONI_MIN + (1 − SUONI_MIN) · clamp(ln(z / ZMIN) / ln(1 / ZMIN), 0, 1)` per `z < 1`, `v = 1` per `z ≥ 1`. La scala logaritmica perché ogni pressione del tasto cambia lo zoom dello stesso fattore (×1,25): così ogni pressione cambia il volume dello stesso tanto.
2. **Chi dipende dallo zoom**: i suoni delle altre barche e dell'ambiente (onde, gabbiani, vento lontano). **Chi no**: i suoni della propria barca (sartiame, scafo, vento sulla barca, gorgoglio) e i segnali (tromba, avviso, contatto, boa), sempre pieni. Da leggere nel codice alla fermata 2 quali dei nodi esistenti vanno in quale gruppo; non si inventano suoni nuovi.
3. **Variazione dolce**: `setTargetAtTime` con costante 0,15 s, come già per `sMaster`; nessuno scalino quando si preme un tasto o si gira la rotella.
4. **Il tasto del volume sparisce** dalle impostazioni. Resta **un solo interruttore «Suoni: sì / no»** (chi vuole il silenzio non deve abbassare il PC), che oggi è il livello «spento». Raccomandazione mia; Ale può toglierlo anche lui.
5. **Livello fisso**: a zoom 1 il volume è `0,6` (l'attuale «alto»), perché è il livello su cui è già misurato H5. Attenzione: oggi la partenza è «basso» (0,22): **a zoom 100% i suoni saranno circa 8,7 dB più forti** di quanto sente oggi chi non ha mai toccato l'impostazione. È la conseguenza voluta di «zoom 100% = volume 100%»: se Ale lo trova troppo, si abbassa il fisso (per esempio a 0,45, «medio»), non si rimette la scelta all'utente. Il valore dell'impostazione vecchia salvata nel browser si ignora.

## Scelte aperte (raccomandazione in grassetto, ipotesi nostre)

| Scelta | Raccomandazione |
| --- | --- |
| Livello a zoom 1 | **0,6** (misurato in H5); si cambia a orecchio dopo una prova di Ale |
| Minimo a `ZMIN` (`SUONI_MIN`) | **0,35** (−9 dB); condizione di Ale: tromba, contatto e boa si sentono anche lontano. I segnali non lo usano |
| Zoom oltre 1 (fino a 3) | **volume fisso a 1** (nessun aumento: il picco di H5 non deve salire) |
| Interruttore sì/no | **sì, tenerlo** |

## Criteri (soglie nostre, dichiarate prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| V1 | La curva | `zoomVol` letto dal gioco in 25 valori di `userZoom` fra 0,1 e 3 coincide con la formula ricalcolata nel collaudo (non letta dal gioco) a ±1%; vale 1 per z ≥ 1 e `SUONI_MIN` a `ZMIN`; non cresce mai quando z scende |
| V2 | I segnali non scendono | tromba, avviso, contatto e boa a zoom 0,1: stessa energia di quelli a zoom 1 (±0,5 dB), con il metodo di `collaudo_suoni_si_sentono.py` |
| V3 | La propria barca | sartiame, scafo, vento sulla barca a zoom 0,1 e a zoom 1: stessa energia (±0,5 dB) |
| V4 | Gli altri calano | onde e gabbiani a zoom 0,1 sono più bassi di quelli a zoom 1 di almeno 6 dB e di non più di 10 dB (il minimo dichiarato è −9 dB) |
| V5 | Il picco | H5 invariato: a zoom 1 e a zoom 3 picco al più −0,5 dB |
| V6 | Dolcezza | con 20 pressioni di **2** di fila e poi di **1**, nessun salto di guadagno superiore a 1 dB in 50 ms |
| V7 | Il menu | nessun elenco di livelli, interruttore sì/no che mette a 0 e riporta; pannello a 1360x650 con 0 px di eccesso; il vecchio valore salvato non fa niente |
| V8 | La regata non cambia | posizioni e tempi identici al bit con i suoni accesi o spenti, a ogni zoom (come P4 della 1.3.28) |
| V9 | Come un giocatore | pagina senza `#collaudo`, una regata giocata con i tasti 1 e 2, 0 errori |

Il metro non deve dipendere da ciò che misura: V1 e V8 si calcolano nel collaudo, non leggendo il valore dal gioco; il collaudo stampa il numero dei casi (V1 25, V6 40 pressioni, V2-V4 almeno 3 prove per evento) e non passa con zero casi. V2-V6 si misurano solo in Chromium (ffmpeg), come H4; in Firefox si controllano V1, V7, V8, V9.

## Rischi

- **Troppo forte alla prima prova** (vedi punto 5): è la scelta più probabile da ritoccare. Lo giudica Ale a orecchio: io non posso sentire.
- **Chi gioca con lo zoom a 100% e il PC già alto** si trova suoni più forti di prima. Si risolve con il livello fisso.
- **Suoni misti nello stesso nodo**: se qualcuno dei suoni «del mondo» e «della barca» oggi passa dallo stesso nodo, va diviso (più lavoro del previsto): si vede alla fermata 2.
- **I collaudi esistenti** misurano a un solo livello («alto»): restano validi a zoom 1; da rimisurare H4 e H5 col livello fisso.

## Passi, dopo il via

1. Leggere i nodi in `js/suoni.js`, dividere «mondo» e «barca/segnali», aggiungere `zoomVol` (un solo punto in `suoniAgg`, che già legge lo stato) e l'interruttore; togliere `SUONI_LIV` a più livelli.
2. `collaudo_suoni_zoom.py` (V1-V9, Chromium e Firefox dove si può); rimisurare `collaudo_suoni_si_sentono.py` (H4, H5).
3. Documenti, versione, `CHANGELOG.md`. Opus per la lettura dei nodi audio.

## Cambio del 21 novembre 2026 (1.3.34, Ale: «sì, tutto cala»)

La condizione (2) di sopra (i suoni della propria barca non dipendono dallo zoom) è **superata**: allontanando lo zoom cala tutto, tranne i segnali (tromba, contatto, boa, arrivo) che restano pieni. Stessa curva e stesso minimo (0,35). Il collaudo `collaudo_suoni_zoom.py` ha il grafo audio aggiornato; V3 diventa «la barca cala come l'ambiente». Aggiunto il campanello del Coach (voce 68, `PROPOSTA-COACH-DURATA.md`): non segue lo zoom.
