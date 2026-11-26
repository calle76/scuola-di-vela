# Proposta: l'angolo morto della barca M (voce 90)

Scritta il 26 novembre 2026, notte. Osservazione di Ale: «l'angolo morto mi sembra ristretto rispetto alla barca precedente; nelle derive non è più ampio?». Via di Ale: «ok correggere».

## Il difetto (misurato, 1.3.60)

Prua tenuta, scotta migliore: con 10 nodi a 30° dal vento vero la barca M fa 3,6 nodi (70% della velocità a 45°; la 1.3.58 1,3 nodi, 28%), con il vento apparente a 21°; a 25° 1,4 nodi. **Day (F17 §6.2): l'ILCA di bolina ha il vento apparente fra circa 27° (5 nodi) e 33° (15 nodi)**; sotto, la vela sbatte sul davanti. La causa: nella M la vela smette di portare in base all'incidenza sul boma (0-10°), non più in base al vento apparente; col boma a 9° la vela lavora con 20° di apparente. Il criterio dell'angolo morto della 84 provava solo 0-15° da ferma.

## Modello più semplice

La portanza della tabella ORC della M si moltiplica per un fattore che va da 0 a 1 col vento apparente, fra `a1` e `a1 + 7°` (7° come la barca fino alla 1.3.58). Un solo numero nuovo, `a1`: **taratura** sui criteri qui sotto (Day §6.2 dà il campo dell'apparente di bolina, non il punto esatto in cui la vela sbatte). La resistenza della vela non cambia.

## Criteri (attese nostre, scritte prima di provare)

| | Criterio | Soglia | Da dove |
|---|---|---|---|
| A1 | Stringere troppo costa | a 30° dal vento vero, prua tenuta, velocità al massimo il 40% di quella a 45° (6, 10, 15 nodi) | manuali (qualitativo); la 1.3.58 dava 28-33% |
| A2 | Angolo morto | a 25° sotto 0,5 nodi (era R4 della 1.3.60) | |
| A3 | Apparente di bolina come Day | vento apparente alla VMG migliore fra 26° e 34° con 6, 10, 15 nodi | Day §6.2 (27-33°, ±1° di lettura) |
| A4 | La bolina non peggiora | VMG migliore sulla rotta contro Day (6 / 10 / 15 nodi) e Binns 9 nodi: nessun punto peggiora di più di 1 punto rispetto alla 1.3.60 | criteri B1-B2 della 84 |
| A5 | Il resto | R1 e R3 della 1.3.60 passano; impronte nuove; medaglie, lezioni (pilota veloce, 6.3), «Stare fermi» non peggiorano | |

**Regola di scelta:** `a1` da 14° a 24° a passi di 1°; si sceglie il più basso che passa A1, A2 e A3. Se nessuno passa A1-A4 insieme, ci si ferma e si riporta.

## Esito della scelta (26 nov, notte; copia del motore, `js/` non toccato)

Metro controllato: per la 1.3.60 ridà i numeri del sesto giro (Day −4,0 / −3,2 / −2,8%, Binns 9 nodi −3,5 / −2,9 / −4,1 / −5,0%).

| `a1` | A1 30°/45° (6/10/15 n) | A2 25° | A3 apparente | Day | Binns 9 nodi (42 / 46,5 / 55 / 60°) |
|---|---|---|---|---|---|
| 1.3.60 | 65 / 70 / 59% | 1,66 | 27/27/32 | −4,0 / −3,2 / −2,8 | −3,5 / −2,9 / −4,1 / −5,0 |
| 18 | 50 / 58 / 58% | 1,06 | uguale | uguale | uguale |
| 19 | 45 / 52 / 54% | 0,86 | 27/27/32 | uguale | −4,4 / −2,9 / −4,1 / −5,0 |
| 20 | 40 / 46 / 54% | 0,73 | 27/27/32 | uguale | −6,6 / … |
| 21 | 35 / 39 / 51% | 0,65 | 28/27/32 | −4,5 / −3,4 / −2,8 | −9,7 / … |
| 22 | 30 / 32 / 39% | 0,65 | 29/29/32 | −5,6 / −3,8 / −2,8 | −13,5 / −4,4 / … |
| 24 | 20 / 19 / 19% | 1,03 | 30/30/32 | −8,9 / −5,3 / −2,8 | −23,4 / −9,8 / … |

**Nessun `a1` passa A1-A4 insieme: ci si ferma.** A1 chiede `a1` ≥ 22, che rompe Binns a 42° di rotta (−13,5% contro −3,5%) e Day con 6 nodi. Binns dice che la barca vera, sulla rotta a 42° (prua a circa 36-37°, apparente circa 24-25°), va a 4,65 nodi con 9 nodi di vento: la vela vera porta ancora lì. **A1 (40%) era probabilmente troppo severo** (preso dalla barca della 1.3.58, che era lenta di bolina); non si cambia, si riporta. **A2 non passa con nessun valore** (0,65-1,66 nodi): da capire a parte.

**Per Ale:** (1) `a1` = 19 (stringere a 30° costa il 46-55% invece del 30-41%; Day invariato, Binns a 42° −0,9 punti; A1 e A2 dichiarati); (2) lasciare com'è, dichiarando; (3) cercare prima fonti con la velocità a 30-35° dal vento.

## Decisione di Ale (26 nov): «falla più simile alla realtà possibile»; il valore lo sceglie Claude con questa regola

Ricerca breve (26 nov): nessuna misura dell'ILCA a 30-35°. Unico dato vicino, qualitativo e non sicuramente sull'ILCA: un blog di tecnica (waterspeedapp.com, «Upwind angles and VMG in a dinghy») dà a 40° l'89% della velocità a 45°. Una polare teorica del forum sailingforums.com: l'ILCA non risale più stretto di 30°. **Scelta di Claude (non di Ale): `a1` = 19°**, il valore più severo che lascia Day e Binns entro 1 punto (A4): velocità rispetto a 45° = 45-54% a 30°, 70-82% a 35°, 89-93% a 40° (1.3.60: 59-70 / 80-84 / 91-93%). A1 e A2 restano non passati, dichiarati. Nel gioco (1.3.61) dopo la misura dei rivali della voce 2.
