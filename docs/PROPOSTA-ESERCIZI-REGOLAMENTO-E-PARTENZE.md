# Proposta: gli esercizi pratici del gruppo D (regolamento) e del gruppo C (partenze)

1 novembre 2026. **Fermata 1: solo documento, nessun codice nel gioco.** Le lezioni D1-D4 (1.1.9) sono solo teoria, perché un esercizio sulle precedenze ha bisogno di un'altra barca che si muove, e oggi barche che si muovono ci sono solo in regata. Ale ha chiesto perché proprio la regata: questa proposta divide il lavoro in due meccanismi, a seconda di cosa serve all'esercizio.

## 1. Il problema, misurato sul codice

- Una lezione ha una sola barca. Le barche di scena della 1.1.9 (`scena`) sono **ferme**: servono solo per il disegno.
- Linea di partenza, conto alla rovescia, bandiere, boe da girare, giri di penalità e semaforo esistono **solo in regata** (`js/regate.js`: `startRace`, `chiCede`, `semaforo`, `giriPenalita`).
- Il contatto fra gli scafi si calcola già con i contorni veri (`hullOverlap`, 1.0.39) e si può riusare.

## 2. Meccanismo A: una barca di scena che si muove (esercizi D1, D2, D3)

Una o due barche che **vanno dritte a velocità costante**, oppure cambiano rotta in un momento scritto nel passo. Non hanno fisica e non hanno guida: sono un copione. Il giocatore guida la sua barca come in ogni passo pratico. È l'esercizio più semplice che si possa scrivere, e la situazione capita **ogni volta**. In regata, invece, l'incrocio giusto può non capitare mai.

| Lezione | Esercizio (idea) | Il passo vale se |
|---|---|---|
| D1 Mure opposte | Tu di bolina mure a sinistra; una barca mure a dritta arriva su una rotta che ti colpirebbe | nessun contatto, e passi dietro alla sua poppa oppure viri per tempo; distanza minima fra gli scafi almeno **2 m** |
| D2 Stesse mure | Tu sopravento e sovrapposta; la barca sottovento orza piano di 10° in 10 s (lo può fare, ma lasciandoti spazio: regola 16.1) | nessun contatto e distanza minima almeno **2 m** per 20 s |
| D3 Chi vira cede | Una barca mure a dritta ti passa vicino; devi virare | viri **dopo** che è passata: durante la tua virata, dal vento alla bolina, nessuna barca a meno di **10 m** |

- **A mani ferme** ogni copione porta al contatto, quindi il passo non si completa da solo (criterio L3 della scuola: 0 su 10).
- **Costanti nuove, tutte ipotesi nostre:** 2 m di distanza minima, 10 m durante la virata, velocità delle barche di scena 2,2 m/s (circa la bolina della barca dell'1b con 10 nodi, da misurare), orzata di 10° in 10 s.
- **Codice:** un campo del passo (`scenaMobile`), il movimento delle barche nel ciclo delle lezioni, `hullOverlap` per il contatto, il pilota delle lezioni esteso a questi tre passi. Le regate non si toccano.

## 3. Meccanismo B: una lezione che apre una regata (D5, D6, D7, C1, C2)

Qui servono linea, conto alla rovescia, bandiere e boe, quindi la regata vera. Il passo pratico ha un pulsante **«Apri l'esercizio»**. Il pulsante apre una regata in un modo speciale, «esercizio»:
- la regata **non salva niente**: niente record, piazzamenti, meriti né registrazioni;
- in alto c'è l'**obiettivo** del passo;
- appena l'obiettivo è raggiunto, oppure se si sceglie «Torna alla lezione», si torna al passo, che risulta fatto o da rifare.

| Lezione | Regata di partenza | Obiettivo |
|---|---|---|
| D5 I segnali di partenza | bastone, senza avversari, 5 minuti di sequenza | partire senza anticipo: nessuna X dopo il segnale |
| D6 La partenza anticipata | come D5 | partire apposta in anticipo, tornare dietro la linea (29.1) e ripartire |
| D7 Toccare una boa e i giri | «Regata con i giri di penalità», senza avversari | toccare la boa e fare il giro di penalità (31, 44.2), sempre nello stesso verso |
| C1 Partenza in velocità | bastone, senza avversari | tagliare la linea entro **5 s** dal via, a più di **3,5 nodi**, senza anticipo |
| C2 Partenza da fermi | bastone, senza avversari, barca quasi ferma al via | tagliare la linea entro un tempo da fissare con il pilota |

- **Soglie di C1 e C2** (attese nostre, `PROPOSTA-LEZIONI-SCUOLA.md` §4): scelte sui semi 1-20, confermate sui semi 101-120. Per confronto, gli avversari partono con un ritardo mediano di 1-2,3 s a 4,6-4,75 nodi.
- **Codice:** il modo «esercizio» in `startRace` (niente salvataggi), l'obiettivo letto ogni passo di simulazione, il ritorno alla lezione. È il pezzo più grosso, perché tocca il codice delle regate.
- **Non-regressione:** le regate normali devono restare identiche al bit (`arrivi_regate.py`, `impronta1b.js`).

## 4. Criteri (soglie scritte prima, attese nostre)

- **E1:** ogni esercizio si completa guidando col pilota in **almeno 9 semi su 10** e **mai a mani ferme** (0 su 10). Soglie scelte sui semi 1-10, confermate sui semi 11-20.
- **E2:** un pilota che sbaglia apposta non passa: nella D1 tira dritto, nella D3 vira subito, nella D6 non torna dietro la linea. Al più **1 su 10**: è la lezione imparata con la B5.
- **E3:** con il meccanismo B nessun dato salvato cambia. Controllo sul salvataggio prima e dopo un esercizio: identico.
- **E4:** regate normali identiche al bit; fisica identica (`polare.js`, `raffiche_e_virate.js`, `impronta1b.js`).
- **E5:** pannello a 1360×650 senza pixel di eccesso, in Chromium e in Firefox; pagina senza `#collaudo` senza errori.

## 5. Rischi

- **Il copione del meccanismo A è rigido.** La barca di scena non si scansa mai, quindi un contatto è sempre colpa del giocatore. Nelle D1-D3 è giusto, perché il giocatore è quello che deve lasciare strada.
- **Il meccanismo B tocca le regate:** è lì che servono più collaudi. Per questo si fa dopo il meccanismo A.
- **Uscire dalla regata a metà** (menu, chiusura della pagina) non deve contare come ritiro né lasciare tracce nel salvataggio.

## 6. Ordine proposto

1. Meccanismo A ed esercizi D1-D3 (una versione).
2. Meccanismo B ed esercizi D5-D7 (una versione). Le teorie D5-D7 si scrivono insieme.
3. Gruppo C con il meccanismo B (una versione).
4. Esame e glossario; poi il menu nuovo, che toglie le precedenze dalla lezione 3.

## 7. Da decidere (Ale)

1. Va bene dividere così: barca di scena per D1-D3, regata come esercizio per D5-D7 e per il gruppo C?

## 8. Avanzamento

- **Ale, 1 novembre 2026:** via a tutti e due i meccanismi. «La 1 è la simulazione di un evento, un copione»; per la 2, un'idea da verificare (Ale: «era solo un'idea»): usarla anche nella modalità coach, per rivivere un episodio della regata e farlo meglio.
- **1.2.1:** meccanismo B ed esercizi D5-D7 fatti, con lo stato di partenza (regata, avversari, preparazione, o la barca già vicino alla boa) separato dall'obiettivo, come chiesto da Ale. Tutti e tre: guidando 10 su 10 sui semi 1-10 e 11-20, a mani ferme 0 su 10, chi sbaglia apposta 0 su 10; salvataggio identico; regate normali identiche al bit (`CHANGELOG.md`, `collaudo_esercizi_regata.py`). Resta il gruppo C (C1, C2) con lo stesso meccanismo.
- **1.2.0:** meccanismo A ed esercizi D1-D3 fatti. Tutti e tre: guidando 10 su 10 sui semi 1-10 e 11-20, a mani ferme 0 su 10; nella D3, chi vira subito 0 su 10 (`CHANGELOG.md`).
