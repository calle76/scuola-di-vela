# La regata come fonte: replay, situazioni da ripetere, quiz e consigli

Proposta del 18 ottobre 2026, nata in chat da un'idea di Ale. **Nessun codice toccato.**

**Aggiornamento del 19 ottobre 2026:** con l'impianto nuovo dei livelli (`VISIONE-LIVELLI-E-CARRIERA.md` §2) questo meccanismo è il cuore della parte «b» di ogni livello, a cominciare dall'1b; le domande sugli incidenti con le precedenze arrivano col livello 2 (regolamento). Il «campo di vento in sviluppo» citato qui sono i salti di vento della 1.0.28.

Stati usati come in `VISIONE-LIVELLI-E-CARRIERA.md`: **[deciso]**, **[proposta]**, **[aperto]**, **[da verificare]** (qui vuol dire anche «da controllare nel codice prima di proporre l'implementazione»).

## 1. L'idea

Ogni regata giocata diventa materiale didattico. **[deciso]** (idea di Ale)

Dalla stessa regata si ricavano cinque cose:

| Cosa | A cosa serve |
| --- | --- |
| **Replay** | Rivedere la regata dove serve, non solo leggere i dati scritti |
| **Momenti chiave** | Brevi spezzoni attorno agli eventi, con il commento del coach |
| **Quiz sugli incidenti** | «Blu tocca Verde ed è penalizzata: perché?», con lo spezzone. Vale anche per gli incidenti fra avversari, non solo per i propri. Dà punti come i quiz |
| **Ripeti da qui** | Rientrare nella stessa situazione registrata e rifarla meglio: «hai perso tempo nel giro di boa, ripetila» |
| **Consigli di rotta** | «Hai virato troppo presto», «la rotta migliore era questa», «il vento migliore era dall'altra parte» |

Il coach di fine regata esiste già (Ale, 18 ottobre 2026): questa proposta lo collega al replay e ai quiz, non lo sostituisce.

## 2. Su cosa si appoggia (da verificare nel codice)

Quanto risulta dai file del progetto caricati il 16 ottobre. **Il campo di vento sul campo di regata è in sviluppo (Ale, 18 ottobre 2026)** e i documenti non sono aggiornati: questa sezione va riletta con il codice di oggi. **[da verificare]**

- **Coach di fine regata**: c'è. Da vedere quali eventi conosce e con quali dati.
- **Registratore di sessione** (`registratore.js`): una riga di stato al secondo **solo per la barca del giocatore**, più eventi, tasti e messaggi. È di sola lettura e non chiama `Math.random`, quindi la simulazione resta identica al bit con o senza. È il principio da tenere anche qui.
- **Fantasma** (`regate.js`, `rec.samples`): campioni della sola barca del giocatore, con un tetto di circa 20 minuti; si ridisegna interpolando. È già un replay in piccolo.
- **Registro degli errori** (`reg`) e contatti con o senza colpa (`contacts()`, 0.21.1).
- **Seme** (`__seed` nei collaudi): le regate si possono ripetere uguali. Nella 0.21.1 si è visto che ogni frame del browser consuma `Math.random` in `draw()`: la ripetibilità vale solo se il seme si rimette subito prima dei passi.
- **Campo di vento**: in sviluppo. Decide quanto valgono i consigli di §3.F.

## 3. I pezzi

### A. Registrazione della regata in memoria **[proposta]**

- A ogni regata si salvano in memoria, alcune volte al secondo, posizione, prua, velocità, sbandamento, boma e barra di **tutte** le barche, più lo stato del vento (raffiche presenti, direzione e forza nel punto di ogni barca, e quello che il campo di vento in sviluppo permetterà di salvare).
- Gli eventi (virate, giri di boa, contatti con chi e con quale colpa, penalità, partenza anticipata, arrivo) si salvano con l'istante e le barche coinvolte.
- Sola lettura, come il registratore: con o senza registrazione la regata resta identica al bit. Si collauda come il registratore.
- Ordine di grandezza: 4 barche, 10 campioni al secondo, regate di 5 minuti fanno circa 12.000 righe. Poche. **[da verificare]**
- **[aperto]** Se la regata registrata si tiene solo fino alla regata dopo, o se si possono conservare le ultime N regate (memoria del browser).

### B. Replay **[proposta]**

- Si apre **dove serve**: dal riepilogo, toccando un evento o un consiglio del coach. Non è una schermata obbligatoria.
- Gioco fermo; barra del tempo con i segni degli eventi; pausa, 1×, 2×, 4×; scie delle barche; si può seguire una barca qualsiasi.
- La vista del replay può mostrare quello che in barca non si vedeva tutto: le raffiche su tutto il campo, la layline, la scia del fantasma. È il punto dove il replay insegna più del gioco. **[proposta]**
- Disponibile anche nel gioco libero (principio «tutto sempre giocabile»).

### C. Momenti chiave **[proposta]**

- Il gioco ritaglia da solo 10-15 secondi attorno a ogni evento importante e ci attacca la frase del coach.
- Frasi brevi a video, spiegazione lunga nel manuale (preferenza di Ale: «non deve essere tutto a video»).

### D. Quiz sugli incidenti **[proposta]**

- Generati dai dati dell'incidente: mure delle due barche, chi è sopravento, se sono affiancate, se sono vicino alla boa, chi ha cambiato rotta.
- Domande del tipo: «Chi è penalizzato?», «Perché?» (risposte con la regola in parole semplici, parafrasata dal regolamento, mai copiata), con lo spezzone del momento chiave.
- Valgono anche per i contatti fra avversari: ogni regata ne produce altri.
- **Prerequisito duro:** le regole di precedenza del livello 2. Oggi la colpa si decide solo da mure e posizione, e `ROADMAP.md` annota già casi in cui può sbagliare (stesse mure senza affiancamento, contatto provocato da sottovento). Un quiz costruito su quel giudizio insegnerebbe regole sbagliate. Prima di allora si possono fare solo domande su **mure diverse**, dove il giudizio è già corretto. **[da verificare]**
- **Punti in Conoscenza**, come i quiz. **[aperto]** Quanti, con quale tetto, se ogni incidente vale una volta sola: senza tetto basterebbe giocare tante regate con molti contatti.

### E. Ripeti da qui **[proposta]**

- Dal momento chiave: «Hai perso tempo nel giro di boa / hai avuto un contatto: ripetila». Si riparte qualche secondo prima dell'evento, nella stessa situazione.
- Serve un'**istantanea completa** dello stato: barche e loro IA, raffiche e vento, generatore casuale, tempo della regata, penalità, registro. **[da verificare]** se oggi tutto lo stato si può salvare e ricaricare, o se qualche variabile vive nascosta in una funzione.
- Il vento si ripete uguale solo se non dipende dalle azioni del giocatore. Gli avversari invece reagiscono alla manovra nuova: va bene, è un **esercizio sulla situazione**, non una ripetizione identica. Da scrivere nel manuale.
- Accanto, la propria versione registrata come fantasma, per confrontare.
- Esito della ripetizione: tempo perso rispetto alla prima volta, contatto evitato o no.
- **[aperto]** Se una ripetizione dà qualcosa (un punto di Abilità? niente?). Non deve cambiare il piazzamento della regata vera.

### F. Consigli di rotta **[proposta]**

Due famiglie diverse:

1. **Geometrici, affidabili subito:** virata troppo presto o troppo tardi rispetto alla layline, metri navigati in più, giro di boa largo, tempo perso in virata rispetto al pilota. Si calcolano dalla polare e dalla registrazione.
2. **Di vento:** «il vento migliore era dall'altra parte», «la rotta migliore era questa». Hanno senso solo con un vento che cambia sul campo, cioè col campo di vento in sviluppo. **Vanno progettati insieme a quello**, non dopo. Si presentano onestamente come «col senno di poi» (rotta trovata conoscendo tutto il vento registrato), non come «la» rotta ottima. **[aperto]** Come si calcola (per esempio il pilota che rifà il lato con il vento già noto) e quanto costa.

## 4. Ordine proposto **[proposta]**

| Fase | Contenuto | Dipende da |
| --- | --- | --- |
| 1 | A (registrazione) + B (replay) | Niente: non tocca la fisica. Utile subito anche ai collaudi |
| 2 | C (momenti chiave) + consigli geometrici (F.1) | Fase 1, coach esistente |
| 3 | E (ripeti da qui) | Istantanea completa dello stato |
| 4 | D (quiz sugli incidenti), con i punti | Regole di precedenza del livello 2 (prima, solo mure diverse) |
| 5 | Consigli di vento (F.2) | Campo di vento in sviluppo |

Ogni fase è una versione a sé, collaudata guidando davvero la barca, con il `CHANGELOG.md` aggiornato.

## 5. Domande per Ale **[aperto]**

1. Il replay si apre solo dagli eventi del riepilogo, o anche dal menu («rivedi l'ultima regata»)?
2. Quante regate si conservano: solo l'ultima, o le ultime di un torneo?
3. Punti in Conoscenza dai quiz sugli incidenti: quanti e con quale tetto?
4. La ripetizione di una situazione dà qualcosa per i meriti?
5. I consigli di vento: si progettano dentro il lavoro sul campo di vento in corso, o subito dopo?

## 6. Da controllare in Claude Code prima della proposta di implementazione

- Stato attuale del campo di vento e cosa se ne può salvare per il replay.
- Dove vive il coach di fine regata e quali dati usa.
- Se tutto lo stato della regata si può fotografare e ricaricare (per E).
- Frequenza e contenuto dei campioni del fantasma; se riusarli per le altre barche.
- Memoria occupata da una regata registrata con tutte le barche.
- Che registrazione e replay lascino la simulazione identica al bit (stesso controllo del registratore).

## 7. Principi di `PROGETTO.md`

- **Tutto sempre giocabile:** replay, quiz e ripetizioni anche nel gioco libero.
- **Simulatore plausibile:** i consigli dichiarano su cosa si basano; quelli di vento solo col campo di vento.
- **Confini legali:** regole parafrasate, nessuna copia di casi ufficiali o testi del regolamento.
- **Solo computer:** nessun vincolo nuovo.

## 8. Gioco a più persone (aggiunto il 18 ottobre 2026)

Ale vorrebbe giocare uno contro uno e due contro due con altre persone, contro o nella stessa squadra. Le altre idee della chat del 18 ottobre (partenza a cancello, inseguimento, match race, vela latina e il resto) **non sono scartate**: qui si guarda solo come la regata registrata aiuta il gioco a più persone. **[proposta]**

### Perché è fattibile in questo gioco

- **La vela è lenta.** Un ritardo di rete di circa un decimo di secondo, grave in un gioco d'azione, qui pesa poco. **[da verificare]** giocando.
- **Tutto gira nel browser.** Due browser possono parlarsi direttamente (WebRTC), senza un server del progetto da mantenere.
- **Gli avversari del computer esistono già.** In un due contro due con due sole persone, gli altri posti li prende il computer, sia come compagni sia come avversari.
- **Si riusa il lavoro di §3.** La registrazione (A) e l'istantanea dello stato (E) sono gli stessi dati che servono per spedire la regata da un computer all'altro.

### Gradini, dal più semplice

| Gradino | Cosa | Costo | Limite |
| --- | --- | --- | --- |
| 1 | **Sfida a distanza.** Un amico corre la regata e manda il file della registrazione; si corre contro la sua barca, che si muove come lui l'ha guidata | Basso, dopo la fase 1 di §4 | Non reagisce a chi gioca: niente contatti né precedenze vere |
| 2 | **Due giocatori sullo stesso computer** | Medio | Due persone su una tastiera; vista più larga per vedere entrambe le barche; i tasti si scontrano con la regola del 7 ottobre (W S per la vela): da ripensare a parte |
| 3 | **Uno contro uno online in tempo reale.** Un computer fa da «padrone di casa» e calcola la regata; l'altro manda i propri tasti e riceve le posizioni | Alto | Vedi le avvertenze sotto |
| 4 | **Due contro due online**, con persone e computer mescolati nelle squadre | Il più alto | Richiede il gradino 3 e le regole a squadre |

Perché il «padrone di casa» e non due computer che calcolano ciascuno la regata in parallelo: la seconda strada richiede risultati identici al bit su due browser diversi, e le funzioni matematiche del browser (seno, coseno e simili) non lo garantiscono. **[da verificare]**

### Avvertenze

- **Presentare i due browser.** Per collegarsi serve un piccolo servizio esterno che li metta in contatto, oppure uno scambio di codici a mano fra i due giocatori. Ci sono servizi gratuiti: da scegliere con i confini legali di `PROGETTO.md` (condizioni d'uso, nessun dato personale salvato). **[aperto]**
- **Reti che non si collegano.** Su alcune reti (uffici, alcuni operatori) la connessione diretta non passa e servirebbe un ripetitore, di solito a pagamento. Il gioco deve dirlo chiaramente invece di bloccarsi. **[da verificare]**
- **Privacy.** Collegati direttamente, ciascun computer vede l'indirizzo di rete dell'altro. Fra amici va bene; va scritto nel manuale.
- **Chi bara.** Nessuna protezione, come già scritto per la fase F di `ROADMAP.md`. Va bene fra amici, non per classifiche pubbliche.
- **Regole prima.** Il due contro due vive di precedenze e penalità: con persone vere va giocato solo dopo le regole del livello 2. Il match race uno contro uno ha in più le sue regole di partenza (ingresso nell'area da estremi opposti, prepartenza): proposta a parte, se si sceglie quel formato.
- **Ospitalità.** Il gioco sta su GitHub Pages: le pagine restano statiche, la rete passa solo fra i browser. **[da verificare]** che il servizio scelto per presentarli funzioni da lì.

### Ordine proposto **[proposta]**

1. Gradino 1 subito dopo la fase 1 di §4 (registrazione e replay).
2. Gradino 3 dopo le regole del livello 2 e dopo l'istantanea dello stato (fase 3 di §4).
3. Gradino 4 per ultimo. Il gradino 2 solo se Ale lo vuole: non è un passo obbligato verso l'online.

### Domande per Ale **[aperto]**

1. Il gradino 2 (stesso computer) interessa o si salta?
2. Si accetta un servizio esterno gratuito per presentare i browser, o si preferisce lo scambio di codici a mano (più scomodo, nessun servizio)?
3. Nel due contro due online: prima due persone nella stessa squadra contro il computer, o una persona per squadra?
