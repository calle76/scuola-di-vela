# Proposta: torneo ampliato, giri di penalità e vento misto (9 novembre 2026)

Voce 2 di `DA-FARE.md`. Decisione di Ale del 9 novembre (`DECISIONI.md`): «ampliare il torneo, ci sono regate con punti di penalità e aggiungiamo quelle con giri di penalità». Domanda di Ale: «ogni gara ha una particolarità, salti di vento o raffiche. Ma nella realtà non c'è tutto assieme?»

**Fermata 1: niente codice finché Ale non dà il via.**

## 1. Com'è oggi (letto nel codice, `js/regate.js`, sezione torneo)

- **Regate.** Il torneo ha 4 regate, sempre con la penalità sul punteggio: +1 contatto con colpa vale il 20% dei punti di chi non arriva (regola 44.3).
  - Le regate 1 e 3 sono a bastone, la 2 e la 4 a triangolo.
  - Le condizioni sono «10 nodi costanti», «raffiche» (12 nodi) e «salti di vento». La quarta regata è sorteggiata fra le tre.
- **Le regate con i giri ci sono già fuori dal torneo** (1.0.61-1.2.18), sia per il giocatore sia per gli avversari:
  - due giri per un contatto con colpa, uno per la boa toccata (solo il giocatore);
  - squalifica per chi arriva coi giri non fatti.
- **Il vento.**
  - Le raffiche portano già un piccolo cambio di direzione: ognuna gira il vento fino a ±6° (fino a ±10° per le raffiche forti), più un'oscillazione lenta di circa ±4,5°.
  - I «salti» sono un'altra cosa: un'oscillazione di una dozzina di gradi ogni due minuti circa, oppure una rotazione sempre dalla stessa parte (una regata su tre).
  - Oggi raffiche e salti non stanno mai insieme.

## 2. La domanda di Ale: raffiche e salti insieme

Sì, nella realtà di solito stanno insieme. Le fonti trovate sono articoli di riviste di regata e forum (secondarie, da aggiungere a `FONTI-PUBBLICHE.md` se si adotta):
- spesso la raffica arriva con un cambio di direzione (salto sul fronte della raffica);
- con vento medio e forte conviene giocare soprattutto i salti, con vento leggero soprattutto le raffiche.

Fonti: [Speed & Smarts, «Go for puffs in light air, shifts in breeze»](https://canadianboating.ca/sailing/racing/speed-smarts-go-for-puffs-in-light-air-shifts-in-breeze/), [Sailing World, «Why wind shifts matter more than you think»](https://www.sailingworld.com/racing/why-wind-shifts-matter-more/), [forum Daysailer](https://forum.daysailer.org/forum/viewtopic.php?p=33170).

Le condizioni separate restano utili per **imparare** una cosa alla volta, come fa la Scuola. Nel torneo invece una condizione mista è più vicina al vero.

## 3. Modello più semplice

**A. Regate con i giri nel torneo.** Il torneo resta di 4 regate:

| Regata | Penalità | Percorso |
| --- | --- | --- |
| 1 | punteggio | bastone |
| 2 | punteggio | triangolo |
| 3 | giri | bastone |
| 4 | giri | triangolo |

- Prima i punti, poi i giri, così ogni sistema di penalità si prova sia a bastone sia a triangolo. Dipende solo dal numero della regata, come oggi il percorso.
- **Nelle regate con i giri:**
  - si usa la regata dei giri che esiste già: stesse regole, stesse bandiere, stessi avversari che scontano;
  - nessuna penalità sul punteggio;
  - chi è squalificato per i giri non fatti prende i punti di chi non arriva (5, come il ritiro; appendice A5.2).
- **Tabella dei risultati:** un segno nuovo per la squalifica («Sq»).
- **Il punto in più dei meriti** «senza penalità» vale se non ci sono né punti di penalità né giri da fare.

**B. Condizione mista «raffiche e salti».** Una quarta condizione: 12 nodi con raffiche e salti insieme. È solo l'unione delle due che esistono, senza costanti nuove. La quarta regata, che oggi si sorteggia fra tre condizioni, diventa sempre «raffiche e salti»: l'ultima regata è la più completa.

**Cosa non si tocca:** la fisica, chi cede, la guida degli avversari, il tempo fra regate, lo scarto, la finestra d'arrivo, le regate fuori dal torneo.

**Rischi:**
- Due regate su quattro coi giri allungano il torneo: i giri costano tempo.
- Con raffiche e salti insieme gli avversari potrebbero fare più contatti (misurato: nei salti fuori torneo +25% con la 1.2.19).
- Un torneo salvato a metà con la versione vecchia deve continuare con le sue regate: si legge il campo `ver` già salvato.

## 4. Criteri (soglie nostre, scritte prima di misurare)

Misura con lo strumento delle regate del torneo (`misura_boa_avversari.py` esteso), giocatore guidato dal pilota, principianti ed esperti. Scelta delle soglie sui semi 921-950, conferma sui 951-980.

- **T1, funziona:** `collaudo_torneo.py` verde, con casi nuovi:
  - regata 3 e 4 coi giri;
  - squalifica che vale 5 punti;
  - torneo vecchio salvato a metà che continua come prima;
  - tabella con «Sq».
- **T2, squalifiche degli avversari** nelle regate con i giri del torneo: al massimo il 5% delle barche. Se sono di più, gli avversari non riescono a scontare in gruppo.
- **T3, durata:** arrivo mediano delle regate coi giri al massimo +15% rispetto alle stesse regate col punteggio.
- **T4, vento misto:** contatti dopo il via al massimo +15% rispetto alle raffiche sole, e nessun aumento delle non arrivate.
- **T5, non-regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; le regate fuori dal torneo invariate.
- **T6, pannello** a 1360x650 senza pixel in eccesso con la tabella del torneo nel caso peggiore.

## 5. Cosa serve da Ale

1. **Il via, oppure un ordine diverso delle regate** (per esempio giri nelle regate 2 e 4).
2. **Visibile subito o nascosto?** Il torneo oggi si apre nella Scuola, dopo l'attestato. La decisione del 4 novembre vuole il lavoro su Deriva nascosto. Si può:
   - cambiare il torneo per tutti, con la versione 1.2.21;
   - tenerlo dietro una prova nascosta finché Deriva non si apre.

   Raccomando di cambiarlo per tutti: è il torneo che diventerà quello di Deriva, e così le regate di Ale e Lucio lo provano subito.

## 6. Costo

Circa mezza giornata: codice del torneo e testi (breve, lezione del torneo), collaudo esteso, poi la misura col termostato (circa 2 ore di calcolo).
