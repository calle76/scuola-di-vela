# Documento di progetto

## Scopo e principi

La Scuola di vela è un simulatore didattico per imparare la vela su una deriva e, in seguito, il carteggio. Queste decisioni guidano tutto il resto:

1. **Simulatore prima che gioco.** La fisica deve essere plausibile, perché quello che si impara deve valere anche in barca: vento apparente, filetti, barra invertita, abbrivio, sbandamento, scuffia.
2. **Tutto sempre giocabile.** Nessuna lezione, prova o regata va sbloccata: deve essere sempre possibile provare al volo una cosa specifica. Un'eventuale modalità carriera, con progressione e barche da conquistare, sarà una modalità separata con un salvataggio suo.
3. **Aiuti disattivabili al posto della semplificazione.** Chi parte da zero ha suggerimenti, barra che torna al centro, comando «gira la prua» e timoniere che si sporge da solo; chi vuole più realismo li spegne.
4. **Onestà sui contenuti.** Ogni affermazione nautica deve essere verificabile (vedi `CONTENUTI-DA-VERIFICARE.md`). Le semplificazioni del simulatore sono dichiarate, non nascoste.
5. **Progetto personale e non commerciale**, entro confini legali prudenti: nessun marchio di classi o costruttori, nessun titolo che sembri ufficiale, dati esterni solo con licenze libere e citazione.
6. **Computer con tastiera.** Il telefono non è un obiettivo.

## Architettura

Il gioco è un unico file HTML, senza dipendenze da installare. Le sole risorse esterne sono i caratteri tipografici di Google Fonts. Se non sono disponibili, il testo usa caratteri di riserva.

Dentro `index.html`, nell'ordine:

| Parte | Cosa contiene |
| --- | --- |
| CSS | Colori come variabili (tema chiaro e scuro), menu, pannello, dialoghi di quiz e glossario. |
| HTML | Menu, dialoghi, area di gioco (canvas più pannello laterale con schede per lezione, prova, regata, navigazione libera). |
| Motore fisico | Costanti della barca (`BOAT`), coefficienti della vela (`CL`, `CD`), funzione `step(stato, comandi, vento, dt)`. È puro: non tocca la pagina. |
| Contenuti | Lezioni `L1`–`L6`, `LESSONS`, prove `MISSIONS`, sequenza consigliata `SEQ`, parti future `FUTURE`, `QUIZ`, `GLOSS`. |
| Stato | Modalità corrente, vento (`env` generale, `local` sulla barca), raffiche, comandi, opzioni. |
| Raffiche | Chiazze che viaggiano col vento; `windAt(x, y)` dà il vento in un punto. |
| Menu, progressi, glossario, quiz | Salvataggi in `localStorage`. |
| Modalità | `startLesson`, `showStep`, `startMission`, `startFree`, `startRace`. |
| Input | Tastiera, pulsanti delle lezioni, cursori. |
| Simulazione | `simulate(dt)`: comandi, raffiche, fisica, manovre (virata, strambata), scuffia, obiettivi. |
| Fantasma e regate | Registrazione e riproduzione del fantasma; avversari guidati dal computer; partenza, precedenze, classifica. |
| Pannello | Strumenti e suggerimenti, aggiornati 10 volte al secondo. |
| Disegno | Mare, raffiche, scia, boe, barca, cerchio delle andature, etichette, strumenti a schermo. |
| Ciclo | `requestAnimationFrame`; un errore imprevisto viene mostrato nel pannello senza bloccare il gioco. |

### Coordinate e unità

- Mondo in **metri**, asse x verso est e asse y verso sud (come lo schermo), angoli in **gradi da nord in senso orario**.
- Velocità della barca in **m/s** (il pannello mostra nodi: 1 m/s = 1,944 nodi).
- **Attenzione alle unità**: la velocità di rotazione `S.r` è in gradi al secondo, la velocità di sbandamento `S.heelRate` in **radianti al secondo**. Un errore proprio su questo punto rendeva la strambata 57 volte troppo violenta (vedi `CHANGELOG.md`, versione 0.11).
- «Coordinate del vento» (`toWF` e `fromWF`): sistema ruotato in cui il vento arriva sempre da −y. Prove, regate e fantasmi sono descritti così, e quindi funzionano con qualsiasi direzione del vento.

### Salvataggi (`localStorage`)

| Chiave | Contenuto |
| --- | --- |
| `scuolaVelaSim.v1` | Voci completate, record delle prove e delle regate, migliori punteggi dei quiz. |
| `scuolaVelaGhost.v1` | Fantasmi: un campione ogni 0,2 s (tempo, posizione, rotta e boma rispetto al vento, sbandamento). |

### Aggancio per i collaudi

Aprendo il gioco con `#collaudo` in fondo all'indirizzo, la pagina espone `window.__sv`, che serve solo ai collaudi automatici: apertura diretta di lezioni e passi, lettura dello stato, accelerazione del tempo. Senza `#collaudo` l'aggancio non esiste.

## Come aggiungere contenuti

### Un passo di lezione

Ogni passo è un oggetto nell'array della lezione. I campi principali:

| Campo | Significato |
| --- | --- |
| `title`, `text` | Titolo e paragrafi (HTML ammesso: `<em>` per i termini). |
| `pause` | Passo di sola spiegazione: la barca è ferma. |
| `zoom`, `labels` | Ingrandimento; etichette delle parti (`prua`, `poppa`, `dritta`, `sinistra`, `albero`, `boma`, `randa`, `timone`, `barra`, `deriva`, `filetti`, `sopravento`, `sottovento`). |
| `sem` | Pulsanti semplificati (`orza`, `poggia`, `cazza`, `lasca`), usati nella lezione 1. |
| `tiller`, `sheet` | Abilitano barra e scotta. |
| `autoTrim` | La vela si regola da sola. |
| `hud` | Strumenti visibili: 0 nessuno, 1 base, 2 venti, 3 tutti. |
| `hintKind` | Suggerimento: `sail` (semplice), `tt` (filetti), `none`. |
| `rose`, `maneuvers`, `arrows` | Cerchio delle andature, frecce di virata e strambata, frecce del vento. |
| `mark` | Boa relativa alla posizione di partenza del passo, in metri. |
| `env` | Vento del passo: `{ tws: nodi, gusts: 0/1/2 }`. |
| `course`, `yawNoise` | Rotta da tenere e disturbi delle onde. |
| `bigGust` | Garantisce una raffica forte (usato per la scuffia volontaria). |
| `cond`, `hold`, `done` | Condizione di completamento `(I, S, B) => …`, secondi in cui deve restare vera, testo mostrato al completamento. |
| `final` | Ultimo passo: segna la lezione come completata. |

`I` è la lettura istantanea (`twa`, `kn`, `tt` stato dei filetti, `heel`, `r`, `sheet`, `tiller`, `inGust`), `S` lo stato della barca, `B` i contatori all'inizio del passo (virate, strambate, scuffie).

**Regola pratica, imparata a proprie spese:** ogni condizione nuova va collaudata guidando davvero la barca, non solo leggendo il codice. Diversi passi sembravano corretti ma non erano completabili, oppure si completavano senza fare nulla.

### Una prova o una regata

Le prove (`MISSIONS`) e le regate (`RACES`) sono descritte con il vento da nord; all'avvio vengono ruotate secondo il vento scelto. Le boe hanno un raggio di 12 m nelle prove e 15 m nelle regate.

## Avversari

Gli avversari sono guidati da regole scritte, con la stessa fisica del giocatore. I punti più delicati, tutti emersi dai collaudi:

- **Partenza:** attendono sottovento e di fianco alla linea, poi arrivano di bolina larga senza dover virare. Attendere vicino alla linea li costringeva a manovrare controvento da fermi, e si piantavano.
- **Mai virare da fermi:** se la rotta voluta attraversa il vento e la velocità è bassa, prima poggiano per prendere abbrivio. La regola vale solo *prima* di iniziare la virata: applicata a metà virata la interrompeva, e la barca girava attorno alla boa senza fine.
- **Isteresi di 8 secondi** nella scelta del bordo vicino a un bersaglio, altrimenti virano avanti e indietro senza avanzare.
- **Evitare le altre barche** senza mai portare la prua nell'angolo morto.

## Limiti noti

- File unico di circa 2000 righe: comodo da distribuire, ma andrà diviso in moduli se il progetto cresce (fisica, contenuti, disegno, avversari).
- Gli avversari «esperti» sono solo poco più forti dei «principianti».
- Regole di regata semplificate: non si controlla da che lato si gira la boa, e la penalità è di 15 secondi invece dei giri di penalità.
- Le semplificazioni della fisica sono elencate in `FISICA-E-TARATURE.md`.
