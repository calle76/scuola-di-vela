# Voce 88, onde nel motore: ricerca delle fonti (26 novembre 2026)

Via di Ale: «Via. Ma non fermarti ai primi risultati. Accumula ricerche». Ricerca e basta: `js/` non si tocca. Le fonti hanno qui una sigla (O1, O2…) e, se nuove, il numero F di `docs/FONTI-PUBBLICHE.md` (F138-F145).

## Le domande

1. **Surf in poppa e al lasco:** quanto rende su una deriva da 4 m, con che onde, e con quale modello semplice.
2. **Bolina con le onde:** quanto frena (resistenza aggiunta, velocità persa).
3. **Che onde ci sono** con 10-20 nodi su un lago o vicino a costa (altezza, periodo, lunghezza, velocità).

## Fonti trovate

### O1 (F138). He, Zhang, Ma, «Hydrodynamic characteristics of an ILCA6 sailing dinghy in calm water and head waves», *Scientific Reports* 16:37050 (2026), https://doi.org/10.1038/s41598-026-66658-z, licenza CC BY 4.0 (letto il PDF intero)

- CFD, scafo dell'ILCA 6 (lo stesso scafo dell'ILCA 7) con onde di prua regolari. Tab. 1: Lwl 3,381 m, Bwl 1,105 m, massa 58 kg + 65 kg (velista come massa), Iyy 95 kg m².
- Velocità 2-6 m/s; lunghezza d'onda da 0,5 a 2 volte Lwl; **altezza d'onda 4 cm soltanto** (onde piccolissime).
- Fig. 11a (letta dal grafico, ±5 N): resistenza in acqua piatta circa 22 / 85 / 125 / 155 / 195 N a 2 / 3 / 4 / 5 / 6 m/s; con le onde da 4 cm fino a circa 205 N a 5 m/s (+30%) e 235 N a 6 m/s (+20%).
- Fig. 11b: coefficiente di resistenza aggiunta Caw = Raw / (ρ g ζa² Bwl²/Lwl) fra 0 e 2 a 2-3 m/s, fino a 5-8 a 4-6 m/s. Con ζa = 2 cm, 1 punto di Caw vale circa 1,5 N.
- Gli autori: la barca leggera cambia molto assetto e immersione, quindi la resistenza aggiunta non segue solo il beccheggio; nessuna prova in vasca di conferma (dicono che servirebbe).
- **Uso possibile:** l'andamento (cresce con la velocità e con onde lunghe come lo scafo), non la grandezza: con onde vere (20-40 cm) la teoria lineare (cresce col quadrato dell'altezza) darebbe numeri assurdi (centinaia di newton), quindi non si estrapola.

### O2 (F139). A. Persson, *Predicting Yacht Performance in Waves Using a CFD Velocity Prediction Program*, tesi di dottorato, Chalmers, 2025, https://research.chalmers.se/publication/546243 (letta: cap. 2.4, 2.5, 5, 6)

- Elenca da dove viene la resistenza in onda (van Oossanen 2019): moto di sussulto e beccheggio; onda riflessa; più forza laterale; più timone per tenere la rotta; poi momento raddrizzante, lunghezza al galleggiamento e superficie bagnata che cambiano.
- Larsson (1990): la resistenza aggiunta è l'effetto più importante per la velocità media con mare di prua.
- **In poppa «la perdita di velocità (vista di bolina) diventa spesso un guadagno»** (cap. 1.2): il suo lavoro si ferma alla bolina.
- Barca di 14 m: nessun numero utile per una deriva.
- Rassegna dei metodi: Harris, Thomas e Renilson (2001) simulano la barca in poppa con le onde con **un solo grado di libertà** (avanti/indietro): resistenza, spinta della vela e forza dell'onda di Froude-Krylov, partendo dai risultati di una VPP in acqua piatta. È il modello più semplice ed è quello che Day (F17) suggerisce per stimare il surf.

### O3 (F140). Maki, Sakai, Ueta, «Review of the analytical prediction method of surf-riding threshold in following sea…», arXiv 2406.12853 (2023) (letto in parte)

- Navi, non barche a vela, ma il modello è lo stesso di O2 (Harris): equazione del moto lungo l'onda (massa + massa aggiunta) · accelerazione = spinta − resistenza + forza dell'onda; la forza dell'onda è una sinusoide della posizione sull'onda: −f · sin(k ξ).
- Il surf «aggancia» la barca alla velocità dell'onda c; per le navi la soglia approssimata dell'IMO è un numero di Froude di 0,3 (MSC.1/Circ.707).
- Esempio numerico: soglia del surf a Fr 0,33 con onda lunga 1,25 volte la nave e ripida 0,04 (altezza / lunghezza).

### O4. Day 2017 (F17, già nelle fonti; riletto per le onde)

- «Il modello trascura le onde, che contano in alcune condizioni: … guadagni di velocità col surf in poppa» (sez. 2 e 6.1).
- I dati di Binns (9 e 12 nodi) sono presi «in condizioni dove ci si poteva aspettare un po' di surf in poppa»: la VPP di Day è più lenta in poppa, e anche aggiungere 2 nodi di vento chiude solo in parte la distanza. Day conclude che è più probabile che la differenza venga da surf e/o movimenti del velista.
- Suggerisce Harris e altri (2001) per stimare il surf, «ma servono le onde del giorno delle misure».

### O5. Schutt 2017 (F109, già nelle fonti; riletto per le onde)

- Le misure delle S (il +19% di VMG) sono su un lago (Cayuga), vento 12 nodi; **le onde non sono descritte né misurate**. Il guadagno lui lo spiega col rollio e col vento apparente che la vela vede muovendosi (la «spinta» nel passaggio dallo strapoggio alla poppa piena), non col surf.
- Scrive che con onde e vento medio-leggero conviene usare le S per «prendere» le onde e passare dall'una all'altra.
- **Correzione alla voce 86 di DA-FARE:** lì era scritto «+19%, comprese le onde che il gioco non ha». Più giusto: +19% su un lago, in parte senza onde: le S rendono anche in acqua quasi piatta.

### O6. Binns, McRae, Thomas, «The Windward Performance of Yachts in Rough Water», 14th Chesapeake Sailing Yacht Symposium, 1999; McRae, Binns, Klaka, Dovell, «Windward performance of the AME CRC systematic yacht series», RINA Modern Yacht, 1998 (copie da cmst.curtin.edu.au)

- Barche di 11,3 m in vasca, solo bolina. Nessun dato per una deriva. Servono solo come contesto (metodo con l'operatore di risposta).

### O7 (F144). Pagine di tecnica (fonti basse, solo qualitative)

- Tillerman, «How to Sail a Laser Downwind in Waves», blog Proper Course, 26 giugno 2013: circa 12 nodi; strapoggio o lasco molto largo sono più veloci della poppa piena; si gira ogni pochi secondi per prendere più onde; «una pompata per onda» è ammessa (regola 42).
- Blog dell'associazione inglese della classe (ILCA UK, n. 65, data senza anno): sbandare sottovento aiuta a orzare verso il lasco, sopravvento a poggiare verso lo strapoggio; «a meno che sia molto ventoso, le onde passano sotto la barca» (la barca è più lenta delle onde); peso avanti per surfare, indietro se la prua si pianta.
- World Sailing, interpretazioni della regola 42 per il Laser: una pompata per onda o raffica per iniziare il surf o la planata, e solo se la barca poi accelera davvero giù dall'onda.

### O8 (F141). D. Harris, G. Thomas, M. Renilson, «Downwind Performance of Yachts in Waves», 2nd Australian Sailing Science Conference, Hobart, febbraio 1999, https://cmst.curtin.edu.au/local/docs/pubs/sailingscience99.pdf (letto intero; licenza non scritta)

- **È il modello che ci serve, il più semplice con una base.** Un solo grado di libertà (avanti): (massa + massa aggiunta) × accelerazione = forza dell'onda X(ξ) + resistenza R(u) + spinta della vela T(vento apparente). Passo di 0,1 s.
- Forza dell'onda (Froude-Krylov, ipotesi «quasi statica»: dipende solo da dove sta la barca sull'onda): X(ξ) = −ρ g ζ k ∫ e^(−k d(x)) S(x) sin k(ξ + x) dx (S = area della sezione immersa). Per uno scafo corto rispetto all'onda vuol dire: **peso della barca × pendenza dell'onda**, ridotto quando la barca è lunga quanto mezza onda.
- Prove in vasca (scafo di 10 m in scala 1:6,7, onde 1/30-1/20 di ripidità, lunghezza 1-2 volte lo scafo): la teoria va «eccezionalmente bene» con onda lunga 1,5 volte lo scafo, peggio con onde più lunghe (fig. 15); la forza cresce quasi in proporzione all'altezza dell'onda (fig. 14). Forza massima sul fianco davanti dell'onda.
- Esempio (fig. 4): onda di 20 m, vento 15 nodi: con 0,6 m la velocità oscilla, con 2,0 m la barca viene accelerata fino alla velocità dell'onda e ci resta (surf). Il risultato dipende da dove la barca parte sull'onda.
- Falsone (1997), citato: con onde da poppa più lunghe di circa due scafi la resistenza aggiunta è **negativa** (aiutano); oltre cinque scafi torna come in acqua piatta.

### O9 (F142). Onde da vento con poco spazio (fetch): Shore Protection Manual 1984, eq. 3-39/3-40, riportate nel corso NPTEL «Module VI, Wind-wave modelling» (IIT Madras), https://archive.nptel.ac.in/content/storage2/courses/114106028/Module-6.pdf (letto)

- g Hm0 / UA² = 0,0016 (g F / UA²)^½; g Tp / UA = 0,286 (g F / UA²)^⅓; UA = 0,71 U10^1,23 (m/s). F = fetch (spazio d'acqua su cui soffia il vento).
- Il Coastal Engineering Manual (2003, eq. II-2-36) ha la stessa forma con u* (coefficienti 4,13·10⁻² e 0,651): letto solo in modo confuso, non usato.
- Calcolo (`onde_fetch.py`): vedi tabella sotto.

### O10 (F143). ORC, *VPP Documentation 2023*, cap. 6.8 «Added Resistance in Waves», https://orc2.orc.org/rules/ORC%20VPP%20Documentation%202023.pdf (letto il cap. 6.8)

- Una boa ha misurato le onde in varie regate negli Stati Uniti; lo spettro è stato normalizzato sul vento, col periodo fisso a 5 s (mare aperto).
- **Con l'altezza che cresceva in modo lineare col vento, la resistenza aggiunta era troppo alta: con 6-8 nodi pesava troppo «quando i velisti vedevano che non c'erano onde»**. L'ORC ha messo un «avvallamento» nella curva: fattore del mare per barche di 25 piedi 1,06 / 2,87 / 6,1 / 10,0 / 13,5 / 16,0 / 18,0 / 20,0 con 6 / 8 / 10 / 12 / 14 / 16 / 18 / 20 nodi (fig. 6.13). In pratica **niente onde che contano fino a 8 nodi, poi crescono in fretta fra 10 e 16 nodi**.
- La resistenza aggiunta di bolina è calcolata per onde di prua e moltiplicata per 0,55 perché la barca va a circa 45° dalle onde.
- Formula per barche a chiglia (25-75 piedi): non si applica a una deriva da 4 m.

### O11. Regate: Pan e Sun (F134) e regole

- Pan e Sun (regate in mare): VMG di poppa oltre 12 nodi 7,8 nodi; la barca M con 15 nodi fa 6,28 (−20%). In regata contano onde, S, pompate dove la regola 42 lo permette (una per onda per cominciare il surf: regola 42.3(c)). Per l'ILCA la regola 42 non è allentata col vento forte: quello vale per la classe Finn (forum di regolamento, non verificato sul testo delle regole di classe).

## Le onde con il vento del gioco (`onde_fetch.py`, SPM 1984)

| vento | fetch 2 km | 5 km | 10 km | 20 km |
|---|---|---|---|---|
| 6 nodi | 0,06 m, 1,1 s, 1,9 m, 3,4 nodi | 0,10 m, 3,6 m, 4,6 nodi | 0,15 m, 5,7 m, 5,8 nodi | 0,20 m, 8,6 m, 7,1 nodi |
| 10 nodi | 0,12 m, 2,9 m, 4,2 nodi | 0,19 m, 5,4 m, 5,7 nodi | 0,27 m, 8,6 m, 7,1 nodi | 0,38 m, 13,7 m, 9,0 nodi |
| 15 nodi | 0,20 m, 4,1 m, 4,9 nodi | 0,32 m, 7,6 m, 6,7 nodi | 0,45 m, 12,0 m, 8,4 nodi | 0,63 m, 19,0 m, 10,6 nodi |
| 20 nodi | 0,29 m, 5,2 m, 5,5 nodi | 0,45 m, 9,6 m, 7,5 nodi | 0,64 m, 15,2 m, 9,5 nodi | 0,90 m, 24,1 m, 11,9 nodi |

(altezza significativa, lunghezza dell'onda al periodo di picco, velocità dell'onda; ripidità fra 1/18 e 1/43)

**Cosa dice:** con poco spazio (un lago, una baia) le onde sono corte (1-3 volte la barca) e lente (4-8 nodi), **circa quanto la barca in poppa**: è proprio la condizione in cui si surfa, e spiega «a meno che sia molto ventoso, le onde passano sotto la barca» (O7). In mare aperto le onde sono più lunghe e veloci della barca.

## Prova grezza sul banco: la barca M con la forza dell'onda di Harris (`surf_grezzo.js`)

Prua ferma (come il pilota del banco), scotta migliore in acqua piatta, nessun beccheggio, nessuna resistenza aggiunta, niente timone: **solo ordine di grandezza**. Onde regolari (altezza = Hs) e irregolari (5 componenti, 10 semi fissi).

| vento, fetch | angolo | piatta | regolari | irregolari (10 semi) | punta |
|---|---|---|---|---|---|
| 10 n, 5 km | 180 / 150 / 135 | 4,47 / 4,72 / 5,19 | +26 / +4 / −1% | +4 / +2 / −1% | 5,9-6,1 |
| 12 n, 5 km | 180 / 150 / 135 | 5,12 / 5,42 / 5,96 | +19 / +30 / +1% | +7 / +3 / +3% | 6,8-7,5 |
| 15 n, 2 km | 180 / 150 / 135 | 6,16 / 6,62 / 7,58 | −1 / −14 / −8% | −6 / +2 / 0% | 6,4-8,7 |
| 15 n, 5 km | 180 / 150 / 135 | 6,16 / 6,62 / 7,58 | +9 / +17 / +5% | +2 / +5 / −1% | 8,5-9,1 |
| 15 n, 10 km | 180 / 150 / 135 | 6,16 / 6,62 / 7,58 | +37 / +10 / −1% | +7 / +14 / +1% | 9,2-9,7 |
| 20 n, 5 km | 180 / 150 / 135 | 8,35 / 9,26 / 10,48 | −10 / −6 / +2% | −3 / −3 / 0% | 10,7-12,0 |

**Cosa dice:**
1. **Senza timonare, le onde vere (irregolari) danno poco: da −6 a +14%, di solito +2-7%.** Le punte di velocità invece sono grandi (+30-50%): la barca accelera sul fianco dell'onda e rallenta sul dorso.
2. Con onde regolari la barca a volte si «aggancia» all'onda (+20-37%), a volte no (fino a −14%): dipende dalla velocità della barca rispetto a quella dell'onda, come scrivono Harris e Maki (O3, O8).
3. Quando la barca va più veloce delle onde (20 nodi, 5 km: 8-10 nodi contro 7,5) le onde **frenano** un poco: la barca passa più tempo sul dorso, dove l'onda spinge indietro.
4. Quindi il guadagno vero delle regate (+20-30% in poppa, tabella sotto) **non viene dalle onde da sole ma dal timonare per restare sul fianco davanti dell'onda** (S, scelta dell'onda, una pompata per prenderla). Nel gioco, le onde nel motore renderebbero solo se il giocatore (o un aiuto) timona con l'onda.

## Misura sul banco: quanto manca in poppa alla barca M (rispetto ai dati di Binns e Bethwaite, presi con un po' di surf)

`bethwaite.js` con M (copia in `$TMPDIR/onde/beth_M.js`), velocità migliore a ogni angolo, scotta da 0 a 1:

| vento | bolina | traverso | lasco 135° | poppa 180° |
|---|---|---|---|---|
| 6 nodi | 3,7 (−8%) | 4,4 (−18%) | 3,6 (−28%) | 2,9 (−30%) |
| 9 nodi | 4,7 (−1%) | 5,7 (−9%) | 4,8 (−21%) | 4,1 (−25%) |
| 12 nodi | 5,1 (+2%) | 7,8 (+7%) | 6,0 (−26%) | 5,1 (−24%) |

Di bolina M è d'accordo con Binns; dal lasco alla poppa è **più lenta del 21-30%**. Da Day (O4) questa differenza viene in parte da surf e tecnica, in parte forse dal vento misurato. È il limite più alto di quello che le onde e le S possono aggiungere.

### O12 (F145). G. Bordogna, *The Aero-Hydrodynamic Characteristics of Yachts Sailing Upwind in Waves*, tesi magistrale, TU Delft, 2013 (copia già in `fonti-pdf/`)

- Barche a chiglia: la forza della vela smorza beccheggio e sussulto e **abbassa la resistenza aggiunta fino al 20%**. Nessun dato per derive.

## Stima grezza della bolina con le onde (conto a mano, non sul banco)

Con O1 (coefficiente Caw dell'ILCA 6 a 2-3 m/s fra 1 e 2), lo spettro irregolare (ζa² equivalente = Hs²/8) e il fattore 0,55 dell'ORC per la bolina a 45° (O10):

- 10 nodi, 5 km (Hs 0,19 m): Raw ≈ 1,5 × 1025 × 9,81 × 0,0045 × 1,105²/3,381 × 0,55 ≈ **13 N**, contro circa 45-60 N di resistenza a 2,4-2,6 m/s (O1 fig. 11a) → +25-30% di resistenza → **circa −8% di velocità** (la resistenza lì cresce circa con la velocità alla 3,3).
- 15 nodi, 5 km (Hs 0,32 m): **circa 38 N → circa −15-20%**.
- Con meno di 8 nodi: niente (onde sotto i 10-15 cm; e l'ORC stesso ha dovuto togliere le onde a quei venti, O10).

**Fiducia bassa:** Caw viene da onde di 4 cm, regolari e di prua; qui è allargato a onde 5-8 volte più alte, irregolari e a 45°. L'ordine di grandezza (qualche per cento con 10 nodi, 10-20% con 15) torna con la regola pratica «nel mare formato di bolina si va più piano e si poggia un po' per tenere velocità» (O2: le barche vanno «poco più piano della VPP, un po' più larghe»), ma non c'è una misura su una deriva che lo confermi.

## Cosa resta senza fonte

- **Nessuna misura diretta su una deriva in onda** (né di bolina né di poppa): solo CFD con onde piccolissime (O1), modelli (O3, O8) e il confronto con i dati di Binns presi «con un po' di surf» (O4).
- Le onde sui laghi italiani: nessuna misura trovata; solo le formule (O9).
- Keuning e altri 1993 (forza dell'onda su scafi di barche a vela da poppa, TU Delft): chiuso.
- Harris, Thomas e Renilson 2001 (la versione completa del 1999, con i risultati in onda): non trovato in rete libero.

## Cosa dice la ricerca per la voce 88 (da usare nella proposta)

1. **Il modello c'è ed è semplice:** forza dell'onda = peso della barca × pendenza dell'onda, ridotta per la lunghezza dello scafo (O8, O3). Si aggiunge alla spinta come una forza in avanti; da sola, col timone fermo, rende poco (+2-7% in poppa con onde vere, prova grezza).
2. **Le onde giuste si calcolano dal vento e dallo spazio d'acqua** (O9): sul campo del gioco (un lago o una baia) sono corte e lente come la barca in poppa, quindi il surf è possibile; sotto 8 nodi praticamente non ci sono (O10).
3. **Il guadagno grosso viene dalla tecnica** (O5, O7, prova grezza): timonare per restare sul fianco davanti dell'onda, S e strapoggio, una pompata per prenderla. Senza questo, le onde nel motore cambiano poco la velocità media e molto le punte.
4. **Di bolina le onde frenano:** stima grezza −8% con 10 nodi, −15-20% con 15 (fiducia bassa).
5. **Le S rendono anche senza onde** (O5: misure di Schutt su un lago, il +19% di VMG): quindi la voce 86 (strapoggio) non dipende tutta dalla 88; la 88 aggiunge il surf. La voce 86 di DA-FARE è stata corretta.
6. Da decidere nella proposta: onde regolari o irregolari (le regolari esagerano: la barca si aggancia), il disegno (dalla 1.0.23 c'è già un'onda disegnata, da far coincidere con quella del motore), come si accorge il giocatore dell'onda che arriva, e un aiuto disattivabile (principio 3).
