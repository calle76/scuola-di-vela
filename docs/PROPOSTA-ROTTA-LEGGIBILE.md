# Proposta: rotta ottimale più leggibile (fermata 1)

13 novembre 2026, sera. Voce 32 di `DA-FARE.md`, osservazione 122 (Ale, 11 novembre). Ale ha scelto due idee su quattro: **1, il filo fra i due punti dello stesso istante** («va bene se ti sembra bella, poi la capirò meglio quando la vedo») e **3, nascondere la barra laterale del gioco**. Lo zoom e le linee più grosse no. È la fermata 1: in `js/` non è stato scritto niente.

## Cosa c'è oggi

La rotta ottimale si apre a regata finita. Nella vista dall'alto (`rotVista` e `rotDisegna`, `js/rotta.js`):
- la rotta ottimale è una linea verde, la tua è blu;
- su ciascuna c'è un punto ogni 30 s;
- la frase in alto dice «un punto ogni 30 s», ma non dice che vanno confrontati i due punti dello stesso istante;
- la barra laterale del gioco (`.panel`, 390 px) resta, e la mappa usa solo lo spazio a sinistra.

## Modello più semplice

**1. Il filo dello stesso istante.**
- Ogni **60 s** dal tuo taglio della linea, un trattino sottile e chiaro, grigio-bianco semitrasparente, unisce il punto verde e il punto blu di quell'istante.
- Accanto al punto verde c'è il tempo scritto piccolo: «1:00», «2:00»…
- I punti ogni 30 s restano come oggi; il filo e il tempo solo ogni minuto, perché ogni 30 s sarebbero troppi.
- Si disegna finché esistono tutte e due le rotte, cioè fino all'arrivo della prima.
- La frase in alto cambia: «…un punto ogni 30 s; ogni minuto un filo unisce dove eri tu e dove saresti stato con la rotta ottimale nello stesso istante».

**2. La barra laterale nascosta.**
- Solo con la rotta ottimale aperta compare il pulsante **«Allarga la mappa»** nella barra della moviola, insieme al tasto **B**.
- La barra laterale del gioco sparisce, la mappa prende tutta la larghezza della finestra, e il riquadro del campo si ricalcola da solo.
- Lo stesso pulsante («Rimetti la barra») o B la rimettono.
- Quando la rotta ottimale si chiude (Esc, «Chiudi»), la barra torna sempre.
- Non c'entra lo schermo intero del browser, che resta F11 come oggi.

**Costanti nuove:** 60 s fra un filo e l'altro; colore e spessore del filo. Sono scelte nostre, di sola grafica, senza fonte.

## Criteri, con soglie fissate prima di provare

| # | Criterio | Soglia |
| --- | --- | --- |
| L1 | Ogni filo unisce due punti dello stesso istante: per ogni filo, il tempo del punto verde e quello del punto blu contati dal tuo taglio | differenza ≤ 1 fotogramma registrato, in tutte le regate provate (bastone, raffiche, salti, torneo; 5 semi ciascuna). Ci deve essere almeno un filo per regata: con zero fili il controllo non conta |
| L2 | Numero di fili | uguale ai minuti interi della rotta più corta fra le due |
| L3 | Barra nascosta | con B e col pulsante: larghezza della mappa = larghezza della finestra (±1 px), barra laterale non visibile; la vista del campo ricalcolata, con campo e tracce tutti dentro |
| L4 | Barra rimessa | B di nuovo, il pulsante, Esc o «Chiudi»: la barra torna, e la pagina è identica a prima di aprire la rotta (larghezze uguali al pixel) |
| L5 | Fuori dalla rotta ottimale | B non fa niente nel gioco, nella moviola normale e nelle lezioni; il pulsante non c'è |
| L6 | Pannello 1360×650 | 0 px di eccesso, con la barra e senza |
| L7 | Non-regressione | `polare.js` e `raffiche_e_virate.js` identici; `collaudo_rotta.py` come prima; le regate non cambiano, perché si tocca solo il disegno |
| L8 | Giocatore vero | in Chromium e Firefox, senza `#collaudo`: rotta aperta, B, fotografia della mappa allargata, B, Esc; 0 errori della pagina |

## Rischi

- **Fili che si incrociano** quando le due rotte vanno da parti opposte del campo: è giusto così, perché dice proprio che eri lontano. Ma con molte linee può diventare confuso. Lo guardo sulle fotografie e lo riporto; Ale dirà se è bello quando lo vede.
- **Tasto B:** oggi non è usato né nel gioco né nella moviola. Se servisse per altro in futuro, si cambia.
- **La barra nascosta cambia la misura della tela del gioco:** al ritorno il gioco deve ridisegnarsi giusto. Lo controllano L4 e L8.

## Cosa serve da Ale

Il via. Versione prevista: 1.2.32, oppure 1.2.33 se prima vengono i nomi dei rivali. Si toccano solo `js/rotta.js`, `js/moviola.js` per il tasto e il pulsante, e `index.html` per il pulsante e lo stile.
