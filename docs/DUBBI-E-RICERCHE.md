# Dubbi e ricerche

Aggiornato al 5 ottobre 2026. È l'elenco vivo dei piccoli dubbi e delle idee rimandate, da riprendere in sessioni di ricerca dedicate. Non serve risolverli per andare avanti: il progetto procede, e ogni semplificazione è dichiarata (vedi `FISICA-E-TARATURE.md`, sezione «Stato finale del prototipo del fiocco», e `MANUALE-bozza.md`).

Come si usa:

- Ogni voce ha uno **stato** e il **tipo di sessione** che serve per chiuderla: *web* (ricerca online), *libro* (un testo da consultare), *video* (guardare o misurare un video: lo fa Ale; non c'è una persona esperta a cui chiedere), *codice* (una sessione di Claude Code), *prova* (giocare e guardare).
- Quando un dubbio si chiude, non si cancella: si barra e si scrive la data e la fonte.
- Le affermazioni nautiche del gioco vero stanno in `CONTENUTI-DA-VERIFICARE.md`; qui ci sono quelle che hanno un seguito di lavoro.
- Una sola fonte non basta per dire «verificato».

## Da fare per primi (proposta di priorità)

1. **Chiudere con fonti le righe aperte di `CONTENUTI-DA-VERIFICARE.md`** (sessioni *web*, *libro*, *video*): ogni riga si chiude con una fonte citata, oppure resta una scelta dichiarata. Non ci sarà una persona esperta che le legga tutte (13 ottobre 2026).
2. **Controllare la fonte sul momento di imbardata** (sessione *web*): il centro velico a circa 0,2 m a prua del centro scafo, il momento orziero che cresce con lo sbandamento, lo scafo sbandato che orza da solo. Due affermazioni risultano nel testo, la terza solo in parte.
3. **Leggere l'articolo di Binns, Bethwaite e Saunders del 2002** (sessione *web*): previsione di velocità per una deriva monoposto; serve per calibrare la polare.
4. **Studiare By The Lee** (sessione *codice*, sola lettura): come un simulatore dinamico organizza equilibrio, centro velico e smorzamento.
5. **Titoli delle regole di regata 10, 11, 14 e 18** (sessione *web*): prima di scrivere le domande dell'esame.

## 1. Lezioni e regate del gioco vero

Lista completa in `CONTENUTI-DA-VERIFICARE.md`. Quelle che hanno un dubbio dichiarato:

| Dubbio | Stato | Per chiuderlo |
| --- | --- | --- |
| Strambata e abbattuta: sono sinonimi? Alcuni testi chiamano abbattuta la manovra voluta e strambata quella involontaria | Aperto | *libro* o *video* |
| Posizione dei filetti sulla randa: sulla balumina o vicino all'inferitura? La regola di lettura è confermata, la posizione no | Aperto | *libro* o *video* |
| Colori dei filetti (rosso a sinistra, verde a destra): scelta del gioco | Dichiarata, da confermare | *libro* o *video* |
| Da quale andatura i filetti della randa non si usano più, e su che cosa si regola la vela al loro posto. Dalla 0.17 il pannello dice «in poppa i filetti non servono» a scotta tutta lascata | Aperto | *libro* o *video* |
| Il limite oltre cui nel gioco i filetti dritti non esistono più (**112° di vento apparente**, cioè circa **135° di vento reale**) è figlio di una barca lenta: il boma arriva al massimo a 85° (`BOAT.maxBoom`) e oltre quell'angolo l'incidenza supera lo stallo. Su un 470 le fonti danno circa **75° apparenti a 120° reali** (F4), contro i **97,5°** del nostro motore: una barca più veloce tiene il vento apparente molto più avanti e i filetti lavorano più a poppa. Da capire se il confine va spostato, e se per farlo serve una barca più veloce o un limite di scotta diverso | Aperto | *libro* o *video*, poi *codice* |
| Comandi di manovra («Pronti a virare?», «Viro!»…): varianti tra scuole | Aperto | *libro* o *video* |
| Orziera: verificare il termine usato nell'esercizio di rotta | Aperto | *libro* o *video* |
| Definizione di «scadere» da confermare con un velista: nel glossario e nella lezione 5 (0.17) dice che una barca ferma o in retromarcia vicino al vento gira da sola, lentamente, allontanandosi dal vento. Comportamento già dichiarato come semplificazione in `FISICA-E-TARATURE.md`, non risulta una fonte pubblica specifica sul verso o sulla velocità di rotazione | **Chiuso il 5 ottobre 2026**: due glossari pubblici (marinasveva.com, scuolavelaargentario.com) confermano che «scadere» significa essere spinti sottovento da scarroccio o corrente, non la prua che gira. Il gioco usava il termine nel senso sbagliato: corretto in «poggiare» (0.17.1). Resta aperto solo se la velocità di rotazione modellata sia plausibile | *libro* o *video*, poi *codice* |
| Confini delle andature (angolo morto circa 40°, testi «circa 45° per lato») | Allineato alle dispense come convenzione didattica | *libro* o *video*, per le derive reali |
| Procedura di partenza reale (5 minuti; il gioco permette anche 1 e 3) | Da verificare | *web* o *video* |
| Boe lasciate sempre a sinistra: le istruzioni di regata reali lo stabiliscono di volta in volta | Dichiarata | *libro* o *video* |
| Toccare una boa in regata comporta una penalità: nel gioco non è ancora gestito | Aperto | *codice*, dopo la verifica della regola |
| Penalità di 15 secondi per un contatto invece dei giri di penalità | Semplificazione dichiarata | *libro* o *video*, poi *codice* |
| Regole di precedenza da inserire nelle domande dell'esame: il corso federale cita le regole 10, 11, 14 e 18 | Titoli da verificare sul testo ufficiale | *web* |
| Angolo di scotta del fiocco: nel gioco/prototipo 50°–60°, ma potrebbe essere più vicino a 80° | Aperto (fonte: risposte di una IA, non una verifica) | *libro* o *video* |
| Fiocco a collo tenuto un attimo in virata: potrebbe aiutare la prua a girare | Aperto (fonte: risposte di una IA, non una verifica) | *libro* o *video* |
| Recupero da una virata fallita: fiocco a collo o barra inversa, invece di «centra la barra» | Aperto (fonte: risposte di una IA, non una verifica) | *libro* o *video* |
| Posizione dei filetti principali della randa: potrebbero stare vicino all'albero invece che sulla balumina | Aperto (fonte: risposte di una IA, non una verifica) | *libro* o *video* |

## 2. Il fiocco e la barca a due (prototipo, tappe A, B e C)

Il prototipo è chiuso con le semplificazioni dichiarate. I dubbi che restano:

| Dubbio | Cosa sappiamo | Per chiuderlo |
| --- | --- | --- |
| **Limite di apertura della scotta del fiocco (80° nel prototipo)** | Nessuna fonte; su questo si appoggia tutta la zona in cui il fiocco non si regola (oltre circa 107° apparenti) | *libro* o *video* |
| **Soglia dell'ombra della randa sul fiocco** (95°-107° apparenti) | Una sola fonte, con spinnaker: il fiocco aiuta fino a circa 100° e da circa 120° è un ostacolo. Senza spinnaker non è noto | *libro* (Marchaj) o *video* |
| **Il fiocco coperto dà zero, non resistenza** | Le fonti lo chiamano «un ostacolo»: una vela che sbatte frena. Il modello azzera la spinta ma non la rende negativa | *libro* o *video* |
| **Il fiocco a farfalla** (dal lato opposto alla randa) | È la manovra vera in poppa; con spinnaker o gennaker il fiocco si fissa. Da quale andatura serve, e se sulle derive a due si usa l'asta, non risulta | *libro* o *video*; poi *codice* per modellarla |
| **L'upwash della randa sul fiocco** | Spiega perché il fiocco fa stringere meglio il vento; non modellato, per questo l'ottimo di bolina resta a 50° e non a 48°. La spiegazione «Venturi» è sbagliata | *libro*; poi *codice* |
| **Quanto spinge un fiocco a collo** | Nessuna fonte, né in gradi al secondo né in newton | *libro* o *video* |
| **Il ginocchio nella velocità fra 126° e 132° di vento reale** (fino a 0,16 nodi per grado) | Dovuto alla rampa stretta dell'ombra; da giudicare giocando | *prova* |
| **Il limite del vento per il livello 2** (stimato in 12-15 nodi) | È una stima: a 20 nodi di raffica si scuffia e a 15 la virata non riesce; il confine non è stato misurato | *codice* (misura), con le lezioni |

## 3. Equilibrio, timone e raddrizzamento

Dalla fonte su una deriva olimpica a due (una sola barca):

| Dubbio | Cosa sappiamo | Per chiuderlo |
| --- | --- | --- |
| **Momento d'imbardata dovuto alle vele** (randa che fa orzare, fiocco che fa poggiare, scafo sbandato che orza da solo) | Non modellato: il motore gira solo col timone. Modellare il solo fiocco dà una barca sempre poggiera, contro la fonte | *web* (ricontrollare la fonte), poi *codice* con un motore più dinamico |
| **Timone in stallo oltre circa 15°** | Nel motore non stalla mai: barra a fondo (30°) gira 1,93 volte più in fretta che a 15° ed è sempre la scelta migliore | *Aggiornato il 17 ottobre 2026:* nel livello 1 resta così, dichiarato; il livello 2 in prova ha lo stallo (`PROPOSTA-STALLO-TIMONE.md`), ma l'effetto didattico non c'è ancora. **Da cercare:** virate misurate su una deriva singola da circa 4 m (più pertinenti del 470), e la frenata della barca prua al vento |
| **Coppia raddrizzante di una deriva a due** | Circa 60 kgf·m senza trapezio e circa 220 col trapezio (una barca); il prototipo vale 83,7 kgf·m a 22,6° | *libro* o *video* |
| **Massa e resistenza dello scafo** | Nel motore la massa non entra nella resistenza: una barca più pesante andrebbe più veloce. Nessun dato per ritarare | *web* (polari di derive) |
| **Peso dell'equipaggio come comando** | Oggi il timoniere si sporge da solo, con 0,9 s di ritardo; nella realtà è una manovra (lezione 2.5) | *codice*, con il prodiere |
| **Planata** (livello 3) | Non c'è: sopra gli 8 nodi circa le velocità non possono essere realistiche | *libro*, poi *codice* |

Gennaker e planata richiedono un prototipo dedicato prima di progettare le lezioni 3.x. Le lezioni 2.3 (errore di coordinamento) e 2.5 (peso come comando) non dipendono da fisica che manca: si possono progettare con il motore attuale.

~~Pagina di domande per un velista (`domande-per-un-velista.pdf`)~~: non ci sarà un velista (13 ottobre 2026). Le domande restano come ricerche da fare (sez. 9).

### Angolo morto, barca che arretra, ripartenza dopo la scuffia (ricerca *web* dell'11 ottobre 2026)

Nasce da due registrazioni (0.19.5 e 0.20): nel gioco, con la barca che arretra e la barra al centro, la prua **non** poggia da sola, mentre lo dicono il passo 5.4, il suggerimento «Stai andando all'indietro…» e la domanda d'esame 22. Nel motore la prua poggia da sola solo con vento apparente sotto 36° **e** velocità sotto 0,5 m/s (`index.html`, riga 443). Ricerca a tempo limitato, in inglese e in italiano. Domande solo per derive. Regola: una sola fonte = «non verificato»; i forum contano poco.

**Come sono state lette le citazioni.** I PDF sono stati letti con `pdftotext`, quindi le loro citazioni sono il testo originale. Le pagine web (US Sailing, Cal Sailing Club, Small Craft Advisor) sono passate da uno strumento di lettura che restituisce le frasi citate: sono da ricontrollare sulla pagina prima di usarle nei testi del gioco.

**Fonti usate**

| Sigla | URL | Chi scrive | Barca |
| --- | --- | --- | --- |
| W1 | https://www.ussailing.org/news/getting-in-and-out-of-irons/ | US Sailing (federazione statunitense), 12 ottobre 2016 | non nominata: barca con randa e fiocco, barra |
| W2 | https://myc.org/wp-content/uploads/2021/02/Sunfish-How-to-get-out-of-Irons.pdf | Ken Zorovich, PDF pubblicato da un circolo (MYC) | Sunfish, deriva monoposto |
| W3 | https://www.papertigercatamaran.org/ptcia/media/pdf/reverse_logic_-_getting_out_of_irons.pdf | Notiziario dell'associazione di classe Paper Tiger, febbraio 2011; autore non indicato | **catamarano** monoposto, non una deriva |
| W4 | https://cal-sailing.org/blogfrontpage/recent-blog-posts/entry/a-couple-of-capsize-recovery-tips?format=amp | Michael Sherrell, blog di un circolo (Cal Sailing Club), 2014 | deriva con deriva mobile, classe non nominata |
| W5 | https://smallcraftadvisor.substack.com/p/on-capsizing-and-recovery | Richard Woods, progettista, trascrizione di una conferenza del 2016 (rivista Small Craft Advisor) | piccole barche, derive comprese |

**1. Barca ferma nel vento dopo una virata mancata: la prua poggia da sola?**

- **Esito: «poggia da sola» non trovato in nessuna fonte.** Due fonti dicono il contrario, cioè che la barca **resta** nell'angolo morto se non si fa qualcosa. Nessuna delle due tratta il caso della barra al centro.
- W2 (Sunfish, deriva): «there is powerful and EQUAL PRESSURE on both sides of the sail that can prevent the Sunfish from turning.» Il testo lo riferisce al vento sopra i 15 nodi e a un timoniere leggero.
- W3 (catamarano): «The boat has to be steered out of irons and it won't do this by going forward any time soon.» Descrive anche la barca ferma che non risponde: «sit motionless with the boat refusing to respond to any amount of mainsheet tugging and rudder waggling».
- **Misura del 16 ottobre 2026 (1.0.12, `PROPOSTA-CORREZIONI-PASSI.md` §2):** a mani ferme dopo il passo 1.8 la barca esce da sola dall'angolo morto 40 volte su 40. Su una copia con `ironsYaw` = 0 resta nel vento e arretra a circa 2 nodi, e il passo 1.9 guidato come dice il testo non riesce più (0 su 20): togliere la regola senza fonte richiede anche un modo di uscire per i principianti (le fonti: spingere il boma, comando previsto nel livello 2). Decisione di Ale: per ora non si cambia.
- W1 non dice né l'una né l'altra cosa; dice solo «you'll find it hard to steer».
- **Conteggio:** due fonti indipendenti, di cui una sola su una deriva e l'altra su un catamarano. Per il caso «deriva, barra al centro» il risultato è **non verificato**, ma **va contro** i testi attuali del gioco (passo 5.4, suggerimento, domanda 22).

**2. Come si esce dall'angolo morto?**

- **Esito: concordano tre fonti indipendenti** (W1 federazione, W2 circolo su una deriva, W3 associazione di classe su un catamarano). Si spinge il boma fuori, cioè si mette la randa «a collo», e la barra va dalla stessa parte. La barca va all'indietro e la prua si allontana dal vento. Poi si raddrizza la barra, si cazza e si riparte.
- W1: «If the boat does not have a jib, back the mainsail by pushing the boom on the side you want to turn toward.» «hold the tiller in that same direction as the mainsail, the direction you want to turn toward.» «As you back the sails, your boat will start to move backwards.» «This will cause the bow (the front of the boat) to turn toward the boom, and away from the wind.» Alla fine: «release the backed sail and pull in the sheets».
- W2: «When stuck in irons, push your tiller and boom in the same direction until you are luffing on a beam reach, straighten your tiller, sheet in and go.» «Your boat will start sailing backwards and will start to turn.»
- W3: «Release the mainsheet. Push the boom and tiller hard away from you.» «The boat will reverse and the stern will turn to windward. Once the boat is pointing slightly below the angle of the next beat, release the boom, pull the tiller towards you and sheet in gradually as the boat accelerates.»
- **Da ferma e arretrando.** Le fonti partono dalla barca ferma e la fanno arretrare apposta. Il caso della barca che **già** arretra non è trattato a parte: **non trovato**.
- In italiano: **non trovato**. Nessuna scuola o federazione italiana descrive la manovra nelle pagine trovate.
- **Per il gioco, isteresi del suggerimento: decisa e applicata (11 ottobre 2026, ancora dentro la 0.20.2).** Il problema: il suggerimento «all'indietro» cambiava testo a 45° esatti. Con le raffiche la prua oscillava attorno alla soglia e i due testi si alternavano. Nel collaudo, partendo da 45° il primo testo compariva in 26 prove su 40, partendo da 46° in 1 su 40. Decisione di Ale, dopo la terza registrazione (`sessione-20261011-1432(3).txt`):
  - una soglia unica di 40° (`IRONS_A`) per rosa, registro, suggerimento e passo 5.4;
  - dal secondo testo si torna al primo solo sotto 37°;
  - lo stato sta in `S.indietro`, fuori dal motore.

  Nel collaudo: 0 ritorni al primo testo con la prua da 37° in su, e il controllo «solo il secondo testo» è passato nei casi 2, 4 e 5 in tutte le prove. Era una scelta di interfaccia, senza bisogno di fonti.
- **Per il gioco.** Il gioco non ha un comando per spingere il boma. *Corretto l'11 ottobre 2026:* il dato «3,4-10,2 s» scritto qui prima era sbagliato. In quella prova la barra stava **lontano dal boma** e la prua attraversava il vento (a 0°) prima di uscire dall'altro lato. La misura giusta: mentre la barca arretra, barra a fondo **verso il boma**, poi al centro. Nel gioco libero, tre casi delle registrazioni, scotta 100 e 50, con e senza raffiche, 10 semi: la prua arriva a 45° dal vento in 60 casi su 60 e non passa mai a meno di 10° dal vento. Con la barra lontano dal boma la prua attraversa il vento in 60 casi su 60. *Corretto l'11 ottobre 2026 (0.20.2):* qui c'era scritto «e non esce mai», ma quel collaudo contava come uscita solo quella sulla stessa mura e fermava la prova dopo circa 12 s; lasciata fare, la barca esce sull'altra mura (8 su 8 nel collaudo del passo 5.4, circa 9 s dopo essersi piantata). Dalla 0.20.2 il passo 5.4 la conta come uscita buona: nessuna fonte dice che sia sbagliata. Griglia e collaudo su tutte e due le mure nel `CHANGELOG.md`, 0.20.1.

**3. Dopo la scuffia e il raddrizzamento: si lasca o si cazza per ripartire?**

- **Prima e durante il raddrizzamento le scotte vanno libere: due fonti indipendenti, nessuna di una federazione.**
  - W4: «uncleat the gnav/vang (in addition to the mainsheet & jib)», perché questo riduce l'effetto del vento sulla vela quando la barca torna su.
  - W5: «if it is windy you don't really want the jib sheeted in as you right the boat»; altrimenti la barca «will probably capsize again and certainly start sailing off before you are ready». W5 consiglia anche di tenere la barca con la prua al vento: «This ensures the boat stays head to wind when it comes up and so won't blow over again.»
- **Per ripartire dopo il raddrizzamento (lascare o cazzare, e se dipende dall'angolo col vento): non trovato.**
- Non è stato possibile leggere theyachtmarket.com (errore 403). Il materiale della federazione inglese (RYA) e quello di US Sailing sulla scuffia non sono stati trovati.

**Domanda d'esame sulle scotte durante il raddrizzamento: da riprendere dopo una conferma da fonti.** Scritta l'11 ottobre 2026 come versione (a) della domanda 26 e **non messa nel gioco** (nella 0.20.1 la 26 è quella su come si vede arrivare una raffica). Per usarla bisogna anche rimettere nel passo «Raddrizzare» la frase sulle scotte libere, che dalla 0.20.1 c'è già.

- Passo: L6 «Raddrizzare».
- Domanda: «Stai per raddrizzare la barca scuffiata. Come lasci le scotte?»
- Giusta: «Libere, così la vela non spinge mentre la barca torna su».
- Sbagliate: «Cazzate a ferro, così la barca riparte appena torna dritta»; «Legate al centro, così il boma non si muove»; «Non importa: in acqua le scotte non contano». Controllare la lunghezza: oggi la giusta (56 caratteri) è più corta della prima sbagliata (58).
- Spiegazione: «Con le scotte libere la vela non prende vento mentre la barca torna dritta: così non riparte da sola e non si rovescia di nuovo prima che tu sia a bordo.»
- Si regge su W4 e W5 (due fonti deboli). Segnale contrario non verificato: un forum e una dispensa di Yachting New Zealand (non letta) parlano di cazzare un poco in certi raddrizzamenti.

**Cosa resta aperto.** La domanda 1 (prua al vento con barra al centro su una deriva) e la domanda 3 (ripartenza) vanno cercate nelle fonti scritte o nei video. Nella 0.20.1 i testi del passo 5.4, del suggerimento e della domanda 22 sono stati cambiati lo stesso: non dicono più che la prua poggia da sola e insegnano solo ciò che il gioco permette (barra verso il boma), misurato. Restano da confermare con fonti.

### Dai video (11 ottobre 2026)

Quattro video informali (trascrizioni automatiche incollate da Ale, non viste né sentite), schedati in `SCHEDATURA-FONTI.md`. Sono fonti informali: parafrasate, **mai usate per tarare il motore**. Servono a controllare cosa insegniamo e a raccogliere indizi per il livello 2.

| Dubbio | Cosa sappiamo | Per chiuderlo |
| --- | --- | --- |
| **Oscillazione orza-poggia attorno a 0-1 nodo** | Contaldo (3:00-3:32) descrive in panna un procedere a zig-zag lento: il fiocco a collo fa poggiare, la barca prende velocità, col timone tutto all'orza interviene l'effetto orziero (3:14) e la prua risale, poi la velocità cala e il ciclo riparte; velocità massima circa 1 nodo. Osservazione nostra, non della fonte: coerente con l'effetto del timone che cresce con la velocità. Nel gioco manca il momento della vela (fiocco), che è la forza contraria. Una fonte, barca con genoa | *libro* o *video*; poi *codice* se si modella il momento di imbardata |
| **Quanto in fretta cambia l'effetto della barra attorno a velocità zero** | Nessuna fonte. La prua «poggia da sola» (fino a 6 °/s) ha costanti senza fonte | da cercare nelle fonti (sez. 9, punto 10) |
| **Uscita dallo stallo: tre modi e perché si ricade** | Lee (2022): boma e barra dallo stesso lato (preferito); boma fuori e barra verso di sé; solo barra, con vento da moderato a forte, più lenta e da fare con pazienza se c'è poco vento. Ricaduta nei ferri se, cazzando, la barra resta dal lato del boma. Il gioco implementa il terzo modo. Una fonte, trascrizione inglese originale. *Collegamento nostro, non dalla scheda:* la sez. 9, punto 2 parla delle fonti schedate per la manovra con il boma spinto fuori (US Sailing, guida Sunfish, associazione di classe); il terzo modo di Lee è una fonte informale in più per la sola barra. Il punto 2 resta com'è | *libro* o *video* |
| **Fiocco a collo come aiuto nella virata** | Bombaci (4:56-5:16): con poca velocità si vira con il fiocco a collo, che spinge lateralmente la prua. Contaldo: stesso principio in panna. Nessun numero | già aperto: «Quanto spinge un fiocco a collo»; resta senza fonte quantitativa |

## 4. Velocità e polari

| Dubbio | Cosa sappiamo | Per chiuderlo |
| --- | --- | --- |
| Polari pubbliche di derive | Non risultano. I database aperti vengono da certificati ORC e riguardano barche a chiglia e sportboat; la licenza dei dati non è chiara | *web* |
| Confronto del gioco con una deriva monoposto standard | Una tabellina in un forum (provenienza non verificabile): a 10 nodi il gioco risulta più lento del 20-40%, soprattutto in poppa, dove una barca vera plana | *web* (articolo del 2002), poi *codice* |
| Braccio sbandante `zCE` = 2,0 m, senza fonte (17 ottobre 2026, `PROPOSTA-BOLINA.md` §11) | Cambia solo il vento forte: con 2,8 m la bolina con 15 nodi passa da +7% a −1% contro Day, con 9 nodi non cambia. Il braccio va dal centro velico al centro della spinta laterale sotto l'acqua; Day dà le proporzioni (36,4% dell'inferitura sopra il boma, 43% della deriva) ma non le misure dell'armo | *web*: misure dell'armo con una fonte usabile (principio 5), quando si cambia la barca (livello 3) |
| Coefficienti di portanza e resistenza delle vele leggibili nel testo | Le figure dello studio sulla deriva olimpica non lo sono | *libro* |

## 5. Modelli e dati esistenti

| Idea | Stato | Per chiuderla |
| --- | --- | --- |
| **By The Lee** (simulatore di vela in JavaScript, licenza Apache-2.0): riferimento per una dinamica minima nel nostro motore | Ricordata come riferimento; letto solo il README | *codice*, sola lettura: come organizza equilibrio, centro velico, smorzamento |
| Python-VPP, sailboat-playground, simulatore su atterwind.info | Licenze non verificate | *web*, solo se serve |
| **Scala del realismo**: gradino 1 motore cinematico dichiarato (oggi); gradino 2 pochi pezzi mirati con dati di fonte (barra «pesante» da sbandata, stallo del timone); gradino 3 motore dinamico completo | Idea | Decidere confrontando il livello 1 con le fonti (vedi `PROPOSTA-RESISTENZA-SCAFO.md`) |

## 6. Livelli, ruoli e carriera

Decisioni ancora aperte (vedi `VISIONE-LIVELLI-E-CARRIERA.md` e `ROADMAP.md`):

- Gli aiuti (barra che torna al centro, «gira la prua», suggerimenti) valgono per i meriti in carriera?
- Rosa dei candidati dell'equipaggio: profili, quanto cambiano, valore del tetto del bonus.
- Come si danno gli ordini all'equipaggio (tasti e presentazione) e il preavviso minimo di ogni manovra.
- Il fiocco a collo come errore di coordinamento nel registro degli errori: tempi e regola (lezione 2.3).
- Livelli 4 e oltre: ruoli, regole, quali barche entrano davvero. Quanti ruoli servono per il brevetto dal livello 3.
- Tarature dei numeri dei meriti, durata dei tornei, bonus del primo torneo in un ruolo nuovo, soglie della competizione.
- Il gennaker asimmetrico come soluzione più diffusa rispetto allo spinnaker con tangone: non verificato (*libro* o *video*).
- Esistenza e funzione del tattico su equipaggi di più persone (*libro* o *web*).
- Tasti con due vele: A e D sulla randa nel prototipo; l'idea di A S D W per la barca a una vela va ripensata.
- Quiz con domande in più, perché il ripasso non coincida con l'esame.

## 7. Cose tecniche

- Il pannello delle lezioni ha margine zero: un cursore in più per il fiocco non ci sta e andrà ripensato per le lezioni a due vele.
- Il paragrafo troncato nelle impostazioni (la classe del pannello è riusata nel dialogo dove il testo è lungo), difetto trovato in `index.html`.
- Playwright non è installato in modo permanente: i collaudi usano una copia temporanea.
- Font Barlow Semi Condensed e Source Serif 4: se mancano, le misure del pannello sono più pessimistiche del vero.
- Il giudizio di chi gioca sulla tappa C1 non è ancora arrivato: va chiesto dopo aver giocato il prototipo.
- Le conoscenze del progetto vanno ricaricate quando cambiano i documenti (`CONTENUTI-DA-VERIFICARE.md` per ultimo).

## 8. Persone da coinvolgere

- ~~Un velista esperto~~: non ci sarà (13 ottobre 2026). Le sue domande diventano ricerche su fonti scritte e misure dai video.
- **Lucio**, per provare il prototipo con tre domande: dove una posizione giusta del fiocco c'è la trovi? Il messaggio nel pannello ti dice cosa fare? Qualcosa ti confonde?

## 9. Domande da chiudere con fonti scritte o video (derive)

Domande pensate un tempo per un velista esperto, che non ci sarà: ognuna si chiude con fonti scritte o con misure dai video. Solo derive. Accanto a ogni voce, le fonti che i documenti hanno oggi (sez. 3 di questo file, `CONTENUTI-DA-VERIFICARE.md`, `FONTI-PUBBLICHE.md`).

1. **Virata mancata per poca velocità, barca ferma con la prua nel vento: la prua poggia da sola, anche lentamente, o resta lì finché non si agisce?** Fonte attuale per «poggia da sola»: nessuna. *Nel gioco succede, ed è voluto (riga 443 di `index.html`): vento apparente sotto 36° e barca sotto 0,5 m/s (circa 1 nodo). Visto nella registrazione `sessione-20261011-1259.txt` (0.20.2). Fra 237 e 241 s, con la barra al centro e la scotta tutta cazzata (0), la prua passa da 24° a 42° dal vento e la barca riparte: è anche la nota M3 di Ale, «se ho la vela cazzata esce da sola dall'angolo morto». Fra 277,1 e 279,2 s, con la barra a −4%, 0% e 0% e la scotta a 100, la prua passa da 330° a 323° (dal vento da 30° a 37°) con la barca quasi ferma. È un episodio quasi pulito: la barra era appena tornata da −100, due secondi prima. Comportamento senza fonte (annotato l'11 ottobre 2026; corretta la prima versione della nota, che aveva letto la colonna della scotta come barra).* Due fonti dicono che la barca resta nell'angolo morto, ma una sola riguarda una deriva (Sunfish); l'altra un catamarano (sez. 3, W2 e W3).
2. **Uscita arretrando: barra verso il boma, poi al centro, e si cazza (domanda d'esame 22 dalla 0.20.1). Vale anche con il boma non spinto a mano?** Fonte attuale per la manovra con il boma spinto fuori, la randa «a collo»: tre (US Sailing, guida Sunfish, associazione di classe di un catamarano; sez. 3). Con il boma lasciato dove lo mette il vento: nessuna; è solo misurato nel gioco (`tests/fisica/angolo_morto.js`).
3. **Dopo la scuffia: scotte libere durante il raddrizzamento? Per ripartire si lascia o si cazza, e dipende dall'angolo col vento?** È la versione (a) della domanda 26, da riprendere dopo la conferma (sez. 3). Fonte attuale per le scotte libere: due, deboli (blog di un circolo, conferenza di un progettista). Per ripartire: nessuna.
4. **In poppa piena una deriva è meno veloce che al traverso o al lasco? (domanda d'esame 11)** Fonte attuale: una, debole (la tabellina di un forum, F9, provenienza non verificabile, in `FONTI-PUBBLICHE.md`).
5. **Con la vela già tutta lasca e troppo sbandamento, orzare un poco aiuta?** È il messaggio del pannello dalla 0.19.4. Fonte attuale: nessuna (`CONTENUTI-DA-VERIFICARE.md`, «Dubbi specifici»).
6. **Cause della barca orziera nel glossario: sono corrette e complete?** Le cause elencate sono vento e raffiche, onde che spostano la prua, barca molto sbandata, vele troppo cazzate, posizione e peso dell'equipaggio. Fonte attuale: una per «vele troppo cazzate» (F1) e una per «sbandamento» (F4); per le altre cause nessuna.
7. **Lezione 1, «Ripartire»: con la barca quasi ferma, «da entrambi i lati si poggia». Vale?** Nel gioco la prua lì gira per la riga 443 di `index.html`, non per il timone. Fonte attuale: nessuna.
8. **Regola delle stesse mure (lascia strada chi è sopravento): non è insegnata in nessuna lezione. Si conferma che è giusto così per il livello 1?** Fonte attuale nei documenti: nessuna (`CONTENUTI-DA-VERIFICARE.md`, regate, esito vuoto).
9. **Il resto:** i «Dubbi specifici» di `CONTENUTI-DA-VERIFICARE.md` e il questionario di 27 domande di `RIPARTI-DA-QUI.md` (negli appunti, fuori dal repository).
10. **Dopo l'uscita dall'angolo morto, mentre si cazza: la barra va al centro o un po' dal lato opposto al boma?** Il testo B dice «barra al centro». Lee (2022, originale inglese, righe 248-277) dice che cazzando con la barra un po' dal lato del boma la barca orza di nuovo e ricade nei ferri, e consiglia di tirare la barra un po' verso di sé oltre la linea centrale. Una fonte, informale (video, parafrasato, non usato per tarare il motore); nessun'altra. Da confermare con un'altra fonte prima di cambiare qualcosa. Origine: parte D di `SCHEDE-VIDEO-2026-10-11.md` (negli appunti); le altre due domande della parte D sono già coperte dai punti 1 e 2.
