# Tappa C4 — massa e coppia raddrizzante di una deriva a due: proposta (fermata 1)

> **ESITO, deciso il 4 ottobre 2026: NON CAMBIARE NIENTE.** Il prototipo resta con lo scafo e il
> timoniere del gioco a una vela, e il sovrainvelamento si dichiara. Il banco grande (108 raffiche,
> 12 soglie di scuffia, 132 equilibri di polare, 288 virate, 36 giri nel browser) **non è stato
> eseguito**, e la riga nel gancio `window.__sv` **non è stata aggiunta**: `step()` e
> `sperimentale/fiocco.html` non sono stati toccati. Le ragioni sono ai punti 1, 5 e 8 di questa
> proposta e riassunte in `docs/FISICA-E-TARATURE.md`. Il resto del documento resta come era scritto
> prima della decisione, come registro.

Scritta il 4 ottobre 2026. **Solo proposta: nessun codice nel motore, `index.html` non si tocca.**
La tappa C4 è dichiarata «solo confronto» in `docs/SPERIMENTALE.md`: serve a sapere **cosa cambierebbe**
se il prototipo del fiocco girasse sulla massa e sulla stabilità di una barca a due, non a cambiarlo.

## 1. Il problema, in numeri che già abbiamo

Il prototipo ha lo scafo e il timoniere del gioco (`mass` 135 kg, `sailorMass` 75 kg, `hikeArm` 1,0 m)
e il 37% di vela in più (7,0 + 2,6 = 9,6 m²). Conseguenze già misurate: una raffica da 10 a 20 nodi
senza reagire fa **scuffiare** (con la sola randa si fermava a 55°), e a 15 nodi la virata non riesce.

Conto sulle costanti attuali (non una misura del motore: aritmetica su `BOAT`), coppia raddrizzante
totale = `sailorMass·g·hikeArm·cos φ + formK·sin 2φ / 2`:

| Sbandamento | 0° | 10° | **22,6°** | 25° | 45° | 60° |
| --- | --- | --- | --- | --- | --- | --- |
| Coppia del prototipo (kgf·m) | 75,0 | 80,8 | **83,7 (massimo)** | 83,6 | 73,4 | 55,2 |

Due cose da notare subito.

- **La forma della curva è già coerente con la fonte:** il massimo cade a 22,6°, la fonte lo mette a
  circa 25°. Non è un caso costruito: viene dalla somma di un termine che cala con `cos φ` (il
  timoniere) e di uno che cresce fino a 45° (la stabilità di forma).
- **Il valore no, ma al rovescio di come sembra.** Il nostro timoniere singolo dà **83,7 kgf·m**,
  cioè **più** dei **circa 60 kgf·m** che la fonte attribuisce a una deriva a due **senza trapezio**.
  Se si prende quel numero alla lettera, passare alla barca a due *senza* trapezio rende la barca
  **meno** stabile di oggi, non più. L'unica configurazione che risolve davvero il sovrainvelamento
  è quella **con il trapezio**, circa 220 kgf·m.

Questo è il nodo della tappa, e non si può decidere leggendo il codice: va misurato.

## 2. Le configurazioni da provare: quattro, dichiarate adesso

| Sigla | Cosa rappresenta | `mass` | `sailorMass` | `hikeArm` | `formK` | `rollI` | `rollDamp` | Coppia a 25° |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **a** | oggi: scafo e timoniere del gioco | 135 | 75 | 1,00 | 400 | 260 | 520 | 83,6 kgf·m |
| **b1** | due persone, **senza** trapezio | 200 | 110 | 0,37 | 593 | 385 | 770 | 60 kgf·m |
| **b2** | due persone, **con** trapezio | 200 | 110 | 1,97 | 593 | 385 | 770 | 220 kgf·m |
| **b3** | barca più pesante, con trapezio | 250 | 130 | 1,62 | 741 | 481 | 963 | 220 kgf·m |

Come sono stati ricavati i valori di `b*` (ogni passaggio è una scelta, dichiarata):

- `mass`: 200 kg = scafo circa 90 + equipaggio 110 (estremo «classe giovanile», la fonte dà
  190-225); 250 kg = scafo 120 + equipaggio 130 (estremo olimpico). Sono i due estremi della fascia
  190-250 kg delle fonti, non una media.
- `sailorMass`: la massa dell'equipaggio intero, perché nel motore è l'unica massa che si sporge.
- `hikeArm`: **non scelto, ricavato**, imponendo che la coppia raddrizzante **totale a 25°** valga
  quella della fonte (60 oppure 220 kgf·m). 25° è l'unico punto che la fonte dà.
  `hikeArm = (coppia − formK·sin 50°/2) / (sailorMass·g·cos 25°)`.
- `formK`, `rollI`, `rollDamp`: scalati in proporzione alla massa (`× mass/135`). **Ipotesi pura,
  nessuna fonte:** è la regola più semplice (stessa forma, stesso raggio di inerzia), non una misura.
- `capsizeAt` resta **60°** in tutte le configurazioni. Confrontare la soglia di scuffia con la
  fonte è la calibrazione futura 5, non questa tappa.
- `zCE`, `zJibCE`, le aree e tutta l'aerodinamica restano **identiche**: qui si cambia solo la barca
  sotto le vele.

Effetto collaterale da dichiarare: con la calibrazione «uguale a 25°» il **massimo** si sposta
(b1 a 34°, b2 a 14°, b3 a 17°, contro i 22,6° di oggi e i 25° della fonte), perché nelle b* con
trapezio il termine dell'equipaggio domina e cala con `cos φ`. La fonte dà un solo punto: non si
possono rispettare insieme il valore e l'angolo del massimo senza cambiare la **forma** della curva,
e cambiare la forma è codice nel motore (il braccio dovrebbe crescere con lo sbandamento). **Fuori
dalla tappa C4.**

## 3. Il banco: come legge `step()` senza modificarlo

`BOAT` è un oggetto esportato da `motore_fiocco.js` e i suoi campi sono scrivibili: il banco
**sovrascrive le costanti prima di chiamare `step()`**, e `step()` non viene toccato. Stessa tecnica
già usata in `misure_tappaC2.js` e `banco_tappaC3.js`, ma più pulita: lì il modello candidato era
emulato fuori dal motore, qui non c'è nessun modello nuovo, solo altri numeri negli stessi posti.

Due file nuovi, nessun file esistente riscritto (i risultati di A, B, C1-C3 restano come sono):

- `sperimentale/banco_tappaC4.js` (Node) — sbandamento, soglia di scuffia, polare, virate.
  Esce in `banco_tappaC4.txt`.
- `sperimentale/banco_tappaC4.py` (browser, Playwright) — i tempi delle prove 1-3 guidando davvero
  la barca col pilota automatico, come fa `collaudo_fiocco.py`. Esce in `banco_tappaC4-prove.txt`.

**Per la parte nel browser serve una riga nel prototipo**, perché `BOAT` sta dentro una funzione
chiusa e dal browser non è raggiungibile: aggiungere `get BOAT(){ return BOAT; }` al gancio
`window.__sv`, **dentro il blocco `if (location.hash === "#collaudo")`**, marcata `// FIOCCO`.
Non è codice nel motore ed è lo stesso genere di appiglio che il gancio ha già per il colpo della
strambata (`kick: n => GYBE_KICK = n`). Una pagina caricata da un giocatore, senza `#collaudo`, non
ha il gancio e non cambia di una virgola. L'alternativa — riscrivere i numeri nel testo della pagina
con l'intercettazione di Playwright, senza toccare il file — la scarto perché **non si potrebbe
verificare che la sostituzione abbia funzionato**, e un collaudo che non parte passa sempre.
Con `BOAT` nel gancio il banco **rilegge le costanti dalla pagina e si ferma se non coincidono**
con quelle che voleva.

Due limiti da dichiarare prima:

- Sovrascrivere `BOAT` cambia **tutte** le barche, comprese quelle degli avversari e il fantasma, che
  leggono le stesse costanti. Per questo si misurano **solo le prove 1-3 e la navigazione libera**,
  dove non ci sono avversari. **Niente regate in questa tappa.**
- I valori assoluti del banco Node **non sono confrontabili** con quelli del browser (lezione della
  tappa C3: il pilota del browser tiene la barra a 0,8 invece di spingerla a fondo). Confrontabili
  sono solo le righe dello stesso banco fra loro.

## 4. Criteri, dichiarati prima di misurare

Soglie scritte adesso come **attese nostre**, non come verità. Un numero fuori fascia si riporta
così come è. Ogni prova stampa **quanti casi ha misurato** e fallisce se sono zero.

| # | Cosa si misura | Casi | Attesa dichiarata |
| --- | --- | --- | --- |
| C4-1 | Sbandamento massimo con raffica improvvisa da 10 a 16, 18 e 20 nodi, senza reagire, di bolina e al traverso | 4 config × 3 andature (45°, 60°, 90°) × 3 raffiche = **108** | **a** scuffia a 20 nodi (già noto). **b1** scuffia a 20 nodi **o peggio di a**. **b2** e **b3** non scuffiano a 20 nodi e restano **sotto 45°** |
| C4-2 | Soglia di scuffia: il vento di raffica più basso che fa superare i 60°, cercato da 12 a 30 nodi a passi di 0,5 | 4 config × 3 andature = **12 ricerche** | **a** fra 18 e 20 nodi. **b1 più bassa di a.** **b2** e **b3** sopra 24 nodi |
| C4-3 | Polare: velocità di equilibrio con la regolazione migliore delle due vele | 4 config × 11 angoli × 3 venti (6, 10, 15 nodi) = **132 equilibri** | A 6 e 10 nodi scarto **entro il 5%** fra le configurazioni; a 15 nodi **le b\* più veloci di a** (sbandano meno, quindi le vele prendono più vento), di **più del 10%** da qualche parte |
| C4-4 | Virata di bolina: riuscita e tempo, a 10 e 15 nodi, con fiocco cazzato, a metà e lascato | 4 config × 2 venti × 4 velocità iniziali × 3 regolazioni × 3 direzioni del vento = **288 virate** | **a** a 15 nodi riesce in meno di metà dei casi (è il problema). Per le **b\*** **non sappiamo il verso**: più massa porta più abbrivio attraverso l'angolo morto ma accelera peggio. Diciamo risolto se riesce in **almeno 2 casi su 3** |
| C4-5 | Tempi delle prove 1, 2 e 3 nel browser, col pilota automatico | 4 config × 3 prove × 3 direzioni del vento = **36 giri** | Prove 1 e 2 (lasco e poppa, sbandamento piccolo): scarto **entro il 10%**. Prova 3 (tutta di bolina, con virate): può cambiare di più. Nessuna scuffia, nessuna barca piantata |
| C4-6 | Non-regressione, con le sovrascritture **spente** | 30 casi di `polare.js` + uscite di `polare.js` e `raffiche_e_virate.js` | Scarto **zero** e uscite **identiche carattere per carattere**; `index.html` non modificato |

**Perché nessuno di questi criteri è vero per costruzione.** Il punto debole della tappa C3 era che
l'effetto da misurare era anche la taratura: «col fiocco cazzato si vira meglio» era vero perché
l'avevamo scritto noi. Qui è diverso, ma non per tutti i criteri, e lo dico prima:

- **C4-1 e C4-2 sono in parte veri per costruzione:** più coppia raddrizzante dà meno sbandamento,
  per forza. Quello che **non** è automatico è **di quanto** e **con quale verso per b1**: la fonte
  dà a una barca a due senza trapezio *meno* coppia del nostro timoniere singolo, quindi l'attesa
  dichiarata per b1 è un **peggioramento**. Se b1 venisse meglio di a, il conto del punto 1 è
  sbagliato e lo scopriamo.
- **C4-3 non è affatto automatico, ed è il criterio più importante.** Nel motore la resistenza dello
  scafo (`4u + 12u² + 0,9u⁴`) **non dipende dalla massa**: la massa entra solo nell'accelerazione.
  Quindi una barca da 250 kg, a regime, va **come** una da 135 kg, e anzi **più forte**, perché
  sbanda meno e le vele prendono più vento (`cos φ`) e lo scafo frena meno (`heelDrag`). Una barca
  più pesante che va più veloce è **sbagliata**, e sarebbe un risultato della tappa, non un difetto
  del banco.
- **C4-4 non è automatico:** massa e inerzia di rotazione tirano in versi opposti.
- **C4-5 non è automatico:** i tempi dipendono da polare, virate e da quanto il pilota automatico se
  la cava con una barca diversa.

## 5. Quello che mi aspetto di trovare, scritto prima

Che la strada (b) **non sia finibile oggi**, e per un motivo che non c'entra con la stabilità: senza
ritarare `hullK2` e `hullK4` la barca a due risulta più pesante **e più veloce**, e per ritararli non
c'è una fonte (F10 non è stata letta, polari pubbliche di derive non risultano). Se i numeri lo
confermano, la tappa C4 si chiude come le C2 e C3: **confronto fatto, modello non adottato**, con il
motivo scritto. Se invece lo scarto della polare resta entro il 5% anche a 15 nodi, la strada (b)
diventa praticabile con quattro costanti e la decisione passa alla giocabilità (punto 7).

## 6. Timone a 30° contro lo stallo a circa 15° della fonte (nessuna modifica)

Richiesto: dire se è coerente, senza toccarlo. Conti sulle costanti attuali, a 6 nodi (3,09 m/s),
gli stessi 6 nodi della fonte:

| | Fonte (F4) | Motore |
| --- | --- | --- |
| Resistenza totale dello scafo | 19 kgf | **21,2 kgf** |
| Resistenza del timone a 15° | 12 kgf | **2,9 kgf** (14% dello scafo) |
| Resistenza del timone a 30° | — (è già in stallo) | **10,9 kgf** (51% dello scafo) |

**Risposta: non è coerente, ma l'incoerenza si compensa in parte.** La resistenza totale dello scafo
coincide quasi (21,2 contro 19 kgf: buon segno per `hullK2`/`hullK4` a quella velocità). Il timone
invece, nel motore, a 15° costa **un quarto** di quello che dice la fonte; il prezzo che la fonte
mette a 15° il motore lo raggiunge solo **vicino a 30°**. Quindi l'angolo massimo di 30° del motore
«costa» più o meno come il 15° reale, e un giocatore che tiene la barra a fondo paga un prezzo
dell'ordine di grandezza giusto.

Resta però una differenza che non si compensa: **nel motore la pala non va mai in stallo.** La
velocità di rotazione cresce con `sin` dell'angolo fino a 30°, cioè portare la barra da 15° a 30°
fa girare **1,93 volte più in fretta**, mentre nella realtà oltre i 15° circa si perde autorità e
resta solo la resistenza. Nel motore la barra a fondo è sempre la scelta migliore per girare; nella
realtà no, ed è una cosa che si insegna. Rimane la **calibrazione futura 4**, con due osservazioni
per quando si farà: (1) toccare il timone cambia **tutte** le virate e tutti i tempi delle prove e
delle fasce, quindi è una modifica al gioco, non al prototipo; (2) l'alternativa più piccola non è
abbassare `maxRudder`, ma far **calare** la velocità di rotazione oltre i 15°, così la barra a fondo
resta possibile e diventa un errore.

## 7. Giocabilità: cosa cambia per chi gioca

- **Strada (a), nessun cambiamento.** Il livello 2 in aria fresca è duro: raffica da 20 nodi =
  scuffia, a 15 nodi la virata non riesce. Giocabile solo se le lezioni e i tornei del livello 2
  restano **sotto i 12-14 nodi**, e se l'eccesso di vela si **insegna** («questa barca ha troppa
  vela per uno: è per questo che siete in due»). Costo: la lezione **2.5 «Raffiche in due»**, in cui
  «il prodiere lascia e sposta il peso», non si può fare — nel motore il peso lo sposta un automatismo
  da 0,9 s, non un ruolo.
- **Strada (b1), due senza trapezio.** Secondo la fonte la barca diventa **meno** stabile e più
  lenta a reagire: il peggio dei due mondi. Da provare proprio perché l'attesa è negativa.
- **Strade (b2) e (b3), con trapezio.** La barca regge i 20 nodi, ma il trapezio è una **seconda
  novità principale** per il livello 2, e `VISIONE-LIVELLI-E-CARRIERA.md` ne ammette una sola per
  livello (la novità del 2 è «il fiocco e il coordinamento a due»). È anche un meccanismo nuovo:
  prodiere dentro e fuori, tempi, e il peso che diventa un **comando** invece di un automatismo.
  Non è una taratura di quattro costanti: è un pezzo di gioco.
- In tutte le b* la barca **accelera più lentamente** e perde meno abbrivio: più lenta a ripartire
  dall'angolo morto, più «piantata» a vento leggero. Sono le due sensazioni da far giudicare a chi
  gioca, e sono l'unica domanda che gli faremo (non la plausibilità nautica).

## 8. «Non cambiare niente e dichiarare il sovrainvelamento»: quando è la scelta migliore

Lo è **adesso**, e sarebbe la mia raccomandazione se si verificano le condizioni qui sotto — che è
anche quello che il banco deve dirci:

1. **La polare si rompe** (criterio C4-3 fuori dal 5% a 15 nodi) e non c'è fonte per ritarare la
   resistenza dello scafo. Cambiare la massa senza la resistenza dà una barca pesante e veloce:
   sarebbe una fisica peggiore di quella di oggi, non migliore.
2. **La stabilità vera richiede il trapezio** (b1 peggiore di a), e il trapezio è una novità che il
   disegno dei livelli assegna altrove.
3. **Il peso dell'equipaggio dovrebbe diventare un ruolo**, non un automatismo: è la lezione 2.5, e
   tocca il motore e il pannello, non le costanti.

In quel caso la tappa C4 si chiude così: la barca a due **non si approssima** con quattro costanti,
si costruisce in una volta — massa, resistenza dello scafo, peso dell'equipaggio come comando,
trapezio e pannello — quando ci sarà una fonte per la resistenza. Fino a lì il prototipo resta
quello che è, **con il sovrainvelamento scritto** in `FISICA-E-TARATURE.md` e in
`CONTENUTI-DA-VERIFICARE.md` (c'è già) e con il vento del livello 2 tenuto nella fascia in cui la
barca si governa. Il guadagno del banco non è il modello: è **sapere di quanto** si sbaglia, e
avere i quattro numeri pronti per il giorno in cui si farà la barca a due.

Sarebbe invece **sbagliato** non cambiare niente se il banco mostrasse che le b* non rompono la
polare (scarto entro il 5% anche a 15 nodi) e che b1 **senza** trapezio già risolve raffica e
virata: in quel caso quattro costanti compererebbero una barca più plausibile senza novità nuove, e
rifiutarle sarebbe pigrizia.

## 9. Quali numeri sono ipotesi

| Numero | Stato |
| --- | --- |
| `mass` 200 e 250 kg | **Dalle fonti** (fascia 190-250), ma la scelta dei due estremi è nostra |
| Massa dell'equipaggio 110 e 130 kg | **Dalle fonti** |
| Coppia a 25°: 60 e 220 kgf·m | **Dalle fonti, ma una sola barca** e un solo punto della curva |
| `hikeArm` 0,37 / 1,97 / 1,62 m | **Ricavati** dalla coppia, non scelti. Dipendono dall'ipotesi su `formK` |
| `formK` 593 e 741 Nm | **Ipotesi pura:** stabilità di forma scalata con la massa. Nessuna fonte |
| `rollI` 385 e 481, `rollDamp` 770 e 963 | **Ipotesi pura:** scalati con la massa. Nessuna fonte. Il dubbio maggiore è lo smorzamento, che nella realtà dipende dalla forma dello scafo, non dalla massa |
| Ritardo del timoniere 0,9 s invariato | **Ipotesi:** con due persone e un trapezio il tempo di reazione è un'altra cosa |
| `capsizeAt` 60° invariato | **Da confrontare** con le fonti: è la calibrazione futura 5, non questa tappa |
| Forma della curva raddrizzante (`cos φ`) | **Semplificazione del motore.** Il massimo cade a 22,6° contro i 25° della fonte: coerente oggi, ma con le b* si sposta a 14-34° |
| Tutta l'aerodinamica, aree, `zCE` | Invariate: le ipotesi sono quelle già elencate in `CONTENUTI-DA-VERIFICARE.md` |

## 10. Rischi

- **Il banco misura una barca che non esiste.** Quattro costanti non fanno una deriva a due: non c'è
  il secondo corpo che si muove, né il trapezio, né una resistenza che dipenda dal dislocamento.
  I numeri valgono come **confronto**, non come calibrazione. Va scritto in ogni riga del rapporto.
- **Tre delle sette costanti sono ipotesi pure** (`formK`, `rollI`, `rollDamp`), e `hikeArm` dipende
  da una di esse. Rimedio: riportare la coppia a 25° **misurata** nel banco, che è il numero
  confrontabile con la fonte, non `hikeArm`.
- **Sovrascrivere `BOAT` cambia anche avversari e fantasma.** Rimedio: niente regate, solo prove 1-3
  e navigazione libera; dichiarato nel rapporto.
- **La riga nel gancio `#collaudo`** è una modifica a `sperimentale/fiocco.html`. Rimedio: una riga,
  marcata `// FIOCCO`, dentro il blocco del collaudo; non-regressione (C4-6) e controllo che
  `index.html` non risulti modificato.
- **36 giri nel browser sono lunghi** (stimo 15-25 minuti). Rimedio: il banco accetta la
  configurazione come argomento, così si lancia una per volta.
- **Si potrebbe scoprire che il problema vero è un altro** (la resistenza dello scafo, o il timone
  del punto 6) e che la massa era la domanda sbagliata. Non è un rischio da evitare: è un esito.

## 11. Cosa non c'è in questa proposta

Nessuna modifica a `step()`. Nessun trapezio. Nessuna ritaratura della resistenza dello scafo, del
timone, della soglia di scuffia o della forma della curva raddrizzante. Nessun cambiamento ai
contenuti del livello 2. Nessuna regata misurata.

## 12. Serve il via

Con il via faccio: `banco_tappaC4.js`, `banco_tappaC4.py`, la riga nel gancio `#collaudo`, i sei
criteri misurati con i casi dichiarati, il rapporto con i numeri così come escono, e
l'aggiornamento di `SPERIMENTALE.md`, `FISICA-E-TARATURE.md`, `FONTI-PUBBLICHE.md`,
`CONTENUTI-DA-VERIFICARE.md` e `CHANGELOG.md` (sotto «Sperimentale»). Poi mi fermo.

Se preferisci meno: la parte Node (C4-1 a C4-4 e C4-6) sta in un file e non tocca il prototipo.
I tempi delle prove 1-3 (C4-5) sono l'unica parte che chiede la riga nel gancio.
