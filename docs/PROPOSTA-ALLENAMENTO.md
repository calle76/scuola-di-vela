# Proposta: l'Allenamento al posto delle due regate di Deriva (fermata 1)

16 novembre 2026, sera. Nasce dalla chiacchierata con Ale dello stesso giorno: «dovrebbero essere regate di allenamento, ma se hanno meno cose non ha più senso». **Via di Ale il 16 novembre** («toglie due regate inutili e ne mette una in cui scegliere come impostarla»): le due regate escono dal menu; record su 4 combinazioni, come consigliato.

## Cosa c'è oggi

In Deriva ci sono due regate, nate prima di Deriva, e il torneo:

| | Regata nei salti di vento (1.0.28) | Regata con i giri di penalità (1.0.61) | Torneo |
| --- | --- | --- | --- |
| Percorso | bastone, bolina di 300 m | bastone | bastone e triangolo |
| Vento | salti, niente raffiche, 10 nodi | costante, 10 nodi | raffiche e salti, 10 o 12 nodi |
| Contatto con colpa | +15 s | due giri | 1 punto (regate 1-2) o due giri (3-4) |
| Cono d'ombra | no | no | sì |
| Regole 15 e 16 | sì (1.3.10) | sì (1.3.10) | sì |
| Barche | 4 | 4 | 4 o 6 |

Le due regate sono un pezzo del torneo: allenarsi lì vuol dire allenarsi su una regata diversa da quella vera. In più `IL-GIOCO.md` dice che in Deriva «le vele si tolgono il vento», e lì il cono non c'è.

## Il modello più semplice

**Una voce sola in Deriva, «Allenamento»:** una regata singola fatta **come una regata del torneo** (stesso vento con raffiche e salti, stesso cono, stesse regole, stessi rivali con nome e doti), e prima di partire si sceglie:
- **percorso:** bastone o triangolo;
- **penalità:** punti o giri;
- **barche:** 4 o 6;
- **rivali:** principianti o esperti (come oggi nelle regate).

Il vento (10 o 12 nodi, direzione) si sorteggia come nel torneo. Niente classifica di serie, niente stagione, niente punti di Deriva. Restano: la classifica della regata, «Rivedi», la rotta ottimale col Coach, il record del tempo per ogni combinazione di percorso e barche.

**Le due regate di oggi** escono dal menu di Deriva, ma restano nel codice: gli esercizi delle lezioni 16, 17 e 20 della Scuola usano la regata dei giri, e i collaudi le usano tutte e due.

**Gioco libero e carriera:** nel gioco libero sempre; in carriera con Deriva (dopo l'attestato), come il torneo.

## Criteri (soglie nostre, scritte prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| A1 | È davvero una regata del torneo | con lo stesso seme, lo stesso formato e gli stessi rivali, una regata d'allenamento e la regata del torneo corrispondente danno arrivi e penalità identici, 8 combinazioni × 5 semi |
| A2 | Ogni scelta funziona | le 16 combinazioni (percorso × penalità × barche × livello) col pilota: tutte partono e finiscono, 0 errori |
| A3 | Niente cambia altrove | Scuola, esercizi delle lezioni, torneo, stagione, finale identici al bit (`collaudo_regole_15_16` R3, K1 del Coach, `impronta1b.js`, fisica) |
| A4 | Non salva quello che non deve | dopo un allenamento: nessuna stagione, nessun torneo, nessun punto di Deriva cambiato; il record sì, solo per la sua combinazione |
| A5 | Spazio e pagina | menu di Deriva e riquadro delle scelte a 1360x650 e 1360x768 senza eccesso; pagina senza `#collaudo`, Chromium e Firefox, 0 errori |

## Costanti nuove

Nessuna: tutto viene dal torneo. Le combinazioni del record sono 4 (percorso × barche); penalità e livello non separano il record (ipotesi nostra: altrimenti 16 record quasi tutti vuoti).

## Rischi

- **Si perde la bolina di 300 m:** era l'unico posto con un lato lungo per vedere i salti. Il torneo ha la bolina normale; se serve, si può aggiungere «bolina lunga» come scelta di percorso (non in questa proposta).
- **I collaudi delle due regate** (salti2, giri, semaforo, regola21, layline, segnali, bandiere) restano validi perché le regate restano nel codice; i collaudi del menu vanno aggiornati.

## Cosa serve da Ale

1. Il via.
2. Va bene togliere dal menu le due regate di oggi (restano nel codice per le lezioni)?
3. Il record: 4 combinazioni (percorso × barche) va bene?
