# Proposta: esame e brevetto del livello 1 (traguardo 1.0)

Bozza del 9 ottobre 2026, aggiornata lo stesso giorno con le decisioni di Ale (§6) e con i controlli sul codice (§1, in fondo). **Prima fermata**: solo proposta, nessuna modifica al codice. Le righe di `index.html` citate sono quelle della 0.19.5.

**Principi decisi da Ale [deciso, 9 ottobre 2026]:**

- **Il gioco libero è il banco di prova; il vero gioco è la carriera.** Attestato, brevetto e libretto esistono solo in carriera. Nel gioco libero l'esame si può fare come prova, senza conseguenze salvate.
- **L'esame è una verifica interna al gioco.** Non c'è niente da studiare fuori dalle lezioni.

Stati come negli altri documenti: **[deciso]**, **[proposta]**, **[provvisorio]**, **[aperto]**, **[da verificare]**.

Traguardo **[deciso]**: 1.0 = livello 1 completo, cioè esame a risposte chiuse, brevetto con attestato e libretto minimo con il bivio gioco libero / carriera. Tutto il resto è fuori.

Nota sui documenti: il `CHANGELOG.md` sta nella cartella principale, non in `docs/`. `RIPARTI-DA-QUI.md`, citato nel piano generale, non è nel repository.

---

## 1. Cosa esiste già e si riusa

| Cosa | Dove (`index.html`) | Come si riusa |
| --- | --- | --- |
| Domande del ripasso `QUIZ`: 6 lezioni, 29 domande, formato `[domanda, giusta, [3 sbagliate], spiegazione]` | 723-754 | Lo stesso formato per la banca dell'esame. Le 29 domande **restano al ripasso** e non entrano nell'esame (decisione 9, §6). |
| `openQuiz(li, only)`: costruisce le domande, mescola le risposte (Fisher-Yates in linea) e apre il dialogo | 982-992 | Si generalizza: prende una lista di domande e un titolo invece dell'indice della lezione. Il rimescolamento diventa una funzione da 3 righe, usata anche per estrarre le domande. |
| `renderQuiz()`: una domanda alla volta, spiegazione subito, alla fine il punteggio e l'elenco delle sbagliate in una zona che scorre (0.19.5) | 995-1027 | Si riusa così com'è per l'esame, cambiando solo la schermata finale: le sbagliate raggruppate per lezione, l'esito (superato o no) e, in carriera, i pulsanti dei ripassi da fare. |
| Dialogo `#quiz`, già misurato a 1360×650 e 1360×768 con 6 errori (`collaudo_quiz.py`) | 216; CSS `.qz`, `.wlist` | Lo stesso dialogo per l'esame. Con 20 domande gli errori possono arrivare a 20: l'elenco scorre già, ma va rimisurato. |
| Record del ripasso `progress.quiz["q"+i]`, aggiornato solo con un ripasso completo | 998-999 | È l'area **Conoscenza**. Serve anche al ripasso mirato: «almeno l'80% nel quiz della lezione». |
| «Rivedi la lezione» (`startLesson`) e «Fai il ripasso» a fine lezione (`lQuiz`) | 1003-1006, 1144, 1157 | Pulsanti del ripasso mirato. |
| Salvataggio `progress = { done, best, clean, quiz }` nella chiave `STORE = "scuolaVelaSim.v1"`; `saveProgress()` | 893, 900, 907-908 | **Il punto chiave per la carriera:** tutto il gioco scrive già in `progress`. Se in carriera `progress` si carica da un'altra chiave, lezioni, prove, regate e ripassi finiscono nel salvataggio di carriera **senza toccare il loro codice** (§2). |
| Lezione completata: `progress.done["l"+i]` all'ultimo passo (`final`) | 1145 | Area **Esperienza**. |
| Prova finita: tempo migliore `progress.best`, `done`, `clean` se il registro è vuoto | 1416-1420 | Area **Abilità**, con `medalOf(i, sec)` (904) e le fasce `bands` (697-718). |
| Regata finita: tempo migliore, `done`, `clean` | 1799-1804 | **Il piazzamento non viene salvato da nessuna parte:** lo calcola solo `raceResults()` (1811) con `ranking()` (1807) per scriverlo a schermo. Va aggiunto (§2). |
| `ranking()`: chi è arrivato prima sta davanti, chi non è arrivato sta dietro | 1807-1810 | All'arrivo del giocatore il suo piazzamento è già definitivo: chi non è ancora arrivato non può più superarlo. |
| Avversari: `opt.aiLevel` (`principianti`, `esperti`, `nessuno`) | 265, 815, 1538-1541 | Con «nessuno» il giocatore è «1° su 1»: **va escluso dalla Competizione**. |
| Registro degli errori `reg`, `regTotal()`, `regText()` | 1062-1095 | Il «+1 senza errori» di Abilità e Competizione (già usato per la ★). |
| Menu a riquadri `showMenu()`; nel riquadro «Ripasso ed esame» c'è già il pulsante spento «Esame su tutte le lezioni · in arrivo» | 921-964; 951-952 | Il pulsante si accende; il testo «In arrivo» si aggiorna. Il libretto va nello stesso riquadro, in carriera. |
| «Azzera i progressi» | 961 | In carriera deve azzerare solo la carriera, e dirlo nella conferma. |
| Selettore a due pulsanti `.seg` con `seg(id, key)` | 1278-1284, HTML 227-230 | Per il bivio «Gioco libero / Carriera». |
| Aiuti in `opt`: `helm` («girano la prua»), `autoCenter`/`autoCenterComp`, `hint`, `arrows`, `dead`, `allInstr`, `ghost` | 815, 233-243 | Con l'opzione A (§6) non servono ai meriti: nessun campo in più da salvare. |
| Aggancio `#collaudo` (`window.__sv`) | 2701-2707 | Va esteso: estrazione dell'esame, calcolo dei meriti, piazzamento. |
| Pilota automatico delle prove (`collaudo_fasce.py`, `__sv.run` a passi fissi, semi fissi) | tests | Collaudo dell'Abilità e della carriera guidando la barca. |
| `collaudo_quiz.py`: risposte sbagliate apposta, misura del dialogo con i caratteri veri | tests | Base per `collaudo_esame.py`. |

**Cosa non c'è e va scritto:** banca d'esame, estrazione, piazzamento salvato, salvataggio di carriera, calcolo dei meriti, libretto, regola del ripasso mirato, attestato. Non esiste un pilota che guidi la barca del giocatore **in regata** (i collaudi delle regate guidano solo gli avversari): serve per tarare la Competizione (§4).

**Cosa non mi è chiaro nel codice, e non ho supposto:**

- Se `aiControl(b, dt)` (1618) funziona anche sulla barca del giocatore: scrive `b.ctl`, e per il giocatore `ctl` passa anche da `applyInput()` (1308), che potrebbe sovrascrivere barra o scotta. Va provato prima di contarci (fetta 2).
- `resetProg` (961) rimette `progress = { done, best, clean }`: cancella anche i ripassi (`quiz`), e cancellerebbe anche i campi nuovi. Va bene, ma la conferma deve dirlo.

### Controlli del 9 ottobre (solo lettura)

**1. Domande del ripasso su precedenze e regole di regata.** Ho cercato nelle 29 domande (723-754) «strada», «precedenza», «regol», «incroc», «contatt», «rotta». Ne parla **una sola**:

| Domanda | Ripasso | Passo che la insegna |
| --- | --- | --- |
| «Due barche a vela si incrociano, una mure a sinistra e una mure a dritta. Chi deve lasciare strada?» (giusta: mure a sinistra) | Lezione 3 (740) | **Sì**: lezione 3, passo «Le mure» (574-576), seconda frase: «Le mure contano anche per le precedenze: quando due barche a vela si incrociano con mure diverse, quella mure a sinistra deve lasciare strada.» È un passo di sola spiegazione (`PAUSE`), una frase, senza esercizio. Lo dice anche il glossario, voce «Mure» (777). |

Le altre due righe che contengono «regola» o «rotta» non sono di precedenze («La regola: barra sottovento orza…», lezione 2; «Orzi e cazzi», lezione 3). Il sospetto di Ale non si conferma per il ripasso. Si conferma invece **fuori dalle domande**: la regola «stesse mure, lascia strada chi è sopravento» **non è insegnata in nessuna lezione**. Compare solo nel messaggio di contatto delle regate (1766-1767) e in `CONTENUTI-DA-VERIFICARE.md`. Nessuna domanda la usa.

**2. «Le frecce girano la prua» (`opt.helm === "prua"`).** In `applyInput()` (1308-1317) cambia una sola cosa: il verso delle frecce. La freccia destra muove la barra in modo che la prua giri a destra, e il verso si inverte da sola quando la barca va all'indietro (`S.u < 0`). La barra si muove alla stessa velocità (1,6 al secondo) e torna al centro con le stesse regole di prima (`autoCenter`, 1319-1321). **Non corregge la rotta da sola** e non gira la prua direttamente: è solo un'altra corrispondenza fra tasti e barra. Il nome dell'impostazione lo fa sembrare più di quello che è.

Strumenti:

- **Sempre visibili**, senza impostazione: bussola (`drawCompass`, 2136), riquadro del vento (`drawWindBox`, 2137), freccia verso l'obiettivo fuori schermo (2130), indicatore di sbandamento quando il passo ha `hud` ≥ 3 e sempre fuori dalle lezioni (2139-2140). Nel pannello, Velocità, Andatura, Prua e Rilevamento secondo il livello `hud` (327-332, `setHud` 1051-1057).
- **Attivabili** nelle impostazioni (233-243): suggerimenti (`hint`, 1286), frecce del vento e della velocità (`arrows`, 2134 e 2443), rosa dell'angolo morto (`dead`, 2142), tutti gli strumenti nel pannello fuori dalle lezioni (`allInstr`: vento reale, vento apparente, sbandamento, scarroccio, righe con `data-x` 329-334, 1054), fantasma (`ghost`), barra che torna al centro (`autoCenter`), «girano la prua» (`helm`).

**3. Livello degli avversari.** Si sceglie nel riquadro delle istruzioni della regata, menu a tendina «Avversari»: principianti, esperti, nessuno (265; valore in `opt.aiLevel`, 815; cambio 1295). Entra in `aiParams()` (1538-1541) e nella scelta dell'avversaria aggressiva (1561). **Non viene salvato nei risultati:** il tempo migliore della regata (`progress.best`, 1801-1803) e il fantasma (`recStart`, 1572) hanno la stessa chiave per tutti e tre i livelli. Un record fatto da soli («nessuno») vale come uno fatto contro gli esperti. Lo scrive solo il registratore di sessione (2535), che non entra in nessun calcolo. Oggi quindi non può entrare nei meriti: per usarlo serve la chiave nuova proposta nel §2.

---

## 2. Struttura dei dati

### Banca delle domande **[proposta]**

```js
// Esame: [lezione, titolo del passo da cui viene, domanda, giusta, [3 sbagliate], spiegazione]
const ESAME = [
  [0, "Dritta e sinistra", "…", "…", ["…", "…", "…"], "…"],
  …
];
```

- Stesso formato del `QUIZ` più due campi: la **lezione** (serve all'estrazione per quote e al ripasso mirato) e il **titolo del passo** da cui nasce la domanda **[deciso]**. Il titolo del passo serve al collaudo, che controlla che il passo esista (§5).
- Le 29 domande del ripasso restano separate **[deciso]**.
- Nessuna domanda con disegno nella 1.0: le «situazioni» si descrivono a parole («il vento arriva sul lato destro, a 90° dalla prua: …»). Il piccolo disegno di barca e vento della visione va dopo la 1.0.

### Estrazione **[proposta]**

- 20 domande **per quote di lezione**: L1 4, L2 3, L3 4, L4 3, L5 3, L6 3. Ogni esame copre tutte le lezioni, e le sbagliate si possono attribuire a una lezione senza ambiguità.
- Dentro ogni lezione l'estrazione è casuale (lo stesso rimescolamento delle risposte); poi si rimescola l'ordine delle 20 domande.
- Soglia **[deciso]**: 16 su 20.

### Salvataggio **[proposta]**

| Chiave | Contenuto |
| --- | --- |
| `scuolaVelaSim.v1` | Gioco libero, come oggi, più il campo `race` (piazzamento). **L'esame non salva niente** **[deciso]**. |
| `scuolaVelaCarriera.v1` (nuova) | Stessa forma di `progress`, più `exam: { prove, migliore, superato, data, nome, ripasso: [lezioni] }`. |
| `scuolaVelaModo` (nuova) | `"libero"` o `"carriera"`: l'ultima scelta, ricordata all'apertura. |
| `scuolaVelaGhost.v1` | Fantasmi del gioco libero. ~~In comune fra le due modalità~~: **separati dalla 0.22** (§11, decisione di Ale del 14 ottobre 2026); in carriera `scuolaVelaGhostCarriera.v1`. Non sono meriti. |

- **Come si separano:** `STORE` diventa una variabile. Il bivio, solo dal menu, salva il `progress` corrente, cambia chiave e ricarica `progress` dalla chiave nuova. Il resto del gioco non cambia.
- **Piazzamento delle regate:** all'arrivo, accanto al tempo migliore, si salva `progress.race[chiave] = { pos, n, pulita }`, ma solo se ci sono avversari. Si salva anche nel gioco libero, perché il codice è lo stesso e un ramo in più costerebbe di più; lì non si mostra e non conta.
- **Livello degli avversari nel piazzamento: alternativa non ancora decisa** (vedi l'avvertenza della fetta 0.21). Oggi il livello non è salvato da nessuna parte (controllo 3). Due strade: in carriera il livello degli avversari è fisso, oppure entra nel risultato salvato (per esempio con una chiave come `r0.2:principianti`, `r0.2:esperti`). **Decisione di Ale (12 ottobre 2026, avvio della 0.21): strada B minima.** Solo `progress.race` usa la chiave con il livello (`recK("r"+i) + ":" + livello`, per esempio `r0.2:principianti`); record, stelle, fantasmi e `KEYV` restano invariati, quindi non si azzera niente. Il piazzamento si salva quando è definitivo, non all'istante dell'arrivo; per ogni chiave si tiene il migliore per punti.
- Niente importazione dal gioco libero **[deciso]**: la carriera parte vuota.
- I meriti **non si salvano**: si ricalcolano ogni volta da `progress` con una funzione pura `meriti(progress) → { aree, totale, livelloSuperato, manca }`. `manca` elenca ciò che manca per superare il livello: soglie dei meriti, esame, ruoli. Un numero solo da tarare, nessun dato da migrare.

---

## 3. Schermate

Regola: niente testo in più a video quando basta il manuale. Le regole dei meriti stanno in `MANUALE-bozza.md`, non nel gioco.

**Bivio.** Nell'intestazione del menu, accanto a «Glossario», un selettore a due pulsanti: **Gioco libero | Carriera**. Di norma è su «Gioco libero» e ricorda l'ultima scelta. Niente schermata in più all'avvio: chi apre il gioco lo trova come oggi. In carriera il menu è lo stesso, perché al livello 1 non c'è niente da sbloccare: cambiano solo il salvataggio e il terzo riquadro.

**Riquadro dell'esame** **[deciso]**: nel menu, nel riquadro «Ripasso ed esame», vicino ai ripassi (dove oggi c'è il pulsante spento, 951). Il pulsante è acceso sia nel gioco libero sia in carriera; in carriera si spegne solo dopo un esame non superato, finché il ripasso mirato non è fatto.

**Libretto** (solo in carriera, nello stesso riquadro, sotto ripassi ed esame):

- Quattro barre, una per area: Abilità, Conoscenza, Competizione, Esperienza. Su ogni barra una tacca al minimo e il numero «12 / 20 (minimo 8)». Sotto, il totale con il suo minimo.
- **Una riga «cosa manca»** per superare il livello, sola e concreta, scelta in quest'ordine: prima l'area sotto il minimo più lontana, poi il totale, poi l'esame. Per esempio «Manca 1 punto in Competizione: arriva in fondo a una regata con gli avversari.» oppure «Manca l'esame.» Con il livello superato: «Brevetto ottenuto il …» e il pulsante «Attestato».
- Il **pulsante dell'esame** non dipende dai meriti: è sempre acceso, tranne dopo un esame non superato, finché il ripasso mirato non è fatto. In quel caso la riga «cosa manca» dice quali ripassi servono.

**Esame** (lo stesso dialogo del ripasso):

- Titolo «Esame · livello 1», «Domanda 7 di 20». Una domanda alla volta.
- **Spiegazione delle sbagliate: solo alla fine, non dopo ogni risposta** **[deciso]**. È diverso dal ripasso: se la spiegazione arriva subito, aiuta nelle domande dopo.
- Alla fine: «17 su 20: superato» oppure «14 su 20: non superato (servono 16)», poi le sbagliate **raggruppate per lezione**, con risposta data, risposta giusta e spiegazione.
  - Nel gioco libero: «Rifai l'esame» e «Chiudi». Niente si salva **[deciso]**.
  - In carriera, se l'esame non è superato: per ogni lezione con errori un pulsante «Ripasso: Lezione 3», che apre il ripasso già esistente. Il pulsante dell'esame resta spento finché ognuna di quelle lezioni non ha un ripasso completo con almeno l'80%, fatto **dopo** l'esame; poi si riaccende. È l'unico caso in cui è spento. Nessuna attesa, nessuna penalità, i meriti restano.
  - In carriera, se l'esame è superato: si passa all'attestato.

**Attestato** **[deciso]**: compare come **breve scena nel passaggio da un livello all'altro**, solo in carriera. Oggi c'è un solo livello, quindi il passaggio è la chiusura del livello 1: la scena arriva **quando viene raggiunta l'ultima condizione** per superarlo (soglie dei meriti, esame superato, ruoli). Se l'esame è superato prima dei meriti, la scena arriva più tardi, con l'ultimo merito che mancava. Poi si riapre dal libretto. È una pagina sopra il menu, con «Stampa» e «Chiudi».

- Il testo: «Scuola di vela · Brevetto di livello 1 · Timoniere di deriva», il nome (campo facoltativo, scritto dal giocatore e salvato solo nel browser), la data, il punteggio dell'esame, i quattro meriti, e in evidenza: «Nessun valore legale: non sostituisce un corso di vela né la patente nautica.» Niente loghi, niente sigle, niente «patente» o «patentino» nel titolo.
- **Stampa** con `window.print()` e un foglio di stile `@media print` che stampa solo l'attestato. Niente PDF generato, niente librerie.
- Il nome del brevetto è «Timoniere di deriva» **[deciso]**.
- **Nel gioco libero non c'è attestato** **[deciso]**: l'esame lì è una prova.

---

## 4. Punteggi

### Tabella del livello 1 ricalcolata **[provvisorio]**, scritta prima di qualsiasi misura

> **Superata il 14 ottobre 2026** per la Competizione: niente «+1 senza errori», massimo 8, totale massimo 46. Tabella in vigore nel §12, «Tabella dei meriti dalla 0.23».

| Area | Punti | Massimo | Minimo |
| --- | --- | --- | --- |
| Abilità | 5 prove: bronzo 1, argento 2, oro 3, +1 se completata almeno una volta senza errori | 20 | 8 |
| Conoscenza | 6 ripassi: 2 punti se il migliore è almeno l'80%, 1 punto se almeno il 60% | 12 | 6 |
| **Competizione** | **2 regate singole, solo con avversari** (principianti o esperti, stessi punti); per ogni regata conta il risultato migliore: 1° = 4, 2° = 3, 3° = 2, 4° = 1, +1 se senza errori | **10** | **3** |
| Esperienza | 1 punto per ogni lezione completata | 6 | 6 |
| **Totale** | somma dei minimi 23 | **48** | **29 richiesti** |

Perché così:

- **Competizione.** Il minimo 3 si raggiunge arrivando ultimi in entrambe le regate, una delle due senza errori (1 + 2), oppure con un 3° posto e un ultimo. Quindi non serve battere nessuno, serve **finire le regate**, in linea con il piano (§5: «il passaggio non deve mai dipendere dalla forza dell'equipaggio»). Il «senza errori» segue la regola della ★ (`regTotal() === 0`). **Dalla 0.21.1 (decisione di Ale, 13 ottobre 2026) un contatto senza colpa del giocatore non conta:** `regTotal()` somma `contactsPen` e non più `contacts`; il contatto resta scritto nel riepilogo («senza colpa, non conta») e nel registratore. Prima della 0.21.1 qui c'era «conta anche un contatto subìto».
- **Totale.** Il margine sopra la somma dei minimi resta +6, come nella tabella della visione (22 → 28).
- **Conoscenza, attenzione:** i ripassi delle lezioni 2, 4 e 6 hanno 4 domande. L'80% di 4 è 3,2, quindi servono 4 su 4; con 3 su 4 (75%) si prende 1 punto. Lo stesso vale per il ripasso mirato. È un effetto della soglia sui numeri piccoli, non un errore: lo dichiaro.

Esempi ricalcolati (come nella visione):

| Giocatore | Abilità | Conoscenza | Competizione | Esperienza | Totale | Esito |
| --- | --- | --- | --- | --- | --- | --- |
| A: prove in argento, due 3° posti, una regata pulita | 10 + 2 = 12 | 8 | 2 + 3 = 5 | 6 | 31 | Meriti a posto; livello superato quando supera l'esame |
| B: tutti ori senza errori, nessuna regata | 20 | 12 | 0 | 6 | 38 | Livello non superato. Cosa manca: Competizione sotto 3 (ed esame, se non fatto) |
| C: forte, ma ha saltato tre lezioni | 14 | 10 | 6 | 3 | 33 | Livello non superato. Cosa manca: Esperienza sotto 6 (ed esame, se non fatto) |
| D: bronzo ovunque, una prova pulita, ultimo nelle due regate con una pulita | 6 | 6 | 3 | 6 | 21 | Livello non superato. Cosa manca: Abilità sotto 8 e totale sotto 29 (ed esame, se non fatto) |

### Come si verifica che i numeri non siano né troppo facili né impossibili

**Competizione: misura nuova, soglie scritte adesso.**

- **Metro:** un pilota sostituto guida la barca del giocatore. Proposta: la stessa guida degli avversari (`aiControl` con `aiParams("principianti")`), se funziona sulla barca del giocatore (§1, da provare). È un principiante del computer, non una persona: misura la scala, non il giocatore vero.
- **Campione:** 40 regate per tipo (bastone e raffiche), semi fissi 1-40, avversari principianti, preparazione 3 minuti, `__sv.run` a passi fissi, una pagina nuova per regata. Poi le stesse 80 con gli esperti, che si riportano soltanto, senza soglia.

Soglie, da non cambiare dopo aver visto i risultati:

| # | Criterio | Soglia |
| --- | --- | --- |
| C0 | **Validità del metro**: il sostituto arriva in fondo | almeno 90% delle regate per tipo; sotto, la misura non vale e si sistema il pilota, non i punti |
| C1 | Con avversari pari, nessun posto è impossibile né scontato | ogni piazzamento (1°-4°) tra il 10% e il 40% |
| C2 | Il minimo si raggiunge con un tentativo per regata (coppie seme k, regata 1 e 2) | almeno il 60% delle coppie |
| C3 | Il minimo si raggiunge con tre tentativi per regata (migliore di 3 semi consecutivi) | almeno il 90% |
| C4 | Il massimo non è scontato: 10 punti con un tentativo per regata | al massimo il 10% delle coppie |
| C5 | Il controllo ha misurato davvero | numero di regate concluse e di coppie stampato; fallisce se è zero |

**Abilità: nessuna misura nuova.** Le fasce sono tarate sul pilota: oro = tempo del pilota arrotondato, bronzo = +60% (0.16 e 0.19). Il minimo 8 equivale a bronzo ovunque più 3 prove pulite, oppure argento in 4 prove. Nelle prove 1-4 il pilota di `collaudo_fasce.py` fa oro per costruzione; nella prova 5 finisce 19 corse su 24, con mediana 353,6 s contro l'oro a 355 s (valori del PC di Ale; nella sandbox la prova 5 varia: 18-21 su 24, mediana 353,6-354,6). Basta riportarlo.

**Esame.**

- **Indovinare a caso** con 4 risposte: la probabilità di fare 16 su 20 è **3,9·10⁻⁷** (binomiale, calcolata).
- **Memoria al posto della comprensione:** quante domande hanno in comune due esami di seguito dipende dalla banca. Il calcolo: per ogni lezione, quota² diviso numero di domande della lezione, poi la somma. **Con la banca minima decisa (26 domande, quota + 1 per lezione) sono in media circa 15 su 20** (3,2 + 2,25 + 3,2 + 2,25 + 2,25 + 2,25 = 15,4). Con 8 domande per lezione sarebbero circa 8,5. È un numero, non un problema da risolvere adesso: lo riporto perché con la banca minima chi ripete l'esame ritrova quasi tutte le domande.
- **Un difetto da non ripetere**, misurato sulle 29 domande attuali: la risposta giusta è la più lunga in **12 casi su 29 (41%)**, contro il 25% del caso. Chi ha l'occhio allenato la indovina. Soglia per la banca nuova: **al massimo il 30%**.
- **«Né impossibile»** il collaudo non lo può misurare: lo misurano le persone. Criterio proposto: Ale, dopo aver fatto le lezioni e senza aver letto la banca, fa l'esame 2 volte e riporta i punteggi. Chi gioca non deve giudicare se le domande sono giuste nauticamente: quello lo dicono le fonti (§5).

---

## 5. Le domande

### Quante e come scriverle

- **Regola della banca [deciso]:** una domanda per ogni concetto che una lezione insegna davvero e che si può verificare con una risposta chiusa. **Nessun obiettivo numerico fisso.**
- **Minimo per lezione [deciso]:** la quota dell'esame più una, cioè L1 5, L2 4, L3 5, L4 4, L5 4, L6 4 (26 in tutto). Se una lezione offre meno concetti del minimo, lo segnalo invece di riempire.
- **Ogni domanda porta il passo di lezione da cui nasce [deciso].** Il glossario da solo non basta: serve un passo.
- **Una domanda senza un passo che la insegna si toglie [deciso].** L'alternativa è aggiungere il passo mancante alla lezione, e questo lo decide Ale, non chi scrive le domande.
- **Fuori** **[deciso]**: le precedenze e le regole di regata 10, 11, 14, 18. Questo esclude anche «mure a sinistra lascia strada a mure a dritta», che pure è insegnata in una frase del passo «Le mure» (controllo 1). Quella domanda resta nel ripasso così com'è.

**Stima dei concetti per lezione** (dalla tabella sotto, da contare davvero scrivendo la banca): L1 circa 12, L2 circa 5, L3 circa 7, L4 circa 6, L5 circa 5, L6 circa 6. **Le lezioni 2 e 5 sono le più strette**: 5 concetti contro un minimo di 4. Se nella lezione 5 si toglie «comandi di manovra» (fra i dubbi, vedi sotto), resta un concetto solo di margine.
- **Fuori anche (proposta mia):**
  - i punti della sezione «Dubbi specifici» di `CONTENUTI-DA-VERIFICARE.md`, cioè strambata o abbattuta, confini in gradi delle andature, posizione e colori dei filetti, comandi di manovra (varianti tra scuole), orziera e scadere;
  - **i numeri del motore** (33°, 40°, 60° di scuffia): sono tarature, non nozioni di vela.
- Tre risposte sbagliate plausibili e della **stessa lunghezza** della giusta. Niente «tutte le precedenti», niente doppie negazioni.
- Spiegazione di una o due frasi, parafrasata dalla lezione.
- Ogni domanda nuova va aggiunta a `CONTENUTI-DA-VERIFICARE.md` sotto la sua lezione, con l'esito vuoto. **Attenzione:** in quel file quasi tutte le righe delle lezioni hanno l'esito **vuoto**. «Solo contenuti già nelle lezioni» vuol dire «nessuna affermazione nuova», non «affermazioni verificate».

### Argomenti per lezione (senza domande)

| Lezione | Argomenti (dai titoli dei passi e dal glossario) |
| --- | --- |
| 1 · La barca e il vento | prua e poppa; dritta e sinistra (della barca, non dello schermo); albero, boma, randa; timone, barra, deriva (a cosa serve la lama); il vento si nomina da dove arriva; sopravento e sottovento, lato del boma e del timoniere; poggiare; orzare e angolo morto (concetto, non gradi); ripartire dall'angolo morto; lascare e cazzare; vela che fileggia; vela troppo cazzata |
| 2 · Il timone | la barra si spinge dalla parte opposta a dove si vuole girare; barra sottovento orza, sopravento poggia; poca barra perché la pala frena; il timone non funziona da fermi e funziona al contrario all'indietro; tenere la rotta con piccole correzioni |
| 3 · Andature, mure e precedenze | bolina, traverso, lasco, gran lasco, poppa (ordine e descrizione, non i gradi esatti); più veloce al traverso e al lasco che in poppa; le mure (nome, lato del boma; **senza precedenze**); cosa dicono i filetti (sopravento agitato, dritti, sottovento agitato) e cosa fare; «orzi e cazzi, poggi e laschi» |
| 4 · Vento reale e apparente | definizione del vento apparente; da fermi apparente = reale; accelerando si sposta verso prua e la vela va cazzata; in poppa è più debole del reale, di bolina più forte; il segnavento indica l'apparente |
| 5 · Virata e strambata | virata (prua nel vento) e strambata (poppa nel vento); virata che non riesce per poca velocità; bordeggiare e bordo; strambata violenta con la vela aperta; strambata controllata (cazzare, poggiare, lascare) |
| 6 · Raffiche e scuffia | riconoscere una raffica (chiazza scura che arriva da sopravento); lascare come prima reazione, orzare un poco di bolina; tenere la barca piatta; cos'è la scuffia; come si raddrizza una deriva nella realtà (sulla lama) |

### Banca della 0.20 e concetti per la 0.20.1 e seguenti **[deciso, 10 ottobre 2026]**

La 0.20 ha la **banca minima**: 26 domande (L1 5, L2 4, L3 5, L4 4, L5 4, L6 4), una per concetto, sui concetti più centrali che il ripasso non chiede già. Testo, passo e riga di ciascuna in `CONTENUTI-DA-VERIFICARE.md`, sezione «Domande dell'esame (0.20)». Il meccanismo funziona con qualunque numero di domande per lezione, purché sia almeno la quota più una (`tests/collaudo_esame.py` lo prova anche con la lezione 2 a 7 domande).

Concetti insegnati e verificabili con risposta chiusa, **ancora senza domanda**: la banca cresce da qui, una lezione alla volta. Valgono le stesse regole (nessuna cifra, parole vietate, niente dubbi specifici né testi solo del pannello o del glossario).

| Lezione | Concetti (passo) |
| --- | --- |
| 1 | deriva come barca (La barca); prua e poppa (La barca); albero, boma, randa e scotta (Albero, boma, randa); timone e barra, lama di deriva (Timone e deriva); il vento si nomina da dove arriva (Il vento); definizione di sopravento e sottovento (Sopravento e sottovento); orzare (Orzare e l'angolo morto); orzare e poggiare riferiti al vento, con la prua nel vento si poggia da tutti e due i lati (Ripartire); la vela troppo aperta fileggia (La scotta: lascare); regola pratica della scotta (La scotta: cazzare); la vela troppo cazzata va in stallo (Troppo cazzata) |
| 2 | piccole correzioni presto invece che grandi tardi (Tenere la rotta) |
| 3 | definizione di andatura (Le andature); bolina più vicina al vento, bolina stretta e larga (Bolina); traverso (Traverso); lasco e gran lasco (Lasco e gran lasco); oltre la poppa si stramba (Poppa); nome delle mure (Le mure); filetti dritti, filetto sopravento (I filetti); orzi e cazzi (Orzi e cazzi) |
| 4 | definizione del vento apparente (Il vento che senti a bordo); il segnavento indica l'apparente (Il vento che senti a bordo); accelerando bisogna cazzare (Accelerando); in poppa l'apparente è più debole (In poppa) |
| 5 | due manovre per cambiare mure, virata, si vira per risalire e si stramba col vento da dietro (Cambiare mure); per virare barra sottovento con decisione, in bolina la vela resta cazzata su tutte e due le mure (Virare); la barca si pianta, all'indietro la barra va al contrario (Una virata che non riesce); bordeggiare e bordo, risalire allunga la strada (Risalire il vento); strambata involontaria (Strambata violenta); strambata controllata (La strambata, Strambata controllata) |
| 6 | la raffica arriva da sopravento, in raffica il vento gira, il timoniere si sporge (Raffiche e sbandamento); lascare in raffica, di bolina orzare un poco (Assorbire una raffica); scuffiare = rovesciarsi (La scuffia); raddrizzare sulla lama (Raddrizzare) |

---

## 6. Decisioni di Ale (9 ottobre 2026)

Sostituiscono le alternative della prima stesura.

| Tema | Decisione |
| --- | --- |
| Gioco libero e carriera | Il gioco libero è il banco di prova, il vero gioco è la carriera. Attestato, brevetto e libretto solo in carriera. Nel gioco libero l'esame si fa come prova, senza conseguenze salvate. |
| Aiuti in carriera (decisione 8) | **Opzione A: tutti gli aiuti e le impostazioni contano per i meriti.** Da riesaminare dopo la lettura del codice (controllo 2) e dopo qualche partita. |
| Banca delle domande (decisione 9 e «quante all'inizio») | Una domanda per ogni concetto che una lezione insegna davvero e che si verifica con risposta chiusa; nessun obiettivo numerico; minimo quota + 1 per lezione (L1 5, L2 4, L3 5, L4 4, L5 4, L6 4); ogni domanda porta il suo passo; una domanda senza passo si toglie, oppure Ale decide di aggiungere il passo; le 29 del ripasso restano separate. |
| Natura dell'esame | Verifica interna al gioco: niente da studiare fuori dalle lezioni. |
| Attestato | Breve scena nel passaggio da un livello all'altro, in carriera; stampabile con `window.print()`; scritta «nessun valore legale»; nel gioco libero non compare. |
| Spiegazione delle sbagliate | Solo alla fine dell'esame. |
| Dove sta l'esame | Riquadro nel menu, vicino ai ripassi. |
| Un solo esame | Un solo esame per tutti, stesse domande e stessa soglia 16/20. «Esperti» indica solo il livello degli avversari, come opzione delle regate nel gioco libero. |

**Sugli aiuti, dopo il controllo 2:** «girano la prua» è solo un'altra corrispondenza fra frecce e barra, non un pilota. Gli altri aiuti danno informazioni (suggerimenti, frecce, rosa, strumenti, fantasma) oppure riportano la barra al centro. Nel codice non c'è niente che guidi la barca al posto del giocatore. Questo è un argomento in più per l'opzione A, ma la conferma la danno le partite.

### Decisione 4: ordine in carriera **[deciso]**

**Tutto in parallelo, in qualsiasi ordine.** In carriera lezioni, regate ed esame sono sempre aperti. Il gioco suggerisce un ordine (lezioni, regate, esame) ma non lo impone e non blocca nulla. Il livello è superato quando:

- tutte le soglie dei meriti sono raggiunte;
- l'esame è superato;
- i ruoli del livello sono sufficienti (al livello 1 il ruolo è uno solo).

Motivo: la Competizione si guadagna con le regate, quindi le regate non possono dipendere dal brevetto né dall'esame.

### Ultime quattro scelte, chiuse da Ale

| Scelta | Decisione |
| --- | --- |
| Bivio | **Sì**: un selettore nell'intestazione del menu, senza schermata all'avvio (§3). |
| Punti in Competizione | **Sì, stessi punti con principianti ed esperti** (§4). Precisazione: nell'esame non esistono principianti ed esperti; il livello degli avversari riguarda solo le regate (vedi l'avvertenza della fetta 0.21, §7). |
| Nome del brevetto | **Sì: «Timoniere di deriva».** |
| Passo nuovo nella lezione 3 sulla regola delle stesse mure | **No.** I testi delle lezioni del livello 1 sono chiusi e non si modificano per la 1.0. Nessuna domanda d'esame su questa regola: nel gioco resta solo nel messaggio di contatto delle regate. Vedi «Dopo la 1.0» (§9). |

---

## 7. Fette di lavoro, in ordine

Ogni fetta è una versione giocabile e chiusa, con `VERSIONE` e `CHANGELOG.md` aggiornati. Per ognuna si lanciano sempre `polare.js` e `raffiche_e_virate.js` (identici carattere per carattere): nessuna fetta tocca la fisica. A fine fetta, `tests/lancia_tutti.sh --veloce` sul PC di Ale.

| # | Versione | Contenuto | Collaudo |
| --- | --- | --- | --- |
| 1 | 0.20 | **Esame nel gioco libero, come prova.** Banca `ESAME`, estrazione per quote, pulsante del menu acceso, spiegazioni solo alla fine con le sbagliate per lezione, «Rifai l'esame», nessun salvataggio. | Nuovo `collaudo_esame.py`. **Banca:** ogni domanda ha la lezione e un passo che esiste, ogni lezione ha almeno quota + 1 domande (fallisce sotto), 3 sbagliate diverse dalla giusta, nessun testo uguale al `QUIZ`, giusta più lunga al massimo nel 30%. **Nessuna spiegazione prima della fine. Nessuna scrittura nel salvataggio** (`localStorage` identico prima e dopo). **Estrazione:** 500 estrazioni a seme fisso, sempre 20 domande diverse con le quote giuste, ogni domanda della banca estratta almeno una volta. **Soglia:** 15 giuste = non superato, 16 = superato, 20 e 0 agli estremi. **Dialogo:** 20 sbagliate a 1360×650 e 1360×768 con i caratteri veri (sul PC). **Pagina senza `#collaudo`:** il pulsante è acceso e apre l'esame. Più `collaudo_quiz.py`, perché `openQuiz` cambia. Non c'è barca da guidare: lo dico invece di inventare un collaudo finto. |
| 2 | 0.21 | **Piazzamento salvato e taratura della Competizione.** `progress.race`; pilota sostituto esposto in `__sv`. **Avvertenza:** oggi il livello degli avversari (principianti / esperti / nessuno) non viene salvato nei risultati, e il record della regata ha la stessa chiave per tutti e tre (controllo 3). Prima di usare il piazzamento per i meriti, in carriera il livello degli avversari deve essere fisso **oppure** entrare nel risultato salvato. Quale delle due è da decidere. | Nuovo `collaudo_competizione.py`: le 160 regate del §4 con le soglie C0-C5, **guidando davvero la barca del giocatore**. Pagina senza `#collaudo`: una regata finita con avversari salva il piazzamento, con «nessuno» no. Se C0 fallisce, la fetta si ferma qui e si riporta. |
| 3 | 0.22 (fatta) | **Bivio e salvataggio di carriera.** `STORE` variabile, selettore nel menu, «Azzera» solo sulla modalità corrente. | Pagina senza `#collaudo`: in carriera il pilota di `collaudo_fasce.py` completa la prova 1, e la chiave del gioco libero resta **identica byte per byte**; poi il contrario. Ricaricando, la modalità è ricordata. Un ripasso in carriera non tocca il record del libero. Menu a 1360×650 senza eccesso. |
| 4 | 0.23 (fatta) | **Libretto.** `meriti(progress)`, quattro barre, riga «cosa manca» per superare il livello. Il pulsante dell'esame non dipende dai meriti. | `meriti()` sui giocatori A-D del §4 e sui casi al bordo (minimo esatto, minimo meno 1, «nessuno» escluso), con l'esame superato e non: «livello superato» solo con tutte le condizioni. Nel browser: salvataggi di carriera preparati, poi lettura delle barre e della riga; **pulsante dell'esame acceso anche con meriti a zero**. Menu a 1360×650 e 1360×768 senza eccesso, con i caratteri veri. |
| 5 | 0.24 (fatta) | **Esame in carriera, ripasso mirato, scena dell'attestato.** | Percorso in pagina senza `#collaudo`. Con una carriera vuota: pulsante acceso, esame superato, **nessuna scena** (mancano i meriti); poi meriti completati, la scena compare. Con una carriera dai meriti a posto: esame sbagliato apposta, pulsante spento, ripassi delle lezioni sbagliate al 100% e, a parte, a 75% (resta spento), pulsante acceso, esame superato, scena dell'attestato con «nessun valore legale» e senza «patente», stampa provata con `emulate_media("print")` e schermata. Nel gioco libero lo stesso esame superato **non** mostra l'attestato e il pulsante non si spegne mai. |
| 6 | 1.0 (fatta) | **Rilascio.** Manuale (sezione meriti ed esame), documenti, `CHANGELOG.md`. | Una carriera da zero **guidata davvero**: le lezioni con `collaudo_lezioni.py`, le prove con il pilota delle fasce, le due regate con il sostituto, i ripassi e l'esame risposti; il libretto deve arrivare al brevetto. È lungo: lo lancia Ale sul PC. Poi una partita a mano di Ale. |

Le fette 1 e 2 sono indipendenti e si possono scambiare. La 3 viene prima di 4 e 5.

**Esito della fetta 2 (0.21, 12 ottobre 2026).** Strada B minima, piazzamento definitivo (salvato quando nessuno può più superarlo), il migliore per punti per ogni chiave. Il sostituto guida davvero la barca del giocatore: C0-C5 tutti dentro le soglie sui semi 1-40 e sui semi di conferma 41-80 (numeri in `CHANGELOG.md`, 0.21). **Avvertenze:** il sostituto non ha mai finito una regata pulita (0 su 320), quindi il «+1 senza errori» non è misurato, C2 e C3 sono stime prudenti senza bonus e C4 non ha misurato niente. Pagina senza `#collaudo`: con avversari il piazzamento si salva; con «nessuno» il pilota da tastiera non è arrivato in fondo (NON VALIDO), quindi quella parte la prova Ale a mano.

### Dentro e fuori dalla 1.0

| Dentro la 1.0 | Fuori dalla 1.0 |
| --- | --- |
| Lezioni e quiz già esistenti | Istruttore completo con replay e confronto (resta solo il registro degli errori già esistente) |
| Regate singole con avversari, già esistenti | Crescita della bravura dei personaggi |
| Meriti in forma minima: una barra per area e una riga «cosa manca» | Tornei |
| Esame | Livelli 2-6 |
| Brevetto | |
| Attestato come scena al passaggio di livello | |

---

## 8. Rischi e cosa NON fare adesso

### Rischi

- **Banca minima e memoria.** Con 26 domande, due esami di seguito hanno in media circa 15 domande in comune su 20 (§4). La banca cresce con i concetti, non con un obiettivo numerico: se le lezioni non ne offrono di più, il numero resta questo.
- **Contenuti non verificati.** L'esame trasforma in «risposta giusta» contenuti che in `CONTENUTI-DA-VERIFICARE.md` hanno quasi tutti l'esito vuoto. Mitigazione: fuori i «Dubbi specifici» e i numeri del motore; ogni domanda annotata con il suo passo, così una correzione della lezione trova subito la domanda da correggere. L'attestato non va mostrato a nessuno come prova di competenza, e lo dice.
- **Un `progress` per due modalità.** Se si cambia modalità mentre si gioca, un risultato può finire nel salvataggio sbagliato. Mitigazione: il cambio si fa solo dal menu, e il collaudo della fetta 3 controlla byte per byte.
- **Il sostituto non è un giocatore.** La Competizione si tara su un principiante del computer. Se il sostituto non riesce a guidare la barca del giocatore, la fetta 2 si ferma e si ripiega su una scala dichiarata, senza misura.
- **La riga dei punti spinge a ottimizzare.** Ripetere le regate finché esce un 1° posto pulito è possibile: è tempo di gioco, non un difetto. Conta solo il migliore per regata.
- **Spazio a schermo.** Libretto nel menu ed esame con 20 sbagliate: il margine a 1360×650 si misura con i caratteri veri, cioè sul PC di Ale.
- **Salvataggio nel browser.** Se si cancellano i dati del sito, la carriera sparisce. Va detto nel manuale. Niente esportazione nella 1.0.
- **Stampa.** L'aspetto stampato cambia da un browser all'altro: si collauda l'emulazione, l'aspetto lo giudica Ale.

### Cosa NON fare adesso

- Niente diario, importazione dal gioco libero, tornei o mini tornei, brevetti progressivi, istruttore.
- Niente domande su precedenze e regole di regata, niente domande con disegno, niente numeri del motore nelle domande.
- Niente penalità per errori gravi nei meriti (piano §5): restano [proposta] per dopo la 1.0.
- Niente sblocchi: né nel gioco libero né, al livello 1, in carriera.
- Non toccare fisica, fasce di tempo, avversari, regate, le 29 domande del ripasso.
- Niente testo nuovo a video oltre a riga «cosa manca», esito dell'esame e attestato: le regole vanno nel manuale.
- Nessun nuovo documento di progettazione finché la fetta 1 non è giocabile.

---

## 9. Dopo la 1.0

- **Regola delle stesse mure («lascia strada chi è sopravento»).** Oggi non è insegnata in nessuna lezione: compare solo nel messaggio di contatto delle regate (`index.html`, righe 1766-1767, in `contacts()`), e in `CONTENUTI-DA-VERIFICARE.md`. Per la 1.0 non si aggiunge un passo alla lezione 3, perché i testi delle lezioni del livello 1 sono chiusi (restano da fare esame, brevetto e libretto; i tornei sono fuori dalla 1.0). Per lo stesso motivo nessuna domanda d'esame la usa. Da riprendere quando si toccheranno le lezioni o le regate, insieme alle regole 10, 11, 14, 18, i cui titoli restano **[da verificare]**.

---

## 10. Da confermare all'avvio della fetta 0.20

- Righe 208-209, «Fuori anche»: niente domande sui dubbi specifici di `CONTENUTI-DA-VERIFICARE.md` e niente numeri del motore.
- Riga 274, fetta 0.21: livello degli avversari in carriera fisso, oppure salvato nel risultato.
- Marcature [proposta] di Banca, Estrazione e Salvataggio (§2), pilota sostituto (riga 173) e verifica a mano dell'esame (riga 194): dettagli di realizzazione, da approvare con il via alla fetta 0.20.

**Esito (10 ottobre 2026, avvio della 0.20).** «Fuori anche» confermato e reso controllabile: nessuna cifra nei testi dell'esame; parole vietate «lascia strada», «lasciare strada», «precedenz», «abbattuta», «Viro», «Strambo», «orzier», «scader», «rosso», «verde» («strada» da sola è ammessa); fuori anche i testi che stanno solo nei messaggi del pannello o nel glossario e i tasti del gioco. Lo controlla `tests/collaudo_esame.py`. Il livello degli avversari non tocca la 0.20 e resta da decidere alla 0.21. Banca, estrazione e salvataggio come al §2, con la banca raggruppata per lezione (`ESAME[lezione] = [[passo, domanda, giusta, [sbagliate], spiegazione], …]`) e nessun salvataggio nel gioco libero. Durante l'esame nessun colore e nessuna spiegazione, risposta non modificabile; alla fine, accanto a ogni sbagliata, la riga «dal passo «…»».

---

## 11. Fetta 3 (0.22): bivio e salvataggio di carriera — proposta di dettaglio

Del 14 ottobre 2026. **Fermata 1: nessun codice.** Righe di `index.html` lette oggi (0.21.6).

### Cosa c'è oggi [codice]

- `STORE = "scuolaVelaSim.v1"` è una costante (938); `progress` si carica una volta all'avvio (952) e `saveProgress()` lo scrive sempre lì (953). Lezioni (1221), prove (1499-1500), ripassi (1062), regate (1898-1911) scrivono solo in `progress`.
- I fantasmi stanno in `GHOST_STORE = "scuolaVelaGhost.v1"` (1515-1518). `recSave()` (1532) scrive il fantasma **solo quando il tempo batte il record di `progress.best`** (1499, 1898).
- «Azzera i progressi» (1007) svuota `progress` e lo salva; **i fantasmi non si toccano** (comportamento di oggi).
- Le impostazioni (`opt`) non si salvano: non riguardano questa fetta.

### Il modello più semplice

1. `STORE` diventa `let`: `"scuolaVelaSim.v1"` in gioco libero, `"scuolaVelaCarriera.v1"` in carriera. La modalità sta in `scuolaVelaModo` (`"libero"` / `"carriera"`); se manca o il browser non salva, si parte in gioco libero.
2. **Selettore** nell'intestazione del menu, accanto a «Glossario», con lo stile `.seg` che esiste già: **Gioco libero | Carriera**. Esiste solo nel menu, quindi non si cambia modalità a metà di una prova.
3. **Al cambio:** `saveProgress()`, poi si cambia chiave, si ricarica `progress` dalla chiave nuova (vuoto se non c'è), si ricaricano i fantasmi della modalità (punto 5), si scrive `scuolaVelaModo`, si ridisegna il menu. Nessun'altra riga del gioco cambia.
4. **«Azzera i progressi»** svuota solo la modalità in uso, e lo dice: «Azzerare i progressi della carriera? Il gioco libero non cambia.» (e il contrario). I fantasmi restano come oggi.
5. **Fantasmi separati per modalità** — cambia una riga [proposta] del §2, che li voleva in comune. Motivo [codice]: il fantasma si scrive a ogni record della modalità in uso, quindi la prima regata in carriera (record vuoto) sovrascriverebbe il fantasma del gioco libero anche se più lento del record libero. In carriera si usa `scuolaVelaGhostCarriera.v1`; il gioco libero resta su `scuolaVelaGhost.v1`.
6. La pulizia delle chiavi vecchie della 0.19 (1519) resta com'è: gira sulla modalità caricata all'avvio. Chi ha dati di prima della 0.19 non ha ancora `scuolaVelaModo`, quindi parte in gioco libero e la pulizia avviene dove serve.
7. In carriera il menu è identico a quello del gioco libero (§3): niente libretto, niente esame salvato, niente attestato. Arrivano nelle fette 4 e 5.

Costanti nuove: nessuna. Chiavi nuove: tre (`scuolaVelaCarriera.v1`, `scuolaVelaModo`, `scuolaVelaGhostCarriera.v1`).

### Collaudo: nuovo `tests/collaudo_carriera.py` [proposta]

Criteri scritti adesso, prima del codice. Ogni corsa in un contesto nuovo del browser (salvataggio vuoto), passi fissi e seme fisso dove c'è la barca. La modalità si cambia **sempre cliccando il selettore**, mai dall'aggancio.

- **K1, prova 1 in carriera** (pagina con `#collaudo`, perché il pilota di `collaudo_fasce.py` usa `__sv.run`; il §7 diceva «senza `#collaudo`», ma quel pilota lì non può girare): si prepara un gioco libero con un record della prova 1 e un fantasma; si passa in carriera e il pilota completa la prova 1. Atteso: `scuolaVelaSim.v1` e `scuolaVelaGhost.v1` **identici byte per byte** a prima; `scuolaVelaCarriera.v1` contiene `done.m0` e `best["m0.2"]`; `scuolaVelaGhostCarriera.v1` contiene il fantasma. Poi il contrario (record in carriera, prova in gioco libero). Semi 1-3 per ognuno dei due versi: 6 corse.
- **Controllo del metro:** l'identità byte per byte vale solo se nella stessa corsa la chiave della modalità in uso **è cambiata davvero**. Se il pilota non arriva, la corsa è NON VALIDA, non OK.
- **K2, ripasso in carriera** (pagina **senza** `#collaudo`, come la carica un giocatore, solo clic): gioco libero con il ripasso della lezione 1 a un punteggio noto; in carriera si fa il ripasso della lezione 1. Atteso: `quiz.q0` del gioco libero invariato, quello della carriera scritto.
- **K3, ricaricando la modalità resta** (senza `#collaudo`): in carriera, ricarica, selettore su «Carriera» e menu con i dati della carriera; idem in gioco libero.
- **K4, «Azzera»** (senza `#collaudo`): in carriera con dati in tutte e due le chiavi, «Azzera» con conferma accettata: la carriera è vuota e il gioco libero è identico byte per byte; poi il contrario. Il testo della conferma nomina la modalità.
- **K5, primo avvio:** senza nessuna chiave si parte in gioco libero e il menu è uguale a quello della 0.21.6 tolto il selettore (stessi riquadri e stesse voci).
- **Menu a 1360×650 senza pixel di eccesso**, con il selettore: si misura con la parte del menu di `collaudo_esame.py`. Nella sandbox mancano i caratteri veri, quindi la misura valida è quella sul PC di Ale.
- **Non-regressione:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere (la fetta non tocca `step()`); `collaudo_versione.py`.

### Rischi

- **Due fantasmi:** un giocatore che ha già fantasmi nel gioco libero non li ritrova in carriera. È voluto (la carriera parte vuota, §2).
- **Dimenticare un punto che scrive** nel salvataggio: oggi passano tutti da `progress`/`saveProgress()` e `ghosts`/`saveGhosts()` (verificato con `grep localStorage`: 4 righe, tutte in questi due punti). Una scrittura nuova scritta fuori da lì sfuggirebbe al bivio; K1 e K2 lo coprono solo per prove e ripassi, non per regate e lezioni (coperte dal codice comune, non da una corsa).
- **Spazio nell'intestazione del menu:** il selettore può far andare a capo il sottotitolo. Si vede solo con i caratteri veri.

### Decisioni per Ale

1. **Fantasmi separati** (punto 5) invece che in comune come diceva il §2. **Deciso da Ale (14 ottobre 2026): separati.**
2. **«Azzera» lascia i fantasmi**, come oggi. Consiglio: lasciarlo così in questa fetta; se si vuole che li cancelli, cambia anche il gioco libero e va detto nel `CHANGELOG.md`. **Ale (14 ottobre 2026): cancellare non è un problema, siamo in fase di prova.** Scelta fatta: «Azzera» cancella anche i fantasmi della modalità in uso (vale anche per il gioco libero).
3. **K1 con `#collaudo`** invece che senza, per il motivo detto sopra. **Approvato da Ale (14 ottobre 2026).**

**Esito (0.22, 14 ottobre 2026).** Fatto come proposto, con «Azzera» che cancella anche i fantasmi della modalità in uso. Un cambio rispetto al punto 3: al cambio di modalità **non** si chiama `saveProgress()`, perché ogni risultato è già salvato quando nasce; il collaudo ha mostrato che quella scrittura riscriveva la modalità lasciata (stesso contenuto, byte diversi). `collaudo_carriera.py`: 57 controlli, 0 falliti, 6 corse K1 valide su 6. Numeri e limiti in `CHANGELOG.md`, 0.22.

---

## 12. Fetta 4 (0.23): libretto — proposta di dettaglio

Del 14 ottobre 2026. **Fermata 1: nessun codice.** Righe di `index.html` della 0.22.

### Da dove si leggono i meriti [codice]

Tutto c'è già in `progress`; la fetta **non scrive niente di nuovo** nel salvataggio.

| Area | Dato | Righe |
| --- | --- | --- |
| Abilità | `progress.best[recK("m"+i)]` → fascia con `medalOf(i, sec)` (oro 3, argento 2, bronzo 1); `progress.clean[recK("m"+i)]` → +1 | 950-951, 1514 |
| Conoscenza | `progress.quiz["q"+i]` (migliore ripasso completo) su `QUIZ[i].length` | 1062 |
| Competizione | `progress.race[recK("r"+i)+":principianti"]` e `…":esperti"` = `{ pos, n, pulita }`; per regata il migliore dei due | 1911-1917 |
| Esperienza | `progress.done["l"+i]` | 1236 |
| Esame | `progress.exam?.superato`: **nessuno lo scrive fino alla fetta 5**, quindi nella 0.23 l'ultima riga è sempre «Manca l'esame» | — |

### Il modello più semplice

1. **`meriti(progress)`, funzione pura**, con la tabella del §4 [provvisorio, scritta il 9 ottobre prima di ogni misura] come unica costante `MERITI`:
   - Abilità: per ogni prova `medalOf` + 1 se pulita; massimo 20, minimo 8.
   - Conoscenza: per ogni ripasso 2 punti se `punti·5 ≥ domande·4` (80%), 1 se `punti·5 ≥ domande·3` (60%); conti interi per non sbagliare sui decimali; massimo 12, minimo 6.
   - Competizione: per ogni regata il migliore fra principianti ed esperti, `5 − pos` (+1 se pulita), solo con `n = 4`; le chiavi con «nessuno» non esistono, e comunque si leggono solo le due chiavi con il livello; massimo 10, minimo 3.
   - Esperienza: lezioni completate; massimo 6, minimo 6.
   - Totale: massimo 48, minimo 29.
   - Restituisce `{ aree, totale, superato, manca }`.
2. **Riga «cosa manca»**, una sola, in quest'ordine: l'area sotto il minimo con **più punti mancanti** (a parità, l'ordine della tabella: scelta nostra, il §3 diceva «più lontana» senza definirla), poi il totale, poi l'esame. Testi:
   - Abilità: «Manca N punto/i in Abilità: migliora i tempi delle prove o completane una senza errori.»
   - Conoscenza: «… in Conoscenza: porta un ripasso almeno all'80%.»
   - Competizione: «… in Competizione: arriva in fondo a una regata con gli avversari.»
   - Esperienza: «… in Esperienza: completa le lezioni che mancano (Lezione 3, Lezione 5).»
   - Totale: «Mancano N punti al totale: migliora una qualsiasi area.»
   - Esame: «Manca l'esame.»
   - Tutto fatto: «Livello 1 superato.» (la scena dell'attestato è della fetta 5).
3. **Libretto nel menu, solo in carriera:** nel terzo riquadro, al posto di «In arrivo» (che resta nel gioco libero). Quattro righe compatte «Abilità ▬▬▬│▬▬ 12 / 20» con una tacca al minimo e il minimo nel `title`, poi «Totale 31 / 48 (minimo 29)», poi la riga «cosa manca». Niente spiegazioni delle regole a video: vanno nel manuale (§3).
4. **Il pulsante dell'esame non cambia**: acceso sempre, anche con meriti a zero.

Costanti nuove: la tabella `MERITI` (punti, massimi, minimi del §4), **ipotesi provvisorie**, da tarare giocando. Nessun'altra.

### Spazio a 1360×650 [misura, sandbox, caratteri di riserva]

Oggi: riquadro Scuola 454 px (il più alto), terzo riquadro 367 px, piede del menu che finisce a 582 px su 650. Il libretto può crescere di circa 87 px senza superare il riquadro Scuola, e di altri 68 px prima del bordo. Togliendo «In arrivo» si recuperano circa 50 px. Il libretto stimato è circa 150 px: **ci sta, ma di poco**. Con i caratteri veri il riquadro Scuola è 464,5 px: la misura valida è sul PC di Ale.

### Collaudo: nuovo `tests/collaudo_libretto.py` [proposta]

Criteri scritti adesso, prima del codice.

- **L1, giocatori del §4.** Per A, B, C e D si prepara un `progress` costruito **dalle regole scritte, non dal codice**: i tempi presi dalle fasce lette nel testo di `index.html` (per esempio argento = il tempo massimo dell'argento), i ripassi con punteggi scelti, i piazzamenti con `{ pos, n: 4, pulita }`. Atteso: i numeri della tabella degli esempi (A 12/8/5/6 = 31, B 20/12/0/6 = 38, C 14/10/6/3 = 33, D 6/6/3/6 = 21) e la riga «cosa manca» prevista: A «Manca l'esame»; B Competizione; C Esperienza, con le tre lezioni nominate; D Abilità.
- **L2, casi al bordo:** ogni area al minimo esatto e al minimo meno 1; totale a 29 e a 28 con tutte le aree a posto; ripasso di 4 domande a 3 su 4 (1 punto) e a 4 su 4 (2 punti); ripasso di 5 o 6 domande al 60% e all'80% esatti; una regata solo con «esperti» e una con tutti e due i livelli (conta il migliore); una chiave «nessuno» preparata a mano, che non deve contare; `progress` vuoto (tutto a zero, riga = l'area con più punti mancanti, cioè Abilità: 8). Con l'esame superato e senza: «Livello 1 superato» **solo** con tutte le condizioni.
- **Controllo del metro:** il collaudo stampa quanti casi ha verificato per ogni parte e fallisce se una parte ne ha zero; almeno un caso per area deve dare un numero **diverso da zero** e uno **diverso dal massimo**.
- **L3, nel browser senza `#collaudo`:** salvataggi di carriera preparati in `localStorage` (A e D), menu caricato come un giocatore: si leggono dal DOM i numeri delle quattro barre, il totale e la riga, e devono coincidere con L1. Nel gioco libero il libretto **non** c'è e «In arrivo» sì. Il pulsante dell'esame è acceso anche con la carriera vuota.
- **L4, spazio:** menu in carriera con il libretto a 1360×650 e 1360×768, **0 px di eccesso** e il piede del menu dentro la finestra; nel caso peggiore (riga «cosa manca» più lunga, quella di Esperienza con sei lezioni). Valida solo con i caratteri veri (PC di Ale).
- **Non-regressione:** `polare.js`, `raffiche_e_virate.js` identici carattere per carattere; `collaudo_carriera.py`, `collaudo_esame.py`, `collaudo_versione.py`.

`meriti()` si raggiunge dal collaudo tramite `__sv` (solo con `#collaudo`) per L1 e L2; L3 non usa l'aggancio.

### Rischi

- **Spazio:** se non ci sta a 1360×650, si toglie prima il totale come riga a sé (va nel titolo del libretto), poi si accorciano le etichette. Non si toccano gli altri riquadri.
- **I numeri del §4 sono provvisori:** scritti prima di qualsiasi partita in carriera. La Competizione è misurata (0.21), le altre aree no. Si tarano giocando, dichiarando ogni cambio.
- **Prova 5:** il pilota delle fasce la finisce 19 volte su 24 (PC di Ale); l'oro lì è di misura. Riportato, non è un difetto del libretto.
- **Il libretto riconosce le prove dalle chiavi di oggi** (`m0.2` … `m4.4`). Se un giorno cambia un percorso e la sua chiave, quella prova torna a zero anche in carriera: è la regola già in uso per i record.

### Decisioni per Ale

1. Libretto **al posto di «In arrivo»** in carriera (consiglio: sì, per lo spazio).
2. Riga «cosa manca»: a parità di punti mancanti, l'ordine della tabella (Abilità, Conoscenza, Competizione, Esperienza). Consiglio: sì.
3. Testi delle righe «cosa manca» come sopra: si possono cambiare adesso, prima del codice.

### Risposte di Ale (14 ottobre 2026)

1. Libretto al posto di «In arrivo» in carriera: **sì**.
2. Ordine a parità di punti mancanti: Ale non ha preferenze; resta l'ordine della tabella (scelta nostra).
3. Testi della riga «cosa manca»: da rivedere quando Ale li vede nel gioco.
4. **Nuova richiesta, che ferma la fetta 4 finché non è decisa: due registri separati.**
   - **Classifica** delle regate e dei tornei: solo i punti del regolamento (sistema del punteggio minimo, Appendice A: 1 punto al primo, 2 al secondo e così via; vince chi ne ha meno). Nessun bonus.
   - **Meriti** (libretto): un registro a parte. Il «+1 senza errori» non deve mai cambiare un piazzamento: oggi, nei meriti, un 3° posto senza errori vale quanto un 2° con errori (osservazione 31), e Ale lo legge come un 2° posto a pari merito.
   - Da decidere quali punti si danno in ogni fase (lezioni, prove, ripassi, esame, regate, tornei, errori) e se le regate e le prove giocate in carriera contano tutte. Riepilogo dello stato e domande nel rapporto del 14 ottobre; le decisioni si scrivono qui.

### Decisioni di Ale sui punti (14 ottobre 2026)

- **Classifica e meriti separati.** La classifica usa solo i punti del regolamento (punteggio minimo, Appendice A: 1 al primo, 2 al secondo…, vince chi ne ha meno); oggi la classifica a punti non c'è, perché le regate sono singole: entra con i tornei, dopo la 1.0.
- **Competizione nei meriti: solo il piazzamento.** Il «+1 senza errori» si toglie.
- **«Senza errori» nelle regate:** resta la ★; nel libretto un conteggio a parte, «Regate senza errori: N su 2», **senza punti**.
- **Errori in generale:** per ora contano solo per la «senza errori» (★ e +1 nelle prove). Il livello 1 non deve essere troppo punitivo.

### Tabella dei meriti dalla 0.23 [provvisoria, da tarare giocando]

| Area | Punti | Massimo | Minimo |
| --- | --- | --- | --- |
| Abilità | 5 prove: bronzo 1, argento 2, oro 3, +1 se completata almeno una volta senza errori | 20 | 8 |
| Conoscenza | 6 ripassi: 2 punti se il migliore è almeno l'80%, 1 se almeno il 60% | 12 | 6 |
| Competizione | 2 regate, solo con avversari; per ogni regata il piazzamento migliore: 1° = 4, 2° = 3, 3° = 2, 4° = 1 | **8** | 3 |
| Esperienza | 1 punto per lezione completata | 6 | 6 |
| Totale | somma dei minimi 23 | **46** | 29 |

- **Minimo di Competizione invariato (3):** un 3° e un 4° posto, oppure un 2° posto e l'altra regata non finita. Due ultimi posti fanno 2: non bastano. Le misure C2 e C3 della 0.21 restano valide così come sono, perché il sostituto non ha mai finito una regata pulita: il bonus non era mai entrato nei conti.
- **C4 cambia significato:** il massimo è ora 8 (due primi posti). La soglia resta quella scritta allora (al massimo il 10% delle coppie); va rimisurata con `collaudo_competizione.py` aggiornato, nella fetta 4.
- **Esempi ricalcolati:** A (due 3° posti) 12 + 8 + 4 + 6 = 30, meriti a posto, manca l'esame. B 20 + 12 + 0 + 6 = 38, manca Competizione. C (un 1° e un 3° posto) 14 + 10 + 6 + 3 = 33, manca Esperienza. D (due ultimi posti) 6 + 6 + 2 + 6 = 20: mancano Abilità (2 punti), Competizione (1 punto) e totale; la riga dice Abilità. L1 del collaudo usa questi numeri.

### Esame in carriera: un voto solo (Ale, 14 ottobre 2026, per la fetta 5)

«Il test scritto non è realistico poterlo rifare: quando ti promuovono hai un voto e finisce lì.» Quindi, in carriera, **un esame superato è definitivo**: il voto resta quello e l'esame non si rifà per migliorarlo. Cambia il §3 («Rifai l'esame» resta solo nel gioco libero). Da confermare all'avvio della fetta 5: dopo un esame **non** superato resta la strada del §3 (ripasso mirato delle lezioni sbagliate, poi si riprova).

**Esito della fetta 4 (0.23, 14 ottobre 2026).** Fatta come nel §12, con la tabella dei meriti dalla 0.23. Una correzione per lo spazio: la riga di Esperienza dice «completa le lezioni 1, 2… e 6» invece dei nomi «Lezione N». Numeri in `CHANGELOG.md`, 0.23.

### Revisione del libretto dopo la prova di Ale (14 ottobre 2026) [fatta nella 0.23]

Prova di Ale, carriera con una sola prova fatta: la riga diceva «Mancano 6 punti in Conoscenza…» quando mancava quasi tutto, e la tacca rossa del minimo sembrava un indicatore di avanzamento (in Esperienza stava in fondo, con 0 / 6).

- **Ordine libero confermato** (Decisione 4 del 9 ottobre): niente sblocchi. Ale: le regate servono anche da allenamento mentre si impara, per non annoiarsi.
- **Barre:** via la tacca; accanto al numero «servono N», in rosso finché non si raggiunge, poi in verde. La barra a riempimento resta (Ale: «più bella e comprensibile»).
- **Due righe al posto di una:**
  1. cosa manca, tutto insieme: «Ti mancano punti in Abilità, Conoscenza, Competizione ed Esperienza; poi l'esame.» (solo le aree sotto il minimo; poi il totale; poi l'esame);
  2. **«Cosa potresti fare adesso: …»**, un suggerimento concreto che **cambia a ogni ritorno al menu**, girando fra le aree che mancano. Per ogni area una voce precisa: Esperienza → la prima lezione non completata nell'ordine della Scuola; Abilità → la prima prova senza fascia, altrimenti la prima non in oro; Conoscenza → il primo ripasso sotto l'80%; Competizione → la regata con meno punti. Con tutte le aree a posto e il totale sotto 29, si gira fra le aree non al massimo; poi l'esame. Il giro si conta in memoria, non si salva: alla riapertura del gioco riparte dalla prima area che manca, nell'ordine della tabella.
- Collaudo: L1-L3 si aggiornano con i testi nuovi; il giro del suggerimento si prova aprendo il menu più volte (ogni area che manca deve comparire almeno una volta in tanti giri quante sono le aree); L4 si rimisura con le due righe.

**Esito della revisione.** Fatta come scritta. Due cambi per lo spazio a 1360×650: il suggerimento delle regate è «la Regata a bastone (con avversari).» e le righe del libretto sono un po' più strette. «Ti manca 1 punto» al singolare. Nella sandbox il caso peggiore (Competizione) lascia il piede del menu proprio al limite: la misura valida è sul PC di Ale.

---

## 13. Fetta 5 (0.24): esame in carriera, ripasso mirato, attestato — proposta di dettaglio

Del 14 ottobre 2026. **Fermata 1: nessun codice.** Righe di `index.html` della 0.23.

### Cosa c'è oggi [codice]

- `openEsame()` estrae 20 domande; `renderQuiz()` non mostra né colori né spiegazioni durante l'esame (chi lo fa non sa come sta andando); `renderEsito()` mostra il voto, le sbagliate per lezione, «Rifai l'esame» e «Chiudi». Nessuna scrittura nel salvataggio.
- Il ripasso completo scrive il migliore in `progress.quiz["q"+i]`; «Ripassa solo le sbagliate» (giro parziale) non scrive niente.
- `meriti()` legge già `progress.exam?.superato`, che nessuno scrive.
- Non c'è nessun `@media print`.

### Il modello più semplice

**Gioco libero: non cambia niente.** L'esame resta una prova, «Rifai l'esame» resta, niente si salva, niente attestato.

**Carriera:**

1. **Esame superato (16 o più): voto definitivo** (decisione di Ale del 14 ottobre). Si salva `progress.exam = { superato: true, voto, data }`. Nella schermata finale niente «Rifai l'esame». Nel menu il pulsante diventa «Esame superato: 17 su 20» e non si apre più.
2. **Esame non superato:** si salva `progress.exam = { superato: false, voto, data, ripasso: [lezioni con almeno un errore] }`. La schermata finale mostra, al posto di «Rifai l'esame», un pulsante per ogni lezione da ripassare («Ripasso: Lezione 3»), che apre il ripasso che esiste già. Il pulsante dell'esame nel menu è spento e dice «Esame: prima i ripassi delle lezioni 3 e 5».
3. **Una lezione esce dall'elenco** quando se ne fa un ripasso **completo** con almeno l'80%. Il giro «solo le sbagliate» non basta. Il ripasso conta solo se fatto dopo l'esame, ed è automatico: l'elenco nasce con l'esame. Svuotato l'elenco, il pulsante si riaccende. Nessuna attesa, nessuna penalità, i meriti restano.
4. **Esame lasciato a metà** (Esc o «Chiudi»): non conta e non si salva, come oggi. Durante l'esame non si vede se le risposte sono giuste, quindi abbandonarlo non permette di scegliere il risultato.
5. **Libretto:** la riga «Ti manca l'esame.» resta finché l'esame non è superato. Con i ripassi da fare, il suggerimento dice «il ripasso della Lezione 3 (dopo l'esame)». Con il livello superato, al posto delle due righe: «Brevetto ottenuto il 14 ottobre 2026» e il pulsante «Attestato».
6. **Attestato:** una scena sopra il menu (lo stesso tipo di riquadro del glossario). Compare **da sola la prima volta che si torna al menu con tutte le condizioni raggiunte**, qualunque sia stata l'ultima (esame, una regata, una prova…). Si salva `progress.brevetto = { data }`, poi si riapre dal libretto.
   - Testo: «Scuola di vela · Brevetto di livello 1 · Timoniere di deriva», il nome, la data, il voto dell'esame, i quattro meriti. In evidenza: «Nessun valore legale: non sostituisce un corso di vela né la patente nautica.» Niente loghi, niente sigle.
   - **Nome:** un campo facoltativo nell'attestato, salvato in `progress.brevetto.nome`, solo nel browser.
   - **«Stampa»** con `window.print()` e un `@media print` che stampa solo l'attestato; **«Chiudi»**.
7. **«Azzera»** in carriera cancella anche esame e brevetto (fanno parte di `progress`): già così, nessuna riga in più.

Costanti nuove: nessuna. Il campo `prove` previsto nel §2 per `exam` non serve: non lo legge niente, quindi si toglie.

### Collaudo: nuovo `tests/collaudo_carriera_esame.py` [proposta]

Criteri scritti adesso. Pagina **senza `#collaudo`**, solo clic; le risposte giuste si riconoscono leggendo la banca `ESAME` dal testo di `index.html`, come fa `collaudo_esame.py`.

- **E1, carriera vuota:** pulsante dell'esame acceso; esame fatto tutto giusto, 20 su 20: «superato», **nessun «Rifai l'esame»**, `progress.exam.superato` vero con voto 20; **nessuna scena** dell'attestato (mancano i meriti); pulsante del menu «Esame superato: 20 su 20» e spento; libretto senza la riga «Ti manca l'esame».
- **E2, esame non superato:** carriera con i meriti a posto; esame con errori apposta in due lezioni, voto sotto 16. Atteso:
  - `progress.exam.superato` falso e `ripasso` uguale alle due lezioni sbagliate, calcolate dal collaudo dalle risposte date;
  - pulsante del menu spento;
  - un ripasso della prima lezione al 75% (dove le domande sono 4) o comunque sotto l'80%: resta spento;
  - lo stesso ripasso al 100%: quella lezione esce dall'elenco, il pulsante resta spento;
  - «solo le sbagliate» sulla seconda: resta spento;
  - ripasso completo della seconda al 100%: pulsante acceso.
  - Poi esame superato: compare la **scena dell'attestato**, con «Nessun valore legale» e **senza** «patente» né «patentino» nel titolo.
- **E3, attestato:** nome scritto, chiuso e riaperto dal libretto: il nome resta. Stampa provata con `emulate_media("print")`: si vede solo l'attestato (menu nascosto). Schermata salvata a 1360×650.
- **E4, l'ultima condizione non è l'esame:** carriera con esame superato e un punto mancante in Competizione (preparata in `localStorage`); si scrive il piazzamento che manca e si torna al menu: la scena compare **una volta sola** (al secondo ritorno al menu non ricompare).
- **E5, gioco libero:** lo stesso esame superato non salva niente (`localStorage` identico byte per byte), «Rifai l'esame» c'è, nessun attestato, pulsante sempre acceso.
- **E6, esame lasciato a metà in carriera:** niente si salva.
- **Spazio:** riquadro dell'attestato e menu con «Brevetto ottenuto…» a 1360×650 senza eccesso, con i caratteri veri (PC di Ale).
- **Non-regressione:** `polare.js`, `raffiche_e_virate.js`; `collaudo_esame.py`, `collaudo_quiz.py`, `collaudo_libretto.py`, `collaudo_carriera.py`, `collaudo_versione.py`.

### Rischi

- **Un voto solo è severo** se l'esame va male per distrazione: ma vale solo per chi lo **supera** (il voto non si migliora). Chi non lo supera lo rifà dopo i ripassi.
- **Un ripasso «dopo l'esame» si può fare subito**, anche senza aver studiato: basta farlo all'80%. È il ripasso mirato del §3, non un blocco: chi gioca vede le spiegazioni delle sbagliate.
- **La scena dell'attestato compare al menu**, non nell'istante esatto: se l'ultima condizione è una regata, prima si vede il riepilogo della regata, poi tornando al menu la scena.
- **Stampa:** l'aspetto cambia da un browser all'altro; si collauda solo l'emulazione, l'aspetto lo giudica Ale.

### Decisioni per Ale

1. **Esame non superato:** ripasso mirato delle lezioni sbagliate (almeno 80%), poi si riprova, come nel §3. Va bene? Oppure preferisci un'altra regola (per esempio un numero massimo di tentativi)?
2. **Nome sull'attestato:** campo facoltativo, scritto da chi gioca. Va bene?

### Risposte di Ale ed esito (0.24, 14 ottobre 2026)

- **Esame non superato:** «ripassa le lezioni di cui hai sbagliato le risposte e torna a fare il test». Il ripasso completo di ogni lezione segnalata basta, **con qualsiasi punteggio**: la soglia dell'80% (§3 e punto 3 qui sopra) è tolta. «Una regola vale l'altra»: si vedrà giocando.
- **Nome sull'attestato:** facoltativo, scritto da chi gioca.
- **Prova a mano senza giocare ore:** `tests/prova_carriera.py` apre il gioco con una carriera in cui manca solo l'esame.
- Fatta come scritta. Nel collaudo il controllo «"solo le sbagliate" non basta» non c'è: quel pulsante compare solo alla fine di un ripasso completo, che conta già. E4 scrive il piazzamento nel salvataggio invece di correre una regata (dichiarato nel `CHANGELOG.md`). Numeri in `CHANGELOG.md`, 0.24.

---

## 14. Fetta 6 (1.0): rilascio — proposta di dettaglio

Del 14 ottobre 2026. **Fermata 1: nessun codice.**

### Cosa manca per la 1.0

Il gioco, per il livello 1, è completo: bivio (0.22), libretto (0.23), esame in carriera e attestato (0.24). Restano tre cose.

1. **Documenti.**
   - `VERSIONE = "1.0"` e la voce del `CHANGELOG.md`, con il riepilogo di cosa è il livello 1.
   - `ROADMAP.md`: fase A chiusa.
   - `PIANO-GENERALE.md`: punti 3 e 4 del §11 fatti; le decisioni 8 e 9 chiuse (8: tutti gli aiuti valgono per i meriti, opzione A; 9: banca dell'esame separata dai ripassi, 0.20).
   - `README.md`: una riga sullo stato.
   - Nessun cambio al gioco oltre a `VERSIONE`.
2. **Manuale** (`MANUALE-bozza.md`): le sezioni su carriera, libretto, esame e attestato ci sono già (0.22-0.24). Da aggiungere:
   - gli aiuti accesi o spenti non cambiano i punti (decisione 8, opzione A);
   - le semplificazioni della 1.0: Competizione dalle due regate singole e non da un torneo, un brevetto solo, banca dell'esame piccola (26 domande), numeri del libretto provvisori;
   - i dati restano nel browser e si perdono cancellandoli (già scritto nella 0.22; si controlla che ci sia).
3. **Collaudo di una carriera intera** e una prova a mano di Ale.

### Il collaudo: nuovo `tests/collaudo_carriera_intera.py` [proposta]

Una sola pagina, salvataggio vuoto, «Carriera» scelta **cliccando il selettore**. Si gioca tutto nella stessa carriera, nell'ordine della Scuola, e alla fine si legge **solo quello che il gioco ha salvato**. Serve l'aggancio `#collaudo`, perché i piloti lo usano.

- **Lezioni:** si percorrono tutte, passo per passo, fino all'ultimo passo (è lì che il gioco segna la lezione come completata). Come dice il §7, si usa `collaudo_lezioni.py`:
  - i passi pratici che ha già (13 su 33) si guidano davvero, a passi fissi;
  - **gli altri 20 si saltano con «Avanti» forzato dall'aggancio.** È il limite più grosso del collaudo, ed è dichiarato.
- **Prove 1-4:** il pilota di `collaudo_fasce.py` (oro per costruzione, quindi 12 punti di Abilità senza la prova 5).
- **Regate:** il pilota sostituto (`__sv.pilota`), avversari principianti. Ogni regata si rifà con semi diversi finché la somma dei due piazzamenti migliori dà almeno 3 punti, **al massimo 3 tentativi per regata** (C3: con 3 tentativi il minimo si raggiunge nel 100% delle finestre).
- **Ripassi:** tutti e sei, a clic, risposte giuste.
- **Esame:** a clic, tutte giuste.

Criteri, scritti adesso:

- **I1:** alla fine il libretto dice «Brevetto ottenuto il …», la scena dell'attestato è comparsa da sola una volta, e `progress` ha `brevetto`, `exam.superato` e voto 20.
- **I2:** i meriti letti dal salvataggio coincidono con un calcolo fatto dal collaudo sulle regole scritte, area per area.
- **I3:** la chiave del gioco libero non esiste o è identica byte per byte dall'inizio alla fine.
- **I4, il metro ha misurato davvero:**
  - le 6 lezioni risultano completate dal gioco, non scritte dal collaudo;
  - le 4 prove sono finite con un tempo;
  - nelle regate il sostituto ha mosso la barra;
  - si stampano i passi guidati e quelli saltati.
  - Se una prova o una regata non arriva in fondo, il risultato è NON VALIDO, non FALLITO.
- Si stampano tempi, piazzamenti, tentativi e meriti finali.

Durata stimata: pochi minuti (tutto a passi fissi). Se resta sotto i 5 minuti entra in `lancia_tutti.sh --veloce`, altrimenti fra i collaudi lunghi.

### Alternativa più completa (non nella 1.0, salvo decisione di Ale)

**Un pilota per tutti i 33 passi pratici delle sei lezioni.** Oggi nessun collaudo dimostra che **ogni** passo pratico si possa completare guidando: lo dimostrano solo le partite a mano. È un compito a sé, con due fermate e probabilmente qualche difetto da trovare. Proposta: farlo **dopo** la 1.0, come primo compito, oppure prima, se Ale preferisce una 1.0 più solida. Costa più tempo dell'intera fetta 6.

### Prova a mano di Ale

Non ore di gioco.
- Gioco caricato normalmente, in «Carriera», con la carriera di prova azzerata.
- Una lezione, una prova e una regata, guardando il libretto e il suggerimento che cambiano.
- Poi `tests/prova_carriera.py` per esame e attestato, già fatto il 14 ottobre: si può saltare.

### Rischi

- **Una 1.0 con 20 passi pratici mai guidati da un collaudo.** Le lezioni sono giocate a mano da Ale da settimane, ma non tutte, e non dopo ogni versione.
- **Il sostituto non fa regate pulite** (0 su 320): «Regate senza errori» resta 0 nel collaudo. Non toglie punti.
- **Prova 5 esclusa dal collaudo**, perché il pilota la finisce 19 volte su 24; non serve per il minimo.

### Decisioni per Ale

1. 1.0 con il collaudo come sopra (13 passi guidati, 20 saltati e dichiarati), e il pilota completo delle lezioni dopo la 1.0. Oppure prima il pilota completo, poi la 1.0.
2. Prova a mano ridotta come sopra.

### Decisione di Ale (14 ottobre 2026)

**«La 1.0 è la versione giocabile.»** La 1.0 esce con la barca di oggi e il collaudo del §14 (13 passi pratici guidati, 20 saltati e dichiarati). Dopo la 1.0, nell'ordine proposto: pilota completo delle lezioni (rete di sicurezza per le modifiche di fisica), resistenza dello scafo con le fasce ritarate, timone e virate, penalità a giri e regole di colpa, disegno della vela; poi le voci piccole.

**Esito della fetta 6 (1.0, 14 ottobre 2026).** Fatta come nel §14, con una correzione dei numeri: i passi pratici sono **32**, non 33, e quelli guidati sono **14**, non 13 (18 saltati). Il collaudo corre le due regate almeno una volta ciascuna, anche quando una sola basterebbe per il minimo. Il seme di ogni regata si fissa nello stesso comando che la apre: senza, in un giro su tre la regata 2 dava un altro piazzamento, perché il disegno consuma numeri casuali fra un comando e l'altro (come nella 0.21.1). Numeri in `CHANGELOG.md`, 1.0.
