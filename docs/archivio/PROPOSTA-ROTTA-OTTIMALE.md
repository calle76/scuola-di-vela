# Proposta: la rotta ottimale, a regata finita (fermata 1, 9 novembre 2026; via di Ale lo stesso giorno)

**Nome:** Ale l'aveva chiamata «rotta ottimale» e ha chiesto il termine tecnico, se c'è. Nella navigazione si chiama **rotta ottimale** (in inglese *optimal route*): è quella che calcolano i programmi di *routing* meteo con il metodo delle isocrone. Qui è la rotta ottimale **col senno di poi**, calcolata sul vento che c'è stato davvero.

**Via di Ale (9 novembre):** «via, fuori dalla Scuola, prima la rotta ottimale».

**Idea di Ale, 9 novembre:**
- «sarebbe bello se alla fine di ogni regata fosse mostrata la migliore strada che si sarebbe dovuta percorrere per arrivare col miglior tempo»;
- poi: «avremo momento clou e miglior regata che spiega dove avrei potuto migliorare».

Fa parte del coach, accanto alla moviola (che c'è già) e al momento clou (fase 2 di `PROPOSTA-COACH-REGISTRATORE.md`, da fare).

**Niente codice finché Ale non dà il via.**

## 1. Cosa vede il giocatore

A fine regata, accanto a «Rivedi», un pulsante **«Rotta ottimale»**. Apre la moviola con:
- la tua traccia e, in verde, la strada più veloce che c'era con il vento di quella regata;
- un segno ogni 30 s su tutte e due le tracce, per vedere dove eri tu e dove saresti stato;
- un riassunto breve, per esempio: «La rotta ottimale arriva in 3:12, tu in 3:40 (+28 s). Bolina +19 s, poppa +9 s. Dove hai perso di più: a 1:05 il vento è girato di 9° contro di te e la rotta ottimale ha virato; tu hai tenuto il bordo per altri 40 s.»

**Cosa la rotta ottimale non è (detto anche nel gioco):**
- è la strada **col senno di poi**: conosce le raffiche e i salti prima che arrivino, cosa che in acqua nessuno sa;
- ignora le altre barche (precedenze, coperture, partenza affollata);
- è il limite di quello che si poteva fare, non quello che un velista bravo avrebbe fatto.

**Non svela le regate future:** ogni regata ha vento, raffiche e salti estratti a caso (il gioco non usa semi fissi), quindi la strada di oggi non vale domani. Restano le regole generali: virare sugli scarsi, andare verso le raffiche, nel salto persistente andare verso la rotazione. Sono proprio quelle da imparare.

## 2. Modello più semplice

**A. Registrare il vento.** Durante la regata, una volta al secondo, si copia:
- lo stato delle raffiche (al massimo 12, con posizione, raggio, forza, rotazione ed età);
- l'angolo del salto;
- il tempo del gioco, da cui dipende l'oscillazione lenta.

Così si ricostruisce il vento esatto in ogni punto e in ogni istante, con la formula di `windAt`. Fra un secondo e l'altro le raffiche si spostano in linea retta, come già fanno nel gioco.

Si legge soltanto: nessun numero casuale in più, quindi la regata resta identica con e senza registrazione (criterio S6). Costa circa 40 000 numeri per 5 minuti di regata.

**B. La polare della barca del gioco.**
- È una tabella di velocità per angolo dal vento (ogni 5°) e forza del vento (da 6 a 18 nodi).
- Si calcola una volta con il motore stesso, barca tenuta a regime col pilota, come fa `tests/fisica/polare.js`, e si scrive in un file di dati.
- La barca della rotta ottimale non accelera e non rallenta: in una raffica va subito alla velocità della polare. È una semplificazione, da dichiarare.

**C. Le manovre costano tempo.** Ogni virata e ogni abbattuta costano un numero fisso di secondi, `T_VIR` e `T_ABB`. Si misurano con il pilota sulla barca del gioco (come `virata1b.js`) e sono ipotesi nostre. Senza questo costo la rotta ottimale farebbe cento virate.

**D. Il calcolo: le isocrone.** È il metodo dei programmi di rotta per le regate d'altura.
1. Si parte dal punto e dall'istante in cui il giocatore ha tagliato la linea: la partenza non si giudica qui, la guarda il momento clou.
2. A ogni secondo si allarga il «fronte» di tutti i punti raggiungibili, ognuno con la sua prua e le sue mure.
3. Per ogni direzione si tiene solo il punto più avanti.
4. Arrivati alla boa (un punto 2 m fuori, dal lato giusto), il fronte riparte da lì verso la boa dopo, fino alla linea d'arrivo.

Si calcola nella pagina a fine regata, in pochi secondi (criterio S4). Il fronte si sfoltisce: un punto ogni 2°, una griglia di 1 m.

**E. Dove hai perso.** Si confrontano le due tracce, per lato e nel tempo:
- **secondi persi per lato:** il tuo tempo contro quello della rotta ottimale, dalla boa alla boa;
- **le due differenze più grandi**, ciascuna detta con il suo motivo, se lo si riconosce dai dati del vento:
  - **virata sullo scarso:** la rotta ottimale vira entro 10 s da un salto di almeno `SCARSO` gradi contro le mure del momento, e tu no;
  - **raffica:** la rotta ottimale passa in una raffica che tu hai lasciato a più di 20 m;
  - **lato del campo:** la rotta ottimale va dalla parte verso cui ruota il vento persistente, e tu dall'altra;
  - **manovre in più:** hai fatto almeno 3 virate o abbattute più della rotta ottimale.

  Se il motivo non si riconosce, si dice solo dove e quanto.

**Costanti nuove (ipotesi nostre):** `T_VIR`, `T_ABB` (da misurare), `SCARSO` (6°), la griglia del fronte (2°, 1 m), il passo del calcolo (1 s).

**Cosa non si tocca:** la fisica, gli avversari, il vento, le regate. Si aggiungono una registrazione che legge soltanto e una schermata a regata finita.

**Utile anche per noi:** la stessa misura dice quanti secondi perde ogni avversario rispetto alla rotta ottimale. Sarà il metro per migliorare le loro scelte in bolina (oggi bordi di durata a caso e nessuna virata sugli scarsi, `js/regate.js`).

## 3. Criteri (soglie nostre, scritte prima di misurare)

Misura con il pilota sulle regate del torneo (le 4 del torneo ampliato), principianti ed esperti. Scelta sui semi 981-1010, conferma sui semi 1011-1040. Per ogni barca, giocatore e avversari, si calcola la rotta ottimale dal suo taglio della linea.

- **S1, è davvero la migliore:** il tempo della rotta ottimale è minore o uguale a quello della barca vera, al massimo con l'1% di eccezioni, e nessuna oltre 3 s. Almeno 400 barche-regata.
- **S2, non è fantascienza:** il vantaggio mediano sulla barca più veloce di ogni regata è al massimo il 20%. Se è di più, la polare o il costo delle manovre sono troppo ottimisti.
- **S3, il vento ricostruito è quello vero:** nei punti delle barche, ogni secondo, scarto massimo 0,05 nodi e 0,5°.
- **S4, tempo di calcolo:** al massimo 3 s per regata su questo PC, in Chromium e in Firefox (sul PC di Ale sarà di più: lo si riporta).
- **S5, pannello e schermata** a 1360x650 senza pixel in eccesso.
- **S6, non-regressione:** con lo stesso seme la regata è identica al bit con e senza registrazione; `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici.
- **S7, i motivi sono veri:** su 20 regate guardate da me con le immagini, ogni motivo detto («virata sullo scarso», «raffica»…) corrisponde a quello che si vede. Si riportano anche i casi senza motivo.

## 4. Rischi

- **Un ottimo troppo ottimista** («dovevi fare 2 minuti in meno») scoraggia e non insegna. Lo controlla S2; il testo dice sempre «col senno di poi».
- **I motivi possono essere sbagliati.** Si comincia con 4 tipi semplici; quando non si riconosce niente, si dice solo dove.
- **Il PC di Ale è lento:** se il calcolo pesa, si fa a pezzi mentre si guarda la moviola.
- **Le boe:** la rotta ottimale deve girarle dal lato giusto e senza toccarle, con il punto 2 m fuori.

## 5. Cosa serve da Ale

1. **Il via.**
2. **Dove si vede:** propongo dopo **ogni regata fuori dalla Scuola**, cioè le regate a tema e il torneo. Nelle regate a tema è anche didattica: «nei salti di vento, ecco dove virare». Nella Scuola no, per non aggiungere cose.
3. **Ordine rispetto al cono d'ombra.** La rotta ottimale senza cono d'ombra è più semplice. Se poi il cono si aggiunge, la rotta ottimale lo ignora come ignora le altre barche, e resta valida.

## 6. Costo

Circa due giornate:
- registrazione del vento e polare (mezza);
- calcolo e controlli S1-S3 (una);
- schermata, motivi e S7 (mezza).

## 7. Fermata 2: cosa è cambiato rispetto a questa proposta (scritto prima della misura)

- **Costi delle manovre misurati** (`tests/fisica/costo_manovre.js`, timoniere semplice, 60 s con la manovra contro 60 s dritti):
  - virata 2,7 s con 6 nodi e 1,9-2,0 s con 10-14 nodi, quindi `T_VIR` = 2 s;
  - abbattuta 0,0 s, perché nel gioco la barca strambando quasi non rallenta (traccia a 10 nodi: 4,25 → 4,11 nodi). `T_ABB` = 1 s è un minimo nostro, perché la rotta non cambi mure a ogni passo.
- **Polare** (`tests/fisica/polare_tabella.js --scrivi` → `js/rotta-dati.js`): da 4 a 20 nodi, da 25° a 180°, con lo scarroccio. La VMG di bolina migliore sta a circa 48° di rotta sul fondo dal vento, con 6-15 nodi.
- **Settori del fronte a 2°,** come scritto qui: per sbaglio il codice era partito con 1° (2 s per rotta invece di 1 s).
- **Layline** (Ale, 9 novembre: «la layline … come si può inserire nel gioco?»; «sì adesso»):
  - nella vista si disegnano le due layline della boa di bolina, col vento alla boa nell'istante della moviola;
  - un quinto motivo: l'ultima virata per la boa oltre la layline di almeno `LAY_TOLL` 5° e `LAY_MIN` 10 m, oppure almeno 2 virate negli ultimi `LAY_VICINO` 80 m.

  Le costanti sono ipotesi nostre. Gli altri pezzi della layline (aiuto in acqua, lezione, avversari) sono una voce a parte di `DA-FARE.md`.
- **Vista:** con la rotta aperta la camera mostra tutto il campo, nord in su, sopra la barra della moviola.
- **Prova** (semi 981-982, 63 barche-regata; solo per vedere che funziona, non è la misura):
  - S1: 0 eccezioni;
  - S2: mediana 10,4%;
  - S3: scarto 0,0000 nodi e 0,0025°;
  - S4: mediana 1,0 s;
  - S6: 0 regate diverse su 16.
- **Pannello:** con la moviola aperta il pannello a destra sfora di 20 px. Succede anche con il solo «Rivedi», quindi non viene da qui; si riporta.

## 8. Esito: adottata nella 1.2.22

| | semi 981-1010 | semi 1011-1040 | soglia |
| --- | --- | --- | --- |
| S1 rotta ottimale più lenta della barca vera | 0 su 915 | 0 su 906 | ≤1%, nessuna oltre 3 s |
| S2 vantaggio mediano sulla barca più veloce | 12,9% | 11,8% | ≤20% |
| S3 scarto del vento ricostruito | 0,0000 nodi, 0,0025° | 0,0000 nodi, 0,0026° | 0,05 nodi, 0,5° |

**S4**, misurato da solo sul PC (semi 981-985, 159 rotte; Firefox semi 981-982, 58 rotte):
- Chromium: mediana 1,08 s, massimo 1,41 s;
- Firefox: mediana 1,27 s, massimo 1,74 s.

Nelle misure lunghe col termostato, 40 tempi di circa 6,2 s su 1918: sono le pause da 5 s del termostato, nessuno fra 2 e 3 s.

**S5:** pannello +20 px con la moviola aperta, uguale col solo «Rivedi» (difetto vecchio); il riquadro di fine regata e la barra della moviola stanno nello schermo.

**S6:** 0 regate diverse su 40.

**S7** (20 regate: 10 nei salti di vento, 10 del torneo, che per un limite del collaudo erano tutte la regata 1):
- i motivi che si vedono nell'immagine corrispondono alle tracce;
- quelli sul vento non si vedono nell'immagine;
- un difetto trovato e corretto: le abbattute in poppa contate come virate.

Esempio di testo: «Rotta ottimale 5:24 dal tuo taglio della linea, tu 6:55 (+90 s). Bolina +63 s, Poppa +27 s. Hai virato per la boa 13 m oltre la layline: virando prima avresti fatto meno strada. Bolina: hai cambiato mure 8 volte, la rotta ottimale 3.»

**Misura più frequente:** «negli ultimi 80 m hai virato 2 volte» compare in 8 regate su 20 col pilota. Il pilota fa spesso una virata in più vicino alla boa.

**Per gli avversari:** dalla rotta ottimale di ogni barca, vantaggio mediano sulla barca stessa del 19,5-20,1%. È il metro per le prossime voci sugli avversari.
