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

## Esito (24 novembre 2026, 1.3.51)

Fatto come scritto. A1 40 su 40 (il confronto è con una regata non ultima di un torneo di cinque, perché nell'ultima c'è la marcatura della 1.3.50; in Firefox solo riportabile e non lanciato), A2 16 su 16 (Chromium corte e lunghe, Firefox), A3 verde (elenco nel `CHANGELOG.md`), A4 e A5 OK in Chromium e Firefox. Dopo aver visto il primo rosso di A4 è stato corretto il collaudo, non la soglia: azzerava i tratti dei rivali, che poi rinascevano. Dallo screenshot si è visto che la scelta fatta non si distingueva: corretto (pulsanti a due posizioni). Aggiunte nostre: il record non conta con una penalità sul punteggio; gli aiuti «regate» valgono anche qui; storico dei rivali fuori.

## Scegliere i rivali (voce 83; via di Ale del 24 novembre 2026: «Ok 83»; criteri scritti prima del codice)

**Modello:** nel riquadro un pulsante «Scegli i rivali» apre l'elenco dei 20 (zonale e nazionale); si toccano fino a 3 nomi (5 con 6 barche). I posti non scelti restano ai sorteggiati; nessuno scelto = sorteggio, come prima. Scegliere non cambia il vento né il carattere (prudente, normale, aggressiva), che resta della barca. Passando da 6 a 4 barche restano i primi tre scelti. La scelta resta finché la pagina è aperta, come le altre. Anche in carriera si possono scegliere i nazionali. Il record non si separa per rivali (come per il livello).

**Costanti nuove:** nessuna. **Semplificazione dichiarata:** scegliendo un nazionale mai incontrato, i tratti dei dieci nazionali nascono lì e restano, come già succede agli zonali col sorteggio.

| # | Criterio (soglie nostre) | Soglia |
| --- | --- | --- |
| S1 | In acqua ci sono quelli scelti | 40 scelte a caso (seme fisso; 1-5 nomi dei due gruppi, 4 e 6 barche, due livelli): tutti gli scelti in regata, nomi tutti diversi, numero giusto, tratti uguali a quelli salvati: 40 su 40 |
| S2 | Senza scelta non cambia niente | regata preparata identica alla 1.3.54 (stessi numeri a caso): 20 semi su 20; A1 ancora 40 su 40 |
| S3 | Si corre | 16 regate col pilota con scelte a caso (4 tutte di nazionali esperti): partono e finiscono, 0 errori: 16 su 16 |
| S4 | Non salva altro | dopo una regata con rivali scelti cambiano solo `done`, `best` e, coi nazionali mai visti, i loro tratti: niente storico, tratti già nati identici |
| S5 | Spazio e comandi | riquadro ed elenco a 1360x650 e 1360x768: 0 px; al massimo 3 o 5 scelti; mouse e tastiera; pagina senza `#collaudo`, Chromium e Firefox, 0 errori |
| S6 | Vento e barche | scegliere non cambia il vento; da 6 a 4 restano i primi tre |

**Esito (24 novembre 2026, 1.3.55):** S1 40 su 40 (30 con scelta parziale), S2 20 su 20 e A1 40 su 40 (Chromium), S3 16 su 16, S4 OK, S5 0 px, S6 OK; S1 e S3-S6 anche in Firefox. Regate corte; soglie non toccate.
