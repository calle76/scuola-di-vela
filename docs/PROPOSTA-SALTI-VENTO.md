# Proposta: i salti di vento (livello 2)

Del 17 ottobre 2026. **Fermata 1: nessun codice nel gioco.** Misure con `tests/fisica/salti_bolina.js` (barca del livello 2 e un pilota, fuori dal gioco). Terzo pezzo della barca del livello 2 deciso da Ale (`VISIONE-LIVELLI-E-CARRIERA.md` §3); la linea di partenza resta perpendicolare al vento medio e sono i salti a renderla storta.

Tipi delle affermazioni: **[fonte]**, **[misura]**, **[stima]**, **[giudizio]**.

---

## 0. In breve

1. **Cosa dicono le fonti** [fonte, divulgative e coerenti fra loro]: in regata il vento oscilla di circa 10-20° (a volte fino a 40°) con un periodo di circa 3,5-8 minuti; si vira sugli scarsi e si resta sulle mure buone; se il periodo è sotto i 2 minuti virare sui salti di solito non ripaga le virate; se il ciclo è più lungo della bolina il salto si gioca come persistente (si va verso la parte da cui ruota il vento).
2. **Il gioco oggi** [codice]: con le raffiche accese il vento oscilla di ±3° ogni 4,7 minuti più ±1,5° ogni 1,8 minuti, e ogni raffica ha un suo salto (fino a ±6° o ±10°). Senza raffiche il vento non gira mai. La regata ha la boa di bolina a **140 m**: la bolina dura circa 90 s, contro gli 8-15 minuti di una bolina vera.
3. **La misura più importante** [misura]: con una bolina di 140 m virare sui salti fa guadagnare al massimo il 2-4%, qualunque sia il salto: la bolina è troppo corta rispetto ai salti veri, e i salti veloci costano più virate di quanto rendano. Con una bolina di **300 m** (circa 3,3 minuti) e salti di ±15° ogni 2-3 minuti si guadagna il **10-12%**; con 400 m e ±15° ogni 4 minuti l'11%. Il guadagno c'è quando il periodo è circa 0,6-0,9 volte la durata della bolina.
4. **Proposta** [giudizio]: nelle regate del livello 2 la bolina passa a 300 m e il vento oscilla in modo irregolare attorno al vento medio, con ampiezza 8-15° e periodo 2-3 minuti, uguale in tutto il campo; in alcune regate il vento ruota sempre dalla stessa parte (salto persistente). Così la tattica «vira sugli scarsi» vale circa il 10% della bolina, come dicono le fonti. Le regate durano di più (stima: da circa 3 a circa 6 minuti più la preparazione).

---

## 1. Le fonti

| Fonte | Tipo | Cosa dice (parafrasi) |
|---|---|---|
| Dellenbaugh, «Windshift Rules of Thumb», *Sailing World* (1987, ripubblicato 2020); stesso autore di F7 | Rivista, allenatore | Sui salti oscillanti si vira sugli scarsi e si resta sulle mure buone; la «prua media» è la media delle prue più alta e più bassa viste su una mura (nell'esempio 240-270°, cioè ±15°), e si vira quando si è scarsi di una decina di gradi; nell'esempio ogni oscillazione dura circa 4 minuti; quando alla boa manca meno di un'oscillazione, l'ultimo salto si gioca come persistente. Sui salti persistenti si va verso lo scarso invece di virare |
| Raymarine, guida «Wireless Race Master» | Costruttore di strumenti | Il periodo si misura col tempo fra una virata sugli scarsi e la successiva; **sotto circa 2 minuti** le virate possono costare più di quanto rendono i salti; se il ciclo è più lungo della bolina i salti vanno giocati come persistenti; più i salti sono ampi e regolari, più conta stare in fase |
| Cronache di regate (WindCheck, Sailing World) | Divulgazione | Oscillazioni misurate di 10-19° con 3,5-4,5 minuti fra l'una e l'altra; in un altro giorno 15-18°; fino a 40° in certe giornate; periodi di 5-8 minuti su percorsi brevi |
| Ciccarella, Dalang, Vinckenbosch, arXiv 2404.03773 (2024), e gli studi statistici fatti per una squadra di America's Cup che cita | Articolo scientifico | Le variazioni di direzione del vento contano più di quelle d'intensità; nei dati disponibili gli incrementi della direzione sono descritti bene da un moto casuale (gaussiano) senza tendenza. **Nessun valore numerico** nelle pagine lette |

Nessuna fonte con licenza libera dà una tabella di numeri: ampiezze e periodi sono **ordini di grandezza da divulgazione**, usati come fascia, non come taratura.

---

## 2. Le misure [misura]

`node tests/fisica/salti_bolina.js D '[[A,P],...]'`: barca del livello 2, 10 nodi, vento medio da nord che oscilla di ±A gradi con periodo P secondi; 24 fasi del salto per ogni caso; due strategie con le stesse regole per lay line e bordi del campo (largo mezza bolina per lato): **«due bordi»** ignora i salti, **«sui salti»** vira in più quando è scarso di oltre 5° rispetto al vento medio (conosciuto: lo si osserva prima della partenza). Nessuna corsa fallita.

| Bolina | Salti | Due bordi | Sui salti | Guadagno |
|---|---|---|---|---|
| 140 m (oggi) | ±10° ogni 30 s | 101 s | 173 s (11 virate) | **−71%** |
| 140 m | ±15° ogni 60 s | 108 s | 104 s | +4% |
| 140 m | ±15° ogni 120 s | 92 s | 90 s | +2% |
| 140 m | ±15° ogni 240 s | 89 s | 108 s | −21% (salto più lungo della bolina) |
| 300 m | ±10° ogni 120 / 180 s | 211 / 205 s | 201 / 193 s | +5% / +5% |
| 300 m | ±15° ogni 120 s | 216 s | 194 s | **+10%** |
| 300 m | ±15° ogni 180 s | 203 s | 179 s | **+12%** |
| 300 m | ±15° ogni 240 s | 191 s | 186 s | +3% |
| 400 m | ±15° ogni 60 s | 271 s | 298 s | −10% |
| 400 m | ±15° ogni 240 s | 265 s | 236 s | **+11%** |
| 400 m | ±20° ogni 240 s | 257 s | 229 s | +11% |

Lettura:
- **Periodo corto = virare sui salti costa** (−71% con 30 s): le virate della barca costano più di quanto rendano i salti. È quello che dice Raymarine.
- **Periodo lungo rispetto alla bolina = il salto è persistente**: virare sugli scarsi è sbagliato (−21% con 240 s su 140 m). È quello che dicono Dellenbaugh e Raymarine. *Limite del pilota:* non riconosce un salto persistente e vira a vuoto; in quei casi il numero esagera la perdita.
- **Il guadagno c'è quando il periodo è circa 0,6-0,9 volte la bolina** e l'ampiezza è almeno ±10-15°.
- **Con la bolina di oggi (140 m) i salti realistici non danno tattica**: o sono troppo lenti (persistenti) o troppo veloci (costano virate).

---

## 3. Il modello proposto [giudizio, stime]

Solo nelle regate e nella navigazione libera del livello 2:

1. **Vento oscillante, uguale in tutto il campo.** Direzione = vento medio + un'oscillazione irregolare: ogni mezza oscillazione sceglie a caso la sua ampiezza (fra 8° e 15°) e la sua durata (fra 60 e 90 s, quindi periodo fra 2 e 3 minuti), con passaggi morbidi (mezza sinusoide). Così i salti non si possono prevedere a orologio ma hanno il ritmo delle fonti. Le raffiche restano come sono, con il loro piccolo salto.
2. **Salto persistente** in alcune regate: il vento ruota sempre dalla stessa parte, 10-20° nella durata della bolina, più una piccola oscillazione. La tattica giusta è l'opposto (andare verso la parte da cui ruota).
3. **Bolina di 300 m** nelle regate del livello 2 (oggi 140), linea di partenza perpendicolare al **vento medio**: un salto al momento del via rende un'estremità più vantaggiosa.
4. **Il livello 1 non cambia** (regate, prove, impronta).

**Costanti nuove, tutte ipotesi dentro le fasce delle fonti, ridotte nel periodo per stare nel campo del gioco (dichiarato):**

| Costante | Valore | Perché |
|---|---|---|
| ampiezza dell'oscillazione | 8-15° a caso per mezza oscillazione | Fonti: 10-20° tipico |
| durata di mezza oscillazione | 60-90 s (periodo 2-3 min) | Fonti: 3,5-8 min; ridotto perché il percorso è più corto, mantenendo il rapporto periodo/bolina che dà il guadagno |
| salto persistente | 10-20° nella durata di una bolina | Fonti: esiste, nessun numero |
| bolina delle regate | 300 m | Misura del §2 |

**Cosa vede chi gioca**: la prua in gradi c'è già nel pannello («Prua 040°»), ed è proprio lo strumento delle fonti (la bussola). Proposta, per dopo e come aiuto disattivabile (principio 3): accanto alla prua, di quanto si è buoni o scarsi rispetto al vento medio. Prima si prova senza.

---

## 4. Criteri per la fermata 2 (attese nostre)

Dichiarato: le fasce sono scelte **dopo** le misure del §2.

- **S1** Nel gioco, sulla bolina di 300 m con il vento del §3, il pilota «sui salti» batte il pilota «due bordi» in media di almeno il 5% e in almeno 2 regate su 3 (40 semi di taratura, poi 40 mai guardati).
- **S2** Con il salto persistente il pilota che va verso la parte da cui ruota il vento batte quello che va dall'altra parte, in almeno 3 regate su 4.
- **S3** Gli avversari del livello 2 finiscono tutte le regate col vento nuovo (nessuno fermo o fuori dal campo).
- **S4** Il livello 1 identico al bit (impronta, `polare.js`, `raffiche_e_virate.js`); la barca del livello 2 senza salti identica alla 1.0.27.
- **S5** Pannello a 1360×650 senza eccesso; pagina senza `#collaudo` senza errori.

---

## 5. Rischi

- **Regate più lunghe**: da circa 3 a circa 6 minuti più la preparazione (3 minuti di serie). È una scelta di gioco.
- **Il livello 2 come schermata non esiste ancora**: le regate col vento nuovo servono una regata del livello 2 (oggi c'è solo la barca in prova nella navigazione libera). Proposta: una regata «Regata nei salti di vento» provvisoria, raggiungibile come la barca in prova, finché non c'è il menu dei livelli.
- **Gli avversari non giocano i salti**: guidano col vento del momento, quindi seguono i salti senza sceglierli. Un giocatore bravo li batterà sui salti: va bene per insegnare, ma va detto. Avversari che giocano i salti: dopo, con gli avversari del livello 2.
- **Periodi accorciati**: 2-3 minuti invece di 3,5-8. Dichiarato come semplificazione; il rapporto con la bolina è quello che conta (§2).
- **Il vento è uguale in tutto il campo**: nella realtà i salti arrivano con le raffiche e si vedono sull'acqua. Le raffiche del gioco hanno già un loro salto; il vento oscillante uguale ovunque è la semplificazione più piccola.

---

## 6. Decisioni che spettano ad Ale

1. Il via alla fermata 2.
2. La bolina di 300 m nelle regate del livello 2, con regate più lunghe (circa 6 minuti), oppure un'altra lunghezza.
3. Dove si prova finché non c'è il menu dei livelli: una regata provvisoria «nei salti di vento» con la barca del livello 2, e i salti anche nella navigazione libera con la barca del livello 2.

**Ale, 17 ottobre 2026:** bolina di 300 m va bene, le regate saranno più lunghe. E i percorsi non sono solo «a bastone» (avanti e indietro da una boa): esistono anche percorsi **a trapezio** e **a triangolo**. Da prevedere nelle regate del livello 2, con una ricerca sulle fonti (forma, angoli dei lati, quali lati sono di lasco), dopo i salti di vento.

