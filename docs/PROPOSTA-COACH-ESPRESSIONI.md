# Proposta: più espressioni del Coach (voce 69)

*Fermata 1, 20 novembre 2026. Richiesta di Ale: «aumentare le espressioni del Coach». Nessun codice finché non arriva il via e finché Ale non ha deciso quali espressioni e fatto le immagini. Collegata alla voce 58 (un volto per tutti) e a `PROPOSTA-COACH-IN-REGATA.md`.*

## Cosa c'è oggi

- **Tre volti**, file in `img/coach-*.jpg`: *contento*, *serio*, *arrabbiato*. Gli originali di Ale sono `Coach_contento.png`, `Coach_serio.png`, `Coach_arrabbiato.jpeg` in `registrazioni/` (non tracciati).
- Il Coach li usa in due posti: nella moviola a fine regata (3 frasi coi numeri) e durante la regata in Deriva (1.3.28), dove ogni commento ha un umore: `contento`, `serio`, `arrabbiato` (`js/rotta.js`, `crDi`, `crVolto`).
- Nel codice ci sono circa 15 punti in cui il Coach parla in regata (`crDi`); quali umori compaiono più spesso non è misurato: si conta dai file delle regate con le righe «C».

## Il modello più semplice

**Nuove espressioni = nuove immagini + una riga di tabella.** Il codice non cambia struttura: ogni commento sceglie un umore, l'umore sceglie un file `img/coach-<umore>.jpg`. Se un file manca, il volto cade su «serio» (così il gioco non si rompe se Ale aggiunge le immagini a tappe). Nessun marchio, nessun testo nelle immagini.

**Espressioni candidate** (da scegliere con Ale; le immagini le fa lui):

| Espressione | Quando comparirebbe (frasi che esistono già) |
| --- | --- |
| *preoccupato* | coperto da una barca, scarso, oltre la layline (oggi «serio») |
| *sorpreso* | scuffia, strambata andata male, un rivale fermo che riparte davanti |
| *incoraggiante* (pollice o sorriso) | penalità scontata, dopo il richiamo, regata che inizia male e si riprende |
| *fiero* | podio di tappa, sponsor raggiunto, primo posto |
| *pensieroso* | consigli sulla scelta della rotta (lezione 11), prua media |
| *dispiaciuto* | non arrivato, ritirato, squalificato |

Sono sei idee, non un impegno: si può cominciare con due o tre. Le frasi non cambiano.

## Due scelte per Ale

1. **Quali espressioni** (e quante): consiglio due per cominciare, *preoccupato* e *sorpreso*, perché «serio» copre oggi situazioni molto diverse (coperto, scarso, layline, sponsor).
2. **Stile delle immagini:** stesse dimensioni e stesso sfondo dei tre di oggi (48 px a schermo in regata, più grandi nella moviola), per non cambiare il pannello. Se Ale preferisce un altro stile, la proposta si rifà.

## Costanti nuove

Nessuna: la mappa «commento → umore» è una tabella nel codice; il volto di riserva è «serio».

## Criteri (soglie nostre, dichiarate prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| E1 | Ogni umore usato ha il suo file | per ogni umore scritto nella tabella, `img/coach-<umore>.jpg` esiste e si carica (larghezza e altezza non nulle); 0 mancanti |
| E2 | Il volto giusto | su 20 regate lunghe col pilota, ogni commento ha l'umore atteso dalla tabella (ricalcolata dal collaudo, non letta dal gioco); casi controllati almeno 100 |
| E3 | Volto di riserva | con un file tolto apposta, il commento si vede col volto «serio» e 0 errori |
| E4 | Moviola | ogni frase del Coach nella moviola usa lo stesso umore della tabella; 0 differenze su 8 regate registrate |
| E5 | Pannello | 1360x650, 0 px di eccesso con ogni volto; costo dei file: peso totale delle immagini nuove dichiarato (soglia: non oltre 200 KB in più) |
| E6 | Come un giocatore | pagina senza `#collaudo`: ogni nuovo volto compare almeno una volta in un torneo giocato, 0 errori |

## Rischi

- **Troppe espressioni** diventano rumore o si confondono col testo; per questo si parte da due o tre.
- **Le immagini non si possono verificare qui**: la plausibilità e lo stile li giudica Ale a occhio; io controllo solo che esistano, si carichino e compaiano al momento giusto.
- **Peso della pagina**: ogni jpg pesa circa quanto i tre attuali; da misurare.

## Passi, dopo il via

1. Ale sceglie le espressioni e prepara le immagini (`img/` o la radice; le converto io come per i tre di oggi).
2. Tabella umore → file, volto di riserva, criteri E1-E6.
3. Documenti, versione, `CHANGELOG.md`.
