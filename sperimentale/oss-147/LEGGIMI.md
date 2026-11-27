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

## Esito della prima prova (`r16-prua-di-adesso.patch`): non adottata

Giro «Misura», Chromium, 450 regate per gruppo (il gioco dà gli stessi numeri in due giri: misura ripetibile). Gioco → prova:

| | Scelta 2261-2410 | Conferma 2411-2560 | Soglia |
| --- | --- | --- | --- |
| K1 rivale colpevole per 15-16 | 172 → 151 (−12%) | 149 → 152 (+2%) | −40% / −25%: **no** |
| di cui dopo il via, per la 16 | 37 → 24 | 26 → 27 | (non scritto prima) |
| K2 contatti | 579 → 546 | 496 → 515 (+3,8%) | +10%: sì |
| K3 bolina esperti barca per barca | mediana +0,0, media +0,6 s | +0,0, +0,25 s | +2 s: sì |
| K3 M4 (mediana delle mediane dei pezzi) | 587,1 → 586,2 | 587,9 → 588,3 | +2 s: sì |
| K5 coppie dopo il via | 35 → 33 | 28 → 35 (+25%) | +20%: **no** |

K1 era scritto male: conta anche i contatti prima del via (90 e 86, uguali nelle due versioni), dove la correzione non agisce. Soglia lasciata com'è. Causa del fallimento: la correzione agisce quando la 16 è già scattata, a virata fatta.

## Seconda prova (`r16-v2-non-girare-verso.patch`, contiene anche la prima)

Chi ha la precedenza (dopo lo sparo, in Deriva), con una barca vicina che deve cedergli, non gira la prua verso di lei: se la rotta voluta è almeno G147 = 5° (ipotesi nostra) più vicina alla direzione dell'altra, tiene la prua che ha. Prima, «tenere la rotta» voleva dire seguire la rotta voluta, che girando la boa è una virata verso l'altra.

Criteri: gli stessi K1-K5, più **K1b, scritto prima di vedere i numeri di questa prova:** contatti con colpa di un rivale per la regola 16 dopo il via, almeno −30% sulla scelta e −20% sulla conferma. K4 sul PC, Chromium: 80, 81, 82, 83 tutti 10 su 10 (80: minimo 140-142° contro 143-150°, soglia 60°).

## Esito della seconda prova: non adottata

Gioco → prova. Scelta 2261-2410 (450 regate): K1 172 → 139 (−19%, **no**); **K1b 37 → 22 (−41%, sì)**; K2 579 → 516 (sì); K3 bolina esperti barca per barca mediana +0,0, media +1,2 s, M4 587,1 → 586,4 (sì); **K5 coppie dopo il via 35 → 54 (+54%, no)**: tutte fra stesse mure, in bolina da 15 a 30 (il rischio detto da Ale prima dei numeri). Conferma 2411-2560: un pezzo (2531-2540) fallito su GitHub mentre installava il browser, 420 regate contro 450: K1b 26 → 21, K5 28 → 40; non confrontabile alla pari, non serve per la decisione.

I contatti per la 16 dopo il via, nel gioco, sono per metà fra mure diverse (17 su 37 e 10 su 26); le coppie sono tutte fra stesse mure.

## Terza prova (`r16-v3-mure-diverse.patch`, contiene la prima)

Come la seconda, ma solo fra barche con le **mure diverse** (come la 1.3.71) e per al massimo T15 = 5,2 s (la finestra della regola 16 del gioco) per la stessa barca. Criteri: gli stessi K1-K5 e K1b, soglie invariate. K4 sul PC, Chromium: 80, 81, 82, 83 tutti 10 su 10.
