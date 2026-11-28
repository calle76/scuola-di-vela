# Proposta: confrontare le raffiche del gioco con quelle misurate in mare (voce 78)

*22 novembre 2026 (Opus). Domanda di Ale: «raffiche molto forti come quelle in partenza non sono previste durante la regata?» e «cerca registrazioni del meteo sul campo di regata». Via di Ale lo stesso giorno («sì, via alla 78»). È una **misura**: non cambia il gioco; se il gioco esagera, la correzione si propone a parte.*

## Dati

- **NOAA, National Data Buoy Center**, dati «standard» del 2023 (https://www.ndbc.noaa.gov/data/historical/stdmet/), scaricati il 22 nov 2026: BUZM3 (Buzzards Bay, Massachusetts: baia dove si regata, stazione costiera), DBLN6 (Dunkirk, lago Erie, stazione costiera), 44005 (boa nel golfo del Maine, mare aperto). Per ogni riga: WSPD vento medio (2 minuti nelle stazioni costiere, 8 nelle boe) e GST raffica di picco di 5-8 s nello stesso intervallo (descrizione dei campi: https://www.ndbc.noaa.gov/faq/measdes.shtml). Dati di un ente pubblico USA; la licenza esatta va scritta in `FONTI-PUBBLICHE.md` dopo averla letta. Si usano solo numeri misurati (eccezione del 16 ottobre 2026), non testi.
- Si tengono solo le righe con vento medio fra 10 e 14 nodi (il gioco usa 10 e 12).
- Limiti: stazioni a 5-30 m d'altezza (il gioco: vento all'altezza della vela di una deriva), luoghi americani, nessuna stazione su un campo di regata italiano (ISPRA e Garda: da cercare dopo).

## Il metodo

**Dal mare:** fattore di raffica = GST / WSPD, riga per riga: mediana, 90° e 99° percentile, per stazione.

**Dal gioco, con lo stesso metro:** regate lunghe del torneo (semi fissi), un punto fermo al centro del campo e la barca del giocatore guidata dal pilota; ogni 2 minuti (come le stazioni costiere) e ogni 8 minuti (come la boa): vento medio nell'intervallo e picco della media mobile di 5 s; fattore = picco / medio.

## Criteri (attese nostre, scritte prima di guardare i numeri)

| # | Criterio | Soglia |
| --- | --- | --- |
| G1 | Le raffiche del gioco non sono più deboli del mare | mediana del fattore nel gioco ≥ 25° percentile del mare (stessa durata dell'intervallo) |
| G2 | Non sono più forti | 99° percentile del fattore nel gioco ≤ 99° percentile del mare; e mediana del gioco ≤ 75° percentile del mare |
| G3 | Ha misurato davvero | almeno 300 righe del mare per stazione fra 10 e 14 nodi, almeno 300 intervalli del gioco; si stampano |

Se G2 fallisce, proposta a parte per abbassare la forza delle raffiche (`k` in `spawnGust`) o per limitare quante se ne sommano.

## Esito

Misura del 22 nov (1.3.40, Chromium; `tests/misura_raffiche_vere.py`, semi 1401-1430, 30 regate lunghe, 16 punti del campo e la barca). Fattore = raffica di 5 s / vento medio, vento medio 10-14 nodi:

| | casi | 25° | mediana | 75° | 99° |
| --- | --- | --- | --- | --- | --- |
| Gioco, 2 min | 2227 | 1,09 | 1,14 | 1,19 | 1,40 |
| BUZM3, 2 min | 2045 | 1,06 | 1,08 | 1,11 | 1,27 |
| DBLN6, 2 min | 1320 | 1,10 | 1,15 | 1,25 | 1,85 |
| Gioco, 8 min | 510 | 1,21 | 1,25 | 1,31 | 1,59 |
| 44005, 8 min | 7692 | 1,19 | 1,22 | 1,27 | 1,49 |

- **G1** passa con tutte e tre le stazioni.
- **G2** passa con DBLN6; **non passa** con BUZM3 (mediana 1,14 sopra il 75° di 1,11; 99° 1,40 sopra 1,27) né, per il solo 99°, con 44005 (1,59 contro 1,49). La soglia non diceva quale stazione: si riporta per stazione, senza scegliere.
- **G3** passa.
- In breve: raffica tipica come in mare (12 nodi → 13-15); le rare sono un po' troppo forti (17-19 nodi contro 15-18 di baia e mare aperto). Limite: anemometri più alti della vela di una deriva (vicino all'acqua le raffiche contano di più).
- Proposta possibile, da scrivere solo col via: indebolire solo dove si sommano due o più raffiche, lasciando com'è la raffica singola.

## Correzione delle raffiche rare: fermata 1 (23 nov 2026, notte; Ale: «continua in autonomia»)

**Metro senza browser** (`sperimentale/raffiche-78/campo_raffiche.js`): copia in Node del campo di raffiche delle regate lunghe del torneo (gustLevel 1, raffiche come zone, nascita sopravento a un punto a caso del campo invece che a una barca), stesso calcolo di `tests/misura_raffiche_vere.py`, 200 regate di 10 minuti. **Controllo del metro:** col gioco di oggi ridà la misura del browser (2 minuti: 1,09 / 1,14 / 1,20 / 1,39 contro 1,09 / 1,14 / 1,19 / 1,40; 8 minuti 1,23 / 1,28 / 1,36 / 1,65 contro 1,21 / 1,25 / 1,31 / 1,59: un po' più alto).

**Da dove vengono le raffiche rare:** nel torneo una raffica sola vale da 1,2 a 1,4 volte il vento medio nel suo centro (k 0,2-0,4); le forze di più raffiche sovrapposte si sommano.

**Criteri (attese nostre, scritti prima di provare le varianti):**

| # | Criterio | Soglia |
| --- | --- | --- |
| R1 | Raffiche rare meno forti | 99° con 2 minuti ≤ 1,30 (oggi 1,39; BUZM3 1,27, DBLN6 1,85) e con 8 minuti ≤ 1,49 (boa 44005) |
| R2 | Le tipiche restano come oggi | mediana con 2 minuti entro ±0,02 da oggi (1,14) |
| R3 | Non più deboli del mare (G1) | mediana con 2 minuti ≥ 1,10 (25° di DBLN6), con 8 minuti ≥ 1,19 (25° della boa) |
| R4 | Le lezioni non cambiano | la raffica garantita delle lezioni (`bigGust`) e le prove non si toccano: la correzione vale solo nel modo «zone» delle regate lunghe |
| R5 | Conferma nel browser | dopo la correzione `tests/misura_raffiche_vere.py` sugli stessi semi 1401-1430 ridà R1-R3 (fermata 2) |

**Varianti da provare:** (a) somma che satura, 1 − Π(1 − f·k): due raffiche da 0,3 danno 0,51 invece di 0,6; (b) conta tutta la raffica più forte e metà delle altre; (c) raffiche singole più deboli (k 0,2-0,3).

**Risultati della copia in Node** (`campo_raffiche.js [variante] [primo seme]`, 200 regate per riga):

| Variante | semi | 2 min: mediana / 99° | 8 min: mediana / 99° | esito |
| --- | --- | --- | --- | --- |
| oggi | 1-200 | 1,14 / 1,39 | 1,28 / 1,65 | R1 no |
| (a) somma che satura | 1-200 | 1,14 / 1,32 | 1,26 / 1,47 | R1 no |
| (b) metà delle altre | 1-200 | 1,13 / 1,30 | 1,24 / 1,44 | passa |
| (b) metà delle altre | 1001-1200 (conferma) | 1,14 / **1,31** | 1,25 / 1,42 | **non confermata** (0,01 oltre) |
| (c) k 0,2-0,3 | 1-200 | 1,12 / 1,33 | 1,24 / 1,55 | R1 no |
| (b') 0,4 delle altre | 1-200 | 1,13 / 1,29 | 1,23 / 1,41 | passa, margine 0,01 |
| (b'') 0,3 delle altre | 1-200 | 1,13 / 1,27 | 1,23 / 1,37 | passa |
| (b'') 0,3 delle altre | 2001-2200 (conferma, mai guardati) | 1,13 / 1,27 | 1,23 / 1,36 | **confermata** |

Detto com'è: dopo che (b) non si è confermata ho provato pesi più bassi (scelta di nuovo sui semi 1-200, conferma su un terzo gruppo mai guardato); le soglie non sono cambiate.

## Esito della fermata 2 (23 nov 2026, versione 1.3.44)

Fatta in autonomia (Ale: «continua in autonomia, non posso più darti degli ok»). `js/gioco.js`, `ventoDa`: con le raffiche a zone (solo regate lunghe) la raffica più forte conta tutta, le altre per `RAFF_SOMMA` = 0,3. Regate corte, lezioni e prove: stessi conti di prima.
- **R5 nel browser** (`tests/misura_raffiche_vere.py 1401 1431`, Chromium, 30 regate, picco 44 °C): con 2 minuti 25° 1,07, mediana **1,12** (prima 1,14), 75° 1,17, 99° **1,28** (prima 1,40); con 8 minuti mediana **1,22** (prima 1,25), 99° **1,35** (prima 1,59). R1 passa (≤ 1,30 e ≤ 1,49), R2 passa al limite (−0,02), R3 passa (≥ 1,10 e ≥ 1,19).
- **Rivali** (`tests/misura_rivali_vento_forte.py 1 10`, stessi semi del 22 nov): vento locale massimo **18,0 nodi** (prima 23,6), oltre 16 nodi il 2,3% del tempo (prima 4,8%); scuffie 0; virate bloccate 8 su 856 (prima 5 su 842); sbandati oltre 12° il 15,3% (prima 15,7%).
- `collaudo_percorso_lungo.py` OK in Chromium (P4: bolina in raffica 33% e 28%, fascia 20-40%). Motore invariato: `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.
