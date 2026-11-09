# Proposta: la layline, pezzi 2-4 (9 novembre 2026, sera)

`DECISIONI.md`, 9 novembre: la layline in quattro pezzi. Il pezzo 1 (nella rotta ottimale) è nella 1.2.22.

Ale: «ok, passa alla layline senza chiedere». Il via è in anticipo, come per la boa: proposta e soglie committate **prima** di misurare, poi codice e misura senza fermata.

## 1. Cosa c'è già

- **La polare della barca del gioco** (`js/rotta-dati.js`) dà l'angolo della layline: la rotta sul fondo della bolina più conveniente, scarroccio compreso. È circa 48° dal vento con 6-15 nodi (`rotLay`, `js/rotta.js`).
- **Gli avversari in bolina** (`js/regate.js`, guida generale):
  - fanno bordi di durata a caso;
  - quando il bersaglio è più largo della loro bolina (`ai.up`, angolo di **prua** 45-54° secondo il livello), lo puntano dritto.

  Lo scarroccio (3-5°) fa scendere la barca sotto la rotta: chi punta dritto «appena» sulla layline di prua arriva corto, torna in bolina e rivira.

  È proprio il motivo che la rotta ottimale trova più spesso col pilota, che usa la stessa guida: «negli ultimi 80 m prima della boa hai virato 2 volte», in 8 regate su 20 (`PROPOSTA-ROTTA-OTTIMALE.md` §8).

## 2. Modello più semplice

**Pezzo 2, aiuto in acqua (disattivabile).**
- **Cosa si vede:** due linee tratteggiate dalla boa di bolina, una per mura, con l'angolo di `rotLay` e il vento alla boa in quell'istante. Coi salti girano.
- **Quando si vede:**
  - fino a quando la boa non è girata;
  - solo nelle regate fuori dalla Scuola, cioè regate a tema e torneo, non negli esercizi.
- **Impostazioni (⚙):** una riga «Layline» con tre scelte:
  - «no»;
  - «nelle regate, non nel torneo», che è quella di partenza;
  - «anche nel torneo».

  Così nel torneo parte spenta ma si può accendere (decisione di Ale).

**Pezzo 3, lezione.** Deriva resta nascosta (decisione del 4 novembre), quindi la lezione si scrive come testo nella `PROPOSTA-LIVELLO-DERIVA.md` ed entra in gioco con Deriva. Fonti: F77 e F78 (Dellenbaugh, *Speed & Smarts*), parafrasate.

**Pezzo 4, avversari: la layline col loro scarroccio.**
- **Bolina:** in bolina finché il bersaglio non è oltre la loro rotta sul fondo di bolina, cioè `ai.up` più lo scarroccio della polare a quell'angolo, più un margine `LAY_MARG`. Oggi si guarda solo `ai.up`.
- **Puntando un bersaglio a proravia del traverso:** la prua si tiene sopravento al bersaglio dello scarroccio, ma mai più stretta di `ai.up`, così la rotta sul fondo va al bersaglio.
- **Costanti:** `LAY_MARG` ∈ {0, 2, 4}° è l'ipotesi da scegliere. Lo scarroccio viene dalla polare: nessun numero nuovo.

**Cosa non si tocca:** la fisica, chi cede, i punti di passaggio alla boa (`targetOf`), la partenza, il giocatore.

**Rischi:**
- Chi aspetta di più prima di puntare dritto può andare oltre la layline: lo controllano i secondi vicino alla boa.
- Più barche sulla stessa layline vuol dire più incroci: lo controllano i contatti.

## 3. Criteri (soglie nostre, scritte prima di misurare)

**Pezzo 4**, `misura_boa_avversari.py` con `TORNEO=nuovo` (le 4 regate del torneo più le 2 di confronto), principianti ed esperti, contro il gioco della 1.2.22 sugli stessi semi. Scelta di `LAY_MARG` sui **semi 1041-1070**, conferma sui **semi 1071-1100**, mai usati.

- **L1, virate vicino alla boa:** le virate degli avversari entro 40 m dalla boa 1 calano di almeno il 10%.
- **L2, arrivo mediano** degli avversari: al massimo +1 s.
- **L3, secondi entro 40 m** dalla boa (mediana): al massimo +1 s.
- **L4, fermate entro 40 m:** al massimo +20%.
- **L5, boa toccata:** al massimo il più grande fra +10% e +5 casi.
- **L6, contatti dopo il via:** al massimo +10%.
- **L7, boe sbagliate e non arrivate:** non aumentano più di 2.
- **L8, Scuola:** `collaudo_regate.py` 6 0, 6 1 e `--lungo` su tutte e due, nessuna «BLOCCATA».
- **L9, non-regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.

Fra i valori che passano si sceglie quello con meno virate (L1). A parità, il margine più piccolo. Se nessuno passa, gli avversari restano come sono e lo si riporta.

**Pezzo 2:**
- **P1, dove si vede:**
  - con «nelle regate» si vede nelle regate a tema e non nel torneo, nelle regate della Scuola né negli esercizi;
  - con «anche nel torneo» si vede anche nel torneo;
  - con «no» non si vede mai;
  - sparisce dopo il giro della boa.

  Controllato nella pagina in tutti i casi.
- **P2, è giusta:**
  - l'angolo disegnato coincide con `rotLay`;
  - con un salto di 10° le linee girano di 10°;
  - una barca della polare che parte da un punto della layline a 100 m e va col vento costante alla rotta sul fondo della layline passa entro 2 m dalla boa.
- **P3, pannello e impostazioni** a 1360x650 senza pixel in eccesso (`collaudo_pannello.py`; riquadro ⚙).
- **P4, pagina caricata come la carica un giocatore** (senza `#collaudo`): la riga «Layline» funziona, nessun errore.

## 4. Costo

Mezza giornata per il codice. Per la misura, col termostato, 3 valori sulla scelta e 1 sulla conferma: circa 2 ore.
