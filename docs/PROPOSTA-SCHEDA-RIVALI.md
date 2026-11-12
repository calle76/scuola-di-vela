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
