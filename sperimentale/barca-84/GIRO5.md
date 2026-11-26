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
