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
