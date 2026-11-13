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

**Seconda risposta di Ale (stesso giorno):** «parlavi dei giudizi, non delle qualità: organizzale come vuoi, le qualità e un commento, oppure un grado di valore se occupa meno spazio». Tengo le qualità dette a parole (una dote e un difetto in una riga), che sulla scheda occupano una riga sola come un grado.

## 9. Misure sui semi di scelta (13 novembre, pomeriggio) e cambio del terzo tratto

**Semi 2101-2130**, 4 regate del torneo, principianti ed esperti: 240 regate e 720 barche-regata per versione, contro la 1.2.30 sugli stessi semi. Le flotte sono diverse, perché cambia il sorteggio, ma hanno la stessa distribuzione. Misure fatte con il freno termico: picco 69 °C.

| Criterio | Soglia | Misurato | Esito |
| --- | --- | --- | --- |
| T1a partenza | ritardo «parte tardi» − «parte bene» ≥ 0,5 s principianti, 0,15 s esperti | principianti 3,37 − 1,72 = **1,65 s**; esperti 4,48 − 1,30 = **3,18 s** | sì |
| T1b bolina | «stringe» ≤ 0,85 × «va larga» (persi in bolina sulla rotta ottimale, mediana) | principianti 29,1% contro 41,0% (**0,71**); esperti 25,1% contro 30,6% (**0,82**) | sì |
| T1c raffiche | «lenta» ≥ 1,10 × «pronta» (persi su tutti i lati) | principianti **0,86**, esperti **0,81**: le lente perdono *meno* | **no** |
| T2 arrivo dei rivali | ≤ +3% sulla 1.2.30 | 201,2 s contro 201,1 s (**+0,0%**) | sì |
| T3 scuffie | 0,5-5% | **0 su 720** | **no** |
| T4 primo-ultimo rivale | ±20% | 6,0 contro 6,0 punti (**+0%**) | sì |

**Perché le raffiche non si vedono (prova a coppie, semi 2101-2110, 240 barche-regata: stesse regate con il ritardo spento e acceso).**
- Con 1 s e 2,5 s: le barche «lente» arrivano +0,7 s (mediana) rispetto al ritardo spento, cioè rumore. Lo sbandamento massimo è uguale e le scuffie sono 0.
- Con 5 s e 10 s (prova di diagnosi, non una proposta): +5,3 s (mediana, 52 più lente e 18 più veloci), sbandamento +1,8°, scuffie 0.
- La causa è che le raffiche del torneo sono deboli: dal 20% al 40% di vento in più (`spawnGust`, livello 1), su chiazze di 9-20 m. Con 10-12 nodi lo sbandamento dei rivali resta intorno ai 23°, lontano dai 60° della scuffia. Anche non lascando per niente, si perde poco.
- Il confronto diretto (T1c) è falsato anche dalla partenza: chi ha il difetto nelle raffiche ha la dote o la media in partenza.

Era il rischio scritto al §4 («le raffiche del torneo potrebbero essere troppo deboli»). Come stabilito lì, il tratto si toglie e le raffiche non si alzano.

**Il terzo tratto diventa la poppa.** Come la bolina, è un valore che ogni rivale ha già: `down`, l'angolo in poppa, che dalla 1.2.24 sposta la prua rispetto all'angolo della VMG migliore (`DOWN_E`). Dote: «va forte in poppa», `down` nel terzo più alto della fascia. Difetto: «in poppa va piano», terzo più basso. Anche qui la distribuzione resta quella di prima e non c'è nessuna costante nuova, quindi i semi di scelta non servono.

**T1c nuovo, scritto prima di misurare:** chi «va forte in poppa» perde in poppa, rispetto alla rotta ottimale, almeno il 15% in meno di chi «va piano», in mediana; si contano i lati di poppa delle regate a bastone (1 e 3). **T3** non ha più senso, perché le scuffie non sono più un effetto atteso: il numero si riporta solo come informazione.

**Conferma:** tutto (T1a, T1b, T1c nuovo, T2, T4) sui semi 2131-2160, mai usati, per la 1.2.31 e per la 1.2.30.

**Per dopo:** le raffiche possono tornare come tratto nei circuiti con vento più forte, quando ci saranno.

## 10. Conferma sui semi 2131-2160 (13 novembre, pomeriggio): versione NON chiusa

Semi 2131-2160, mai usati: 240 regate e 720 barche-regata per versione, contro la 1.2.30 sugli stessi semi. Picco 63 °C.

| Criterio | Soglia | Misurato | Esito |
| --- | --- | --- | --- |
| T1a partenza | ≥ 0,5 s principianti, ≥ 0,15 s esperti | principianti 2,32 − 1,72 = **0,60 s**; esperti 1,83 − 1,55 = **0,28 s** (sui semi di scelta erano 1,65 e 3,18) | sì, di poco |
| T1b bolina | rapporto ≤ 0,85 | principianti **0,65**; esperti **1,09**: chi «stringe bene» perde di più di chi «va larga» | **no per gli esperti** |
| T1c poppa | rapporto ≤ 0,85 | principianti **0,96**, esperti **0,94** | **no** |
| T2 arrivo dei rivali | ≤ +3% | 196,2 s contro 195,2 s (**+0,5%**) | sì |
| T4 primo-ultimo | ±20% | 6,0 contro 6,0 (**+0%**) | sì |
| T3 (solo informazione) | — | 0 scuffie su 720 | — |

**Cosa vede un giocatore in un torneo intero.** È solo informazione, non un criterio dichiarato: la media delle 4 regate di ogni rivale. Contando le volte in cui, nello stesso torneo, il rivale con la dote fa meglio di quello col difetto:
- principianti: bolina **17 su 22**, partenza **13 su 19**, poppa **11 su 23**;
- esperti: bolina **10 su 23**, partenza **10 su 19**, poppa **11 su 21**.

Quindi solo la bolina dei principianti si nota con una certa sicurezza; il resto è come tirare una moneta.

**Perché.** Le fasce di oggi sono strette rispetto a tutto il resto che decide una regata: salti di vento, posizione in partenza, incroci con le altre barche. Per esempio, gli esperti hanno il margine di partenza fra 0 e 1 s e l'angolo di bolina fra 45° e 48°: un terzo della fascia vale 0,33 s o 1°.

**Esito: la 1.2.31 così com'è non si chiude.** Mostrare «stringe bene di bolina» su un esperto che va come gli altri sarebbe un'etichetta falsa. La decisione spetta ad Ale (§11).

## 11. Diagnosi: fasce raddoppiate (13 novembre, pomeriggio) e scelta per Ale

**Prova di diagnosi**, non una versione: le fasce di dote, media e difetto sono allargate del doppio attorno al centro della fascia di oggi. Per esempio, la bolina degli esperti va da 43,5° a 49,5° invece che da 45° a 48°; il margine di partenza non scende sotto 0. La manopola è `__sv.trattiAmp(2)`; il valore 1 lascia tutto identico a prima. Semi di scelta 2101-2115: 120 regate, 360 barche-regata.

| Tratto | Per barca-regata (rapporto o differenza) | Nello stesso torneo la dote fa meglio |
| --- | --- | --- |
| Partenza | principianti +1,66 s, esperti **+4,25 s** | principianti 7 su 10, esperti **6 su 6** |
| Bolina | principianti **0,47**, esperti **0,63** | principianti 7 su 11, esperti 5 su 10 |
| Poppa | principianti 0,79, esperti **1,16** | principianti 7 su 10, esperti 3 su 7 |

Il resto, sempre contro la 1.2.30 sugli stessi semi:
- T2: arrivo dei rivali **+0,5%**;
- T4: primo-ultimo invariato;
- scuffie: 0.

**Lettura.**
- Con le fasce doppie, partenza e bolina si vedono bene anche per barca-regata: rapporti 0,47-0,63, cioè chi ha la dote perde in bolina circa la metà di chi ha il difetto. La flotta nel complesso resta la stessa.
- **La poppa non si vede nemmeno così**: in poppa l'angolo conta poco, perché vicino ai 170° la velocità utile cambia poco con qualche grado.
- I confronti dentro lo stesso torneo sono pochi, perché i semi sono 15: sono un indizio, non una misura.

**Opzioni (decide Ale):**
- **A (la mia proposta): due tratti, partenza e bolina, con le fasce doppie.** Ogni area è sorteggiata da sola: dote, media o difetto, una volta su tre ciascuna. La scheda dice solo quello che non è nella media, per esempio «parte bene; di bolina va larga», oppure «nella media». Il carattere (prudente, normale, aggressiva) resta com'è. Poi la conferma completa su semi nuovi, 2161-2190, con gli stessi criteri.
- **B: tre tratti come prima, con le fasce doppie,** ma la poppa non passa: si tornerebbe ad A.
- **C: fermare la 1.2.31** e tenere i tratti nascosti come oggi, finché non ci saranno i circuiti e le raffiche più forti.

**Cosa cambia in A rispetto al via del 13 novembre:**
- i tratti sono due invece di tre;
- non c'è più per forza «una dote e un difetto»: un rivale può avere due doti, due difetti o essere nella media;
- le differenze fra i rivali dello stesso livello sono più grandi di oggi, anche se la media della flotta resta quella.

Per questo serve un via nuovo.

## 12. Via di Ale ad A, con le manovre al posto della poppa (13 novembre, sera)

Ale: «chi è meno bravo direi che è più lento nelle manovre, meno preciso», poi «ok vai avanti». Quindi l'opzione A del §11, con un terzo tratto nuovo al posto della poppa.

**Modello, scritto prima di misurare.**
- **Tre aree, ognuna sorteggiata da sola:** partenza, bolina, manovre. In ciascuna il rivale è nel terzo migliore (dote), in quello di mezzo (media) o nel peggiore (difetto), una volta su tre.
- **Partenza e bolina:** le fasce doppie della diagnosi del §11 (formula identica a `trattiAmp(2)`).
- **Manovre (nuovo):** i due valori del timone che oggi sono fissi per livello, `react` (quanto in fretta il timone va dove deve: più alto = virata più svelta) e `gain` (quanti gradi di scarto servono per dare tutto timone: più basso = rotta tenuta più stretta). Con u da 0 (il migliore) a 1 (il peggiore):
  - esperti: react 6 → 4, gain 15 → 21 (oggi 5 e 18, il centro);
  - principianti: react 4 → 2, gain 22 → 30 (oggi 3 e 26, il centro).
  Le ampiezze (±1 su react, ±3 e ±4 su gain) sono **ipotesi nostre**, nessuna fonte: scelte perché il centro resta quello di oggi e il migliore dei principianti resta sotto il peggiore degli esperti per la prontezza.
- **Poppa:** l'angolo torna sorteggiato come nella 1.2.30, senza tratto.
- **Scheda:** si dicono solo le aree fuori dalla media, per esempio «parte bene; vira lenta e imprecisa»; «nella media» se nessuna.

**Criteri, soglie scritte prima di misurare** (contro la 1.2.30 sugli stessi semi):
- **T1a partenza:** come prima, almeno 0,5 s (principianti) e 0,15 s (esperti) di differenza nel taglio della linea fra difetto e dote.
- **T1b bolina:** come prima, rapporto dote/difetto ≤ 0,85 delle perdite di bolina sulla rotta ottimale, per entrambi i livelli.
- **T1d manovre (nuovo):** rapporto dote/difetto ≤ 0,85 delle perdite su **tutti i lati** rispetto alla rotta ottimale, in mediana, per entrambi i livelli.
- **T2:** arrivo mediano dei rivali entro +3%. **T4:** primo-ultimo entro ±20%.
- **T5 (nuovo, rischio del timone):** scuffie e boe toccate dai rivali non più del doppio della 1.2.30 più 5; un timone troppo pronto o troppo pigro potrebbe far serpeggiare la barca.

**Semi:** scelta sui 2101-2115 (si possono ritoccare solo le ampiezze delle manovre, dicendolo); conferma sui 2161-2190, mai usati. Se T1d non passa sui semi di scelta, le manovre si tolgono e resta A con due tratti.

## 13. Semi di scelta 2101-2115 col modello del §12 (13 novembre, sera)

Il confronto è con la 1.2.30 sugli stessi semi: 120 regate e 360 barche-regata. Picco di temperatura **72 °C**, con due misure insieme: d'ora in poi ne gira una sola.

| Criterio | Soglia | Principianti | Esperti |
| --- | --- | --- | --- |
| T1a partenza (difetto meno dote) | 0,5 s e 0,15 s | **0,99 s** sì | **0,42 s** sì |
| T1b bolina (dote/difetto) | ≤ 0,85 | **0,54** sì | **0,82** sì, di poco |
| T1d manovre (dote/difetto, tutti i lati) | ≤ 0,85 | **1,14 NO** | **1,37 NO** |
| T2 arrivo dei rivali | ≤ +3% | −1,0% sì (tutta la flotta) | |
| T4 primo-ultimo | ±20% | +0% sì | |
| T5 scuffie / boe toccate | ≤ doppio + 5 | 0 contro 0; 28 contro 40: sì | |

Due informazioni senza soglia:
- **contatti dopo il via:** 49 contro 73;
- **nello stesso torneo la dote batte il difetto:**

  | | Principianti | Esperti |
  | --- | --- | --- |
  | Partenza | 9 su 11 | 6 su 12 |
  | Bolina | 5 su 8 | 9 su 13 |
  | Manovre | 6 su 8 | 1 su 4 |

**Le manovre vanno al contrario:** chi «vira svelta e precisa» perde di più. **Causa probabile, letta nel motore:**
- il timone frena, perché la resistenza della pala cresce col quadrato del seno del suo angolo (`js/motore.js`), e oltre l'angolo di stallo la pala stalla;
- un timone più pronto, con meno gradi per dare tutto timone, si muove di più: la barca serpeggia e frena.

Quindi «preciso» non vuol dire «più timone». Vuol dire tenere la rotta col timone giusto.

**Diagnosi a coppie, prima di decidere.** Non è una versione. Tutti i rivali hanno la stessa regolazione del timone e si confrontano gli stessi semi (2101-2105) con il centro di oggi; i numeri casuali sono identici. Le varianti, come scarto dal centro in frazioni della fascia del §12:

| Prontezza (mr) | Precisione (mg) | Cosa provano |
| --- | --- | --- |
| −0,5 | −0,5 | la dote del §12 |
| +0,5 | +0,5 | il difetto del §12 |
| −0,5 | 0 | solo più pronta |
| 0 | +0,5 | solo timone più dolce |
| −0,5 | +0,5 | pronta e dolce |
| 0 | −0,5 | solo timone più brusco |

Se una direzione rende i rivali più veloci, il tratto «manovre» si rifà su quella e si rimisura sui semi di scelta, dicendolo: la direzione del tratto cambia, quindi non è un semplice ritocco delle ampiezze. Se nessuna direzione dà una differenza chiara, le manovre si tolgono e resta A con due tratti.

Manopola di diagnosi: `__sv.manovre([mr, mg])`. Con `null` resta il sorteggio, e si toglie prima di chiudere.

## 14. Diagnosi delle manovre: nessuna direzione chiara, le manovre si tolgono (13 novembre, sera)

Semi 2101-2105, 40 regate per variante, 60 barche-regata per livello. Tutti i rivali hanno la stessa regolazione del timone e il confronto è a coppie con il centro (0, 0). Picco 59-64 °C, un processo solo.

| Variante (mr, mg) | Principianti: arrivo, mediana | Esperti: arrivo, mediana |
| --- | --- | --- |
| −0,5, −0,5 (la dote del §12) | −0,8 s | +0,9 s |
| +0,5, +0,5 (il difetto del §12) | −2,8 s | +1,6 s |
| −0,5, 0 (solo più pronta) | +0,6 s | −0,2 s |
| 0, +0,5 (solo più dolce) | −2,0 s | **+5,6 s** |
| −0,5, +0,5 (pronta e dolce) | −1,4 s | +1,4 s |
| 0, −0,5 (solo più brusca) | **−3,6 s** | +1,9 s |

**Lettura.**
- Gli arrivi sono di circa 200 s. In ogni variante si mescolano barche più veloci e più lente: per esempio 21 contro 37, oppure 45 contro 14.
- Per i principianti quasi ogni cambio fa guadagnare 1-4 s; per gli esperti quasi ogni cambio ne fa perdere 1-6. Il centro di oggi sembra vicino al meglio per gli esperti.
- **Nessuna direzione vale per tutti e due i livelli**, e le differenze stanno nel rumore che c'è anche fra due regate quasi uguali. L'effetto «al contrario» dei semi di scelta (§13) era in gran parte rumore.

**Decisione, secondo la regola scritta al §13 prima di misurare:** le manovre si tolgono. Resta l'opzione A del §11, scelta da Ale:
- due tratti, partenza e bolina;
- fasce doppie;
- ogni area sorteggiata da sola.

`react` e `gain` tornano fissi come nella 1.2.30, e la manopola di diagnosi è tolta.

**Conferma:** semi 2161-2190, mai usati, contro la 1.2.30 sugli stessi semi (già misurata). Criteri T1a, T1b, T2, T4 e T5 come al §12. T1d non c'è più.
