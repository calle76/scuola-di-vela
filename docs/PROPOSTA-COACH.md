# Proposta: il coach nella moviola (fermata 1)

15 novembre 2026, sera. Versione **1.3.3** del piano di Deriva, al posto del «momento clou» (`PROPOSTA-DERIVA-CIRCUITI.md`). Nasce dalla chiacchierata con Ale dello stesso giorno. **Solo proposta: in `js/` niente finché Ale non dà il via.**

## Cosa è già deciso (Ale, 15 novembre 2026)

- Il coach vive nella moviola, a regata finita, e **prende il posto del riassunto di oggi** della rotta ottimale (il paragrafo lungo sotto la mappa).
- È una **figura con un volto** (lo crea Ale con un'AI, come quelli dei rivali), **senza nome: si chiama «Coach»** (Ale, 15 novembre: così nella stagione con un amico non ci sono due nomi diversi).
- Serve **in carriera, nei tornei**, e in tutte le regate dove oggi c'è la rotta ottimale.
- **Frasi corte**: se non ci stanno, si accorciano le frasi.
- La **migliore in assoluto (V)** resta com'è, uno strumento a sé: con V si vede tutta la regata disegnata. **Il coach non dipende da V** (Ale, 15 novembre: «non vorrei complicare le cose se premo o no il tasto V, dimmi tu»; questa è la mia scelta, da confermare col via): dice le stesse cose che V sia premuto o no.
- Il **momento clou** non si butta: diventa la prima cosa che il coach indica.
- La **situazione da ripetere** (prove estratte dalle regate) e le **domande sulle penalità** restano per i livelli dopo (il Fiocco), come in `PROPOSTA-COACH-REGISTRATORE.md` fasi 3 e 4.

## Il nome (deciso)

«Coach». Le proposte di nome (Ettore Marin, Renata Fabbri, Carlo Mancin) sono cadute il 15 novembre.

## Cosa fa (il modello più semplice)

A regata finita, aprendo «Rotta ottimale», accanto alla mappa compare un riquadro con il volto, la scritta «Coach» e **al massimo tre frasi**. Ogni frase:
- è costruita da un **modello fisso riempito con numeri misurati** (nessun testo inventato al momento);
- ha un **momento della regata**: cliccandola, la moviola salta lì (qualche secondo prima, come per i segni);
- dove serve, rimanda a **una lezione** («lezione 23»).

Le frasi, in ordine di importanza; il coach dice le tre più pesanti, contate in secondi:

| # | Frase (esempio) | Da che cosa si misura | Lezione |
| --- | --- | --- | --- |
| F1 | **Momento clou.** «Qui hai perso di più: fra 4:10 e 5:10 il distacco dalla rotta ottimale è cresciuto di 35 m.» Più, se c'è, il motivo di quel tratto: vento girato, virate in più, raffiche (i «motivi» che la rotta ottimale calcola già) | il minuto in cui il filo bianco (distanza fra te e la rotta ottimale nello stesso istante) si allunga di più | 11 (salti di vento), 8 (raffiche) |
| F2 | **Coperto.** «Fra 2:30 e 3:20 eri nel cono d'ombra della Rossa: circa 9 s persi.» | il vento tolto dal cono, registrato istante per istante, trasformato in velocità persa con la polare del gioco | — (testo del torneo, F75) |
| F3 | **Alla boa.** «Sei arrivato alla boa 25 m oltre la layline.» / «Sei arrivato corto: due virate in più negli ultimi 80 m.» | la tua traccia e la layline col vento di quel momento | 23 |
| F4 | **Partenza.** «Al via eri 4 s dietro la linea, a 1,2 nodi: sei partito lento.» | i secondi fra lo sparo e il tuo taglio della linea e la velocità allo sparo (già registrati); nessun calcolo della migliore in assoluto | 18 |
| F5 | **Penalità.** «A 6:40 contatto con colpa con la Verde: +1 punto.» | i segni dei contatti già nella moviola | 12-15 |
| F6 | **Bene.** Se in nessun lato hai perso più di 5 s: «Bolina quasi perfetta: 3 s dalla rotta ottimale.» | i secondi per lato di oggi | — |

**Il punto debole, detto apertamente.** La rotta ottimale conosce il vento in anticipo e ignora le altre barche. F2 toglie la parte che dipende dalle vele altrui; il resto (dover cedere, scansare) il gioco non lo misura. Per questo: F1 sceglie il momento clou **solo fuori dai tratti in cui eri coperto o avevi una barca entro 3 lunghezze**; se il tratto peggiore era proprio lì, il coach lo dice («qui c'erano altre barche: la rotta ottimale non ne tiene conto»).

**Cosa cambia nel codice** (per capire il peso, non è ancora il via):
- `moviola.js`: in ogni fotogramma registrato si aggiunge, per il giocatore, la quota di vento tolta dal cono e chi la toglie (oggi c'è già durante la regata, `b.cop` e `b.copDa`); sola lettura, come il resto della moviola;
- `rotta.js`: le frasi, a partire dai motivi e dai secondi per lato che ci sono già; il paragrafo di oggi si toglie (la legenda dei colori resta, in una riga);
- `index.html`: il riquadro del coach; il volto come immagine piccola (finché non arriva, un cerchio con le iniziali).

Fuori dalla Scuola come oggi: dove non c'è la rotta ottimale non c'è il coach. **Mai obbligatorio**; i punti di Deriva («hai rivisto con il coach il tuo momento clou», area Esperienza) arrivano con la 1.3.4.

## Criteri (soglie nostre, scritte prima)

Tutti in Chromium e Firefox, regate del torneo col pilota a passi fissi, semi 1-20 per scegliere e 21-40 per confermare (regola dei semi).

| # | Criterio | Soglia |
| --- | --- | --- |
| K1 | Niente cambia sotto | `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; arrivi, penalità e posizioni del torneo identici al bit prima e dopo su 20 regate (la registrazione del cono è sola lettura) |
| K2 | Spazio | riquadro del coach dentro la moviola a 1360x650, senza scorrere, nel caso peggiore (tre frasi più lunghe, anche con la migliore in assoluto aperta); 0 px di eccesso |
| K3 | Ogni frase ha il suo numero | in ogni regata ogni frase detta contiene almeno un numero, e quel numero coincide (entro l'arrotondamento) con quello ricalcolato dal collaudo per conto suo; al più 3 frasi |
| K4 | Il momento clou è quello vero | il collaudo cerca da solo il minuto in cui il filo si allunga di più (fuori dai tratti coperti o affollati): coincide con quello del coach in 20 regate su 20 |
| K5 | Coperto: niente di inventato | regate costruite con il giocatore tenuto nel cono di una barca per 30-60 s: F2 c'è in 10 su 10, con i secondi persi entro ±25% della stima indipendente; regate senza nessuna barca entro 10 lunghezze: F2 mai (0 su 10) |
| K6 | Il salto | cliccando una frase la moviola va al suo momento, entro 1 s (meno i secondi di anticipo dichiarati) |
| K7 | Bene quando va bene | il pilota che segue la rotta ottimale in una regata senza avversari: nessuna frase «hai perso», F6 c'è |
| K9 | Uguale con e senza V | in 10 regate le frasi del coach sono identiche prima e dopo aver premuto V |
| K8 | Pagina vera | senza `#collaudo`, dal menu al torneo alla moviola: coach visibile, 0 errori; il calcolo delle frasi aggiunge al più 200 ms a quello della rotta ottimale |

## Costanti nuove (ipotesi nostre)

Massimo 3 frasi; finestra del momento clou 60 s; «coperto» quando il cono toglie almeno il 10% del vento per almeno 10 s; minimo 5 s persi per citare una perdita; «affollato» = una barca entro 3 lunghezze; «oltre la layline» da 10 m; anticipo del salto 5 s.

## Fonti

Nessuna affermazione nautica nuova: le frasi rimandano a lezioni già verificate (F75 per il cono, F77-F78 per la layline, le regole per penalità e partenza). **Volti fatti con un'AI:** si cita lo strumento usato e si controllano le sue condizioni d'uso (principio 5); nessun volto che somigli a una persona reale.

## Rischi

- **Consigli sbagliati:** la rotta ottimale non sa delle altre barche; K4, K5 e la frase «qui c'erano altre barche» lo limitano, non lo eliminano.
- **Il filo in metri non è tempo:** 35 m in bolina e 35 m in poppa non valgono gli stessi secondi. Se nella fermata 2 il momento clou «in metri» risulta strano, si converte in secondi con la polare (detto prima, non dopo).
- **Spazio:** tre frasi e un volto nella moviola a 650 px di altezza sono pochi; si accorciano le frasi (decisione di Ale).
- **Calcolo:** la rotta ottimale è già pesante sul PC di Ale; le frasi usano i suoi risultati, non la ricalcolano.

## Cosa serve da Ale

1. Il via.
2. ~~Il nome~~: deciso, «Coach».
3. Il volto: quando c'è, un file quadrato (va bene 256x256 px, PNG o JPG) e il nome dello strumento con cui è fatto. Fino ad allora le iniziali in un cerchio.

## Esito (fermata 2, 15 novembre 2026)

Fatto nella 1.3.3. Tutti i criteri K1-K9 passano in Chromium e Firefox su 20 regate del torneo col pilota (semi 2601-2605, mai usati prima); numeri in `CHANGELOG.md` 1.3.3.

- **Cambiato prima di misurare le soglie:** il clou non usa più la lunghezza del filo, ma i metri di percorso mancanti in più della rotta ottimale. Il filo cresce anche quando le due rotte vanno su lati diversi del campo senza perdere niente: nella prima prova il «tratto peggiore» cadeva quasi sempre nel primo minuto dopo il via.
- **Da decidere (Ale):** «c'erano altre barche» esce in 17 regate su 20, perché la regola dell'affollato (anche un solo secondo con una barca entro 3 lunghezze) col pilota, che naviga in gruppo, scatta quasi sempre. Strade: (a) tenerla così e guardare cosa succede a un giocatore vero; (b) affollato solo se le barche vicine ci sono per più di metà del minuto. Consiglio (a), poi decidere con le regate registrate.
- «Coperto» non è uscito in nessuna regata vera: i tratti coperti sono costati 0,9-2,7 s, sotto i 5 s.

## Il volto (1.3.4, 15 novembre 2026)

Tre espressioni fatte da Ale con ChatGPT (F104), ritagliate a 128 px in `img/`. Regola di Ale: arrabbiato con una penalità o la partenza anticipata; contento con «quasi perfetta» o se nessuna frase pesa almeno 10 s (soglia nostra); serio altrimenti. Criterio K10 in `collaudo_coach.py`.
