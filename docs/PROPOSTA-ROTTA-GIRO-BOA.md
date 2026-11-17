# Proposta: la rotta ottimale deve girare la boa come la gira il gioco

*Fermata 1, 17 novembre 2026. Voce 50 di `DA-FARE.md`, osservazione 134. Nessun codice nel gioco finché non arriva il via di Ale.*

## Da dove viene

Ale, 17 novembre, su una foto di Lucio (regata del 21:00, vento 180°): «la rotta ideale calcolata gira la boa dalla parte opposta». Misurato il giorno stesso (`tests/misura_lato_boa.py`, 90 regate in Chromium, principianti, 8 venti, 10 e 12 nodi): la rotta ottimale del giocatore ha almeno un attraversamento della semiretta della boa nel verso sbagliato in **24 regate su 90**, quella in assoluto in **9 su 90**, quelle delle altre barche in **77 rotte su 270**.

## Il difetto

- **Gioco** (`roundCheck`, `js/gioco.js`): ogni attraversamento della semiretta che esce dalla boa (verso `mk.out`, entro 90° da quella direzione, oltre 1,5 m dalla boa) vale +1 se giusto, −1 se sbagliato; la boa è girata solo con somma ≥ 1. «Sbagliato poi giusto» fa 0: boa **non** girata.
- **Rotta ottimale** (`rotCancBoa` e `rotLato`, `js/rotta.js`): il lato finisce al primo attraversamento giusto a più di 2 m dalla boa, e **non controlla** se prima ce n'è stato uno sbagliato. Esempio (seme 2, 180°, 10 nodi): scende a est della boa, passa 3 m a sud verso ovest, vira sul posto, torna a est: tocca la punta della boa e risale. Una barca vera così non avrebbe girato.
- **Conseguenza:** la rotta ottimale è più corta di una valida, quindi «quanto hai perso», le frasi del Coach che ne dipendono (clou, «oltre la layline», perdita in bolina) e le misure dei rivali sulla rotta ottimale (`misura_avversari_rotta.py`) sono sovrastimate in circa una regata su tre. **Di quanto non è misurato**: è il numero 4 dei criteri qui sotto.

## Modello più semplice

In `rotLato`, un passo che attraversa la semiretta nel verso sbagliato (stesso test di `roundCheck`: entro 90° dalla direzione di uscita, oltre 1,5 m dalla boa) **non genera il punto nuovo**. Così nessuna rotta può avere un −1 e, quando arriva al cancello (+1), la somma è 1: come per una barca vera. Un solo controllo in più dentro il ciclo che c'è già; la stessa funzione serve la rotta del giocatore, quella in assoluto, quelle dei rivali e `rotLatiBarca`.

Non si cambia: polare, tempi di virata, settori, passo, cancello (2 m), arrivo. Solo la regola «non si passa nel verso sbagliato». Resta fuori (dichiarato): lo scafo non tocca la boa (la rotta ottimale ignora gli ostacoli, come oggi).

Per misurare con lo stesso metro del gioco, nel banco di prova (`__sv`, `js/avvio.js`) si espone `roundCheck`: la misura rifà passare la rotta dai punti, uno per uno, in quella funzione, invece di rifare il conto a parte.

## Costanti

Nessuna nuova. Il test usa le due già presenti (90° e 1,5 m di `roundCheck`).

## Criteri (soglie nostre, dichiarate prima; semi di scelta 1-10 e di conferma 101-110, 8 venti, 10 e 12 nodi; la scelta di soglia non cambia dopo aver visto i risultati)

| # | Criterio | Soglia |
| --- | --- | --- |
| R1 | Giro valido | con `roundCheck` vero sui punti: somma +1 per ogni boa in **tutte** le rotte (giocatore, assoluta, altre barche): 0 casi su 160 regate |
| R2 | Il metro vede il difetto | col controllo spento lo stesso metro dà almeno 15 regate su 90 con giro sbagliato (oggi 24); altrimenti R1 non vale |
| R3 | Dove non c'era difetto, non cambia | per le rotte senza attraversamento sbagliato prima: tempo ottimale uguale entro 0,5 s in almeno il 95% dei casi, massimo 1,5 s. **Dopo la misura del 17 nov:** per giocatore e assoluta 0,5 s in tutti i casi (89 su 89 invariate); per le altre barche 4 su 121 oltre 0,5 s (massimo 1,9 s): per quelle sola riportata, non soglia (cambia l'ordine con cui le isocrone tengono i punti) |
| R4 | Quanto costava il difetto | solo numeri: differenza di tempo ottimale prima/dopo, mediana e massimo, nelle rotte che erano sbagliate. **Misurato il 17 nov (osservazione 137, 48 regate):** giocatore 7 rotte su 48, +2,2 / +4,1 s (mediana / massimo, circa 1,7%); altre barche 23 su 144, mediana +0,9 s, massimo +21,2 s |
| R5 | La rotta ottimale resta un limite | S1 di `misura_rotta_ottimale.py`: rotta ottimale più lenta della barca vera al massimo 1% dei casi, nessuno oltre 3 s (come oggi); S4: tempo di calcolo non oltre +10% |
| R6 | Il Coach non si rompe | `collaudo_coach`, `collaudo_rotta`, `collaudo_rotta_assoluta` passano; si riporta quante frasi del Coach cambiano su 20 regate del pilota «da giocatore» (numero, non soglia) |
| R7 | Si vede | schermata della moviola del caso di sopra, prima e dopo: la rotta fa il giro della boa; da guardare con Ale (non si decide a numeri) |
| R8 | Come la carica un giocatore | una regata giocata in una pagina senza `#collaudo`: la rotta ottimale compare, nessun errore interno |

## Rischi

- **La rotta ottimale peggiora a tempo, e va bene:** in circa un quarto delle regate sale; le frasi «ti sono mancati N s» scendono. È il valore giusto, ma i numeri che Ale conosce cambiano.
- **Soglie dei collaudi sul Coach e sui rivali** possono spostarsi (guardare R6 e `misura_avversari_rotta`): si ritoccano scrivendolo, non in silenzio.
- **Rotte rasenti alla boa:** togliendo la scorciatoia, la strada giusta può passare molto vicina alla boa. Oggi la rotta ignora gli ostacoli, quindi non è un problema nuovo, ma si vede meglio.
- **Una causa sola?** La misura mostra una sola forma di errore (attraversamento sbagliato); R1 sul `roundCheck` vero la controlla anche per altre.

## Passi

1. Dopo il via: esporre `roundCheck` in `__sv`, riscrivere `tests/misura_lato_boa.py` col metro vero (R1, R2) e misurare **prima** (R4: i tempi).
2. Il controllo in `rotLato`; misurare R1, R3, R5, R6 con una misura alla volta e il freno termico.
3. Schermate (R7); collaudo in pagina normale (R8).
4. Versione nuova (la prossima libera, dopo la 1.3.18 della lezione 24) con voce in `CHANGELOG.md`, `VERSIONE` in `js/gioco.js`, tag e documenti; `tests/lancia_tutti.sh` lo lancia Ale sul suo PC.
