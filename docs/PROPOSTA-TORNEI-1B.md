# Proposta: i tornei dell'1b

20 ottobre 2026, fermata 1; **T1 fatta nella 1.0.34** (§7).

## 0. Contesto (da leggere prima, anche in chat)

- **Dove sta nell'impianto** (`VISIONE-LIVELLI-E-CARRIERA.md` §2): l'1b è la parte **pratica** del livello 1, con la barca completa (timone che stalla, Z, salti di vento, raddrizzata lunga). La pratica è fatta di **tornei** con le regole semplici di oggi (mure, sopravento, 15 s di penalità) e dello strumento di scuola dalla regata (`PROPOSTA-REGATA-COME-FONTE.md` §9), che **vive solo dentro i tornei** ed è rimandato a dopo questa proposta.
- **La barca dell'1b non è ancora congelata.** Quindi qui si separa quello che si può costruire subito (formato, punteggio, salvataggio, schermate, geometria del percorso) da quello che aspetta la barca congelata («prima la barca, poi il resto»): gli avversari sui lati al lasco e la lunghezza dei lati in secondi.
- **Già deciso, non si ridiscute:** 4 regate e uno scarto (`VISIONE` §7); il triangolo nell'1b, mentre il trapezio è rimandato (`RICERCA-CONTENUTI-LIVELLI.md` §7); le regole semplici dell'1b (le penalità a giri arrivano col livello 2).

## 1. Fonti

- **F15, appendice A** (regolamento 2025-2028, copia locale), parafrasata:
  - A4, sistema a punti bassi: 1 punto al primo, 2 al secondo e così via;
  - A2.1, uno scarto: il totale della serie è la somma delle regate meno la peggiore; a parità di peggiore, si scarta la più vecchia. Vince chi ha meno punti;
  - A5.2: chi non arriva, si ritira o è squalificato prende i punti del posto «iscritti + 1»;
  - A8: parità nella serie. Si confrontano i punteggi dal migliore al peggiore, senza gli scarti, e vince chi ha il primo punteggio migliore. Se la parità resta, conta l'ultima regata, poi la penultima e così via, scarti compresi.
- **F36 (nuova): Wikipedia, «Olympic triangle»** (CC BY-SA), parafrasata:
  - il triangolo classico è equilatero, 60° a ogni boa;
  - una variante ha 90° alla boa di poppa (la boa «di lato», dove si stramba) e 45° alle altre due;
  - il triangolo equilatero regge meglio ai salti di vento: con 15° di salto un lato al lasco diventa più largo e l'altro più stretto, ma restano tutti e due al lasco;
  - le boe si lasciano di solito a sinistra;
  - la pagina dice anche che alle Olimpiadi oggi si usano percorsi a quattro lati.

## 2. Modello più semplice plausibile

### 2.1 Formato

- **Una serie di 4 regate di fila** contro **gli stessi tre avversari**, con lo stesso carattere per tutta la serie. Nella realtà la flotta di una serie è sempre la stessa.
- **Punteggio** come in F15 appendice A:
  - punti bassi (1-4);
  - chi non arriva prende 5 punti (iscritti + 1);
  - uno scarto;
  - parità come in A8.
- **Penalità** (decisione di Ale, 20 ottobre: «seguiamo i regolamenti»): non più 15 s sul tempo, ma la **penalità sul punteggio** di F15 44.3. La regata vale i punti del piazzamento, più il 20% dei punti di chi non arriva: con 4 barche fa +1 punto, e i punti non vanno oltre quelli di chi non arriva. I punti delle altre barche non cambiano, quindi due barche possono avere lo stesso punteggio. Semplificazione dichiarata: la decide il gioco al contatto, senza bandiera gialla e senza dichiararla all'arrivo. I giri (44.1) arrivano col livello 2. Le regate fuori dai tornei (1a e la regata libera dell'1b) restano con i 15 s, che **non hanno una fonte**: sono una semplificazione del gioco.
- **Classifica della serie** fra una regata e l'altra: una tabella con le 4 barche, i punti di ogni regata, lo scarto fra parentesi e il totale. A fine torneo, il piazzamento finale.

### 2.2 Salvataggio e abbandono

- Il torneo si salva **dopo ogni regata** nei progressi (nuovo campo `progress.torneo`): condizioni, avversari e risultati.
- **Chiudere la pagina non è abbandonare:** alla riapertura si riprende dalla regata interrotta, che si ricorre da capo.
- **Abbandonare** è un pulsante esplicito, «Ritirati dal torneo». Come dice la visione, il torneo ritirato non conta. Dentro una regata invece vale A5.2: chi non arriva prende 5 punti.

### 2.3 Percorso

**Il triangolo di una sola volta, con arrivo sulla linea di partenza:**
1. partenza;
2. bolina fino alla boa 1;
3. lasco fino alla boa 2, che sta a sinistra guardando il vento;
4. lasco di ritorno, tagliando la linea dalla parte del percorso.

Tutte le boe si lasciano a sinistra. È la forma della **prova 5 dell'1a** («Percorso nelle raffiche»), quindi il giocatore la conosce già. `roundCheck()` (`gioco.js`) vale già per qualsiasi boa, e il controllo d'arrivo delle regate (`raceLegs`, lato 2) è quello di oggi.

**Forma (da decidere, §5):**
- **equilatero, 60-60-60:** due lati al lasco a circa 120° dal vento; regge meglio ai salti di vento (F36);
- **90° alla boa 2:** due lati di gran lasco, a 135° dal vento;
- **come la prova 5:** traverso, poi gran lasco.

**Lunghezza dei lati:** si ricava dalla barca, non si scrive a mano. È la lunghezza che fa durare la regata del pilota fra 4 e 5 minuti (`VISIONE` §7), e si calcola dopo il congelamento. Fino ad allora: **200 m**, ipotesi nostra. Stima: bolina circa 2 minuti, i due lati al lasco circa 1 minuto ciascuno.

**Da cambiare nel codice** (oggi le regate sono a bastone):
- `leg` va da 0 a 3 invece che da 0 a 2;
- `strada()` dei distacchi diventa la strada lungo i lati;
- `targetOf` ha più boe;
- `legName` deve chiamare i lati «al lasco».

### 2.4 Condizioni delle quattro regate

Proposta: **un solo torneo**, con condizioni diverse in ogni regata, come i giorni diversi di una serie vera:
1. 10 nodi costanti;
2. raffiche;
3. salti di vento;
4. sorteggiata fra le tre.

È un torneo solo, ma copre tutti gli argomenti dell'1b. I tornei divisi per categoria di `VISIONE` §7 (vento leggero, teso, raffiche, salti) restano per i livelli con due persone a bordo.

### 2.5 In due tappe

| Tappa | Cosa | Aspetta la barca congelata? |
| --- | --- | --- |
| **T1** | Formato, punteggio, salvataggio, ritiro, classifica della serie, schermate. Le regate di T1 sono **a bastone** con la barca dell'1b, perché gli avversari sanno già girare la boa di bolina | **No.** Si può fare subito |
| **T2** | Triangolo: boa 2, lati al lasco, avversari che girano la boa 2 e tagliano l'arrivo al lasco; lunghezza ricavata dalla barca | **Sì** per gli avversari e la lunghezza. Il disegno del percorso e i lati del giocatore si possono preparare prima |

## 3. Costanti nuove (tutte ipotesi nostre)

| Costante | Valore | Perché |
| --- | --- | --- |
| Regate per torneo | 4 | `VISIONE` §7 |
| Scarti | 1 | F15 A2.1 (valore di base) |
| Punti a chi non arriva | 5 | F15 A5.2 con 4 iscritti |
| Lato del triangolo | 200 m, poi ricavato dalla barca | Regate di 4-5 minuti (`VISIONE` §7) |
| Penalità sul punteggio | 20% dei punti di chi non arriva (+1 con 4 barche) | F15 44.3(c), valore di base |

## 4. Criteri (soglie nostre, dichiarate ora)

Semi da 1 a 20 per tarare, da 101 a 120 (mai guardati) per la conferma. Ogni criterio dichiara quante volte ha misurato davvero; zero casi = **FALLITO**.

| | Criterio | Soglia |
| --- | --- | --- |
| C1 | **Punteggio:** casi costruiti a mano da F15 (scarto, scarto a pari merito, chi non arriva, penalità sul punteggio, con il tetto e con due barche a pari punti, parità A8.1, parità A8.2 risolta all'ultima regata e alla penultima), con i valori attesi scritti prima | 0 errori su almeno 12 casi |
| C2 | **Serie completa guidata dal pilota:** 20 tornei. La classifica del gioco si confronta con una ricalcolata **in modo indipendente** dai tempi d'arrivo registrati (il collaudo ha il suo calcolo, non chiama quello del gioco) | 0 differenze; 80 regate concluse dichiarate |
| C3 | **Ripresa:** chiusura della pagina dopo la regata 1, 2 e 3, poi riapertura | 30 casi, stato del torneo identico e serie completata |
| C4 | **Ritiro:** un torneo ritirato non lascia punti né record | 10 casi; localStorage senza voci del torneo ritirato |
| C5 | **1a identica:** impronta, `polare.js`, `raffiche_e_virate.js` | identici al bit |
| C6 | **Pannello** a 1360×650 nel caso peggiore (tabella con 4 regate, scarti, chi non arriva, nomi più lunghi) | 0 pixel di eccesso |
| C7 | **Prova da giocatore:** pagina senza `#collaudo`, un torneo intero con una chiusura in mezzo | completo, nessun errore nella console |
| C8 | (solo T2) **Durata:** regata del pilota sul triangolo | mediana fra 4 e 5,5 minuti, su 40 regate |
| C9 | (solo T2) **Avversari sul triangolo:** girano la boa 2 dal lato giusto e arrivano | almeno il 97% delle barche arriva; giri sbagliati dichiarati |

## 5. Decisioni per Ale (una alla volta)

**Prese il 20 ottobre 2026:** (a) prima T1, con le regate a bastone, e il triangolo (T2) dopo la barca congelata e gli avversari; (b) nei tornei la penalità sul punteggio di 44.3 al posto dei 15 s; (c) un solo torneo con 4 regate di vento diverso (§2.4). La regata con raffiche obbliga a risolvere il primo rischio di §6 (raffiche attorno al solo giocatore, mure giudicate col suo vento) prima di T1; (d) triangolo equilatero, 60° a ogni boa (F36).

(e) Meriti di Competizione dell'1b dalla tabella provvisoria di `VISIONE` §6: piazzamento finale nel torneo 1° = 6, 2° = 4, 3° = 3, 4° = 2, più 1 se il torneo si chiude senza penalità sul punteggio. Si guadagnano solo in carriera; il minimo per il brevetto dell'1b si decide col menu. (f) Il torneo c'è anche nel gioco libero (principio «tutto sempre giocabile») e lì non dà meriti, come le regate di oggi.

## 6. Rischi

- **Raffiche nei tornei dell'1b:**
  - nascono attorno al giocatore (`spawnGust`), quindi un avversario lontano naviga senza raffiche;
  - `contacts()` giudica le mure col vento nel punto del giocatore (`local.twd`), difetto noto dalla 1.0.1.

  Nell'1b vanno corretti tutti e due, o la regata con raffiche va dichiarata «raffiche solo vicino a te». Le regate dell'1a non si toccano.
- **Flotta fissa a 4.** La formula dei punti di oggi (`5 - pos`) e il «5 a chi non arriva» valgono per 4 barche. Si scrivono come «iscritti + 1», non come 5.
- **Il triangolo tocca il codice dei distacchi e della classifica:** `ranking()` e `strada()` presuppongono il bastone. In T2 vanno riscritti e ricollaudati (`collaudo_distacchi.py`).
- **Salvataggio con la barca che cambia:** un torneo salvato prima di un cambio della barca dell'1b mescolerebbe due barche. Si salva la versione del gioco nel torneo; se cambia, il torneo si chiude con un avviso. I salvataggi si possono sempre azzerare.
- **Avversari dell'1b non ancora rifatti** (`STATO.md`, prossimo lavoro 3): il torneo T1 eredita gli avversari di oggi, con il 17% di virate oltre la bolina + 15°. È giocabile, ma i piazzamenti si tareranno dopo.

## 7. Fermata 2, tappa T1 (1.0.34, 20 ottobre 2026)

**Fatto:** formato, punteggio, salvataggio, ritiri, classifica della serie e riquadro, meriti, raffiche attorno a tutte le barche e mure col vento di ciascuna (solo 1b). Dettagli nel `CHANGELOG.md`, 1.0.34.

**Scelte prese durante il lavoro (non erano nella fermata 1):**
- **Finestra d'arrivo** (F15 appendice S, 12.3): chi non arriva entro 1,5 volte il tempo della prima prende i punti di chi non arriva. Il 50% è un'ipotesi nostra. Serve anche a chiudere la regata: quando il giocatore ha finito, le barche ancora in acqua arrivano in una simulazione accelerata.
- **Lo scarto conta dalla quarta regata** (la serie ne ha 4 e uno scarto); prima la tabella non ne mostra.
- **Lunghezza:** tutte e quattro le regate con la boa a 140 m, come le regate dell'1a, anche quella coi salti (la «Regata nei salti di vento» ha 300 m): regate di 4-5 minuti (`VISIONE` §7).
- **Niente «Ricomincia» né «Cambia vento»** nel torneo; restano «Ritirati dalla regata» e «Ritirati dal torneo». **Dalla 1.0.50:** tornando al menu a metà regata, o chiudendo la pagina, quella regata vale come ritirata (5 punti). Limite: se il browser viene ucciso senza `pagehide` (blocco del PC, batteria) l'uscita non si registra e la regata si ricorre da capo.
- In carriera il torneo si apre col brevetto di livello 1 (`VISIONE` §8: un livello è chiuso finché non si hanno i brevetti giusti).
- Pannello: nel caso peggiore il pannello sforava (prima misura 202 px, con tutti e 7 i tipi di errore). Finita la regata del torneo il suggerimento si nasconde, il risultato non ripete errori e distacchi e «Classifica del torneo» sta nella riga di «Ritirati dalla regata»: 0 px.

**Misure** (`tests/collaudo_torneo.py`):

| | Criterio | Misura | Esito |
| --- | --- | --- | --- |
| C1 | Punteggio, casi a mano | 0 errori su 15 casi | OK |
| C2 | 40 tornei col pilota (1-20 gioco libero, 101-120 carriera, meriti compresi) | 0 differenze; 80 + 80 regate concluse | OK |
| C3 | Ripresa | 30 su 30; 10 serie completate; chiusura a metà regata 2 senza effetti in 10 su 10 | OK |
| C4 | Ritiro | 10 su 10 | OK |
| C5 | 1a identica | `polare.js` e `raffiche_e_virate.js` identici al 19 ottobre; impronta: 62 scene su 63 identiche, cambia solo il menu (riquadro del torneo, «In arrivo») | OK |
| C6 | Pannello e riquadro a 1360×650, caso peggiore | 0 px | OK |
| C7 | Da giocatore, senza `#collaudo` | torneo intero, pagina chiusa dopo la regata 2, nessun errore. **Il giocatore si ritira da ogni regata**: le regate le finiscono gli avversari; guidare davvero lo provano C2 (col pilota) e Ale | OK |
| C10 | (aggiunto alla fermata 2, prima di misurare) raffiche: tempo in raffica degli avversari almeno metà di quello del giocatore | 92% (12,5% contro 13,6%), 20 regate; nell'1a 67% | OK |

**Da sapere:**
- Piazzamenti finali del pilota: 1° 9, 2° 7, 3° 13, 4° 11 su 40 tornei; una sola barca non arrivata su 640.
- **Penalità:** il pilota ne prende 1,7 per regata (265 in 160), circa tre su quattro prima del via, come nell'1a (33 in 20 regate a bastone dell'1a, 39 in 20 regate del torneo). Con +1 punto l'una pesano molto più dei 15 s. Da riguardare con gli avversari dell'1b (prossimo lavoro 3) e giocando.
- Nella regata con raffiche dell'1a gli avversari erano già al 67% del giocatore: il difetto delle raffiche era meno grave di quanto si temeva.
- **Difetto trovato fuori dal torneo:** nelle regate dell'1a, all'arrivo, il pannello sfora di 48 px con errori normali (153 con tutti gli errori), perché il risultato ripete errori e distacchi. Mai misurato in quello stato. L'1a è congelata: da decidere con Ale.

**T2 (triangolo) aspetta la barca dell'1b congelata.**

## 8. T2, fermata 1 aggiornata (27 ottobre 2026) — nessun codice toccato

Le due condizioni di §2.5 ci sono: la barca dell'1b è congelata (23 ottobre) e gli avversari dell'1b sono rifatti (1.0.49). Questa sezione dice come far diventare il percorso del torneo un **triangolo equilatero** (decisione (d) di §5, F36) e come misurarlo. §2.3 resta valida per la forma; qui c'è il lavoro sul codice letto oggi.

### 8.1 Cosa c'è oggi nel codice (`js/regate.js`)

Il percorso è una sola boa in `R.mark` (0, −`R.up`) e tre «lati» (`leg` 0 = prima della partenza, 1 = bolina, 2 = poppa verso l'arrivo). Lo presuppongono: `targetOf` (punti di passaggio degli avversari solo per la boa di bolina), `raceLegs` (un solo `roundCheck`, `b.rnd`), `strada` (percorso = 2·`R.up`), `distacco`, `ranking` (usa `leg` e la distanza dal bersaglio), il disegno e le frecce, e il registratore (evento `lato N`).

### 8.2 Modello più semplice plausibile

- **Il percorso diventa una lista di boe**: il bastone ha 1 boa, il triangolo 2. I lati valgono 1 = verso la boa 1, 2 = verso la boa 2 (**nuovo**), 3 = verso l'arrivo. Con una sola boa tutto resta com'è.
- **Geometria** (coordinate del vento, linea al centro in (0, 0)): boa 1 in (0, −L); boa 2 in (∓0,866·L, −0,5·L), a sinistra guardando il vento, così il lato fra le due boe e quello verso l'arrivo sono a 120° dal vento. Tutte le boe si lasciano a sinistra, come nella prova 5 dell'1a.
- **Giro della boa 2**: lo stesso `roundCheck` della boa 1 con un secondo contatore (`rnd2`). Dal lato sbagliato vale come oggi: si rigira, e si conta in `wrongMarks`.
- **Avversari**: gli stessi tre punti di passaggio di §`targetOf`, riportati sulla boa 2 (ipotesi nostra: stessa forma, già misurata sulla boa 1 nelle 1.0.42 e 1.0.49).
- **Strada e distacchi**: `strada` diventa la somma dei lati già fatti più la proiezione sul lato corrente (lunghezza totale = L + L + L). Il resto di `distacco` non cambia.
- **Solo nel torneo dell'1b.** Le regate dell'1a e la «Regata nei salti di vento» restano a bastone.

### 8.3 Costanti nuove (ipotesi nostre)

- **L**, lunghezza del lato. Si ricava dalla barca, non si scrive a mano: si prova L = 140, 170, 200, 230 m e si prende la più piccola per cui la mediana del pilota sta in 4-5,5 minuti (C8), scelta sui semi 1-20 e confermata sui semi 21-40 (regola dei semi).
- Raggio entro cui un avversario considera «raggiunto» un punto di passaggio alla boa 2: lo stesso della boa 1.

### 8.4 Criteri (scritti prima di misurare; C8 e C9 sono quelli di §4)

| | Criterio | Soglia |
| --- | --- | --- |
| C8 | Durata: regata del pilota sul triangolo | mediana fra 4 e 5,5 minuti, su 40 regate |
| C9 | Avversari: arrivano e girano la boa 2 dal lato giusto | almeno il 97% delle barche arriva; i giri sbagliati si dichiarano |
| T2a | Non regressione: regate dell'1a e salti di vento, stessi arrivi al bit; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici | identici |
| T2b | Distacchi sul triangolo: `collaudo_distacchi.py` esteso, segno e valore coerenti su tutti e tre i lati | 100% dei confronti, con il numero dei confronti stampato (non vale «nessun errore» a zero) |
| T2c | Il pilota gira la boa 2 dal lato giusto | almeno il 97% su 40 regate |
| T2d | Torneo intero: C1-C11 di `collaudo_torneo.py` ancora verdi (R7 resta il limite noto) | OK |
| T2e | Pannello a 1360×650 e disegno: due boe sul mare, quella giusta evidenziata | 0 px di eccesso; boe contate dai tratti disegnati |
| T2f | Registratore: `lato 3` nel file e nell'analizzatore | file letto senza errori |

### 8.5 Rischi

- **Il lavoro più grosso è il passaggio da «una boa» a «lista di boe»**: tocca `targetOf`, `raceLegs`, `strada`, `ranking`, disegno e registratore. Per questo T2a (identità al bit sul bastone) è un criterio e non un'attenzione.
- **Penalità alla boa 2**: tre barche che arrivano insieme sulla boa 2 si urtano come sulla boa 1; la regola 18 (spazio alla boa) è del livello 2 e qui non c'è. Atteso più contatti del bastone: si misura e si riporta, senza tarare.
- **Salvataggi del torneo** a metà: se cambia il percorso, il torneo salvato si chiude con un avviso (già previsto in §6).
- **Salti di vento**: con boe fissate al vento di partenza un salto persistente cambia gli angoli dei lati al lasco; si dichiara, come nel bastone.

### 8.6 Deciso (Ale, 27 ottobre 2026: «si era scelto di seguire le regole ufficiali, quindi percorsi misti»)

**Percorsi misti:** regata 1 bastone (10 nodi), regata 2 triangolo (raffiche), regata 3 bastone (salti di vento), regata 4 triangolo (condizione sorteggiata). Perché: in una serie vera il percorso lo sceglie il comitato (F39, regola 27.1); i salti di vento restano sul bastone, dove si impara a virare sugli scarsi, e non deformano i lati al lasco; le regate 1 e 3 restano quelle di oggi, quindi si possono confrontare al bit (§8.7, punto 7). Scartato: tutte e 4 a triangolo. Il percorso dipende solo dal numero della regata: nessun numero a caso in più. Caso da dichiarare: la regata 4 sorteggia i salti una volta su tre, e allora sono salti sul triangolo.

**Dopo il via di Ale:** versione 1.0.55, con Sonnet per il codice.

### 8.7 Correzioni dopo la lettura del codice (27 ottobre 2026, Opus)

1. **Il metro del «prima e dopo» non misura i tornei.** In `tests/arrivi_regate.py` (riga 36) il clic su «Corri la regata» è finito dentro un commento: le 4 righe di ogni torneo riportano tutte la stessa regata a bastone dell'1a (stessi tempi, «Vento da nord», nessuna penalità sul punteggio). Quindi «2 tornei identici» del commit `8cf6f47` non è stato misurato. Prima di T2: correggere la riga, aggiungere un controllo che le 4 regate siano davvero del torneo (titolo «Torneo, regata k di 4», 4 regate diverse, giocatore arrivato o ritirato), rifare il confronto fra `05ec528` (prima della pulizia) e `8cf6f47`, e solo allora fare il file «prima» di T2.
2. **Geometria, un segno solo.** In coordinate del vento (verso il vento = −y, sinistra guardando il vento = −x, come il punto 1 di `targetOf`): boa 2 in (−0,866·L, −0,5·L). La semiretta del giro (`out` di `roundCheck`) della boa 2 punta fuori dal percorso, a sinistra guardando il vento: `out` = vento − 90°. Con questi segni il giro giusto (boa a sinistra) conta +1, come alla boa 1.
3. **Contatore del giro:** invece di un secondo contatore `rnd2`, al cambio di lato si azzerano `rnd`, `rndA` e `rp`, come fanno già le prove (`gioco.js`, riga 775). `legName` e il registratore («boa girata dal lato sbagliato», `sba`) guardano «lato di una boa» invece di `leg === 1`. Sul bastone l'azzeramento cade nel lato verso l'arrivo, dove quei campi non servono.
4. **Punti di passaggio alla boa 2:** quelli della boa 1 ruotati di 90° attorno alla boa. Non è la stessa situazione già misurata: alla boa 1 si arriva di bolina, alla boa 2 al lasco e si stramba, e il tratto fra il punto 0 e il punto 1 diventa una poppa piena, dove la guida fa bordi con abbattute. Ipotesi più debole di come era scritta: C9 deve contare anche i giri sbagliati con una soglia (criterio T2g).
5. **Strada per i distacchi:** sul bastone resta la formula di oggi, scritta uguale (una formula generale darebbe numeri diversi nell'ultima cifra). Sul triangolo la strada si misura **lungo il lato** e non più nella direzione del vento (sui lati al lasco la direzione del vento ne vedrebbe metà), limitata fra 0 e L.
6. **T2c non è un metro a sé:** il pilota dei collaudi è la guida degli avversari principianti (`avvio.js`, `pilota`), quindi T2c misura la stessa cosa di C9. Si tiene come riga di C9, non come prova indipendente; il giro della boa 2 si prova anche con scenari fissi (T2h).
7. **T2a precisato:** identiche al bit le 20 regate e le 9 introduzioni di `arrivi_regate.py`; con i percorsi misti anche le regate 1 e 3 di ogni torneo (bastone); le regate 2 e 4 cambiano per costruzione.
8. **Durata, numeri di oggi** (`arrivi_regate.py`, 27 ottobre, pilota, tempo senza penalità): bastone a 140 m con la barca dell'1a da 173 a 232 s (circa 3,4 minuti), salti di vento a 300 m con la barca dell'1b da 401 a 468 s. Le regate a bastone del torneo stanno quindi **sotto** i 4-5 minuti di `VISIONE` §7, contro quello che dice §7 (misura del torneo da rifare col metro corretto). Stima per il triangolo (bolina circa 0,8 s/m, lasco circa 0,35 s/m): durata ≈ 1,5·L s, quindi 140 m ≈ 3,5 minuti, 170 m ≈ 4,3, 200 m ≈ 5. Si sceglie con C8 come scritto; il bastone del torneo resta a 140 m (consiglio: non toccarlo ora, così le regate 1 e 3 restano confrontabili al bit).
9. **Semi:** i semi 1-40 sono già stati guardati per gli avversari. Taratura di L sui semi 1-20, conferma sui **61-80**.
10. **C9 senza finestra d'arrivo:** nel torneo chi arriva dopo 1,5 volte il tempo del primo non arriva per regola. C9 si misura fuori dalla finestra: barca arrivata entro `R.t` = 1500 s.
11. **Nome della boa 2:** a schermo «Boa 2 · lasciala a sinistra», senza «boa di poppa» o «di strambata» finché il nome italiano non è in una fonte (`CONTENUTI-DA-VERIFICARE.md`). Da riscrivere anche i testi che dicono «quattro regate a bastone» e «girare la boa gialla e tornare a tagliare la linea» nel torneo.

Criteri in più (scritti ora, prima di misurare):

| | Criterio | Soglia |
| --- | --- | --- |
| T2g | Giri sbagliati alla boa 2 (avversari e pilota, 40 regate) | al massimo il 5% dei passaggi; il numero dei passaggi stampato |
| T2h | Scenari fissi del giro della boa 2: barca che la lascia a sinistra (+1) e a destra (−1), da 4 direzioni del vento | 8 casi su 8 |
| T2i | Il metro dei tornei (`arrivi_regate.py` corretto): 4 regate diverse per torneo, tutte con titolo del torneo | 8 regate su 8 |
| — | Penalità per regata sul triangolo contro il bastone | si riporta, senza soglia (§8.5) |
