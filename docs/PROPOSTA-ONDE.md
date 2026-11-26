# Proposta: le onde nel motore (voce 88, fermata 1)

Scritta il 26 novembre 2026, **prima del via**: niente codice in `js/`. Ricerca, fonti e prova grezza: `sperimentale/onde-88/RICERCA-ONDE.md` (fonti F138-F145).

## Il punto di partenza

- **Oggi le onde sono solo disegnate** (dalla 1.0.23, `js/disegno.js`, `waveTilt`): la barca beccheggia e rolla, ma il motore non le vede.
- **La barca M** (voce 84, se Ale la accende) **va come le misure in bolina e al traverso**. Dal lasco alla poppa invece è più lenta del 21-30% rispetto ai dati di Binns e Bethwaite, che sono presi «con un po' di surf» (Day, F17).
- **La prova grezza** (`surf_grezzo.js`) è stata fatta con M, prua ferma e onde irregolari. In poppa la velocità media guadagna di solito il 2-7%, mentre le punte salgono del 30-50%. Il resto del guadagno viene dal timonare sull'onda: le S e lo strapoggio, cioè le voci 86 e 87.

**Ordine:** questa voce si costruisce sopra M. Se M non viene accesa, si rifà la prova sul banco con la barca di oggi prima di andare avanti.

## Il modello (il più semplice con una fonte)

1. **Le onde.** Altezza e periodo vengono dal vento e dallo spazio d'acqua libero (formule del Shore Protection Manual 1984, F142).
   - Sono onde irregolari: 5 componenti con fasi fisse, prese dal seme della corsa. Così regate, registrazioni e moviola restano uguali a ogni ripetizione.
   - Le onde vanno nella direzione del vento medio, non di quello che gira: le onde vere ci mettono minuti a girare.
   - Non c'è onda lunga del mare aperto (niente onde lunghe venute da lontano).
2. **La spinta dell'onda sulla barca** (Harris, Thomas, Renilson 1999, F141). È la forza di Froude-Krylov: il peso della barca per la pendenza dell'onda sotto lo scafo, ridotta per la lunghezza dello scafo (fattore sinc(kL/2)). Si somma alla spinta della vela lungo la prua, moltiplicata per il coseno dell'angolo fra la prua e la direzione delle onde. In bolina, nella media, questa forza vale circa zero.
3. **La resistenza in più di bolina** (F138 per lo scafo dell'ILCA, F143 per il fattore 0,55 dell'ORC a 45° dalle onde). Il coefficiente Caw viene dall'ILCA 6 con onde di 4 cm. Cresce col quadrato dell'altezza dell'onda. Vale con le onde da prua fino al traverso; con le onde da poppa è zero.
4. **Cosa resta fuori:**
   - lo sbandamento e l'imbardata dovuti all'onda (l'orza in poppa, la straorzata);
   - il beccheggio come grado di libertà;
   - le onde riflesse dalla costa.

   Il disegno di beccheggio e rollio resta com'è oggi, ma prende periodo e lunghezza dalle stesse onde del motore, così quello che si vede e quello che si sente coincidono. Già oggi il disegno usa 1,5-2,5 s, e il modello dà circa 1,9 s con 10 nodi e 5 km.
5. **Come se ne accorge il giocatore.**
   - L'onda è già disegnata.
   - In più c'è un **aiuto disattivabile** (principio 3): un segno quando la poppa si alza e conviene poggiare per prendere l'onda. Le onde invece sono fisica e non si spengono, come il vento che gira.

## Costanti nuove

| Costante | Valore | Fonte o ipotesi |
|---|---|---|
| Formule di altezza e periodo | SPM 1984 | F142 |
| Spazio d'acqua libero | **5 km** (lago grande o baia) | **ipotesi**: il gioco non dice dove si naviga. In futuro si potrebbe dare un valore diverso a ogni circuito |
| Spettro in 5 componenti | periodi fra 0,7 e 1,5 volte quello di picco, fasi dal seme | **ipotesi** (lo spettro intero non serve per un ordine di grandezza) |
| Lunghezza al galleggiamento | 3,381 m | F138 tab. 1 |
| Volume immerso | massa / densità dell'acqua | fisica |
| Coefficiente di resistenza in più Caw | 1,5 | F138, allargato da onde di 4 cm a onde di 20-30 cm: **ipotesi, fiducia bassa** |
| Fattore per la bolina a 45° | 0,55 | F143 (ORC) |
| Come cala la resistenza in più fra le onde da prua e il traverso | col coseno | **ipotesi** |

## Criteri (attese nostre, scritte prima)

Tutti sul banco, con M più le onde e 10 semi fissi; la conferma va fatta su altri 10 semi mai guardati.

| | Criterio | Soglia | Da dove |
|---|---|---|---|
| O1 | Sotto gli 8 nodi le onde non contano | velocità media cambiata meno dell'1% a ogni angolo | ORC (F143), F142 (onde sotto i 10 cm) |
| O2 | In poppa e al lasco, con 10-15 nodi e prua ferma, le onde aiutano | guadagno medio fra 0 e +12% | Day (F17): Binns surfa; Harris (F141) |
| O3 | Le onde da sole non bastano a pareggiare le misure | velocità con prua ferma **sotto** Binns e Bethwaite a 135-180° | se le superasse, la forza sarebbe troppo grande: il resto deve venire dalla tecnica |
| O4 | Le punte di velocità in poppa si vedono | punta almeno +20% sopra la velocità in acqua piatta, con 12-15 nodi | F141, F140 (la barca accelera sul fianco dell'onda) |
| O5 | Timonare sull'onda rende | un pilota che poggia quando la poppa si alza guadagna più della prua ferma | Day, F144 (qualitativa) |
| O6 | Di bolina le onde frenano | perdita di velocità 3-15% con 10 nodi, 8-25% con 15 | stima di `RICERCA-ONDE.md` (fiducia bassa: soglie larghe) |
| O7 | Di bolina non sotto le regate | VMG di bolina con 15 nodi non sotto 3,7 nodi | F134 (media di regata con più di 12 nodi: è un limite basso) |
| O8 | Ripetibile | stesso seme → stessa traccia, al bit; moviola e registrazioni uguali | regola del gioco |
| O9 | Spenta la forza delle onde, il motore è M al bit | impronta uguale | non-regressione |

**Un rischio già visibile su O6-O7.** M in acqua piatta fa 3,70 nodi di VMG con 15 nodi, cioè proprio la media delle regate. Se le onde le tolgono il 15%, scende a circa 3,15, sotto il limite basso.

Ci sono tre spiegazioni possibili:
- la stima della resistenza in più è troppo alta;
- M di bolina col vento forte è un po' lenta (−2,8% su Day);
- quelle regate (Coppa del mondo e Tokyo 2020, in mare) avevano onde lunghe che frenano meno di quelle corte di un lago.

Se O6 e O7 non passano insieme, si riporta e decide Ale. Il Caw non si ritocca per farli passare.

## Cosa si misura anche sul gioco (dopo il via, senza soglie nuove)

- Lezioni con almeno 8 nodi: quante si completano, come per la voce 84.
- Fasce dei tempi del pilota e medaglie.
- Avversari: hanno le stesse onde. Si guarda se il giocatore che timona sull'onda li batte di più; i piloti degli avversari che surfano sono un lavoro a parte.
- Registrazioni vecchie: se la moviola ricalcola la corsa, quelle fatte prima delle onde cambierebbero. Si controlla, e se serve si segna la versione nel file.

## Lavoro, in due passi

1. **Sul banco, in `sperimentale/onde-88/`.** Si usa una copia del motore M con le onde, senza toccare `js/`, e si misurano O1-O9. Poi ci si ferma e si riporta.
2. **Nel gioco, solo con un altro via.** Il motore, il disegno con le stesse onde, l'aiuto disattivabile, i collaudi e una versione nuova.

## Cosa serve da Ale

1. Il via al passo 1 (solo banco).
2. Lo spazio d'acqua libero: 5 km per tutti (lago grande o baia), oppure un valore diverso per ogni circuito.
3. Se l'aiuto «prendi l'onda» va fatto adesso o insieme alla voce 87 (la lezione a S).

## Decisioni di Ale (26 novembre 2026)

«Ok come dici tu»: **via al passo 1** (solo banco, sopra M; se M non si accende si rifà con la barca di oggi), **spazio d'acqua 5 km per tutti** (un valore per circuito solo se un giorno i circuiti avranno un luogo), **aiuto «prendi l'onda» con la voce 87**, dopo che O5 dice se timonare sull'onda rende.
