# Proposta: la barca nuova nel motore (voce 84, fermata 1)

Scritta il 26 novembre 2026, **prima del via**: niente codice in `js/`. La ricerca è in `PROPOSTA-SESSIONE-BARCA.md` §Esito e `sperimentale/barca-84/` (`INTERVALLI.md`, `RICERCA-K.md`). Il motore pronto è `sperimentale/barca-84/motore84.js`, scritto da `fa_motore84.py` partendo da `js/motore.js`.

## Cosa cambia (modello più semplice che passa le fonti)

| Cosa | Oggi | Proposta | Fonte o ipotesi |
|---|---|---|---|
| Massa barca + timoniere | 135 (75) | 160 (80) | Day §4: 79,5 kg pesati + 80 |
| Area della vela | 7,0 | **7,92** (candidato K) | 7,06 nominale, 7,92 tela (F119 + formula ORC); le fonti non decidono |
| Braccio velico `zCE` | 2,0 | 2,8 | Flay 2,4-2,6, F121 3,0: centro |
| Braccio del timoniere | 1,0 | 0,90 | Taylor 0,87-0,93, Day 0,956 |
| Raddrizzata dello scafo | formula | curva F121 fig. 31 fino a 22,5°, poi retta a 0 a 90° | oltre 22,5° **ipotesi** |
| Vela di bolina | retta fino a 20° | tabella ORC di Day (tab. 1) letta all'incidenza + 9° | il 9° **ipotesi** (appoggio parziale F109) |
| Vela che fileggia | sul vento apparente | sull'incidenza, da 0° a 10° | 0°: Newman e Low 1984 (vele 2D sbattono a incidenza appena negativa); 10°: svergolamento (F109), scelto guardando F109 |
| Resistenza della vela che sbatte | 0,2 | 0,08 | F109 (0,02-0,08) e bandiere F131 |
| Passaggio alla curva vecchia | — | fra 40° e 60° di vento apparente | Flay a 60° |
| Vela piatta e svergolata al limite | no | sì, fino a 0,6 e 0,186, poi svergola fino a 1 | Day §2.3-2.4, §5; la regola del timoniere **ipotesi** |
| Ritardo dell'appiattimento | — | 1,5 s | **ipotesi**; più lento dell'uscita fuori bordo (0,9 s), come l'ordine descritto da Taylor |
| Poppa: resistenza della vela | 1,15 | 10,45 m² di forza | Magnander (F120, F124) + scafo e timoniere |
| Deriva alzata nelle portanti | no | attrito 0,0049 → 0,0026 fra 100° e 140° | qualitativa (dispensa) |
| Resistenza indotta, smorzamento | 0,4 | 0,1 | Day fig. 11 |

## Criteri (scritti prima, invariati) e dove siamo

B1-B7b come in `PROPOSTA-SESSIONE-BARCA.md`. Col candidato J: passano B1, B3-B7b, virata a 16 nodi, raffica, angolo morto; **non passano B2** (−5,7 / −7,3% a 55-60°, dentro l'incertezza delle fonti: `RICERCA-K.md` §1) **e B8** (ipotesi rimaste: il 9°, raddrizzata oltre 22,5°, ritardo dell'appiattimento, ampiezza `w` della vela che fileggia). Si accende sapendolo, oppure non si accende.

## Cosa va rifatto nel gioco se si accende

Misurato sulla copia, prima del via: vedi la tabella «Sul gioco» qui sotto. Da rifare in ogni caso: fasce dei tempi e medaglie (i tempi cambiano), la lezione 6.3 (la barca scuffia da sola 5 volte su 30), le impronte dei collaudi della barca (`polare.js`, `raffiche_e_virate.js`, `impronta1b.js`: cambiano per forza), le soglie che dipendono dalla barca (`collaudo_regola18` Z1). I rivali usano la stessa barca: si guarda la partenza (fuori linea).

## Sul gioco (copia del repo, motore candidato)

Misure del 26 novembre sul clone del repo: due varianti con l'appiattimento a 1,5 s e la vela che sbatte da 2° (`RICERCA-K.md` §7), poi il **candidato K** (7,92, 1,5 s, vela che sbatte da 0° a 10°, §8):

| | oggi | 7,5 m² | 7,9 m² | **K** |
|---|---|---|---|---|
| Day 6 / 10 / 15 nodi (VMG) | −16 / −10 / +6% | −3,6 / −0,4 / +0,6% | −1,8 / −0,3 / +0,5% | −1,8 / −0,3 / +0,5% |
| Binns 9 nodi, 42-60° | −12 … −15% | −1,1 … −7,3% | +0,2 … −5,2% | +0,2 … −5,2% |
| Binns 12 nodi | −2 … 0% | ±0,6% | ±0,7% | ±0,7% |
| 3,2 nodi a 45° (misura) | −15% | +1,2% | +3,6% | +3,6% |
| VMG a 20 nodi | | 3,92 | 3,57 | 3,63 |
| Raffica 10→18 nodi, sbandamento massimo | 52° | 50° | 52° | 52° |
| Stessa raffica che sale in 2 s (`RICERCA-K.md` §14) | 44° | | | 33° |
| Virate misurate di un ILCA 7 (F137: uscita 92%, 80% dopo 7,6 s), `RICERCA-K.md` §15 | 14 nodi 78%, 9,3 s; 18 nodi resta ferma | | | 14 nodi 91%, 7,7 s; **18 nodi resta ferma** |
| Lezioni, 41 passi, 30 semi | | 6.3: 23/25, a mani ferme 5/30; 2.6 e 5.8 1-2 volte | 6.3: 25/25, a mani ferme 5/30; 2.6, 5.8, 6.2 1 volta | 6.3: 21/21, **a mani ferme 9/30**; 6.2 2 volte; 2.6, 5.8 1 volta |
| Tempi del pilota preciso, prove 1-5 (s) | 79 / 124 / 159 / 286 / 302 | 79 / 119 / 137 / 249 / 285 | 79 / 119 / 137 / 248 / 285 | 79 / 119 / 136 / 248 / 285 |
| Medaglie, 30 corse, fasce di oggi | | **tutte OK** (l'oro diventa più facile) | **tutte OK** | **tutte OK** |
| Regola 18, 90 regate | Z4: 2 contatti decisi | Z1 no (per forza), Z4 2: ok | Z1 no, **Z4 0: no** (pochi casi) | Z1 no, Z4 0: no |
| Torneo completo (C1-C11, 27 controlli) | | 26 ok, no solo C11 R7 (uscita lenta già nota sul PC) | uguale | uguale |

## Rischi

- La barca diventa più veloce col poco vento (fino al 15%): i record e le medaglie di prima non sono confrontabili (si azzerano, regola già data da Ale).
- Il timoniere automatico che appiattisce è un aiuto in più che il giocatore non controlla.
- Gli scarti residui (B2) e le ipotesi (B8) restano scritti come limiti noti.
- **Con vento forte (18 nodi) la barca riparte dalla virata molto più piano di quella vera** (oggi e K; `RICERCA-K.md` §15): trovato il 26 novembre dopo questa proposta, da capire prima del via.

## Scelte, col criterio di Ale (26 nov: «mi interessa di più il comportamento simile a quello reale» che il funzionamento di una lezione)

- **Ritardo dell'appiattimento: 1,5 s.** Non per la lezione 6.3, ma per l'ordine descritto da Taylor (la prima risposta alla raffica è uscire di più fuori bordo, la regolazione della vela viene dopo): nel gioco il timoniere esce in 0,9 s, quindi la vela deve appiattirsi più piano. Il numero resta un'ipotesi.
- **Vela che sbatte da 0° a 10°** (prima da 2° a 10°): lo 0° ha ora una fonte (Newman e Low 1984). Con 2° il calo della VMG a 20 nodi della vela grande era in parte un effetto di questa ipotesi.
- **Area: 7,9 consigliata.** Più vicina a più misure vere (Day 6 nodi, Binns 9) ed è l'area con cui Day ha verificato il suo modello; F109 corretto per il vento in testa d'albero chiede anche di più. Contro: la regola scritta prima sceglieva 7,06; a 20 nodi la VMG scende (3,57 contro 3,92), senza una misura per dire quale sia giusta.
- Le lezioni si ritoccano dopo, sulla barca scelta (6.3: scuffia da sola 5 volte su 30).

## Decisione di Ale

Accendere (con B2 e B8 non passati dichiarati) o tenere la barca di oggi come limite noto. Se si accende: il **candidato K** (area 7,92, appiattimento 1,5 s, vela che sbatte da 0° a 10°), già scritto da `fa_motore84.py` in `motore84.js`.
