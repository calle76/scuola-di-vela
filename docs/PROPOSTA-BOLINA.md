# Proposta: resistenza indotta e bolina con poco vento

**Seconda stesura, 16 ottobre 2026, con le correzioni della revisione in chat (§8). Fermata 1: il motore non è stato toccato.** La prima stesura (stesso giorno, nella storia di git) è stata rivista dalla chat del progetto sul testo completo di Day 2017; la revisione ha dato un via condizionato a cinque condizioni, tutte trattate qui (§8).

Le misure sono fatte con una copia del motore cambiata solo in memoria, con script fuori dal repository (banco: angoli dal vento reale da 32° a 70° grado per grado, scotta a passi di 0,02, 60 s di equilibrio come `polare.js`). Sul motore di oggi il banco ridà la VMG della 1.0.6: 2,07 / 3,13 / 4,02 nodi contro 2,07 / 3,09 / 3,99 (lo scarto viene dal passo più fine degli angoli).

Tipi delle affermazioni: **[fonte]** letto, con dove; **[misura]** motore fatto girare; **[stima]** ragionamento senza misura; **[giudizio]** da decidere.

---

## 0. In breve

- **Due difetti, un solo compito**, perché si toccano: tutti e due cambiano la bolina, in versi opposti.
  - **A. Resistenza indotta.** Oggi la spinta laterale fa solo scarrocciare, non frena mai. Si aggiunge la formula di Delft usata da Day 2017, con **una costante nuova**: la profondità efficace della deriva `TE`.
  - **B. La vela non stringe.** Oggi sotto i 34° di vento apparente la portanza crolla: a 28° ne resta il **10%**, mentre nei coefficienti usati da Day ne resta quasi tutta. Si cambiano **tre costanti esistenti**: `minBoom`, `luffA0` e il peso di CL² nella resistenza della vela (0,12 → 0,08).
- **Due varianti di B**, da scegliere (§7, decisione di Ale):

  | | Oggi | Variante 9° / 22° | Variante 11° / 24° |
  |---|---|---|---|
  | `TE` (scelta sul 14% con 10 nodi) | — | 0,80 m | 0,78 m |
  | Portanza a 28° apparenti (Day/ORC: quasi piena) | 10% | **81%** | 49% |
  | VMG di bolina 6 / 10 / 15 nodi (Day: 2,65 / 3,6 / 3,8) | 2,07 / 3,13 / 4,02 | 2,25 / 3,29 / 4,07 | 2,23 / 3,27 / 4,07 |
  | Angolo della VMG migliore (Day fig. 9: ~44° / ~40,5° / ~43,5°) | 54° / 51° / 47° | **45° / 45° / 42°** | 49° / 46° / 45° |
  | Binns con 12 nodi a 42° (misura ~5,0) | 3,73 | **4,94** | 4,57 |
  | Velocità a 32° dal vento, 10 nodi | 0,5 | 1,9 | 1,3 |

  **Consiglio la variante 9° / 22°**: è più vicina a Day e a Binns su tutto quello che si misura. La revisione suggeriva 11° / 24° per la posizione del boma, che però non ha una fonte (§5).
- **Con 12 nodi la barca coincide con le misure di Binns** (fig. 5). Lo scarto di bolina che resta è **con poco vento**: −15% con 6 nodi contro Day, −12…−14% contro Binns con 9 nodi. La causa non è identificata (§6).
- **Con 15 nodi resta il +7%** contro Day: è un difetto di forma della curva (Day fra 10 e 15 nodi cresce del 5%, il gioco del 24%), compito separato (§6).
- **Di poppa non cambia niente** (scarti sotto 0,03 nodi).
- **Versione 1.0.11**, una sola: fasce ritarate e record azzerati una volta. Nel laboratorio A e B si spengono separatamente.

---

## 1. Cosa fa oggi il motore [codice, `js/motore.js`]

- **Unità:** `S.u` è in **m/s** (la tabella della vasca converte in nodi dentro `hullDrag`).
- **In acqua (`res`):** tabella della vasca (scafo nudo, F16) + `appDA` 0,0049 m² (attrito e resistenza residua di **deriva e timone**, Day fig. 11, bolina) + la barra girata (`rudderDragK`), il tutto moltiplicato per il freno dello sbandamento. Quindi **le appendici ci sono**: il totale del gioco è confrontabile con il totale di Day (mancano solo dRi e le variazioni con lo sbandamento, pochi punti). [misura] A 4,5 nodi `appDA` vale il 28% dello scafo nudo; in Day (fig. 11, 10 nodi) le appendici valgono il 25% di Ruh.
- **In aria:** c'è **una sola resistenza**, quella della vela `CD(α)`. Non esiste un termine a parte per scafo, albero o timoniere: `CD` rappresenta tutta la barca. `appDA` è solo in acqua, quindi **nessun doppio conteggio**.
- La forza laterale `side` decide scarroccio e sbandamento: **nessun freno**.
- Vela: incidenza α = vento apparente − boma; il boma non scende sotto `minBoom` = 14°; la portanza ha il massimo (1,35) a α = 20°, quindi a **34°** di vento apparente; sotto `luffA0` = 27° la vela si sgonfia del tutto, piena da 27 + 7 = 34°.
- `CD = 0,06 + 1,15·sin²α + 0,12·CL²`: al punto di lavoro di bolina (α = 20°) vale **0,413**.
- `minBoom`, `luffA0`, `luffW`, 0,12: **nessuna fonte**, tarate a occhio nella 0.1x.

---

## 2. Fonti

Tutte da **F17**: A. H. Day, «Performance prediction for sailing dinghies», *Ocean Engineering* 136 (2017), manoscritto «2nd Revision Feb 2017», CC BY-NC-ND 4.0, <https://strathprints.strath.ac.uk/59980/>. Copia locale fuori da git: `fonti-pdf/day2017/` (pagine 47, 51 e 54 = figure 4, 8 e 11). Si usano solo numeri, con citazione. Letture confermate dalla revisione (§8).

**Resistenza indotta**
- **[fonte, §3.4, eq. 15]** `Ri = Fh² / (π · ½ρ · V² · TE²)` (Delft, Keuning e Katgert 2008). In Delft `TE` dipende dallo **sbandamento** e dal **numero di Froude**; Day non scrive il valore per il Laser.
- **[fonte, §3.4]** Con 10 nodi di bolina e un timoniere da 80 kg, l'indotta è **il 14%** della resistenza in acqua: è **Ri da sola**; con la parte dovuta al timone (dRi) arriva a circa 17,5%. In poppa i termini di Delft sono sotto l'1%.
- **[fonte, fig. 11]** Di bolina, in % del totale in acqua, 5 / 10 / 15 nodi: Ri ≈ 8 / 14,5 / 15; dRi ≈ 2,5 / 3 / 3,5; scafo nudo ≈ 67 / 66 / 66,5. Quindi Ri / scafo nudo ≈ **0,12 / 0,22 / 0,23**.
- **[fonte, §5]** Day stesso, senza equilibrio di imbardata, usa la forza aerodinamica sbandante come `Fh`.

**Vela**
- **[fonte, Tab. 1]** Coefficienti ORC «low lift» usati da Day: CL **1,164** a 12°, **1,347** a 28°, 1,239 a 60° di vento apparente. **[fonte, §2.4]** Massimo della portanza «intorno a 34°»; da zero a 34° la scotta non cambia. Quindi sotto il massimo la portanza ORC **cala piano**: a 28° è quasi piena, a 12° è ancora l'86% di 1,347.
- **[fonte, §2.1]** Galleria del vento su un armo da Laser (Flay 1992, riportato da Day): misure **solo** a 30° e 60° di vento apparente orizzontale (sul piano del ponte da circa 26° a 30°); CL riportato all'area di tessuto 1,30-1,36. Resistenza totale di vela, albero e scafo, senza timoniere, circa **0,27**; con i coefficienti ORC nella stessa condizione Day stima **0,20**, non sa spiegare la differenza e **adotta ORC**.
- **[fonte, §2.5]** Day aggiunge a parte il timoniere (Du Bois; Cd 1,075 di fronte e 0,954 di fianco, −10%, −20% di schermo). **[stima, confermata dalla revisione]** Per 80 kg e 1,83 m: circa 0,06-0,07 riportato ai 7 m² della vela.
- **[fonte, fig. 12]** Di bolina il timoniere fa circa il 15,5% / 17% / 21% della resistenza aerodinamica (5 / 10 / 15 nodi). **[stima della revisione]** Ne segue una resistenza aerodinamica totale al punto di lavoro di Day di circa **0,28-0,42**: lo 0,20 ORC vale nella condizione di Flay, non al punto di lavoro.

**Angoli**
- **[fonte, §6.1]** «Un Laser ha la VMG migliore di bolina intorno a 40-46° dal vento reale, in acqua piatta» (fatto noto, non risultato del modello).
- **[fonte, fig. 9]** Angolo della VMG migliore nel modello di Day: circa **44°** con 5-6 nodi, **40,5°** con 9-10, **43,5°** con 15.
- **[fonte, §6.2]** Vento apparente di bolina da circa 27° (5 nodi) a 33° (15 nodi), vicino all'angolo di portanza massima. Di bolina la barca è piatta fino a circa 9 nodi (lo sbandamento sopravento di circa 20° è **solo in poppa**).

**Misure in mare (Binns 2002, da Day)**
- **[fonte, fig. 4]** 9 nodi: 4,65 / 5,0 / 5,6 / 5,9 nodi a 42° / 46,5° / 55° / 60°. Il modello di Day: circa 4,6 a 40°, 5,2 a 50°, 5,4 a 55°, 5,5 a 60°.
- **[fonte, fig. 5]** 12 nodi: circa 5,0 / 5,4 / 5,65 / 6,0 / 6,3 a 42° / 46,5° / 50° / 55° / 60°; il modello di Day coincide.

**Non usata:** un forum dà al Laser circa 0,75 m di pescaggio con la deriva giù ([catsailor.com](https://www.catsailor.com/forum/ubbthreads.php/posts/179032)); fonte non affidabile.

**Altre fonti cercate sui dubbi rimasti (16 ottobre, dopo la revisione).** Copie locali fuori da git in `fonti-pdf/altre-bolina/`.
- **Pennanen e altri, «Numerical prediction of the best heel and trim of a Laser dinghy», *Procedia Engineering* 147 (2016) 336-341, CC BY-NC-ND 4.0** (<https://research.chalmers.se/publication/234579>). È un **modello** (CFD sulla stessa vasca di Day e Nixon), non una misura.
  - [fonte, §1] Di bolina la velocità della barca cresce fino a circa 11 nodi di vento, poi «non aumenta affatto o molto poco». Va nel verso di Day fig. 8 (VMG quasi piatta fra 10 e 15 nodi), contro il gioco (+24%): sostiene il difetto 2 del §6.
  - [fonte, fig. 5, letta a occhio] Vento che serve per andare di bolina a 3 / 4 / 5 nodi: circa 4,9 / 6,9 / 10,5 nodi (asse in nodi; la legenda del primo grafico dice m/s, incoerenza della figura). **L'angolo dal vento non è scritto.** [misura] Il gioco con A + B (9° / 22°), al suo angolo di VMG migliore, con quei venti va a 2,84 / 3,69 / 4,72 nodi (a 48° / 47° / 44°); oggi 3,03 / 3,88 / 5,12 (a 55° / 53° / 51°). Senza l'angolo il confronto non decide niente.
  - Lo scarroccio usato non è scritto nell'articolo (sta nella tesi, Aalto 2015, non scaricabile).
- **«Laser and Laser Radial Speeds Under Various Wind Ranges»**, guida per comitati di regata, autore non indicato (<https://www.setcourses.com/Dinghy-Speed-Leg-Length.pdf>). [fonte] Laser, minuti per miglio di bolina: 20 / 19 / 16 / 15 con 5-8 / 8-12 / 12-15 / oltre 15 nodi, cioè VMG di circa **3,0 / 3,2 / 3,8 / 4,0** nodi, virate comprese. [giudizio] Fonte debole (indicativa, senza metodo), ma è la terza che dà la bolina con poco vento più veloce del gioco (2,25 con 6 nodi). Con oltre 15 nodi dà 4,0, vicino al gioco (4,07) più che a Day (3,8).
- **Angolo del boma:** nessun numero trovato. Solo un forum: con la scotta cazzata del tutto «il boma sta sopra lo spigolo di poppa», e nelle derive a una vela è circa la posizione migliore di bolina ([yachtsandyachting.com](https://www.yachtsandyachting.com/FORUM/printer_friendly_posts.asp?TID=770)). Senza le misure di boma e poppa non diventa un angolo.
- **Scarroccio:** solo un forum, circa 4° di bolina «tipici» ([boatdesign.net](https://www.boatdesign.net/goto/post?id=876429)); il gioco ne fa circa 2°. Fonte debole: lo annoto, non lo uso.

---

## 3. Il modello proposto

### A. Resistenza indotta (una costante nuova)

```
Ri = side² · u·|u| / (π · ½ · rhoW · TE² · (u² + 0,4)²)      (u in m/s)
S.u += (drive − res · heelDrag − Ri) / mass · dt
```

- **La regolarizzazione 0,4 non è piccola.** Alle velocità di bolina toglie a Ri il 29% con 5 nodi (u ≈ 1,5 m/s), il 13% con 10 (2,3 m/s), il 9% con 15 (2,9 m/s), rispetto alla formula pura. `TE` è scelto con la regolarizzazione dentro, quindi con 10 nodi la quota è quella di Day.
- **Perché non più piccola [misura]:** con 0,05 la barca partita da ferma al traverso stretto con 10 nodi **non arriva mai a 2 nodi** in 30 s: verso 0,2 m/s la formula frena più della spinta della vela. Con 0,1 arriva a 2 nodi in 4,1 s, con 0,2 in 3,1 s, con 0,4 in 2,6 s (oggi 2,5 s). La formula pura non vale a bassa velocità, dove la deriva non regge la spinta laterale; il motore rappresenta già lo stesso fatto con lo **stesso 0,4** nello scarroccio (`foilK · (u² + 0,4)`). Nessuna costante nuova. [stima, semplificazione dichiarata]
- **Sulle VMG la regolarizzazione pesa poco [misura]:** con 0,4 e con 0,05, variante 9° / 22°, 3,27 contro 3,24 nodi con 10 nodi di vento.
- Con la barca ferma Ri = 0; all'indietro frena all'indietro.
- **`TE`** = **0,80 m** con la variante 9° / 22°, **0,78 m** con 11° / 24° [ipotesi]: il valore che dà Ri = 14% del totale in acqua con 10 nodi.
- Non moltiplicata per il freno dello sbandamento: è una forza a sé.
- **Semplificazioni dichiarate:** `TE` non dipende dallo sbandamento né dal numero di Froude (in Delft `TE` cala sbandando, quindi con la barca sbandata Ri è un po' **sottostimata**); il 2-3,5% del timone (dRi) non c'è, c'è già `rudderDragK`.

### B. La vela che stringe (tre costanti esistenti)

| Costante | Oggi | Variante 9° / 22° | Variante 11° / 24° |
|---|---|---|---|
| `minBoom` | 14° | 9° | 11° |
| `luffA0` (`luffW` resta 7°) | 27° | 22° | 24° |
| peso di CL² in `CD` (nuova voce di `BOAT`) | 0,12 | 0,08 | 0,08 |

**Portanza rispetto al massimo, per angolo di vento apparente** [misura, conto sulle formule del motore]:

| Apparente | 24° | 26° | 28° | 30° | 32° | 34° |
|---|---|---|---|---|---|---|
| Oggi | 0% | 0% | **10%** | 34% | 64% | 100% |
| 9° / 22° | 21% | 49% | **81%** | 98% | 95% | 92% |
| 11° / 24° | 0% | 21% | **49%** | 81% | 98% | 95% |
| ORC (Day Tab. 1) | | | 1,347, **quasi piena** | | | massimo intorno a 34° |

- **Perché:** oggi il massimo è a 34°, **come dice Day §2.4**; il difetto è sotto il massimo, dove il gioco perde la portanza in pochi gradi e ORC quasi niente. Day naviga a 27-33° apparenti; il gioco oggi non può (VMG migliore sempre a 34°).
- **Resistenza della vela 0,413 → 0,340:** dentro l'intervallo 0,28-0,42 della fig. 12 (§2). Scelta **prima** di vedere la VMG che produce, come somma 0,27 (Flay) + 0,07 (timoniere); le prove con 0,27 sono venute dopo e restano solo come sensibilità. Il timoniere a 0,06 invece di 0,07 darebbe 0,33.
- **Si abbassa solo il peso di CL²:** è il termine legato alla portanza; il termine 1,15·sin²α, che spinge in poppa, **non si tocca**.
- **Nessuna formula nuova.** Si portano dietro da soli (leggono `BOAT`): suggerimento della scotta (`gioco.js:83`), «vela che sbatte» (`gioco.js:73`, sotto `luffA0 + luffW/2`: 25,5° o 27,5°), avversari (`regate.js:293`), disegno del boma.

---

## 4. Misure [misura]

**VMG di bolina**, nodi; tra parentesi angolo dal vento reale, vento apparente, Ri sul totale in acqua, Ri sullo scafo nudo:

| Motore | 5 nodi | 6 nodi | 10 nodi | 15 nodi |
|---|---|---|---|---|
| Oggi | 1,76 (55°, 34,0°) | 2,07 (54°, 34,0°) | 3,13 (51°, 34,1°) | 4,02 (47°, 33,9°) |
| Solo A (`TE` 0,75) | 1,71 (54°, 34,0°, 8,8%, 0,13) | 2,01 (53°, 34,0°, 10,2%, 0,16) | 3,00 (50°, 34,0°, 15,0%, 0,23) | 3,84 (47°, 34,3°, 13,0%, 0,19) |
| A + B 9° / 22°, `TE` 0,80 | 1,92 (48°, 30,1°, 8,4%, 0,13) | 2,25 (45°, 29,0°, 11,3%, 0,18) | 3,29 (45°, 30,5°, 14,1%, 0,21) | 4,07 (42°, 30,7°, 12,6%, 0,18) |
| A + B 11° / 24°, `TE` 0,78 | 1,91 (50°, 31,1°, 8,2%, 0,13) | 2,23 (49°, 31,0°, 9,5%, 0,14) | 3,27 (46°, 31,1°, 14,0%, 0,21) | 4,07 (45°, 32,6°, 11,0%, 0,15) |
| **Day** | ~44°, ~27°, 8%, 0,12 | 2,65 (~44°) | 3,6 (~40,5°), 14,5%, 0,22 | 3,8 (~43,5°, ~33°), 15%, 0,23 |

- La riga con 10 nodi serve a **scegliere** `TE`: non prova niente.
- **Con 5 nodi la quota non è una prova indipendente** (la regolarizzazione pesa il 29%). **Con 15 nodi sì:** 12,6% e 11,0% contro il 15% di Day, cioè un po' sotto.
- «Solo B» (`TE` = 0), variante 9° / 22°: 2,36 / 3,46 / 4,27 con 6 / 10 / 15 nodi.
- VMG di poppa con 6 / 10 / 15 nodi: oggi 2,66 / 4,18 / 5,74; con A + B 2,65 / 4,17 / 5,72 (Day 2,95 / 4,55 / 6,3).

**Contro Binns**, nodi:

| | 42° | 46,5° | 50° | 55° | 60° |
|---|---|---|---|---|---|
| 9 nodi, Binns | 4,65 | 5,0 | | 5,6 | 5,9 |
| 9 nodi, oggi | 2,82 | 3,75 | | 4,80 | 4,98 |
| 9 nodi, 9° / 22° | 4,00 | 4,43 | | 4,86 | 5,05 |
| 9 nodi, 11° / 24° | 3,54 | 4,43 | | 4,86 | 5,06 |
| 12 nodi, Binns | ~5,0 | ~5,4 | ~5,65 | ~6,0 | ~6,3 |
| 12 nodi, oggi | 3,73 | 4,84 | 5,55 | 5,93 | 6,25 |
| 12 nodi, 9° / 22° | **4,94** | **5,35** | **5,60** | **5,99** | **6,36** |
| 12 nodi, 11° / 24° | 4,57 | 5,33 | 5,62 | 6,01 | 6,35 |

**Quanto vicino al vento si avanza, 10 nodi** (velocità migliore, nodi):

| Angolo dal vento | 26° | 28° | 30° | 32° | 34° | 36° | 40° | 45° |
|---|---|---|---|---|---|---|---|---|
| Oggi | −1,1 | −0,7 | −0,2 | 0,5 | 1,1 | 1,6 | 2,6 | 3,8 |
| 9° / 22° | 0,0 | 0,7 | 1,3 | 1,9 | 2,4 | 3,0 | 3,9 | 4,7 |
| 11° / 24° | −0,5 | 0,1 | 0,7 | 1,3 | 1,9 | 2,4 | 3,4 | 4,5 |

**Partenza da ferma** al traverso stretto (60° dal vento, 10 nodi, scotta migliore), tempo per arrivare a 2 e a 3 nodi: oggi 2,5 / 3,6 s; solo A 2,9 / 4,3 s; 9° / 22° 2,6 / 3,9 s; 11° / 24° 2,6 / 3,8 s.

**Sensibilità** (variante 9° / 22°, `TE` 0,75, VMG di bolina 6 / 10 / 15 nodi):
- `TE` 0,6 m: 2,16 / 3,14 / 3,92; `TE` 0,9 m: 2,26 / 3,33 / 4,12;
- resistenza della vela 0,27 (peso di CL² 0,041): 2,39 / 3,47 / 4,23;
- resistenza della vela come oggi (0,12): 2,05 / 3,04 / 3,86;
- regolarizzazione 0,05 / 0,1 / 0,2 / 0,4: 3,24 / 3,24 / 3,25 / 3,27 con 10 nodi.

**Nota sul banco:** l'angolo della VMG migliore e le quote saltano di qualche grado o punto fra varianti vicine (per esempio con 6 nodi 45° con `TE` 0,80 e 48° con 0,90), perché la curva della VMG è piatta vicino al massimo. Vanno lette come ±2° e ±1,5 punti.

---

## 5. La scelta fra le due varianti di B

| | 9° / 22° | 11° / 24° |
|---|---|---|
| Portanza a 28° (ORC quasi piena) | 81% | 49% |
| Angolo della VMG migliore contro Day fig. 9 | +1 / +4,5 / −1,5° | +5 / +5,5 / +1,5° |
| Binns 12 nodi a 42° | −1% | −9% |
| Binns 9 nodi a 42° | −14% | −24% |
| Velocità a 32° dal vento con 10 nodi (testi oggi: «sotto 33° non avanza») | 1,9 nodi | 1,3 nodi |
| Boma cazzato | 9° dall'asse | 11° dall'asse |

- **Numeri:** la 9° / 22° è più vicina alle fonti in tutte le righe misurate.
- **Contro:** il boma a 9° non ha una fonte. La revisione [giudizio, senza fonte] dice che di bolina, nella pratica, l'estremità del boma sta circa sopra lo spigolo dello specchio di poppa, a 10-13° dall'asse, e che nel modello il boma rappresenta anche lo svergolamento, che spinge verso valori più alti. Una verifica come quella di Day sull'albero (foto, §2.1) darebbe un numero con una base; oggi non c'è.
- **In tutte e due** i testi che dicono «circa 35-40° per lato» e «sotto 33° non avanza» vanno corretti.

---

## 6. Cosa non torna, riportato com'è

1. **Con poco vento la bolina resta lenta:** −15% contro Day con 6 nodi; con 9 nodi −12…−14% contro Binns fra 46,5° e 60° e circa −8…−15% contro il modello di Day. **Con 12 nodi invece coincide con Binns**: il difetto pesa col vento leggero. La causa **non è identificata**. Esclusi: lo sbandamento sopravento (solo in poppa); la resistenza della vela (la fig. 12 non giustifica di scendere sotto 0,34). Restano da guardare, uno per volta: lo scarroccio del gioco e la sua resistenza; quanto porta la vela del gioco verso il traverso stretto (ORC: CL 1,24 a 60°); la massa (inerzia di 135 kg contro resistenza misurata per 160 kg).
2. **Con 15 nodi la bolina resta al +7%:** è un difetto di forma. Fra 10 e 15 nodi Day cresce del 5% (3,62 → 3,79), il gioco del 24% (3,29 → 4,07). **[fonte, §2.3 eq. 5, §6.2]** Quando sventa, Day aumenta lo svergolamento e con lui l'indotta della vela; a 15 nodi scafo e timoniere fanno più del 60% della resistenza aerodinamica. Il gioco sventa solo lascando, che riduce anche la resistenza. Compito separato, insieme al timoniere che raddrizza troppo bene (`PROPOSTA-VELOCITA.md` §4).
3. **Di poppa il gioco resta dall'8 al 10% sotto Day**, a tutti i venti. Fuori da questo compito; registrato.
4. **La quota di Ri con 15 nodi** è un po' sotto Day (12,6% o 11,0% contro 15%).

---

## 7. Rischi e criteri della fermata 2

### Rischi

1. **L'angolo morto si stringe** (da circa 31° a 26-28° per lato): testi di `FISICA-E-TARATURE.md`, `CONTENUTI-DA-VERIFICARE.md`, lezioni e manuale da ricontrollare uno per uno.
2. **Lezioni:** «Orzare e l'angolo morto», «Ripartire», virata (3,3 nodi), «Da fermi» (2,5 nodi), i 40° dell'angolo morto delle lezioni (nel laboratorio `luffA0 + luffW` ≤ 40: rispettato, 29 o 31).
3. **Barca ferma nel vento:** la prua poggia da sola sotto `ironsA` = 36° anche con la vela piena da 29-31°. Succedeva già fra 34° e 36°; ora la fascia è più larga. Non lo cambio qui, lo misuro.
4. **Prove e regate:** cambia la bolina → fasce ritarate, **record azzerati** (chiavi `KEYV`).
5. **Avversari:** regolano il boma a `vento apparente − 17` (α = 17, sotto il massimo a 20) e partono da `minBoom`.
6. **Raffiche, retromarcia, virate:** Ri frena anche lì; `raffiche_e_virate.js` e `retromarcia.js` cambieranno.
7. **Disegno:** boma cazzato più vicino all'asse.
8. **Prototipo del fiocco:** resta col motore suo, dichiarato in `SPERIMENTALE.md`.
9. **Non-regressione:** la barca del gioco **cambia apposta**; `polare.js` e `raffiche_e_virate.js` daranno uscite diverse, riportate prima e dopo.

### Criteri

**Controlli di esecuzione** (numeri già visti: provano che il motore cambiato è quello misurato qui):
1. VMG, angoli, quote di Ri della riga della variante scelta (§4) uguali al banco, al centesimo e al decimo;
2. tabelle «Binns», «quanto vicino al vento» e «partenza da ferma» uguali al §4;
3. `polare.js` con **quattro motori**: oggi, solo A, solo B, A + B.

**Rapporti** (senza soglia): VMG contro Day fig. 8; Binns 9 e 12 nodi; angolo della VMG migliore contro Day fig. 9; vento apparente contro 27-33°; quota di Ri con 15 nodi contro fig. 11.

**Prove del gioco** (soglie dichiarate adesso, prima del collaudo):
4. **nessun conto in errore** con passi di 1/240 e 0,0125 s e cursori del laboratorio agli estremi; `TE` da 0,4 a 1,5 m, e 0 = senza resistenza indotta;
5. **laboratorio:** profilo «barca 1.0.10» (A e B spenti) che ridà `polare.js` di oggi **carattere per carattere**; A e B spegnibili uno alla volta;
6. **regate:** `collaudo_regate.py` (bastone e raffiche, semi 1-6) con 0 avversari BLOCCATI su 18 arrivi; `collaudo_partenze.py` OK;
7. **avversari:** VMG di bolina degli avversari con 10 nodi (pilota delle regate, semi 1-6), divisa per la VMG del banco con lo stesso motore. Soglia: il rapporto dopo **non scende più di 5 punti** sotto quello di oggi (oggi si misura in fermata 2, prima di cambiare il motore);
8. **«vela che sbatte»:** dove compare l'avviso (sotto `luffA0 + luffW/2`) la portanza è sotto il 50% del massimo (conto sulle formule: 41% in tutte e due le varianti, a 25,5° e a 27,5°);
9. **prove:** `collaudo_fasce.py`, fasce ritarate con la regola di `contenuti.js`;
10. **lezioni:** pilota sui semi 1-20, conferma sui semi 21-100 mai guardati; rapporto sui sei passi da correggere;
11. **pagina:** nessun errore con `#collaudo`, senza e con `#lab`; pannello 1360×650, eccesso 0 px;
12. `retromarcia.js`, `angolo_morto.js`, `raffiche_e_virate.js`: prima e dopo, riportati.

**Da guardare giocando (Ale):** di bolina con 6 e 10 nodi, quanto si stringe; dove la barca si ferma nell'angolo morto; una raffica di bolina con 15 nodi; una partenza da ferma.

---

## 8. Revisione in chat (16 ottobre 2026) e risposte

Testo completo della revisione: `fonti-pdf/REVISIONE-BOLINA.md` (fuori da git). Esito: **via condizionato** a cinque condizioni.

| Condizione | Risposta |
|---|---|
| 1. Togliere «massimo a 28,5° come Flay»; usare ORC a 28° e il «circa 34°» di Day §2.4; misurare la portanza a 28° oggi e con B | Fatto, §2 e §3: oggi 10%, 9° / 22° 81%, 11° / 24° 49%. Il massimo a 34° c'è già: il difetto è sotto il massimo |
| 2. Unità di `u` e peso della regolarizzazione; quote con un termine piccolo | `u` in m/s. Il termine piccolo non si può usare: con 0,05 la barca non riparte da ferma (§3 A). Resta 0,4, con il suo peso scritto (−29 / −13 / −9%) e la quota con 5 nodi dichiarata non indipendente |
| 3. Cosa contiene `appDA` (doppio conteggio) | Solo acqua: deriva e timone. In aria c'è solo `CD` della vela, che vale per tutta la barca. Nessun doppio conteggio (§1) |
| 4. Cosa contiene `res` (appendici sì o no) | Sì, con `appDA`: la quota sul totale è confrontabile con Day. Riporto anche Ri / scafo nudo (§4) |
| 5. Scelta 9° / 22° o 11° / 24°, con le tabelle davanti; resistenza della vela | Tabelle al §4 e §5; consiglio 9° / 22°, decide Ale. Resistenza 0,34, come suggerito |

Correzioni di lettura accolte: il 14% è Ri da sola; Day adotta ORC (0,20) nella condizione di Flay; `TE` dipende anche dal numero di Froude; lo sbandamento sopravento è solo in poppa; aggiunti Binns con 12 nodi (fig. 5), l'angolo di Day (fig. 9), la ripartizione aerodinamica (fig. 12) e la forma della curva fra 10 e 15 nodi.

Altre richieste accolte: laboratorio con A e B spegnibili e `polare.js` con quattro motori (criteri 3 e 5); criterio sugli avversari con soglia (7); avviso «vela che sbatte» (8); partenza da ferma (§4).

---

## 9. Decisioni per Ale

1. **Variante della vela: DECISA da Ale il 16 ottobre 2026, 9° / 22°** (`minBoom` 9°, `luffA0` 22°, peso di CL² 0,08, `TE` 0,80 m), dopo aver visto le tabelle del §4 e §5 e le fonti cercate in più (§2).
2. **Il via** alla fermata 2, versione 1.0.11, record azzerati.

---

## 10. Esito della fermata 2 (16 ottobre 2026, versione 1.0.11)

Variante 9° / 22° (`minBoom` 9°, `luffA0` 22°, `sailCL2` 0,08, `TE` 0,80 m). Riferimento «prima» preso sul motore della 1.0.10 prima di cambiarlo, o su una copia della 1.0.10 presa da git (lezioni, partenze), o con i valori della 1.0.10 rimessi nella pagina (avversari: dà la stessa polare carattere per carattere).

| Criterio | Esito |
|---|---|
| 1-2. Numeri del §4 sul motore vero | **Uguali** (VMG, angoli, quote, Binns, vicino al vento, partenza da ferma), con il banco nuovo `tests/fisica/bolina.js` |
| 3. `polare.js` con quattro motori | Fatto (`node bolina.js polare 1010 / soloA / soloB` e `polare.js`); la barca 1.0.10 ridà `polare.js` di prima **carattere per carattere** |
| 4. Nessun conto in errore | 12.960 casi (`TE` 0 / 0,05 / 0,4 / 0,8 / 1,5, `minBoom` 5 / 9 / 20, `sailCL2` 0,02 / 0,2, passi 1/240 e 0,0125 s, vento 0-25 nodi, sei andature, tre comandi, tre velocità iniziali): **0 in errore** |
| 5. Laboratorio | OK (`collaudo_laboratorio.py`); profili «barca della 1.0.10», «senza resistenza indotta», «vela della 1.0.10» |
| 6. Regate | Bastone e raffiche, semi 1-6: **18 arrivi su 18** ciascuna, 0 BLOCCATE; partenze OK e uguali alla 1.0.10 |
| 7. Avversari | VMG di bolina 2,45 → 2,44 nodi; rapporto col banco 78,3% → 74,2%: **−4,1 punti, dentro la soglia di 5** |
| 8. «Vela che sbatte» | Per costruzione: 41% della portanza dove compare l'avviso (25,5°) |
| 9. Prove | Fasce ritarate: 3 [160, 200, 255], 4 [280, 350, 450], 5 [300, 375, 480]; prova 5 finita 24 volte su 24 |
| 10. Lezioni | Semi 1-20 e conferma 21-100, contro la 1.0.10 sugli stessi semi: **«Orzare e l'angolo morto» si rompe** (guidando 0 su 80, prima 74 su 80); il resto sotto |
| 11. Pagina | Senza niente, con `#collaudo` e con `#lab`: 0 errori; pannello 1360×650 eccesso 0 px |
| 12. Altri banchi | `retromarcia.js` quasi uguale; `angolo_morto.js` 2.184 su 2.196 (prima 2.188), 41 su 4.860 (prima 28); `raffiche_e_virate.js` vedi sotto |

**Cosa non era previsto nella proposta:**
- **Lezione 1, «Orzare e l'angolo morto».** Orzando dalla poppa e tenendo la barra «finché la barca non si ferma quasi del tutto», la barca arriva al vento con più velocità e lo attraversa: vira sull'altra mura invece di piantarsi. Il passo chiede prua a meno di 40° dal vento e meno di 1,5 nodi; con la vela nuova la barca a 35° va ancora a 2,7 nodi. **Prova di Ale giocando** (16 ottobre, `sessione-20261016-1916.txt`, un tentativo): orzando a piccoli colpi, prua ferma a 11-19° dal vento, passo completato in 10 s, «funziona perfettamente». Deciso di non cambiarlo ora; da riguardare nelle correzioni dei passi, perché tenendo il tasto di continuo la barca vira.
- **Raffiche (§7 rischio 6 diceva «qualche grado»).** `raffiche_e_virate.js` passa da 28° / 42° / 55° a 38° / 54° / **67° (scuffia)**: tiene fissa la scotta a 0,1, e con `minBoom` 9° la stessa scotta cazza la vela di 4,5° in più. A parità di boma (21,1°) la barca sbanda **meno** di prima: 26° / 39° / 53°. Con la scotta suggerita dal gioco una raffica da 20 nodi fa scuffiare sia prima (71°) sia dopo (67°).
- **Lezione 5 passo 4 nel collaudo del suggerimento:** anche il caso 4 (45° dal vento, −0,5 nodi, scotta a metà) riparte senza piantarsi; elenco dei casi «non misurati» aggiornato **dopo** aver visto il risultato (tutti i 20 casi riusciti).

**Lezioni, il resto (semi 21-100, prima → dopo):** «Ripartire» già fatto dopo un colpo lungo 29 → 2, ma a mani ferme 1 → 17 (arriva dal passo prima saltato); «La scuffia» a mani ferme 28 → 21, dopo un colpo lungo 20 → 11; «Assorbire una raffica» a mani ferme 46 → 54; «Troppo cazzata» dopo un colpo lungo 7 → 1; «Risalire il vento» 71 → 67 s.

---

## 11. Ultimo tentativo sulla bolina lenta con poco vento (17 ottobre 2026, fermata 1, versione 1.0.22)

**Fermata 1: il motore non è stato toccato.** Misure con una copia di `js/motore.js` cambiata solo in memoria (script fuori dal repository, stesso banco del §4: angoli dal vento reale da 34° a 60° grado per grado, scotta a passi di 0,02, 60 s di equilibrio). Il banco non usa numeri casuali: un giro basta, e la riga «oggi» ridà i numeri della 1.0.11 (VMG 2,25 / 3,29 / 4,07, Binns uguali al §4).

### 11.1 Cosa ho misurato [misura]

**Al punto di VMG migliore**, oggi:

| Vento | Barca | Apparente | Incidenza | Portanza della vela | Sbandamento | Timoniere fuori | Scarroccio |
|---|---|---|---|---|---|---|---|
| 6 nodi | 3,18 nodi a 45° | 29,0° | 20,0° | **piena** (CL 1,35, rampa al 100%) | 4,7° | 25% | 2,3° |
| 10 nodi | 4,66 nodi a 45° | 30,5° | 20,0° | piena | 4,9° | 71% | 2,1° |
| 15 nodi | 5,66 nodi a 44° | 32,0° | 13,8° | sventata (CL 0,93) | 5,0° | 99% | 1,6° |

- **Con poco vento la vela porta già al massimo**: la causa non è la rampa dell'angolo morto. Spostarla di 4° o renderla un gradino non cambia la VMG al centesimo.
- **Esclusi (nessun effetto, al centesimo, su VMG e Binns con 9 nodi):** timoniere che può spostarsi anche sottovento (barca piatta con poco vento, come dice Day §6.2); vasca sotto i 3 nodi più leggera del 10%. Barca tenuta per forza sempre piatta: +0,01 nodi con 6 nodi.
- **Acqua: d'accordo con Day.** Con 6 nodi lo scafo nudo fa il 64% della resistenza in acqua (Day fig. 11, 5 nodi: 67%), la resistenza indotta l'11% (Day 8%; con 5 nodi il gioco dà 8,4%, §4).

**Prove di sensibilità** (scarto contro Day fig. 8 e contro le misure di Binns, fig. 4 e 5):

| Copia del motore | Day 6 / 10 / 15 nodi | Binns 9 nodi, 42°-60° | Binns 12 nodi, 42°-60° |
|---|---|---|---|
| oggi | −15 / −9 / +7% | −14 −11 −13 −14% | −1 −1 −1 0 +1% |
| vela più forte del 15% (portanza e resistenza) | −11 / −5 / +9% | −13 −8 −9 −10% | +2 +1 +2 +2 +4% |
| vela più forte del 30% | −8 / −3 / +9% | −11 −5 −6 −7% | +3 +3 +4 +4 +6% |
| resistenza della vela 0,27 | −9 / −3 / +12% | −10 −6 −9 −10% | +6 +5 +6 +6 +6% |
| resistenza della vela 0,21 | −4 / +2 / +16% | −7 −2 −6 −8% | +10 +10 +11 +10 +12% |
| braccio della vela `zCE` 2,4 m | −15 / −9 / +3% | uguale a oggi | −3 −3 −4 −3 −3% |
| braccio della vela `zCE` 2,8 m | −15 / −9 / −1% | uguale a oggi | −4 −6 −6 −7 −6% |
| resistenza 0,27 + `zCE` 2,8 m | −9 / −3 / +2% | −10 −6 −9 −10% | −1 −2 −3 −3 −2% |

### 11.2 Cosa se ne ricava

1. **Nessun ritocco della sola vela mette a posto insieme 9 e 12 nodi.** Fra 9 e 12 nodi la barca di Binns guadagna circa l'8% (5,0 → 5,4 a 46,5°), il gioco il 21%. Una vela più forte o meno frenata alza 9 nodi ma porta 12 nodi sopra le misure.
2. **Il braccio sbandante `zCE` = 2,0 m non ha una fonte** (`FISICA-E-TARATURE.md`, tabella delle costanti: «altezza del centro velico») e cambia solo il vento forte: con 2,8 m il +7% con 15 nodi diventa −1%, e con 9 nodi non cambia niente. Fisicamente il braccio va dal centro velico al centro della spinta laterale sotto l'acqua, non dal pelo dell'acqua [stima]. Day mette il centro velico al 36,4% dell'inferitura sopra il boma (§2.1) e la spinta della deriva al 43% della sua profondità (§3), ma non scrive le misure dell'armo (la tabella 2 dà solo lo scafo): **il numero non c'è nel materiale in mano.**
3. **La resistenza della vela del gioco è più alta di quella di Day.** Il gioco usa 0,34 = 0,27 di Flay in galleria (vela, albero e scafo, senza timoniere) + 0,07 per il timoniere (§3 B); Day, nella stessa condizione, adotta lo 0,20 dei coefficienti ORC (§2.1) più il timoniere a parte. È una scelta già fatta e motivata il 16 ottobre (§8, condizione 5), non un errore: la riporto perché da sola spiega circa 6 dei 15 punti con 6 nodi.
4. **Anche con le due correzioni insieme resta circa −9% con poco vento** (Day con 6 nodi, Binns con 9). **La causa di quel residuo non è stata trovata.**

### 11.3 Proposta

**Decisione di Ale, 17 ottobre 2026: «A»** (limite noto, motore invariato, livello 1 chiuso).

Secondo la regola decisa da Ale il 17 ottobre («se la causa non si trova, limite noto dichiarato e livello 1 chiuso»), **propongo di non toccare il motore**:

- **Limite noto, dichiarato** in `FISICA-E-TARATURE.md` e qui: con poco vento la bolina è dal 9% al 15% più lenta delle fonti, e con 15 nodi il 7% più veloce. Si scrive cosa è escluso (§11.1), cosa spiega una parte (braccio sbandante senza fonte, resistenza della vela scelta più alta di Day) e cosa resta senza causa (circa −9%).
- **`zCE` va fra i dubbi** (`DUBBI-E-RICERCHE.md`): da risolvere quando si cambia la barca (livello 3, barca a due), cercando prima una misura dell'armo con una fonte usabile (principio 5), altrimenti fermandosi.
- **Livello 1 chiuso**, si passa al livello 2.

**Alternativa, se Ale vuole correggere almeno il vento forte:** fermata 2 sul solo `zCE`, **solo dopo aver trovato una fonte** per l'altezza del centro velico e per la profondità della deriva. Soglie dichiarate adesso, come attese nostre: VMG con 15 nodi entro ±5% da Day; Binns con 12 nodi entro ±5% a tutti gli angoli; con 6, 9 e 10 nodi nessun peggioramento oltre 0,02 nodi. Costo: cambiano sbandamento e raffiche (`raffiche_e_virate.js`, lezioni «Assorbire una raffica» e «La scuffia»), fasce delle prove ritarate e record azzerati, revisione in chat prima della fermata 2. **Rischio:** il livello 1 appena chiuso nei collaudi si riapre.
