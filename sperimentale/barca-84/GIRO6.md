# Voce 84, sesto giro (26 novembre 2026): tarare la barca sul vero — regole scritte PRIMA di misurare

Via di Ale: «Cerca di adattare la barca alla realtà. Anche senza fonti che risulti vera. Sai come deve comportarsi. Risolvi quelle piccole differenze.» Quindi una **taratura dichiarata** è ammessa: la costante non ha una fonte sua, ma il comportamento deve risultare vero. `js/` non si tocca (ricerca sul banco; il motore cambia solo con un altro via).

## Il rischio, e come si tiene sotto controllo

Tarando sugli stessi dati con cui si giudica, la barca «passa» per costruzione. Quindi:
- **Taratura solo su:** Day (VMG di bolina 6, 10, 15 nodi) e F121 (velocità a 45° con 4 venti). Come nella regola del giro J. Metro sulla rotta (GIRO5 §1).
- **Controllo, mai usato per scegliere:** Binns 9 e 12 nodi (B2, B3), F109 (3,2 nodi a 45°, B5, e virate secondo per secondo), le 12 virate di Semb (F137) con 14 nodi, i GPS di regata (Pan e Sun: la velocità media di bolina in regata è un limite basso), poppa contro Day (B7b), virata a 16 nodi, raffica, angolo morto.
- Se il controllo peggiora mentre la taratura migliora, si dice e ci si ferma.

## Le manopole (solo quelle con un senso fisico) e i loro intervalli

| Manopola | K/L | Intervallo | Senso fisico |
|---|---|---|---|
| Spostamento fra tabella ORC e incidenza del boma (`off`) | 9° | 5-13° | quanto la vela svergolata «vede» più angolo del boma: F109 misura la vela a metà altezza 4-10° oltre il boma |
| Resistenza dell'aria di scafo, albero e velista (`par`) | 0,105 | 0,06-0,105 | Day fig. 12 dà 0,105; il velista sporto fuori e l'albero piegato possono pesare meno; più alta di Day non ha senso |
| Scafo (`hullScale`) | 0,965 (L) | 0,93-1 | le due vasche |

Area 7,92 (la tela intera, il massimo), braccio 2,8, timoniere 0,90 e il resto come K. Griglia: `off` 5 / 7 / 9 / 11 / 13, `par` 0,06 / 0,075 / 0,09 / 0,105, scafo 0,93 / 0,965 / 1 (60 combinazioni).

## La regola di scelta

Errore quadratico medio sulla taratura (Day 3 + F121 4, in %), il più piccolo. A parità entro 0,2 punti si sceglie quello più vicino a L (meno cambiamenti). Il candidato si chiama **M**. Poi tutti i controlli, riportati così come escono.

## Cosa resta di Ale

Se M passa i controlli: proposta per il motore con M, ogni costante tarata scritta come taratura (non come fonte). B8 diventa «costanti con fonte o tarate e controllate su dati non usati». Ogni cambiamento di B8 è di Ale: qui lo si propone soltanto.
