# Proposta: saturazione del timone (Scuola di vela, dalla 0.21.2)

> **Archiviato il 13 ottobre 2026.** Prova non adottata: il gioco resta con il timone della 0.21.2. Il codice della prova è sul ramo `prova-saturazione`. Seguito in `../PROPOSTA-RESISTENZA-SCAFO.md`.

Stato: **proposta, non implementata.** Scritta il 13 ottobre 2026 in una sessione di sola lettura: nessun file del repository è stato modificato. Le misure sono state fatte su una copia in memoria del motore (`step()` letto da `index.html`, riga 441 sostituita in memoria).

Tipi delle affermazioni:
- **[codice]** = letto nel codice;
- **[misura]** = calcolato sul motore in memoria;
- **[stima]** = ragionamento senza misura.

Le misure sono deterministiche (nessun numero casuale), salvo l'emulazione di `collaudo_rotta.py`, che usa semi fissi. «Molti tentativi» vuol dire griglie di condizioni, con il numero dei casi scritto accanto.

---

## 0. In breve

- **Decisione di Ale:** tetto a 15° di angolo della pala, con la rotazione compensata, escluso all'indietro. Si dichiara come **saturazione (scelta di bilanciamento)**, non come stallo fisico.
- **Effetto principale:** sopra 15° la rotazione non cresce più. A 15° si gira come oggi a 30°, quindi **sotto 15° ogni angolo gira 1,93 volte di più.** La barca **non diventa più lenta: diventa più svelta e più sensibile.**
- **Cosa non cambia** [misura]:
  - polare, raffiche, uscita dall'angolo morto (parti 1 e 2), identiche carattere per carattere;
  - fasce oro delle prove 1-4.
- **Cosa cambia** [misura]:
  - virate più rapide e più facili;
  - la virata a 1,9 nodi, che oggi fallisce, riesce;
  - la barra a fondo non è più la scelta migliore;
  - il pilota del collaudo «Tenere la rotta» va a zig-zag (13 cambi di barra contro 3), ma completa lo stesso.
- **Da misurare nel browser:** prova 5 (raffiche), regate, lezioni, e la sensazione di guida di una persona.

---

## 1. Il codice di oggi [codice]

`index.html`:

- riga 372: `rudderDragK: 45`
- riga 378: `turnLen: 1.05,       // m, lunghezza efficace per la virata`
- riga 379: `maxRudder: 30,`
- riga 419: `const rud = C.tiller * BOAT.maxRudder;` (barra da −1 a 1, quindi pala da −30° a +30°)
- righe 420-421, resistenza della barra angolata:
  `BOAT.rudderDragK * S.u * Math.abs(S.u) * Math.sin(Math.abs(rud) * D2R) ** 2`
- riga 441:
  `let rTarget = -(S.u / BOAT.turnLen) * Math.sin(rud * D2R) / D2R; // gradi/s`
- riga 443 (la prua poggia da sola, barca lenta nel vento; **non si tocca**, decisione separata):
  `if (A < 36 && Math.abs(S.u) < 0.5) rTarget += (awa >= 0 ? -1 : 1) * 6 * (1 - Math.abs(S.u) / 0.5);`
- riga 444: `S.r += (rTarget - S.r) * Math.min(1, dt * 4);` (la rotazione insegue il valore voluto in circa 0,25 s)

`turnLen` è una costante unica, usata solo alla riga 441. All'indietro (`S.u < 0`) il segno della rotazione si inverte da solo: la barra funziona al contrario.

Raggio di virata a regime = `turnLen / sin(angolo pala)`: 2,1 m a 30°, 4,1 m a 15°. Non dipende dalla velocità; lo scarroccio è escluso dal conto.

---

## 2. La modifica proposta (codice esatto)

In `BOAT`, dopo la riga 379:

```js
  rudderSat: 15,      // gradi: oltre, in avanti la rotazione non cresce più (saturazione, scelta di bilanciamento)
```

La riga 441 diventa:

```js
  // saturazione (scelta di bilanciamento, non stallo misurato): in avanti la rotazione smette di crescere oltre rudderSat,
  // dove vale quanto valeva prima a maxRudder; all'indietro la formula di prima
  const rudF = S.u >= 0 ? Math.sign(rud) * Math.sin(Math.min(Math.abs(rud), BOAT.rudderSat) * D2R) * Math.sin(BOAT.maxRudder * D2R) / Math.sin(BOAT.rudderSat * D2R)
                        : Math.sin(rud * D2R);
  let rTarget = -(S.u / BOAT.turnLen) * rudF / D2R; // gradi/s
```

Note:
- **Non cambiano:** `turnLen`, `maxRudder`, la resistenza della barra (riga 421) e la riga 443, che però si sposta alla **448**.
- **Una sola costante nuova** (15°). La compensazione non è un numero scelto: deriva da «a 15° si gira come oggi a 30°» (fattore sin 30° / sin 15° = 1,932).
- In pratica sono due lunghezze efficaci: 0,5435 m in avanti e 1,05 m all'indietro.
- Verificato [misura] che questo codice esatto dia gli stessi risultati della variante misurata: uscita di `raffiche_e_virate.js` identica carattere per carattere.
- `VERSIONE` e `CHANGELOG.md` vanno aggiornati come per ogni versione.

---

## 3. La fonte: una sola (F4)

*Riscritto il 13 ottobre 2026, dopo la verifica sull'origine della frase «stallo a 30-35°».*

**F4** (`docs/FONTI-PUBBLICHE.md`, riga 20): Masuyama e Ogihara, «Science of the 470 Sailing Performance», *Journal of Sailing Technology* 5(1), 2020, pp. 20-46.
- Il timone lavora bene fino a circa ±15°; oltre, la forza laterale smette di crescere e la resistenza continua a salire.
- A 6 nodi: circa 5 kgf a 10° e 12 kgf a 15°, contro circa 19 kgf di resistenza totale.
- Una sola barca, una deriva olimpica a due: non la barca del gioco (deriva singola, una vela).

**La frase «un lavoro CFD: stallo a 30-35°» non è una fonte.**
- È entrata nel commit `2b7ea3c` (9 ottobre 2026), insieme a tutto `RICERCA-DATI-IMBARDATA.md`, e da lì in `PIANO-GENERALE.md`.
- Non ha autore, titolo né collegamento in nessun documento. Nessun PDF di `fonti-pdf/` parla di stallo del timone a 30-35° (ricerca con `pdftotext`).
- Il documento era stato scritto da un assistente in una sandbox (sua riga 72): l'origine IA è **probabile ma non provabile**, perché la sessione del 9 ottobre non è salvata.
- Per la regola del progetto («le risposte di un'IA non sono fonti») la frase è stata tolta dai documenti il 13 ottobre 2026, insieme a «timonata normale 2-5°, oltre 8° è troppa», anch'essa senza fonte.

**Conseguenza:** 15° è una **scelta di bilanciamento su una fonte sola** (F4, un 470). Non è un dato misurato sulla barca del gioco, e non c'è una seconda fonte che lo confermi o lo smentisca.

### Dubbio aperto, separato da questa versione: la barca frena troppo in fretta?

Non riguarda il timone e la saturazione non lo cambia. Si annota qui perché è emerso misurando le virate.

- **[misura]** A 10 nodi, la barca lanciata al massimo con la prua messa nel vento si ferma dopo **1-1,6 lunghezze di scafo** (4,2 m: commento alla riga 361 e disegno dello scafo `hullPath`). Partendo di bolina sono circa 1,0; partendo dal traverso 1,3 con la scotta tutta lasca e 1,6 con la scotta regolata. Oggi e con la variante cambia al massimo di 0,1.
- **Riferimento esterno**, solo per l'ordine di grandezza: Cockerill parla di circa **3-4 lunghezze** di scivolamento partendo dalla massima velocità.
- **[stima]** Se le due misure sono confrontabili, la barca del gioco rallenta circa 2-3 volte più in fretta. Il motivo starebbe nella frenata (resistenza dello scafo, vela che sbatte, massa), non nel timone.
- **Incertezze:** non sappiamo cosa misuri esattamente Cockerill (da dove a dove, quale barca, scotta lasca o no), quindi l'accostamento è nostro. Il numero **non va usato per tarare niente**: è una domanda per il velista e per una ricerca futura.

---

## 4. Misure sulla variante proposta

### 4.1 Il guadagno a barra piccola: 1,93×, non «circa 1,7×»

- **[codice]** A parità di velocità il rapporto è esatto: 1,932.
- **[misura]** Bolina a 10 nodi a regime, barra 0,1 (3°). Rapporto tra rotazione (°/s) e velocità (m/s):

  | Dopo | Oggi | Variante | Rapporto |
  |---|---|---|---|
  | 0,25 s | 1,82 | 3,52 | 1,93 |
  | 2 s | 3,02 | 5,97 | 1,98 |

  Lo scarto da 1,93 viene dal ritardo di circa 0,25 s della riga 444.
- **Perché una prima misura diceva 1,7×** (4,1 → 7,1 °/s): confrontava la rotazione assoluta dopo 2 s. La barca della variante, girando di più, era già orzata a 30° (contro 37°) e aveva rallentato a 2,34 nodi (contro 2,68). La rotazione è proporzionale alla velocità.

### 4.2 All'indietro: perché due lunghezze e non una [misura]

Griglia della parte 1 di `tests/fisica/angolo_morto.js`: 2.196 partenze, barra verso il boma finché la barca arretra. Parte 2: 4.860 partenze, barra mossa di continuo, cioè la risposta sbagliata della domanda d'esame 22.

| Variante | Parte 1 | Parte 2 |
|---|---|---|
| Oggi | 2.180 su 2.196; mediane per vento e scotta 9,3 / 4,4 / 6,7 / 3,3 / 5,5 / 2,8 s | 26 su 4.860 |
| **Proposta (indietro escluso)** | **identica carattere per carattere** | **identica** |
| `turnLen` unico 0,5435 m anche all'indietro | 2.182; mediane circa dimezzate (6 nodi, scotta 100: da 9,3 a 4,6 s) | **337 su 4.860** |
| Saturazione e guadagno anche all'indietro | identica | identica |

- Con `turnLen` unico la risposta sbagliata della domanda 22 funzionerebbe 13 volte più spesso. Per questo servono le due lunghezze.
- L'ultima riga è identica solo perché il collaudo usa la barra a ±1, e a 30° il fattore torna 0,5. Con barra parziale all'indietro cambierebbe, ma nessun collaudo la misura.

### 4.3 Virate, strambate, raggio [misura]

Pilota dei collaudi: barra = errore/20 + r·0,02, limitata a ±1.

| Manovra | Oggi | Variante |
|---|---|---|
| Virata 45° → −45°, 6 nodi | 6,18 s | 5,55 s |
| Virata, 10 nodi | 4,41 s | 3,60 s |
| Virata, 14 nodi | 3,47 s | 2,81 s |
| Strambata 150° → 210°, 6 / 10 / 14 nodi | 2,89 / 2,05 / 1,73 s | 2,48 / 1,79 / 1,55 s |
| Da bolina a poppa, 10 nodi | 3,54 s | 3,29 s |

Virata a barra fissa, 10 nodi:

| Barra | 0,3 | 0,4 | 0,5 | 0,6 | 0,8 | 1 |
|---|---|---|---|---|---|---|
| Oggi | fallisce | 10,56 s | 8,69 s | 6,91 s | 4,46 s | 3,29 s |
| Variante | 6,65 s | 3,96 s | **2,85 s** | 2,90 s | 3,07 s | 3,29 s |

La barra a fondo non è più la migliore. Costa la resistenza della riga 421, che a 30° vale 3,7 volte quella a 15°.

Griglia di 84 virate: 4 andature × 7 velocità × 3 regolazioni della scotta. Miglior risultato per posizione di barra:

| Vento | Oggi | Variante |
|---|---|---|
| 6 nodi | 66 | 72 |
| 10 nodi | 66 | 71 |
| 15 nodi | 62 | 67 |

Raggio di virata in avanti [conto dal codice]:

| Pala | 3° | 6° | 9° | 12° | 15° e oltre |
|---|---|---|---|---|---|
| Oggi | 20,1 m | 10,0 m | 6,7 m | 5,1 m | 4,1 m a 15°, 2,1 m a 30° |
| Variante | 10,4 m | 5,2 m | 3,5 m | 2,6 m | 2,1 m |

Il raggio minimo non cambia. All'indietro non cambia niente.

### 4.4 Collaudi

**`polare.js`** e parte **raffiche** di `raffiche_e_virate.js`: identici (barra al centro) [misura].

**`raffiche_e_virate.js`, virate con barra 0,8** [misura]:

| Partenza | Oggi | Variante |
|---|---|---|
| 3,9 nodi | riuscita in 4,0 s | riuscita in **2,8 s** |
| 1,9 nodi | fallita (prua a 12°, velocità −1,2 nodi) | **riuscita in 6,4 s** |
| 0,4 nodi | fallita (prua a 31°, velocità 0,1 nodi) | fallita (prua a 34°, velocità 0,1 nodi) |

L'uscita passa da 364 a 339 caratteri. La frase di `FISICA-E-TARATURE.md:51` «a 1,9 nodi fallisce» non vale più.

**`collaudo_rotta.py`**, emulato in Node. Lezione 2 «Tenere la rotta», con onde e orziera di 3 °/s come in `simulate()`, barra che torna al centro, generatore a seme. Semi 1-50 × 6 prue = 300 corse per gruppo [misura]:

| | Oggi | Variante |
|---|---|---|
| A mani ferme, completati | 0 su 300 (massimo 6,6 s di fila) | 0 su 300 (massimo 6,6 s) |
| Con correzioni a colpi di 0,3, completati | 300 su 300, mediana 8,0 s | 300 su 300, mediana 8,0 s |
| Cambi di lato della barra (mediana) | 3 | **13** |
| Scarto massimo dalla rotta, mediana | 2,8° | 4,1° |
| Scarto massimo dalla rotta, massimo | 4,6° | 6,1° |

Il pilota adesso corregge troppo e va a zig-zag.

**`collaudo_fasce.py`, prove 1-5**, emulate in Node con lo stesso pilota. Col motore di oggi l'emulazione ridà i tempi del browser [misura]:

| Prova | Browser oggi | Emulata oggi | Emulata variante |
|---|---|---|---|
| 1 | 92,1 s | 92,1 s | 92,1 s |
| 2 | 142,6 s | 142,6 s | 142,6 s |
| 3 | 196,4 s | 196,4 s | 195,9 s |
| 4 | 333,3 s | 333,4 s | 332,8 s |
| 5 | mediana 353,6 s | 365,5 s | 361,7 s |

La prova 5 **non è riprodotta**: l'emulazione non ha le raffiche. Il −3,8 s è solo un indizio [stima].

**Avversari**, imitazione semplificata di `aiControl`, virata [misura]:

| Vento | Oggi (principianti / esperti) | Variante |
|---|---|---|
| 6 nodi | 5,3 / 5,8 s | 4,8 / 5,1 s |
| 10 nodi | 4,5 / 3,6 s | 3,3 / 3,2 s |
| 12 nodi | 4,0 / 3,4 s | 2,9 / 2,7 s |
| 14 nodi | 3,8 / 3,1 s | 2,7 / 2,4 s |

**Oscillazione dei piloti** [misura]. Cambio di rotta a gradino di 20° e di 60° al traverso, 10 nodi:
- nessun sorpasso e nessuna oscillazione, né col pilota errore/20 né con gli avversari (guadagno 26 o 18, barra con ritardo);
- il guadagno quasi doppio solo accorcia l'assestamento (pilota, salto di 20°: da 1,4 a 1,1 s);
- l'unico zig-zag trovato è quello del collaudo della rotta, sopra.

**Passo 5.4 «Una virata che non riesce»** [misura]:
- 360 tentativi sotto 1 nodo (3 venti × 4 prue × 5 velocità × 2 barre × 3 scotte): riescono 88 oggi, 99 con la variante;
- l'uscita all'indietro con la barra verso il boma è identica (§4.2).

### 4.5 Fasce e record

- **[misura, prove 1-4]** La regola delle fasce (riga 705: oro = tempo del pilota arrotondato ai 5 s superiori) dà ancora **95, 145, 200, 335**. Nessuna fascia cambia.
- **Prova 5:** fascia oro 355 s contro 353,6 s, margine 1,4 s. Da misurare nel browser.
- **[codice]** La medaglia si calcola sul momento dal record salvato (`medalOf`, riga 949). Con le fasce uguali, nessun record già salvato cambia medaglia.
- **[stima]** I record nuovi saranno un po' più facili:
  - il pilota guadagna 0,5-0,6 s;
  - un giocatore che tiene la freccia arriva alla saturazione in 0,31 s invece di 0,63 (la barra cresce di 1,6 al secondo), e guadagna qualche decimo per virata.
- **Cambiare `KEYV`** cancellerebbe record, stelle e fantasmi, come nella 0.19. Non sembra necessario: decide Ale.

---

## 5. Tabella prima e dopo

| Misura | Oggi | Proposta | Tipo |
|---|---|---|---|
| Rotazione a parità di velocità, sotto 15° | 1× | 1,93× | codice |
| Raggio a 9° / 15° / 30° | 6,7 / 4,1 / 2,1 m | 3,5 / 2,1 / 2,1 m | conto |
| Virata col pilota, 6 / 10 / 14 nodi | 6,18 / 4,41 / 3,47 s | 5,55 / 3,60 / 2,81 s | misura |
| Virata, barra 0,5 / 1, 10 nodi | 8,69 / 3,29 s | 2,85 / 3,29 s | misura |
| Strambata, 10 nodi | 2,05 s | 1,79 s | misura |
| Virate riuscite su 84 (miglior barra), 6 / 10 / 15 nodi | 66 / 66 / 62 | 72 / 71 / 67 | misura |
| `raffiche_e_virate`, 3,9 / 1,9 / 0,4 nodi | 4,0 s / fallita / fallita | 2,8 s / 6,4 s / fallita | misura |
| `polare.js`, raffiche | — | identici | misura |
| `angolo_morto.js`, parti 1 e 2 | — | identici | misura |
| Virate sotto 1 nodo, su 360 | 88 | 99 | misura |
| Rotta: cambi di barra / scarto massimo | 3 / 4,6° | 13 / 6,1° | misura, emulazione |
| Prove 1-4 | 92,1 / 142,6 / 196,4 / 333,4 s | 92,1 / 142,6 / 195,9 / 332,8 s | misura, emulazione |
| Fasce oro 1-4 | 95 / 145 / 200 / 335 | uguali | misura |
| Prova 5 | 353,6 s (browser) | non misurata nel browser | — |
| Avversari, virata a 10 / 12 nodi (principianti) | 4,5 / 4,0 s | 3,3 / 2,9 s | misura, imitazione |

---

## 6. Cosa va dichiarato e dove

**`CHANGELOG.md`**, voce di versione:
- «Saturazione del timone: scelta di bilanciamento, non stallo fisico misurato.»
- Formula, costante `rudderSat` = 15° come ipotesi nostra, compensazione, indietro escluso.
- La fonte unica (F4, un 470: §3) e la tabella del §5, compresi i numeri sgraditi:
  - barca più sensibile sotto 15°;
  - virata a 1,9 nodi che ora riesce;
  - zig-zag nel collaudo della rotta;
  - prova 5 e regate non misurate.

**`docs/FISICA-E-TARATURE.md`**:
- punto 7 «Timone»: nuova formula, «riga 443» diventa «riga 448»;
- tabella `BOAT`: aggiungere `rudderSat` 15° con «ipotesi di progetto»;
- riga 51: la virata a 1,9 nodi ora riesce in 6,4 s;
- riga 90 e riga 153 (tabella «Cosa non fa»): da «la pala non stalla mai» a «la rotazione satura oltre 15°, per scelta».

**`docs/CONTENUTI-DA-VERIFICARE.md`, riga 243:**
- stato: «modellato come saturazione, scelta di progetto (versione X), non verificato»;
- restano le domande al velista: da che angolo la barra smette di far girare, e se oltre frena soltanto.

**Da allineare** (oggi dicono «non modellata»):
- `docs/FONTI-PUBBLICHE.md`, righe 54 e 108;
- `docs/DUBBI-E-RICERCHE.md`, riga 67;
- `docs/MANUALE-bozza.md`, righe 104 e 120;
- `docs/RICERCA-DATI-IMBARDATA.md`, riga 39;
- `docs/PIANO-GENERALE.md`, righe 45, 211 e 265;
- `docs/COLLAUDI.md`: risultati attesi di `raffiche_e_virate.js` («virata riuscita in circa 4 s» diventa «circa 2,8 s»; a 1,9 nodi riesce).

---

## 7. Piano di collaudo nel browser, guidando davvero la barca

Ogni corsa in una pagina nuova, con seme fisso e passi di 1/60 s (`__sv.run`). Regola dei semi: soglia scelta su un gruppo, confermata su un altro mai guardato, ed entrambi dichiarati.

1. **`collaudo_fasce.py`**:
   - prove 1-4: tempi attesi entro 0,1 s da quelli emulati;
   - prova 5 con le raffiche: 24 corse, poi conferma su semi nuovi;
   - se la mediana scende, decidere la fascia oro.
2. **Lezioni e suggerimenti:** `collaudo_lezioni.py`, `collaudo_rotta.py`, `collaudo_suggerimento.py` (parti 3c-3i, perché l'uscita in avanti dopo l'arretramento usa la barra), `collaudo_registro.py`, `collaudo_giro_boa.py`, `collaudo_linea.py` (parte 3, «Risalire il vento»).
3. **Avversari:** `collaudo_regate.py` (tipi 0 e 1), `collaudo_partenze.py`, `collaudo_competizione.py` (C0-C5, semi 1-40 e 41-80), `collaudo_aggressiva.py`.
4. **Pagina senza `#collaudo`, a mano (Ale):** lezione 1, lezione 2 «Tenere la rotta» e una virata della lezione 5. Ale dice se la barca è diventata troppo nervosa: il collaudo automatico non lo può misurare.
5. **Sempre:**
   - `polare.js`: deve restare identico;
   - `raffiche_e_virate.js`: uscita nuova attesa, carattere per carattere, quella del §4.4;
   - `angolo_morto.js`: deve restare identico;
   - `collaudo_versione.py`.

---

## 8. Rischi aperti

- **Barca più nervosa a barra piccola** [misura su un pilota, stima per una persona]. La lezione 2 insegna i «piccoli colpi»: ora bastano colpi più piccoli. In lezione 1, con la barra che torna al centro, la prua risponde il doppio a ogni pressione [stima].
- **Il gioco diventa più facile, non più realistico nel tempo di virata:** virate più rapide, più virate riuscite, a 1,9 nodi si vira.
- **«Barra a fondo è un errore» si sente poco:** costa 0,44 s su una virata di circa 3 s, ed è la resistenza che c'era già.
- **Prova 5 e regate non misurate nel browser.**
- **`sperimentale/fiocco.html`** ha una sua copia di `step()` (riga 493): la non-regressione «senza fiocco identico al gioco» si rompe se non la si allinea.
- **Una fonte sola** (F4, un 470), non sulla barca del gioco (§3).
- **La barra parziale all'indietro** non è coperta da collaudi. Qui non è un rischio, perché all'indietro la formula resta quella di oggi.

---

## 9. Decisioni che spettano ad Ale

1. Se accettare una barca **più sensibile** sotto 15° (1,93×). Altrimenti: compensare meno, che allunga di nuovo le virate, oppure non fare la modifica.
2. Se la virata a 1,9 nodi che ora riesce va bene per la lezione 5 e i suoi testi.
3. Numero di versione (0.22?) e se cambiare `KEYV`. Consiglio di no, perché fasce e medaglie non cambiano.
4. Se allineare `sperimentale/fiocco.html`.
5. 15° = scelta di bilanciamento su una fonte sola (F4, un 470): da confermare o correggere con la prova a mano e il parere del velista.
6. A parte, e non in questa proposta: la riga 443.

---

## Appendice: varianti scartate (prima analisi, stesso giorno)

Senza compensazione (tetto, calo lineare o calo graduale oltre 15°) la rotazione massima scende a 0,52 volte quella di oggi [misura]:

| Misura | Oggi | Tetto senza compensazione |
|---|---|---|
| Virata col pilota, 10 nodi | 4,4 s | 9,5 s |
| Virata col pilota, 6 nodi | 6,2 s | fallisce |
| Avversari, virata a 10 nodi | 4,5 s | 11,7 s |
| Avversari, 6 nodi | virano | non virano |
| Prova 3 col pilota delle fasce | arriva | non arriva (gira in tondo tentando di virare) |
| Griglia di 84 virate, 6 nodi (miglior barra) | 66 | 34 |

Calo lineare e calo graduale facevano peggio. Per questo si è scelta la variante compensata.

## Appendice: come rifare le misure

Gli script stavano nella cartella temporanea della sessione (non nel repository) e caricavano il motore da `index.html` come fa `tests/fisica/motore.js`, sostituendo la riga 441 in memoria:

- `motori3.js`: codice esatto della proposta;
- `m1.js`: guadagno a barra piccola;
- `am.js`: `angolo_morto.js` sulle varianti;
- `m3.js`: virate e strambate;
- `m3b.js`: griglia di 84 virate;
- `m4_lenta.js`: virate sotto 1 nodo;
- `m5_rotta.js`: emulazione di `collaudo_rotta.py`;
- `m6_prove.js`: emulazione delle prove 1-5;
- `m7_ai.js`: virata degli avversari;
- `m8_osc.js`: oscillazione dei piloti.

La cartella temporanea può sparire a fine sessione: se servono, vanno copiati altrove.
