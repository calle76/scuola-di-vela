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

## 9. Esiti della fermata 2 (7 novembre 2026): **non superata, correzione tolta**

Ale: «vai». Fonte riletta: in F15 la definizione «Keep Clear» dice solo che chi ha la precedenza deve poter tenere la sua rotta senza manovrare per evitare l'altra, e, se le barche sono affiancate, cambiare rotta in tutte e due le direzioni senza toccarla subito; non dice come chi cede ci riesca, quindi rallentare è ammesso. Il «come vuole» del §7 era una mia parafrasi: la regola fissa il risultato, non il modo.

Fatto come al §4: candidato «frena» in `cedeAvv1b` (vela tutta lascata, prua tenuta), valutato con `step()` due volte al secondo, scelto solo se passa più lontano del miglior cambio di rotta. Misura sui **semi di scelta 521-540**, rigioco delle 4 regate di Ale, 80 corse per browser, prima e dopo sugli stessi semi (il prima su una copia congelata del codice).

| | Chromium: prima → dopo | Firefox: prima → dopo | Soglia | Esito |
| --- | --- | --- | --- | --- |
| K1 S3, contatti di chi cede, a corsa | 1,15 → 1,00 (**-13%**) | 1,00 → 0,94 (**-6%**) | -30% | **no** |
| K2 S4 | 0,95 → 1,00 (+5%) | 0,93 → 1,01 (+9%) | +10% | sì |
| K2 contatti in tutto | 2,10 → 2,00 (-5%) | 1,93 → 1,95 (+1%) | +10% | sì |
| K2 S1 stretta | 2,89 → 2,91 (+1%) | 2,46 → 2,60 (+6%) | +10% | sì |
| K3 frenate scelte | 0 → 2.515 | 0 → 2.558 | almeno 20 | sì |
| K3 ferme oltre 25 s per la frenata | massimo 8,5 s | massimo 2,4 s | nessuna | sì |
| S7 barche ferme (senza soglia) | 0,04 → 0,19 a corsa | 0,07 → 0,19 | | peggio |
| K5 casi costruiti | 80: 10, 81: 6, 82: 10, 83: 10 | 83: in 7 varianti su 10 una barca esce, ma il caso è superato (soglia: al massimo una barca fuori), quindi 10 su 10 | come oggi | da confrontare, vedi sotto |

**Perché non basta, dai numeri:** dei contatti di chi cede con la barca lenta, ne restano 44 su 52 (Chromium) e 38 su 39 (Firefox). Una barca già lenta, frenando, cambia poco: è l'altra che le arriva addosso. Le frenate sono tante (2.500 in 80 corse) perché la scelta cambia quasi a ogni passo: la vela si lasca e si cazza a scatti.

**Decisione presa da me secondo le regole:** soglia K1 non raggiunta, quindi la correzione non resta. `js/regate.js` è tornato identico al commit di prima (`git diff` vuoto); `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici. La conferma sui semi 541-560 non serve e non è stata guardata; K4 (`misura_avversari.py`) misurato solo sul codice nuovo, non confrontato. Restano nello strumento `rigioca_regata.py` i contatori delle frenate (valgono 0 sul gioco di oggi).

**Che cosa resta vero:** i contatti di chi cede si concentrano sulle barche lente e, nel rigioco, sull'altra barca che gira o su una terza barca vicina. Una barca lenta non si toglie di mezzo né girando né frenando: per evitarli bisognerebbe che non diventasse lenta vicino alle altre, cioè agire prima (in attesa e in partenza), oppure che la barca veloce che arriva se ne accorga (ma ha la precedenza). Sono due proposte diverse, da decidere con Ale.
