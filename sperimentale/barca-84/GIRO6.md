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

---

# Esito (26 novembre 2026, scritto dopo le misure)

## Griglia (`scansione6.txt`, 60 combinazioni)

La taratura ha un limite suo: **Day chiede più velocità, F121 (Pennanen) col poco vento meno** (+4 / +7% a 3,3 nodi di vento); l'errore non scende sotto 3,07 punti. Il minimo (`off` 5, `par` 0,105, scafo 0,93) e altri cinque stanno entro 0,2 punti. **La regola «più vicino a L» non diceva come misurare la distanza:** sciolta, dichiarandolo dopo aver visto la tabella, con la somma degli spostamenti divisi per l'ampiezza dell'intervallo. Vince **M: `off` 7, `par` 0,105 (invariato), scafo 0,93 (la vasca SSPA)**. Due cambiamenti rispetto a K, uno solo rispetto a L più lo spostamento.

## Controlli (`giro6_controlli.txt`, metro sulla rotta)

| | M | M5 (il minimo, `off` 5) | misura / soglia |
|---|---|---|---|
| B1 Day 6 nodi | −4,0% | −4,5% | ≥ −5 |
| Day 10 / 15 | −3,2 / −2,8% | −3,2 / −2,8% | |
| B2 Binns 9, 42-60° | −3,5 / −2,9 / −4,0 / **−5,1** | −3,8 / −3,1 / −4,4 / −4,9 | ±5 |
| B3 Binns 12 | −2,9 … +0,8 | −2,8 … +0,8 | ±3 |
| B5 3,2 nodi a 45° | +1,0% | +0,4% | ≥ −8 |
| B6, B7b, virata 16, raffica, angolo morto | passano | passano | |
| VMG 20 nodi | 3,73 | 3,72 | (K 3,43) |
| Semb 14 nodi: uscita / media / 80% | 92% / 89% / 7,6 s | 92% / 89% / 7,6 s | 92% / 86% / 7,6 s |
| Semb 18 nodi | 71% / 79% / 9,6 s | 73% / 80% / 9,4 s | |
| Regate (medie, limite basso) VMG bolina 6 / 10 / 15 | 2,54 / 3,50 / 3,70 | 2,53 / 3,50 / 3,69 | 2,5 / 3,2 / 3,7 |
| lasco 110° | 4,11 / 5,95 / 9,28 | uguale | 4,2 / 5,8 / 9,1 |
| VMG poppa | 2,92 / 4,51 / 6,28 | uguale | 3,3 / 4,7 / 7,8 (con le S, tecnica che il gioco non ha) |

M non passa B2 per 0,1 punti a 60° (meno della precisione con cui i dati di Binns sono letti dal grafico di Day); M5 passa B1-B7b. Il controllo non è peggiorato mentre la taratura migliorava: anzi B2 e B3 migliorano (scafo più leggero). Restano −3 / −4% su Day: è il limite fra Day e F121.

## Sul gioco (copia del repo, motore M con la raddrizzata del 470; `fa_motore84.py` ora scrive M, controllato uguale al banco)

- **Lezioni** (30 semi, 41 passi): 6.3 «La scuffia» guidando **non completata 9 volte su 28** (la barca regge di più e la lezione non riesce a farla scuffiare), a mani ferme si completa da sola 2 su 30 (K 9, oggi 1); 5.8 strambata 3 su 30 non completata guidando, 6.2 raffica 1, 2.6 1. La 6.3 va rifatta in ogni caso.
- **Fasce:** tempi del pilota preciso 76,8 / 117,7 / 133,5 / 242,7 / circa 278,5 s (K 78,8 / 119,3 / 136,3 / 248,0 / 284,9; oggi 79 / 124 / 159 / 286 / 302).
- **Medaglie** (30 corse, fasce di oggi): tutte OK.
- **Regola 18:** Z1 fallisce per forza (barca diversa); **Z4 ora passa (5 contatti decisi dalla 18; K 0)**; Z3, Z5 ok.
- **Torneo completo:** tutto ok tranne C11 R7 (uscita dal menu lenta, già nota sul PC), come K.

## Conclusione

M è la barca più vicina al vero trovata: passa tutti i criteri di velocità col metro giusto tranne B2 per 0,1 punti, le virate misurate, le regate (dove il confronto ha senso), e sul gioco si comporta come K o meglio. Le sue costanti nuove sono **tarate e dichiarate** (spostamento 7°, scafo della vasca SSPA), più la raddrizzata del 470. Restano: le ipotesi della vela che fileggia e del ritardo dell'appiattimento, la velocità bassa (`reg`), la poppa più lenta delle regate (tecnica), le strambate troppo facili (motore di oggi).
