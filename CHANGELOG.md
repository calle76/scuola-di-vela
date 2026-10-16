# Diario delle modifiche

I difetti sono riportati con la causa, perché ricordare come sono nati aiuta a non ripeterli.

**Le versioni dalla 0.1 alla 0.19.5 sono in `docs/archivio/CHANGELOG-0.1-0.19.md`** (spostate il 13 ottobre 2026), **quelle dalla 0.20 alla 0.24 in `docs/archivio/CHANGELOG-0.20-0.24.md`** (spostate il 16 ottobre 2026); testo invariato. I rimandi degli altri documenti a «`CHANGELOG.md`, 0.2x» si trovano lì.

## Sperimentale

Prove che **non sono versioni del gioco**: vivono in `sperimentale/` e non toccano `index.html`. Verificato a ogni passo che, per una barca a una vela sola, polare, virate e raffiche restino identiche a quelle del gioco.

- **Prototipo del fiocco** (`sperimentale/fiocco.html`), in vista di una futura deriva a due. Tappa A: il fiocco come seconda superficie portante, con scotta propria (tasti Q ed E), filetti e disegno. Tappa B: la randa che copre il fiocco alle andature larghe, e il pannello che dice chiaramente dove il fiocco non si regola. Costanti, semplificazioni e fonti in `FISICA-E-TARATURE.md` e `CONTENUTI-DA-VERIFICARE.md`. Non ci sono ancora l'upwash della randa sul fiocco, il fiocco a collo in virata e la manovra a farfalla.
- **Prototipo del fiocco, tappa C, primo compito: la vista e la forza del fiocco coperto adesso dicono la stessa cosa.** In tappa B il pannello diceva «qui non si regola (coperto dalla randa)» mentre il fiocco dava ancora dal 10% al 19% della spinta. Portare solo `slotShade` a 1,0 non bastava: fra 107° e 135° di vento apparente ne restava il 16-10%, perché lì l'ombra era ancora parziale. Ritarate tre costanti: `slotA0` 85→**95**, `slotW` 50→**12**, `slotShade` 0,70→**1,00**. L'ombra ora è nulla fino a 95° apparenti e totale da 107°, che non è un numero scelto ma l'angolo oltre il quale non esiste più una posizione del fiocco con i filetti dritti. `jibShadedAt` perde la soglia propria e diventa «`jibRange` nullo»: strumento e messaggio del pannello non possono più contraddirsi. **Misure:** quota di spinta del fiocco da 108° a 180° apparenti, grado per grado, **0,00%** (soglia dichiarata 3%); nessuna ombra fino a 95°; bolina +10,9% contro larghe +6,3% (il confronto regge); polare senza nuovi denti; nessuna bistabilità su sei andature larghe partendo da ferma e lanciata; non-regressione senza fiocco a scarto zero e uscite di `polare.js` e `raffiche_e_virate.js` identiche carattere per carattere. **Prezzo dichiarato:** la curva si irrigidisce fra 126° e 132° reali (massima variazione 0,163 nodi/° contro 0,085 in tappa B), e la prova 2 «Lasco e poppa» torna esattamente al tempo del gioco (149 s contro 145/142 della tappa B), perché su un percorso portante il fiocco ora non dà più niente. **Difetto nel collaudo, trovato e corretto:** la verifica «senza `#collaudo`» cliccava il titolo del menu invece del pulsante, il gioco non partiva e la prova passava leggendo «—» dappertutto; ora controlla di essere partita e di aver attraversato davvero le andature che dice di misurare.
- **Prototipo del fiocco, tappa C, secondo compito: il momento di imbardata dovuto alle vele non si modella, e la semplificazione è dichiarata.** Si era proposto di modellare il solo contributo del fiocco, lasciando alla randa l'equilibrio implicito nel motore. Misurato fuori dal motore, senza toccare `step()`: su 12 casi (6, 10 e 14 nodi × 45°, 70°, 90° e 110° reali) quel momento fa poggiare **12 volte su 12**, e il termine che dovrebbe far orzare sbandando non arriva mai a ribaltarlo (dal 3% al 23% dell'altro). F4 dice il contrario: barca piatta e vele regolate, la barra sta circa al centro; sbandando, la barca orza. Emulando quel momento con la barra libera, a 10 nodi la barca partita a 45° dal vento è a 75° dopo 10 s e a 124° dopo 60, cioè circa 3 °/s di scarto: ingiocabile. Il momento riguarda **tutta la barca** — randa, fiocco, scafo sbandato — e non si aggiunge a metà. Il motore non è stato toccato (`git diff` vuoto su `fiocco.html` e `index.html`). Il termine che farà girare la prua col fiocco a collo starà nel terzo compito e dovrà funzionare anche a barca ferma, dove questo valeva zero.
- **Prototipo del fiocco, tappa C, terzo compito: il fiocco a collo in virata non si modella, e la semplificazione è dichiarata.** Provati due modelli fuori dal motore, senza toccare `step()` (`git diff` vuoto su `fiocco.html` e `index.html`). Quello senza memoria del lato del fiocco è peggio di niente: resiste nella prima metà della virata e le riuscite scendono da 75 a 69 su 84. Quello con un filo di memoria funziona (`backRate` 12 °/s, `backT` 1,2 s; virata di bolina a 10 nodi da 4,35 a 3,79 s col fiocco cazzato, da 75 a 78 riuscite su 84, da 179 a 188 su 200 tentativi con seme fisso), ma è stato scartato lo stesso: in un motore cinematico è una **taratura**, con due costanti senza nessuna fonte e il verso scritto nel codice, quindi «col fiocco cazzato si vira meglio» è vero per costruzione; le soglie dei criteri erano state scritte dopo aver visto i numeri del banco, contro le regole dei prototipi; la memoria del lato del fiocco **sostituisce l'equipaggio** e andrebbe rifatta con il prodiere e le due scotte della barca a due (tappa C4); il guadagno è modesto (col fiocco lascato da 136 a 138 su 200); e si perderebbe un comportamento in navigazione libera, perché col fiocco cazzato non ci si potrebbe più fermare nell'angolo morto. **Oggi in virata il fiocco conta solo per la resistenza della vela che sbatte**, non perché vada a collo. Modello, criteri, rischi e numeri restano in `sperimentale/PROPOSTA-C3.md`, `banco_tappaC3.js` e `banco_tappaC3.txt` come registro della decisione.
- **Prototipo del fiocco, tappa C chiusa, quarto compito: la barca a due non si modella e il sovrainvelamento si dichiara.** Il prototipo resta con lo scafo e il timoniere del gioco a una vela (135 kg, un velista da 75 kg) e il 37% di vela in più: una raffica da 20 nodi fa scuffiare e a 15 nodi la virata non riesce. Il banco di confronto proposto (quattro configurazioni da 135 a 250 kg, 108 raffiche, 12 soglie di scuffia, 132 equilibri di polare, 288 virate, 36 giri nel browser) **non è stato eseguito**, perché i conti che già avevamo bastavano a decidere, e `step()` e `sperimentale/fiocco.html` **non sono stati toccati** (`git diff` vuoto). Tre ragioni: (1) la coppia raddrizzante del prototipo vale **83,7 kgf·m** al massimo, a 22,6° di sbandamento, contro i **circa 60 kgf·m** che la fonte dà a una deriva a due **senza** trapezio, quindi quella barca sarebbe **meno** stabile di questa, e l'unica configurazione che risolve il sovrainvelamento è quella **col trapezio** (circa 220 kgf·m), che per il livello 2 sarebbe una **seconda novità principale**; (2) nel motore la **massa non entra nella resistenza dello scafo**, quindi una barca più pesante andrebbe a regime più **veloce** perché sbanda meno, e per ritarare `hullK2` e `hullK4` non c'è fonte (polari pubbliche di derive non risultano, F10 non letta); (3) il **peso dell'equipaggio dovrebbe diventare un'azione del prodiere** (lezione 2.5), non l'automatismo da 0,9 s di oggi. Annotata anche, senza cambiarlo, l'incoerenza del timone: a 6 nodi il motore dà 21,2 kgf di resistenza dello scafo contro i 19 della fonte (vicina) ma solo 2,9 kgf di timone a 15° contro 12, e arriva a 10,9 solo vicino a 30°; soprattutto **la pala non stalla mai**, così la barra a fondo fa girare 1,93 volte più in fretta che a 15° ed è sempre la scelta migliore, mentre nella realtà no. Conseguenza per il gioco: **il livello 2 va giocato con vento da leggero a medio** (sopra i 12-15 nodi circa, limite da decidere con le lezioni). Con questo la tappa C è chiusa: proposta e criteri in `sperimentale/PROPOSTA-C4.md`, decisione e stato finale del prototipo in fondo a `FISICA-E-TARATURE.md`.


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

