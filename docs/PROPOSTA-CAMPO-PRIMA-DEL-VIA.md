# Proposta: vedere il campo di regata e la boa prima del via

*Fermata 1, 22 novembre 2026 (Opus). Segnalazione di Lucio (21-22 nov): «occorre una visualizzazione o una mappa che mostri tutto il campo, almeno prima della partenza. La freccia che indica la boa appare solo dopo lo sparo: occorre sapere prima dove si trova la boa per preparare una tattica di partenza e di gara»; già il 21 nov: «con i lati lunghi la vista Q non mostra il campo alla partenza». Nessun codice finché non arriva il via.*

## Cosa c'è oggi

- **La freccia dell'obiettivo** (1.3.36): prima del via indica la linea («Linea»), dopo il via la boa («Boa 1», «Arrivo»). La boa prima del via non è indicata.
- **Il tasto Q** (vista): allontana la vista finché l'obiettivo entra nello schermo. Prima del via l'obiettivo è la linea, quindi la boa, a 400-600 m nelle regate lunghe, resta fuori.
- **Il campo intero** si vede solo a regata finita, aprendo la rotta ottimale (`rotVista`, js/rotta.js), che già sa inquadrare linea, boe e arrivo.
- In una regata vera la boa di bolina di solito si vede dalla linea, e il comitato espone la direzione della prima boa (da verificare nelle fonti prima di scriverlo nel gioco: è un'affermazione nautica, principio 4).

## Il modello più semplice (due pezzi, si può dare il via anche a uno solo)

**A. Il tasto Q prima del via mostra tutto il campo.** Finché R.t < 0, tenendo Q la vista si allontana fino a inquadrare linea, boe e barche, come la vista della rotta ottimale (stessa funzione di inquadratura). Dopo il via Q torna come oggi (verso l'obiettivo). È un aiuto: si usa solo se si preme Q.

**B. Prima del via, una seconda freccia piccola verso la boa 1**, con il nome e la distanza («Boa 1 · 520 m»), più chiara e senza pulsazione, per non confondersi con quella della linea. Sparisce allo sparo, quando la freccia principale passa alla boa. Si spegne con l'interruttore delle frecce (principio 3).

Cosa **non** propongo ora: una minimappa fissa in un angolo (occupa il mare a 1360x650 e si sovrappone a riquadri già fitti: bandiere, Coach, vento).

## Criteri (soglie nostre, dichiarate prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| M1 | Q prima del via inquadra tutto | in 20 regate lunghe e 20 corte, a −120 s con Q tenuto per 2 s: linea, tutte le boe e tutte le barche dentro lo schermo (a 1360x650, margine 20 px); 0 casi fuori |
| M2 | Q dopo il via come prima | a +30 s, zoom e spostamento uguali alla 1.3.38 con lo stesso seme (20 regate) |
| M3 | La freccia della boa dice il vero | a −120 s, direzione verso la boa 1 entro 2° e distanza entro 5 m da un calcolo del collaudo; 0 sbagliate su 40 regate; sparisce entro 0,1 s dallo sparo |
| M4 | Non copre niente | la freccia piccola non si sovrappone ai riquadri (bandiere, Coach, vento) come la freccia principale (criterio F della 1.3.36); 32 casi con controprova |
| M5 | La regata non cambia | 20 regate identiche al bit con A e B accesi e spenti |
| M6 | Come un giocatore | pagina senza `#collaudo`, regata lunga: Q prima del via mostra la boa, 0 errori |

Chromium e Firefox, uno per volta col freno.

## Rischi

- Con Q tenuto e il campo intero le barche diventano piccolissime: serve solo per guardare, non per guidare (la vista torna appena si lascia Q).
- Due frecce prima del via possono confondere: per questo la seconda è più piccola, senza pulsazione, e scompare allo sparo.

## Cosa serve da Ale

Via ad A, a B o a tutte e due.

## Riscrittura del 22 novembre, sera: «tutto il campo, come nella realtà»

Ale riporta che Lucio l'ha ribadito più volte: vuole vedere **tutto** il campo, perché in mare la boa e la linea si vedono. Quindi non solo la boa prima del via: il campo intero, quando lo si vuole. Tre modi, dal più semplice:

| | Come | Pro | Contro |
| --- | --- | --- | --- |
| **A2** | **Q tenuto mostra sempre tutto il campo** (linea, boe, arrivo, barche), prima e dopo il via. Oggi dopo il via Q mostra solo l'obiettivo | un tasto che c'è già, niente spazio in più sul mare | finché tieni Q le barche sono piccole; non si vede mentre si guida |
| **C** | **Minimappa fissa** in un angolo del mare: campo intero, boe, linea, tutte le barche, la tua evidenziata; si spegne dalle impostazioni (principio 3) | si vede sempre, come in mare; utile per la tattica | spazio: a 1360x650 il mare è 970x650 e gli angoli in alto sono occupati (bandiere, Coach, vento); va misurato dove sta senza coprire niente |
| B | la freccia piccola verso la boa prima del via (vedi sopra) | | con A2 o C diventa quasi inutile |

**Consiglio:** A2 subito (è piccolo e risponde a «prima della partenza»), poi C se Lucio la vuole sempre a schermo. Per C i criteri in più: nessuna sovrapposizione con i riquadri (32 casi con controprova, come la freccia), 0 px di eccesso a 1360x650, posizioni delle barche nella minimappa entro 2 px dal calcolo del collaudo, regata identica al bit accesa e spenta.

## Via di Ale (22 nov, sera): A2, niente minimappa

«La mappa piccola a lato no.» Si fa A2: **in regata, Q tenuto inquadra tutto il campo** (linea di partenza, boe, linea d'arrivo, tutte le barche), prima e dopo il via. Nelle prove e negli esercizi Q resta com'è (verso l'obiettivo). Al rilascio di Q tutto torna come prima.

**Costante nuova (ipotesi nostra):** con Q in regata la vista può allontanarsi fino a `ZQ_MIN = 0,02` (oggi il limite è `ZMIN = 0,1`: a 0,1 un campo di 560 m non sta nei 650 px). Margine come oggi, `VIEW_M` 50 px.

**Criteri della A2 (soglie nostre, scritte prima del codice):**

| # | Criterio | Soglia |
| --- | --- | --- |
| Q1 | Tutto dentro | 20 regate lunghe e 20 corte, Q tenuto 2 s a −120 s, +30 s e a metà regata: linea, boe e tutte le barche dentro lo schermo con almeno 20 px di margine, vista a prua e vista a nord; 0 casi fuori su almeno 240 controlli |
| Q2 | Torna com'era | 1 s dopo il rilascio di Q, zoom e spostamento a meno dell'1% da quelli di prima |
| Q3 | Prove come prima | nelle prove e negli esercizi Q dà la stessa vista della 1.3.40 (20 casi, a meno dell'1%) |
| Q4 | La regata non cambia | 20 regate identiche al bit con Q tenuto a lungo e senza Q |
| Q5 | Come un giocatore | pagina senza `#collaudo`, regata lunga, Q tenuto prima del via: boa e linea dentro lo schermo, 0 errori |

Chromium e Firefox, uno per volta col freno. Da sapere: i suoni calano con lo zoom (1.3.33), quindi tenendo Q si sentono più piano.

## Esito

*(da scrivere dopo il codice)*
