# Proposta: registrazioni delle regate più ricche (voce 55)

*23 novembre 2026, notte (Opus), in autonomia (Ale: «vai in autonomia, non chiedere permessi»). Fermata 1 e fermata 2 nella stessa sessione; le soglie sono scritte qui prima di misurare.*

## Da dove viene

Osservazioni 135 e 136: per capire una situazione raccontata da Lucio («ero in mezzo a due barche, il semaforo rosso») il file della regata non bastava. Mancavano:
1. **il colore del semaforo** del giocatore (rosso, giallo, verde) e con quale barca;
2. **chi aveva la colpa di un contatto**, nella riga del contatto (oggi solo nella riga Q della penalità, a parole);
3. **quello che succede dopo il proprio arrivo**: la registrazione si chiudeva al traguardo del giocatore, e i rivali che arrivavano dopo non c'erano.

## Il modello più semplice

- `E t semaforo rosso|giallo|verde|spento Nome`: una riga a ogni cambio di colore (calcolato dal gioco anche quando il semaforo non è acceso sullo schermo); nelle impostazioni dell'intestazione `semaforo=sì|no` dice se il giocatore lo vedeva.
- `E t contatto_barche A B colpa C regola N`: la stessa riga di prima con chi ha preso la penalità e la regola.
- **Dopo il proprio arrivo** la registrazione continua finché arrivano tutti, o per al più **60 s** (`REG_DOPO`, ipotesi nostra); si chiude prima se il giocatore esce dalla regata, apre la rotta ottimale o scarica il file (la chiusura resta «arrivo»).
- Il registratore resta in sola lettura: il gioco si annota solo due cose in più dentro la regata (con quale barca è calcolato il semaforo e la colpa di ogni contatto), che la simulazione non legge.

## Criteri (soglie nostre, scritte prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| G1 | La regata non cambia | torneo e regata col pilota identici al bit con e senza registrazione (come già `collaudo_registratore`) |
| G2 | Semaforo | ogni cambio di `R.sem` misurato dal collaudo compare nel file, nello stesso ordine; almeno 20 cambi visti |
| G3 | Colpa | ogni `contatto_barche` ha la colpa, e coincide con la riga Q della penalità; almeno 3 contatti visti |
| G4 | Dopo l'arrivo | le righe continuano dopo il proprio arrivo; ogni rivale arrivato entro 60 s ha la sua riga `avv_arrivo`; la chiusura resta «arrivo» |
| G5 | Peso | regata lunga del torneo: ogni pezzo al più 1 MB, il file intero al più 2,5 MB (oggi circa 2 MB, voce 66b: «lasciali così») |

## Rischi

- Chi apre la rotta ottimale prima che la registrazione si chiuda: la si chiude in quel momento, così le righe del Coach finiscono nel file come prima.
- Il collaudo del registratore che controlla la chiusura proprio all'arrivo va riletto (G4 cambia la regola).

## Esito (23 nov 2026, versione 1.3.46)

G1-G5 passano (numeri in `CHANGELOG.md` 1.3.46). Una scelta cambiata durante la prova, detta: il semaforo si scrive anche quando, con lo stesso colore, cambia la barca con cui è calcolato (il collaudo li vedeva e il file no). **G3 misurato solo in parte:** il collaudo controlla che ogni contatto abbia la colpa, non che coincida con la riga Q (stessa fonte nel gioco, `chiCede1516`; da aggiungere se serve). Collaudi vecchi adattati alla chiusura dopo l'arrivo: `collaudo_coach` K12, `collaudo_registrazione` A, F3, F5.

## Seconda aggiunta: vento dei rivali e attese della 4B (via di Ale, 25 nov: «ok aggiungi»; scritta prima del codice)

**Perché:** Ale e Lucio stanno per giocare regate lunghe con gli esperti (voce 2) e alla boa (Z7). Il file non dice la forza del vento dei rivali (raffiche prese o perse) né quando la 4B (1.3.56) li fa aspettare.

- `V t nome tws coperta%`: per ogni rivale, una volta al secondo, il vento vero nel suo punto (nodi, raffiche e salti compresi, cono d'ombra escluso) e la percentuale di vento tolto dal cono. Righe nuove e non un campo in fondo alle righe B (come detto ad Ale): così chi legge i file vecchi non cambia.
- `D t nome virata N` (N = rinvii di questo bordo, al più 4) e `D t nome partenza N` (N = rinvii fino a lì), a ogni rinvio: un tipo di riga nuovo e non un evento E, così i lettori vecchi che contano gli eventi non cambiano (deciso prima del codice). Il gioco si annota quante volte ha rimandato la partenza (`rinvioVia`), che la simulazione non legge.

| # | Criterio | Soglia |
| --- | --- | --- |
| H1 | La regata non cambia | arrivi e posizioni finali identici alla 1.3.56, 6 regate lunghe su 6 |
| H2 | Rinvii | quelli visti dal collaudo (contatori del gioco, passo per passo) uguali nel file, per tipo e barca, 6 regate su 6; almeno 10 virate e 10 partenze in tutto |
| H3 | Vento | ogni riga V uguale al vento ricalcolato nel collaudo nel punto della barca (0,1 nodi); almeno 1000 righe; al più 1,5 s fra due righe dello stesso rivale |
| H4 | Peso | come G5: pezzo al più 1 MB, intero al più 2,5 MB |
| H5 | Lettori vecchi | `scene_strane`, `conta_boa_zona`, `analizza_sessione` danno la stessa uscita su un file nuovo con e senza le righe V e D |
