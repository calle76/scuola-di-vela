# Proposta: niente raffiche ammucchiate sulla barca al via delle regate lunghe

*Fermata 1, 22 novembre 2026 (Opus). Segnalazione di Lucio (21 nov): «non ho fatto in tempo a prendere i comandi dopo Parti che, in una raffica forte, ho scuffiato in pochi secondi». Nessun codice finché non arriva il via.*

## Cosa succede (misurato)

- **Registrazioni del 20-21 nov (1.3.31 e 1.3.37, 8 regate lunghe del torneo, Lucio e Ale):** in 6 su 8 c'è una scuffia prima del via, due a 1,5 s da «Parti». In tutte e 8 la prima riga ha 20-24 nodi di vento vero; la media della regata è 13-14 nodi (impostati 12). La barca parte al traverso, a 3 nodi, scotta al 35%.
- **Nel gioco (1.3.38), 40 tornei lunghi, semi 1001-1040:** al via il vento sulla barca è 1,59-1,93 volte la media del campo (mediana 1,77), in **40 su 40**. Lasciando i comandi fermi, 2 barche su 40 scuffiano entro 2 s (a 1,2 e 1,7 s).
- **Nelle regate corte non succede** (vento al via uguale alla media, 8 su 8): per questo i collaudi senza `--lungo` non l'hanno mai visto.

## Causa

`setGusts` (js/gioco.js) all'inizio mette 4 raffiche già formate a 22, 45, 70 e 95 m sopravento alla barca del giocatore. Erano pensate per le raffiche piccole (raggio 9-20 m). Dalla 1.3.26, nelle regate lunghe le raffiche sono zone di 80-160 m di raggio che durano 120-240 s: le quattro coprono tutte la barca e si **sommano** (`ventoDa`: k += …), e restano per quasi tutto il conto alla rovescia. Le raffiche che nascono dopo, invece, sono sparse sul campo (150-300 m sopravento, ±135 m di lato).

## Il modello più semplice

Solo nelle regate lunghe (`gustZona`): le 4 raffiche iniziali si mettono come quelle che nascono dopo (distanza e lato a caso, con le stesse costanti `RAFF_DIST` e `RAFF_LAT`), già formate. Nessuna costante nuova. Le regate corte, le prove e la navigazione libera non cambiano (stesse estrazioni a caso nello stesso ordine).

Cosa **non** propongo: cambiare la scotta o la posizione di partenza. Nota per Lucio: per prendere meno vento la scotta si **lasca**, non si cazza (con la vela lascata la barca perde potenza e sbanda meno; è quello che dice la lezione sulle raffiche). Se dopo la correzione il primo secondo resta difficile, si può proporre a parte una partenza con la scotta più lascata.

## Criteri (soglie nostre, dichiarate prima)

Soglie scelte guardando i semi 1001-1040 e confermate sui semi 1041-1080, mai guardati (regola dei semi).

| # | Criterio | Soglia |
| --- | --- | --- |
| V1 | Vento al via come in un momento qualunque | rapporto vento sulla barca / media del campo a −180 s: mediana ≤ 1,15 e al più 25% dei casi sopra 1,3 (40 semi + 40 di conferma) |
| V2 | Niente scuffia senza colpa | comandi fermi per i primi 20 s: 0 scuffie su 80 |
| V3 | Le regate corte non cambiano | 20 regate corte a semi fissi identiche al bit alla 1.3.38 (Chromium) |
| V4 | Le raffiche in regata restano quelle | `collaudo_percorso_lungo` P2/P4 sotto la soglia di sempre (40% di bolina in raffica), Chromium e Firefox |
| V5 | Come un giocatore | pagina senza `#collaudo`, torneo lungo: vento al via sotto 1,3 volte la media, 0 errori |

Il metro (vento medio del campo su una griglia di 21x18 punti) non dipende dalla correzione.

## Rischi

- Le regate lunghe a semi fissi cambiano (cambiano le estrazioni a caso del via): i collaudi `--lungo` vanno rilanciati sul giro di GitHub.
- Una raffica lontana può comunque arrivare sulla barca durante il conto alla rovescia: è giusto che succeda, ma non al secondo zero.

## Esito

*(da scrivere dopo il via)*
