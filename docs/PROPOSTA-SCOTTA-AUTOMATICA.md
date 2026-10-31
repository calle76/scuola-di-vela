# Proposta: la vela che si manovra da sola (scotta automatica) come aiuto attivabile

31 ottobre 2026. **Fermata 1: solo documento, nessun codice toccato.** Nasce dalla decisione di Ale (30-31 ottobre): «sì all'idea della vela (attivabile) che manovra da sola per la scuola». Serve alla scuola (le 20 lezioni) e a chi vuole imparare a timonare prima di imparare a regolare la vela. Principio 3 di `PROGETTO.md`: gli aiuti si possono disattivare.

## Oggi [codice]

- `autoSheet()` (`js/gioco.js:88`): porta il boma a `|vento apparente| − 17°` (non meno del minimo della barca), cioè la vela sempre «appena sotto il fremito». Nessuna reazione alla sbandata.
- La usano **solo** i passi delle lezioni con `autoTrim: true` (13 passi in `js/contenuti.js`, per esempio «Poggiare», «Orzare e l'angolo morto», «Ripartire», «Barra a sinistra/dritta») e la pausa (`js/avvio.js:18`). In regata e nelle prove la scotta è sempre manuale.
- Non è un'opzione: il giocatore non può accenderla né spegnerla.

## Proposta (modello più semplice)

**Una sola impostazione, «Scotta automatica» (spenta all'inizio), nelle impostazioni (⚙).** Quando è accesa, a ogni passo la scotta è `autoSheet()` invece dei tasti. Tutto il resto (barra, peso dell'equipaggio, fisica) resta del giocatore.

1. **Regola base:** quella che c'è già (`|awa| − 17°`). Nessun modello nuovo.
2. **Una sola correzione, per non scuffiare da fermi sulla regola:** se la sbandata supera una soglia, la vela viene lascata di quanto serve a rientrare (una raffica non deve scuffiare chi non può toccare la scotta). Costanti nuove (ipotesi nostre): soglia di sbandata e guadagno. Si scelgono sui semi 1-20 e si confermano sui semi 101-120 (regola dei semi).
3. **Se il giocatore tocca i tasti della scotta**, l'automatismo si spegne (con un avviso breve): niente doppio comando. Si riaccende dalle impostazioni o dal tasto.
4. **Nelle lezioni** resta com'è: i passi con `autoTrim` lo accendono da soli; negli altri passi vale l'impostazione del giocatore. Una lezione sulla scotta (1.11 «La scotta») lo spegne sempre, perché è proprio ciò che insegna.
5. **Segno visibile ma piccolo:** una scritta nel pannello delle impostazioni e una nota nel riquadro del vento quando è accesa («scotta aut.»). Niente nuovi elementi sul mare.

## Dove vale (da decidere, vedi sotto)

Proposta del consiglio: **lezioni, gioco libero e prove sì; medaglie e tornei no** (vedi decisione 1).

## Costanti nuove (tutte ipotesi nostre)

Soglia di sbandata oltre la quale si lasca, guadagno della lasca, durata dell'avviso di spegnimento. L'offset di 17° e il minimo del boma sono quelli già nel gioco. Fonti: nessuna nuova; è un aiuto di gioco, non una regola nautica. Semplificazione dichiarata: una vela vera si regola anche per la raffica e per la forma, qui si regola solo l'angolo.

## Criteri (soglie scritte prima; metro indipendente da ciò che si misura)

- **A1 acceso = spento, bit per bit.** 20 regate dell'1a, 20 dell'1b e il torneo con l'opzione spenta: istantanee del motore **identiche** alla 1.0.72; `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici carattere per carattere.
- **A2 velocità.** Con scotta automatica e barra tenuta dal pilota su 8 rotte fisse (45°, 60°, 90°, 110°, 135°, 150°, 180°, 30° al limite) e venti 6, 10 e 15 nodi: velocità media **almeno il 90%** di quella con la scotta migliore ottenuta cercandola su una griglia (metro: la griglia, calcolata fuori dal gioco). Soglia scritta prima; se esce meno si dice com'è.
- **A3 raffiche.** Raffiche da 10 a 16, 18 e 20 nodi (come `raffiche_e_virate.js`): con scotta automatica la sbandata massima è **minore o uguale** a quella di chi non fa nulla, e le scuffie non crescono (soglia: 0 scuffie in più su 20 raffiche per vento).
- **A4 chi tocca i tasti.** In 20 prove con tasto premuto a caso: l'automatismo si spegne entro 1 passo in 20 su 20 e non si riaccende da solo.
- **A5 il metro ha misurato.** Casi con l'automatismo davvero acceso (il boma cambia in almeno il 95% dei passi in cui il vento apparente cambia) e verifica che il controllo A2 trovi una scotta migliore sulla griglia.
- **A6 pagina senza `#collaudo`**: la casella c'è, si accende, nessun errore di pagina. Salvata nelle impostazioni come le altre.
- **A7 pannello e dialogo impostazioni** a 1360×650 senza pixel di eccesso (la casella nuova può farlo traboccare: è già successo con l'etichetta del registratore).
- **A8 Chromium e Firefox** per tutto A1-A7.

## Rischi

- **Insegna male:** chi imparasse sempre con l'automatismo non capirebbe la scotta. Per questo resta spento all'inizio, le lezioni sulla scotta lo escludono e le medaglie non lo contano.
- **Troppo bravo:** se batte il giocatore a mano sulla polare, toglie senso alle prove. A2 dice quanto vale (90%), non di più.
- **Due strade per la stessa scotta:** per questo punto 3 (i tasti lo spengono).
- **Dialogo impostazioni troppo lungo** (A7).

## Da decidere (Ale)

1. **Medaglie e tornei con la scotta automatica:** non contano (consiglio), contano ma con la scritta «con aiuto», o contano e basta?
2. **Dove si può accendere:** lezioni, gioco libero e prove (consiglio), oppure anche nelle regate?
3. **Tasto:** solo casella nelle impostazioni (consiglio, nessun tasto nuovo) o anche un tasto?

## Versione e file

Prevista **1.0.73** dopo il via. Tocca `js/gioco.js` (autoSheet, impostazioni), `index.html` (casella), `js/regate.js` solo per le medaglie se la decisione 1 lo richiede; un collaudo nuovo (`collaudo_scotta_automatica.py`: A1-A7). Il motore non cambia.

## Cosa resta fuori

Regolare anche il peso dell'equipaggio o la barra (sarebbe un pilota automatico vero, già presente solo nei collaudi); adattare la vela alla forma o al tempo; un livello di aiuto «progressivo» che si spegne da solo con l'esperienza.
