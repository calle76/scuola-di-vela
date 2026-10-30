# Proposta: livello 2a, il regolamento (prima fetta: i giri di penalità)

30 ottobre 2026. Per decisione di Ale (30 ottobre, «procedi in autonomia, senza fermate») la proposta e l'implementazione vanno di seguito; le soglie sono scritte **prima** di misurare e non si cambiano dopo senza dirlo. Punto di partenza: `REGOLE-DI-REGATA.md` (confronto con F15, le RRS 2025-2028), `VISIONE-LIVELLI-E-CARRIERA.md` §2 e §3, `ROADMAP.md`. Gli avversari dell'1b restano come sono (`DECISIONI.md`, 30 ottobre): niente correzioni alla loro guida.

## Cosa contiene il 2a (visione) e in che ordine lo faccio

Il 2a è grande: bandiere e segnali, tecnica di partenza, precedenze 14-17, 21, 23, il giallo del semaforo, spazio alla boa (18), penalità a giri, «il gioco come arbitro», lezioni, regate di prova. Lo divido in fette, ognuna con i suoi collaudi e un commit a sé, dal valore più alto al più basso (ordine di `REGOLE-DI-REGATA.md`):

1. **Giri di penalità al posto dei 15 secondi** (RRS 44.1, 44.2): questa proposta, prima per il giocatore.
2. Un giro per la boa toccata (31, 44.1): richiede boe che si toccano.
3. Regole 11, 12, 13 nella colpa dei contatti (sovrapposizione, chi è libero dietro, chi sta virando).
4. Procedura di partenza 5-4-1-0 con le bandiere (26) e bandiera X (29.1).
5. Dopo: 21.2 (chi sconta lascia strada), 18, 30, 14; poi le lezioni del 2a.

## Fetta 1: i giri di penalità

**Cosa dice la regola (parafrasi, F15):** chi può aver violato una regola della parte 2 sconta **due giri** (44.1); i giri si fanno **appena possibile** dopo essersi allontanati dalle altre barche, **nello stesso verso**, e **ogni giro comprende una virata e una strambata** (44.2). Se si arriva senza averli fatti, nella realtà si rischia protesta e squalifica.

**Dove entra nel gioco.** Una regata nuova in fondo a `RACES`: «Regata con i giri di penalità» (barca dell'1b, tre avversari, vento 10 nodi, flag `giri: true`). In fondo alla lista, come le altre dell'1b, quindi gli indici di record e di carriera non cambiano; non conta per meriti e carriera (come «Regata nei salti di vento»). **Le regate esistenti non cambiano.**

**Modello più semplice plausibile.**
- **Il giocatore.** Un contatto con colpa (come oggi, `chiCede`) non dà più +15 s: dà un **debito di due giri** (`R.need += 2`). Un giro è fatto quando la prua ha ruotato di almeno **360° nello stesso verso** e nel frattempo ci sono state **almeno una virata e una strambata** (i contatori `S.tacks` e `S.gybesC + S.gybesV` che il gioco ha già). Il verso del secondo giro deve essere lo stesso del primo; se è opposto, il primo non conta più. Se la rotazione inverte il verso di più di 20° (oltre il disturbo delle onde) la finestra riparte da zero. Una scuffia azzera la finestra.
- **Il segnale a schermo.** La riga delle regole nel pannello (`rRule`, nessun pixel in più) dice «Penalità: due giri (…)»; quando ne è fatto uno, «ne manca uno»; finiti, «Penalità scontata».
- **Se si arriva con giri non fatti.** Ripiego **dichiarato**, più semplice della squalifica: **+15 s per ogni giro che manca**, con la voce nell'elenco della penalità («Tu, giri di penalità non fatti: …»). Non c'è la squalifica.
- **Gli avversari.** In questa fetta **continuano a prendere +15 s** (la manovra «girare due volte» nella loro guida è il pezzo più costoso e la guida non si tocca ora). Differenza dichiarata: un avversario colpevole paga 15 s, il giocatore due giri. Il costo dei due giri del giocatore si misura (criterio 4) e, se è molto diverso da 15 s, si valuta di dare agli avversari un tempo equivalente: **decisione rimandata a dopo la misura**.
- **Aiuto per chi comincia (principio 3):** in questa fetta non c'è l'interruttore (il dialogo delle impostazioni non ha un pixel libero); la regata dei giri è una regata a parte, e chi non la vuole non la gioca. Da rivedere se i giri diventano la regola di tutte le regate del 2.

**Fonti.** F15 44.1, 44.2 (testo letto in `fonti-pdf/RRS-2025-2028-World-Sailing.pdf`, parafrasato). Il tempo che costano i due giri **non** è in nessuna fonte: lo misuriamo noi.

**Costanti nuove, tutte ipotesi nostre:** giro = 360° (dal regolamento, uno o più giri completi ma solo il numero di rotazioni); isteresi del verso 20° (disturbo delle onde: ±3-6° a colpi); ripiego 15 s per giro mancante (continuità con oggi).

## Criteri misurabili (soglie scritte prima di misurare)

Pilota di prova che esegue le manovre al comando, a passi fissi con semi fissi (30 prove per caso, il numero dei casi si riporta sempre):

1. **Due giri dello stesso verso con virata e strambata ciascuno estinguono il debito** in 30 prove su 30, in entrambi i versi (15 + 15).
2. **Un giro solo non estingue il debito** (30 su 30 rimangono a debito di uno).
3. **Un giro a destra e uno a sinistra non estinguono il debito** (30 su 30).
4. **Una rotazione di 360° senza virata e senza strambata** (per esempio un testacoda con la vela lasca, se esiste) **non vale come giro** (30 su 30, o `0 casi possibili` e lo si dice).
5. **Il metro non dipende da ciò che misura:** nel collaudo si conta anche quanti casi hanno davvero un debito all'inizio (devono essere 30 su 30).
6. **Costo dei due giri in tempo:** si riporta la mediana in secondi e il minimo-massimo su 30 prove a 10 nodi. Nessuna soglia: è l'informazione che serve a decidere sul +15 s degli avversari. Atteso (stima, `REGOLE-DI-REGATA.md`): 15-25 s.
7. **Non-regressione.** 1a e 1b identiche al bit: arrivi e penalità di 20 regate (1a: regate 1 e 2, 1b: regata 3 e torneo) uguali a quelle della 1.0.60; `polare.js`, `raffiche_e_virate.js` invariati; prove 1-3.
8. **Registratore** (1.0.60): il debito e i giri compaiono nel file (righe `Q` e un evento `giro_penalita`), e la registrazione continua a passare i suoi 25 controlli.
9. **Regata in una pagina caricata come un giocatore** (senza `#collaudo`): si apre dal menu, un contatto con colpa dà il debito e il messaggio, nessun errore di pagina.
10. **Pannello a 1360×650** senza pixel di eccesso.

## Rischi

- Il riconoscimento del giro può sbagliare con manovre atipiche (girata lenta con la barca quasi ferma, scuffia). Per questo il criterio 4 e la finestra che riparte.
- Un giocatore che non sa fare i giri paga di più (15 s per giro mancante) che con la penalità a tempo di prima: è voluto, ma da guardare giocando.
- Gli avversari con +15 s e il giocatore con due giri non sono confrontabili finché non si decide l'equivalente.
- Il record della nuova regata è a sé (non confrontabile con le altre).

## Esito della fetta 1 (30 ottobre 2026, 1.0.61)

Fatta e misurata: vedi `CHANGELOG.md`. Cambiamenti rispetto a questa proposta, dichiarati: i criteri 1-3 e 6 sono misurati senza avversari; il criterio 4 ha 0 casi possibili; aggiunto il criterio K (nessun giro riconosciuto dopo il debito) e poi corretto perché contava giri veri fatti prima; D misura gli incrementi. Costo dei due giri: mediana 17,5 s (16,8-18,4). Le soglie non sono state cambiate.

## Cosa non c'è in questa fetta

Giri degli avversari, un giro per la boa toccata, regola 21.2, bandiere, lezioni, interruttore a tempo per chi comincia.
