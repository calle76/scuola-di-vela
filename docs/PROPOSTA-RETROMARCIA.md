# Proposta: la retromarcia senza tetto

16 ottobre 2026. **Fermata 1:** il gioco non è stato toccato. Le misure qui sotto vengono da un banco fuori dal gioco, che usa il motore vero (`tests/fisica/motore.js`) e toglie il tetto solo in memoria.

## La scelta di Ale

**Ale (16 ottobre 2026):** la retromarcia va impostata come una **barca lasciata andare con la vela che sventola**. La velocità all'indietro nasce solo dalla spinta della vela che sbatte contro il freno dell'acqua, senza un tetto messo apposta.

Ricerca di partenza: `RICERCA-RETROMARCIA.md`. La retromarcia è vera e si insegna; nessuna fonte dà velocità o tempi; il tetto `backMax` (1,2 m/s, cioè 2,3 nodi) non ha una fonte.

## La proposta (modello più semplice)

- **[codice]** In `step()` (`js/motore.js`) si toglie la riga `S.u = Math.max(-BOAT.backMax, S.u)` e la costante `backMax`. Si toglie anche dal laboratorio (`js/laboratorio.js`) e dalla guida ai valori.
- **Nessun freno «di poppa» in più.** La ricerca lo suggeriva come ipotesi (lo specchio di poppa e il timone frenano di più quando si va all'indietro), ma non c'è nessun numero: aggiungerlo vorrebbe dire scegliere un valore a occhio. All'indietro resta la tabella della vasca, misurata con la prua avanti: **semplificazione dichiarata**.
- **Nessuna costante nuova.** Ne sparisce una.
- Versione **1.0.8**.

## Cosa cambia: misure sul banco (prima e dopo)

Barca con la prua al vento, barra al centro, scotta al 100% e al 50% (stesso risultato), ferma o lanciata a 2 nodi; 60 s a passi di 1/240 s.

| Vento | Massimo all'indietro oggi | Senza tetto | Prua bloccata nel vento, senza tetto |
|---|---|---|---|
| 6 nodi | 0,97 nodi | 0,97 (uguale) | 1,57 |
| 10 nodi | 2,33 nodi | 2,34 | 2,60 |
| 15 nodi | 2,33 nodi | **3,40** | 3,73 |
| 20 nodi | 2,33 nodi | **4,31** | 4,66 |

- **Con vento fino a 10 nodi non cambia quasi niente.** Il tetto conta solo con vento più forte.
- **Quanto presto parte la retromarcia non cambia.** I tempi per arrivare a −0,5 nodi sono identici: con 10 nodi 1,6 s da ferma e 5,7 s da 2 nodi; con 15 nodi 0,6 s e 2,6 s. Se la retromarcia sembra partire troppo presto (impressione di Ale), questa modifica **non** la corregge: dipende dalla spinta della vela che sbatte e da quanto in fretta la barca si ferma, non dal tetto.
- **Correzione alla ricerca.** `RICERCA-RETROMARCIA.md` §3 stimava 3,5 nodi all'indietro con 10 nodi di vento. Sul motore vero, con la prua tenuta ferma nel vento, sono 2,60 nodi: andando all'indietro il vento apparente cala, e con lui la spinta. La stima della ricerca era un conto a mano con la spinta fissa.
- **La barca all'indietro gira più in fretta.** Nel motore la rotazione è proporzionale alla velocità: con la barra a fondo, a 2,3 nodi all'indietro circa 33 °/s, a 3,4 nodi circa 48 °/s (conto dalla formula, da misurare nella fermata 2).

## Criteri della fermata 2 (soglie: attese nostre, dichiarate prima)

1. **Banco della retromarcia** (questo, messo in `tests/fisica/retromarcia.js`): dopo la modifica, i numeri «senza tetto» della tabella devono uscire uguali al centesimo di nodo. È il controllo che la modifica sia quella proposta.
2. **Avanti non cambia niente:** `polare.js` identico carattere per carattere.
3. **`raffiche_e_virate.js`:** si riporta l'uscita prima e dopo. Attesa nostra: identica, perché lavora a 10 nodi.
4. **Uscita dall'angolo morto (`angolo_morto.js`):** oggi escono 2188 casi su 2196 (gli 8 che restano sono barche ferme a 52-56° dal vento, che non arretrano). Soglia: **non meno di 2188**; tempi mediani riportati per ogni vento. Seconda parte (risposta sbagliata della domanda 22): oggi 28 su 4860, si riporta.
5. **Nel gioco, guidando:** `collaudo_suggerimento.py` (il suggerimento della retromarcia) e il passo «Ripartire» della lezione 5 con `collaudo_lezioni.py`: stesso esito di oggi. `collaudo_laboratorio.py` aggiornato (oggi usa `backMax` in una prova) e passato.
6. **Impronta del gioco:** riferimento preso subito prima; si riporta quante scene cambiano. Attesa nostra: poche, solo dove la barca va all'indietro oltre 2,3 nodi.
7. **Pagina caricata come la carica un giocatore** (senza `#collaudo`): nessun errore.
8. **Il giudizio giocando è di Ale**, soprattutto con 15-20 nodi.

## Rischi

- **Con vento forte la retromarcia diventa vistosa:** 3,4 nodi con 15 nodi, 4,3 con 20. L'unico appiglio è un forum (affidabilità bassa), dove si dice che una deriva in singolo «può planare all'indietro» con vento forte. Senza il freno di poppa, i valori sono probabilmente un po' alti; non sappiamo di quanto.
- **La barca all'indietro può girare molto in fretta** con la barra a fondo, e il suggerimento a schermo dice di mettere la barra verso il boma. Da guardare giocando.
- **I record delle prove** non dovrebbero cambiare (nelle prove non si va all'indietro di proposito). Si controlla con l'impronta; se cambiano, si dice.
- **Cosa resta fuori:** l'impressione che la retromarcia parta troppo presto; il comando «spingi il boma» (livello 2); la regola 21.3 sulle barche che vanno all'indietro (livello 2, da riportare in `REGOLE-DI-REGATA.md` quando servirà).

## Cosa serve da Ale

Il via alla fermata 2, oppure una correzione. In particolare: va bene **nessun freno di poppa**, cioè la barca lasciata andare così com'è, anche se con 20 nodi arriva a 4,3 nodi all'indietro?

## Decisione di Ale ed esito (fermata 2, 16 ottobre 2026, versione 1.0.8)

**Ale:** «sì va bene», anche senza freno di poppa (fino a 4,3 nodi all'indietro con 20 nodi).

**Fatto:** tolta da `step()` la riga del tetto e la costante `backMax` (anche da `js/laboratorio.js`); il collaudo del laboratorio usa `maxRudder` al posto di `backMax` nella prova di esportazione. Banco in `tests/fisica/retromarcia.js`.

**Criteri:**
1. Banco: numeri uguali al centesimo a quelli della tabella sopra (0,97 / 2,34 / 3,40 / 4,31; regime 1,57 / 2,60 / 3,73 / 4,66). **OK.** Rotazione all'indietro con la barra a fondo, misurata: 33 / 46 / 56 °/s con 10 / 15 / 20 nodi.
2. `polare.js` identico carattere per carattere. **OK.**
3. `raffiche_e_virate.js` identico. **OK** (attesa confermata).
4. `angolo_morto.js`: 2.188 su 2.196 e 28 su 4.860, uscita identica a prima. **OK** (soglia: non meno di 2.188).
5. `collaudo_suggerimento.py` identico; `collaudo_lezioni.py` stesso esito (una differenza di tempo nella scuffia della lezione 6, 0,8 contro 1,0 s, ripetuta 3 volte prima e 3 dopo: sempre 1,0 s, quindi variazione fra corse); `collaudo_laboratorio.py` OK.
6. Impronta: **0 scene diverse su 63** (attesa nostra «poche»: nessuna). Vuol dire che lezioni, prove e regate dell'impronta non portano mai la barca all'indietro oltre 2,3 nodi; non dice niente sul gioco libero con vento forte, che è il caso che cambia.
7. Pagina caricata senza `#collaudo`: nessun errore.
8. Giudizio giocando: di Ale, soprattutto con 15-20 nodi.
