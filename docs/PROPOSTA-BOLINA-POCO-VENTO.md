# Proposta: bolina e virata con poco vento (voce 81)

*Fermata 1, 23 novembre 2026, sera. Ale: «sì ok» a riaprire il «limite noto» del 17 ottobre come voce nuova. Nessun codice nel motore finché non arriva il via.*

## Da dove viene

- **17 ottobre 2026:** con poco vento la bolina del gioco è più lenta delle fonti (−15% con 6 nodi contro Day, F17; −12/−14% con 9 nodi contro Binns, F10 in F17), con 12 nodi coincide con Binns. Due tentativi non hanno trovato la causa; Ale ha scelto «limite noto» (`archivio/PROPOSTA-BOLINA.md` §11).
- **22-23 novembre 2026 (voci 73 e 80):** una terza fonte indipendente, **F109** (Laser misurato in acqua), dice la stessa cosa: con 3,2 nodi di vento, prua a 45°, la barca vera fa 1,05 m/s, il gioco 0,88 (−16%). E la **virata** con poco vento costa nel gioco 2,2-2,7 m contro 0,67 m della barca vera; col vento medio invece è giusta (`PROPOSTA-BARCA-73.md` §5b).
- **Perché ora:** regola di Ale «prima la barca, poi il resto» e «prima ciò su cui si tarano le altre voci»: i rivali (voci 2, 4B, 49 B, marcatura) si tarano sulla barca.

## Cosa è già escluso (17 ottobre, al centesimo)

Rampa dell'angolo morto della vela, barca tenuta piatta, timoniere che va anche sottovento, vasca sotto 3 nodi più leggera del 10%. Una vela «più forte» o meno frenata alza il poco vento ma porta i 12 nodi sopra Binns: **nessuna costante della sola vela mette a posto insieme 9 e 12 nodi.**

## Ipotesi nuove (da verificare con fonti prima di misurare)

1. **La forma della vela non cambia col vento.** Nel gioco la vela ha lo stesso profilo con 3 e con 15 nodi; in mare con poco vento si lascia la vela più grassa (vang e cunningham lenti), col vento medio la si appiattisce. I programmi di previsione delle velocità (VPP) lo rappresentano con un fattore di appiattimento («flat») che toglie portanza solo quando la barca è al limite dello sbandamento. Se è così, con poco vento la vela vera porta di più del gioco, e col vento medio uguale: **è l'unica ipotesi che separa 9 da 12 nodi.** Fonti da cercare: documentazione del VPP ORC (fattore flat), guide di regolazione della deriva monoposto (vang e cunningham con poco vento), Day 2017 (se usa il flat).
2. **Il vento all'altezza della vela.** Il gioco usa lo stesso vento a tutte le altezze; le fonti misurano il vento a un'altezza precisa (da leggere in F17, F10, F109). Con poco vento il gradiente pesa di più. Può spiegare una parte, in un verso o nell'altro: prima si legge a che altezza è misurato il vento delle fonti.
3. **La virata con poco vento** costa di più anche perché la barca è più lenta prima e dopo (parte dell'ipotesi 1) e perché con la tastiera la barra va tutta alla banda (la pala frena: con la prua girata dolcemente si perdono 1,74 m invece di 2,2-2,7). La seconda parte non è un difetto della barca ma del comando: si guarda dopo l'ipotesi 1.

## Come si procede (fermata 1, poi fermata 2)

- **Fermata 1 (questa):** leggere le fonti delle ipotesi 1 e 2; solo se c'è un numero con fonte, una prova **fuori dal motore** (copia in memoria, banco del 17 ottobre e `prua_imposta.js`), senza numeri a caso. Poi proposta con le costanti e i criteri definitivi, e ci si ferma.
- **Fermata 2 (dopo il via):** motore cambiato, collaudi, rivali, fasce delle prove e record.

## Criteri (attese nostre, scritte ora; restano le soglie della fermata 2)

| | Cosa | Soglia |
| --- | --- | --- |
| B1 | VMG di bolina con 6 nodi contro Day (F17 fig. 8) | entro −5% (oggi −15%) |
| B2 | Binns con 9 nodi, 42°-60° | entro ±5% a tutti gli angoli (oggi −11/−14%) |
| B3 | Binns con 12 nodi | entro ±3% (oggi −1/+1%): non deve peggiorare |
| B4 | 15 nodi contro Day | non peggio di oggi (+7%) |
| B5 | Velocità a 45° con 3,2 nodi contro F109 (1,05 m/s) | entro −8% (oggi −16%) |
| B6 | Virata con 3,2 nodi, prua imposta come F109 | metri persi da 1,74 verso 0,67: almeno −30% |
| B7 | Poppa e lasco | invariati entro 0,03 nodi |
| B8 | Una costante nuova al massimo, con fonte; nessuna costante cambiata senza fonte | sì |

## Costo, se si arriva alla fermata 2

Cambia la barca: polare e `raffiche_e_virate.js` con riferimenti nuovi (dichiarato), fasce delle prove ritarate e record azzerati (decisione di Ale del 15 novembre: azzerabili), rivali da rimisurare (torneo, guardiano), collaudi coi tempi. Lavoro da Opus, in più sessioni.

## Rischi

- Le fonti potrebbero non dare un numero usabile per il fattore di appiattimento: allora ci si ferma e il limite resta (come il 17 ottobre).
- Il gioco «sembra» diverso: con poco vento la barca va più forte; le lezioni che parlano di bolina con poco vento vanno rilette.

## Fermata 1: cosa dicono le fonti e cosa dà il banco (23 novembre 2026, sera)

### Le fonti [fonte]

- **Ipotesi 2 (vento all'altezza della vela): esclusa.** F109 misura il vento **in testa d'albero** (anemometro su un'asta sopra la cima, cap. 1.3.2): il vento vero alla vela è un po' più debole, quindi semmai la barca vera va forte con *meno* vento del gioco, e il divario cresce invece di spiegarsi. Binns (F10, in F17 §4) non dice dove era misurato il vento; Day non usa un gradiente.
- **Ipotesi 1 (fattore «flat»): riformulata.** In Day (F17 §2.3, eq. 2 e 6) FLAT *toglie* portanza e si usa solo quando la barca è al limite del momento raddrizzante; con poco vento vale 1 (vela piena). Non può quindi dare più velocità con poco vento. Il gioco ha già il suo modo di sventare (la scotta, §11.1 dell'archivio: con 15 nodi CL 0,93).
- **Il numero che conta, invece:** Day (§6.2 e §6.3) dice che **il timoniere comincia a sventare intorno ai 9 nodi** (da lì in su vince chi pesa di più). Nel gioco, a 46,5° dal vento, il timoniere è fuori al 58% con 9 nodi e arriva al massimo solo verso i 12-15 nodi. È questo che separa 9 da 12 nodi: la barca vera con 12 nodi è già frenata dallo sbandamento, quella del gioco no. Per questo, a ottobre, una vela più forte alzava anche i 12 nodi.
- **Braccio sbandante `zCE` (2,0 m, senza fonte):** Day mette il centro velico al 36,4% dell'inferitura sopra il boma, ma le misure dell'armo non ci sono né in Day né nel regolamento ILCA scaricato (`HANDBOOK_2025.pdf`: solo area 7,06 m², lunghezze dello scafo). **La costante resta senza fonte.**

### Il banco [misura]

`sperimentale/bolina-81/banco81.js` (copia del motore in memoria, nessun numero casuale: un giro basta; uscita in `banco81_varianti.txt`). Resistenza della vela al punto di lavoro: oggi 0,34; 0,27 = Flay in galleria; 0,21 ≈ ORC come Day.

| Variante | Day 6 / 10 / 15 nodi | Binns 9 nodi, 42°-60° | Binns 12 nodi, 42°-60° | Timoniere fuori a 9 nodi |
|---|---|---|---|---|
| oggi | −16 / −10 / +6% | −15 −12 −14 −15 | −2 −2 −2 −1 0 | 58% |
| vela 0,27 | −9 / −4 / +11% | −11 −7 −9 −11 | +3 +4 +5 +4 +4 | 58% |
| vela 0,27, `zCE` 2,8 | −9 / −5 / +2% | −11 −7 −10 −11 | −2 −3 −4 −3 −4 | 82% |
| vela 0,27, `zCE` 3,2 | −9 / −6 / −2% | −11 −7 −10 −11 | −4 −6 −6 −8 −7 | 95% |
| vela 0,21, `zCE` 3,2 | **−4** / −3 / 0% | −8 −3 −7 −9 | −2 −3 −5 −5 −5 | 93% |
| vela 0,21, `zCE` 3,6 | −4 / −5 / −4% | −8 −5 −7 −9 | −4 −7 −8 −8 −8 | 100% |

Virata con la prua imposta (`prua_imposta.js`, 3,2 nodi, virata in 10 s; F109: velocità 1,05 m/s, −0,67 m):

| Variante | Velocità prima | Metri persi | Di cui «prima» (F109 +1,48) |
|---|---|---|---|
| oggi | 0,88 m/s (−16%) | −1,74 | +0,28 |
| vela 0,27, `zCE` 3,2 | 0,92 m/s (−12%) | −1,65 (−5%) | +0,29 |
| vela 0,21, `zCE` 3,2 | 0,94 m/s (−10%) | −1,57 (−10%) | +0,30 |

### Contro i criteri scritti prima

La variante migliore (vela 0,21, `zCE` 3,2): **B1 passa** (−4%), **B4 passa** (0%), **B2 no** (−3…−9%, soglia ±5%), **B3 no** (fino a −5%, soglia ±3%), **B5 no** (−10%, soglia −8%), **B6 no** (−10%, soglia −30%), **B8 no** (due costanti cambiate, `zCE` senza fonte). Nessuna variante passa tutti i criteri.

### Cosa se ne ricava

1. La **forma** si raddrizza: con un braccio più lungo la barca del gioco comincia a sventare verso i 9 nodi come in Day, e il salto 9 → 12 nodi diventa simile a Binns. Il **livello** resta basso del 3-9% a tutti i venti.
2. La **virata** non migliora con la velocità: la barca vera guadagna 1,48 m nella prima metà (porta l'abbrivio verso il vento), quella del gioco 0,3 m con tutte le varianti. È un'altra cosa (abbrivio nella orzata), non la vela.
3. Il braccio `zCE` manca di fonte: per la fermata 2 servirebbero le misure dell'armo (altezza del boma, lunghezza dell'inferitura, profondità della deriva) da una fonte usabile.

### Proposta

Secondo la regola del giro della lista (Ale, 23 nov): **la voce 81 non passa e va fra quelle da rivedere alla fine.** Il motore non cambia. Da riprendere, se Ale vuole: (a) cercare le misure dell'armo per dare una fonte a `zCE`; (b) guardare a parte l'abbrivio nella prima metà della virata.

## Ricerca del braccio (25 novembre 2026, via di Ale: «si cerca il braccio della vela»; motore intatto)

**Correzione:** più sopra, e ad Ale in chat, c'è scritto che `zCE` non ha fonte. È inesatto: Day (altezza in frazione dell'inferitura) e l'inferitura c'erano già il 23 ottobre (`archivio/PROPOSTA-CENTRO-VELICO-1B.md`, 2,5-2,8 m). Mancavano le misure dell'armo e della deriva: stanno nei disegni di misura della classe (`HANDBOOK_2025.pdf`, già sul PC di Ale: F38 e F119).

| Pezzo | Valore | Da dove |
|---|---|---|
| Attacco del boma sopra il piede dell'albero | 0,945 m ± 5 mm | F119, disegno a pag. 35 |
| Inferitura | 5,13 m massimo (5,12 in F120) | F119 pag. 35; F120 tab. 1 |
| Centro velico sopra il boma | 36,4% dell'inferitura, 32% svergolata a 15 nodi | Day, F17 §2.2 e eq. 4 |
| Controllo: baricentro della vela dalle larghezze del disegno | 36,2% | conto nostro su F119 |
| Deriva sotto la chiglia | 680 mm lungo il bordo inclinato, circa 0,63 m in verticale (angolo stimato su un disegno non in scala) | F119 pag. 34 |
| Immersione della carena | circa 0,094 m (conto nostro da Day, tab. 2) | F17 |
| Piede dell'albero rispetto all'acqua | **senza fonte**: da 0,09 m sotto a 0 m | ipotesi; il fondo del pozzo sta vicino alla chiglia |
| Centro della spinta della deriva | 43% dell'immersione totale, 0,31-0,34 m sotto l'acqua | Day, F17 (Keuning e Vermeulen) |

- **Centro velico sopra l'acqua: 2,7-2,8 m** (2,5-2,6 svergolata). Conferma il conto del 23 ottobre.
- **Braccio della coppia sbandante, fino al centro della deriva: 3,0-3,15 m** (2,8-2,9 svergolata). Il motore usa un braccio solo (`zCE`, 2,0) contro il peso del timoniere, quindi il numero da confrontare dovrebbe essere questo; che Day lo conti così è una deduzione nostra, il testo non lo dice in modo esplicito.

**Banco** (stesso di novembre, 8 varianti, ripetute due righe vecchie per controllo: uguali entro 1 punto). Attenzione: 0,21 è ORC **senza** timoniere; Day aggiunge il timoniere a parte (circa 0,07, conto del 16 ottobre), quindi il valore coerente con Day è circa 0,27.

| Variante | Day 6 / 10 / 15 nodi | Binns 9 nodi, 42°-60° | Binns 12 nodi, 42°-60° | Timoniere fuori a 9 nodi |
|---|---|---|---|---|
| oggi | −16 / −10 / +6% | −15 −12 −14 −15 | −2 −2 −2 −1 0 | 58% |
| braccio 3,05, il resto com'è | −16 / −10 / −3% | −16 −12 −14 −15 | **−7 −8 −9 −9 −8** | 90% |
| braccio 2,85, il resto com'è | −16 / −10 / −2% | −16 −12 −14 −15 | −5 −7 −7 −8 −7 | 84% |
| vela 0,27, braccio 3,05 (le due cose con fonte) | −10 / −6 / −1% | −12 −7 −10 −11 | −3 −5 −5 −6 −6 | 90% |
| vela 0,21, braccio 3,05 | −4 / −2 / +1% | −8 −3 −7 −9 | 0 −2 −3 −3 −3 | 89% |
| vela 0,21, braccio 2,85 | −4 / −1 / +4% | −8 −3 −7 −9 | +1 0 −1 −1 −1 | 83% |

**Contro i criteri scritti prima:** con le due cose che hanno fonte (vela 0,27, braccio 3,05) B4 passa; **B1 (−10%), B2 e B3 no**. Con 0,21 passano B1, B3 e B4, **B2 no**, e 0,21 non conta il timoniere. B5 e B6 rimisurati in novembre solo a braccio 3,2: non passavano. B7 non rimisurato.

**Cosa se ne ricava:** il braccio ora ha una fonte (salvo il piede dell'albero), ma **col poco vento non cambia la velocità** (−16% con 6 nodi, uguale a oggi): sotto i 10 nodi il timoniere non è ancora al limite. Da solo peggiora i 12 nodi. **La 81 non si risolve con il braccio.**

## Seconda ricerca (25 novembre 2026, risposta di una ricerca sul web portata da Ale, controllata sulle fonti originali; motore intatto)

**La fonte utile è la tesi di Pennanen (F121),** che la ricerca citava senza i numeri: stanno nelle figure, non nel testo.
- **Centro velico: 2,68 m sopra l'acqua** (fig. 7, disegno quotato, boma a 0,60 m sulla coperta; stimato con Hazen, 39% della linea dal boma alla penna). Cade la parte «senza fonte» sul piede dell'albero. Con la spinta della deriva al 45% della profondità (F121 §2.6.3; 43% in Day) il **braccio è circa 3,0 m**.
- **Terzo confronto col poco vento, vento vero a 45° (calcolato):** 2 nodi di barca con 3,28 di vento, 3 con 4,94, 4 con 6,91, 5 con 10,5 (fig. 23, 25, 27, 29). Coincide con la misura di F109 (3,2 nodi: 1,05 m/s = 2,04 nodi). **Limiti:** portanza della vela (Hazen) più alta di Day e nessuna resistenza del timoniere, quindi ottimista; l'autore dice che i valori assoluti della vela contano poco per lui.
- **Resistenza totale in acqua (tesi / gioco, N):** 9,5 / 9,8, 21,7 / 23,2, 42,7 / 47,9, 91,5 / 99,5. La CFD della tesi è 4-6% sotto la vasca fra 3 e 5 nodi: **l'acqua nel gioco va bene** (circa 0-7% in più).
- **Spinta della vela alla stessa velocità (N):** 9,5 / **5,4**, 21,7 / **12,4**, 42,7 / **28,9**, 91,5 / 87,6. **Il difetto è la spinta della vela, e solo col poco vento.** Alla velocità giusta il vento apparente è a circa 27,7°, dove il gioco taglia la portanza (rampa fra 22° e 29°, `luffA0` 22, `luffW` 7, senza fonte): 81% invece di 100%. La tabella ORC usata da Day dà CL 1,35 a 28° e 1,16 a 12°.

**Perché a ottobre la rampa sembrava esclusa:** provata da sola, con la barca lenta il vento apparente sta a 29° e la rampa non si vede. Tolto il freno della vela, la barca accelera, l'apparente stringe e la rampa la ferma. Le due cose si nascondono a vicenda.

**Banco** (esplorazione, conti senza numeri a caso; `banco_pennanen.js`, `banco81.js`; 15 e 5 scelti da noi, 18 e 7 danno lo stesso). Variante **R** = `luffA0` 15, `minBoom` 5, vela 0,27, braccio 3,0.

| | Oggi | Vela 0,27, braccio 3,0 | Variante R |
|---|---|---|---|
| Tesi 2 / 3 / 4 / 5 nodi | −11 / −12 / −12 / −5% | −8 / −8 / −7 / −2% | **0 / −3 / −5 / −2%** |
| B1, Day 6 nodi (−5%) | −16% | −10% | −9% no |
| B2, Binns 9 (±5%) | −15 −12 −14 −15 | −12 −7 −10 −11 | −6 −7 −10 −11 no |
| B3, Binns 12 (±3%) | −2 … 0 | −3 … −6 | −3 … −5 no |
| B4, Day 15 nodi (≤ +6%) | +6% | −1% | 0% passa |
| B5, 3,2 nodi a 45° contro 1,05 m/s (−8%) | 0,88 (−16%) | non misurato | 0,96 (−8,6%) no per poco |
| B6, virata 10 s (−30%) | −1,74 m | non misurato | **−1,14 m (−34%) passa** |
| B7, poppa e lasco (0,03 nodi) | — | non misurato | no (12 nodi: 180° −0,11, 90° +0,21) |
| B8, una costante al massimo, con fonte | — | — | no (4 costanti; due con fonte, la rampa con fonte sul principio ma non sul numero) |

**Cosa se ne ricava:** il difetto ha una spiegazione fisica con fonte (vela che a 28° non porta tutto) e la virata col poco vento migliora da sola; restano **circa −6/−11% a 9 nodi oltre i 46°**, senza causa, e la prova di ottobre va corretta. Non è un limite da chiudere, ma nemmeno una soluzione: serve una proposta nuova.

**Errori della ricerca sul web** (da non riportare): «la regressione Delft può rendere il modello troppo lento» è al contrario (Delft sottostima la resistenza, e il gioco usa la vasca); CL 1,36 e 1,30 attribuiti per certi a turbolento e liscio, mentre in Day l'ordine è ambiguo. Virata rollata +5,3% e +2,8% (Kudo, F122): è un Laser Radial, in acqua, con 2-4 e 4-6 m/s di vento; confermato solo dal riassunto.
