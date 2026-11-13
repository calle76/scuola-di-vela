# Proposta: i tratti dei rivali, secondo passo (fermata 1, 13 novembre 2026)

**Stato: proposta. Nessun codice toccato. Aspetta il via di Ale.**

Viene dalla voce 23 di `DA-FARE.md` (idea di Ale del 12 novembre: per ogni avversario, a inizio torneo, tratti estratti a caso e indipendenti: tendenza all'errore, lettura del vento e scelta del lato, aggressività). È il passo dopo la scheda dei rivali (`PROPOSTA-SCHEDA-RIVALI.md`, 1.2.30), che mostra solo fatti. Il materiale più ampio (pool di rivali, sponsor, salita e discesa) è in `PROPOSTA-RIVALI-E-SPONSOR.md` e resta da discutere: qui niente di quello.

## 1. Cosa c'è già (letto in `js/regate.js` sul ramo della 1.2.30)

**Ogni avversario ha già dei tratti, ma nascosti.** A inizio torneo `aiParams` sorteggia per ogni barca (`regate.js:125-130`):

| Valore | Esperti | Principianti | Cosa fa in acqua |
| --- | --- | --- | --- |
| `up` | 45-48° | 49-54° | angolo di bolina: più basso = stringe di più |
| `down` | 150-155° | 142-150° | angolo in poppa |
| `trim` | ±2° | ±6° | errore fisso nella regolazione della vela |
| `boardMin`-`boardMax` | 35-90 s | 25-60 s | lunghezza dei bordi di bolina, sorteggiata a ogni virata |
| `gain`, `react` | 18, 5 | 26, 3 | prontezza al timone (uguali per tutti nello stesso livello) |
| `startM` | 0-1 s | 0-3 s | margine in partenza: quanto tardi arriva alla linea |

Poi c'è il **carattere** (prudente, normale, aggressiva), detto prima della regata. Una sola aggressiva, e solo con gli esperti.

I valori restano gli stessi per tutte e 4 le regate del torneo (deciso da Ale), ma il giocatore non li vede: una Rossa che stringe 45° e una Verde che stringe 48° sembrano solo «più o meno veloci».

**Cosa manca rispetto all'idea di Ale:**
- **errori:** gli avversari non scuffiano mai (0 su circa 50 registrazioni) e non sbagliano manovre. Regolano la vela sul vento apparente a ogni istante;
- **lettura del vento:** la durata dei bordi è sorteggiata. Nessuno sceglie il lato del campo e nessuno vira sugli scarsi: la proposta della bolina, che li faceva virare sugli scarsi, non è stata adottata (`PROPOSTA-AVVERSARI-BOLINA.md`, 10 novembre).

## 2. Il passo (modello più semplice)

**Tre tratti per rivale**, sorteggiati a inizio torneo, indipendenti, ognuno su tre gradi (debole, medio, forte):

1. **Bolina.** Esiste già: è `up` più `trim`. Il passo è solo **dirlo**: il grado si ricava dai valori sorteggiati, divisi in terzi della fascia del livello. Non cambia niente in acqua.
2. **Partenza.** Esiste già: `startM` più il carattere. Anche questo solo detto.
3. **Raffiche (nuovo).** Quanto è pronto a lascare quando entra una raffica:
   - **forte:** come oggi, regola subito;
   - **medio:** regola con un ritardo di `RIT_M` secondi;
   - **debole:** ritardo di `RIT_D` secondi, e nel frattempo tiene la vela dove era.
   La conseguenza la decide la fisica, la stessa del giocatore: più sbandamento, più scarroccio, e nelle raffiche forti anche la scuffia. È la causa nautica richiesta dai principi di `PROPOSTA-RIVALI-E-SPONSOR.md` §4: **niente errori tirati a sorte**, solo una reazione più lenta.

**Perché le raffiche e non la strambata a vela aperta.** Il ritardo nel lascare è una debolezza vera dei principianti (lezione «Assorbire una raffica», fonti F81-F84: lascare subito) e si vede in acqua (la barca sbanda e rallenta). La strambata a vela aperta richiederebbe una manovra sbagliata apposta, e la sua conseguenza fisica sugli avversari non è misurata: resta per un passo dopo, se serve.

**Lettura del vento (scelta del lato):** non in questo passo. La strada più semplice (virare sugli scarsi) è stata misurata e non è passata; va prima la diagnosi delle cause in bolina, già proposta il 10 novembre. Lo scrivo per non far credere che sia dimenticata.

**Dove si vedono i tratti.** Sulla scheda dei rivali della 1.2.30, una riga in più per rivale: «Bolina: forte · Partenza: media · Raffiche: debole». Due modi possibili, da scegliere (§7):
- **A, detti subito**, come oggi il carattere;
- **B, scoperti:** il tratto compare sulla scheda dopo la prima regata in cui si è visto (per esempio «Raffiche» dopo la prima regata con una raffica forte vicino a quella barca). È l'idea 1 della sezione 9 di `PROPOSTA-RIVALI-E-SPONSOR.md`; costa di più (bisogna definire «si è visto»).

Propongo **A** per questo passo: si misura meglio, e B si può aggiungere dopo senza rifare niente.

**Dove vale:** solo nel torneo. Le regate della Scuola e quelle a tema restano identiche al bit (decisione di Ale del 9 novembre: gli avversari si migliorano per Deriva e il torneo; la Scuola non deve peggiorare).

**Costanti nuove (ipotesi nostre, da fissare nella fermata 2 sui semi di scelta):**
- `RIT_M`, `RIT_D`: ritardi in secondi (punto di partenza: 1 s e 2,5 s);
- soglia di «raffica» per far partire il ritardo: vento locale sopra 1,12 volte il medio, la stessa del pannello (`gioco.js`, `inGust`);
- i terzi della fascia per dire debole, medio e forte su `up`, `trim` e `startM`.

## 3. Criteri misurabili (soglie nostre, scritte prima di misurare)

Misura col pilota sulle 4 regate del torneo, principianti ed esperti. Scelta delle costanti sui semi 2101-2130, conferma sui semi 2131-2160, mai usati: nei documenti compaiono semi fino a circa 1930, e prima di cominciare lo ricontrollo.

- **T1, i tratti si vedono nei risultati.** Per la bolina: i rivali «forti» perdono in bolina, rispetto alla rotta ottimale (`rotLatiBarca`), almeno il 15% in meno dei «deboli», in mediana. Per le raffiche: i «deboli» perdono nei lati con raffiche almeno il 10% in più dei «forti». Se un tratto non si vede, non si mostra: un'etichetta che non corrisponde a niente è peggio di nessuna etichetta.
- **T2, non si peggiorano gli avversari.** Il tempo mediano dei rivali nel torneo non sale più del 3% rispetto alla 1.2.30. Il tratto «debole» toglie qualcosa a uno, ma la flotta resta quella.
- **T3, le scuffie sono rare e spiegabili.** Rivali scuffiati: fra lo 0,5% e il 5% delle barche-regata del torneo, e **solo** fra quelli «deboli» nelle raffiche. Zero scuffie vuol dire che il tratto non fa niente; più del 5% rende il torneo una lotteria.
- **T4, il torneo non diventa una lotteria.** La differenza di punti fra primo e ultimo rivale a fine torneo non cambia più del 20% rispetto alla 1.2.30, in mediana.
- **T5, non-regressione.** Regate della Scuola e a tema identiche al bit (`impronta`, regata per regata); `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; la 1.2.30 senza tratti nuovi deve dare gli stessi tempi.
- **T6, pannello e scheda** a 1360x650 senza pixel in eccesso, misurati sul riquadro intero (lezione del 13 novembre: il primo metro guardava l'elemento sbagliato).
- **T7, collaudo guidando la barca** (`#collaudo`) e in una pagina caricata come la carica Ale, Chromium e Firefox.

## 4. Rischi

- **Un tratto debole che non si vede** (T1) rende la scheda falsa: si toglie quel tratto, non si gonfia l'effetto.
- **Le raffiche del torneo potrebbero essere troppo deboli** per far scuffiare anche con il ritardo: allora T3 non passa e si riporta, senza alzare le raffiche (sarebbe un'altra modifica).
- **Il PC è lento:** 60 tornei col pilota sono circa un'ora e mezza per gruppo di semi. Si misura con al massimo 2 processi e il termostato.

## 5. Cosa questo passo NON fa

Lettura del vento, memoria che cambia il comportamento, pool di rivali, sponsor, salvataggio fra tornei, nomi propri. Tutto in `PROPOSTA-RIVALI-E-SPONSOR.md`.

## 6. Versione e costo

1.2.31 (dopo la 1.2.30 della scheda). Circa una giornata:
- tratto delle raffiche e misura T1-T4: mezza;
- riga sulla scheda, collaudo, documenti: mezza.

## 7. Domande per Ale

1. **Il via.**
2. **Tratti detti subito (A) o scoperti giocando (B)?** Propongo A.
3. **Bastano tre tratti** (bolina, partenza, raffiche)? La lettura del vento resta fuori finché non c'è la diagnosi della bolina.

## 8. Il via di Ale e il modello rivisto (13 novembre 2026)

Ale: «via ai tratti, detti subito se è la soluzione più semplice. Ma non dovevano essere debole, medio e forte, ma caratteristiche tipo bravo in partenza». Quindi: **via, modo A (detti subito)**, e i tratti diventano **caratteristiche dette a parole**, non gradi. Questa sezione sostituisce i §2 e §3 dove sono diversi.

**Il modello.** A inizio torneo ogni rivale riceve **una dote e un difetto**, in due aree diverse fra le tre (partenza, bolina, raffiche); nella terza area è nella media e la scheda non dice niente. Area della dote a caso fra le tre, area del difetto a caso fra le due rimaste, indipendente per ogni rivale.

| Area | Dote | Difetto | Cosa cambia in acqua |
| --- | --- | --- | --- |
| Partenza | «brava in partenza» | «parte tardi» | `startM` nel terzo migliore o peggiore della fascia del livello |
| Bolina | «stringe bene di bolina» | «di bolina va larga» | `up` e l'errore di regolazione `|trim|` nel terzo migliore o peggiore |
| Raffiche | «pronta a lascare nelle raffiche» | «lenta a lascare nelle raffiche» | ritardo 0 s (come oggi) o `RIT_D`; nella media `RIT_M` |

Il femminile è perché si parla della barca, come oggi il carattere («aggressiva in partenza»). Il carattere resta com'è e si legge accanto. Esempio di scheda: «Rossa: brava in partenza, ma lenta a lascare nelle raffiche. Prudente e sta alla larga.»

**Perché così la flotta resta la stessa.** Per ogni area, un rivale ha la dote con probabilità 1/3, il difetto con 1/3 e la media con 1/3. Quindi `startM`, `up` e `|trim|` hanno ancora la distribuzione uniforme sulla fascia di oggi: cambia solo l'abbinamento (nessuno è bravo o scarso in tutto). L'unico peggioramento medio viene dalle raffiche, dove oggi tutti sono «pronti»: lo misura T2.

**Dove vale:** solo nel torneo, come prima. Un torneo salvato prima della 1.2.31 (senza tratti) continua con i valori che ha e la scheda non mostra caratteristiche.

**Criteri rivisti (soglie nostre, scritte prima di misurare).** T2-T7 restano come al §3. T1 diventa, area per area, dote contro difetto, in mediana su tutte le barche-regata:
- **T1a partenza:** i rivali «bravi in partenza» tagliano la linea dopo il colpo con un ritardo minore di quelli che «partono tardi»: almeno 0,5 s fra i principianti e 0,15 s fra gli esperti (metà della larghezza di un terzo della fascia).
- **T1b bolina:** chi «stringe bene» perde in bolina, rispetto alla rotta ottimale (`rotLatiBarca`), almeno il 15% in meno di chi «va larga».
- **T1c raffiche:** chi è «lento a lascare» perde nei lati con raffiche almeno il 10% in più di chi è «pronto»; in più sbanda di più (sbandamento massimo mediano più alto).

Se un'area non passa T1, la sua caratteristica non si mostra e lo dico: un'etichetta che non corrisponde a niente è peggio di nessuna etichetta.

**Semi:** scelta delle costanti `RIT_M` e `RIT_D` sui semi 2101-2130, conferma sui semi 2131-2160. Ho ricontrollato: nei documenti i numeri fra 2100 e 2199 sono numeri di riga, non semi.
