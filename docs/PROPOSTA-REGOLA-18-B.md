# Proposta: regola 18, versione B, i rivali che danno e prendono spazio alla boa (voce 49)

*Fermata 1, 24 novembre 2026. Nessun codice nel gioco. Prima misura fatta con `tests/misura_zona18_b.py`.*

## La domanda

Dalla 1.3.49 la regola 18 decide la colpa e il semaforo, ma i rivali guidano ancora con le sole regole 10-13. Serve insegnargliela? Solo se la 18 dice spesso una cosa **diversa** da quelle che già seguono, e con le barche abbastanza vicine da toccarsi.

## Misura (24 novembre, Chromium, torneo col pilota, semi mai usati)

| | 60 regate corte (semi 3601-3615) | 30 regate lunghe (3701-3710) |
| --- | --- | --- |
| Debiti di spazio visti dalla misura | 327 (aperti 337) | 72 (aperti 75) |
| Con le due barche entro 15 m per almeno 1 s | 106 | 22 |
| …in cui la 18 e le regole 10-13 dicono cose diverse per almeno 1 s | **25** | **7** |
| …e le barche si sono avvicinate a meno di 6 m | **4** | **3** |
| di questi 7, un rivale che doveva spazio al giocatore | 2 | 3 |
| Contatti alla boa (entro 13,6 m) | 1, deciso dalla 18 | 0 |

**Che cosa dice.** Per lo più la 18 e le regole 10-13 danno la stessa risposta (nelle corte, in 81 casi vicini su 106 non sono mai state diverse per un secondo intero): alla boa la barca interna è quasi sempre anche quella sottovento o quella davanti. I momenti in cui un rivale dovrebbe comportarsi diversamente, e da vicino, sono **7 in 90 regate**, 5 verso il giocatore.

**Limite della misura:** il pilota gira le boe largo e si tiene lontano; Ale e Lucio no (10 contatti alla boa su 12 nelle registrazioni di prima della 18 erano col giocatore). La misura vera è Z7, sulle vostre regate.

## Il modello più semplice, se un giorno serve

Una riga in `cedeAvv1b`: se fra le due barche c'è un debito di spazio aperto (`debito18`), cede chi lo deve; se no, come oggi. Niente rotte nuove e nessuna costante: lo scarto è quello che i rivali usano già. Non comprende il «prendere spazio» (infilarsi all'interno), che sarebbe un'altra cosa.

## Criteri (soglie nostre, scritte prima; si misurano solo dopo il via)

| # | Cosa | Soglia |
| --- | --- | --- |
| B1 | Scene costruite alle due boe, rivale esterno che deve spazio a chi è all'interno, regole diverse fra loro (almeno 40, posizioni sorteggiate) | contatti con colpa del rivale almeno dimezzati, con almeno 10 contatti prima |
| B2 | Regate del torneo, 120 corte e 60 lunghe, semi nuovi | contatti totali e piantate non oltre +10%, non arrivati non di più, tempo mediano dei rivali entro ±1% |
| B3 | Scuola identica | 0 differenze |
| B4 | Zona senza debiti | regate in cui non si apre un debito identiche al bit |

## Consiglio

**Non ora.** Il guadagno atteso è 7 momenti in 90 regate, il rischio è sulla guida dei rivali alle boe, che è stata tarata a lungo. Prima Z7: se nelle prime regate lunghe di Ale e Lucio con la 18 c'è **almeno un contatto ogni cinque regate** alla boa in cui il rivale doveva lo spazio, si fa; se no si chiude. (La soglia di uno ogni cinque è nostra, scritta prima di vedere le regate.) Le regate si possono fare su misura con l'Allenamento (1.3.51): triangolo, giri di penalità, 6 barche, girando le boe stretti in mezzo agli altri.

## Cosa serve da Ale

Le regate alla boa (Z7). Nessuna decisione adesso.
