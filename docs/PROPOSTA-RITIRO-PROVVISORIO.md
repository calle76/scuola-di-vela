# Proposta: il ritiro salvato anche se la pagina si chiude di colpo (voci 41 e 6, osservazione 86)

*Fermata 1, 24 novembre 2026; via di Ale e fermata 2 lo stesso giorno (1.3.53): esito in fondo.*

## Il difetto

Chi chiude la scheda a metà di una regata del torneo è ritirato. Per salvarlo il gioco deve prima simulare il resto della regata dei rivali (`torEsci` → `torChiudi`): 1,3-2,7 s nelle regate corte, **3-6 s nelle lunghe**, quelle che giocate. Il browser non aspetta tanto: se interrompe la simulazione, il ritiro si perde e la regata si può ricorrere da capo. Cioè: chiudendo la scheda si può cancellare una regata andata male. Non si perdono le regate già finite.

**Numeri che abbiamo:** osservazione 86, Firefox, regate corte: 39 su 40 salvate a computer scarico, 0 su 5 a computer carico. `collaudo_torneo` C11: 4 su 40 perse, poi 1 su 40, di nuovo 1 su 40 (giro GitHub del 24 novembre, Firefox, «torneo 6, chiusura a 1 s»); Chromium 40 su 40. **Sulle regate lunghe la chiusura della scheda non è stata misurata** (C11 lungo è fuori dalla suite, voce 71); l'attesa, dai tempi, è che si perda spesso.

**Peso:** basso per chi gioca onesto, perché si perde solo una regata che si stava abbandonando; alto solo per la stagione con un amico, dove è una scappatoia.

## Il modello più semplice

Salvare **prima** un risultato provvisorio, poi simulare come oggi.

1. In `torEsci`, prima di `torChiudi`: `progress.torneo.provv = { k, r }` e `saveProgress()` (pochi millisecondi). In `r`: il giocatore ritirato; chi è già arrivato col suo tempo vero; chi naviga ancora in fila dietro, nell'ordine della classifica di quel momento (`ranking()`).
2. Se la simulazione finisce, `torChiudi` mette il risultato vero e cancella `provv`: niente cambia rispetto a oggi.
3. Se è stata interrotta, all'apertura del torneo (`torApri`) il provvisorio diventa il risultato della regata `k`, con le stesse strade di oggi (`stoAgg`, fine del torneo, tappa della stagione).

**Semplificazione dichiarata:** nel caso interrotto l'ordine dei rivali è quello del momento della chiusura, non quello che sarebbe uscito.

## Criteri (soglie nostre, scritte prima)

| # | Cosa | Soglia |
| --- | --- | --- |
| P1 | Simulazione interrotta apposta (si lancia un errore dentro il ciclo di `torChiudi`): il ritiro c'è alla riapertura, un solo risultato per regata | 40 su 40 (4 momenti × 10 tornei), Chromium e Firefox; lo stesso nella quarta/terza regata, dove il torneo si chiude, e in una tappa di stagione |
| P2 | Non interrotta: risultati identici a oggi | 40 su 40 identici al bit, `provv` assente |
| P3 | Chiusura vera della scheda, regate **lunghe**, Firefox, computer scarico | ritiro registrato 20 su 20 (oggi: da misurare prima, sugli stessi 20) |
| P4 | Chi ha già finito la sua regata e chiude: il suo risultato resta quello vero | 20 su 20 |
| P5 | Un salvataggio vecchio senza `provv` si apre; la «forma della stagione» non cambia | 0 errori |

## Costanti nuove

Nessuna.

## Rischi

- Basso: tocca `torEsci`, `torChiudi`, `torApri`. Il rischio vero è il doppio risultato (P1 lo conta).
- Il collaudo C11 resta com'è; con questa modifica il suo rosso in Firefox dovrebbe sparire, e lo si vede nei giri GitHub.

## Cosa serve da Ale

Il via, oppure «lascialo così» come per l'uscita lenta (voce 71).

## Esito (fermata 2, 1.3.53, 24 novembre 2026)

Passano tutti: P1, P2, P4, P5 in Chromium e Firefox. **P3** (Firefox, regate lunghe): prima 0, 4 e 4 su 20 riaprendo dopo 0, 3 e 10 s; dopo **20 su 20** in tutti e tre. La proposta non diceva quando si riapre: le tre attese sono state scelte dopo aver visto lo 0 su 20, e misurate allo stesso modo sul gioco di prima.

Una cosa in più rispetto al modello: il provvisorio si scrive anche in `beforeunload`, perché scritto solo in `pagehide` in Firefox si legge troppo tardi (ancora 0 su 20 riaprendo subito). Aggiunto il criterio P6 (chiusura annullata, allenamento): 10 su 10 e 10 su 10. Al contrario di quanto scritto nei rischi, C11 non è rimasto com'era: ora riapre il torneo prima di leggere. Numeri completi in `CHANGELOG.md` 1.3.53.
