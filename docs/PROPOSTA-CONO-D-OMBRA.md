# Proposta: il cono d'ombra delle vele (10 novembre 2026, fermata 1)

Ale, 9 novembre: nelle regate non didattiche la fisica c'è tutta, cono d'ombra compreso (`DECISIONI.md`). Ale, 10 novembre: il cono prima del lavoro sugli avversari. La ricerca è in `RICERCA-CONO-D-OMBRA.md` (fonti F75 e F76). Questa è la **fermata 1**: niente codice nel gioco finché Ale non dà il via.

## 1. Cosa cambia per chi gioca

Una barca che ha un'altra barca fra sé e il vento riceve **meno vento** e va più piano. Succede:
- al via, a chi parte in seconda fila;
- di bolina, a chi sta sottovento e un po' dietro a un'altra;
- in poppa, a chi sta davanti: chi insegue gli toglie il vento.

Vale per tutti, giocatore e avversari, in tutte e due le direzioni. **Solo nelle regate non didattiche:** oggi il torneo, poi Deriva. Scuola, prove, lezioni e regate a tema restano identiche.

## 2. Il modello più semplice plausibile

Il cono cambia il **vento** che una barca riceve, non la barca. Oggi ogni barca chiede il vento del suo punto (`windAt`); col cono, prima di darlo al motore, lo si riduce se un'altra barca la copre. Il motore (`step`) non si tocca.

Per ogni coppia «barca che copre» A e «barca coperta» B:

1. **Asse del cono.** Parte da A e va sottovento lungo il **vento apparente** di A (il motore lo calcola già), girato di **5° verso la poppa** di A (F75). In poppa piena vento apparente e reale coincidono, come dicono le fonti.
2. **Quanto vento manca sull'asse,** secondo la distanza da A in altezze d'albero (H):

   | Distanza | Spinta del coperto (F75, Caponnetto) | Vento che resta (radice della spinta, conversione nostra) | Vento che manca |
   | --- | --- | --- | --- |
   | fino a 0,5 H | circa un quinto | 46% | **54%** |
   | 1 H | circa due quinti | 62% | **38%** |
   | 2 H | metà | 71% | **29%** |
   | 10 lunghezze | intera | 100% | **0** |

   Fra un punto e l'altro si va in linea retta.
3. **Di lato:** l'effetto cala in linea retta fino a zero a **una lunghezza di barca** dall'asse (F75, Hooper).
4. **Vela che non porta:** l'ombra di A è moltiplicata per quanto lavora la sua vela, da 0 (sbatte, angolo d'incidenza zero) a 1 (da 10° d'incidenza in su). Una barca ferma in attesa del via, con la vela lascata, fa poca ombra. Una barca scuffiata non ne fa.
5. **Più barche che coprono la stessa:** vale l'ombra più forte, non la somma.

**Lasciati fuori da questa prima fetta, e dichiarati:**
- il vento **girato** dentro la scia (uno scarso di circa 4° a 3 altezze d'albero, F75);
- la zona **favorevole** sottovento e avanti («posizione sicura sottovento», +20% di spinta, F75) e il piccolo vantaggio sopravento;
- il «rifiuto» (*backwind*) sulla barca sopravento;
- gli avversari **non reagiscono** al cono: non cercano il vento libero. Arriva col lavoro sugli avversari, dopo le registrazioni (`DECISIONI.md`, 10 novembre).

## 3. Costanti nuove

| Costante | Valore | Da dove |
| --- | --- | --- |
| Angolo dell'asse verso poppa | 5° | F75 (bolina). Al lasco F75 dà 9°, ma con lo spi: **ipotesi nostra** tenere 5° sempre |
| Vento che manca a 0,5 / 1 / 2 H | 54% / 38% / 29% | F75 (Caponnetto), convertito da spinta a vento: **la conversione è nostra** |
| Fine del cono | 10 lunghezze (42 m) | F75 (Marchaj), senza curva: **la retta fra 2 H e 10 lunghezze è ipotesi nostra** |
| Mezza larghezza | 1 lunghezza (4,2 m) | F75 (Hooper) |
| Altezza d'albero H | 5,5 m | **ipotesi nostra**: nel motore non c'è; deriva di 4,2 m con 7 m² di randa |
| Incidenza da cui la vela fa ombra piena | 10° | **ipotesi nostra** |
| Più barche: la più forte | — | **ipotesi nostra** |

Le misure delle fonti sono su yacht grandi: usarle in altezze d'albero sulla nostra deriva è un'ipotesi, già dichiarata nella ricerca.

## 4. Cosa vede il giocatore

- **Sul mare:** dietro ogni barca un cono tenue, più scuro dove toglie più vento. È un **aiuto disattivabile** (riga «Cono d'ombra» nelle impostazioni).
- **Negli strumenti:** il vento del pannello è già quello che la barca riceve, quindi dentro un cono scende da solo.
- **Nel testo prima della regata del torneo:** una frase che lo spiega.
- La lezione vera va in Deriva, con le altre lezioni di regata.

## 5. Cosa tocca del resto

- **Rotta ottimale a fine regata:** resta calcolata col vento libero. Il tempo perso in un cono compare come tempo perso, che è giusto.
- **Registrazione delle regate:** una colonna in più nelle righe delle barche, con la percentuale di vento tolto. Serve a leggere le vostre regate dopo.
- **Guardiano degli avversari:** i suoi numeri cambieranno; il riferimento si riscrive e la differenza è proprio la misura dell'effetto del cono.
- **Barca congelata** (`polare.js`, `raffiche_e_virate.js`, `impronta1b.js`): una barca sola col vento libero, devono restare identici.

## 6. Criteri (soglie nostre, scritte prima di misurare)

**Il cono fa quello che dice** (`tests/collaudo_cono.py`, casi costruiti con due barche ferme o guidate):
- **K1, sull'asse:** il rapporto fra la spinta di chi copre e quella del coperto a 0,5 / 1 / 2 H sta entro il 15% da 4,8 / 2,6 / 2,0 (i numeri di F75), misurato sulla spinta vera del motore.
- **K2, di lato:** a una lunghezza dall'asse la spinta è almeno il 99% di quella libera.
- **K3, fuori dal cono:** sopravento ad A, al traverso sopravento e oltre 10 lunghezze il vento è identico al bit a quello libero.
- **K4, l'asse segue il vento apparente:** con A ferma e con A di bolina a 4 nodi l'asse cambia direzione di almeno 10°.
- **K5, vela che non porta:** A con la vela che sbatte toglie al massimo il 10% del vento a 1 H; A scuffiata zero.
- **K6, in navigazione:** B di bolina, 1,5 lunghezze sottovento e dietro ad A, dopo 20 s ha perso almeno il 10% di velocità rispetto alla stessa corsa senza A; B sottovento e **avanti**, fuori dal cono, meno dell'1%. 10 varianti ciascuno, almeno 9 su 10.

**La Scuola non cambia:**
- **K7:** le 4 regate del menu e le 5 prove, 10 semi, principianti ed esperti: arrivi identici al bit alla 1.2.24 (confronto con una copia del gioco di prima).

**Nel torneo** (`misura_avversari_rotta.py`, semi **1521-1550**, mai usati, 240 regate, contro la 1.2.24 sugli stessi semi; non c'è niente da scegliere, quindi un gruppo solo):
- **K8, il cono succede davvero:** almeno 200 episodi di barca coperta (più del 10% di vento tolto per almeno 2 s). Sotto, la misura non vale.
- **K9, arrivo mediano degli avversari:** peggiora al massimo del **5%**. Attesa nostra: il cono rallenta un po' tutti.
- **K10, avversari non arrivati o squalificati:** al massimo +2; nessuna barca «BLOCCATA» in `collaudo_regate.py --lungo`.
- **K11, contatti dopo il via:** al massimo +15%.
- **K12, partenza:** taglio mediano della linea al massimo +1 s; tagli oltre 10 s dal via al massimo +20%.
- **K13, il pilota** arriva come prima: `collaudo_torneo.py` verde come oggi.
- Solo riportati, senza soglia: tempo perso in bolina e in poppa, distacco fra primo e ultimo, quota di tempo passata coperti.

**Schermo e costo:**
- **K14:** pannello a 1360×650 senza pixel di eccesso con la riga nuova; pagina senza `#collaudo` senza errori.
- **K15:** il costo di un passo di gioco sale al massimo del 3% (come E2 di `collaudo_registrazione.py`).

**Non-regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.

## 7. Rischi

- **Avversari che restano coperti.** Non reagiscono al cono: chi finisce dietro al gruppo può restarci. K9-K12 dicono quanto pesa. Se le soglie non passano, il gioco resta la 1.2.24 e la patch va in `sperimentale/`.
- **Partenze più dure.** In seconda fila non c'è vento: è vero in regata, ma il giocatore alle prime armi lo sentirà. Per questo c'è il cono disegnato.
- **Sorpassi più difficili di bolina, più facili in poppa.** È l'effetto voluto.
- **Scala.** Le distanze vengono da yacht grandi. Se giocando il cono sembra troppo lungo o troppo corto, la costante da toccare è una (le 10 lunghezze), ma solo con una fonte o con una decisione di Ale dichiarata.

## 8. Costo

Circa mezza giornata per codice, disegno e collaudo nuovo; circa un'ora e mezza di misura col termostato. Versione **1.2.25**.

## 9. Decisioni che servono da Ale

1. **Il cono disegnato sul mare, nel torneo:** acceso o spento all'inizio? Le layline nel torneo partono spente. Proposta: **acceso**, perché senza vederlo non si capisce perché la barca rallenta.
2. **La fisica del cono si può spegnere?** Proposta: **no**, come le raffiche; si spegne solo il disegno.
3. **Va bene la prima fetta così,** senza vento girato nella scia e senza la zona favorevole sottovento? Si possono aggiungere dopo, con una proposta loro.

## 10. Esito (10 novembre 2026, fermata 2): tutti i criteri passano, versione 1.2.25

Via di Ale («ok va bene così, procedi fino alla fine»), con le tre decisioni del §9 come proposte: cono disegnato acceso nel torneo, fisica non spegnibile, prima fetta così.

**Una differenza dalla proposta:** nella registrazione non c'è una colonna in più nelle righe delle barche ma due eventi, `coperta nome da nome2 N%` e `libera nome` (più del 10% di vento tolto da 2 s). Le righe delle barche restano uguali, così i programmi che le leggono non cambiano.

| Criterio | Soglia | Misurato | |
| --- | --- | --- | --- |
| K1 spinta libera / coperta a 0,5 / 1 / 2 H | entro il 15% da 4,8 / 2,6 / 2,0 | 4,73 / 2,60 / 1,98 | ✓ |
| K2 a una lunghezza di lato | almeno 99% | 100,0% | ✓ |
| K3 fuori dal cono | zero esatto | zero in 6 punti su 6 | ✓ |
| K4 l'asse segue il vento apparente | almeno 10° | 13,7° | ✓ |
| K5 vela che sbatte / scuffiata | al massimo 10% / zero | 7,6% / zero | ✓ |
| K6 dentro il cono, 10 varianti | almeno −10% di velocità in 9 | da −27% a −29% in 10 | ✓ |
| K6 fuori dal cono, 10 varianti | meno dell'1% in 9 | 0,00% in 10 | ✓ |
| K7 Scuola identica al bit | tutte | 80 regate del menu su 80; impronta del gioco: 67 scene, diversa solo la regata del torneo | ✓ |
| K8 episodi di barca coperta | almeno 200 | 985 (6,0% del tempo di regata) | ✓ |
| K9 arrivo mediano degli avversari | al massimo +5% | 201,6 → 199,1 s (−1,2%) | ✓ |
| K10 non arrivati o squalificati | al massimo +2 | 0 → 0 e 4 → 3 | ✓ |
| K11 contatti dopo il via | al massimo +15% | 149 → 128 (−14%) | ✓ |
| K12 taglio della linea, mediana / oltre 10 s | +1 s / +20% | 2,6 → 2,4 s / 114 → 104 | ✓ |
| K13 `collaudo_torneo.py` | verde come prima | veloce e giocatore OK; misura: cade solo C11 R7 (uscita dal menu 3,16 s contro 2), misura di tempo già nota sul PC sotto carico | ✓ |
| K14 pannello e pagina vera | senza eccesso, senza errori | `collaudo_pannello` a 1360×650 e 1360×768 OK; finestra delle impostazioni 0 px in torneo, regata del menu e navigazione libera; pagina senza `#collaudo` OK | ✓ (dopo una correzione, sotto) |
| K15 costo del passo | al massimo +3% | −0,8% (0,0982 → 0,0974 ms, 8 blocchi alternati) | ✓ |

Solo riportati (senza cono → col cono): bolina persi media 29,4 → 27,6 s; poppa persi mediana 6,7 → 6,6 s; boa toccata 60 → 46; distacco fra primo e ultimo avversario, mediana, 33,9 → 27,8 s.

**Un difetto mio trovato dai collaudi e corretto:** la casella nuova allungava la finestra delle impostazioni, che in lezione e in navigazione libera sforava a 650 px (`collaudo_registratore`). Ora la casella compare solo nel torneo; `collaudo_cono.py` lo controlla nelle tre modalità.

**Cosa non mi aspettavo: col cono gli avversari non rallentano, vanno un po' meglio.** Pensavo che il cono rallentasse la flotta. Ho quindi misurato tre gruppi di semi, la stessa regata con e senza cono:

| Gruppo | Regate | Arrivo degli avversari, differenza media | Contatti |
| --- | --- | --- | --- |
| semi 1521-1550 (quello dichiarato) | 240 | −2,5 s ±1,0 | 149 → 128 |
| semi 1551-1580 (aggiunto per conferma) | 240 | −2,8 s ±1,0 | 144 → 105 |
| semi 1491-1502 (quelli del guardiano) | 96 | +1,7 s ±1,3 | 60 → 61 |
| tutti insieme | 576 | circa −2 s ±0,6 (l'1% del tempo di regata) | 353 → 294 (−17%) |

- **Il guadagno è nella prima bolina** (−3,0 s ±0,6 sui due gruppi grandi) e, nel primo gruppo, quasi solo dei principianti (−4,6 s ±1,5; esperti −0,4 ±1,4).
- **Non è un cono finto:** nel ciclo del gioco gli avversari coperti oltre il 20% ricevono in media il 78% del vento apparente libero, e il valore coincide col ricalcolo entro 0,007 m/s (400 campioni).
- **La causa non è dimostrata.** Ipotesi: dopo il via le barche in gruppo si disturbano (cedono, poggiano, si toccano); col cono chi sta dietro e sottovento rallenta e si stacca prima, e il gruppo si scioglie. I contatti in meno (−17%) vanno in questa direzione.
- **Dipende dal gruppo di semi:** su uno dei tre la differenza è di segno opposto, dentro l'incertezza.
- **Lettura prudente: il cono non peggiora gli avversari,** che era il rischio da controllare; in media li aiuta di poco.

**Il guardiano su questa modifica ha dato un allarme più forte del vero.** Contro il riferimento della 1.2.24 ha segnato l'arrivo mediano a +4,75 s (soglia 1,78) e il lasco a +0,75 s (soglia 0,5). Sugli stessi semi il confronto regata per regata dà +1,7 s ±1,3: la mediana su 96 regate salta molto quando una modifica rimescola le regate. Il suo riferimento è riscritto sulla 1.2.25. Da ricordare: quando il guardiano suona, prima di concludere si fa il confronto regata per regata su un gruppo grande.

**Resta da fare, dichiarato nel §2:** avversari che cercano il vento libero, vento girato nella scia, zona favorevole sottovento.
