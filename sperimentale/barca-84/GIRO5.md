# Voce 84, quinto giro (26 novembre 2026): regole scritte PRIMA di misurare

Via di Ale: «fai l'altro giro di ricerca sul banco come proponi». `js/` non si tocca. Punto di partenza: `RICERCA-K.md` §17 (la VMG del banco ignorava lo scarroccio).

## 1. Il metro

- **VMG di bolina sulla rotta**: velocità vera (√(u² + scarroccio²)) × cos(angolo di prua + angolo di scarroccio). Vale per Day (F17, «speed, track, leeway»), regate e GPS.
- **Binns, Pennanen (F121) e la velocità con 3,2 nodi a 45° (F109)**: l'angolo dato è quello della rotta. Binns è un GPS; per F121 (programma di previsione) e F109 (GPS) vale lo stesso.
- In poppa e al lasco lo scarroccio è quasi zero: si usa lo stesso metro.
- Il banco (`banco84.js`) passa a questo metro per tutti; il vecchio resta con `BANCO_PRUA=1` per rifare i numeri di prima.
- **Criteri e soglie invariati** (B1-B7b, virata 16 nodi, raffica, angolo morto).

## 2. Lo scafo: quale vasca (regola scritta prima)

Due vasche a grandezza vera: Day e Nixon (F16, scafo pesato 150-170 kg, è quella del gioco) e SSPA (F121 tab. 2, scafo bloccato in affondamento e assetto, peso non scritto), 4-14% di resistenza in meno. Nessuna delle due è «la giusta»: ognuna ha un limite noto. **Regola, la stessa del candidato J (centro degli intervalli delle fonti): scafo × 0,965**, metà fra le due. Non si sceglie guardando i criteri.

## 3. L'area della vela

Resta 7,92 (K), scelta il 26 novembre per ragioni scritte (`PROPOSTA-BARCA-MOTORE.md`: area con cui Day ha verificato il suo modello; F109 corretto per il vento in testa d'albero chiede di più). Il Monte Carlo la fa variare fra 7,06 e 7,92 come prima.

## 4. Candidato L = K + scafo × 0,965, misurato col metro nuovo

Si riportano i criteri così come escono. Poi il Monte Carlo (200 combinazioni, stesso seme, stessi intervalli di K: area 7,06-7,92, braccio 2,4-3,1, timoniere 0,87-0,956, scafo 0,93-1,0, `fg` 0,02-0,08) col metro nuovo.

## 5. La velocità bassa: lo smorzamento della resistenza indotta `reg`

- **Vincolo da Day (fig. 11):** quota della resistenza indotta sul totale a 5 nodi = 10,5%. Si accettano i valori di `reg` che danno fra 9 e 12% (attesa nostra: la lettura del grafico).
- Fra quelli, **si sceglie il valore con l'errore più piccolo sulle virate di F109** (scarto secondo per secondo a 3,2 e 11 nodi, già nel banco: è la misura del regime lento usata come taratura fin dal giro J).
- **Conferma, non usata per scegliere:** le 12 virate di Semb (F137) con 14 nodi, col pilota di `virate_semb.js` (entrata, uscita, media, 80%), e le virate del 470 (F4 fig. 5-6, solo come ordine di grandezza).

## 6. Cose mai provate (solo misura, nessuna scelta)

- La scotta automatica «sicura» del gioco (`autoSheet(true)`: lasca 1,5° di boma per grado di sbandamento oltre 12°) dopo una virata con 14 e 18 nodi, oggi e L.
- Strambata con 10, 15 e 20 nodi: velocità minima, sbandamento massimo, se scuffia; oggi e L. Nessuna fonte numerica: si riporta e basta.

## 7. Il velista che appiattisce la vela da solo (principio 3)

Non è una misura: si scrivono le due possibilità per Ale.

---

# Esito (26 novembre 2026, scritto dopo le misure)

## 1-4. Criteri col metro sulla rotta (`giro5.js`; il banco ora misura sulla rotta, `BANCO_PRUA=1` ridà i numeri vecchi: controllato su K)

| | B1 Day 6 | Day 10 / 15 | B2 Binns 9, 42-60° | B3 Binns 12, 42-60° | B5 3,2 nodi | altri |
|---|---|---|---|---|---|---|
| oggi | −19,5% | −14,8 / +1,1% | −28,5 … −15,2 | −17,0 … −2,7 | −25% | B6 e B7b no |
| K | **−5,9%** | −5,0 / −4,8% | −5,5 / −4,5 / −5,7 / −6,9 | **−4,9 / −4,6** / −3,9 / −3,0 / −1,5 | −1,2% | passano |
| L (K, scafo ×0,965) | **−4,8%** | −4,2 / −3,8% | −4,4 / −3,6 / −4,7 / **−5,8** | **−4,0 / −3,7** / −3,0 / −1,9 / −0,4 | +0,1% | passano |

L passa B1, non B2 (solo a 60°) né B3 (a 42 e 46,5°). VMG a 20 nodi 3,46 (K 3,43; col metro vecchio 3,63). La barca di oggi sulla rotta è peggio di quanto scritto finora (−19,5% con 6 nodi; con 3,2 nodi −25%).

**Monte Carlo** (`montecarlo_K_rotta.txt`, 200 combinazioni, stesso seme e stessi intervalli di `montecarlo_K.txt`): B1 **16%** (col metro vecchio 96%), B2 2% (24%), B3 25% (41%), B4 100%, B5 100%, B6 90%, B7b 98%, virate e raffica come prima; **tutti tranne B2 3%** (35%), tutti 0% (7%). B1 passa di più con area grande, poca resistenza parassita, scafo leggero. **Dentro gli intervalli delle fonti la barca resta lenta di bolina di circa il 4-6%**: con il metro giusto le fonti di velocità (Day, Binns) chiedono più spinta o meno resistenza di quanto gli intervalli permettano. Cause possibili, non decise: dove era misurato il vento di Binns (altezza, posizione), la convenzione di Day (Binns invece è un GPS: per lui la rotta è sicura), la resistenza parassita (0,105 da Day fig. 12), l'area.

## 5. Velocità bassa (`reg_giro5.txt`)

Tutti i valori di `reg` fra 0,05 e 0,4 danno la quota di Day (9-10,9%). Scarti sulle virate F109: 0,111 (0,05) … 0,117 (0,4): **la regola sceglie 0,05, ma la differenza (0,006) sta sotto la precisione della lettura dei grafici (±0,03): F109 non decide**. Conferma con le virate di Semb a 14 nodi: uguali per tutti (uscita 91-92%, media 88-89%, 80% dopo 7,5-7,7 s; misura 92 / 86 / 7,6). Con 18 nodi più `reg` aiuta (uscita 8% con 0,05, 55% con 0,1, 77% con 0,4), ma il vento vero di Semb è incerto. **`reg` resta senza misura che lo fissi**; L con 0,1 esce con 18 nodi al 55% (K 28%).

## 6. Mai provati (`mai_provati.txt`)

- **Scotta automatica «sicura» del gioco dopo la virata:** la barca riparte sempre. Con 14 / 18 nodi minimo 32 / 22% oggi, 60 / 37% K, 61 / 38% L; dopo 20 s 98-100% per tutti. Il blocco del §15 di `RICERCA-K.md` viene dal pilota che cazza tutto, non succede con l'aiuto del gioco.
- **Strambate** (150° → 150°, 10 / 15 / 20 nodi): per tutte le barche il giro dura 1,6-3 s, la velocità scende dell'1-2%, sbandamento massimo 2-5°, mai scuffia. **La strambata del gioco è troppo facile con vento forte** (nella realtà il boma che passa dà uno strappo e si rischia la scuffia): limite del motore di oggi, non della barca nuova; nessuna fonte numerica trovata.

## 7. Il velista che appiattisce la vela da solo (principio 3)

Due possibilità per Ale: (a) è fisica del velista, come l'uscita fuori bordo che il gioco fa già da solo (IL-GIOCO: «l'aiuto disegnato è disattivabile, la fisica no»); (b) è un aiuto, e allora serve un interruttore (vela regolata a mano, cioè comandi nuovi). Con (a) non cambia niente; con (b) è lavoro in più.

## Conclusione del quinto giro

1. **Il risultato solido non cambia:** la vela di oggi è molto più debole del vero col poco vento (col metro giusto −20% con 6 nodi), e K/L sono molto più vicini alle fonti.
2. **Ma col metro giusto nessun candidato dentro gli intervalli delle fonti passa i criteri di bolina** (3% delle combinazioni senza B2): manca ancora circa il 4-6% di bolina, con una causa non trovata.
3. Velocità bassa: non decisa dalle misure; la scotta automatica del gioco riparte sempre.
4. Strambate troppo facili: limite vecchio, nuovo da segnare.
