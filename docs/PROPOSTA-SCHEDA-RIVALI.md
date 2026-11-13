# Proposta: la scheda dei rivali, primo passo (fermata 1, 12 novembre 2026)

**Stato: proposta. Nessun codice toccato. Aspetta il via di Ale.**
Nasce dalle risposte di Ale del 12 novembre sulla `PROPOSTA-RIVALI-E-SPONSOR.md`: i rivali restano gli stessi per tutto il torneo (deciso, `DECISIONI.md`), la memoria parte «solo mostrata», si procede a piccoli passi.

## 1. Cosa c'è già (letto in `js/regate.js`, versione 1.2.29)
- Nel torneo i tre avversari restano gli stessi per tutte e 4 le regate, con gli stessi parametri e lo stesso carattere (`regate.js:169`, `torNuovo`). La decisione di Ale è quindi già vera nel codice.
- Il carattere (prudente, normale, aggressiva) si dice prima della regata e nella classifica (`regate.js:190` e `1295`).
- Dopo ogni regata il torneo salva per ogni barca: tempo d'arrivo (o niente), punti di penalità, giri non fatti, squalifica (`tor.ris`, `regate.js:1260`), dentro `progress.torneo`.
- **Non c'è** nessun fatto su partenza, boa 1 e contatti per singolo rivale: oggi i rivali sono tre colori con un carattere.

## 2. Il passo (modello più semplice)
Una **scheda per rivale**, che si riempie a ogni regata del torneo e si vede a fine regata. Solo fatti misurati dal gioco, **memoria solo mostrata**: la guida degli avversari non cambia di un bit.

Fatti proposti, quattro:
1. **Arrivo**: posizione in ogni regata già corsa (c'è già).
2. **Partenza**: se ha attraversato la linea prima o dopo di te, e se è partita in anticipo (fuori linea). Dato nuovo.
3. **Prima boa**: se l'ha girata prima o dopo di te. Dato nuovo.
4. **Contatti**: se c'è stato un contatto con te, e di chi era la colpa. Dato nuovo.

Frasi: scritte dal gioco, solo sui fatti, per esempio «Rossa: davanti a te alla partenza in 2 regate su 3». Con una sola regata si dice «una volta». Niente giudizi («è forte»): solo conteggi.

Nessun salvataggio fra tornei in questo passo: la scheda vive col torneo, come oggi i risultati. L'identificativo del rivale (il colore) e un campo `storico` per regata sono già pensati per essere salvati dopo, senza rifare niente.

## 3. Criteri misurabili (soglie nostre, dichiarate prima)
1. **La guida non cambia.** Su 40 tornei interi a semi fissi (160 regate), tempi d'arrivo uguali al bit con e senza il nuovo codice. I dati nuovi non devono consumare numeri casuali.
2. **La scheda dice il vero.** Su quegli stessi 160 regate, ogni fatto (partenza, boa 1, contatti) confrontato col registro della regata (`tests/analizza_registro_torneo.py`): zero righe che non tornano. Il controllo riporta quante righe ha confrontato, perché un «zero errori» vale solo se ha misurato (`CLAUDE.md`).
3. **Torneo a metà.** Chiudere la pagina dopo la regata 2 e riaprirla: scheda identica. Un torneo salvato prima di questa versione (senza i campi nuovi) si apre senza errori e con la scheda vuota.
4. **Pannello** a 1360x650 senza pixel di eccesso, anche nel caso peggiore (3 rivali, 4 regate, contatti in tutte).
5. **Collaudo guidando davvero la barca** (pilota automatico, `#collaudo`) e in una pagina caricata come la carica Ale; Firefox compreso.
6. `polare.js`, `raffiche_e_virate.js`, `impronta1b.js`: invariati (non si tocca il motore).

## 4. Costanti nuove
- **Quando una frase passa da «una volta» a «in X regate su Y»**: a partire da 2 regate. **Ipotesi nostra**, nessuna fonte.
- Nessun'altra costante.

## 5. Rischi
- **Spazio nel pannello di fine regata.** È il rischio principale: tre schede di quattro righe non entrano senza una finestra o un'altra schermata. Da decidere dove va (domanda 1).
- **Un fatto singolo sembra un carattere.** Se la Rossa parte avanti per caso, la scheda sembra dire che è una partenzista. Per questo le frasi sono conteggi e non etichette, e il carattere vero (già dichiarato) resta separato.
- **Nella Scuola** il torneo non c'è: nessun effetto. Fuori torneo (regate singole) la scheda non compare.

## 6. Cosa questo passo NON fa
Nuovi tratti in acqua (errori, scelta del lato), memoria che cambia il comportamento, salvataggio fra tornei, fasce, sponsor, salita e discesa, compagni di equipaggio. Ognuno è un passo a sé (`PROPOSTA-RIVALI-E-SPONSOR.md`).

## 7. Versione e costo
1.2.30. Costo medio: dati nuovi in `regate.js`, la scheda nel riquadro del torneo, 2-3 collaudi nuovi. Il motore non si tocca.

## 8. Domande per Ale
1. **Dove si vede la scheda?** A fine regata (accanto al risultato), a fine torneo, o in una schermata a parte dal menu del torneo?
2. **Bastano questi quattro fatti** (arrivo, partenza, boa 1, contatti), o ne togli o aggiungi?

**Risposte di Ale (12 novembre, dalla chat):** la scheda «dove si vede meglio, anche una schermata a parte»; i quattro fatti vanno bene. Implementata su un ramo (`scheda-rivali`) la sera del 12, non chiusa; ripresa e chiusa il 13 in autonomia.

## 9. Fermata 2: cosa è cambiato rispetto alla proposta (scritto prima della misura finale)

- **Dove si vede:** pulsante «I rivali» nel riquadro del torneo, dopo la prima regata e a torneo finito. Schermata a parte nello stesso riquadro, con «Indietro» che torna alla classifica.
- **Una scheda per volta** (13 nov), con tre pulsanti Rossa, Verde, Blu. Le tre schede insieme non stanno nei 650 px: nel caso peggiore il riquadro scorreva e la Blu restava sotto il bordo. **Il primo metro aveva sbagliato elemento:** misurava lo scorrimento del contenuto (0 px), mentre a scorrere era il riquadro intero. L'ha mostrato l'immagine. Ora il collaudo misura il riquadro, il contenuto e la posizione di «Indietro».
- **Colonne:** tabella a larghezze fisse, celle centrate (prima erano allineate a caso: la prima colonna dei risultati a sinistra, le altre a destra).
- **S1 sbagliava per colpa del collaudo, non del gioco.** Diagnosi su 3 tornei (12 regate):
  - la pagina nuova senza aprire la scheda, contro la 1.2.29: 0 regate diverse;
  - aprire e chiudere la scheda consuma 0 numeri casuali;
  - la 1.2.29 contro se stessa con 300 ms di attesa fra le regate: 9 regate diverse su 12. Fra una regata e l'altra la pagina consuma numeri casuali a ogni fotogramma.

  Correzione nel collaudo: il seme si rimette prima di ogni regata, uguale nelle due pagine.
- **Collaudo nuovo, S3b:** un torneo salvato prima della 1.2.30 (senza i campi nuovi) si apre senza errori, con gli arrivi pieni e il resto «–».
- **Termostato nel collaudo** (`--termostato GRADI`, `--da PRIMO`): il PC di Ale arriva a 84 °C anche con un collaudo solo.

## 10. Misure (13 novembre, mattina): versione NON chiusa, manca un pezzo di S1

| Criterio | Soglia | Misurato | Esito |
| --- | --- | --- | --- |
| S1 la guida non cambia | 40 tornei (160 regate), 0 differenze | **30 tornei (120 regate), 0 differenze** (semi 1-30), più la prova breve (semi 1-3, 12 regate, 0 differenze) | **incompleto:** misura fermata dal caldo, mancano i semi 31-40 |
| S2 la scheda dice il vero | 0 celle sbagliate su almeno 160 regate; ogni tipo di cella confrontato almeno una volta | 0 celle sbagliate su 120 regate. Conteggi per tipo solo nella prova breve: arrivo, partenza, boa e contatto 36 ciascuno, fuori linea 11, davanti 15, dietro 8, colpa sua 8, colpa tua 8, parità non giudicate 2 | incompleto come S1; i tipi sono tutti misurati |
| S3 torneo a metà | scheda uguale dopo la chiusura | uguale | sì |
| S3b torneo salvato prima | si apre, arrivi pieni, il resto «–» | sì | sì |
| S4 spazio a 1360x650 | 0 px in eccesso, riquadro intero, tre schede | 0 px, «Indietro» dentro, una scheda visibile, 4 regate | sì |
| S6 fisica | identica | `polare.js`, `raffiche_e_virate.js`, `impronta1b.js`: OK, identici | sì |
| S5 pagina come la carica Ale, Firefox | — | **non fatto** (script pronto, non lanciato per il caldo) | da fare |

**Il caldo.** Un collaudo solo, con due pagine in Chromium, porta il PC a onde di 65-84 °C. Prove fatte:
- termostato a 62 °C prima di ogni regata: picchi di 73-78 °C durante la regata;
- tutto su un core solo: quel core resta a 71-73 °C, e la misura avanza a fatica.

Tutte le misure si sono fermate appena sopra i 72 °C.

**Per chiudere la 1.2.30** mancano i semi 31-40 di S1 e S2 (circa 25 minuti a PC freddo), poi S5: la pagina senza `#collaudo`, in Chromium e Firefox. Il comando è in `STATO.md`.
