# Oss. 147: chi ha la precedenza gira la boa e prende la regola 16 (voce 2)

27 novembre 2026, sera. `js/` invariato finché i criteri non passano.

## Causa (letta nel codice, `js/regate.js`, `cedeAvv1b`)

Quando la regola 16 (o la 15) toglie la precedenza a un rivale che l'aveva per le regole 10-13 (ha girato verso l'altra barca), la guida lo tratta come chiunque ceda: prova gli scarti partendo dalla **rotta che vuole**. Mentre gira la boa di poppa, la rotta voluta è la bolina: «poggiare di 15°» da lì resta un'orzata di 45-60° rispetto alla prua che ha, cioè ancora verso l'altra (regata 1030, Blu da 77° a 120° di prua e contatto).

## Correzione provata (`r16-prua-di-adesso.patch`)

Solo per chi cede **per le regole 15 o 16** (la precedenza di base era sua): gli scarti partono dalla prua di quando ha cominciato a cedere (`cedeH`), con anche lo scarto 0 (tenere quella prua), e la direzione preferita è lontano dall'altra barca. Nessuna costante nuova. Scuola invariata (lì le regole 15-16 non ci sono).

## Criteri (soglie nostre, scritte prima di vedere i numeri del gioco e della prova)

Torneo lungo, giro «Misura» su GitHub, `misura_r16.py --conf m4 --lungo`, Chromium; scelta sui semi 2261-2410 (450 regate), conferma sui semi 2411-2560 mai guardati con la prova.

- **K1, il caso:** contatti con colpa di un rivale per le regole 15 o 16: almeno −40% sulla scelta e −25% sulla conferma. Se il gioco ne ha meno di 10 su 450 regate lo strumento non distingue: si dichiara.
- **K2:** contatti in tutto al massimo +10%.
- **K3:** bolina degli esperti, barca per barca, mediana al massimo +2 s; arrivo mediano dei rivali (M4) al massimo +2 s.
- **K4:** casi 80-83 di `collaudo_avversari_deriva.py` almeno 9 su 10 (con la prova, PC, Chromium: 10, 10, 10, 10).
- **K5:** coppie dopo il via al massimo +20%.
