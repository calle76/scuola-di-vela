# Proposta: lo strapoggio (voce 86; fermata 1, 27 novembre 2026, Opus; via di Ale: «fai anche il punto 86»)

## 1. Cosa c'è oggi (letto nel codice)

- **Il motore** calcola le forze della vela dal valore assoluto del vento apparente (`A = |awa|`): una barca 10° in strapoggio (vento apparente a 190°, boma dalla sua parte) ha le stesse forze di una a 170° con il boma dall'altra. Il lato del boma «non entra nelle forze, solo nel disegno» (`js/motore.js`, 1.0.71). Il boma cambia lato quando il vento apparente passa oltre **5°** da dietro (`BOOM_ISTERESI`, ipotesi del 1.0.71, osservazione 63).
- **Il gioco** conta la strambata quando cambia di segno il vento **vero** (`detectManeuvers` in `js/gioco.js`), non quando passa il boma; con la vela oltre 45° la strambata è «violenta»: velocità × 0,55 e colpo di sbandamento (scuffia sicura con 15 nodi, `tests/misura_strambata.py`).
- **Quindi:** andare in strapoggio non si può. Appena la prua passa i 180° dal vento vero il gioco dà una strambata, violenta se la vela è aperta, anche se il boma (che segue il vento apparente) non si è mosso. Chi va in poppa piena oscillando di un grado attorno a 180° prende strambate a ripetizione.

## 2. Le fonti

- **F124 / F120 (Magnander, galleria del vento sulla vela dell'ILCA 7, dati CC BY 4.0):** spinta a vento apparente 190° (10° in strapoggio, boma dalla sua parte) uguale a quella a 180°: coefficiente massimo 1,42 a 180° e 1,42 a 190° (vento leggero, vang medio), con il boma fino a 120° dall'asse.
- **F109 (Schutt, tesi Cornell, cap. 3, Laser con sensori):** nelle S il vento apparente va e viene di circa ±38° attorno a 183°, cioè fino a una ventina di gradi e oltre in strapoggio, con la scotta a 85-100°. **Il guadagno di VMG delle S misurato da Schutt viene dalla parte non stazionaria** (barca che gira e sbanda, vento apparente che cresce, vortici della vela): il nostro motore, a forze di regime, non può darlo, e in parte è cinetica che la regola 42 limita. **Questa voce non recupera quel guadagno:** rende possibile lo strapoggio, che serve per scendere più profondi senza strambare.

## 3. Proposta (modello più semplice plausibile)

1. **Il boma tiene il suo lato fino a `STRAPOGGIO_MAX` = 20°** di vento apparente oltre la poppa (era 5°). IPOTESI di Claude: Magnander misura spinta piena fino a 10°; Schutt mostra strapoggi più profondi nelle S; oltre, il boma passa da solo (strambata involontaria).
2. **La strambata si conta quando passa il boma** (cambio di `S.boomSide` con il vento al traverso o più largo), non quando cambia segno il vento vero. Le virate restano come oggi.
3. **Le forze non cambiano** (simmetriche, come i dati di Magnander fino a 190°). Fra 190° e 200° nessun dato: semplificazione dichiarata.

## 4. Criteri (soglie nostre, scritte prima di misurare)

- **S1** `polare.js`, `raffiche_e_virate.js`, `virata1b.js` identici; `rotta-dati.js` identico.
- **S2 strapoggio:** con 6, 10 e 15 nodi, prua tenuta a 190° e 195° dal vento vero (10° e 15° in strapoggio) per 30 s con la vela aperta: nessuna strambata contata, il boma resta dal suo lato, velocità entro ±3% di quella a 170°/165° sulle altre mure.
- **S3 strambata involontaria:** prua a 205° (25° in strapoggio): il boma passa e la strambata è contata (violenta con la vela aperta).
- **S4 strambata voluta:** `tests/misura_strambata.py` (150° → 150°): vela aperta ancora violenta 20/20 e scuffia 20/20 con 15 nodi; scotta corta ancora 0/20 violente.
- **S5 non peggiorano:** lezioni col pilota (5.x strambate, 3.5 poppa), medaglie (tempi del pilota), `collaudo_boma_poppa` (da adattare: misura proprio l'isteresi di 5°; si riscrive dicendolo), `collaudo_regole_15_16` e regola 10 in poppa (le mure seguono il vento vero, non il boma: la regola resta sul vento vero).

## 5. Rischi

- **Mure e precedenze:** per il regolamento le mure dipendono dal lato del boma (definizione di «mure»: lato opposto a quello del boma). Il gioco oggi le prende dal vento vero (`tackOf`). Con lo strapoggio le due cose possono differire fino a 20°: **non si cambia ora** (si tocca la regola 10), si annota.
- Rivali: non vanno in strapoggio (la loro poppa è a 142-155°); non cambiano.
- Disegno: il boma resta dal suo lato più a lungo.

## Esito (1.3.68, 27 novembre 2026)

Fatto. Margine del boma che dipende dall'apertura (5° → 35° apparenti), invece dei 20° fissi della proposta: con 20° a 195° veri strambava ancora, e con un margine fisso le lezioni 5.7 e 5.8 col pilota fallivano 92-94 volte su 100 (chi vuole strambare cazza e il boma passa subito). Passano S1-S5; numeri in `CHANGELOG.md` 1.3.68.
