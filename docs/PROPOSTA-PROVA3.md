# Proposta: prova 3 del giro di boa, «linea d'arrivo» (fermata 1, 17 ottobre 2026)

## Il fatto

`collaudo_giro_boa.py`, prova 3 (una sola boa, la linea d'arrivo, nessuna boa da girare): **NON finisce**, in 169 secondi, con il pilota che si ferma a 88. Stessa cosa il 16 ottobre (169 s); l'11 ottobre finiva (197 s). Le prove 1 e 2, con lo stesso pilota, finiscono (79 e 135 s).

## Cosa abbiamo misurato (copia del gioco, 3 semi, nessuna modifica)

La barca si ferma **6-10 metri prima** del punto d'arrivo (`dist` 9,7 / 6,2 / 6,2) e il pilota smette di guidarla. Il pilota ha come ultimo punto il **centro della linea d'arrivo**, e passa al passo successivo quando è entro 7 metri: con quel punto era l'ultimo, e da lì non dà più ordini. La barca va avanti per inerzia a 1-1,5 nodi e non attraversa la linea. Il collaudo legge il risultato 2 secondi dopo e lo segna come «non finita».

## Storia (aggiunta dopo la domanda di Ale: «non era già stato corretto?»)

Il difetto è **noto dalla 1.0.10**: `CHANGELOG.md` lo chiama «difetto vecchio del collaudo», non del gioco, e non è mai stato corretto. Quello che è già corretto è un caso vicino: dalla 0.21.4 gli **avversari** dopo l'arrivo vanno nella zona di sosta, 25 metri oltre l'estremità della linea e 30 dietro (`docs/PROGETTO.md`, riga 109; osservazione 37 in `OSSERVAZIONI-GIOCANDO.md`). Il **pilota di prova** del collaudo non ha mai avuto una regola simile: si ferma sul punto d'arrivo. Nel gioco per il giocatore non serve, perché la prova si chiude al taglio della linea (`finCross` in `js/gioco.js`).

## Perché pensiamo che sia il collaudo e non il gioco

- Le prove 1 e 2 arrivano alla linea con lo stesso pilota e finiscono: il meccanismo di arrivo funziona.
- Un giocatore non si ferma sul punto: taglia la linea e tutto quello che c'è dietro.
- COLLAUDI.md lo dice già: «il pilota automatico è volutamente semplice: se non arriva, controlla dove si è fermato».

## Ipotesi da verificare (non ancora provata)

Il pilota deve **puntare un punto oltre la linea** (per esempio 25 metri oltre) e continuare a guidare finché il gioco non dichiara la prova finita o scatta il tempo massimo. Così tagliare la linea diventa parte del percorso invece di una fermata.

## Criteri (scritti prima di provare)

1. **Prova 3 finisce** in almeno **3 semi su 3** (semi 1-3, sul codice attuale), entro il tempo massimo già previsto.
2. **Prove 1, 2, 4 e 5 non cambiano esito**: stesse finali, stessi giri sbagliati (1 nei casi sbagliati, 0 in quelli giusti).
3. **Il gioco non viene toccato**: `index.html` e `js/` identici a prima; si cambia solo `collaudo_giro_boa.py`.
4. **Il metro misura davvero**: il collaudo stampa a che distanza dal punto d'arrivo si ferma il pilota; se la distanza è sotto 7 metri in tutti i semi, il criterio 1 non vale, perché vuol dire che non è cambiato niente.

## Rischi

- Se la prova 3 finisce con il pilota modificato ma il gioco ha un difetto vero di arrivo (per esempio una linea che non si attraversa mai da un certo lato), il collaudo lo nasconderebbe. Il criterio 4 serve a questo: confermare che la barca passa davvero la linea, non che il collaudo dica «finita».
- Il pilota diventa un po' più complicato da leggere: va commentato in modo chiaro.

## Passi successivi (dopo il via)

Fermata 2: modifica del solo pilota, tre semi, poi le prove 1-5 del giro per la regressione. Nessuna modifica al gioco, quindi nessuna nuova versione.

## Esito (fermata 2, 17 ottobre 2026): fatto, solo nel collaudo

**Fatto:** `collaudo_giro_boa.py`, quando il traguardo diventa il punto da raggiungere, aggiunge un punto 25 metri oltre, sulla direzione da cui si arriva. Il collaudo stampa anche la distanza dal punto d'arrivo (criterio 4). Il gioco non è stato toccato (`index.html` e `js/` identici).

| Criterio | Esito |
| --- | --- |
| 1. prova 3 finisce, 3 semi su 3 | **rispettato**: 157 / 156 / 157 s |
| 2. prove 1, 2, 4, 5 non cambiano esito | **rispettato** (vedi sotto, dopo un primo tentativo sbagliato) |
| 3. gioco non toccato | **rispettato** |
| 4. il metro misura | **rispettato**: il pilota finisce a 14-15 m **oltre** il punto d'arrivo, prima a 6-10 m prima (soglia: sotto 7 m in tutti i semi = nessun cambiamento) |

**Primo tentativo, sbagliato:** il punto oltre il traguardo lo calcolavo dalla direzione partenza-traguardo. Nella prova 3 va bene, ma nella prova 4 si risale fino alla boa e poi si torna, quindi partenza e traguardo sono vicini e la direzione risultava sbagliata: **le prove 4 «boa a sinistra» e «sbaglia e rimedia» non finivano più** (prima 310 e 345 s). Il criterio 2 ha preso l'errore. Ora il punto si calcola nel momento in cui il traguardo diventa il bersaglio, dalla posizione di allora.

**Prove dopo la correzione** (un giro completo): prova 4 boa a sinistra finita in 310 s, boa a dritta non finita con 1 giro sbagliato, sbaglia e rimedia finita in 345 s con 1 giro sbagliato; prova 5 triangolo finita in 298 s, boa 2 a dritta non finita con 1 giro sbagliato; prove 1 e 2 finite in 79 e 135 s.
