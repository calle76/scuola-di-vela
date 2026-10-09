# Piano generale: livelli, ruoli, bravura, barche

Bozza del 9 ottobre 2026, da approvare. Nasce dalla chiacchierata del 9 ottobre sera e dai documenti `VISIONE-LIVELLI-E-CARRIERA.md`, `ROADMAP.md`, `RICERCA-DATI-IMBARDATA.md`, `RIPARTI-DA-QUI.md`.

Stato dei punti (come nella visione):

| Stato | Significato |
| --- | --- |
| **[deciso]** | Scelta presa. |
| **[proposta]** | Idea da discutere. |
| **[provvisorio]** | Numero o regola da tarare giocando. |
| **[aperto]** | Da decidere. |
| **[da verificare]** | Affermazione da controllare su una fonte. |

Se questo documento e `VISIONE-LIVELLI-E-CARRIERA.md` o `ROADMAP.md` dicono cose diverse, vale questo, **dopo l'approvazione**; i punti che cambiano sono elencati nel §12 e andranno riportati negli altri due file.

Nota: i principi di `docs/PROGETTO.md` (tutto sempre giocabile, simulatore plausibile, confini legali prudenti, solo computer) sono ripresi dalle istruzioni di lavoro. `PROGETTO.md` non è stato riletto per scrivere questa bozza.

## 1. Principi che restano

- Progetto personale non commerciale.
- Tutto sempre giocabile: nessun contenuto è bloccato nel gioco libero. Lo sblocco per livelli vale solo nella carriera.
- Simulatore plausibile: dove manca una fonte, la costante è una **taratura dichiarata**, mai presentata come dato.
- Confini legali prudenti: nomi generici, nessun marchio, regole di regata parafrasate, dati esterni solo con licenza libera e citazione.
- Solo computer.
- Ogni modifica si collauda guidando davvero la barca; ad ogni versione si aggiorna il `CHANGELOG.md`.
- Le risposte di un'IA non sono fonti; una sola fonte non basta per «verificato».

## 2. Definizioni

| Termine | Significato |
| --- | --- |
| **Competenza** | Una cosa che si comanda: barra, randa, fiocco, gennaker, tattica. |
| **Ruolo** | La posizione di una persona a bordo, con una o più competenze. **[deciso]** Bravura, punteggi e mini tornei si contano per ruolo. I ruoli non superano mai le persone. |
| **Personaggio** | Un membro dell'equipaggio, con pregi e difetti e una bravura per ruolo. |
| **Bravura del personaggio** | Quanto bene un personaggio svolge un ruolo. Cresce ogni volta che lo svolge, lo muova il giocatore o il computer. **[deciso]** |
| **Meriti del giocatore** | I punteggi che servono a passare di livello. Salgono **solo** da ciò che fa il giocatore. **[deciso]** |

## 3. Livelli, persone e ruoli

| Livello | Barca (categoria) | Persone | Ruoli | Stato |
| --- | --- | --- | --- | --- |
| 1 | Deriva, solo randa | 1 | 1: barra + randa | esiste |
| 2 | Randa + fiocco | 2 | Timoniere (barra); chi regola le vele (randa + fiocco) | prototipo del fiocco |
| 3 | Con gennaker | 2 | Gli stessi due; il gennaker va a chi regola le vele | proposta |
| 4 | Equipaggio da tre | 3 | Timoniere, trimmer, tattico | aperto |
| 5 | Catamarano | da definire | da definire | direzione |
| 6 | Cabinato | da definire | da definire | direzione |

- **[deciso]** Ruoli del livello 2 con la divisione «barra / vele» (opzione A del 9 ottobre): allinea il livello 2 al livello 4 (timoniere, trimmer, tattico).
- **[deciso]** Al livello 1 si possono registrare nel diario errori e tempi separati per barra e randa, ma sono dettagli interni a un solo ruolo.
- **[aperto]** I livelli 5 e 6: l'ordine tra catamarano e cabinato non è fissato. Sono una direzione, non un impegno.
- **[aperto]** La barca vera di ogni livello. Qui sono indicate solo per categoria (vedi §9).
- Il tattico arriva al livello 4: su una barca a due la tattica la fa chi sta al timone. **[da verificare]** con un velista.
- Altri ruoli possibili, non inseriti: prodiere separato (dal livello 3 se serve), navigatore/stratega, peso dell'equipaggio come ruolo. Uomo d'albero, pitman e grinder solo in un eventuale cabinato da regata. **[proposta]**

### Equipaggio

- Il giocatore sceglie il compagno del livello 2 da una **rosa** di candidati, ognuno con un pregio e un difetto (per esempio preciso ma lento, veloce ma impreciso). **[proposta]**
- Ogni personaggio **parte già con una bravura** di base: nessuno è inutile, nessuno è il migliore in assoluto. **[deciso]**
- Quando arriva il terzo (livello 4): si aggiunge il terzo ai due già cresciuti, oppure si rifà la scelta? **[aperto]**. Proposta: si aggiunge il terzo, così l'equipaggio cresce con il giocatore.
- Personaggi inventati, senza somiglianze con persone reali e senza marchi.

## 4. Bravura e meriti

### La crescita dei personaggi

- Ogni personaggio ha una bravura per ruolo. Cresce a fine prova, anche quando il ruolo è guidato dal computer.
- Per il computer basta una regola di contabilità, non una simulazione: punti in base al risultato della barca e agli errori attribuiti a quel ruolo. Il registro dovrà avere il campo «ruolo responsabile» (già previsto nella visione). **[proposta]**
- Rendimenti decrescenti: oltre una certa bravura i punti per prova diminuiscono. Serve a evitare che si lasci giocare il computer solo per far crescere l'equipaggio. **[proposta]**
- Più bravura vuol dire effetti visibili (errori più rari, manovre più pulite), non solo un numero. **[proposta]**

### Una scala assoluta

- Un'unica scala di bravura per tutti i livelli. Il livello di riferimento degli avversari sale di livello in livello; un equipaggio appena sufficiente al livello 4 è debole perché il riferimento è più alto, non perché la scala cambia. **[proposta]**
- La scala e il livello degli avversari di ogni livello si scrivono **prima** di vedere i risultati. **[deciso]**

### I meriti del giocatore

Le quattro aree restano come nella visione: Abilità, Competizione, Conoscenza, Esperienza. Salgono solo da ciò che fa il giocatore. Un personaggio guidato dal computer può «superare la prova» e crescere, ma i meriti del giocatore non cambiano.

## 5. Passare di livello

```
prove, mini tornei, quiz, lezioni -> soglie per ogni ruolo + totale -> esame -> brevetto
```

- **[deciso]** Tutto ha una soglia, come la patente: si passa con il minimo, senza dover essere i migliori.
- **[deciso]** Servono **tutti i ruoli del livello** a livello sufficiente (non più «almeno due»).
- **[deciso]** L'esame resta obbligatorio e va superato. La soglia, il banco di 80-100 domande e il ripasso mirato restano come nella visione.
- **[deciso]** Il punteggio è una somma di componenti sufficienti: totale e minimi per area, più la soglia dell'esame.
- **[proposta]** Errori gravi tolgono punti, con una lista chiusa e valori fissi, scritti prima: rovesciare la barca, arrivare con un ritardo enorme, e simili.
- **[proposta]** I minimi devono poter essere raggiunti anche con un equipaggio debole (come nel livello 1: ultimo su quattro dà 2 punti e il minimo è 2). Il passaggio non deve mai dipendere dalla forza dell'equipaggio.
- La difficoltà crescente è una **conseguenza**, non un blocco: chi avanza con voti appena sufficienti ha un equipaggio più debole del riferimento e avversari ben addestrati, e perde più spesso. Libretto e istruttore devono mostrare «bravura del tuo equipaggio» contro «bravura degli avversari». **[proposta]**
- Le tabelle numeriche del livello 1 restano **[provvisorie]**. Con più ruoli vanno ricalcolate quando si costruisce il livello 2.

## 6. Mini tornei

- **[deciso]** Mini tornei, più brevi del torneo da 4 regate previsto finora, per non appesantire il gioco.
- Il ruolo è scelto all'iscrizione e resta bloccato (regola esistente). Per coprire tutti i ruoli servono quindi almeno tanti mini tornei quanti sono i ruoli.
- **[aperto]** Quante regate per mini torneo, se c'è uno scarto, come si conta la Competizione (un torneo per ruolo, oppure un totale).
- Categorie con condizioni diverse (vento leggero, vento teso, raffiche, salti di vento) come nella visione. I salti di vento arrivano per ultimi (richiedono un vento che oscilla).
- Prerequisito: avversari affidabili su più regate.

## 7. L'istruttore

- Dice dove si è perso più tempo e quali errori si fanno, con i numeri del registro. **[deciso, già discusso]**
- Mostra il confronto tra bravura dell'equipaggio e riferimento degli avversari (§5). **[proposta]**
- Commento dei replay e confronto con il «fantasma» dalle registrazioni. **[proposta]**
- Non compare nei titoli dei brevetti: «istruttore» è una qualifica federale.

## 8. Contenuti per livello (direzione)

- **Livello 1** (esiste): assetto delle vele, andature, virata, strambata, scadere, orziera, arresto, raffiche, barra, randa, prove, regate, esame e brevetto del livello 1 da fare.
- **Livello 2**: fiocco, coordinamento a due, ordini, virata e strambata a due, raffiche in due, occhi dell'equipaggio. **Le lezioni 2.x della visione vanno riscritte** con la divisione «timoniere / chi regola le vele»: la 2.2 diventa regolazione di randa e fiocco insieme. Il fiocco a collo si insegna come errore di coordinamento, non come effetto fisico (il prototipo non lo modella).
- **Livello 3**: vela di portanza, alzata e ammainata, regolazione, strambata, planata, strumenti e angoli limite. Livello più difficile da modellare: prima un prototipo isolato.
- **Livello 4**: VMG e layline, partenza (sequenza, linea, lato favorito), precedenze (regole 10, 11, 14, 18: titoli **[da verificare]**), cono d'ombra delle vele sopravento, campo di vento esteso, ruolo del tattico.
- **Livelli 5-6**: vento apparente dominante, scuffia diversa; inerzia, mare, correnti.

Fattibile senza dati nuovi: VMG, layline, partenza, punteggi, ruoli, sblocchi, esame. Il cono d'ombra è una regola di gioco ispirata alla fisica, da dichiarare come taratura (nessuna fonte con numeri trovata).

## 9. Barche e documentazione

**Metodo [deciso]:** prima la documentazione, poi la barca. La barca di ogni livello si sceglie dopo, in base ai dati. Nel frattempo i livelli indicano solo la categoria («deriva a due»), con la porta aperta a un altro tipo di barca dal livello 2.

**Griglia (una etichetta per casella: misurato / regolamento di classe / stimato / assente):**

1. lunghezza al galleggiamento, massa, superficie di randa e fiocco
2. posizione di albero e deriva (da cui l'anticipo)
3. raggio di giro d'imbardata (inerzia)
4. area e allungamento del timone, angolo di stallo
5. polare di velocità
6. virata misurata: tempo, velocità persa, velocità di rotazione
7. effetto del fiocco sul centro velico

**Soglia fissata prima [deciso]:** una barca è «ben documentata» se ha le righe 1, 2 e 5 come misurato o da regolamento e almeno una tra 3, 4, 6.

**Come si usa:**

- Sessione di ricerca a **tempo limite** (una sessione). Dove la griglia resta vuota, la costante è una taratura dichiarata e si prosegue.
- Nel gioco ogni numero della scheda barca ha una di tre etichette: *fonte*, *stima da regolamento di classe*, *taratura di gioco*.
- Il piano dei livelli e il fiocco nel livello 2 **non** aspettano questa ricerca.

**Cosa blocca la mancanza di dati:** differenza fisica fine tra barche, stallo del timone, effetto vero del fiocco sul centro velico, planata. Il motore resta parametrico; le barche si differenziano per lunghezza, massa, superfici, albero e velocità relativa, tutti numeri ricavabili dai regolamenti di classe come stima.

**Fonti consultate o da consultare**

- Verificato nell'esistenza: lavoro Keuning, Vermeulen, de Ridder (2005) sulla manovra e virata di uno yacht (PDF non letto; riguarda uno yacht, serve come scala e per la struttura del modello); Python-VPP (yacht, 3 gradi di libertà, MIT); ORC (solo equilibrio stazionario); Airfoil Tools (profili NACA, per la questione dello stallo, con Reynolds basso da dichiarare).
- **Portsmouth Yardstick** (RYA, verificato il 9 ottobre): numeri di handicap tra classi diverse, aggiornati ogni anno con i risultati; la lista 2026 include anche i multiscafi. Misura una velocità relativa media su equipaggi e condizioni diversi, non la fisica. **Licenza d'uso non verificata**: prima di usare i numeri va chiarita. Per ora solo ordini di grandezza.
- Regolamenti di classe delle derive (masse, lunghezze, albero, superfici): da cercare per le classi candidate.
- Libri (Marchaj, Larsson e Eliasson, Bethwaite): non comprare prima di aver visto l'indice; contenuto per le derive non confermato.
- Ricerche suggerite sul sito TU Delft (autore Keuning; «yaw balance»; «tacking»; «rudder» con «sailing yacht»; «added mass» con «yaw»; «dinghy»): se per «dinghy» non esce nulla, si annota, è un'informazione utile. Cosa estrarre: valore, unità, pagina, barca di riferimento.

**Testimonianze e divulgazione (etichettate come tali, non come fonti tecniche)**

- Lucio: su una barca grossa (tipo non ricordato), la barra tutta a fondo di colpo a velocità alta fa prendere un'imbarcata; piccole variazioni sono più efficaci e sicure; i movimenti ampi si fanno in manovra a bassa velocità. Sulla soglia di velocità: «dipende dal tipo di imbarcazione». Una persona, **non una deriva**.
- Articoli di SVN solovelanet e del Giornale della Vela (2022): una leggera tendenza a orzare da circa 8 nodi di vento è desiderabile; utile fino a circa 15 nodi, oltre diventa un freno; si regola con rake e potenza della randa. Senza fonti, cabinati, probabilmente non indipendenti: **una sola fonte debole**, non «verificato».

**Contraddizione aperta:** stallo del timone a circa 15° (F4) contro 30-35° (CFD). Possibile spiegazione (angolo del timone contro angolo d'incidenza dell'acqua): non risolta. Il timone massimo del gioco è 30°.

## 10. Comandi

Regola già decisa (7 ottobre, 0.19.2): per ogni ruolo il comando principale è su W S; la seconda coppia verticale (E D) solo se serve; A e Z liberi per funzioni speciali; Q è la vista; barra con ← →, Spazio, R e M invariati.

- **[aperto]** Nel ruolo «chi regola le vele» (livello 2): quale vela va su W S e quale su E D (randa o fiocco). Ordine dei cursori nel pannello come sulla barca vista dall'alto: fiocco in alto, randa nel mezzo, timone in basso.
- **[aperto]** A quale ruolo va il peso dell'equipaggio come comando (lezione sulle raffiche in due).

## 11. Ordine di lavoro proposto

Regola: due fermate per ogni compito di modellazione (proposta, poi implementazione dopo il via); un passo alla volta.

1. **Salvare** `docs/RICERCA-DATI-IMBARDATA.md` e questo piano (se non fatto), poi ricaricare nelle conoscenze del progetto.
2. **Registrazioni** delle lezioni: portarle in chat tutte insieme e leggerle.
3. **Esame e brevetto del livello 1**, con il sistema dei meriti provvisorio: chiude il livello.
4. **Fiocco nel gioco** (livello 2): porting dal prototipo (commit `e616212`, righe `// FIOCCO`), con le semplificazioni dichiarate. Insieme: definizione dei due ruoli (A), assegnazione dei tasti, riscrittura delle lezioni 2.x.
5. **Sessione di ricerca a tempo limite** sulla documentazione, per decidere le barche dei livelli 2 e 3 (e 4 se serve).
6. **Prototipo del livello 3** (gennaker e planata) prima di progettarne le lezioni; poi un prototipo per ogni livello successivo.
7. **Equipaggio del computer**: bravura, crescita, errori plausibili, registro con «ruolo responsabile».
8. **Mini tornei, libretto e istruttore.**
9. **Livello 4**: campo di vento esteso, partenza, precedenze, tattico, cono d'ombra.
10. **Carriera**: bivio, salvataggio proprio, importazione.

Il questionario al velista parte quando vuole Ale, senza contarci. Il Giornalino per Lucio resta una cosa simpatica da fare quando c'è tempo.

## 12. Cambiamenti rispetto a visione e roadmap

Da riportare in `VISIONE-LIVELLI-E-CARRIERA.md` e `ROADMAP.md` dopo l'approvazione:

1. «Per il brevetto servono almeno due ruoli» → **tutti i ruoli del livello**.
2. Via il bonus per il primo ruolo nuovo (tutti i ruoli sono obbligatori).
3. Ruolo = persona a bordo; livello 2 con due ruoli «timoniere / chi regola le vele» (prima: timoniere e prodiere, con la randa al timoniere e il fiocco al prodiere). Le lezioni 2.x e l'esempio dei comandi nella visione (§12) vanno rifatti.
4. Torneo da 4 regate con scarto → **mini tornei** (struttura aperta).
5. La bravura dei personaggi cresce anche quando li guida il computer, senza toccare i meriti del giocatore.
6. Scala di bravura assoluta, con avversari di riferimento per livello.
7. Livelli 5 e 6 nominati esplicitamente (catamarano, cabinato; ordine non fissato).
8. Barche per categoria finché la ricerca documentale non decide; il livello 3 su deriva è una proposta, non un impegno.

## 13. Decisioni aperte

1. Equipaggio al livello 4: si aggiunge il terzo o si rifà la scelta?
2. Mini tornei: numero di regate, scarto, conteggio della Competizione.
3. Tasti del ruolo «chi regola le vele»; ruolo del peso dell'equipaggio.
4. Valori della scala di bravura, dei rendimenti decrescenti, delle penalità per errori gravi.
5. Esito della ricerca documentale: derive per i livelli 2-3 oppure un altro tipo di barca.
6. Licenza d'uso dei numeri Portsmouth.
7. Contraddizione sullo stallo del timone (15° contro 30-35°).
8. Aiuti in carriera: valgono per i meriti? (già aperta)
9. Quiz con domande in più perché il ripasso non coincida con l'esame. (già aperta)

## 14. Rischi

- **Mole di lavoro:** ruoli, personaggi, tornei e barche insieme sono tanto per un progetto personale. Un livello completo vale più di quattro abbozzati.
- **«Grind»:** la crescita della bravura può diventare ripetizione per accumulare. Rendimenti decrescenti e soglie scritte prima.
- **Tarature a mano:** vanno dichiarate nel manuale come regole di gioco ispirate alla fisica.
- **Livello 3 (gennaker e planata):** il più difficile da modellare, e quello con meno dati.
- **Tastiera:** un giocatore non può muovere più persone; i ruoli del computer devono sbagliare in modo plausibile.
