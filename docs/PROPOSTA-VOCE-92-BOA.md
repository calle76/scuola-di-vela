# Voce 92: lo scenario 5 di `collaudo_avversari1b` in Firefox (un rivale non gira la boa)

28 novembre 2026. Via di Ale nella richiesta della sessione. Criteri scritti **prima** di cambiare il codice.

## Riproduzione (fatta)

Gioco 1.3.81 (copia da `git archive`), Firefox: 7 su 10 come nel giro GitHub (varianti 1, 2 e 3 con una barca su tre senza giro). Anche con la correzione (a) della voce 99: 7 su 10.

**Causa (traccia della variante 1, Blu, secondo per secondo):** a 31 s la Blu è a sinistra della boa e sotto (`sopraDaSinistra`): va al punto 2 e a 34 s riparte verso il punto 0, segnando `b.p2`. Poi cede alla Rossa, che scende dopo il giro, e finisce 27 m a sinistra e quasi all'altezza della boa. Da lì la retta verso il punto 0 passa **sopra** la boa: la Blu la attraversa da sinistra a destra 1,3 m sopra (51 s), nel verso sbagliato, e il conto del giro si annulla; rientra, rifà il giro e a 70 s non ha ancora finito. Con `b.p2` la regola «da sinistra della boa» non può più scattare: è stata spenta così nella 1.2.27 (`archivio/PROPOSTA-BOA-PIANTATA.md` §12) per un rimbalzo fra punto 2 e punto 0 con la retta appena dentro il margine `PASSO_SX` (3 m).

## Correzione

Dopo il punto 2 (`b.p2`) la regola torna a valere, ma con margine 0 invece di `PASSO_SX`: solo se la retta verso il punto 0 passa sopra il centro della boa. Il rimbalzo del §12 (retta 0-3 m sotto la boa) resta escluso. Interruttore `V92` (false = come fino alla 1.3.81). Nessuna costante nuova.

## Criteri (soglie nostre)

- **C1** `collaudo_avversari1b.py` scenario 5 in Firefox: almeno 9 su 10.
- **C2** `collaudo_avversari1b.py` intero, Chromium e Firefox: tutti gli scenari almeno 9 su 10.
- **C3** il caso del §12 (seme 28, regata 2, esperti, Chromium, `tests/esplora.py 28 28`): la Verde arriva.
- **C4** torneo lungo, giro «Misura», stessi semi della voce 99: rivali non arrivati non in aumento, arrivo mediano entro ±2 s.

## Esito (28 nov 2026): non adottata (C4 non passa)

- **C1** Firefox scenario 5: 9 su 10 (prima 7). La variante 2 resta senza giro per un'altra causa: per scendere al punto 2 la guida usa il ramo «bersaglio in poppa» con le abbattute a tempo, e nel collaudo il bordo non scade mai (`boardMax` 999): la Blu va di lasco fino a 40 m a sinistra prima di tornare.
- **C2** `collaudo_avversari1b.py` intero: Chromium 10/10 in tutti gli scenari; Firefox 10/10, scenario 5 9/10.
- **C3** `esplora.py 28 28`: la Verde della regata 2 arriva.
- **C4** giro «Misura» (run 46165684057 e 46165691339, insieme alla correzione (a) della voce 99, contro la 1.3.81): rivali non arrivati **507 → 514 e 466 → 470** (soglia: non in aumento), **non passa**; arrivo mediano +1,6 e +1,0 s, contatti −1,8% e −0,4%. Con la sola (a) (voce 99, A5): 507 → 513 e 466 → 464; la parte della voce 92 aggiunge +1 e +6.
- Il codice è in `sperimentale/voce-99/v99-e-92.patch` (con la (a)). Scelta per Ale: lasciarla così (scenario 5 rosso in Firefox, 7 su 10) o accettare il piccolo aumento dei non arrivati.
