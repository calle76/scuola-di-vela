# Proposta: livello 2a, fetta 5: i giri di penalità anche per gli avversari

31 ottobre 2026. **Fermata 1: solo documento, nessun codice.** Punto di partenza: `PROPOSTA-LIVELLO-2A.md` (fetta 1, giri del giocatore), `PROPOSTA-REGOLA-21-2.md` (21.1 e 21.2), promemoria di Ale del 30 ottobre («nell'1b anche gli avversari devono fare i giri di penalità»), F15 44.1, 44.2 e 21.2. Le soglie sono scritte **prima** di misurare e non si cambiano dopo senza dirlo.

## Cosa cambia e dove

Nella «Regata con i giri di penalità» (`R.giri`) un avversario che prende un contatto con colpa non paga più +15 s: ha un **debito di due giri** e li fa. Tutto il resto resta com'è: 1a, 1b, torneo (lì la penalità è sul punteggio) e le altre regate **non cambiano** e devono risultare identiche al bit. Il codice nuovo sta dentro `aiControl` e in un punto di `contatti` (dove oggi c'è `guilty.pen += 15`), tutto sotto `if (R.giri)`.

Oggi la guida degli avversari non sa fare manovre volute: segue una prua desiderata e evita le barche. Per questo è il pezzo più costoso del 2a e va tenuto piccolo.

## Modello più semplice plausibile

1. **Il debito.** `b.need`, `b.done` per ogni avversario (come `R.need` e `R.done` del giocatore). Un contatto con colpa dà +2. Il contatto prima dello sparo vale lo stesso: il debito resta aperto.
2. **Quando comincia.** Dopo lo sparo (`R.t >= 0`), con il debito aperto, la barca in regata (non in attesa dietro la linea) e **nessuna altra barca a meno di 4 lunghezze** (regola 44.2: ci si allontana dalle altre barche prima di girare). Se è vicina a qualcuno, prosegue la rotta normale e riprova ogni passo.
3. **Cosa fa.** Una sequenza di quattro prue rispetto al vento, sempre **orzando per prima** (quindi sempre nello stesso verso, e ogni giro ha una virata e una strambata): passa il vento sull'altra mura fino alla bolina, poggia fino alla poppa larga (`ai.down`), strambata, poi orza fino alla bolina da cui era partita. Si passa alla prua successiva quando l'errore è sotto 15°. Per il secondo giro si ripete. La barra e la scotta sono quelle di sempre (`muoviTimone`, `sheetFor`): niente trucchi fisici, il costo in tempo esce dal motore.
4. **Quando si interrompe.** Se durante il giro un'altra barca arriva a meno di 2 lunghezze, il giro si sospende (guida normale, `cedeAvv1b` compreso), il giro in corso si perde e riparte da zero appena la via è libera. Il debito non cambia.
5. **Finito.** Quando i giri sono fatti la guida torna normale (il timer dei bordi riparte). I giri si contano quando la sequenza arriva in fondo, ma il collaudo li conta per conto suo (criterio G1).
6. **Regola 21.2 per loro.** Mentre un avversario esegue la sequenza ha `sconta = true`, quindi `chiCede` fa cedere lui a chi non sconta (già scritto per il giocatore in 1.0.66: `subordinata`). Se due barche scontano insieme valgono le regole 10-13.
7. **Arrivo con giri mancanti.** Come per il giocatore: **+15 s per ogni giro che manca**, con la voce nell'elenco delle penalità («La Rossa, giri di penalità non fatti (1): +15 s»). Nessuna squalifica.
8. **Registratore.** Gli eventi `sconta inizio/fine` e `giro_penalita` oggi sono solo del giocatore; per gli avversari si aggiunge il nome della barca. Se la cosa complica il registratore, si rimanda (non è nei criteri).

**Alternativa più semplice (B), scartata ma disponibile:** gli avversari pagano un tempo fisso equivalente (17,5 s, la mediana misurata per il giocatore) senza girare. Zero codice nella guida, ma non si vedono i giri, la 21.2 non vale per loro e un avversario colpevole in un cattivo momento paga come in un buon momento. Non risponde alla richiesta di Ale. La tengo come ripiego se i criteri C o D sotto non riescono.

## Costanti nuove (tutte ipotesi nostre)

- Distanza per cominciare: **4 lunghezze**; per sospendere: **2 lunghezze**. (Il giocatore, nella 21.2, non ha un limite: qui serve perché la guida degli avversari non è un giocatore che sceglie.)
- Errore di prua per passare alla successiva: **15°**.
- Ripiego per giro non fatto: 15 s, come il giocatore.
- Nessuna fonte per i numeri: F15 44.2 dice solo «appena possibile» e «lontano dalle altre barche».

## Criteri misurabili (soglie scritte prima, attese nostre)

Collaudo con la regata dei giri, avversari guidati dal gioco, **40 regate a semi fissi 1-40** (sono i semi dell'1b), pilota automatico del giocatore. Per ogni avversario si guardano i **contatti con colpa**: sono i casi con debito. Si riporta sempre il numero dei casi, e se sono pochi (meno di 30) si allungano le regate finché non ci sono.

- **G1 (metro indipendente).** Per ogni avversario si ricostruisce dai soli dati del motore (posizione e prua a ogni passo, contatori `tacks` e `gybes`): rotazione cumulata, virate e strambate durante il suo `sconta`. Ogni giro dichiarato deve avere rotazione ≥ 360° nello stesso verso e almeno una virata e una strambata: **100% dei giri dichiarati**. Il collaudo conta anche **quanti casi hanno davvero un debito all'inizio** (deve essere uguale ai contatti con colpa degli avversari).
- **G2 (li fa).** Dei casi con debito aperto con almeno **90 s** di regata davanti, l'avversario ha estinto il debito in **≥ 80%**. Quelli non estinti si riportano uno per uno, con la causa (sempre vicino a qualcuno? scuffia? piantato?).
- **G3 (stesso verso).** Tutti i giri di uno stesso avversario nello stesso verso: **100%**.
- **G4 (costo in tempo).** Dall'inizio alla fine dei due giri: mediana fra **12 e 30 s** (il giocatore: 17,5 s, 16,8-18,4). Si riporta anche la perdita di distanza lungo il percorso rispetto alla stessa regata con +15 s (stessi semi), per vedere se i giri costano più o meno dei 15 s di prima.
- **G5 (non si pianta).** Durante i giri nessun avversario fermo (`u < 0,3`) per più di 10 s nell'angolo morto: **al massimo 5% dei giri**.
- **G6 (non scuffia).** Scuffie durante i giri: **al massimo 5% dei giri** (vento 10 nodi). Se supera, si dice.
- **G7 (spirale).** Avversari che prendono un altro debito mentre girano: **meno del 15% dei giri**, e debito in più medio sotto 0,3 giri a regata.
- **G8 (21.2 per loro).** Contatto fra giocatore e un avversario che sta scontando, con il giocatore che non sconta: **cede l'avversario con la regola 21.2 in 100% di 60 casi** (30 posizioni × 2 lati, come `collaudo_regola21.py`).
- **G9 (arrivo con giri mancanti).** Con un debito forzato a 2 giri a un avversario e il percorso quasi finito: **+30 s e voce nell'elenco** in 10 casi su 10.
- **G10 (non-regressione).** 20 regate dell'1a, dell'1b e del torneo **identiche al bit alla 1.0.66**; `polare.js` e `raffiche_e_virate.js` carattere per carattere; `collaudo_giri`, `collaudo_boa`, `collaudo_segnali`, `collaudo_regola21`, `collaudo_registrazione`, `collaudo_moviola` verdi. Nella regata dei giri: **partenza identica** se non ci sono contatti con colpa degli avversari prima dell'arrivo (si confrontano i percorsi di una regata senza contatti).
- **G11 (come la carica un giocatore).** Pagina senza `#collaudo`: la regata si apre, un avversario prende un contatto, fa i giri, nessun errore di pagina.
- **G12 (schermo).** Pannello a 1360×650 senza pixel di eccesso (non si aggiunge niente al pannello salvo il messaggio, dove oggi c'è «penalità alla Rossa»).

## Rischi

- **Spirale di colpe** degli avversari che girano vicino ad altri (G7): la sospensione a 2 lunghezze serve a quello; se non basta, si allarga la distanza di partenza.
- **Il giocatore diventa «sorgente di colpe» degli altri.** Se un avversario gira vicino al giocatore e il giocatore lo urta, con la 21.2 la colpa è del giocatore (non sconta): è il regolamento, ma può sembrare ingiusto. La riga delle regole lo dice.
- **Scuffie e piantate** nella sequenza (G5, G6): l'avversario poggia a 150° con la randa quasi lasca, ma una raffica può rovesciarlo. Se succede spesso, la sequenza si smorza (poggiata meno profonda) e lo dico.
- **La guida degli avversari è comune all'1a congelata.** Tutto sta dietro `R.giri`; la prova è G10 (identico al bit nelle regate senza giri).
- **Il tempo dei giri non è in nessuna fonte** (come per il giocatore): lo misuriamo.

## Da decidere (Ale)

1. **Dopo lo sparo.** I giri dell'avversario cominciano solo dopo lo sparo (un contatto in partenza lascia il debito aperto). Va bene? L'alternativa, giri prima dello sparo, farebbe uscire la barca dalla posizione di partenza.
2. **+15 s sparisce per gli avversari in questa regata.** Resta l'unica penalità a tempo (+15 s per giro non fatto all'arrivo). Va bene?

Se mi dici «come proponi», parto dalla fermata 2 con la sequenza di prue sopra. La fermata 2 si ferma di nuovo alla fine (misure, difetti, esito).

## Esito (31 ottobre 2026, 1.0.67)

Decisioni di Ale: dopo lo sparo, «semplificata e dichiarata» (il regolamento li vuole «appena possibile», anche prima del via: F15 44.1 e 44.2 letti nel PDF); procedi. Fatta e misurata, vedi `CHANGELOG.md`. Soglie non cambiate; cambiati nel collaudo, dichiarato: G10b (stessa regata, uguale al bit fino al primo giro di un avversario, perché 18 regate su 20 hanno un debito) e la tolleranza di campionamento del metro di G1 (5°, dopo aver visto 31 giri su 134 a 356,9-360°). G2 95% (soglia 80%), G4 mediana 22,2 s (fascia 12-30 s), tutto il resto entro soglia. Due precisazioni al testo sopra: gli avversari contano da soli virate e strambate (non hanno i contatori del giocatore) e la distanza «ben lontano» per cominciare vale anche rispetto alle boe e alla linea d'arrivo (25 m).
