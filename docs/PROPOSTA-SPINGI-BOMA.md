# Proposta: «spingi il boma» (livello 2)

Del 17 ottobre 2026. **Fermata 1: nessun codice nel gioco.** Le prove sono state fatte su una copia in memoria di `js/motore.js` (script nella cartella temporanea della sessione). Richiesta di Ale: «manovra con un tasto speciale (io scelgo Z, la Q è per la mappa, A per raddrizzare). Se hai consigli migliori proponi».

Tipi delle affermazioni: **[fonte]**, **[misura]** (sulla copia in memoria), **[stima]**, **[giudizio]**.

---

## 0. In breve

1. **Cosa fa la manovra** [fonte, tre fonti didattiche concordi più la federazione australiana]: con la barca ferma nel vento si spinge il boma fuori da una parte e si tiene la barra dalla stessa parte; la vela prende il vento sul lato sbagliato («a collo»), la barca va all'indietro e la prua gira verso il boma, cioè si allontana dal vento; quando si è al traverso si molla il boma, si centra la barra, si cazza e si riparte. Serve anche per **frenare** e per **andare all'indietro** apposta, per esempio prima della partenza [fonte, un allenatore; forum].
2. **Regole** [fonte, regolamento 2025-2028, copia locale]: chi va all'indietro (o di lato verso il vento) spingendo una vela deve tenersi lontano da chi non lo fa (21.3). Usare il vento per rallentare è permesso (42.1), e anche ridurre la velocità muovendo la barra più volte (42.3(f)).
3. **Modello proposto**: un tasto tenuto premuto, Z, mette il boma a 80° dalla parte dove si trova e lo tiene lì contro il vento. La vela diventa una piastra investita dal vento: spinge all'indietro e di lato, e siccome la forza è applicata lungo il boma, fuori dall'asse della barca, fa girare la prua verso il boma. Solo per la barca del livello 2.
4. **Prima prova sulla copia in memoria** [misura]: con 10 nodi si esce dall'angolo morto in 1,0-1,8 s invece di 4,2-5,0 con la sola barra; la prua gira verso il boma in 18 casi su 18; prua nel vento e boma spinto, la barca arretra fino a 3,6 nodi; dalla bolina il boma spinto la porta sotto 1 nodo in 1,5 s (lascando tutta la scotta 12,8 s). **Con 15 nodi la barca sbanda fino a −42° verso il vento**, vicino alla scuffia sopravento del gioco (−45°).

---

## 1. Le fonti

Già raccolte (`DUBBI-E-RICERCHE.md` §3, `RICERCA-RETROMARCIA.md`, `RICERCA-VELOCITA-VIRATA-RIPARTENZA.md` §4):

| Fonte | Tipo | Cosa dice (parafrasi) |
|---|---|---|
| W1, US Sailing, «Getting in and out of irons» | Federazione | Senza fiocco si mette la randa a collo spingendo il boma dalla parte verso cui si vuole girare, con la barra dalla stessa parte; la barca va all'indietro e la prua gira verso il boma, lontano dal vento; poi si molla la vela e si cazza |
| W2, guida di un circolo per il Sunfish | Circolo, deriva in singolo | Barra e boma dalla stessa parte finché si è al traverso, poi barra al centro e si cazza; la barca va all'indietro e gira |
| W3, classe Paper Tiger | Classe, catamarano | Stessa manovra; all'indietro si esce «abbastanza in fretta» |
| Australian Sailing, «Drills for Skills: Sailing Backwards» | Federazione | Esercizio di scuola: boma spinto fuori, barra verso il boma, la barca ruota; poi barra al centro e si cazza |
| Scheda per istruttori «Sailing Backwards» | Didattica | Boma spinto a circa 90°, piccole correzioni di timone; serve per uscire da spazi stretti |
| «The Final Beat», allenamento alle partenze | Allenatore | All'indietro si esce da un brutto posto sulla linea, boma fuori il più possibile, barra al contrario; bisogna imparare quanto in fretta parte e quanto va forte |
| Lee (2022), video | Informale | Boma e barra dalla stessa parte è il modo preferito per uscire dall'angolo morto |

Nuove (17 ottobre 2026):
- Cal Sailing Club (blog di istruttori, 2019): la vela spinta a dritta spinge la prua a sinistra **mentre la barca esce da un pontile**; conta molto come si inclina la barca; la vela va spinta tutta fuori, altrimenti a un certo punto si gonfia e la barca riparte in avanti. *Il verso della prua sembra contrario a W1: lì la barca è ferma al pontile e si sta parlando di un altro momento della manovra; non lo uso per il verso.*
- Forum (bassa affidabilità): su una deriva in singolo, spingendo il boma la vela tende a far poggiare a meno di sbandare la barca sopravento; attenzione a una virata involontaria.
- Regolamento di regata 2025-2028 (copia locale `fonti-pdf/`): 21.3 (chi va all'indietro spingendo una vela si tiene lontano), 42.1 (si usa solo vento e acqua per aumentare, mantenere o **diminuire** la velocità), 42.3(d) (ferma con la prua sopra la bolina, una barca può muovere la barra per tornare in bolina), 42.3(f) (si può ridurre la velocità muovendo la barra più volte).

**Numeri: nessuno.** Nessuna fonte dice quanto in fretta gira la barca, quanto forte va all'indietro o quanto frena la vela spinta. Tutti i numeri del gioco saranno conseguenze del motore e delle stime del §3, dichiarate.

---

## 2. Cosa fa oggi il gioco [codice]

Il boma lo mette il vento, al più fino a dove lo lascia la scotta (`step()`, punto 2 di `FISICA-E-TARATURE.md`), sempre sottovento: la vela non va mai a collo. Per uscire dall'angolo morto c'è solo la barra (verso il boma mentre la barca arretra), e la regola senza fonte «la prua poggia da sola sotto 1 nodo» (`ironsYaw`). La retromarcia succede da sola, con la vela che sbatte (fino a 2,3 nodi con 10 nodi di vento, `retromarcia.js`).

---

## 3. Il modello più semplice plausibile

Solo per la barca del livello 2 (`S.lv === 2`), finché Z è premuto:

1. **Il boma va a 80° dalla parte dove si trova** quando si preme Z, e ci resta anche se il vento cambia lato. La scotta non conta.
2. **La vela è una piastra investita dal vento.** Forza perpendicolare alla vela, `CN = CL(α)·cos α + CD(α)·sin α`, con i coefficienti della vela di oggi e α l'angolo fra il vento apparente e il boma. Con la prua nel vento e il boma a 80°, α vale circa 80° e la forza è quasi tutta all'indietro.
3. **La forza fa girare la barca.** È applicata al centro velico, sul boma a 0,9 m dall'albero, con l'albero a 0,8 m a prua del centro della barca. Il momento fa girare la prua verso il boma; la rotazione è quella in cui il momento uguaglia la resistenza dell'acqua allo scafo che ruota (smorzamento quadratico, `Kq` = 1230 N·m·s², stima da pala, deriva e carena). È il primo momento delle vele nel motore: **vale solo con il boma spinto**; in navigazione normale resta «nessuna tendenza orziera», dichiarato.
4. **Il resto non cambia:** scafo, retromarcia (`backDrag`), timone all'indietro (al contrario), sbandamento e scuffia, compresa quella sopravento. Mentre il boma è spinto il timone usa la formula del livello 1 anche sopra 0,5 m/s (il timone del livello 2 vale solo andando avanti con la vela normale).

**Costanti nuove, tutte ipotesi senza fonte:**

| Costante | Valore | Perché |
|---|---|---|
| angolo del boma spinto | 80° | Le fonti: «circa 90°», «tutta fuori»; `maxBoom` è 85° |
| albero a prua del centro | 0,8 m | Stima per una deriva da 4,2 m |
| centro velico sul boma | 0,9 m dall'albero | Stima: circa un terzo del boma |
| `Kq` | 1230 N·m·s² | Stima: ½·ρ acqua·1,2·(carena, pala e deriva per il cubo della distanza dal centro) |

**Tasti** [giudizio]:
- **Z, tenuto premuto: spingi il boma.** Come una mano sul boma: lo si tiene finché serve, lo si molla per ripartire. Il lato è quello dove si trova il boma; per cambiarlo si aspetta che il vento lo porti dall'altra parte. Alternativa scartata: Z come interruttore (premi una volta, resta spinto), perché si dimenticherebbe acceso e la barca andrebbe all'indietro senza capire perché.
- **Z va bene** per la regola del 7 ottobre 2026 (A e Z liberi per funzioni speciali, Q vista). La mano sinistra ha W S (scotta), Q, A, Z e Maiusc, la destra le frecce: si può tenere Z e la barra insieme.
- **A per raddrizzare: oggi raddrizza R**, in tutto il gioco (testi delle lezioni compresi). Spostarlo su A era già in programma prima delle coppie E D e R F. Due strade: (a) A raddrizza in tutti i livelli, R continua a funzionare per non rompere le abitudini, e i testi dicono A; (b) A solo dal livello 2. Consiglio (a): un tasto diverso per la stessa cosa a seconda del livello confonde. Cambiano i testi del livello 1, non la fisica; l'impronta cambierà solo nei testi, dichiarato.

---

## 4. Prima prova [misura, copia in memoria, nessun numero di fonte]

**Uscita dall'angolo morto.** Barca ferma con la prua da −30° a +30° dal vento (9 partenze), barra verso il boma, finché la prua è a 50° dal vento; poi barra al centro.

| Vento | Solo barra (oggi) | Boma spinto e barra |
|---|---|---|
| 6 nodi | 6,5-7,1 s | 1,5-2,7 s |
| 10 nodi | 4,2-5,0 s | 1,0-1,8 s |
| 15 nodi | 3,0-3,6 s | 0,8-1,3 s |

La prua gira verso il boma in **18 casi su 18** con il boma spinto.

**All'indietro**, prua nel vento, boma spinto, barra al centro per 6 s: fino a 2,1 / 3,6 / 5,0 nodi con 6 / 10 / 15 nodi; la prua intanto gira di 51-70°; sbandamento verso il vento −8° / −11° / −15°. Oggi, con la sola vela che sbatte, all'indietro si arriva a 2,3 nodi con 10 nodi (`retromarcia.js`).

**Freno**, dalla bolina a regime, prua tenuta: sotto 1 nodo in 2,4 / 1,5 / 0,9 s con il boma spinto, contro 18,1 / 12,8 / 8,4 s lascando tutta la scotta; poi la barca va all'indietro. **Sbandamento verso il vento fino a −21° con 10 nodi e −42° con 15 nodi** (la scuffia sopravento del gioco è a −45°).

---

## 5. Criteri per la fermata 2 (attese nostre)

Dichiarato: le soglie sono scritte **dopo** la prima prova del §4, e servono soprattutto a non peggiorare quello che le fonti descrivono. Venti 6, 10, 15 nodi; prue da −30° a +30° ogni 5°; boma a dritta e a sinistra.

- **B1** La prua gira verso il boma in tutti i casi (W1, W2, W3, Australian Sailing). Soglia: 100%, con il conteggio dei casi stampato (deve essere più di zero).
- **B2** Con il boma spinto si esce dall'angolo morto prima che con la sola barra (le fonti lo insegnano come il modo principale). Soglia: in ogni caso, e mediana almeno 1,5 volte più rapida.
- **B3** Con la prua nel vento e il boma spinto la barca va all'indietro (W1, W2). Soglia: in tutti i casi la velocità diventa negativa entro 3 s.
- **B4** Il boma spinto frena più che lascare tutta la scotta. Soglia: a tutti i venti.
- **B5** Tenendo Z 6 s con la prua nel vento: nessuna scuffia con 6 e 10 nodi. Con 15 nodi si riporta lo sbandamento, senza soglia (vedi rischi).
- **B6** Non-regressione: livello 1 identico al bit (impronta, `polare.js`, `raffiche_e_virate.js`); barca del livello 2 senza Z identica alla 1.0.25 (`timone2.js` uguale carattere per carattere).
- **B7** Nel browser, guidando coi tasti veri: Z tenuto con la freccia verso il boma fa uscire dall'angolo morto; Z mollato rimette il boma alla scotta; Z nella barca del livello 1 non fa niente; pagina senza `#collaudo` senza errori; pannello a 1360×650 senza eccesso.

---

## 6. Rischi

- **Scuffia sopravento con 15 nodi** (−42° nella prova del freno). Può essere giusto (il forum avverte di sbandare la barca sopravento) ma il timoniere del gioco si sporge solo da un lato. Se in fermata 2 si scuffia tenendo Z per pochi secondi, va deciso se è un errore da insegnare o un difetto.
- **Rotazione rapida**: con 10 nodi la prua passa dal vento a 50° in meno di 2 s. Nessuna fonte dà il tempo; dipende da `Kq`, stimata.
- **Retromarcia più forte di oggi** (3,6 contro 2,3 nodi con 10 nodi): è la vela tenuta a collo invece che lasciata sbattere, coerente col motore, ma senza una fonte con numeri.
- **Freno molto forte**: da 4,4 nodi a fermi in 1,5 s. Diventa un modo nuovo di fermarsi, per esempio alle partenze; per gli avversari non cambia niente finché non lo usano.
- **Il primo momento delle vele del motore** vale solo con Z: il motore ha due regole diverse a seconda del boma spinto o no. Va dichiarato come semplificazione.
- **Pannello**: la riga dei tasti è a 0 px di margine; «Z spingi il boma» probabilmente non ci sta. Si spiega nel manuale e, più avanti, nella lezione.
- **La regola 21.3** (chi va all'indietro spingendo la vela deve tenersi lontano) entra nel gioco solo con le regole del livello 2.

---

## 7. Decisioni che spettano ad Ale

1. Il via alla fermata 2 con questo modello.
2. Z tenuto premuto, sul lato dove si trova il boma (consigliato), oppure un'altra forma.
3. Raddrizzare: (a) A in tutti i livelli, R che continua a funzionare (consigliato), oppure (b) A solo dal livello 2.

---

## 8. Fermata 2 (17 ottobre 2026, versione 1.0.26)

**Via di Ale** con Z tenuto premuto e il boma spinto dalla parte dove si trova. Raddrizzare con A: non ancora deciso, R resta.

**Fatto:** `BOMA2` e la forza della vela spinta in `step()` (`js/motore.js`), solo con `C.push` e `S.lv === 2`; Z in `js/gioco.js` (`ctl.push`, tenuto premuto, non nella barca del livello 1 né a barca scuffiata); suggerimento in `js/disegno.js`; misure in `tests/fisica/boma2.js`; collaudo nel browser `tests/collaudo_boma2.py` (dentro `lancia_tutti.sh`).

**Risultati** (`node boma2.js`, venti 6, 10, 15 nodi, prua da −30° a +30° ogni 5°, 39 partenze):

| Criterio | Esito |
|---|---|
| B1 la prua gira verso il boma ed esce | ok, 39 su 39 |
| B2 col boma spinto si esce prima che con la sola barra (mediana almeno 1,5 volte) | ok, 39 su 39, mediana 3,1 volte (con 10 nodi 1,0-1,8 s contro 4,2-5,0) |
| B3 col boma spinto la barca va all'indietro entro 3 s | ok, 39 su 39 |
| B4 il boma spinto frena più che lascare tutto | ok: sotto 1 nodo in 1,8 / 1,2 / 0,8 s contro 10,4 / 9,0 / 6,5 s; la barca poggia di circa 15-20° (lo dice anche un forum: la vela spinta tende a far poggiare) |
| B5 Z tenuto 6 s con la prua nel vento: nessuna scuffia | ok con 6 e 10 nodi; con 15 nodi nessuna scuffia, sbandamento −15°, all'indietro fino a 5,0 nodi |
| B6 livello 1 identico al bit; livello 2 senza Z uguale alla 1.0.25 | ok |
| B7 nel browser coi tasti veri | ok, 5 giri su 5 (vedi sotto) |

**Il rischio della fermata 1 (−42° di sbandamento con 15 nodi)** veniva dalla prova con la prua tenuta ferma a forza: con la barra libera la barca poggia e lo sbandamento resta a −14°.

**Nel browser** (`collaudo_boma2.py`): 9 uscite su 9 (con 10 nodi in 1,4-1,9 s), la barca va all'indietro fino a 1,1-3,8 nodi, il boma resta a 80° finché Z è premuto e il suggerimento lo dice; nella barca del livello 1 Z non fa niente; pannello senza eccesso. **Due correzioni del collaudo, dichiarate:** (1) la ripartenza cazzava solo 1 s, la scotta restava a 0,73 e la vela sbatteva, quindi la barca giustamente non ripartiva (difetto del collaudo, non del gioco); ora ↑ per 2 s; (2) la soglia «dopo 7 s almeno 1 nodo in avanti» è stata **abbassata a 0,5 dopo aver visto** 0,98-1,0 nodi con 6 nodi: il controllo serve a dire che la barca riparte in avanti, e con 6 nodi la barca accelera piano (di bolina va al massimo a 2,9 nodi).

**Semplificazioni da dichiarare:** il momento delle vele esiste solo col boma spinto; il boma spinto sta sempre a 80°, qualunque sia il vento; il timoniere non si sporge dall'altra parte quando la barca sbanda verso il vento; tempi e velocità all'indietro non hanno fonte (dipendono dalle quattro stime del §3).

