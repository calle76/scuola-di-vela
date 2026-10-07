# Documento di progetto

## Scopo e principi

La Scuola di vela è un simulatore didattico per imparare la vela su una deriva. Il carteggio e il mare aperto sono previsti come espansione o gioco a parte (vedi `ROADMAP.md`). Queste decisioni guidano tutto il resto:

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
| Contenuti | Lezioni `L1`–`L6`, `LESSONS`, prove `MISSIONS` (con le fasce di tempo `bands`), sequenza consigliata `SEQ`, `QUIZ`, `GLOSS`. |
| Stato | Modalità corrente, vento (`env` generale, `local` sulla barca), raffiche, comandi, opzioni. |
| Raffiche | Chiazze che viaggiano col vento; `windAt(x, y)` dà il vento in un punto. |
| Menu, progressi, glossario, quiz | Salvataggi in `localStorage`. |
| Modalità | `startLesson`, `showStep`, `startMission`, `startFree`, `startRace`. |
| Input | Tastiera, pulsanti Cazza e Lasca della lezione 1, cursori. |
| Simulazione | `simulate(dt)`: comandi, raffiche, fisica, manovre (virata, strambata), scuffia, obiettivi. |
| Fantasma e regate | Registrazione e riproduzione del fantasma; avversari guidati dal computer; partenza, precedenze, classifica. |
| Registro degli errori | `reg`: scuffie, strambate a vela aperta, episodi e secondi da piantato, boe dal lato sbagliato, contatti, partenze anticipate, linea fuori dagli estremi. `regAdd`, `ironsCheck`, `regText`. Si azzera a ogni avvio e si chiude all'arrivo. |
| Pannello | Strumenti, suggerimento, comandi, stato (tempo, classifica, errori), aggiornati 10 volte al secondo. In prove, regate e navigazione libera l'ordine è fissato con la proprietà CSS `order` (classe `play`); nelle lezioni vale l'ordine dell'HTML. Istruzioni di prove e regate in un riquadro sul mare a gioco fermo (`showBrief`, `hideBrief`); impostazioni in una finestra (`setDlg`). |
| Disegno | Mare, raffiche, scia, boe, barca, cerchio delle andature, etichette, strumenti a schermo. |
| Registratore di sessione | Dalla 0.18 (`ses`, `sesTick`): spento a ogni apertura, acceso dalle impostazioni; legge lo stato del gioco a ogni fotogramma, senza scriverlo, e scarica un file di testo con riassunto, legenda, eventi, messaggi, tasti, marcatori (tasto M) e stato una volta al secondo. Si legge con `tests/analizza_sessione.py`. Proposta e decisioni in `PROPOSTA-REGISTRATORE.md`. |
| Ciclo | `requestAnimationFrame`; un errore imprevisto viene mostrato nel pannello senza bloccare il gioco. |

### Coordinate e unità

- Mondo in **metri**, asse x verso est e asse y verso sud (come lo schermo), angoli in **gradi da nord in senso orario**.
- Velocità della barca in **m/s** (il pannello mostra nodi: 1 m/s = 1,944 nodi).
- **Attenzione alle unità**: la velocità di rotazione `S.r` è in gradi al secondo, la velocità di sbandamento `S.heelRate` in **radianti al secondo**. Un errore proprio su questo punto rendeva la strambata 57 volte troppo violenta (vedi `CHANGELOG.md`, versione 0.11).
- «Coordinate del vento» (`toWF` e `fromWF`): sistema ruotato in cui il vento arriva sempre da −y. Prove, regate e fantasmi sono descritti così, e quindi funzionano con qualsiasi direzione del vento.

### Salvataggi (`localStorage`)

| Chiave | Contenuto |
| --- | --- |
| `scuolaVelaSim.v1` | Voci completate (`done`), record delle prove e delle regate (`best`), prove e regate completate almeno una volta senza errori (`clean`, dalla 0.15), migliori punteggi dei quiz. I record dei percorsi cambiati nella 0.14 (regate) usano chiavi nuove (`r0.2`, `r1.2`), e quelli delle prove, cambiati con la linea d'arrivo nella 0.19, `m0.2`, `m1.2`, `m2.2`, `m3.3`, `m4.4`; vedi `KEYV`. Anche `clean` e i fantasmi usano queste chiavi. Al primo avvio della 0.19 record, stelle e fantasmi delle chiavi vecchie delle prove (`OLD_M`) si cancellano, senza migrazione, e il menu lo dice una volta sola. |
| `scuolaVelaGhost.v1` | Fantasmi: un campione ogni 0,2 s (tempo, posizione, rotta e boma rispetto al vento, sbandamento). |

### Aggancio per i collaudi

Aprendo il gioco con `#collaudo` in fondo all'indirizzo, la pagina espone `window.__sv`, che serve solo ai collaudi automatici: apertura diretta di lezioni e passi, lettura dello stato e del registro degli errori (`reg`), accelerazione del tempo, lettura del registratore di sessione (`__sv.ses`). Con `#collaudo` il riquadro delle istruzioni è saltato (`__sv.skipBrief = false` lo riattiva). Senza `#collaudo` l'aggancio non esiste.

## Che modello è il motore

Il motore è un modello cinematico didattico, non un previsore di prestazioni. Il timone produce direttamente una velocità di rotazione; non ci sono momenti, inerzia d'imbardata, onde né planata; l'equipaggio è un automatismo (il timoniere si sporge da solo). Le conseguenze sono dichiarate nel manuale. Un effetto si aggiunge solo se si sente guidando e ha una fonte; se manca una delle due cose si dichiara come semplificazione e si annota in `docs/DUBBI-E-RICERCHE.md`. Le cose che richiedono un modello dinamico (momento d'imbardata, planata, onde) vogliono un prototipo dedicato prima di costruirci sopra delle lezioni; la decisione si prende dopo il parere di un velista esperto sul livello 1.

## Come aggiungere contenuti

### Un passo di lezione

Ogni passo è un oggetto nell'array della lezione. I campi principali:

| Campo | Significato |
| --- | --- |
| `title`, `text` | Titolo e paragrafi (HTML ammesso: `<em>` per i termini). Un paragrafo può essere una funzione, calcolata all'apertura del passo (la lezione 1 la usa per dire quale freccia premere). |
| `pause` | Passo di sola spiegazione: la barca è ferma. |
| `zoom`, `labels` | Ingrandimento; etichette delle parti (`prua`, `poppa`, `dritta`, `sinistra`, `albero`, `boma`, `randa`, `timone`, `barra`, `deriva`, `filetti`, `sopravento`, `sottovento`). |
| `sem` | Pulsanti semplificati `cazza` e `lasca`, usati nella lezione 1 (rispondono anche a W S e ↑ ↓). Orza e Poggia sono stati tolti nella 0.16. |
| `turnHint` | Mentre la prua gira, la riga di stato dice se si sta orzando o poggiando; la barra torna al centro in fretta e il cursore spento della scotta è nascosto (lezione 1). |
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
| `allow` | Errori che il passo chiede apposta e che quindi non entrano nel registro: `capsizes`, `gybesV`, `irons`. |

`I` è la lettura istantanea (`twa`, `kn`, `tt` stato dei filetti, `heel`, `r`, `sheet`, `tiller`, `inGust`), `S` lo stato della barca, `B` i contatori all'inizio del passo (virate, strambate, scuffie).

**Regola pratica, imparata a proprie spese:** ogni condizione nuova va collaudata guidando davvero la barca, non solo leggendo il codice. Diversi passi sembravano corretti ma non erano completabili, oppure si completavano senza fare nulla.

### Una prova o una regata

Le prove (`MISSIONS`) e le regate (`RACES`) sono descritte con il vento da nord; all'avvio vengono ruotate secondo il vento scelto. Nelle prove le boe intermedie vanno girate lasciandole a sinistra (`roundCheck`, `markOut`). Dalla 0.19 l'ultima voce di `marks` è una **linea d'arrivo** (`finCross`): centrata in quel punto, perpendicolare all'ultimo lato, 12 m per lato (`FIN_HALF`, ipotesi nostra), con due boe piccole agli estremi. Conta solo il taglio dal lato del percorso verso l'arrivo, fra le due boe comprese, del centro della barca (nella realtà conta la prua, circa 2 m prima); il tempo è quello dell'istante esatto del taglio. Passare fuori dagli estremi dà solo un messaggio, le boe non fanno da ostacolo e toccarle non è punito. Nelle prove 4 e 5 la barca nasce sulla linea e il passaggio prima del giro di boa non conta. L'evento «boa» del registratore conta solo le boe girate (`markIdx`), l'arrivo è l'evento «arrivo». Nelle regate la boa di bolina va girata a sinistra e l'arrivo è la linea. Un percorso di prova deve girare in senso antiorario, cioè con svolte a sinistra: con svolte a destra, lasciare le boe a sinistra richiederebbe un giro di quasi 360°. Se si cambia un percorso, cambiano i tempi: va aggiornata la sua chiave in `KEYV`.

## Avversari

Gli avversari sono guidati da regole scritte, con la stessa fisica del giocatore. I punti più delicati, tutti emersi dai collaudi:

- **Partenza:** attendono sottovento e di fianco alla linea, poi arrivano di bolina larga senza dover virare. Attendere vicino alla linea li costringeva a manovrare controvento da fermi, e si piantavano.
- **Mai virare da fermi:** se la rotta voluta attraversa il vento e la velocità è bassa, prima poggiano per prendere abbrivio. La regola vale solo *prima* di iniziare la virata: applicata a metà virata la interrompeva, e la barca girava attorno alla boa senza fine.
- **Isteresi di 8 secondi** nella scelta del bordo vicino a un bersaglio, altrimenti virano avanti e indietro senza avanzare.
- **Evitare le altre barche** senza mai portare la prua nell'angolo morto.
- **Giro di boa:** tre punti di passaggio in coordinate del vento: sotto e a destra della boa, poi oltre e a sinistra (lì si attraversa la semiretta e la boa è girata); un terzo, sotto a sinistra, solo per riprovare dopo un giro mancato. Il secondo punto si punta solo da sopra il livello della boa: da più in basso la bolina porta la barca sopra la boa.
- **Virare da un'andatura larga:** se il bersaglio è sull'altra mura e a proravia del traverso, prima orzano fino alla bolina, poi virano. Virare direttamente dal traverso al traverso opposto fa perdere l'abbrivio a metà.
- **Barca piantata:** sotto 44° dal vento e sotto 0,6 m/s poggiano per ripartire (40° in partenza, dove 44° le faceva poggiare troppo presto vicino alla linea).
- **Posizioni di partenza casuali** (dalla 0.17), giocatore compreso: `startSpots` piazza le barche una alla volta dietro la linea, scartando chi sta a meno di 20 m da un'altra o si avvicinerebbe sotto i 14 m entro 25 secondi; se una non trova posto si riparte da zero. Prima erano fisse, e il giocatore nasceva a 18 m dalla Blu con le prue una contro l'altra. Con un minuto di preparazione la banda è 26–54 m dalla linea invece di 38–74: la distanza iniziale era il motivo dei ritardi al via (correlazione +0,75 con un minuto).
- **Prima del via gli avversari non superano la linea** se sono a meno di 7 m da essa (era 4 m): con le posizioni casuali qualcuna ci scivolava oltre. Resta qualche partenza anticipata fra i principianti, ed è voluta: è plausibile.
- **Caratteri** (dalla 0.17), scritti nel riquadro delle istruzioni: *prudente* (evita le altre da 22 m invece di 14, anche quando ha la precedenza), *normale* (il comportamento di sempre), *aggressiva* (prima del via attende dall'altro lato per arrivare alla linea mure a dritta, e punta le barche mure a sinistra vicine per costringerle a manovrare). Una sola aggressiva, solo con gli avversari esperti.
- **L'aggressiva resta evitabile:** sotto 15 m (`AGGRO_OFF`) smette di stringere e sotto 14 m cerca di non urtare, così una manovra per scansarla esiste sempre. È lo spirito delle regole 14 e 16, non la regola 16: la colpa di un contatto la decidono solo mure e sopravento.

## Pannello: una regola da rispettare

Su uno schermo 1360×768 con le barre del browser (finestra di circa 1360×650) il pannello deve stare tutto nella finestra, senza scorrere. Nei riepiloghi finali delle lezioni il margine è zero: ogni riga aggiunta al pannello va verificata con `collaudo_pannello.py`.

## Limiti noti

- File unico di circa 2000 righe: comodo da distribuire, ma andrà diviso in moduli se il progetto cresce (fisica, contenuti, disegno, avversari).
- Gli avversari «esperti» sono solo poco più forti dei «principianti».
- Regole di regata semplificate: la boa va girata dal lato giusto (dalla 0.14), ma la penalità per un contatto è di 15 secondi invece dei giri di penalità, e toccare la boa non è punito.
- Le semplificazioni della fisica sono elencate in `FISICA-E-TARATURE.md`.
