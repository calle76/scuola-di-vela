# Voce 84, quarto giro (26 novembre 2026): le ipotesi senza fonte e B2

Giro di sola ricerca dopo il «continua» di Ale; `js/` non toccato. Base: candidato J (`candidato.json`).

## 1. Resistenza dello scafo: due vasche a grandezza vera (B2)

- **F121 (Pennanen 2015) tab. 2, pag. 32:** vasca SSPA, scafo nudo vero, dritto, assetto di minima resistenza: 2 / 3 / 4 / 5 / 6 nodi = 5,97 / 14,96 / 31,06 / 65,93 / 112,73 N.
- Il gioco (Day e Nixon, F16, 160 kg) alle stesse velocità: 6,78 / 16,11 / 34,01 / 70,19 / 117,43 N, cioè **+14 / +8 / +9 / +6 / +4%**.
- **Limite della SSPA** (Lindstrand Levin, Peter, Finnsgård, icSports 2014, §1.4): la barca era **bloccata in affondamento e assetto** (non libera) e il peso non è scritto. Day e Nixon pesano lo scafo a 150-170 kg. La SSPA quindi **non sostituisce** F16: dice solo che fra due vasche vere c'è circa il 5-10% di differenza.
- **Prova (dopo aver visto B2, quindi non è una scelta):** J con lo scafo ×0,93 passa B1-B5, con B2 −4,8% a 60°; J con area 7,9 e scafo ×0,93 dà B2 −2,8%, ma Day a 15 nodi +2,4% e F121 fino a +11%.
- **Day §6.1 sui dati di Binns (F10):** velista, strumenti e metodo non sono noti; gli autori dicono che con le onde la barca poteva surfare, quindi **in bolina larga le velocità sono più alte che in acqua piatta**. Anche il modello di Day è sotto di circa il 6% a 60°.
- **Conclusione:** lo scarto di B2 a 55-60° (−5,7 / −7,3%) è **dentro l'incertezza delle fonti**: la resistenza dello scafo (5-10%) e un dato di Binns con un errore noto verso l'alto. La soglia ±5% era più stretta di quanto le fonti permettano. **B2 resta «non passa» com'è scritto**; non si cambia la soglia.

## 2. Le otto ipotesi (B8): cosa si è trovato

| Ipotesi | Valore J | Fonte trovata | Quanto pesa |
|---|---|---|---|
| Vela che sbatte, `a0` / `w` | 2° / 8° | nessuna. Flay tiene il boma fisso (pag. 20: 5° a 30°, 35° a 60°); Magnander prova solo la poppa (150-190°) | Sulle virate F109 su tutta la griglia `a0` 0-4, `w` 4-14 l'errore resta 0,035-0,09 (oggi 0,14). 3,2 nodi preferisce vela che sbatte presto, 11 nodi tardi: **F109 non decide** |
| Il 9° fra tabella ORC e boma | 9° | **parziale:** F109 §4.2 tab. 4.1, angolo della vela a bolina misurato a metà altezza (striscia al 62%): **13° col poco vento, 19° col medio**. Il boma sta sotto, per lo svergolamento: 9° è plausibile, non misurato | non provato |
| Passaggio 40-60° alla curva vecchia | | Flay a 60° (già nel giro J) | |
| Ritardo dell'appiattimento τ | 0,9 s | **solo qualitativa:** Taylor 2020, app. (specifica dell'ergometro, 2013): alla raffica prima si esce di più fuori bordo (risposta rapida), poi, se la raffica dura, si cambia regolazione o rotta. Nessun numero | **Solo le raffiche:** sbandamento massimo con la raffica 10→18 = 28° (0,5 s), 40° (0,9), 54° (2), 62° (4, criterio «<60°» non passa). Tutto il resto identico. **Leva per la lezione 6.3** |
| Raddrizzata oltre 22,5° | retta fino a 0 a 90° | nessuna: F121 fig. 31 si ferma a 22,5°; Day §4 calcola la GZ dal peso (79,5 kg, baricentro 12 cm sopra la coperta) ma non la pubblica | solo la scuffia (lezioni 6.3-6.4) |
| `dz` | 0 | F121 fig. 31 (curva dei momenti col timoniere): −0,1…+0,1, già nel giro J; J prende il centro | piccolo |
| Deriva che si alza fra 100° e 140° | | **qualitativa:** dispensa di scuola vela 2019 (`fonti-pdf/`, autore non dichiarato): deriva abbassata da un terzo a due terzi nelle andature portanti, tutta alzata in poppa | |
| Vela che sbatte, resistenza `fg` | 0,08 | **Misure di bandiere:** Raynaud e Mulleners 2026 (arXiv 2602.06237, CC BY 4.0), resistenza media 0-0,55, tipica 0,15-0,35; le bandiere leggere (tela da vela) sono fuori dal campo provato e la loro formula dà meno. **F109:** velocità minima nella virata a 11 nodi con scotta lascata 51%: con `fg` 0,02 / 0,08 / 0,2 / 0,35 il modello dà 53 / 49 / 43 / 36%: **F109 mette `fg` fra 0,02 e 0,08**; con 0,2 non passa B6, con 0,35 la virata a 20 nodi non riesce | solo manovre: virate, angolo morto |

## 3. Lezione 6.3 col ritardo dell'appiattimento a 2 s (clone, `collaudo_pilota_lezioni.py --solo 6`, 30 semi)

| | oggi | J (0,9 s) | J con 1,5 s | J con 2 s |
|---|---|---|---|---|
| 6.3 «La scuffia», guidando | 29/29 | 9/29 | **23/25** | **22/23** |
| 6.3 a mani ferme (si completa da sola) | 1/30 | 1/30 | 5/30 | 7/30 |
| 6.2 raffica, guidando | 30/30 (7 s) | 30/30 (15 s) | 30/30 (16 s) | 29/30 (18 s) |
| 6.4 raddrizzare | 30/30 | 30/30 | 30/30 | 30/30 |

(«oggi» rimisurato sul gioco vero nello stesso giro.) Con 1,5-2 s la lezione torna a funzionare, ma 5-7 volte su 30 la barca scuffia da sola a mani ferme (oggi 1): il collaudo lo segnala come difetto, la lezione andrebbe comunque ritoccata. Il ritardo non ha fonte numerica: è una **leva di gioco** dichiarata, non un risultato.

## 4. L'area della vela (7,5 o 7,9): cosa c'è di nuovo

- Il regolamento di classe (ILCA 2026) non dà le misure della vela.
- **Magnander 2022, tab. 4.12:** il modello piatto della vela usato nei calcoli occupa l'1,66% di 8,7 m² (e il 7% di 2,07 m²), cioè 0,144 m² in scala 1:7, **circa 7,06-7,10 m² a grandezza vera**; la tabella delle classi nel cap. 3 della tesi riporta 7,06. I suoi coefficienti sono quindi riferiti all'area nominale. La misura ORC del modello fatto da North Sails (§4.4.7) è annunciata ma il numero non è nel testo.
- Su J non cambia niente: la resistenza in poppa è fissata in m² di forza (9,8-10,6), non in coefficiente.
- **Le fonti continuano a non decidere fra 7,5 e 7,9.**

## 5. Monte Carlo K (200 combinazioni, stesso seme del giro J; `montecarlo84k.js`, `montecarlo_K.txt`)

Intervalli come J, più due cambiati da questo giro: scafo ×0,93-1,0 (le due vasche) e `fg` 0,02-0,08 (da F109, prima 0,05-0,11).

| | J | K |
|---|---|---|
| B1 | 73% | 96% |
| B2 | 1% | 24% (55% senza i 60°) |
| B3 | 53% | **41%** |
| B4 / B6 / B7b | 92 / 84 / 75% | 83 / 90 / 98% |
| tutti tranne B2 | 20% | 35% |
| tutti | 0% | 7% |

Lo scafo più leggero aiuta Binns 9 e peggiora Binns 12 (B3 va oltre +3%): **le due serie di Binns tirano in direzioni opposte**, segno che lo scarto residuo sta dentro la precisione dei dati.

## 6. Controllo nuovo: angolo del boma a bolina (`boma_schutt.js`)

F109 tab. 4.1: angolo della vela a metà altezza (striscia al 62%) sulle barche vere: 13° col poco vento (3,2 nodi), 19° col medio (11 nodi). Il boma sta sotto di qualche grado per lo svergolamento. Barca col miglior VMG:

| Vento | oggi | J |
|---|---|---|
| 3,2 nodi | 10,9° | 9,0° (vela piena) |
| 6 nodi | 10,9° | 9,0° |
| 11 nodi | **10,9°** | **16,6°** (vela piatta 0,92) |
| 15 nodi | 18,5° | 22,3° |

J apre il boma col vento medio come le barche vere; oggi resta chiuso fino a 15 nodi. Controllo fatto dopo aver fissato J, non usato per sceglierlo.

## 7. Le due varianti sul gioco (clone, appiattimento 1,5 s): lezioni, fasce, medaglie (30 corse), regola 18, torneo completo

Numeri in `docs/PROPOSTA-BARCA-MOTORE.md` §«Sul gioco». In breve: medaglie tutte OK con le fasce di oggi; torneo 26 controlli su 27 (manca solo l'uscita lenta C11 R7, già nota sul PC); regola 18 Z1 fallisce per forza, Z4 2 contatti (7,5) e 0 (7,9); lezione 6.3 23/25 (7,5) e 25/25 (7,9), ma la barca scuffia da sola 5 volte su 30.

## 8. La vela che comincia a sbattere: fonte trovata (`a0`), e candidato K

- **Newman e Low, J. Fluid Mech. 144 (1984) 445-462** (solo il riassunto, l'articolo è a pagamento): vele bidimensionali di tela impermeabile in galleria; **la vela sbatte a incidenze appena negative**, e rende al meglio a incidenze molto più alte di 0°. Bundock (tesi, Waikato 1980) tratta la tela poco tesa, non l'incidenza: non serve.
- Su una vela vera svergolata la parte alta è più aperta e sbatte prima: la vela intera comincia a perdere spinta quando il boma arriva a circa 0° d'incidenza e la perde tutta in un intervallo pari allo svergolamento (F109: la vela a metà altezza sta 4° oltre il boma col poco vento). Quindi **`a0` = 0 (fonte)**, **`w` ≈ 10 (svergolamento, e il valore più vicino a F109 nella virata con scotta lascata: 52% contro 51%; scelto guardando F109, dichiarato)**.
- Effetto: a 20 nodi la VMG della barca da 7,9 passa da 3,57 (`a0` 2) a 3,63 (`a0` 0, `w` 10); il calo a 20 nodi veniva in parte da questa ipotesi. Criteri B1-B7b invariati; virate F109 scarto 0,046 / 0,067.
- **Candidato K** (`candidato.json`, quarta voce; `fa_motore84.py` ora scrive K): area 7,92, appiattimento 1,5 s, vela che sbatte da 0° a 10°, il resto come J.
- **Dati GPS di regata** (Pan e Sun, Heliyon 2022, CC BY-NC-ND, 63 prove di Coppa del mondo e Tokyo 2020): velocità media di bolina, ricavata da distanza e tempo, 3,7 / 4,5 / 4,9 nodi con vento sotto 8 / 8-12 / oltre 12 nodi (i primi dieci fino a 5,0); VMG 2,5 / 3,2 / 3,7. Medie di regata (partenze, virate, aria sporca): limiti bassi, la barca in rotta va almeno così. Non distinguono 7,5 da 7,9.

## 9. Le portanti contro le regate vere (`portanti_k.js`)

| Vento | regate (Pan e Sun) traverso/lasco | K traverso / lasco | regate VMG poppa | K VMG poppa | oggi VMG poppa |
|---|---|---|---|---|---|
| sotto 8 (circa 6) | 4,2 | 4,26 / 4,06 | 3,3 | 2,87 | 2,65 |
| 8-12 (circa 10) | 5,8 | 6,02 / 5,76 | 4,7 | 4,45 | 4,17 |
| oltre 12 (circa 15) | 9,1 | 9,40 / 9,13 | 7,8 | 6,16 | 5,71 |

- **Laschi: K coincide con le regate.**
- **Poppa: le regate vanno più forte** (+15 / +6 / +27%). Schutt (F109 cap. 3, fig. 3.18, vento 12 nodi a 6 m): andando dritti VMG circa 2,5 m/s (4,9 nodi), con le «S» circa 3,0 m/s (5,8 nodi, +19%); «in regata quasi nessuno va dritto in poppa, salvo col vento molto debole». K a 12 nodi fa 5,10: **vicino a chi va dritto**. La differenza con le regate è tecnica (S, onde, pompaggio permesso col vento forte), che il gioco non ha: possibile voce futura, non è la barca.

## 10. Sbandamento di bolina (F121 §4.3-4.4 e §6)

Pennanen: a 2 nodi di velocità conviene sbandare di 10-15° sottovento (meno superficie bagnata), da 3 nodi in su conviene andare dritti, poi un piccolo sbandamento dà momento raddrizzante in più («i velisti accettano qualche grado»). K: 1° con 6 nodi di vento, 4° da 10 a 15 nodi; con vento debolissimo va dritto, perché nel gioco lo sbandamento non cambia la resistenza dello scafo. **Limite minore** (Pennanen: con vento debolissimo le differenze di velocità sono molto piccole).

## 11. Velocità prima della virata, Laser Radial (Eiraku e altri, Japan J. Coaching Studies 27(1) 2013, accesso libero; il riassunto era F122)

13 atlete e atleti, GPS, vento misurato da un gommone: 3,1 m/s (6 nodi) e 5,0 m/s (10 nodi); velocità di bolina prima della virata 1,8-1,9 m/s (3,6 nodi) e 2,2-2,3 m/s (4,4 nodi). Radial: vela più piccola e velisti più leggeri, quindi solo un ordine di grandezza; K (vela intera) a 6 nodi fa circa 3,7 nodi di bolina. Coerente.

## 12. Scarroccio (`scarroccio_k.js`, F121 fig. 11)

Pennanen (CFD) usa 3,7° a 2-3 nodi di velocità, 4,0° a 4 e 4,65° a 5 nodi (angoli presi dal suo primo calcolo, non misurati); a 5 nodi la forza laterale è circa 290 N. K, con la formula di Day e le misure di deriva e pala del regolamento (`DERIVA2.q` 873, voce del 1.0.45): 2,1 / 2,5 / 2,7 / 3,2 / 3,1° con 3,2 / 6 / 8 / 11 / 15 nodi di vento, 305 N a 4,8 nodi. La CFD dà alla deriva circa il 35% di forza in meno (q equivalente circa 540). Con q 540: Day 6 nodi −3,7%, Binns 9 a 60° −6,4%, Binns 12 −1,5%: **1-2% in meno, conclusioni uguali**. Due modelli, nessuna misura in acqua: q resta 873 (coerente con Day).

## 13. Barca che orza sbandando

Già nel motore dalla 1.0.46 (F4 eq. 6: spinta applicata al centro velico spostato sottovento); con K (braccio 2,8) l'effetto cresce. Una barca lasciata a sé stessa in raffica tende a orzare; la scuffia a mani ferme della lezione 6.3 (9 su 30 con K) va guardata nella lezione.

## Restano aperti (fine del quarto giro)

- Ampiezza della vela che fileggia `w`, ritardo dell'appiattimento, raddrizzata oltre 22,5°: senza misura (cercate: nessuna curva GZ del Laser pubblicata; nessuna misura dei tempi di regolazione).
- **Da scaricare a mano (il sito blocca i programmi):** «Multi-Sensor System for Analysis of Maneuver Performance in Olympic Sailing», Applied Sciences 15 (2025) 8629, https://doi.org/10.3390/app15158629: un ILCA 7 con sensori su timone, albero e sbandamento; può dare virate e raffiche misurate.
- Poppa con le S e le onde: tecnica che il gioco non ha (possibile voce futura).
