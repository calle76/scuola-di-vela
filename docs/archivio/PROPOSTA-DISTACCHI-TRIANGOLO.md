# Proposta: il controllo T2b dei distacchi del triangolo

*Fermata 1, 17 novembre 2026. Voce 53 di `DA-FARE.md`. Nessun codice nel gioco finché non arriva il via di Ale.*

## Da dove viene

`collaudo_triangolo.py` T2b fallisce dalla 1.0.55 (soglia 100%, oggi circa 126 casi su 166). `PROPOSTA-TORNEI-1B.md` §8.8 diceva: causa nota («la strada resta ferma» tra la boa e la fine del giro) e «decide Ale se tenere così o aggiungere un termine d'arco». La decisione non è mai stata presa. Il 17 novembre ho rimisurato.

## Cosa fa il gioco e cosa chiede il collaudo

- **Il gioco** (`distacco`, `js/regate.js`): il distacco è «da quanti secondi la barca davanti aveva la strada che ho fatto io» (metri fatti in direzione del percorso). Vale in ogni istante.
- **Il collaudo T2b**: legge il distacco **10 s dopo** che l'ultima delle due barche ha girato la boa e lo confronta con la differenza dei **tempi di giro**.

Sono due cose diverse: dopo il giro le due barche vanno a velocità diverse e il distacco **deve** cambiare. Il collaudo scambia questo cambiamento per un errore.

## Misura del 17 novembre (`collaudo_triangolo.py 1 20 N`, semi 1-20, Chromium, una misura per volta col freno)

| Lettura a | Entro 3 s | Segno giusto | Errore massimo |
| --- | --- | --- | --- |
| 3 s | 161 su 172 (93,6%) | 168 su 172 (97,7%) | 12,9 s |
| 10 s (oggi) | 126 su 166 (75,9%) | 160 su 166 | 18,8 s |
| 20 s | 95 su 161 (59,0%) | 153 su 161 | 19,9 s |

L'errore **cresce con l'attesa**: non è solo la «strada ferma» di circa 9 s alla boa 2, è il metro che mescola due cose. A 3 s dopo il via 52 su 57, boa 1 60 su 60, boa 2 49 su 55.

## Modello più semplice

1. **Il gioco non cambia.** Il distacco resta com'è.
2. **Si cambia il metro di T2b**: lettura a 3 s dal giro (il momento più vicino al confronto), e due soglie come quelle già usate in `collaudo_distacchi.py` (D1, 90%): **almeno il 90% dei confronti entro 3 s e almeno il 95% col segno giusto**. Non sono tarate su questi numeri: il 90% c'è già in D1. Oggi il metro nuovo darebbe 93,6% e 97,7%: passerebbe.
3. Il controllo del segno resta, perché è quello che il giocatore vede: «avanti» o «dietro».

## Se invece si vuole correggere il gioco (non lo propongo)

Aggiungere alla strada un termine d'arco intorno alle boe (più codice, nel pezzo che disegna anche la classifica): si rimisura tutto (D1, T2b, `collaudo_distacchi`). Lo si riapre solo se Ale vede nel gioco distacchi sbagliati. Su 172 letture, 4 hanno il segno sbagliato (2,3%).

## Criteri

| # | Criterio | Soglia |
| --- | --- | --- |
| D1b | Entro 3 s a 3 s dal giro | almeno 90% dei confronti (oggi 93,6%) |
| D2b | Segno giusto a 3 s dal giro | almeno 95% (oggi 97,7%) |
| D3b | Il collaudo misura davvero | numero di confronti stampato, almeno 100 (oggi 172) |
| D4b | Il gioco non cambia | solo `tests/`, nessun file in `js/` |
| D5b | GitHub | le voci a frammento della voce 45 si tolgono quando T2b passa in tutti e due i browser (Firefox da misurare) |

## Rischi

- Il 3 s è scelto per il confronto con la differenza dei tempi: con 2 s o 5 s i numeri cambiano un poco. Resta una scelta nostra, dichiarata qui.
- Firefox non è misurato: potrebbe non passare lo stesso.
- Il collaudo smette di segnalare il difetto della «strada ferma». Se serve, lo si misura a parte (errore massimo e quando).

## Passi

1. Dopo il via: cambiare `RIT` e le soglie in `collaudo_triangolo.py` (un controllo, nessun `js/`), misurare Chromium e Firefox una volta per volta.
2. Togliere le voci a frammento e le righe esatte di T2b da `tests/fallimenti_noti.txt`, `docs/COLLAUDI.md`.
3. Nessuna versione del gioco: solo collaudi.
