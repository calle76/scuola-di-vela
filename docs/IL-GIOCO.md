# Il gioco, in una pagina

**Scritto il 6 novembre 2026. Se un altro documento dice una cosa diversa, vale questo** (è il passo 7 di `PROPOSTA-RIORGANIZZAZIONE.md`). Il dettaglio delle decisioni sta in `DECISIONI.md`, lo stato delle versioni in `CHANGELOG.md`.

Accanto a ogni cosa: **[fatto]** è nel gioco; **[deciso]** l'ha deciso Ale, ma non è ancora nel gioco; **[proposta]** aspetta il via; **[da misurare]** è un'ipotesi nostra.

## 1. Cos'è

Un simulatore didattico di vela in una pagina, da giocare sul computer con la tastiera. Prima simulatore, poi gioco. Progetto personale, non commerciale, nessun valore legale. I principi stanno in `PROGETTO.md`.

**Gioco libero e carriera.** Nel gioco libero è sempre tutto aperto, a ogni livello. In carriera i livelli si aprono uno dopo l'altro. **[fatto per la Scuola]**

## 2. I livelli

Ogni livello ha una sola novità grande.

| Livello | Barca | Novità | Stato |
| --- | --- | --- | --- |
| **La scuola** | deriva in singolo | tutta la teoria, le regole, le prove | **[fatto]**, chiusa come contenuti (Ale, 13 novembre 2026): niente da aggiungere, solo cose da sistemare rigiocando |
| **Deriva** | la stessa, senza fiocco | gareggiare e rivedersi | **[proposta]**, `PROPOSTA-LIVELLO-DERIVA.md`; nascosta finché Ale non dice di mostrarla |
| **Fiocco** | deriva a due, randa e fiocco | il fiocco | prototipo in `sperimentale/`, non nel gioco |
| Dopo | gennaker, equipaggio da tre | una per volta | solo una direzione (`VISIONE-LIVELLI-E-CARRIERA.md` §2) |

## 3. Come si passa al livello dopo

| | La scuola | Da Deriva in poi |
| --- | --- | --- |
| **Cosa serve** | punti (totale e minimo in ogni area), poi l'esame | **due strade**, vedi sotto |
| **Esame** | sì | no |
| **Riconoscimento** | l'attestato, uno solo | nessuno: il gioco lo dice e si apre il livello dopo |
| **Punti** | restano nella Scuola | ogni livello ha i suoi, non si portano dietro |

**Le due strade (Ale, 6 novembre 2026) [deciso]:**

- **Del piazzamento:** arrivare fra i primi tre nel torneo. **[da misurare]**
- **Del merito:** finire il torneo senza ritirarsi **e** avere quasi tutti i punti del livello. **[da misurare]**

Senza finire il torneo non si passa mai. Ripetere una cosa senza migliorare non dà punti, quindi non si passa solo insistendo. I numeri si fissano dopo aver corretto gli avversari, col pilota, su gruppi di semi diversi.

**Le quattro aree, da Deriva in poi [deciso]:**

| Area | Da cosa |
| --- | --- |
| Esperienza | lezioni del livello, regate finite, il momento clou rivisto la prima volta |
| Conoscenza | quiz del livello; dal Fiocco anche le domande del coach |
| Competizione | piazzamenti nelle regate e nel torneo |
| Abilità | prove con medaglie del livello; dal Fiocco anche le manovre da rifare riuscite |

**Il cono d'ombra (1.2.25) [deciso]:** nel torneo, e poi in Deriva, le vele si tolgono il vento (`PROPOSTA-CONO-D-OMBRA.md`); il cono disegnato sul mare è un aiuto disattivabile, la fisica no. Scuola, prove e lezioni restano senza.

**Il coach (Ale, 6 novembre 2026) [deciso]:** in Deriva registratore, moviola e momento clou da rivedere, mai obbligatorio; dalla 1.2.22, fuori dalla Scuola, la **rotta ottimale** a regata finita con le layline e «dove hai perso» (`PROPOSTA-ROTTA-OTTIMALE.md`). Dal Fiocco domande e manovre da rifare, con un tetto di punti: nascono dagli errori, quindi non possono essere obbligatorie, e nel torneo una penalità deve costare più di quanto si recupera col coach.

## 4. Deriva non è un doppione della Scuola (Ale, 6 novembre 2026) [deciso]

- **Niente esame, niente attestato, nessuna regola di passaggio uguale.** Nella Scuola bastano punti ed esame; in Deriva senza il torneo non si passa.
- **Solo contenuti nuovi.** Lezioni: come funziona il torneo e come rivedere la regata; le regole già insegnate non si ripetono.
- **Una sola prova con medaglie, i giri di penalità, diversa dall'esercizio della Scuola:** lì si tocca una boa e si fa un giro, senza tempo e senza salvare niente; qui si fa un percorso a tempo con i giri da scontare. Dettagli in `PROPOSTA-LIVELLO-DERIVA.md` §3.
- **Punti propri.** I punti della Scuola non contano in Deriva.

## 5. Regole fisse del lavoro

Stanno in `CLAUDE.md` e `METODO.md`: due fermate, soglie scritte prima, commit a collaudi verdi, push di Ale, nessuna persona esperta da consultare (valgono fonti scritte e video). Deriva resta nascosta o su un ramo a parte, e chi apre il gioco non la vede.
