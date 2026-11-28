# Proposta: regola 21.2, chi sconta una penalità lascia strada (livello 2a, fetta 4)

31 ottobre 2026, **fermata 1: nessun codice**. Continua `PROPOSTA-LIVELLO-2A.md` (fetta 1 giri di penalità, 1.0.61). Come le fette 1-3 vale **solo nella «Regata con i giri di penalità»** (`R.giri`): le altre regate non cambiano.

## La regola (F15, RRS 2025-2028, testo letto in `fonti-pdf/RRS-2025-2028-World-Sailing.pdf`, parafrasato)

- **21.2:** una barca che sta scontando una penalità lascia strada a una che non la sta scontando.
- Nella Sezione D, **quando fra due barche vale la 21, le regole della Sezione A (10, 11, 12, 13) non valgono**. Quindi una barca che sconta non ha più alcun diritto di precedenza, nemmeno con le mure a dritta.
- Se la barca che sconta tocca un'altra barca, ha violato la 21.2: nuova penalità (due giri, 44.1), senza esonero. È proprio il motivo per cui il regolamento dice di fare i giri «appena possibile, dopo essersi allontanata dalle altre» (44.2).
- 21.1 (chi torna dopo una partenza anticipata lascia strada) e 21.3 (barca che va indietro con la vela a collo) non fanno parte di questa fetta: vedi «Da decidere».

## Oggi nel gioco

`chiCede(A, B)` (`js/regate.js`) decide chi cede con le regole 10, 11, 12, 13. Il giocatore che sconta due giri è una barca come le altre: se passa mure a dritta, ha la precedenza anche mentre gira. Nella 1.0.61 avevo già visto che il pilota prende colpe nei primi 25-30 s di regata e ancora durante i giri.

## Modello più semplice plausibile

1. **Quando si «sta scontando».** Solo per il giocatore (gli avversari non fanno giri). Con un debito aperto (`R.need > R.done`) non basta avere il debito: finché non inizi i giri sei una barca normale (è il «appena possibile»). Si comincia a scontare quando **negli ultimi 20 s la prua ha già ruotato di almeno 120° nello stesso verso** (più di una virata normale, che sono circa 90°). Si continua finché il debito non è estinto o finché passano 20 s senza completare un giro (stessa finestra dei giri della 1.0.61, che riparte a ogni giro fatto). Se si smette di girare, si torna barca normale e il debito resta.
2. **Chi cede.** In `chiCede`, se una sola delle due barche sta scontando, cede quella: `{ cede: la barca che sconta, regola: 21 }`, prima delle regole 10-13 (la Sezione A non vale). Se nessuna o entrambe, tutto come oggi.
3. **Gli avversari non cambiano la guida:** chi ha la precedenza «tiene la rotta» come nella 1.0.49 e non evita il giocatore che gira. È il comportamento che già hanno con qualunque altra barca che deve cedere; qui però pesa di più, perché il giocatore può prendere altri due giri nel mezzo dei suoi giri. È il punto più delicato (vedi rischi).
4. **Il messaggio** del contatto dice «regola 21.2: stavi scontando una penalità e dovevi lasciare strada a chi non la scontava». **Il semaforo rosso/verde** (se acceso) diventa rosso per il giocatore che sconta con un'altra barca vicina, perché usa già `chiCede`.
5. **Registratore:** nell'evento del contatto compare «21» come regola; un evento `sconta` (inizio e fine) a ogni cambio di stato.

## Costanti nuove (tutte ipotesi nostre)

- **GIRO_INIZIO = 120°** di rotazione in 20 s per iniziare a scontare. Scelta fra una virata (90°) e un giro intero (360°); non c'è una fonte, perché il regolamento dice solo «quando comincia a scontare la penalità».
- Il tempo di 20 s e il resto sono quelli della fetta 1.

## Criteri (soglie scritte prima, semi fissi, numero di prove sempre dichiarato)

1. **K1 la precedenza passa.** Giocatore che sta scontando e un avversario messo a 3 m, in 30 posizioni diverse (mure, affiancamento e dietro-davanti, sia con mure a dritta sia a sinistra, entrambi i lati): `chiCede` dà sempre `cede` = il giocatore con regola 21: 30 su 30; in almeno 10 di queste, le regole 10-13 avrebbero fatto cedere l'altro (si misura il caso, perché è quello che cambia).
2. **K2 senza giri, nessun cambiamento.** Giocatore con debito aperto ma che non gira (meno di 120° in 20 s): `chiCede` identico a quello senza debito, nelle stesse 30 posizioni: 30 su 30.
3. **K3 debito estinto: si torna a 10-13**, nelle stesse posizioni: 30 su 30.
4. **K4 contatto mentre sconta:** contatto vero con un avversario mentre il giocatore gira: debito +2, motivo «regola 21» nell'elenco e nel pannello: 10 casi su 10.
5. **K5 il metro:** si conta in quante prove il giocatore stava davvero scontando al momento del confronto (devono essere 30 su 30; altrimenti la prova non vale).
6. **K6 quanto pesa (nessuna soglia, solo riportato):** 30 regate con la flotta, debito di due giri aperto a 25 s, giocatore che fa i giri subito con il timone a mano come nella 1.0.61. Si riporta: in quante regate i giri riescono; quanti contatti con colpa prende durante i giri; quanto debito in più. Atteso, stima nostra: debito estinto in almeno 24 regate su 30 e meno di 0,5 giri di debito in più in media. Fuori da questa fascia si riporta com'è e si discute.
7. **K7 non-regressione:** 20 regate 1a/1b identiche al bit alla 1.0.65; schermata a −30 s identica; `polare.js`, `raffiche_e_virate.js`; `collaudo_giri.py`, `collaudo_boa.py`, `collaudo_segnali.py`; registratore e moviola.
8. **K8** pagina senza `#collaudo`: la regata si apre e un contatto con la regola 21 mostra il testo; pannello a 1360×650 senza pixel in più.

## Rischi

- **Spirale di colpe.** Chi gira vicino ad altre barche prende altri due giri a ogni urto. È il regolamento vero (ci si allontana prima), ma in un gioco con avversari che non evitano può diventare frustrante. Rimedi possibili, da non fare ora: far evitare agli avversari la barca che gira; un avviso quando le barche sono vicine («allontanati prima di girare»).
- **Riconoscimento:** una virata con una poggiata lunga può superare 120° senza essere un giro di penalità: in quel caso il giocatore cede senza saperlo. La riga delle regole dice «stai scontando una penalità» quando scatta.
- **Gli avversari ancora a +15 s:** niente giri per loro, quindi la 21.2 vale solo per il giocatore.

## Da decidere (Ale)

1. **21.1** (chi torna dietro la linea dopo un via anticipato lascia strada, anche ai compagni): va dentro questa fetta o dopo? Ha senso farla insieme, perché si usa lo stesso punto di `chiCede`. Tocca anche gli avversari che tornano (loro sì: qui `b.ocs` c'è già).
2. **120°** come soglia: va bene, o preferisci un giro intero (360°, il giocatore cede solo dopo aver fatto il primo)?

## Esito (31 ottobre 2026, 1.0.66)

Decisioni di Ale: 21.1 insieme, 120°. Fatta e misurata, vedi `CHANGELOG.md`. Soglie non cambiate; K6: 30 su 30 estinti, 0,47 giri in più (atteso meno di 0,5: appena dentro). Due difetti del mio collaudo corretti prima dell'esito.

## Dopo il 2a: rimettere a posto il gioco (promemoria di Ale, 31 ottobre 2026)

Ale: «di congelato c'è poco; finite le aggiunte e le correzioni il gioco va rimesso a posto». Elenco di partenza, da rivedere a fine 2a (non ora):
- decidere se le regole del 2a (giri, boa toccata, boe ostacolo, bandiere, 21.2) diventano di **tutte** le regate dell'1b, e togliere la regata «dei giri» a parte;
- rigenerare le **impronte** (`impronta1b.js`, scene in `collaudo_impronta.py`) e i riferimenti sul PC di Ale, e riscrivere cosa significa «congelato»;
- **pulizia del codice**: `js/regate.js` è cresciuto (giri, boe, bandiere, ostacoli); aggiornare la mappa a intestazioni, togliere duplicati, controllare i commenti;
- aggiornare `STATO.md`, `PROGETTO.md`, `ROADMAP.md`, `DECISIONI.md`, `COLLAUDI.md`, il manuale;
- **giro completo** `tests/lancia_tutti.sh` (circa un'ora e mezza) e **revisione con Opus** delle differenze dalla 1.0.60;
- poi la riorganizzazione in «La scuola» e «Deriva» (`PROPOSTA-RIORGANIZZAZIONE.md`).
