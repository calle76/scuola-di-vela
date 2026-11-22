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
