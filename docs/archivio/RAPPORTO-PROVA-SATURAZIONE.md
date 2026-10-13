# Rapporto: prova della saturazione del timone (ramo `prova-saturazione`)

> **Archiviato il 13 ottobre 2026.** Prova non adottata: il gioco resta con il timone della 0.21.2. Il codice della prova è sul ramo `prova-saturazione`. Seguito in `../PROPOSTA-RESISTENZA-SCAFO.md`.

Del 13 ottobre 2026. Segue `docs/PROPOSTA-SATURAZIONE-TIMONE.md` (la proposta, con modello, misure preliminari e decisioni). Qui c'è cosa è stato fatto sul ramo e cosa hanno detto i collaudi.

Tipi delle affermazioni:
- **[codice]** = letto nel codice;
- **[misura]** = collaudo o calcolo eseguito;
- **[stima]** = ragionamento senza misura.

---

## 0. In breve

- **Ramo:** `prova-saturazione`, creato da `main` (commit `9efafc5`, versione 0.21.2).
- **Lo stato non è salvato:** al momento di scrivere niente è committato, perché i commit li fa Ale. Prima di tornare su `main` va fatto il commit sul ramo, altrimenti le modifiche seguono il cambio di ramo.
- **Non cambiati:** `VERSIONE` (0.21.2), `KEYV`, `sperimentale/fiocco.html`, gli altri documenti di `docs/`.
- **La modifica:** in avanti la rotazione dovuta al timone non cresce più oltre 15° di pala, e a 15° vale quanto valeva prima a 30°. Quindi sotto 15° la barra gira **1,93 volte di più**. All'indietro la formula è quella di prima.
- **Esito dei collaudi** [misura]: 14 su 16 con lo stesso esito di main o con i numeri previsti dalla proposta. **Due differenze:**
  1. `collaudo_lezioni.py`: la lezione 5 non si completa, perché lo stesso colpo di freccia porta la barca dentro l'angolo morto (sensibilità doppia);
  2. `collaudo_aggressiva.py`: 193 incontri evitabili su 199 contro 198 su 200 su main. Peggioramento possibile, **non dimostrato**.
- **Prossimo passo:** la prova a mano di Ale (§6), poi la decisione.

---

## 1. Cosa è cambiato nei file (sul ramo, non committato)

### 1.1 `index.html` [codice]

In `BOAT`, dopo `maxRudder: 30,` (nuova riga 380):

```js
  rudderSat: 15,      // gradi: oltre, in avanti la rotazione non cresce più (saturazione, scelta di bilanciamento)
```

La vecchia riga 441, ora righe 442-446:

```js
  // saturazione (scelta di bilanciamento, non stallo misurato): in avanti la rotazione smette di crescere oltre rudderSat,
  // dove vale quanto valeva prima a maxRudder; all'indietro la formula di prima
  const rudF = S.u >= 0 ? Math.sign(rud) * Math.sin(Math.min(Math.abs(rud), BOAT.rudderSat) * D2R) * Math.sin(BOAT.maxRudder * D2R) / Math.sin(BOAT.rudderSat * D2R)
                        : Math.sin(rud * D2R);
  let rTarget = -(S.u / BOAT.turnLen) * rudF / D2R; // gradi/s
```

- La riga «la prua poggia da sola» (`if (A < 36 && Math.abs(S.u) < 0.5) …`) era la 443 e ora è la **448**, invariata.
- Non cambiano: `turnLen` (1,05), `maxRudder` (30) e la resistenza della barra angolata.

### 1.2 `docs/PROPOSTA-SATURAZIONE-TIMONE.md`

- **§3 riscritto: F4 è l'unica fonte.** Masuyama e Ogihara, «Science of the 470 Sailing Performance», *Journal of Sailing Technology* 5(1), 2020, pp. 20-46: il timone lavora bene fino a circa ±15°. È una sola barca, una deriva a due, non quella del gioco.
- La frase «un lavoro CFD: stallo a 30-35°» **non è una fonte**:
  - è entrata con il commit `2b7ea3c` del 9 ottobre 2026;
  - non ha autore, titolo né collegamento;
  - nessun PDF di `fonti-pdf/` ne parla;
  - l'origine IA è probabile ma non provabile, perché la sessione del 9 ottobre non è salvata.
- Decisione 5: «15° = scelta di bilanciamento su una fonte sola».
- **Aggiunto come dubbio aperto, separato da questa versione:** la barca lanciata al massimo, con la prua nel vento, si ferma in 1-1,6 lunghezze (scafo 4,2 m). Cockerill parla di circa 3-4 lunghezze di scivolamento. Non sappiamo cosa misuri esattamente, quindi l'accostamento è nostro e il numero non serve per tarare niente.
- Allineati i rimandi alla «fonte CFD» nei §6, 8 e 9.

### 1.3 Frasi senza fonte tolte

Ciascuna è sostituita da «*(Riga tolta il 13 ottobre 2026: nessuna fonte rintracciabile, probabile origine IA.)*»:
- `docs/RICERCA-DATI-IMBARDATA.md`, riga 22: «Un lavoro CFD contraddice: stallo a 30–35°…»;
- `docs/RICERCA-DATI-IMBARDATA.md`, riga 23: «Timonata normale in bolina: 2–5°; oltre 8° è troppa…»;
- `docs/PIANO-GENERALE.md`, riga 211: «Contraddizione aperta: stallo… a circa 15° (F4) contro 30-35° (CFD)…».

**La stessa idea resta in tre punti, non toccati (da decidere):**
- `docs/RICERCA-DATI-IMBARDATA.md:24`: «plausibile solo se lo stallo vero è 30–35°»;
- `docs/PIANO-GENERALE.md:45`: «Stallo del timone (15° contro 30-35°)»;
- `docs/PIANO-GENERALE.md:265`: «Contraddizione sullo stallo del timone (15° contro 30-35°)».

---

## 2. Come sono stati lanciati i collaudi

- Gli stessi collaudi, in sequenza, sul ramo e su una copia di `main` estratta con `git archive` in una cartella temporanea fuori dal repository. Stessa macchina, stesse condizioni.
- Nella sandbox mancano i caratteri del gioco (Barlow, Source Serif): le misure dell'altezza del pannello non valgono, né sul ramo né su `main`.
- `collaudo_regate.py`, `collaudo_partenze.py` e `collaudo_aggressiva.py` **non hanno un seme fisso**: un giro solo non basta per confrontare. L'aggressiva è stata ripetuta 5 volte per parte; regate e partenze una volta sola.
- I collaudi della fisica si lanciano da `tests/fisica` con Node.

---

## 3. Risultati, collaudo per collaudo [misura]

| Collaudo | Ramo | Main | Previsto dalla proposta | Esito |
|---|---|---|---|---|
| `polare.js` | identico a main, carattere per carattere | — | identico | ✔ |
| `raffiche_e_virate.js` | virata da 3,9 nodi in 2,8 s; da 1,9 nodi riuscita in 6,4 s; da 0,4 nodi fallita (34°); raffiche identiche | 4,0 s / fallita / fallita | uguale carattere per carattere (339 caratteri) | ✔ |
| `angolo_morto.js`, parti 1 e 2 | identico a main (2.180 su 2.196 e 26 su 4.860) | — | identico | ✔ |
| `collaudo_versione.py` | 3 confronti, tutti OK (0.21.2) | — | — | ✔ |
| `collaudo_fasce.py`, prove 1-4 | 92,1 / 142,6 / 195,9 / 332,7 s, 8 su 8 | 92,1 / 142,6 / 196,4 / 333,4 s | 92,1 / 142,6 / 195,9 / 332,8 s | ✔ (scarto di 0,1 s sulla prova 4) |
| `collaudo_fasce.py`, prova 5 | 21 finite su 24, mediana 351,3 s | 19 su 24, 353,8 s | non stimata (emulazione senza raffiche) | ✔, fascia oro 355 s ancora valida |
| `collaudo_lezioni.py` | **lezione 5: «prepararsi», «virata» e «assestamento» NON completati**; il resto OK | tutto completato | non previsto | **✘** (§4.1) |
| `collaudo_rotta.py` | 0 su 25 a mani ferme (massimo 6 s di fila su 8), 6 su 6 con correzioni, mediana 8 s | 0 su 25 (massimo 5 s), 6 su 6, mediana 8 s | uguale (emulato: 0 su 300 e 300 su 300) | ✔ |
| `collaudo_suggerimento.py` | casi sbagliati: nessuno; caso 8: 8 su 8; esce con 1 per i caratteri | uguale, esce con 1 per lo stesso motivo | — | ✔ (limite della sandbox) |
| `collaudo_linea.py` | 234 casi, 0 sbagliati, tutto OK | uguale | — | ✔ |
| `collaudo_giro_boa.py` | stessi esiti in tutti i casi; prova 5 359 s, prova 3 196 s | prova 5 356 s, prova 3 197 s | — | ✔ |
| `collaudo_registro.py` (abcdefghi) | tutti i controlli OK | tutti OK | — | ✔ (nota sul 5.4 al §5) |
| `collaudo_regate.py`, bastone (6 corse) | 0 «BLOCCATA»; arrivo avversari: mediana 258,5 s, media 271,1 | 0; mediana 271,5 s, media 277,2 | avversari più veloci | ✔ |
| `collaudo_regate.py`, raffiche (6 corse) | 0 «BLOCCATA»; mediana 207,5 s, media 215,3 | 0; mediana 218,5 s, media 221,8 | avversari più veloci | ✔ |
| `collaudo_partenze.py` (preparazione 60 s) | ritardo medio 9,7 s, mediana 4,9, massimo 60,5; nessuna ancora anticipata | 15,4, 5,1, 87,4; nessuna | — | ✔ (un giro solo, senza seme) |
| `collaudo_aggressiva.py`, 5 giri | 193 incontri evitabili su 199 | 198 su 200 | — | **⚠** (§4.2) |
| `collaudo_competizione.py` | C0-C5 tutti OK nei quattro gruppi | tutti OK, uguali alla 0.21 | — | ✔ |

### 3.1 Dettaglio di `collaudo_competizione.py`

Su `main` i numeri coincidono con quelli scritti nel `CHANGELOG.md` per la 0.21, quindi il confronto è affidabile. Nessuna regata pulita né sul ramo né su `main` (0 su 80 per gruppo), come nella 0.21.

| Gruppo | C1: 1°/2°/3°/4° su 80 (main) | (ramo) | C2: coppie con almeno 3 punti (main) | (ramo) |
|---|---|---|---|---|
| Principianti, semi 1-40 | 12/24/24/20 | 15/15/26/24 | 38 su 40 | 38 su 40 |
| Principianti, semi 41-80 | 10/18/26/26 | 13/18/25/24 | 35 su 40 | 36 su 40 |
| Esperti, semi 1-40 | 13/22/22/23 | 14/13/26/27 | 38 su 40 | 36 su 40 |
| Esperti, semi 41-80 | 8/25/21/26 | 9/23/23/25 | 36 su 40 | 37 su 40 |

C0 (arrivate 100%), C3 (38 finestre su 38), C4 (0 coppie a 10 punti) e C5 sono uguali su ramo e `main` in tutti i gruppi.

---

## 4. Le due differenze

### 4.1 `collaudo_lezioni.py`, lezione 5

**Cosa fa il collaudo** [codice, `tests/collaudo_lezioni.py`]: apre il passo «Prepararsi a virare» con la barca al traverso, tiene → per **0,7 s fissi**, poi ↑ per 1,5 s, e aspetta il passo. Il colpo è a tempo fisso, senza guardare dove va la prua.

**Sul ramo:** «prepararsi» non si completa (finisce a 38° dal vento, 1,6 nodi). La virata parte da ferma e non riesce (finisce a −1 nodi), e così l'assestamento.

**Riproduzione in Node** con gli stessi tasti: barra +1,6 al secondo, poi ritorno al centro con fattore exp(−2,5·dt), scotta −0,27 al secondo [misura]:

| | Prua minima dal vento | A 2 s | A 10 s |
|---|---|---|---|
| Barca di oggi | 51,9° | 54°, 3,9 nodi | 52°, 4,0 nodi |
| Barca del ramo | 32,6° | 35°, 3,1 nodi | 37°, 0,9 nodi |

**Lettura** [stima]: è la sensibilità doppia della barra che si vede davvero, non un errore della barca. Chi è abituato alla barca di oggi, con lo stesso colpo, orza troppo e si pianta.

Il collaudo andrebbe adattato (un colpo più corto, o un colpo che guarda la prua). **Non è stato cambiato:** prima la prova a mano.

### 4.2 `collaudo_aggressiva.py`

Criterio [`docs/COLLAUDI.md`]: per ogni incontro, almeno una manovra deve evitare il contatto. Somma di 5 giri per parte, senza seme [misura]:

| Distanza | Main: evitabili | Ramo: evitabili | Main: contatti per manovra (poggia subito / poggia dopo 1 s / orza dopo 1 s / niente) | Ramo |
|---|---|---|---|---|
| 18 m | 48 su 50 | 47 su 50 | 10 / 12 / 3 / 10 | 5 / 5 / 3 / 4 |
| 24 m | 50 su 50 | 46 su 49 | 0 / 2 / 3 / 2 | 3 / 4 / 4 / 7 |
| 30 m | 50 su 50 | 50 su 50 | 0 / 0 / 3 / 7 | 0 / 0 / 1 / 6 |
| 38 m | 50 su 50 | 50 su 50 | 0 / 0 / 0 / 5 | 0 / 0 / 0 / 8 |

- **Anche su `main` il criterio non regge sempre:** a 18 m due giri su cinque danno 9 su 10.
- Sul ramo, a 24 m, i tre incontri non evitabili sono **tutti nel primo giro**; negli altri quattro giri 10 su 10 (una volta 9 su 9, con un incontro saltato).
- **Lettura** [stima]: peggioramento possibile, non dimostrato. Possibile causa, non verificata: l'aggressiva vira quasi due volte più svelta e insegue meglio.
- Per dirlo servono più giri, oppure un seme fisso nel collaudo.

---

## 5. Lezione 5 e passo 5.4: testi e condizioni (nessun testo modificato)

Numeri di riga di `index.html` sul ramo.

| Passo | Cosa dice | Cosa cambia con la variante |
|---|---|---|
| 5.2 «Prepararsi a virare» (riga 636) | Testo: «Mettiti in bolina, regola la vela e lascia che la barca arrivi ad almeno 3,3 nodi». Condizione: prua fra 43° e 72°, filetti ok, almeno 3,3 nodi per 1 s. Non nomina la barra | Il testo resta valido. Lo stesso colpo di barra fa orzare circa il doppio: è qui che il collaudo si pianta (§4.1) |
| 5.3 «Virare» (riga 641) | «Sposta la barra sottovento (verso il boma) **con decisione** e **tienila** finché la prua ha attraversato il vento e sei in bolina sull'altro lato. Poi centra la barra.» | Funziona ancora, ma la barra a fondo non è più la migliore: a 10 nodi 3,29 s a fondo contro 2,85 a metà corsa [misura, proposta §4.3]. «Con decisione» oggi vuol dire «a fondo»; con la variante basta metà corsa. Condizione (virate in più, prua fra 40° e 78°, più di 1,2 nodi, tenuta 0,8 s): invariata, e più facile perché la velocità minima in virata resta al 32% di quella d'ingresso invece del 29% |
| 5.4 «Una virata che non riesce» (righe 645-657) | Testo: «lasca la vela finché la barca scende sotto 1 nodo, poi prova a virare. Se non rallenti abbastanza, orza fino alla bolina…». Uscita: «sposta la barra verso il boma…». Fine del passo: «senza velocità il timone non fa effetto… si vira sempre con la barca lanciata» | La virata lenta riesce un po' più spesso: sotto 1 nodo 99 su 360 contro 88 [misura]; a 1,9 nodi ora riesce (`raffiche_e_virate.js`). Quindi «se non rallenti abbastanza» pesa di più. L'uscita all'indietro è **identica** (formula invariata all'indietro). La frase finale resta vera, perché la rotazione è proporzionale alla velocità. La condizione non cambia |
| 5.4, dal collaudo del registro (parte i) | Sul ramo, nelle 8 prove, la prua passa dall'altra parte del vento prima di piantarsi; su `main` resta sulla stessa mura | Il passo si completa lo stesso: 4 su 4 e 4 su 4 su tutti e due |
| 5.5 «Risalire il vento» (riga 658) | Nessun testo sulla barra | Bordeggiare è un po' più facile |
| Riepilogo (riga 674) | «Virata: prua nel vento, con la barca lanciata» | Invariato |

**Testi collegati:**
- **Lezione 2**, righe 543, 547, 551-552: «a piccoli colpi e non con un colpo lungo», «usare poca barra». Ancora più vere, perché un colpo piccolo ora gira il doppio.
- **Domande 749 e 785** («ogni angolo di barra frena»): restano vere, la resistenza della barra non è cambiata.
- **Domanda 22 dell'esame** (riga 798, «come ne esci?») e suggerimento «all'indietro»: comportamento identico (`angolo_morto.js` uguale carattere per carattere).

---

## 6. Prova a mano di Ale (da fare)

Il ramo è quello attivo. Per aprire il gioco:

```
xdg-open /home/callle/scuola-di-vela/index.html
```

Cosa guardare:

1. **Lezione 2, «Tenere la rotta»:** la prua scappa da una parte all'altra? Bastano colpi più piccoli di prima? Nell'emulazione il pilota passa da 3 a 13 cambi di lato della barra.
2. **Lezione 5, «Prepararsi a virare»:** orzando dal traverso, finisci oltre la bolina e ti pianti?
3. **Lezione 5, «Virare»:** prova la barra a fondo e la barra a metà corsa. Si sente la differenza?
4. **Lezione 5, «Una virata che non riesce»:** riesci ancora a farla fallire rallentando sotto 1 nodo?
5. **Una regata con avversari esperti** (c'è l'aggressiva): si riesce a evitarla?
6. **In generale:** la barca è troppo nervosa? La lezione 1, con la barra che torna al centro, è ancora facile?

---

## 7. Rischi e cose aperte

- **Sensibilità doppia sotto 15°** [misura]: è l'effetto principale, e quello da giudicare a mano.
- **Il gioco diventa più facile:** virate più rapide e più riuscite, a 1,9 nodi si vira, gli avversari arrivano 6-13 s prima (mediane).
- **«Barra a fondo è un errore» si sente poco:** costa circa 0,44 s su una virata di 3 s.
- **`collaudo_lezioni.py` va adattato** se la variante resta (§4.1).
- **Aggressiva:** da ripetere con più giri o con un seme fisso (§4.2).
- **`sperimentale/fiocco.html`** ha la sua copia di `step()`: non allineata (decisione di Ale), quindi la non-regressione «senza fiocco identico al gioco» oggi non vale sul ramo.
- **Le tre righe con «30-35°» ancora nei documenti** (§1.3).
- **Dubbio separato:** la barca frena troppo in fretta (1-1,6 lunghezze contro 3-4)? Riguarda la frenata, non il timone.

---

## 8. Decisioni che spettano ad Ale

1. Dopo la prova a mano: tenere la variante, compensare meno, oppure non farla.
2. Se adattare `collaudo_lezioni.py` e ripetere l'aggressiva con più giri o con un seme fisso.
3. Se togliere o riscrivere le tre righe con «30-35°» rimaste.
4. Se la versione diventa la 0.22: allora `VERSIONE`, `CHANGELOG.md` e l'allineamento dei documenti, come elencato nel §6 della proposta.
5. Se allineare `sperimentale/fiocco.html`.
6. Se cambiare `KEYV`. Tecnicamente non serve: i fantasmi sono traiettorie e non comandi rigiocati, e le fasce non cambiano.

---

## 9. Comandi git (li esegue Ale)

Sul ramo `prova-saturazione`:

```
git add index.html
git add docs/PROPOSTA-SATURAZIONE-TIMONE.md
git add docs/RAPPORTO-PROVA-SATURAZIONE.md
git add docs/RICERCA-DATI-IMBARDATA.md
git add docs/PIANO-GENERALE.md
```

`.codex/` e `.gitmodules` vanno lasciati fuori. Niente `git add -A` né `git add .`.
