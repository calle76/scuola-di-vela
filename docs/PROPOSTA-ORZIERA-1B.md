# Proposta: la barca dell'1b orziera sbandando

Stato: **fermata 1 approvata, scelta 1** (Ale, 23 ottobre 2026: «vai con la scelta 1»); fermata 2 dopo il giro di collaudi di Ale. Punto 2 dell'ordine deciso da Ale prima del congelamento (`PROPOSTA-PALA-DERIVA-1B.md`, in fondo). L'1a resta senza.

## Fonti
- **F4** (Masuyama e Ogihara 2020, `fonti-pdf/sname-jst-2020-05.pdf`, rilette oggi). **La copia c'è**: le «tre precisazioni da ricontrollare» di `FONTI-PUBBLICHE.md` (riga «Momento di imbardata») e `DUBBI-E-RICERCHE.md` §2 sono tutte nel testo:
  1. di bolina, deriva tutta giù e sbandamento zero, centro velico e punto di spinta di scafo e deriva stanno tutti e due circa 0,2 m a prua del centro: barra circa a zero (p. 28, fig. 13);
  2. **eq. 6** (p. 32, galleria del vento con randa e fiocco a 10°, 20° e 30° di sbandamento): `CN = (CN₀ + CX₀·zCE/√A·sin φ)·cos²φ`. In parole: sbandando il centro velico va sottovento e **la spinta della vela, per la sua altezza, per il seno dello sbandamento**, fa orzare. Il calcolo coincide con la misura a 20°; a 30° la misura sta sotto (vela regolata male, dice l'autore);
  3. lo scafo sbandato orza anche da solo, perché la parte bagnata diventa asimmetrica (p. 33, fig. 16-17), **senza un numero**.
- **F38** (manuale di classe, pagina «Rudder and Tiller»): la barca sbandata sottovento diventa molto orziera; poggiare sbandati carica molto pala e barra; prima si raddrizza (sporgendosi o lascando la scotta).

## Il 470 ha due vele, la nostra una (domanda di Ale, 23 ottobre 2026)
- **Dal 470 si prende solo il meccanismo**, che è geometria: sbandando, il punto dove spinge la vela va sottovento di `zCE·sin φ`, e la spinta lì fa girare la barca verso il vento. Con una vela sola è lo stesso conto, anzi più semplice (una spinta, un centro velico). La conferma in galleria del vento F4 l'ha fatta con randa e fiocco: per una vela sola il conto non è stato misurato.
- **I numeri sono tutti della nostra barca:** la spinta della nostra vela da 7 m² (`step()`), l'altezza del suo centro velico (`zCE`), l'inerzia del nostro scafo (`Izz`).
- **Per la nostra barca parla F38** (stessa classe di F37): sbandata sottovento «prende una forte tendenza orziera», e la vela piccola ha l'albero scelto apposta per tenere il timone equilibrato. Solo a parole, senza numeri: conferma il verso e che a barca dritta la barra sta circa al centro (l'ipotesi del gioco di oggi), non la misura.
- **Punto debole:** `zCE` 2,0 m è senza fonte (`FISICA-E-TARATURE.md`) e l'effetto le è proporzionale. Le regole di classe che abbiamo non danno l'altezza dell'albero. Riporto la sensibilità con 1,8 e 2,6 m (circa −10% e +30%).

### Ricerca sull'altezza del centro velico (23 ottobre 2026, dopo il via di Ale alla scelta 1)
- **F17** (Day 2017, già nostra, p. 9 e eq. 4; il suo VPP è proprio per la nostra barca a una vela): centro velico al **36,4% dell'inferitura sopra il boma** (regola ORC con la correzione per la curva della base); con la vela svergolata a 15 nodi scende al 32%. Day mette nel suo VPP anche l'equilibrio d'imbardata, con la barra che lo pareggia: +1% di velocità di bolina rispetto a barra al centro (sez. 6.3).
- **Inferitura 5,13 m**: solo fonti secondarie sul web, due che concordano (banca dati di vele [Good Old Boat](https://goodoldboat.com/saildata/boat/laser/), guida di un negozio [West Coast Sailing](https://westcoastsailing.net/guides-advice/laser-sail-and-rig-sizes-explained)); le regole di classe F37 e il manuale F38 non la danno. Quindi centro velico **1,87 m sopra il boma** (1,64 m svergolata).
- **Altezza del boma sull'acqua: non trovata.** Con una stima di 0,6-0,9 m (bordo libero più snodo del boma, nessuna fonte) il centro velico starebbe a **circa 2,5-2,8 m** sull'acqua, contro i 2,0 m del motore.
- **Conseguenza:** il termine nuovo con `zCE` 2,0 m è probabilmente **il 25-40% più debole** del vero. Non lo cambio solo qui: lo stesso `zCE` fa anche lo sbandamento, e usarne due diversi nella stessa barca non sarebbe coerente. Portare `zCE` a circa 2,6 m in tutta la barca dell'1b cambierebbe sbandamento, bolina e scuffie (già noto: con 2,8 m la bolina a 15 nodi passerebbe da +7% a −1% rispetto a Day, `FISICA-E-TARATURE.md`): passo separato, decide Ale. La sensibilità con 2,6 m resta fra i criteri.

## Modello (solo barca dell'1b, ramo `lv2` di `step()`)
Un termine solo, l'eq. 6 di F4 in forma dimensionale: momento `N = spinta · zCE · sin(sbandamento)`, verso il vento, che entra nella rotazione come `N / Izz`.
- **Nullo a barca dritta per costruzione** (il rischio del 4 ottobre era un momento delle vele non legato allo sbandamento). Sbandata sopravento (sbandamento negativo) la barca poggia: viene dalla stessa formula.
- **Nessuna costante nuova:** `zCE` 2,0 m (già in `BOAT`), `Izz` 200 kg·m² (già in `RUD2`, stima con fascia 130-300: l'effetto va come 1/`Izz`, riporto la sensibilità).
- Vale solo dove vale il timone dell'1b (`u ≥ uMin`, non col boma spinto). Sotto 0,5 m/s la spinta è quasi zero.
- **Lasciati fuori, dichiarati:** lo scafo che orza da solo (F4 non dà numeri: il modello è quindi il minimo dell'effetto); il secondo `cos φ` dell'eq. 6 (il motore riduce la vela inclinata con un `cos` solo, `ch`); la scia della deriva sulla pala, che la nota della 1.0.45 voleva riprendere qui: Day non dà il coefficiente e `yawG` è già una stima, quindi resta a zero.

## Anteprima [banco fuori dal repository, termine aggiunto dopo `step()`, 1a e gioco non toccati]
**Vento costante.** Il timoniere automatico tiene la barca a 4,6-5,0° di sbandamento con ogni vento: il momento è piccolo, la pala lo pareggia con 0,3-0,5°. A barra al centro la prua sale di 0,2-0,7 °/s:

| Barra al centro, scotta ferma | 6 nodi | 10 nodi | 14 nodi |
|---|---|---|---|
| Partenza in bolina (45°), dopo 10 s / 30 s | 42,9 / 39,2° | 41,4 / 36,5° | 40,6 / 35,2° |
| Partenza al traverso (90°), dopo 10 s / 30 s | 86,7 / 80,5° | 84,2 / 74,4° | 81,7 / 69,6° |

(Il 4 ottobre, col momento delle vele non legato allo sbandamento: 3 °/s, ingiocabile.)

**Raffica** (vento +60% per 4 s, dall'equilibrio):

| | sbandamento max | prua, barra al centro | barra per tenere la prua | stallo |
|---|---|---|---|---|
| 10→16 nodi, bolina | 43° | +12,7° | 6,8° | no |
| 10→16 nodi, traverso | 20° | +13,3° | 1,9° | no |
| 14→22 nodi, bolina, scotta ferma | 69° | +17,0° | **35° (a fondo)** | 1,1 s, prua fuori 15,5° |
| 14→22 nodi, bolina, scotta lascata di 0,3 | 40° | | 3,6° | no, prua fuori 0,8° |

È quello che dice F38: sbandati la barca orza forte e la barra da sola non basta, raddrizzando sì. Senza il termine, in tutte le righe, prua ferma e barra a zero.

## Criteri per la fermata 2 (attese nostre; i numeri dell'anteprima li ho già visti, non è una prova alla cieca)
1. **1a identica:** `polare.js`, `raffiche_e_virate.js`, `retromarcia.js`, `angolo_morto.js` carattere per carattere.
2. **Giocabile a vento costante:** barra al centro, 6-14 nodi, bolina e traverso: prua che sale al massimo **1 °/s** in media sui primi 10 s.
3. **Si sente nella raffica:** raffica +60% di 4 s con 10 nodi, barra al centro: prua che sale **almeno 5°** in bolina e al traverso.
4. **Raddrizzare serve (F38):** raffica 14→22 nodi di bolina tenendo la prua col pilota: con la scotta ferma barra oltre 20°; lascando, barra sotto 10°.
5. **Virata dell'1b:** criterio 1 della 1.0.43 su tutti i venti 6-16 nodi (`virata1b.js`).
6. **Avversari e pilota dell'1b** (`misura_scarroccio.py` rifatto per questo, 20 tornei, semi 1-20, 80 regate): non arrivate e boe sbagliate non in aumento; tempo medio del pilota entro +3%; contatti e scuffie riportati.
7. Riportati senza soglia: sensibilità con `Izz` 130 e 300 e con `zCE` 1,8 e 2,6 m (solo nel termine nuovo, lo sbandamento resta quello di oggi); `bolina.js` e `scarroccio1b.js`; `timone2.js`, `salti2.js`, `boma2.js`; nel browser `collaudo_torneo.py --veloce` e `--giocatore`, `collaudo_semaforo.py`, `collaudo_contatto_vero.py`, `collaudo_raddrizzata.py`, `collaudo_timone2.py`.

## Rischi
- **Avversari nelle raffiche:** la loro guida tiene la prua con la barra; se orzano in raffica possono avvicinarsi di più fra loro (contatti, criterio 6).
- **Barra che torna al centro** (aiuto): in raffica la barca orzerà da sola di 5-15°. È fedele, ma chi gioca senza toccare la barra lo vedrà subito.
- **Pala in stallo più spesso con molto vento:** è la cosa voluta (F38), ma cambia i numeri di `timone2.js` e dei salti.
- Le lezioni dell'1b non esistono ancora: il pannello non spiega la cosa. Una riga nel glossario («Orziera») c'è già; la lezione verrà con le lezioni brevi dell'1b.

## Decisione per Ale
1. **Solo l'eq. 6 di F4** (consiglio): nessuna costante nuova, nulla a barca dritta, minimo dell'effetto.
2. Anche lo scafo che orza da solo: servirebbe un numero inventato (F4 non lo dà). Sconsigliato.
3. Non farla: resta il limite dichiarato di oggi.

## Fermata 2 (23 ottobre 2026): versione 1.0.46, non ancora in commit
Fatto come scritto (scelta 1), una riga in `step()`. Numeri completi nel `CHANGELOG.md`, 1.0.46; banco `tests/fisica/orziera1b.js` (`node orziera1b.js k` per la sensibilità).

| Criterio | Esito |
|---|---|
| 1. 1a identica | **ok** (`polare`, `raffiche_e_virate`, `retromarcia`, `angolo_morto`, `bolina` carattere per carattere) |
| 2. Barra al centro, al massimo 1 °/s | **FUORI** solo con 14 nodi al traverso: 1,06 °/s (gli altri 0,23-0,69) |
| 3. Raffica con 10 nodi, almeno 5° | **ok**: 12,9° di bolina, 16,4° al traverso |
| 4. Raddrizzare serve | **ok**: scotta ferma barra a fondo e stallo 0,9 s; lascando 3,7° |
| 5. Virata dell'1b | **FUORI** a 16 nodi: minima 34% contro 35% (era 36%) |
| 6. Regate (80, semi 1-20) | **FUORI** come scritto: non arrivate 0 → 1 (il pilota dei collaudi); boe sbagliate 3 → 1, tempo pilota +0,4%, penalità 289 → 229, scuffie 71 → 73 |
| 7. Senza soglia | sensibilità: `zCE` 2,6 m porta il criterio 2 a 1,23 °/s, `Izz` 300 fa uscire il 4; `collaudo_semaforo.py` fallito per due casi del metro (vedi `CHANGELOG.md`) |

Soglie non cambiate. Decide Ale: tenere la 1.0.46 con i tre fuori dichiarati, o no.
