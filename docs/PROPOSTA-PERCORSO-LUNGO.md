# Proposta: regate più lunghe e raffiche che si sentono (voce 63)

*Fermata 1, 20 novembre 2026. Richiesta di Ale del 18 novembre, ripresa il 20 («ci sarà da allungare le regate»). Nessun codice nel gioco finché non arriva il via. Va letta insieme a `PROPOSTA-COACH-IN-REGATA.md` (voce 65): il Coach che parla durante la regata ha senso solo se la regata è lunga.*

## Da dove viene

Ale, 18 novembre: lati da 140 m, 3 minuti, una virata sola, poppa dritta, raffiche che non si sentono. Direzione proposta da lui: lati da 400-500 m (giro di 6-8 minuti), raffiche come zone sull'acqua.

## Cosa dicono le vostre registrazioni (misurato il 20 novembre, prima di proporre)

Le 31 regate intere con arrivo in `registrazioni/` (dal 7 al 16 novembre, Ale e Lucio), lette con uno script fuori dal gioco:

| Cosa | Misura |
| --- | --- |
| Tempo all'arrivo | mediana **192 s** (da 164 a 380) |
| Virate dopo il via | mediana **2** (da 1 a 6) |
| Regate con le raffiche | 22 su 31 |
| Tempo passato in raffica (vento almeno 2 nodi sopra la base) | mediana **8%** della regata (da 2% a 25%) |
| Raffiche incontrate | mediana 5 per regata (da 2 a 10), quasi tutte brevi |
| Velocità di bolina (vento a 35-55°) | **4,70 nodi** fuori dalla raffica, **4,90** dentro: **+0,30 nodi** (mediana su 20 regate) |

Cosa vuol dire: la barca **in raffica accelera davvero poco, e per poco**. Le raffiche del gioco sono macchie di 20-40 m (raggio da 9 a 20 m, `spawnGust` in `js/gioco.js`) che scorrono col vento all'80% della sua velocità e durano 40-60 s. La barca le attraversa in pochi secondi, quasi sempre prima di aver preso velocità. La fisica della barca non c'entra: la polare dà +1 nodo di bolina passando da 10 a 15 nodi di vento (4,6 → 5,7), ma ci vogliono diversi secondi dentro la raffica per arrivarci.

## Il modello più semplice

**A. Lati più lunghi, solo in Deriva.** `MARK_UP` (bastone) e `TRI_L` (triangolo) da 140 m a **300 m** nelle regate di Deriva, nel torneo e nella stagione. La Scuola resta com'è: lì le regate servono alle lezioni, e lunghe sarebbero noiose. Stima dai vostri tempi (circa 1,3 s per metro di lato, partenza e giri di boa compresi): 300 m → circa **6,5 minuti** di regata; 400 m → circa 8,5; 450 m → circa 10. Quindi i 400-500 m di Ale danno **8-11 minuti**, non 6-8: per i 6-8 minuti chiesti bastano **300-350 m**. Lo propongo come primo passo; si allunga dopo, se Ale lo vuole.

**B. Raffiche come zone sull'acqua, solo nelle regate lunghe.** Stesse forze di oggi (+20-40% del vento al livello 1, nessun numero di fisica nuovo), ma:
- **più grandi:** raggio 40-80 m invece di 9-20, cioè zone di 100-200 m;
- **più lunghe:** 2-4 minuti invece di 40-60 s;
- **in tutto il campo**, non solo vicino al giocatore (oggi nel torneo nascono sopravento a una barca a caso);
- **visibili da lontano**, scure come oggi.

Così una raffica si attraversa in 20-60 s invece che in 5-10, la barca fa in tempo ad accelerare, e scegliere da che parte andare per prenderla diventa una scelta di regata (è anche quello che insegnano le fonti sulle raffiche, `FONTI-PUBBLICHE.md`, da ricontrollare nella fermata 2).

**C. Tutto il resto si adatta, senza cambiare le regole:** telecamera e freccia della boa (la boa a 300 m può uscire dallo schermo), finestra d'arrivo del torneo (`TOR_FIN`, già in proporzione al tempo della prima), frasi del Coach (finestre di 60 s del momento clou: forse da allungare in proporzione), tempi dei collaudi (46 script contengono 900 s come limite: da rivedere uno per uno).

## Costanti nuove (tutte ipotesi nostre, da misurare)

`LATO_DERIVA = 300` m; `RAFF_R = [40, 80]` m; `RAFF_VITA = [120, 240]` s; `RAFF_CAMPO` (le raffiche nascono in tutto il campo, a distanza dalla linea di bolina). Nessuna costante della barca cambia.

## Criteri (soglie nostre, dichiarate prima; semi di scelta e di conferma separati, pilota sul giocatore e rivali «medio»)

| # | Criterio | Soglia |
| --- | --- | --- |
| L1 | Durata | tempo all'arrivo del giocatore (pilota): mediana fra 6 e 8 minuti, su 20 semi |
| L2 | Si vira di più | virate dopo il via del pilota: mediana almeno 4 |
| L3 | Le raffiche si sentono | tempo in raffica di bolina fra il 20% e il 40%; durata mediana di una raffica sulla barca almeno 20 s (oggi da misurare: atteso sotto 10); velocità di bolina in raffica almeno +0,6 nodi rispetto a fuori (oggi +0,30) |
| L4 | I rivali reggono | contatti per regata, barche ferme e «oltre la layline» non peggiori di oggi oltre il 20%; posti dei rivali per carattere nello stesso ordine di oggi |
| L5 | La rotta ottimale | si calcola entro 3 s nel gioco (oggi sotto 1 s) |
| L6 | Schermo | la boa sempre visibile o indicata dalla freccia; pannello a 1360x650 con 0 px di eccesso |
| L7 | File | la registrazione di una regata lunga sotto 1 MB |
| N | Non-regressione | Scuola identica: `polare.js`, `raffiche_e_virate.js`, `impronta1b.js`, regate della Scuola bit per bit |

## Rischi e costi (detti chiari)

- **Ritaratura dei rivali:** la guida dei rivali è tarata su lati da 140 m (layline, virate, momento in cui puntano la boa). È la parte più cara e più incerta.
- **Tempo di una tappa:** 4 regate da 7 minuti = circa 30 minuti a tappa, 2 ore a stagione. Forse il torneo passa a 3 regate.
- **Record e medaglie di Deriva** non sono più confrontabili: si azzerano (si può fare senza chiedere).
- **Collaudi:** molti hanno limiti di tempo pensati per 3 minuti; il giro su GitHub si allunga.
- **Il PC di Ale:** le misure lunghe costano il triplo (oggi circa 1,5 minuti a regata con la rotta ottimale).

## Domande per Ale (una per volta, nella fermata 2)

1. **Solo Deriva** (torneo, stagione, regate di Deriva) o anche le regate della Scuola? Consiglio: solo Deriva.
2. **Quanto lungo:** 300 m (circa 6-7 minuti) per cominciare, o subito 400-500 m (circa 9-11)?
3. **Il torneo resta di 4 regate** o passa a 3?

## Passi, dopo il via

1. Misurare lo stato di oggi coi criteri L1-L3 (durata di una raffica sulla barca: non si legge nei file, va misurata col pilota).
2. Lati lunghi dietro una costante, provati con `__sv`; poi raffiche-zona; misure una alla volta col freno.
3. Rivali: prima si misura quanto peggiorano (L4), poi si decide se ritarare.
4. Versione nuova, `CHANGELOG.md`, documenti.

## Risposte di Ale (20 novembre 2026, sera)

1. **Solo Deriva.**
2. **Regate di circa 9-11 minuti:** quindi lati di circa **400-450 m**, non 300 (stima: 400 m → circa 8,5 minuti, 450 m → circa 10). La soglia L1 diventa «mediana fra 9 e 11 minuti».
3. **Tre regate per tappa e per torneo** (oggi quattro): circa 30 minuti a tappa.

Via al codice: non ancora dato esplicitamente.

## Esito (20 novembre 2026, notte; versione 1.3.26)

Via di Ale («ora VIA col lavoro autonomo»). Fatto: lati 560/460 m, tre regate per torneo (niente scarto con tre: scelta mia), raffiche-zona; tornei già cominciati restano corti; con `#collaudo` le regate restano corte finché i collaudi non sono adattati. Numeri in `CHANGELOG.md` 1.3.26.

| # | Esito |
| --- | --- |
| L1 | **passa:** 10,3 e 10,0 min (semi 101-110), 10,5 e 10,7 (301-310) |
| L2 | **passa:** virate 8-11 (oggi 4) |
| L3 | **in parte:** in raffica 28-30% (passa); durata sulla barca 17-26 s, a cavallo dei 20 (non sempre); velocità +0,2/+0,6 nodi, sotto +0,6 (non passa) |
| L4 | **passa** per penalità e barche ferme; layline non misurata |
| L5 | **non passa:** rotta ottimale 3,3-4,1 s, in assoluto 13,5-14,9 s su questo PC, a pagina ferma |
| L6 | **passa** (freccia con la distanza) |
| L7 | **non passa** (stima 2-2,5 MB) |
| N | **passa** (fisica identica; collaudi di torneo, stagione, sponsor, finale, Deriva superata verdi) |

Prossimi passi: rotta ottimale calcolata a pezzi o con passo più lungo (L5); registrazione più leggera (L7); collaudi portati alle regate lunghe; poi il Coach in regata (65).
