# Proposta: la virata della barca dell'1b (freccia agile, Maiusc che frena da veloce)

Stato: **fermata 1, nessun codice nel gioco** (23 ottobre 2026, notte). Richiesta di Ale: la barca dell'1b è lenta in virata con la sola freccia; idea: freccia agile come nell'1a senza barra a fine corsa, Maiusc a fine corsa che frena se la barca è veloce (virata di colpo davanti a un ostacolo, pagata) e serve a bassa velocità (boe, giri di penalità, partenza). Viene prima delle regole 15 e 16 (la finestra T dipende dalla barca: `PROPOSTA-REGOLE-PRECEDENZA-1B.md`, 1.0.43).

## Fonti
- **F4** (470 vero, `PROPOSTA-STALLO-TIMONE.md` §7): virata accompagnata fino a 45° circa 3,4 s, minima 43-44% dell'entrata; data in fretta 2,9 s, minima 42% in una figura e **29%** nell'altra; fermata a 30° circa 5 s. Barca a due, inerzia circa 2,5 volte la nostra.
- **Video già usati:** circa 3,3 s (virata chiusa da Ale), `RICERCA-VELOCITA-VIRATA-RIPARTENZA.md` §2 (da rimisurare sullo stesso intervallo).
- **Ricerca di Ale con l'AI** (`ricerca_virata_ILCA7.docx`, 21 ottobre 2026, fuori da git): nessuna misura pubblicata di durata, angolo di barra o perdita di velocità per una deriva singola; i suoi «3-7 s» e «10-50%» sono intervalli di prova, non dati. Utili: la forza del timone cresce col quadrato della velocità; la didattica della classe dice di accorciare il tratto prua al vento. Rimandi: Gale e Walls 2000 (simulatore di deriva tarato in acqua: trovato solo il riassunto, https://ecite.utas.edu.au/19717), de Ridder e Keuning 2004 (barche a chiglia).

## Misure (motore di oggi, gesto da tastiera: barra a 1,6 della corsa al secondo, al centro quando la prua è 30° oltre il vento; tempo fino a quel punto; `$TMPDIR`, script non in git)

| Vento | 1a (barra a fondo) | 1b freccia (35°) | 1b Maiusc (45°) |
|---|---|---|---|
| 6 nodi | 2,7 s, minima 56% | 4,5 s, 48% | 3,6 s, 52% |
| 10 nodi | 2,1 s, 52% | 3,2 s, 44% | 2,5 s, 48% |
| 15 nodi | 1,9 s, 44% | 3,0 s, 33% | 2,3 s, 40% |

Una prima tabella data ad Ale in chat (barra a fondo di colpo e tenuta fino a 40° oltre) diceva 3,7-5,4 s per la freccia: era un gesto diverso, questa è quella del gioco.

**Cosa ne esce:**
1. Con 10-15 nodi la virata dell'1b con la freccia (3,0-3,2 s) **è già quella delle fonti** (F4 3,4 s, video 3,3 s). È l'1a a essere più rapida delle fonti (1,9-2,1 s). Con 6 nodi l'1b è lenta (4,5 s; nessuna fonte con poco vento).
2. **Maiusc in virata non frena e il motore non lo fa frenare in nessun modo provato:** barra data in fretta (4 e 10 corse al secondo invece di 1,6): la pala stalla 0,1-0,2 s, la minima scende di 2-4 punti al più e resta **sopra** quella della freccia. Con più autorità della pala (`yawG` 2,5) o meno freno dell'acqua sullo scafo (`hullKq` 300) le virate sono più rapide e perdono **meno**. Nel motore la perdita nasce dal tempo passato con la prua al vento: girare più in fretta costa sempre meno. Coerente con la didattica (accorciare il tratto al vento) e con una figura su due di F4; non con l'altra.
3. **Barca lenta** (1,5 nodi al traverso, 3 s di barra): Maiusc gira 85° contro 70° della freccia, con 0,3 nodi in meno: lì Maiusc serve, come Ale vuole.

## Strade
- **A. Freccia più agile, solo con fisica.** `hullKq` 600 → 300 (stima della revisione in chat, mai misurata): freccia 3,8 / 2,7 / 2,5 s con 6 / 10 / 15 nodi, minima 56 / 52 / 42%; prua dopo la virata 40-41° (non va oltre). Si allontana un po' dalle fonti (più rapida di F4 e dei video), si avvicina all'1a. Costo: rifare la taratura di `yawG` con la sua regola, `timone2.js`, avversari (`collaudo_virate2.py`), giri di penalità.
- **B. Maiusc che frena da veloce = regola del gioco senza fonte.** Per esempio una resistenza in più della pala oltre 35° di barra, col quadrato della velocità (a 1-2 nodi quasi zero). Fa quello che Ale descrive, ma non nasce dalla fisica del motore e nessuna fonte la misura su una deriva singola: si dichiara come regola didattica, come i 35° della freccia.
- **C. Prima misurare.** Video di derive singole: virate «sbattute» contro «accompagnate», durata e (se si vede) velocità prima e dopo. Solo se mostrano la differenza si apre B con un numero.

## Consiglio
A (se la virata con la freccia a 10 nodi si sente lenta giocando) e C prima di B. Senza fonte, B insegnerebbe una cosa che il motore stesso contraddice (girare in fretta conviene).

## Criteri (se si va avanti; attese nostre)
1. Freccia: virata 2,5-3,5 s con 8-15 nodi (F4 e video), al massimo 4,5 s con 6 nodi; minima 35-60%.
2. Maiusc: almeno il 10% più rapida della freccia; con B, minima almeno 5 punti sotto la freccia con 10 e 15 nodi e non più di 2 punti sotto a 1,5 nodi.
3. Prua dopo la virata non oltre 60° (V1 della 1.0.31).
4. 1a identica al bit; `polare.js` e `raffiche_e_virate.js` identici.
5. Regola dei semi per ogni costante scelta: venti di scelta 10 e 14 nodi, di conferma 6, 8, 12 e 16 (come nella 1.0.24 e 1.0.31).

## Decisione di Ale e fermata 2 (23 ottobre 2026): strada A, versione 1.0.43
Ale: «A» (e: le derive girano anche col peso del timoniere; nel gioco il corpo non è un comando, quindi quell'agilità sta dentro il timone, semplificazione dichiarata). Regola fissata prima della griglia: il valore più basso di `hullKq` (barca più agile) con il criterio 1 ok a 10 e 14 nodi. Griglia 600-100: ok fino a 400, da 300 in giù la virata a 14 nodi scende sotto 2,5 s. **Scelto 400.** Conferma (6, 8, 12, 16 nodi): ok a 6, 8, 12; **FUORI a 16 nodi** (minima 34% contro 35%; con 600 era 27%). Numeri e collaudi nel `CHANGELOG.md`, 1.0.43. Strade B e C non fatte; B resta da aprire solo se i video (C) mostrano che la virata «sbattuta» perde più velocità.
