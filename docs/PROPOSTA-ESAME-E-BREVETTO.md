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
| `scuolaVelaGhost.v1` | Fantasmi: **in comune** fra le due modalità. Non sono meriti. |

- **Come si separano:** `STORE` diventa una variabile. Il bivio, solo dal menu, salva il `progress` corrente, cambia chiave e ricarica `progress` dalla chiave nuova. Il resto del gioco non cambia.
- **Piazzamento delle regate:** all'arrivo, accanto al tempo migliore, si salva `progress.race[chiave] = { pos, n, pulita }`, ma solo se ci sono avversari. Si salva anche nel gioco libero, perché il codice è lo stesso e un ramo in più costerebbe di più; lì non si mostra e non conta.
- **Livello degli avversari nel piazzamento: alternativa non ancora decisa** (vedi l'avvertenza della fetta 0.21). Oggi il livello non è salvato da nessuna parte (controllo 3). Due strade: in carriera il livello degli avversari è fisso, oppure entra nel risultato salvato (per esempio con una chiave come `r0.2:principianti`, `r0.2:esperti`).
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

| Area | Punti | Massimo | Minimo |
| --- | --- | --- | --- |
| Abilità | 5 prove: bronzo 1, argento 2, oro 3, +1 se completata almeno una volta senza errori | 20 | 8 |
| Conoscenza | 6 ripassi: 2 punti se il migliore è almeno l'80%, 1 punto se almeno il 60% | 12 | 6 |
| **Competizione** | **2 regate singole, solo con avversari** (principianti o esperti, stessi punti); per ogni regata conta il risultato migliore: 1° = 4, 2° = 3, 3° = 2, 4° = 1, +1 se senza errori | **10** | **3** |
| Esperienza | 1 punto per ogni lezione completata | 6 | 6 |
| **Totale** | somma dei minimi 23 | **48** | **29 richiesti** |

Perché così:

- **Competizione.** Il minimo 3 si raggiunge arrivando ultimi in entrambe le regate, una delle due senza errori (1 + 2), oppure con un 3° posto e un ultimo. Quindi non serve battere nessuno, serve **finire le regate**, in linea con il piano (§5: «il passaggio non deve mai dipendere dalla forza dell'equipaggio»). Il «senza errori» segue la regola della ★ (`regTotal() === 0`), quindi conta anche un contatto subìto.
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

**Abilità: nessuna misura nuova.** Le fasce sono tarate sul pilota: oro = tempo del pilota arrotondato, bronzo = +60% (0.16 e 0.19). Il minimo 8 equivale a bronzo ovunque più 3 prove pulite, oppure argento in 4 prove. Nelle prove 1-4 il pilota di `collaudo_fasce.py` fa oro per costruzione; nella prova 5 finisce 18 corse su 24, con mediana 353,2 s contro l'oro a 355 s. Basta riportarlo.

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
| 3 · Andature e filetti | bolina, traverso, lasco, gran lasco, poppa (ordine e descrizione, non i gradi esatti); più veloce al traverso e al lasco che in poppa; le mure (nome, lato del boma; **senza precedenze**); cosa dicono i filetti (sopravento agitato, dritti, sottovento agitato) e cosa fare; «orzi e cazzi, poggi e laschi» |
| 4 · Vento reale e apparente | definizione del vento apparente; da fermi apparente = reale; accelerando si sposta verso prua e la vela va cazzata; in poppa è più debole del reale, di bolina più forte; il segnavento indica l'apparente |
| 5 · Virata e strambata | virata (prua nel vento) e strambata (poppa nel vento); virata che non riesce per poca velocità; bordeggiare e bordo; strambata violenta con la vela aperta; strambata controllata (cazzare, poggiare, lascare) |
| 6 · Raffiche e scuffia | riconoscere una raffica (chiazza scura che arriva da sopravento); lascare come prima reazione, orzare un poco di bolina; tenere la barca piatta; cos'è la scuffia; come si raddrizza una deriva nella realtà (sulla lama) |

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
| 3 | 0.22 | **Bivio e salvataggio di carriera.** `STORE` variabile, selettore nel menu, «Azzera» solo sulla modalità corrente. | Pagina senza `#collaudo`: in carriera il pilota di `collaudo_fasce.py` completa la prova 1, e la chiave del gioco libero resta **identica byte per byte**; poi il contrario. Ricaricando, la modalità è ricordata. Un ripasso in carriera non tocca il record del libero. Menu a 1360×650 senza eccesso. |
| 4 | 0.23 | **Libretto.** `meriti(progress)`, quattro barre, riga «cosa manca» per superare il livello. Il pulsante dell'esame non dipende dai meriti. | `meriti()` sui giocatori A-D del §4 e sui casi al bordo (minimo esatto, minimo meno 1, «nessuno» escluso), con l'esame superato e non: «livello superato» solo con tutte le condizioni. Nel browser: salvataggi di carriera preparati, poi lettura delle barre e della riga; **pulsante dell'esame acceso anche con meriti a zero**. Menu a 1360×650 e 1360×768 senza eccesso, con i caratteri veri. |
| 5 | 0.24 | **Esame in carriera, ripasso mirato, scena dell'attestato.** | Percorso in pagina senza `#collaudo`. Con una carriera vuota: pulsante acceso, esame superato, **nessuna scena** (mancano i meriti); poi meriti completati, la scena compare. Con una carriera dai meriti a posto: esame sbagliato apposta, pulsante spento, ripassi delle lezioni sbagliate al 100% e, a parte, a 75% (resta spento), pulsante acceso, esame superato, scena dell'attestato con «nessun valore legale» e senza «patente», stampa provata con `emulate_media("print")` e schermata. Nel gioco libero lo stesso esame superato **non** mostra l'attestato e il pulsante non si spegne mai. |
| 6 | 1.0 | **Rilascio.** Manuale (sezione meriti ed esame), documenti, `CHANGELOG.md`. | Una carriera da zero **guidata davvero**: le lezioni con `collaudo_lezioni.py`, le prove con il pilota delle fasce, le due regate con il sostituto, i ripassi e l'esame risposti; il libretto deve arrivare al brevetto. È lungo: lo lancia Ale sul PC. Poi una partita a mano di Ale. |

Le fette 1 e 2 sono indipendenti e si possono scambiare. La 3 viene prima di 4 e 5.

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
