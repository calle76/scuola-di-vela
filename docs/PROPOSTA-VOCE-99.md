# Voce 99 (oss. 155): colpa per la regola 15 e la Blu alla boa 1

28 novembre 2026. Via di Ale nella richiesta della sessione («prima riprodurre, poi correggere, con criteri scritti prima»). Criteri scritti **prima** di cambiare il codice.

## Riproduzione (fatta)

`registrazioni/regata-20261128-1434-intera.txt`, 380-397,48 s: le posizioni, le prue e le velocità registrate di Ale e della Blu ripassate nel gioco vero (`aggiornaPrecedenze`, `chiCede1516`, regata dei giri ruotata col vento a nord; script nella cartella di lavoro, copia in `sperimentale/voce-99/riproduci155.py`). Il gioco dà lo stesso esito del file: al 397,12 s la precedenza di base (regola 11) passa ad Ale; nessuna delle due cambia mure né vira, quindi l'«autore» del cambio è la più veloce, Ale (5,7 contro 5,3 nodi), e al contatto (397,48) la colpa è sua per la 15.

**Causa (a), la colpa.** Il cambio è fra «Ale sopravento» e «Ale sottovento» (11 → 11): la Blu attraversa la prua di Ale. Controprove: con la prua di Ale tenuta ferma da 396,2 s il cambio avviene lo stesso (397,45 s); con la prua della Blu ferma da 396,4 s pure (397,12 s). Lo fa il moto di lato della Blu (circa 2,5 m/s di traverso alla prua di Ale), non la velocità di Ale.

**Causa (b), la Blu alla boa.** Entrando in zona Ale le doveva spazio («zona Tu deve_spazio Blu», 386,64 s), ma la guida dei rivali non usa la regola 18 (voce 49 B, «non ora»): la Blu cede ad Ale (391-392,6 s), si scosta e finisce 3-5 m a sinistra della boa e pochi metri sotto. Lì `targetOf` (regola «da sinistra della boa», `sopraDaSinistra`) la manda al punto 2, 14 m sotto e 10 m a sinistra della boa: poggia fino a 20° (394,4 s), poi torna su, vira due volte e conta il giro solo a 416,9 s, 25,6 s dopo Ale.

## Correzione (a): chi ha causato un cambio di lato

Fra due barche affiancate con le stesse mure, quando la sopravento diventa l'altra (11 → 11) e nessuna delle due ha cambiato mure o virato, l'autore è la barca che ha portato l'altra dall'altro lato della prua di riferimento (quella di A, la stessa che usa `chiCede`): si confrontano il moto di lato di B rispetto alla prua di A (velocità per il seno della differenza delle prue) e la rotazione di A (velocità di rotazione della prua, misurata sull'ultimo mezzo secondo della sua storia, per la distanza di B lungo la prua di A). Gli altri cambi senza manovra (12 ↔ 11, cioè superare da dietro o restare indietro) restano come prima: la più veloce. Nessuna costante nuova (il mezzo secondo è una scelta nostra, dichiarata: due passi della storia delle prue).

**Criteri (soglie nostre):**

- **A1** la scena dell'oss. 155 ripassata: al 397,48 s la colpa non è di Ale (attesa: Blu, regola 11). Chromium e Firefox.
- **A2** due casi a mano nuovi in `collaudo_regole_15_16.py`: (15g) B, più lenta, attraversa la prua di A che va dritta: niente 15 per A; (15h) A, più lenta, gira la prua sopra B che va dritta e prende la precedenza: 15 per A (con la regola di prima il caso 15h darebbe «nessuna 15», per costruzione: A è la più lenta; non misurato).
- **A3** tutti i casi R1 di prima restano com'erano (R1 è scritto prima, nessuno cambia esito).
- **A4** la Scuola non cambia (R3) e i veloci (`polare.js`, `raffiche_e_virate.js`, `impronta1b.js`) restano identici.
- **A5** effetto nelle regate del torneo, lungo, giro «Misura» su GitHub, 150 + 150 semi (scelta 2261-2410, conferma 2411-2560), stessi semi col gioco com'è e con la patch: si riportano contatti per regola e colpa del pilota. **Soglie:** contatti in tutto non oltre +5%; colpa del pilota per la 15 non in aumento; arrivo mediano dei rivali entro ±2 s.

## Correzione (b): un punto 2 vicino

**Scena** (`sperimentale/voce-99/scena_boa.py`, rivale solo, 2-6 m a sinistra e 1-4 m sotto la boa, 48-68° dal vento, 20 varianti, Chromium): oggi 20 su 20 passano dal punto 2, scendono fino a 8,7-9,1 m sotto la boa e contano il giro in mediana a **23,5 s** (massimo 25,3; nella regata vera 25,6 s). La causa prima (cedere avendo diritto allo spazio) resta la voce 49 B, ferma per decisione di Ale.

**Correzione:** quando la regola «da sinistra della boa» scatta a meno di `R_DIR` (15 m, la costante del giro diretto) dalla boa, il punto 2 è vicino: 3 m a sinistra e 7 m sotto la boa, raggiunto entro 3 m (scelte nostre: da lì la retta verso il punto 0 passa almeno 4,5 m sotto la boa, sopra il margine `PASSO_SX` di 3 m). Più lontano dalla boa resta il punto 2 di prima.

**Criteri (scritti prima di provarla; soglie nostre):**

- **B1** scena, varianti 0-19 (scelta) e 20-39 (conferma, mai guardate): giro mediano ≤ 15 s; nessuna variante senza giro entro 90 s; nessuna boa toccata.
- **B2** `collaudo_avversari1b.py` scenario 5 non peggiore del gioco di oggi, Chromium e Firefox (stessi semi); `collaudo_giro_boa.py` verde.
- **B3** torneo lungo, giro «Misura», stessi semi di A5: arrivo mediano dei rivali entro ±2 s, contatti non oltre +5%, rivali non arrivati non in aumento.

**Esito B1 (28 nov, Chromium, varianti 0-19): non passa.** Punto 2 vicino (3 m a sinistra, 7 m sotto, entro 3 m): giro mediano **16,9 s** (da 23,5), massimo 18,1, tutte girano, nessuna boa toccata; soglia 15 s. Seconda prova, dichiarata dopo aver visto il primo numero (2 m a sinistra, 5 m sotto, entro 2 m, su una copia): mediana 16,5 s ma una variante a 48,5 s. Il tempo che resta è la risalita dopo il punto 2, non la discesa. **Non adottata**; la prova è in `sperimentale/voce-99/v99-a-e-b.patch` (con la (a)). Conferma (varianti 20-39) non lanciata: inutile dopo un no in scelta.

## Esito della correzione (a) (28 nov 2026): adottata nella 1.3.82

- **A1** scena dell'oss. 155: al contatto cede la Blu (regola 11), autore del cambio la Blu. Chromium e Firefox.
- **A2-A3** `collaudo_regole_15_16.py`: R1 19 casi su 19 (17 di prima e 15g, 15h), Chromium e Firefox; R3 Scuola 12 su 12 identiche alla 1.3.80.
- **A4** `polare.js`, `raffiche_e_virate.js` identiche; `impronta1b.js` 25 corse identiche.
- **A5** giro «Misura» (run 46163454685 e 46163462386, 450 + 450 regate lunghe): contatti 543 → 534 (−1,7%) e 466 → 462 (−0,9%); colpa del pilota 162 → 154 e 142 → 134, per la 15: 62 → 56 e 46 → 41; arrivo mediano +0,7 e +0,9 s; contatti per la 15: 172 → 160 e 140 → 135. Passa.
- **Da sapere:** cambiando l'autore cambia anche la guida dei rivali (usa `chiCede1516`). `esplora.py 28 28`: nella regata 103 esperti (sequenza intera nella stessa pagina) Pietro Gallo non arriva prima che si chiuda la regata; con la 1.3.81 arrivava. Da sola, la stessa regata arriva. Caso singolo di traiettoria diversa (giri di penalità alla partenza, ultimo tratto di lasco 137 m di lato); il conto dei non arrivati su 900 regate è nel giro della voce 92.
