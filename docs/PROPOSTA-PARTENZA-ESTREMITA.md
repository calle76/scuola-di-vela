# Proposta: barche che in attesa scivolano oltre l'estremità sinistra della linea (8 novembre 2026, notte)

Voce 2 di `DA-FARE.md`; osservazioni 93, 96, 100 di `OSSERVAZIONI-GIOCANDO.md`. **Fermata 1: nessun codice scritto.** Fermata 2 (9 novembre): **non adottata**, la conferma non passa sui contatti (§9).

## 1. Era già stato risolto?

In parte.
- **1.1.1** (`PROPOSTA-PARTENZE-1B.md`): le barche che non partivano affatto (25 → 0 su 1440).
- **1.2.15** (fetta 4 della Deriva): al via, chi taglierebbe oltre l'estremità sinistra stringe o cambia mure. Barche fuori linea 62 → 24.
- **29 ottobre** (`PROPOSTA-DERIVA-ATTESA-1B.md`): la deriva **durante l'attesa** fu provata con 8 varianti e nessuna fu adottata. Quella che toglieva le uscite raddoppiava le partenze anticipate. Restava da provare: «far sì che la barca in attesa non scivoli».

Quello che vedi tu è proprio il pezzo rimasto: l'attesa.

## 2. Cosa succede (misurato sulle 14 regate registrate dalla 1.2.15, 42 partenze di avversari)

- Nessun taglio valido cade fuori dalla linea (0 su 42): il gioco li fa rientrare. Il danno è il **tempo**.
- **5 barche su 42 sono oltre l'estremità sinistra allo sparo** (x da -41,5 a -52, l'estremità è a -35): 17:25 Rossa e Verde, tagliano a 23,7 s; 22:14 Rossa e Blu, a 7,4 e 10,2 s, con 4 richiami; 9:10 Verde, quasi (-33,9). Una partenza normale taglia entro 1-3 s.
- **Quasi tutti partono nella metà sinistra:** 30 tagli su 42 hanno x sotto -10.
- Nell'ultimo minuto le barche in attesa scivolano verso sinistra di circa 10 m (da -60 a -5 s), poi altri 5-10 m nella partenza di bolina.

## 3. Perché (letto nel codice, `js/regate.js`, `aiControl`)

1. **L'attesa si ferma dove capita.** La barca si avvicina al suo punto d'attesa (`waitX`). Ma appena la simulazione dell'abbrivio (`glideY`) dice che si fermerebbe a meno di due lunghezze dalla linea, smette di andare e aspetta (`hold`), **ovunque sia di lato**. Da lì, mure a dritta e vela che sbatte, scivola verso sinistra. Nessuna regola la riporta indietro finché non parte. Alle 22:14 Blu era già a -27 a un minuto dal via, a -34 a 30 s, a -38 a 8 s.
2. **Al via, chi è già fuori va ancora più fuori.** La fetta 4 le fa cambiare mure verso il centro. Ma ferme non riescono a virare, e la regola «prima prendi abbrivio» le fa poggiare a 95° dal vento: corrono ancora più a sinistra (Blu da -38 a -52) prima di virare. Alle 22:14 per Rossa si aggiunge un cedere a Blu, che la fa poggiare anche lei.

## 4. Modello più semplice (due parti, solo nella guida degli avversari; la barca non cambia)

**A. Riposizionarsi in tempo.** Mentre aspetta e manca più di `T_RIPOS` secondi al via: se il punto dove taglierebbe la linea partendo adesso (lo stesso calcolo della fetta 4: x − tan(bolina + 4°) × distanza dalla linea) è più a sinistra di `X_RIPOS`, la barca smette di aspettare e va al suo punto di ritrovo (`yF`, 25 m dietro la linea, già spostato a destra). Ci va con la guida generale, che sa poggiare, abbattere e risalire. Poi rifà l'avvicinamento come all'inizio. È quello che fa un timoniere che si accorge di essere scivolato verso la boa: ci gira dietro e torna su.

Differenza con la prova del 29 ottobre: allora il ritorno scattava tardi, fino a 12-25 s dal via, e la barca rientrava di corsa sulla linea (partenze anticipate dal 9,6% al 20-27%). Qui scatta solo con tempo sufficiente (`T_RIPOS`) e guarda il punto di taglio previsto, non la distanza dal punto d'attesa.

**B. Al via, chi è già fuori gira in poppa invece di poggiare verso fuori.** Se allo scadere la fetta 4 chiede di cambiare mure e la barca è troppo lenta per virare, invece di poggiare a 95° mure a dritta, cioè verso fuori, poggia fino alla poppa e abbatte, poi risale mure a sinistra verso il centro. Si fa solo se A da sola non basta (si misura prima A, poi A+B).

**Cosa non si tocca:** la fisica (impronta dell'1b al bit, `polare.js`, `raffiche_e_virate.js`), chi cede e le regole, l'aggressiva, i giri di penalità, il giocatore.

**Fuori da questa proposta:** le osservazioni 101 (Blu che poggia all'ultimo addosso ad Ale) e 102 (virate subito dopo il via sulla rotta di una mure a dritta). Nascono dal cedere e dallo scarto dell'ultimo momento (`cedeAvv1b`), non dall'attesa: le sposto alla voce delle manovre addosso a una vicina (osservazioni 105-106).

## 5. Costanti nuove (ipotesi nostre)

- `X_RIPOS`: quanto a sinistra può cadere il taglio previsto prima di riposizionarsi. Da scegliere fra −(35 − 2), −(35 − 6) e −(35 − 10) m.
- `T_RIPOS`: secondi minimi al via per riposizionarsi. Da scegliere fra 30, 40 e 50 s (girare dietro e risalire dovrebbe costare 20-30 s, da misurare).
- Per B nessuna costante nuova: la poppa e l'abbattuta usano gli angoli già in uso (`ai.down`, 172°).

Scelta sui semi 601-640 (mai usati), confermata sui semi 641-680 (mai guardati), come vuole la regola dei semi.

## 6. Criteri (soglie nostre, scritte prima di misurare)

Misura: regate di avversari col giocatore fermo dietro la linea (come `collaudo_partenze`, anticipi allo sparo), bastone, raffiche e salti, principianti ed esperti, 1, 3 e 5 minuti. Per ogni avversario si misura: x allo sparo, istante del taglio valido, partenza anticipata sì/no, contatti fra -60 s e +20 s. Riferimento: la 1.2.18 sugli stessi semi.

1. **Oltre l'estremità allo sparo** (|x| > 35 m): almeno dimezzate rispetto al riferimento, e al massimo il 3% delle partenze.
2. **Partenze anticipate allo sparo:** al massimo +2 punti percentuali sul riferimento. È il criterio su cui cadde la prova del 29 ottobre.
3. **Ritardo al taglio:** la mediana non peggiora più di 1 s; i tagli dopo 10 s non aumentano.
4. **Contatti prima del via e nei primi 20 s:** al massimo +10%.
5. **Riposizionamenti:** si contano. Il controllo vale solo se ce ne sono stati almeno 10 nei semi di scelta: con zero il criterio 1 non misurerebbe niente.
6. **Non-regressione:** `polare.js` e `raffiche_e_virate.js` identici, `impronta1b.js` al bit. `collaudo_partenze` e `collaudo_regate` come prima.
7. **Rigiocate le regate di Ale** delle 17:25 e delle 22:14 (`rigioca_regata.py`, 20 semi ciascuna): si riportano quante barche sono oltre l'estremità allo sparo, prima e dopo. Senza soglia: è un controllo sul caso vero.

Se nessuna combinazione passa 1-4 sui semi di scelta, non si adotta nulla e si riporta così. Restano due strade: «nella Scuola qualche avversario parte largo, e lo diciamo», oppure attese che alternano le mure.

## 7. Rischi

- Il riposizionamento fa passare le barche in mezzo al gruppo, mure a sinistra: più incroci, e quindi più contatti (criterio 4).
- Una barca che si riposiziona tardi arriva in ritardo al via. È peggio di un'uscita? Lo dice il criterio 3.
- Con il vento che gira (salti) il taglio previsto cambia: una barca potrebbe riposizionarsi due volte. Si contano anche questi casi.
- B tocca la stessa regola dell'abbrivio che nella 1.1.1 aveva tolto le barche ferme: si misurano anche le barche non partite entro 60 s (devono restare 0).

## 8. Costo

Due sessioni: misura del riferimento e di A con le combinazioni di costanti; poi, se serve, B e la conferma. Collaudi: quelli del punto 6, e alla fine `tests/lancia_tutti.sh --veloce` sul PC di Ale.

## 9. Esito della fermata 2 (9 novembre 2026, notte): non adottata

Via di Ale l'8 sera. Misurato con `tests/misura_partenza_estremita.py`: 720 regate e 2160 partenze di avversari per gruppo di semi. Solo la parte A: B non è servita, perché A da sola passava la scelta.

**Scelta, semi 601-640.** Il riferimento è la 1.2.18:

| | oltre l'estremità | anticipate | mediana taglio | dopo 10 s | contatti | riposizionamenti | non partite |
| --- | --- | --- | --- | --- | --- | --- | --- |
| riferimento | 287 (13,3%) | 36 (1,7%) | 2,10 s | 294 | 298 | 0 | 5 |
| −33 / 30 s | 42 | 45 (2,1%) | 1,98 | 184 | 310 | 347 | 5 |
| −33 / 40 s | **65 (3,0%)** ✗ | 36 | 2,00 | 183 | 316 | 278 | 4 |
| −33 / 50 s | **96 (4,4%)** ✗ | 35 | 2,02 | 195 | 318 | 250 | 4 |
| −29 / 30 s | 29 | 42 (1,9%) | 1,95 | 160 | 295 | 465 | 6 |
| −29 / 40 s | 39 | 30 (1,4%) | 1,95 | 167 | 301 | 356 | 5 |
| −29 / 50 s | 56 | 31 | 1,98 | 183 | 314 | 313 | 5 |
| −25 / 30 s | 33 | 54 (2,5%) | 2,03 | 154 | 318 | 671 | 8 |
| **−25 / 40 s** | 35 (1,6%) | 36 (1,7%) | 1,93 | 152 | 302 | 426 | 5 |
| −25 / 50 s | 34 | 37 | 1,93 | 163 | 306 | 385 | 5 |

Le soglie, ricavate dal riferimento: oltre l'estremità ≤64, anticipate ≤3,7%, mediana ≤3,10 s, dopo 10 s ≤294, contatti ≤327, riposizionamenti ≥10. Sette combinazioni su nove passano. Ho scelto **X_RIPOS = −25, T_RIPOS = 40**: è quella che toglie più uscite senza peggiorare né le anticipate né le barche non partite. La regola di scelta fra le combinazioni che passano non era scritta nella proposta, quindi la dichiaro qui.

**Conferma, semi 641-680 (mai guardati):**

| | oltre l'estremità | anticipate | mediana | dopo 10 s | contatti | non partite |
| --- | --- | --- | --- | --- | --- | --- |
| riferimento 1.2.18 | 316 (14,6%) | 35 (1,6%) | 2,12 s | 289 | 272 | 7 |
| −25 / 40 s | 41 (1,9%) ✓ | 31 (1,4%) ✓ | 1,95 ✓ | 144 ✓ | **313 (+15,1%)** ✗ | 8 |

**Criterio 4 non passato** (soglia +10%, cioè 299): non si adotta, e il gioco resta la 1.2.18. Due cose da sapere:
- Fra i due gruppi di semi il riferimento passa da 298 a 272 contatti, cioè il 9%: il rumore è grande quanto la soglia. Il «+15%» va però letto come esce, e la soglia non si cambia.
- I tempi al taglio migliorano: chi era fuori allo sparo perdeva secondi, e i tagli dopo 10 s si dimezzano (289 → 144).

Non fatti, perché servivano solo per l'adozione: il criterio 7 (rigiocate 17:25 e 22:14) e i collaudi del criterio 6. Il codice resta spento e fuori dal gioco in `sperimentale/partenza-ripos/ripos-1.2.18.patch` (si applica sulla 1.2.18 con `git apply`; `__sv.ripos(x, t, poppa)` lo accende nel collaudo).

**Strade per Ale:**
1. Lasciare così.
2. Rimisurare i contatti con più semi (per esempio 80 per gruppo) per capire se il +15% è rumore. Sarebbe una proposta nuova con soglie nuove, scritte prima.
3. Un riposizionamento che eviti chi ha già precedenza mentre passa in mezzo al gruppo, per ridurre i contatti: sarebbe la causa del rischio 1 del §7.

## 10. Strada 2: rimisurare i contatti con più semi (9 novembre 2026, mattina; Ale: «fai la strada 2»)

Domanda: il +15% di contatti della conferma è un effetto vero o rumore? Stessa correzione del §9 (X_RIPOS −25, T_RIPOS 40 s, senza B), nessuna costante cambiata.

**Misura.** Semi nuovi **681-760** (80 semi, mai usati): 1440 regate per il riferimento 1.2.18 e 1440 con la correzione, stesse condizioni del §6. In più, per ogni regata si salvano i contatti, così da confrontare regata per regata (stesso seme, stessa regata) e calcolare l'intervallo al 95% della differenza di contatti (bootstrap sui semi, 10 000 ricampionamenti).

**Criteri (soglie scritte prima di misurare, gli stessi del §6):**
1. Oltre l'estremità ≤3% e almeno dimezzate; 2. anticipate ≤ +2 punti; 3. mediana del taglio ≤ +1 s e tagli dopo 10 s non in aumento; 4. **contatti ≤ +10%** sul riferimento degli stessi semi.

**Decisione:** se 1-4 passano sui semi 681-760, la correzione si adotta (versione 1.2.19, con i collaudi del criterio 6 e le rigiocate del criterio 7). Altrimenti resta fuori. L'intervallo al 95% e il totale dei tre gruppi di semi (601-760, 160 semi) si riportano ma non decidono.
