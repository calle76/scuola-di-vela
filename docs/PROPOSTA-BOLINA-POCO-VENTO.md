# Proposta: bolina e virata con poco vento (voce 81)

*Fermata 1, 23 novembre 2026, sera. Ale: «sì ok» a riaprire il «limite noto» del 17 ottobre come voce nuova. Nessun codice nel motore finché non arriva il via.*

## Da dove viene

- **17 ottobre 2026:** con poco vento la bolina del gioco è più lenta delle fonti (−15% con 6 nodi contro Day, F17; −12/−14% con 9 nodi contro Binns, F10 in F17), con 12 nodi coincide con Binns. Due tentativi non hanno trovato la causa; Ale ha scelto «limite noto» (`archivio/PROPOSTA-BOLINA.md` §11).
- **22-23 novembre 2026 (voci 73 e 80):** una terza fonte indipendente, **F109** (Laser misurato in acqua), dice la stessa cosa: con 3,2 nodi di vento, prua a 45°, la barca vera fa 1,05 m/s, il gioco 0,88 (−16%). E la **virata** con poco vento costa nel gioco 2,2-2,7 m contro 0,67 m della barca vera; col vento medio invece è giusta (`PROPOSTA-BARCA-73.md` §5b).
- **Perché ora:** regola di Ale «prima la barca, poi il resto» e «prima ciò su cui si tarano le altre voci»: i rivali (voci 2, 4B, 49 B, marcatura) si tarano sulla barca.

## Cosa è già escluso (17 ottobre, al centesimo)

Rampa dell'angolo morto della vela, barca tenuta piatta, timoniere che va anche sottovento, vasca sotto 3 nodi più leggera del 10%. Una vela «più forte» o meno frenata alza il poco vento ma porta i 12 nodi sopra Binns: **nessuna costante della sola vela mette a posto insieme 9 e 12 nodi.**

## Ipotesi nuove (da verificare con fonti prima di misurare)

1. **La forma della vela non cambia col vento.** Nel gioco la vela ha lo stesso profilo con 3 e con 15 nodi; in mare con poco vento si lascia la vela più grassa (vang e cunningham lenti), col vento medio la si appiattisce. I programmi di previsione delle velocità (VPP) lo rappresentano con un fattore di appiattimento («flat») che toglie portanza solo quando la barca è al limite dello sbandamento. Se è così, con poco vento la vela vera porta di più del gioco, e col vento medio uguale: **è l'unica ipotesi che separa 9 da 12 nodi.** Fonti da cercare: documentazione del VPP ORC (fattore flat), guide di regolazione della deriva monoposto (vang e cunningham con poco vento), Day 2017 (se usa il flat).
2. **Il vento all'altezza della vela.** Il gioco usa lo stesso vento a tutte le altezze; le fonti misurano il vento a un'altezza precisa (da leggere in F17, F10, F109). Con poco vento il gradiente pesa di più. Può spiegare una parte, in un verso o nell'altro: prima si legge a che altezza è misurato il vento delle fonti.
3. **La virata con poco vento** costa di più anche perché la barca è più lenta prima e dopo (parte dell'ipotesi 1) e perché con la tastiera la barra va tutta alla banda (la pala frena: con la prua girata dolcemente si perdono 1,74 m invece di 2,2-2,7). La seconda parte non è un difetto della barca ma del comando: si guarda dopo l'ipotesi 1.

## Come si procede (fermata 1, poi fermata 2)

- **Fermata 1 (questa):** leggere le fonti delle ipotesi 1 e 2; solo se c'è un numero con fonte, una prova **fuori dal motore** (copia in memoria, banco del 17 ottobre e `prua_imposta.js`), senza numeri a caso. Poi proposta con le costanti e i criteri definitivi, e ci si ferma.
- **Fermata 2 (dopo il via):** motore cambiato, collaudi, rivali, fasce delle prove e record.

## Criteri (attese nostre, scritte ora; restano le soglie della fermata 2)

| | Cosa | Soglia |
| --- | --- | --- |
| B1 | VMG di bolina con 6 nodi contro Day (F17 fig. 8) | entro −5% (oggi −15%) |
| B2 | Binns con 9 nodi, 42°-60° | entro ±5% a tutti gli angoli (oggi −11/−14%) |
| B3 | Binns con 12 nodi | entro ±3% (oggi −1/+1%): non deve peggiorare |
| B4 | 15 nodi contro Day | non peggio di oggi (+7%) |
| B5 | Velocità a 45° con 3,2 nodi contro F109 (1,05 m/s) | entro −8% (oggi −16%) |
| B6 | Virata con 3,2 nodi, prua imposta come F109 | metri persi da 1,74 verso 0,67: almeno −30% |
| B7 | Poppa e lasco | invariati entro 0,03 nodi |
| B8 | Una costante nuova al massimo, con fonte; nessuna costante cambiata senza fonte | sì |

## Costo, se si arriva alla fermata 2

Cambia la barca: polare e `raffiche_e_virate.js` con riferimenti nuovi (dichiarato), fasce delle prove ritarate e record azzerati (decisione di Ale del 15 novembre: azzerabili), rivali da rimisurare (torneo, guardiano), collaudi coi tempi. Lavoro da Opus, in più sessioni.

## Rischi

- Le fonti potrebbero non dare un numero usabile per il fattore di appiattimento: allora ci si ferma e il limite resta (come il 17 ottobre).
- Il gioco «sembra» diverso: con poco vento la barca va più forte; le lezioni che parlano di bolina con poco vento vanno rilette.
