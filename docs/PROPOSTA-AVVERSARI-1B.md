# Avversari con la barca dell'1b — fermata 1

Scritta il 26 ottobre 2026, sulla 1.0.48. Passo 2 del «Prossimo lavoro» di `STATO.md`; punto «1b alfa» di `METODO.md` §5. Nessun codice nel gioco: c'è solo lo strumento di misura `tests/misura_avversari.py` (nuovo, senza soglie).

## 1. Da dove nasce

Dal check di Ale sulla 1.0.47 (`CHECK SCUOLA DI VELA.docx`, 26 ottobre 2026):

- avversari che **si piantano in bolina**, anche quando **avevano la precedenza** (la Verde mure a dritta si ferma per lasciar passare Ale mure a sinistra);
- nel torneo la Rossa **resta alla boa** senza girarla;
- la Blu e la Verde si urtano e «non è chiaro se una delle due sia stata penalizzata o se si sono attraversate come fantasmi»;
- la Rossa rallenta strambando;
- una barca esce oltre la boa di partenza e deve rientrare.

Ale ha chiesto anche il **motivo delle penalità a fine regata** e un **registratore che registri tutte le barche** (§7).

## 2. Misura di partenza

`python tests/misura_avversari.py 1 20 0,1,2`: semi 1-20, le tre regate, avversari principianti ed esperti, giocatore guidato dal pilota dei collaudi (che usa la stessa guida degli avversari). 120 corse, 360 barche avversarie. Uscita completa in `tests/output/misura_avversari/semi1-20.txt`.

| Regata | Livello | Piantate (≥5 s sotto 0,5 nodi) | di cui vicino a una barca (<22 m) | di cui **avendo la precedenza** | Penalità prese | Ferme alla boa >60 s | Fuori al via |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bastone (1a) | principianti | 21 | 20 | 11 | 50 | 5 | 7 |
| bastone (1a) | esperti | 21 | 20 | 13 | 74 | 2 | 4 |
| raffiche (1a) | principianti | 16 | 14 | 10 | 67 | 0 | 6 |
| raffiche (1a) | esperti | 42 | 41 | 28 | 68 | 1 | 6 |
| salti di vento (1b) | principianti | 11 | 8 | 3 | 37 | 0 | 10 |
| salti di vento (1b) | esperti | 13 | 9 | 7 | 33 | 1 | 11 |

Su 60 barche per riga. Inoltre: **0 barche non arrivate e 0 boe sbagliate** in tutte le 360. Strambate: perdita di velocità mediana 1-2%, la peggiore 43% (salti di vento): la strambata lenta vista da Ale esiste, ma è rara.

**Dove si piantano:** 82 piantate su 124 a meno di 30 m dalla boa di bolina, quasi tutte le altre lungo la bolina. **Con chi:** in 51 casi la barca vicina è quella del giocatore.

**Cosa dicono i numeri:** le piantate sono quasi sempre vicino a un'altra barca, e in 72 casi su 124 la barca piantata aveva la precedenza. È il caso visto da Ale.

## 3. La causa nel codice (`js/regate.js`, `aiControl`)

1. **Evita tutte le barche, sempre.** Se una barca si trova davanti entro 14 m (22 m per la prudente), l'avversario scarta fino a 45°, anche quando la precedenza è sua. Dalla 1.0.17 può farlo orzando dentro l'angolo morto, e così si pianta.
2. **Chi cede non usa le regole dell'1b.** L'avversario conosce solo la regola 10: mure a sinistra contro mure a dritta, entro 30 m, poggia di 28°. Non usa `chiCede` (regole 11, 12 e 13), che pure decide le penalità e il semaforo.
3. **Alla boa** non c'è nessuna regola: la 18 (spazio alla boa) è del livello 2. Le barche si ammassano e lo scarto del punto 1 le pianta.
4. **I contatti fra avversari non si vedono:** la penalità c'è (15 s, o 1 punto nel torneo), ma non compare nessun messaggio. Da qui il dubbio «fantasmi».

## 4. Proposta (modello più semplice plausibile)

Vale **solo nell'1b** (`R.lv2`). L'1a resta identica al bit (domanda 1, §8).

**A. Chi deve cedere cede, chi ha la precedenza tiene la rotta.** L'avversario chiede a `chiCede` chi deve cedere, per ogni barca entro `D_CEDE` metri che si sta avvicinando:
- se **deve cedere**: con mure diverse poggia e passa di poppa (com'è oggi); con le stesse mure si allontana dall'altra barca, cioè orza se è sottovento, poggia se è sopravento o dietro. Non entra mai nell'angolo morto: se per evitare dovrebbe orzare oltre, poggia;
- se **ha la precedenza**: tiene la rotta (spirito delle regole 14 e 16 di F15). Scarta solo all'ultimo momento, quando il contatto è vicino (meno di `D_ULTIMO` metri e in avvicinamento), e sempre poggiando, mai nell'angolo morto.

**B. Uscire da una piantata:** già c'è (poggia a 80° e lascia la vela). Resta com'è.

**C. Penalità fra avversari visibili.** Un messaggio breve quando due avversari si toccano («Contatto: penalità alla Blu»), e a fine regata, sotto la classifica, l'elenco delle penalità col motivo, per tutte le barche. Il motivo c'è già: è il testo che oggi riceve solo il giocatore. Solo testo, niente fisica.

**Costanti nuove (ipotesi nostre, da derivare dalla barca dove si può):**
- `D_CEDE` = 30 m: è il valore che la regola 10 degli avversari usa già oggi;
- `D_ULTIMO` = 1,5 lunghezze della barca (`1.5 * BOAT.length`, circa 6,6 m): da qui la barca con la precedenza scarta;
- lo scarto di chi cede con le stesse mure: 28°, come oggi con mure diverse.

## 5. Criteri (soglie nostre, decise ora)

Si misurano sulla regata nei salti di vento (1b), principianti più esperti, 40 corse (120 barche). **Regola dei semi:** si lavora sui semi 1-20; la conferma si fa sui semi 21-40, mai guardati; le soglie non cambiano dopo.

| N. | Criterio | Oggi (semi 1-20) | Soglia |
| --- | --- | --- | --- |
| 1 | Piantate avendo la precedenza | 10 | al massimo 2 |
| 2 | Piantate in tutto | 24 | al massimo 12 |
| 3 | Penalità prese dagli avversari | 70 | al massimo 70 (non devono aumentare) |
| 4 | Tempo d'arrivo medio degli avversari | 402,8 s | al massimo 410,9 s (+2%) |
| 5 | Non arrivate, boe sbagliate | 0, 0 | 0, 0 |
| 6 | Scenari fissi (§6), ognuno in 10 varianti | — | almeno 9 su 10 per scenario |
| 7 | 1a invariata | — | regate 0 e 1 identiche alla misura di oggi, carattere per carattere; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici |

## 6. Scenari fissi (collaudo nuovo, `tests/collaudo_avversari1b.py`)

Situazioni costruite a mano, con l'esito atteso scritto prima. Due avversari soli, vento costante a 10 nodi, nessun giocatore in mezzo. 10 varianti per scenario: distanze e angoli spostati con un seme fisso.

1. **Incrocio con mure diverse** in rotta di collisione a 40 m: la barca mure a sinistra passa di poppa; quella mure a dritta non devia più di 10° e non scende sotto il 70% della sua velocità; nessun contatto.
2. **Stesse mure, affiancate:** quella sopravento si allontana; quella sottovento non si pianta.
3. **Stesse mure, una dietro più veloce:** quella dietro non urta quella davanti.
4. **Virata davanti a un'altra** (regola 13): nessun contatto, o la penalità a chi virava.
5. **Tre barche alla boa insieme:** tutte la girano entro 60 s, senza piantate di oltre 5 s.

Quando un difetto si vede giocando, diventa uno scenario nuovo: così, una volta corretto, non può tornare senza che un collaudo se ne accorga.

## 7. Fuori da questo passo (vengono dopo, ognuno con la sua proposta)

- **Registratore di tutte le barche:** serve anche al replay semplice (`ROADMAP.md`); da proporre insieme a quello.
- **Regata lasciata a metà = ritiro** da quella regata, mentre il torneo continua (chiarito da Ale il 26 ottobre). Oggi `collaudo_torneo.py` C3 controlla proprio il contrario: il salvataggio non deve cambiare.
- **Classifica più leggibile** (oggi «+30» non dice che sono due penalità).
- **Raddrizzata** di 10 s contro i 15 s cronometrati in un video: da misurare (`Tracker`).
- **Boe dal lato sbagliato:** 0 su 360 barche avversarie in questa misura. Succedeva al pilota nell'1a: resta un limite noto dell'1a.
- **Partenze fuori dalla linea** (21 su 120 nell'1b): l'avversario rientra da solo; è anche realistico. Non si tocca.

## 8. Domande per Ale

1. **Anche nell'1a?** Nella misura le piantate dell'1a sono di più (100 contro 24). L'1a però è congelata. Consiglio: prima l'1b, poi si guarda se portare la correzione all'1a con i numeri in mano.
2. **Il punto C** (messaggi e elenco delle penalità): va bene in questo passo? Tocca anche la schermata finale dell'1a (solo testo).

## 9. Rischi

- Se la barca con la precedenza scarta meno, i contatti possono aumentare: lo controlla il criterio 3.
- **Il pilota dei collaudi usa la stessa guida:** nei collaudi dell'1b (torneo, salti di vento, regole) cambiano i numeri. È previsto; le soglie di quei collaudi non si toccano.
- Le scene dell'1b di `collaudo_impronta.py` cambieranno: Ale rigenera il riferimento. `impronta1b.js` (sola fisica) deve restare identica.
- Record e fantasmi delle regate dell'1b si possono azzerare (decisione di Ale, memoria del progetto).

## 10. Fermata 2: cosa è stato fatto e misurato (26 ottobre 2026, 1.0.49)

Via di Ale il 26 ottobre: solo 1b (l'1a si decide dopo, coi numeri) e punto C compreso.

**Fatto** (`js/regate.js`): `cedeAvv1b` nella guida degli avversari dell'1b, con le costanti dichiarate in §4 (30 m, 28°, 1,5 lunghezze) e due aggiunte nate dalle prove, tutte e due senza costanti nuove: (a) chi sta cedendo continua finché le due barche non si allontanano (prima tornava in bolina appena la previsione diceva «passi», e urtava); (b) se la guida chiede di virare mentre si cede (timer dei bordi), si cede sulle mure di adesso; (c) chi deve cedere a una barca davanti e non può orzare (angolo morto) poggia. Una previsione del punto di massimo avvicinamento decide con chi (entro 15 s e a meno di due lunghezze: `T_CEDE`, ipotesi nostra non scritta in §4). Prima del via, chi è fermo in attesa non usa `cedeLv2`. Punto C: messaggio sui contatti fra avversari (solo 1b) ed elenco delle penalità col motivo nella schermata finale (1a e 1b). Corretto anche «finché non eri» nel testo della regola 13 detto di un avversario.

**Prove scartate** (sui semi 1-20): scarto di 45° e 40°, preavviso 40 m / 20 s, chi ha la precedenza che scarta da 3 o 5 lunghezze, `cedeAvv1b` anche in attesa del via, guida vecchia fino al via. Le penalità scendono fino a 71-77, ma tornano le piantate (fino a 17) o le boe sbagliate (fino a 5); in attesa del via le penalità salgono a 128. Il numero delle penalità cambia di ±7 fra prove quasi uguali.

**Regola dei semi:** lavoro sui semi 1-20; i semi 21-40 li ho guardati prima dell'ultima correzione (c), trovata con lo scenario 3 e non sui numeri; la conferma vera è sui semi 41-60, mai guardati prima.

| Criterio (regata nei salti di vento, 40 corse, 120 barche) | Soglia | 1-20 prima | 1-20 dopo | 21-40 prima | 21-40 dopo | **41-60 prima** | **41-60 dopo** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 Piantate avendo la precedenza | ≤ 2 | 10 | 2 | 20 | 0 | 16 | **1, ok** |
| 2 Piantate in tutto | ≤ 12 | 24 | 4 | 36 | 4 | 36 | **2, ok** |
| 3 Penalità prese dagli avversari | ≤ 70 | 70 | 108 | 84 | 109 | 73 | **97, FUORI** |
| 4 Arrivo medio degli avversari | ≤ 410,9 s | 402,8 | 409,0 | 408,1 | 408,7 | 405,4 | **407,9, ok** |
| 5 Non arrivate / boe sbagliate | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 4 | 0 / 2 | 0 / 1 | **0 / 1, FUORI** |

Sui semi 41-60 le 97 penalità sono 43 fra avversari e 54 col pilota (che guida con la stessa logica).

**6 Scenari** (`tests/collaudo_avversari1b.py`): 1 incrocio 10/10, 2 affiancate 10/10, 3 da dietro 10/10, 4 virata davanti 10/10, **5 tre barche alla boa 7/10, FUORI** (2 piantate, 1 barca che non gira in 60 s; contatti dopo la boa in 9 varianti su 10, fra chi ha girato e chi arriva: è la regola 18, livello 2). Contro-prove del metro: con la guida della 1.0.48 lo scenario 1 dà 0/10 e il 5 0/10; con una guida che non scansa nessuno, nelle situazioni costruite c'è un contatto nello scenario 1 in 10 varianti su 10, nel 3 in 10 su 10, nel 4 in 3 su 10, **nel 2 mai**: lo scenario 2 non distingue (in bolina la guida riporta subito la barca all'angolo di bolina, quindi non converge) e vale solo come non-regressione.

**7 1a invariata:** regate 0 e 1, semi 1-20, 80 corse identiche carattere per carattere alla misura della 1.0.48; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.

**Collaudi:** `collaudo_regole.py`, `collaudo_contatto_vero.py`, `collaudo_salti2.py`, `collaudo_torneo.py --veloce` OK. **`collaudo_semaforo.py` FALLITO** per 1 contatto su 37: semaforo verde un passo prima, penalità al giocatore per la regola 10. Probabile fine di una virata dell'altra barca proprio in quel momento (la 13 lascia il posto alla 10; il passaggio lo regola la 15, livello 2): non verificato passo per passo.

**In sintesi:** gli avversari non si piantano più (piantate da 36 a 2, quelle avendo la precedenza da 16 a 1, sui semi mai guardati) e arrivano in un tempo simile, ma si toccano di più (penalità da 73 a 97, +33%). Prima evitavano tutto, anche quando la precedenza era loro, e così si fermavano. Decide Ale.

**Decisione di Ale (26 ottobre 2026, dopo una regata nei salti di vento):** tenuta. L'1a non si corregge: «se sono meno bravi lo sono come me; è meno frustrante se inizio a giocare e vedo gli altri che ancora non sono esperti». Niente aiuto a schermo per i salti di vento («troppi aiuti non li vorrei»): si leggono dalla prua nel pannello. Visti giocando e già nelle misure: una barca che esce dalla linea di lato e rientra (non si tocca, §7), una che gira la boa dal lato sbagliato cedendo vicino alla boa (va con la regola 18, livello 2).
