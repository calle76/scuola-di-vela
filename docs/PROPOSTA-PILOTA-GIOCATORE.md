# Proposta: un pilota «da giocatore» per i collaudi (fermata 1)

15 novembre 2026, gioco alla 1.3.11. Solo documento: nessun codice del gioco né dei collaudi è stato toccato. Chiesta da `PER-FABLE.md` §3.

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
