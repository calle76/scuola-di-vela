# Proposta: gli avversari dell'1b che non partono

1 novembre 2026. **Fermata 1: solo documento, nessun codice del gioco toccato.** Ale ha scelto di sistemarlo prima delle lezioni (scelta A, 1 novembre). Si lavora sul ramo `pulizia`.

## 1. Che cosa succede (misurato)

Dalla 1.1.0 «Regata a bastone» e «Regata nelle raffiche» hanno gli avversari dell'1b. Il criterio (4) di `collaudo_partenze.py` chiede che nessun avversario resti senza partire 60 s dopo lo sparo, e ora cade:

| Dove | Barche non partite entro 60 s | Con gli avversari dell'1a (fino alla 1.0.78) |
|---|---|---|
| GitHub, Chromium (bastone e raffiche, principianti ed esperti, 60/180/300 s, semi 1-20) | 12 su 720 | 0 |
| GitHub, Firefox (stesso giro) | 6 su 720 | 0 |
| Qui, Chromium (solo principianti, 180 e 300 s, semi 1-20) | 11 su 240 | — |

Quasi tutte le barche sono principianti, con 3 o 5 minuti di preparazione. Prima nessuno se n'era accorto, perché il criterio (4) guarda solo bastone e raffiche, che erano della 1a. Nelle regate dei salti e dei giri e nel torneo gli avversari dell'1b non sono mai stati misurati così: **probabilmente il difetto c'è già anche lì.** È da misurare (criterio P2).

## 2. Due comportamenti, letti nel registro di 11 casi

**A. Due barche che si cedono a vicenda sulla linea.** Visto in tutti e 4 i casi del bastone: bastone 180 s seme 11; bastone 300 s semi 6 e 17. In ogni caso sono due barche insieme:
- Allo sparo le due barche sono affiancate, 5-8 m dietro la linea.
- Quella che deve cedere (nel seme 11 Blu, che cede a Rossa) poggia di 28° (`CEDE_A`).
- Quella con la precedenza resta entro una lunghezza e mezza e si scosta anche lei «all'ultimo momento» (35°).
- Tutte e due vanno al traverso, a 80-90° dal vento, parallele alla linea. Scivolano oltre la boa e tagliano fuori dagli estremi, dove non vale.
- Poi tornano, ma passano il resto del minuto a cavallo della linea.

**Causa probabile, letta nel codice e non ancora misurata.** In `cedeAvv1b` il «contatto in arrivo» si calcola dal punto più vicino fra le due barche, nell'ipotesi che tengano la rotta. Due barche parallele alla stessa velocità restano sempre alla stessa distanza: se questa è sotto le due lunghezze (8,4 m), il contatto risulta «in arrivo adesso» a ogni passo, anche se nessuna delle due si avvicina all'altra. Per questo la barca che cede continua a cedere e l'altra continua a scostarsi.

**B. Una barca che torna alla linea e poi ci naviga sopra.** Visto in tutti e 7 i casi delle raffiche, tutti principianti con 300 s:
- A 5 s dallo sparo la barca è già quasi sulla linea (0,3-0,8 m), al traverso e a circa 2 nodi, ancora senza il «via».
- Passa la linea prima dello sparo e viene richiamata.
- Torna indietro e poi naviga **lungo la linea**, a meno di 0,2 m, al traverso e a 6-7 nodi, per 30-40 s.
- La barca passa e ripassa la linea, ma mai nel verso giusto in un punto valido: il richiamo si accende e si spegne.

**Causa da trovare.** Le ipotesi sono due:
- il punto a cui punta la logica generale dopo il richiamo, che la porta sulla linea invece che dietro;
- l'attesa troppo vicina alla linea nella regata con le raffiche, dove le raffiche spingono la barca avanti.

La prima cosa della fermata 2 è misurarlo.

## 3. Che cosa propongo (correzioni più piccole, solo nella guida degli avversari)

- **A.** In `cedeAvv1b`, una barca cede o si scosta solo se l'altra **si avvicina davvero**: la distanza deve diminuire più di una soglia al secondo, oppure gli scafi devono essere già a meno di una lunghezza. Due barche parallele che non si avvicinano non cedono più: ognuna tiene la sua rotta verso la linea. **Costante nuova:** la soglia di avvicinamento, un'ipotesi nostra. Si sceglie sui semi 1-20 e si conferma sui semi 21-40, mai guardati.
- **B.** Prima si misura la causa. Poi si fa la correzione più piccola che fa **tagliare** la linea a chi torna dopo il richiamo, invece di farla seguire: per esempio un punto di mira qualche metro dietro la linea e dentro gli estremi. Questa correzione la descrivo con i numeri prima di scriverla nel codice.
- **Cosa non si tocca:** la fisica (impronta dell'1b al bit), le regole e chi cede (`chiCede`), la logica di partenza dell'1a (che non c'è più), i giri di penalità degli avversari.

## 4. Criteri (soglie scritte prima, attese nostre)

- **P1, partono tutti:** criterio (4) di `collaudo_partenze.py` con **0 barche non partite** su 720 per browser, Chromium e Firefox. Il metro dichiara quante barche ha contato, e devono essere 720.
- **P2, anche nelle altre regate dell'1b:** lo stesso conteggio, nuovo, su salti di vento e giri di penalità (principianti ed esperti, 60/180/300 s, semi 1-20). Si misura **prima** e dopo la correzione. Dopo: 0 non partite.
- **P3, non si urta di più:** contatti per regata in 80 regate di bastone e raffiche (arrivi_regate, semi 1-40), prima e dopo. L'aumento ammesso è al massimo del 20%: è un'attesa nostra, perché cedere meno può voler dire toccarsi di più. Si riportano anche le penalità date agli avversari, senza soglia.
- **P4, il resto delle partenze non peggiora:** gli altri criteri di `collaudo_partenze.py` (richiami, ritardo mediano entro 3 s, velocità) dentro le loro soglie, come oggi.
- **P5, non-regressione:** `impronta1b.js` al bit. Restano come oggi:
  - `collaudo_avversari1b.py`: scenario 5 a 7 su 10, gli altri a 10 su 10;
  - `collaudo_regole.py`, `collaudo_semaforo.py`, `collaudo_giri_avversari.py`;
  - `collaudo_regate.py`: 18 arrivi su 18, nessuna barca bloccata.

## 5. Rischi

- La guida degli avversari dell'1b vale in tutte le regate e nel torneo: **cambiano gli arrivi delle regate dei salti e dei giri e del torneo** (`arrivi_regate.py` non sarà più identico). È voluto, e si dichiara; la soglia del torneo si tara dopo (passo 4).
- Cedere meno può portare più contatti fra avversari (P3).
- B ha la causa ancora da trovare: se la correzione non è piccola, mi fermo e lo dico prima di scriverla.

## 6. Fatto (1.1.1, 1 novembre 2026)

Esito con i numeri nel `CHANGELOG.md`, alla voce 1.1.1. Sui semi 1-20 le barche non partite passano da 25 a 0 su 1440; sui semi 21-40 di conferma ne resta 1 su 1440, e la soglia 0 lì non è raggiunta. I contatti crescono del 12,7%, dentro la soglia del 20%.

La correzione B è diversa da quella scritta al §3. La causa misurata non era la mira dopo il richiamo. Erano due cose: un'altalena attorno alla soglia di 1,1 m/s per prendere abbrivio (B1), e la prua di partenza che porta fuori dall'estremo vicino alla boa (B2). La versione del §3 l'ho provata e tolta: creava un giro attorno alla boa.
