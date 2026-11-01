# Diario delle modifiche

I difetti sono riportati con la causa, perché ricordare come sono nati aiuta a non ripeterli.

**Le versioni dalla 0.1 alla 0.19.5 sono in `docs/archivio/CHANGELOG-0.1-0.19.md`** (spostate il 13 ottobre 2026), **quelle dalla 0.20 alla 0.24 in `docs/archivio/CHANGELOG-0.20-0.24.md`** (spostate il 16 ottobre 2026); testo invariato. I rimandi degli altri documenti a «`CHANGELOG.md`, 0.2x» si trovano lì. **Dal 23 ottobre 2026 le proposte finite stanno in `docs/archivio/`**: qui sotto sono citate col percorso di allora (`docs/PROPOSTA-…`).

**Nomi dei livelli:** fino alla 1.0.46 queste voci chiamano spesso «livello 2» la barca dell'1b; nelle più vecchie «livello 2» è anche il fiocco, che oggi è il livello 3 (`docs/VISIONE-LIVELLI-E-CARRIERA.md` §2).

## Sperimentale

Prove che **non sono versioni del gioco**: vivono in `sperimentale/` e non toccano `index.html`. Verificato a ogni passo che, per una barca a una vela sola, polare, virate e raffiche restino identiche a quelle del gioco.

- **Prototipo del fiocco** (`sperimentale/fiocco.html`), in vista di una futura deriva a due. Tappa A: il fiocco come seconda superficie portante, con scotta propria (tasti Q ed E), filetti e disegno. Tappa B: la randa che copre il fiocco alle andature larghe, e il pannello che dice chiaramente dove il fiocco non si regola. Costanti, semplificazioni e fonti in `FISICA-E-TARATURE.md` e `CONTENUTI-DA-VERIFICARE.md`. Non ci sono ancora l'upwash della randa sul fiocco, il fiocco a collo in virata e la manovra a farfalla.
- **Prototipo del fiocco, tappa C, primo compito: la vista e la forza del fiocco coperto adesso dicono la stessa cosa.** In tappa B il pannello diceva «qui non si regola (coperto dalla randa)» mentre il fiocco dava ancora dal 10% al 19% della spinta. Portare solo `slotShade` a 1,0 non bastava: fra 107° e 135° di vento apparente ne restava il 16-10%, perché lì l'ombra era ancora parziale. Ritarate tre costanti: `slotA0` 85→**95**, `slotW` 50→**12**, `slotShade` 0,70→**1,00**. L'ombra ora è nulla fino a 95° apparenti e totale da 107°, che non è un numero scelto ma l'angolo oltre il quale non esiste più una posizione del fiocco con i filetti dritti. `jibShadedAt` perde la soglia propria e diventa «`jibRange` nullo»: strumento e messaggio del pannello non possono più contraddirsi. **Misure:** quota di spinta del fiocco da 108° a 180° apparenti, grado per grado, **0,00%** (soglia dichiarata 3%); nessuna ombra fino a 95°; bolina +10,9% contro larghe +6,3% (il confronto regge); polare senza nuovi denti; nessuna bistabilità su sei andature larghe partendo da ferma e lanciata; non-regressione senza fiocco a scarto zero e uscite di `polare.js` e `raffiche_e_virate.js` identiche carattere per carattere. **Prezzo dichiarato:** la curva si irrigidisce fra 126° e 132° reali (massima variazione 0,163 nodi/° contro 0,085 in tappa B), e la prova 2 «Lasco e poppa» torna esattamente al tempo del gioco (149 s contro 145/142 della tappa B), perché su un percorso portante il fiocco ora non dà più niente. **Difetto nel collaudo, trovato e corretto:** la verifica «senza `#collaudo`» cliccava il titolo del menu invece del pulsante, il gioco non partiva e la prova passava leggendo «—» dappertutto; ora controlla di essere partita e di aver attraversato davvero le andature che dice di misurare.
- **Prototipo del fiocco, tappa C, secondo compito: il momento di imbardata dovuto alle vele non si modella, e la semplificazione è dichiarata.** Si era proposto di modellare il solo contributo del fiocco, lasciando alla randa l'equilibrio implicito nel motore. Misurato fuori dal motore, senza toccare `step()`: su 12 casi (6, 10 e 14 nodi × 45°, 70°, 90° e 110° reali) quel momento fa poggiare **12 volte su 12**, e il termine che dovrebbe far orzare sbandando non arriva mai a ribaltarlo (dal 3% al 23% dell'altro). F4 dice il contrario: barca piatta e vele regolate, la barra sta circa al centro; sbandando, la barca orza. Emulando quel momento con la barra libera, a 10 nodi la barca partita a 45° dal vento è a 75° dopo 10 s e a 124° dopo 60, cioè circa 3 °/s di scarto: ingiocabile. Il momento riguarda **tutta la barca** — randa, fiocco, scafo sbandato — e non si aggiunge a metà. Il motore non è stato toccato (`git diff` vuoto su `fiocco.html` e `index.html`). Il termine che farà girare la prua col fiocco a collo starà nel terzo compito e dovrà funzionare anche a barca ferma, dove questo valeva zero.
- **Prototipo del fiocco, tappa C, terzo compito: il fiocco a collo in virata non si modella, e la semplificazione è dichiarata.** Provati due modelli fuori dal motore, senza toccare `step()` (`git diff` vuoto su `fiocco.html` e `index.html`). Quello senza memoria del lato del fiocco è peggio di niente: resiste nella prima metà della virata e le riuscite scendono da 75 a 69 su 84. Quello con un filo di memoria funziona (`backRate` 12 °/s, `backT` 1,2 s; virata di bolina a 10 nodi da 4,35 a 3,79 s col fiocco cazzato, da 75 a 78 riuscite su 84, da 179 a 188 su 200 tentativi con seme fisso), ma è stato scartato lo stesso: in un motore cinematico è una **taratura**, con due costanti senza nessuna fonte e il verso scritto nel codice, quindi «col fiocco cazzato si vira meglio» è vero per costruzione; le soglie dei criteri erano state scritte dopo aver visto i numeri del banco, contro le regole dei prototipi; la memoria del lato del fiocco **sostituisce l'equipaggio** e andrebbe rifatta con il prodiere e le due scotte della barca a due (tappa C4); il guadagno è modesto (col fiocco lascato da 136 a 138 su 200); e si perderebbe un comportamento in navigazione libera, perché col fiocco cazzato non ci si potrebbe più fermare nell'angolo morto. **Oggi in virata il fiocco conta solo per la resistenza della vela che sbatte**, non perché vada a collo. Modello, criteri, rischi e numeri restano in `sperimentale/PROPOSTA-C3.md`, `banco_tappaC3.js` e `banco_tappaC3.txt` come registro della decisione.
- **Prototipo del fiocco, tappa C chiusa, quarto compito: la barca a due non si modella e il sovrainvelamento si dichiara.** Il prototipo resta con lo scafo e il timoniere del gioco a una vela (135 kg, un velista da 75 kg) e il 37% di vela in più: una raffica da 20 nodi fa scuffiare e a 15 nodi la virata non riesce. Il banco di confronto proposto (quattro configurazioni da 135 a 250 kg, 108 raffiche, 12 soglie di scuffia, 132 equilibri di polare, 288 virate, 36 giri nel browser) **non è stato eseguito**, perché i conti che già avevamo bastavano a decidere, e `step()` e `sperimentale/fiocco.html` **non sono stati toccati** (`git diff` vuoto). Tre ragioni: (1) la coppia raddrizzante del prototipo vale **83,7 kgf·m** al massimo, a 22,6° di sbandamento, contro i **circa 60 kgf·m** che la fonte dà a una deriva a due **senza** trapezio, quindi quella barca sarebbe **meno** stabile di questa, e l'unica configurazione che risolve il sovrainvelamento è quella **col trapezio** (circa 220 kgf·m), che per il livello 2 sarebbe una **seconda novità principale**; (2) nel motore la **massa non entra nella resistenza dello scafo**, quindi una barca più pesante andrebbe a regime più **veloce** perché sbanda meno, e per ritarare `hullK2` e `hullK4` non c'è fonte (polari pubbliche di derive non risultano, F10 non letta); (3) il **peso dell'equipaggio dovrebbe diventare un'azione del prodiere** (lezione 2.5), non l'automatismo da 0,9 s di oggi. Annotata anche, senza cambiarlo, l'incoerenza del timone: a 6 nodi il motore dà 21,2 kgf di resistenza dello scafo contro i 19 della fonte (vicina) ma solo 2,9 kgf di timone a 15° contro 12, e arriva a 10,9 solo vicino a 30°; soprattutto **la pala non stalla mai**, così la barra a fondo fa girare 1,93 volte più in fretta che a 15° ed è sempre la scelta migliore, mentre nella realtà no. Conseguenza per il gioco: **il livello 2 va giocato con vento da leggero a medio** (sopra i 12-15 nodi circa, limite da decidere con le lezioni). Con questo la tappa C è chiusa: proposta e criteri in `sperimentale/PROPOSTA-C4.md`, decisione e stato finale del prototipo in fondo a `FISICA-E-TARATURE.md`.


## 1.1.9 — Gruppo D, prima parte: lezioni D1-D4 sul regolamento (nascoste nel menu, ramo `pulizia`)

Le prime quattro delle sette lezioni sul regolamento (`docs/PROPOSTA-LEZIONI-2A.md`, approvata il 31 ottobre): D1 «Mure opposte», D2 «Stesse mure», D3 «Chi vira cede», D4 «Evitare il contatto». Sono `LESSONS[11]`-`LESSONS[14]`, con `nascosta: true` e `gruppo: "D"`.

**Fonti:** le regole 10-16, le definizioni (libera dietro e avanti, sovrapposte, sopravento e sottovento, tenersi lontano) e la regola 43.1(c), rilette oggi nel PDF di F15. Le regole sono parafrasate, con il numero.

**Il testo dice quello che fa il gioco.** Il gioco applica le regole 10, 11, 12 e 13 (`chiCede`, 1.0.40, provate da `collaudo_regole.py` e `collaudo_semaforo.py`). Le regole 14, 15 e 16 non le applica, e non ci sono danni: la D4 lo dice. Le penalità scritte nella D1 (15 s, due giri, un punto nel torneo) sono quelle degli avvisi del gioco.

**Campo nuovo delle pagine di teoria, `scena`:** barche ferme accanto a quella della lezione, disegnate con la funzione degli avversari (`drawOther`), con il colore dello scafo e una scritta sotto ciascuna. `scenaH` dà la prua della barca della lezione e `me` la sua scritta. Controllato con gli screenshot: nella prima stesura la barca rossa della D1 finiva sul bordo dello schermo, ed è stata avvicinata da 28 a 14 m.

**Rimandato, ed ecco perché:**
- **Gli esercizi pratici in regata** (proposta §2: «prove in regata con il semaforo»). Oggi una lezione non può aprire una regata. Lo stesso meccanismo serve alle partenze del gruppo C, quindi si fa una volta sola, insieme. Per ora le D1-D4 sono teoria, disegni, quiz (4 domande) ed esame (4 domande). La D4 doveva restare solo teoria comunque.
- **La pagina sulle precedenze della lezione 3** resta finché le lezioni D sono nascoste. Se la togliessi adesso, chi gioca non troverebbe più le precedenze da nessuna parte. Si toglie insieme al menu nuovo, con il titolo «Andature e mure».

**Misurato:**
- `collaudo_pannello_lezioni`: 83 passi su 83 a 0 px, in Chromium e in Firefox. Pagina senza errori.
- Verdi `collaudo_lezioni`, `collaudo_quiz`, `collaudo_esame`, `collaudo_carriera`, `collaudo_carriera_intera`, `collaudo_libretto`, `collaudo_versione`.
- Il pilota delle lezioni percorre anche le D1-D4: 0 passi pratici, perché non ne hanno. Il numero atteso dei passi pratici per lezione è stato aggiornato, così il metro non dà per buono uno zero che non dovrebbe esserci.
- Fisica identica al bit.

## 1.1.8 — Lezione B5 «I salti di vento» (nascosta nel menu, ramo `pulizia`): il gruppo B è completo

Quinta lezione del gruppo B, undicesima nel gioco (`LESSONS[10]`, `nascosta: true`).

**Fonte, letta oggi prima del testo:** Dellenbaugh, «Windshift Rules of Thumb», *Sailing World* (nuova **F41**). La proposta delle lezioni diceva che per la B5 mancava una fonte sulla bolina nei salti, perché si citava F7, che parla delle andature portanti. In realtà quella fonte c'era già in `archivio/PROPOSTA-SALTI-VENTO.md`, senza numero: ora è riletta e numerata. È una sola fonte, di un allenatore su una rivista, e il testo lo dice («in un esempio di un allenatore»). Due fonti della stessa proposta non sono state rilette: WindCheck, che ha rifiutato la lettura, e la guida di Raymarine. Il testo non usa niente di loro.

**La lezione:** due pagine di teoria («Il vento gira», «Vira sugli scarsi»), un passo pratico e il riepilogo; 4 domande di quiz e 4 per l'esame.
- **Campo nuovo dei passi, `shifts`:** accende i salti di vento delle regate dell'1b (`SALTI2`, 1.0.28: 12-15° per parte, una mezza oscillazione ogni 60-75 s). Il testo dice che nel gioco il vento oscilla più in fretta che nell'esempio della fonte.
- **Passo pratico «Vira sullo scarso»:** il vento medio arriva da nord, come dice la scritta del vento, e lo scarso si legge con la «Prua» del pannello. La vela si regola da sola. Il passo vale con **due virate fatte da scarsi di almeno 7°**, poi 3 s di bolina sopra i 2 nodi. Una virata fatta da buoni di almeno 3° fa fallire il passo: compare un avviso e si preme Ricomincia. Contano solo le virate volute, cioè con la barra verso il boma negli ultimi 4 s, e partite da bolina, cioè fra 35° e 75° dal vento negli ultimi 4 s.

**Come si è arrivati alla condizione (soglie cambiate dopo aver visto i numeri, ecco quali):**
1. Prima stesura: una virata da scarsi di almeno 5°. Il pilota bravo passava 10 volte su 10, ma anche un pilota che vira a caso ogni 20 s passava 10 volte su 10: il passo non distingueva niente.
2. Soglia a 7° e virata da buoni che fa fallire. Chi vira a caso passava ancora 6 volte su 10, e il pilota bravo passava solo 8 volte su 10. La causa era nel pilota: decideva prima di essere di bolina e virava su uno «scarso» letto male. È stato corretto, e ora decide dopo 3 s di bolina tenuta, come chiede il testo. Nello stesso giro sono state aggiunte le due regole «virata voluta» e «partita da bolina».
3. Una virata non bastava ancora: chi vira a caso passava 6 volte su 10. Con **due virate** le attese erano state scritte prima di misurare: pilota bravo almeno 9 su 10, chi vira a caso molto sotto la metà.

**Misurato (versione finale):**

| Pilota | semi 1-10 | semi 11-20 (conferma) |
|---|---|---|
| bravo (vira quando legge 10° di scarso) | 10 su 10, in media 105,1 s | 10 su 10, 104,7 s |
| a mani ferme, 30 s (collaudo) e 120 s | 0 su 10 | 0 su 10 |
| vira a caso ogni 20 s | 0 su 10 | **1 su 10** |
| vira quando è buono di 8° | 0 su 10 | 0 su 10 |

- Il passo è lungo, circa due minuti, perché bisogna aspettare due scarsi.
- Lasciata a sé per 120 s, la barca non vira mai da sola: 0 virate su 20 semi.
- `collaudo_pilota_lezioni.py --solo 11` per l'undicesima lezione.
- `collaudo_pannello_lezioni`: 72 passi su 72 a 0 px, in Chromium e in Firefox.
- Verdi `collaudo_lezioni`, `collaudo_quiz`, `collaudo_esame`, `collaudo_carriera_intera`, `collaudo_libretto`, `collaudo_versione`.
- Fisica identica al bit. Le regate non cambiano: il campo `shifts` agisce solo nei passi delle lezioni.

## 1.1.7 — Lezione B4 «La raddrizzata lunga» (nascosta nel menu, ramo `pulizia`)

Quarta lezione del gruppo B, decima nel gioco (`LESSONS[9]`, `nascosta: true`).

**Fonti**, scritte nel codice sopra la lezione:
- **Il video di un allenatore** (19 ottobre 2026) è l'unica fonte per la barca con una persona sola. È divulgativo e il testo lo dice («un allenatore, in un video»). **La trascrizione non è salvata nel progetto**: ho usato il riassunto di `docs/archivio/PROPOSTA-RADDRIZZATA.md`. Dice: schiena al vento, albero sottovento, vela che sale e sbatte libera, 15-20 s dalla scuffia alla barca che naviga.
- **La dispensa di una scuola di vela** (`fonti-pdf/Dispensa-Scuola-Vela-2019.pdf`, pp. 24-25, riletta oggi): non si lascia la barca; con le vele cazzate la barca non si raddrizza; spalle al vento; piedi vicino allo scafo. Con l'equipaggio insegna anche a tenere la barca con la prua al vento. **Questo il gioco non lo fa, e il testo lo dice.** È una fonte informale: per decisione di Ale non diventa domande di quiz, e infatti quiz ed esame si reggono sul video e sul gioco.
- W4 e W5 (`DUBBI-E-RICERCHE.md` §3), due fonti deboli: le scotte vanno libere.

**La lezione:** due pagine di teoria («Prima di raddrizzare», «Spalle al vento»), un passo pratico e il riepilogo; 4 domande di quiz e 4 per l'esame.
- **Passo pratico:** «Raddrizza e riparti». La barca parte scuffiata, con 12 nodi e raffiche leggere. Il passo vale se la barca, dopo essere stata raddrizzata, va fra 60° e 120° dal vento ad almeno 2,5 nodi con i filetti dritti, per 1 s.
- **Trovato misurando:** premendo solo A e poi più niente, con la vela che sbatte, la barca arriva da sola a 2,4-3,2 nodi in 30 s (semi 1-10). Per questo il passo chiede anche i filetti dritti, e una risposta sbagliata dell'esame, «aspetto che riparta da sola», è stata cambiata: nel gioco non era del tutto falsa.

**Misurato:**
- pilota delle lezioni esteso alla B4 (A, attesa, poi colpi di scotta guardando i filetti): semi 1-10, guidando 10 su 10 (in media 14,3 s), a mani ferme 0 su 10; semi 11-20 lo stesso. Premendo solo A: 0 su 10.
- `collaudo_pilota_lezioni.py --solo 10` per la decima lezione (una cifra non bastava più; `--solo 1,10` per più lezioni).
- `collaudo_pannello_lezioni`: 68 passi su 68 a 0 px, in Chromium e in Firefox.
- Verdi `collaudo_lezioni`, `collaudo_quiz`, `collaudo_esame`, `collaudo_carriera_intera`, `collaudo_libretto`, `collaudo_versione`.
- Fisica identica al bit.

## 1.1.6 — Lezione B3 «La barca che orza sbandando» (nascosta nel menu, ramo `pulizia`)

Terza lezione del gruppo B, nona nel gioco (`LESSONS[8]`, `nascosta: true`).

**Fonti rilette nei PDF prima del testo**, scritte nel codice sopra la lezione:
- F4 (`fonti-pdf/sname-jst-2020-05.pdf`): p. 28 e fig. 13, di bolina con la barca dritta la barra sta circa al centro; p. 32, eq. 6, sbandando il centro velico va sottovento e la barca orza di più; p. 33, anche lo scafo sbandato orza da solo, senza numeri.
- F38 (`fonti-pdf/HANDBOOK_2025.pdf`, pagina «Rudder and Tiller»): sbandata, la barca diventa molto orziera; poggiare sbandati carica molto pala e barra, ed è così che si rompono; prima si raddrizza, sporgendosi o lascando.
- **Semplificazione detta nel testo:** nel gioco conta solo la vela (il termine della 1.0.46), lo scafo sbandato non fa orzare.

**La lezione:** due pagine di teoria («Perché la barca orza», «Nella raffica»), un passo pratico e il riepilogo; 4 domande di quiz e 4 per l'esame.
- **Passo pratico:** «La rotta nella raffica». Al traverso, 12 nodi, una raffica media (+45%) che arriva da sola, come nella lezione 6. Il passo vale se nel cuore della raffica la prua resta entro 6° dalla rotta indicata, lo sbandamento sotto 15° e la velocità sopra 2 nodi, per 2 s di fila.
- **Il testo dice quello che il gioco fa** (misurato sul motore, 12 nodi al traverso, raffica +45% per 6 s, vela regolata):
  - con la barra al centro la prua sale di 19° (5° senza raffica);
  - tenendo la prua con la sola barra servono 2,5° di barra e la barca sbanda fino a 22°;
  - lascando un poco (0,15) bastano 1,1° di barra e la barca sbanda fino a 11,5°.
  - Nel gioco, a mani ferme, in 30 s la barca passa dal traverso a circa 40° dal vento e sbanda fino a 39-51° (semi 1-10).

**Corretto, trovato rileggendo:** i testi della lezione B1 (1.1.4) dicevano tre volte «470», il nome di una classe, contro il principio 5. Ora dicono «una deriva da regata». Il nome resta solo nei commenti del codice, che citano la fonte.

**Misurato:**
- pilota delle lezioni esteso alla B3: semi 1-10, guidando 10 su 10 (in media 17,1 s), a mani ferme 0 su 10. Semi 11-20: lo stesso (17,4 s).
- `collaudo_pannello_lezioni`: 64 passi su 64 a 0 px, in Chromium e in Firefox.
- Verdi `collaudo_lezioni`, `collaudo_quiz`, `collaudo_esame`, `collaudo_carriera_intera`, `collaudo_libretto`, `collaudo_versione`.
- Fisica identica al bit (`polare.js`, `raffiche_e_virate.js`, `impronta1b.js`).

## 1.1.5 — Lezione B2 «Spingere il boma» (nascosta nel menu, ramo `pulizia`)

Seconda lezione del gruppo B, ottava nel gioco (`LESSONS[7]`, `nascosta: true`).

**Fonti lette prima del testo**, scritte nel codice sopra la lezione:
- `docs/archivio/PROPOSTA-SPINGI-BOMA.md` §1: US Sailing, la guida di un circolo per una deriva in singolo, Australian Sailing «Sailing Backwards», un allenatore di partenze. Tutte dicono boma spinto fuori, barra dalla stessa parte, la barca arretra e la prua gira verso il boma; al traverso si molla, si centra e si cazza. Nessuna dà numeri.
- Regola 21.3 di F15, **riletta nel PDF**: chi va all'indietro, o di lato verso il vento, spingendo una vela si tiene lontano da chi non lo fa. **Il gioco non la applica, e il testo lo dice** (come deciso per le regole che il gioco non fa).

**La lezione:** due pagine di teoria («Fuori dall'angolo morto», «All'indietro, apposta»), un passo pratico e il riepilogo; 4 domande di quiz e 4 per l'esame.
- **Passo pratico:** «Spingi il boma e riparti». La barca parte ferma nell'angolo morto (campo nuovo dei passi, `startIrons`: prua a 10° dal vento, ferma, vela lascata). Il passo vale se il boma è stato spinto (Z) per almeno 0,5 s in tutto e poi la barca va avanti al traverso, fra 60° e 120° dal vento, ad almeno 1,5 nodi, per 1 s.
- **Il testo dice quello che il gioco fa** (misurato, 10 nodi):
  - a mani ferme, in 30 s, la prua passa solo da 10° a 20° dal vento e la barca scivola all'indietro a 1,8 nodi. Per questo la prima stesura, «la barca prima o poi poggia da sola», è diventata «resta lì a lungo e scivola all'indietro»;
  - con Z e la barra verso il boma la barca arretra fino a 2,4 nodi, la prua gira verso il boma ed è al traverso in 2,7 s.

**Misurato:**
- pilota delle lezioni esteso con Z: semi 1-10, guidando 10 su 10 (in media 6,7 s), a mani ferme 0 su 10. Semi 11-20: lo stesso (6,6 s).
- `collaudo_pannello_lezioni`: 60 passi su 60 a 0 px, in Chromium e in Firefox.
- Verdi `collaudo_lezioni`, `collaudo_quiz`, `collaudo_esame`, `collaudo_carriera_intera`, `collaudo_libretto`.
- Fisica identica al bit.

## 1.1.4 — Lezione B1 «Il timone che stalla» (nascosta nel menu, ramo `pulizia`)

Prima lezione del gruppo B (`docs/PROPOSTA-LEZIONI-SCUOLA.md`). Come ha deciso Ale il 1 novembre, **non compare nel menu** finché non arriva il menu nuovo: nel gioco è la settima lezione (`LESSONS[6]`, `nascosta: true`). Il libretto, i meriti, il ripasso e il pulsante del quiz la ignorano. Quiz ed esame stanno nella lezione e si collegano col menu.

**Fonti lette prima del testo** (`docs/archivio/PROPOSTA-STALLO-TIMONE.md` §1, §9, §10), e scritte nel codice sopra la lezione:
- F4 (vasca, modellino del 470): la forza della pala cresce fino a circa 15° e poi resta uguale, mentre la resistenza continua a crescere. Nelle virate vere la barra arriva a 45°, e accompagnarla è il modo più ragionevole.
- F35 (calcolo a grandezza vera): stallo a circa 30°.
- Day 2017: l'angolo che la pala sente non è quello della barra.
- Regole di questo gioco, dichiarate come tali nel testo: la sola freccia arriva a 35° (1.0.25), Maiusc a 45°.

**La lezione:** due pagine di teoria («La pala è un'ala», «35° e 45°»), un passo pratico e il riepilogo; 4 domande di quiz e 4 per l'esame. Nel glossario nessuna voce nuova: «Stallo» c'è già (per la vela).
- Il **passo pratico** è «Una virata con la barra in fondo»: virata riuscita, con la barra oltre 36° (cioè con Maiusc) per almeno 0,3 s in tutto. Il conteggio è nuovo (`base.maiusc`), con lo stesso metodo della barra sottovento della 1.1.3.
- Un passo «fai stallare la pala» non c'è, perché **con i tasti la pala non stalla**. Misurato: 0 s di stallo in 6 prove, partendo da 2, 3 e 5,5 nodi, con 35° e con 45°. La barca comincia a girare prima che l'angolo diventi troppo grande (1.0.31). Il testo lo dice: «con i tasti la pala stalla di rado; se succede, il pannello lo dice».

**Misurato:**
- `collaudo_pilota_lezioni.py --solo 7` (pilota esteso: vira tenendo Maiusc): semi 1-10, guidando 10 su 10, a mani ferme 0 su 10, tempo medio 3,3 s. Semi 11-20: lo stesso.
- Tutte le lezioni, semi 11-20: 32 passi 10 su 10 e il 6.3 9 su 9, come nella 1.1.3.
- `collaudo_pannello_lezioni`: 56 passi su 56 a 0 px, in Chromium e in Firefox.
- Verdi `collaudo_lezioni`, `collaudo_quiz`, `collaudo_esame`, `collaudo_carriera`, `collaudo_carriera_intera`, `collaudo_carriera_esame`, `collaudo_libretto`, `collaudo_pannello`, `collaudo_schermate`, `collaudo_pulsanti`. Il menu non cambia.
- Fisica identica al bit.
- Il pilota riconosce l'ultimo passo anche dalla scritta del pulsante: le lezioni nascoste non hanno il pulsante del quiz, e senza questa correzione andava oltre la fine (720 errori della pagina nella prima prova).

## Collaudi: il giro mirato delle partenze sui semi 1-100 (1 novembre 2026, nessuna versione nuova)

- Su GitHub, versione `97d3dde` (guida degli avversari della 1.1.2), `collaudo_non_partite` con i semi 1-100: in tutto 7200 barche per browser.
  - **Chromium:** 3 non partite su 7200 (0,04%), tutte nella regata dei salti. Bastone, raffiche e giri: 0.
  - **Firefox:** 9 su 7200 (0,13%): 8 nei salti (semi 22, 36, 47, 54, 56, 80) e 1 nelle raffiche (seme 89).
  - Nella 1.1.0 era l'1,7% (25 su 1440).
  - I due browser danno casi diversi, perché i conti differiscono all'ultima cifra e le traiettorie si separano. Il seme 22 in Firefox cade dentro i semi 1-40 che avevo misurato solo in Chromium.
- **Decisione di Ale:** il residuo si accetta e si annota; ci si torna lavorando sugli avversari. Nel giro normale (semi 1-20) il collaudo è verde in tutti e due i browser.

## 1.1.3 — Lezioni, gruppo A, prima parte: i cinque passi che la barca dell'1b rompeva (ramo `pulizia`)

Prima fetta di `docs/PROPOSTA-LEZIONI-SCUOLA.md`. La fisica non cambia: `impronta1b.js` identica al bit, `polare.js` e `raffiche_e_virate.js` identici.

**La causa, misurata.** Dal traverso, con la barra al centro e la vela che si regola da sola, la barca dell'1b orza da sola di circa 0,8° al secondo, già con 4-6° di sbandamento. È la barca orziera della 1.0.46 (fonte F4). In 30 s passa da 90° a 67° dal vento:
- nei passi 2.4 «Barra sottovento: si orza», 3.2 «Bolina» e 5.2 «Prepararsi a virare» entrava da sola nel settore della bolina;
- nel 6.2 «Assorbire una raffica» la raffica la faceva sbandare (fino a 52°) e poi orzare fino a 40° dal vento, così la vela si scaricava da sola;
- nel 3.10 «Filetto sottovento» il passo non ha la barra: la barca orzava fino a 32° dal vento, dove il filetto sottovento non si può agitare. In più la condizione chiedeva un angolo d'attacco oltre 29°, ma il filetto si agita già da 27°: chi si fermava appena lo vedeva agitarsi (come dice il testo) non arrivava mai alla soglia.

**Correzioni, solo nelle lezioni:**
- **2.4, 3.2, 5.2:** il passo vale solo se il giocatore ha **spostato davvero la barra verso il boma** (barra sottovento) per almeno 0,1 s in tutto. Conta solo la barra mossa in quel momento, con i tasti o il cursore: quella rimasta dal passo prima non vale.
- **6.2:** il passo vale solo se il giocatore ha **lascato durante la raffica**, almeno 0,05 di scotta in tutto. È la tecnica che la lezione insegna.
- **3.10:** la condizione è il filetto sottovento agitato, cioè quello che il giocatore vede, per 0,5 s. Prima chiedeva un angolo oltre 29° per 1 s.
- **Nei passi senza barra (3.8-3.10, 4.2, 4.3) la rotta la tiene la scuola**, come la vela si regola da sola nei passi con `autoTrim`. È una semplificazione dichiarata e scritta nei testi dei passi 3.8 e 4.2. Con la 1a, a barra ferma, la rotta restava quella; con la barca orziera dell'1b no.
- **6.4 «Raddrizzare»:** il testo dice che ci vogliono una decina di secondi e che la barca torna dritta al traverso, con la vela lascata. È il comportamento dell'1b (1.0.32).
- **Soglie del gioco, scelte sui semi 1-10 e confermate sui semi 11-20:** 0,3 s di barra, poi 0,2 s, poi 0,1 s.
  - Con 0,3 s, 3.2 e 5.2 si completavano guidando 6 volte su 10: dopo l'attesa a mani ferme la barca è già quasi in bolina e basta poca barra.
  - Con 0,2 s, 3.2 era a 8 su 10.

**Misurato** (`collaudo_pilota_lezioni.py`):
- **Semi 1-10: 32 passi su 32 completati guidando 10 volte su 10, 0 passi che si completano da soli.** Con la 1.1.0: 27 su 32, il 3.10 mai completato, 4 passi completati da soli.
- **Semi 11-20 (conferma):** 31 passi 10 su 10 e il 6.3 «La scuffia» 9 su 9. Il 6.3 si completa da solo 1 volta su 10: è noto e voluto dalla 1.0.15 (con la 1a succedeva 6 volte su 10), perché lì si scuffia apposta.
- «Già fatto dopo un colpo lungo» 1 volta su 10 per 3.5 «Poppa» e per 6.3, il tipo già noto.

**Collaudi:**
- `collaudo_lezioni` verde in Chromium e Firefox (18 passi). Il colpo di scotta del suo «L5 prepararsi» passa da 1,5 a 1,0 s: era tarato sulla 1a e con l'1b la vela finiva troppo cazzata. Provati 1,0, 0,7 e 0,5 s, tutti OK.
- `collaudo_carriera_intera` di nuovo verde: tolte le sue voci dai fallimenti noti.
- Verdi anche `collaudo_registro` (15 su 15), `collaudo_suggerimento`, `collaudo_pannello` (Chromium e Firefox), `collaudo_quiz`, `collaudo_libretto`.
- **Nuovo `collaudo_pannello_lezioni.py`** (nel giro): misura il pannello a 1360×650 in **tutti i 52 passi** delle lezioni, con il testo di fine passo. Ha trovato un difetto vecchio: il **6.4 sforava di 17 px** già prima, e nessun collaudo lo misurava. Con la prima versione del testo nuovo arrivava a 41 px; il testo accorciato lo porta a 0 px in Chromium e in Firefox. Sulla 1.1.2 la stessa misura trova i 17 px: il metro se ne accorge.

**Ancora da fare nel gruppo A:** togliere le precedenze dalla lezione 3. Si fa insieme alle lezioni del gruppo D, così il contenuto non resta scoperto per un periodo. Poi il controllo frase per frase dei testi contro la barca dell'1b (criterio L2).

## Collaudi dopo il giro su GitHub della 1.1.2 (1 novembre 2026, nessuna versione nuova)

- Giro completo su GitHub, Chromium e Firefox: **cadono solo `collaudo_lezioni`** (passo 5.2, va col gruppo A delle lezioni), **`collaudo_registro`** (Chromium) e una serie di fallimenti noti con i numeri cambiati.
- **`collaudo_registro`, corretto:** contava come «contatto annunciato al giocatore» anche il messaggio «Contatto fra X e Y», che riguarda due avversari e dalla 1.1.0 compare in tutte le regate. Ora conta solo i messaggi che non cominciano con «Contatto fra». Rilanciato qui: 15 su 15.
- **Fallimenti noti aggiornati** con le righe del giro (`tests/fallimenti_noti.txt`, ogni voce col motivo):
  - `collaudo_partenze`, Chromium e Firefox: oltre al criterio (1), noto, il (2), cioè le partenze lente con 300 s nelle raffiche, circa 8 s. È un difetto degli avversari dell'1b presente dalla 1.1.0.
  - `collaudo_virate2` e `collaudo_competizione` (misura): stessi criteri di prima, numeri della 1.1.2.
  - `collaudo_giri_avversari` in Firefox: G4 ha trovato 14 casi di due giri di fila contro i 15 che il metro chiede. La mediana (22,2 s) è dentro la soglia. G2 è all'82% (soglia 80%; nella 1.1.0, in Firefox, 91%).
- Il collaudo nuovo `collaudo_non_partite` è verde in tutte e quattro le regate, in tutti e due i browser.

## 1.1.2 — Gli avversari cedono come prima dopo il via; collaudi sistemati dopo il giro della 1.1.1 (ramo `pulizia`)

Il giro su GitHub della 1.1.1 ha trovato un peggioramento vero: con la correzione A (cedere solo a chi si avvicina) in tutta la regata, gli avversari estinguevano meno debiti di giri. `collaudo_giri_avversari` G2 era all'80% in Chromium e al 74% in Firefox, contro il 93% e il 91% della 1.1.0, con soglia 80%.

**Correzione:** A vale solo in partenza, finché la barca non ha tagliato la linea (`b.leg === 0`). Dopo il via gli avversari cedono come nella 1.1.0. B1 e B2 restano come nella 1.1.1.

**Prove senza ciascuna correzione** (G2, Chromium, 40 regate):
- 1.1.1 così com'era: 80%;
- senza A: 90%;
- senza B1: 86%;
- senza B2: 80%.

**Misurato sulla 1.1.2:**
- **Barche non partite:** semi 1-20, 0 su 1440; semi 21-40 (conferma), **0 su 1440**. Anche il caso del seme 40 che Ale aveva accettato ora parte. La scelta di limitare A alla partenza è venuta dopo aver visto i numeri della 1.1.1, e lo dico: i semi 21-40 erano già stati usati come conferma della 1.1.1.
- **Contatti in 80 regate intere:** 333, contro 332 della 1.1.0 e 374 della 1.1.1.
- **`collaudo_giri_avversari`:** verde, G2 **92%**, G1 102 su 102.
- **`collaudo_avversari1b`, scenario 5:** di nuovo 7 su 10, come nella 1.1.0. Il 9 su 10 della 1.1.1 veniva da A in tutta la regata.
- **Fisica:** `impronta1b.js` identica al bit.
- **Partenze lente nelle raffiche** (criterio (2) di `collaudo_partenze`): non le ha portate la 1.1.1. Nel giro della 1.1.0 il ritardo mediano con 300 s era già di 12,4 s per i principianti e di 8,3 s per gli esperti, e con 180 s di 7,4 s; nella 1.1.1 è sceso a 7,9 s, 8,2 s e 2,3 s. Resta fuori soglia (3 s) da quando la regata nelle raffiche ha gli avversari dell'1b: difetto noto, da guardare con gli avversari.

**Collaudi corretti** dopo il giro della 1.1.1:
- `collaudo_regola21` (K2, K3): il caso costruito ora azzera i richiami (21.1) e i debiti degli avversari (21.2). Con la guida nuova il pilota a volte era ancora oltre la linea, o un avversario stava scontando, e la regola misurata era giustamente 21.1 o 21.2.
- `collaudo_giri` E1: si aspetta 15 s per ogni giro non fatto, invece di 30 s fissi. In Firefox, seme 501, il pilota tocca anche la boa e i giri non fatti sono 3, +45 s, come deve essere.
- `collaudo_moto_mare`: salti di vento spenti, perché misura il moto con la prua fissa rispetto al vento. Era rimasto indietro dalla 1.1.0.
- `collaudo_boma_poppa` B4a, `collaudo_riquadro_bandiere` Q6a, `collaudo_scotta_automatica` A1: da quando cambia la guida degli avversari, nessuna regata può più essere identica alle versioni vecchie (1.0.69-1.0.72). Il confronto delle regate ora è **solo riportato**, e A1 confronta solo le corse a scotta fissa. Il controllo «la modifica non cambia le regate» lo fa `tests/arrivi_regate.py` a ogni modifica.
- Verdi qui: `collaudo_regola21` (Chromium e Firefox), `collaudo_giri` (Chromium e Firefox), `collaudo_linea` (Firefox), `collaudo_moto_mare`, `collaudo_scotta_automatica`, `collaudo_semaforo`, `collaudo_regate` raffiche (18 su 18).
- I fallimenti noti con numeri cambiati (`collaudo_virate2`, `collaudo_competizione`, `collaudo_partenze`, `collaudo_avversari1b` in Firefox) si aggiornano con le righe del prossimo giro.

## Collaudi: le partenze su tanti semi e i collaudi scelti su GitHub (1 novembre 2026, nessuna versione nuova)

- **`tests/collaudo_non_partite.py`, nuovo.** Conta gli avversari non partiti entro 60 s in una delle quattro regate, con principianti ed esperti, 60/180/300 s di preparazione e semi 1-20 (si possono cambiare con `NONPARTITE_SEMI`). È la misura della 1.1.1 diventata collaudo: soglia 0, e il metro deve contare tutte le barche. Nel giro sono quattro voci lunghe, una per regata.
  - Provato qui: bastone, semi 1-20, 360 barche contate su 360, 0 non partite, OK.
  - Salti, seme 40: FALLITO con la barca giusta (Verde). È il caso accettato da Ale.
- **Su GitHub, «Run workflow» ha due caselle nuove:**
  - «Solo questi collaudi»: un pezzo del nome, per esempio `non_partite`, passato a `lancia_tutti.sh --solo`;
  - «Semi di collaudo_non_partite», per esempio `1-100`.
- **Perché non «10 volte lo stesso collaudo»:** i collaudi girano a semi e passi fissi, quindi ripetuti danno lo stesso numero carattere per carattere. Per vedere di più servono semi diversi, come fanno l'Esploratore e ora questo collaudo.
- **Decisione di Ale:** il caso del seme 40 si accetta.

## 1.1.1 — Gli avversari dell'1b partono (ramo `pulizia`)

Da `docs/PROPOSTA-PARTENZE-1B.md`, con il via di Ale (scelta A, 1 novembre 2026). Si cambia solo la guida degli avversari, in `js/regate.js`. La fisica non cambia: `impronta1b.js` identica al bit, `polare.js` e `raffiche_e_virate.js` identici.

**Il difetto.** Con la 1.1.0 alcuni avversari non partivano entro 60 s dallo sparo (criterio (4) di `collaudo_partenze.py`). Misurato qui, in Chromium, sulle quattro regate: principianti ed esperti, 60/180/300 s di preparazione, semi 1-20, cioè 1440 barche. Le barche non partite erano **25 su 1440**: 6 nel bastone, 6 nelle raffiche, 5 nei salti, 8 nei giri. Sulla 1.0.78 bastone e raffiche avevano 0, ma la regata dei giri, già dell'1b, ne aveva già **8 su 360**: il difetto c'era da prima e nessun collaudo lo guardava.

**Tre correzioni:**
- **A. Si cede solo a chi si avvicina.** Due barche parallele alla stessa velocità, a meno di due lunghezze, risultavano «sul punto di toccarsi» a ogni passo. Così si cedevano a vicenda: tutte e due al traverso lungo la linea, tagliata poi fuori dagli estremi. Ora, con gli scafi a più di una lunghezza, una barca che si avvicina a meno di `V_AVV` = 0,1 m/s non conta. Chi sta già cedendo continua finché le barche si avvicinano. **Ipotesi nostra:**
  - scelta sui semi 1-20: con 0,3 m/s le barche non partite erano 0, ma i contatti crescevano del 25%;
  - senza questa correzione, nei salti restano 5 barche su 360 non partite.
- **B1. Abbrivio prima di virare.** Per virare da quasi ferma, la barca poggiava finché superava 1,1 m/s, poi orzava, rallentava sotto 1,1 e poggiava di nuovo. Restava così per minuti a 2,1 nodi, in un caso fino a 250 m dal centro della linea. Ora continua a prendere abbrivio fino a `U_ABBRIVIO` = 1,6 m/s, circa 3,1 nodi (le virate dell'1b riescono da circa 2,9 nodi, 1.0.43), e intanto la vela si regola invece di sbattere. Ipotesi nostra.
- **B2. Chi taglierebbe fuori lascia la prua di partenza.** Dopo lo sparo, una barca vicina alla boa che, tenendo la prua di partenza, taglierebbe la linea fuori dall'estremo (scivola di lato di tan(bolina + 4°) metri per metro) passa alla guida generale. Prima, nei 18 casi rimasti dopo A e B1, la barca girava attorno alla boa per tutto il minuto.
- **Provate e tolte:**
  - un punto di rientro dietro la linea per chi era fuori dagli estremi: creava proprio il giro attorno alla boa;
  - cedere al lasco quando la guida chiede di andare sottovento, per chi torna dopo un richiamo: le barche non partite salivano a 18 su 1440 sui semi 1-20 e i contatti quasi raddoppiavano.

**Misurato** (Chromium, 4 regate, 2 livelli, 3 preparazioni):
- **P1/P2, semi 1-20 (scelta): 0 barche non partite su 1440.**
- **Semi 21-40 (conferma, mai guardati): 1 su 1440.** È la regata dei salti, esperti, 60 s, seme 40, Verde: parte in anticipo e, mentre deve tornare, cede a Rossa che va di bolina e si allontana fino a 65 m oltre la linea. Con la 1.1.0 lo stesso seme partiva. **La soglia dichiarata (0) non è raggiunta sui semi di conferma**, e lo riporto così.
- **P3, contatti in 80 regate intere** (bastone e raffiche, semi 1-40): 374 contro 332 della 1.1.0, cioè **+12,7%** (soglia 20%). Tutte le barche arrivano in 80 regate su 80.
- **P4:** `collaudo_partenze.py` completo non sta nei 10 minuti di un comando qui. Il bastone è dentro tutte le soglie: richiami 0% e 1,7%, ritardo mediano 1,1-2,2 s, velocità mediana 4,8 e 4,6 nodi. Le raffiche si leggono nel giro su GitHub.
- **P5:**
  - `collaudo_avversari1b`: lo scenario 5 passa da 7 a **9 su 10** (soglia 9: verde), gli altri 10 su 10;
  - verdi `collaudo_regole`, `collaudo_semaforo`, `collaudo_contatto_senza_colpa` (21 su 21) e `collaudo_regate` bastone e raffiche (18 arrivi su 18);
  - non lanciati qui: `collaudo_giri_avversari` (40 regate) e i tornei.
- Cambiano, come previsto, gli arrivi di tutte le regate e dei tornei: `arrivi_regate.py` non è più identico.

## Collaudi dopo il giro su GitHub della 1.1.0 (1 novembre 2026, ramo `pulizia`, nessuna versione nuova)

Il primo giro completo su GitHub sul ramo `pulizia` (Chromium e Firefox, 65 collaudi per browser) ha dato più cadute di quelle che avevo lanciato in locale. Una per una:
- **Collaudi che dipendevano dalla 1a**, corretti senza cambiare le soglie:
  - `collaudo_laboratorio` (4): misura la velocità a vento fermo, ma la navigazione libera ha ora sempre i salti di vento. Salti spenti nel collaudo.
  - `collaudo_timone2` (Firefox, barra a 0,853 invece di 0,8): togliendo il controllo della 1a avevo tolto anche il primo tasto premuto, quello che lasciava passare i fotogrammi veri prima dei controlli. Ora il ciclo del browser è fermo (`__sv.fast(0)`) prima dei controlli sulla barra.
  - `collaudo_fantasma`: il suo pilota lascava la barra ferma. La barca dell'1b orza quando sbanda (nella mia prova la prua passa da 0° a 338° in 180 s) e non arrivava più. Ora tiene la prua con la barra: prova 1 completata in 1 min 27 s, fantasma salvato.
  - `collaudo_registro` (contatto, solo Chromium su GitHub): l'inseguimento in tempo vero passa da 60 a 120 s, perché gli avversari dell'1b cedono e il contatto ora è fra gli scafi.
  - `collaudo_scotta_automatica` A1: le 2 regate erano identiche alla 1.0.72; le 4 corse a scotta fissa differivano di poco. Causa misurata: la navigazione libera accende sempre i salti di vento, i numeri casuali si consumano in un altro ordine e le raffiche nascono altrove. Senza raffiche le 5 parti sono identiche al bit, quindi A1 ora confronta senza raffiche.
  - `collaudo_riquadro_bandiere` Q6a e Q6b: confrontano con la 1.0.69 solo le regate che erano già dell'1b, come `collaudo_boma_poppa`.
  - Rilanciati qui: verdi `collaudo_laboratorio` e `collaudo_timone2` (Chromium e Firefox), `collaudo_registro` (15 su 15), `collaudo_scotta_automatica`, `collaudo_fantasma`; `collaudo_riquadro_bandiere` verde fino a Q6b compreso, fermato dal mio limite di 10 minuti durante Q7, che è una misura di tempo.
- **Fallimenti noti aggiornati** (`tests/fallimenti_noti.txt`), con le righe prese dal giro:
  - `collaudo_competizione` (misura): C1 era già fuori fascia ed è peggiorato con la barca dell'1b. Il giocatore guidato dal pilota arriva quarto nel 40-51% delle regate in Chromium e nel 45-54% in Firefox (prima 34-48% e 35-48%). Da ritarare al passo 4, con medaglie e soglia del torneo.
  - `collaudo_carriera_intera` I4: il passo 3.10 si salta. Va col gruppo A delle lezioni.
- **Restano FALLITO apposta:**
  - `collaudo_lezioni` («L5 prepararsi», passo 3).
  - **`collaudo_partenze`, che è un difetto vero della 1.1.0:** con gli avversari dell'1b, in bastone e raffiche, alcune barche non partono entro 60 s dallo sparo: 12 barche su 720 in Chromium e 6 su 720 in Firefox, quasi tutte principianti con 300 s di preparazione. Con gli avversari dell'1a erano 0. Gli avversari dell'1b non sono mai stati misurati da questo collaudo, perché nella regata dei salti non c'è. La correzione tocca la guida degli avversari dell'1b: decide Ale.
- Atteso e già detto: `collaudo_fasce` e `collaudo_pilota_lezioni` DA CONTROLLARE; `collaudo_torneo` C11 è una misura di tempo.

## 1.1.0 — Pulizia del codice: resta solo la barca dell'1b (ramo `pulizia`)

Primo passo della riorganizzazione in «La scuola» e «Deriva» (`docs/PROPOSTA-RIORGANIZZAZIONE.md` §5, passo 2; proposta e misura 0 in `docs/PROPOSTA-PULIZIA-CODICE.md`). **Sta nel ramo `pulizia`, non in `main`:** lezioni e prove sono state provate con la barca dell'1a, e con l'1b alcune cose non vanno (misura 0). Il ramo entra in `main` insieme alle lezioni riscritte (passo 3), così il gioco online non cambia prima.

**Cosa cambia per chi gioca:**
- Lezioni, prove, navigazione libera e tutte le regate usano la barca dell'1b: la barra arriva a 35° con la sola freccia e a 45° con Maiusc, la pala può stallare, Z spinge il boma, la raddrizzata dura 10 s.
- La scelta «Barca» nelle impostazioni non c'è più. In navigazione libera il vento ha sempre i salti dell'1b.
- «Regata a bastone» e «Regata nelle raffiche» ora sono della barca dell'1b: regole 10-13, contatto fra gli scafi, avversari dell'1b, semaforo. Carriera e meriti contano ancora queste due, come prima: menu e carriera si rifanno al passo 5.
- Testi: tolta «Barca dell'1b» dove non c'è più una scelta. Dalle introduzioni delle regate è tolta la frase «Da questo livello i contatti sono quelli veri… Prima avevi imparato…», che parlava della 1a; resta la spiegazione di chi cede, ora in tutte le regate. Il semaforo nelle impostazioni dice «regate» e non più «solo regate 1b». I tasti Maiusc e Z sono spiegati al passaggio del mouse sulla riga dei tasti, perché l'unica spiegazione stava nella scelta «Barca», che non c'è più. La lezione vera arriva con il passo 3.
- **Difetto corretto per strada:** dalla 1.0.61 l'introduzione della «Regata con i giri di penalità» diceva che il vento gira e che la boa è a 300 m. Non era vero: il testo seguiva la barca dell'1b e non la regata. Ora lo dice solo la regata nei salti di vento.
- Il registratore non scrive più «(barca 1a|1b)» nell'intestazione della regata.

**Codice:**
- `js/motore.js`: quello che valeva con `S.lv === 2` vale sempre; tolti lo scarroccio dell'1a (`BOAT.foilK`) e `raddT`. Sotto 0,5 m/s e all'indietro resta il timone di prima, come già nell'1b.
- `js/regate.js`: tolti la regola 10 propria degli avversari dell'1a, lo scarto da qualsiasi barca davanti, il contatto fra cerchi e le regole «10 e 11 semplificate». `RACES1` diventa `RACES_CARRIERA` (le regate col campo `scuola: false` ne restano fuori).
- `js/gioco.js`, `js/disegno.js`, `js/registratore.js`, `index.html`: tolti selettore e rami dell'1a.
- Le righe di codice in `index.html` e `js/` che contengono `S.lv`, `lv2`, `RACES1`, `boatLv` o `.lv` erano **46**, ora sono **0**. Le righe di solo commento non contano. Il comando, uguale prima (su `main`) e dopo: `cat index.html js/*.js | grep -E "S\.lv|lv2|RACES1|boatLv|\.lv\b" | grep -vE "^\s*//" | wc -l`.
- I nomi `RUD2`, `RADD2`, `BOMA2`, `DERIVA2`, `SALTI2` restano: il cambio dei nomi previsto dalla proposta (§2.A) **non è fatto**. Tocca 20 script di collaudo e non cambia niente nel gioco: lo propongo per la pulizia finale, dopo le lezioni.

**Collaudi della fisica e prototipo:**
- Nuova copia congelata del motore della 1a, `tests/fisica/motore1a_sorgente.js`, letta da `tests/fisica/motore1a.js`; con `MOTORE=1a` la legge anche `tests/fisica/motore.js`. Il prototipo del fiocco (`sperimentale/misure_fiocco.js`) si confronta con questa: uscita identica carattere per carattere prima e dopo (136 righe). **Trovato:** già prima della pulizia, il prototipo «senza fiocco» non era più identico al gioco: 30 casi, scarto massimo 2,73 nodi a 15 nodi e 90°. La 1a del gioco era cambiata dopo la tappa C e il prototipo è rimasto indietro. La regola di `CLAUDE.md` sulla non-regressione va riscritta.
- **P1:** `impronta1b.js` è identica al bit (25 corse, 51.802 passi).
- **P2:** `MOTORE=1a node polare.js` e `MOTORE=1a node raffiche_e_virate.js` danno i riferimenti di prima, carattere per carattere.
- **P3:** riferimenti nuovi di `polare.txt` e `raffiche_e_virate.txt`, rigenerati: ora misurano la barca dell'1b, perché il gioco ha solo quella. I valori nuovi sono identici carattere per carattere a quelli che la barca dell'1b dava già prima (stessi script con `lv: 2` sulla copia congelata). Polare con 10 nodi: 4,6 nodi a 45° (prima 4,7), 6,0 a 90°, 4,1 a 180°. Virata da 3,9 nodi in 3,9 s (prima 3,0), da 1,9 nodi in 7,5 s (prima 6,6). Raffica a 20 nodi senza reagire: 65°, scuffia (prima 67°).
- `scarroccio1b.js` e `timone2.js` mettono ancora a confronto 1a e 1b, prendendo la 1a dalla copia congelata: uscite identiche a prima. `timone2.js` esce con «almeno un criterio FUORI soglia» come prima.
- `bolina.js`, `retromarcia.js`, `angolo_morto.js`, `raffiche_portanti.js` e `virate2.js` misuravano la barca senza `lv` e ora misurano l'1b. Non sono nel giro e non li ho rilanciati.

**Regate (P4, P5):**
- **P4:** `tests/arrivi_regate.py`, con in più la regata dei giri (6 semi): le 28 righe di salti, giri e 2 tornei sono identiche al bit a `main`. Restano esclusi i testi di introduzione, cambiati come detto sopra.
- **P5:** bastone e raffiche con gli avversari dell'1b, semi 1-20 principianti e 21-40 esperti. Arrivano tutte le barche in **80 regate su 80** (soglia 19 su 20 per regata e livello). Tempo medio di tutte le barche: bastone 225/221 s, raffiche 204/208 s (prima, con la 1a, sui 7 semi di `arrivi_regate.py`: 221/214 e 203/201). Barche con almeno una penalità: 49, 52, 49, 57 su 80 per gruppo, 61-71%. Con la 1a, sui 7 semi, erano 7/16, 8/12, 12/16, 7/12, cioè 44-75%.

**Riquadro delle istruzioni a 1360×650** (misurato in tutte e quattro le regate, 3 livelli di avversari, Chromium e Firefox):
- Bastone e raffiche: **0 px**, come prima. In una prima stesura avevo aggiunto anche lì la frase su chi cede: sforava di 35-88 px e `collaudo_pannello.py` l'ha preso. La frase ora c'è solo dove c'era già: salti, giri e torneo (campo `precedenze`).
- **Difetto vecchio, trovato ora:** il riquadro di salti e giri sfora già su `main`. Su `main` 158-210 px per i salti e 354-406 px per i giri; ora 84-137 e 207-284, perché i testi sono più corti. Nessun collaudo lo vedeva: `collaudo_pannello.py` misura solo la prima regata. Da sistemare con i testi della scuola (passo 3), insieme a un collaudo che misuri tutte le regate.

**Lezioni e prove sulla barca nuova (P7, solo numeri):** identici alla misura 0, carattere per carattere.
- `collaudo_pilota_lezioni.py`, semi 1-10: 27 passi su 32 completati 10 volte su 10. 3.10 «Filetto sottovento» mai completato (0 su 10). Quattro passi si completano da soli, senza toccare niente: 2.4, 3.2, 5.2, 6.2.
- `collaudo_fasce.py`: oro mancato nella prova 4 (285,8 s contro 280) e nella 5 (302,4 s contro 300, una corsa su 24 bloccata). Le prove 1-3 vanno come prima.
- `collaudo_lezioni.py`: ESITO FALLITO solo per «L5 prepararsi (bolina lanciata)». Va col passo 3 e non l'ho aggiunto ai fallimenti noti. Ho portato l'attesa di «L6 raddrizzare» da 8 a 12 s, perché la raddrizzata dell'1b dura 10 s.

**Pagina come la carica un giocatore (P8):** in Chromium e Firefox, senza `#collaudo`, si aprono lezione 1, prova 1, navigazione libera e le quattro regate: 7 su 7, 0 errori della pagina, pagina che non scorre (0 px).

**Collaudi lanciati:**
- **Verdi:** `collaudo_versione`, `collaudo_timone2`, `collaudo_boma2`, `collaudo_raddrizzata`, `collaudo_salti2`, `collaudo_pannello` (90 misure del pannello, 6 del riquadro), `collaudo_quiz`, `collaudo_regole` (35 controlli), `collaudo_semaforo`, `collaudo_carriera`, `collaudo_registratore`, `collaudo_registro` (15 su 15), `collaudo_libretto`, `collaudo_contatto_vero`, `collaudo_contatto_senza_colpa`, `collaudo_suggerimento`, `collaudo_regate` bastone e raffiche (6 corse ciascuna, 18 arrivi su 18, nessuna BLOCCATA), `collaudo_partenze`.
- **Fallisce, come su `main`:** `collaudo_triangolo` T2b, 129 su 168 confronti dei distacchi; numeri identici a quelli di `main` rilanciato qui.

**Collaudi cambiati,** perché misuravano la barca dell'1a o sceglievano la barca dal selettore «Barca». Ogni cambio è scritto nel file.
- `collaudo_boma2`: tolto «nella 1a Z non fa niente».
- `collaudo_timone2`: tolti i controlli sulla scelta «Barca» e sulla barra della 1a; ora controlla che la scelta «Barca» non ci sia più.
- `collaudo_raddrizzata`: solo la 1b; la regata 0 si raddrizza ora in 15 s a 90°.
- `collaudo_salti2`: tolto «nella libera dell'1a il vento non gira».
- `collaudo_scotta_automatica`: solo la 1b; A1 confronta con la 1.0.72 solo le regate che erano già dell'1b.
- `collaudo_boma_poppa`: tolta la 1a (B2b); B4a confronta solo le 10 regate già dell'1b.
- `collaudo_regole`: la regata 0 ha gli attesi di F15. In fila con le stesse mure cede chi è dietro (12), non il più sopravento (11).
- `collaudo_semaforo`: nella regata 0 il semaforo ora si deve vedere (1.824 passi).
- `collaudo_contatto_vero`: la regata 0 ha gli attesi del contatto fra scafi.
- `collaudo_contatto_senza_colpa`: barche affiancate a 1,2 m invece di 3 e «non in virata» all'inizio. Il caso costruito spostava le prue a mano e la regola 13 lo prendeva per una virata.
- `collaudo_suggerimento`: salti di vento spenti nella navigazione libera, perché misura i tempi del suggerimento con il vento fermo.
- `collaudo_lezioni`: attesa della raddrizzata (vedi sopra).
- `collaudo_impronta`: solo la riga del selettore. Il riferimento resta vecchio, come prima.
- `tests/lancia_tutti.sh`: i valori da confrontare a mano per `polare.js` e `raffiche_e_virate.js`.
- **Non lanciati qui:** `collaudo_boma_poppa`, `collaudo_scotta_automatica`, `collaudo_impronta`, i collaudi della carriera intera e dell'esame, `collaudo_avversari1b`, `collaudo_giri*`, `collaudo_torneo`, `collaudo_moviola` e gli altri del giro. Li lancia `tests/lancia_tutti.sh`.

## 1.0.78 — Descrizione della regata dei giri: «per un contatto con colpa»

La descrizione nel menu diceva «due giri se lasci male la strada», una frase mia della 1.0.69 che non vuol dire niente: segnalata da Ale il 1 novembre 2026. Ora dice: «Livello 2: due giri per un contatto con colpa, uno se tocchi una boa; bandiere sulla giuria.» È anche più precisa, perché nel gioco i due giri arrivano solo con un contatto in cui avevi la colpa.

Misurato a 1360×650, in Chromium e Firefox: la descrizione resta su una riga (38,9 px) e il menu non scorre (0 px). Scartata «se urti chi ha la precedenza»: va a capo e il menu scorre di 13 px in Chromium e 11 px in Firefox. Verdi `collaudo_quiz.py`, `collaudo_esame.py` e `collaudo_salti2.py`, che nella 1.0.69 cadevano proprio per il menu che scorreva.

## 1.0.77 — In regata la riga degli errori mostra solo il numero

L'Esploratore su GitHub (osservazione 78) ha trovato il pannello che sforava di 9 px in Firefox: regata dei giri, seme 38, giocatore scuffiato con la regola 21.2 e un elenco lungo di errori. C'era già nella 1.0.74.

**Scelta di Ale (A):** durante la regata la riga degli errori del pannello dice solo il numero, per esempio «Errori: 5 (l'elenco a fine regata)» oppure «Errori: nessuno». L'elenco completo resta:
- al passaggio del mouse sulla riga;
- nella schermata di fine regata.

Prove e lezioni non cambiano. Provato e non adottato: accorciare il suggerimento della scuffia, che non serve perché quel riquadro è alto almeno 2 righe.

Effetto collaterale, già nella scelta A: in regata la nota «N contatti senza colpa, non contano» non si vede più nella riga, ma resta nell'elenco al passaggio del mouse e a fine regata.

**Misurato:**
- **Caso peggiore nuovo in `collaudo_pannello.py`:** regata dei giri dopo il via, barca scuffiata per una strambata, regola 21.2 con le istruzioni dei giri, tutti i tipi di errore insieme. È scritto prima della correzione.
  - Sulla 1.0.76: sfora di **29 px** in Chromium e in Firefox, e il collaudo cade.
  - Sulla 1.0.77: **0 px** a 1360×650 e 1360×768, in tutti e due i browser.
- **Le 100 regate dei giri con i principianti in Firefox,** rigiocate come l'Esploratore: 0 sforano (prima 1, il seme 38).
- **`collaudo_contatto_senza_colpa.py`:** aggiornato, perché leggeva l'elenco nella riga. Ora lo legge al passaggio del mouse (`title`) e controlla anche la riga corta. Verde.
- **`collaudo_registro.py`:** verde.
- **Fisica:** identica.
- `collaudo_impronta.py`, che non è nel giro, segnerà diversa la riga `stErr` delle regate: è voluto.

## Collaudi, 1 novembre 2026 — l'esploratore prova tutte le regate (nessuna versione nuova)

- `tests/esplora.py` girava solo le prime 3 regate: `range(3)` era fisso, quindi la regata dei giri (dalla 1.0.61) non è mai stata esplorata. Ora legge quante sono (`RACES.length`, oggi 4).
- Provato sulla 1.0.76, semi 1 e 2: 14 corse, 0 numeri non finiti su 445.018 controllati, 0 barche non arrivate, 0 eccezioni, 0 errori della pagina, pannello 0 px. La scimmia, 30 s e 41 azioni: 0 errori, la pagina non scorre.
- L'ultimo giro lungo dell'esploratore risaliva al 23 ottobre (1.0.45 circa).
- **Esploratore su GitHub:** `.github/workflows/esplora.yml`, solo a mano: scheda Actions → «Esploratore» → «Run workflow».
  - Si scelgono primo e ultimo seme, semi per pezzo, secondi e numero di giri della scimmia, e il browser.
  - I pezzi girano insieme. Alla fine un passo «Riepilogo» unisce tutti i file in un solo riepilogo, che compare nella pagina del giro ed è nell'allegato `esplora-riepilogo`.
- `esplora.py` scrive anche il browser in ogni riga, e il riepilogo divide per versione e browser.
- Opzione nuova `--seme-scimmia N`, per rifare un giro di scimmia con gli stessi tasti.
- Variabile `ESPLORA_NOME` nel nome del file, perché i file dei pezzi non si sovrascrivano.
- **Esploratore anche ogni settimana** (Ale), nella notte fra domenica e lunedì (lunedì 03:00 UTC, dopo i collaudi). Nelle settimane pari i semi 1-100, nelle dispari un blocco nuovo di 100 semi, a giro fino a 1000.

## 1.0.76 — La moviola rivede tutta la regata, partenza compresa

Da `docs/PROPOSTA-MOVIOLA-INTERA.md`, con il via di Ale del 1 novembre 2026 e i due consigli: partenza inclusa, ← → di 5 s. Osservazione 73.

**Cosa cambia per chi gioca**
- «Rivedi» mostra **tutta la regata**: dalle bandiere a −5 minuti all'arrivo o al ritiro. Fino alla 1.0.75 mostrava pezzi di 18 s, solo dopo lo sparo, al massimo 12.
- Il tasto O, ogni contatto (anche fra avversari e anche prima del via) e ogni boa toccata mettono un **segno**. I segni sono tacche gialle sul cursore. Il limite dei 6 contatti automatici non c'è più.
- In alto la barra dice «Tutta la regata», oppure «Segno 2 di 5 — …» nei 10 s prima e negli 8 s dopo un segno.
- La riproduzione parte 10 s prima del primo segno, o 10 s prima dello sparo se non ci sono segni. Alla fine si ferma: non ricomincia più da capo.
- **Tasti della moviola:**
  - ← → spostano indietro e avanti di 5 s (fino alla 1.0.75 cambiavano pezzo);
  - ↑ ↓ portano al segno prima o dopo, 10 s prima del segno;
  - 1 2 3 4 5 danno le velocità 1×, ½×, ¼×, 4×, 8×;
  - R torna all'inizio, spazio mette in pausa, Esc chiude;
  - i pulsanti si chiamano «◀ Segno prima» e «Segno dopo ▶».
- Aprendo la moviola il fuoco va su «Pausa». Prima andava su «Chiudi», e lo spazio chiudeva la moviola invece di metterla in pausa.
- Il tetto è di 60 minuti di regata (36.000 copie): oltre si tengono gli ultimi 60 e la barra lo dice. Costanti ipotesi nostre.

La moviola resta in memoria: lasciata la regata, si perde. La registrazione per il coach non cambia. Il gioco non cambia: la moviola legge e basta.

**Misurato** con `tests/collaudo_moviola.py`, riscritto con i criteri V1-V10 della proposta. 12 regate del torneo col pilota per browser, confrontate con una copia della 1.0.75.

| | Chromium | Firefox |
|---|---|---|
| V1 fedeltà (soglia 0,5 m e 5°) | 0,109 m e 0,25° su 4658 confronti, 2148 prima del via | 0,098 m e 0,31° su 4905, 2148 prima del via |
| V2 gioco identico al bit alla 1.0.75 | 12 su 12 | 12 su 12 |
| V3 copertura: scarto all'inizio / alla fine | 0,02 s / 0,00 s | 0,02 s / 0,00 s |
| V4 segni, tutti al loro posto e con la tacca | 66 (42 automatici, 16 prima del via) | 72 (48 automatici, 20 prima del via) |
| V7 costo (soglia +3%) | +0,3% | −0,1% |

- **V5**, tutti i tasti premuti con la tastiera vera: OK in tutti e due i browser.
- **V6**, uscita pulita: OK.
- **V8**, tetto: riempita con 37.000 copie, si ferma a 36.000 e lo dice.
- **V9**, barra a 1360×650: eccesso 0 px.
- **V10**, pagina senza `#collaudo`: la regata si apre dal menu e la moviola copia durante il conto alla rovescia (29 e 28 copie in 3 s). È stata aperta chiamando `rivApri`, non dal pulsante: per arrivare al pulsante bisognerebbe finire la regata in tempo vero.
- Al primo giro su 4 regate V5 e V10 erano caduti, per due errori corretti prima del giro vero. V5: con il fuoco su «Chiudi», lo spazio chiudeva. V10: il collaudo non chiudeva il riquadro delle istruzioni della regata. Le soglie non sono cambiate.

## 1.0.75 — «Cambia vento» di nuovo nelle regate (non nel torneo)

Decisione di Ale del 1 novembre 2026 (osservazione 74): «rimetti "cambia vento" dove era, ma non deve essere un'opzione per i tornei». Cambia la decisione della 1.0.70 (`DECISIONI.md`).

- Il pulsante torna dov'era fino alla 1.0.69: nel pannello della regata (`rWind`) e nella schermata finale (`finWind`).
- Un clic sceglie un'altra direzione del vento, a caso fra le 8 (`otherWind`, come nelle prove), e ricomincia la regata.
- Nel torneo non c'è, né nel pannello né alla fine, come prima della 1.0.70: è nascosto con `rc.tor`.

**Misurato** con il collaudo nuovo `tests/collaudo_cambia_vento.py`, ora nel giro, in Chromium e in Firefox: OK.
- Nelle 4 regate il pulsante c'è.
- Nella regata 1 del torneo non c'è, e alla fine del torneo mancano sia «Cambia vento» sia «Ricomincia».
- Un clic nella regata dei giri porta il vento da 0° a 135° e apre una regata nuova.
- Nessun errore della pagina.

Verdi anche `collaudo_pannello.py` a 1360×650 e 1360×768: eccesso 0 px con il pulsante in più. La fisica non cambia.

## 1.0.74 — Il conto dei giri di penalità non torna indietro

Difetto trovato da Ale nella prova a mano del 1 novembre (osservazione 72, `sessione-20261101-0018.txt`). Il gioco sommava tutte le penalità della regata. Un giro nel verso opposto al precedente rimetteva i giri fatti a 1, e così cancellava anche quelli delle penalità già scontate.
- Nella registrazione: debito di 6 giri (tre contatti), «Giro fatto: ne manca ancora 5», all'arrivo +75 s. La sola penalità aperta valeva 2 giri.
- **Causa:** il «verso opposto» (1.0.61) era pensato per una penalità sola. Il collaudo provava una penalità alla volta, quindi non l'ha visto.

**Correzione** (`js/regate.js`, `giriPenalita`):
- `R.base` tiene i giri delle penalità già scontate.
- Il verso opposto fa ricominciare solo la penalità in corso: `R.done = R.base + 1`.
- Quando una penalità è scontata, il verso torna libero: ogni penalità ha il suo verso, regola 44.2.
- Il riquadro dice «fatti» contando solo i giri della penalità aperta. Prima diceva «2 da fare · fatti 2», con i giri della penalità precedente.
- L'elenco di fine regata dice «penalità scontata: 2 giri» per ogni penalità, invece del totale.

**Registratore** (`js/registratore.js`):
- La riga `giro_penalita` compare anche per il giro nel verso opposto, con la parola `verso_opposto`. Prima quel giro mancava, perché il conto scendeva.
- La riga non compare più all'arrivo con i giri non fatti. Prima scriveva un finto `6/6`; quei giri sono nella riga Q.

Gli avversari non cambiano: hanno un conto loro, `gDebt`. Il motore e la fisica non cambiano.

**Misurato** (Chromium):
- `collaudo_giri.py 12`: tutto verde, con due controlli nuovi scritti prima di misurare.
  - **P1:** prima penalità scontata in un verso, seconda penalità, primo giro nel verso opposto. Il conto va a 3 (manca 1 giro), poi a 4. 12 su 12, 0 scuffie.
  - **P2:** l'elenco dice due volte «penalità scontata: 2 giri». 12 su 12.
  - **Controprova:** lo stesso collaudo sul codice della 1.0.73 cade su P1 e P2. Il conto torna a 1 in 12 prove su 12, come nella regata di Ale.
- Verdi anche `collaudo_riquadro_bandiere.py` e `collaudo_regola21.py 12`.
- `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` sono identici.
- Firefox: lo fa il giro notturno su GitHub.

## Collaudi, 1 novembre 2026 — fallimenti noti (nessuna versione nuova, il gioco non cambia)

- `tests/fallimenti_noti.txt` e `tests/noti.py`: 10 fallimenti noti e 3 misure di tempo.
  - Un collaudo fallito vale come **NOTO** solo se la sua uscita contiene tutte le righe registrate, identiche, e nessun'altra riga di fallimento. Altrimenti resta FALLITO, con il motivo: «manca …» oppure «fallimento in più …».
  - Le misure di tempo (torneo C11, registrazione E2, riquadro Q7) vanno in DA CONTROLLARE solo su GitHub.
  - `lancia_tutti.sh` ha la sezione NOTI. Elenca anche i noti che ora passano, la cui voce va tolta.
- Provato sulle uscite vere del giro di Ale e di GitHub del 1 novembre: 26 su 26 classificate come atteso, cioè 18 noti, 6 misure di tempo e 2 errori della moviola rimasti FALLITO.
- Provato anche su 5 uscite cambiate apposta, tutte FALLITO: un numero cambiato, un controllo in più, l'uscita dell'altro browser, una misura di tempo con un controllo vero sbagliato, un collaudo fuori elenco.
- Rifatta da capo una copia del giro con collaudi finti, che ristampano le uscite vere: esiti e codici di uscita giusti, sul PC e con `GITHUB_ACTIONS=true`.
- `collaudo_moviola.py` apriva il gioco da un percorso fisso, `/home/callle/scuola-di-vela`, che su GitHub non esiste. Da una copia del gioco collaudava quindi l'originale. Corretto.

## Collaudi, 1 novembre 2026 — i collaudi su GitHub Actions (nessuna versione nuova, il gioco non cambia)

- Nuovo `.github/workflows/collaudi.yml` (`docs/PROPOSTA-COLLAUDI-SU-GITHUB.md`, fermata 2). Di notte (circa alle 3, solo se nelle ultime 24 ore c'è stato un commit su `main`) o a mano dalla scheda Actions, lancia `tests/lancia_tutti.sh` con Chromium e Firefox in 8 pezzi che girano insieme: Node 20.19.2, Python 3.13 e Playwright 1.60.0, come sul PC.
- `tests/lancia_tutti.sh --parte K/N`: lancia solo un pezzo; i collaudi lunghi si distribuiscono a turno fra i pezzi. Provato con `--dry-run`: 4 pezzi da 16, che insieme danno esattamente i 64 collaudi. Senza l'opzione il giro è come prima.
- Criteri G1-G6 ancora da misurare: serve il primo giro su GitHub, che parte la notte dopo il push di Ale, oppure subito se lo lancia a mano.

## Collaudi, 1 novembre 2026 — il «test dei test» (nessuna versione nuova, il gioco non cambia)

Da `docs/PROPOSTA-TEST-DEI-TEST.md` (fermata 1 del 31 ottobre, via di Ale per tutto: A, B e C, in sessione notturna autonoma). Toccati solo `tests/` e i documenti; `index.html` e `js/` identici.

- **A. Conteggio dei casi.** Nuovo `tests/metro.py`: `metro.tutti()` e `metro.nessuno()` sono falsi con zero casi. I 97 `all(...)` di 25 collaudi chiari sono diventati `metro.tutti(...)`; a fine collaudo una riga `METRO:`. Giro di verifica sui 31 lanci toccati: nessun controllo sotto il minimo, falliti solo i tre noti (virate2, competizione misura, torneo misura), con i numeri di prima. Lanciati con zero prove, 5 collaudi su 5 cadono (`collaudo_regola21.py` non usa il numero di prove: misura su griglie fisse, l'etichetta «12 prove» in `lancia_tutti.sh` è solo un nome).
- **B. Da ambigui a chiari: 59 su 64** (prima 46). `polare.js` e `raffiche_e_virate.js` confrontati carattere per carattere con `tests/fisica/polare.txt` e `raffiche_e_virate.txt` (nuovo `tests/fisica/confronta.js`; uscite identiche alla 1.0.70); pannello (un pixel di eccesso basta), strambata, registro, fantasma, schermate, giro di boa, regate e lezioni con la riga `ESITO:` e il codice d'uscita. Restano ambigui 5 (pilota delle lezioni ×2, competizione da tastiera, partenze, fasce).
- **Difetto nascosto trovato in `collaudo_lezioni.py`:** il passo 1.8 «Orzare e l'angolo morto» risultava NON COMPLETATO **dal 16 ottobre** (1.0.6; dalla 1.0.12 il testo dice di rilasciare quando la prua entra nel rosso, il collaudo teneva premuto 25 s). Nessuno l'aveva visto perché il collaudo era «da controllare». Era il collaudo, non il gioco (il pilota delle lezioni il passo lo completava): allineato al testo.
- **C. Controprove**, nuovo `tests/controprove.py` (difetto messo apposta in una copia del gioco, il collaudo deve cadere; commento innocuo, deve restare verde). Scritte e messe in git prima di lanciarle. **Mutanti presi 15 su 16; neutre verdi 15 su 16.** Il mutante non preso: la soglia di scuffia 60° → 90° non fa cadere `collaudo_strambata.py` (a 15 nodi la strambata violenta porta lo sbandamento oltre 90° comunque); la stessa soglia la protegge `collaudo_registro.py` (14 su 15, cade). La neutra caduta: `collaudo_giri_avversari.py` con 12 regate invece di 40 (riduzione mia, per il tempo) ha 7 casi in G4 che ne vuole 15, cade per il minimo di casi; con 40 regate resta verde (riga aggiunta dopo, dichiarata).

## 1.0.73 — Scotta automatica (aiuto attivabile)

Da `docs/PROPOSTA-SCOTTA-AUTOMATICA.md`, con le tre risposte di Ale del 31 ottobre 2026 «come consigli tu». Casella **«Scotta automatica»** nelle impostazioni (⚙), **spenta all'inizio**, che vale solo nelle prove e nella navigazione libera (non nelle regate e nei tornei; le lezioni restano com'erano: i loro passi con `autoTrim` usano la regola semplice). Con la casella accesa la scotta segue la regola già nel gioco (`|vento apparente| − 17°`) più una **lasca per la sbandata** (costanti ipotesi nostre, `AUTO_HEEL0 = 12°`, `AUTO_K = 1,5` gradi di boma per grado di sbandata oltre; scelte prima di misurare e non toccate dopo). I tasti della scotta (frecce su/giù) e il cursore la spengono, con un avviso. **Una prova fatta con la scotta automatica si completa ma non vale record, medaglia né stella** (il testo lo dice). Motore e fisica non cambiano.

Collaterali: la riga «La barra torna al centro da sola» perde la spiegazione lunga (resta nel suggerimento al passaggio del mouse) e il vuoto fra le righe del dialogo passa da 4 a 2 px, perché la riga nuova non ci stava a 1360×650 (eccesso 25 px, poi 13, ora 0). Il registratore scrive anche `scotta_automatica=sì/no` fra le impostazioni.

Misurato con `tests/collaudo_scotta_automatica.py` (semi 1-20 per la scelta, 101-120 per la conferma, uguali; Chromium e Firefox, due giri ciascuno uguali):
- **A1** casella spenta: 4 corse a scotta fissa e 5 regate identiche alla 1.0.72, al bit.
- **A2** velocità contro la migliore scotta fissa (griglia di 21 valori), 7 angoli × 3 venti: media 97,3% (barca 1b) e 97,2% (1a) su 21 corse ciascuna; peggiore 91,2-91,3% (15 nodi, 110°). Soglia 90%.
- **A3** 15 nodi, raffiche forti, 60 corse per barca: con la lasca 0 scuffie contro 8 (1b) e 6 (1a) della regola semplice; sbandata massima media 18,6-18,7° contro 43,3-45,5°.
- **A4** i tasti la spengono in 20 su 20; **A5** la scotta cambia nel 99% dei passi (a mano, 0); **A6** prova 1 con la scotta automatica: arrivata, nessun record né medaglia né stella salvati; **A7** pagina senza `#collaudo`: la casella c'è, si accende, nessun errore.
- Dialogo impostazioni e pannello a 1360×650: eccesso 0 px (`collaudo_registratore.py`, `collaudo_pannello.py`).
- `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.

**Il metro cambiato durante il lavoro (dichiarato):** (1) il primo confronto di A3 era con una scotta ferma «iniziale», che era più lasca della regola e dava meno sbandata: non confrontava la correzione; ora il confronto è con la stessa regola senza lasca (K = 0). (2) La prima prova della prova 1 non arrivava (il pilota puntava male); ora punta alla boa dell'arrivo. (3) A1 non era ripetibile (anche lo stesso codice due volte dava differenze all'ultima cifra, in Chromium e Firefox): `openItem` rimette il tempo del gioco a velocità normale, e fra una chiamata e l'altra il ciclo del gioco consumava numeri casuali; ora il tempo si ferma dopo l'apertura (`fast(0)`).

## 1.0.72 — La X non risale dopo il rientro

Trovato dal giro di Firefox del 31 ottobre 2026 (`collaudo_segnali.py`, G2, 29 campioni sbagliati nella regata seme 44). Una barca richiamata rientra dietro la linea e la X scende; se poi la ripassa fuori dai limiti della linea (`ocs` torna vero) la X risaliva, anche a 22 s dallo sparo. La regola 29.1 vale solo per le barche oltre la linea allo sparo. **Causa:** la X era calcolata sull'elenco delle barche richiamate ma quel elenco non perdeva le barche rientrate. **Correzione:** una barca che rientra esce dall'elenco (`js/regate.js`, una riga). Nessun cambio di fisica. In Chromium il caso non compariva perché le traiettorie con altri semi sono diverse.

Misurato: `collaudo_segnali.py` tutto verde in Firefox e in Chromium (G2: 12 regate con richiamo e 6 senza, 0 errori; prima 29 errori in Firefox).

## 1.0.71 — Il boma non saltella più con il vento in poppa

Osservazione 63 di Ale (`docs/PROPOSTA-BOMA-IN-POPPA.md`, via di Ale del 31 ottobre 2026). Tocca una riga del motore (`js/motore.js`, lato del boma); le forze non cambiano.

- **Causa e rimedio.** Il lato del boma era il segno dell'angolo del vento apparente: con il vento esattamente da poppa il segno oscillava (onde, assetto) e il boma saltellava. Ora il lato cambia solo se il vento apparente è passato oltre **5°** da dietro (`BOOM_ISTERESI`, ipotesi nostra, nessuna fonte). Il lato del boma non entra nelle forze: serve al disegno, al lato della scuffia e al lato del peso dell'equipaggio.
- **Prima, sul motore di prima** (B1, 20 semi 1-20, prua a 180° dal vento vero per 60 s, barca 1b): cambi di lato del boma senza salti di vento **18 a 6 nodi, 95 a 10, 330 a 15**; con i salti **1 a 6 nodi, 32,5 a 10 (massimo 51)**; a 15 nodi con i salti 10 prove su 20 scuffiano e tra le altre la mediana è 316,5. **Sulla 1a il difetto non si riproduce: 0 cambi in tutti i venti** (l'ho visto solo sulla 1b).
- **Dopo** (B2): **0 cambi di lato in 60 s in tutte le prove valide**: 110 prove sui semi di scelta 1-20 e 111 sui semi di conferma 101-120, mai guardati, a 6, 10 e 15 nodi, con e senza salti (soglia: al più 1 cambio in almeno il 95% delle prove). B5: a 150°, 120° e 210° dal vento nessun cambio in 90 prove.
- **La strambata vera non si perde** (B3): la prua porta il vento da +150° a −150° e al contrario a 5°/s, con la scotta lasca e cazzata: **30 prove valide su 36**, in tutte il boma cambia lato **una sola volta**, **0,5-0,7 s dopo** che il vento apparente è passato da dietro (soglia 1,5 s). Le 6 prove escluse sono scuffie a 15 nodi durante la strambata forzata.
- **Non regressione** (B4): `polare.js` e `raffiche_e_virate.js` identici carattere per carattere; **20 regate (1a, 1b, salti di vento, giri) identiche al bit** (arrivi, penalità, posizioni finali); la strambata a 6 e 15 nodi come prima (0 scuffie su 20, 10 su 10; il massimo sbandamento varia da 16° a 24° sia prima sia dopo, per il caso nel colpo del boma). **`impronta1b.txt` rigenerato, dichiarato:** 2 corse su 25 (strambata a 10 e a 16 nodi) cambiano la firma perché la firma contiene `S.boomSide`; togliendolo dalla firma (copia in una cartella temporanea) le 25 corse sono **identiche** fra motore vecchio e nuovo: cambia solo il momento del cambio di lato nelle strambate. Collaudi collegati verdi: `collaudo_boma2.py`, `collaudo_timone2.py`, `collaudo_raddrizzata.py`, `collaudo_moto_mare.py`, `collaudo_moviola.py`, `collaudo_registratore.py`.
- **Metri cambiati dopo aver visto i numeri, dichiarato** (nessuna soglia del gioco cambiata): (1) la proposta diceva 14 nodi, ma nel menu i venti sono 6, 10 e 15 e con «14» la prova non misurava niente (il metro non vedeva il caso): si usa 15; (2) con i salti di vento a 15 nodi circa metà delle prove scuffia: B1 richiede almeno 10 prove valide per caso e le scuffie si escludono; (3) B3 era scritto da +170° a −170°, ma a 15 nodi il vento apparente non passa da dietro in quei ±10° (scarroccio): scenario allargato a ±30°, soglia di 1,5 s invariata, e le scuffie escluse (almeno 24 prove valide).
- **Non provato:** Firefox (`BROWSER=firefox`) per il collaudo nuovo; `collaudo_impronta.py` ha un riferimento vecchio (27 scene su 67 diverse per le modifiche di disegno e testi dalla 1.0.62 alla 1.0.70) e va rigenerato prima della pulizia del codice: non è nel giro. `collaudo_virate2.py` resta il fallimento noto.
- **La spunta «Registra» nelle impostazioni** dice ora «Registra fuori dalle regate (M segna un momento)»: in regata la registrazione parte da sola. Scritta lunga più di una riga faceva sforare la finestra di 9 px (trovato da `collaudo_registratore.py`), quindi è corta.

## 1.0.70 — Il riquadro delle bandiere e delle penalità, l'avviso «sei oltre la linea», un mare e un pannello più puliti

Dalle osservazioni di Ale sulla 1.0.68 e dalle sue richieste del 31 ottobre 2026 (`docs/PROPOSTA-RIQUADRO-BANDIERE.md`). Il riquadro vale solo nella «Regata con i giri di penalità»; il motore non è toccato.

- **Riquadro in due pezzi, in alto ai lati del mare** (non in un angolo né sotto l'orologio, per scelta di Ale; dove prima c'erano la spia della registrazione, il vento e la bussola): a **sinistra** le bandiere esposte in grande (44 × 30 px, nome sotto) con una riga che dice cosa significano, visibili 10 s dopo ogni cambio e la X finché c'è; a **destra** la X, la penalità («Penalità: 2 giri da fare · fatti 1», il motivo, «Stai scontando: lascia strada», «Penalità scontata» per 6 s) e l'avviso. Il disegno delle bandiere è uno solo (`drawBandiera`), usato anche dalla barca giuria. I messaggi al centro restano come prima (un messaggio lungo può coprire per qualche secondo il pezzo di destra: è disegnato sopra).
- **Avviso «Oltre la linea: torna dietro»** prima dello sparo, quando il centro della barca è oltre la linea (lo stesso test che decide la X allo sparo). Si spegne dai Suggerimenti. Che la X non compaia se si passa la linea e si torna dietro prima dello sparo non è un difetto: regola 29.1.
- **Un gruppo solo in basso a destra:** la scritta del vento (senza «da») in basso, la **bussola sopra la scritta**, centrata, e a sinistra della scritta la **«R» rossa** della registrazione (con «· M1» quando si mette un marcatore, al posto di «● REG»). Dove c'erano «Q vista» e «1 / 2 zoom», tolte dal mare: sono comandi che si conoscono; «Q vista» resta nella legenda del pannello se ci sta. (Una prima versione aveva spostato solo la scritta e lasciato la bussola in alto: Ale voleva tutto raccolto.)
- **Tolti dal mare e dal pannello, su richiesta di Ale:** la **banderuola** in testa d'albero (c'è la freccia del vento apparente; la lezione 4 non la nomina più), i **nomi «reale», «apparente» e «velocità»** accanto alle frecce (restano i colori), il pulsante **Glossario** del pannello (resta nel menu), il **titolo della regata ripetuto** in basso nel pannello (resta «Istruzioni») e **«Cambia vento»** da tutte le regate, pannello e schermata finale (non cambiava il vento a regata in corso: la ricominciava con un'altra direzione; nelle gare ufficiali il vento non si sceglie, decisione di Ale; resta nelle prove).
- **Misure** (`collaudo_riquadro_bandiere.py`, nuovo, in `lancia_tutti.sh`; Chromium): **Q1** 16473 campioni in 9 regate (1, 3 e 5 minuti), riquadro visibile in 2331, 2919 bandiere verificate sui pixel (tre punti per bandiera, che distinguono le quattro), 0 errori; **Q2** passare la linea a −40…−30 s e tornare dietro: X mai (0 su 20); partenza anticipata vera (−9,5…−1 s): X sempre dopo lo sparo e tolta dopo il ritorno (20 su 20); **Q3** avviso giusto in 1600 campioni con la barca oltre la linea, mai dopo lo sparo, mai con i Suggerimenti spenti; **Q4** «2 giri da fare», «1 giro da fare · fatti 1», «Penalità scontata» in 6 prove su 6, mai scontata dopo un giro nel verso opposto (6 su 6), motivo del contatto in 11 casi con colpa su 20, nessuna penalità scritta senza debito in 5 casi; **Q5** sparisce dopo 10 s (688 campioni); **Q6** 20 regate (1a, 1b, salti di vento, giri) identiche al bit alla 1.0.69, schermata 1a e 1b identica al pixel fuori dalle zone cambiate; **Q7** costo del disegno: mediana di 5 ripetizioni +0,04 ms (0,4%; singole 0,28, 0,04, 0,04, 0,04, 0,19 ms) contro la soglia di 0,2 ms o 3%; **metro cambiato dopo aver visto i numeri, dichiarato:** con una sola misura il collaudo era uscito 0,05 / 0,06 / −0,08 e una volta 0,345 ms (3,4%, sopra soglia) perché il rumore fra blocchi è di 6 ms; in 7 prove a parte la mediana era 0,07 ms (0,7%) e la massima 0,27 ms (2,7%), quindi il costo è piccolo ma non misurabile con precisione: non è una prova di costo zero; le soglie non sono cambiate; **Q8** i due pezzi stanno nel mare e non toccano bussola, orologio, messaggio, vento, indicatori a 1360×650 e 1360×768 (canvas 970×650 e 970×768; pezzi 166×89 e 186×104); **Q9** pagina senza `#collaudo`. Controlli collegati verdi: pannello (eccesso 0 px), vista (161 casi), versione, lezioni, moto del mare (24000 quadri), segnali (G4 saltato: il riferimento 1.0.64 non vale più dopo il vento in basso), giri, registratore, quiz, esame, salti2, pulsanti, schermate; `polare.js` e `raffiche_e_virate.js` identici carattere per carattere.
- **Difetti miei nel collaudo, corretti prima di dichiarare l'esito:** Q2b contava come partenza anticipata un passaggio esattamente a 0 s (che è una partenza giusta); Q4e non teneva conto di un debito già aperto prima del contatto e con 6 casi ne misurava zero (ora 20 casi e almeno 2 richiesti); Q6b non escludeva le zone volutamente cambiate (frecce, banderuola, vento). Nessuna soglia del gioco è cambiata.
- `collaudo_vista.py` e `collaudo_versione.py` aggiornati ai nuovi testi.
- **Da guardare a occhio (Ale, Firefox):** posizione dei due pezzi, leggibilità delle bandiere (44 × 30 px), pannello senza Glossario e senza titolo ripetuto.

## 1.0.69 — Il menu a 1360×650 non scorre più

Corregge un difetto della 1.0.61-1.0.65 trovato dal giro dei collaudi del 30-31 ottobre (`docs/PROPOSTA-MENU-1360X650.md`, rimedio R2, scelto da Ale).

- **Causa:** la descrizione della regata dei giri (184 caratteri) andava a capo su più righe nel menu, e ogni fetta del 2a l'aveva allungata. A 1360×650 la pagina scorreva di 68 px.
- **Cosa cambia:** la descrizione è su una riga («Livello 2: due giri se lasci male la strada, uno se tocchi una boa; bandiere sulla giuria.») e il `padding` delle righe del menu passa da 6 a 4 px. Nessun altro testo cambia; il motore non è toccato.
- **Misure:** la pagina dietro il menu scorre di **0 px** a 1360×650 e 1360×768 (`collaudo_quiz.py` 35 casi, `collaudo_pannello.py`, `collaudo_vista.py` 161 casi, `collaudo_salti2.py`, `collaudo_esame.py` verdi).
- **Soglia cambiata dopo aver visto i numeri, dichiarato:** `collaudo_esame.py` confrontava anche l'altezza della scheda più alta del menu con quella della 0.19.5 (464 px); ora è 501 px (prima 575) perché la regata dei giri è una riga in più. Quel confronto è tolto; resta quello che conta, che la pagina non scorra (650 px contro 650).
- **Da guardare a occhio (Ale, Firefox):** le righe del menu sono 4 px più basse.

## 1.0.68 — Giri di penalità degli avversari: scelgono il verso e ripartono se si fermano

Seguito della 1.0.67, per una domanda di Ale (31 ottobre 2026): la regola 44.2 (F15) vuole i giri «nello stesso verso» ma **non dice quale**, quindi «orzare per prima» era una semplificazione mia, e da un lasco con poca velocità orzare porta la prua al vento senza abbrivio. Solo nella regata dei giri.

- **Il verso.** All'inizio del debito l'avversario sceglie: da un'andatura larga (**80° o più dal vento**) o con **poca velocità (sotto 1,5 m/s)** poggia per prima (strambata, poi virata: prende velocità); altrimenti orza per prima (virata, poi strambata). Il verso resta lo stesso per tutta la penalità, anche se un giro è sospeso e ripreso. La sequenza di prue è la stessa, specchiata. Le due soglie sono ipotesi nostre.
- **Difetto trovato dal collaudo e corretto:** una barca quasi ferma (a 44° dal vento, `u` = 0,02) restava ferma 26 s perché durante il giro avevo spento le regole di ripartenza della guida e con la barca ferma il timone non governa. Ora, sotto 0,6 m/s, il giro lascia la guida normale finché la barca riparte, poi riprende.
- **Misure** (`collaudo_giri_avversari.py`, 40 regate, stessi semi della 1.0.67; soglie scritte prima nel messaggio a Ale e in `PROPOSTA-GIRI-AVVERSARI.md`): barca ferma oltre 10 s **0 segmenti su 97** (prima 2 su 95; soglia: non peggio di 2); giri partiti da andature larghe o lente: fermi **0 su 28** (prima 2 su 28); segmenti con almeno un giro fatto **82 su 97** (prima 79 su 95); durata dei due giri **22,2 s di mediana (19,9-27,4, 19 casi)**; G1 127 su 127; G3, G6, G7, G8, G9, G10, G11 verdi; **G12 (nuovo)** il verso scelto è quello previsto in 69 segmenti su 69 (17 poggiando, 52 orzando; esclusi 19 ripresi nel verso già scelto). `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici carattere per carattere alla 1.0.67; 1a e 1b identiche al bit su 20 regate; regata dei giri identica fino al primo giro di un avversario.
- **Soglia non raggiunta, detta com'è:** debiti estinti **69 su 74 (93%)** contro il 95% che avevo scritto per questa versione (era 70 su 74 nella 1.0.67; la soglia della proposta, 80%, è rispettata). La differenza è un debito. Dei 5 non estinti, 3 non hanno mai avuto la via libera (verificato nella 1.0.67), uno aveva 10 giri da fare (cinque contatti) e ne ha fatti 2, uno ne ha fatti 4 su 6. I numeri non mostrano un miglioramento netto sull'estinzione; mostrano meno barche ferme e più segmenti con un giro. La scelta resta per la ragione fisica, non per un salto nei numeri.
- **Difetti miei nel collaudo, corretti prima di dichiarare l'esito:** (1) G12 con una finestra di 4 s non vedeva che una virata da 45° ha già passato il vento e l'angolo ricomincia a crescere: ora 1 s e partenze a più di 30° dal vento; (2) G12 contava come scelte nuove i giri ripresi dopo una sospensione, che invece mantengono il verso (44.2): esclusi; (3) G9 contava come caso un avversario che aveva fatto i giri prima di arrivare, perché la rotta lo aveva riportato a più di 25 m dalla linea: ora si misura la differenza dei giri fatti da quando il debito è stato dato. Nessuna soglia del gioco è cambiata.

## 1.0.67 — Livello 2a, fetta 5: i giri di penalità anche per gli avversari

Quinta fetta del 2a (`docs/PROPOSTA-GIRI-AVVERSARI.md`, F15 44.1 e 44.2), con le risposte di Ale del 31 ottobre 2026: giri **dopo lo sparo**, «semplificata e dichiarata». Solo nella «Regata con i giri di penalità»; 1a, 1b, torneo e le altre regate non cambiano (verificato al bit).

- **Cosa cambia.** Un avversario colpevole di un contatto non prende più +15 s: ha un debito di **due giri** (`b.gDebt`). Dopo lo sparo, in regata, con **nessuna altra barca a meno di 4 lunghezze** e lontano (25 m) da boe e, sull'ultimo lato, dalla linea d'arrivo, comincia a girare; se un'altra barca arriva a meno di **2 lunghezze** sospende, il giro in corso si perde e riparte da zero. Il giro è una sequenza di prue rispetto al vento (sempre **orzando per prima**, quindi nello stesso verso: bolina dall'altra parte del vento, poppa larga, strambata, bolina di partenza); un giro è fatto con 360° nello stesso verso, una virata e una strambata, contate dalla barca stessa (gli avversari non hanno i contatori del giocatore). Barra, scotta e motore sono quelli di sempre: il costo in tempo esce dal motore. Nel codice: `giroAI`, `giroLibero`, `giroLontano`, `giriMancantiAI` in `js/regate.js`; tre regole della guida (angolo morto, abbrivio, piantata) non valgono mentre gira.
- **Regola 21.2 per loro.** Mentre gira ha `sconta = true`: `chiCede` fa cedere lui a chi non sconta, con la regola nel messaggio. Se scontano tutti e due valgono le regole 10-13.
- **Arrivo con giri mancanti.** Come per il giocatore: +15 s per giro che manca, con la voce nell'elenco. La riga delle regole dice «Penalità alla Rossa: due giri.»
- **Semplificazioni dichiarate:** (1) i giri cominciano solo dopo lo sparo (il regolamento li vuole «appena possibile» dopo l'incidente, anche prima del via: si farebbe uscire la barca dalla posizione di partenza); (2) l'avversario non gira mai vicino ad altre barche né alle boe, quindi può arrivare con giri non fatti e pagare 15 s per giro (regola 44.2 vuole «ben lontano dalle altre barche» ma non dice che sia sempre possibile); (3) la 44.1(a) (se si viola una regola della parte 2 e la 31 nello stesso incidente basta la prima) non c'è: i giri si sommano; (4) gli avversari non toccano boe e non evitano chi gira; (5) soglie 4 e 2 lunghezze, 25 m e 12° sono ipotesi nostre.
- **Misure** (`tests/collaudo_giri_avversari.py`, nuovo, in `lancia_tutti.sh`; Chromium; 40 regate a semi fissi 1-40 con avversari principianti ed esperti alternati; soglie scritte prima in `PROPOSTA-GIRI-AVVERSARI.md`): **G0 il metro:** 224 giri di debito = 112 contatti con colpa degli avversari, uguali ai contatti nell'elenco (37 regate su 40 con almeno un debito). **G1:** 134 giri dichiarati su 134 con rotazione ≥ 360° (tolleranza 5° del metro, vedi sotto), una virata e una strambata. **G2:** debiti con almeno 90 s di regata davanti **estinti in 70 casi su 74 (95%**, soglia 80%): 3 dei 4 non estinti non hanno mai avuto la via libera (verificato: nessuna barca entro 4 lunghezze **e** lontano da boe e arrivo nello stesso istante), il quarto ha fatto 4 giri su 6. **G3:** stesso verso in 23 avversari con almeno due giri. **G4:** i due giri di fila durano **22,2 s di mediana (19,9-29,3, 21 casi)**; il giocatore 17,5 s; G4b (solo riportato) rispetto all'avanzamento di prima si perdono 25,8 s (18,1-33,0, 11 casi) contro i 15 s di prima. **G5:** fermo oltre 10 s in 2 segmenti su 95 (soglia 5%). **G6:** scuffie 0 su 95. **G7:** altro debito mentre girano 0 su 95 (la sospensione a 2 lunghezze lo evita). **G8:** l'avversario che sconta cede con la 21.2 in 120 posizioni su 120 (in 52 il giocatore avrebbe ceduto senza la regola); G8b se scontano in due, regole 10-13 in 120 su 120. **G9:** arrivo con due giri da fare, +30 s e voce nell'elenco in 10 casi su 10. **G10a:** 20 regate dell'1a e dell'1b identiche al bit alla 1.0.66; **G10b:** regata dei giri identica al bit fino al primo giro di un avversario (980 istantanee in 20 regate; 18 regate su 20 divergono dopo, quindi il metro vede la differenza). **G11:** pagina senza `#collaudo`: l'avversario con due giri da fare ne fa 2 in 120 s simulati, nessun errore. `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici carattere per carattere alla 1.0.66; `collaudo_giri.py` (D2 aggiornato: il debito è dell'avversario, non +15 s) e `collaudo_boa.py` verdi; pannello a 1360×650 con eccesso 0 px.
- **Difetti miei trovati e corretti prima di dichiarare l'esito (nessuna soglia del gioco cambiata):** (1) nessun giro si chiudeva perché gli avversari non hanno i contatori di virate e strambate del giocatore (`S.tacks` non esiste per loro): ora li conta `giroAI`; (2) l'ultima prua della sequenza cadeva sul bordo del salto di 360° e la barca restava ferma a 147° di poppa: spostato il bordo di 12°; (3) G0 non contava i contatti prima dello sparo; (4) G8 provava una sola mura del giocatore e non vedeva mai il caso che cambia: ora due; (5) G10b come scritta in proposta (regate senza debiti) aveva solo 2 regate su 20: cambiata in «identica fino al primo giro», dichiarato; (6) G1 non vedeva bene i giri: 31 su 134 stavano fra 356,9° e 360° per il campionamento ogni 0,1 s (la barca ruota fino a 36°/s): tolleranza del metro portata a 5° **dopo aver visto i numeri**, dichiarato; il motore conta 360° esatti.
- **Limiti:** i giri costano all'avversario più dei 15 s di prima (7-11 s in più): è il costo vero delle manovre, e a parità di colpa chi gira ora paga di più di chi pagava a tempo; la sequenza è una guida e non il modo in cui un timoniere girerebbe; il registratore e la moviola non registrano i giri degli avversari; il torneo non è toccato.

## 1.0.66 — Livello 2a, fetta 4: chi sconta la penalità lascia strada (21.2) e chi torna dopo il via anticipato pure (21.1)

Quarta fetta del 2a (`docs/PROPOSTA-REGOLA-21-2.md`, F15 21.1 e 21.2), con le due risposte di Ale (31 ottobre 2026: «come proponi tu»: la 21.1 insieme, soglia 120°). Solo nella «Regata con i giri di penalità»; le altre regate non cambiano.

- **21.2.** Il giocatore «sta scontando» quando ha un debito aperto e negli ultimi 20 s la prua ha ruotato di almeno **120°** nello stesso verso (più di una virata, circa 90°); resta così finché il debito non è estinto o finché passano 20 s senza finire un giro. Se sta scontando e l'altra barca no, **cede lui**, con la regola 21.2 nel messaggio («stavi scontando una penalità e dovevi lasciare strada a chi non la scontava»): la Sezione A (10-13) fra le due non vale, come nel regolamento. Un contatto mentre si sconta dà altri due giri.
- **21.1.** Dopo lo sparo, una barca ancora oltre la linea (`ocs`) che deve tornare lascia strada a una che non lo è. Vale per tutte le barche, **avversari compresi**: nella regata dei giri chi deve tornare cede e chi ha la precedenza tiene la rotta (la guida degli avversari usa `chiCede`), quindi la loro guida cambia lì e non altrove. Se sono entrambe oltre la linea, o una sconta e l'altra torna, nessuna è «quella che non lo fa» e valgono le regole 10-13.
- **Semaforo e registratore.** Il semaforo (se acceso) diventa rosso per chi sconta con un'altra barca vicina, perché usa `chiCede`. Nel registratore gli eventi `sconta inizio` e `sconta fine`.
- **Misure** (`tests/collaudo_regola21.py`, nuovo, in `lancia_tutti.sh`; Chromium; soglie scritte prima; 4 partenze × 30 posizioni dell'avversario = 120 casi, più ampio dei 30 della proposta): giocatore che sconta cede con la 21.2 in **120 casi su 120**, e in **63** di questi senza la regola avrebbe ceduto l'altro (è il caso che cambia); in tutti il giocatore stava davvero scontando; debito aperto senza girare: **chiCede identico a prima in 120 su 120**; debito estinto (4 su 4): regole 10-13 in 120 su 120; contatto mentre si sconta: **debito +2 e «regola 21.2» in 10 casi su 10**; 21.1: avversario che deve tornare cede in 90 posizioni su 90 (in 63 prima avrebbe ceduto il giocatore), giocatore che deve tornare cede in 90 su 90, entrambi o chi sconta contro chi torna: regole 10-13 in 90 su 90 ciascuno; registratore e pagina senza `#collaudo` a posto. **Non-regressione:** 20 regate dell'1a e dell'1b identiche al bit alla 1.0.65; `polare.js` e `raffiche_e_virate.js` identici; `collaudo_giri`, `collaudo_boa`, `collaudo_segnali`, `collaudo_registrazione`, `collaudo_moviola` verdi; pannello con 0 px di eccesso.
- **Quanto pesa (K6, solo riportato, atteso nostro: almeno 24 regate su 30 estinte e meno di 0,5 giri di debito in più):** 30 regate con la flotta, debito di due giri a 25 s, giri a mano: **debito estinto in 30 su 30**; giri di debito in più **0,47 in media** (massimo 4, quindi appena sotto la soglia: in alcune regate la spirale c'è); contatti con colpa del giocatore durante i giri 0,23 a regata, di cui 8 in tutto per la regola 21.2 su 30 regate. Il rischio della proposta (chi gira vicino agli altri prende altri giri) si vede ma non è la regola.
- **Difetti nel mio collaudo, trovati e corretti prima di dichiarare l'esito (nessuna soglia cambiata):** (1) i casi usavano la regata senza avversari e la griglia non aveva l'avversario: ora la flotta; (2) la partenza non era pulita: il pilota di prova prende colpe nei primi 25 s e ruota per conto suo, e un debito del pilota faceva risultare «sta scontando» anche nel caso «senza girare»: ora i casi partono da debito zero e con il debito di due giri messo da me (in K6 le colpe naturali restano).
- **Limiti:** la soglia di 120° e i 20 s sono ipotesi nostre (una poggiata lunga può superare 120° senza essere un giro: il giocatore cede senza saperlo; la riga delle regole lo dice quando scatta); gli avversari non fanno giri (+15 s) e quindi la 21.2 non vale per loro; gli avversari non evitano chi gira; manca la 21.3 (barca che va indietro con la vela a collo).

## 1.0.65 — Livello 2a, fetta 3: le bandiere della partenza (classe, P, X, blu)

Terza fetta del 2a (`docs/PROPOSTA-SEGNALI-PARTENZA.md`, fetta 3; F15 26 e 29.1), per decisione di Ale (31 ottobre 2026) di seguito. Vale **solo nella «Regata con i giri di penalità»**: le altre regate, 1a compresa, non cambiano né nel gioco né nello schermo (verificato al pixel). Le lezioni sulle bandiere vengono dopo, dentro la riorganizzazione.

- **Le bandiere sulla barca giuria.** Con 5 minuti la sequenza del regolamento: bandiera di classe a −5, P a −4, P ammainata a −1, classe ammainata al via. Con 3 minuti una sequenza breve (classe a −3, P a −2, P giù a −1) e con 1 minuto solo la classe: sono ipotesi nostre, dichiarate. Dopo il via c'è la bandiera blu (la linea è d'arrivo). La **X** (richiamo individuale) sale allo sparo se una barca è oltre la linea e scende quando è tornata dietro la linea, o dopo 4 minuti al massimo. Le bandiere sono quattro riquadri sul ponte; la bandiera di classe è nostra (bianca con una vela blu), la P (blu con quadrato bianco) e la X (bianca con croce blu) sono quelle internazionali.
- **Messaggi** che seguono le bandiere («Avviso: alzata la bandiera di classe, partenza tra N minuti», «Preparatorio: alzata la bandiera P», «Un minuto: ammainata la P»); 30 e 10 secondi come prima. Il gioco non ha suoni: lo dice il testo della regata. Nel registratore l'evento `bandiere`.
- **Misure** (`tests/collaudo_segnali.py`, nuovo, in `lancia_tutti.sh`; Chromium; soglie scritte prima): bandiere giuste a ogni decimo di secondo con 1, 3 e 5 minuti (3 regate ciascuna), **66.612 controlli, 0 errori** contro una tabella scritta a parte nel collaudo; messaggi una volta e al tempo giusto in tutti i casi; X: **12 regate con richiamo e 6 senza**, X su quando c'è una barca oltre la linea e giù quando l'ultima è tornata (guardando le posizioni delle barche, non i campi del gioco), mai senza richiamo, e se una barca resta oltre la linea la X scende a 240 s (6 regate); **le altre regate: 20 regate identiche al bit alla 1.0.64 e schermata a −30 s identica al pixel nella 1a e nella 1b**, diversa nella regata dei giri (le bandiere si vedono); registratore: classe, classe+P, classe, blu nell'ordine giusto; pagina senza `#collaudo` senza errori. `polare.js` e `raffiche_e_virate.js` identici carattere per carattere, `collaudo_giri.py`, `collaudo_boa.py`, `collaudo_registrazione.py`, `collaudo_moviola.py` verdi, pannello a 1360×650 con eccesso 0 px.
- **Difetti nel mio collaudo, trovati e corretti prima di dichiarare l'esito:** (1) il controllo senza richiamo lasciava la barca alla deriva: oltre la linea con 1 minuto di preparazione era un richiamo vero e la X saliva giustamente; ora la barca resta ferma; (2) il controllo della X contava come «ancora oltre la linea» una barca che era tornata e poi ripartita regolarmente: ora «tornata» vale per sempre; (3) il confronto al pixel fra due pagine dopo molte regate falliva anche fra due versioni uguali (i riflessi dell'acqua dipendono dal tempo reale): ora ogni schermata sta in una pagina nuova; (4) il controllo del registratore leggeva anche registrazioni di prove precedenti. Nessuna soglia è cambiata.
- **Limiti:** le bandiere sono piccole (circa 15 pixel a zoom normale: si giudica giocando); l'X resta su fino a 4 minuti anche se la barca richiamata se ne va in altro modo; la linea tratteggiata passa sopra le bandiere; manca la lezione; il richiamo generale e le altre bandiere non ci sono.

## 1.0.64 — La barca dei giudici ha la forma della barca dei giudici

Ale (31 ottobre 2026, giocando la 1.0.63): «ho provato a schiantarmi sulla barca dei giudici, ma ci passo attraverso». Verificato: era vero a prua e a poppa.

- **Causa.** Nella 1.0.63 il comitato era un cerchio di 2 m attorno al centro, ma disegnato è lungo 8 m e largo circa 3 (`drawRace`): oltre 2 m dal centro si vedeva la barca e non succedeva niente. L'avevo scritto fra i limiti («di prua o di poppa ci passa vicino senza urtare») ma sottovalutato; il mio collaudo guardava un cerchio e quindi passava.
- **Correzione.** Il comitato è il poligono con cui è disegnato (cinque punti, prua al vento, stessi numeri di `drawRace`). Il contatto fra due poligoni convessi usa la stessa funzione dei contatti fra scafi (`hullOverlap` ora è una riga sopra `polySep`, che dà anche la distanza): spinta fuori lungo la direzione di minima sovrapposizione e velocità al 60% al primo urto. Spillo e boe restano cerchi di 0,9 m. `CB_R` non esiste più.
- **Misure** (`collaudo_boa.py`, parte I, 30 prove, soglie della 1.0.63 estese al comitato): scafo messo sopra il comitato **al centro, a prua e a poppa**, sui lati 1 e 2 (6 casi) più boa e spillo: **respinto fuori in tutti i 270 casi**, partendo dentro in tutti; velocità dopo il primo passo 0,595 (270 casi su 270, soglia 0,61); 72 lanci da 12 m a 3 e 5 m/s da 12 direzioni, comprese quelle lungo l'asse della barca: **mai attraversato**; penalità come prima. **Pilota di prova, 60 regate:** 60 su 60 arrivate, mediana 251,8 s contro 251,8 s della 1.0.62 (**differenza +0,02 s**), nessun tocco del comitato. **Non-regressione:** 20 regate dell'1a e dell'1b identiche al bit alla 1.0.62 (anche con `hullOverlap` riscritta), `polare.js` e `raffiche_e_virate.js` identici carattere per carattere, `collaudo_contatto_vero.py` 23 controlli su 23.
- **Cosa è venuto fuori mentre misuravo (riportato com'è):** in `collaudo_giri.py` K1 (12 regate, pilota con un debito iniziale) una regata su 12 **non arriva**: il pilota di prova ha anticipato il via, deve tornare dietro la linea proprio dal lato del comitato e resta fermo contro lo scafo per oltre 200 s (seme 812: 37,5; −4,0; prua 238°, 2,5 nodi). Un giocatore può sterzare; il pilota (che è anche la guida degli avversari) no, e la sua guida non si tocca. **Metodo cambiato dopo aver visto il risultato (dichiarato):** K1 non chiede più «tutte arrivate» ma «al più una su dieci non arrivata», contata e riportata; i giri spuri restano a zero. Nelle 60 regate del pilota e nelle 30 prove di `collaudo_boa.py` nessun incastro. Il comitato fermo ha però un effetto sulla partenza anticipata di chi torna da quel lato.
- **Limiti:** l'oggetto non si sposta; gli avversari ci passano ancora attraverso; spillo e boe sono cerchi di 0,9 m; manca il caso di una scotta o di un'ancora (non ci sono).

## 1.0.63 — Livello 2a, fetta 2b: boe e barca dei giudici sono ostacoli per il giocatore

Ale (30 ottobre 2026): «se tocco una boa o la barca dei giudici non mi scontro?». Dalla 1.0.62 la penalità c'era ma la barca passava attraverso. Criteri e soglie scritti prima in `docs/PROPOSTA-LIVELLO-2A.md` (fetta 2b). Solo nella «Regata con i giri di penalità» e solo per il giocatore.

- **Ostacolo fermo.** Spillo, barca dei giudici e boe (anche quelle che in quel momento non danno penalità) non si attraversano: lo scafo che entra nel raggio (0,9 m, comitato 2,0 m) viene spinto fuori lungo la retta fra i centri, a ogni passo, fino a 0,05 m oltre il raggio; al primo passo del tocco perde il 40% della velocità, come nel contatto fra barche. La penalità (un giro) resta quella della 1.0.62 e spetta solo alle boe che contano. L'oggetto non si sposta; gli avversari non sono respinti (come prima, passano attraverso).
- **Misure** (`tests/collaudo_boa.py`, parte I, 30 prove): scafo messo sopra lo spillo, il comitato e la boa (sia dove contano sia dove no) **respinto fuori dal raggio 30 su 30 per ciascuno dei cinque casi** (distanza minima 0,99 m con raggio 0,9; 2,08 m con raggio 2,0); velocità dopo il primo passo **0,595 di prima in 150 casi su 150** (soglia 0,61); respingimento senza effetti sul debito (spillo e comitato sul lato 1: nessun debito; gli altri: +1); **scafo lanciato contro l'oggetto da 12 m, 12 direzioni, 3 e 5 m/s, 72 lanci: mai attraversato** (distanza minima 0,90 m); avversario messo sopra l'oggetto: non respinto (3 su 3). Gli altri criteri della 1.0.62 (A-E, H) restano verdi con le stesse soglie.
- **Il pilota di prova** (60 regate con la flotta, stessi semi della 1.0.62, soglia scritta: tutte arrivano e il tempo mediano cambia di non più di 3 s): **60 su 60 arrivate, nessuna incastrata; mediana 252,7 s contro 251,8 s, differenza +0,9 s**. Dettaglio da riportare: **21 regate su 60 hanno un tempo diverso** (quelle in cui tocca lo spillo e la flotta poi si muove in modo diverso), con scarti da −64 s a +55 s e media −3,1 s sulle 21: non c'è una perdita sistematica, c'è la variabilità di una regata che cambia dopo un urto.
- **Non-regressione:** arrivi, penalità e posizioni finali di 20 regate dell'1a e dell'1b identici al bit alla 1.0.62; `polare.js` e `raffiche_e_virate.js` identici carattere per carattere (motore non toccato); `collaudo_giri.py`, `collaudo_registrazione.py` e `collaudo_moviola.py` verdi.
- **Difetto nel collaudo, trovato e corretto:** il primo controllo sulla velocità metteva la velocità a 3 m/s *prima* di posizionare lo scafo, e il posizionamento la azzerava: il rapporto usciva «−inf» e il controllo passava a vuoto. Ora la velocità si imposta dopo il posizionamento, il controllo richiede un rapporto maggiore di zero e il rapporto reale (0,595) è riportato.
- **Limiti:** il comitato è un cerchio di 2 m, ma disegnato è lungo 8 m, quindi di prua o di poppa la barca ci passa vicino senza urtare; l'oggetto non si sposta né reagisce; gli avversari ci passano ancora attraverso; il confronto dei tempi del pilota con la 1.0.62 è una prova a parte (`TEMPI=1`, circa 15 minuti), non nel giro di `lancia_tutti.sh`.

## 1.0.62 — Livello 2a, fetta 2: un giro di penalità per la boa toccata

Seconda fetta del regolamento del livello 2a (`docs/PROPOSTA-LIVELLO-2A.md`, F15 regole 31 e 44.1), per decisione di Ale (30 ottobre 2026) fatta di seguito. Vale solo nella «Regata con i giri di penalità» e solo per il giocatore; le altre regate e gli avversari non cambiano.

- **Il tocco.** La boa è un cerchio di 0,9 m (come disegnata), la barca del comitato di 2,0 m; si tocca quando il contorno dello scafo (lo stesso dei contatti) arriva al raggio. Le boe **non sono ostacolo** in questa versione (lo diventano per il giocatore nella 1.0.63): ci si passa attraverso, il tocco è solo la penalità. Un tocco vale **una volta** finché lo scafo non si allontana di 3 m dal bordo. Costa **un giro** (`giriDebito(1)`), che si somma ai due di un contatto; il resto dei giri è quello della 1.0.61.
- **Quali boe contano.** Spillo e comitato durante il conto alla rovescia, fino al via e sull'ultimo lato; la boa del lato in corso; dal secondo lato in poi anche la boa da cui il lato parte. Messaggio, riga delle regole e voce nell'elenco dicono «regola 31»; nel registratore l'evento `boa_toccata`; «Rivedi» ne fa uno spezzone.
- **Misure** (`tests/collaudo_boa.py`, nuovo, in `lancia_tutti.sh`; Chromium; soglie scritte prima nella proposta; 30 prove salvo dove detto): scafo sulla boa o sulla linea d'arrivo, **debito +1 esatto 30 su 30**, nessun +15 s; a 0,5 m dal bordo **nessun tocco 30 su 30** (e le stesse prove con lo scafo sopra: +1 in 30 su 30); fermo 5 s: **un solo giro 30 su 30**, allontanato e di nuovo sopra: +1 (totale 2) 30 su 30; la linea sul lato 1 e la boa 1 prima del via non contano (0 su 30 e 0 su 30), la boa lasciata sull'ultimo lato sì (30 su 30); un giro estingue il debito 30 su 30, senza scuffie; registratore `boa_toccata` e pagina senza `#collaudo` senza errori. **Non-regressione:** arrivi, penalità e posizioni finali di 20 regate dell'1a e dell'1b identici al bit alla 1.0.61; `polare.js` e `raffiche_e_virate.js` identici carattere per carattere (il motore non è toccato); `collaudo_giri.py` (12 prove) e `collaudo_pannello.py` (eccesso 0 px) verdi.
- **Quanto tocca da solo il pilota di prova (solo riportato, nessuna soglia):** in 60 regate con la flotta a 10 nodi **21 regate su 60 hanno almeno un tocco** (23 tocchi in tutto): 22 sullo spillo e 1 sulla boa di bolina, nessuno sul comitato. I tocchi allo spillo sono del pilota che ha anticipato il via e torna dietro la linea girando attorno allo spillo (nei casi guardati era fuori dalla linea, a 2-3 m dal centro, dopo 9-69 s di regata). Per chi gioca a mano è un rischio da guardare.
- **Limiti:** raggi e distanza di 3 m sono ipotesi nostre; niente tocchi degli avversari; il triangolo non è provato (la regata dei giri è un bastone); l'aiuto «penalità a tempo» non ha ancora l'interruttore; la boa toccata non frena la barca.

## 1.0.61 — Livello 2a, fetta 1: i giri di penalità al posto dei 15 secondi

Prima fetta del regolamento del livello 2a (`docs/PROPOSTA-LIVELLO-2A.md`, F15 regole 44.1 e 44.2), per decisione di Ale (30 ottobre 2026) fatta di seguito, senza le due fermate. **Gli avversari dell'1b non si toccano** (stessa decisione).

- **Una regata nuova, in fondo all'elenco:** «Regata con i giri di penalità» (barca dell'1b, tre avversari, vento 10 nodi, flag `giri`). Come «Regata nei salti di vento» resta fuori da meriti e carriera; le altre regate non cambiano.
- **Il debito.** Un contatto con colpa del giocatore non dà più +15 s ma un debito di **due giri**; ogni colpa nuova ne aggiunge due e azzera la finestra, perché i giri contano dopo l'infrazione. Un giro è fatto quando, negli ultimi 20 s, la prua ha ruotato di almeno 360° nello stesso verso (senza tornare indietro di più di 20° dal picco) e ci sono state almeno una virata e una strambata. Un giro nel verso opposto al precedente fa ricominciare il conto. Una scuffia azzera la finestra. La riga delle regole nel pannello dice quanti giri mancano (nessun pixel in più).
- **Se si arriva col debito aperto:** +15 s per ogni giro che manca, con la voce nell'elenco («Tu, giri di penalità non fatti (2): +30 s»). Nessuna squalifica (ripiego dichiarato).
- **Gli avversari restano a +15 s** per ogni colpa: non fanno giri. Differenza dichiarata. Il costo misurato dei due giri del giocatore è 17,5 s (sotto), quindi la differenza è piccola; la scelta su un tempo equivalente resta aperta.
- **Registratore:** evento `giro_penalita fatti/dovuti`, riga `Q` «penalità scontata», legenda aggiornata.
- **Misure** (`tests/collaudo_giri.py`, nuovo, in `lancia_tutti.sh`; Chromium; pilota che governa a mano il timone, soglie scritte prima nella proposta, 30 prove salvo dove detto): **due giri estinguono il debito 30 su 30** (15 a destra e 15 a sinistra, senza avversari, nessuna scuffia); **un giro solo no, 30 su 30**; **un giro in un verso e uno nell'altro no, 30 su 30** (rotazione nel verso opposto 400°); costo dei due giri **mediana 17,5 s, da 16,8 a 18,4** (atteso, stima nostra: 15-25); contatto vero con colpa del giocatore: debito di due giri e nessun +15 s (5 casi su 10 con la flotta, entrambi i lati), colpa dell'avversaria: +15 s a lei e niente al giocatore (5 casi), ogni contatto dà 0 o 2 di debito mai altro; arrivo senza avversari con il debito aperto: +30 s in 6 regate su 6, già scontato: nessun secondo in più (6 su 6); **nessun giro riconosciuto dopo il debito a un pilota che non ne fa a posta, 30 regate su 30**; registratore: eventi `giro_penalita` 1/2 e 2/2 e la riga «penalità scontata»; pagina senza `#collaudo`: la regata è nel menu, si apre, il debito compare nel pannello; nessun errore di pagina. **Le altre regate non cambiano:** arrivi, penalità e posizioni finali di 20 regate dell'1a e dell'1b identici al bit alla 1.0.60.
- **Cosa è venuto fuori mentre misuravo (riportato com'è):** (1) il pilota ha una colpa spesso già nei primi 25-30 s di regata (debito di partenza di 2 o 4 in molte prove) e durante i giri a volte ne arriva un'altra: nella regata dei giri la flotta pesa; la regola 21.2 (chi sconta lascia strada) non c'è ancora. (2) Il mio primo K1 («nessun giro spurio») contava anche giri **veri** fatti prima del debito artificiale: in 2 regate su 30 il pilota, dopo una colpa nel conto alla rovescia, ha girato su se stesso con virata e strambata ed è stato riconosciuto giustamente. K1 ora misura solo l'incremento dopo il debito: 0 su 30. La finestra di 20 s e l'azzeramento a ogni colpa li ho messi pensando a un caso che era probabilmente lo stesso giro vero: restano corretti per le regole, ma non sono dimostrati necessari da quel caso. (3) Il criterio 4 della proposta (rotazione di 360° senza virata e strambata) ha 0 casi possibili: la prua che gira passa sempre dal vento e da poppa; dichiarato.
- **Metodo cambiato dopo aver visto i risultati (dichiarato):** i criteri 1-3 e 6 si misurano senza avversari (con la flotta i contatti naturali sommano debiti e falsano il conto); K1 aggiunto dopo (e corretto come sopra); D misura gli incrementi del debito e non il valore assoluto. Le soglie (30 su 30, nessun giro spurio) non sono cambiate.
- **Limiti:** niente giri degli avversari, niente un giro per la boa (RRS 31), niente 21.2, niente bandiere né lezioni (fette successive); l'aiuto «penalità a tempo» non ha un interruttore (le impostazioni non hanno un pixel libero); il tempo massimo di un giro (20 s) e il ripiego di 15 s sono ipotesi nostre.

## 1.0.60 — La registrazione parte da sola in ogni regata (fase 1 della modalità coach)

Da `docs/PROPOSTA-COACH-REGISTRATORE.md`, con due idee di Ale (29 ottobre 2026): registrare anche i minuti **prima del via** e dividere le regate lunghe (in futuro 20 minuti) in **pezzi da 5 minuti**.

- **Parte e si ferma da sola.** In ogni regata (1a, 1b, torneo) il registratore si accende all'inizio del conto alla rovescia e si chiude all'arrivo. Prove, lezioni e navigazione libera non registrano. La registrazione a mano (impostazioni ⚙) ha la precedenza: se è già accesa la regata non ne apre un'altra; se la si accende a regata in corso, quella automatica si chiude. Se si esce dalla regata, si preme «Ricomincia» o si chiude la pagina, il file si chiude come «interrotto».
- **Un file per regata, a pezzi.** Il primo pezzo va dall'inizio del conto alla rovescia a 120 s di regata, gli altri durano 300 s. Ogni pezzo ha l'intestazione (versione, regata, impostazioni, barche e carattere degli avversari) e un fotogramma in comune con il pezzo vicino, che dà le posizioni di tutte le barche all'inizio. Formato 3: `t` = secondi di regata (negativi prima del via), righe `S` e `B` a **10 al secondo** (nel formato 2 una al secondo), tempo con i centesimi. Una riga `F` per barca alla chiusura (posto, tempo, penalità, stato). I marcatori M ripartono da 1 a ogni regata; il tasto O della moviola scrive `segno_rivedi n`, con lo stesso numero di «Rivedi».
- **Dove stanno.** Salvati da soli in IndexedDB di Firefox, uno per pezzo, le **ultime 5 regate** (ipotesi nostra). Nel piè di pagina del menu il link «Regate registrate» apre una finestra con la lista, «Scarica» (un pezzo alla volta) e «Cancella tutte»; una riga dice che restano solo nel browser. (Messa in una finestra a parte perché nelle impostazioni ⚙ non c'era un pixel di spazio: la prima versione faceva sforare il dialogo di 24 e 80 px, preso da `collaudo_registratore.py`.) In una finestra privata restano in memoria finché la pagina è aperta.
- **Non c'è il seme.** Il gioco usa `Math.random` ovunque, quindi nell'intestazione non c'è nessun seme per rigiocare la regata identica; c'è la situazione di partenza (impostazioni, barche, carattere).
- **Correzione della 1.0.58.** `collaudo_ricarica.py` segnalava un errore di pagina (`reading 'frames'`): il cursore della moviola (`#movPos`) spostato a moviola chiusa. Un giocatore non poteva raggiungerlo; ora non fa niente se la moviola è chiusa.
- **Misure** (`tests/collaudo_registrazione.py`, nuovo, in `lancia_tutti.sh`; Chromium; 25 verifiche su 25): 20 regate di fila col pilota, 42 pezzi, nessun byte della regata prima; prima riga a −180 s; righe `S` a 0,10 s tutte; 22 giunture con un fotogramma in comune; pezzi chiusi a 120, 420 e 700 s; riga `F`: posto, tempo e penalità del giocatore uguali al gioco in 20 regate su 20; pezzo più grande 0,56 MB (soglia 2 MB), medio 0,38 MB; dopo la ricarica della pagina i pezzi ci sono ancora e si scaricano; pagina senza `#collaudo` provata. **Il gioco non cambia:** arrivi, penalità, posizioni finali e passi identici al bit su 20 regate, sia accesa contro spenta nello stesso codice sia contro la 1.0.59. `polare.js` e `raffiche_e_virate.js` invariati; `motore.js` non toccato.
- **Costo, da non dare per chiuso.** La soglia era «al massimo +3%» sul passo di simulazione. Tre misure: (1) due pagine diverse in sequenza, a macchina occupata: +25,5% (metodo sbagliato); (2) rapporti per coppie alternate: mediana +14,3%, da −4,5% a +37,1% sulla stessa regata (troppo rumore); (3) stessa regata, 10 corse per modalità, rapporto fra le mediane: **+0,4%** (89 contro 88 µs per passo) e, nel giro finale, **+0,5%** (90 contro 89 µs); i tempi minimi danno però **+7,5%** e **+6,9%** (88 contro 82 e 88 contro 83 µs). **Il metodo è stato cambiato due volte dopo aver visto i risultati; la soglia no.** Il costo vero sta fra 0 e circa 8%: non provato sotto il 3%. `collaudo_registratore.py`: accende la registrazione a mano con `if (!ses.on || ses.auto)` (prima bastava `!ses.on`, ora `ses.on` è già vero in regata).
- **Giro completo di Ale sulla 1.0.60** (30 ottobre 2026, 56 collaudi; test-only, nessun cambio di versione): i numeri dei collaudi già noti sono **identici carattere per carattere** a quelli del giro sulla 1.0.59 (virate2 12,5% e 13,2%, partenze 6,7% contro 5,0%, avversari1b 7 su 10, competizione C1, torneo C11 R7 2,72 e 2,70 s): la 1.0.60 non ha spostato il gioco. Due falliti nuovi, entrambi dei collaudi: (1) `collaudo_carriera.py` K5 confronta il piede del menu con quello della 1.0.1 e non conosceva il link «Regate registrate»: aggiunto fra le differenze volute, ora OK (57 controlli su 57); (2) `collaudo_registrazione.py` E2 con +8,4% di mediana (macchina occupata); su macchina libera sei misure da 0,0% a +2,2% e le due dopo il cambio (20 corse per modalità invece di 10) +0,0% e +0,4%. **Metodo cambiato una terza volta, soglia sempre 3%.** `collaudo_laboratorio.py` OK.
- **Limiti dichiarati:** la chiusura alla chiusura della pagina (`pagehide`) parte, ma il browser può non completare la scrittura: in quel caso si perde al massimo l'ultimo pezzo (fino a 5 minuti). Il file si scarica un pezzo alla volta. Alla chiusura per arrivo la riga `F` mostra gli avversari arrivati fino a quel momento. Firefox: provato solo il collaudo in Chromium (da lanciare con `BROWSER=firefox`).

## 1.0.59 — La moviola passa dal tasto M al tasto O

Con il registratore acceso, M faceva due cose insieme: scriveva il marcatore nel file e salvava lo spezzone della moviola. Ora **M resta al marcatore** e la moviola usa **O** (scelta di Ale, 29 ottobre 2026: gli altri tasti restano per la mano sinistra). Cambiano la condizione in `js/moviola.js` e `tests/collaudo_moviola.py`; nessuna modifica al motore (`js/motore.js` intatto; `polare.js` e `raffiche_e_virate.js` girano e danno i valori di sempre). **Misure:** `collaudo_moviola.py` OK (10 regate, 728 confronti, massimo 0,019 m e 0,28°, spezzoni per regata da 2 a 6, uscita pulita); `collaudo_versione.py` OK. Non provato in modo diretto che M non apra più spezzoni: lo dice la riga di codice, non una misura.

## 1.0.58 — «Rivedi": la moviola delle regate (prima fetta della modalità coach)

Idea di Ale (28-29 ottobre 2026): quando si ha un dubbio durante la regata si preme **O** (dalla 1.0.59; nella 1.0.58 era M), e a fine regata si rivede il momento. Nuovo file `js/moviola.js`, tra `registratore.js` e `avvio.js` (`docs/PROPOSTA-COACH-REGISTRATORE.md`, fase 2 ridotta; la ripetizione «non identica» e il momento clou automatico restano da fare).

- **Registrazione in memoria:** dopo lo sparo le posizioni di tutte le barche (posizione, prua, sbandamento, boma, scuffiata) a 10 al secondo, buffer di 10 s. **M** (in regata, anche col registratore spento) e ogni contatto con penalità (al massimo 6) ne fanno uno **spezzone**: 10 s prima e 8 s dopo; al massimo 12 spezzoni. Solo lettura: non chiama `Math.random` e non scrive nel gioco.
- **«Rivedi»** (nuovo pulsante nella schermata finale, visibile solo se c'è almeno uno spezzone): gioco fermo, barra con titolo («Il tuo segno n. 1, a 1:00» o la penalità col motivo), cursore, pausa, velocità 1× ½× ¼×, momento prima/dopo, Esc. Durante la moviola la barca non si guida, il registratore di sessione e il pannello sono fermi, le scie sono nascoste. All'uscita le barche tornano esattamente com'erano.
- **Limiti dichiarati:** la forma della vela e i filetti sono quelli dell'ultimo istante (non registrati); la moviola vale per le regate (1a e 1b), non per le prove; gli spezzoni non si salvano nel file della sessione e spariscono a «Ricomincia» o a un'altra regata.
- **Misure** (`tests/collaudo_moviola.py`, nuovo, in `lancia_tutti.sh`): 12 regate del torneo col pilota, Chromium: posizioni riprodotte entro 0,019 m e 0,28° dalla simulazione (818 confronti; soglia 0,5 m e 5°); arrivi, penalità e posizioni finali **identici al bit** con e senza moviola; tempo di calcolo −0,7%; stato e scie identici dopo l'uscita; Firefox su 3 regate: 0,114 m e 0,17°, tutto OK. Schermata a 1360×650 senza barre di scorrimento.

## 1.0.57 — Tornei: la frase sulla finestra d'arrivo dice «non si classifica»

Osservazione 58 (prova a mano di Ale, 28 ottobre 2026): nella schermata dei Tornei la frase «chi non arriva entro metà del tempo della prima, dopo il suo arrivo, non arriva» si leggeva male, perché «non arriva» ripeteva la parola della condizione. Ora dice «contato dal suo arrivo, non si classifica» (la correzione era già decisa). Solo testo di `torBrief` in `js/regate.js`: la finestra (1,5 volte il tempo della prima, `TOR_FIN`) e i punti non cambiano. Nessun cambio al motore.

## 1.0.56 — Firefox: le impostazioni non si scambiano più dopo F5

Firefox, alla ricarica della pagina (F5), rimette caselle e menu come li aveva l'utente, mentre il gioco riparte con le sue impostazioni (`opt` in `js/gioco.js`, mai salvate): lo schermo poteva mostrare, per esempio, «semaforo» spuntato col semaforo spento. Trovato dal giro dei collaudi su Firefox (`collaudo_semaforo.py`: «il semaforo non è spento all'avvio»); su Chromium non succede. Ora ogni `<input>` e `<select>` di `index.html` ha `autocomplete="off"` (16 controlli, più la ricerca del glossario che l'aveva già). Il gioco non cambia in altro. **Misurato:** `collaudo_ricarica.py` (nuovo): su Firefox prima della correzione 0 controlli su 16 tornavano uguali a una pagina nuova, dopo 16 su 16; su Chromium 16 su 16.

**Collaudi su Firefox (giro `--veloce` di Ale sulla 1.0.55, 20 OK e 11 falliti):** sei collaudi si fermavano con «Navigation to "about:blank" is interrupted by another navigation» (`goto("about:blank")` non è accettato da Firefox): ora si scrive `location.href='about:blank'` e si aspetta (`boma2`, `salti2`, `timone2`, `strambata`, `schermate`, `vista`, `torneo`, `raddrizzata`, `registro`, `registratore`). Restano da guardare su Firefox: `collaudo_contatto_vero.py` (1a: penetrazione massima 0,29 m contro 0,25 attesi, su 6 corse; la regata diverge da quella di Chromium e ha 41 contatti invece di 22: una corsa sola sopra soglia, non toccata), `collaudo_partenze.py` (criterio 1, noto, e in più (1) con raffiche 10,0% contro 3,3%).

**Collaudi, dopo il giro del 27 ottobre (sera):** `collaudo_torneo.py` C11 falliva 7 controlli su Chromium e su Firefox (chiusura della pagina: regate registrate 0) perché la nuova `chiudi` della 1.0.56 non lasciava in Chromium il tempo di salvare; il gioco non c'entrava. Ora `chiudi` prova `goto("about:blank")` e, se il browser lo rifiuta (Firefox), naviga con `location.href` e aspetta 1,5 s (con 0,3 s Firefox salvava 2 chiusure su 4). C11 `--veloce`: Chromium R2 4/4, R3 8/8, R4 2/2, R5 2/2, OK; Firefox stesse cifre, OK. `collaudo_contatto_vero.py` su Firefox: nell'1a scafi sovrapposti 0,01 s a regata e penetrazione massima 0,29 m (soglia 0,25 m), 41 contatti e 78460 istanti con barche entro 5 m contro 22 e 29350 su Chromium (penetrazione 0,01 m, OK); 1b a posto su entrambi. Soglia non toccata, causa non cercata (ipotesi non provata: seno e coseno dei due browser fanno divergere le rotte).

## 1.0.55 — torneo dell'1b con percorsi misti: bastone, triangolo, bastone, triangolo

Tappa T2 del torneo (`docs/PROPOSTA-TORNEI-1B.md` §8, scelta di Ale del 27 ottobre 2026): le regate 1 e 3 restano a bastone (140 m), le regate 2 e 4 sono a **triangolo equilatero** di lato **140 m** con due boe da lasciare a sinistra (regola 27.1: il percorso lo sceglie il comitato). La «Regata a bastone» dell'1a e la «Regata nei salti di vento» non cambiano. Il percorso dipende solo dal numero della regata: nessun numero a caso in più.

**Cosa cambia in `js/regate.js`:** il percorso è una lista di boe (`R.marks`; `R.mark` resta la prima); i lati diventano 1 = verso la boa 1, 2 = verso la boa 2, 3 = verso l'arrivo (a bastone 1 e 2 come prima); al cambio di lato il giro riparte da zero (`rnd`, `rndA`, `rp`). Boa 2 in (−0,866·L, −0,5·L) in coordinate del vento, semiretta del giro a vento − 90°. Avversari: i tre punti di passaggio della boa 1 ruotati di 90° attorno alla boa 2. Strada per i distacchi: sul triangolo lungo il lato, ma nell'ultimo lato la strada che manca alla linea in direzione del vento portata a L (la proiezione sul lato arrivava a L fino a 8 s prima del traguardo: D1 sul triangolo 5 regate su 13, dopo la correzione 16 su 16). Disegno: due boe con «Boa 1 / Boa 2 · lasciala a sinistra» e un anello sulla boa da girare. Testi del torneo e dell'introduzione riscritti. `registratore.js`: il giro sbagliato vale per ogni boa. `avvio.js`: aggancio `__sv.triL` per la misura.

**Misurato:** L scelto con la regola scritta prima (la più piccola con la mediana del pilota fra 4 e 5,5 minuti): semi 1-20 L=140 4,03 min, 170 4,82, 200 5,42, 230 6,19; conferma sui semi 61-80 con L=140 4,16 min (L=170 4,74). Avversari: 160 barche su 160 arrivate a L=140 (semi 1-20 e 61-80), giri sbagliati 1 su 161 passaggi e 0 su 160 (0,6% e 0%). Non-regressione: `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; `arrivi_regate.py`: 20 regate e 9 introduzioni identiche al bit, regate 1 e 3 dei due tornei identiche (arrivi, penalità, punteggi), le regate 2 e 4 cambiano per costruzione.
**Altri collaudi:** `collaudo_triangolo.py` (nuovo, semi 1-20): T2h 16 casi su 16; D1 sul triangolo 16 su 16 (peggiore 1,8 s); T2e boe, anello e pannello 0 px; T2f «lato 2» e «lato 3» nel file e analizzatore senza errori. **Fuori soglia, riportato com'è:** T2b come scritto (distacchi a ogni boa entro 3 s, 100%): 129 su 168 (dopo il via 39/60, boa 1 60/60, boa 2 30/48; segno giusto 160/168; errore massimo 15,9 s); causa nota, la strada resta ferma tra l'abeam e la fine del giro (`docs/PROPOSTA-TORNEI-1B.md` §8.8). `collaudo_torneo.py`: tutto verde tranne R7 (uscita dal menu 2,71 s contro 2, limite noto tenuto da Ale); `collaudo_distacchi.py` OK (D1 conferma 94%, D2 303/303); `collaudo_versione.py` e `collaudo_pannello.py` (0 px). Da lanciare sul PC di Ale: `tests/lancia_tutti.sh --veloce`, `collaudo_impronta.py` (disegno) e la prova giocando.

## Pulizia di `js/regate.js` prima del T2 (27 ottobre 2026, senza nuova versione: resta la 1.0.54)

Il gioco non cambia. `js/regate.js` 69 310 → 70 312 byte (più righe, i commenti nuovi). Fatto: mappa aggiornata (intestazioni «sagoma degli scafi», «semaforo e contatti», «svolgimento: updateRace…», «distacchi e classifica», «aiuti a schermo e fantasma»); `cedeLv2` → `cedeAvv1b`; commento e ramo morto di `windOf` nell'avversario dell'1a; `latDi` e `piuSopravento` in `chiCede`; `muoviTimone` (la stessa legge del timone nella regata e nelle due simulazioni `startTime` e `glideY`), `cambiaBordo`, `sorteggiaAggressiva` e `carattere` (stesso ordine dei numeri a caso); `motivoContatto`, `introRegata`, `salvaArrivo`, `salvaPiazzamento`, `torTabella`, `drawOrologio`; `stepAI` a capo; `R.t < 0 || R.t < 3` → `R.t < 3`. **Misurato:** `tests/arrivi_regate.py` (nuovo: 20 regate e 2 tornei da 4, 112 barche, 109 penalità col motivo, 28 regate su 28 con almeno un contatto; arrivi, penalità, testi, classifiche e dati salvati) identico prima e dopo, e il riferimento è uguale in due giri; `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici; `collaudo_versione.py` e `collaudo_pannello.py` (eccesso 0 px). `collaudo_impronta.py` (disegno): da lanciare sul PC di Ale.

## 1.0.54 — classifica del pannello: distacchi in parole

- **Cosa è cambiato** (`docs/PROPOSTA-DISTACCHI-IMMEDIATI.md`, dal punto 7 del check di Ale; «facciamo le cose più semplici e che funzionino», 27 ottobre 2026): accanto a ogni barca il pannello dice «12 s avanti» o «12 s dietro» al posto di «+12 s» / «−12 s»; se il distacco arrotondato è zero dice «alla pari» (prima «0 s»). Il calcolo non cambia. Solo testo: tutte le regate, anche l'1a.
- **Un cambio non previsto, dichiarato:** nella riga della barca che naviga verso l'arrivo «in poppa verso l'arrivo» diventa «verso l'arrivo». Con «davanti» e il nome lungo la riga andava a capo (169 letture su 3108 con 42 px invece di 21, in barche con penalità); con il nome corto 7 letture; con anche «avanti» al posto di «davanti» 0 letture. Il testo vecchio non andava mai a capo. «Verso l'arrivo» è anche più giusto per il triangolo del T2, dove gli ultimi lati non saranno in poppa.
- **Misure** (`tests/collaudo_distacchi_testo.py`, nuovo; 18 regate guidate dal pilota, semi 1-6, e 3 tornei): **3108 righe con distacco confrontate**, tutte uguali all'atteso; 1284 righe senza distacco, nessuna con il testo del distacco; righe a capo 0. Le soglie D1-D4 della proposta sono quelle scritte prima; D3 è passato solo dopo i due cambi di testo qui sopra (prima 169, poi 7 letture a capo: nessuna soglia cambiata).
- **Non regressione:** motore e base non toccati; `polare.js` e `raffiche_e_virate.js` identici.
- **Non c'entra con la 1.0.54, ma trovato oggi:** `collaudo_competizione.py` C1 (il pilota arriva ultimo troppe volte) è verde alla 1.0.21, 1.0.29 e 1.0.38 (identico: 35% e 28%) ed è fuori da **1.0.42** in poi (41% e 41%, stessi numeri alla 1.0.42, 1.0.48 e 1.0.53). La 1.0.42 è la correzione degli scafi che non si compenetrano nemmeno nell'1a (richiesta di Ale). Il criterio misura il pilota di prova, non il gioco; soglia non toccata, resta fuori.

## 1.0.53 — il registro dice se la regata è dell'1a o dell'1b; casella del semaforo più chiara

- **Cosa è cambiato** (dal file di sessione di Ale del 26 ottobre 2026: semaforo acceso ma invisibile in una «Regata a bastone», che è dell'1a): (1) l'evento `apre` di una regata nel registro finisce con «(barca 1a)» o «(barca 1b)», e la legenda lo spiega; (2) la casella nelle impostazioni dice «Semaforo di precedenza sullo scafo (solo regate 1b)», con il dettaglio (salti di vento e torneo) nel suggerimento al passaggio del mouse. Il semaforo si vedeva già come previsto: nell'1a non compare.
- **Non cambiato:** motore, regole, disegno. Solo testo di una casella e una parola nel registro.

## 1.0.52 — il registratore di sessione registra tutte le barche

- **Cosa è cambiato** (`docs/PROPOSTA-REGISTRATORE-TUTTE-LE-BARCHE.md`, via di Ale del 26 ottobre 2026: tutte le regate, con «cede a…»; dal check di Ale sulla 1.0.47): con la registrazione accesa, in ogni regata (1a, 1b e torneo) il file ha, per ogni avversario, una riga `B` al secondo (nome, posizione, prua, nodi, angolo al vento, lato, stato: partenza anticipata, scuffiata, arrivata, non arrivata, in partenza, `cede:Nome`). Eventi nuovi: `avv_fermo` (sotto 0,5 nodi per 5 s di gioco dopo il via, con lato e posizione) e `avv_riparte` (sopra 1 nodo), `avv_lato`, `avv_arrivo`, `avv_ocs`, `avv_scuffia`, `avv_penalita`, `avv_boa_lato_sbagliato` (la stessa condizione che mostra «boa girata dal lato sbagliato» nel pannello) e `contatto_barche` per ogni contatto fra due barche qualsiasi, avversari compresi; righe `Q` col motivo di ogni penalità (la voce dell'elenco a fine regata). Formato 2; `tests/analizza_sessione.py` legge anche il formato 1 e per ogni avversario scrive righe, secondi fermo, contatti, penalità e secondi passati a cedere. Solo lettura (nessuna chiamata a `Math.random`, nessuna scrittura nello stato del gioco): `js/registratore.js` (nuova `sesAltre`), `analizza_sessione.py`, versione. Motore, barca e regate non toccati.
- **Misure** (`tests/collaudo_registratore_barche.py`, nuovo; 20 regate: 7 a bastone 1a, 7 nei salti di vento 1b, 6 del torneo, principianti ed esperti). **G1** stato finale identico al bit con e senza registrazione: 20 su 20. **G2** 27 423 righe `B` confrontate con i valori veri (posizione, prua, nodi, lato): 0 diverse; righe `B` = 3 × righe `S`. **G3** contatti registrati 82 = penalità assegnate 82 (conteggio indipendente: penalità e punti sommati sulle barche); costruiti a 1 m 10 su 10, a 12 m nessun evento 10 su 10. **G4** barche ferme registrate 11 = episodi veri 11 (contati qui dalle velocità vere, stessa isteresi); costruiti (barca tenuta a zero per 8 s e rilasciata) 10 su 10. **G5** `analizza_sessione.py` su tutti i 20 file: riassunto del gioco uguale a quello ricalcolato. **G7** pagina vera senza `#collaudo`, torneo dal menu: righe `B` di Blu, Rossa e Verde. Non regressione: `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` senza differenze; `collaudo_registratore.py` parti a, c ed e tutte OK.
- **G6 (dimensione): metro corretto, dichiarato.** Soglia: al massimo 20 kB per minuto. La prima versione del collaudo divideva per `R.t`, che non conta il conto alla rovescia (180 s) mentre le righe sì: su 2 regate di 6 dava 20,1 e 20,6 kB al minuto (fuori). Corretto il denominatore nei minuti davvero registrati: massimo **11,2 kB al minuto** su 20 regate. **Con il vecchio metro il massimo sarebbe 21,2 (fuori soglia)**; la soglia non è stata toccata, ma la stima della fermata 1 (9 kB al minuto) era troppo bassa: sono righe `B` di tre avversari più la `S`, i tasti e i suggerimenti.
- **Un caso del collaudo scartato e dichiarato:** un caso costruito su 10 (contatto a 1 m, caso 8) aveva già le due barche in contatto per conto loro: l'evento non poteva nascere. Il collaudo ora riconosce il caso e cambia seme (1 volta su 10).
- **Limite:** il registratore dice *cosa* fa una barca, non *perché*: i campi interni della guida (`goStart`, `waitX`…) non sono registrati, solo a chi cede. Se serve, secondo passo.

## 1.0.51 — classifica del pannello: le penalità si leggono

- **Cosa è cambiato** (proposta in chat, via di Ale del 26 ottobre 2026; dal check di Ale sulla 1.0.47, punto 7): accanto a ogni barca il pannello diceva «+30 s» (due penalità da 15, da indovinare) o «+2 pt». Ora dice «2 penalità (+30 s)» nelle regate normali e «2 penalità (+2 pt)» nel torneo. Una riga in `racePanel` (`js/regate.js`); il riepilogo di fine regata non cambia. Non toccato il secondo punto del check (i secondi di distacco «più immediati»): da proporre a parte.
- **Misure** (`tests/collaudo_penalita_testo.py`, nuovo): valori imposti 1, 2 e 3 in secondi e in punti, giusti; 36 regate guidate dal pilota (regate 0, 1, salti di vento, semi 1-12) e 6 del torneo: **102 barche con penalità vere lette, testo giusto in tutte, nessuna riga «penalità» senza penalità**. Pannello a 1360×650 con 3 penalità su ogni barca: eccesso 0 px (classifica e pagina). `collaudo_pannello.py` 0 px, `collaudo_riquadro_regata.py` 60 semi a 0 px, `collaudo_distacchi.py 1 4` OK.
- **Non regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` senza differenze (motore non toccato). **Limite del controllo:** il caso con penalità in secondi e in punti insieme sulla stessa barca (visto nelle misure) non esiste nel gioco, perché nel torneo le penalità sono solo in punti.

## 1.0.50 — torneo dell'1b: la regata lasciata a metà vale come ritiro

- **Cosa è cambiato** (`docs/PROPOSTA-RITIRO-A-META.md`, decisione di Ale del 26 ottobre 2026, via dello stesso giorno): nella regata del torneo, uscire dal menu o lasciare la pagina (chiusura, ricarica) dal clic su «Corri la regata» conta come «Ritirati dalla regata»: il giocatore prende 5 punti, gli avversari finiscono la regata in simulazione, il risultato si salva e il torneo va avanti. Prima la regata si rifaceva da capo, quindi una regata andata male si poteva ripetere. Dal menu c'è un avviso («Uscire dalla regata? Conta come ritirata»); alla chiusura della pagina nessun avviso. Chi ha già finito la regata, o l'ha già ritirata col pulsante, non cambia: nessun secondo risultato. Codice: `torEsci` e `torEsciOk` in `regate.js`, `showMenu` e il pulsante «Menu» in `gioco.js`, evento `pagehide` in `avvio.js`. Motore e barca non toccati.
- **Misure** (`collaudo_torneo.py`, nuovo C11; C3 non contiene più la chiusura a metà). 10 tornei: uscita dal menu a 1, 40, 150 e 300 s dal clic su «Corri» **40 su 40**; pagina lasciata negli stessi momenti **40 su 40**; torneo concluso dopo l'uscita **80 su 80**; uscita a metà della quarta regata **20 su 20**; nessun doppio risultato (regata ritirata o arrivata, poi uscita) **20 su 20**. **R7 FUORI soglia: uscita dal menu al massimo 2,51 s contro 2 s attesi** (soglia non toccata; è la simulazione degli avversari fino in fondo, nel caso peggiore a 1 s dal via; misurata nell'ambiente di Claude Code, sul PC di Ale può essere diversa).
- **Limiti dichiarati:** (1) se il browser viene ucciso senza `pagehide` (blocco del PC, batteria) l'uscita non si registra e la regata si ricorre da capo come prima; (2) il collaudo lascia la pagina con una navigazione (`about:blank`), perché in Chromium senza interfaccia `page.close()` da solo **non** fa partire `pagehide` (misurato): la chiusura vera della scheda nel browser di Ale non è provata qui; (3) nessun avviso del browser alla chiusura della scheda (Ale: va bene così, una riga in `avvio.js` se servisse).
- **Non regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` girano senza differenze (`motore.js` e `base.js` non toccati: `git diff` vuoto).

## 1.0.49 — avversari dell'1b: chi deve cedere cede, chi ha la precedenza tiene la rotta

- **Cosa è cambiato** (`docs/PROPOSTA-AVVERSARI-1B.md`, via di Ale del 26 ottobre 2026): nell'1b la guida degli avversari (e il pilota dei collaudi, che la usa) chiede a `chiCede` chi deve cedere, per la barca che si avvicinerà di più entro 15 s e a meno di due lunghezze: chi deve cedere poggia (mure diverse) o si scosta (stesse mure; se non può orzare, poggia), e continua finché non si allontanano; chi ha la precedenza tiene la rotta fino a 1,5 lunghezze. Mai dentro l'angolo morto. Prima del via e nell'1a la guida è quella di prima. Penalità visibili: messaggio quando si toccano due avversari (1b) ed elenco di tutte le penalità col motivo nella schermata finale (1a e 1b). Testo della regola 13 detto di un avversario: «finché non era» (diceva «eri»).
- **Misure** (`tests/misura_avversari.py`, nuovo, e `tests/collaudo_avversari1b.py`, nuovo; tabella completa nella proposta, §10). Semi 41-60 mai guardati, regata nei salti di vento, 120 barche: piantate avendo la precedenza 16 → 1, piantate 36 → 2, arrivo medio 405,4 → 407,9 s (ok); **penalità 73 → 97 (soglia 70, FUORI)**; boe sbagliate 1 → 1 (soglia 0, FUORI). Scenari: 4 su 5 a 10/10, **tre barche alla boa 7/10 (soglia 9, FUORI)**; lo scenario 2 non distingue (dichiarato).
- **1a identica:** regate 0 e 1, 80 corse carattere per carattere; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici. `collaudo_regole.py`, `collaudo_contatto_vero.py`, `collaudo_salti2.py`, `collaudo_torneo.py --veloce` OK; **`collaudo_semaforo.py` FALLITO** per 1 contatto su 37 (probabile fine di una virata in quell'istante, non verificato).

## 1.0.48 — zoom coi tasti 1 e 2, testi più corti

- **Dal check di Ale sulla 1.0.47** (`CHECK SCUOLA DI VELA.docx`, 26 ottobre 2026). Quattro cambi, nessuno nella fisica:
  - **Titolo nel pannello:** «Regata: Regata nei salti di vento» andava a capo (la correzione della 1.0.38 non bastava); ora «Regata: salti di vento» (campo `where` della regata in `js/regate.js`). Il nome nel menu e nel riquadro resta quello lungo. Misurato a 1360x650: altezza della riga 19 px (prima 38, cioè due righe).
  - **Lezione 3, «Le mure e le precedenze»:** «nelle regate di questo gioco 15 secondi» → «nelle regate di questo livello» (nell'1b arriveranno i giri di penalità).
  - **Sotto la bussola:** «Vento reale da N (000°), 10 nodi» → «da N (000°), 10 nodi».
  - **Zoom:** tasti 1 (avvicina) e 2 (allontana), vicini a Q; i pulsanti + e − sul mare non ci sono più (idea di Ale: prendere il mouse è scomodo). Resta la rotellina. In basso a destra sul mare la scritta «1 / 2 zoom»; «Q vista», quando non sta nel pannello, va sopra.
- **Collaudi cambiati:** `collaudo_vista.py` e `collaudo_schermate.py` usano i tasti al posto dei pulsanti; `collaudo_versione.py` cerca la riga del vento senza «Vento reale». `docs/MANUALE-bozza.md` aggiornato.
- **Misure:** `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici al giro di Ale del 24 ottobre carattere per carattere. `collaudo_versione.py`, `collaudo_vista.py` (161 casi, 0 sbagliati), `collaudo_schermate.py`, `collaudo_pannello.py 1360 650` (eccesso 0 px) OK. Sonda a parte: 14 volte il tasto 2 portano lo zoom da 1 a 0,1 (il minimo), 20 volte il tasto 1 a 3 (il massimo); nessun pulsante dello zoom nella pagina; nessun errore. L'impronta del gioco cambia (testi sul mare): Ale rigenera il riferimento.
- **Non fatto:** la regata lasciata a metà che vale come ritiro (tocca i salvataggi del torneo: prima la proposta).

## 1.0.47 — pulizia: la barca si chiama «1a» e «1b»

- **Pulizia dopo il congelamento della barca dell'1b** (`docs/PROPOSTA-PULIZIA-1B.md`, decisioni di Ale del 23 ottobre 2026). Il gioco fa le stesse cose; cambiano solo tre testi che il giocatore vede: nelle impostazioni «Barca: livello 1 / livello 2 (prova)» diventa «1a / 1b» (e il suggerimento «Livello 2, in prova: …» diventa «Barca dell'1b: …»); nel menu e nell'introduzione della «Regata nei salti di vento» «Barca del livello 2» diventa «Barca dell'1b». La barca non è più «in prova»: è congelata.
- **Solo commenti:** «livello 2» → «1b» e «livello 1» → «1a» nei commenti di `motore.js`, `gioco.js`, `regate.js`; intestazione della mappa «BARCA DELL'1B (nel codice lv 2; 1.0.24-1.0.46)». I nomi nel codice (`lv2`, `S.lv === 2`, `RUD2`, `BOMA2`, `SALTI2`, `RADD2`) restano: circa 100 punti, nessun guadagno per chi gioca. 77 rimandi ai documenti spostati in `docs/archivio/` corretti nei commenti di `js/` e `tests/`, 0 rimasti. «Brevetto di livello 1» ed «Esame · livello 1» non sono toccati: parlano del livello 1, non della barca.
- **`lancia_tutti.sh`:** entrano `collaudo_raddrizzata.py`, `collaudo_virate2.py` e `collaudo_distacchi.py`, solo fra i lunghi (il giro `--veloce` non si allunga). `collaudo_virate2.py` fallisce da sempre (avversari oltre la bolina + 15° nel 15-17% delle virate, soglia 5%): è scritto accanto.
- **Misure:** `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici alla 1.0.46 carattere per carattere. Impronta del gioco (riferimento della 1.0.46 del 23 ottobre, 67 scene): 64 identiche, 3 diverse (menu, «Regata nei salti di vento» con principianti ed esperti); dentro, **6 valori diversi su 5081, tutti i due testi nuovi**, nessuno stato di barca. L'impronta non vede la finestra delle impostazioni: misurata a parte a 1360×650 senza `#collaudo`, non scorre (prima e dopo 0 px) ed è più bassa, 524 px invece di 580, perché la scelta «Barca», più corta, sta sulla riga del vento. Verdi: `collaudo_versione.py`, `collaudo_pannello.py` 1360×650 (0 px), `collaudo_esame.py` e `collaudo_quiz.py` (0 px), `collaudo_timone2.py` e `collaudo_raddrizzata.py` (usano la scelta «Barca»). Codice 325 539 → 325 737 byte.

## 1.0.46 — la barca dell'1b orziera sbandando

- **Cosa è cambiato** (`docs/PROPOSTA-ORZIERA-1B.md`, scelta 1 di Ale): nella barca dell'1b, sbandando, la spinta della vela applicata al centro velico spostato sottovento fa girare la prua verso il vento: momento `spinta · zCE · sin(sbandamento)`, F4 eq. 6, diviso per `Izz` (`js/motore.js`, ramo `lv2`). Nullo a barca dritta, sbandata sopravento poggia. Nessuna costante nuova (`zCE` 2,0 m e `Izz` 200 già nel motore). Lasciato fuori, dichiarato: lo scafo sbandato che orza da solo (F4 senza numeri). Ricerca: Day 2017 e l'inferitura della vela dicono che `zCE` vero è probabilmente 2,5-2,8 m (effetto più debole del vero del 25-40%): passo separato, decide Ale.
- **Criteri** (`tests/fisica/orziera1b.js`, nuovo): (1) 1a identica: `polare.js`, `raffiche_e_virate.js`, `retromarcia.js`, `angolo_morto.js`, `bolina.js` carattere per carattere, **ok**. (2) Barra al centro a vento costante, prua che sale al massimo 1 °/s nei primi 10 s: 0,23-0,69 °/s, **FUORI con 14 nodi al traverso, 1,06 °/s** (senza il termine 0,33). (3) Raffica +60% con 10 nodi a barra al centro, almeno 5°: 12,9° di bolina, 16,4° al traverso, **ok**. (4) Raffica 14→22 nodi di bolina, il pilota tiene la prua: scotta ferma barra a fondo (35°, stallo 0,9 s, prua fuori 16°), lascando 3,7°, **ok**. (5) Virata dell'1b (`virata1b.js`): **FUORI a 16 nodi**, minima 34% contro 35% (era 36%); gli altri venti ok. (6) 80 regate del torneo col pilota (`misura_scarroccio.py` ora conta anche contatti e scuffie, semi 1-20): tempo medio pilota 204,0 → 204,8 s (+0,4%), avversari 197,5 → 197,8 s; boe sbagliate 3 → 1; **non arrivate 0 → 1** (il pilota dei collaudi, seme 14 regata 4: 3 scuffie e una boa sbagliata), quindi fuori come scritto; penalità per contatto 289 → 229; scuffie 71 → 73 (tutte del pilota).
- **Sensibilità** (`node orziera1b.js k`): con `zCE` 2,6 m (×1,3) o `Izz` 130 (×1,54) il criterio 2 al traverso con 14 nodi va a 1,23 e 1,35 °/s; con `Izz` 300 (×0,67) la raffica forte non porta più la barra a fondo (15°, criterio 4 fuori); con `zCE` 1,8 m tutto dentro.
- **Nel browser:** `collaudo_versione.py`, `collaudo_torneo.py --veloce` e `--giocatore`, `collaudo_contatto_vero.py`, `collaudo_raddrizzata.py`, `collaudo_salti2.py` OK; `collaudo_timone2.py` fallito una volta con 8 collaudi in parallelo (il solito fotogramma in più, barra 0,853) e OK da solo. **`collaudo_semaforo.py` FALLITO anche da solo:** 2 contraddizioni su 27 contatti, nessuna è un errore del gioco. (a) Tre barche ammassate: semaforo rosso verso la Verde, la più vicina, giusto; urto con la Blu, che doveva cedere, penalità alla Blu, giusto: il collaudo confronta anche quando le barche sono diverse. (b) Al passo prima dell'urto la Blu era a 8 mm dalla linea che decide chi è sopravento (regola 11) e l'ha passata nel passo: è un caso al confine come quelli che il collaudo esclude già sotto i 5 cm, ma per l'altro confine. Le traiettorie cambiano per la barca orziera, e questi casi prima non capitavano nei semi 1-8. **Collaudo corretto (decisione di Ale, dopo aver visto i due casi, quindi non alla cieca):** si confrontano solo i contatti con la barca su cui era calcolato il semaforo (gli altri si riportano a parte) e il margine di 5 cm vale anche per il confine della regola 11. Dopo: 1.0.46 OK (0 contraddizioni, 1 al confine, 1 con un'altra barca, 26 confrontati), 1.0.45 OK (23 confrontati); con i colori del semaforo invertiti apposta FALLITO con 25 contraddizioni: il metro misura.
- **Cambiano di poco:** `scarroccio1b.js` (VMG con 10 nodi 3,09 → 3,08), `timone2.js` (C3 0,31 → 0,30 rad/m, ora al bordo della fascia; C1 resta fuori), `salti2.js` (guadagno sui salti 9,8 → 9,4%, conferma 10,4 → 9,7%, nelle soglie), `boma2.js` (tutto ok).

## 1.0.45 — lo scarroccio dell'1b viene da deriva e pala

- **Cosa è cambiato** (`docs/PROPOSTA-SCARROCCIO-1B.md`, scelta 1 di Ale): nella barca dell'1b lo scarroccio si calcola come in Day 2017, eq. 11-12 (F17): deriva e pala sono due ali che reggono la spinta laterale, con le misure delle regole di classe (F37), barca dritta, scia della deriva sulla pala a zero. Costante nuova `DERIVA2` (`q` 873 = ½·ρ·K, `K` 1,70 m², dalle misure; `u0` 0,307 m/s, ipotesi: da ferma la barca scarroccia come nell'1a). La formula di prima (`foilK`, senza fonte) resta all'1a. Non è una taratura.
- **Scarroccio di bolina** (`tests/fisica/scarroccio1b.js`, nuovo; VMG sulla rotta vera): 2,3 / 2,4 / 3,2 / 2,9° con 5 / 6 / 10 / 15 nodi (prima 2,1 / 2,3 / 2,1 / 1,6°). **VMG** 1,83 / 2,13 / 3,09 / 3,84 nodi, da −0,5% a −3,0% (criterio 2: al massimo −4%, **ok**). Il banco ridà la riga «Day» della proposta al decimo e al centesimo (criterio 1, ok); la prima tabella della proposta comprendeva l'effetto dello sbandamento, che il modello lascia fuori come scritto: 0,1° di differenza. Con 10 nodi al traverso 1,0° (prima 0,5°), velocità al traverso 5,98 nodi (prima 6,01). Sensibilità col 470 misurato in vasca (F35, `node scarroccio1b.js 470`): 3,0-4,0°.
- **Il metro della bolina:** `bolina.js` e `PROPOSTA-BOLINA.md` calcolano la VMG con la sola prua, senza scarroccio: sulla rotta vera la VMG dell'1a è circa il 3% più bassa (2,16 / 3,18 / 3,96 invece di 2,25 / 3,29 / 4,07). L'1a è congelata: non cambia, è scritto nei documenti.
- **Regate dell'1b** (`tests/misura_scarroccio.py`, nuovo: 20 tornei col pilota, semi 1-20, 80 regate, 320 barche): tempo medio del pilota 202,5 → 204,0 s (+0,7%), degli avversari 195,6 → 197,5 s (+1,0%); non arrivate 2 → 0, boe sbagliate 4 → 3 (criterio 5, ok).
- **Collaudi di fisica:** `polare.js`, `raffiche_e_virate.js`, `retromarcia.js`, `angolo_morto.js` identici alla 1.0.44 carattere per carattere. `virata1b.js`: criterio 1 ok su tutti i venti (freccia 2,9 s e minima 50% con 10 nodi; 2,8 s e 36% con 16). `timone2.js`: C5 a 16 nodi 35% (era 34%, ora dentro), il resto come prima (C1 fuori, C4 fuori a 6 nodi). `salti2.js` tutto nelle soglie (guadagno sui salti 9,8%, conferma 10,4%). `boma2.js` tutto ok.
- **Nel browser:** `collaudo_versione.py`, `collaudo_torneo.py --veloce`, `collaudo_torneo.py --giocatore` (pagina senza `#collaudo`), `collaudo_semaforo.py`, `collaudo_contatto_vero.py` OK.

## 1.0.44 — la pala dell'1b frena come una pala della sua taglia

- **Ricontrollo di pala e deriva prima di congelare la barca** (richiesta di Ale, `docs/PROPOSTA-PALA-DERIVA-1B.md`), con le misure delle regole di classe di una deriva singola da 4,2 m (F37, usate con citazione per decisione di Ale) e il modello delle appendici di Day 2017 (F17). Confermati `TE` (0,80 contro circa 0,83 m) e `appDA` (0,0049 contro 0,0044-0,0048 m²); `yawG` 1,5 dentro la fascia fisica 1,1-4,0 (larga perché l'inerzia è una stima). **Lo scarroccio del gioco è circa la metà** di quello che danno deriva e pala (1,6-1,9° contro 2,4-4,1° di bolina): passo separato, deciso da Ale, con la sua fermata 1.
- **Cosa è cambiato:** `dragK` da 184 a **117** (solo barca dell'1b): la frenata della pala misurata in F4 sulla pala del 470 (0,169 m²) riportata alla pala di questa barca (0,107 m²). Non è una taratura.
- **Virata col gesto da tastiera** (`tests/fisica/virata1b.js`), sola freccia: 4,0 / 3,2 / 2,8 / 2,6 / 2,5 / 2,7 s con 6 / 8 / 10 / 12 / 14 / 16 nodi, minima 55 / 54 / 51 / 47 / 44 / **36%**: criterio 1 della 1.0.43 **ok su tutti i venti** (a 16 nodi era 34%). Numeri già visti nell'anteprima della proposta: non è una prova alla cieca. Sensibilità con tutta la pala in acqua (0,129 m², `dragK` 141): stessi tempi, minima uguale o 1 punto sotto.
- **Collaudi di fisica:** `polare.js`, `raffiche_e_virate.js`, `retromarcia.js`, `angolo_morto.js`, `boma2.js` identici alla 1.0.43. `salti2.js` **di nuovo tutto nelle soglie** (S1 taratura 4,5 → 8,8%, conferma 9,4%). `timone2.js`: C3 0,31 rad/m (fuori come nella 1.0.43), C4 fuori a 6 nodi (5,25 s), C5 a 16 nodi 34% (col suo gesto), C1 fuori come prima; giri di penalità 10 nodi 11,0 s con la freccia.
- **Nel browser:** `collaudo_salti2.py`, `collaudo_torneo.py --veloce`, `collaudo_semaforo.py`, `collaudo_contatto_vero.py`, `collaudo_regole.py`, `collaudo_raddrizzata.py`, `collaudo_versione.py` OK. `collaudo_timone2.py` OK da solo; con quattro collaudi in parallelo è fallito una volta su un tempo dei tasti (barra a 0,853 invece di 0,8 dopo 0,5 s con Maiusc: un fotogramma in più), come nella 1.0.43 per l'1a.

## 1.0.43 — virata dell'1b più agile

- **Richiesta di Ale** (23 ottobre 2026): la barca dell'1b è lenta in virata con la sola freccia. Prima di congelarla (servirà a 1b, 2a e 2b) e prima delle regole 15 e 16, che ora diventano la 1.0.44 (la loro finestra di tempo dipende dalla barca). Proposta, misure e strade in `docs/PROPOSTA-VIRATA-1B.md`; Ale ha scelto la strada A (solo fisica).
- **Cosa è cambiato:** nella barca dell'1b l'acqua frena meno lo scafo che ruota, `hullKq` da 600 a **400** (`js/motore.js`, solo il ramo dell'1b). Regola fissata prima: il valore più basso con la virata della sola freccia fra 2,5 e 3,5 s (F4 3,4 s, video 3,3 s), minima 35-60% e prua non oltre 60°, con 10 e 14 nodi; 300 dava 2,4 s con 14 nodi, più rapida delle fonti. `tests/fisica/virata1b.js` (`griglia` rifà la scelta).
- **Virata col gesto da tastiera** (barra al centro a 30° oltre il vento), sola freccia / Maiusc: 6 nodi 4,5 → **4,0 s** / 3,6 → 3,2 s; 10 nodi 3,2 → **2,9 s** / 2,5 → 2,3 s; 14 nodi 2,9 → **2,5 s** / 2,2 → 2,0 s. Velocità minima più alta (10 nodi: 44 → 49%). Prua dopo la virata 39-40° con la freccia, 43-46° con Maiusc (non va oltre). Barca lenta al traverso (1,5 nodi, 3 s di barra): 70 → 76° con la freccia, 85 → 94° con Maiusc. Giri di penalità più corti (10 nodi: 12,4 → 11,2 s freccia, 10,0 → 8,7 s Maiusc).
- **Conferma sui venti mai usati (6, 8, 12, 16): FUORI a 16 nodi**, minima 34% contro la soglia del 35% (prima 27%, già fuori). Gli altri tre venti nelle soglie.
- **Quello che non è cambiato, detto chiaro:** Maiusc in virata non frena più della freccia (§10 di `PROPOSTA-STALLO-TIMONE.md`): nel motore nessuna leva fisica provata lo fa frenare (girare in fretta costa sempre meno, perché la perdita nasce dal tempo con la prua al vento). Il peso del timoniere che aiuta a girare non c'è: l'agilità sta dentro il timone (semplificazione dichiarata).
- **Collaudi di fisica:** `polare.js`, `raffiche_e_virate.js`, `retromarcia.js`, `angolo_morto.js`, `boma2.js` identici carattere per carattere alla 1.0.42 (l'1a non cambia: `hullKq` è solo nel ramo dell'1b). Cambiano, come atteso: `timone2.js` (C3 curvatura media 0,29 → **0,31 rad/m, FUORI** contro 0,30 su tutti i venti; C4 rientra a 8 nodi, 4,31 s; resta fuori a 6 nodi, 5,39 s; C5 a 16 nodi 25 → 32%, ancora fuori; C1 fuori come prima); `salti2.js` **S1 FUORI sui semi di taratura** (guadagno virando sui salti 6,2 → 4,5%, soglia 5%), conferma 8,1 → 8,9% ok; `virate2.js` cambia di decimi di grado.
- **Nel browser:** `collaudo_timone2.py`, `collaudo_salti2.py`, `collaudo_torneo.py --veloce`, `collaudo_raddrizzata.py`, `collaudo_contatto_vero.py`, `collaudo_regole.py` OK. `collaudo_virate2.py` (non in `lancia_tutti.sh`): avversari oltre la bolina + 15° 17,1 → 15,9% sui semi di conferma (soglia 5%: fallito come prima). `collaudo_timone2.py` era fallito una volta con 9 collaudi in parallelo (barra dell'1a a 0,88 invece di 0,8 dopo 0,5 s: un fotogramma in più) e OK da solo.
- **`collaudo_semaforo.py`, difetto del collaudo trovato e corretto:** falliva «col semaforo spento l'immagine cambia», anche da solo. Causa: nel seme 3 esperti la foto cadeva durante lo scossone di un urto (`S.shake`), che sposta l'immagine a caso a ogni disegno: anche due foto di fila senza toccare niente erano diverse. Ora la foto si fa solo senza scossone; 12 controlli, 0 falliti, 29 contatti del giocatore, 0 contraddizioni.
- **Per le regole 15 e 16** (dopo la barca): finestra T rimisurata con la barca nuova, 5,2 s (semi 1-50), conferma 4,8 s (semi 51-100), uguale a prima. Soglia G della regola 16 da decidere con Ale (`PROPOSTA-REGOLE-PRECEDENZA-1B.md`, sezione «Regole 15 e 16»); strumenti `tests/fisica/finestra.js` e `tests/misura_finestra.py`.

## 1.0.42 — gli scafi non si compenetrano nemmeno nell'1a

- **Correzione di un difetto trovato giocando** (decisione di Ale, 23 ottobre 2026: «sì, correggilo anche nell'1a»): nell'1a, dopo un contatto, gli scafi restavano sovrapposti 2,8 s a regata (6 regate, penetrazione massima 1,37 m), come nell'1b prima della 1.0.41. Ora anche nell'1a, finché i contorni si toccano, si spingono fuori ad ogni passo; il contatto resta quello del cerchio di 4,2 m e la penalità è una sola. Dopo: **0,00 s a regata, penetrazione massima 0,01 m** (attese: al massimo 0,5 s e 0,25 m, scritte nel collaudo). **L'1a non è più identica al bit alla 1.0.41:** cambiano le traiettorie dopo i contatti (impronta delle scene di regata diversa, vedi sotto); la barca senza fiocco, `polare.js` e `raffiche_e_virate.js` non cambiano.
- **Impronta** (63 scene, confronto con una copia della 1.0.41): diverse solo le 4 scene di regata dell'1a (posizioni, passi, classifica, registro, testi); lezioni, prove e menu identici (59 scene su 63). Riferimento da rigenerare sul PC di Ale.
- **Verdi dopo la modifica:** `competizione --veloce`, `aggressiva`, `contatto_senza_colpa`, `regole`, `riquadro_regata`, `pannello`, `versione`, `semaforo`, `torneo`, `fantasma`, `contatto_vero` (23 controlli), `regate` bastone e raffiche (arrivi 18 su 18, nessuna BLOCCATA).
- **`collaudo_partenze.py`, da guardare (non l'ho cambiato né ho cambiato soglie):** sui semi 1-20 il criterio (1) «gli esperti hanno meno richiami dei principianti» è passato a FALLITO (esperti 4 su 60 = 6,7%, principianti 3 su 60 = 5,0%; prima 3 e 4). Sui semi 21-100 (mai guardati prima, 240 partenze per condizione) il criterio (1) era fallito nella 1.0.41 (principianti 4,6%, esperti 5,4%) e passa ora (5,4% e 4,2%): il verso si inverte, differenze di 1-3 partenze, quindi rumore e non un effetto sistematico. Il criterio (4) «partita entro 60 s» è fallito in tutte e due le versioni sui semi 21-100 (6 casi nella 1.0.41, 11 ora): i casi che ho guardato (seme 89, Blu) sono barche richiamate che stanno tornando dietro la linea, non bloccate; le traiettorie cambiano già durante il conto alla rovescia perché dopo un contatto le barche ora non si compenetrano. Da riguardare con Ale se vuole aggiornare i criteri. `collaudo_registro.py` è uscito una volta con 14 su 15 (lezione 1, «piantato», con 11 collaudi in parallelo) e 15 su 15 da solo: è il caso h già noto come non deterministico (`ROADMAP.md`).

## 1.0.41 — correzioni dopo il check visivo della 1.0.40

Dal check di Ale (23 ottobre 2026, sulla 1.0.40): «la cornice rossa o verde non è visibile come pensavo; a volte siamo entrambi io e l'avversario rossi; a volte vedo le barche sovrapporsi; l'omino ha il braccio che parte dal fianco e non dalla spalla».
- **Semaforo sugli avversari (difetto mio della 1.0.40).** Le altre barche vengono disegnate dalla stessa funzione del giocatore (`drawOther` scambia lo stato globale `S`), e la mia condizione controllava solo che il semaforo fosse acceso: il colore finiva su tutte e quattro le barche. Ora solo se `S` è la barca del giocatore. `collaudo_semaforo.py` aveva controllato solo il colore del giocatore e non vedeva la cosa: ora conta gli aloni disegnati per immagine (atteso 1, il giocatore). Contro-prova: con il difetto rimesso dà 4-5 aloni per immagine e il collaudo fallisce; con il codice corretto 1 per immagine, 16 immagini su 16.
- **Cornice più visibile:** alone largo e trasparente (0,5 m rosso, 0,36 m verde, trasparenza 30%) sotto la linea colorata (0,22 m rosso, 0,14 m verde, prima 0,12 e 0,08); rosso più spesso come secondo segnale. Guardato in screenshot a zoom normale: si vede.
- **Scafi sovrapposti dopo il contatto (nell'1b).** Misurato prima di cambiare (30 regate, semi 1-15): **9,0 s a regata con gli scafi sovrapposti, 236 s su 269 col giocatore, penetrazione massima 1,37 m**, 2,57 episodi a regata, circa 3,5 s ciascuno. Causa: il contatto dava una sola spinta all'istante dell'urto e poi la coppia restava «in contatto» (nessuna penalità nuova finché non si separano di 8 m) senza nessuna correzione: le barche continuavano a entrare l'una nell'altra. Ora, nell'1b, finché i contorni si sovrappongono si spingono fuori ad ogni passo (metà della penetrazione più 2 cm per barca); la penalità resta una sola. Dopo: **0,00 s a regata e 0,00 m di penetrazione** (6 regate, passi di 1/240 s; attese scritte prima: al massimo 0,5 s e 0,25 m). Nell'**1a** (congelata) il difetto resta: 2,8 s a regata con gli scafi sovrapposti dopo il contatto (6 regate, penetrazione massima 1,37 m); decide Ale se correggerlo.
- **Misure dopo** (regata dei salti di vento, semi 1-15, `tests/misura_regole.py`): 73 contatti, decisi dalla regola 10 in 37, dalla 11 in 20, dalla 12 in 3, dalla 13 in 13; colpevole diverso dalle regole di prima in 17 su 73; penalità per barca (giocatore, Rossa, Blu, Verde) prima 27, 20, 13, 13, ora 23, 22, 16, 12. Le traiettorie sono cambiate perché le barche non si compenetrano più: i numeri della 1.0.40 (41, 17, 5, 10) non sono confrontabili. Torneo col pilota (160 regate): 0,95 penalità a regata (era 0,83), piazzamento medio 2,7 (2,85). Verdi: `torneo`, `competizione --veloce`, `aggressiva`, `contatto_senza_colpa`, `registro`, `regole`, `riquadro_regata`, `pannello`, `versione`; `esplora --rigioca` 0 px su 95 e 100; impronta: stato delle barche, registro e testi identici alla 1.0.40, cambiano solo le immagini del mare per il disegno dell'omino (20 scene).
- **Omino:** due spalle ai lati della fine del busto (una dietro, per il braccio della barra; una davanti, per quello della scotta); ogni braccio ha un bordo scuro, perché prima si confondeva con il busto dello stesso colore e sembrava partire dal fianco. Solo disegno.

## 1.0.40 — chi cede: regole 10, 11, 12 e 13 nell'1b, e il semaforo sullo scafo

- **Una sola funzione decide chi cede:** `chiCede(A, B)` in `js/regate.js` ritorna la barca che cede e la regola. La usano la penalità, il testo di fine regata (ora con «regola N») e il semaforo: non possono contraddirsi. L'1a usa le due regole di sempre (mure opposte; stesse mure: la più sopravento in y), identica al bit (impronta delle 63 scene uguale alla 1.0.39, confronto con la cartella `fonts`).
- **Nell'1b valgono 10, 11, 12 e 13 di F15**, con le definizioni sui contorni degli scafi: «dietro» = tutto lo scafo dietro la linea al traverso dalla poppa dell'altra; **affiancate** = nessuna delle due dietro; **regola 11** = fra affiancate con le stesse mure cede quella sul lato delle mure dell'altra (sopravento); **regola 12** = non affiancate, cede quella dietro (prima la penalità andava alla barca davanti di bolina, 4 casi su 4 provati sbagliati); **regola 13** = chi sta virando (dalla prua nel vento fino a 42° dal vento vero, o dopo 10 s: ipotesi nostre) cede a tutte; se lo sono due, cede quella a sinistra dell'altra. Boma e vela non contano (limite dichiarato).
- **Introduzione delle regate dell'1b:** dice in due frasi chi cede (non c'è ancora una lezione dell'1b); la lezione 3 dell'1a non è toccata.
- **Semaforo di precedenza sul bordo dello scafo del giocatore**, impostazione «Semaforo di precedenza…» in ⚙, **spenta di default**, solo regate dell'1b: con un'altra barca entro 8 m che si avvicina (confronto ogni 0,5 s, almeno 0,1 m), resta 2 s dopo l'ultimo avvicinamento e sparisce oltre 10 m. **Rosso** (bordo 0,12 m) se secondo `chiCede` devi cedere, **verde** (0,08 m) se cede l'altra; il verde dice «hai la precedenza», non «puoi urtare». Giallo e regole 15-18 non ci sono ancora (1.0.41 e 1.0.42). Con l'impostazione spenta l'immagine del mare è identica a quella senza colore (16 immagini su 16).
- **Misure** (regata dei salti di vento, semi 1-15, principianti ed esperti, 30 corse, `tests/misura_regole.py`): 73 contatti (2,43 a regata, come nella 1.0.39), decisi dalla regola 10 in 41, dalla 11 in 17, dalla 12 in 5, dalla 13 in 10. **Il colpevole cambia rispetto alle regole di prima in 14 contatti su 73 (19%)**: 7 per la definizione di affiancate (11), 4 per la 12, 3 per la 13. Penalità per barca (giocatore, Rossa, Blu, Verde): prima 28, 17, 17, 11; ora 22, 18, 21, 12. Torneo col pilota (40 tornei, 160 regate): 0,83 penalità del pilota a regata (133), contro 0,99 nella 1.0.39; piazzamento medio 2,85 (era 2,9). Gli avversari **non** conoscono ancora le nuove regole (guida invariata): prendono penalità per cose che non sanno di dover rispettare; il lavoro «avversari che usano `chiCede`» viene dopo la 1.0.42.
- **Coerenza del semaforo** (`collaudo_semaforo.py`, 16 regate, 26 contatti del giocatore, tutti con il semaforo visibile): 0 contraddizioni fra il colore un passo prima e la penalità. Un contatto (seme 7 esperti, prima del via, Rossa) aveva il colore diverso: al passo prima la geometria dietro/affiancate era a 1,2 cm dal confine e nel passo la regola è cambiata. **La soglia «5 cm dal confine» per non contarlo l'ho aggiunta dopo aver visto quel caso**; è riportato a parte («più 1 con la regola al confine»).
- **Finestra delle impostazioni:** la riga nuova del semaforo la faceva scorrere di 37 px a 1360×650 (era 0): ho accorciato la sua etichetta (la spiegazione sta nel suggerimento al passaggio del mouse) e l'etichetta «Nel pannello, anche fuori dalle lezioni, i numeri…» che andava a capo, ora «Numeri di vento, sbandamento e scarroccio nel pannello, sempre»: la finestra è alta 580 px e non scorre.
- **Collaudi nuovi** `tests/collaudo_regole.py` (24 casi a mano dal regolamento per le regole 10-13, confini a 0,2 m, virata a 41° e 43°, scadenza dei 10 s, e 3 casi dell'1a: 35 controlli, 0 falliti; un primo giro aveva 1 fallito per un mio errore nella prova della scadenza: la barca guidata dall'IA incrociava di nuovo il vento) e `tests/collaudo_semaforo.py`. Verdi dopo la modifica: `collaudo_contatto_vero.py`, `torneo`, `competizione --veloce`, `aggressiva`, `contatto_senza_colpa`, `registro`, `riquadro_regata`, `pannello` (0 px).

## 1.0.39 — contatto vero fra gli scafi nell'1b

- **Nell'1b (regata dei salti di vento e torneo) il contatto scatta quando i contorni degli scafi si sovrappongono**, non più quando i centri sono a meno di 4,2 m. Contorno: poligono di 24 punti dagli stessi punti di `hullPath`, controllo con gli assi separatori; la penetrazione dà anche la spinta di separazione (metà penetrazione più 0,15 m per barca, cioè 0,3 m fra gli scafi). Colpa, penalità, velocità ×0,6 e «stesso contatto finché si separano di 8 m» non cambiano. Solo lo scafo: boma e vela non toccano (limite dichiarato, decisione di Ale). L'1a resta con il cerchio di 4,2 m (distanza di sicurezza dichiarata), identica al bit: l'impronta delle 63 scene è uguale alla 1.0.38 (confronto su una copia della 1.0.38 con i caratteri; un primo confronto senza la cartella `fonts` dava 21 immagini diverse per il solo testo disegnato).
- Frase nell'introduzione delle regate dell'1b: «Da questo livello i contatti sono quelli veri, scafo contro scafo. Prima avevi imparato a stare lontano perché il contatto scattava prima del contatto vero.»
- Misura prima (1.0.38, semi 1-15, 90 regate, `tests/misura_contatti.py`): 4,2-4,8 contatti a regata, con in mediana 1,5-1,6 m d'acqua fra gli scafi al contatto; in un mondo senza regola di contatto gli scafi si sovrappongono davvero 2,6 volte a regata nei salti di vento.
- **Difetto trovato dal collaudo nuovo, prima di chiudere:** il contorno ha l'ultimo punto uguale al primo, quindi un lato di lunghezza zero senza asse: nella prima scrittura il test di sovrapposizione non trovava mai niente nell'1b (11 902 istanti con scafi sovrapposti e 0 contatti). Lati di lunghezza zero ora saltati.
- **Dopo** (stesse 30 regate dei salti di vento, semi 1-15): 2,43 contatti a regata (73, in 28 corse su 30; prima 4,6), con in mediana 0,01 m fra gli scafi al contatto (massimo 0,04 m al passo di 1/60 s). Torneo col pilota (40 tornei, 160 regate): 0,99 penalità del pilota a regata (159), prima 1,7 (265 in 160); piazzamento medio del pilota 2,9.
- Verdi dopo la modifica: `collaudo_torneo.py`, `collaudo_competizione.py --veloce`, `collaudo_registro.py` (15 su 15), `collaudo_riquadro_regata.py`, `collaudo_pannello.py` (0 px), `collaudo_aggressiva.py` e `collaudo_contatto_senza_colpa.py` (30 contatti su 30).
- Nuovo `tests/collaudo_contatto_vero.py`: 8 coppie a mano (l'1a usa il cerchio, l'1b lo scafo, ognuna con il contatto atteso nei due livelli) e regate intere con passi di 1/240 s.

## 1.0.38 — vento e bussola insieme, suggerimento del lasco più onesto, titolo della regata a salti più corto

- **Vento e bussola nello stesso angolo (in alto a destra).** La riga «Vento reale da … nodi» passa sotto la bussola, dove stava la versione; la versione sul mare non c'è più (resta nel menu e nel registratore). L'angolo in alto a sinistra è libero. `collaudo_versione.py` ora controlla che sul mare ci sia il vento e non la versione.
- **Suggerimento delle vele (e dei filetti in navigazione libera).** Misurato con il motore a 6, 10 e 15 nodi, da 90° a 150°: il massimo di velocità sta a circa 20° di incidenza della vela, ma la banda dei filetti «dritti» va da 8° a 27°, e dentro la banda la velocità cala fino al 10-25% (a 15 nodi e 110°, 34% fra un bordo e l'altro). Prima il pannello dava verde a vela tutta aperta e rosso «troppo cazzata» dove cazzare un po' faceva guadagnare velocità. Ora: verde solo fra 17° e 25° di incidenza; sotto 17° «regolata, ma cazzando un po' vai più veloce»; sopra 25° «lascando un po' vai più veloce» (o «vela tutta aperta: più di così non si può» se la scotta è già al massimo); rosso solo oltre 30°. I filetti sul mare e la fisica non cambiano. Misura (free, 6/10/15 nodi, 90-140° ogni 5°, scotta da 0 a 1 ogni 0,1, 362 stati con sbandamento ≤ 25°; il numero cambia di 1 da una corsa all'altra): rossi «troppo cazzata» 190, di cui **2 sbagliati** (6 nodi, 135°: il massimo sta a una scotta più cazzata, +3% o più); verdi «regolata» 33, di cui **0 sbagliati** (nessuno con una scotta diversa oltre il +10%). Un primo giro con i bordi a 15° e 27° dava 4 verdi sbagliati su 44: i bordi sono stati stretti dopo aver visto quei numeri, non prima.
- **Pannello che sfora di 17 px a regata non finita** (seme 256, salti di vento, giocatore scuffiato): il titolo «Regata nei salti di vento (livello 2, prova)» andava a capo, e così barra e titolo erano più alti di 20 px. Ora «Regata nei salti di vento» (la descrizione dice già che è la barca del livello 2). `esplora.py --rigioca`: 0 px su 95 + 100 casi.
- Impronta: stato delle barche, barra e scotta identici alla 1.0.37; cambiano solo i testi del suggerimento, le immagini del mare (21, il vento) e due titoli del menu.
- **Collaudo corretto:** `collaudo_carriera.py` K5 confronta il menu con quello della 1.0.1 e non conosceva il titolo nuovo della lezione 3 (1.0.37): era fallito senza che nessuno lo vedesse; aggiornato, 57 controlli, 0 falliti.

## 1.0.37 — lezione 3: filetti con margine, mure e precedenze; il timoniere ha due braccia

- **Filetti (lezione 3, passi 8-10).** Il passo dopo poteva chiudersi da solo: la vela lascata piano si ferma sul confine dei filetti (8° di incidenza; misurato: a scotta ferma l'incidenza tende a 8,0°), il filetto torna dritto e «filetti dritti» trova la condizione già vera. Ora i passi chiedono 2° di margine (sopravento sotto 6°, dritti fra 10° e 25°, sottovento sopra 29°); i filetti sul mare e la fisica non cambiano. `readI()` espone `alpha`. Misura: 30 tentativi a velocità di lasco diverse, passo 8 chiuso 29 su 30 (1 no: lasco troppo lento per scendere sotto 6° in 60 s, limite del mio test) e il passo 9 mai chiuso da solo (0 su 29). Non sono riuscito a riprodurre il difetto con la condizione vecchia (0 su 30): la prova mostra il meccanismo (l'incidenza si ferma a 8,0° dopo 20 s) ma non lo fa scattare; il margine resta per come la causa è letta nel codice. `collaudo_pilota_lezioni.py`: passi 3.8-3.10 guidando 20 su 20, «dopo un colpo lungo» 0 su 20.
- **Lezione 3: «Andature, mure e precedenze».** Titolo della lezione e del passo («Le mure e le precedenze»); il passo spiega le due regole che il gioco applica (mure diverse: cede quella mure a sinistra; stesse mure e barche affiancate: cede la sopravento, regole 10 e 11 di F15, lette sul testo) e la penalità (15 s nel gioco, due giri in mare, regola 44.1). Voce «Mure» del glossario completata. Rinominati i riferimenti nei collaudi (`collaudo_libretto.py`, `collaudo_carriera_esame.py`) e nella banca delle domande.
- **Timoniere con due braccia:** il secondo, dalla spalla davanti verso la scotta; solo disegno, posizione da giudicare giocando.
- Impronta: stato delle barche e registro identici alla 1.0.36 (misurato su una copia della 1.0.36); cambiano solo i testi (lezione 3, glossario, menu) e le immagini del mare (21, il braccio). Riferimento rigenerato sulla 1.0.37. Il vecchio riferimento (1.0.35) differiva già nell'ultima cifra dei decimali.

## 1.0.36 — schermata finale di regata fuori dal pannello

- A regata finita (arrivo, ritiro, torneo) il riepilogo e la classifica passano dal pannello a un riquadro sopra il mare, con Ricomincia, Cambia vento e (nel torneo) Classifica del torneo; il primo pulsante ha il fuoco, quindi Invio ricomincia. Restano finché non si sceglie.
- Causa: `status` (una riga per barca) e `rDone` (riepilogo) facevano scorrere il pannello a 1360×650. I riquadri restano compilati (i collaudi li leggono), solo nascosti con la classe `fin`.
- Misurato con `esplora.py --rigioca` (95 regate che sforavano + 100 di controllo): 94 su 95 ora a 0 px, controllo 0 su 100 che sfora. **Resta 1 caso su 95 (seme 256, salti di vento, 17 px)**: giocatore scuffiato a regata non finita, quindi non è la schermata finale; da guardare a parte.
- Barca invariata: `polare.js` e `raffiche_e_virate.js` usano `tests/fisica/motore.js`, non toccato.

## 1.0.35 — il menu torna a stare in 1360×650

Del 20 ottobre 2026, dal giro `lancia_tutti.sh --veloce` di Ale sulla 1.0.34 (20 OK, 3 falliti). **Solo il menu cambia.**

- Il riquadro del torneo, in «Regate», allungava il menu del gioco libero di 29 px a 1360×650: la pagina scorreva, anche dietro quiz ed esame (`collaudo_esame.py`, `collaudo_quiz.py`, `collaudo_salti2.py` falliti). Il riquadro più alto passava da 464 a 536 px. Non l'avevo visto perché nella 1.0.34 avevo lanciato solo i collaudi del menu della carriera (dove ci stava) e del pannello.
- Ora nel gioco libero il torneo sta nel terzo riquadro, in una sezione «Tornei» sopra «In arrivo»; in carriera resta in «Regate». Il pulsante non ha più la descrizione (la dà il riquadro che si apre). Altezze: pagina 650 px in tutti e due i modi, riquadro più alto 448 px nel gioco libero (limite di `collaudo_esame.py`: 464).
- `collaudo_carriera.py` K5: la regola che toglie il riquadro della regata nei salti ammette una riga vuota prima della descrizione (cambiava con l'impaginazione).
- Rilanciati: esame, quiz, salti2, carriera, libretto, torneo (veloce e giocatore) tutti OK; impronta: cambia solo il menu, riferimento rigenerato.

## 1.0.34 — torneo dell'1b, prima tappa (T1)

Del 20 ottobre 2026, dalla fermata 1 di `docs/PROPOSTA-TORNEI-1B.md` con le decisioni di Ale. **La fisica non cambia; le regate dell'1a, le lezioni e le prove sono identiche al bit** (impronta: cambia solo il menu).

- **Torneo dell'1b** nel riquadro «Regate» del menu: 4 regate a bastone con la barca completa dell'1b, contro gli stessi tre avversari (stesso livello e stesso carattere per tutta la serie). Vento: 10 nodi costanti, raffiche, salti di vento, e la quarta sorteggiata fra le tre; direzione a caso, fissata all'inizio del torneo.
- **Punteggio del regolamento** (F15, appendice A): 1 punto al primo, 2 al secondo e così via; chi non arriva o si ritira prende 5 (iscritti + 1); dopo la quarta regata si scarta la peggiore (a parità, la più vecchia); parità della serie con A8.1 e A8.2. Tabella della serie fra una regata e l'altra.
- **Penalità sul punteggio** (regola 44.3, decisione di Ale): nel torneo un contatto con colpa vale +1 punto nella regata (20% di 5), mai oltre 5, invece dei 15 s. Le altre regate restano con i 15 s.
- **Finestra d'arrivo** (appendice S del regolamento, 12.3): chi non arriva entro una volta e mezza il tempo della prima non arriva. Il 50% è un'ipotesi nostra: il regolamento lascia il valore alle istruzioni di regata. Serve anche a chiudere la regata: finito il giocatore, le barche ancora in acqua arrivano in una simulazione accelerata quando si apre la classifica.
- **Salvataggio**: il torneo si salva dopo ogni regata (`progress.torneo`); chiudendo la pagina o tornando al menu a metà regata, quella regata si ricorre da capo (si può quindi ripetere una regata andata male: limite dichiarato). Se cambia la versione del gioco, il torneo in corso si chiude senza punti. Nel torneo non ci sono «Ricomincia» e «Cambia vento»; ci sono «Ritirati dalla regata» (5 punti) e, nel riquadro, «Ritirati dal torneo» (il torneo non conta: niente punti, niente piazzamento).
- **Meriti di Competizione dell'1b** (solo carriera, tabella provvisoria di `VISIONE` §6): 1° = 6, 2° = 4, 3° = 3, 4° = 2, più 1 senza penalità nel torneo; si salva il migliore. In carriera il torneo si apre dopo il brevetto di livello 1; nel gioco libero c'è sempre e non dà meriti.
- **Raffiche attorno a tutte le barche** (primo rischio di §6 della proposta), solo nel torneo: prima nascevano solo sopravento al giocatore. E nelle regate dell'1b le mure di un contatto si giudicano col vento nel punto di ciascuna barca (prima col vento del giocatore, difetto noto dalla 1.0.1, che nell'1a resta).
- Pannello: finita la regata del torneo, il suggerimento si nasconde e il risultato non ripete errori e distacchi, che stanno già nelle righe sopra; «Classifica del torneo» prende il posto di «Ritirati dalla regata».
- Nuovo `tests/collaudo_torneo.py`; `collaudo_carriera.py` K5 sa del riquadro nuovo del menu.
- **Misure** (`collaudo_torneo.py`, tutti i criteri nelle soglie): punteggio 0 errori su 15 casi scritti a mano; 40 tornei col pilota (160 regate concluse su 160), classifica del gioco uguale a quella ricalcolata dal collaudo in tutte; ripresa dopo la pagina chiusa 30 casi su 30; ritiro 10 su 10 senza tracce; pannello e classifica a 1360×650 nel caso peggiore 0 px. Raffiche: tempo passato in raffica dagli avversari pari al 92% di quello del giocatore (nell'1a 67%). Prova da giocatore senza `#collaudo`: torneo intero, nessun errore.
- **Da sapere:** il pilota prende in media 1,7 penalità per regata (265 in 160), circa tre su quattro prima del via, quasi come nella regata a bastone dell'1a (33 in 20 contro 39 in 20 nel torneo). Con +1 punto l'una pesano molto: spesso arriva a 5 punti anche arrivando. Gli avversari dell'1b sono ancora quelli di oggi (prossimo lavoro 3 di `STATO.md`).

## 1.0.33 — distacchi in secondi nella classifica delle regate

Del 19 ottobre 2026, richiesta di Ale (`docs/PROPOSTA-DISTACCHI.md`). Tutte le regate; fisica e arrivi identici.

- Nella classifica del pannello, accanto a ogni barca, i secondi da te: positivi se è davanti, negativi se è dietro. Sono un tempo vero: quanti secondi fa quella barca era alla tua altezza (strada fatta nella direzione del vento, senza le penalità). Dopo il tuo arrivo, le differenze dei tempi d'arrivo.
- All'arrivo il risultato dice anche i secondi dalla barca davanti e dalla prima: «3° su 4 in 4 min 34 s, a 57 s dalla Rossa, a 74 s dalla Blu (prima)».
- Prima idea: due righe sul mare sotto «Vento reale»; spostate nella classifica su proposta di Ale (tutte le barche, nessuna riga nuova).
- **Misure** (360 regate col pilota): il distacco mostrato 5 s prima dell'arrivo è entro 3 s da quello vero in 193 casi su 200 (soglia 90%); il primo metro (distanza in linea d'aria) ne dava il 68% e l'ho cambiato, dichiarato. Pannello nel caso peggiore: 0 px di eccesso. Nuovo `tests/collaudo_distacchi.py`.

## 1.0.32 — livello 2: raddrizzata più lunga, al traverso

Del 19 ottobre 2026, dal video di un allenatore portato da Ale (`docs/PROPOSTA-RADDRIZZATA.md`). **Solo la barca del livello 2; il livello 1 è identico al bit.**

- Premuto A, la barca si tira su in **10 s** (prima 3) e torna dritta **al traverso** (prima 60° dal vento), ferma, con la **vela tutta lascata** che sbatte: si cazza e si riparte. Gli avversari del livello 2 restano rovesciati 15 s (prima 5) e ripartono al traverso del vento vero.
- Fonte: un video divulgativo (raddrizzare con la schiena al vento, vela che sbatte libera, 15-20 s in tutto); il traverso è letto dagli schemi. Da confermare con altre fonti.
- Misure: 8 casi su 8 a 90° e senza riscuffiare; ripartenza a 2 nodi in 1,3-3,5 s con 6-15 nodi. Con 20 nodi la barca non riparte in 30 s, come già nel livello 1 (da guardare a parte).
- Nuovo `tests/collaudo_raddrizzata.py`. Una lezione breve del livello 2 lo spiegherà (da scrivere).

## 1.0.31 — livello 2: la prua non va più oltre la bolina dopo la virata

Del 19 ottobre 2026, dalle registrazioni di Ale del 18 ottobre. Proposta, revisione in chat e misure in `docs/PROPOSTA-VIRATE-AVVERSARI.md`. **Il livello 1 è identico al bit.**

- **Il difetto:** nella barca del livello 2, dopo la virata, la prua girava ancora di 20-45° con la barra al centro (14 virate su 21 di Ale oltre 65° dal vento, 4 in poppa) e gli avversari arrivavano a 97-111° dal vento in quasi ogni virata (97% nel browser). Causa: la rotazione la frenava solo la pala, che a fine virata va piano e stalla.
- `js/motore.js`, solo il ramo del livello 2: la pala sente anche l'acqua che le arriva di lato perché la poppa ruota (V² = u² + (r·xR)², idea della revisione in chat), e l'acqua frena lo scafo che ruota (`hullKq` 600, `Izz` 200: stime, non tarate); `yawG` da 0,6 a 1,5 con la regola di scelta della 1.0.24.
- **Misure:** prua massima del giocatore 67-81° → 34-40°; rotazione ferma in 0,6-0,8 s; avversari nel browser oltre la bolina + 15° dal 97,1% al 17,1% delle virate (conferma, semi 21-60; soglia 5%: fuori), mediana da +58,9° a +0,3°; curvatura delle virate dentro la fonte per la prima volta (0,29 rad/m).
- **Provata da Ale e tenuta** (registrazione del 19 ottobre: dopo aver centrato la barra la prua va oltre di 5° al più). **Prezzo dichiarato:** la pala quasi non stalla più nelle virate e Maiusc non costa più velocità (C1 fuori; `collaudo_timone2.py` ora crea lo stallo apposta, con la barca lenta e la barra a fondo di colpo); virate più lente con 6 e 8 nodi (C4 fuori), giri di penalità più lunghi del 30% circa.
- **Collaudi:** nuovi `tests/fisica/virate2.js` e `tests/collaudo_virate2.py`. Corretto il pilota di prova di `salti_bolina.js` (virava quasi da fermo vicino alla boa e restava piantato) e `salti2.js` ora vuole tutte le bolinate arrivate: prima passava contandone 23 su 40. Riferimento dell'impronta rigenerato sulla 1.0.30 (quello della 1.0.27 falliva anche senza modifiche).

## 1.0.30 — omino con due gambe, banderuola, W e S sempre attivi

Del 19 ottobre 2026. Dal giudizio di Ale giocando (registrazioni del 18 ottobre). **Fisica identica**: cambiano disegno e tastiera.

- `js/disegno.js`: il timoniere ha due gambe (prima una linea sola), con i piedi uno avanti all'altro nel pozzetto. La banderuola in testa d'albero ha il perno a 0,4 della lunghezza dalla punta (era 0,3), cioè più al centro.
- `js/gioco.js`: **W e S valgono sempre come ↑ e ↓** (cazza e lasca la randa), in navigazione libera, prove e regate. Nessuna scritta del gioco cambia: i tasti restano indicati solo nel manuale e nella lezione 1, dove i pulsanti W e S funzionano come prima. Nella registrazione compaiono come ↑ e ↓.
- Rimandati (da proporre): posizione della barca dopo la raddrizzata e tempo per girare; avversari e virate (dopo la virata l'angolo al vento arriva a 65-92° in 14 virate su 21, in 4 a 147-180°); distacchi in regata; cosa influenza l'abilità.

## 1.0.29 — pulizia: solo commenti e collaudi

Del 17 ottobre 2026. **Il gioco non cambia**: in `js/` cambiano solo commenti e la costante `VERSIONE`.

- `js/motore.js`: intestazione «BARCA DEL LIVELLO 2» che elenca dove stanno i controlli `S.lv === 2` (motore, gioco, regate, disegno) e come trovarli con `grep`; `js/regate.js`: commento su `RACES1` (cosa conta per carriera e meriti). Nessuna logica spostata: le costanti del livello 2 stavano già insieme in `motore.js`.
- `tests/collaudo_carriera.py`, K5: il riquadro «Regata nei salti di vento» del menu (voluto dalla 1.0.28) non è più un fallimento. Era l'unico fallito dell'ultimo giro `--veloce --parallelo 3`; il gioco era a posto, il collaudo era rimasto indietro.
- Controllati i promemoria: i commenti di `timone2.js` e `collaudo_timone2.py` non parlano più di barra lenta a 20°/s (già a posto dalla 1.0.25); le due funzioni `bolina()` di `timone2.js` e `salti_bolina.js` fanno cose diverse e restano separate.
- **Dimensione del codice:** 292 864 byte alla 1.0.28 (`index.html` 34 849, `js/` 258 015).

## 1.0.28 — livello 2 in prova: i salti di vento

Del 17 ottobre 2026. Proposta, fonti, misure e storia del modello in `docs/PROPOSTA-SALTI-VENTO.md`.

- **Fonti** (divulgative, coerenti): in regata il vento oscilla di circa 10-20° ogni 3,5-8 minuti; si vira sugli scarsi; sotto i 2 minuti di periodo non conviene; se il ciclo è più lungo della bolina il salto è persistente e si va verso la parte da cui ruota il vento.
- **Misura che ha deciso la proposta:** con la bolina di oggi (140 m, circa 90 s) virare sui salti dà al più il 2-4%; con una bolina di 300 m e salti di ±15° ogni 2-3 minuti il 10-12%.
- **Nel gioco, solo per la barca del livello 2:** vento che oscilla attorno al medio, uguale in tutto il campo, con ampiezza (12-15°) e periodo (2-2,5 minuti) propri di ogni regata e mezze oscillazioni diverse del ±10%; una regata su tre con salto persistente (10-20° per bolina, fino a 25°), che comincia al via. Generatore puro in `js/motore.js` (`SALTI2`, `newShift`, `stepShift`).
- **Regata nuova «Regata nei salti di vento (livello 2, prova)»**: barca del livello 2 per tutti, boa a 300 m, linea perpendicolare al vento medio. Solo nel gioco libero: fuori da meriti, libretto e carriera. Nella navigazione libera con la barca del livello 2 il vento oscilla.
- **Misure** (`tests/fisica/salti2.js`, bolina di 300 m col pilota): virare sugli scarsi guadagna il 7,0% sui semi di taratura (vince 31 su 40) e il **5,7%** su quelli di conferma mai guardati (28 su 40); col salto persistente partire verso la rotazione è meglio 40 volte su 40 in tutti e due i gruppi.
- **Il modello è cambiato due volte prima della conferma, dichiarato:** con oscillazioni del tutto irregolari (ampiezza 8-15° e durata nuove a ogni mezza oscillazione) virare sugli scarsi **perdeva** (−8,9% e −2,6%); con oscillazioni regolari per regata ma mezze di 75-90 s guadagnava il 3,8-3,9%, sotto la soglia del 5%. Scelte mezze di 60-75 s (dentro la fascia della proposta) sui semi 1-40 e confermate sui semi 121-160 mai usati.
- **Collaudo nuovo `collaudo_salti2.py`**: 12 regate col pilota, tutte le barche arrivano; libera del livello 1 senza salti; menu. Prove in più: 40 regate con principianti e 40 con esperti, tutte le barche arrivate. **Due difetti trovati e corretti** (solo nella regata del livello 2): il salto persistente cominciava prima del via e una barca non riusciva più a partire; col vento girato una barca passata fuori dall'estremo non rientrava più (ora, dopo il via, fuori dagli estremi usa la guida normale).
- **Controlli:** livello 1 identico (impronta: cambia solo il menu del gioco libero, con il pulsante della regata nuova; meriti e carriera identici); `polare.js`, `raffiche_e_virate.js`, `timone2.js` identici; `boma2.js` OK; i collaudi del timone e del boma ora spengono i salti (`__sv.setShifts(null)`), perché misurano altro.

## 1.0.27 — raddrizzare con A

Del 17 ottobre 2026, decisione di Ale: «il tasto R è da lasciare libero, perché nei livelli successivi potrebbe servire per manovrare; quelli speciali erano già predisposti: Q, A, Z». Raddrizzare passa da R ad A in tutti i livelli; R non fa più niente.

- **Gioco:** tasto A (`js/gioco.js`), testi «(o A)» nel suggerimento della scuffia, nel passo «Raddrizzare» della lezione 6 e nel pulsante «Raddrizza la barca (A)». A prima non era usato.
- **Collaudi:** gli 8 collaudi che premevano R ora premono A (impronta, fasce, giro di boa, registro, registratore, lezioni, pilota delle lezioni, competizione).
- **Controlli in due tempi:** prima il gioco accettava R e A e i collaudi premevano A: impronta identica, 63 scene su 63; poi R tolto e testi cambiati: diverse solo le scene 6.4 e 6.5, e solo nei tre testi «(o R)» → «(o A)». Riferimento dell'impronta rigenerato sulla 1.0.27. `collaudo_lezioni.py`: L6 «La scuffia» (A non raddrizza) e «Raddrizzare» OK, errori nessuno. Con `#collaudo` R su una barca scuffiata non fa niente, A la raddrizza; pagina senza `#collaudo` senza errori.
- **Documenti:** `README.md`, `MANUALE-bozza.md`, `VISIONE-LIVELLI-E-CARRIERA.md` §12 (R torna libero).

## 1.0.26 — livello 2 in prova: «spingi il boma» (Z)

Del 17 ottobre 2026, richiesta di Ale (tasto Z). Proposta, fonti e misure in `docs/PROPOSTA-SPINGI-BOMA.md`.

- **Fonti:** la manovra la descrivono allo stesso modo US Sailing, una guida per una deriva in singolo, una classe di catamarani e la federazione australiana (boma spinto fuori, barra dalla stessa parte, la barca va all'indietro e la prua gira verso il boma, al traverso si molla, si centra la barra e si cazza). Nessuna fonte dà numeri. Regolamento: 21.3 (chi va all'indietro spingendo una vela si tiene lontano), 42.3(f) (si può rallentare muovendo la barra).
- **Motore, solo per la barca del livello 2** (`BOMA2` in `js/motore.js`): con Z tenuto il boma resta a 80° dalla parte dove si trova; la vela è una piastra investita dal vento, applicata lungo il boma, quindi spinge indietro, di lato e fa girare la prua verso il boma. Quattro costanti nuove, tutte stime senza fonte. È il primo momento delle vele nel motore e vale solo col boma spinto.
- **Nel gioco:** navigazione libera con «Barca: livello 2 (prova)», Z tenuto premuto; un suggerimento spiega cosa succede e cosa fare dopo.
- **Misure** (`tests/fisica/boma2.js`, 39 partenze): la prua gira verso il boma 39 volte su 39; si esce dall'angolo morto 3,1 volte più in fretta che con la sola barra (con 10 nodi 1,0-1,8 s contro 4,2-5,0); all'indietro fino a 2,1 / 3,5 / 5,0 nodi con 6 / 10 / 15 nodi; dalla bolina sotto 1 nodo in 1,8 / 1,2 / 0,8 s contro 10,4 / 9,0 / 6,5 lascando tutta la scotta, e la barca poggia. Nessuna scuffia.
- **Collaudo nuovo `collaudo_boma2.py`** (tasti veri, 9 uscite dall'angolo morto e ripartenza): OK 5 volte su 5. Due correzioni del collaudo, dichiarate: la ripartenza cazzava 1 s soltanto (scotta a 0,73, vela che sbatte: la barca giustamente non ripartiva), ora 2 s; la soglia «almeno 1 nodo dopo 7 s» è scesa a 0,5 **dopo** aver visto 0,98-1,0 nodi con 6 nodi.
- **Controlli:** livello 1 identico al bit (impronta 63 scene su 63, `polare.js`, `raffiche_e_virate.js`); barca del livello 2 senza Z identica alla 1.0.25 (`timone2.js` uguale carattere per carattere, `collaudo_timone2.py` OK); pannello a 1360×650 senza eccesso col suggerimento nuovo; pagina senza `#collaudo` senza errori.
- **Ancora da decidere (Ale):** raddrizzare con A invece di R.

## 1.0.25 — livello 2 in prova: la freccia fino a 35°, Maiusc fino a 45°

Del 17 ottobre 2026, idea di Ale giocando la 1.0.24 (osservazione 56: «nessun'altra conseguenza»). `docs/PROPOSTA-STALLO-TIMONE.md` §9.

- Con la barca del livello 2 la barra va sempre veloce come nel livello 1; **la sola freccia si ferma a 35°**, **Maiusc + freccia arriva a 45°**. 35° è una regola del gioco, senza fonte. Il motore non cambia.
- **Misure:** con 45° la virata è più rapida a tutti i venti (C2 ok ovunque); con Maiusc da subito si perdono più punti di velocità con 5 venti su 6 (C1 fuori con 16 nodi); freccia, pausa e poi Maiusc è la virata migliore con 10 e 14 nodi (accompagnare la barra, che nasce dal motore). Restano fuori C3 ovunque, C4 e C8 con 6 nodi. Nel browser la perdita in più con Maiusc è piccola e con 15 nodi si inverte: dipende da come si molla la barra. Le soglie nuove sono state scritte dopo aver visto le tabelle in chat: dichiarato.
- **Controlli:** livello 1 identico al bit (impronta, `polare.js`, `raffiche_e_virate.js`); `collaudo_timone2.py` OK 5 volte su 5 (il controllo del cursore ora legge la barra nella stessa chiamata dei passi: con un fotogramma vero in mezzo falliva a caso); `collaudo_versione.py`.
- **Rimandato da Ale:** gli avvisi che si sovrappongono e spariscono prima di poterli leggere (osservazione 56).

## 1.0.24 — il timone del livello 2, in prova

Del 17 ottobre 2026. Primo pezzo della fisica del livello 2 (decisioni di Ale: vale solo per il livello 2, il livello 1 resta identico; barra lenta con la freccia, veloce con Maiusc). Proposta, revisione in chat, letture delle fonti e tutte le misure in `docs/PROPOSTA-STALLO-TIMONE.md`.

- **Fonti nuove:** F4 (Masuyama e Ogihara 2020) letta per intero, con le virate misurate di un 470 (figure 5 e 6, lette sulla griglia); F35, calcolo al computer del timone del 470 (stallo a 30-35°). In F4 i 5 e 12 kgf sono resistenza della barra, non forza laterale.
- **Motore, solo per la barca del livello 2** (`RUD2` in `js/motore.js`): la pala sente l'angolo effettivo, stalla oltre 22° (la forza resta, la resistenza cresce), la rotazione nasce dalla forza della pala, la barra arriva a 45°. Sotto 0,5 m/s e all'indietro resta il timone di sempre.
- **Nel gioco, in prova:** impostazioni della navigazione libera, «Barca: livello 2 (prova)». Freccia = barra a 20°/s, Maiusc + freccia = barra veloce; il cursore col mouse non va più veloce di Maiusc; un suggerimento dice quando la pala stalla. La finestra delle impostazioni va a capo per far stare la scelta (564 px su 650).
- **Esito, riportato com'è: l'obiettivo didattico non è raggiunto.** Sui venti di conferma mai guardati la barra veloce non perde più velocità di quella lenta con 6, 8 e 16 nodi (C1 fuori), la curvatura resta più stretta di quella del 470 a tutti i venti (C3 fuori), con 6 nodi la virata lenta dura 4,73 s (C4 fuori), la strambata con la barra lenta è 1,6-1,7 volte quella del livello 1 (C8 fuori). E dove la differenza c'è, nasce **mollando la barra dopo la virata**, non sbattendola: mentre la prua gira la pala quasi non stalla. Con lo stallo a 15° o a 30° l'effetto sparisce: è fragile.
- **Errore di misura trovato e corretto durante il lavoro:** il primo giro di `timone2.js` contava lo stallo anche dopo la virata, e faceva sembrare l'effetto quello voluto; la scelta dei valori è stata fatta su quel giro. Ora le due fasi si stampano separate.
- **Controlli:** livello 1 identico al bit (impronta 63 scene su 63; `polare.js`, `raffiche_e_virate.js`, `retromarcia.js`, `raffiche_portanti.js`, `bolina.js` identici); `collaudo_timone2.py` nuovo, OK 5 volte su 5; pannello a 1360×650 senza eccesso, anche con l'avviso di stallo; `collaudo_versione.py`.

## 1.0.23 — la barca balla sull'acqua

Del 17 ottobre 2026, idea di Ale giocando («una barchetta così navigando è molto poco ferma… dall'alto sembra una nave»). **Solo disegno: il motore non cambia** (impronta: 4.049 voci di stato su 4.049 identiche; cambiano solo le immagini del mare). Proposta, decisioni di Ale ed esito in `docs/PROPOSTA-MOTO-SUL-MARE.md`.

- **Onda corta solo disegnata**, che arriva da dove arriva il vento: di lato la barca rolla, di prua e di poppa beccheggia; contro le onde il ritmo è più fitto (1,6 s di bolina contro 4,4 in poppa con 10 nodi). Da ferma balla fino al doppio. Ampiezze e periodo sono **ipotesi nostre senza fonte** (5° di rollio con 15 nodi), dichiarate in `FISICA-E-TARATURE.md`.
- **Lo scafo si inclina con lo sbandamento** (sopravento compare la carena) e **la scuffia si vede cadere**: l'albero arriva sull'acqua in 0,6 s, con uno spruzzo. Prima la barca passava di colpo da sbandata a sdraiata.
- **Il timoniere ha un corpo**: gambe nel pozzetto, busto che esce fuori bordo quanto più si sporge, braccio di 45 cm sulla **prolunga** del timone (disegnata).
- **Baffi d'acqua alla prua**, più lunghi con la velocità, aperti di circa 20° (angolo di Kelvin), e uno spruzzo quando la prua scende sull'onda.
- **Collaudo nuovo `collaudo_moto_mare.py`** (dentro `lancia_tutti.sh`): 24.000 quadri, OK. Un criterio della proposta («di bolina il beccheggio almeno il doppio del rollio») era sbagliato in partenza ed è stato tolto, dichiarato; il primo giro aveva un metro che misurava anche lo sbandamento vero, corretto.
- **Controlli:** `polare.js` e `raffiche_e_virate.js` identici all'ultimo commit; costo del disegno sotto il rumore della misura; pagina con e senza `#collaudo` senza errori; `collaudo_versione.py`.

## 1.0.22 — pulizia del codice della partenza degli avversari

Del 17 ottobre 2026. **Solo pulizia: il gioco non cambia** (impronta identica al bit). È il primo punto dell'ordine deciso il 17 ottobre per chiudere il livello 1: rileggere a freddo il codice della partenza scritto in fretta nella 1.0.16-1.0.18 (`js/regate.js`).

- **La guida degli avversari era scritta tre volte**: nella regata (`aiControl`) e nelle due simulazioni che decidono quando partire (`startTime`) e quando smettere di spingere (`glideY`). Le simulazioni valgono solo se fanno quello che poi farà la barca: con tre copie bastava ritoccarne una per farle divergere senza che niente se ne accorgesse. Ora barra, scotta e prua d'attesa (45°/55°) stanno in tre funzioni piccole (`tillerFor`, `sheetFor`, `holdAngle`) usate da tutte e tre.
- **Tolto `b.startT`**, scritto a ogni simulazione e mai letto (nemmeno dai collaudi). **`b.holdS`**, riscritto a ogni passo e sempre −1 (si parte mure a dritta), è diventato la costante `HOLD_S`.
- **Controlli:** riferimento di `collaudo_impronta.py` rigenerato sulla 1.0.21 e confrontato due volte (con sé stesso e con la 1.0.22): 63 scene, 0 diverse. `polare.js` e `raffiche_e_virate.js` identici carattere per carattere all'ultimo commit. `collaudo_versione.py`.

## 1.0.21 — la lezione 5 dice che andando all'indietro la barra va al contrario

Del 17 ottobre 2026, testo di Ale. **Cambia il testo del passo 4 della lezione 5 «Una virata che non riesce» e una frase del riquadro delle regate** (`js/contenuti.js`, `js/regate.js`); motore, condizioni dei passi e avversari invariati.

- **Lezione 5, passo 4.** Il passo insegnava l'azione («sposta la barra verso il boma») ma non diceva che andando all'indietro la barra funziona al contrario: la frase c'era solo nell'esame, e il ripasso della lezione 5 (dalla 1.0.20) la dava per nota. Ora il primo paragrafo resta l'azione («Ora senza abbrivio: lasca la vela finché la barca scende sotto 1 nodo, poi prova a virare.») e il secondo è il testo di Ale: «Orza a bolina lascando: rallenta fino a perdere l'abbrivio e fallendo la virata. Se la barca arretra risponde al timone in modo opposto. Porta la prua fuori dall'angolo morto, centra e cazza per ripartire.» (corretto il refuso «opposto», aggiunto il punto finale). Ale ha scelto fra tre stesure; la prima, scritta per intero al posto del secondo paragrafo, non ci stava: +19 px a 1360×650 nel passo completato (+43 px con «verso il boma» aggiunto). **Da sapere:** il testo non dice da che parte spostare la barra («verso il boma», che c'era nel testo di prima); si ricava dalla lezione 2 (barra sottovento orza) e dall'inversione in retromarcia.
- **Riquadro delle regate: difetto della 1.0.18, corretto.** La frase sul richiamo che avevo aggiunto allungava il riquadro, che descrive il carattere di ciascun avversario (assegnato a caso): con tre avversari «prudente», il caso più lungo, il testo arrivava a 994 caratteri e il riquadro sforava di **15 px a 1360×650 in 10 partenze su 60 (17%)** (sulla 1.0.17 il massimo era 0 px, 856 caratteri). La 1.0.18 l'avevo misurata 6 volte di fila su una partita sola, e il testo cambia a ogni partenza: il collaudo del pannello segnalava l'eccesso solo ogni tanto (due volte su dieci giri). Ora la frase è «Se tagli prima dello zero vieni richiamato: torna dietro la linea e riparti subito, senza attese.» (era «… non c'è nessuna attesa da scontare.»): eccesso massimo **0 px su 60 partenze** con caratteri a caso, caso peggiore compreso.
- **Controlli:** pannello a 1360×650 e 1360×768 senza eccesso, pilota della lezione 5 (`--veloce --solo 5`), `collaudo_quiz.py`, `collaudo_versione.py`.
- **Collaudo nuovo, `collaudo_riquadro_regata.py` (60 partenze con i caratteri degli avversari a caso, dentro `lancia_tutti.sh`):** misura il riquadro con la pagina vera e il seme fisso, e vuole aver visto il caso peggiore (tre «prudente») o l'esito è NON VALIDO. Contro-prova: sulla versione della 1.0.18 dà **FALLITO** (10 semi su 60, 15 px), su questa **OK** (0 su 60). Prima il riquadro lo misurava solo `collaudo_pannello.py`, una volta sola con un testo a caso.

## 1.0.20 — due domande del ripasso tornano al loro posto

Del 17 ottobre 2026, decisione di Ale. **Cambiano solo testi e domande** (`js/contenuti.js`); motore e avversari invariati. Chiude le due voci aperte di «Da sistemare dopo la 0.20» in `docs/CONTENUTI-DA-VERIFICARE.md`.

- **Ripasso della lezione 2, domanda 4 spostata nel ripasso della lezione 5.** «La barca si è fermata nel vento e comincia ad andare all'indietro. Cosa succede alla barra?» (giusta: «Funziona al contrario») non aveva un passo che la insegnasse nella lezione 2: lo insegna la lezione 5, nel passo «Una virata che non riesce». Ora sta lì, dopo «Perché una virata può fallire?». **Da sapere:** quel passo insegna l'azione («sposta la barra verso il boma») ma non scrive con queste parole che la barra funziona al contrario; la frase sta nell'esame. Se si vuole, è una mezza riga da aggiungere al passo.
- **Nuova domanda nel ripasso della lezione 2, al suo posto:** «Vuoi poggiare, cioè allontanare la prua dal vento. Dove sposti la barra?», giusta «Sopravento, cioè lontano dal boma». Copre il passo «Barra sopravento: si poggia», che prima aveva solo la domanda sulla barra sottovento. Testo mio, facile da cambiare.
- **Lezione 3, passo «Filetti dritti»:** «Ora cazza…» diventa «Ora impara a cazzare: tira la scotta (freccia ↑) poco alla volta, finché entrambi i filetti scorrono dritti. In mare puoi anche poggiare; qui la barra è bloccata e si esercita la scotta.» Ora la risposta giusta del ripasso della lezione 3 («Cazzo la vela, oppure poggio») contiene una cosa che la lezione ha detto.
- **Controlli:** pannello a 1360×650 e 1360×768 senza eccesso (il passo 8 della lezione 3 è più lungo; margine misurato), `collaudo_quiz.py`, `collaudo_versione.py`.

## 1.0.19 — l'acqua dentro la raffica si vede di più

Del 17 ottobre 2026. **Cambia solo il disegno dell'acqua dentro le chiazze delle raffiche** (`js/disegno.js`); motore, avversari e testi invariati. Voce 4b della ROADMAP, idea di Ale. Proposta, fonti, criteri scritti prima di provare ed esito in `docs/PROPOSTA-INCRESPATURE.md`.

- **Cosa cambia:** dentro le chiazze (`gustAt > 0,04`) si disegna un **secondo strato di increspature**, fino al doppio dei trattini nel cuore, sfumato a zero sul bordo; questi trattini hanno uno **scorrimento proprio**, quello del vento della raffica più forte in acqua, così la trama slitta visibilmente dove il vento è più forte. Fuori dalle raffiche non cambia niente, e restano tutti i freni di prima (dissolvenza sotto zoom 0,5, niente increspature sotto 0,35, salto oltre 2500 celle).
- **Fonti** (F31-F34): la chiazza scura è l'increspatura capillare che riflette la luce in modo diverso, e **chiazze con increspature più ravvicinate indicano più vento**: la densità è il segnale. **Non è sostenuto da fonti** che la trama debba *scorrere* più in fretta: è plausibile (il vento locale trascina le onde capillari) e resta un **aiuto visivo dichiarato**.
- **Misure** (1360×650, 5 semi, nel momento in cui una raffica passa sulla barca; trama = scarto quadratico medio della luminanza su blocchi di 24 px, dentro il cuore della chiazza contro l'acqua calma): da **+267% a +340%** a zoom pieno, da **+196% a +506%** a zoom 0,5. **Costo** (300 quadri dopo 90 di riscaldamento, 5 semi): **12,62 ms contro 11,51** a zoom pieno (**+9,6%**, tetto dichiarato +15%) e 12,15 contro 11,70 a zoom 0,51 (+3,8%); a zoom 0,26 le increspature sono spente e il costo non cambia.
- **Criterio non raggiunto, dichiarato:** si chiedeva **+40% di trama rispetto a oggi**; a zoom 0,5 è +105%, a **zoom pieno +20%**.
- **Due passi falsi, corretti per strada:** accorciare i trattini (`1 + 0,6k` invece di `1 + 2k`, per seguire le fonti sulla densità) **peggiorava** il contrasto (da +267% a +226%): la lunghezza è rimasta quella di prima. E la densità scalata su `gk` puro aggiungeva **un solo trattino** quasi invisibile, perché nel gioco le raffiche arrivano a `k ≈ 0,4` e non a 1: ora si scala su 0,4 (costante nuova, ipotesi nostra).
- **Controlli:** `collaudo_vista.py` tutto OK (161 casi, nessuno sbagliato, compresi i controlli delle increspature ai vari zoom); `polare.js` e `raffiche_e_virate.js` identici carattere per carattere (il motore non è stato toccato); schermate in `tests/output/increspature/` (`prima-*` e `dopo2-*`), **giudizio sull'aspetto di Ale, giocando**: lo scorrimento più veloce in una schermata ferma non si può vedere.
- **Collaudi (nessun cambio al gioco):** `collaudo_carriera_intera.py` ora guida le lezioni con il **pilota delle lezioni** invece della sua tabella di 14 passi, e `collaudo_pilota_lezioni.py` è diventato importabile (guardia `__main__`). Il limite dichiarato di quel collaudo (18 passi su 32 saltati con l'aggancio) **non c'è più**: una carriera intera, da zero all'attestato, con **32 passi su 32 guidati e completati**, 0 saltati; prove 1-4 finite in 79,0 / 124,4 / 156,5 / 282,2 s; **ESITO OK**. Criterio I4 riscritto sui conteggi nuovi (prima controllava la tabella che non c'è più).
- **`collaudo_giro_boa.py`, prova 3 « linea d'arrivo »:** non finiva dal 16 ottobre (finiva l'11), con il pilota fermo 6-10 m prima del traguardo; il diario la chiamava «difetto vecchio del collaudo» dalla 1.0.10. Il pilota ora aggiunge un punto 25 m oltre il traguardo, sulla direzione da cui arriva (`docs/PROPOSTA-PROVA3.md`): la prova 3 finisce 3 volte su 3 (156-157 s). Nessun cambio al gioco.
- **`collaudo_registro.py` tornato a 15 su 15** (era 14 su 15, con verifiche diverse a seconda del giro): (1) «partenza anticipata» fermava la barca oltre la linea con la prua nel vento, ma con la retromarcia senza tetto (1.0.8, `backDrag` nella 1.0.13) una barca piantata scivola all'indietro a 1,1 m/s e in 40 s rientrava dietro la linea prima dello sparo: ora il pilota continua a bolinare verso il largo; (2) «contatto» insegue l'avversario più vicino fino a un contatto, e dalla 1.0.17 gli avversari si scansano meglio anche dal giocatore: la finestra di inseguimento passa da 30 a 60 secondi reali. Nessun cambio al gioco; tre giri completi su tre a 15 su 15.
- **`collaudo_competizione.py --tastiera` tornato valido (parte 5 delle partenze, aperta dalla 1.0.11):** in solitaria il pilota da tastiera passava sette minuti reali a 41-48° dal vento, all'indietro a 0,5 nodi, e non arrivava mai. Non era la fisica (il motore fa girare una barca che va all'indietro a 41° con la barra a fondo, da una parte o dall'altra, in 5 s): il pilota rimbalzava fra due regole contraddittorie. Allo sparo il rilevamento della linea gli faceva scegliere la mura opposta a quella su cui era fermo, e per cambiare mura da fermi la virata non riesce; la regola «piantata» lo riportava sulle mure di prima. Ora, sotto i 3 nodi e con la mura sbagliata, poggia prima con la scotta regolata e poi vira. **Due giri completi su due: ESITO OK** (con gli avversari quarto in 452 e 420 s, in solitaria arrivato in 423 e 458 s senza salvare nessun piazzamento). Provate tre varianti su una copia: senza l'inversione della barra in retromarcia si pianta nel vento; con la vela lascata resta a 95° a 2,2 nodi per sempre; solo con la scotta regolata funziona. Nessun cambio al gioco.
- **Passo 5.8 «Strambata controllata», 4 non completati su 100: non è un difetto del gioco.** Il pilota preciso strambava con la scotta a 0,53, cioè un boma a 49° (9° + 0,53 × 76°), mentre il gioco chiede 45° o meno (`sheetMax > 45` in `js/gioco.js`) e chiama violenta ogni strambata oltre: il pilota legge il boma con qualche grado d'errore, il giocatore vero ha il numero sotto il cursore della scotta. Il pilota impreciso scuffia 52 volte su 100 nel passo, ma lo faceva già nella 1.0.10 (56) e nella 1.0.13 (52): comportamento di chi strambo male, non una regressione.
- **Trovato per strada, non è un difetto del gioco:** il riferimento di `collaudo_impronta.py` era del 16 ottobre, quindi 61 scene su 63 risultavano diverse per i cambi delle versioni dalla 1.0.6 alla 1.0.18. **Rigenerato** su questa versione, così il collaudo torna utile alla prossima pulizia del codice (il file sta in `tests/output/`, che non è in git).

## 1.0.18 — il riquadro dice cosa fare se parti in anticipo

Del 17 ottobre 2026. **Cambia solo il riquadro delle regate** (una frase in `js/regate.js`); motore, avversari e pannello invariati. Chiude le parti 2, 4 e 6 del compito partenze (`docs/PROPOSTA-PARTENZE.md` §9).

- **Riquadro:** aggiunta la frase «Se tagli prima dello zero vieni richiamato: torna dietro la linea e riparti subito, non c'è nessuna attesa da scontare» (regola 29.1, F15). Durante la regata i messaggi c'erano già («Partenza anticipata! Torna dietro la linea», la scritta gialla sul mare e «Sei tornato dietro la linea: ora riparti»): mancava l'avviso **prima** di partire. Testo scelto da Ale, facile da cambiare: sta in un punto solo.
- **Parte 2, estremi della linea: chiusa senza modifiche.** Nelle misure della 1.0.16 e della 1.0.17 (oltre 3.600 partenze di avversari) **nessuno ha tagliato fuori dagli estremi** e nessuno è rimasto fuori senza partire; il punto d'attesa spostato di lato, pensato per il taglio, risolve anche questo. Il punto d'attesa è per costruzione entro due metri dagli estremi.
- **Parte 6, `collaudo_competizione.py` C1: rientrata.** Dalla 1.0.11 il pilota sostituto arrivava **ultimo nel 46-48%** delle regate (fascia 10-40%): adesso **35%** sui semi di misura e **28%** su quelli di conferma, e il collaudo dà **OK** in tutte le sue parti (C0-C5, 80 regate arrivate su 80 per livello). L'ha risolto il calo dei contatti della 1.0.17. Con gli avversari esperti, solo riportato, l'ultimo posto resta al 35% e al 48%.
- **Parte 5, pilota da tastiera: metà risolta, resta un difetto del collaudo.** Il difetto aperto dalla 1.0.11 (il pilota restava fermo all'indietro a 41-49° dal vento prima del via) **è sparito**: ora parte e con gli avversari arriva quarto. Ma nella regata in solitaria non taglia l'arrivo (si perde in poppa sull'ultimo lato), quindi `--tastiera` resta **NON VALIDO**. È il pilota di prova, non il gioco: da sistemare come collaudo, a parte.
- **Controlli:** pannello a 1360×650 con il riquadro più lungo, eccesso **0 px** su 6 misure; `collaudo_competizione.py` completo OK; nessun cambio al motore, quindi `polare.js` e `raffiche_e_virate.js` non rilanciati.

## 1.0.17 — gli avversari si evitano anche quando devono orzare

Del 17 ottobre 2026. **Cambia solo come gli avversari evitano le altre barche** (`js/regate.js`, due righe); barca, partenza e testi invariati. Parte 3 del compito partenze: proposta, criteri scritti prima di provare, varianti scartate ed esito in `docs/PROPOSTA-PARTENZE.md` §8.

- **Il difetto, misurato:** lo scarto per evitare veniva **riscritto** dalla regola «la prua desiderata non deve mai finire nell'angolo morto». Su 40 regate complete: annullato (ne resta meno di un terzo) nel **39%** degli istanti in cui una barca stava scartando, ridotto in un altro 12%; e in **83 contatti su 88** nei dieci secondi prima c'era uno scarto annullato. Le barche si vedevano, provavano a evitarsi e venivano rimesse in rotta di collisione.
- **Ora:** chi sta evitando può orzare **anche dentro l'angolo morto** (perde velocità, come nella realtà; se si pianta riparte con la regola che già c'era), e il cono in cui guarda le altre barche passa da **60° a 90°** dalla prua, perché i contatti misurati hanno le prue a **93°** in mediana: chi arriva di fianco prima non veniva nemmeno considerato.
- **Misure** (diagnostica temporanea, 80 regate complete per variante: due regate x due livelli x semi 1-20, giocatore fermo): contatti totali da **208 a 128** (−38%), nella risalita alla boa da **158 a 82** (−48%), prima del via **45 contro 47**, nei 30 s dopo il via **1 come prima**; barche con almeno una penalità da **141 su 240 (59%) a 97 su 240 (40%)**. Mediane d'arrivo su 24 semi: bastone **207 s contro 204**, raffiche **195 contro 188** (+1,5% e +3,7%, soglia +5%), 72 arrivi su 72 e nessuna BLOCCATA in entrambe. Metro verificato: stesso codice su 20 semi mai usati (21-40) dà gli stessi numeri entro il 3%.
- **Criteri non raggiunti, dichiarati:** si chiedevano i contatti nella risalita **dimezzati** (≤79: sono 82) e le barche con penalità **sotto il 30%** (sono il 40%). Quel che resta sono tre barche che convergono sulla stessa boa su mure opposte e si sfiorano a 1,4-3,1 nodi: per risolverlo servono le regole di precedenza alla boa, cioè il livello 2.
- **Tre varianti provate e scartate**, con i numeri in §8.6: evitare in base al **tempo** al minimo avvicinamento invece che alla distanza (scattava a 26 m fra due boline che convergono: contatti 255, regata +16%); **poggiare** invece di orzare quando orzare finirebbe nell'angolo morto (275, e in partenza da 47 a 137 contatti, perché poggiando la barca accelera dentro il gruppo); la stessa poggiata **solo per chi naviga** (254). La **boa sfalsata per barca** non è stata fatta: c'era già (`rOff`, da 0 a 6 m per avversario).
- **Controlli:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere (il motore non è stato toccato); criteri della partenza rilanciati; pannello e testi invariati, quindi non rimisurati.

## 1.0.16 — gli avversari aspettano sulla linea e partono quando serve

Del 17 ottobre 2026. **Cambia la partenza degli avversari** (`js/regate.js`) e il consiglio del riquadro delle regate; la barca del giocatore non cambia. Proposta, criteri (scritti prima di provare) ed esito in `docs/PROPOSTA-PARTENZE.md`.

- **Il difetto (dalla 1.0.6):** gli avversari frenavano a 7 m fissi dalla linea e partivano a una velocità stimata fissa (1,9 m/s). Con la barca della vasca, che scivola 10-11 m invece di 5-6, l'**83%** era oltre la linea allo sparo (era il 22-32% fino alla 1.0.4) e il ritardo mediano al via era di 6-15 s. Il salto era passato inosservato perché il collaudo controllava solo che le anticipate rientrassero entro 60 s.
- **Ora, senza nessun numero in metri scritto a mano:**
  - **fascia d'attesa in lunghezze di barca:** costante nuova `BOAT.length` = 4,2 m (`js/motore.js`), fascia da una a due lunghezze dietro la linea, punto d'attesa a una lunghezza e mezza;
  - **quando lascare lo decide la barca:** due volte al secondo simula con lo stesso `step()`, su una copia di sé, dove si fermerebbe lascando adesso (`glideY`), e lasca quando lo scivolamento finisce dentro la fascia;
  - **quando partire, uguale:** quattro volte al secondo simula in quanti secondi taglierebbe cazzando adesso (`startTime`), e parte quando quel tempo più il margine del carattere arriva al conto alla rovescia (esperti 0,5 ± 0,5 s, principianti 1,5 ± 1,5 s, la prudente +1 s; ipotesi nostre);
  - **punto di ritrovo a sei lunghezze** (25 m) dietro la linea fino a 45 s dal via: l'attesa vicino alla linea dura mezzo minuto, non tre, e la barca non ha tempo di andare alla deriva;
  - **attesa e ritrovo spostati di lato** di quanto la barca scivolerà risalendo (`tan(bolina+4°)` per metro guadagnato), così il taglio cade fra le boe;
  - **avvicinamento affidato alla logica generale**, che sa fare i bordi: puntando con una prua sola un punto controvento la barca scivolava fino a 90 m di lato, fuori dagli estremi, dove il taglio non conta e la barca non partiva mai.
- **Due difetti vecchi trovati per strada:** il timone dei bordi (`boardT`) scadeva durante l'attesa, così allo sparo tutti viravano subito perdendo metà della velocità sulla linea (ora resta a zero fino al taglio, e la prua della partenza si tiene finché non si taglia); chi era segnato anticipato continuava di bolina invece di tornare dietro la linea (ora esce dal blocco della partenza e rientra con la logica generale, come prima della 1.0.16).
- **La prua di attesa a 62°** della proposta **è stata tolta**: misurata, scivola di lato 0,3-0,5 m/s, cioè ~30 m in un'attesa lunga, e porta la barca fuori dagli estremi. In attesa si tiene 55° (0,01 m/s di lato) e 45° sotto mezza lunghezza. **Cambio dichiarato rispetto al §2 della proposta, deciso dopo aver visto le misure.**
- **Pannello del giocatore:** «Alla linea: … s alla velocità attuale» compare solo sotto 60 s (con la barca quasi ferma veniva un numero enorme). **Riquadro delle regate:** via «l'ideale è tagliarla lanciato proprio allo zero», al suo posto il metodo delle fonti (aspettare vicino alla linea quasi fermi con la vela lascata e cazzare negli ultimi secondi).
- **Misure** (`collaudo_partenze.py`, criteri del §3; semi 1-20 per scegliere, **21-100 mai guardati per confermare**; 2880 partenze di avversari nella conferma): partenze con almeno un richiamo **6,7% principianti e 5,4% esperti** a bastone, **4,6% e 3,8%** nelle raffiche (soglie 30% e 20%, esperti meno dei principianti); ritardo mediano al via **0,9-2,2 s** (soglia 3) con 1, 3 e 5 minuti; velocità mediana al taglio **4,65-5,33 nodi** (soglie 3,72 e 4,20); **nessun avversario non partito entro 60 s** e nessuno rimasto anticipato (prima della correzione del rientro erano 37 su 720); nessuna anticipata fuori dagli estremi; **718-719 barche su 720 passate dalla fascia d'attesa**, cioè il metro ha misurato davvero. Esito del collaudo **OK** sui semi di conferma; sui semi 1-20 l'unico criterio fuori era «esperti meno dei principianti» nelle raffiche, pari a 3,3% contro 3,3%, che con 80 semi si separa.
- **Costo di calcolo:** 3,1 ms per secondo simulato (massimo 5,8), con tre avversari che simulano sé stessi.
- **Controlli:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere a quelli della 1.0.15; regate a bastone e nelle raffiche (semi 1-6) 18 arrivi su 18 e nessuna BLOCCATA, mediana 201 s e 188 s; pannello a 1360×650 eccesso 0 px e riquadro delle istruzioni 0 px su 6 misure. **Non misurati in questa versione:** contatti fra avversari (restano le penalità, parte 3 del compito) e `collaudo_competizione.py`.
- **Restano aperte le altre parti** del compito partenze (estremi della linea, contatti, rientro dopo l'anticipo, pilota da tastiera all'indietro, C1 della competizione): `docs/PROPOSTA-PARTENZE.md` §5.

## 1.0.15 — la raffica da assorbire arriva davvero

Del 16 ottobre 2026. **Cambia il passo 6.2 «Assorbire una raffica»** (lezione 6); testo e motore invariati. Proposta ed esito in `docs/PROPOSTA-CORREZIONI-PASSI.md` §5-6.

- **Il difetto:** il passo si completava a mani ferme 16 volte su 20 (pilota, semi 1-20), perché bastava il bordo di una raffica moderata (+12%) e la barca restava sotto i 20° da sola.
- **Ora:** una raffica media garantita (+45%, `bigGust: 0.45`), che nasce 45 m sopravento sulla strada della barca; la condizione vale solo nel cuore della raffica (almeno +30%) e di bolina (entro 75° dal vento). Costanti ipotesi nostre, senza fonte. La raffica forte del 6.3 resta identica.
- **Misure** (pilota, semi 1-20 e conferma 21-100, sulla copia poi portata nel gioco senza differenze): guidando **20 su 20 e 80 su 80**, mediana 11,3 s (prima 38 s); a mani ferme **0 su 20 e 0 su 80**; contro-prova di bolina senza lascare: 1 su 20. Senza la condizione di bolina, con la raffica che arriva davvero, il passo si completava da solo 98 volte su 100 (barca al traverso con la vela troppo cazzata).
- **6.3 «La scuffia» non cambia:** si completa a mani ferme in parte delle corse (con la 1.0.15, 47 su 80, perché si arriva dal 6.2 con la vela regolata), ed è voluto: chi non fa niente non lascia, e la raffica forte lo fa scuffiare.
- **Controlli:** `polare.js` e `raffiche_e_virate.js` identici; testo dei passi invariato, quindi pannello non rimisurato. Pilota veloce sul gioco vero: 32 passi tutti guidati, da guardare solo 1.11 e 2.4 dopo un colpo lungo e 6.3 a mani ferme; note di `lancia_tutti.sh` aggiornate a questi casi.

## 1.0.14 — orzare fino a un terzo della strada

Del 16 ottobre 2026. **Cambia solo il testo del passo 2.4 «Barra sottovento: si orza»** (lezione 2). Proposta ed esito in `docs/PROPOSTA-CORREZIONI-PASSI.md` §3.

- **Il difetto (dalla 0.16):** il testo diceva di fermarsi con la lancetta «a metà strada tra il rosso e l'orizzontale», circa 65°, ma il passo accetta da 43° a 67°: chi legge la lancetta con qualche grado di errore la supera.
- **Ora:** «a un terzo della strada», circa 57°, al centro della finestra; come dice già il passo 2.5. Condizione e motore invariati.
- **Misure** (pilota con lettura ±5°): semi 1-20 da 20 su 20 con 5 riprese a 20 su 20 senza riprese; semi 21-100 da 79 su 80 con 29 riprese a **80 su 80 senza riprese**. Resta l'osservazione 49 (dopo un colpo lungo nel passo 2.3 la prua è già in bolina, 3 su 80): voluto, è ciò che fa la barra tenuta.
- **Collaudi:** pilota delle lezioni aggiornato al bersaglio nuovo (57°).

## 1.0.13 — la retromarcia un po' più lenta

Del 16 ottobre 2026, decisione di Ale. Esito in `docs/PROPOSTA-CORREZIONI-PASSI.md` §2.

- **Retromarcia** (`js/motore.js`): costante nuova `backDrag` = 1,5, che moltiplica la resistenza dello scafo quando la barca va all'indietro (specchio di poppa e pala al contrario). **Ipotesi, nessuna fonte.** Massimo all'indietro con la prua al vento e la barra al centro: con 10 nodi da 2,33 a **1,99 nodi**, con 15 da 3,40 a **2,96**, con 20 da 4,30 a **3,79**. Non cambia quanto presto parte (con 10 nodi −0,5 nodi dopo 1,6 s, come prima). Cursore nuovo nel laboratorio (da 1 a 4).
- **Passo 1.9 «Ripartire»:** nessun cambio (strada A di Ale). La barca esce da sola dall'angolo morto per una regola senza fonte (`ironsYaw`); toglierla renderebbe il passo impossibile senza il comando «spingi il boma» (livello 2). Osservazione 45 chiusa come semplificazione dichiarata.
- **Misure:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere; `angolo_morto.js` stesse uscite, da 0,1 a 0,3 s più lente; pilota veloce delle lezioni 1 e 5 tutto completato. Per scelta di Ale nessun altro collaudo: le prove e le regate in cui la barca va all'indietro possono cambiare di poco (record non azzerati).

## 1.0.12 — orzare fino al rosso, non fino a fermarsi

Del 16 ottobre 2026. **Cambia solo il testo del passo 1.8 «Orzare e l'angolo morto»** (lezione 1); motore e condizione del passo invariati. Proposta ed esito in `docs/PROPOSTA-CORREZIONI-PASSI.md` §1.

- **Il difetto (dalla 1.0.11):** il testo diceva di tenere la freccia «finché la barca non si ferma quasi del tutto». Con la vela che stringe di più la barca arriva al vento più veloce e, tenendo la barra, vira: il pilota completava il passo 0 volte su 80.
- **Ora:** «Quando la prua è quasi nel vento (la lancetta della rosa entra nel rosso), rilascia», più una frase scelta da Ale: chi tiene troppo vira e preme *Ricomincia*.
- **Misure** (pilota che rilascia nel rosso, prima della modifica): preciso 20 su 20 (semi 1-20) e 80 su 80 (semi 21-100), mediana 7 s; impreciso, che tiene da 0,3 a 1,5 s di troppo, 12 su 20 e 45 su 80 (le altre volte vira, ed è realistico). Pannello a 1360×650: eccesso 0 px. `polare.js` e `raffiche_e_virate.js` identici. **Conferma sui semi 101-200 non fatta:** Ale ha provato giocando («funziona») e ha deciso di non proseguire coi collaudi.
- **Collaudi allineati al testo nuovo** (non rilanciati qui): `collaudo_pilota_lezioni.py` e `collaudo_registro.py` rilasciano la freccia quando la prua entra nel rosso invece di tenerla fino al completamento; tolta da `lancia_tutti.sh` la nota sul passo 1.8 come caso noto.

## 1.0.11 — la resistenza indotta e la vela che stringe

Del 16 ottobre 2026. **La barca cambia di bolina.** Proposta (due stesure, revisione in chat sul testo completo di Day 2017), scelta di Ale (variante 9° / 22°), criteri ed esito in `docs/PROPOSTA-BOLINA.md`.

- **Cosa cambia nel motore** (`js/motore.js`):
  - **resistenza indotta:** la spinta laterale ora frena, con la formula di Delft usata da Day 2017 (eq. 15): `Ri = side²·u·|u| / (π·½ρ·TE²·(u² + 0,4)²)`. Costante nuova `TE` = 0,80 m (ipotesi: dà il 14% di Day con 10 nodi). Il termine 0,4 è lo stesso dello scarroccio: senza, la barca non ripartiva da ferma;
  - **la vela stringe:** `minBoom` 14° → 9°, `luffA0` 27° → 22°: la vela porta del tutto da 29° di vento apparente invece che da 34° (a 28° dava il 10% della portanza, ora l'81%; i coefficienti usati da Day quasi tutta);
  - **la vela frena meno:** nella resistenza il peso di CL² passa da 0,12 a 0,08 (nuova voce `sailCL2`), cioè CD di bolina da 0,413 a 0,34.
- **Laboratorio:** tre cursori nuovi (`minBoom`, `sailCL2`, `TE`) e tre profili per confronto: «barca della 1.0.10», «senza resistenza indotta», «vela della 1.0.10».
- **Misure** (nuovo banco `tests/fisica/bolina.js`; `node bolina.js 1010` rifà la barca di prima):
  - VMG di bolina con 6 / 10 / 15 nodi: 2,07 / 3,13 / 4,02 → **2,25 / 3,29 / 4,07** (Day: 2,65 / 3,6 / 3,8); angolo della VMG migliore 54° / 51° / 47° → **45° / 45° / 42°** (Day: circa 44° / 40,5° / 43,5°); di poppa invariata;
  - con 12 nodi contro le misure di Binns: da −1% a +1% fra 42° e 60° (prima −25% a 42°); con 9 nodi resta dal −12% al −15%: **la bolina con poco vento resta lenta**, causa non identificata;
  - con 10 nodi la barca avanza da circa 26° dal vento (prima 31-33°): 1,3 nodi a 30°, 3,9 a 40°;
  - controlli di esecuzione: tutti i numeri della proposta ritrovati uguali sul motore vero; la barca «1.0.10» ridà `polare.js` di prima **carattere per carattere**; 12.960 casi con i cursori nuovi agli estremi e due passi di tempo, nessun conto in errore;
  - partenza da ferma al traverso stretto: 2 nodi in 2,6 s (prima 2,5), 3 nodi in 3,9 s (prima 3,6);
  - **raffiche:** a parità di boma (21°) sbanda un po' meno: 26° / 39° / 53° con 16 / 18 / 20 nodi (prima 28° / 42° / 55°). `raffiche_e_virate.js` dà invece 38° / 54° / **67° (scuffia)**, perché tiene fissa la scotta (0,1), che ora cazza la vela di 4,5° in più: il confronto non è alla pari. Con la scotta suggerita dal gioco una raffica da 20 nodi fa scuffiare prima (71°) e dopo (67°);
  - virata da 3,9 nodi in 3,0 s (prima 3,3), da 1,9 nodi in 6,6 s (prima 7,6);
  - `retromarcia.js` quasi uguale (massimi entro 0,05 nodi); `angolo_morto.js` 2.184 su 2.196 (prima 2.188) e 41 su 4.860 (prima 28); `raffiche_portanti.js` 18 su 18.
- **Avversari:** VMG di bolina nella regata a bastone (semi 1-6) 2,45 → 2,44 nodi; diviso per quella del banco, dal 78,3% al 74,2%, −4,1 punti, dentro la soglia di 5 dichiarata prima. Non sfruttano la vela nuova perché stringono sempre a 49-54°. Regate a bastone e nelle raffiche: 18 arrivi su 18 ciascuna, nessuna BLOCCATA. Partenze uguali alla 1.0.10 (stesso collaudo lanciato su una copia della 1.0.10).
- **Prove:** pilota 79,0 / 124,5 / 156,8 / 276,0 s, prova 5 finita 24 volte su 24 (prima 23), mediana 297,8 s, una sola corsa lunga (prima 7). Fasce ritarate con la regola di sempre: 3 [160, 200, 255], 4 [280, 350, 450], 5 [300, 375, 480]; 1 e 2 uguali. **Record azzerati** (chiavi `KEYV` nuove; le vecchie si cancellano al primo avvio).
- **Lezioni, pilota sui semi 1-20 e conferma sui 21-100, contro la 1.0.10 sugli stessi semi:**
  - **si rompe «Orzare e l'angolo morto» (lezione 1):** guidando 0 su 80 (prima 74 su 80). Tenendo la barra come dice il testo («finché la barca non si ferma quasi del tutto»), la barca ora arriva al vento con più velocità e lo attraversa: vira invece di fermarsi. **Prova di Ale giocando** (registrazione `sessione-20261016-1916.txt`, un tentativo): orzando a piccoli colpi e fermandosi con la prua a 11-19° dal vento, il passo si completa in 10 s; Ale: «funziona perfettamente». **Deciso di non cambiarlo ora**; resta da guardare nelle correzioni dei passi (chi tiene il tasto premuto di continuo vira);
  - migliora «Ripartire» già fatto dopo un colpo lungo: 2 su 80 (prima 29), ma si completa a mani ferme 17 volte su 80 (prima 1), perché arriva dal passo prima saltato;
  - «La scuffia» a mani ferme 21 (prima 28), dopo un colpo lungo 11 (prima 20);
  - peggiora «Assorbire una raffica» a mani ferme: 54 su 80 (prima 46);
  - il resto entro 1-2 casi.
- **Collaudi aggiornati:** chiavi dei record in 9 collaudi; tempi dell'oro in `collaudo_pannello.py`; in `collaudo_linea.py` anche le chiavi della 1.0.10 fra quelle da cancellare; in `collaudo_suggerimento.py` l'elenco delle prove «non misurate» della lezione 5 passo 4 comprende ora anche il caso 4 con la scotta a metà, che con la vela nuova riparte senza piantarsi (**cambio fatto dopo aver visto il risultato**; tutti i 20 casi riusciti).
- **Collaudi sistemati dopo la prima consegna (richiesta di Ale):**
  - `raffiche_e_virate.js` stampa anche tre righe «boma a 21°» (26° / 39° / 53°), così il confronto con le versioni di prima torna alla pari; le prime sei righe restano identiche;
  - `collaudo_suggerimento.py`, parte «raffica in arrivo»: apriva la prova 5 senza seme e aspettava 300 ms veri, e in 1 giro su 4 non trovava nessuna raffica adatta (0 casi misurati). Ora usa Math.random a seme fisso (il primo seme con una raffica adatta, oggi 1, stampato) e legge i 6 casi in una sola chiamata, con un passo di simulazione prima di leggere. Tre giri su tre: 6 casi su 6, nessuno sbagliato. **Contro-prova:** su una copia del gioco con il testo della raffica cambiato il collaudo fallisce e indica i 6 casi;
  - `lancia_tutti.sh`: note «cosa guardare» aggiornate ai numeri della 1.0.11 (polare, raffiche, e il passo 1.8 nel pilota veloce).
- **Collaudi lanciati qui, OK:** laboratorio, linea, libretto, carriera, carriera con esame, esame, pannello (eccesso 0 px), suggerimento, regate, partenze, fasce, pilota delle lezioni.
- **Giro completo sul PC di Ale** (`lancia_tutti.sh`, 16 ottobre sera; il riepilogo finale non è uscito perché lo script è stato modificato mentre girava, le uscite sono tutte in `tests/output/lancia_tutti/20261016-192024/`). OK tutti quelli con esito chiaro, salvo:
  - `collaudo_contatto_senza_colpa.py`: il controllo «almeno una regata pulita su 6» passava per un soffio nella 1.0.10 (1 su 6) e ora no (0 su 6), perché il pilota sostituto prende per caso altri contatti con penalità. **Corretto il collaudo** (cambio deciso dopo aver visto il risultato): nella regata costruita «colpa dell'avversario» anche i contatti con penalità presi dopo quello costruito sono «altri errori». Ora 6 su 6 e TUTTO OK; nel testo costruito restano «penalità comprese: 15 s» accanto a «Errori: nessuno», perché il tempo di penalità non si tocca;
  - `collaudo_registro.py` 14 su 15: è il passo 1.8 della lezione 1 (orzando la barca vira invece di piantarsi), già noto;
  - `collaudo_competizione.py` misura **FALLITO, effetto vero della 1.0.11**: il pilota sostituto arriva ultimo nel 48% e 46% delle regate (semi 1-40 e 41-80; nella 1.0.10, stesso collaudo su una copia, 39% e 40%; fascia 10-40%). Al passaggio dell'arrivo è ultimo come prima (18 e 20 su 80 contro 17 e 18): lo spostano le **penalità dei contatti**. Da riprendere nel compito «avversari e partenze»;
  - `collaudo_competizione.py --tastiera` NON VALIDO: senza avversari il pilota da tastiera resta prima della partenza a 41-49° dal vento, all'indietro a 0,5-0,6 nodi, per oltre 7 minuti (due giri su due, quello di Ale e uno qui). Nella 1.0.10 arrivava, ma lento (10 min 40 s, fermo a lungo fra 39° e 48° a meno di 1 nodo). È la semplificazione già dichiarata nella 0.20.1 (barca che arretra fra 36° e 56° con la scotta lascata); da capire nel compito sulle partenze;
  - `collaudo_giro_boa.py` prova 3 «linea d'arrivo» non finita: **difetto vecchio del collaudo**, uguale sulla 1.0.10 (due giri su due per versione).

- **Testi da ricontrollare (Ale):** nel glossario «Bolina stretta: circa 45°, il massimo che la barca riesce a stringere»: ora la barca stringe fino a circa 30°, lentamente; la VMG migliore resta intorno a 45°.
- **Prototipo del fiocco:** resta col motore suo.

## 1.0.10 — il perno del segnavento vicino alla punta

Del 16 ottobre 2026, da un'osservazione di Ale. **Cambia solo il disegno.** Proposta ed esito in `docs/PROPOSTA-DISEGNO-VELA.md`, ultime sezioni.

- **Il difetto (dalla prima versione):** il segnavento era attaccato alla testa d'albero al 70% della lunghezza verso la punta, cioè col perno più vicino alla coda. Un segnavento vero gira come una banderuola: la coda, più grande, va sottovento, quindi il perno sta verso la punta.
- **Ora** la punta sporge 0,3 sopravento dal perno e la coda 0,7 sottovento; stessa lunghezza, stessa direzione. Con la barca sbandata un pallino scuro segna il perno in testa d'albero: senza, sbandando sopravento la freccia sembrava staccata dall'albero (Ale). I testi (lezione 4, glossario) non cambiano: la punta indica ancora da dove arriva il vento apparente.
- **Misure:** impronta con riferimento preso subito prima: diverse solo le immagini del mare, 20 scene su 21 (campo `tela`, nient'altro); `polare.js` e `raffiche_e_virate.js` identici; pagina da giocatore senza errori; schermate in `tests/output/vela/v110/`.
- **Da guardare giocando (Ale):** la coda ora finisce più spesso sopra la vela.

## 1.0.9 — le raffiche secondo l'andatura

Del 16 ottobre 2026 (osservazione 52). **Cambiano solo i testi:** il motore è lo stesso. Proposta, fonti, decisioni di Ale ed esito in `docs/PROPOSTA-RAFFICHE-PORTANTI.md`.

- **Il difetto.** Al lasco e al gran lasco, in raffica, il pannello diceva di lascare anche con la vela già lascata, e con la vela tutta lasca diceva di orzare a qualunque andatura: al traverso e al lasco è il consiglio sbagliato.
- **Ora il suggerimento dipende dall'andatura** (confini del pannello: bolina fino a 75°, traverso e lasco fino a 135°, poi gran lasco e poppa):
  - raffica in arrivo: «sfruttala per accelerare», poi di bolina «Se sbandi troppo, lasca o orza un poco.», al traverso e al lasco «Se sbandi troppo, poggia e lasca un poco.», al gran lasco e in poppa «Se poggi troppo rischi la strambata.» (testo di Ale);
  - oltre 25° di sbandamento, dal traverso in giù: «lasca la scotta e poggia un poco», e con la vela già tutta lasca «poggia un poco». Di bolina come prima; il confine per «orza» passa da 80° a 75°.
  - **Indicazione di Ale:** la prudenza vale per le lezioni, ma in regata le raffiche si cercano per andare più veloci, e si manovra quando arriva il pericolo. Per questo il consiglio di manovrare vale solo «se sbandi troppo».
- **Lezione 6:** nel passo «Raffiche e sbandamento» una frase nuova: al traverso e al lasco in raffica si poggia anche un poco, perché orzare fa sbandare di più. (Nel «Riepilogo», dove era proposta, il pannello sforava di 31 px.)
- **Fonti** F18-F22 in `FONTI-PUBBLICHE.md` (due classi di derive, Wikipedia, riviste, un circolo e forum) più F7 (Dellenbaugh); disaccordo dichiarato in `CONTENUTI-DA-VERIFICARE.md`.
- **Misure:**
  - **il motore dà ragione al consiglio** (`tests/fisica/raffiche_portanti.js`): la regola finale, «poggiando non si sbanda mai più che non facendo niente, dove senza reagire si sbanda oltre 15°», è passata **18 su 18** su un gruppo mai guardato. **Le due regole precedenti non erano passate** (6 su 12 e 24 su 30): a 80° con raffica leggera anche orzare aiuta un poco, e oltre 125° la barca sbanda così poco (4-8°) che poggiare cambia meno di un grado, a 130° anche in peggio. Ogni regola è stata cambiata **dopo** aver visto i numeri, con il via di Ale, e confermata su un gruppo nuovo;
  - `collaudo_suggerimento.py` esteso: 12 casi di sbandamento (3 fasce, 2 mure, vela tutta lasca o no) e 6 di raffica in arrivo, tutti col testo atteso; pannello 0 px;
  - `collaudo_pannello.py` a 1360×650: nessun passo eccede, 0 px;
  - impronta: diversi **solo** 3 testi (lezione 6.1, 6.3, regata 2 esperti), stato delle barche identico; `polare.js`, `raffiche_e_virate.js` e `collaudo_lezioni.py` identici; pagina da giocatore senza errori.
- **Da rivedere (Ale):** i testi vanno resi più efficaci e forse più corti; li riguarda giocando.

## 1.0.8 — la retromarcia senza tetto

Del 16 ottobre 2026. **Scelta di Ale:** la barca all'indietro è una barca lasciata andare con la vela che sventola. Proposta, criteri ed esito in `docs/PROPOSTA-RETROMARCIA.md`; ricerca in `docs/RICERCA-RETROMARCIA.md`.

- **Cosa cambia nel motore.** Tolto il tetto `backMax` (1,2 m/s, cioè 2,3 nodi), che non aveva una fonte: anche dal laboratorio. All'indietro la barca va solo per la spinta della vela che sbatte, contro la resistenza della tabella della vasca (misurata con la prua avanti: semplificazione dichiarata). **Nessun freno di poppa** in più: non ci sono numeri. Nessuna costante nuova.
- **Misure** (nuovo banco `tests/fisica/retromarcia.js`):
  - massimo all'indietro con la prua al vento 0,97 / 2,34 / **3,40** / **4,31** nodi con 6 / 10 / 15 / 20 nodi di vento (prima 0,97 / 2,33 / 2,33 / 2,33): **fino a 10 nodi non cambia quasi niente**;
  - **quanto presto parte non cambia** (−0,5 nodi dopo 1,6 s da ferma con 10 nodi, come prima): l'impressione che parta troppo presto resta aperta;
  - all'indietro con la barra a fondo la barca gira fino a 33 / 46 / 56 °/s con 10 / 15 / 20 nodi;
  - `polare.js`, `raffiche_e_virate.js` e `angolo_morto.js` identici carattere per carattere (2.188 uscite su 2.196);
  - impronta del gioco identica al bit (63 scene, 0 diverse): lezioni, prove e regate non portano mai la barca all'indietro oltre 2,3 nodi;
  - `collaudo_suggerimento.py` identico; `collaudo_lezioni.py` stesso esito (una differenza di tempo, 0,8 contro 1,0 s nella scuffia della lezione 6, era una variazione fra corse: 3 corse prima e 3 dopo danno sempre 1,0 s); `collaudo_laboratorio.py` OK, con `maxRudder` al posto di `backMax` nella prova di esportazione.
- **Corretta la ricerca:** stimava 3,5 nodi all'indietro con 10 nodi; sul motore vero sono 2,60 (con la prua tenuta nel vento), perché andando all'indietro il vento apparente cala.

## 1.0.7 — la vela disegnata come un triangolo, attaccata alla testa d'albero

Del 16 ottobre 2026 (osservazione 41). **Cambia solo il disegno:** la fisica è la stessa. Proposta, scelta di Ale ed esito in `docs/PROPOSTA-DISEGNO-VELA.md`.

- **Il difetto.** Vista dall'alto, la parte alta della randa era lunga quanto il boma: un cuneo largo anche in cima. Inoltre, sbandando, l'albero disegnato finiva a 5,5 × seno dello sbandamento sottovento, la cima della vela solo a 2,6 × seno, e il segnavento restava alla base dell'albero: la vela sembrava attaccata a qualcos'altro.
- **Ora** la randa è un triangolo: base sul boma (appena gonfia), balumina dalla fine del boma alla penna (gonfia sottovento), penna in **testa d'albero**. Albero, penna e segnavento stanno nello stesso punto: sbandando, l'albero si sdraia e si porta dietro vela e segnavento. Le stecche partono dalla balumina; i filetti restano esattamente dove erano. Il gonfiore della balumina (1,6 × grasso + svergolamento) è una scelta a occhio, senza fonte. L'etichetta «randa» punta al centro del triangolo.
- **Misure:** impronta del gioco con riferimento preso subito prima: diverse **solo** le immagini del mare, 20 scene su 21 (uguale la 6.5, barca scuffiata, disegno a parte); stato delle barche, testi e registro identici. `polare.js` e `raffiche_e_virate.js` identici carattere per carattere. Pannello a 1360×650: eccesso 0 px. Schermate in 12 situazioni (bolina 0°/15°/30°, traverso 15°/30°, lasco, mure a dritta, vela che sbatte dritta e sbandata, strambata col boma al centro, poppa, sbandata sopravento) in `tests/output/vela/v107/`.
- **Da giudicare giocando (Ale):** barca sbandata, vela che sbatte, strambata, e il segnavento che ora segue la testa d'albero e può finire disegnato sopra la vela.

## 1.0.6 — la resistenza dello scafo misurata in vasca

Del 16 ottobre 2026. **La barca cambia:** è più veloce e vira meglio. Proposta (due stesure, due revisioni in chat), criteri ed esito in `docs/PROPOSTA-VELOCITA.md`. Scelta di Ale: si tara la barca **condotta bene**.

- **Cosa cambia nel motore.** La resistenza dello scafo non è più `hullK1`·u + `hullK2`·u² + `hullK4`·u⁴ (4, 12, 0,9), che frenava da 1,45 a 2,5 volte il vero. Ora è una **tabella misurata in vasca** su uno scafo da 4,2 m (F16, F17 fig. 2, letta a occhio), da 2 a 9 nodi, più l'attrito di deriva e timone (`appDA` 0,0049 m², F17 fig. 11). Sotto i 2 nodi e sopra i 9 l'area resta quella dell'estremo (nessuna misura). `hullK1`, `hullK2`, `hullK4` non esistono più; nel laboratorio ci sono `hullScale` (1 = la vasca) e `appDA`.
- **Errore trovato dalla chat nella prima stesura:** il «+20% per deriva e timone» era una lettura sbagliata di Day 2017. Quel 20% vale solo di bolina, e per il 14% è resistenza indotta, che nel motore non c'è.
- **Regola sui dati (Ale):** in `PROGETTO.md`, `FONTI-PUBBLICHE.md` e `CLAUDE.md`, i valori numerici misurati, letti da pubblicazioni scientifiche e citati, si possono usare nel motore. Senza questa eccezione la tabella non poteva entrare: una fonte non dichiara licenza, l'altra è CC BY-NC-ND.
- **Misure** (vento 10 nodi salvo dove detto):
  - polare 3,8 / 6,0 / 4,1 nodi a 45° / 90° / 180° (era 3,4 / 5,2 / 3,5); con 15 nodi al traverso 9,5 nodi, oltre la tabella;
  - virata da 3,9 nodi in 3,3 s (era 4,0); da 1,9 nodi riesce in 7,6 s (prima falliva);
  - raffiche quasi uguali (28°, 42°, 55° con 16, 18, 20 nodi);
  - retromarcia fino a 2,3 nodi (era 1,8), che arriva al tetto `backMax`: da guardare nel compito sulla retromarcia;
  - **controlli di esecuzione OK:** resistenza uguale alla tabella (scarto 0,000%), polare e VMG uguali alla proposta;
  - nessun conto in errore con i cursori agli estremi.
- **Rapporti, non soglie:**
  - VMG contro Day 2017 (stessa vasca, quindi non prova lo scafo): di poppa −10 / −8 / −9% con 6 / 10 / 15 nodi; di bolina −22 / −14 / **+5%**;
  - contro le misure di Binns con 12 nodi: −4% a 60°, −6% al traverso, −27% a 42°, dal −21 al −32% sottovento (misure con del surf);
  - con 6 nodi, contro le medie GPS di Caraballo: −36% di bolina, −16% a 120°, −23% in poppa;
  - con la curva della vasca da 70 kg invece che da 80, la barca andrebbe dallo 0,4 al 3% più forte.

  Cause probabili degli scarti di bolina (vela che non stringe con poco vento, resistenza indotta assente, timoniere che raddrizza troppo bene): compiti separati.
- **Prove:**
  - fasce delle medaglie ritarate con la regola di sempre: 1 [80, 100, 130], 2 [125, 155, 200], 3 [165, 205, 265], 4 [290, 365, 465], 5 [305, 380, 490];
  - tempi del pilota 79,6 / 124,2 / 161,8 / 285,1 s; prova 5 finita 23 volte su 24, mediana 304,6 s. 7 corse su 24 sono lunghe (556-897 s): il pilota a tratti si pianta, da capire.
- **Record azzerati** (Ale: «tutti i miei salvataggi possono sempre essere cancellati»). Chiavi `KEYV` nuove; le chiavi vecchie si cancellano al primo avvio, con il messaggio «La barca o le prove sono cambiate». I piazzamenti delle regate restano salvati ma non si leggono più.
- **Lezione 4, passo «Da fermi»:** soglia da 2 a **2,5 nodi** (testo e condizione), scelta di Ale. Con la resistenza giusta, vela tutta lascata al traverso, la barca si assesta a 2,1 nodi, e il passo era diventato impossibile (0 corse su 20).
- **Pilota delle lezioni, semi 21-100** (tra parentesi stamattina):
  - **migliora** «Accelerando», uno dei sei passi da correggere: nessuna ripresa (80) e 6,4 s (13,7);
  - «Ripartire» resta già fatto dopo un colpo lungo 29 volte (27);
  - «Assorbire una raffica» si completa a mani ferme 46 volte (56), ma guidando 25 su 34 (24 su 24);
  - **peggiorano:**
    - «Orzare e l'angolo morto», guidando 74 su 80 (80) e 16,3 s (5,7): la barca scivola più a lungo e a volte passa il vento;
    - «La scuffia» a mani ferme 28 volte (18);
    - «Strambata controllata» 76 su 80 (79);
    - «Troppo cazzata» dopo un colpo lungo 7 (4);
    - «Barra sopravento» dopo un colpo lungo 5 (2).

  Tutto da riportare nelle correzioni dei passi.
- **Collaudi corretti:**
  - pilota di `collaudo_fasce.py` (e copia in `collaudo_impronta.py`): arrivato all'ultimo punto continua a puntarlo; uscito dall'angolo morto tiene la mura finché non ha 3,3 nodi, invece che per un tempo fisso (osservazione di Ale: chi naviga guarda la velocità, non conta i secondi). Sulla barca della 1.0.5 ridà i tempi di prima entro 2,2 s;
  - chiavi dei record e tempi dell'oro scritti a mano aggiornati in `collaudo_carriera.py`, `collaudo_carriera_esame.py`, `collaudo_carriera_intera.py`, `collaudo_competizione.py`, `collaudo_contatto_senza_colpa.py`, `collaudo_esame.py`, `collaudo_libretto.py`, `collaudo_linea.py` (che ora controlla anche la cancellazione delle chiavi della 1.0.5), `collaudo_pannello.py`, `prova_carriera.py`;
  - `collaudo_laboratorio.py` usa `hullScale` al posto di `hullK2`.
- **Collaudi lanciati qui, OK:** regate (bastone e raffiche, semi 1-6: 18 arrivi su 18, nessuna BLOCCATA), partenze, fasce, laboratorio, pannello 1360×650 e 1360×768 (eccesso 0, caratteri veri), lezioni, carriera, carriera intera, carriera con esame, competizione veloce, linea, libretto, esame, contatto senza colpa, fantasma, suggerimento, strambata 6 e 15 nodi (come prima: scuffia a 15 nodi 10 su 10), pilota senza `#collaudo` 3 su 3.
- **Prototipo del fiocco:** resta con la resistenza della 1.0.5 (`SPERIMENTALE.md`).

## 1.0.5 — i caratteri dentro il progetto

Del 16 ottobre 2026. **Il gioco appare identico al pixel**, ma non chiede più niente a Google. Su consiglio della chat del progetto: chi gioca non manda più il proprio indirizzo a Google (tema GDPR, se il gioco viene pubblicato) e il gioco funziona anche senza rete.

- **Cosa cambia.** I caratteri Barlow Semi Condensed (400, 500, 600, 700) e Source Serif 4 (400, 600) stanno nella cartella nuova `fonts/`: 10 file, 365 KB, sottoinsiemi «latin» e «latin-ext». Sono **gli stessi file** che Google Fonts mandava al browser, e le regole che li dichiarano in `index.html` sono le sue, con l'indirizzo cambiato. Tolte le tre righe che chiamavano Google.
  - «latin» copre tutti i testi del gioco, controllato carattere per carattere; le frecce e i simboli (← → ★ ⚑ ⚙ ⛵) non erano in quei caratteri nemmeno prima.
  - «latin-ext» serve per un nome con lettere straniere nell'attestato.
- **Licenze:** tutti e due sono SIL Open Font License 1.1, senza nomi riservati. Il testo è accanto ai file (`fonts/OFL-Barlow-Semi-Condensed.txt`, `fonts/OFL-Source-Serif-4.txt`), scaricato dal repository di Google Fonts.
- **Misure:**
  - impronta del gioco identica al bit con i caratteri locali e con quelli di Google, 63 scene su 63. Riferimento preso sulla 1.0.4 con i caratteri di Google, facendo passare il browser dal proxy della sandbox, solo per quella prova. L'impronta presa senza caratteri era diversa (`6d04cc5bd6d4` contro `29c1ef0eb7cd`), quindi il confronto vede i caratteri;
  - 8 foto di parti della pagina (menu del gioco libero e della carriera, pannello nei passi 1.1 e 3.5, regata, glossario, ripasso, istruzioni della prova) uguali al pixel, con la versione scritta nel menu riportata a 1.0.4 per la foto;
  - pagina aperta come un giocatore, senza niente e con `#lab`: caratteri caricati dal disco, **nessuna richiesta fuori dal disco**, nessun errore;
  - **nella sandbox, con Google bloccato, i collaudi del pannello sono validi per la prima volta**, tutti con «caratteri veri True» ed eccesso 0 px: `collaudo_pannello.py` (1360×650 e 1360×768), `collaudo_suggerimento.py`, `collaudo_quiz.py`, `collaudo_esame.py`, `collaudo_libretto.py`, `collaudo_carriera_esame.py`. Anche `collaudo_laboratorio.py` è OK.
- **Collaudi adattati:**
  - `tests/sorgente.py` copia anche `fonts/` insieme alla pagina;
  - `collaudo_esame.py` confronta l'altezza del menu con la 0.19.5, che prendeva i caratteri da Google. Nella sandbox quella pagina restava con i caratteri di riserva: 454 px contro 464,45, e il primo giro dava FALLITO. Ora la 0.19.5 riceve gli stessi caratteri locali, e le due altezze sono 464,45 tutte e due, come sul PC di Ale col vecchio collaudo.
- **Sandbox:** i due indirizzi di Google aggiunti per prova all'elenco della sandbox sono stati tolti; non servono più.

## 1.0.4 — il laboratorio della barca

Del 16 ottobre 2026. **Il gioco normale non cambia** (impronta identica al bit). Proposta, limiti misurati, criteri ed esito in `docs/PROPOSTA-LABORATORIO.md`.

- **Cos'è.** Aprendo la pagina con `#lab` in fondo all'indirizzo compare una finestra con 15 cursori sui valori della barca: velocità, virata, marcia indietro, ripartenza dall'angolo morto. Si apre e si chiude col tasto L. Serve a provare valori diversi a confronto con i video, prima dei compiti sulla barca. Non compare nel menu.
- **Con `#lab` il gioco non salva niente:** record, medaglie, fantasmi, lezioni, quiz, esame, carriera. I progressi si leggono come sempre; quello che si fa resta in memoria fino a quando si ricarica la pagina. In alto c'è l'avviso «LABORATORIO · *profilo* · niente salvataggi».
- **Profili:** per ora solo «come oggi», che è la barca del gioco. Un profilo nuovo entra solo con fonte e stato per ogni valore. Il pulsante «Esporta» scrive i valori come profilo, e ogni valore toccato a mano esce «prova a mano», «non verificato». In regata un valore cambiato cambia anche gli avversari.
- **Il motore:** sei numeri che erano scritti dentro `step()` ora sono voci di `BOAT`, con gli stessi valori: `hullK1` 4, `yawK` 4, `backMax` 1,2, `ironsA` 36, `ironsU` 0,5, `ironsYaw` 6. Sono quelli di marcia indietro e ripartenza, che un cursore altrimenti non raggiungeva.
- **Altri file:** `js/laboratorio.js` nuovo, caricato per ultimo; `LAB` in `base.js`; una condizione in `saveProgress()` e `saveGhosts()`; i tasti dentro la finestra non guidano la barca (`gioco.js`); la testata del registratore aggiunge `profilo=` e i valori cambiati; l'aggancio dei collaudi accetta anche `#collaudo-lab`; `collaudo_impronta.py` si può importare.
- **Misure:**
  - `polare.js`, `raffiche_e_virate.js` e `angolo_morto.js` identici carattere per carattere dopo lo spostamento dei sei numeri;
  - impronta identica al bit, 63 scene su 63, riferimento preso dalla 1.0.3 appena prima;
  - `collaudo_laboratorio.py` nuovo: 14 controlli su 14; 10 corse su 10 senza salvataggi, contro-prova 10 su 10 salvate;
  - `collaudo_registratore.py` OK;
  - limiti dei cursori rimisurati sul motore della 1.0.4: nessun conto in errore agli estremi, passi di tempo 1/240 e 0,0125 s uguali entro 0,1 s e 1°.
- **Difetto nel collaudo, trovato e corretto:** il caso «luffA0 33» doveva essere rifiutato, ma con `luffW` 7 la somma fa esattamente 40, che è permesso. Era sbagliato il caso, non il controllo; ora è 33 + 8.

## 1.0.3 — il codice diviso in file

Del 16 ottobre 2026. **Il gioco non cambia:** stesso comportamento, stessi testi, stesse immagini, misurato al bit. Proposta, criteri e decisione in `docs/PROPOSTA-DIVISIONE-CODICE.md`: manutenzione decisa da Claude Code, prima del laboratorio e delle correzioni della barca.

- **Com'è fatto adesso.** `index.html` contiene stile e struttura della pagina (30 KB, era 244). Il codice è in `js/`, otto file caricati in ordine come script classici: `motore.js` 6 KB, `base.js` 1, `contenuti.js` 55, `gioco.js` 57, `regate.js` 35, `disegno.js` 45, `registratore.js` 15, `avvio.js` 4. Il gioco si apre ancora con un doppio clic, senza server. Il codice è **spostato, non riscritto**: i file uniti, nell'ordine, danno esattamente il testo che stava dentro il blocco unico, che è stato tolto. L'unica aggiunta sono due righe di intestazione per file. **Uno scostamento dalla proposta:** il pannello sta in `disegno.js` e non in `gioco.js`, perché nel file stava fra le regate e il disegno, e così l'ordine resta quello di prima.
- **Nomi globali:** 292 nomi diventano globali; nessuno coincide con un nome che il browser usa già (controllato su una pagina vuota di Chromium).
- **Misure:**
  - **impronta identica al bit**, 63 scene su 63, con nessun errore della pagina; riferimento preso dalla 1.0.2 a file unico, appena prima;
  - `polare.js` e `raffiche_e_virate.js` identici carattere per carattere;
  - pilota delle lezioni (veloce) identico riga per riga;
  - nessun errore al caricamento, né con `#collaudo` né senza.

  Collaudi lanciati qui:
  - OK: `collaudo_carriera.py` (57 controlli, 0 falliti), `collaudo_pulsanti.py`, `collaudo_versione.py`;
  - NON VALIDI solo per i caratteri mancanti nella sandbox, il resto OK: `collaudo_esame.py`, `collaudo_quiz.py`, `collaudo_libretto.py`, `collaudo_carriera_esame.py`;
  - `collaudo_carriera_intera.py`.
- **Contro-prova sull'ordine dei file.**
  - Scambiare `contenuti.js` e `gioco.js` non cambia niente: al caricamento nessuno dei due usa l'altro, quindi l'ordine fra loro è indifferente.
  - Caricare `avvio.js` prima di `regate.js` invece rompe la pagina, e l'impronta ora lo dice: «NON VALIDO (la pagina non si avvia: errori ['RACES is not defined'])», con uscita 2. Prima si interrompeva con un errore tecnico.
- **Collaudi adattati:**
  - `tests/fisica/motore.js` legge `js/motore.js`;
  - aiuto comune nuovo `tests/sorgente.py`: `testo()` dà tutto il codice come un testo, `copia()` fa una copia della pagina con modifiche, per le contro-prove;
  - lo usano `collaudo_versione.py`, `collaudo_impronta.py`, `collaudo_esame.py`, `collaudo_registratore.py`, `collaudo_quiz.py`, `collaudo_libretto.py`, `collaudo_carriera.py`, `collaudo_carriera_esame.py`, `collaudo_carriera_intera.py` e `prova_carriera.py`.
- **Documenti:** `CLAUDE.md` (la mappa ora è per file, e il codice nuovo che parte all'avvio va in `avvio.js`), `PROGETTO.md`, `README.md`, `COLLAUDI.md`.
- **Conoscenze del progetto su claude.ai:** al posto di `index.html` si caricano `index.html` (ora piccolo) e i file di `js/`.

## Dopo la 1.0.2 (lavori che non cambiano il gioco)

- **Pilota completo delle lezioni** (16 ottobre 2026; proposta, revisione in chat ed esito in `docs/PROPOSTA-PILOTA-LEZIONI.md`). Collaudo nuovo `tests/collaudo_pilota_lezioni.py`: tutti i 32 passi pratici, percorsi dall'inizio come un giocatore, con tre misure («a mani ferme», «guidando», «dopo un colpo lungo»). `index.html` non è cambiato. Messa a punto sui semi 1-20 (solo il pilota: sette correzioni dichiarate), conferma sui semi 21-100 senza toccarlo: «guidando» completa 2.558 corse su 2.560. Trovati, e **non corretti** (ogni caso diventerà una proposta):
  - **«Ripartire»:** la barca esce da sola dall'angolo morto in 80 corse su 80 (osservazione 45); dopo un colpo lungo il passo è già fatto in 27 su 80.
  - **«Barra sottovento»:** già fatto dopo un colpo lungo in 3 su 80, che è l'osservazione 49 riprodotta; in più il bersaglio del testo (circa 65°) sta a 2° dal bordo della finestra (67°).
  - **«Accelerando»:** ai primi filetti dritti la barca va a 3,7 nodi; ne servono più di 4.
  - **«Assorbire una raffica»:** si completa a mani ferme in 56 corse su 80.
  - **«La scuffia»:** in 18 su 80.
  - **Casi minori:** 2.5, 1.11 e 1.12 dopo un colpo lungo.

  Contro-prove superate: condizione sempre falsa e sempre vera; pagina senza `#collaudo` 3 tentativi su 3. In `lancia_tutti.sh` tre voci nuove: `--veloce`, semi 1-100 (lungo), senza `#collaudo`.

## 1.0.2 — correzioni dalle osservazioni sulla 1.0

Del 16 ottobre 2026. Dalle osservazioni 44-54 di Ale (`OSSERVAZIONI-GIOCANDO.md`). **La fisica non cambia** (`step()` non è toccato; `polare.js` e `raffiche_e_virate.js` identici carattere per carattere). Cambiano testi, un pezzo di lezione 6, i pulsanti di fine prova e regata, l'attestato.

- **44, nomi.** «Lezione» resta alla Scuola; ripasso ed esame usano «Ripasso N»: voci del menu («Ripasso 1 · La barca e il vento»), titolo del ripasso, pulsanti dopo l'esame («Ripasso 1»), «prima i ripassi · ripassi 1 e 3», suggerimenti del libretto («Ripasso 3, Andature e filetti.»). Nell'esito dell'esame le domande sbagliate restano raggruppate per lezione (è da lì che nascono).
- **46, medaglie.** «Tempi delle medaglie: oro entro…», «Medaglia: argento.», «Nessuna medaglia: il bronzo è entro…»; il piede del menu parla della medaglia del tempo migliore.
- **49 (testo), «a piccoli colpi»** in evidenza nei passi 4 e 5 della lezione 2.
- **50, lezione 6.** Nel passo «La scuffia» la barca resta rovesciata: il tasto R non fa niente, né il pulsante né il riquadro compaiono, il suggerimento dice di premere Avanti. Il passo «Raddrizzare» parte sempre con la barca rovesciata: dopo «Ricomincia», arrivando da «Indietro», o da dritta. Prima, se si raddrizzava nel passo prima, quello dopo si completava da solo. Il passo si completa quando una barca partita rovesciata torna dritta (non più «ha scuffiato almeno una volta»). Tornando indietro da «Raddrizzare» a «La scuffia» la barca si rimette dritta: altrimenti il passo non si sarebbe più potuto completare.
- **53, pulsanti doppi.** All'arrivo di una prova restano il testo e «Prosegui» (nascosto nell'ultima prova della Scuola, dove diventava «Torna al menu», doppione di «Menu»); «Rifai» e «Rifai con altro vento» sono tolti, restano «Ricomincia la prova» e «Cambia vento» sotto. In regata all'arrivo resta solo il testo («Nuova regata» e «Con altro vento» tolti, restano «Ricomincia» e «Cambia vento»).
- **54, attestato.** Nome del gioco in grande, una deriva stilizzata disegnata da noi (SVG, nessun marchio né logo), cornice doppia con filetto, «Attestato del gioco». **Niente timbro né firma** (decisione di Ale, principio 5). Stampa in bianco e nero.
- **Collaudi aggiornati:** `collaudo_lezioni.py` (4 controlli nuovi sulla lezione 6; sul codice della 1.0.1 ne falliscono 3: il quarto vale in entrambi i casi), `collaudo_carriera.py` (K5 confronta il menu col codice della 1.0.1 invece della 0.21.6, con i due testi voluti portati al nuovo), `collaudo_libretto.py`, `collaudo_carriera_esame.py`, `collaudo_fantasma.py`, `collaudo_registratore.py` (nomi dei pulsanti).
- **`collaudo_impronta.py`:** ogni gruppo di scene in una pagina nuova. Prima lo stato globale del gioco (come la lezione 6 lascia la barca) passava alle scene dopo e cambiava l'immagine delle prove: l'impronta non attribuiva la differenza alla scena giusta. Con la 1.0.1 come riferimento, la 1.0.2 cambia **15 scene su 63**, tutte volute: testi dei passi 2.4-2.6 (`<em>`), lezione 6.4 e 6.5 (barca rovesciata), menu e finestre, testi di fine prova (5) e di fine regata (4). Nessuna differenza di stato delle barche in prove e regate, nessuna differenza di immagine tranne la 6.5.
- **Pannello a 1360×650, i sette passi che sforano.** Misura di Ale sul suo PC con la 1.0.2 senza questa correzione: i sette passi noti con gli stessi pixel (l1p7 +12, l2p4 +44, l2p6 +20, l3p5 +79, l5p3 +7, l6p2 +37, l6p4 +13) e, nella lezione 6, due numeri nuovi (passo 4 +49, passo 5 +8) che erano un difetto del collaudo, non del gioco: il collaudo mostra i passi uno dopo l'altro senza giocarli, e il passo «Raddrizzare», che ora parte rovesciato, restava rovesciato anche nel «Riepilogo» e a passo «completato» con il pulsante visibile (nel gioco, a quel punto, la barca è dritta). **Prima correzione, misurata da Ale sul suo PC:** a passo completato il suggerimento del pannello si nascondeva (tranne avvertimenti e passi con Cazza e Lasca). Da sette passi a tre: l3p5 +18 (era +79: i 61 px previsti), l5p3 +7 e l6p2 +37 invariati, perché nel collaudo, con la barca non giocata, il suggerimento è un avvertimento («Si agita il filetto sottovento»), e il suo stato dipende dall'istante della misura. **Seconda correzione (da misurare):** a passo completato il suggerimento si nasconde **sempre**, salvo barca rovesciata, sbandamento oltre 25°, barca che arretra, o passo con Cazza e Lasca (per non spostarli sotto il puntatore, difetto della 0.18.1); in più spazi del pannello un poco più stretti: margini del pannello 8/8/7 → 6/6/6 px, titolo e paragrafi della scheda −2 px ciascuno, spazio sopra i pulsanti della scheda 8 → 4 px, pulsanti 1 px più bassi. Risparmio misurato in sandbox (altezza del contenuto, indipendente dai caratteri): 20 px nel passo 5 della lezione 3 (servono 18), da 15 a 27 px negli altri passi. **Collaudo:** `collaudo_pannello.py` ora chiama il vero `completeStep()` (esposto in `__sv`), ridisegna il pannello, mette la barca rovesciata in «La scuffia» e dritta in «Raddrizzare» prima di misurare il passo completato. **Esito, misura di Ale sul suo PC (caratteri veri): eccesso massimo 0 px a 1360×650 e a 1360×768, 32 passi misurati anche da completati, «pannello che eccede: nessuno».** Il margine misurato in sandbox era di 2 px nel passo più stretto (passo 5 della lezione 3): da tenere d'occhio se si aggiunge testo ai passi. In sandbox il collaudo resta NON VALIDO (mancano i caratteri veri). Impronta contro la 1.0.2: 3 scene su 63 (lezioni 1.9, 2.3, 4.3), solo il suggerimento, dove il passo è completato.
- **Non fatto, rimandato al pilota delle lezioni:** passi che si completano da soli (osservazioni 45 e 49, seconda parte).

## 1.0.1 — giro di manutenzione del codice

Del 16 ottobre 2026. **Il gioco non cambia:** stesso comportamento, stessi testi, stesse immagini, misurato al bit. Lo scopo è spendere meno lettura a ogni sessione e avere il codice più ordinato prima del pilota delle lezioni.

- **Leggere a pezzi.**
  - Venti sottotitoli `// ---- … ----` dentro le sezioni grandi di `index.html` (contenuti, menu, modalità, regate, disegno). Con le intestazioni `// ====` già presenti formano la mappa del file; il comando che la stampa con le righe di oggi è in `CLAUDE.md`, con la regola di non leggere mai il file intero.
  - Versioni dalla 0.20 alla 0.24 spostate in `docs/archivio/CHANGELOG-0.20-0.24.md`, testo invariato: `CHANGELOG.md` da 98 KB a 12 KB. Di `COLLAUDI.md`, a inizio sessione, si legge tutto tranne la tabella dei collaudi nel browser (35 KB), da cui si prende solo la riga che serve.
  - Lettura obbligatoria a inizio sessione: da circa 158 KB a circa 40 KB.
- **Pulizia di `index.html`** (da 243.481 a 241.890 byte, −1,6 KB comprese le righe di commento nuove; la stima della proposta era 3-5 KB):
  - una sola funzione per la direzione di un punto (`bearingTo`, prima anche `brgFrom` e un calcolo scritto direttamente nel pannello); la rotazione delle prove usa `fromWF`; `changeWind` sostituito da `otherWind`, che era la stessa cosa;
  - nei meriti il punteggio di una regata si calcola una volta sola (`racePt`);
  - un solo formato «minuti:secondi» (`fmtClock`, al posto anche di `sesHms` e di due calcoli nell'orologio della regata) e un solo `p2` per le date;
  - `font()` al posto della stessa riga ripetuta 24 volte nel disegno; `releaseKeys()` al posto di due comandi ripetuti 6 volte; scia (`drawWakeOf`) e punta delle frecce (`shaftHead`) disegnate da una sola funzione;
  - tolti: il ripiego per i browser senza `<dialog>`, il parametro `quiet` mai usato, il tema scuro forzato con `data-theme` che nessuno attivava (resta quello automatico), un `Math.sin(0) * 0` nella bussola, i controlli «se la prova ha le fasce» (le hanno tutte).
- **Due sospetti dalla revisione.**
  - *Disegno che cambia la regata:* la classifica, chiamata dal disegno e dal pannello, cambia il punto di passaggio degli avversari alla boa (`targetOf`). Misurato: la stessa regata con e senza la classifica a ogni passo dà gli stessi arrivi e le stesse posizioni in **160 regate su 160** (semi 1-10 per la scelta, 11-40 di conferma; 2 regate × 2 livelli). Il cambio dipende solo dalla posizione della barca. Contro-prova: un numero casuale in più a ogni passo cambia 8 regate su 8, quindi il confronto vede le differenze. Annotato nel codice, nessuna correzione.
  - *Mure giudicate col vento del giocatore:* quando un avversario decide se un'altra barca è mure a dritta, e quando si assegna la colpa di un contatto, si usa il vento che c'è dove si trova il giocatore, non quello sul posto. Con le raffiche, vicino alla prua al vento, le mure possono risultare sbagliate. **Non corretto**, perché cambierebbe le regate: va con le regole di regata (`ROADMAP.md`, punto 4).
- **Collaudo nuovo `tests/collaudo_impronta.py`**, per tutte le pulizie future (descrizione e contro-prove in `COLLAUDI.md`). Impronta fatta sul codice d'inizio sessione e confrontata dopo ogni gruppo di modifiche: **63 scene su 63 identiche** ogni volta. Contro-prove: costante fisica cambiata di poco → 62 scene diverse, disegno spostato di 1 mm → 12, uno spazio in un testo → 1. Due difetti del collaudo, trovati e corretti prima di usarlo: (1) due giri sullo stesso codice davano immagini diverse, perché il ciclo del browser continuava a disegnare in tempo reale fra un comando e l'altro: ora è fermo; (2) un testo cambiato nelle istruzioni di una prova non veniva visto: ora legge anche quel riquadro.
- **Non-regressione:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere; `collaudo_registratore.py` tutto OK (era legato alla modifica: usa i formati dei tempi); `collaudo_versione.py`.
- **Non fatto:** divisione in più file (decisa no, `PROGETTO.md`); revisione dei collaudi Python (circa 4.200 righe), rinviata al prossimo giro.

## 1.0 — il livello 1 completo

Del 14 ottobre 2026. **La 1.0 è la versione giocabile** (decisione di Ale): il livello 1 si gioca dall'inizio alla fine, dalle lezioni al brevetto. È la stessa barca della 0.21.6: la fisica non cambia. In `index.html` cambia solo la costante `VERSIONE`.

**Cosa contiene il livello 1:**
- sei lezioni, cinque prove a tempo con fasce, due regate contro tre avversari (principianti o esperti) o il proprio fantasma, navigazione libera;
- registro degli errori, ripassi (29 domande), esame (banca di 26 domande, 20 estratte, servono 16), glossario;
- gioco libero e carriera separati;
- in carriera: libretto dei meriti con suggerimenti, esame con voto definitivo, ripassi dopo un esame non superato, brevetto di livello 1 «Timoniere di deriva» con attestato stampabile **senza valore legale**.

**Il percorso verso la 1.0 (fase A, `PROPOSTA-ESAME-E-BREVETTO.md`):** 0.20 esame; 0.21 piazzamento e Competizione; 0.21.1-0.21.6 correzioni delle regate; 0.22 bivio; 0.23 libretto; 0.24 esame in carriera e attestato.

- **Collaudo nuovo `tests/collaudo_carriera_intera.py`** (criteri I1-I4 scritti prima del codice), aggiunto a `lancia_tutti.sh` (circa 13 s). Fa una carriera intera nella stessa pagina e nello stesso salvataggio:
  - lezioni percorse fino all'ultimo passo;
  - prove 1-4 col pilota delle fasce;
  - le due regate col pilota sostituto;
  - ripassi ed esame a clic.

  Alla fine legge solo il salvataggio. Nella sandbox, **5 giri identici**: prove 92,1 / 142,6 / 196,4 / 333,3 s (tutte oro), regate 2° e 2° al primo tentativo, meriti Abilità 16, Conoscenza 12, Competizione 6, Esperienza 6 (totale 40), esame 20 su 20, attestato comparso da solo, gioco libero non toccato. ESITO OK.
- **Limiti del collaudo, dichiarati:**
  - dei **32 passi pratici** delle lezioni se ne guidano davvero **14**; gli altri 18 si saltano con l'aggancio. Nessun collaudo dimostra ancora che ogni passo si possa completare guidando: è il primo lavoro dopo la 1.0 (`ROADMAP.md`);
  - prova 5 esclusa (il pilota la finisce 19 volte su 24);
  - il sostituto non fa regate pulite;
  - è **una** carriera, cioè un solo percorso con semi fissi, non un campione.
- **Difetto del collaudo trovato e corretto:** nella prima stesura, in un giro su tre la regata 2 finiva 4ª invece che 2ª. Il seme si fissava in un comando diverso da quello che apriva la regata, e nel frattempo il disegno consumava numeri casuali (lo stesso effetto della 0.21.1). Ora il seme si fissa nello stesso comando.
- **Documenti:**
  - `README.md` (stato e contenuti);
  - `ROADMAP.md` (fase A chiusa, ordine dopo la 1.0 deciso da Ale: pilota completo delle lezioni, resistenza dello scafo, timone e virate, regole di regata, vela, voci piccole);
  - `PIANO-GENERALE.md` (punti 3 e 4 fatti, decisioni 8 e 9 chiuse);
  - manuale (gli aiuti non cambiano i punti; semplificazioni della 1.0).
- **Non-regressione:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere; `collaudo_versione.py`.
- **Sul PC di Ale** (`lancia_tutti.sh --veloce`, 14 ottobre 2026, caratteri veri): 14 OK, 0 falliti, 13 da controllare, 5 saltati, 1298 s. I 13 «da controllare» danno i valori di sempre:
  - polare 3,4 / 5,2 / 3,5 nodi a 10 nodi; raffica a 20 nodi 55°;
  - lezioni: tutti i passi completati, salvo il caso noto «L1 cazzare (primo tratto)»;
  - regate: BLOCCATA 0, mediane 245,0 e 208,0 s; partenze: 3,3 / 4,8 / 3,6 s;
  - fasce: prove 1-4 come sempre, prova 5 finita 19 volte su 24, mediana 353,6 s;
  - strambate: 0 scuffie su 10 a 6 nodi, 10 su 10 a 15 nodi;
  - pannello a 1360×650: solo i sette passi noti; fantasma salvato.
- **Prova a mano di Ale:** carriera azzerata, prove nuove giocate e registrate nel libretto.

