# Proposta: chi cede e tocca lo stesso (fermata 1)

**7 novembre 2026, ramo `deriva`. Fermata 1: nessuna riga del gioco cambiata.** Ale: «va bene questa strada» (cedere che non riesce, prima e dopo il via insieme).

## 1. In breve

Il contatto più comune con gli avversari è quello di una barca che dichiara di cedere e tocca lo stesso, come Rossa alle 18:33. Misurato sulle tue regate rigiocate, sei volte su dieci succede **a una barca lenta**, sotto 3 nodi. Proposta: chi deve cedere ha una scelta in più oltre a cambiare rotta, **rallentare lascando la vela**. La sceglie solo se, simulata con il motore del gioco, passa più lontano dall'altra barca di ogni cambio di rotta possibile.

## 2. Da dove si parte (diagnosi, `tests/rigioca_regata.py` con `DIAGNOSI=1`)

Le 4 regate intere di Ale, semi 481-520, la barca di Ale rifà la sua rotta e non si scansa. 160 corse per browser.

| | Chromium | Firefox |
| --- | --- | --- |
| S3, contatto di chi cede, a corsa | **0,81** (129) | **0,77** (123) |
| … di cui con la barca lenta (sotto 1,6 m/s, 3,1 nodi) | **79** | **76** |
| … prima del via | 52 | 36 |
| S4, contatto di chi doveva cedere e non lo dichiarava, a corsa | 0,64 (103) | 0,70 (112) |
| … di cui prima del via | 70 | 75 |
| S1 stretta: chi cede passa sotto 6,3 m (1,5 lunghezze), a corsa | 2,87 (459) | 2,87 (459) |

**Le cause, nell'ordine in cui le ho controllate (una sola per caso), per S3:** l'altra barca gira di oltre 30° nei 5 s prima, 46 e 37 casi (spesso è la barca di Ale, che nel rigioco non reagisce); una terza barca entro 15 m, 44 e 39; nessuna delle cause controllate, 25 e 31; chi cede gira di meno di 15°, 9 e 6; scarto finito dopo 25 s, 3 e 8. «Lenta» non era fra le cause in ordine: l'ho contata a parte, e attraversa tutte le altre.

**Correzione del mio metro, dichiarata dopo aver visto i numeri:** S1 («cede ma si avvicina», sotto 8,4 m) scatta anche quando il passaggio riesce come previsto, perché la guida mira proprio a passare a 8,4 m (due lunghezze). Delle 1.460 S1 in Chromium, 624 sono fra 8,0 e 8,4 m. S1 resta com'è nello strumento; come misura uso la S1 stretta, sotto 6,3 m, cioè sotto la distanza (`ULTIMO`, 1,5 lunghezze) in cui anche chi ha la precedenza scarta.

## 3. Causa probabile (letta nel codice, non provata)

In `cedeAvv1b` (`js/regate.js`) chi cede può solo cambiare rotta, di 15, 28, 45 o 60 gradi. Da lenta non può orzare (regola aggiunta in Deriva, per non piantarsi), e una barca lenta gira poco e risponde piano. La previsione di `passaggio()` tratta poi una barca lenta come se andasse ad almeno 1 m/s. Quindi a bassa velocità nessuna rotta della lista basta, e la barca prende la meno peggio e tocca.

## 4. Il modello più semplice

Fra i candidati di `cedeAvv1b`, uno in più: **«frena»**, tenendo la prua che ha e lascando tutta la vela. Si valuta con la simulazione che la guida ha già (quella di `glideY`, lo stesso `step()` del gioco). Così fermarsi non è istantaneo e lo spazio di frenata non è un numero inventato. Nessuna costante nuova sullo spazio di frenata.

- Si sceglie solo se la distanza minima prevista frenando è **maggiore** di quella del miglior cambio di rotta, e solo per chi deve cedere.
- Non vale per chi ha la precedenza, per chi sta virando, né per chi sconta giri.
- Dopo, la barca riparte con la logica dell'abbrivio che c'è già.
- Vale prima e dopo il via, con lo stesso limite di 25 s (`SCARTO_MAX`) che hanno gli scarti.

**Fuori da questo compito:** S4 (chi doveva cedere ma non lo sapeva, quasi tutti prima del via, quasi sempre fermi in attesa), che fu già provato nella fetta 1 di `PROPOSTA-AVVERSARI-DERIVA.md` e peggiorò; l'altra barca che cambia rotta all'ultimo (regola 16, è una questione di regolamento, non di guida).

## 5. Criteri (soglie nostre, scritte prima di misurare)

Soglie scelte sui **semi 521-540**; poi conferma sui **semi 541-560, mai guardati**. Chromium e Firefox. Il metro principale è il rigioco delle 4 regate intere di Ale; si misura prima e dopo sugli stessi semi.

- **K1, contatti di chi cede (S3):** almeno **-30%** in tutti e due i browser.
- **K2, non peggiorare:** S4 e contatti in tutto al massimo **+10%**; S1 stretta al massimo **+10%**.
- **K3, frena davvero:** il candidato «frena» viene scelto almeno 20 volte su 160 corse (se no la correzione non ha fatto niente), e in nessun caso una barca resta sotto 0,5 nodi per più di 25 s dopo il via per colpa sua.
- **K4, gli avversari corrono ancora** (`tests/misura_avversari.py`, semi 361-380, confronto con il §11 della proposta avversari): penalità al massimo 190, fuori linea al massimo 36, non arrivate 0, arrivo mediano al massimo +5%, piantate non più di oggi più 2 (oggi 13 e 11).
- **K5, i casi costruiti** (`collaudo_avversari_deriva.py`): nessuno dei quattro peggiora rispetto a oggi.
- **K6, barca invariata:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.
- **Da riportare, senza soglia:** il torneo col pilota; S3 nelle regate vere di Ale, quando ne scaricherà altre.

Un numero fuori soglia si riporta com'è.

## 6. Costanti nuove

Nessuna sulla fisica. Una sola regola di scelta: «frena» vince solo se passa più lontano del miglior cambio di rotta (nessuna soglia numerica).

## 7. Fonti

Regolamento di regata F15 e F39: chi deve tenersi discosto può farlo come vuole, rallentando o cambiando rotta (definizione «tenersi discosto», regole 10-13): **da rileggere sulla copia locale prima della fermata 2**. Che lascando la vela una deriva rallenti e si fermi in una decina di metri lo dice il motore (`glideY`, già misurato in `docs/archivio/PROPOSTA-PARTENZE.md`), non una fonte esterna.

## 8. Rischi

- **Frenare davanti a una barca che arriva da dietro:** la simulazione guarda tutte le barche vicine, ma una barca che cambia rotta all'ultimo resta imprevedibile.
- **Più barche ferme o lente prima del via:** è la ragione di K3 e delle piantate in K4.
- **Il rigioco esagera:** la barca di Ale non reagisce, quindi i contatti contati sono più di quelli veri. Conta il confronto prima e dopo, non il numero assoluto.
- **Costo di calcolo:** una simulazione in più, solo per chi cede e solo due volte al secondo, come `glideY`.
- **Vale anche per la Scuola** (decisione di Ale del 6 novembre), quando il ramo entrerà in `main`.
