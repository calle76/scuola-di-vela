# Il Coach dopo le misure col pilota «da giocatore»

**Stato: via di Ale il 16 novembre 2026; fatto nella 1.3.13 (fermata 2). Esito al §8: C1, C5, C6 passano; C2 e C4 no; C3, C7 e C8 non misurati.**

16 novembre 2026, gioco alla 1.3.12. Solo documento e strumento di misura (`tests/misura_coach_varianti.py`): il gioco non è stato toccato. Nasce dal §8 di `PROPOSTA-PILOTA-GIOCATORE.md` e dalle risposte di Ale del 16 novembre («il Coach è da migliorare anche nella frase "c'erano altre barche"», «c'è da sistemare quella che non esce mai», «al massimo tre frasi»).

## 1. Che cosa non va oggi

1. **«C'erano altre barche» esce quasi sempre e non distingue niente.** Oggi basta un secondo, nei 60 della finestra peggiore, con una barca entro 3 lunghezze o un cono. Esce in 18 regate su 20 col pilota vecchio (che naviga nel gruppo) e in 16 su 20 col pilota nuovo (che naviga più pulito e arriva primo o secondo): due modi di navigare diversi, la stessa frase.
2. **«Hai virato N volte vicino alla boa: ne bastava una» non esce mai con 2 o 3 virate.** Ogni virata in più pesa 2 s e sotto i 5 s il Coach tace: esce solo da 4 virate. Col pilota vecchio 2 o 3 virate in 24 regate su 40: mai detta.
3. **«Hai virato per la boa N m oltre la layline» guarda solo l'ultima virata del lato.** Se dopo la virata lunga ce n'è un'altra vicino alla boa, non esce: con un errore di 25 m messo apposta, 4 volte su 10.

## 2. Che cosa si propone

**A. «C'erano altre barche»: la finestra è affollata solo se le altre barche ci sono state per almeno 20 secondi su 60, e i primi 15 secondi dopo il taglio della linea non contano.** Il resto non cambia: quando la finestra non è affollata, la stessa perdita la dice «qui hai perso di più».

Perché i primi 15 secondi: al via le barche sono insieme per forza, e il costo di una brutta partenza ha già la sua frase.

**B. La frase delle virate esce da 3 virate in su**, con un peso di almeno 5 s (la soglia sotto cui il Coach tace). Con 2 virate resta zitto: una virata in più costa 2 s, è poco. Il testo non cambia.

**C. «Oltre la layline» guarda la prima virata fatta oltre la layline**, non l'ultima del lato. Se dopo ce ne sono altre vicino alla boa, vale la frase col peso più grande fra le due (oltre la layline, o troppe virate).

**D. Restano tre frasi al massimo.** Con A il posto più alto non lo prende più sempre la stessa frase.

**Il volto non cambia regola.** Misurato: con nessuna delle varianti di A e B cambia un solo volto su 20 regate (vedi §3). La perdita resta la stessa, cambia solo il nome della frase. Coi piloti il Coach è arrabbiato in 10-11 regate su 20 per penalità e scuffie, serio in 7-8, contento in 2: quanto sia severo con una persona lo dicono le regate registrate di Ale e Lucio, non i piloti.

## 3. Misure già fatte (senza toccare il gioco)

Lo strumento mette nella pagina una copia della funzione del clou con due numeri in più e fa ricalcolare le frasi al gioco. Riscontro: coi numeri di oggi dà le stesse frasi del gioco in 20 regate su 20. Semi 2601-2605, 20 regate per riga; numero di regate in cui esce la frase.

| Regola dell'affollato | Pilota vecchio: «altre barche» | «qui hai perso di più» | Pilota nuovo: «altre barche» | «qui hai perso di più» |
| --- | --- | --- | --- | --- |
| oggi (1 s) | 18 | 4 | 16 | 11 |
| oggi, senza i primi 15 s | 18 | 5 | 14 | 12 |
| almeno 10 s su 60 | 13 | 11 | 12 | 15 |
| almeno 10 s, senza i primi 15 | 13 | 13 | 10 | 15 |
| almeno 20 s su 60 | 10 | 14 | 5 | 18 |
| **almeno 20 s, senza i primi 15 (proposta A)** | **10** | **14** | **3** | **19** |
| almeno 30 s su 60 | 7 | 17 | 4 | 19 |
| almeno 30 s, senza i primi 15 | 7 | 18 | 2 | 19 |

Con la proposta A il pilota che naviga nel gruppo se la sente dire in 10 regate su 20, quello che naviga pulito in 3: la frase torna a dire qualcosa. Con 30 s la differenza si stringe (7 contro 2-4).

Frase delle virate (pilota vecchio, con la regola dell'affollato di oggi): le regate con una frase sulla boa passano da 7 a 10 con la soglia a 3 virate (proposta B), a 11 con la soglia a 2.

Volti, in tutte le righe: pilota vecchio 2 contento, 7 serio, 11 arrabbiato; pilota nuovo 2, 8, 10.

## 4. Criteri per la fermata 2 (attese nostre, scritte prima)

Le costanti (20 s, 15 s, 3 virate) sono state scelte sui semi 2601-2605. La conferma è sui semi 2611-2615, su cui le varianti non sono mai state misurate.

| # | Cosa | Soglia |
| --- | --- | --- |
| C1 | «altre barche» col pilota nuovo, semi di conferma | al più 8 regate su 20 (è il G2 del pilota) |
| C2 | «altre barche» col pilota vecchio meno col pilota nuovo, semi di conferma | almeno 4 regate di differenza |
| C3 | frase delle virate: con 3 o più virate entro 80 m e nessuna virata oltre la layline, la frase c'è fra quelle calcolate (prima del taglio a tre) | tutte le regate di quel tipo, almeno 5 casi |
| C4 | errore messo apposta, 25 m oltre la layline (10 regate): la frase «oltre la layline» esce | almeno 8 su 10; il numero entro 5 m da quello del Coach di oggi nei casi in cui oggi esce |
| C5 | arrivi, penalità e classifica delle regate | identici alla 1.3.12 (il Coach legge soltanto) |
| C6 | `collaudo_coach.py` (K1-K11) col suo ricalcolo indipendente aggiornato alla regola nuova | verde |
| C7 | le regate registrate di Ale del 15-16 novembre, se ci sono: quante volte «altre barche» prima e dopo | solo riportato |
| C8 | pannello a 1360x650 | 0 px di eccesso |

Con meno casi di quelli scritti: «NON VALIDO».

## 5. Costanti nuove (ipotesi nostre)

- `COA_AFF_S` = 20: secondi affollati minimi nella finestra di 60.
- `COA_AFF_VIA` = 15: secondi dopo il taglio della linea che non contano come affollati.
- soglia della frase delle virate: 3 (oggi di fatto 4).

## 6. Rischi

- **Meno «altre barche» vuol dire più «qui hai perso di più» detto a chi era davvero in mezzo alle barche per meno di 20 secondi.** È una frase più dura: la rotta ottimale non tiene conto delle altre barche. Per questo 20 e non 30.
- **I numeri vengono da due piloti, non da persone.** C7 serve a questo; se le regate di Ale dicono altro, valgono quelle.
- **Il ricalcolo di `collaudo_coach.py` va riscritto insieme** (K4, K5): se si aggiorna copiando la regola nuova dal gioco non controlla più niente. Va riscritto dai dati registrati, come oggi.
- **C tocca `rotSpiega`**, che serve anche al riassunto «dove hai perso»: la frase di quel riassunto cambia insieme.

## 7. Che cosa serve da Ale

Il via, oppure no. Una sola scelta possibile da cambiare prima di cominciare: i 20 secondi (la tabella del §3 mostra 10 e 30).

## 8. Esito (16 novembre 2026, 1.3.13)

Fatte A, B, C e D come scritte. **Un'aggiunta non scritta:** le virate dentro un giro di penalità non contano più fra le virate vicino alla boa (con la soglia a 3, due giri di penalità vicino alla boa avrebbero fatto dire «hai virato 3 volte»).

| # | Cosa | Soglia | Misurato | Esito |
| --- | --- | --- | --- | --- |
| C1 | «altre barche» col pilota nuovo, semi 2611-2615 | al più 8 su 20 | 5 | **passa** |
| C2 | pilota vecchio meno pilota nuovo, semi 2611-2615 | almeno 4 | 6 − 5 = 1 | **non passa** |
| C3 | frase delle virate con 3 o più virate | tutte | non misurato come scritto: la lista prima del taglio a tre non si legge da fuori. Col pilota vecchio la frase passa da 3 regate su 40 a 12 | **non misurato** |
| C4 | 25 m oltre la layline messi apposta: la frase esce | almeno 8 su 10 | 7 (prima 4); dice 28-43 m | **non passa**, di una |
| C5 | regate identiche | identiche | `collaudo_coach` K1: 20 su 20 uguali al riferimento; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici | **passa** |
| C6 | `collaudo_coach.py` col ricalcolo aggiornato | verde | verde; clou ricalcolato uguale in 14 regate | **passa** |
| C7 | regate registrate di Ale | solo riportato | non ci sono file nuovi da leggere | **non fatto** |
| C8 | pannello a 1360x650 | 0 px | `collaudo_coach` K2: 0 px in 21 casi (le frasi non sono più lunghe) | **passa** |

«Altre barche», regate su 20: semi di scelta da 18 (vecchio) e 16 (nuovo) a **10 e 3**; semi di conferma da 18 e 16 a **6 e 5**.

**C2, che cosa dice.** Sui semi di scelta la regola distingue i due piloti (10 contro 3), sui semi di conferma no (6 contro 5). La soglia dei 20 secondi è stata scelta sui primi: la conferma dice che la differenza fra i due piloti non è solida. Resta vero che la frase esce molto meno (da 16-18 a 3-10 regate su 20). Riportato com'è; i 20 secondi non sono stati ritoccati.

**C4.** Nelle 3 regate su 10 in cui la frase non esce, o passano davanti tre frasi più pesanti, o il pilota non ha virato davvero oltre la layline del Coach.

**Nel collaudo:** K4 pretendeva «qui hai perso di più» ogni volta che c'era una perdita libera grande. Con la regola nuova le perdite libere sono molte di più, e in due regate (2601-1, 2603-1) la frase resta fuori perché ce ne sono tre più pesanti: ora K4 la pretende solo quando c'è posto. Cambiato dopo aver visto il rosso, detto qui.

**Volti nelle 20 regate del collaudo:** 11 arrabbiato, 7 serio, 2 contento, come prima.
