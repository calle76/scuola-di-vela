# Proposta: strambate vere (voce 85; fermata 1, 27 novembre 2026, Opus; gioco invariato)

**Il difetto** (`sperimentale/barca-84/GIRO5.md` §6): con 10, 15 e 20 nodi la strambata dura 1,6-3 s, la velocità scende dell'1-2%, lo sbandamento massimo è 2-5°, mai una scuffia. Nella realtà con vento forte la strambata è la manovra dove si scuffia di più.

## 1. Perché nel motore non costa niente (letto nel codice, `js/motore.js`)

- **Il boma non ha un movimento suo:** a ogni passo è `min(scotta, vento apparente − 2°)`. Quando il vento passa dall'altra parte il boma è subito dall'altra parte, senza viaggio e senza colpo.
- **Il timoniere non cambia lato:** il raddrizzamento è `rmMax · S.hike`, sempre contro lo sbandamento, quindi il peso del timoniere è sempre già dalla parte giusta. Nella realtà, subito dopo la strambata, il timoniere è ancora dalla parte che è diventata sottovento.

## 2. Fonti (lette o cercate oggi; nessuna dà numeri)

- F112 (ILCA, «Gybing for Lasers»): scotta tesa, recuperata in fretta mentre la barca stramba; niente colpi alla scotta.
- ILCA «Lasers in Strong Wind», Yachting NZ (Laser con vento forte), National 12 (strambare con vento forte), forum Y&Y: con vento forte si entra veloci (meno vento apparente), si cambia lato in fretta; **le scuffie vengono quasi sempre subito dopo, con la barca che orza e si sdraia sottovento** (dopo) o sopravento (prima).
- Southampton, misure delle forze durante la strambata di uno yacht: barca grande, non deriva; da leggere solo per l'ordine di grandezza del colpo.
- **Nessun numero per una deriva** (tempo del boma, colpo, tempo per cambiare lato).

## 3. Proposta: il modello più semplice plausibile, due pezzi

1. **Il timoniere cambia lato in `T_LATO` secondi** (IPOTESI: 1,0 s, nessuna fonte). Quando il boma cambia lato, il peso del timoniere per `T_LATO` secondi passa da +1 (raddrizza) a −1 (sbanda dalla parte del boma): è una rampa, nessuna costante oltre al tempo.
2. **Il boma viaggia:** quando il vento lo spinge dall'altra parte, l'angolo del boma ruota con una velocità che dipende dal vento apparente (forza sulla vela per il braccio, inerzia della vela e del boma: IPOTESI, ordine di 0,3-0,8 s per attraversare); a fine corsa, contro la scotta, il colpo entra come un impulso di sbandamento e di imbardata (la barca orza dopo la strambata, come dicono le fonti).

Chi stramba veloce, con poca scotta lasca e con la barra dolce sente meno vento e meno colpo; chi stramba piano, con la scotta tutta fuori e col vento forte rischia: è la tecnica di F112 e delle fonti del §2, senza regole scritte apposta.

**Il pezzo 1 da solo** potrebbe bastare: si prova prima quello (meno costanti), poi il 2 solo se non basta.

## 4. Criteri (soglie nostre, scritte prima di misurare)

- **G1, poco vento resta facile:** con 6 e 10 nodi, strambata col pilota (150° → 150°), 20 semi: mai scuffia, sbandamento massimo sotto 20°.
- **G2, vento forte costa:** con 20 nodi, strambata del pilota «buono» (veloce, scotta corta): scuffia in almeno 1 su 20 e al massimo 5 su 20; sbandamento massimo mediano oltre 30°. Con il pilota «cattivo» (lento, scotta tutta lasca): scuffia in almeno 8 su 20.
- **G3, la manovra costa tempo:** con 15 nodi il costo della strambata (`costo_manovre.js`, T_ABB) cresce almeno del 50%.
- **G4, la virata non cambia:** `virata1b.js` e il costo della virata identici; polare identica (non c'entra il cambio di lato).
- **G5, i rivali non peggiorano troppo:** regate lunghe col pilota, scuffie dei rivali nelle strambate al massimo +5 su 120 regate (altrimenti la loro guida va aggiornata, voce a parte).

## 5. Rischi e costo

- Cambio della barca: lista intera (rotta-dati con T_ABB nuovo, medaglie con abbattute, Coach, rivali, lezioni 5 e 13 sulle abbattute col pilota).
- Le soglie G2 sono inventate: nessuna fonte dice quante strambate su 20 finiscono in scuffia. Si dichiarano come attese nostre.
- Lavoro: un giorno, più il giro della lista.

## 6. Cosa serve da Ale

Il via al pezzo 1 (timoniere che cambia lato), e se vuole fin da ora anche il pezzo 2. È prima della 86 (strapoggio).

Fonti: [ILCA, Lasers in Strong Wind](https://ilcasailing.org/lasers-in-strong-wind/), [ILCA, Gybing for Lasers](https://ilcasailing.org/gybing-for-lasers/), [Yachting NZ, Laser Heavy Wind](https://www.yachtingnz.org.nz/sites/default/files/2018-10/coaches%20and%20officials%20-%20Resources%20-%20Laser%20Heavy%20Wind.pdf), [National 12, gybing in strong winds](https://national12.org/hints/coaching/coaching_gybing.shtml), [Y&Y forum](https://www.yachtsandyachting.com/Forum/printer_friendly_posts.asp?TID=9540), [Southampton, strambata di uno yacht](https://eprints.soton.ac.uk/176485/). Le pagine non sono state lette per intero: prima del codice vanno lette e messe in `FONTI-PUBBLICHE.md`.
