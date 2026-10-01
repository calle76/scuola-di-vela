# Diario delle modifiche

Tutte le versioni fino alla 0.16 sono del 26–29 settembre 2026; la 0.17 è del 1 ottobre 2026. I difetti sono riportati con la causa, perché ricordare come sono nati aiuta a non ripeterli.

## 0.17 — in corso: «Tenere la rotta» che si vinceva da sé, partenza di regata rifatta

Fatti i punti 1 e 2; i punti da 3 a 8 sono elencati in fondo alla sezione.

### Lezione 2, «Tenere la rotta»: il passo si completava senza toccare nulla

- **Difetto.** Giocando, la barca teneva la rotta da sola e il passo si completava. **Causa:** nel passo convivono due disturbi di forza molto diversa, l'orziera (2 °/s costanti verso il vento) e le spinte delle onde (3–6 °/s per 0,8 s, una ogni 1,8–3,4 s). Ogni spinta d'onda vale 2,4–4,8°, cioè da una volta e mezza a tre volte l'orziera, e **il suo segno è casuale**. La condizione chiede 8 secondi entro 6°: in 8 secondi l'orziera accumula 16°, e in quegli stessi 8 secondi cadono tre o quattro spinte che, se escono tutte col segno «poggia», la cancellano. Quando capita il passo si completa **esattamente all'ottavo secondo**, cioè subito, mentre il giocatore legge il testo. Verifica col segno forzato: onde che poggiano sempre, completato a 8,0 s; onde che orzano sempre, non completato. Se non si vince nei primi 8 secondi non si vince più, perché dopo la deriva ha già portato la prua fuori: allargando la finestra da 30 a 60 secondi i completamenti non cambiano.
- **Decisione:** orziera da 2 a 3 °/s, onde invariate. `yawNoise: true` è usato in un solo passo, quindi è l'unico toccato.
- **Numeri.** Si completa da sé: 0.16 nel browser **5 su 60**, circa una volta su otto, con tenuta di 8,0 s; 0.17 Monte Carlo sul motore **0 su 3000**, 0.17 nel browser **1 su 1000** (tenuta massima 8,0 s). Il Monte Carlo è stato ripetuto su sette prue di ingresso con gli stessi semi: è lo stesso esperimento ripetuto, quindi il numero è 0 su 3000, non 21 000. **Il caso raro è reso molto improbabile, non escluso**, e il Monte Carlo sul motore estratto lo sottostima rispetto al browser: causa non indagata.
- Il passo resta fattibile correggendo: un pilota pronto completa 6 su 6 in 8,0 s, che è il minimo possibile, identico alla 0.16 misurata nello stesso momento. Un pilota lento, che guarda la rotta due volte al secondo: 12 su 12 in entrambe le versioni, mediana 8,0 s, caso peggiore da 18,5 a 25,1 s.
- **Difetto di metodo.** `collaudo_rotta.py` faceva **un solo** tentativo senza correzioni e concludeva che il passo non si completava da sé. Con una probabilità di una volta su otto, un tentativo singolo mostra quasi sempre il fallimento: il collaudo non era sbagliato, era sotto-campionato. Riscritto con molti tentativi a passi fissi (`__sv.run`), entrando dal traverso e dalle andature larghe, e stampa i **secondi in rotta di fila raggiunti al massimo**, che è il margine vero. Aggiunto il punto in `COLLAUDI.md`: un solo tentativo non basta nemmeno per dire che una cosa **non** succede.

### Partenza di regata: posizioni casuali e caratteri degli avversari

- **Difetto.** Il giocatore nasceva sempre in (10, 45) mure a sinistra e la Blu in (28, 50) mure a dritta: rotta di collisione frontale, e in caso di contatto la penalità di 15 s era sempre del giocatore, perché mure a sinistra. **Causa:** posizioni iniziali fisse. Misurato: distanza minima all'avvio **18,1 m** e avvicinamento minimo **4,9 m a 6 secondi**, identici a ogni partenza. Il contatto scatta sotto i 4,2 m, quindi mancavano 0,7 m.
- **Decisioni:** posizioni casuali per tutti, giocatore compreso, dietro la linea, ben distanziate e senza coppie in rotta di collisione; tre caratteri degli avversari (prudente, normale, aggressiva), estratti a sorte a ogni partenza; una sola aggressiva e solo con gli esperti; il carattere di ogni barca scritto nel riquadro delle istruzioni.
- **Posizioni** (`startSpots`): le barche si piazzano una alla volta, scartando chi sta a meno di 20 m da un'altra o si avvicinerebbe sotto i 14 m entro 25 secondi; se una non trova posto si riparte da zero, fino a 40 giri, con un ripiego a zigzag calcolato a mano. Banda x ±30 m, y 38–74 m dalla linea, **26–54 m quando la preparazione è di un minuto**. Risultato: distanza minima all'avvio da 18,1 m fisso a **19,8–28,8 m**, avvicinamento minimo da 4,9 m a **14,9–18,7 m**. Campionatore verificato fuori dal browser: **0 configurazioni fuori vincolo su 20 000** per ciascuna preparazione, con una e con quattro barche.
- **Caratteri.** La *prudente* evita le altre da 22 m invece di 14, anche quando ha la precedenza. La *normale* si comporta come prima. L'*aggressiva* attende dall'altro lato della linea, così ci arriva mure a dritta con la precedenza in mano, e punta le barche mure a sinistra entro 40 m per costringerle a manovrare. Rispetta lo spirito delle regole 14 e 16: sotto 15 m (`AGGRO_OFF`) smette di stringere e sotto 14 m cerca comunque di non urtare, così una manovra per evitarla esiste sempre. La regola 16 vera **non** è stata aggiunta: la colpa di un contatto la decidono solo mure e sopravento, come prima.
- **L'aggressiva resta evitabile.** Il collaudo riprova lo stesso incontro con manovre diverse, salvando e rimettendo lo stato della regata, e la manovra parte **un secondo dopo** l'inizio dell'incontro. Con `AGGRO_OFF` a 15, 18 e 22 m il risultato è **40 incontri su 40** evitabili in tutti e tre i casi, su quattro distanze d'incontro (18, 24, 30, 38 m): scelto **15 m**, il valore più basso che basta, quindi nessuna modifica. In un campione indipendente precedente, a 15 m un incontro su 40 non aveva via d'uscita ritardata: con 40 incontri per valore la differenza fra 0 e 1 è dentro il rumore, quindi **il tasso di fallimento è basso ma non dimostrato nullo**. Le manovre provate sono solo le due estreme, barra tutta da un lato, mentre un giocatore vero può anche virare o rallentare.
- **Ritardi al via.** La **finestra di misura è la stessa** per 0.16 e 0.17 (stesso script, stessa formula: preparazione più circa 60 s di gioco dopo il via), ma si confrontano **solo le mediane**: le barche che non tagliano la linea entro la finestra vengono escluse dal conteggio, sono per definizione le più in ritardo, e il loro numero cambia fra le versioni, il che abbassa la media. Il confronto è principianti contro principianti, perché la 0.16 era misurata solo al livello predefinito. Mediane con 1, 3 e 5 minuti di preparazione, 10 partenze per tipo: 0.16 **9,4 / 9,3 / 8,7 s**, 0.17 principianti **3,7 / 3,0 / 3,4 s**, 0.17 esperti **4,4 / 5,8 / 6,1 s**.
- **Causa dei ritardi a un minuto, trovata misurando:** la distanza iniziale dalla linea. Correlazione fra distanza e ritardo **+0,75**, con 5,4 s di mediana per chi nasceva vicino contro **24,9 s** per chi nasceva lontano. Avvicinando la banda a 26–54 m la correlazione è scesa a +0,28 e il divario a 3,5 contro 4,2 s.
- **Partenze anticipate degli avversari.** Prima del via non superano la linea se sono a meno di **7 m** da essa (era 4 m): con le posizioni casuali e la prudente che evita da 22 m, qualcuna ci scivolava oltre. Restano **3 partenze anticipate su 90 con i principianti** (2 con un minuto di preparazione, 1 con tre) e **0 su 90 con gli esperti**: accettate così, perché è plausibile che un principiante anticipi e il gioco lo gestisce già, facendolo tornare dietro la linea.
- **Record delle regate invariati.** Il percorso non cambia — linea, boa e distanze sono identiche — e cambia solo da dove parte il giocatore dietro la linea: i tempi restano confrontabili e `KEYV` non si tocca.
- **Nuovo collaudo** `collaudo_aggressiva.py`. `collaudo_partenze.py` esteso: prende il numero di partenze e il livello degli avversari, e misura anche distanza minima all'avvio, avvicinamento minimo, caratteri assegnati e la correlazione fra distanza dalla linea e ritardo.
- **Collaudi:** 10 regate (6 a bastone, 4 nelle raffiche) con tutti gli avversari all'arrivo e nessuna bloccata; fantasma con gli esperti 3 corse su 3, fantasma salvato; pannello a 1360×650 senza eccedenze e i quattro `True` del riquadro, anche col testo più lungo dei caratteri; riquadro coerente con i caratteri veri, 0 aggressive su 6 partenze con i principianti e 6 su 6 con gli esperti; lezioni tutte completate.
- **Due misure buttate via, entrambe per lo stesso errore: il metro di misura legato a ciò che si voleva misurare.** La prima versione del collaudo dell'aggressiva poggiava **sempre**, e a 18 m poggiare è spesso la manovra sbagliata, perché il giocatore si trova sopravento e poggiando le va incontro: 4 contatti su 10 che sembravano colpa del gioco. La seconda faceva partire la manovra dalla condizione «l'aggressiva mi sta puntando», che dipende da `AGGRO_OFF`: con la soglia a 22 m e un incontro a 18 m la manovra non partiva mai, e le quattro righe davano numeri identici. Entrambe le avvertenze sono ora in `COLLAUDI.md`.
- **Difetto introdotto e corretto nella stessa sessione:** con la banda ravvicinata, il campionatore delle posizioni non riusciva a sistemare quattro barche e ricadeva sul ripiego **3823 volte su 20 000**, e il ripiego era scritto male, con barche fino a **0,2 m** l'una dall'altra, cioè molto peggio del difetto che si stava correggendo. La prima verifica non lo vedeva perché controllava solo la distanza minima, che il vecchio ripiego rispettava, e non che le posizioni fossero dentro la banda sorteggiata.

### Ancora da fare nella 0.17

3. Consiglio sulla vela in gran lasco e in poppa: oltre il lasco i filetti non scorrono, quindi `ttMsg` e `sailMsg` non devono più dire «lee» a vela tutta lascata; verificare i passi che controllano `I.tt`.
4. Lezione 2, «Barra sottovento» e «Barra sopravento»: riscrivere il testo con la rosa dell'angolo morto invece dei gradi, che in quei passi il pannello non mostra.
5. Lezione 3, «Bolina» e gli altri passi che chiedono un'andatura: evidenziare il settore di arrivo con un bordo tratteggiato e adattare il testo.
6. `drawLabels`: anello vuoto al posto del pallino pieno, che copre l'oggetto indicato.
7. Lezione 5, «Una virata che non riesce»: spiegare «lascia che la prua scada», aggiungere «scadere» al glossario e rendere coerente il suggerimento.
8. Ambiente dei collaudi stabile: playwright installato in modo permanente, versione allineata al browser in cache, istruzioni aggiornate in `COLLAUDI.md`.

## 0.16 — Menu a riquadri, fasce di tempo, lezione 1 con il timone, rosa e freccia della velocità
- **Decisioni (fase A, 29 settembre):** menu principale a riquadri, tutto visibile senza scorrere; fasce di tempo oro, argento e bronzo per le prove; lezione 1 con le frecce del timone al posto dei pulsanti Orza e Poggia; rosa dell'angolo morto; freccia della velocità; pannello ridotto fuori dalle lezioni. Carteggio e mare aperto escono dal menu: diventeranno un'espansione o un gioco a parte. Nei titoli del gioco si dice «brevetto», non «patente».
- **Menu a riquadri.** Tre colonne: Scuola (le 11 voci in ordine, una riga ciascuna, descrizione al passaggio del mouse); Regate e Navigazione libera; Ripasso ed esame (i sei quiz e, in grigio, «Esame su tutte le lezioni», in arrivo) e In arrivo (una riga: esame, tornei, altri tipi di barca). A 1360×650 sta tutto nella finestra, con circa 60 pixel di margine. I nomi interni dei pulsanti non cambiano, quindi i collaudi li trovano ancora.
- **Fasce di tempo delle prove** (campo `bands` di `MISSIONS`, in secondi): oro uguale al tempo di un pilota automatico, argento +25%, bronzo +60%, arrotondati ai 5 s superiori. Prova 1: 1:30, 1:50, 2:20. Prova 2: 2:20, 2:55, 3:40. Prova 3: 3:05, 3:55, 5:00. Prova 4: 5:30, 6:50, 8:45. Prova 5: 5:55, 7:20, 9:25. Si vedono nel menu (pallino accanto al record), nel riquadro delle istruzioni, nel pannello («oro entro 1:30», poi argento, poi bronzo) e all'arrivo (fascia del tentativo appena fatto). Nessun salvataggio nuovo: la fascia del menu si ricava dal record. Valgono anche con gli aiuti accesi. Il vento delle prove ha già forza fissa; cambiarne la direzione ruota il percorso e non cambia i tempi (verificato: 8 venti, 8 tempi identici). Da ritoccare dopo averci giocato: nella prova 1 il pilota regola la vela all'istante e l'oro potrebbe essere troppo stretto.
- **Taratura.** Pilota automatico dei collaudi con due correzioni: in poppa cazza solo quando sta per strambare (prima teneva la vela mezza cazzata per tutta la poppa) e in poppa piena tiene le mure invece di strambare per sbaglio. Tempi: 87, 136, 185, 327 s; prova 5 tra 342 e 353 s, mediana 351 (nelle raffiche il pilota si pianta spesso: 7 tentativi su 24 non finiti, esclusi).
- **Difetto di metodo trovato durante la taratura:** i primi tempi, presi con il tempo accelerato e cinque browser aperti insieme su un solo processore, erano falsati (108 s invece di 87 nella prova 1): il pilota reagiva più di rado del previsto. Nuovo comando dell'aggancio `#collaudo`, `__sv.run(dt, n)`, che fa avanzare la simulazione a passi fissi: i tempi non dipendono più dal computer.
- **Lezione 1 con il timone.** Via i pulsanti Orza e Poggia e i tasti A e D. Nei passi «Poggiare», «Orzare e l'angolo morto» e «Ripartire» si usano le frecce ← →, che funzionano come nel resto del gioco (barra, oppure «girano la prua» se scelto nelle impostazioni). Il testo dice quale freccia premere, calcolata all'apertura del passo secondo il lato da cui arriva il vento e l'impostazione delle frecce; con la barra aggiunge che la barra va dall'altra parte e che il perché si vede nella lezione 2. Mentre la prua gira, la riga di stato dice «Stai orzando» o «Stai poggiando». Nel passo «Poggiare» c'è l'avviso sulla strambata. Cazza e Lasca restano pulsanti e rispondono anche a ↑ ↓ oltre che a W e S.
- **Due difetti trovati collaudando la lezione 1:** rilasciata la freccia, la barra tornava al centro lentamente e la prua continuava a girare; nel passo «lascare» la barca arrivava a 118° dal vento, dove la vela tutta aperta non sbatte, e il passo non si completava. Correzioni: nella lezione 1 la barra torna al centro in fretta, come con i vecchi pulsanti; «Ripartire» chiede il vento tra 70° e 105° per un secondo; nei passi della scotta la barra resta disponibile per correggere la rotta.
- **Comportamento voluto da tenere d'occhio:** tenendo premuta la freccia troppo a lungo nel passo «Poggiare», la barca stramba a vela aperta e il registro la conta. Con i vecchi pulsanti non si poteva strambare.
- **Rosa dell'angolo morto**, a destra dell'indicatore di sbandamento (al suo posto dove lo sbandamento non c'è): vento sempre dall'alto, settore rosso di 40° per lato (la stessa costante del registro, `IRONS_A`, e lo stesso limite della voce «Andatura»), lancetta della prua che diventa rossa nel settore. Compare in prove, regate, navigazione libera e nei passi pratici delle lezioni, non nelle pause né dove c'è già la rosa grande delle andature. Impostazione «Rosa dell'angolo morto», accesa di norma. Usa il vento locale: nelle raffiche la lancetta oscilla un poco.
- **Freccia della velocità**, verde chiaro: dal centro della barca nella direzione del moto vero (avanti più scarroccio; all'indietro esce dalla poppa), più lunga con la velocità (la parte che sporge dallo scafo è proporzionale), nascosta sotto 0,3 nodi, da scuffiati e nelle pause. La scritta «velocità» sta dal lato opposto al vento. Si accende e spegne con le frecce del vento.
- **Pannello ridotto** in prove, regate e navigazione libera: Velocità, Andatura, Prua, Rilevamento boa. Vento reale, vento apparente, sbandamento e scarroccio ora si vedono sullo schermo (rosa, frecce, indicatore) e tornano con l'impostazione «Tutti gli strumenti nel pannello», spenta di norma. Le lezioni non cambiano.
- **Nuovo collaudo:** `collaudo_fasce.py` (taratura delle fasce, a passi fissi). Aggiornati `collaudo_lezioni.py` e `collaudo_registro.py` alle frecce nella lezione 1; in «Ripartire» il pilota ora rilascia la freccia come un giocatore.
- **Collaudi:** registro 13 verifiche su 13 (in quattro gruppi: qui ogni comando ha un limite di 5 minuti); lezioni tutte completate in tre passate; pannello senza eccedenze a 1360×650 e 1280×800; schermate, quiz, rotta, strambata (6 nodi nessuna scuffia, 15 nodi sempre), fantasma, giro di boa (casi a, b, f) e 6 regate senza differenze. Partenze non rilanciate: avversari e fisica non sono cambiati.
- **Difetto noto, non corretto:** con la prua nel vento le scritte «reale» e «apparente» delle frecce del vento si sovrappongono.

## 0.15 — Registro degli errori e pannello ordinato
- **Decisioni (fase A):** registro degli errori in lezioni, prove e regate; nelle lezioni non conta l'errore che il passo chiede apposta. Contatore sempre visibile durante il gioco. Segno ★ nel menu per le prove e le regate completate almeno una volta senza errori. Pannello leggibile tutto senza scorrere su uno schermo 1360×768, anche senza schermo intero.
- **Registro degli errori.** Voci e definizioni:
  - scuffia;
  - strambata a vela aperta (boma oltre 45°, la soglia del colpo del boma). Il gioco non può sapere se una strambata era voluta, quindi non la chiama «involontaria»;
  - piantato nell'angolo morto: prua a meno di 40° dal vento e velocità sotto 1 nodo per almeno 3 secondi di fila; si contano gli episodi e i secondi. Non conta prima della partenza delle regate né da scuffiati. Taratura: una virata partita a 3,1 nodi resta 1,9 s sotto 1 nodo e non conta; una partita a 2,3 nodi ne resta 4,2 e conta. Il pilota automatico dei collaudi, in 27 virate nelle prove 3, 4 e 5, non ne ha contata nessuna;
  - boa girata dal lato sbagliato (ogni attraversamento della semiretta nel verso sbagliato);
  - contatto (solo regate), separando quelli con penalità;
  - partenza anticipata e linea tagliata fuori dagli estremi (solo regate).
- Il registro si chiude all'arrivo e riparte a ogni nuovo tentativo. I record restano tempi: il registro non li modifica.
- **Lezioni:** campo `allow` nei passi che chiedono l'errore (lezione 1 «Orzare e l'angolo morto», lezione 5 «Una virata che non riesce» e «Strambata violenta», lezione 6 «La scuffia»). Un episodio di barca piantata iniziato in un passo che lo chiede non conta nemmeno se prosegue nel passo dopo.
- **Pannello riordinato** in prove, regate e navigazione libera: strumenti su tre colonne, suggerimento, barra e scotta, poi stato (tempo e record nelle prove, che prima non si vedevano; classifica nelle regate; errori), poi i comandi. Nelle lezioni l'ordine resta quello di prima, con spazi più compatti; dalla lezione 3 in poi spariscono le scritte agli estremi dei cursori.
- **Istruzioni di prove e regate** in un riquadro sul mare, a gioco fermo. Il cronometro della prova e il conto alla rovescia della regata partono con «Parti» o Invio; prima il conto alla rovescia scorreva mentre si leggeva. Il pulsante «Istruzioni» le riapre, sempre a gioco fermo. Avversari e Preparazione si scelgono nel riquadro.
- **Impostazioni** in una finestra aperta dal pulsante ⚙; mentre è aperta il gioco è fermo, come con il glossario.
- Legenda dei tasti su una riga: «R raddrizza» resta sul pulsante e nel messaggio di scuffia. «Ricomincia il passo» diventa «Ricomincia».
- **Misure** (con i caratteri veri del gioco): a 1360×650, cioè 1360×768 meno le barre del browser, il pannello sta tutto nella finestra in ogni passo di lezione, prova e regata. Nei riepiloghi finali delle lezioni il margine è zero: con F11 (schermo intero) ci sono circa 118 pixel in più.
- **Nuovi collaudi:** `collaudo_registro.py` (provoca ogni errore guidando la barca: 13 verifiche) e `collaudo_pannello.py` (altezza del pannello e riquadro delle istruzioni). Nei collaudi automatici il riquadro delle istruzioni è saltato; `collaudo_partenze.py` e `collaudo_fantasma.py` impostano Avversari e Preparazione direttamente, perché ora stanno nel riquadro.
- **Collaudi:** registro 13 verifiche su 13 (due volte); 10 regate su 10 concluse con tutti gli avversari; partenze confrontate con la 0.14.1 nello stesso momento su 36 partenze ciascuna: ritardo medio 8,2 s contro 8,3, due ritardi oltre un minuto in entrambe (difetto noto), nessuna partenza anticipata; lezioni, schermate, quiz, rotta, strambata, fantasma e giro di boa invariati.
- **Lacuna trovata durante il lavoro:** nelle prove il tempo non era mostrato da nessuna parte mentre si navigava, solo all'arrivo.

## 0.14.1 — Prova 5 con tre andature
- **Decisione:** nella prova 5 la boa 2 è spostata a sinistra della boa 1, alla stessa altezza. Il percorso diventa bolina, traverso (90° dal vento), gran lasco (circa 146°): tre andature diverse, come prometteva il testo originale. Lunghezza da circa 590 a 636 m.
- Testo della prova aggiornato; record e fantasma della prova 5 ripartono da zero (chiave `m4.3`).
- Collaudi: triangolo con le boe a sinistra completato; con la boa 2 a dritta non si completa e compare il messaggio del lato sbagliato.

## 0.14 — Giro di boa, andatura nascosta, barra ferma in gara
- **Decisioni (fase A):** andatura nascosta nel pannello delle lezioni 1 e 2; boe da lasciare a sinistra in prove e regate; barra che non torna al centro in prove e regate, riattivabile.
- **Andatura nel pannello:** nascosta nelle lezioni 1 e 2, perché le andature si spiegano nella lezione 3.
- **Barra:** l'impostazione «La barra torna al centro da sola» vale ora per la modalità in corso. Lezioni e navigazione libera: attiva, come prima. Prove e regate: spenta, perché un regatante tiene la barra ferma; la barra spaziatrice la riporta al centro. Si può riattivare.
- **Giro di boa:** prima una boa contava appena ci si passava entro 12 m (prove) o 15 m (regate), senza girarla davvero. Ora le boe intermedie vanno girate lasciandole a sinistra: conta l'attraversamento, in senso antiorario, della semiretta che parte dalla boa verso l'esterno della curva del percorso. Chi la gira dal lato sbagliato deve tornare indietro e rifare il giro, come nella regola del filo teso; il gioco lo segnala. Una freccia curva mostra il verso di giro. La boa di arrivo delle prove e l'unica boa delle prove 1–3 restano punti da raggiungere.
- **Prova 5:** il triangolo girava in senso orario (boe a dritta); ora è specchiato. **Difetto di contenuto trovato:** il testo diceva «traverso» per il secondo lato, che in realtà era un lasco a circa 126° dal vento. Testo corretto.
- **Record e fantasmi** delle prove 4 e 5 e delle regate ripartono da zero (chiavi nuove): con il giro vero i tempi non sono confrontabili. Le voci completate restano completate.
- **Avversari:** girano la boa passando per tre punti (sotto a destra, oltre a sinistra; un terzo punto solo per riprovare dopo un giro mancato), con un giro leggermente diverso per ciascuno.
- **Difetti trovati nei collaudi e corretti:**
  - avversari che passavano sopra la boa senza girarla: il cambio di rotta scattava ancora sotto la boa, da dove la bolina li portava dritti sulla boa;
  - avversari che tentavano di virare dal traverso al traverso opposto, perdevano l'abbrivio a metà e ricominciavano all'infinito. Ora prima orzano fino alla bolina, poi virano, poi poggiano;
  - barca ferma tra 40° e 44° dal vento che non ripartiva mai, perché la regola «piantata: poggia» scattava solo sotto 40°. Ora 44°, tranne in partenza, dove 44° faceva poggiare troppo presto vicino alla linea (resta 40°, salvo chi torna dietro la linea dopo una partenza anticipata).
- **Tempi degli avversari** (regata a bastone): bolina da 124 a 150 s, poppa da 84 a 93 s. Circa 12 s dipendono dalla vecchia scorciatoia del cerchio di 15 m, il resto dal giro vero. Le fasce di tempo della fase A vanno tarate sui tempi nuovi.
- **Nuovo collaudo** `collaudo_giro_boa.py`: un pilota automatico guida la barca con barra e scotta e verifica il giro dal lato giusto, dal lato sbagliato, sbagliato e poi corretto, il triangolo, e le prove 1–3 invariate. Aggancio `#collaudo` esteso con barra, scotta e boe.
- **Collaudi:** 19 regate su 19 concluse con tutti gli avversari (prima delle correzioni circa una su dieci si bloccava); contatti tra avversari non aumentati (22 in 12 regate contro 44 della 0.13); ritardi al via uguali alla 0.13 su 36 partenze; lezioni, strambata, quiz, rotta, schermate e fantasma invariati.

## 0.13 — Angolo morto realistico
- **Decisione:** angolo morto allineato alle dispense di vela (45° per lato come convenzione didattica, circa 35° per le derive). Prima la barca avanzava fino a 25–30° dal vento, più di qualsiasi fonte.
- Fisica: la vela si sgonfia quando il vento apparente è troppo stretto (`luffA0` 27°, `luffW` 7°), angolo minimo del boma 14°. Ora la barca è ferma sotto circa 33° dal vento, arranca fino a 40° e risale meglio a 45–48°.
- Timone leggermente più efficace (`turnLen` 1,05 m): con l'angolo morto più largo la virata lanciata durava 6 secondi; ora circa 4, come una deriva vera.
- Cerchio delle andature: angolo morto fino a 40°. Aggiornate le condizioni delle lezioni 1, 2, 3 e 5, i testi (bolina «tra 45° e 75°»), il glossario (angolo morto, bolina) e gli angoli di bolina degli avversari.
- Collaudi: tutte le lezioni completabili; 6 regate su 6 concluse; strambata invariata. Resta il difetto noto delle partenze degli avversari (vedi ROADMAP, fase B).

## 0.12 — Revisione generale
- Lezione 2, «Tenere la rotta»: onde che spostano la prua e barca orziera. Prima l'esercizio si completava senza fare nulla.
- Lezione 4: vento apparente indicato «tra 60° e 70°», coerente con il pannello.
- Lezione 6: testo del raddrizzamento coerente con la simulazione.
- Lezioni 1–3: solo la freccia del vento reale (il vento apparente si spiega nella lezione 4).
- Scotta più lenta di circa un quarto: la finestra di «vela regolata» era sotto il secondo di pressione.
- Più spazio tra i comandi di barra e scotta.

## 0.11 — Strambata corretta
- **Difetto:** qualsiasi strambata con la vela aperta faceva scuffiare, anche con 6 nodi. **Causa:** il colpo del boma era sommato in gradi/s a una velocità di sbandamento espressa in radianti/s, quindi era 57 volte più forte. **Correzione:** unità corrette e colpo proporzionale al vento (19° di sbandamento con 6 nodi, 39–58° con 10, scuffia con 15).
- «Vela a metà» spiegato: boma a una quarantina di gradi dal centro barca.
- Lezione 3: spiegato cosa succede superando i 180° in poppa.
- Messaggio specifico quando si scuffia per una strambata.

## 0.10 — Partenze e aiuti al timone
- Preparazione della regata a scelta: 1, 3 (predefinita) o 5 minuti; segnali adattati.
- Distanza e tempo alla linea durante l'attesa.
- Regata in solitaria contro il proprio fantasma.
- Freccia sulla prua che mostra da che parte gira la barca, e scritta «Barra a … → la prua gira a …».
- **Difetto:** gli avversari partivano con 5–70 secondi di ritardo. **Cause:** attendevano sottovento alla linea e dovevano risalire controvento; poi, attendendo vicino alla linea, tentavano virate da fermi e si piantavano. **Correzione:** attesa di fianco e sottovento, arrivo di bolina larga senza virare; regola «mai virare da fermi», valida solo prima di iniziare la virata.
- **Difetto introdotto e corretto:** la regola «mai virare da fermi», applicata anche a metà virata, faceva girare gli avversari attorno alla boa senza fine.

## 0.9 — Fantasma e regate
- Fantasma del record nelle prove e nelle regate, registrato rispetto al vento.
- Regata a bastone e regata nelle raffiche contro tre avversari, con partenza, partenza anticipata, precedenze e penalità, classifica.
- **Difetti trovati nei collaudi:** avversari che si scontravano di continuo (fino a 17 contatti a regata); avversari piantati nell'angolo morto durante le manovre per evitarsi; avversari che viravano avanti e indietro vicino alla boa; linea superata fuori dagli estremi senza conseguenze. Tutti corretti.

## 0.8 — Ripasso e verifica
- 29 domande di ripasso sulle sei lezioni.
- Scheda dei contenuti da verificare.

## 0.7 — Scuola sul nuovo motore
- Sei lezioni ricostruite sul simulatore: la barca e il vento, il timone, andature e filetti, vento reale e apparente, virata e strambata, raffiche e scuffia.
- Cinque prove con vento da direzioni diverse; navigazione libera; glossario ampliato.
- **Difetti trovati nei collaudi:** nella lezione 1, tenendo premuto Orza la barca virava, strambava e scuffiava; la scuffia «volontaria» della lezione 6 poteva richiedere più di un minuto. Corretti.

## 0.6 — Nuovo motore (campo prova)
- Vento apparente, portanza e resistenza della vela, filetti, barra reale, scarroccio.
- Sbandamento con timoniere che si sporge, raffiche visibili, scuffia e raddrizzamento.
- **Difetti:** raffiche invisibili (più grandi dell'area inquadrata); pannello che «saltava» cambiando altezza sotto i cursori; gioco bloccato dopo una scuffia su schermi piccoli. Corretti.

## 0.5 — Menu e glossario
- Menu con progressi salvati, glossario, vento da direzioni diverse nelle prove.

## 0.4 — Virata e strambata
- Lezione sulle due manovre; virata che fallisce senza abbrivio.

## 0.3 — Le andature
- Cerchio delle andature attorno alla barca.

## 0.2 — Lezione guidata
- Prima lezione passo passo, dopo che il primo prototipo si era rivelato incomprensibile per chi parte da zero.

## 0.1 — Primo prototipo
- Vista dall'alto, una vela, comandi Orza, Poggia, Cazza, Lasca, quattro prove.
