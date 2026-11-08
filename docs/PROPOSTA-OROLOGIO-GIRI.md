# Proposta: un orologio per il giro di penalità (fermata 1)

**8 novembre 2026, su `main` (1.2.16). Fermata 1: nessuna riga del gioco cambiata.** Ale: «invece di una scritta piccola che si fatica a leggere sarebbe bello una sorta di orologio che da rosso si riempie di verde e dice quanto hai fatto di giro di penalità».

## 1. In breve

Oggi, durante un giro, nel riquadro in alto a destra c'è una riga a 12 pixel: «Giro in corso: 180° di 360° · virata sì · strambata no». È piccola, e si legge male mentre si governa. Proposta: **un cerchio grande** nello stesso riquadro, sotto la riga «Penalità: 2 giri da fare». Il cerchio è un anello **rosso** che si riempie di **verde** man mano che la prua gira, nel verso del giro. Al centro c'è un numero grande: i gradi fatti. Sotto ci sono due segni, **V** (virata) e **S** (strambata), grigi finché non li hai fatti e verdi dopo.

```
 ┌───────────────────────────────┐
 │ Penalità: 2 giri da fare      │
 │          ╭───────╮            │
 │        ╱ ███     ╲   ← verde: fatto
 │       │  180°     │  ← rosso: da fare
 │        ╲         ╱            │
 │          ╰───────╯            │
 │     giro 1 di 2   V ✓   S ·   │
 │ Stai scontando: lascia strada │
 └───────────────────────────────┘
```

## 2. Il modello più semplice

- **Dove:** pezzo destro del riquadro (`rqDati`/`drawRiquadro`, in `js/regate.js`), solo mentre c'è un giro in corso (`R.giro.v`, dalla 1.2.16). Al posto della riga «Giro in corso…», che sparisce. Il pannello a destra non cambia.
- **Il cerchio:** diametro 64 px, anello spesso 10 px. Il rosso è lo stesso delle bandiere; il verde è quello di «Penalità scontata» (`#7FD6A8`). L'arco verde parte dall'alto e va nel verso del giro (orario se giri a dritta, antiorario a sinistra), lungo `cum / 360`. Al centro i gradi, a 18 px in grassetto, a passi di 10°.
- **Sotto il cerchio:** «giro N di M» (quanti giri della penalità aperta) e i due segni V e S.
- **Giro interrotto:** il cerchio torna tutto rosso; resta il messaggio a comparsa che c'è già («Giro interrotto: ricomincia…»).
- **Prima che il giro cominci** (debito aperto, prua ferma): il cerchio tutto rosso con «0°», così si vede subito cosa fare. Si mostra solo dopo il via e se il giocatore non è arrivato.
- **Chi non distingue rosso e verde:** il numero al centro e i segni V/S dicono la stessa cosa senza i colori.

Nessuna costante del gioco cambia; solo misure di disegno (diametro, spessore, caratteri), ipotesi nostre.

## 3. Criteri (soglie nostre, scritte prima di implementare)

- **O1, il cerchio c'è quando serve:** con il debito aperto dopo il via c'è; senza debito, prima del via e dopo l'arrivo no (letto da `sv.riquadro`, in 10 prove).
- **O2, i pixel:** su un giro guidato dal pilota (come `collaudo_giri`), letti sul disegno vero: a 0° un punto dell'anello a ore 3 è rosso; quando il gioco dice 90° o più nel verso orario, quel punto è verde; lo stesso a ore 6 con 180°. Il verso giusto anche per i giri a sinistra (ore 9). In 10 prove, 5 per verso.
- **O3, il numero:** il testo al centro coincide con i gradi del gioco, arrotondati per difetto a 10°, in tutte le letture.
- **O4, V e S:** diventano verdi nell'istante in cui il gioco conta la virata e la strambata del giro, e tornano grigi quando il giro riparte.
- **O5, niente sovrapposizioni:** il riquadro, nel caso più alto (X, penalità, cerchio, «stai scontando», «oltre la linea»), non tocca la bussola né il vento (in basso a destra) a 1360x650.
- **O6, niente altro cambia:** `collaudo_riquadro_bandiere.py`, `collaudo_giri.py`, `collaudo_pannello.py` verdi; la barca identica (`polare.js`, `raffiche_e_virate.js`, `impronta1b.js`).
- **O7, pagina come la carica un giocatore** (senza `#collaudo`): il cerchio si vede (pixel) dopo un contatto con colpa.

## 4. Rischi

- **Il riquadro diventa più alto** (circa 100 px in più): sta in alto a destra, lontano dalla bussola; O5 lo controlla.
- **Disegno a ogni fotogramma:** un arco e due testi, costo trascurabile; il testo delle misure è già in cache (`rqLarg`).
- **Colori sul mare:** il riquadro ha già lo sfondo scuro; rosso e verde ci si vedono bene.

## 5. Fonti

Nessuna fonte nautica: è un aiuto a schermo, che si può disattivare con «Suggerimenti» come gli altri? **No:** il riquadro delle penalità si vede sempre nella regata dei giri, anche oggi; il cerchio segue lui. Se Ale lo vuole legato a «Suggerimenti», è una riga.
