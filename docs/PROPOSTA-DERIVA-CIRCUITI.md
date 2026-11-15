# Proposta: la cornice di Deriva, coi circuiti (fermata 1)

14 novembre 2026, notte. Tappa 2 di `PIANO-CHIUSURA-DERIVA.md`. Riscrive `PROPOSTA-LIVELLO-DERIVA.md` (4-6 novembre), che era nata prima dei circuiti: quella resta come storia, e da lì si prende tutto ciò che vale ancora. **Solo proposta: in `js/` niente finché Ale non dà il via.**

## Cosa è già deciso

- **6 novembre:** stessa barca; niente esame né attestato; lezioni solo nuove; una prova con medaglie (i giri di penalità); momento clou in Deriva; punti propri, nelle quattro aree; due strade per passare (`IL-GIOCO.md` §3-4).
- **14 novembre, notte:** si supera Deriva con il **diritto al nazionale** (primi 3 dello zonale) o con la **strada del merito**; nazionale e finale sono la carriera dentro Deriva; Deriva **si mostra quando questa cornice è pronta**; gli sponsor solo dopo (tappa 4).

## Cosa c'è dentro

| | Deriva |
| --- | --- |
| **Lezioni** | 21 «Come funziona il torneo» (punti bassi, scarto, penalità sul punteggio, finestra d'arrivo); 22 «Rivedi la tua regata» (tasto O, «Rivedi», regate registrate, rotta ottimale); 23 «La layline» (testo e quiz già scritti, `PROPOSTA-LIVELLO-DERIVA.md`, in fondo) |
| **Prova con medaglie** | i giri di penalità: bolina fino a una boa e ritorno, a tempo, due giri da scontare (§3 della vecchia proposta) |
| **Regate** | quelle di oggi fuori dalla Scuola: salti di vento, giri di penalità, torneo singolo (allenamento, anche a 6 barche) |
| **Carriera** | stagione **zonale** → **nazionale** → **finale** (tappa 3) |
| **Coach** | registratore, moviola e rotta ottimale (ci sono); **momento clou** da fare, con una proposta a sé (`PROPOSTA-COACH-REGISTRATORE.md`, fase 2). Idea da misurare: il minuto in cui il filo della rotta ottimale si allunga di più (voce 32) |
| **Ripassi** | i 3 quiz nuovi; nessun esame |

**Il menu:** due pulsanti in alto, «La scuola» e «Deriva». Nel gioco libero tutto aperto (principio 2). In carriera Deriva si apre con l'attestato, come oggi il torneo; finché la cornice non è finita resta nascosta (decisione 4), come le lezioni con `nascosta: true`.

**Superare Deriva:**
- **piazzamento:** fra i primi 3 di una stagione zonale;
- **merito:** una stagione zonale finita senza ritirarsi da nessuna tappa **e** quasi tutti i punti di Deriva (quota da misurare nella tappa 7, dopo i rivali).

Il gioco lo dice, una volta («Deriva superata»); il Fiocco non c'è ancora, quindi non si apre niente di nuovo. Con la strada del merito Deriva è superata ma il nazionale no: quello si apre solo col diritto.

**Punti di Deriva** (propri, quelli della Scuola non contano):

| Area | Da cosa |
| --- | --- |
| Esperienza | lezioni 21-23 fatte, tappe finite, il momento clou rivisto la prima volta |
| Conoscenza | i 3 quiz |
| Competizione | piazzamenti nelle tappe e nella classifica della stagione |
| Abilità | la prova dei giri, con le medaglie |

Ripetere la stessa cosa senza migliorare non dà punti.

## Versioni (traguardi di `METODO.md` §5)

1. **1.3.0, alfa:** menu a due livelli e voci al loro posto, Deriva ancora nascosta in carriera. Nessun contenuto nuovo.
2. **1.3.1, beta:** lezioni 21-23 con quiz e glossario, prova dei giri con le medaglie.
3. **1.3.2:** momento clou (proposta a sé).
4. **1.3.3:** punti di Deriva, «Deriva superata», libretto; Deriva visibile in carriera.
5. La **quota del merito** si misura nella tappa 7, dopo la tappa 5 (rivali): i rivali spostano i numeri.

## Criteri (soglie nostre; dalla vecchia proposta, rifatti per i circuiti)

| # | Criterio | Soglia |
| --- | --- | --- |
| D1 | Niente cambia sotto | `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; impronta del guardiano identica |
| D2 | Spazio | menu senza eccesso in ogni combinazione di livello, modo e gruppo, a 1360×650 e 1360×768, col libretto al massimo |
| D3 | Tutto al suo posto | ogni voce apre la sua lezione, regata, prova o stagione; nel gioco libero tutto aperto; in carriera Deriva chiusa senza attestato e aperta con; pagina senza `#collaudo` in Chromium e Firefox, 0 errori |
| D4 | La Scuola resta com'è | meriti, esame (34 domande, 28 per passare) e «di 25 completate» identici; le lezioni 21-23 fuori da meriti ed esame della Scuola; `collaudo_carriera_intera.py` verde |
| D5 | Le lezioni | esercizi completati guidando 10 su 10, a mani ferme 0 su 10, semi 1-10, confermati su 11-20 |
| D6 | Superare | primi 3 dello zonale: superata; stagione lasciata o con un ritiro: mai per merito; 4° o peggio solo con la quota del merito (controprove); il risultato resta alla ricarica; un salvataggio della 1.2.39 con lo zonale già fra i primi 3 risulta superato; nel gioco libero non si supera niente |
| D7 | Raggiungibile (tappa 7) | semi mai guardati, stagioni zonali col pilota: fra i primi 3 in una quota da riportare; la soglia D7 si scrive prima di misurarla, dopo la tappa 5 |
| D8 | Niente doppioni | nessuna domanda dei quiz di Deriva uguale a una della Scuola; nessuna voce di glossario ripetuta; i punti della Scuola non cambiano quelli di Deriva e viceversa |
| D9 | La prova | il pilota la completa 10 su 10 coi giri fatti, a mani ferme 0 su 10; un giro non fatto costa 15 s; medaglie scelte su un gruppo di semi e confermate su un altro |
| D10 | Il merito non si compra | ripetere senza migliorare non dà punti; chi ha solo le stagioni senza il resto non passa per merito |

## Costanti nuove (nostre)

Il piazzamento (3°), la quota del merito, i tempi delle medaglie della prova, i punti per area. Si salvano in più i punti di Deriva.

## Fonti

Lezione 21: F15 (appendice A, 44.3), parafrasata. Lezione 23: F77-F78, già nel testo scritto. Lezione 22: solo il gioco, nessuna affermazione nautica.

## Rischi

- **La più grossa del piano:** tocca menu, carriera e salvataggi. Chi ha già una carriera non deve perdere niente (D4, D6).
- **Una stagione è lunga** (16 regate): superare Deriva chiede tempo. Si salva dopo ogni regata.
- **Il merito dipende dai rivali:** la quota si fissa solo dopo la tappa 5.

## Risposte di Ale (15 novembre 2026)

Via dato. Il torneo singolo resta in Deriva come allenamento, fuori dalla carriera. La lezione della layline è la 23. Si parte dalla 1.3.0 (menu a due livelli).

## Cosa serviva da Ale

1. Il via.
2. Va bene che il **torneo singolo** resti in Deriva come allenamento, fuori dalla carriera?
3. La lezione della layline come **23**, dopo le due già previste?

## Esito della 1.3.0 (15 novembre 2026)

Fatta: menu a due livelli nel gioco libero; in carriera niente cambia (costante `DERIVA_IN_CARRIERA`, da accendere con la 1.3.3). Nella vista Deriva, per ora, solo le voci che c'erano già: regate nei salti di vento e con i giri di penalità, torneo (con la stagione). La navigazione libera resta nella Scuola.
- **D1:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.
- **D2 (parte della 1.3.0):** 0 px di eccesso a 1360x650 e 1360x768 in 12 combinazioni (gioco libero; carriera vuota e col libretto pieno; livello salvato Scuola o Deriva), Chromium e Firefox (`collaudo_menu_livelli.py`). Il caso «col libretto al massimo» dentro Deriva in carriera si misura con la 1.3.3.
- **D3 (parte della 1.3.0):** ogni regata si apre cliccando dal menu, il torneo apre il suo riquadro, la navigazione libera parte; il livello scelto resta alla ricarica e tornando da una regata; pagina senza `#collaudo`, 0 errori, in tutti e due i browser. «Deriva chiusa senza attestato e aperta con» si misura con la 1.3.3.
- Da notare: nel gioco libero il pulsante «Deriva» si vede da subito, come chiede questa proposta («Deriva ancora nascosta in carriera»); le voci dentro erano già visibili prima.

## Esito della 1.3.1 (15 novembre 2026)

Fatte le lezioni 21-23 con ripassi, glossario (6 voci) ed esercizi delle lezioni 22 e 23; **la prova dei giri di penalità passa alla 1.3.2**, e le versioni dopo scalano di uno (1.3.3 momento clou, 1.3.4 punti di Deriva, «Deriva superata», Deriva visibile in carriera). Numeri in `CHANGELOG.md` 1.3.1:
- **D4:** esame 34/28 senza domande di Deriva; «di 25 completate»; meriti identici con e senza Deriva (6 salvataggi); `collaudo_carriera_intera.py` verde.
- **D5:** lezione 22 10 su 10 guidando sui semi 1-10, confermato 11-20 e 21-30, 0 a mani ferme. Lezione 23: col primo pilota del collaudo **7 su 10 sui semi 11-20, fuori soglia**, perché a 20 m dalla boa la guida degli avversari virava di nuovo (voce 1b); col pilota corretto 20 su 20 sui semi 1-20 e 10 su 10 sui semi 21-30 mai guardati; 0 a mani ferme. L'esercizio dipende poco dal seme (vento costante, nessun avversario).
- **D8:** 13 domande di Deriva, nessuna uguale alle 167 della Scuola; glossario senza termini ripetuti.

## Esito della 1.3.2 (15 novembre 2026)

Fatta la prova 6, «I giri di penalità»: al via due giri dovuti, contati con le stesse regole delle regate; bolina fino alla boa a 170 m e ritorno; 15 s per ogni giro non fatto.
- **D9:** col pilota 10 su 10 con i giri fatti, a mani ferme 0 su 10, +15 s a giro non fatto (`collaudo_prova_giri.py`). Medaglie **240/300/385 s** con la regola di `PROPOSTA-MEDAGLIE-E-NOMI.md` sui semi 1-30; confermate sui semi 101-130 (30 su 30 entro l'oro col pilota preciso, 30 su 30 entro il bronzo e 0 ori col pilota con errori, Chromium e Firefox).
- Da sapere: saltare i due giri costa 30 s ma ne fa risparmiare circa 18: conviene farli, ma senza giri si prende ancora l'argento.
