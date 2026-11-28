# Proposta: la freccia dell'obiettivo più visibile (voce 72)

*Fermata 1, 21 novembre 2026. Nasce dalla chat di Lucio («con i lati lunghi, anche con la visuale più larga, non si vede tutto il campo, in particolare in partenza») e dalla risposta di Ale: non allargare lo zoom (le boe diventerebbero puntini), **rendere più visibile la freccia**. Nessun codice finché non arriva il via. Si lega a `PROPOSTA-VOLUME-ZOOM.md` solo per il tasto dello zoom.*

## Cosa c'è oggi (letto in `js/disegno.js`, `arrowAt` e `offscreenArrow`)

- Quando l'obiettivo (boa, linea o arrivo) è fuori dallo schermo compare un **triangolo arancione di circa 22 px** sul bordo, verso l'obiettivo, con la **distanza** accanto («120 m», arrotondata ai 5 m). Dentro lo schermo non c'è nulla.
- Nelle regate sta a 30 px dal bordo e, se cadrebbe sull'orologio in alto, scende a 80 px.
- Il nome dell'obiettivo **non** c'è: una freccia a 300 m dice «da quella parte», non «la boa 1» né «la linea di partenza».
- Lo zoom (tasti 1 e 2, rotella) arriva a 0,1: a quel punto il campo si vede, ma le boe sono puntini. Con le regate lunghe (lato da circa 440 m) a zoom 1 la partenza e la prima boa non stanno insieme sullo schermo.

## Il modello più semplice

1. **Più grande:** da 22 px a circa 34 px (ipotesi nostra, ×1,5), con un **contorno scuro** attorno per leggersi su mare chiaro e scuro.
2. **Con il nome dell'obiettivo** sopra la distanza: «Boa 1», «Linea», «Arrivo» (le parole che il gioco già usa). Una riga, stesso carattere della distanza.
3. **Una pulsazione dolce** (da 100% a 115% della grandezza, circa 1,2 volte al secondo) **solo se l'obiettivo è lontano più di 150 m** e resta fuori schermo (ipotesi nostra, per non distrarre da vicino). Si spegne quando l'obiettivo entra nello schermo.
4. **Non coprire:** continua a evitare l'orologio, il riquadro delle bandiere, quello del Coach e il riquadro delle penalità (stesso criterio di oggi, esteso ai nuovi ingombri).
5. **Nessuna impostazione nuova:** vale per tutti gli obiettivi di tutte le regate; fuori regata (lezioni, prove) cambia solo la grandezza.

Non propongo: ingrandire lo zoom massimo, una mini-mappa, o frecce multiple (una per boa): sono altri passi, se serviranno.

## Costanti nuove (tutte ipotesi nostre, senza fonte)

Grandezza 34 px (da 22), contorno 2 px, pulsazione ±15% a 1,2 Hz oltre 150 m, riga del nome da 13 px (come la distanza).

## Criteri (soglie nostre, dichiarate prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| F1 | Grandezza | freccia letta dai tratti del canvas: lunghezza almeno 30 px, larghezza almeno 24 px; contorno presente |
| F2 | Il nome | a ogni obiettivo il nome giusto: partenza «Linea», boa 1, boa 2, arrivo «Arrivo»; 100% su almeno 40 casi, ricalcolati dalla posizione delle boe e non letti dal gioco |
| F3 | La pulsazione | oltre 150 m la dimensione oscilla fra 100% e 115% (±2%) e sotto 150 m resta fissa; fuori schermo lontano in 20 situazioni, vicino in altre 20 |
| F4 | Non copre | su 1360x650 e su 1280x720, nessuna sovrapposizione fra la freccia (con nome e distanza) e orologio, bandiere, Coach e penalità, nel caso peggiore (tutti in vista); 0 px di eccesso |
| F5 | Regata uguale | arrivi e tempi identici al bit con la freccia nuova e con quella vecchia (solo disegno) |
| F6 | Regate lunghe | nelle regate lunghe, alla partenza (t = −30 s) l'obiettivo (la linea) è fuori schermo a zoom 1: la freccia compare e il nome è «Linea»; la prima boa a 440 m idem |
| F7 | Come un giocatore | pagina senza `#collaudo`, una regata lunga giocata con i tasti 1 e 2: freccia vista, 0 errori |

Il metro non deve dipendere da ciò che misura: F2 e F6 si ricalcolano dalle coordinate delle boe nel collaudo; il collaudo stampa il numero dei casi e fallisce con zero casi.

## Rischi

- **Troppo vistosa** in una regata affollata. La pulsazione è solo oltre i 150 m e si può togliere o ridurre dopo la prova di Ale.
- **Il nome può essere ambiguo** quando l'obiettivo cambia (dopo la boa 1 la freccia punta alla boa 2): si ricalcola dal giro (`me.leg`) e si prova in F2.
- **Lucio ha detto che non vede il campo alla partenza**: la freccia non fa vedere il campo, dice dove andare. Se la partenza resta confusa si può valutare un cenno diverso (una seconda freccia verso la linea con la scritta «Linea»); fuori da questa proposta.

## Passi, dopo il via

1. Dimensione, contorno, nome e pulsazione in `offscreenArrow`; criteri F1-F7 in `collaudo_freccia.py` (Chromium e Firefox).
2. Il pannello e i riquadri (`collaudo_pannello.py`, riquadro bandiere, Coach) restano da rilanciare.
3. Documenti, versione, `CHANGELOG.md`. Sonnet va bene.
