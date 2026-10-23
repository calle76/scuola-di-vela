# Proposta: i distacchi in regata, in secondi

19 ottobre 2026, fermata 1. Richiesta di Ale: vedere il distacco dalla barca davanti e da quella dietro, soprattutto in secondi, e i secondi all'arrivo; scritte sul mare in alto a sinistra, sotto «Vento reale». Solo secondi: i metri in bolina sarebbero imprecisi (due barche su bordi diversi hanno la stessa distanza dalla boa ed essere lontane).

## Cosa si vede

Dopo il via, finché non si arriva, sotto «Vento reale da…» (`drawWindBox`, `js/disegno.js`), stesso carattere:

```
Davanti: Rossa, 6 s
Dietro: Blu, 3 s
```

Una riga sola se si è primi o ultimi. Niente durante la preparazione, niente dopo il proprio arrivo. Tutte le regate (livello 1 e 2): è un'informazione, non fisica; il pannello non cambia.

All'arrivo, nel risultato: «2° su 4 in 3 min 12 s, a 4 s dalla Rossa (prima).» Se si è primi, nessun distacco (chi arriva dopo non è ancora arrivato).

## Come si calcola (il modo più semplice che è un tempo vero)

- **Strada fatta** di ogni barca, in metri: sul lato di bolina, lunghezza del lato meno la distanza dalla boa; sul lato in poppa, lunghezza della bolina più la lunghezza del lato meno la distanza dall'arrivo. Davanti e dietro: lo stesso ordine della classifica di oggi (`ranking`).
- Ogni barca si ricorda la sua strada fatta ogni 0,5 s.
- **Distacco dalla barca davanti** = adesso meno l'istante in cui lei aveva la mia strada fatta di adesso. **Dalla barca dietro** = adesso meno l'istante in cui io avevo la sua. Sono secondi veri, già passati: non una stima della velocità.
- Arrivo: differenza dei tempi d'arrivo (`b.fin`), già esatta.

Limite dichiarato: vicino alla boa la strada fatta si misura in linea d'aria, quindi il distacco può saltare di qualche secondo quando una barca gira la boa.

## Criteri (soglie nostre, dichiarate ora)

Regate senza giocatore (pilota), semi 1-20 da guardare e 21-60 di conferma, principianti ed esperti, regate 1, 2 e quella nei salti.

- **D1** il distacco dalla barca davanti mostrato 5 s prima dell'arrivo del giocatore, confrontato con la differenza vera dei tempi d'arrivo: entro **3 s** nel 90% delle regate (si dice quante sono state misurate).
- **D2** all'arrivo i secondi scritti sono la differenza dei `b.fin`, arrotondata: 100%.
- **D3** il distacco non è mai negativo e cambia al più di 5 s fra due aggiornamenti, salvo quando cambia la barca davanti (si conta quante volte succede).
- **D4** a 1360×650 e a una finestra più piccola le righe non si sovrappongono ad altre scritte; pannello identico (`collaudo_pannello.py`).
- **D5** fuori dalle regate niente cambia: impronta identica, salvo le immagini del mare delle regate (attese diverse, per le righe nuove).

## Rischi

- Un'informazione in più sul mare: si giudica giocando se distrae.
- Con una barca che parte in anticipo o scuffia, l'ordine cambia di colpo e il distacco salta (D3 lo conta).

## Fermata 2 (19 ottobre 2026, versione 1.0.33)

**Cambiato durante il lavoro, su decisione di Ale:** le scritte sul mare sono state tolte; i distacchi stanno **nella classifica del pannello**, accanto a ogni barca («Rossa di bolina · 6 s», «Blu di bolina · −3 s»: positivo davanti, negativo dietro), per tutta la regata; dopo il proprio arrivo la classifica mostra le differenze dei tempi d'arrivo (con le penalità). Nessuna riga nuova nel pannello. Il risultato d'arrivo dice «, a 57 s dalla Rossa, a 74 s dalla Blu (prima)».

**Fatto** (`js/regate.js`): `strada`, `quando`, `distacco`, `arrivoDistacchi`; la strada fatta si salva ogni 0,5 s in `updateRace`; `racePanel` aggiunge il distacco. Tutte le regate, livello 1 e 2.

**Il metro della strada fatta è cambiato dopo il primo giro, dichiarato.** Prima: distanza in linea d'aria dalla boa e dal centro della linea. D1 nella conferma: **67 su 99 (68%), fuori**; nei casi dei semi 1-12 (guardati uno per uno) gli errori grandi erano arrivi ravvicinati col segno sbagliato, perché gli avversari tagliano la linea (24 m) fino a 15-19 m dal centro. Ora: metri nella direzione del vento medio, come nel tracciamento delle regate vere. Soglia invariata.

**Misure** (`tests/collaudo_distacchi.py`, regate 1, 2 e nei salti, principianti ed esperti, 360 regate col pilota, tutte arrivate):
- **D1 ok**: conferma (semi 21-60) **193 su 200 entro 3 s (96%)**, errore mediano 0,5 s, massimo 7,3 s; guardati (1-20) 91 su 95 (96%), massimo 5,9 s.
- **D2 ok**: 277 risultati su 277 con i secondi giusti.
- **D3**: 562 477 letture, 2178 salti oltre 5 s della stessa barca (0,4%), soprattutto quando la barca davanti ha virato o si è fermata in un punto (il suo «quando era qui» cambia di colpo). Dopo l'arrivo la classifica coincide sempre con i tempi d'arrivo.
- **D4 ok**: caso peggiore a 1360×650 (quattro barche con «boa girata dal lato sbagliato · +45 s · −119 s» e la spiegazione di un contatto): eccesso del pannello 0 px, nessuna riga a capo.
- **D5 ok**: impronta identica salvo i testi delle 4 regate (risultato e classifica); arrivi e immagini del mare identici; `polare.js` e `raffiche_e_virate.js` identici.

**Limite dichiarato:** è «quanti secondi fa la barca davanti era alla mia altezza», non una previsione: se nell'ultimo tratto una va più veloce, all'arrivo il distacco vero è diverso (errori di 2-5 s con distacchi di 20-30 s).
