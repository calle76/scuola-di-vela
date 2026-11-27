# Proposta: avversari meno confusi, per il livello Deriva

6 novembre 2026, sulla 1.2.14. **Fermata 1: solo questo documento, nessuna riga nel gioco.** Nasce dalla regata giocata da Ale (`OSSERVAZIONI-GIOCANDO.md`, 80-85) e dalla sua decisione: in Deriva gli avversari sono da migliorare (`DECISIONI.md`, 6 novembre). Va fatta prima di misurare la soglia del torneo, perché ne sposta i numeri.

## 1. In breve

Oggi più di metà delle penalità nasce **prima del via**, più di una barca su quattro esce dalla linea, e chi cede spesso non si scosta abbastanza. Propongo cinque correzioni piccole alla guida degli avversari, una alla volta, ciascuna misurata. La barca e il modo di decidere chi ha torto (`chiCede`) non cambiano.

## 2. Da dove si parte: i numeri di oggi

`tests/misura_avversari.py`, semi 41-60, in Chromium, 20 regate per ogni riga, 60 avversari per riga. La barca del giocatore la guida il pilota, che usa la guida degli avversari: non guida come una persona.

| Regata, avversari | Penalità | di cui prima del via | Fuori linea al via | Piantate | Boe sbagliate | Arrivo mediano |
| --- | --- | --- | --- | --- | --- | --- |
| Bastone, principianti | 73 | 45 | 13 | 2 | 0 | 213,5 s |
| Bastone, esperti | 65 | 32 | 16 | 3 | 2 | 212,0 s |
| Salti di vento, principianti | 63 | 37 | 17 | 2 | 1 | 413,5 s |
| Salti di vento, esperti | 69 | 38 | 19 | 1 | 0 | 404,5 s |
| **Totale** | **270** | **152 (56%)** | **65 su 240 (27%)** | **8** | **3** | |

Nessuna barca resta senza arrivare. **Questa misura non conta ancora** gli scarti verso la bolina (osservazione 80), chi urta mentre cede (81) e le strambate ravvicinate (85): i contatori si aggiungono prima di toccare la guida.

## 3. Cosa si è visto e la causa probabile

Le cause sono **lette nel codice, non provate**. Ogni correzione parte verificando che il caso si riproduca. La regata di Ale è una sola, e le sue penalità sono nella norma: il problema è come si comportano, più di quante volte urtano.

| # | Cosa si è visto | Causa probabile (`js/regate.js`) |
| --- | --- | --- |
| 80 | Chi ha la precedenza, in poppa, scarta all'ultimo tornando di bolina | `cedeAvv1b`: se lo scarto calcolato non è valido, l'ultima riga manda sempre la barca di bolina, `twd - side * (ai.up - 2)`. In poppa è un giro di oltre 100° |
| 81 | Chi cede dichiara di cedere ma urta lo stesso | L'angolo di scarto è fisso (28°) e nessuno controlla se la nuova rotta evita davvero l'altra barca |
| 82 | Due barche si vengono incontro e nessuna scarta | Si guarda solo la barca col contatto più vicino nel tempo; le altre non esistono |
| 83 | Al via corrono lungo la linea e due escono oltre lo spillo | Cedendo poggiano senza guardare dove finisce la linea (ipotesi, da provare) |
| 84 | Contatti prima del via | In attesa (`hold`) la barca non cede affatto: riga 318. Il contatto a -170 s resta da capire |
| 85 | Due strambate in 3 s, tornando alla stessa rotta | Non cercata |

## 4. Il modello più semplice

Tutto dentro la guida degli avversari. Una fetta alla volta, nell'ordine di quanto pesa, con misura e commit a ogni fetta.

- **Fetta 1, prima del via (84).** Una barca in attesa cede anche lei, se chi si avvicina arriva a meno di due lunghezze. È la fetta che pesa di più: il 56% delle penalità.
- **Fetta 2, cedere davvero (81, 82).** Chi deve cedere prova scarti crescenti, **15°, 28°, 45°, 60°**, e prende il più piccolo con cui, prevedendo le rotte, passa a più di due lunghezze da **tutte** le barche vicine. Se nessuno basta, prende quello che passa più lontano.
- **Fetta 3, niente ritorno di bolina (80).** Chi ha la precedenza, all'ultimo momento, si scosta di poco rispetto alla rotta che ha: non torna mai di bolina se sta scendendo, e non passa oltre il vento.
- **Fetta 4, la linea (83).** Prima e subito dopo il via, uno scarto che porterebbe oltre lo spillo non si sceglie: se serve, si cede dall'altra parte o si rallenta.
- **Fetta 5, strambate (85).** Prima si cerca la causa. Solo se serve: dopo una strambata si resta sulle stesse mure almeno 10 s, salvo per cedere o per girare una boa.

**Fuori da questa proposta:** avversari più bravi a regatare, regola 18 alle boe, i casi in cui `chiCede` decide male, il pilota.

## 5. Criteri (soglie nostre, scritte prima di misurare)

Stessa tabella del §2, Chromium e Firefox. Le soglie si controllano sui semi 41-60, poi si **confermano sui semi 301-320, mai guardati**.

- **V1, penalità:** da 270 ad al massimo 190 (-30%).
- **V2, prima del via:** da 152 ad al massimo 90 (-40%).
- **V3, fuori linea:** da 65 su 240 (27%) ad al massimo 36 (15%).
- **V4, ritorni di bolina:** barche in poppa, con la precedenza, che tornano a meno di 60° dal vento per evitare un'altra barca: 0. Il contatore deve trovarne almeno uno sulla 1.2.14, se no non misura niente.
- **V5, chi urta mentre cede:** contatti di chi cedeva da almeno 3 s: almeno -50% rispetto alla 1.2.14 (numero di partenza da misurare col contatore nuovo).
- **V6, strambate ravvicinate:** due in meno di 5 s: almeno -50%, stessa cosa.
- **V7, non peggiorare:** non arrivate 0; piantate al massimo 12 (oggi 8); boe sbagliate al massimo 5 (oggi 3); arrivo mediano al massimo +5%; `collaudo_avversari1b.py` non peggiore di oggi.
- **V8, i casi di Ale:** una situazione costruita per ciascuna delle osservazioni 80, 81, 82 e 83, 10 varianti, va bene in almeno 9 su 10. Se va bene anche sulla 1.2.14, non distingue e si riscrive.
- **V9, barca invariata:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici. Cambiano invece le regate fotografate da `collaudo_impronta.py`: si dichiara e si rifà il riferimento.
- **Da riportare, senza soglia:** il torneo col pilota (piazzamenti e penalità, confronto con il §2 di `PROPOSTA-LIVELLO-DERIVA.md`), perché serve a scegliere la soglia.
- **Il giudizio vero è di Ale:** una regata giocata che non sembri più confusa. Questo non lo misura nessun numero.

Un numero fuori soglia si riporta com'è.

## 6. Costanti nuove (tutte ipotesi nostre)

Gli scarti di 15°, 45° e 60° (il 28° c'è già); il limite di 60° dal vento in V4; i 10 s fra due strambate, solo se servono. Le due lunghezze ci sono già.

## 7. Fonti

Le regole di riferimento sono la 14 e la 16 (F15), già usate dal codice. Le scelte di guida sono del gioco: nessuna affermazione nautica nuova, nessun testo da cambiare.

## 8. Rischi

- **Avversari che si evitano troppo:** rallentano e arrivano lontani, e il giocatore vince più facilmente. V7 lo controlla in parte; il torneo col pilota lo mostra.
- **Il pilota usa la stessa guida:** i suoi numeri cambiano insieme agli avversari. Il criterio C1 di `collaudo_competizione.py`, le penalità del torneo e l'esploratore vanno riletti.
- **Le simulazioni della partenza** usano la stessa guida: se divergono, gli avversari sbagliano il tempo del via. Va controllato a ogni fetta con `collaudo_partenze.py`.
- **Sulla stessa regata le fette si disturbano:** per questo una alla volta, e se una non porta niente si toglie.
- **Regate della Scuola:** la guida è una sola. Vedi §9.

## 9. Dove si lavora, e la domanda per Ale

Si lavora sul ramo `deriva`, in una cartella separata: la cartella di Ale, `main` e il gioco online non cambiano.

**Una domanda, da decidere prima di portare il lavoro su `main`:** la guida nuova vale anche per le regate della Scuola? **Consiglio di sì.** Avversari diversi fra i due livelli confonderebbero chi gioca e raddoppierebbero il codice. In cambio i punti di Competizione nella Scuola possono cambiare un poco: si misurano e si riportano prima.

## 10. Esiti della fermata 2 (6 novembre 2026, ramo `deriva`)

Ale: «sì parti, e la guida vale anche per la Scuola». Il lavoro è solo sul ramo `deriva`, non su `main`.

**Misura finale sui semi 341-360, mai usati prima**, stesso codice nei due browser, 80 regate per browser, 240 avversari. Il codice è stato fermato prima di questa misura.

| | Soglia | Chromium: prima → dopo | Firefox: prima → dopo | Esito |
| --- | --- | --- | --- | --- |
| V1 penalità | al massimo 190 | 332 → **162** | 338 → **162** | sì |
| V2 prima del via | al massimo 90 | 169 → **110** | 166 → **94** | **no** |
| V3 fuori linea | al massimo 36 | 62 → **24** | 63 → **25** | sì |
| V4 ritorni di bolina con la precedenza | 0 | 18 → **0** | 3 → **0** | sì |
| V5 urti mentre si cede | -50% | 123 → **41** | 136 → **32** | sì |
| V6 strambate ravvicinate | -50% | 29 → **7** | 18 → **5** | sì |
| V7 non arrivate | 0 | 0 → 0 | 0 → 0 | sì |
| V7 piantate | al massimo 12 | 8 → **20** | 10 → **20** | **no** |
| V7 boe sbagliate | al massimo 5 | 7 → 1 | 0 → 2 | sì |
| V7 arrivo mediano | al massimo +5% | migliora o resta | migliora o resta | sì |

**Le soglie non sono state cambiate.** Fuori soglia restano V2 e le piantate. Prima del via le penalità calano del 35-43% rispetto a oggi, ma il punto d'incontro delle barche resta affollato. Le piantate raddoppiano: sono soste brevi, spesso vicino a un'altra barca, soprattutto al via e vicino alla boa. Non ho cercato oltre, per non adattare il codice ai semi.

**Cosa è cambiato rispetto al §4:**

- **Fetta 1 tolta:** far cedere chi è in attesa ha **peggiorato** (penalità 270 → 409, prima del via 152 → 254, semi 41-60): chi era fermo si muoveva e urtava altri.
- **Fette 2 e 3 fatte:** lo scarto più piccolo che passa lontano da tutte le barche vicine; chi ha la precedenza parte dalla rotta che aveva.
- **Fetta 4 ridotta:** la causa ipotizzata per l'osservazione 83 era sbagliata. Le barche che escono non stanno cedendo: corrono oltre lo spillo partendo. La correzione vale negli ultimi 8 s prima del via.
- **Fetta 5 fatta:** le strambate ravvicinate erano la prua che oscillava attorno ai 180°. Sulle stesse mure si resta entro 172° dal vento, e per 10 s dopo una strambata.
- **Aggiunte, trovate misurando:** chi è lento non orza per cedere; chi scende non sale oltre il traverso per cedere; vicino alla boa non si taglia dalla parte interna; nessuno scarto dura più di 25 s. Quest'ultima serve a evitare un difetto mio: due barche parallele si tenevano a vicenda su una rotta e non arrivavano più (2 barche in Firefox, semi 41-60).

**V8, situazioni costruite** (`collaudo_avversari_deriva.py`, Chromium, 10 varianti, soglia 9):

| Caso | Prima | Dopo | Giudizio |
| --- | --- | --- | --- |
| 80 ritorno di bolina | 10 | 10 | **non distingue**: non riproduce il caso di Ale. Il contatore V4 lo vede (18 → 0) |
| 81 chi cede, a 2-3,2 s dall'altra | 0 | **6** | migliora, ma **fuori soglia**; resa più difficile dopo averla vista facile (era 9 → 10 da 3-4,5 s) |
| 82 due barche, una terza vicina | 8 | **10** | sì |
| 83 giocatore fermo vicino allo spillo | 10 | **7** | **peggiora**, e sul gioco di prima non riproduce ciò che Ale ha visto. Da riguardare giocando |

**Non-regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici. `collaudo_avversari1b.py`: fallisce lo scenario 5 a 8 su 10, già noto come fallimento a 7 su 10.

**Da fare prima di portarlo su `main`:** il giudizio di Ale giocando; rifare il riferimento di `collaudo_impronta.py`, che fotografa le regate; rileggere `collaudo_competizione.py` e l'esploratore; misurare i punti di Competizione nella Scuola, come promesso al §9.

**Torneo col pilota** (`collaudo_torneo.py`, Chromium, semi 101-120, 20 tornei, confronto col giro della 1.2.12; numeri da riportare, senza soglia):

| | 1° | 2° | 3° | 4° | Fra i primi tre | Penalità del pilota a torneo | Barche non arrivate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1.2.12 | 4 | 1 | 8 | 7 | 13 su 20 | 4,3 | 3 su 320 |
| Ramo `deriva` | 4 | 7 | 3 | 6 | 14 su 20 | 2,35 | 5 su 320 |

Il pilota usa la stessa guida degli avversari, quindi non dice quanto è difficile per chi gioca. C11 non si è concluso: la misura si è fermata al limite di tempo che le avevo dato, 25 minuti, insieme a un altro collaudo. Firefox non è stato misurato.

**Difetto nuovo, corretto dopo (vedi in fondo):** `collaudo_partenze.py` aggiunge un fallimento che nel giro della 1.2.12 non c'era: criterio (4), regata nelle raffiche, principianti, 180 s, seme 5: Verde e Blu non partono entro 60 s. Va capito prima di portare il lavoro su `main`. I fallimenti (1) e (2) sono già noti.

**Aggiornamento, stesso giorno: correzione allo spillo rifatta.** Era la correzione di partenza a far correre via le barche oltre lo spillo. Ora chi taglierebbe fuori stringe il vento o cambia mure verso il centro, negli ultimi 15 s prima del via. `collaudo_partenze.py` (Chromium): il criterio (4) non fallisce più; restano (1) e (2), già noti. Quindi la tabella sopra descrive il codice di prima.

**Misura sul codice attuale, semi 361-380, mai usati**, 80 regate per browser (Chromium / Firefox): penalità 169 / 161 (massimo 190), prima del via 117 / 109 (massimo 90, **fuori**), fuori linea 21 / 30 (massimo 36), ritorni di bolina con la precedenza 0 / 0, urti mentre si cede 36 / 34, strambate ravvicinate 4 / 9, non arrivate 0 / 0, piantate 13 / 11 (massimo 12, **fuori in Chromium**), boe sbagliate 2 / 5. Il gioco di oggi non è stato misurato su questi semi: il confronto resta quello della tabella.

**Regata giocata da Ale** (6 novembre, 15:50, a bastone, codice precedente all'aggiornamento): nessun contatto, penalità o fuori linea fino al suo arrivo, primo in 181 s. Al via resta del disordine: Rossa corre lungo la linea e taglia a 8 s, Blu passa a 3,6 m da Ale. Una regata sola.

## 11. Il giro della boa (regata di Ale delle 17:59, osservazione 90; criteri scritti prima di correggere)

**Cosa si vede.** Verde arriva a 2 m sotto il punto di passaggio 0, lo sorpassa e vira indietro per raggiungerlo; appena è sopra la boa cambia bersaglio e rivira senza velocità: 7 s sotto 1 nodo, anche all'indietro. Blu e Rossa, a circa 30 m dalla boa, fanno due virate di fila: scade il timer del bordo, poi la regola «vicino al bersaglio» riporta sul bordo di prima. Non nasce dalla guida nuova: c'è anche nella 1.2.14.

**Correzioni, una alla volta.** A: si punta già il punto oltre la boa quando ci si arriva senza virare e passando sopra la boa di almeno 3 m. B: il timer dei bordi non fa più virare entro 60 m dal bersaglio.

**Soglie**, rispetto al ramo prima di questa correzione. Pilota, Chromium e Firefox, bastone e raffiche, principianti ed esperti, 90 barche per regata: scelta sui semi 401-415, conferma sui semi 421-435 mai guardati.

- G1, ferme almeno 3 s sotto 1 nodo entro 40 m dalla boa: da 16 (7 bastone, 9 raffiche) ad al massimo 8.
- G2, barche con 3 o più virate entro 40 m: da 83 (43 + 40) ad al massimo 55.
- G3, tempo mediano entro 40 m: bastone da 37,8 s ad al massimo 32, raffiche da 31,6 s ad al massimo 27.
- G4, non peggiorare (`misura_avversari.py`): stesse soglie di V1, V3, V7; prima del via resta riportato, oggi fuori soglia.
- G5, barca invariata, `collaudo_partenze.py` senza criteri nuovi fuori.

Costanti nuove, ipotesi nostre: 3 m sopra la boa, 56° dal vento come limite di «senza virare», 60 m.

**Esiti (semi 401-415, solo Chromium; soglie non cambiate). Non superate.** Dentro: correzione A. Tolta: correzione B, che alzava le barche ferme e portava il massimo entro 40 m a 119 s.

| | Prima | A | A + B | Soglia |
| --- | --- | --- | --- | --- |
| G1 ferme | 16 | 9 | 12 | ≤ 8 |
| G2 3 o più virate | 83 | 78 | 69 | ≤ 55 |
| G3 bastone | 37,8 s | 37,5 s | 37,1 s | ≤ 32 s |
| G3 raffiche | 31,6 s | 30,1 s | 30,65 s | ≤ 27 s |

G4, semi 361-380, Chromium, con A (prima → dopo): penalità 169 → 174 (≤ 190), fuori linea 21 → 21 (≤ 36), ritorni di bolina 0 → 1 (soglia 0: **fuori**), urti cedendo 36 → 40, piantate 13 → 13 (≤ 12: **fuori**, come prima), boe 2 → 1, non arrivate 0. G5: barca identica; `collaudo_partenze.py` non concluso per tempo (fermato a 590 s). Firefox e conferma sui semi 421-435 non fatti, perché le soglie non sono raggiunte. Per confronto, Ale nella stessa regata è stato 29,5 s entro 40 m dalla boa. Molte virate restano perché chi arriva mure a sinistra deve passare sotto la boa e rivirare.

## 12. Casi 81 e 83 sulla barca M (27 novembre 2026, mattina; gioco 1.3.67 invariato)

- **Situazione:** 81 è fuori soglia dalla nascita (6 su 10, soglia 9); 83 sul PC 10 su 10, su GitHub (1.3.65) 7 su 10 in Chromium e 10 su 10 in Firefox.
- **Prova sul caso 81, su una copia:** se chi cede non trova nessuno scarto che passi ad almeno una lunghezza (`passaggio`), lascia tutta la vela e frena (con la 1.3.63 la vela libera frena davvero). Ipotesi nostra, una sola prova. **Risultato: 81 da 6 a 0 su 10** (sempre una penalità): ferma, la barca resta sulla traiettoria dell'altra. Scartata. 80, 82 e 83 invariati.
- **Da fare se si riprende:** guardare le 4 scene fallite una per una (dove sono le due barche quando comincia lo scarto, che rotta sceglie, perché non basta); il codice ricalcola già lo scarto a ogni istante (`cedeAvv1b`), quindi la causa del §3 («l'angolo si calcola una volta sola») non è più quella.

## 13. Proposta: caso 81 e vento sporco (27 novembre 2026, fermata 1; gioco 1.3.68 invariato)

**Dopo la chiusura della parte bolina della voce 2** (Ale, 27 nov) restano il caso 81, il caso 83 e il vento sporco. L'83 nel giro sulla 1.3.68 passa in Chromium e in Firefox (run 45957380469): **non si tocca**, si riguarda solo se torna rosso.

### 13.1 Caso 81: chi cede urta lo stesso

- **Oggi:** 6 su 10 (soglia 9, criterio V8 del §5). La scena: una barca con la precedenza arriva al punto d'incontro fra **2 e 3,2 s**; chi cede va a 2,3 m/s. La causa del §3 («l'angolo si calcola una volta sola») non c'è più: `cedeAvv1b` ricalcola a ogni istante.
- **Passo 1, solo misura (nessun cambio nel gioco):** per le 10 varianti, scena per scena: istante in cui chi cede comincia a scartare, rotta scelta (poggia o orza), quanto gira al secondo, distanza minima fra gli scafi, e la stessa distanza minima con le **altre due scelte** (l'altro verso, oppure vela lasciata e barra tutta da un lato) provate con la stessa fisica su una copia. Esce una tabella di 10 righe.
- **Come si decide dopo il passo 1 (scritto ora):**
  - se in almeno 9 varianti su 10 **una** delle scelte evita il contatto, la guida sceglie male: passo 2 = provare in `cedeAvv1b` tutte e due i versi (e la vela lasciata) e prendere quello con la distanza minima più grande, guardando avanti 3 s;
  - se in 2 o più varianti **nessuna** scelta evita il contatto, la scena è impossibile per la barca M (non si gira abbastanza in 2 s): il collaudo chiede qualcosa che la fisica non permette. In quel caso la proposta sarà di **escludere dalla soglia le varianti impossibili**, dichiarandolo (cambio del metro, motivato dalla tabella), e non di toccare la guida.
- **Criteri del passo 2 (soglie nostre):** 81 almeno 9 su 10 sulle varianti 0-9 e **almeno 17 su 20 sulle varianti 10-29, mai guardate** (regola dei semi); 80, 82, 83 non peggiorano; nel torneo (`misura_manovre.py --lungo`, semi già usati per la 4B) i contatti con colpa dei rivali non crescono più del 10% e il tempo di bolina degli esperti non peggiora più di 2 s.
- **Costanti nuove:** l'orizzonte di 3 s (ipotesi nostra: il caso 81 nasce a 2-3,2 s); nessun'altra.
- **Fonti:** nessuna sul «come scarta un timoniere»; la velocità di accostata è quella del motore (barca M), non si tocca.
- **Rischi:** scarti più bruschi ovunque (si controlla con il torneo); impronte e confronti al bit da rifare (cambia la guida dei rivali).

### 13.2 Vento sporco

- **Cosa sappiamo:** nelle regate di Ale e Lucio (§15 di `PROPOSTA-AVVERSARI-BOLINA.md`) i rivali stanno nel vento coperto quasi sempre meno di 15 s a regata (massimo 69 s, una volta). Sulle regate lunghe simulate (§16-18) gli esperti perdono circa 10 s per bolina contro il «miope», e il vento coperto non è fra le cause trovate.
- **Proposta:** **chiudere anche il vento sporco** con la stessa condizione della bolina: si riapre se nelle vostre regate un rivale resta coperto a lungo (per esempio più di 30 s di fila) e si segna col tasto M.

### 13.3 Cosa serve da Ale

1. Via al **passo 1 del caso 81** (solo misura, leggero).
2. Ok a **chiudere il vento sporco** con la condizione scritta sopra.

### 13.4 Esito del passo 1 (27 novembre 2026; gioco 1.3.68 invariato; Chromium, varianti 0-9, i semi del collaudo)

- **Scena vera:** in tutte e 10 le varianti chi cede comincia a scartare dopo 0,27 s, gira al massimo a 25-28 °/s e **orza**: dal traverso (95° dal vento) a 67-73°, cioè prova a passare **davanti**. Riesce in 6 (incontro a 2,6-3,0 s), urta nelle 4 con l'incontro più vicino (0, 2, 6, 8: incontro a 2,0-2,3 s, contatto dopo 1,6-2,1 s).
- **Conto geometrico (approssimazione dichiarata: velocità costante, accostata a velocità costante, l'altra barca dritta; contatto dal contorno degli scafi del gioco, `hullOverlap`):** **poggiare** (passare di poppa) con la stessa velocità di accostata e lo stesso ritardo **evita il contatto in 10 varianti su 10**; orzare lo evita solo nelle 6 riuscite. Anche partendo subito (0 s) o girando a 30 °/s, orzare urta nelle stesse 4.
- **Quindi:** secondo la regola scritta al §13.1 vale il primo caso: **la scena è possibile, la guida sceglie male**.
- **Perché sceglie male (letto nel codice):** `cedeAvv1b` prova gli scarti a partire dalla rotta che la barca **vuole** (di bolina, verso la boa), non da quella che **ha**: dal traverso, «bolina + 28°» è un'orzata di 22°. E `passaggio()` controlla la nuova rotta come se la barca ci fosse già sopra, senza il tempo per girare: a 2 s dall'incontro l'orzata sembra passare a più di due lunghezze ma non c'è il tempo di farla.
- **Proposta per il passo 2 (aspetta il via):** in `passaggio()` la barca tiene la prua di adesso per il tempo dell'accostata (gradi da girare / **25 °/s**, la velocità misurata qui sul motore, non un'ipotesi) e poi segue la rotta nuova. Niente altro. Criteri quelli del §13.1 (81 almeno 9 su 10 e 17 su 20 sulle varianti 10-29 mai guardate; 80, 82, 83 non peggiorano; torneo: contatti con colpa dei rivali +10% al massimo, bolina degli esperti +2 s al massimo). Rischio in più: anche fuori dal caso 81 i rivali preferiranno passare di poppa quando l'incontro è vicino (è quello che chiede il regolamento a chi cede, quindi atteso).

### 13.5 Esito del passo 2 (27 novembre 2026; non adottato, `js/` identico alla 1.3.68 per la guida; prova in `sperimentale/caso-81/scafi-e-accostata.patch`)

- **Come proposto** (in `passaggio()` la prua di adesso per gradi/25 °/s, poi la rotta nuova): **81 resta 6 su 10**, stesse 4 varianti; 82 da 10 a 8 su 10 in una prima prova. Due cause trovate coi registri della variante 0: (a) gli scarti di chi cede partono dalla rotta voluta (bolina), quindi poggia al massimo a 110° dal vento; (b) la distanza fra i **centri** con l'accostata dà 2,6-2,8 m sia orzando sia poggiando: non distingue.
- **Aggiunte di Claude, dichiarate (oltre la proposta):** scarti anche dalla prua che ha; accostata continua a 25 °/s a passi di 0,1 s; distanza fra gli **scafi** (segmenti lunghi 4,2 m) per T_CEDE s. Risultato: **81 10 su 10, 82 8 su 10** (varianti 5 e 6, un contatto fra le due barche). Orizzonte 6 o 15 s e soglia di una o due lunghezze fra gli scafi (scelta dopo aver visto i numeri) non cambiano nulla. 82 peggiora: criterio non rispettato, non adottato. Varianti 10-29 e torneo non misurati.
- **Prossimo passo, se Ale lo vuole:** registri sulle varianti 5 e 6 del caso 82 con la patch, per capire perché le due barche si toccano.

### 13.6 Seconda prova (27 novembre 2026, pomeriggio; `js/` invariato, patch in `sperimentale/caso-81/scafi-e-accostata-v2.patch`)

- **Cause dell'82 trovate coi registri:** (a) variante 5: lo scarto «dalla prua che ha» si ricalcolava dalla prua del momento, quindi la barca continuava a poggiare (da −50° a −146° in un secondo); ora la base è la prua di quando lo scarto comincia (`cedeH`, come `rottaU` per chi ha la precedenza). (b) Variante 2: con due lunghezze libere fra gli scafi nessuna rotta bastava e si sceglieva sempre lo scarto più grande; ora basta **una lunghezza libera fra gli scafi** (scelta dopo aver visto i numeri, dichiarata). (c) Ancora variante 2: la Verde poggiava supponendo la Rossa dritta, ma la Rossa poggiava anche lei verso lo stesso punto; ora **chi sta cedendo si prevede mentre gira verso la rotta che ha scelto** (`ndCede`). La parte nuova vale solo dopo lo sparo.
- **Casi (Chromium), varianti 0-9 e 10-29 mai guardate:** 80 10/10 e 20/20 (minimo 131° dal vento, riferimento 106°); **81 10/10 e 20/20** (riferimento 6/10 e 8/20); 82 10/10 e 20/20 (riferimento 10/10 e 20/20); 83 10/10 e 20/20, «fuori 1» in tutte come il riferimento (il «fuori 0» del mattino era della prima variante, non del gioco).
- **Torneo** (`misura_manovre.py --lungo --conf m4`, semi 2201-2230, 90 regate per parte; metro dichiarato prima: lo strumento non dà la bolina degli esperti, si usa l'arrivo mediano dei rivali M4 con la stessa soglia di +2 s): contatti M3 **94 contro 94** (soglia +10%: passa); arrivo mediano **588,3 contro 589,9 s** (passa). **Fuori dai criteri, peggio:** contatti dopo una virata nei 5 s prima (M1) 14 contro 8; «coppie dopo il via» (un rivale che cede da 10 s a una barca entro 12,6 m e quasi parallela) **13 contro 4**. Non arrivati 104 contro 111, fuori linea 36 contro 37.
- **Stato:** i criteri scritti passano tutti, ma le coppie triplicano: non adottata finché non si guarda da dove vengono (sono il difetto della voce 3, visto giocando).

### 13.7 Terza prova (27 novembre 2026, sera; `js/` invariato, patch `sperimentale/caso-81/scafi-e-accostata-v3.patch`, misura `sperimentale/caso-81/misura_bolina_coppie.py`)

- **Da dove venivano le coppie in più della seconda prova:** quasi tutte in poppa e al lasco, stesse mure, 5-8 m fra i centri. Con «una lunghezza libera fra gli scafi» chi cede si accontentava dello scarto di 15° e restava lì, ancora «in cessione» (per la guida il pericolo vale fino a due lunghezze fra i centri). **Terza prova:** di nuovo due lunghezze fra gli scafi (scelta guardando i semi 2201-2230, dichiarata); restano la prua di base fissa e la previsione di chi cede.
- **Casi:** 80-83 verdi in Chromium (varianti 0-9 e 10-29) e in Firefox (0-9); 81 20/20 contro 8/20 del gioco.
- **Torneo lungo, 90 regate per parte, gioco → prova:**
  - semi 2201-2230 (scelta): contatti 94 → 94, coppie dopo il via 4 → 5, contatti dopo una virata 8 → 9, arrivo mediano 589,9 → 587,9 s;
  - semi 2231-2260 (conferma, mai guardati): contatti 122 → 119, coppie 11 → 11, contatti dopo una virata 5 → 3, **arrivo mediano 584,2 → 587,1 s (+2,9: fuori dalla soglia di +2)**.
- **Bolina degli esperti** (il criterio scritto al §13.1; misurata dopo aver visto fallire l'arrivo mediano, che avevo usato al suo posto: dichiarato). Tempo dallo sparo alla prima boa, semi pari, 135 rivali per parte: semi 2201-2230 **mediana 341,0 → 345,1 s (+4,2, fuori soglia)**, media +3,5; semi 2231-2260 mediana +1,2 (dentro), media +1,5. Principianti: −0,6 e +5,8 di mediana.
- **Esito:** i criteri su 80-83 e sui contatti passano, **la bolina degli esperti no** (+4,2 s in un gruppo su due) e l'arrivo mediano no sul gruppo di conferma. **Non adottata.** Passo dopo possibile: capire dove si perdono i 3-4 s (scarti più larghi quando si cede?).
