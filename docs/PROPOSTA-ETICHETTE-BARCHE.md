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
