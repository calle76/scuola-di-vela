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

**Regate** (percorso a bastone, boa a 140 m): 3–5 minuti; avversari al via tra 0,5 e 11 secondi dopo lo zero, con 3 o 5 minuti di preparazione.

## Semplificazioni dichiarate

- Nessuna planata: con vento fresco la barca è più lenta di una deriva vera.
- Una sola vela, niente fiocco.
- Timoniere automatico: nella realtà gestire il peso è una parte importante della conduzione.
- Niente onde né corrente (salvo i piccoli disturbi di rotta nell'esercizio della lezione 2).
- Raddrizzamento con un pulsante, in 3 secondi.
- Raffiche come chiazze che viaggiano col vento, senza la struttura reale del vento sull'acqua.
- Nessuna tendenza orziera nella navigazione normale (c'è solo nell'esercizio di rotta).

## Da tenere presente

- **Unità:** `S.r` in gradi/s, `S.heelRate` in **radianti/s**. Ogni impulso di sbandamento va convertito con `D2R`.
- Angolo morto: nel gioco il cerchio delle andature lo disegna fino a 40° per lato, i testi citano la convenzione didattica di 45°, il motore lo fa sentire tra 33° e 40°. Se si cambia, vanno allineati motore, cerchio, lezioni 1-3 e 5, glossario e avversari.
