# Studio della barca del gioco

*22 novembre 2026 (Opus). Richiesta di Ale: «fai uno studio completo sulla nostra barca: può servire per rendere il gioco più realistico e per una sezione "scientifica" del manuale». Nasce dalla voce 73 (Lucio: «la barca si pianta di più in virata»). È una **misura**: non cambia il gioco. Le correzioni, se servono, si propongono a parte.*

## Che barca è

Una deriva singola di 4,2 m con una sola vela da 7,0 m², 135 kg con il timoniere (75 kg): le misure di un Laser/ILCA 7, senza il nome (principio 5). Il motore è `js/motore.js`, la barca è quella dell'1b (`S.lv = 2`), congelata dalla 1.1.0 (`tests/fisica/impronta1b.js`). Costanti e fonti: `FISICA-E-TARATURE.md`.

## Il metodo

Un solo script, `tests/fisica/studio_barca.js`, in Node: usa lo stesso motore del gioco, senza pagina né browser, senza numeri a caso (vento costante, niente raffiche). Due timonieri:

- **timoniere pulito**: barra proporzionale all'errore di prua (al massimo 35°, 1,6 della corsa al secondo come la tastiera), scotta dalla regola del gioco (boma = vento apparente − 17°): `costo_manovre.js`;
- **gesto da tastiera**: barra a fondo con la sola freccia (35°) fino a 30° oltre il vento, poi il timoniere pulito sulla nuova bolina: `virata1b.js`.

Le regate col pilota (raffiche, salti, altre barche) si leggono dalla misura della voce 73 (`tests/misura_virate_giocatore.py`).

## Cosa si misura

| Parte | Cosa | Venti (nodi) |
| --- | --- | --- |
| A | **Polare**: velocità di equilibrio con la scotta migliore da 30° a 180° dal vento; sbandamento, scarroccio, timoniere fuori bordo; VMG migliore di bolina e di poppa e a che angolo | 4-20 ogni 2 |
| B | **Virata**: durata, velocità minima (% di quella di prima), secondi per tornare al 90%, **metri persi** verso il vento (contro la stessa barca che resta di bolina 60 s) e in lunghezze di barca, sbandamento massimo | 4-20 |
| C | **Abbattuta** (da 150° a 150°): le stesse misure, metri persi sottovento, sbandamento massimo, scuffie | 4-20 |
| D | **Partenza da ferma** (prua a 60° dal vento): secondi per arrivare al 50% e al 90% della velocità di regime, metri fatti in 10 s | 6, 10, 14 |
| E | **Frenare e stare fermi**: dal traverso a regime, scotta tutta lasca: secondi per scendere sotto 1 nodo, metri percorsi; velocità dopo 30 s | 6, 10, 14 |
| F | **Sbandamento**: da che vento il timoniere è tutto fuori di bolina; raffica improvvisa (senza reagire) che fa scuffiare | 6-20 |
| G | **Manovrabilità**: diametro del giro e secondi per un giro (360°) e per il giro di penalità (720°) con la barra a 35° e a 45° | 6, 10, 14 |
| H | **Prua al vento**: dopo quanto la barca ferma arretra, e a che velocità | 6, 10, 14 |

## Con che cosa si confronta

| Fonte | Che cosa dà | Quanto vale |
| --- | --- | --- |
| F17 (Day 2017, fig. 8) | VMG di bolina e di poppa previste per il Laser, 6-15 nodi | articolo scientifico (previsione dalla vasca F16) |
| F10 (Binns, in F17 fig. 4-5) | velocità misurate di un Laser con 9 e 12 nodi | misura |
| F23 (Pennanen 2016) | di bolina la velocità cresce fino a circa 11 nodi, poi quasi non aumenta | articolo scientifico (modello) |
| F24 (setcourses) | minuti per miglio del Laser, bolina con le virate, lasco e poppa, per fasce di vento | tabella senza metodo: bassa |
| **F106** (Dellenbaugh, *Speed & Smarts* n. 155, «Tacking») | lunghezze perse in una virata da una deriva leggera: vento leggero 0 (acqua piatta) / 1 (onde), medio 0,5 / 1, forte 1 / 1,5; «in media forse una lunghezza» | **stima di un allenatore**, dichiarata «a occhio»: solo confronto, non taratura |
| ricerca ILCA 7 (`fonti-pdf/ricerca_virata_ILCA7.docx`, 21 ott) | nessuna misura pubblica della virata (durata, velocità minima); come intervalli di prova: durata 3-7 s, perdita 10-50% | intervalli di prova, non misure |

## Criteri (soglie nostre, scritte prima di far girare lo script)

Onestà sui numeri già visti: le VMG contro F17 sono note dalla 1.0.11 (−15% con 6 nodi, −9% con 10, +7% con 15) e `costo_manovre.js` dà già 1,9-2,0 s persi per virata con 10-14 nodi e VMG di poppa di 3,7-4,7 nodi; F24 dà per la poppa del Laser circa 5 nodi (8-12) e 6 (12-15). Le soglie su quelle cose sono quindi controlli, non scoperte.

| # | Criterio | Soglia |
| --- | --- | --- |
| S1 | Virata, timoniere pulito, 10-14 nodi | metri persi ≤ 1 lunghezza (4,2 m), la «media» di F106 |
| S2 | Virata, vento medio (10-14 nodi) e acqua piatta | si riporta il confronto con 0,5 lunghezze (2,1 m) di F106; se oltre il doppio (4,2 m), si dice |
| S3 | Virata col gesto da tastiera | si riporta; se perde più di 2 lunghezze (8,4 m) con 10-14 nodi, è il gesto che pianta la barca, non il motore |
| S4 | Bolina | VMG entro ±15% da F17 con 6, 10 e 15 nodi (controllo: già nota) |
| S5 | Poppa | VMG del gioco contro F24 (poppa) e F17: se più lenta di oltre il 20% di tutte e due, è un difetto da proporre |
| S6 | Ha misurato davvero | ogni parte stampa quanti casi; nessuna parte con zero casi; nessuna manovra fallita senza dirlo |

Il resto (partenza, frenata, sbandamento, giri, prua al vento) **si riporta e basta**: non c'è una fonte con numeri. Va nel manuale come «cosa fa la barca del gioco», con scritto che non è confrontato.

## Esito (22 nov, motore della 1.3.40, `node tests/fisica/studio_barca.js`, circa 25 s in tutto)

Tutti i numeri sono della barca del gioco con vento costante e acqua piatta (il gioco non ha onde). «L» = una lunghezza di barca, 4,2 m.

### Criteri

| # | Esito |
| --- | --- |
| S1 | **Passa.** Virata col timoniere pulito: persi 3,0 / 3,3 / 3,8 m con 10 / 12 / 14 nodi (0,71 / 0,79 / 0,89 L), soglia 4,2 m |
| S2 | Contro le 0,5 L di F106 (vento medio, acqua piatta): 1,4 / 1,6 / 1,8 volte. Sotto il doppio |
| S3 | Gesto da tastiera: 2,9 / 3,3 / 3,7 m, **uguale** al timoniere pulito (differenza sotto 0,1 m). Non è il gesto che pianta la barca |
| S4 | **Non passa con 6 nodi.** VMG di bolina contro F17 fig. 8 (letta dal grafico: 2,66 / 3,62 / circa 3,80 nodi con 6 / 10 / 15): gioco 2,13 / 3,08 / circa 3,81 → **−20%** / −15% / 0%. Più del −15% già noto con 6 nodi perché qui la VMG è sulla rotta vera, con lo scarroccio dell'1b (3°) |
| S5 | **Passa.** VMG di poppa contro F17: −11% con 6 nodi, −8…−10% da 8 a 16. Contro F24 (tabella debole): −4…−31% con 8-12 nodi, −6…−20% con 12-15 |
| S6 | Casi: polare 279 punti, virate e abbattute 18 + 27 corse, il resto 26. Nessuna parte vuota. Virata **non riuscita** con 18 e 20 nodi (sotto) |

### A. Polare (nodi di velocità della barca, scotta migliore)

| vento | 35° | 40° | 45° | 50° | 60° | 90° | 110° | 135° | 150° | 180° | bolina: VMG a ° | poppa: VMG a ° |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 1,1 | 1,6 | 2,2 | 2,4 | 2,7 | 3,1 | 2,9 | 2,3 | 1,9 | 1,7 | 1,48 a 50° | 1,78 a 170° |
| 6 | 1,7 | 2,4 | 3,2 | 3,4 | 3,9 | 4,2 | 4,0 | 3,4 | 2,8 | 2,6 | 2,13 a 45° | 2,65 a 170° |
| 8 | 2,2 | 3,2 | 4,0 | 4,3 | 4,7 | 5,1 | 4,9 | 4,3 | 3,7 | 3,4 | 2,66 a 45° | 3,45 a 170° |
| 10 | 2,7 | 3,9 | 4,6 | 4,9 | 5,4 | 6,0 | 5,7 | 4,9 | 4,4 | 4,1 | 3,08 a 45° | 4,17 a 170° |
| 12 | 3,2 | 4,5 | 5,1 | 5,5 | 6,3 | 7,2 | 6,7 | 5,6 | 5,0 | 4,7 | 3,42 a 45° | 4,79 a 170° |
| 14 | 3,6 | 5,0 | 5,5 | 6,0 | 6,9 | 8,9 | 8,2 | 6,4 | 5,7 | 5,1 | 3,70 a 45° | 5,39 a 170° |
| 16 | 4,1 | 5,4 | 5,8 | 6,3 | 7,3 | 10,1 | 9,6 | 7,5 | 6,4 | 5,6 | 3,92 a 45° | 6,05 a 165° |
| 20 | 4,8 | 5,6 | 6,1 | 6,6 | 7,9 | 11,0 | 12,0 | 9,8 | 8,3 | 6,0 | 4,13 a 45° | 7,77 a 165° |

- Di bolina, alla VMG migliore: vento apparente 29-34°, sbandamento 5-8°, scarroccio 2,5-3,3°, timoniere fuori il 25% con 6 nodi, il 70% con 10, tutto fuori da 14-16.
- Angolo della VMG migliore: 45° da 6 a 20 nodi (F17 fig. 9: 40,5-44°). La barca del gioco stringe un po' meno.
- Bolina sopra i 12 nodi: il gioco continua a crescere (3,42 → 4,13 nodi da 12 a 20), Day resta quasi fermo (3,73 → 3,81 da 12 a 16). Difetto di forma già noto (`archivio/PROPOSTA-BOLINA.md` §6), qui confermato.
- Velocità massima al traverso o al lasco: 6,0 nodi con 10, 10,1 con 16, 12,3 con 20. Il gioco non ha la planata (lo scafo della vasca F16 è misurato fino a 9 nodi): sopra quella velocità è un'estrapolazione.

### B. Virata (da bolina a bolina, vento costante)

| vento | durata | minima | ritorno al 90% | persi | in L | in s |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 7,2 s | 55% | 18,5 s | 2,9 m | 0,69 | 3,9 |
| 6 | 5,0 s | 54% | 12,8 s | 3,0 m | 0,70 | 2,7 |
| 8 | 4,1 s | 52% | 10,0 s | 2,9 m | 0,69 | 2,1 |
| 10 | 3,6 s | 49% | 8,6 s | 3,0 m | 0,71 | 1,9 |
| 12 | 3,4 s | 45% | 8,0 s | 3,3 m | 0,79 | 1,9 |
| 14 | 3,3 s | 42% | 8,1 s | 3,8 m | 0,89 | 2,0 |
| 16 | 4,0 s | 32% | 8,3 s | 5,0 m | 1,18 | 2,8 |
| 18 | non riesce con la sola freccia: la barca resta quasi ferma | | | | | |
| 20 | con la scotta della regola del gioco la barca non va di bolina (scuffia o si ferma) | | | | | |

(«ritorno al 90%» è contato dall'inizio della manovra; la durata va fino alla prua a 5° dalla nuova bolina.)

- **Il pilota delle regate vira come il timoniere pulito.** Voce 73: minima 47%, ritorno al 90% in 5,8 s contati dal passaggio col vento in prua; qui con 12 nodi 45% e 8,0 s contati dall'inizio, cioè circa 6,5 s dal passaggio. Quello che Lucio sente («si pianta») è la barca, non il modo di guidarla.
- **Contro F106:** con 10-14 nodi il gioco perde 0,7-0,9 L, nella «media di una lunghezza» ma 1,4-1,8 volte le 0,5 L del vento medio in acqua piatta. **Con poco vento (4-8 nodi) la differenza è più grande:** il gioco perde 0,7 L, F106 dice 0 in acqua piatta con una buona virata rollata. Il gioco non ha la virata rollata (il timoniere che fa sbandare la barca per farla girare e poi la raddrizza di colpo, che dà una spinta in più). È qui che la barca del gioco «si pianta» più di una vera.
- Durata 3,3-5 s con 6-16 nodi: dentro l'intervallo di prova della ricerca ILCA 7 (3-7 s, non misurato). La velocità minima scende al 42-55%, nell'intervallo di prova 10-50% di perdita solo con poco vento (sopra i 10 nodi la perdita è 51-58%, un po' oltre).
- **Vento forte:** con 18 nodi la virata riesce solo con Maiusc (barra a 45°): con la sola freccia la prua si ferma a 35° e la barca a 1,2 nodi; lascando la scotta durante la virata va **peggio** (la barca si ferma prima del vento). Con 20 nodi la regola di scotta del gioco (boma = apparente − 17°) non sventa abbastanza e di bolina la barca scuffia o si ferma; con la scotta migliore invece va (polare: 6,1 nodi a 45°, sbandamento 5°).

### C. Abbattuta (da 150° a 150°)

| vento | pulita (motore puro) | controllata (boma a 40°) | violenta (boma oltre 45°, regola di `gioco.js`) |
| --- | --- | --- | --- |
| 6 | 0 m, sbanda 1° | 0 m, sbanda 3° | persi 2,1 m (0,5 L), sbanda 20° |
| 10 | 0 m, sbanda 1° | 0 m, sbanda 5° | persi 2,9 m (0,7 L), sbanda 49° |
| 12 | 0 m, sbanda 1° | 0 m, sbanda 6° | **scuffia** (sbanda 70°) |
| 14-20 | 0 m, sbanda 2-3° | 0 m, sbanda 8-13° | **scuffia** |

- Nel motore l'abbattuta non costa niente: dura 1,2-4,5 s e la velocità non scende sotto il 92%. Tutto il costo e il pericolo sono nella regola del gioco: con il boma oltre 45° al passaggio la velocità si dimezza (× 0,55) e arriva un colpo di sbandamento; con il colpo medio la barca scuffia **da 12 nodi** (il commento in `gioco.js` dice 15).
- Nessuna fonte con numeri sull'abbattuta di una deriva: non confrontato.

### D-H. Le altre misure (solo riportate: nessuna fonte con numeri)

| Misura | 6 nodi | 10 nodi | 14 nodi |
| --- | --- | --- | --- |
| **D.** Partenza da ferma a 60° dal vento: 50% / 90% della velocità | 4,2 / 10,4 s | 2,2 / 5,4 s | 1,6 / 6,6 s |
| metri in 10 s | 10 m (2,4 L) | 20 m (4,7 L) | 26 m (6,3 L) |
| **E.** Frenare a 60°, scotta tutta lasca: sotto 1 nodo | 16,7 s, 15 m | 17,2 s, 18 m | 16,1 s, 18 m |
| al traverso (90°): velocità dopo 30 s | 1,3 nodi | 2,1 nodi | 2,9 nodi |
| **G.** Giro di penalità (720°), sola freccia / Maiusc | 29 / 22 s | 20 / 15 s | 17 / 12 s |
| diametro del giro, sola freccia / Maiusc | 6,8 / 5,2 m | 6,8 / 5,3 m | 7,0 / 5,6 m |
| **H.** Prua al vento da ferma: arretra dopo / a 20 s | 1,7 s / −0,8 nodi | 0,5 s / −2,0 nodi | 0,3 s / −2,8 nodi |

**F. Sbandamento e raffiche** (bolina a 45°, scotta della regola): timoniere fuori il 20% con 6 nodi, 58% con 10, 82% con 12, tutto fuori da 14. Raffica improvvisa che fa scuffiare senza reagire (scotta e prua ferme, 8 s): **19-20 nodi qualunque sia il vento di prima** (da 6 a 18 nodi). Con 20 nodi la barca scuffia già a regime con la regola di scotta.

- Al traverso con la scotta tutta lasca la barca rallenta piano (2 nodi dopo 30 s con 10 nodi): a quell'angolo il boma a 85° prende ancora un po' di vento. Stare fermi si fa a 60° o più stretti (sotto 1 nodo in circa 17 s).
- La barca ferma con la prua al vento arretra subito e forte (2 nodi con 10 nodi di vento dopo 20 s). Scelta della 1.0.8 (`archivio/PROPOSTA-RETROMARCIA.md`, nessun tetto); nessuna fonte con un numero.

### Cosa se ne ricava (per Lucio, per il manuale e per le proposte)

1. **Le virate non sono sbagliate ma sono «da principiante bravo», non da campione**: 0,7-0,9 L con 10-14 nodi. Manca la virata rollata, che con poco vento rende la virata quasi gratis. Proposta possibile (solo col via): un gesto di rollata (per esempio un tasto per sbandare e raddrizzare) che con 4-10 nodi accorcia la perdita verso le 0-0,5 L di F106.
2. **Bolina lenta con poco vento** (−20% con 6 nodi contro Day, sulla rotta vera): difetto già noto, causa non trovata (`archivio/PROPOSTA-BOLINA.md` §6). Nelle regate a 10-12 nodi pesa −8…−15%.
3. **Vento forte (oltre 16 nodi):** la regola di scotta che il gioco insegna non basta più, e con la sola freccia la virata non riesce a 18 nodi. Oggi le regate sono a 10-12 nodi; se si vorranno regate con più vento, serve prima una proposta (sventare, barra).
4. **Abbattuta:** nel motore gratuita, nel gioco tutta nella regola della «strambata violenta» (scuffia da 12 nodi con il boma aperto). Da dire nel manuale così com'è.
5. **Per il manuale:** le tabelle A-H sono «la carta d'identità» della barca del gioco. Vanno con la frase: «misurate sul motore del gioco, in acqua piatta e vento costante; confrontate con le fonti dove ci sono (F17, F24, F106), altrimenti solo riportate».
