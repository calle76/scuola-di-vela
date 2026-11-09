# Proposta: avversario che si pianta alla boa (9 novembre 2026)

Voce 3 di `DA-FARE.md`; osservazioni 90, 103, 109 di `OSSERVAZIONI-GIOCANDO.md`.

Ale (9 novembre): «poi passa alla boa senza chiedere». Il via è dato in anticipo: proposta, soglie e misura senza fermata, ma le soglie sono committate **prima** di misurare. Per la decisione del 9 novembre (`DECISIONI.md`) si misura sulle **regate del torneo**.

## 1. Cosa succede

In tre regate di Ale un avversario arriva alla boa a destra, all'altezza della boa o poco sotto. Invece di passare oltre, vira indietro verso il punto di passaggio e si ferma: 0 nodi e anche all'indietro, per 3-8 s.

- **90** (17:59): Verde manca di 2 m il punto di passaggio 0.
- **103** (22:00 bastone): Blu è 6 m a destra della boa e 1 m sotto, mure a dritta. La rotta verso il punto oltre la boa passa circa 2,3 m sopra la boa: la correzione «sul bordo» della 1.2.15 chiede 3 m (`PASSO_M`), quindi non scatta.
- **109** (22:00 giri): Blu è 7 m a destra e 2,0 m sopra la boa. La regola «sopra la boa» chiede più di 2 m (`wy < -R.up - 2`), quindi non scatta per un soffio.

## 2. Perché (letto nel codice, `js/regate.js`, `targetOf`)

Alla boa 1 l'avversario punta tre punti di passaggio, nell'ordine: 0, a destra e poco sopra la boa; 1, oltre la boa a sinistra; 2, per riprovare. Passa al punto 1 in tre casi:
- quando è entro 4 m dal punto 0;
- quando è «sopra» la boa (più di 2 m sopra e più di 3 m a destra);
- quando è «sul bordo»: arriva al punto 1 senza virare e la sua rotta passa almeno 3 m sopra la boa.

Chi arriva vicino alla boa ma appena fuori da tutte e tre le condizioni punta ancora il punto 0, che ha di fianco o dietro, col vento in faccia. Allora vira, perde velocità e si pianta. Le tre soglie sono ipotesi nostre, e nei tre casi visti si mancano di pochi decimetri.

## 3. Modello più semplice

Nessuna regola nuova: si allargano le due soglie che falliscono per poco, solo alla boa 1.
- `PASSO_M` (la rotta sul bordo deve passare almeno questi metri sopra la boa): oggi 3.
- `SOPRA_M` (quanti metri sopra la boa per contare «sopra»): oggi 2, una costante nuova che dà un nome al 2 scritto nel codice.

Combinazioni da provare (`PASSO_M`, `SOPRA_M`): (2, 2), (1,5, 2), (3, 0), (1,5, 0).

Rischio: una rotta più vicina alla boa la tocca più spesso (le boe sono ostacoli dalla 1.0.63), oppure la lascia dal lato sbagliato. Lo misurano G4 e G5.

**Cosa non si tocca:** la fisica, chi cede, la boa 2 del triangolo, il giocatore.

## 4. Misura

`tests/misura_boa_avversari.py`. Le 6 regate del torneo (bastone e triangolo; 10 nodi costanti, raffiche, salti di vento), principianti ed esperti, preparazione 60 s. Il giocatore lo guida il pilota. Si corre fino all'arrivo di tutti, senza finestra d'arrivo.

Per ogni avversario e per ogni boa si misura, mentre la punta ed è entro 40 m da lei: i secondi passati, le virate, le fermate (3 s di fila sotto 1 nodo), se tocca la boa.

Scelta sui **semi 801-830**, conferma sui **semi 831-860** (mai usati). Riferimento: il gioco di oggi, cioè la 1.2.18, oppure la 1.2.19 se nel frattempo è adottata la proposta della partenza.

## 5. Criteri (soglie nostre, scritte prima di misurare)

- **G1, fermate entro 40 m:** almeno dimezzate rispetto al riferimento. Il criterio vale solo se il riferimento ne ha almeno 10; con meno il contatore non misura niente, e lo si riporta.
- **G2, passaggi con 3 o più virate entro 40 m:** al massimo +10%.
- **G3, mediana dei secondi entro 40 m:** al massimo +1 s.
- **G4, boa toccata:** al massimo il più grande fra +10% e +5 casi.
- **G5, boe sbagliate:** al massimo +2. **Non arrivate:** non aumentano.
- **G6, contatti dopo il via:** al massimo +10%.
- **G7, non-regressione:** `polare.js` e `raffiche_e_virate.js` identici, `impronta1b.js` al bit; `collaudo_giro_boa.py` verde.

Fra le combinazioni che passano si sceglie quella con meno fermate (G1). A parità, quella più vicina ai valori di oggi (3, 2).

Se nessuna passa sui semi di scelta, o la scelta non passa la conferma, non si adotta nulla e lo si riporta così.

## 6. Costo

Circa 4 ore di calcolo col termostato: 5 configurazioni sulla scelta, 2 sulla conferma.
