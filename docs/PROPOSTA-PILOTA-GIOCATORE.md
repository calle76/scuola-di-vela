# Un pilota «da giocatore» per i collaudi

**Stato: via di Ale il 16 novembre 2026; fatto e misurato (fermata 2). Esito al §8: G1, G3, G5 e G7 passano; G2 e G6 no; G4 no sui semi di scelta e sì su quelli di conferma.**

15 novembre 2026, gioco alla 1.3.11. Solo documento: nessun codice del gioco né dei collaudi è stato toccato. Chiesta da `archivio/PER-FABLE.md` §3.

## 1. Il problema

Quasi tutti i collaudi che corrono una regata guidano la barca del giocatore con `__sv.pilota` (`js/avvio.js`), che è la guida dei rivali principianti messa sulla barca del giocatore. Va bene per sapere se una regata arriva in fondo. Non va bene per misurare le cose che parlano **del giocatore**, perché quel pilota:

- naviga in mezzo al gruppo: il Coach dice «c'erano altre barche» in 17 regate su 20 (`PROPOSTA-COACH.md`, Esito);
- scuffia spesso: volto arrabbiato in 10 regate su 20 per le scuffie;
- vira troppo vicino alla boa (circa 1,7 virate negli ultimi 40 m, `DA-FARE.md` voce 1b);
- regola la vela con un errore sorteggiato e cambia bordo a tempo, non quando conviene: nella finale arriva fra i primi 3 in 0-2 casi su 10.

Con un pilota così non si può decidere la regola dell'«affollato» del Coach né la quota del merito di Deriva (tappa 7): i numeri direbbero come gioca il pilota, non come gioca una persona.

## 2. Il modello più semplice plausibile

Un secondo pilota, **solo per i collaudi**, che fa poche cose pulite. Non è un modello di persona: è un metro. Quattro regole, tutte con funzioni che il gioco ha già.

1. **Partenza:** quella del pilota di oggi (funziona), ma coi numeri degli esperti fissati al centro della fascia, senza sorteggio.
2. **Bolina a due bordi con la layline:** parte sul bordo che avvicina di più alla boa, lo tiene fino alla layline (calcolata come la disegna il gioco, con lo scarroccio: `layLee`), vira una volta e va alla boa. Niente cambi di bordo a tempo.
3. **Aria libera:** se resta nel cono d'ombra di un'altra barca (almeno il 10% di vento in meno, la stessa soglia del Coach) per più di 5 s e mancano più di 60 m alla layline, vira via. Per il resto cede e tiene la rotta come i rivali (stessa funzione `chiCede`).
4. **Vela e scuffie:** vela regolata senza errore; lasca prima (da 18° di sbandamento invece di 22°); in poppa stramba solo con la vela già chiusa, come fa già il pilota.

**Dove sta:** in un file dei collaudi (`tests/pilota_giocatore.js`), che il collaudo consegna alla pagina prima di caricarla. Il gioco non cambia: nessuna riga in `index.html` né in `js/`, quindi non è una versione. Il pilota di oggi resta dov'è e tutti i collaudi di oggi continuano a usarlo (i loro numeri di riferimento non si toccano).

**Errori messi apposta.** Il pilota nuovo accetta tre errori a comando: partire N secondi tardi, virare N metri oltre la layline, virare due volte vicino alla boa. Servono a controllare che il Coach dica proprio quell'errore, col numero giusto. Oggi questo controllo non c'è: si controlla che ogni frase abbia un numero, non che la frase sia quella giusta per l'errore fatto.

## 3. Criteri, scritti prima (attese nostre)

Misura: 20 regate del torneo, semi 2601-2605 (gli stessi di `collaudo_coach.py`, così c'è il confronto col pilota di oggi), 4 regate per seme. Le costanti del pilota (5 s, 60 m, 18°) si scelgono su questi semi e si confermano sui semi 2611-2615, mai guardati prima. Se la conferma non passa si riporta com'è.

| # | Cosa | Oggi (pilota vecchio) | Soglia |
| --- | --- | --- | --- |
| G1 | regate con almeno una scuffia | 10 su 20 | al più 2 su 20 |
| G2 | regate in cui il Coach dice «c'erano altre barche» | 17 su 20 | al più 8 su 20 |
| G3 | virate negli ultimi 40 m prima della boa 1, in media | circa 1,7 (rivali; da misurare sul pilota) | al più 1,2 |
| G4 | tempo perso in bolina sulla rotta ottimale, mediana | da misurare prima di tutto | almeno il 30% in meno del pilota vecchio |
| G5 | arriva in fondo, senza squalifica | da misurare | 20 su 20 |
| G6 | errori messi apposta (10 regate per errore): il Coach dice la frase di quell'errore, e il numero è entro 2 s o 5 m da quello imposto | controllo che oggi non esiste | almeno 8 su 10 per ogni errore |
| G7 | il gioco non cambia | — | `git diff` vuoto su `index.html` e `js/`; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici |

G1-G5 devono avere 20 regate misurate davvero, G6 dieci per errore: con meno, «NON VALIDO».

## 4. Costanti nuove (tutte ipotesi nostre)

- 5 s nel cono prima di virare via; 60 m dalla layline sotto i quali non si vira più via; 18° di sbandamento da cui si lasca.
- Numeri degli esperti al centro della fascia: bolina a 46,5° dal vento, poppa a 152,5°, margine di partenza 0,5 s (centri delle fasce di `aiParams`).

Nessuna entra nel gioco.

## 5. Che cosa non è

- Non dice come gioca Ale o Lucio: per quello restano le loro regate registrate. La regola dell'«affollato» si riguarda con quelle (decisione di Ale del 16 novembre); il pilota nuovo dà solo un secondo numero, meno falsato del 17 su 20.
- Non è un giudizio nautico: «pulito» qui vuol dire layline, aria libera e niente scuffie, tre cose che le lezioni del gioco già insegnano (8, 23 e il cono d'ombra del torneo).
- Non migliora i rivali. Se la bolina con la layline andasse molto meglio di quella dei rivali, è un'informazione per la voce 2, non una modifica.

## 6. Rischi

- **Troppo bravo.** Il Coach potrebbe dire quasi sempre «regata quasi perfetta» e la misura servirebbe a poco: per questo ci sono gli errori messi apposta (G6).
- **La layline provata sui rivali non è andata bene** (`PROPOSTA-AVVERSARI-BOLINA.md` §13-14: boa toccata 22 → 44-55). Lì però la regola si aggiungeva ai bordi a tempo e all'arrivo da sinistra; qui il bordo è uno solo. Se G3 o G5 non passano, è lo stesso difetto e lo si riporta.
- **Due piloti da tenere.** Un pezzo in più da mantenere quando cambia la guida dei rivali; costa poco perché usa le loro stesse funzioni.
- **Quota del merito.** Anche col pilota nuovo la quota (22 su 24) non si decide da sola: dà quante stagioni «senza ritiri» arrivano a quota, non se la quota è giusta. La decide Ale alla tappa 7.

## 7. Cosa serve da Ale

Il via, oppure no. Nessuna domanda aperta: i numeri del §4 sono ipotesi nostre e si possono cambiare prima di cominciare.

## 8. Esito (16 novembre 2026, fermata 2)

**Che cosa c'è.** `tests/pilota_giocatore.js` (il pilota: il collaudo lo consegna alla pagina e lui prende il posto di `__sv.pilota`; quello di prima resta in `__sv.pilotaVecchio`) e `tests/misura_pilota_giocatore.py` (lo strumento di misura). Il gioco non è stato toccato. Nessun collaudo del giro usa ancora il pilota nuovo.

**Aggiunte rispetto alla proposta, dette qui:**
- il pilota **fa i giri di penalità** (con la sequenza dei rivali). Senza, arrivava squalificato in 5 regate su 20 e G5 non poteva passare; strambando nei giri scuffiava, quindi nei giri chiude la vela sopra i 120° dal vento (costante nuova, ipotesi nostra);
- una pausa di 15 s fra due virate «per l'aria libera» e un margine di 2° sulla layline (ipotesi nostre; provati 0° e 1°: non cambia niente di misurabile);
- G4 si misura sul **primo lato di bolina** (dal taglio della linea alla boa 1), contro lo stesso lato della rotta ottimale;
- G6 «partenza in ritardo» si è fatto con 15 s e non 8, perché il pilota senza errori taglia già la linea fino a 8,6 s dopo il via.

Le costanti (5 s, 60 m, 18°) sono rimaste quelle della proposta: sui semi di scelta le alternative provate (3 s e 40 m; 15°) non andavano meglio.

**Numeri, 20 regate per riga:**

| # | Cosa | Soglia | Vecchio, scelta (2601-2605) | Nuovo, scelta | Vecchio, conferma (2611-2615) | Nuovo, conferma | Esito |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G1 | regate con una scuffia | al più 2 | 7 | 2 | 6 | 2 | **passa** |
| G2 | regate con «c'erano altre barche» | al più 8 | 18 | 16 | 18 | 16 | **non passa** |
| G3 | virate negli ultimi 40 m dalla boa 1 | al più 1,2 | 1,80 | 0,75 | 1,70 | 0,70 | **passa** |
| G4 | tempo perso nella prima bolina, mediana | −30% sul vecchio | 22,7 s | 21,5 s (−5%) | 27,3 s | 11,0 s (−60%) | **non passa sulla scelta, passa sulla conferma** |
| G5 | arrivate senza squalifica | 20 | 17 | 20 | 17 | 20 | **passa** |
| G7 | il gioco non cambia | diff vuoto | — | `git diff` vuoto su `js/` e `index.html` | — | idem | **passa** |

In più: posto medio 2,35 e 2,20 col nuovo contro 2,75 e 2,95 col vecchio; fra i primi 3 in 14 e 16 regate su 20 (vecchio 13 e 11).

**G4, perché è così diverso fra i due gruppi.** I giri di penalità si fanno in bolina e costano: nelle sole regate senza giri la mediana del nuovo è 12,1 s (15 regate, scelta) e 5,8 s (15 regate, conferma), contro 21,4 e 26,6 del vecchio. Prima di aggiungere i giri, sui semi di scelta il nuovo era a 15,7 s (−31%), ma con 5 squalifiche.

**G2, perché non passa.** Col pilota nuovo l'«affollato» scatta in 16 regate su 20, quasi come col vecchio. Ma è cambiato dove: in 8 casi su 16 (scelta) e 9 su 16 (conferma) la finestra comincia **nei primi 15 secondi dopo il via**, quando le barche sono tutte insieme per forza; col vecchio erano 0 su 18 e 2 su 18. Cioè: con quattro barche che partono dalla stessa linea, la regola di oggi (basta un secondo con una barca entro 3 lunghezze) scatta quasi sempre, anche per chi poi naviga da solo e arriva primo. Questo è un dato per la decisione di Ale sulla regola, non un difetto del pilota che si possa togliere con le sue tre costanti.

**G6, errori messi apposta (10 regate per errore, semi 2601-2603): non passa nessuno dei tre.**

| Errore | Fatto davvero | Il Coach lo dice | Numero giusto | Perché |
| --- | --- | --- | --- | --- |
| partenza 15 s in ritardo | 9 su 10 (linea tagliata a 15,5-26,4 s) | 9 su 10, col numero uguale al taglio vero | 7 su 10 entro 2 s da 15 | in 2 regate il pilota taglia ancora più tardi (20 e 26 s); in una non riesce a ritardare |
| virata 25 m oltre la layline | 10 su 10 | 4 su 10 (dice 28, 32, 42, 43 m) | 1 su 10 entro 5 m | vedi sotto |
| due virate in più vicino alla boa | 3 su 10 | 0 su 10 | — | vedi sotto |

Che cosa si è capito sul Coach (cose vere, da decidere con Ale, non corrette):
1. **«Oltre la layline» guarda solo l'ultima virata del lato.** Se dopo la virata lunga ce n'è un'altra vicino alla boa (al pilota capita in media 0,75 volte), la frase non esce.
2. **Tre frasi al massimo:** «altre barche» (peso 20-45) e una penalità (20) passano davanti a un errore di layline da 25 m (peso 12-20).
3. **«Hai virato N volte vicino alla boa: ne bastava una» non può uscire con 2 o 3 virate.** Ogni virata in più pesa 2 s e sotto i 5 s il Coach tace: la frase esce solo da 4 virate in su. Contato sulle 80 regate misurate (il Coach conta le virate entro 80 m dalla boa): col pilota vecchio 2 o 3 virate in 24 regate su 40, e la frase non esce mai; 4 o più in 6 regate, e la frase esce in 3 (nelle altre passano davanti altre frasi). Col pilota nuovo 2 o 3 virate in 12 regate su 40, mai detta. O la soglia o il testo sono da rivedere.
4. Il numero del Coach per la layline è più grande dell'errore imposto di 3-18 m perché il pilota, anche senza errore, vira già 14-17 m oltre la layline del Coach (le due layline non sono la stessa: la sua è la rotta di bolina più lo scarroccio più 2°; quella del Coach è l'angolo migliore della polare).

**Difetti del pilota rimasti (detti, non corretti):**
- prima del via tocca un'altra barca con colpa in 7 regate su 20 (il vecchio 1-2): la partenza è ancora quella dei rivali, coi numeri degli esperti;
- taglia la linea tardi (mediana 5,5 s sulla scelta, 1,8 s sulla conferma; fino a 8,6 s);
- l'errore «due virate» riesce solo 3 volte su 10.

**Che cosa serve da Ale.** (a) Se il pilota nuovo, così com'è, deve entrare in qualche collaudo (per esempio una seconda misura in `collaudo_coach.py`) o restare uno strumento a parte. (b) I punti 1-3 sul Coach: tenerli, o una proposta per cambiarli. (c) La regola dell'«affollato»: il dato dei primi 15 secondi dopo il via.

## 9. Dopo le risposte di Ale (16 novembre, sera)

- **Il pilota resta uno strumento a parte** (Ale: «è da sistemare a parte»): non entra nei collaudi del giro.
- **Partenza più morbida, come opzione** (`--opz partenza=1`): fino al taglio della linea il pilota usa i numeri dei principianti (centro della fascia), poi quelli degli esperti. Misurata sui due gruppi di semi, 20 regate ciascuno:

| Cosa | Senza, scelta | Con, scelta | Senza, conferma | Con, conferma |
| --- | --- | --- | --- | --- |
| contatti con colpa prima del via (regate) | 7 | 4 | 7 | 3 |
| taglio della linea, mediana | 5,5 s | 2,3 s | 1,8 s | 2,9 s |
| tempo perso nella prima bolina, mediana (G4) | 21,5 s | 11,6 s | 11,0 s | 9,2 s |
| regate con una scuffia (G1, al più 2) | 2 | 3 | 2 | 3 |
| arrivate senza squalifica (G5, 20) | 20 | 20 | 20 | 19 |
| fra i primi 3 | 14 | 17 | 16 | 18 |

  Con la partenza morbida G4 passa su tutti e due i gruppi (−49% e −66% sul pilota vecchio), ma G1 e G5 mancano la soglia di una regata. Per questo resta un'opzione e non il comportamento di base. I contatti prima del via non sono spariti (3-4 regate su 20): la partenza è sempre quella dei rivali.
- **Il Coach:** le tre cose del §8 sono diventate una proposta, `PROPOSTA-COACH-2.md` (fermata 1).
