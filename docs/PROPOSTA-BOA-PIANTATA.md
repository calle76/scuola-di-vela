# Proposta: avversario che si pianta alla boa (9 novembre 2026)

Voce 2 di `DA-FARE.md` (era la 3); osservazioni 90, 103, 109 di `OSSERVAZIONI-GIOCANDO.md`.

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

## 7. Esito della scelta (semi 801-830, 360 regate del torneo, 1620 passaggi di avversari vicino a una boa): non passa

| (`PASSO_M`, `SOPRA_M`) | G1 fermate | G2 3+ virate | G3 mediana | G4 boa toccata | G5 sbagliate / non arrivate | G6 contatti |
| --- | --- | --- | --- | --- | --- | --- |
| oggi (3, 2) | 76 | 350 | 27,0 s | 51 | 0 / 0 | 224 |
| (2, 2) | 53 ✗ | 330 | 26,2 s | **81** ✗ | 0 / 0 | 209 |
| (1,5, 2) | 51 ✗ | 314 | 25,6 s | **139** ✗ | 2 / 0 | 221 |
| (3, 0) | 62 ✗ | 345 | 26,8 s | 47 | 2 / 1 | 211 |
| (1,5, 0) | 51 ✗ | 314 | 25,6 s | **139** ✗ | 2 / 0 | 221 |

Soglie: G1 ≤38 (metà di 76), G4 ≤56. **Nessuna combinazione passa G1**, e abbassare `PASSO_M` fa toccare la boa molto più spesso. Allargare le soglie toglie al massimo un terzo delle fermate. La conferma sui semi 831-860 non si fa. Il gioco resta con (3, 2); restano nel codice i nomi `SOPRA_M` e `PASSO_SX`, con gli stessi valori di prima.

Note:
- Il riferimento ha 76 fermate, quindi il contatore misura davvero (soglia minima 10).
- (1,5, 0) e (1,5, 2) danno numeri identici: con `PASSO_M` 1,5 la regola «sopra» non scatta mai per prima.

## 8. Seconda prova: il giro diretto (9 novembre 2026; via di Ale in anticipo: «vai avanti senza chiedere»)

**Dove si fermano** (diagnosi sui semi 801-815, solo riferimento): 38 fermate. 30 sono con la barca che punta già il punto oltre la boa, tra 4 e 12 m a destra della boa e tra 1 e 4 m sopra. Tracciato un caso (seme 805, esperti, Blu):
1. arriva mure a dritta 4,6 m a destra della boa e 0,5 m sotto;
2. vira verso il punto 0, che sta sopra a destra;
3. a metà virata il bersaglio diventa il punto oltre la boa, e la barca rivira senza velocità: 5 s ferma, anche all'indietro.

È la doppia virata dell'osservazione 90. Eppure da lì, di bolina stretta mure a dritta, sarebbe passata circa 4 m sopra la boa senza virare. La regola «sul bordo» non lo vede, perché guarda la retta verso il punto oltre la boa: è più poggiata della bolina e passa solo 1,9 m sopra.

**Modello.** Alla boa 1, chi soddisfa insieme queste condizioni:
- è mure a dritta;
- è a destra della boa, entro `R_DIR` m da lei;
- di bolina (angolo di bolina + 3°) passerebbe sopra la boa di almeno `M_DIR` m.

Questa barca punta subito il punto oltre la boa (`rp` 1) e, finché non ha superato la boa (fino a 3 m alla sua sinistra), tiene la bolina invece della retta. Così non vira verso il punto 0 e non passa troppo vicino alla boa. Poi poggia verso il punto oltre, come oggi.

**Costanti nuove (ipotesi nostre):** `M_DIR` ∈ {2, 3, 4} m, `R_DIR` ∈ {15, 30} m. Quindi 6 combinazioni. `PASSO_M` e `SOPRA_M` restano 3 e 2.

**Criteri:** gli stessi del §5 (G1-G7, soglie uguali, sul riferimento degli stessi semi). Scelta sui **semi 861-890**, conferma sui **semi 891-920**, mai usati. Regola di scelta come nel §5.

**Nota sulla misura:** bastone e triangolo hanno la stessa prima bolina e quindi danno passaggi identici alla boa 1. I passaggi indipendenti sono circa la metà di quelli contati. Le soglie sono relative, quindi il confronto resta valido; lo si riporta.
