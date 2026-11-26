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
