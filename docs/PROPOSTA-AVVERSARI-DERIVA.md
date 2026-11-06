# Proposta: avversari meno confusi, per il livello Deriva

6 novembre 2026, sulla 1.2.14. **Fermata 1: solo questo documento, nessuna riga nel gioco.** Nasce dalla regata giocata da Ale (`OSSERVAZIONI-GIOCANDO.md`, 80-85) e dalla sua decisione: in Deriva gli avversari sono da migliorare (`DECISIONI.md`, 6 novembre). Va fatta prima di misurare la soglia del torneo, perché ne sposta i numeri.

## 1. In breve

Oggi più di metà delle penalità nasce **prima del via**, più di una barca su quattro esce dalla linea, e chi cede spesso non si scosta abbastanza. Propongo cinque correzioni piccole alla guida degli avversari, una alla volta, ciascuna misurata. La barca e il modo di decidere chi ha torto (`chiCede`) non cambiano.

## 2. Da dove si parte: i numeri di oggi

`tests/misura_avversari.py`, semi 41-60, in Chromium, 20 regate per ogni riga, 60 avversari per riga. La barca del giocatore la guida il pilota, che usa la guida degli avversari: non guida come una persona.

| Regata, avversari | Penalità | di cui prima del via | Fuori linea al via | Piantate | Boe sbagliate | Arrivo mediano |
| --- | --- | --- | --- | --- | --- | --- |
| Bastone, principianti | 73 | 45 | 13 | 2 | 0 | 213,5 s |
| Bastone, esperti | 65 | 32 | 16 | 3 | 2 | 212,0 s |
| Salti di vento, principianti | 63 | 37 | 17 | 2 | 1 | 413,5 s |
| Salti di vento, esperti | 69 | 38 | 19 | 1 | 0 | 404,5 s |
| **Totale** | **270** | **152 (56%)** | **65 su 240 (27%)** | **8** | **3** | |

Nessuna barca resta senza arrivare. **Questa misura non conta ancora** gli scarti verso la bolina (osservazione 80), chi urta mentre cede (81) e le strambate ravvicinate (85): i contatori si aggiungono prima di toccare la guida.

## 3. Cosa si è visto e la causa probabile

Le cause sono **lette nel codice, non provate**. Ogni correzione parte verificando che il caso si riproduca. La regata di Ale è una sola, e le sue penalità sono nella norma: il problema è come si comportano, più di quante volte urtano.

| # | Cosa si è visto | Causa probabile (`js/regate.js`) |
| --- | --- | --- |
| 80 | Chi ha la precedenza, in poppa, scarta all'ultimo tornando di bolina | `cedeAvv1b`: se lo scarto calcolato non è valido, l'ultima riga manda sempre la barca di bolina, `twd - side * (ai.up - 2)`. In poppa è un giro di oltre 100° |
| 81 | Chi cede dichiara di cedere ma urta lo stesso | L'angolo di scarto è fisso (28°) e nessuno controlla se la nuova rotta evita davvero l'altra barca |
| 82 | Due barche si vengono incontro e nessuna scarta | Si guarda solo la barca col contatto più vicino nel tempo; le altre non esistono |
| 83 | Al via corrono lungo la linea e due escono oltre lo spillo | Cedendo poggiano senza guardare dove finisce la linea (ipotesi, da provare) |
| 84 | Contatti prima del via | In attesa (`hold`) la barca non cede affatto: riga 318. Il contatto a -170 s resta da capire |
| 85 | Due strambate in 3 s, tornando alla stessa rotta | Non cercata |

## 4. Il modello più semplice

Tutto dentro la guida degli avversari. Una fetta alla volta, nell'ordine di quanto pesa, con misura e commit a ogni fetta.

- **Fetta 1, prima del via (84).** Una barca in attesa cede anche lei, se chi si avvicina arriva a meno di due lunghezze. È la fetta che pesa di più: il 56% delle penalità.
- **Fetta 2, cedere davvero (81, 82).** Chi deve cedere prova scarti crescenti, **15°, 28°, 45°, 60°**, e prende il più piccolo con cui, prevedendo le rotte, passa a più di due lunghezze da **tutte** le barche vicine. Se nessuno basta, prende quello che passa più lontano.
- **Fetta 3, niente ritorno di bolina (80).** Chi ha la precedenza, all'ultimo momento, si scosta di poco rispetto alla rotta che ha: non torna mai di bolina se sta scendendo, e non passa oltre il vento.
- **Fetta 4, la linea (83).** Prima e subito dopo il via, uno scarto che porterebbe oltre lo spillo non si sceglie: se serve, si cede dall'altra parte o si rallenta.
- **Fetta 5, strambate (85).** Prima si cerca la causa. Solo se serve: dopo una strambata si resta sulle stesse mure almeno 10 s, salvo per cedere o per girare una boa.

**Fuori da questa proposta:** avversari più bravi a regatare, regola 18 alle boe, i casi in cui `chiCede` decide male, il pilota.

## 5. Criteri (soglie nostre, scritte prima di misurare)

Stessa tabella del §2, Chromium e Firefox. Le soglie si controllano sui semi 41-60, poi si **confermano sui semi 301-320, mai guardati**.

- **V1, penalità:** da 270 ad al massimo 190 (-30%).
- **V2, prima del via:** da 152 ad al massimo 90 (-40%).
- **V3, fuori linea:** da 65 su 240 (27%) ad al massimo 36 (15%).
- **V4, ritorni di bolina:** barche in poppa, con la precedenza, che tornano a meno di 60° dal vento per evitare un'altra barca: 0. Il contatore deve trovarne almeno uno sulla 1.2.14, se no non misura niente.
- **V5, chi urta mentre cede:** contatti di chi cedeva da almeno 3 s: almeno -50% rispetto alla 1.2.14 (numero di partenza da misurare col contatore nuovo).
- **V6, strambate ravvicinate:** due in meno di 5 s: almeno -50%, stessa cosa.
- **V7, non peggiorare:** non arrivate 0; piantate al massimo 12 (oggi 8); boe sbagliate al massimo 5 (oggi 3); arrivo mediano al massimo +5%; `collaudo_avversari1b.py` non peggiore di oggi.
- **V8, i casi di Ale:** una situazione costruita per ciascuna delle osservazioni 80, 81, 82 e 83, 10 varianti, va bene in almeno 9 su 10. Se va bene anche sulla 1.2.14, non distingue e si riscrive.
- **V9, barca invariata:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici. Cambiano invece le regate fotografate da `collaudo_impronta.py`: si dichiara e si rifà il riferimento.
- **Da riportare, senza soglia:** il torneo col pilota (piazzamenti e penalità, confronto con il §2 di `PROPOSTA-LIVELLO-DERIVA.md`), perché serve a scegliere la soglia.
- **Il giudizio vero è di Ale:** una regata giocata che non sembri più confusa. Questo non lo misura nessun numero.

Un numero fuori soglia si riporta com'è.

## 6. Costanti nuove (tutte ipotesi nostre)

Gli scarti di 15°, 45° e 60° (il 28° c'è già); il limite di 60° dal vento in V4; i 10 s fra due strambate, solo se servono. Le due lunghezze ci sono già.

## 7. Fonti

Le regole di riferimento sono la 14 e la 16 (F15), già usate dal codice. Le scelte di guida sono del gioco: nessuna affermazione nautica nuova, nessun testo da cambiare.

## 8. Rischi

- **Avversari che si evitano troppo:** rallentano e arrivano lontani, e il giocatore vince più facilmente. V7 lo controlla in parte; il torneo col pilota lo mostra.
- **Il pilota usa la stessa guida:** i suoi numeri cambiano insieme agli avversari. Il criterio C1 di `collaudo_competizione.py`, le penalità del torneo e l'esploratore vanno riletti.
- **Le simulazioni della partenza** usano la stessa guida: se divergono, gli avversari sbagliano il tempo del via. Va controllato a ogni fetta con `collaudo_partenze.py`.
- **Sulla stessa regata le fette si disturbano:** per questo una alla volta, e se una non porta niente si toglie.
- **Regate della Scuola:** la guida è una sola. Vedi §9.

## 9. Dove si lavora, e la domanda per Ale

Si lavora sul ramo `deriva`, in una cartella separata: la cartella di Ale, `main` e il gioco online non cambiano.

**Una domanda, da decidere prima di portare il lavoro su `main`:** la guida nuova vale anche per le regate della Scuola? **Consiglio di sì.** Avversari diversi fra i due livelli confonderebbero chi gioca e raddoppierebbero il codice. In cambio i punti di Competizione nella Scuola possono cambiare un poco: si misurano e si riportano prima.
