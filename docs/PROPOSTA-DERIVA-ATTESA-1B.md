# Proposta: deriva in attesa prima del via, avversari dell'1b (29 ottobre 2026)

Nasce dalle osservazioni 59-61 e 67 (`OSSERVAZIONI-GIOCANDO.md`). Ale ha detto di procedere se la proposta regge (29 ottobre 2026): fermata 1 e 2 nella stessa sessione, soglie scritte qui **prima** di misurare.

## Il problema, misurato
Nei 40 tornei col pilota il 16% dei tagli di linea degli avversari cade oltre 3 m fuori dagli estremi (34% delle regate ne ha almeno uno, massimo 80 m); nella registrazione di Ale del 28 ottobre (sera) due avversari su dodici hanno tagliato a 76 e 93 m e hanno perso circa 100 s. Nell'ultimo minuto prima dello sparo tutte le barche in attesa scivolano di lato verso la boa di circa 25 m al minuto (mediana −24,5 m su 12 barche). `waitX` (`js/regate.js:247`) compensa solo lo scivolamento della rotta di partenza, `lat * yW` (8-10 m), non quello della sosta.

## Modello più semplice
Aggiungere a `waitX` una costante `DERIVA_ATTESA`, in metri, solo nell'1b (`R.lv2`; l'1a resta identico al bit): il punto d'attesa si sposta controvento rispetto alla deriva dell'attesa, così la barca che scivola passa per il punto giusto e taglia dentro. Il limite di `waitX` dentro gli estremi resta. Nessun cambio al motore né alla guida dell'avversario.

## Costanti
- `DERIVA_ATTESA`: ipotesi nostra, da scegliere fra 8, 14 e 20 m (la deriva misurata nella sosta di 20-45 s è 8-19 m). Scelta sui semi 1-20, confermata sui semi 21-40 (regola dei semi).

## Criteri (soglie nostre, scritte prima di misurare; sui semi 21-40 dopo la scelta)
1. Tagli oltre 3 m fuori dagli estremi: **al massimo 5%** (ora 14,5%); regate con almeno uno: **al massimo 15%** (ora 32,5%); massimo **45 m** (ora 80).
2. Tempo medio del taglio entro ±1,5 s di quello di ora (6,1 s).
3. Penalità per regata non oltre +10% (ora 3,5); non arrivati e boe girate male non peggiori (ora 1 e 2 su 80 regate).
4. Non-regressione: 1a identica (collaudi di `polare.js` e `raffiche_e_virate.js`, impronta 1b), `collaudo_partenze.py` e `collaudo_avversari1b.py` senza nuovi falliti.

## Rischi
- Più barche spostate verso lo stesso estremo possono accalcarsi (si guarda il punto 3).
- Il rimedio non toglie le cause occasionali (contatto che spinge fuori); si misura quanto resta.
- Se nessun valore rispetta il punto 1, si riporta com'è e non si cambia soglia.

## Risultati (29 ottobre 2026): provato, **non adottato**, il gioco non è cambiato

Tutte le misure con `tests/misura_partenze_torneo.py` + `tests/riassumi_partenze_torneo.py`, tornei di 4 regate col pilota, semi 1-20 (80 regate, 240 barche). Riferimento: oltre 3 m fuori **17,6%** dei tagli, regate con almeno uno **36,2%**, massimo 70 m, tempo medio del taglio 6,3 s, penalità per regata 3,27, barche già oltre la linea allo sparo **9,6%**. Le prove sono state fatte con costanti provvisorie nel codice (ora tolte, `js/regate.js` è tornato com'era); la conferma sui semi 21-40 non è stata fatta perché nessuna variante ha passato la scelta sui semi 1-20.

**Cosa succede davvero** (guardando una regata passo per passo): gli avversari arrivano nella fascia d'attesa, 6-8 m dietro la linea, già 100-110 s prima dello sparo, e lì si fermano nel punto in cui la simulazione dell'abbrivio (`glideY`) dice di non avvicinarsi di più, non in `waitX`. Quindi spostare `waitX` quasi non serve. Da lì scivolano di lato di circa 0,2 m/s verso la boa, e nell'ultimo tratto verso la linea ne scivolano altri 10-15.

| Variante (solo 1b) | fuori >3 m | regate con uno | massimo | taglio medio | penalità/regata | oltre la linea allo sparo |
| --- | --- | --- | --- | --- | --- | --- |
| nessuna (riferimento) | 17,6% | 36,2% | 70 m | 6,3 s | 3,27 | 9,6% |
| `waitX` spostato di 8 / 14 / 20 m | 17,5 / 14,4 / 11,1% | 32,5 / 31,2 / 28,8% | 74 / 87 / 68 m | 6,2 / 6,3 / 7,0 s | 3,71 / 4,15 / 5,21 | non misurato |
| tornare alla stazione se si è scivolati oltre 8 m, fino a 12 s dal via | 4,7% | 11,2% | 67 m | 8,0 s | 3,64 | **27,1%** |
| come sopra, fino a 25 s dal via | 5,1% | 12,5% | 51 m | 7,2 s | 3,67 | **20,0%** |
| come sopra con tolleranza 6 m, fino a 25 s dal via | 6,5% | 16,2% | 68 m | 7,6 s | 3,51 | 22,9% |
| stessa correzione, fino a 50 s dal via | 17,6% | 36,2% | 70 m | 6,3 s | 3,27 | 9,6% (non scatta mai: la deriva si accumula tardi) |
| correzione fino a 40-60 s dal via, con `waitX` spostato di 8-12 m | 11,6-17,0% | 26-35% | 71-149 m | 5,3-6,2 s | 3,95-4,16 | 5,8-10,4% |
| barche più al centro all'inizio (slot ±18 / ±14 / ±10 invece di ±24) | 21,6 / 23,0 / 36,2% | 40 / 47,5 / 63,8% | 104 / 88 / 110 m | 6,6-7,0 s | 4,06 / 4,42 / 5,54 | 7,1-8,3% |

**Lettura.** Il solo rimedio che abbassa davvero le uscite dagli estremi (tornare alla stazione negli ultimi secondi) le sposta in partenze anticipate: dal 9,6% al 20-27% delle barche oltre la linea allo sparo, che in gioco vuol dire richiamo e circa 100 s persi, come la Rossa e la Verde della registrazione di Ale. Criteri 1 (≤5%, ≤15%, ≤45 m), 2 (±1,5 s), 3 (penalità +10%): nessuna variante li rispetta tutti (la migliore, «oltre 8 m, fino a 25 s», ha 5,1%, 12,5%, 51 m, +0,9 s, +12%, ma raddoppia le partenze anticipate). Avvicinare le barche al centro all'inizio peggiora tutto: si accalcano e si spingono fuori a vicenda. Soglie non cambiate.

**Cosa resterebbe da provare** (tocca la guida dell'attesa, quindi fermata 1 nuova, non fatto): far sì che la barca in attesa non scivoli (per esempio alternare le due mure nell'attesa invece di restare sempre su una, come farebbe un timoniere), oppure accettare che nel livello 1 qualche avversario parta largo o in ritardo e dirlo (come la linea da 70 m, `DECISIONI`). Il primo si misura come questo; il secondo costa solo una riga.
