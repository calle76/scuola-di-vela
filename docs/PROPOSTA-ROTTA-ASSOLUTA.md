# Proposta: due rotte ottimali, «dalla tua partenza» e «in assoluto» (fermata 1, 13 novembre 2026)

**Da dove nasce.**
- Lucio, 13 novembre: la rotta ottimale di oggi parte dal punto in cui il giocatore ha tagliato la linea. Sarebbe interessante una rotta «100% teorica», che dica anche il punto di partenza migliore.
- Ale, lo stesso giorno: «sarebbe bello avere informazioni su due rotte: la migliore regata che potevo fare e la migliore regata in assoluto; due tracciati che mettono a confronto la mia regata».

**Niente codice finché Ale non dà il via.**

## 1. Cosa c'è oggi (1.2.22-1.2.29)

La rotta ottimale (`PROPOSTA-ROTTA-OTTIMALE.md`, `js/rotta.js`) parte **dal punto e dall'istante** in cui il giocatore ha tagliato la linea:
- non giudica dove si è partiti sulla linea;
- non giudica il ritardo: se tagli la linea 10 s dopo lo sparo, anche lei parte 10 s dopo.

**La linea è perpendicolare al vento impostato, non a quello vero.** Nel gioco la linea non è mai storta di proposito, ma allo sparo il vento vero è spostato da oscillazione, salto e raffiche. Esempio, la regata di Ale del 12 novembre alle 22:48 (torneo, regata 1, vento impostato 45°):
- allo sparo il vento veniva da 40-41°, cioè 4-5° a sinistra: era favorito lo spillo;
- su 70 m di linea fanno circa 6 m di vantaggio al vento fra le due estremità;
- Ale è partito 12 m a sinistra del centro, 0,95 s dopo lo sparo;
- durante la regata il vento è andato fino a 28-29°.

## 2. Cosa vede il giocatore

Nella vista «Rotta ottimale» di fine regata, tre tracce invece di due:

| Traccia | Colore | Da dove parte |
| --- | --- | --- |
| la tua | blu (come oggi) | — |
| **migliore dalla tua partenza** | verde (la rotta di oggi) | dal tuo punto e dal tuo istante di taglio |
| **migliore in assoluto** | viola (nuova) | da un punto qualunque della linea, allo sparo |

Un segno ogni 30 s su tutte e tre le tracce, come oggi. Nel testo, tutti i tempi contati **dallo sparo**. Esempio:

> «Dallo sparo: migliore in assoluto 2:58, migliore dalla tua partenza 3:04, tu 3:05. In partenza hai perso 6 s (punto della linea e ritardo); dopo la partenza 1 s. La migliore in assoluto parte vicino allo spillo.»

Poi, come oggi, i secondi persi per lato e fino a due motivi.

**Cosa la rotta in assoluto non è** (detto anche nel gioco, insieme al «col senno di poi» di oggi):
- considera la barca **già lanciata a piena velocità** sulla linea allo sparo: in acqua si arriva accelerando;
- **ignora le altre barche**, e proprio l'estremità favorita è quella dove si affollano tutti. Le guide alla partenza consigliano di partire vicino all'estremità favorita, ma lontano dalla confusione (F86);
- non conosce il rischio di partenza anticipata.

## 3. Modello più semplice

**A. Cosa non cambia.** La registrazione del vento, la polare, i costi delle manovre (`T_VIR` 2 s, `T_ABB` 1 s), il calcolo dei lati dopo il primo e la rotta «dalla tua partenza». La rotta di oggi resta uguale al bit.

**B. La partenza libera.** Il primo fronte delle isocrone non è più un punto solo:
- è fatto di **tutti i punti della linea allo sparo** (t = 0), uno ogni metro;
- si escludono 2 m vicino allo spillo e alla barca del comitato;
- le mure sono libere e senza costo di manovra.

Dal secondo passo in poi il calcolo è quello di oggi. Ogni punto del fronte si porta dietro il suo punto di partenza: alla fine si sa da dove è partita la rotta più veloce.

**C. Il punto delicato.** Oggi, per ogni direzione, il fronte tiene solo il punto più lontano dal punto di partenza. Con una partenza lunga 66 m serve un'origine comune. Propongo **un punto 100 m sottovento al centro della linea**: da lì tutti i punti della linea stanno in direzioni diverse, e «più lontano» vuol dire ancora «più avanti verso il vento». È una scelta nostra e potrebbe scartare la partenza giusta: la controlla il criterio A2 contro un calcolo lento ma sicuro (la forza bruta).

**D. Secondi persi in partenza** = (rotta dalla tua partenza) − (rotta in assoluto). Dentro ci sono insieme il ritardo e il punto della linea. Separarli richiede una terza rotta (dal tuo punto, ma allo sparo): la tengo fuori, per ora.

**Costanti nuove (ipotesi nostre):**
- passo dei punti sulla linea: 1 m;
- margine dalle estremità: 2 m, come `ROT_BOA`;
- origine del fronte: 100 m sottovento al centro;
- forza bruta di controllo: 14 partenze singole, una ogni 5 m.

**Cosa non si tocca:** la fisica, il vento, gli avversari, le regate, la misura degli avversari (`rotLatiBarca`).

## 4. Criteri (soglie nostre, scritte prima di misurare)

Misura col pilota sulle 4 regate del torneo, avversari principianti ed esperti. Scelta sui semi 2001-2030, conferma sui semi 2031-2060 (nei documenti compaiono semi fino a circa 1930; prima di cominciare ricontrollo che questi siano nuovi). Solo la barca del giocatore. Almeno 200 regate per gruppo di semi, e si riporta quante sono.

- **A1, l'assoluta non è peggio:** la rotta in assoluto è al massimo 1 s più lenta di quella dalla tua partenza in almeno il 99% delle regate, mai oltre 3 s. Non può essere 0 su 0: si riporta su quante regate.
- **A2, il fronte non perde la partenza giusta:** la rotta in assoluto è al massimo 1 s più lenta della migliore delle 14 partenze singole (forza bruta) in almeno il 98% delle regate, mai oltre 3 s.
- **A3, tempo di calcolo:** le due rotte insieme in al massimo 3 s per regata su questo PC, in Chromium e in Firefox. Oggi una rotta sola costa circa 1,1 s. Il tempo sul PC di Ale si riporta.
- **A4, non è fantascienza:** il vantaggio mediano della rotta in assoluto sulla barca più veloce della regata è al massimo il 25% (oggi, dalla partenza di ciascuno: 12-13%).
- **A5, non-regressione:** la rotta dalla tua partenza è identica alla 1.2.29 sugli stessi semi (0 differenze); `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici.
- **A6, pannello e schermata** a 1360x650 senza pixel in eccesso: oggi la moviola sfora di 20 px, difetto vecchio non legato alla rotta, e non deve peggiorare.
- **Da riportare, senza soglia:**
  - in quante regate con il vento girato di almeno 3° allo sparo la rotta in assoluto parte nella metà favorita della linea. Può non succedere per buone ragioni, per esempio una raffica dall'altra parte;
  - su 10 regate guardate da me con le immagini: tracce, punto di partenza e testo devono corrispondere.

## 5. Rischi

- **Partire alla perfezione è impossibile:** «in partenza hai perso 6 s» per una barca che in realtà ha fatto un'ottima partenza può scoraggiare. Il testo dice sempre «barca lanciata, senza le altre barche».
- **Il fronte con origine lontana** può scegliere male (lo controlla A2). Se A2 non passa, il ripiego è la forza bruta con meno punti più un affinamento intorno al migliore, misurandone il tempo (A3).
- **Il PC di Ale è lento:** con due rotte, il tempo di attesa raddoppia circa. Se pesa, la seconda si calcola mentre si guarda la prima.
- **Tre tracce sovrapposte** nella prima bolina possono confondere: colori distinti e una legenda nel testo.

## 6. Cosa serve da Ale

1. **Il via.**
2. **I nomi:** propongo «migliore dalla tua partenza» e «migliore in assoluto».
3. **Separare ritardo e punto della linea** nei secondi persi in partenza (una terza rotta, circa 1 s di calcolo in più): adesso o più avanti? Propongo più avanti.

## 7. Costo

Circa una giornata:
- fronte di partenza e forza bruta di controllo (mezza);
- misura A1-A5, schermata e testo (mezza).

## Fonti

- F86 (OneSails, «La partenza in regata»): partire vicino all'estremità favorita ma lontano dalla confusione; misurare quanto la linea è storta rispetto al vento. È una lista di metodo: non spiega come capire quale estremità è favorita.
- Che l'estremità più al vento sia quella favorita è geometria (la linea storta rispetto al vento), non un'affermazione nautica da verificare. Le lezioni del gioco non la usano ancora.

## 8. Versione semplice, idea di Ale (14 novembre 2026, sera; fermata 1)

Ale: «per l'idea della rotta ottimale direi che potrebbe bastare la posizione di partenza ideale e la direzione». Al posto di una terza traccia intera:

**Cosa vede il giocatore.** Nella vista «Rotta ottimale», sulla linea di partenza:
- un **segno nel punto ideale della linea**, cioè il punto da cui, allo sparo, si sarebbe arrivati prima alla boa di bolina;
- una **freccia corta con la direzione ideale** di partenza, cioè le mure con cui partire;
- una riga nel testo, per esempio: «Partenza ideale: vicino allo spillo, mure a dritta. Da lì, alla boa 1 si arrivava 7 s prima che dal tuo punto». Se il tuo punto era già quello giusto, lo dice.

La traccia verde «dalla tua partenza» e la tua blu restano come oggi.

**Modello più semplice.** Niente fronte di partenza nuovo (§3 B-C), che era la parte delicata.
- Si usa il calcolo di oggi, quello che fa la rotta verde dal tuo punto, partendo allo sparo da **7 punti della linea**, uno ogni 10 m da un capo all'altro, solo fino alla boa 1.
- Il punto ideale è quello col tempo più breve alla boa 1, e la direzione è quella del primo bordo della sua rotta.
- Come dal §2, la barca si considera già lanciata allo sparo, e le altre barche non esistono: va detto nel testo.

**Costanti nuove (nostre):** 7 punti, 10 m di passo; solo il primo lato.

**Criteri (soglie nostre, scritte prima di misurare):**

| # | Criterio | Soglia |
| --- | --- | --- |
| P1 | Il punto ideale non è peggio del tuo | in 100 regate col pilota: tempo alla boa 1 dal punto ideale ≤ tempo dal punto del giocatore (stesso calcolo, stesso istante), 100 su 100 |
| P2 | Il metro funziona | con la linea storta apposta di 10° (vento girato di 10° prima dello sparo, 20 regate), il punto ideale è all'estremità più al vento in almeno 18 su 20 (geometria) |
| P3 | Costo | il calcolo in più dura al massimo 1 s in Chromium e Firefox |
| P4 | Niente cambia nel resto | rotta verde, fili e «dove hai perso» identici a prima; impronta del guardiano identica |
| P5 | Pannello | 0 px di eccesso a 1360×650 con la riga in più |

**Costo:** meno di metà della versione completa, circa mezza giornata.

**Cosa serve da Ale:** il via, e quando farla. Consiglio: dopo il nazionale, insieme ai punti da sistemare.

## 9. Lucio vuole anche la rotta intera (14 novembre 2026, sera; fermata 1)

Ale: «Lucio vuole tutta la rotta ideale oltre alla partenza ideale». Si uniscono il §8 e la proposta originale, ma senza la parte delicata del §3 (B-C):

**Cosa vede il giocatore.** Nella vista «Rotta ottimale»:
- il segno del punto ideale della linea e la freccia della direzione, come nel §8;
- **una terza traccia, viola: la rotta migliore intera**, dallo sparo e dal punto ideale fino all'arrivo, con i segni ogni 30 s e, come per la verde, i fili ogni minuto verso la tua barca;
- nel testo, i tempi dallo sparo, per esempio: «Migliore in assoluto 2:58, migliore dalla tua partenza 3:04, tu 3:05: in partenza hai perso 6 s, dopo 1 s».

**Modello.**
1. Come nel §8: 7 punti della linea, uno ogni 10 m, allo sparo; per ciascuno la rotta di oggi fino alla boa 1; si sceglie il più veloce.
2. Da quel punto si calcola la rotta intera, una volta sola, con lo stesso calcolo della verde.

Il punto migliore fino alla boa 1 potrebbe non essere il migliore sull'intero percorso. Dopo la boa 1 le rotte ripartono tutte dalla stessa boa, quindi la differenza dovrebbe essere piccola: lo misura A2.

**Criteri** (quelli del §8, più questi; soglie nostre):

| # | Criterio | Soglia |
| --- | --- | --- |
| A1 | La viola non è mai più lenta della verde | tempo dallo sparo della viola ≤ quello della verde (che parte dal tuo punto e dal tuo istante), in 100 regate su 100 |
| A2 | Scegliere sulla boa 1 basta | in 20 regate, calcolando la rotta intera da tutti e 7 i punti: il punto scelto è il migliore sull'intero percorso, o al massimo 1 s più lento del migliore, in 18 su 20 |
| A3 | Costo | 7 rotte fino alla boa 1 più una intera: al massimo 2 s in Chromium e Firefox |

**Cosa dire nel gioco** (§2): la viola considera la barca già lanciata allo sparo e ignora le altre barche, proprio dove all'estremità favorita ci si affolla.

**Costo:** circa una giornata, come la proposta originale, ma con il rischio più basso.

**Cosa serve da Ale e Lucio:** il via, e quando farla (consiglio: subito dopo il nazionale).

## 10. Esito (14-15 novembre 2026, notte): 1.2.40 fatta, NON chiusa

Via di Ale del 14 notte («sì via alla rotta intera»). Ramo `rotta-assoluta`, `tests/collaudo_rotta_assoluta.py` (nuovo). Le 4 regate del torneo col pilota, semi 2401-2425 (mai usati prima; dispari principianti, pari esperti; ogni regata col suo sorteggio), 100 regate: **97 misurate**, 3 senza il pulsante «Rotta ottimale» (sotto).

| # | Esito | Soglia |
| --- | --- | --- |
| P1 | punto ideale non peggio del tuo alla boa 1: **90 su 97**; il peggiore **+0,46 s** | 100 su 100 ✗ |
| P2 | linea storta di 10°: punto ideale all'estremità più al vento **20 su 20** (vedi sotto) | 18 su 20 ✓ |
| P3 | i 7 tratti fino alla boa 1: al massimo **3,6 s** in Chromium, **4,2 s** in Firefox (8 regate) | 1 s ✗ |
| P4 | rotta verde, «dove hai perso» e fili **identici** al codice di prima in 97 regate su 97; impronta del guardiano `2c0e3804a20d`; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici | ✓ |
| P5 | 0 px di eccesso a 1360×650 con e senza barra; la barra della moviola dentro la finestra | ✓ |
| A1 | viola non più lenta della verde: **96 su 97**; l'unica, **+0,04 s** | 100 su 100 ✗ |
| A2 | scelta sulla boa 1 entro 1 s dal migliore sull'intero percorso: **17 su 20**; le 3 fuori perdono **2,1**, **1,4** e circa **1,0 s** (appena sopra la soglia) | 18 su 20 ✗ |
| A3 | tutta la rotta in assoluto: al massimo **4,0 s** in Chromium, **4,3 s** in Firefox | 2 s ✗ |

Il PC del collaudo è quello di Ale.

**Perché P1 e A1 non passano.** I 7 punti stanno a 10 m l'uno dall'altro: il tuo punto di partenza può cadere fra due di loro ed essere un po' migliore di tutti e 7. Succede in 7 regate su 97, al massimo per mezzo secondo. Quando succede, il testo dice «in partenza non hai perso niente» (sotto mezzo secondo non si conta).

**Perché P3 e A3 non passano.** Ogni tratto fino alla boa 1 costa circa mezzo secondo, come la rotta verde, e sono 7. Ho accelerato il calcolo senza cambiare i risultati (la verde è identica al bit, P4): i punti nuovi si creano solo se servono, la riga della polare si riusa. Nelle prime prove (4 regate, prima delle accelerazioni) i 7 tratti costavano circa 3,4 s; dopo, **3,1 s di media** su 97 regate (tutta la rotta 3,6 s). Il confronto è su regate diverse, quindi il guadagno è misurato male; in ogni caso non basta.

**P2, cosa è successo prima del 20 su 20.**
1. La prima prova, col vento vero del torneo girato di 10°, dava 0 su 6 con 14 regate non misurate: salti e raffiche spostano il vento allo sparo di quanto lo giravo io, e il pilota, col vento girato, spesso non arriva. Non misurava la geometria che il criterio dice; rifatta con vento costante e calcolando la rotta senza aspettare il pilota.
2. Con vento costante dava ancora 0 su 20, e c'era un errore mio nel codice nuovo: i 7 punti seguivano il vento impostato invece della linea vera. Nel gioco normale il vento impostato non cambia, quindi era invisibile, ma era sbagliato: ora i punti stanno fra spillo e comitato. Rifatte le 100 regate: stessi numeri.
3. Detto chiaro: con vento costante le 20 regate sono in pratica **2 situazioni** (vento girato di +10° e di −10°), ripetute.

**Trovato strada facendo:** in 3 regate su 100 (semi 2415 R3 e R4, 2420 R4) il pulsante «Rotta ottimale» non compare, anche col codice della 1.2.39: il pilota arriva, il taglio della linea è registrato. Causa non cercata: va in `DA-FARE.md`.

**Strade per Ale:**
- **Tempo (P3, A3):**
  - **a. (consiglio)** mostrare subito la verde e aggiungere la viola quando è pronta, 3-4 s dopo, con la scritta «sto calcolando la migliore in assoluto»: l'attesa sparisce, ma il calcolo dura uguale e P3-A3 restano dichiarati. Costo piccolo;
  - b. calcolare i 7 tratti in parallelo sui processori del PC (Web Worker): stessi risultati, tempo forse sotto 1-1,5 s sul tuo PC (6 processori), da verificare anche aprendo il gioco come file. Circa mezza giornata;
  - c. lasciare l'attesa com'è.
- **P1, A1, A2:** dichiararli (scarti piccoli: mezzo secondo al massimo, una regata su 97 per la viola), oppure punti più fitti sulla linea, che però costano altro tempo.

## 11. Decisione di Ale e chiusura (15 novembre 2026)

Ale: «è solo questione di attendere il tracciato ideale? ma non è un problema. si potrebbe avere anche un tasto "vuoi la rotta" e si evita di aspettare»; poi «sì vai così, con il tasto». **1.2.40 chiusa con P1, A1, A2, P3 e A3 dichiarati** (numeri nel §10).

**Il tasto.** «Rotta ottimale» si apre come prima, con verde e blu e senza attese. Nella barra c'è «Migliore in assoluto (V)»: col pulsante o col tasto V compare «Sto calcolando la migliore in assoluto: qualche secondo…», poi la viola, il punto ideale e la riga nel testo. Si calcola una volta per regata; poi il pulsante sparisce.

Criteri del tasto (soglie scritte prima di misurare: tutte le regate):

| # | Esito | Soglia |
| --- | --- | --- |
| K1 | aprendo la rotta la viola non si calcola e il pulsante c'è: **40 su 40** (Chromium), **8 su 8** (Firefox) | tutte ✓ |
| K2 | «Sto calcolando» mostrato prima del calcolo: **40 su 40**, **8 su 8** | tutte ✓ |
| K3 | dopo il calcolo, testo con la partenza ideale e pulsante nascosto: **40 su 40** (20 col tasto V), **8 su 8** (4 col tasto V) | tutte ✓ |
| P4 | verde, «dove hai perso» e fili identici al codice di prima: 40 su 40 | ✓ |
| P5 | 0 px di eccesso anche col pulsante in più | ✓ |

Pagina senza `#collaudo` in Chromium e Firefox: 1.2.40, 0 errori. `collaudo_rotta_leggibile --semi 2` e `collaudo_moviola 8` OK.

**Corretto strada facendo (tutti miei, trovati dai collaudi prima della chiusura):**
- il pulsante era collegato a una funzione di `rotta.js`, che si carica dopo `moviola.js`: la riga si fermava con un errore;
- correggendolo, un commento messo a metà riga aveva spento anche «Chiudi» e i pulsanti dei segni della moviola: con «Chiudi» la moviola non si chiudeva più. Trovato da `collaudo_rotta_leggibile` (8 su 8 con `main`, 2 su 8 col ramo), corretto: 8 su 8;
- la moviola riscrive il titolo a ogni fotogramma, quindi «Sto calcolando» spariva subito: il primo metro di K2 (leggere il testo dopo il clic) non lo poteva vedere, perché la pagina è ferma mentre calcola. Il metro nuovo registra il testo a ogni fotogramma e l'ha visto; ora la scritta resta fino alla fine del calcolo.

**Nel giro dei collaudi:** `collaudo_rotta_assoluta.py --regate 4 --dichiarati` (P1, A1, A2, P3, A3 solo riportati).
