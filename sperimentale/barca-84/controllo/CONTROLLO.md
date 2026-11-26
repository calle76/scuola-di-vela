# Controllo completo della barca M (26 novembre 2026, notte; richiesta di Ale: «che non ti sia sfuggito altro»)

Tre motori: 1.3.58 (barca vecchia), 1.3.60 (M di oggi), 1.3.61 in prova (M + angolo morto `a1` 19°). Tutti i banchi di `tests/fisica/` (17, `gira.sh`, copie con caricatore sul motore) e controlli nuovi (`extra.js`: partenza da ferma a ogni angolo 4-20 nodi, accelerazione e frenata, bolina 4-22 nodi, scotta, vento 0 e 30 nodi, passo di tempo). Uscite in `extra_*.txt`.

## Problemi trovati
0. **Grave. La tabella delle velocità del gioco (`js/rotta-dati.js`, `ROT_POL`) è ancora quella della barca vecchia** (non rigenerata nella 1.3.59 con `tests/fisica/polare_tabella.js --scrivi`). Con 10 nodi dice 4,6 / 6,0 / 4,1 nodi a 45 / 90 / 180°, la barca M fa 5,2 / 6,3 / 4,5. La usano: la rotta ottimale dopo la regata e il Coach (`js/rotta.js`), le layline disegnate, lo scarroccio delle layline e la VMG di poppa dei rivali (`layLee`, `vmgPoppa`, `js/regate.js`), il cono d'ombra (secondi persi), `collaudo_coach.py`, `collaudo_layline.py`. **La misura dei rivali della voce 2 sulla 1.3.60 (`sperimentale/rivali_lunghe_M_4501-4520.*`) usa questa tabella per la rotta ottimale: non vale** (rivali «più vicini all'ottimo» perché l'ottimo è quello di una barca più lenta). Picco di temperatura in quella misura: 72 °C (361 pause del freno).
1. **Medio. Da ferma con la vela tutta cazzata e vento forte la barca resta bloccata** (`ferma16.js`): 16 nodi 60° 0,8 nodi, 90° 1,1 nodi, 20 nodi 50° 0,5 nodi, per sempre (1.3.58: 2 nodi in 2-7 s). La correzione della 1.3.60 basta fino a circa 12 nodi; R1 provava 12 nodi cazzata e 20 nodi con la scotta migliore. Stesso meccanismo (resistenza indotta che pareggia la spinta), che cresce col vento come la spinta.
2. **Medio-basso. In raffica con la scotta ferma serve poco timone** (`orziera1b.js` criterio 4 FUORI): raffica 14 → 22 nodi, barra massima 6,9° (1.3.58: 35°; soglia oltre 20°). La vela che si appiattisce da sola toglie gran parte dell'orziera; nella realtà una raffica a scotta ferma chiede molto timone.
3. Già noti: angolo morto (voce 90, `a1` 19 deciso), «Stare fermi» (voce 89), strambate senza costo (85), poppa lenta (86-88).

## Diversi dalla barca vecchia ma non difetti (con fonte o plausibili)
- Virata 2,3-2,4 s, velocità minima 58-71% (`virata1b.js` criterio 1 FUORI: era scritto sul 470 di F4); sull'ILCA misurato (F137, F109) M torna.
- Frenata lascando tutto 2 volte più lunga (`boma2.js` B4: 18-20 s contro 9-10, criteri nelle soglie): barca più pesante e vela che sbatte frena meno (F109). Controllato a parte (`frena2.js`): la barca si ferma e poi va indietro come prima (la riga «ferma —» di `extra.js` a 18 nodi era un difetto del controllo).
- Accelerazione più lenta con poco vento al traverso (6 nodi: 90% in 18,8 s contro 12,3): barca più pesante.
- Domanda d'esame 22 (barra mossa di continuo nell'angolo morto): esce 172 volte su 4860 (1.3.58: 41): la risposta resta sbagliata.
- Bolina: sbandamento 1-4° (velista fuori e vela piatta), scarroccio 2-3°; VMG con 22 nodi 3,63 (con 18 nodi 3,77): nessuna misura per dirlo.

## In ordine
Numeri sempre finiti (vento 0 e 30 nodi); velocità identiche con passo 1/30, 1/60, 1/240; retromarcia e boma spinto nelle soglie; `timone2.js` C1 fuori anche nella 1.3.58 (già noto).
