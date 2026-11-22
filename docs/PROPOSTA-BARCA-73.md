# Proposta: correggere la barca secondo lo studio (voce 73)

*22 novembre 2026 (Opus), **fermata 1**: solo proposta, `js/` non toccato. Base: `STUDIO-BARCA.md` (motore della 1.3.40, uguale alla 1.3.43). Metro prima/dopo: `tests/fisica/studio_barca.js`. Misura nuova di questa fermata: `tests/fisica/misura_scotta_vento_forte.js` (Node, 2 s, nessun numero a caso: un giro basta).*

Lo studio ha trovato tre cose. Qui sono **tre passi separati**, ognuno col suo via. Ordine consigliato: **A → B → C** (A è piccolo e non tocca il motore; B è il cambio grosso; C è solo misura).

| Passo | Cosa | Tocca il motore? | Peso |
| --- | --- | --- | --- |
| A | Vento forte: la **regola della scotta** dei rivali (e del metro) lasca quando la barca sbanda | **No** | piccolo |
| B | **Virata rollata**: un gesto del giocatore, con la fisica vera (vento apparente in più quando si raddrizza) | **Sì** | grosso |
| C | Bolina lenta con poco vento: **solo diagnosi**, niente correzione finché non si trova la causa | No | medio, solo misura |

---

## 1. Cosa dice lo studio (riassunto)

- Virata 0,7-0,9 lunghezze (L) con 10-14 nodi; **0,7 L anche con 4-8 nodi, dove F106 dice 0 con la virata rollata in acqua piatta**.
- Sopra 16-18 nodi: con la sola freccia la virata non riesce a 18 nodi; a 20 nodi con la regola di scotta la barca non va di bolina.
- Bolina con 6 nodi −20% contro F17 (Day), sulla rotta vera. Causa non trovata due volte (`archivio/PROPOSTA-BOLINA.md` §6 e §11; decisione di Ale del 17 ottobre: «limite noto»).

## 2. Una scoperta di questa fermata: il vento forte non è colpa del motore

Misura nuova (`misura_scotta_vento_forte.js`): bolina a 45°, poi virata col timoniere pulito, due regole di scotta.

| vento | regola di oggi (boma = apparente − 17°): velocità di bolina | virata, sola freccia | regola con lasca sullo sbandamento: velocità di bolina | virata, sola freccia |
| --- | --- | --- | --- | --- |
| 14 | 5,40 nodi | riesce (3,2 s) | 5,40 nodi | riesce (3,6 s) |
| 16 | 5,07 | riesce (3,9 s) | 5,60 | riesce (3,7 s) |
| 18 | 4,62 | **non riesce** | 5,77 | riesce (3,9 s) |
| 20 | 0,97, **scuffia** | non riesce | 5,87 | riesce (5,0 s) |

«Regola con lasca» = quella che il gioco ha già nella scotta automatica del giocatore (`autoSheet(true)`, `js/gioco.js`: +1,5° di boma per ogni grado di sbandamento oltre 12°; ipotesi nostre della 1.0.73).

**Perché a 18 nodi non riesce** (traccia passo per passo, `node misura_scotta_vento_forte.js trace`): la barca passa il vento, ma con la vela cazzata dalla regola sbanda subito di 25-35°; lo sbandamento la fa orzare (regola della 1.0.46, F4) più di quanto la pala riesca a farla poggiare, la pala stalla e la barca resta a 30-35° dal vento a circa 1 nodo, per sempre. Una persona vera lascerebbe per poggiare. Con la lasca sullo sbandamento la barca poggia e riparte.

Con la lasca la bolina resta quasi ferma da 14 a 20 nodi (5,4 → 5,9), che è proprio la forma di Day (VMG quasi piatta sopra 12 nodi). **Il motore va bene; è la regola di scotta che non basta.**

## 3. Passo A — scotta che lasca quando la barca sbanda (senza toccare il motore)

**Cosa cambia:**
1. `sheetFor` dei rivali (`js/regate.js`): boma = apparente − 17° + errore del rivale **+ 1,5° per grado di sbandamento oltre 12°** (la stessa regola della scotta automatica del giocatore, nessuna costante nuova).
2. Il metro (`studio_barca.js`): il timoniere pulito usa la regola con lasca; le tabelle di prima restano scritte accanto.
3. Il suggerimento della vela (`js/disegno.js`, «cazzando un po' vai più veloce»): non deve dirlo quando la barca è sbandata oltre 12° (da controllare in fermata 2; se lo dice già bene, non si tocca).

**Criteri (soglie nostre, scritte ora):**

| # | Criterio | Soglia |
| --- | --- | --- |
| A1 | Sotto 12 nodi niente cambia | `studio_barca.js` parti A-B con 4-12 nodi uguali al centesimo (la lasca parte solo oltre 12° di sbandamento; di bolina a 12 nodi la barca sbanda 5-8°) |
| A2 | Vento forte | virata riuscita con la sola freccia con 14, 16, 18, 20 nodi; nessuna scuffia a regime fino a 20 |
| A3 | Rivali nelle regate | torneo e regate coi semi fissi: scuffie dei rivali **non in aumento**; arrivi e penalità riportati (cambiano solo nelle raffiche forti) |
| A4 | Non-regressione | `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` **identici** (il motore non cambia) |

**Fonti:** che in raffica si lasca per tenere la barca piatta è già nelle lezioni (lezione «Assorbire una raffica»); il numero 1,5°/grado oltre 12° è un'ipotesi nostra (1.0.73), dichiarata.
**Rischio:** i rivali nelle raffiche di 17-19 nodi (le regate a 12 nodi con le raffiche rare ci arrivano, voce 78) diventano un po' più veloci: cambiano le classifiche dei semi fissi. Collaudi da rilanciare: `collaudo_torneo` (C11 noto a parte), il guardiano degli avversari, uno per volta col freno.
**Modello:** Opus (guida dei rivali), lavoro breve.

## 4. Passo B — virata rollata

### 4.1 Cos'è (fonti)
- **F106** (Dellenbaugh): con poco vento e acqua piatta una virata rollata può non perdere niente; con vento medio circa 0,5 L. Stima di un allenatore: **solo confronto, non taratura** (come nello studio).
- **Regolamento, regola 42.3(b)** (`fonti-pdf/RRS-2025-2028-World-Sailing.pdf`, World Sailing 2025-2028): l'equipaggio può spostare il peso per accentuare il rollio che aiuta a girare in virata, **purché subito dopo la virata la barca non sia più veloce di quanto sarebbe stata senza virare**. È il limite naturale: la rollata riduce la perdita, non regala velocità.
- **Il gesto (trovato il 22 nov): F107 e F108**, due pagine del sito della classe: orzata lenta, al passaggio del vento la vela passa e il timoniere va sull'altro lato lasciando sbandare molto la barca (con la scotta lascata, F108), poi la raddrizza nell'uscita e ricazza; con poco vento si sbanda di più e l'uscita «dà accelerazione», con vento forte non si sbanda (F107). **Nessuna delle due dà numeri** (gradi, secondi, lunghezze): le costanti del §4.2 restano ipotesi nostre. Una terza pagina (North Sails) parla di una barca a due vele e non si usa; una quarta (Seabreeze) non si è lasciata leggere (403). La regola 42 nelle due pagine non è citata.

### 4.2 Il modello più semplice plausibile
Il guadagno vero della rollata è che, raddrizzando di colpo la barca sul nuovo bordo, l'albero si muove verso il vento: la vela «sente» più vento apparente per un attimo e spinge (è lo stesso effetto per cui la regola 42 vieta il pompaggio ripetuto).

1. **Sbandamento con un lato fisso.** Oggi `S.heel` è contato «verso sottovento»: quando il vento passa la prua il riferimento cambia lato di colpo. Una barca rollata di 20° verso il vecchio sopravento è, dopo il passaggio, sbandata di 20° verso il **nuovo sottovento**; il motore invece la tiene a −20°, cioè sbandata verso il nuovo sopravento. Nelle virate normali lo sbandamento al passaggio è circa 0 e non si vede; con la rollata conta. Correzione: sbandamento e sua velocità conservati nel lato fisico della barca (dritta/sinistra) quando cambia il lato del vento. **Cambia il motore** (vedi §4.5).
2. **Vento apparente della rollata.** La vela si muove di lato alla velocità `velocità di rollio × zCE` (zCE = 2,0 m, la costante che c'è già); questa velocità si somma al vento apparente della vela. Nessuna costante nuova per l'effetto: è geometria.
3. **Il gesto del giocatore (tasto `X` tenuto premuto; decisione di Ale del 22 nov):** si preme quando la prua passa il vento e il timoniere fa inclinare la barca sul nuovo sottovento (fino a 20°); si lascia quando la vela si gonfia sul nuovo lato e il timoniere la raddrizza con un colpo di peso (in 0,8 s). **Costanti nuove, ipotesi nostre fissate prima di misurare:** 20° e 0,8 s (F107-F108 non danno numeri). La scotta resta al giocatore: non si chiede di lascare e ricazzare (F108 lo dice; semplificazione dichiarata). Sequenza con 6 nodi: freccia a 0 s, X giù a circa 2 s, X su a circa 3,5 s, barra al centro a circa 5 s. X lasciata troppo presto: nessuna spinta; tenuta troppo a lungo: barca inclinata che orza e rallenta. È una capacità del giocatore, non un aiuto: non si spegne (principio 3 vale per gli aiuti).
4. **Rivali:** in questo passo **non rollano** (si vede quanto vale il gesto per il giocatore); la rollata dei rivali va con il loro lavoro (voci 4B, 2, 3: «prima la barca, poi i rivali»). Con 10-12 nodi la differenza attesa è piccola (§4.3, B2).

### 4.3 Criteri (soglie nostre, scritte ora, misurate col metro `studio_barca.js` parte B più un modo «rollata»)

| # | Criterio | Soglia |
| --- | --- | --- |
| B1 | Poco vento (4, 6, 8 nodi), gesto nel momento giusto | perdita **≤ 0,35 L** (1,5 m) contro 0,7 L di oggi; F106 dice 0 |
| B2 | Vento medio (10, 12, 14 nodi) | perdita fra 0,4 e 0,8 L (F106: 0,5); la rollata deve servire **meno** che con poco vento |
| B3 | Regola 42.3(b) | velocità a fine virata (prua a 5° dalla nuova bolina) **mai sopra** quella prima della virata, a tutti i venti e tutti i tempi del gesto; perdita mai negativa |
| B4 | È una capacità | gesto 1 s prima o dopo la finestra: perdita **non minore** di quella senza gesto |
| B5 | Virata senza gesto | perdita uguale a oggi entro 0,1 m da 4 a 16 nodi (cambia solo il lato fisso dello sbandamento) |
| B6 | Niente scuffie nuove | col gesto, nessuna scuffia da 4 a 14 nodi; da 16 a 18 si riporta (F107: con vento forte non si rolla) |
| B9 | Rollata e barra (Maiusc) | con la rollata la virata riesce con la sola freccia da 4 a 14 nodi; i numeri con Maiusc si riportano accanto |
| B7 | Ha misurato davvero | ogni riga stampa quanti casi; tempi del gesto provati da −1,5 a +1,5 s a passi di 0,25 s, per ogni vento |
| B8 | Polare | `polare.js` identico carattere per carattere (a regime il lato fisso non cambia niente) |

Se B1 non si raggiunge con le costanti fissate, **non si ritoccano per arrivarci**: si riporta il numero e si decide con Ale.

### 4.4 Cosa serve oltre al motore
- Tasto `X` tenuto premuto (`js/gioco.js`), riga nella scheda dei comandi, una frase nel pannello.
- **Lezione 26 di Deriva, «Virata rollata», tecnica avanzata** (decisione di Ale del 22 nov): testo con F107-F108, F106 e la regola 42.3(b) detta semplice; esercizio con poco vento.
- Registratore: il gesto va scritto nel file (sennò la moviola e il Coach non lo vedono).

### 4.5 Costo (onesto)
- `impronta1b.js` (al bit) e `raffiche_e_virate.js` **cambiano** (lato fisso dello sbandamento): nuovi riferimenti, con la differenza riportata.
- La tabella di `js/rotta-dati.js` no (polare uguale, B8).
- Collaudi con virate da rilanciare uno per volta; giro completo su GitHub alla fine.
- Tempi delle medaglie (voce 7) e lezione 11 (voce 79) si tarano **dopo**: è il motivo per cui la 73 è prima.
**Modello:** Opus.

## 5. Passo C — bolina lenta con poco vento: solo diagnosi

Due tentativi (16 e 17 ottobre) non hanno trovato la causa; il 17 ottobre Ale ha scelto «limite noto». Lo studio aggiunge solo che, contando lo scarroccio, il −15% diventa −20%. **Propongo di non toccare il motore in questa voce.** Al suo posto una misura (Node, senza browser): resistenze della barca del gioco a 6 nodi di vento, voce per voce (scafo, pala e deriva, indotta, vela), contro la figura 11 di Day (`fonti-pdf/day2017`), e lo scarroccio contro quello di Day. Se una voce è fuori di oltre il 30% dalla figura, si scrive una proposta per quella; altrimenti il limite resta dichiarato (`FISICA-E-TARATURE.md`) e va nella pagina dello studio (voce 80) così com'è.
**Modello:** Opus, solo misura.

## 6. Decisione per Ale (una per volta)

**Prima domanda:** via al **passo A** (scotta dei rivali con la lasca; motore intatto)? Le domande sul passo B (tasto `R`, lezione nuova o passo in più, cercare prima la fonte sul gesto) vengono dopo.

## Esito delle fermate

- **Fermata 1 (22 nov 2026):** scritta questa proposta; misura nuova `tests/fisica/misura_scotta_vento_forte.js`. Nessuna modifica a `index.html` né a `js/`.
- **Misura prima del passo A (22 nov 2026, richiesta di Ale), `tests/misura_rivali_vento_forte.py 1 10`** (Chromium, tornei lunghi col pilota, semi 1-10: 30 regate, 90 rivali-regata, 877 minuti dei rivali; 24 s per torneo, picco 47 °C col freno): rivali sbandati oltre 12° (dove la regola con lasca cambierebbe la scotta) il **15,7%** del tempo, quasi tutto di bolina (9,3% con 10 nodi, 22,7% con 12); vento locale oltre 16 nodi il 4,8% (1,2% con 10 nodi, 8,7% con 12), massimo **23,6 nodi**; **0 scuffie**; **5 virate bloccate su 842** (0,6%). Quindi oggi il danno è piccolo (niente scuffie, pochi blocchi), ma il passo A cambierebbe la scotta dei rivali spesso, non solo nelle raffiche rare. Proposta: farlo **insieme alla voce 78** (raffiche rare troppo forti: i 23,6 nodi locali con 12 di media vengono da lì) e rimisurare dopo.
- **Fermata 2 del passo B (22 nov 2026, sera, via di Ale): NON ADOTTATO, `js/` com'era.** Implementato come scritto al §4.2 (sbandamento col lato fisso; vento del rollio = velocità di rollio × zCE; tasto X: fase 1 il timoniere porta la barca a 20° sottovento, fase 2 raddrizzata imposta in 0,8 s; costanti non ritoccate) e misurato col metro (parte R nuova, 270 corse: 9 venti × freccia/Maiusc × senza X, X giusto e 13 spostamenti da −1,5 a +1,5 s). Tutto in `sperimentale/virata-rollata-73/` (`rollata.patch` si applica con `git apply`, misure nei `.txt`).
  - **B1 non passa, di molto:** 4-6-8 nodi, X giusto, persi 0,66 / 0,69 / 0,64 L con la freccia (0,55 / 0,55 / 0,46 con Maiusc) contro ≤ 0,35; senza X 0,68 / 0,69 / 0,67.
  - **B2 al contrario:** la rollata serve di più col vento medio (12-14 nodi Maiusc 0,34 / 0,31 L, sotto la fascia 0,4-0,8) che con poco vento.
  - **B4 non passa:** anticipare il gesto di 0,5-1 s rende quasi sempre di più del «momento giusto» (es. 10 nodi freccia: −1 s 0,48 L, giusto 0,57, senza 0,68).
  - **Passano:** B3 (velocità a fine virata sempre sotto quella di prima: al massimo 82%), B5 (senza X persi uguali entro 0,1 m da 4 a 20 nodi), B6 (nessuna scuffia), B8 (`polare.js` identico), B9 (con X la virata riesce con la sola freccia da 4 a 14 nodi; anche a 18: 1,86 L invece di non riuscire). `raffiche_e_virate.js`: cambiano solo le prime due virate (3,9 → 3,8 s e 7,5 → 7,4 s); `impronta1b.js`: 9 corse su 25 diverse (virate, strambate, retromarcia), come atteso.
  - **Perché (diagnosi, `diagnosi_rollata.js`, Maiusc):** con 4 e 6 nodi la sola raddrizzata (sbandamento messo a 20° gratis) vale **0,12 L**: anche al meglio il vento del rollio non arriva ai 0,33 L che servirebbero. E il gesto intero vale 0,00 L: sbandare sottovento (fase 1) sposta l'albero via dal vento e toglie quanto la raddrizzata rende. Con 12 nodi la fase 1 è quasi gratis (la barca sbanda già da sola) e il gesto rende 0,22 L. Il modello «solo vento apparente del rollio» non spiega F106.
  - **Scoperta in più:** applicare il vento del rollio a **tutti** i rolli (come diceva il §4.2) cambia le raffiche: 10→16 nodi da 37° a 28°, 10→20 nodi non scuffia più (65° → 55°). È lo smorzamento dell'aria, vero, ma fuori dalla proposta; nella prova vale solo durante il gesto.
  - **Da decidere con Ale (una cosa per volta):** (1) tenere almeno il lato fisso dello sbandamento (correzione di fisica, B5 e B8 passano; costa nuovi riferimenti e i collaudi con virate) o lasciare tutto com'è; (2) se riprendere la rollata con un modello diverso (nuova fermata 1: per esempio la barca sbandata che gira con meno timone, cioè meno freno della pala; prima una fonte con numeri) o chiuderla come limite dichiarato.
- **Ricerca e seconda prova (22 nov 2026, notte; Ale: «vedi tu, fai ricerche e test»).** Trovata **F109** (Schutt 2017, Cornell, Laser misurato in acqua, CC BY): la prima fonte con numeri sulla virata rollata (vedi `FONTI-PUBBLICHE.md`). Ancora nessuna modifica a `js/`.
  - **Prova v2** (`rollata_v2.patch`, `misura_v2.js`, `misura_v2.txt`; 144 corse): rollio imposto coi numeri di F109 (sbanda a 25°/s finché X è giù, raddrizza a 50°/s). Con 3,2 nodi (Maiusc) persi 2,2 m senza X, 1,3 m con X: guadagno 0,9 m contro 3,0 m di F109 (rollata contro piatta); con 11 nodi 2,2 → 1,2 m (F109: 2,4 m). Sbandare di più rende di meno (H20 1,3 m, H55 1,6 m), al contrario di F109: il vento in più del rollio, calcolato in modo stazionario, non basta; il guadagno vero viene dai vortici (non modellati).
  - **Scoperta più grossa: la virata normale del gioco non va come quella vera** (`diagnosi_piatta.js`, `misura_piatta.txt`). Con 3,2 nodi il gioco perde 2,2-2,7 m, F109 0,67 m; con 11 nodi il gioco 2,2-3,0 m, F109 **4,39 m**. Quindi col poco vento la virata del gioco costa 3-4 volte troppo, col vento medio circa la metà del vero. Il pezzo che manca è soprattutto **prima del vento in prua**: il gioco guadagna 0,2 m, F109 1,48 m (poco vento) e 0,67 m (medio): la barca vera porta la velocità verso il vento, quella del gioco frena subito (vela che sbatte: con 11 nodi e prua al vento −44 N, in 3 s scende al 28%). Con meno barra va peggio, non meglio (gira più piano e frena prima di arrivare al vento).
  - **Decisione presa (Ale ha lasciato decidere):** (1) il lato fisso dello sbandamento resta nelle patch, non entra da solo: serve solo alla rollata; (2) la rollata non si chiude, ma **prima va sistemata la virata piatta contro F109** (è quella su cui si tara tutto il resto: regola «meno lavoro dopo»), poi la rollata con un termine in più per la raddrizzata tarato sui due punti di F109. Tutti e due chiedono una **nuova fermata 1** (proposta con soglie), che è il prossimo passo della voce 73.
