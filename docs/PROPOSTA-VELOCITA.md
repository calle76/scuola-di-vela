# Proposta: velocità della barca (resistenza dello scafo)

16 ottobre 2026. **Proposta, fermata 1: il motore non è stato toccato.** Sostituisce il §4.1 di `PROPOSTA-RESISTENZA-SCAFO.md` (13 ottobre). Le misure qui sotto sono state fatte con il motore della 1.0.5, cambiando i valori solo in memoria, con script fuori dal repository.

Tipi delle affermazioni:
- **[fonte]** = letto in una fonte, con dove;
- **[misura]** = fatto girare il motore;
- **[stima]** = ragionamento senza misura;
- **[giudizio]** = opinione, da decidere.

**Scelta di partenza (Ale, 16 ottobre 2026):** si tara la barca **condotta bene**. I dati dei velisti di vertice fanno da tetto; la differenza la fa chi conduce.

---

## 0. In breve

- **Il motore frena troppo.** Ricontrollata la misura in vasca di un Laser (Day e Nixon 2014): contando anche deriva e timone, il motore frena **da 1,5 a 2,2 volte** la barca vera fra 2 e 7 nodi. Lo scarto è maggiore sotto i 3 nodi. La stima del 13 ottobre («circa il doppio») regge, un po' ridimensionata.
- **Proposta:** cambiare solo **tre numeri** della barca, scelti per riprodurre la vasca, non la velocità: `hullK1` 4 → **0**, `hullK2` 12 → **6,65**, `hullK4` 0,9 → **0,76**. La formula non cambia. Scarto dalla vasca: medio 6%, massimo 11%.
- **Effetto misurato:**
  - più veloce del 12-37% a seconda di vento e andatura;
  - virata a 10 nodi da 4,0 a **3,3 s**;
  - la virata da 1,9 nodi, che oggi fallisce, **riesce** in 7,3 s;
  - raffiche quasi uguali (+1°).
- **Restano lenti, e non si toccano qui:**
  - la bolina con vento leggero (−33% con 6 nodi rispetto alla media di regata dei velisti di vertice);
  - la poppa.

  Non dipendono dalla resistenza: vanno studiati a parte.
- **Conseguenze nel gioco:**
  - si ritarano le fasce delle medaglie, con la regola che c'è già;
  - si rilancia il pilota delle lezioni;
  - i record vecchi non sono più confrontabili (decisione di Ale, §7).
- **Versione 1.0.6.**

---

## 1. Fonti, ricontrollate il 16 ottobre

**F-A, vasca.** A. H. Day, E. Nixon, «Measurement and prediction of the resistance of a Laser sailing dinghy», *Trans. RINA Part B, Int. J. Small Craft Technology* 156(B1), 2014, pp. 11-20. Testo dell'autore libero su <https://strathprints.strath.ac.uk/46407/>; nessuna licenza dichiarata, si usano solo i numeri citando la fonte.
- **[fonte]** Scafo Laser vero, dritto, senza deriva né timone, in acqua dolce, da 2 a 9 nodi. Figura 4, «area di resistenza» (resistenza divisa per ½ ρ v²), letta a occhio dall'immagine della pagina 6. Curva con timoniere da 80 kg, circa 160 kg in tutto:

| Nodi | 2 | 2,5 | 3 | 3,5 | 4 | 4,5 | 5 | 5,5 | 6 | 6,5 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Area (m²) | 0,0125 | 0,0126 | 0,0132 | 0,0143 | 0,0156 | 0,0177 | 0,0206 | 0,0229 | 0,0240 | 0,0245 | 0,0242 |

  Incertezza di lettura circa ±0,0003 m². La barca comincia a planare verso i 6,5 nodi.

**F-B, previsione e misure in mare.** A. H. Day, «Performance prediction for sailing dinghies», *Ocean Engineering* 136, 2017, pp. 67-79, <https://strathprints.strath.ac.uk/59980/>.
- **[fonte]** Deriva, timone e la resistenza legata al timone valgono **circa il 20%** della resistenza dell'acqua.
- **[fonte]** Figura 4: velocità misurate da Binns e colleghi (2002) con 9 nodi di vento, lette a occhio: 42° → circa 4,65 nodi; 46,5° → 5,0; 55° → 5,6; 60° → 5,9.
- **[fonte]** Figura 3: una seconda serie misurata (Clark 2014, 12,5 nodi) dà valori **circa la metà** di Binns. Day scrive che la differenza è «molto sostanziale» e difficile da spiegare. Le misure in mare danno una **fascia**, non un numero.
- **[fonte] Attenzione:** fra gli autori di Binns c'è Bethwaite. Quindi la «polare di Bethwaite» di `RICERCA-VELOCITA-VIRATA-RIPARTENZA.md` (fonte B) e i dati di Binns **non sono indipendenti**. Indipendenti fra loro sono: la vasca (F-A), Binns/Bethwaite, Clark, e le tracce GPS di Caraballo (fonte A della ricerca).

---

## 2. Il confronto, numero per numero [misura]

Resistenza dello scafo dritto, barra al centro. Vasca convertita in acqua di mare (1025 kg/m³), più il 20% di Day per deriva e timone.

| Nodi | Vasca solo scafo | Vasca +20% | Motore oggi | Oggi ÷ vasca+20% | Proposta | Proposta ÷ vasca+20% |
|---|---|---|---|---|---|---|
| 2 | 6,8 N | 8,1 N | 17,8 N | 2,19 | 7,9 N | 0,97 |
| 3 | 16,1 | 19,3 | 39,9 | 2,06 | 20,2 | 1,04 |
| 4 | 33,9 | 40,6 | 75,2 | 1,85 | 41,8 | 1,03 |
| 5 | 69,9 | 83,8 | 129,1 | 1,54 | 77,3 | 0,92 |
| 6 | 117,2 | 140,6 | 208,4 | 1,48 | 132,3 | 0,94 |
| 7 | 160,8 | 193,0 | 321,4 | 1,67 | 214,0 | 1,11 |

**Come sono stati scelti i tre numeri:** minimi quadrati sugli scarti relativi, da 2 a 7 nodi ogni mezzo nodo (11 punti), con i tre valori non negativi. `hullK1` esce a 0: sopra i 2 nodi la vasca non chiede un termine lineare.

**Cosa non sappiamo [stima]:**
- **Sotto i 2 nodi** la vasca non ha dati. Lì conta per l'abbrivio, la virata lenta e la retromarcia, e la proposta frena meno di oggi.
- **La barca del gioco pesa 135 kg**, il Laser della curva circa 160. Una barca più leggera frena un po' meno (curva da 70 kg nella stessa figura). Usare la curva da 80 kg e l'acqua di mare vuol dire stimare **un poco in eccesso** la resistenza, cioè una barca leggermente più lenta: margine prudente, coerente con «sotto i dati di vertice».
- **Lo sbandamento** frena in più (`heelDrag`, già nel motore, non toccato).

---

## 3. Cosa cambia nella barca [misura]

Velocità con la scotta migliore, nodi (oggi → proposta):

| Vento | 45° | 60° | 90° | 120° | 135° | 150° | 180° |
|---|---|---|---|---|---|---|---|
| 6 nodi | 2,0 → 2,4 | 2,9 → 3,9 | 3,3 → 4,3 | 3,0 → 3,9 | 2,6 → 3,5 | 2,3 → 2,9 | 2,2 → 2,7 |
| 10 nodi | 3,4 → 3,9 | 4,6 → 5,6 | 5,2 → 6,1 | 4,7 → 5,6 | 4,2 → 5,2 | 3,8 → 4,5 | 3,5 → 4,2 |
| 15 nodi | 5,0 → 5,5 | 5,9 → 6,8 | 6,9 → 7,9 | 6,5 → 7,4 | 5,8 → 6,8 | 5,4 → 6,2 | 4,8 → 5,5 |

Altro, con 10 nodi:

| Misura | Oggi | Proposta |
|---|---|---|
| Virata da 3,9 nodi, barra 0,8 | 4,0 s | 3,3 s |
| Virata da 1,9 nodi | fallita | riuscita in 7,3 s |
| Raffica da 10 a 16 / 18 / 20 nodi senza reagire | 27° / 41° / 55° | 28° / 42° / 56° |
| Frenata con la prua nel vento, partendo dalla bolina | da 3,3 nodi: 3,1 m (0,7 lunghezze) in 4,2 s | da 3,8 nodi: 4,4 m (1,0 lunghezze) in 5,1 s |
| Angolo morto da fermi, scotta a metà | indietro dopo 1,7 s, fino a 1,8 nodi | indietro dopo 1,7 s, fino a **2,3 nodi** |

**Confronto con le fonti** (proposta / fonte; nessuna fonte è stata usata per scegliere i tre numeri):

| Caso | Proposta | Fonte | Scarto |
|---|---|---|---|
| 6 nodi, bolina 45° | 2,4 | 3,6 media GPS (Caraballo) · 4,0 punta (Bethwaite) | −33% · −40% |
| 6 nodi, 120° | 3,9 | 4,5 media GPS | −13% |
| 6 nodi, poppa 180° | 2,7 | 3,4 media GPS · 4,1 punta | −21% · −34% |
| 9-10 nodi, bolina 45-46° | 3,9 (con 10 nodi) | 5,0 (Binns, con 9 nodi) | −22% |
| 9-10 nodi, 60° | 5,6 (con 10 nodi) | 5,9 (Binns, con 9 nodi) | −5% |
| 10 nodi, traverso | 6,1 | 6,6 (Bethwaite, interpolata) | −8% |
| 15 nodi, bolina | 5,5 | 5,4 (punta GPS, una sola misura) | **+2%** |
| 12,5 nodi, tutte le andature | — | Clark: circa la metà di Binns | la proposta sta fra le due serie |

**Cosa si vede [stima]:**
- **Con la resistenza giusta, larghi e traverso si avvicinano molto ai dati** (da −5% a −13%).
- **Bolina con vento leggero e poppa restano indietro.** Probabilmente non dipende dallo scafo:
  - di bolina la vela del gioco comincia a sgonfiarsi sotto i 34° di vento apparente (`luffA0` + `luffW`), e a 45° dal vento reale ci si arriva vicino;
  - in poppa la spinta viene solo dalla resistenza della vela.

  Sono due domande nuove, da studiare dopo, con fonti loro.
- **Il +2% a 15 nodi di bolina** supera di poco l'unica punta GPS trovata (affidabilità bassa). Lo riporto com'è.

---

## 4. Criteri della fermata 2

Soglie dichiarate adesso. **Avvertenza:** i numeri dei §2 e §3 li ho già visti, quindi i criteri 1 e 2 sono controlli di coerenza, non prove indipendenti. Le prove indipendenti sono il criterio 3 e le misure del gioco (4-7).

1. **Resistenza:** con i tre valori nuovi, scarto dalla vasca+20% medio non oltre il 6% e massimo non oltre il 12%, da 2 a 7 nodi.
2. **Il motore cambiato è quello misurato qui:** `polare.js` a 6, 10 e 15 nodi uguale alla tabella del §3, al decimo.
3. **Tetto dei velisti di vertice:** nessun punto della polare sopra le fonti di vertice con lo stesso vento o con meno. Oggi l'unico punto sopra è la bolina a 15 nodi (+2% su una misura sola): **lo riporto come fuori fascia** e la decisione resta ad Ale e alla revisione in chat.
4. **Nessun conto in errore,** con i passi di tempo di 1/240 e 0,0125 s (stessa prova del laboratorio, valori agli estremi rifatti con i nuovi valori di partenza).
5. **Regate:** `collaudo_regate.py` (bastone e raffiche, semi 1-6) senza nessun avversario BLOCCATO; `collaudo_partenze.py` OK.
6. **Prove:** `collaudo_fasce.py` dà i tempi nuovi; le fasce si ritarano con la regola già scritta in `contenuti.js` (oro = pilota arrotondato ai 5 s superiori, argento +25%, bronzo +60%), senza scelte nuove.
7. **Lezioni:** pilota delle lezioni sui semi 1-20, poi conferma sui semi 21-100 mai guardati (regola dei semi). Si riportano i sei passi da correggere: quali migliorano, quali peggiorano, quali nascono nuovi. Nessuna soglia: è un rapporto per le correzioni successive.
8. **Non-regressione della pagina:** nessun errore con `#collaudo`, senza, e con `#lab`; pannello a 1360×650 senza eccesso (`collaudo_pannello.py`, valido anche nella sandbox dalla 1.0.5); collaudi della 1.0.4 e 1.0.5 tutti OK.

---

## 5. Rischi

1. **La retromarcia diventa più forte** (fino a 2,3 nodi contro 1,8): con meno freno arriva al tetto `backMax`. Secondo Ale oggi parte già troppo presto. **Non la tocco qui:** è il compito «retromarcia» della roadmap, e con il laboratorio si prova a mano.
2. **La virata migliora** senza toccare il timone. Il compito «timone e virata» va rifatto sulla barca nuova, con le misure dai video.
3. **Tutte le tarature basate sulla velocità vanno riguardate:** fasce delle prove; avversari (per esempio «sotto 0,6 m/s poggia»); soglie delle lezioni (3,3 nodi per prepararsi a virare, più di 4 nodi in «Accelerando», 1 nodo per la virata che non riesce). «Accelerando» oggi è difficile perché la barca arriva a 3,7 nodi: con la proposta dovrebbe migliorare (da misurare col pilota).
4. **Record e medaglie:** un tempo fatto con la barca vecchia non è confrontabile. Il meccanismo c'è già (`KEYV` in `gioco.js`: cambiando la chiave i record vecchi non si leggono più), ma cancella dal menu i record e, in carriera, i meriti di bravura delle prove. Decide Ale (§7).
5. **Il prototipo del fiocco** (`sperimentale/fiocco.html`) ha una copia sua del motore e resterebbe con la resistenza vecchia: la regola «la barca senza fiocco è identica al gioco» non varrebbe più finché non lo si allinea. Proposta: dichiararlo in `SPERIMENTALE.md` e allinearlo solo quando si riprende il fiocco.
6. **Sotto i 2 nodi non ci sono dati:** abbrivio e frenata cambiano su una zona senza misure. La frenata passa da 0,7 a 1,0 lunghezze. La citazione «3-4 lunghezze» (Cockerill) resta non rintracciata, quindi non è un criterio.

---

## 6. Cosa si fa alla fermata 2

1. `js/motore.js`: tre numeri, con la fonte nel commento.
2. Misure dei criteri 1-4; rilancio di `polare.js` e `raffiche_e_virate.js`: le uscite nuove diventano il riferimento, con la tabella vecchia e la nuova in `FISICA-E-TARATURE.md`.
3. Fasce delle prove ritarate con `collaudo_fasce.py`; `KEYV` secondo la decisione di Ale.
4. Regate, partenze, pilota delle lezioni (1-20, poi 21-100), pannello.
5. Documenti: `FONTI-PUBBLICHE.md` (F-A e F-B con numero), `FISICA-E-TARATURE.md`, `SPERIMENTALE.md` (rischio 5), `ROADMAP.md`, `CHANGELOG.md` e `VERSIONE` 1.0.6; in `PROPOSTA-RESISTENZA-SCAFO.md` una riga che rimanda qui.

**Fuori da questo compito,** nell'ordine della roadmap: retromarcia, timone e virata, ripartenza dall'angolo morto; poi bolina con vento leggero e poppa, se si trovano fonti.

---

## 7. Decisioni per Ale

1. **Il via alla fermata 2.**
2. **Record delle prove e delle regate:**
   - (a) si azzerano, cambiando le chiavi `KEYV` (proposta: è onesto, un tempo con la barca vecchia non vale con la nuova);
   - (b) restano, e il tempo vecchio si giudica con le fasce nuove.

   In carriera, (a) toglie i meriti di bravura delle prove già fatte.
3. **Il +2% a 15 nodi di bolina:** accettarlo (una sola misura, affidabilità bassa) o chiedere una barca un poco più frenata. La proposta è accettarlo: la resistenza viene dalla vasca, e ritoccarla per stare sotto un singolo numero sarebbe tarare sul risultato.
