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

## 7. Prima prova vera: il cono d'ombra (1.2.25)

Contro il riferimento della 1.2.24 il guardiano ha suonato: arrivo mediano +4,75 s (soglia 1,78), lasco +0,75 s (soglia 0,5). Il confronto regata per regata sugli stessi 96 regate dà però +1,7 s ±1,3, e due gruppi da 240 regate danno −2,5 e −2,8 s (`PROPOSTA-CONO-D-OMBRA.md` §10). **Cosa insegna:** con una modifica che rimescola le regate la mediana su 96 regate salta di alcuni secondi; il guardiano resta un campanello, e quando suona si fa il confronto regata per regata su un gruppo grande prima di concludere. Riferimento riscritto sulla 1.2.25.

## 8. Rifare il guardiano (voce 33 di `DA-FARE.md`): proposta, fermata 1

14 novembre 2026, mattina. Ale: «ok, scrivi la proposta del guardiano». In `tests/` non è stato scritto niente.

### Il difetto

Le soglie del §3 sono state misurate con due modifiche neutre (`R_DIR` 40 e 80) che **non spostano i sorteggi**: le regate restano quasi le stesse. Basta però un numero casuale in più (i nomi della 1.2.33 sorteggiano i tre rivali) perché raffiche e partenze cambino da capo: sono altre 96 regate, e i numeri ballano più delle soglie. Due prove:
- il cono d'ombra (1.2.25, §7): arrivo mediano +4,75 s sul guardiano, mentre il confronto regata per regata dava +1,7 s ±1,3;
- la 1.2.32 con un solo `Math.random()` in più, cioè lo stesso gioco (`PROPOSTA-RIVALI-E-SPONSOR.md` §15): boe sbagliate 0 → 6, soglia +2.

### Modello più semplice

**1. Misurare il rumore dei sorteggi, non quello della guida.**
- Una manopola nuova del collaudo, `SPOSTA=k`: dopo aver seminato il caso all'inizio della regata, il collaudo tira e butta via k numeri casuali. Il gioco è lo stesso, le regate no. Si tocca solo `tests/misura_avversari_rotta.py`; `js/` non si tocca.
- Sulla versione di oggi (1.2.33) si corre il guardiano **8 volte**, con `SPOSTA` da 0 a 7.
- Le corse usano **24 semi** (1491-1514, 192 regate per corsa). Ogni regata si salva da sola, così dalle stesse corse si calcolano anche i numeri sui primi 12 semi, senza correre di nuovo.

**2. Il riferimento diventa la mediana delle 8 corse**, non una corsa sola: così il riferimento non porta il suo caso dentro il confronto.

**3. Soglia di ogni numero** (G1-G9, gli stessi di oggi) = il più grande fra:
- l'**intervallo** delle 8 corse (massimo − minimo);
- il **minimo del §3**, che resta com'è.

Stima, scritta prima di misurare: con questa regola una versione che non cambia niente fa suonare il guardiano circa **1 volta su 25**. Se capita, vale la regola del §7: confronto su un gruppo grande prima di concludere.

**4. Quanti semi.** Si decide con la contro-prova (punto 5), con questa regola fissata adesso:
- si prendono **12 semi** se con 12 la contro-prova va come deve;
- altrimenti **24**;
- se neanche 24 bastano, lo si dice e il guardiano diventa **solo informativo**, cioè stampa i numeri ma non boccia.

**5. Contro-prova.**
- **Deve passare** con 4 spostamenti mai guardati (`SPOSTA` da 8 a 11): 4 su 4. Così le soglie non sono scelte sulle stesse corse su cui si giudicano (regola dei semi).
- **Deve fallire** con due modifiche che sappiamo peggiori:
  - `DOWNE=off`, la poppa della 1.2.23;
  - la patch della layline di dritta con `R_LAY` 100, su una copia del gioco. Se sulla 1.2.33 la patch non si applica più, lo dico e resta solo `DOWNE=off`, che allora deve fallire anche lui con l'intervallo delle 8 corse.

**6. Informativo, solo se il caldo lo permette:** la 1.2.32 con 4 spostamenti, confrontando la sua mediana con quella della 1.2.33. Dice se i nomi hanno cambiato davvero qualcosa nei rivali. Non decide niente, perché la 1.2.33 è già chiusa (strada A).

### Criteri, con soglie fissate prima di provare

| # | Criterio | Soglia |
| --- | --- | --- |
| Q1 | Il guardiano nuovo, sulla 1.2.33, con gli spostamenti 8-11 | passa 4 volte su 4 |
| Q2 | `DOWNE=off` | fallisce |
| Q3 | Layline di dritta, `R_LAY` 100 (se la patch si applica) | fallisce |
| Q4 | Misura valida | tutte le regate finite (192 o 96 per corsa), 0 errori della pagina; ogni corsa con un'impronta diversa dalle altre, cioè gli spostamenti hanno cambiato davvero le regate |
| Q5 | Non-regressione | `polare.js` e `raffiche_e_virate.js` identici; `js/` non toccato |

### Costanti nuove (nostre, senza fonte)

8 corse per misurare il rumore e 4 per la conferma; l'intervallo come soglia; 12 o 24 semi.

### Rischi

- **Soglie larghe:** il guardiano vedrà solo i peggioramenti grossi. Già oggi è così (§6), solo che oggi non lo sa. Per i peggioramenti piccoli restano la misura lunga e il confronto regata per regata.
- **Tempo:** con 24 semi una corsa dura circa 11 minuti. In tutto sono circa 16 corse, quindi **3 ore** col freno del caldo, una corsa alla volta. Se il guardiano finisce a 24 semi, nei collaudi lunghi di `lancia_tutti.sh` costerà circa 11 minuti invece di 5-6.
- **Boe sbagliate, squalificati, scuffiate** sono numeri piccoli, spesso 0 in tutte le corse: lì l'intervallo vale 0 e decide il minimo del §3. Le 6 boe sbagliate della prova della 1.2.32 dicono che anche quel minimo (+2) potrebbe essere stretto. Se lo è, si vedrà in Q1 e lo riporterò com'è, senza alzarlo dopo.

### Cosa serve da Ale

Il via. Si toccano solo `tests/misura_avversari_rotta.py` (la manopola `SPOSTA`), `tests/collaudo_guardiano_avversari.py` (soglie, riferimento a mediana, regate salvate), il riferimento `tests/guardiano_avversari_rif.json` e `docs/COLLAUDI.md`. Non è una versione del gioco.
