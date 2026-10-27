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

## 9. Fermata 1: la regata come scuola dell'1b (20 ottobre 2026)

**Nessun codice toccato.** Risposte di Ale del 20 ottobre: il replay si apre **dagli eventi del riepilogo e dal menu** («Rivedi l'ultima regata»); si conserva **solo l'ultima regata**. Soprattutto: la registrazione serve **più come strumento di scuola che come replay**. Da una regata nascono tre cose: il **momento saliente** (la lezione), **«ripeti la manovra»** (il ripasso) e la **domanda** («perché la Blu ha preso la penalità?», il test). Nella parte «b» dei livelli sarà lo strumento principale. Quindi il replay completo, con la barra del tempo di §3.B, passa in secondo piano, e l'ordine di §4 cambia: prima A + C + E + D, poi i consigli geometrici (F.1).

### 9.1 Cosa c'è oggi nel codice (letto il 20 ottobre, 1.0.33)

- **Fantasma** (`regate.js`, `rec`): un campione ogni 0,2 s della **sola barca del giocatore** (posizione, prua, boma, sbandamento), salvato nel browser solo quando la regata è un record. Non basta: mancano gli avversari, il vento e tutto quello che serve per ripartire.
- **Contatti** (`contacts()`): si sa già chi è in colpa e perché (`why`), ma il dato resta solo nel messaggio `R.lastRule`, e solo per i contatti del giocatore. Il giudizio: con mure diverse è in colpa chi è mure a sinistra; con le stesse mure, chi è sopravento, **senza guardare se le barche sono affiancate**.
- **Coach di fine regata:** non esiste. A fine regata c'è solo `raceResults()`, cioè posto, tempo, distacchi e il registro degli errori.
- **Stato di una regata:** sta tutto in variabili condivise: `R` (barche, con la loro `S`, i comandi e i dati della guida automatica), `S`, `ctl`, `env`, `local`, `gusts`, `gustLevel`, `gustTimer`, `shiftSt`, `shiftDeg`, `simTime`, `reg`, `wake`. Sono oggetti semplici, quindi si possono copiare. Fanno eccezione `R.signals`, che è un `Set`, e alcuni riferimenti incrociati: `R.boats[0].S` è la stessa `S`, `R.boats[0].ctl` è `ctl`. Al ripristino vanno ricollegati.
- **Caso:** il gioco usa `Math.random` senza un seme (raffiche nuove, virate degli avversari, colpo della strambata). Il suo stato **non si può salvare**, quindi dopo un ripristino le raffiche **nuove** saranno diverse; quelle già presenti si salvano. Va bene, perché la ripetizione è un esercizio sulla situazione, non una copia (§3.E).

### 9.2 Modello più semplice plausibile

**Dove vale:** solo nelle regate con la barca dell'1b (oggi «Regata nei salti di vento», `R.lv2`). L'1a è congelato, quindi le sue regate non cambiano. Le regate dell'1b sono già giocabili dal menu libero, quindi «tutto sempre giocabile» è rispettato.

**Pezzo 1: registrazione (versione 1.0.34, insieme al pezzo 2).** Sola lettura, come il registratore:
- un'**istantanea** dello stato della regata ogni 0,5 s, in memoria. Escluse la scia (solo disegno) e la storia dei distacchi `hist` (si ricostruisce tagliando quella finale);
- un **elenco di eventi** di tutte le barche: contatti (chi, mure di ognuna, chi è in colpa e perché, posizioni), partenze anticipate, giri di boa (con il tempo per girarla), virate e strambate, scuffie, arrivi;
- si tiene **solo l'ultima regata**: si cancella quando ne parte un'altra o quando si chiude la pagina.

**Pezzo 2: momenti salienti (1.0.34).** A fine regata, nel riepilogo, si vedono al massimo 6 momenti, scelti dagli eventi: i contatti in cui era coinvolto il giocatore, la sua partenza anticipata, il suo giro di boa, la sua scuffia, poi i contatti fra avversari. Toccandone uno, lo si rivede a gioco fermo: 10 s prima e 5 s dopo, a 1× o 2×, con pausa, e con una frase che spiega cosa è successo (spiegazione lunga nel manuale). Dal menu, «Rivedi l'ultima regata» apre lo stesso elenco.

**Pezzo 3: ripeti la manovra (1.0.35).** Dal momento saliente si riparte **10 s prima dell'evento**, con l'istantanea ripristinata, e si gioca davvero fino a **15 s dopo**. Accanto c'è la propria barca registrata, come fantasma. Alla fine un esito: contatto evitato o no, e quanti metri di strada (`strada()`, quella dei distacchi) si sono guadagnati o persi rispetto alla prima volta. **Non cambia** né il risultato della regata vera, né i record, né i meriti.

**Pezzo 4: domande sugli incidenti (1.0.36).** Si generano dagli eventi registrati, con tre risposte possibili e lo spezzone del momento. Nell'1b solo i casi in cui il giudizio del gioco è già giusto:
- **contatti con mure diverse**: chi doveva lasciare strada e perché;
- **partenze anticipate**: perché la barca è stata richiamata e cosa doveva fare.

I contatti con le stesse mure restano fuori finché il livello 2 non controllerà se le barche sono affiancate: una domanda su quel giudizio insegnerebbe una regola sbagliata (§3.D). Le regole si scrivono in parole nostre, senza copiare il regolamento.

**Dopo, a parte:** i consigli geometrici (F.1), la barra del tempo sull'intera regata (§3.B), le regate del torneo (si passa a «più regate» quando arriveranno i tornei).

### 9.3 Costanti nuove (tutte ipotesi nostre, niente fonti)

| Costante | Valore | Perché |
| --- | --- | --- |
| Intervallo fra istantanee | 0,5 s | Una virata dura circa 3 s: 6 istantanee bastano per ridisegnarla interpolando |
| Finestra del momento | 10 s prima, 5 s dopo | Una regata dell'1b dura alcuni minuti: si vede l'avvicinamento senza annoiare |
| Ripetizione | da 10 s prima a 15 s dopo | Il tempo per cambiare manovra e vederne l'effetto |
| Momenti nel riepilogo | al massimo 6 | Ci stanno nel pannello |

### 9.4 Criteri (soglie nostre, dichiarate ora)

Semi da 1 a 40 per scegliere e tarare, semi da 101 a 140 (mai guardati) per la conferma. Ogni criterio dice quante volte ha misurato davvero; un criterio che misura zero casi è **FALLITO**, non OK.

| | Criterio | Soglia |
| --- | --- | --- |
| S1 | **Simulazione identica:** 40 regate dell'1b guidate dal pilota, con e senza registrazione: tempi d'arrivo, penalità ed eventi identici al bit. Impronta dell'1a, `polare.js` e `raffiche_e_virate.js` identici | 0 differenze |
| S2 | **Memoria** di una regata registrata (istantanee + eventi), misurata su 20 regate | al massimo 5 MB (stima: 1-3 MB) |
| S3 | **Costo:** tempo di calcolo per passo, con e senza registrazione | al massimo +10% |
| S4 | **Ripristino esatto:** istantanea → ripristino → nuova istantanea, su 20 regate × 10 istanti | 0 differenze, almeno 200 casi |
| S5 | **Ripetizione che gira:** 200 ripetizioni guidate dal pilota, dal ripristino fino alla fine della finestra | 0 errori; nessuna variabile della regata vera cambiata (risultato, record, meriti) |
| S6 | **Momenti completi:** ogni contatto, partenza anticipata e scuffia del giocatore in 40 regate compare fra i momenti | 100%, con il numero di casi dichiarato (più di 0) |
| S7 | **Domande giuste:** in ogni domanda generata, la risposta giusta coincide con il giudizio di `contacts()` o con il richiamo | 100%, almeno 20 domande |
| S8 | **Pannello** a 1360×650 con l'elenco dei momenti e con la domanda | 0 pixel di eccesso |
| S9 | **Prova da giocatore:** pagina senza `#collaudo`; regata, momento, ripetizione, domanda | completa senza errori nella console |

### 9.5 Rischi

- **Stato nascosto.** Una variabile che non entra nell'istantanea farebbe ripartire la regata in uno stato diverso: per esempio i contatori fuori da `S` o `R` (`wakeT`, `holdT`) o lo stato dei messaggi. S4 lo trova solo per quello che l'istantanea contiene: per questo serve anche S5, che controlla che la ripetizione continui senza errori.
- **Riferimenti incrociati** (`R.boats[0].S === S`): se al ripristino non si ricollegano, il giocatore guida una barca e la regata ne muove un'altra. Va un controllo dedicato dentro S5.
- **La ripetizione non deve scrivere nei salvataggi.** `updateRace` salva record e piazzamenti all'arrivo: durante una ripetizione va spento (S5).
- **Memoria:** `R.boats[i].hist` cresce durante la regata, per questo resta fuori dalle istantanee. Se S2 sfora, l'intervallo passa a 1 s, dichiarandolo.
- **Registratore di sessione:** deve scrivere che è partita una ripetizione. Altrimenti, nelle registrazioni che Ale manda, il tempo della regata sembrerebbe tornare indietro.

### 9.6 Ancora aperto per Ale

1. Le domande sugli incidenti danno punti di Conoscenza? Proposta: per ora no, si decide coi tornei e coi meriti dell'1b.
2. La ripetizione dà qualcosa? Proposta: no, solo l'esito a video.

### 9.7 Correzioni di Ale e materiale tarato sul livello (20 ottobre 2026)

**Questa parte vale sopra §9.2 dove le due dicono cose diverse.** Ale: dalla regata nascono quattro cose, e ognuna parla **solo di quello che il livello insegna**.

1. **Il momento saliente** (la lezione).
2. **Il ripasso:** si ripete una cosa che si poteva fare meglio, non solo un errore (la partenza, il giro di boa, un sorpasso). Il gioco rimette il giocatore **esattamente** in quel momento della regata.
3. **Il test, dove si può:** domande esatte su un evento qualsiasi non si generano. Si fanno sulle penalità, dove la risposta giusta si conosce.
4. **Il commento tecnico** sulle scelte (dove cercare il vento, la rotta, quando virare): è **tattica**, quindi materiale dei livelli successivi (5a). Nell'1b non c'è.

**«Esattamente in quel momento»: cambia il §9.1.** Nelle regate dell'1b il caso del gioco (`Math.random`) può essere sostituito da un generatore col seme, il cui stato **entra nell'istantanea**. Gli usi sono pochi: raffiche nuove (`spawnGust`, `updateGusts`), salti di vento (`newShift` e `stepShift` ricevono già il generatore come argomento), lunghezza dei bordi degli avversari (`stepAI`) e colpo della strambata. Così, se il giocatore rifà le stesse mosse, la ripetizione è identica alla regata; se fa altro, cambiano solo le reazioni degli avversari. Il seme si estrae da `Math.random` alla partenza, quindi i collaudi con `__seed` restano ripetibili.
- **Prezzo:** le regate dell'1b non saranno più identiche al bit a quelle di oggi. Restano uguali in media, perché il generatore è diverso ma i numeri sono distribuiti allo stesso modo. Si può fare, perché la barca dell'1b non è ancora congelata. L'1a non si tocca: lì resta `Math.random`.
- **Criterio nuovo S10:** si gioca una regata, poi la si ripete da 10 istanti diversi con le stesse mosse registrate. Le posizioni di tutte le barche devono coincidere al bit fino alla fine della finestra. Su 20 regate e quindi 200 casi: 0 differenze.

**Cosa insegnano 1a e 1b, e quindi di cosa parlano momenti, ripassi e domande nell'1b:**

| Argomento | Dove si impara | Momento e ripasso nell'1b | Cosa misura il gioco (già nei dati) |
| --- | --- | --- | --- |
| **Partenza** | 1a: riquadro delle regate (vicino alla linea, quasi fermi, cazzare negli ultimi secondi) | Ripeti da 30 s prima del via | Ritardo al via, velocità al taglio, distanza dalla linea allo sparo; partenza anticipata |
| **Giro di boa** | 1a: prova del giro di boa, regate | Ripeti da 3 lunghezze prima della boa | Tempo da 3 lunghezze prima a 3 dopo, larghezza del giro, lato sbagliato |
| **Virata** | 1a: lezione 5. 1b: virate corrette, timone che stalla | Ripeti la virata più lenta | Velocità persa, secondi per tornare in velocità, pala in stallo |
| **Strambata e boma** | 1a: lezione 5. 1b: «spingi il boma» (Z) | Ripeti la strambata | Strambata violenta o controllata, velocità persa |
| **Raffiche e scuffia** | 1a: lezione 6. 1b: raddrizzata lunga | Ripeti da 10 s prima della scuffia | Sbandamento, scotta lascata o no, tempo perso |
| **Salti di vento** | 1b: lezione breve sui salti | Ripeti da prima del salto | Solo la reazione di base: viri o no quando il vento scarseggia. È il limite dell'1b; la strategia è del 5a |
| **Sorpasso** | nessuna lezione: fa da contenitore | Ripeti da 20 s prima | Chi ha superato chi e dove (su che lato e in che punto del percorso). Nell'1b le barche non si tolgono vento, quindi niente commento tattico |
| **Penalità** | 1a: regate (mure, sopravento, 15 s) | Rivedere il contatto | **Domande** solo su mure diverse e partenza anticipata (§9.2, pezzo 4) |

**Cosa resta fuori dall'1b:** commenti sulla rotta e sul vento «col senno di poi», copertura del vento (5a); domande sulle stesse mure e sullo spazio alla boa (livello 2, quando il gioco controllerà se le barche sono affiancate); penalità a giri (livello 2).

**Lezioni brevi dell'1b** (§2 di `RICERCA-CONTENUTI-LIVELLI.md`): il timone che stalla e Z; i salti di vento; la raddrizzata; le virate. **I testi si possono scrivere adesso; le soglie dei passi aspettano la barca congelata.** Ogni lezione breve ha il suo argomento nella tabella qui sopra: quello che si impara in una lezione si ritrova nei momenti della regata, e viceversa.

**Ordine delle versioni rivisto:**
- **1.0.34:** generatore col seme nelle regate dell'1b, registrazione e momenti salienti, scelti dagli argomenti della tabella;
- **1.0.35:** ripasso, cioè «ripeti da qui» con l'esito;
- **1.0.36:** domande sulle penalità.

I testi delle lezioni brevi si scrivono a parte, senza toccare il motore.

### 9.8 Revisione in chat del 20 ottobre e decisione di Ale: tutto rimandato

**Decisione di Ale (20 ottobre 2026):** il replay e la scuola dalla regata servono **solo nelle regate dei tornei della parte «b»**, non nelle regate libere della parte «a». Quindi §9.2 e §9.7 hanno il bersaglio sbagliato: oggi non c'è nessuna regata in cui il replay serva. **Il lavoro è rimandato a dopo i tornei dell'1b** (la «strada B» della chat: si costruisce una volta sola, sul percorso vero a triangolo). §9.1-§9.7 restano come materiale per la prossima proposta.

**Come è andata la revisione:** la chat ha lavorato prima su `regate.js` e `avvio.js` vecchi, presi dalle conoscenze del progetto (anteriori alla 1.0.16, con quattro copie di `avvio.js`), e senza sapere che il replay è per i tornei. Poi ha ricontrollato sui file della 1.0.33. Qui sotto ci sono solo i punti che restano veri sul codice di oggi; quelli marcati «verificato qui» li ho ricontrollati io il 20 ottobre.

**Decisione di Ale (20 ottobre 2026): si ripete la situazione, non la regata al bit.** Come un allenatore che dice «rimettiamoci in quel momento: rifai il giro di boa, la strambata, il sorpasso, evita il contatto», senza pretendere la stessa onda. Il ripasso ripristina l'istantanea (posizioni, barche, vento e raffiche presenti in quel momento), poi il caso del gioco prosegue normalmente. **Cadono** quindi il generatore col seme di §9.7, i passi fissi, la registrazione dei tasti e il criterio S10. Il primo e il quarto punto qui sotto non vanno più risolti, basta dichiararli. Resta da garantire che il ripristino sia giusto (S4) e che la ripetizione non scriva niente (S5).

**Da risolvere nella prossima proposta:**
- **Passo della fisica variabile** (verificato qui: `avvio.js:13`, `dt = min(0,05 s, fotogramma)`, ripetuto `timeScale` volte). Il punto di ripartenza può essere esatto; il seguito nel browser no, nemmeno con le stesse mosse. Per avere anche il seguito servono passi fissi in regata, oppure va registrata la durata di ogni passo. Il documento deve dire cosa promette.
- **Mosse del giocatore:** per ripetere una regata vanno registrati i comandi a ogni passo (barra, scotta, Maiusc, Z, A). Senza questi S10 non si può eseguire.
- **L'esito misurato su 25 s insegna il contrario sui salti di vento:** virare su uno scarso costa subito e rende dopo minuti. Ogni argomento ha bisogno del suo metro e della sua finestra (per i salti, la strada dopo 60-90 s).
- **Il generatore va passato come argomento** a chi lo usa, mai messo al posto di `Math.random` per tutta la pagina: `disegno.js:146` lo consuma a ogni fotogramma (tremolio). `step()` è puro, quindi `startTime` e `glideY` non consumano numeri.
- **Le raffiche nascono attorno al giocatore** (`spawnGust`): se in una ripetizione il giocatore va altrove, cambia il vento di tutti. Conta se i tornei avranno raffiche.
- **Le istantanee non devono condividere oggetti con lo stato vivo**, altrimenti la seconda ripetizione parte da uno stato alterato. Riferimenti da ricollegare al ripristino: `S`, `ctl` e anche `wake` (`R.boats[0].wake`). Gli avversari hanno campi propri (`waitX`, `goStart`, `simT`, `glAt`, `glY`, `holdA`, `hist`): si copia tutta la barca.
- **Stato fuori da `R` e `S`:** tasti tenuti, barra lenta o veloce, Z, `reg`, `opt` (livello degli avversari, conto alla rovescia), valori del laboratorio.
- **`hist`** va tagliata all'istante del ripristino e copiata (`quando()` vuole tempi crescenti); la ripetizione non deve allungare quella della regata vera.
- **La ripetizione non deve scrivere niente:** `progress.best`, `recSave()` (fantasma), `progress.done`, `progress.clean`, `R.pend`/`progress.race`, `regAdd`, `raceResults()`, `recStart`; nei tornei, anche classifica, scarto e punti. Controllo: localStorage identico byte per byte.
- **Campionamento:** con istantanee ogni 0,5 s un contatto (sotto 4,2 m) può sembrare un passaggio senza tocco. Posizioni di tutte le barche ogni 0,1 s, istantanee complete ogni 0,5 s.
- **Sorpassi:** `ranking()` oscilla fra due barche vicine. Ci vuole un'isteresi (il sorpasso conta se l'ordine resta tale per 10 s).
- **Domande sulle mure:** si escludono i contatti con una barca in virata o in poppa piena (mure dal lato del boma). Con le stesse mure il «sopravento» si legge col vento medio (`toWF` usa `env.twd`): con salti di 12-15° può essere sbagliato, quindi il momento va segnalato come giudizio semplificato oppure escluso. Con le raffiche `contacts()` legge il vento nel punto del giocatore (difetto noto dalla 1.0.1).
- **La partenza anticipata ha due cause** nel codice (oltre la linea allo sparo; passata fuori dagli estremi): servono due domande diverse.
- **Argomenti a zero casi:** con 10 nodi fissi e senza raffiche non si scuffia. S6 conta i casi argomento per argomento, con scenari costruiti come in `collaudo_registro.py`.
- **Rumore delle onde** (`gioco.js:702`, `S.noiseT`): gira solo nei passi delle lezioni con `yawNoise` (verificato qui), non in regata.
- **Incoerenze da sistemare:** le finestre di §9.3 e §9.7 non coincidono, e non si dice dove finisce ogni ripetizione; avviare una ripetizione non deve cancellare l'ultima regata; la ripetizione parte a gioco fermo con «Parti», come le prove; «coach» va definito (oggi c'è solo il registro degli errori).
- **Il percorso:** i tornei saranno a triangolo, mentre il codice presuppone il bastone (`leg` da 0 a 2, `strada()` vale `2 * R.up` all'arrivo, una boa sola in `targetOf`). Momenti del giro di boa, distacchi ed esito vanno costruiti sul triangolo.

**Criteri da rafforzare:**
- S1: contare istantanee ed eventi (più di 0); fare una contro-prova (un numero casuale in più deve dare differenze).
- S4: confrontare col testo serializzato al momento della cattura, dopo aver fatto avanzare la regata.
- S5: la barca si è mossa e la ripetizione è arrivata alla fine della finestra.
- S6: non deve contraddire il tetto di 6 momenti.
- S7: non deve essere circolare; serve un controllo indipendente (mure ricalcolate dal lato del boma).
- S2-S3: dire come si misura e mettere un tetto alla regata lunga.
- S8: caso peggiore dei testi.

**Da decidere con la proposta dei tornei:** quante regate si tengono (l'ultima o tutte e quattro); replay nei tornei del gioco libero o solo in carriera; punti dalle domande e dalle ripetizioni (§9.6), insieme ai meriti del torneo.

## 10. Modalità coach e registratore (decisione di Ale, 27 ottobre 2026)

**[deciso]** «Modalità coach» è il nome di tutto ciò che usa le regate registrate: momenti chiave, ripeti da qui, domande («perché la Rossa ha preso la penalità?») e analisi per il debugging. Il registratore parte da solo all'inizio di ogni regata e si spegne all'arrivo; il file contiene solo quella regata (oggi, con l'interruttore a mano, il file successivo contiene anche il precedente). Il tasto M resta. Nella navigazione libera, nelle prove e nelle lezioni non si registra niente, salvo registrazione forzata a mano.

**[aperto]** Dove stanno i file: memoria del browser (IndexedDB, ovunque, invisibile) per le ultime regate del coach, e una cartella scelta da Ale (File System Access, solo Chrome ed Edge, conferma a ogni sessione; da provare se funziona da file locale) come archivio per il debugging. Privacy: si registra sempre ma solo nel browser, da dichiarare con una riga. Da scrivere come fermata 1, con criterio di collaudo: 20 regate, nessun byte della regata precedente nel file successivo.

