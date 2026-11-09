# Proposta: avversari, dove perdono tempo e prima correzione (la poppa) (9 novembre 2026, notte)

Ale: «finita la 1.2.23 parti dagli avversari senza chiedere». Il via è in anticipo: proposta e soglie committate **prima** di misurare, poi codice e misura.

Per la decisione del 9 novembre si misura sulle regate del torneo; la Scuola fa da controllo.

## 1. Diagnosi: la rotta ottimale come metro

`tests/misura_avversari_rotta.py`, semi 1101-1130, le 4 regate del torneo, principianti ed esperti, 240 regate e 720 avversari.

Per ogni avversario e ogni lato si confronta il tempo vero con la rotta ottimale partita da dove e quando lui ha cominciato il lato (`rotLatiBarca`, `js/rotta.js`). La rotta ottimale conosce il vento in anticipo e ignora le altre barche: è un limite, non un obiettivo da raggiungere.

| lato | secondi persi, mediana | quota delle perdite | virate vere / della rotta ottimale |
| --- | --- | --- | --- |
| bolina | 24,8 s (29%) | 64% | 3,8 / 2,5 |
| poppa (bastone) | 11,6 s (20%) | 15% | — |
| lasco 1 (triangolo) | 4,4 s (9%) | 7% | — |
| lasco 2 (triangolo, verso l'arrivo) | 11,0 s (28%) | 14% | — |

- **Partenza:** taglio della linea dopo il via, mediana 2,4 s. Va bene.
- **Bolina:** il quarto migliore perde 7,9 s con 2,8 virate (contro 2,3); il quarto peggiore perde 49,8 s con 4,7 virate (contro 2,5).
- **Principianti ed esperti:** i principianti perdono di più in bolina (32% contro 27%) e poco di più in poppa (22% contro 19%).

**Dove sta il margine:**
1. **Bolina** (64%). Due cose:
   - troppe virate: bordi a tempo e quelle vicino alla boa, `PROPOSTA-LAYLINE.md` §5;
   - nessun gioco sui salti: la rotta ottimale vira sugli scarsi, gli avversari no.

   È la correzione più grande e più delicata: una proposta a parte.
2. **Poppa** (15%). La causa si legge nella polare della barca del gioco:
   - la VMG verso la boa sottovento è massima a **circa 170°** dal vento con 6-14 nodi (a 10 nodi 4,17 nodi a 170° contro 3,81 a 150°, il 9% in meno);
   - gli avversari vanno a `ai.down` = 150-155° gli esperti e 142-150° i principianti.

   È la voce 5 di `DA-FARE.md` (osservazione 95: «in poppa gli avversari vanno a zig-zag a 150-155° dal vento, più lenti della poppa piena»). **Prima correzione: questa.**
3. **Lasco 2** (14%), dalla boa 2 all'arrivo: da guardare. Probabilmente il bersaglio è il centro della linea e non il punto più vicino. Voce a parte.

## 2. Modello più semplice (poppa)

L'angolo di poppa di ogni avversario diventa quello della VMG migliore della polare al vento del momento (`vmgPoppa`, circa 170°), meno `DOWN_E` gradi, più la differenza personale di oggi rispetto a 155°: `ai.down − 155`, cioè da −5 a 0 gli esperti e da −13 a −5 i principianti.

Così restano le differenze fra livelli e fra barche, e il carattere di ognuna. Vale nei due punti dove oggi si usa `ai.down`:
- quando il bersaglio è «in poppa piena»;
- per la prua delle abbattute a bordi.

La regola dei 172° e del tempo minimo fra due abbattute (osservazione 85) resta com'è.

**Costante nuova (ipotesi nostra):** `DOWN_E` ∈ {0, 5, 10}°. `null` è spento, come oggi.

**Cosa non si tocca:** la fisica, chi cede, la bolina, la partenza, i giri di boa, il giocatore.

**Rischio:** più vicino ai 180° la barca strambare per sbaglio o scuffiare in raffica. Lo controllano Q4 e Q5.

## 3. Criteri (soglie nostre, scritte prima di misurare)

Misura con `misura_avversari_rotta.py`, aggiunto il conteggio dei cambi di mure in poppa e delle scuffiate, e con `misura_boa_avversari.py` (`TORNEO=nuovo`). Si confronta col gioco di oggi sugli stessi semi.

Scelta di `DOWN_E` sui **semi 1131-1160**, conferma sui **semi 1161-1190**, mai usati.

- **Q1, poppa:** secondi persi sul lato di poppa, mediana, almeno −30%.
- **Q2, arrivo mediano degli avversari:** non peggiora.
- **Q3, contatti dopo il via:** al massimo +10%.
- **Q4, cambi di mure** (abbattute) per lato di poppa, media: al massimo +1.
- **Q5, scuffiate degli avversari:** al massimo +10% e +3 casi.
- **Q6, boe:** toccata, sbagliate, non arrivate come G4-G5 di `PROPOSTA-BOA-PIANTATA.md` §5.
- **Q7, Scuola:** `collaudo_regate.py` 6 0, 6 1, `--lungo`, nessuna «BLOCCATA».
- **Q8, non-regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.

Fra i valori che passano si sceglie quello che perde meno in poppa (Q1). A parità, il `DOWN_E` più grande, cioè più lontano dai 180°. Se nessuno passa, gli avversari restano come sono e lo si riporta.

## 4. Costo

Codice piccolo. Misura col termostato: 4 configurazioni sulla scelta e 2 sulla conferma, circa 2 ore.
