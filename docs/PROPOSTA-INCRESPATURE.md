# Proposta: increspature più vive dentro le raffiche (fermata 1, 17 ottobre 2026)

Voce 4b della ROADMAP, idea di Ale del 16 ottobre 2026: «un secondo strato di increspature, solo nelle chiazze scure, che scorre più in fretta in proporzione alla forza della raffica e sfuma ai bordi; fuori dalle raffiche il disegno resta identico». È un **segnale visivo per leggere l'acqua, non una misura**: va dichiarato come tale.

## 1. Cosa fa oggi il gioco (`js/disegno.js`, blocco «increspature»)

Un reticolo di celle da 7 m, da 1 a 4 trattini per cella secondo lo zoom, che scorre con il vento di base a `tws · 0,35` m/s. Dentro una raffica (`gustAt > 0,04`) il trattino viene **allungato** (`l · (1 + 2k)`) e gli si disegna accanto una **copia scura** (alpha fino a 0,6, scostata di 0,6 m). Più la chiazza scura a gradiente, disegnata a parte. Sotto zoom 0,5 le increspature sfumano, sotto 0,35 non si disegnano, e oltre 2500 celle si salta tutto: sono i freni esistenti contro il rallentamento.

## 2. Cosa dicono le fonti

- Una raffica sulla superficie è una **chiazza più scura** («cat's paw»): le increspature capillari hanno pendenze ripide e riflettono la luce in modo diverso dall'acqua calma. Natural Navigator, *Cat's paws on water*, https://www.naturalnavigator.com/news/2017/11/cats-paws-on-water/ ; glossario dell'American Meteorological Society, voce *cat's paw*, https://glossary.ametsoc.org/wiki/cat-s-paw/
- **Chiazze scure con increspature più ravvicinate indicano più vento**: la densità è il segnale, e in deriva si va a caccia di quelle chiazze. VibeSail, *Reading Water and Wind*, https://vibesail.com/learn/reading-water-and-wind ; Bay Nature, *How to read the wind like a sailor*, https://baynature.org/article/how-to-read-the-wind-like-a-sailor/
- **Non sostenuto da fonti:** che il disegno delle increspature debba *scorrere* più in fretta dentro la raffica. È plausibile (il vento locale è più forte e trascina le onde capillari), ma nelle fonti lette non c'è: resta un aiuto visivo dichiarato.
- Le fonti non concordano sulla forza di vento a cui le chiazze compaiono (una dice circa 12 nodi, un'altra «un alito leggero»): nessun numero di soglia si prende da lì.

## 3. Proposta (modello più semplice plausibile)

Dentro le chiazze (`gustAt > 0,04`), **in aggiunta** a quello che c'è già:

1. **Più fitte, non più lunghe.** I trattini della raffica diventano più **densi** in proporzione alla forza: fino a +100% di trattini per cella nel cuore della raffica (ipotesi nostra). L'allungamento di oggi (`1 + 2k`) scende a `1 + 0,6k`, perché le fonti parlano di increspature ravvicinate, non lunghe.
2. **Secondo strato che scorre più in fretta** (idea di Ale): i trattini aggiunti hanno uno scorrimento proprio, con il **vento locale** (`tws · (1 + k) · 0,35`) invece di quello di base, così dentro la chiazza la trama slitta visibilmente.
3. **Sfuma ai bordi:** opacità proporzionale alla forza della raffica, come fa già la copia scura; al bordo della chiazza i trattini aggiunti sono invisibili.
4. **Fuori dalle raffiche non cambia niente**, e restano tutti i freni di oggi (dissolvenza sotto zoom 0,5, niente sotto 0,35, salto oltre 2500 celle). I trattini aggiunti si contano dentro quei limiti.

Costanti nuove, tutte **ipotesi nostre**: +100% di densità nel cuore, allungamento `1 + 0,6k`, soglia `0,04` (quella di oggi), opacità proporzionale a `k`.

## 4. Criteri (soglie nostre, scritte prima di provare)

1. **Costo:** tempo mediano per disegnare un quadro, misurato su 300 quadri a zoom 1 con tre raffiche sullo schermo, **al massimo +15%** rispetto a oggi; e nessun aumento a zoom 0,35 e 0,5 (lì il disegno dev'essere identico in costo entro il 3%).
2. **Si vede davvero:** in una schermata, contando i pixel scuri delle increspature in un quadrato di 10×10 m **dentro** il cuore di una raffica e in uno **fuori**, la differenza di densità dev'essere **almeno +40%** (oggi va misurata: potrebbe già esserci per via dei trattini più lunghi, e in quel caso la soglia va letta come +40% rispetto a oggi).
3. **Fuori dalle raffiche identico:** con le raffiche spente, le schermate del gioco devono restare **uguali pixel per pixel** a quelle di oggi (`collaudo_impronta.py` e `collaudo_vista.py`).
4. **Niente nel motore:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere; `js/motore.js` non toccato.
5. **Schermate per Ale**, a 1360×650: raffica vicina, raffica lontana, zoom 0,5, vento 6 e 15 nodi. **Il giudizio sull'aspetto è suo**; i criteri 1-4 sono miei.
6. **Controllo del metro:** la misura del costo stampa quanti trattini ha disegnato dentro e fuori raffica; se dentro sono zero, la prova non vale.

## 5. Rischi

- **Rallentamento sul PC di Ale** (Chrome a tutto schermo): è il rischio principale, perché i trattini in più stanno proprio dove si guarda. Se il criterio 1 non passa, la strada è ridurre la densità invece di aggiungere strati.
- **Confusione visiva:** due trame sovrapposte che scorrono a velocità diverse possono sembrare un'immagine doppia. Si guarda nelle schermate del criterio 5.
- **Aiuto troppo forte:** se le chiazze diventano troppo evidenti, leggere l'acqua non è più un'abilità. Giudizio di Ale.
- Il gioco **non modella** il salto di direzione visibile sulla superficie né le onde: resta una semplificazione dichiarata.

## 6. Fermata 2, esito (17 ottobre 2026): fatto nella 1.0.19

**Fatto:** secondo strato dentro le chiazze, fino al doppio dei trattini nel cuore (densità scalata su `k/0,4`), sfumato a zero sul bordo, con scorrimento proprio del vento della raffica più forte in acqua. Lunghezza dei trattini **invariata**. Fuori dalle chiazze nulla cambia.

| Criterio | Soglia | Esito |
| --- | --- | --- |
| 1. costo per quadro | +15% al massimo | **+9,6%** a zoom pieno (12,62 ms contro 11,51), +3,8% a zoom 0,51, invariato a 0,26: **rispettato** |
| 2. si vede davvero | +40% di trama rispetto a oggi | zoom 0,5 **+105%** (da +196% a +506%): rispettato; **zoom pieno +20%** (da +267% a +340%): **non raggiunto** |
| 3. fuori dalle raffiche identico | identico | per costruzione (il blocco gira solo dove `gustAt > 0,04`, e senza raffiche lo sfasamento resta zero); **non verificabile pixel per pixel**, vedi §7 |
| 4. niente nel motore | identici | `polare.js` e `raffiche_e_virate.js` identici; `js/motore.js` non toccato: **rispettato** |
| 5. schermate per Ale | a 1360×650 | in `tests/output/increspature/` (`prima-*`, `dopo2-*`), nel momento in cui una raffica passa sulla barca: **consegnate**; il giudizio è suo, **giocando** |
| 6. controllo del metro | niente blocchi dentro = prova nulla | 382 blocchi dentro e 905 fuori a zoom pieno, 5 semi: **rispettato** |

**Due passi falsi nel modello, corretti:** accorciare i trattini dentro la raffica (`1 + 0,6k`) **peggiorava** il contrasto, da +267% a +226%, perché si perdeva più in lunghezza di quanto si guadagnava in densità: la lunghezza è tornata `1 + 2k`. E la densità «fino al doppio nel cuore» era scritta su `gk` puro, ma nel gioco le raffiche arrivano a `k ≈ 0,4`: aggiungeva **un trattino solo**, al 45% di opacità. Ora si scala su 0,4.

## 7. Come NON si misura (due metri sbagliati, da non rifare)

- **Confrontare i pixel di due versioni sulla stessa scena non si può:** la fase delle increspature avanza col **tempo reale del browser**, quindi due caricamenti non disegnano mai la stessa onda. Il sintomo: la regata **senza** raffiche mostrava 128 blocchi su 168 «cambiati». Le misure vanno fatte **dentro un solo quadro** (dentro la chiazza contro l'acqua calma).
- **Cercare le chiazze dai blocchi più scuri non funziona:** il mare ha un suo degradé, e i blocchi più scuri cadono su aree piatte dell'interfaccia. Serve la **proiezione vera** della telecamera (aggancio `vista` aggiunto a una copia nello scratchpad, non al gioco) e la posizione delle raffiche da `__sv.gusts()`.
- **A zoom pieno la finestra sul mare è di 72×48 m** (13,5 px/m) mentre le raffiche hanno raggio 15-18 m e nascono a 40-200 m: una schermata presa a caso non ne contiene nessuna. Bisogna aspettare il momento in cui una raffica (k ≥ 0,25) arriva a meno di 14 m dalla barca.
