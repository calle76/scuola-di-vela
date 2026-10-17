# Proposta: la barca che si muove sul mare (solo disegno)

**Fermata 1, 17 ottobre 2026. Niente codice.** Osservazione di Ale giocando: «una barchetta così navigando è molto poco ferma… dall'alto sembra una nave molto stabile».

Tipi delle affermazioni: **[fonte]** letto, con dove; **[codice]** visto nel gioco; **[fisica]** conto da una legge nota; **[ipotesi]** scelta nostra, senza fonte.

## 0. Decisione di Ale (17 ottobre 2026) e cosa cambia nella proposta

«Deve essere carino da vedere, non perfetto. Si vede l'albero inclinarsi ma la barchetta rimanere ferma… e si rovescia tutto d'un colpo. Sarebbe bello vederla ballare sull'acqua: sono piccole e leggere, ed è quello che si nota subito guardando un video.» Vale come via alla fermata 2, senza la sessione sui video: i valori restano ipotesi dichiarate. Tre parti, tutte solo disegno:

1. **Lo scafo si inclina con lo sbandamento:** oltre a stringersi, sopravento compare la carena (lo stesso grigio della barca scuffiata), sempre di più sbandando. Così la scuffia continua il movimento invece di cambiare il disegno di colpo.
2. **La scuffia si vede cadere:** nei primi 0,6 s l'albero finisce di cadere sull'acqua, con uno spruzzo che si allarga. Si registra l'istante della scuffia (`S.capAt`, solo per il disegno).
3. **La barca balla sull'onda** (§2). L'interruttore nelle impostazioni **non si fa** (Ale non l'ha chiesto e non è un aiuto); la contro-prova del criterio 1 si fa con le ampiezze a zero in una copia.

## 1. Perché oggi sembra una nave [codice]

- Il gioco **non ha onde** (`FISICA-E-TARATURE.md`, semplificazioni: «niente onde né corrente»). Il mare ha solo le increspature disegnate, che scorrono sottovento.
- Lo sbandamento si disegna già (`js/disegno.js`, `drawBoat`): scafo più stretto, ombra spostata, testa d'albero sottovento. Ma di bolina e al traverso, fino a 15 nodi, il timoniere tiene la barca a **circa 5°** (`PROPOSTA-BOLINA.md` §11.1), e lo sbandamento cambia solo con raffiche e manovre. Fra una raffica e l'altra la barca disegnata è immobile.

## 2. Cosa propongo

**Un moto solo disegnato: il motore non cambia.** Velocità, rotta, sbandamento vero, scuffia, collaudi della fisica restano identici. La semplificazione si dichiara: le onde muovono il disegno, non frenano né spostano la barca.

- **Un'onda corta che arriva da dove arriva il vento** (onde generate dal vento locale, come le increspature) [fisica: le onde di vento vanno nella direzione del vento; ipotesi: niente onda lunga da un'altra direzione].
- **Due oscillazioni disegnate**, sommate al disegno dello sbandamento ma non a `S.heel`:
  - **rollio** (la barca dondola di lato): più forte con le onde al traverso;
  - **beccheggio** (la prua sale e scende): più forte con le onde di prua o di poppa. Dall'alto si vede come la testa d'albero e la parte alta della vela che vanno avanti e indietro, e l'ombra che si allunga e si accorcia.
  - Peso secondo l'angolo θ fra prua e onde: rollio ∝ |sin θ|, beccheggio ∝ |cos θ| [ipotesi, la più semplice].
- **Il ritmo dipende dall'andatura** [fisica, effetto Doppler]: andando contro le onde le si incontra più spesso, con le onde di poppa più di rado. Periodo d'incontro `Te = T / |1 + (u/c)·cos θ|`, con `c = g·T/2π` (velocità dell'onda in acqua profonda) e θ = 0 con la prua sulle onde.
- **Più vento, onde più alte:** ampiezza cresce col vento, zero a vento zero, con un tetto [ipotesi].
- Parte con l'orologio della simulazione (`simTime`), non con quello del browser: così l'impronta resta riproducibile.

**Costanti nuove, tutte ipotesi nostre senza fonte** (la ricerca qui sotto può sostituirle):

| Costante | Valore proposto | Perché |
|---|---|---|
| periodo dell'onda `T` | 2,0 s con 10 nodi, da 1,5 a 2,5 s fra 5 e 20 nodi | maretta corta di acque riparate; con `c = gT/2π` fa onde di circa 6 m, una volta e mezzo la barca |
| rollio massimo disegnato | 4° con 15 nodi, proporzionale al quadrato del vento, tetto 6° | deve vedersi senza sembrare una tempesta |
| beccheggio massimo disegnato | 3° con 15 nodi, stessa legge, tetto 4,5° | idem |

**Il ritmo d'incontro viene da solo:** l'onda è un campo η(x, y, t) che scorre sottovento; la barca prende la pendenza dell'onda nel punto dove si trova, di prua (beccheggio) e di lato (rollio). Andando contro le onde la fase cambia più in fretta, con le onde di poppa più piano: è l'effetto Doppler senza scriverlo a parte. Una seconda onda più corta, 30° di lato, rende il moto meno regolare [ipotesi].

## 3. Fonti

- **Trovato [fonte]:** definizioni di rollio e beccheggio (quiz della patente nautica in `fonti-pdf/`, solo per i termini); «la deriva abbassata dà stabilità ed evita in parte il rollio» (dispensa FIV 2019, in `fonti-pdf/`, frase da parafrasare se usata).
- **Non trovato:** quanti gradi e in quanti secondi oscilla una deriva da 4 m nella maretta. **Proposta di ricerca prima della fermata 2:** una sessione *video* (Ale): due o tre video di derive monoposto di bolina e al traverso con vento medio, contando le oscillazioni in 10 s e stimando l'ampiezza dall'albero. Se non si trova niente, i valori restano ipotesi dichiarate, come la velocità delle increspature nelle raffiche (aiuto visivo senza fonti, 1.0.19).

## 4. Criteri della fermata 2 (soglie dichiarate adesso, attese nostre)

1. **Motore identico:** `polare.js` e `raffiche_e_virate.js` carattere per carattere; `collaudo_impronta.py` uguale su **tutte le scene tranne le immagini del mare** (stato delle barche, registro, testi identici al bit; le 21 immagini cambiano). Contro-prova: con le ampiezze a zero cambiano solo le immagini con la barca sbandata o scuffiata (carena e caduta).
2. **Si vede:** a zoom 1, con 10 nodi, la testa d'albero oscilla di **almeno 4 px** (da picco a picco) a ogni andatura; a vento zero **0 px**.
3. **Dipende da dove arrivano le onde** (misurato sul disegno, 5 semi, 30 s ciascuno): con le onde al traverso il rollio è **almeno il doppio** del beccheggio; di bolina e in poppa il beccheggio è almeno il doppio del rollio; di bolina il periodo d'incontro è **più corto** che in poppa.
4. **Costo del disegno:** al massimo **+2%** per quadro (misurato come per le increspature, 300 quadri).
5. **Pannello:** non cambia (nessun testo nuovo).
6. Pagina con e senza `#collaudo`: nessun errore; partita guidata col pilota in una regata.

## 5. Rischi

- **Confusione fra moto disegnato e sbandamento vero:** le lezioni insegnano a guardare lo sbandamento. Il dondolio deve restare piccolo rispetto allo sbandamento di una raffica (4° contro 20-40°), e il numero dello sbandamento nel pannello resta quello vero.
- **Filetti e vela:** si spostano con la testa d'albero; da controllare che non sembrino sbattere.
- **Avversari:** stesso moto anche per loro (stessa funzione di disegno), altrimenti si nota la differenza.
- **Onde invisibili:** la barca dondola ma il mare non mostra onde. **Seconda parte, da decidere:** disegnare anche creste lunghe e tenui, sincronizzate col dondolio. Costa di più (criterio 4 da rifare) e la propongo solo se, giocando, la prima parte sembra «dondolio senza motivo».

## 6. Esito della fermata 2 (17 ottobre 2026, versione 1.0.23)

**Richieste di Ale arrivate durante il lavoro, tutte solo disegno:** da ferma la barca balla di più («quando naviga si vede di meno»): ampiezza fino al doppio sotto 1,5 m/s, normale da circa 3 nodi; il timoniere disegnato col corpo che si sporge fuori bordo; l'acqua che si alza sulla prua; il timone ha una **prolunga** («non fare un braccio del timoniere lungo due metri»): il braccio è lungo al massimo 45 cm, la prolunga va dalla fine della barra alla mano.

Cosa c'è nel disegno (`js/disegno.js`, `waveTilt` e `drawBoat`): onda corta che scorre sottovento più una seconda più corta a 30°; rollio e beccheggio presi dalla pendenza dell'onda dove sta la barca; leggero avvicinamento sulla cresta; carena grigia sopravento sbandando; caduta dell'albero in 0,6 s con uno spruzzo quando scuffia (`S.capAt`, scritto in `gioco.js` e `regate.js` solo per il disegno); timoniere con gambe, busto, testa e braccio; prolunga; baffi d'acqua alla prua aperti di circa 20° dalla rotta (l'angolo di Kelvin delle scie, [fisica]) e uno spruzzo quando la prua scende sull'onda.

| Criterio | Esito |
|---|---|
| 1. Motore identico | `polare.js` e `raffiche_e_virate.js` identici carattere per carattere all'ultimo commit; impronta: **4.049 voci di stato su 4.049 identiche**, 20 immagini del mare su 21 diverse (com'era previsto). La contro-prova con le ampiezze a zero **non è stata fatta** |
| 2. Si vede | Con 10 nodi da 7 a 12 px a ogni andatura (soglia 4); senza vento 0,0 px |
| 3. Da dove arrivano le onde | Traverso: rollio 11-12 px contro beccheggio 1,5 (rispettato); poppa: beccheggio 7,6-8,7 contro rollio 2,1 (rispettato); periodo di bolina 1,6 s contro 4,4 in poppa (rispettato). **Di bolina il criterio «beccheggio almeno il doppio del rollio» non è rispettato** (7,2-9,0 contro 7,2-9,2): era sbagliato in partenza, perché di bolina le onde arrivano a circa 45° dalla prua e con questo modello i due vengono uguali. **Tolto dal collaudo e dichiarato qui**, senza sostituirlo con un'altra soglia |
| 4. Costo del disegno | Quadro mediano 1,7 ms prima, 1,6 ms dopo (4 giri alternati): la differenza è **sotto il rumore della misura** (da 1,5 a 2,1 ms fra un giro e l'altro della stessa versione), non un guadagno |
| 5. Pannello | Nessun testo nuovo: non lanciato |
| 6. Pagina | Con `#collaudo`: 0 errori su 24.000 quadri; senza `#collaudo`, regata giocata con la tastiera per circa 16 s: 0 errori |

**Primo giro del collaudo: metro sbagliato, corretto.** «Di lato» misurava anche lo sbandamento vero (1,1 px senza vento, fino a 25,7 px in poppa quando il boma cambia lato); ora si toglie la parte dello sbandamento vero. **Non misurato a parte:** quanto balla di più la barca ferma; da giudicare giocando (Ale).
