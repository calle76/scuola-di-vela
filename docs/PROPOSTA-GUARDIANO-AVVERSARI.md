# Proposta: collaudo «guardiano» degli avversari (10 novembre 2026)

Decisione di Ale (10 novembre, `DECISIONI.md`): prima il guardiano, poi il cono d'ombra, poi gli avversari tutti insieme. Il gioco non cambia: è un collaudo nuovo.

## 1. A cosa serve

Fino a oggi, a ogni proposta, i numeri degli avversari (arrivo, tempo perso, boe, contatti) li confrontavo a mano con la versione di prima, con `misura_avversari_rotta.py`. Il guardiano fa lo stesso in automatico, su semi fissi, contro un riferimento salvato in git:
- **dice di quanto cambia ogni numero** rispetto al riferimento;
- **fallisce se uno peggiora oltre la sua soglia**;
- dice anche se la regata è **identica al bit** al riferimento (le regate con lo stesso seme sono ripetibili).

Quando una modifica che peggiora un numero è voluta (per esempio il cono d'ombra, che rallenta tutti), il riferimento si riscrive con `--aggiorna` e lo si dice nel `CHANGELOG.md`.

## 2. Cosa misura

Le 4 regate del torneo, principianti ed esperti, giocatore col pilota, come `misura_avversari_rotta.py` (stessa simulazione, lo stesso codice). Semi **1491-1502** (12, mai usati): 96 regate, 288 avversari. Due pagine in parallelo.

| | Numero | Peggiora se |
| --- | --- | --- |
| G1 | arrivo mediano degli avversari | sale |
| G2 | bolina: secondi persi in media contro la rotta ottimale | sale |
| G3 | poppa: secondi persi, mediana | sale |
| G4 | lati al lasco (triangolo): secondi persi in media | sale |
| G5 | contatti dopo il via | sale |
| G6 | boa toccata; boe sbagliate | salgono |
| G7 | avversari non arrivati; squalificati | salgono |
| G8 | scuffiate | salgono |
| G9 | taglio della linea dopo il via, mediana | sale |

Il guardiano stampa anche, senza soglia, le virate per lato di bolina e gli ultimi 40 m dalla boa 1.

## 3. Come si scelgono le soglie (regola scritta prima di misurare)

Una modifica che non cambia niente di importante cambia comunque le regate, perché basta un decimo di secondo per cambiare il vento che una barca trova dopo. Questo «rumore» va misurato sugli stessi semi, con due modifiche **che sappiamo neutre**: il giro diretto con `R_DIR` 40 e 80 (§10 di `PROPOSTA-AVVERSARI-BOLINA.md`: nessun effetto).

**Soglia di ogni numero** = il più grande fra:
- **due volte** il peggioramento più grande visto nelle due modifiche neutre;
- un **minimo** fissato qui: G1 1 s; G2 0,5 s; G3 0,3 s; G4 0,5 s; G5 il 10% o 3 contatti; G6 boa toccata +3, sbagliate +2; G7 +1 e +1; G8 +2; G9 0,5 s.

## 4. Il metro misura davvero (contro-prova)

Il guardiano deve:
- **passare** con le due modifiche neutre (per costruzione, ma il controllo dice che il conto è giusto);
- **fallire** con due modifiche che sappiamo peggiori:
  - `DOWNE=off`, la poppa della 1.2.23 (poppa persi 11,0 contro 6,5 s, `PROPOSTA-AVVERSARI-ROTTA.md` §6);
  - la patch della layline di dritta con `R_LAY` 100 (`PROPOSTA-AVVERSARI-BOLINA.md` §14: arrivo +3,5 s, boa toccata ×2), applicata su una copia del gioco, mai su `js/`.

**Se non fallisce con una delle due,** 12 semi sono troppo pochi: si passa a 24 semi (1491-1514) una volta sola, rifacendo soglie e contro-prova. Se non basta neanche quello, lo si dice e il guardiano non entra nei collaudi.

## 5. Dove sta

- `tests/collaudo_guardiano_avversari.py`; il riferimento in `tests/guardiano_avversari_rif.json` (in git), con la versione del gioco che l'ha scritto.
- In `lancia_tutti.sh` fra i collaudi lunghi (circa 5-6 minuti), non in `--veloce`.
- Esce con 1 se un numero peggiora oltre la soglia, 2 se la misura non è valida (meno di 96 regate finite, errori della pagina).

## 6. Esito (10 novembre, semi 1491-1502, 96 regate per prova, 1.2.24)

| | 1.2.24 | `R_DIR` 40 | `R_DIR` 80 | **soglia** | poppa 1.2.23 | layline di dritta |
| --- | --- | --- | --- | --- | --- | --- |
| G1 arrivo mediano | 197,9 s | 198,3 | 198,8 | **+1,78** | 200,5 ✗ | 201,3 ✗ |
| G2 bolina persi media | 27,3 s | 28,0 | 27,9 | **+1,3** | 27,3 | 30,0 ✗ |
| G3 poppa persi mediana | 6,4 s | 7,1 | 7,1 | **+1,51** | 10,9 ✗ | 7,1 |
| G4 lasco persi media | 7,9 s | 8,0 | 7,9 | **+0,5** (minimo) | 8,3 | 7,9 |
| G5 contatti | 60 | 56 | 56 | **+6** (10%) | 58 | 57 |
| G6 boa toccata / sbagliate | 18 / 0 | 27 / 0 | 27 / 0 | **+18 / +2** | 18 / 0 | 37 ✗ / 0 |
| G7 non arrivati / squalificati | 0 / 1 | 0 / 0 | 0 / 0 | **+1 / +1** | 0 / 0 | 2 ✗ / 1 |
| G8 scuffiate | 0 | 0 | 0 | **+2** | 0 | 0 |
| G9 taglio mediano | 2,27 s | 2,27 | 2,27 | **+0,5** | 2,27 | 2,27 |

**La contro-prova passa al primo tentativo, con 12 semi:** la poppa della 1.2.23 fallisce su G1 e G3, la layline di dritta su G1, G2, G6 e G7. Le due modifiche neutre passano.

**Cosa non convince:**
- **Il rumore è grande.** Una modifica che non cambia niente sposta l'arrivo mediano di quasi 1 s e la boa toccata da 18 a 27. Il guardiano vede quindi solo i peggioramenti grossi, come le due prove sopra; uno di mezzo secondo gli sfugge. Per quelli resta la misura lunga (`misura_avversari_rotta.py`, 240 regate).
- **Boa toccata:** la soglia (+18) è il doppio del riferimento: su questo numero il guardiano è debole.
- **G9 non si è mosso in nessuna prova** (la partenza non dipende da queste modifiche): controlla che un cambio alle partenze non passi inosservato, ma non è stato provato.
