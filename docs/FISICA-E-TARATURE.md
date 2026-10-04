# Fisica e tarature

Il motore simula una deriva singola da circa 4,2 m con una sola vela (randa) e un timoniere. I valori sono **tarati per essere plausibili**, non ricavati da misure su una barca reale: servono a far imparare comportamenti corretti, non a prevedere prestazioni.

Tutto il motore è nella funzione `step(S, C, E, dt)` di `index.html`: `S` è lo stato della barca, `C` i comandi (`sheet` da 0 a 1, `tiller` da −1 a 1, positivo = barra a dritta), `E` il vento (`twd` direzione di provenienza in gradi, `tws` intensità in m/s). La simulazione avanza a passi di circa 1/240 di secondo.

## Il modello, passo per passo

1. **Vento apparente.** Vettore del vento reale meno vettore della velocità della barca (avanzamento più scarroccio). Se ne ricavano l'angolo `awa` rispetto alla prua (positivo = da dritta) e l'intensità `aws`.
2. **Boma.** La scotta fissa l'angolo massimo del boma, da `minBoom` (14°, anche cazzata a ferro la randa non sta sull'asse) a `maxBoom` (85°). Il vento spinge il boma fino a quel limite, ma mai oltre la direzione del vento stesso.
3. **Forze sulla vela.** Angolo di incidenza α = |awa| − angolo del boma. Portanza `CL(α)`: cresce fino a 1,35 a 20°, poi cala (stallo). Resistenza `CD(α) = 0,06 + 1,15·sin²α + 0,12·CL²`, più una resistenza extra quando la vela sbatte (α < 6°). La pressione è ridotta dallo sbandamento (fattore cos φ). **Angolo morto:** quando il vento apparente scende sotto `luffA0` (27°) l'inferitura si sgonfia e la portanza cala fino ad annullarsi; porta del tutto sopra 34°.
4. **Spinta e forza laterale.** Spinta = L·sin|awa| − D·cos|awa|; forza laterale = L·cos|awa| + D·sin|awa|.
5. **Avanzamento.** Massa 135 kg (barca più timoniere). Resistenza dello scafo `4·u + 12·u² + 0,9·u⁴`, aumentata dallo sbandamento e dalla barra angolata.
6. **Scarroccio.** La deriva oppone una resistenza laterale che cresce col quadrato della velocità: a bassa velocità la barca scivola di più.
7. **Timone.** Velocità di rotazione proporzionale a velocità della barca × seno dell'angolo della pala (fino a 30°). Senza velocità il timone non funziona; all'indietro funziona al contrario. Barca ferma nel vento: la prua scade da sola, lentamente.
8. **Sbandamento.** Momento sbandante = forza laterale × 2 m (altezza del centro velico). Momento raddrizzante = timoniere sporto fuori (75 kg × fino a 1 m) più stabilità di forma dello scafo. Il timoniere si regola da solo con circa 0,9 s di ritardo, per questo le raffiche improvvise fanno sbandare. Oltre 60° la barca scuffia.

## Costanti (`BOAT`)

| Costante | Valore | Significato |
| --- | --- | --- |
| `mass` | 135 kg | Barca più timoniere |
| `sailArea` | 7,0 m² | Superficie della randa |
| `hullK2`, `hullK4` | 12, 0,9 | Resistenza dello scafo |
| `rudderDragK` | 45 | Resistenza della barra angolata |
| `foilK` | 520 | Resistenza laterale della deriva |
| `minBoom`, `maxBoom` | 14°, 85° | Escursione del boma |
| `luffA0`, `luffW` | 27°, 7° | Vento apparente sotto cui la vela si sgonfia, e ampiezza della transizione |
| `turnLen` | 1,05 m | Lunghezza efficace per la rotazione |
| `maxRudder` | 30° | Angolo massimo della pala |
| `zCE` | 2,0 m | Altezza del centro velico |
| `sailorMass`, `hikeArm` | 75 kg, 1,0 m | Timoniere e braccio massimo fuori bordo |
| `formK` | 400 Nm | Stabilità di forma |
| `rollI`, `rollDamp` | 260, 520 | Inerzia e smorzamento del rollio |
| `capsizeAt` | 60° | Soglia di scuffia |

Altre costanti nel codice di gioco: colpo della strambata con vela aperta `GYBE_KICK = 260 °/s`, scalato con (vento / 15 nodi)^1,6 e con una variazione casuale tra −15% e +25%; soglia della strambata «violenta»: boma aperto oltre 45°.

## Risultati delle tarature

Misurati con i collaudi in `tests/`.

**Velocità con vento di 10 nodi** (vela regolata al meglio):

| Angolo dal vento | 30° | 35° | 40° | 45° | 48° | 60° | 90° | 110° | 135° | 150° | 180° |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nodi | 0 | 1,1 | 2,3 | 3,4 | 4,0 | 4,6 | 5,2 | 5,0 | 4,2 | 3,8 | 3,5 |

Sotto circa 33° la barca non avanza, tra 33° e 40° arranca: l'angolo morto effettivo di questa deriva è di circa 35–40° per lato, coerente con le dispense di vela (circa 35° per lato per le derive, 45° come convenzione didattica). La velocità utile controvento è massima intorno a 45–48°.

**Virata** (partendo di bolina): a 3,9 nodi riesce in circa 4 secondi; a 1,9 nodi fallisce vicino alla prua al vento; quasi ferma, fallisce e la barca arretra.

**Raffica improvvisa** da 10 nodi, di bolina con vela regolata:

| Raffica | Senza reagire | Lascando entro mezzo secondo |
| --- | --- | --- |
| 16 nodi | sbandamento 27° | 16° |
| 18 nodi | 41° | 23° |
| 20 nodi | 55° | 31° |

**Strambata con la vela tutta aperta:** 6 nodi, circa 19° di sbandamento; 10 nodi, tra 39° e 58°; 15 nodi, scuffia sempre.

**Regate** (percorso a bastone, boa a 140 m): 3,5–6 minuti; avversari al via di solito entro 12 secondi dallo zero con 3 o 5 minuti di preparazione (in circa una partenza su dieci di più: difetto noto). Dalla 0.14, con il giro di boa vero, gli avversari principianti impiegano in media circa 150 s di bolina e 93 s di poppa con 10 nodi.

## Prototipo del fiocco (`sperimentale/fiocco.html`, non nel gioco)

Prova sperimentale di una seconda vela, in vista di una futura deriva a due. **Non è una versione del gioco**, e il motore di `index.html` non cambia: verificato che, per una barca senza scotta del fiocco, polare, virate e raffiche restano identiche carattere per carattere. Le costanti sono ipotesi, elencate in `CONTENUTI-DA-VERIFICARE.md`.

- **Tappa A — il fiocco come seconda superficie portante.** Stesso vento apparente delle due vele, area 2,6 m² (37% della randa), scotta propria (10°–80°), centro velico a 1,6 m. Spinta e forza laterale si sommano; il momento sbandante diventa `forza_randa · 2,0 m + forza_fiocco · 1,6 m`.
- **Tappa B — l'interazione, nella sola forma dell'ombreggiamento.** Alle andature larghe la randa copre il fiocco: la pressione del fiocco è ridotta secondo un fattore «fessura» che vale 1 sotto `slotA0` di vento apparente e 0 sopra `slotA0 + slotW`. (Una prima taratura, 40° e 100°, metteva l'ombra già al traverso: le fonti parlano di fiocco coperto alle andature larghe e in poppa, non al traverso; la seconda, 85° e 135° con una perdita massima del 70%, è stata ritarata nella tappa C, sotto.) **Semplificazione dichiarata: la copertura dipende solo dall'angolo del vento apparente, non da come sono regolate le due vele.** Nella realtà una randa cazzata a ferro copre il fiocco meno di una tutta lascata, a parità di andatura.
- **Tappa C, primo compito — coerenza fra quello che si vede e la forza del fiocco coperto.** In tappa B il pannello diceva «qui non si regola (coperto dalla randa)» mentre il fiocco dava ancora dal 10% al 19% della spinta: una vela che sbatte non tira. Taratura nuova: `slotA0` da 85° a **95°**, `slotW` da 50° a **12°**, `slotShade` da 0,70 a **1,00**. Quindi niente ombra fino a 95° apparenti, ombra totale da **107°**, che non è un numero scelto: è l'angolo oltre il quale `jibRange()` non trova più una posizione con i filetti dritti (`maxJib` 80° più la finestra di incidenza 8°–27°). I due confini coincidono per costruzione. Il 95° viene dall'unica fonte quantitativa (F4): nel 470 il fiocco aggiunge spinta fino a circa 100° apparenti. A 10 nodi, 95° apparenti sono circa **126° reali** e 107° apparenti circa **132° reali**.
- **Tappa C, secondo compito — nessun momento di imbardata dovuto alle vele: semplificazione dichiarata.** Deciso il 4 ottobre 2026 di **non** modellarlo, dopo averne misurato l'effetto fuori dal motore.
  - **Cosa fa il motore.** La barca gira solo col timone: `step()` non calcola un momento di imbardata, ricava dalla barra una *velocità di rotazione voluta* e ci va dietro in circa un quarto di secondo. L'unica eccezione è la prua che scade da sola quando la barca è quasi ferma dentro l'angolo morto.
  - **Cosa dicono le fonti.** Con randa e fiocco regolati, deriva giù e barca piatta, la barra sta circa al centro: scafo e vele sono quasi in equilibrio. Sbandando, la barca tende a **orzare**, e la tendenza cresce con lo sbandamento (F4). Cazzando la randa il centro velico arretra e la barca orza di più; lascando, il contrario (F1).
  - **Cosa chi gioca non sente.** Il fiocco cazzato che fa poggiare; la randa cazzata che fa orzare; la barca che orza da sola sbandando, e che in raffica tira verso il vento. Sono effetti veri e didatticamente importanti: restano fuori dal prototipo.
  - **Perché il solo fiocco è stato scartato.** Si era proposto di modellare il contributo del **solo** fiocco, lasciando alla randa l'equilibrio già implicito nel motore, così che la barca senza fiocco restasse identica per costruzione. Misurato fuori dal motore (`sperimentale/misure_tappaC2.txt`), quel modello dà una barca **sempre poggiera**: su 12 casi (6, 10 e 14 nodi × 45°, 70°, 90° e 110° reali) il momento del fiocco fa poggiare **12 volte su 12**, e il termine che dovrebbe far orzare con lo sbandamento vale dal 3% al 23% dell'altro, senza mai ribaltarlo. È il contrario di quello che dice la fonte. Emulando quel momento con la barra libera, a 10 nodi, la barca partita di bolina a 45° passa a **75° dopo 10 secondi** e a **124° dopo 60**, superando i 60° dal vento in **5,9 s**: circa 3 gradi al secondo di scarto con la barra al centro, cioè ingiocabile. Il momento di imbardata riguarda **tutta la barca**, non il solo fiocco, e non si può aggiungere a metà.
  - Il termine che farà girare la prua col **fiocco a collo** è un'altra cosa, e starà nel terzo compito della tappa C: dovrà funzionare anche a barca ferma, dove questo valeva zero.
- **Tappa C, terzo compito — il fiocco a collo in virata non è modellato: semplificazione dichiarata.** Deciso il 4 ottobre 2026, dopo averne provato due modelli fuori dal motore.
  - **Cosa fa il motore oggi.** In virata il fiocco **non va mai a collo**: `step()` mette sempre le due vele sottovento, e l'unico effetto del fiocco sulla virata è la **resistenza della vela che sbatte**, già nel modello della randa. Nell'angolo morto il fiocco non dà forza laterale. Quindi la frase «entrando in virata il fiocco va tenuto cazzato» è vera nel prototipo, ma per la ragione sbagliata.
  - **Com'è la virata oggi** (banco `sperimentale/banco_tappaC3.js`, 10 nodi da nord, raffiche spente, partenza di bolina a 45° con circa 3,5 nodi): fiocco cazzato **4,35 s**, fiocco tutto lascato **4,75 s**, senza fiocco **3,88 s**. Su una griglia fissa di 84 casi (4 andature × 7 velocità × 3 regolazioni) riescono **75 virate su 84**; su 200 tentativi con seme fisso, **179 su 200** col fiocco cazzato contro **136 su 200** col fiocco lascato. **Attenzione: i valori assoluti del banco non sono confrontabili con quelli del browser** (`collaudo_tappaC.txt` dà 4,7 s senza fiocco perché tiene la barra a 0,8 invece di spingerla a fondo): confrontabili sono solo le righe dello stesso banco fra loro.
  - **Il modello scartato, pronto se un giorno servisse** (`sperimentale/PROPOSTA-C3.md`). Una variabile di stato, il lato del fiocco che insegue quello del boma con un ritardo `backT`; finché è rimasto indietro, il fiocco è a collo e aggiunge una velocità di rotazione `backRate · (vento apparente / 10 nodi)² · (1 − scotta del fiocco) · (1 − fattore di sgonfiamento)`, nel verso che allontana la prua dal vento. Valori provati: `backRate` 12 °/s, `backT` 1,2 s. Fuori dall'angolo morto vale esattamente zero (0,0° di scarto in 60 s con la barra al centro), e funziona anche a barca ferma.
  - **Perché è stato scartato.** (1) In un motore cinematico l'effetto è una **taratura**: due costanti senza nessuna fonte e il verso scritto nel codice, quindi il criterio «col fiocco cazzato si vira meglio» è vero per costruzione. (2) Le soglie dei criteri sono state scritte **dopo** aver visto i numeri del banco, contro la regola dei prototipi che le vuole dichiarate prima. (3) La memoria del lato del fiocco è un **sostituto dell'equipaggio**: con il prodiere e le due scotte della barca a due (tappa C4) andrebbe rifatta da capo. (4) Il guadagno è **modesto**: da 75 a 78 virate su 84, da 179 a 188 su 200 col fiocco cazzato, e col lascato da 136 a 138. (5) Cambia un comportamento in navigazione libera: col fiocco cazzato **non ci si potrebbe più fermare nell'angolo morto** (la barca passa da 21,6° a 42,9° dal vento, come se il fiocco non ci fosse).
  - Un modello più semplice, senza memoria del lato, era stato provato per primo ed è peggio di non fare niente: resiste nella prima metà della virata e le riuscite scendono da 75 a 69 su 84.
- **Tappa C, quarto compito — la barca a due non è modellata: sovrainvelamento dichiarato.** Deciso il 4 ottobre 2026 di **non** cambiare massa e coppia raddrizzante del prototipo. Il confronto proposto (quattro configurazioni, da 135 a 250 kg) **non è stato eseguito**: le ragioni si vedono già dai numeri che abbiamo, e due delle tre non riguardano la stabilità. Proposta completa e criteri in `sperimentale/PROPOSTA-C4.md`.
  - **Il problema.** Il prototipo ha lo scafo e il timoniere del gioco (135 kg in tutto, un velista da 75 kg) con il 37% di vela in più: una raffica da 20 nodi fa scuffiare e a 15 nodi la virata non riesce.
  - **Primo motivo: senza trapezio la barca a due sarebbe meno stabile di questa.** Conto aritmetico sulle costanti attuali (`sailorMass·g·hikeArm·cos φ + formK·sin 2φ/2`): la coppia raddrizzante del prototipo vale **83,7 kgf·m** al massimo, che cade a 22,6° di sbandamento. La fonte (F4) dà a una deriva a due **circa 60 kgf·m senza trapezio** e **circa 220 con il trapezio**, con il massimo a circa 25°. Quindi il nostro timoniere singolo, sporto a 1 m, è già **più** stabile di due persone sedute in banda; l'unica configurazione che risolve davvero il sovrainvelamento è quella **col trapezio**, che per il livello 2 sarebbe una **seconda novità principale** (vedi `VISIONE-LIVELLI-E-CARRIERA.md`: una per livello) e un meccanismo nuovo, non una taratura. Nota buona: la **forma** della nostra curva è già coerente con la fonte (massimo a 22,6° contro circa 25°); è solo il valore che differisce.
  - **Secondo motivo: nel motore la massa non entra nella resistenza dello scafo.** La resistenza è `4u + 12u² + 0,9u⁴`, senza dislocamento: la massa agisce solo sull'accelerazione. A regime una barca da 250 kg andrebbe come una da 135, e anzi **più veloce**, perché sbanda meno e le vele prendono più vento (`cos φ`) e lo scafo frena meno (`heelDrag`). Una barca più pesante che va più forte è sbagliata; per ritarare `hullK2` e `hullK4` **non c'è fonte** (polari pubbliche di derive non risultano, F10 non è stata letta).
  - **Terzo motivo: il peso dell'equipaggio dovrebbe diventare un'azione del prodiere**, non l'automatismo da 0,9 s che c'è oggi. È il contenuto della lezione 2.5 «Raffiche in due»: tocca motore e pannello, non quattro costanti.
  - **Conseguenza.** La barca a due non si approssima cambiando costanti: si costruisce in una volta — massa, resistenza dello scafo, peso dell'equipaggio come comando, trapezio e pannello — quando ci sarà una fonte per la resistenza. Fino a lì il prototipo resta sovrainvelato, e il livello 2 va giocato con vento da leggero a medio.
  - **Il timone del motore non è coerente con la fonte, e non è stato cambiato.** Conto a 6 nodi, gli stessi della fonte: la resistenza totale dello scafo del motore vale **21,2 kgf** contro i **19 kgf** della fonte (vicina); la resistenza del timone a 15° vale **2,9 kgf** contro i **12 kgf** della fonte, e il motore arriva a **10,9 kgf** solo vicino a **30°**. Quindi il prezzo è dell'ordine di grandezza giusto, ma all'angolo sbagliato. Quello che non si compensa: **nella pala del motore non c'è stallo.** La velocità di rotazione cresce con il seno dell'angolo fino a 30°, così portare la barra da 15° a 30° fa girare **1,93 volte più in fretta**, e barra a fondo è **sempre** la scelta migliore per girare. Nella realtà oltre circa 15° la pala stalla, si perde autorità e resta solo la resistenza: è una cosa che si insegna e che nel gioco oggi non si sente. Resta una calibrazione futura, con due avvertenze: toccare il timone cambia **tutte** le virate e tutti i tempi delle prove e delle fasce (è una modifica al gioco, non al prototipo), e la via più piccola non è abbassare `maxRudder` ma far **calare** la velocità di rotazione oltre i 15°, così la barra a fondo resta possibile e diventa un errore.
- **La lettura del fiocco non ha memoria.** Il messaggio del pannello dipende solo dal fatto che esista una posizione della scotta con i filetti dritti (`jibRange`), qualunque sia la causa che la toglie: randa che copre oppure scotta già al massimo. Esiste da 31° a **107°** di vento apparente, ed è stretta (meno di 10°) da 98° in su. **Dalla tappa C i filetti del fiocco sbattono per copertura esattamente dove quella posizione non esiste più, cioè da 108°**: `jibShadedAt` non ha più una soglia propria (era metà della pressione perdibile, 111°, e con la rampa stretta sarebbe scesa a 101°, facendo dire «sbatte» dove il pannello dice «Fiocco regolato»). Strumento e messaggio non possono più contraddirsi. Una prima versione usava un'isteresi di 4°, ed è stata tolta: metteva una banda di incertezza proprio sul punto di lavoro del gran lasco, e la lettura finiva per dipendere da come ci si era arrivati.
- **Dove il fiocco non si regola il pannello lo dice**, invece di dare un consiglio inutile: «qui non si regola (coperto dalla randa o scotta al massimo); nella realtà si porta dal lato opposto: non ancora nel gioco». La manovra a farfalla **non è modellata**.
- **Nelle lezioni il prototipo naviga con la sola randa.** I testi delle lezioni parlano di «la vela», e il pannello delle lezioni ha margine zero a 1360×650. Verificato che una lezione guidata con gli stessi comandi dà lo stesso identico stato finale del gioco.
- **Non c'è**, per ora, l'effetto opposto: l'upwash della randa sul fiocco (la randa induce un flusso ascendente che fa rendere di più il fiocco di bolina) e il downwash del fiocco sulla randa. Attenzione: la spiegazione corretta è l'upwash, **non** l'accelerazione «Venturi» dell'aria nella fessura, che le fonti indicano come sbagliata. Di conseguenza il fiocco **non migliora la bolina**: la velocità utile controvento resta migliore a 50° invece dei 48° della barca a una vela.
- **La barca del prototipo è sovrainvelata:** stessa deriva del gioco, stesso timoniere da 75 kg, il 37% di vela in più. Una raffica da 10 a 20 nodi senza reagire fa scuffiare, dove con la sola randa si fermava a 55°. **Nessuna di queste misure calibra la futura barca a due.**

## Semplificazioni dichiarate

- Nessuna planata: con vento fresco la barca è più lenta di una deriva vera.
- Una sola vela, niente fiocco.
- Timoniere automatico: nella realtà gestire il peso è una parte importante della conduzione.
- Niente onde né corrente (salvo i piccoli disturbi di rotta nell'esercizio della lezione 2).
- Raddrizzamento con un pulsante, in 3 secondi.
- Raffiche come chiazze che viaggiano col vento, senza la struttura reale del vento sull'acqua.
- Il fiocco non va mai a collo: in virata conta solo per la resistenza della vela che sbatte (tappa C, terzo compito).
- Nessuna tendenza orziera nella navigazione normale (c'è solo nell'esercizio di rotta): né dalla randa, né dal fiocco, né dallo sbandamento. Vale anche per il prototipo del fiocco (tappa C, secondo compito).

## Da tenere presente

- **Unità:** `S.r` in gradi/s, `S.heelRate` in **radianti/s**. Ogni impulso di sbandamento va convertito con `D2R`.
- Angolo morto: nel gioco il cerchio delle andature lo disegna fino a 40° per lato, i testi citano la convenzione didattica di 45°, il motore lo fa sentire tra 33° e 40°. Se si cambia, vanno allineati motore, cerchio, lezioni 1-3 e 5, glossario e avversari.

## Stato finale del prototipo del fiocco

Riassunto in parole semplici, al 4 ottobre 2026, con le tappe A, B e C chiuse. Il prototipo vive in `sperimentale/fiocco.html` e **non è il gioco**: `index.html` non è stato toccato.

### Cosa fa

- **Il fiocco è una seconda vela vera**, con la sua scotta (tasti Q ed E), i suoi filetti e il suo disegno. Spinge e sbanda insieme alla randa, e sbanda un po' meno di lei perché è più bassa.
- **Alle andature larghe la randa gli toglie il vento.** Fino a 95° di vento apparente il fiocco lavora pieno; fra 95° e 107° perde pressione; da 107° non spinge più del tutto.
- **Il pannello dice cosa fare, e dove non c'è niente da fare lo ammette.** Se esiste una posizione della scotta con i filetti dritti, il pannello dice se cazzare o lascare; se è una posizione stretta, lo dice; se non esiste (oltre 107° apparenti, o nell'angolo morto) dice che lì il fiocco non si regola, invece di dare un consiglio inutile. Strumento e messaggio non possono contraddirsi: la forza del fiocco si annulla esattamente dove il pannello dice che non si regola.
- **La barca senza fiocco è rimasta quella del gioco**, verificato carattere per carattere a ogni tappa.

### Cosa non fa, e perché

| Cosa manca | Perché | Dove sta il dubbio |
| --- | --- | --- |
| **Il momento di imbardata dovuto alle vele** (randa cazzata che fa orzare, fiocco cazzato che fa poggiare, barca sbandata che orza da sola) | Il motore gira solo col timone. Modellare il **solo** fiocco dà una barca sempre poggiera, il contrario di quello che dice la fonte, e ingiocabile: circa 3 °/s di scarto con la barra al centro. Il momento riguarda tutta la barca e non si aggiunge a metà | Tappa C, secondo compito. Fonte F4, una sola barca: le due affermazioni su cui si regge la decisione sono in `CONTENUTI-DA-VERIFICARE.md`, da far giudicare a una persona esperta |
| **Il fiocco a collo in virata** | In un motore cinematico sarebbe una taratura: due costanti senza fonte e il verso scritto nel codice, quindi «col fiocco cazzato si vira meglio» sarebbe vero per costruzione. Il meccanismo sostituisce l'equipaggio e andrebbe rifatto col prodiere. Guadagno misurato modesto: da 75 a 78 virate riuscite su 84 | Tappa C, terzo compito. Nessuna fonte dice quanto spinge un fiocco a collo, né in gradi al secondo né in newton |
| **Il fiocco a farfalla** (dal lato opposto alla randa, in poppa) | È la manovra vera per far lavorare il fiocco in poppa, spesso con un'asta. Non modellata: il pannello lo dice a chi gioca | Da modellare più avanti. Da verificare da quale andatura serve e se sulle derive a due si usa l'asta |
| **La massa e il peso dell'equipaggio di una barca a due** | Senza trapezio la barca a due sarebbe **meno** stabile di questa (circa 60 kgf·m contro i nostri 83,7), e col trapezio sarebbe una seconda novità per il livello 2. Inoltre nel motore la massa non entra nella resistenza dello scafo, quindi una barca più pesante andrebbe più veloce, e per ritarare la resistenza non c'è fonte | Tappa C, quarto compito. **Il prototipo resta sovrainvelato:** una raffica da 20 nodi fa scuffiare, a 15 nodi la virata non riesce. Il livello 2 va giocato con vento da leggero a medio |
| **Il peso dell'equipaggio come comando** | Oggi il timoniere si sporge da solo con 0,9 s di ritardo. Nella realtà gestire il peso è una parte importante della conduzione, ed è il contenuto della lezione 2.5 | Tocca motore e pannello, non le costanti: si farà con la barca a due |
| **L'upwash della randa sul fiocco** (il flusso ascendente che fa rendere di più il fiocco di bolina) | Non modellato. Di conseguenza il fiocco non migliora la bolina: l'ottimo resta a 50° invece dei 48° della barca a una vela | Fonte F5. Attenzione: la spiegazione corretta è l'upwash, **non** l'accelerazione «Venturi» nella fessura, che le fonti dicono sbagliata |
| **Lo stallo del timone** | La pala del motore non stalla mai: barra a fondo (30°) fa girare 1,93 volte più in fretta che a 15°, ed è sempre la scelta migliore. La fonte mette lo stallo oltre circa 15° | Una fonte, una barca. Cambiarlo tocca tutte le virate e tutti i tempi del gioco: non è una modifica al prototipo |
| **La planata** | Non c'è nel motore: sopra gli 8 nodi circa le velocità non possono essere realistiche | Fonte F4. Sta al livello 3 |
