# Proposta: le scritte sopra le barche non coprono le barche (fermata 1)

14 novembre 2026, mattina. Nota di Ale del 13 novembre: «a volte quelle scritte coprono le barche. forse sono da allontanare. poi vedremo». In `js/` non è stato scritto niente.

## Cosa c'è oggi

In regata, sopra ogni avversario c'è una scritta: il nome del colore, oppure il cognome nel torneo dalla 1.2.33 (`drawRaceScreen`, `js/regate.js`).
- Sta sempre **58 px sopra** il centro della barca sullo schermo, a qualunque zoom e con la barca girata in qualunque direzione.
- È un rettangolo scuro semitrasparente alto 18 px, largo quanto il testo. Col cognome è più largo di prima, fino a circa 80 px con «Ferraresi».
- Non guarda dove sono le altre barche. Quando due barche sono vicine, una sopra l'altra sullo schermo (in partenza, alla boa), la scritta di quella sotto cade proprio sulla barca di sopra, anche sulla tua.

## Modello più semplice

1. **Due posti possibili per ogni scritta:** sopra la barca (come oggi) oppure sotto, alla stessa distanza.
2. **Si sceglie il posto libero.** Se il rettangolo della scritta sopra copre lo scafo di un'altra barca, compresa la tua, la scritta va sotto. Se anche sotto copre qualcosa, resta sopra ma **più trasparente** (testo e fondo al 40%), così la barca sotto si vede.
3. **Niente sfarfallio:** una scritta spostata resta nel nuovo posto almeno 1 s prima di poter tornare, perché le barche vicine si muovono di poco e la scritta salterebbe su e giù a ogni fotogramma.
4. La distanza dalla barca resta di 58 px. Con lo zoom più lontano le barche sono piccole e la scritta è già lontana; con quello più vicino una barca è lunga circa 60 px. Lo controllo sulle fotografie prima di toccarlo.

Vale per le scritte in acqua. Nella rotta ottimale (vista dall'alto) non ci sono nomi sulle barche: ci sono solo le scritte dei minuti accanto ai punti verdi, e non toccano le barche.

**Costanti nuove**, scelte nostre di sola grafica e senza fonte:
- trasparenza 40%;
- tempo minimo di 1 s prima che una scritta torni al suo posto.

## Criteri, con soglie fissate prima di provare

| # | Criterio | Soglia |
| --- | --- | --- |
| E1 | Il metro misura davvero: sulla versione di oggi, in 20 regate del torneo col pilota (4 regate × 5 semi, principianti ed esperti), si contano i fotogrammi in cui il rettangolo di una scritta copre lo scafo di un'altra barca | almeno 50 fotogrammi; se sono meno, il problema è raro e lo dico prima di cambiare il gioco |
| E2 | Stesse regate, versione nuova: fotogrammi con una scritta piena (non trasparente) sopra uno scafo | al massimo il 10% di quelli di E1, e 0 sopra la tua barca |
| E3 | Sfarfallio | nessuna scritta cambia posto due volte in meno di 1 s |
| E4 | Le regate non cambiano | `impronta` del guardiano identica al bit, `polare.js` e `raffiche_e_virate.js` identici: si tocca solo il disegno |
| E5 | Giocatore vero | Chromium e Firefox senza `#collaudo`: 0 errori della pagina; fotografie di una partenza affollata prima e dopo |
| E6 | Pannello | 0 px di eccesso a 1360×650 |

## Rischi

- **Una scritta sotto la barca** può cadere sulla scia, o vicino alla linea di partenza e alle sue scritte. Lo guardo sulle fotografie.
- **Il calcolo** costa poco: 3 scritte × 3 barche per fotogramma.
- **Non risolve tutto:** in un mucchio di 4 barche alla boa qualche scritta resterà sopra una barca, ma trasparente.

## Cosa serve da Ale

Il via. Si toccano solo `js/regate.js` (`drawRaceScreen`) e un collaudo nuovo. Versione prevista: 1.2.34.

## E1 misurato sulla versione di oggi (14 novembre, mattina; il gioco non è stato toccato)

`tests/misura_etichette.py`: 20 regate del torneo (4 regate × semi 2301-2305, principianti nei semi dispari, esperti nei pari), in Chromium. La pagina si ridisegna ogni 6 passi, cioè ogni 0,1 s di regata, da 60 s prima del via all'arrivo di tutti. Lo strumento intercetta le scritte mentre il gioco le disegna e le confronta col contorno dello scafo delle altre barche sullo schermo.

- **54 335 disegni, in 1870 almeno una scritta copre lo scafo di un'altra barca: il 3,4%.** La soglia di E1 era almeno 50, quindi il problema è reale e il metro lo vede.
- **In 903 di questi la barca coperta è la tua.** In media sono circa 9 s per regata con una scritta sopra una barca, e circa 4,5 s sopra la tua.
- Da regata a regata il numero varia molto: da 11 a 304 disegni, e da 0 a 155 sopra la tua. Il problema si concentra nelle regate in cui si parte o si gira la boa vicini.
- 0 errori della pagina, picco 62 °C.
- Due coppie di regate danno numeri uguali, «regata 2 / regata 4, seme 2303» e «regata 1 / regata 3, seme 2305»: in quei tornei le due regate hanno lo stesso campo e lo stesso vento. Lo segnalo, ma per E1 non cambia niente.

Con questo metro, E2 chiede: al massimo 187 disegni con una scritta piena sopra uno scafo (il 10% di 1870), e 0 sopra la tua barca, sulle stesse 20 regate.

## Seconda parte: la proporzione da lontano (14 novembre, scelta A di Ale; scritta prima del codice)

Osservazione di Ale: «durante la moviola, che vista tutta dall'alto ha barchette piccolissime e scritte grandi». Le fotografie lo confermano (`tests/output/etichette_lontano_*.png`, tasto 2 premuto 8 volte): con la correzione della prima parte la tua barca si vede, ma la scritta di Lunardi finisce 58 px sotto una barca di pochi pixel, e non si capisce più di chi sia. Ale ha scelto A.

**Modello.**
- Un fattore `k`: quanto la vista è più lontana di quella normale, cioè pixel per metro dello schermo diviso per quelli della vista normale. Vale al massimo 1: avvicinando la vista non cambia niente rispetto a oggi.
- La distanza fra il centro della barca e il bordo vicino della scritta è 40 px × `k`, mai meno di mezza barca sullo schermo + 3 px.
- Le lettere sono 13 px × `k`, mai meno di 10 px. Il rettangolo è alto quanto le lettere + 5 px (oggi 18).
- La scelta sopra/sotto e la trasparenza restano quelle della prima parte.

**Costanti nuove**, nostre e senza fonte: 10 px come lettera più piccola, 3 px di spazio minimo dalla barca.

| # | Criterio | Soglia |
| --- | --- | --- |
| F1 | Vista normale: niente cambia rispetto alla prima parte | `collaudo_etichette` in Chromium con gli stessi totali della prima parte: 54 335 disegni, 0 scritte piene su uno scafo, 2 trasparenti, 163 cambi di posto |
| F2 | Da lontano (tasto 2 × 8), stesse 20 regate: di chi è la scritta. Per ogni scritta disegnata, la barca più vicina al rettangolo deve essere la sua | almeno il 90% delle scritte, contro il valore misurato prima del codice sulla 1.2.33 e sulla prima parte, che riporterò com'è |
| F3 | Da lontano: scritte piene sopra uno scafo | al massimo il 10% della 1.2.33 misurata da lontano, e 0 sopra la tua barca |
| F4 | Da lontano: lettere | mai sotto 10 px |
| F5 | Le regate non cambiano, pannello, pagina senza `#collaudo` in Chromium e Firefox | come E4-E6 |

Le misure «prima» (1.2.33 e prima parte, da lontano) si fanno con lo stesso strumento prima di scrivere il codice.

## Esito (14 novembre, pomeriggio): 1.2.34 fatta, NON chiusa (F2 non passa)

**Prima parte, sopra o sotto e trasparenza.** `collaudo_etichette`, 20 regate:

| | Chromium | Firefox |
| --- | --- | --- |
| E2: disegni con una scritta piena su uno scafo | **0** (1.2.33: 1870) | **0** |
| E2: sopra la tua barca | **0** (1.2.33: 903) | **0** |
| trasparenti | 2 | 79 |
| E3: cambi di posto, di cui a meno di 1 s | 163, **0** | 215, **0** |

- E4: impronta del guardiano identica al bit (`2c0e3804a20d`, semi 1491-1502); `polare.js` e `raffiche_e_virate.js` identici; `collaudo_versione` OK.
- E5: pagina senza `#collaudo`, Chromium e Firefox: versione 1.2.34, 0 errori. Fotografie: `tests/output/etichette_vicino_prima.png` e `_dopo.png`.
- E6: 0 px di eccesso.
- **Da dire:** lo 0 di E2 è quasi garantito per costruzione, perché il gioco fa lo stesso controllo dello strumento, anzi più preciso. Il dato che informa è un altro: le scritte trasparenti sono poche (2 e 79 disegni su circa 55 000), quindi quasi sempre c'è un posto libero.
- **Errori miei nello strumento delle fotografie, corretti prima di riportare:**
  - il segnale «scritta sulla tua barca» restava acceso da un momento precedente;
  - la regata non era quella della misura, perché il gruppo dei rivali nasce dal primo torneo aperto.

  Anche le prime misure «da lontano» non valevano: il tasto 2 premuto prima che il gioco partisse veniva ignorato. Ora lo zoom si imposta all'inizio di ogni regata.

**Seconda parte, proporzione da lontano (scelta A).** `misura_etichette.py` con `ZOOM=8` (vista a 0,17), stesse 20 regate, Chromium:

| | 1.2.33 | prima parte | **A** | soglia |
| --- | --- | --- | --- | --- |
| F1 vista normale, totali come la prima parte | – | – | **identici** (54 335 / 0 / 2 / 163) | identici ✓ |
| F2 scritte più vicine alla propria barca | 45,1% | 53,4% | **88,6%** | ≥ 90% ✗ |
| F3 disegni con una scritta piena su uno scafo | 18 664 (34,3%) | 0 | **0**, 0 sulla tua | ≤ 1866, 0 sulla tua ✓ |
| F4 lettere più piccole | 13 px | 13 px | **10 px** | ≥ 10 ✓ |

**Perché F2 non passa, diagnosi senza toccare niente.** Delle 18 574 scritte «sbagliate», 947 hanno un'altra barca entro 10 px, 7197 fra 10 e 20, 10 413 fra 20 e 40, e solo 17 oltre 40. Da lontano 40 px sono circa 4 lunghezze. La scritta più piccola è comunque larga circa 60 px, quindi con due barche così vicine il rettangolo tocca anche la vicina. Fotografia: `tests/output/etichette_lontano_A.png`, con due scritte impilate fra due barche vicine.

**La 1.2.34 non è chiusa:** la soglia di F2 resta 90%. Strade per Ale:
- **chiudere così**, dichiarando F2 a 88,6%: dal 45% al 89%, nessuna scritta piena sulle barche;
- **aggiungere l'iniziale da lontano**, cioè la strada B scartata prima: solo da lontano e solo quando una barca vicina rende ambigua la scritta. Una scritta di una lettera è larga circa 15 px. Andrebbe rimisurata su semi nuovi.

**Decisione di Ale (14 novembre, sera): «chiudi. proviamo così».** La 1.2.34 è chiusa con F2 all'88,6%, sotto la soglia del 90%, dichiarato. L'iniziale da lontano non è fatta: si riprende solo se, giocando, le scritte da lontano confondono.
