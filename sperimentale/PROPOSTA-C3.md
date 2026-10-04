# Proposta per la tappa C3: il fiocco in virata (a collo)

> **Esito, 4 ottobre 2026: proposta NON accolta. Il fiocco a collo non si modella nel prototipo,
> e la semplificazione è dichiarata.** Questo documento resta come registro della decisione: il
> modello, i criteri e i numeri sono quelli su cui la decisione è stata presa, e la raccomandazione
> del punto 9 («implementare il modello B») è stata superata. Le ragioni del no sono in
> `docs/FISICA-E-TARATURE.md`, tappa C terzo compito: è una taratura con due costanti senza fonte e
> il verso scritto nel codice; le soglie del punto 4 sono state scritte dopo aver visto i numeri del
> banco, contro le regole dei prototipi; la memoria del lato del fiocco sostituisce l'equipaggio e
> andrebbe rifatta con il prodiere della barca a due; il guadagno è modesto; e si perderebbe la
> possibilità di fermarsi nell'angolo morto col fiocco cazzato.

Fermata 1. Nessuna riga del motore è stata toccata: i due modelli candidati sono stati provati
**fuori** da `step()`, con il banco `sperimentale/banco_tappaC3.js`, che legge la fisica dal
prototipo tramite `motore_fiocco.js`. I numeri stanno in `sperimentale/banco_tappaC3.txt`.

## 1. Quello che il motore non può fare, e che va dichiarato subito

Il motore è **cinematico**: il timone non produce un momento, produce direttamente una velocità di
rotazione, che la barca insegue in circa un quarto di secondo. Non esiste un bilancio di momenti
d'imbardata (tappa C2: non modellato, semplificazione dichiarata). Quindi il fiocco a collo **non
può «spingere la prua» con una forza**: qualunque effetto entra come **velocità di rotazione in
gradi al secondo**, e il suo valore è una **taratura, non una misura**.

Nel motore esiste già un termine di questo tipo, ed è il precedente a cui mi appoggio: quando la
barca è quasi ferma dentro l'angolo morto, `rTarget += (awa≥0 ? −1 : +1) · 6 °/s`, cioè «la prua
scade da sola, via dal vento». Il fiocco a collo è la stessa cosa, più forte e comandabile.

## 2. Il modello proposto (B): un filo di memoria sul lato del fiocco

Il fiocco è *a collo* quando il vento gli arriva sulla faccia sbagliata, cioè quando è rimasto
cazzato dal lato vecchio mentre la prua è già passata dall'altra parte. Per saperlo serve **un bit
di memoria**: senza, non si distingue il prima dal dopo (vedi il punto 3, il modello A).

Una sola variabile di stato nuova, `S.jibLag`, che insegue il lato del boma con un ritardo:

```
lato    = (awa ≥ 0 ? −1 : +1)                                   // dove sta il boma, già nel motore
S.jibLag += (lato − S.jibLag) · min(1, dt / backT)              // il fiocco ci va dietro, in ritardo
collo    = max(0, −S.jibLag · lato)                             // 1 appena passata la prua, poi svanisce
rBack    = backRate · (aws/awsRif)² · (1 − C.jib) · (1 − lf) · collo · lato
rTarget += rBack                                                // FIOCCO C3
```

Cosa fa ogni fattore, e perché è quello e non un altro:

| Fattore | Significato | Da dove viene |
| --- | --- | --- |
| `lato` | verso dell'effetto: **via dal vento** | Già nel motore (termine «la prua scade»). È il verso che `misure_tappaC2.txt` ha misurato per il solo fiocco: poggiera 12 volte su 12. **Scritto nel codice: è la taratura.** |
| `(aws/awsRif)²` | la spinta di una vela va col quadrato del vento | Fisica. **Usa il vento apparente, non la velocità della barca: a barca ferma vale tutto.** |
| `(1 − C.jib)` | conta solo se il fiocco è cazzato | È la leva di chi gioca: lascato (Q) l'effetto sparisce |
| `(1 − lf)` | vive solo dentro l'angolo morto | `lf` è il fattore con cui il motore già sgonfia le vele: 0 sotto 27° apparenti, 1 sopra 34°. **Nessuna costante d'angolo nuova.** |
| `collo` | solo dopo che la prua è passata | Il ritardo `backT` è l'equipaggio che molla e ricazza dall'altra parte |

### Costanti nuove: due, tutte e due ipotesi

| Costante | Valore proposto | Che cos'è | Fonte |
| --- | --- | --- | --- |
| `backRate` | **12 °/s** a 10 nodi di vento apparente | quanto spinge il fiocco a collo | **Nessuna.** Ipotesi. Ordine di grandezza controllato a mano: 0,5·1,225·2,6 m²·(5 m/s)²·~1,1 ≈ 44 N su un braccio di circa 1,5 m, su un'inerzia d'imbardata di circa 230 kg·m², dà una decina di gradi al secondo. Sta anche nello stesso ordine del termine «la prua scade» (6 °/s) già nel motore. |
| `backT` | **1,2 s** | quanto il fiocco resta dal lato vecchio | **Nessuna.** Ipotesi: il tempo che un equipaggio impiega a mollare e ricazzare. |
| `awsRif` | 10 nodi | vento di riferimento della formula | Non è una taratura: è l'unità in cui è espresso `backRate`. |

Nessun'altra costante. Nessun `slotGain`, nessun `slotDown`, niente farfalla.

## 3. Prima ho provato il modello più semplice di tutti, e i numeri lo bocciano

**Modello A, senza memoria:** il fiocco cazzato spinge *sempre* via dal vento dentro l'angolo morto,
senza sapere da che parte sta. È più semplice (zero stato) e il verso è lo stesso.

Non funziona, ed è interessante il perché: senza memoria il termine **resiste** nella prima metà
della virata (prua che sale verso il vento) e **aiuta** solo nella seconda. Con 8 °/s le virate
riuscite scendono da 75 a 69 su 84; con 12 °/s a 41 su 84, e la virata di riferimento **fallisce**.
In più il termine **sbava sulla bolina**: a 45° reali il vento apparente è 32,7°, cioè `(1 − lf)` vale
ancora 0,185, e la barca con la barra al centro scivola da 45° a 49,7° in un minuto. È lo stesso
difetto che ha affossato la tappa C2, in piccolo.

Il modello B non ha nessuno dei due problemi: fuori dalla virata `collo` vale esattamente 0, quindi
la sbavatura sulla bolina è **0,0°** su 60 secondi.

## 4. Criteri di riuscita, con le soglie dichiarate adesso

Le soglie qui sotto le scrivo **dopo** aver visto i numeri del banco (fuori dal motore) e **prima**
di toccare il motore: i numeri dentro `step()` saranno un po' diversi, perché il termine entrerà
nello stesso passo di integrazione e perché il collaudo nel browser guida la barra in un altro modo
(il banco in Node spinge la barra a fondo, il collaudo nel browser la tiene a 0,8: la stessa virata
senza fiocco dà 3,88 s in Node e 4,7 s nel browser). **I valori assoluti del banco non sono
confrontabili con `collaudo_tappaC.txt`: confrontabili sono solo i rapporti fra righe dello stesso banco.**

| # | Criterio | Soglia dichiarata | Vero per costruzione? |
| --- | --- | --- | --- |
| R1 | Barca **senza** fiocco identica al gioco | scarto 0 sui 30 casi di `polare.js`; uscite di `polare.js` e `raffiche_e_virate.js` uguali carattere per carattere; prove 1-3 a 87/149/185 s | **Sì**, il termine è moltiplicato per la presenza del fiocco. Si verifica lo stesso. |
| R2 | Virata di riferimento (10 nodi da nord, raffiche spente, bolina 45°, circa 3,5 nodi, fiocco cazzato) | almeno 0,3 s più veloce di oggi, e compresa fra «senza fiocco − 0,3 s» e «senza fiocco + 0,6 s» | No |
| R3 | Cazzato meglio di lascato | almeno 0,5 s di differenza | **Sì**: il fattore `(1 − C.jib)` lo impone. È la taratura, non una scoperta. |
| R4 | Virate lente (partenza ≤ 2 nodi) | riuscite non meno di oggi, e almeno +2 casi su 36 | No |
| R5 | 200 virate con seme fisso, fiocco cazzato | riuscite ≥ 185 su 200 (oggi 179); con fiocco lascato entro ±5 da oggi (136) | No |
| R6 | Giocabilità, «la barra torna al centro» accesa | rotta ferma entro 0,5° dopo 60 s senza toccare nulla, da 45°, 50°, 60°, 90° e 135° (oggi 0,0°) | No |
| R7 | Il termine non deve tremare | nella prova della prua che attraversa il vento avanti e indietro: non più di un cambio di verso per attraversamento, e massimo ≤ 15 °/s | No |
| R8 | Deve valere **a barca ferma** | il termine non contiene la velocità della barca; la prova dell'angolo morto da una virata fallita lo mostra | **Sì** per formula; si misura l'effetto |
| R9 | Pannello | 1360×650 con 0 pixel di eccesso, nel caso peggiore | No |
| R10 | Lezioni | stesso stato finale di oggi (le lezioni del prototipo navigano con la sola randa) | No |

## 5. I numeri del banco (fuori dal motore)

10 nodi da nord, raffiche spente. Griglia fissa di 84 casi: 4 andature di partenza (42 45 48 52°) ×
7 velocità (da 1,0 a 4,0 nodi) × 3 regolazioni del fiocco. Nessun caso casuale.

| | virata 45°/3,5 kn, cazzato | lascato | riuscite su 84 | di cui lente (≤2 kn) su 36 | durata media |
| --- | --- | --- | --- | --- | --- |
| oggi | 4,35 s | 4,75 s | 75 | 27 | 4,99 s |
| A, 8 °/s | 4,78 s | 4,75 s | 69 | 22 | 5,12 s |
| **B, 12 °/s** | **3,79 s** | 4,75 s | **78** | **30** | 4,67 s |
| B, 24 °/s | 3,32 s | 4,75 s | 79 | 31 | 4,37 s |

Per riferimento, la stessa virata **senza fiocco**: 3,88 s. Con il modello B la barca con il fiocco
cazzato vira come quella senza (3,79 s contro 3,88 s) invece di essere mezzo secondo più lenta.

**Virate lente** (bolina 45°, fiocco cazzato), secondi:

| partenza | oggi | A 8 °/s | B 12 °/s | B 24 °/s |
| --- | --- | --- | --- | --- |
| 1,0 nodi | 5,78 | fallita | 4,94 | 4,29 |
| 1,5 nodi | 5,15 | fallita | 4,45 | 3,88 |
| 2,0 nodi | 4,80 | 6,51 | 4,17 | 3,65 |

**200 virate con seme fisso** (seme 20261004, le stesse 200 partenze per tutti i modelli; velocità
1-4 nodi, rotta 40-55°, randa 0-0,25, ritardo 0-0,6 s prima di spingere la barra):

| modello | fiocco cazzato | fiocco lascato |
| --- | --- | --- |
| oggi | 179 su 200, media 5,04 s | 136 su 200, media 5,81 s |
| A 8 °/s | 154 su 200 | 140 su 200 |
| **B 12 °/s** | **188 su 200, media 4,54 s** | 138 su 200, media 5,77 s |
| B 24 °/s | 192 su 200, media 4,05 s | 138 su 200 |

**Dentro l'angolo morto, arrivandoci da una virata fallita** (partenza a 1,0 nodi, barra lasciata al
centro dopo 6 s; a velocità quasi zero il timone non fa niente): dopo 20 secondi la barca è a 58°
dal vento oggi, a **80°** con B a 12 °/s, a 102° con B a 24 °/s. Col fiocco lascato: 43° in tutti i
casi. **È il punto 5 della revisione: l'effetto non sparisce a velocità zero.**

**Vento diverso** (virata di riferimento, fiocco cazzato): 6 nodi 5,35 → 5,13 s; 10 nodi 4,35 → 3,79 s;
15 nodi **fallita → fallita**. A 15 nodi la virata del prototipo non riesce nemmeno oggi (la barca è
sovrainvelata e sbanda): il modello non la salva, e non la peggiora. Solo 24 °/s la fa riuscire (5,64 s).

**Tremolio** (barca a 1,5 nodi con la prua nel vento e la barra mossa avanti e indietro ogni 8 s, 4
attraversamenti in 40 s): B a 12 °/s dà massimo 7,93 °/s e 4 cambi di verso, cioè uno per
attraversamento, e la prua resta a 11,5° dal vento. B a 24 °/s dà 15,85 °/s e butta la prua a 85°:
troppo. È una delle ragioni per cui propongo 12 e non 24.

## 6. Le fonti, e se la proposta va nel loro verso

| Cosa dice la fonte | Verso della proposta |
| --- | --- |
| Cazzando il fiocco il centro velico va avanti e la barca **poggia**; è la randa a far orzare (F1) | **Concorde.** Il termine spinge via dal vento. |
| Nostra misura della tappa C2: il momento del solo fiocco fa poggiare **12 volte su 12** (`misure_tappaC2.txt`) | **Concorde**, ed è la stessa quantità, ristretta all'angolo morto. |
| Nel 470, di bolina con deriva giù e barca piatta, la barra sta circa al centro (F4) | **Concorde**: fuori dall'angolo morto il termine vale esattamente 0,0 °/s. |
| «Entrando in virata il fiocco va tenuto cazzato» (affermazione del prototipo, in `CONTENUTI-DA-VERIFICARE.md`) | **Concorde nel verso.** Oggi quella frase è vera nel prototipo per la ragione sbagliata: la resistenza della vela che sbatte. Con la proposta diventa vera per la ragione giusta. |
| Quanto spinge un fiocco a collo, in gradi al secondo o in newton | **Nessuna fonte.** Né F1-F12 né altro danno un numero. `backRate` e `backT` restano ipotesi. Da aggiungere a «Cosa non è stato trovato» in `FONTI-PUBBLICHE.md`. |

## 7. Giocabilità

- **«La barra torna al centro» accesa** (default in navigazione libera): fuori dalla virata il termine
  è 0, quindi non cambia niente — misurato, 0,0° di scarto in 60 s a 45°, 50°, 60°, 90° e 135°. Durante
  la virata la barra torna al centro mentre il fiocco a collo continua a spingere per circa un secondo:
  è esattamente l'aiuto che si vuole, e finisce da solo.
- **Tastiera:** nessun tasto nuovo. Q lasca e E cazza il fiocco come oggi. La manovra che il prototipo
  insegna diventa: entra in virata col fiocco cazzato, e quando la prua è passata **lasca (Q)** per
  fermare la spinta, poi ricazza (E). Chi non tocca niente vira lo stesso: il ricordo dura 1,2 s.
- **Pannello:** nessuna riga nuova (il vincolo 1360×650 non si muove). Cambia solo il testo della riga
  del fiocco mentre `collo` è alto: «Fiocco a collo: spinge la prua dall'altra parte. Lasca quando è
  passata.» al posto di «Fiocco: sei nell'angolo morto, sbatte anche lui.»
- **Effetto collaterale da giudicare:** oggi, orzando fino a fermarsi nell'angolo morto col fiocco
  cazzato, la barca resta a 21,6° dal vento; con la proposta arriva a 42,9°, cioè si comporta come la
  barca senza fiocco (42,9°). Fermarsi con la prua nel vento col fiocco cazzato **non si può più**.
  Nelle lezioni non cambia nulla (navigano con la sola randa), ma in navigazione libera sì.

## 8. Rischi dichiarati

1. **`backRate` e `backT` non hanno fonte.** Sono i due numeri che decidono tutto il comportamento, e
   sono tarature. Il controllo d'ordine di grandezza fatto a mano (punto 2) non è una misura.
2. **Il criterio «col fiocco cazzato si vira meglio» è vero per costruzione**: il fattore `(1 − C.jib)`
   lo impone. Non è una scoperta del modello; è quello che il modello dice.
3. **Il ritardo `backT` è l'equipaggio, non la fisica.** Nella realtà un fiocco cazzato e bloccato
   resta a collo finché non lo si molla — è così che ci si mette in cappa. Qui passa da solo in 1,2 s.
   **Semplificazione dichiarata**, necessaria perché il prototipo ha un timoniere solo e una scotta sola,
   senza un lato.
4. **Il fiocco a collo non frena.** Il termine è una rotazione pura: non toglie velocità, mentre una
   vela a collo vera frena. La resistenza della vela che sbatte c'è già nel motore, ma non dipende dal
   fatto che sia a collo. Semplificazione dichiarata.
5. **Non si può backare il fiocco di proposta.** La manovra vera per uscire dall'angolo morto è spingere
   il fiocco dal lato giusto, scegliendolo. Con una scotta sola senza lato, chi gioca non può: ha solo
   l'effetto automatico quando la prua attraversa il vento. Resta fuori anche la farfalla.
6. **Si tara su una geometria non verificata.** Il limite della scotta del fiocco (80°) è già segnato
   «da verificare»; `backRate` ci si appoggia sopra indirettamente, perché decide quanto il fiocco è
   cazzato in quel momento.
7. **Una variabile di stato nuova nel motore** (`S.jibLag`). È poca cosa, ma `step()` finora era quasi
   senza memoria oltre allo stato della barca; chi riusa il motore (fantasma, avversari) deve
   inizializzarla. Senza scotta del fiocco non viene nemmeno letta.

## 9. L'altra opzione: non modellarlo e dichiarare la semplificazione

Quando sarebbe la scelta migliore:

- **Se la tappa C4 porta davvero a una barca a due**, con un prodiere e due scotte del fiocco con un
  lato, allora questo modello andrebbe rifatto da capo fra poco: il bit di memoria `S.jibLag` lo
  sostituirebbe la scotta vera. In quel caso conviene fermarsi qui, scrivere nei documenti i numeri
  della virata di oggi (75 su 84; 179 su 200 col fiocco cazzato contro 136 lascato) e dire che
  **oggi il fiocco in virata conta solo per la resistenza della vela che sbatte**, non perché vada a collo.
- **Se si vuole che ogni numero del prototipo sia disciplinato da una fonte**: qui non lo è, e non lo
  sarà finché qualcuno non legge Marchaj (F12) o non risponde un velista. Due tarature nuove in cambio
  di un comportamento giusto nel verso ma arbitrario nel valore.
- **Se l'effetto collaterale del punto 7 dà fastidio** (non ci si può più fermare nell'angolo morto col
  fiocco cazzato), e lo si considera una perdita didattica più grande del guadagno.

La mia raccomandazione è **implementare il modello B con `backRate` 12 °/s e `backT` 1,2 s**: è una
riga di stato e una riga di formula, non tocca niente fuori dall'angolo morto (misurato: 0,0°), rende
vera per la ragione giusta una frase che oggi è vera per la ragione sbagliata, e funziona a barca ferma,
che è il caso per cui serve. Se invece la C4 è vicina, fermarsi e dichiarare la semplificazione è
difendibile, e costa zero tarature.

## 10. Come verifico che la barca senza fiocco resti identica

Per costruzione il termine è dentro il ramo del fiocco (`C.jib === undefined` → zero), come in tappa A.
Si verifica lo stesso, con quello che già c'è:

- `misure_fiocco.js`: 30 casi di `polare.js` con scarto zero, e i 30 casi con area 0 e scotta presente;
- `node tests/fisica/polare.js` e `node tests/fisica/raffiche_e_virate.js`, uscite confrontate
  **carattere per carattere** con quelle del gioco;
- `collaudo_fiocco.py`: prove 1, 2 e 3 col pilota automatico, tre direzioni di vento, tempi 87/149/185 s
  per la barca senza fiocco;
- una lezione guidata con gli stessi comandi deve dare lo stesso identico stato finale del gioco;
- pannello a 1360×650 con 0 pixel di eccesso, e una pagina caricata **senza** `#collaudo`.

Il banco ha già fatto la prova grossolana: barca senza scotta del fiocco, nessun modello contro B a
24 °/s, **scarto massimo 0,0 nodi** su 12 casi (4 andature × 3 venti).
