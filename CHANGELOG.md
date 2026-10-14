# Diario delle modifiche

I difetti sono riportati con la causa, perché ricordare come sono nati aiuta a non ripeterli.

**Le versioni dalla 0.1 alla 0.19.5 sono in `docs/archivio/CHANGELOG-0.1-0.19.md`** (spostate il 13 ottobre 2026, testo invariato).

## Sperimentale

Prove che **non sono versioni del gioco**: vivono in `sperimentale/` e non toccano `index.html`. Verificato a ogni passo che, per una barca a una vela sola, polare, virate e raffiche restino identiche a quelle del gioco.

- **Prototipo del fiocco** (`sperimentale/fiocco.html`), in vista di una futura deriva a due. Tappa A: il fiocco come seconda superficie portante, con scotta propria (tasti Q ed E), filetti e disegno. Tappa B: la randa che copre il fiocco alle andature larghe, e il pannello che dice chiaramente dove il fiocco non si regola. Costanti, semplificazioni e fonti in `FISICA-E-TARATURE.md` e `CONTENUTI-DA-VERIFICARE.md`. Non ci sono ancora l'upwash della randa sul fiocco, il fiocco a collo in virata e la manovra a farfalla.
- **Prototipo del fiocco, tappa C, primo compito: la vista e la forza del fiocco coperto adesso dicono la stessa cosa.** In tappa B il pannello diceva «qui non si regola (coperto dalla randa)» mentre il fiocco dava ancora dal 10% al 19% della spinta. Portare solo `slotShade` a 1,0 non bastava: fra 107° e 135° di vento apparente ne restava il 16-10%, perché lì l'ombra era ancora parziale. Ritarate tre costanti: `slotA0` 85→**95**, `slotW` 50→**12**, `slotShade` 0,70→**1,00**. L'ombra ora è nulla fino a 95° apparenti e totale da 107°, che non è un numero scelto ma l'angolo oltre il quale non esiste più una posizione del fiocco con i filetti dritti. `jibShadedAt` perde la soglia propria e diventa «`jibRange` nullo»: strumento e messaggio del pannello non possono più contraddirsi. **Misure:** quota di spinta del fiocco da 108° a 180° apparenti, grado per grado, **0,00%** (soglia dichiarata 3%); nessuna ombra fino a 95°; bolina +10,9% contro larghe +6,3% (il confronto regge); polare senza nuovi denti; nessuna bistabilità su sei andature larghe partendo da ferma e lanciata; non-regressione senza fiocco a scarto zero e uscite di `polare.js` e `raffiche_e_virate.js` identiche carattere per carattere. **Prezzo dichiarato:** la curva si irrigidisce fra 126° e 132° reali (massima variazione 0,163 nodi/° contro 0,085 in tappa B), e la prova 2 «Lasco e poppa» torna esattamente al tempo del gioco (149 s contro 145/142 della tappa B), perché su un percorso portante il fiocco ora non dà più niente. **Difetto nel collaudo, trovato e corretto:** la verifica «senza `#collaudo`» cliccava il titolo del menu invece del pulsante, il gioco non partiva e la prova passava leggendo «—» dappertutto; ora controlla di essere partita e di aver attraversato davvero le andature che dice di misurare.
- **Prototipo del fiocco, tappa C, secondo compito: il momento di imbardata dovuto alle vele non si modella, e la semplificazione è dichiarata.** Si era proposto di modellare il solo contributo del fiocco, lasciando alla randa l'equilibrio implicito nel motore. Misurato fuori dal motore, senza toccare `step()`: su 12 casi (6, 10 e 14 nodi × 45°, 70°, 90° e 110° reali) quel momento fa poggiare **12 volte su 12**, e il termine che dovrebbe far orzare sbandando non arriva mai a ribaltarlo (dal 3% al 23% dell'altro). F4 dice il contrario: barca piatta e vele regolate, la barra sta circa al centro; sbandando, la barca orza. Emulando quel momento con la barra libera, a 10 nodi la barca partita a 45° dal vento è a 75° dopo 10 s e a 124° dopo 60, cioè circa 3 °/s di scarto: ingiocabile. Il momento riguarda **tutta la barca** — randa, fiocco, scafo sbandato — e non si aggiunge a metà. Il motore non è stato toccato (`git diff` vuoto su `fiocco.html` e `index.html`). Il termine che farà girare la prua col fiocco a collo starà nel terzo compito e dovrà funzionare anche a barca ferma, dove questo valeva zero.
- **Prototipo del fiocco, tappa C, terzo compito: il fiocco a collo in virata non si modella, e la semplificazione è dichiarata.** Provati due modelli fuori dal motore, senza toccare `step()` (`git diff` vuoto su `fiocco.html` e `index.html`). Quello senza memoria del lato del fiocco è peggio di niente: resiste nella prima metà della virata e le riuscite scendono da 75 a 69 su 84. Quello con un filo di memoria funziona (`backRate` 12 °/s, `backT` 1,2 s; virata di bolina a 10 nodi da 4,35 a 3,79 s col fiocco cazzato, da 75 a 78 riuscite su 84, da 179 a 188 su 200 tentativi con seme fisso), ma è stato scartato lo stesso: in un motore cinematico è una **taratura**, con due costanti senza nessuna fonte e il verso scritto nel codice, quindi «col fiocco cazzato si vira meglio» è vero per costruzione; le soglie dei criteri erano state scritte dopo aver visto i numeri del banco, contro le regole dei prototipi; la memoria del lato del fiocco **sostituisce l'equipaggio** e andrebbe rifatta con il prodiere e le due scotte della barca a due (tappa C4); il guadagno è modesto (col fiocco lascato da 136 a 138 su 200); e si perderebbe un comportamento in navigazione libera, perché col fiocco cazzato non ci si potrebbe più fermare nell'angolo morto. **Oggi in virata il fiocco conta solo per la resistenza della vela che sbatte**, non perché vada a collo. Modello, criteri, rischi e numeri restano in `sperimentale/PROPOSTA-C3.md`, `banco_tappaC3.js` e `banco_tappaC3.txt` come registro della decisione.
- **Prototipo del fiocco, tappa C chiusa, quarto compito: la barca a due non si modella e il sovrainvelamento si dichiara.** Il prototipo resta con lo scafo e il timoniere del gioco a una vela (135 kg, un velista da 75 kg) e il 37% di vela in più: una raffica da 20 nodi fa scuffiare e a 15 nodi la virata non riesce. Il banco di confronto proposto (quattro configurazioni da 135 a 250 kg, 108 raffiche, 12 soglie di scuffia, 132 equilibri di polare, 288 virate, 36 giri nel browser) **non è stato eseguito**, perché i conti che già avevamo bastavano a decidere, e `step()` e `sperimentale/fiocco.html` **non sono stati toccati** (`git diff` vuoto). Tre ragioni: (1) la coppia raddrizzante del prototipo vale **83,7 kgf·m** al massimo, a 22,6° di sbandamento, contro i **circa 60 kgf·m** che la fonte dà a una deriva a due **senza** trapezio, quindi quella barca sarebbe **meno** stabile di questa, e l'unica configurazione che risolve il sovrainvelamento è quella **col trapezio** (circa 220 kgf·m), che per il livello 2 sarebbe una **seconda novità principale**; (2) nel motore la **massa non entra nella resistenza dello scafo**, quindi una barca più pesante andrebbe a regime più **veloce** perché sbanda meno, e per ritarare `hullK2` e `hullK4` non c'è fonte (polari pubbliche di derive non risultano, F10 non letta); (3) il **peso dell'equipaggio dovrebbe diventare un'azione del prodiere** (lezione 2.5), non l'automatismo da 0,9 s di oggi. Annotata anche, senza cambiarlo, l'incoerenza del timone: a 6 nodi il motore dà 21,2 kgf di resistenza dello scafo contro i 19 della fonte (vicina) ma solo 2,9 kgf di timone a 15° contro 12, e arriva a 10,9 solo vicino a 30°; soprattutto **la pala non stalla mai**, così la barra a fondo fa girare 1,93 volte più in fretta che a 15° ed è sempre la scelta migliore, mentre nella realtà no. Conseguenza per il gioco: **il livello 2 va giocato con vento da leggero a medio** (sopra i 12-15 nodi circa, limite da decidere con le lezioni). Con questo la tappa C è chiusa: proposta e criteri in `sperimentale/PROPOSTA-C4.md`, decisione e stato finale del prototipo in fondo a `FISICA-E-TARATURE.md`.


## 0.24 — esame in carriera, ripassi dopo l'esame, attestato

Del 14 ottobre 2026. Fetta 5 di `docs/PROPOSTA-ESAME-E-BREVETTO.md` (proposta e decisioni nel §13). In `index.html` cambiano:
- la costante `VERSIONE` e gli stili (pulsante spento, attestato, `@media print`);
- un riquadro nuovo `#attest`;
- `renderEsito()`, la fine del ripasso e la scelta del suggerimento in `meriti()`;
- il libretto, con il brevetto e il pulsante «Attestato»;
- il pulsante dell'esame nel menu;
- le funzioni nuove `oggi`, `fmtData`, `lezElenco`, `esameBtn`, `openAttest`.

`step()`, lezioni, prove, regate e avversari non si toccano. **Nel gioco libero non cambia niente:** l'esame resta una prova, si può rifare e non si salva.

- **Esame superato in carriera: voto definitivo** (decisione di Ale). Si salva `progress.exam = { superato, voto, data }`. Nell'esito non c'è «Rifai l'esame» ma la frase «Il voto è definitivo.». Nel menu il pulsante diventa «Esame superato · 17 su 20», spento.
- **Esame non superato:**
  - si salva l'elenco delle lezioni con almeno un errore (`progress.exam.ripasso`);
  - l'esito mostra «Ripassa le lezioni in cui hai sbagliato, poi potrai rifare l'esame.» e un pulsante «Ripasso: Lezione N» per ognuna;
  - il pulsante del menu è spento e dice «Esame: prima i ripassi · lezioni 1 e 3»;
  - **un ripasso completo, con qualsiasi punteggio, toglie la lezione dall'elenco.** Decisione di Ale: «ripassa le lezioni di cui hai sbagliato le risposte e torna a fare il test». La soglia dell'80% proposta nel §3 è tolta. Un ripasso lasciato a metà non conta;
  - svuotato l'elenco, l'esame si riapre. Nel libretto il suggerimento propone quei ripassi.
- **Esame lasciato a metà** (Esc): non conta e non si salva. Durante l'esame non si vede se le risposte sono giuste.
- **Attestato:**
  - compare da solo la prima volta che si torna al menu con tutte le condizioni raggiunte (meriti, totale, esame), qualunque sia stata l'ultima. Si salva `progress.brevetto = { data }`;
  - dopo si riapre dal libretto, che dice «Brevetto ottenuto il 14 ottobre 2026. Attestato»;
  - contenuto: «Scuola di vela · Brevetto di livello 1 · Timoniere di deriva», nome facoltativo (scritto da chi gioca, salvato solo nel browser), data, voto, i quattro meriti e in evidenza «Nessun valore legale: non sostituisce un corso di vela né la patente nautica.»;
  - «Stampa» usa `window.print()`: si stampa solo l'attestato, senza pulsanti né l'etichetta del nome.
- **Collaudo nuovo `tests/collaudo_carriera_esame.py`** (criteri E1-E6 scritti prima del codice, tutto a clic, in una pagina senza `#collaudo`), aggiunto a `lancia_tutti.sh`. Nella sandbox E1-E6 passano tutti (34 controlli):
  - E1: carriera vuota, esame superato senza attestato;
  - E2: esame a 12 su 20, ripassi, poi esame a 17 su 20 e attestato;
  - E3: nome, stampa, ricarica;
  - E4: l'ultima condizione è una regata, e la scena compare una volta sola;
  - E5: gioco libero, niente salvato;
  - E6: esame lasciato a metà.

  La misura dello spazio esce NON VALIDA per i caratteri. Nella sandbox l'attestato sta fra 126 e 524 px su 650; il menu con il brevetto finisce a 582 px. Schermate: `tests/output/C_attestato.png` e `C_attestato_stampa.png`.
- **Limite di E4:** il piazzamento che mancava è scritto direttamente nel salvataggio, seguito da una ricarica della pagina; la regata non è stata corsa. La scena che compare al ritorno al menu dopo una regata vera passa dallo stesso punto (`showMenu`), ma non è provata con una regata.
- **Sul PC di Ale, con i caratteri veri** (`lancia_tutti.sh --solo carriera` e `--solo libretto`, 14 ottobre 2026): `collaudo_carriera.py`, `collaudo_carriera_esame.py` e `collaudo_libretto.py` ESITO OK. L'attestato sta fra 115 e 535 px su 650; il menu con il brevetto finisce a 593 px.
- **Prova a mano di Ale** con `prova_carriera.py`: esame non superato, il gioco elenca le lezioni da ripassare e l'esame resta chiuso finché non si fanno; poi esame superato. L'attestato si legge; nome scritto e chiuso. **La stampa non è stata provata a mano** (solo l'emulazione del collaudo).
- **Prova a mano senza giocare ore:** `tests/prova_carriera.py` apre il gioco in una finestra vera, con un profilo del browser a parte e una carriera in cui manca solo l'esame. Non è un collaudo.
- **Non-regressione:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere; `collaudo_carriera.py` OK; `collaudo_esame.py`, `collaudo_quiz.py`, `collaudo_libretto.py` senza fallimenti nella sandbox (NON VALIDA solo per i caratteri); `collaudo_versione.py`.

## 0.23 — libretto dei meriti

Del 14 ottobre 2026. Fetta 4 di `docs/PROPOSTA-ESAME-E-BREVETTO.md` (proposta e decisioni nel §12). In `index.html` cambiano la costante `VERSIONE`, otto righe di stile, la tabella `MERITI` con le funzioni `meriti()` e `librettoHtml()`, una riga del menu e l'aggancio `__sv`, che ora espone `meriti`. Nel salvataggio non si scrive niente di nuovo. `step()`, lezioni, prove, regate, avversari ed esame non si toccano.

- **Libretto, solo in carriera,** nel terzo riquadro del menu, al posto di «In arrivo» (che resta nel gioco libero):
  - quattro barre (Abilità, Conoscenza, Competizione, Esperienza), con una tacca al minimo e il numero «punti / massimo»;
  - il totale nel titolo, la riga «Regate senza errori: N su 2», una riga con tutto quello che manca e il suggerimento «Cosa potresti fare adesso».
- **I punti si ricalcolano ogni volta** da quello che il gioco salva già: tempi, stelle, ripassi, piazzamenti, lezioni. La tabella è provvisoria, da tarare giocando (§12).
- **Decisioni di Ale (14 ottobre 2026):**
  - i punti della classifica e i meriti sono due registri separati;
  - in Competizione conta **solo il piazzamento** (1° 4, 2° 3, 3° 2, 4° 1; massimo 8, minimo 3; totale massimo 46, minimo 29). Il «+1 senza errori» è tolto, perché un 3° posto pulito sembrava un 2° a pari merito (osservazione 31);
  - le regate senza errori si contano a parte, senza punti;
  - gli errori non tolgono punti: il livello 1 non deve essere troppo punitivo;
  - in carriera l'esame superato sarà definitivo (fetta 5).
- **Prima stesura rivista dopo la prova di Ale** (stesso giorno, prima del commit). Carriera con una sola prova fatta: la riga diceva «Mancano 6 punti in Conoscenza…», mentre mancava quasi tutto. Inoltre la tacca rossa del minimo sembrava un indicatore di avanzamento: in Esperienza stava in fondo, con 0 / 6. Ora:
  - niente tacca: accanto al numero c'è «servono N», in rosso finché non si raggiunge, poi in verde;
  - **una riga con tutto quello che manca**: «Ti mancano punti in Abilità, Conoscenza, Competizione ed Esperienza; poi l'esame.» Se le aree sono a posto: «Ti mancano N punti al totale», poi «Ti manca l'esame.»;
  - **«Cosa potresti fare adesso: …»**, un suggerimento concreto che cambia a ogni ritorno al menu, girando fra le aree che mancano: la prossima lezione, una prova senza fascia o non in oro, un ripasso sotto l'80%, la regata con meno punti; alla fine l'esame. Il giro non si salva.
  - Confermato l'ordine libero (Decisione 4 del 9 ottobre): niente sblocchi, si può gareggiare anche prima dell'esame.
- **L'esame non si salva ancora** (fetta 5): nella 0.23 l'ultima riga possibile è «Ti manca l'esame.».
- **Spazio a 1360×650:** è stato il punto più stretto.
  - La prima stesura sforava di 15 px. Correzione: riga più corta, libretto più compatto.
  - La versione rivista, con due righe, sforava di 12 px nel caso della Competizione. Correzione: il suggerimento dice «la Regata a bastone (con avversari)» e le righe sono un po' più strette.
  - Nella sandbox, con i caratteri di riserva e ognuna delle sette situazioni possibili, il piede del menu arriva al massimo a 636 px, **proprio al limite** (oltre, la pagina scorrerebbe). **Sul PC di Ale, con i caratteri veri** (`lancia_tutti.sh --solo libretto`, 14 ottobre 2026): `collaudo_libretto.py` ESITO OK. Nel caso peggiore il piede del menu arriva a **610 px su 650**, con 0 px di eccesso in tutte e sette le situazioni. Il giro dei suggerimenti mostra le quattro aree.
- **Collaudo nuovo `tests/collaudo_libretto.py`** (criteri L1-L4 scritti prima del codice), aggiunto a `lancia_tutti.sh`. Nella sandbox L1-L3 passano tutti:
  - L1: i giocatori A-D danno 12/8/4/6 = 30, 20/12/0/6 = 38, 14/10/6/3 = 33 e 6/6/2/6 = 20, con le righe e i suggerimenti attesi;
  - L2: 56 casi al bordo, compresi tutti i punteggi possibili dei sei ripassi;
  - L3: 17 controlli letti dal menu, in una pagina senza `#collaudo`, compreso il giro del suggerimento (quattro ritorni al menu, quattro suggerimenti diversi);
  - L4 esce NON VALIDA solo per i caratteri.
- **`collaudo_competizione.py` aggiornato**: punti senza il +1; C4 ora conta le coppie a 8 punti, cioè due primi posti, con la soglia di prima (al massimo il 10%). Esiti nella sandbox, 320 regate:

  | | C1, 1° / 2° / 3° / 4° | C2 | C3 | C4 |
  | --- | --- | --- | --- | --- |
  | Principianti, semi 1-40 (misura) | 8 (10%) / 24 / 24 / 24 | 38 su 40 (95%) | 38 su 38 | 0 su 40 |
  | Principianti, semi 41-80 (conferma) | 15 / 15 / 20 / 30 (38%) | 35 su 40 (88%) | 38 su 38 | 0 su 40 |

  Esito OK. C2 e C3 sono uguali a quelli della 0.21, come previsto: il sostituto ha finito 0 regate pulite su 320, quindi il +1 non entrava nei conti.
  - **Da notare:** C1 non è uguale a quello della 0.21 (allora 12 / 24 / 24 / 20 sui semi 1-40). La causa sono le correzioni agli avversari della 0.21.3 e 0.21.4, non questa versione. Il 1° posto sui semi 1-40 sta proprio sul bordo della fascia (10%).
  - Con gli esperti, solo riportato: 4° posto al 41% sui semi 1-40 (riga C1 «NO», come nella 0.21.3); coppie a 8 punti 0 e 2 su 40.
- **Giro completo sul PC di Ale** (`lancia_tutti.sh --veloce`, sulla prima stesura del libretto, stesso giorno): nessun fallito, i «da controllare» con i valori di sempre; `collaudo_esame.py` e `collaudo_quiz.py` OK con i caratteri veri; il pannello eccede solo nei sette passi noti. Dopo, è cambiato solo il libretto.
- **Non-regressione:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere; `collaudo_carriera.py` OK (57 controlli; il menu del gioco libero ha ancora gli stessi riquadri della 0.21.6); `collaudo_esame.py` OK nella sandbox salvo la misura con i caratteri veri.
- **Manuale:** nuove sezioni «Gioco libero e carriera» e «La carriera: cosa serve per superare il livello 1», con la tabella dei punti.

## 0.22 — bivio gioco libero / carriera

Del 14 ottobre 2026. Fetta 3 di `docs/PROPOSTA-ESAME-E-BREVETTO.md` (§7; proposta di dettaglio e decisioni nel §11). In `index.html` cambiano la costante `VERSIONE`, due righe di stile, il caricamento di progressi e fantasmi, l'intestazione del menu, «Azzera i progressi» e la funzione nuova `setModo`. `step()`, lezioni, prove, regate, avversari ed esame non si toccano.

- **Selettore «Gioco libero | Carriera»** nell'intestazione del menu, accanto a «Glossario» (stile `.seg`, lo stesso delle impostazioni). C'è solo nel menu, quindi non si cambia modalità a metà di una prova. In carriera il menu per ora è identico a quello del gioco libero: libretto, esame salvato e attestato arrivano con le fette 4 e 5.
- **Salvataggi separati.** Gioco libero: `scuolaVelaSim.v1` e `scuolaVelaGhost.v1`, come prima. Carriera: `scuolaVelaCarriera.v1` e `scuolaVelaGhostCarriera.v1`, che partono vuoti (niente importazione). L'ultima modalità scelta resta in `scuolaVelaModo`; se manca, o se il browser non salva, si parte in gioco libero. Tutto il resto del gioco scrive già in `progress` e `ghosts`, quindi non è cambiato.
- **Fantasmi separati (decisione di Ale).** Il §2 della proposta li voleva in comune. Ma il fantasma si salva a ogni record della modalità in uso, quindi la prima regata in carriera avrebbe sostituito il fantasma del gioco libero, anche se più lento.
- **«Azzera i progressi» vale solo per la modalità in uso, e ora cancella anche i suoi fantasmi.** Prima i fantasmi restavano: **questo cambia anche il gioco libero** (Ale: in fase di prova non c'è niente da conservare). La conferma nomina la modalità: «Azzerare i progressi della carriera, fantasmi compresi? Il gioco libero non cambia.» (e il contrario).
- **Difetto trovato dal collaudo e corretto prima di chiudere.** La prima stesura salvava `progress` al cambio di modalità, e così riscriveva la modalità che si lasciava: stesso contenuto, ma non gli stessi byte. Quella scrittura non serviva, perché ogni risultato è già salvato quando nasce: tolta.
- **Collaudo nuovo `tests/collaudo_carriera.py`** (criteri K1-K5 scritti prima del codice, nel §11), aggiunto a `lancia_tutti.sh`. Nella sandbox: **57 controlli, 0 falliti**. K1: 6 corse valide su 6, la prova 1 guidata dal pilota di `collaudo_fasce.py`, 3 in carriera e 3 in gioco libero, con l'altra modalità identica byte per byte. **Limite:** le 6 corse finiscono tutte in 92,1 s. La prova 1 non ha raffiche e il percorso gira col vento, quindi semi e venti diversi non cambiano la corsa: in pratica è un caso solo, ripetuto. Basta per controllare il salvataggio, non dice niente sulla guida. K2-K5 sono stati provati su una pagina senza `#collaudo`.
- **Menu a 1360×650:** nella sandbox, con i caratteri di riserva, altezza della pagina e riquadro più alto restano 650 e 454 px, come nella 0.21.6 (`collaudo_esame.py`, parte del menu); l'intestazione sta su una riga (schermata). **La misura valida, con i caratteri veri, va fatta sul PC di Ale**: `collaudo_esame.py` e `collaudo_quiz.py` qui escono NON VALIDA per i caratteri.
- **Non-regressione:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere (329 e 364 caratteri); `collaudo_versione.py`.
- **Sul PC di Ale (`lancia_tutti.sh --veloce`, 14 ottobre 2026, caratteri veri caricati):** 11 OK, 0 falliti, 13 da controllare, 5 saltati. `collaudo_carriera.py` 57 controlli, ESITO OK. Menu a 1360×650: pagina 650 px e riquadro più alto 464,5 px, come prima; ripasso ed esame con eccesso 0 px. Pannello a 1360×650: esattamente i sette passi noti; a 1360×768 nessuno. Lezioni: tutti i passi completati, salvo il caso di attesa noto «L1 cazzare (primo tratto)». Regate: BLOCCATA 0, mediane 245,0 s a bastone e 208,0 s nelle raffiche, come nella 0.21.4. Partenze: ritardo mediano 3,3 / 4,8 / 3,6 s, come nella 0.21.3. Fasce, strambate e fantasma come atteso.
- **Prova a mano di Ale:** prova giocata in carriera; tornando al gioco libero, i risultati di prima sono intatti.

## 0.21.6 — pulizia: motore e collaudi

Del 13 ottobre 2026. Il gioco non cambia comportamento.

- **Motore.** In `step()` il momento raddrizzante moltiplicava per `(Math.abs(phi) < Math.PI / 4 ? 1 : 1)`, che vale 1 in tutti e due i casi: tolto. `polare.js`, `raffiche_e_virate.js` e `angolo_morto.js` danno uscite identiche carattere per carattere prima e dopo.
- **`collaudo_lezioni.py` a passi fissi:** simulazione del browser ferma, tasti premuti dentro la pagina, `__sv.run` a passi di 1/60 s, seme fisso a ogni azione. Due giri identici in circa 3 s (prima circa 50, in tempo reale). Stessi passi, tasti e durate di prima; stessi esiti, compreso il caso di attesa noto «L1 cazzare (primo tratto)».
- **`collaudo_suggerimento.py` e `lancia_tutti.sh`:** se l'unico problema sono i caratteri del gioco non caricati, il collaudo esce con 3 invece di 1, e `lancia_tutti.sh` lo mostra come «NON VALIDO (ambiente)», con un conteggio a parte nel riepilogo, invece che come fallito. Provato nella sandbox, dove i caratteri mancano.
- **Documenti:** `OSSERVAZIONI-GIOCANDO.md`, voci 36-40 (le osservazioni di Ale sulle regate del 13 ottobre); `COLLAUDI.md`; in `PROPOSTA-RESISTENZA-SCAFO.md` i lavori di Day diventano F16 e F17, perché F14 e F15 sono ora il richiamo individuale e il regolamento di regata.

## 0.21.5 — il richiamo individuale vale anche per gli avversari

Del 13 ottobre 2026. Osservazione di Ale: un avversario partito in anticipo tornava dietro la linea e ripartiva, ma non si vedeva nessun segnale. In `index.html` cambiano la costante `VERSIONE`, la funzione `toast` (durata facoltativa) e il messaggio dello sparo. Motore e avversari non si toccano.

- **Il comportamento era già giusto.** Allo sparo ogni barca oltre la linea viene segnata come anticipata e deve tornare dietro e ripartire. Secondo la regola 29.1 del regolamento di regata (fonte F14, testo riportato) il ritorno è la penalità, e non c'è un tempo da aggiungere. Mancava solo il segnale: il messaggio parlava soltanto del giocatore.
- **Il messaggio nuovo**, nello stesso riquadro degli altri messaggi: «Partenza! Richiamo individuale: Verde deve tornare dietro la linea» (con più barche: «Verde e Blu devono…»). Se è anticipato anche il giocatore: «Partenza anticipata! Torna dietro la linea (anche Verde)». Con nomi resta 4,5 s invece di 2,6. La bandiera X non è disegnata.
- **Verifica** (sandbox, seme fisso, giocatore fermo): 120 partenze (principianti ed esperti, 1, 3 e 5 minuti, semi 1-20), 71 con almeno un avversario anticipato, messaggio giusto in 120 su 120 (tutti i nomi presenti; «Partenza!» quando non ce n'è nessuno). Schermata a 1360×650 con due nomi: il messaggio sta in una riga sopra il mare. Il caso del giocatore anticipato non è stato provato in automatico.

## 0.21.4 — gli avversari arrivati lasciano libera la linea

Del 13 ottobre 2026. Osservazione di Ale: all'arrivo gli avversari restavano sulla linea girandoci intorno, e chi arrivava dopo rischiava di urtarli o doveva manovrare per evitarli. In `index.html` cambiano la costante `VERSIONE` e sei righe all'inizio di `aiControl`. `step()` non si tocca.

- **La causa.** Dopo l'arrivo il bersaglio dell'avversario restava il punto d'arrivo sulla linea (`targetOf`), quindi ci girava intorno. Misurato sulla 0.21.3, semi 1-3, tutti e due i tipi di regata: nei 120 s dopo l'arrivo gli avversari passavano da 24 a 120 s entro 20 m dal centro della linea, e tornavano a passarci sopra (distanza minima 0 m).
- **La correzione.** Dopo l'arrivo l'avversario va in una **zona di sosta** 25 m oltre l'estremità della linea dal proprio lato (la linea è lunga 70 m) e 30 m dietro la linea, e a meno di 12 m da quel punto resta quasi fermo con la vela che sbatte, come prima del via. Le distanze sono una scelta nostra. I contatti con le barche arrivate già non contavano (`contacts()`): cambia solo l'ostacolo, non le regole.
- **Criteri, scritti prima di misurare:** per ogni avversario arrivato, nei 120 s dopo l'arrivo, al massimo 15 s entro 20 m dal centro della linea, e fra 60 e 120 s mai a meno di 40 m dal centro. Semi 1-6 per la misura, 7-30 per la conferma, tutti e due i tipi di regata.
- **Misure:** semi 1-6, 36 avversari arrivati su 36 dentro i criteri (al massimo 11 s vicino alla linea, distanza minima dopo il primo minuto 51 m); conferma 7-30, 144 su 144 (11 s, 50 m).
- **Gli altri collaudi delle regate** (sandbox): `collaudo_regate.py` nessuna BLOCCATA, mediane 245,0 / 253,0 s a bastone e 208,0 / 218,0 s nelle raffiche (semi 1-6 / 7-30); `collaudo_competizione.py` ESITO OK, principianti identici alla 0.21.3, esperti semi 1-40 (solo riportato) 12/19/16/33 contro 12/18/17/33; `collaudo_aggressiva.py` quota OK; `collaudo_partenze.py`, `collaudo_fantasma.py`, `collaudo_registro.py` (f, g, h), `collaudo_contatto_senza_colpa.py` e `collaudo_versione.py` come prima.

## 0.21.3 — l'avversaria che non partiva

Del 13 ottobre 2026. In `index.html` cambiano la costante `VERSIONE` e tre righe di `aiControl`. `step()` e il resto del motore non si toccano.

- **Il difetto.** In `collaudo_regate.py` (passi fissi e seme fisso dal 13 ottobre), regata nelle raffiche, seme 17, la Verde restava dietro la linea per oltre 400 s e arrivava a 884 s (le altre a 189 e 327 s). Probabilmente è il blocco annotato nella 0.21.2 («da tenere d'occhio», causa non stabilita).
- **La causa** (traccia secondo per secondo). La barca era sulla mura sbagliata rispetto al bordo voluto e quasi ferma (0,1-0,27 m/s). Due regole lasciavano scoperta la fascia fra 40° e 44° dal vento: «piantata» (sotto 40° in partenza, sotto 0,6 m/s: poggia) e «mai virare da fermi» (sotto 1,1 m/s, prima poggia: ma solo **oltre 44°**). La barca tentava la virata, scendeva sotto 40°, la prima regola la riportava appena sopra, e ricominciava, ogni 2 s circa.
- **La correzione.** «Mai virare da fermi» usa la stessa soglia di «piantata» (40° in partenza, 44° dopo; prima 44° sempre).
- **Misure** (sandbox, collaudi a seme fisso, criteri scritti prima nella proposta):
  - seme 17, regata nelle raffiche: la Verde arriva a 222 s (prima 884 s, fuori dai 600 s del collaudo);
  - `collaudo_regate.py`: nessuna BLOCCATA, semi 1-6 e conferma 7-30, tutti e due i tipi (prima una, seme 17). Mediane d'arrivo degli avversari: bastone 245,5 s (semi 1-6, prima 247,5) e 252,5 s (7-30, prima 253,5); raffiche 208,0 s (prima 208,0) e 218,5 s (prima 227,0);
  - `collaudo_competizione.py`: ESITO OK, C0-C5 OK nei gruppi con soglie. Nel gruppo «esperti, semi 1-40», solo riportato e senza soglie, il quarto posto passa dal 29% al 41% (riga C1 «NO»). Confronto con la 0.21.2 per i quattro gruppi (chi quadrato con permutazioni): p fra 0,42 e 0,78, quindi dentro il rumore dei semi;
  - `collaudo_partenze.py`: ritardo mediano 3,3 / 4,8 / 3,6 s con 1, 3 e 5 minuti (prima 3,3 / 4,2 / 3,1); con 5 minuti tutti partiti (prima 2 su 30 non partiti entro 60 s); distanza e avvicinamento minimi invariati;
  - `collaudo_aggressiva.py`: quota OK, 10 / 9 / 10 / 10 su 10 e in conferma 40 / 39 / 40 / 40 su 40;
  - `collaudo_fantasma.py`, `collaudo_registro.py` (casi f, g, h), `collaudo_versione.py`: come prima;
  - `polare.js` e `raffiche_e_virate.js`: motore non toccato, uscite identiche.

## 0.21.2 — correzioni piccole

Del 13 ottobre 2026. Quattro voci (osservazioni 23, 29, 30 e la scelta delle parole per la barra). In `index.html` cambiano: `VERSIONE`, 16 righe di testo («spingi/spinge la barra» diventa «sposta»), `contacts()`, `sesTick` e la legenda del file del registratore, una voce del glossario. `step()` non si tocca.

- **A. «Spingi la barra» → «sposta la barra».** passi delle lezioni 2 e 5 (anche «Una virata che non riesce»), descrizione della lezione 2, domande del ripasso e d'esame con risposte e spiegazioni (per l'esame le 6, 7, 8 e 22 di `CONTENUTI-DA-VERIFICARE.md`), voce «Barra» del glossario, suggerimento dal vivo («…spostala verso il boma…»). «non con una spinta lunga» diventa «non con un colpo lungo». Restano «la vela spinge», «il vento spinge», «la spinta» (propulsione) e «tirare la scotta». Il significato non cambia. Aggiornate le stringhe di `collaudo_suggerimento.py` e i documenti `CONTENUTI-DA-VERIFICARE.md` e `COLLAUDI.md`; le citazioni storiche (questo diario) restano com'erano.
- **B. Testo del contatto (osservazione 29).** In `contacts()`, `v(tu, lui)`: «Contatto con X: tu eri mure a sinistra e dovevi lasciare strada…» al giocatore, «Contatto: X era … doveva …» per l'avversario.
- **C. Registratore, regate (osservazione 30).** Evento `arrivo` col tempo netto (`fin`, penalità comprese) una volta sola per regata; evento `regata_in_corso lato N t=Ns` se la registrazione si accende a regata già partita (la partenza non si inventa); nessuno dei due se si accende dopo l'arrivo. Sola lettura, formato 1; legenda aggiornata. `collaudo_registratore.py`, parte `e`.
- **D. Frecce e disegno (osservazione 23).** Voce «Segnavento» nel glossario, blocco «Cosa si vede sul mare» nel manuale, scritti dall'elenco letto nel codice (nessun testo nuovo a video). Ale ha confermato con uno zoom (13 ottobre 2026) che i tratti scuri sono boma, barra e timone, più la linea corta traversale vicino all'albero (albero inclinato visto dall'alto).
- **Prova a mano di Ale (13 ottobre 2026):** regata con contatto con colpa sua (mure a sinistra contro mure a dritta, prima del via): testo «tu eri… dovevi…», `errore contactsPen +1`, riga errori colorata, nessuna ★, `arrivo 310s` una volta sola, tempo netto uguale al pannello. Lezione 2 in finestra normale: il pannello esce in verticale e scorre con la barra laterale (osservazioni 34 e 35). Rotellina non provata.
- **Etichetta dell'opzione strumenti:** «Nel pannello, anche fuori dalle lezioni, i numeri di vento reale e apparente, sbandamento e scarroccio» (prima «Tutti gli strumenti nel pannello anche fuori dalle lezioni (venti, sbandamento, scarroccio)»). L'opzione agisce solo sul pannello: verificato che i pixel del canvas non cambiano. Il disegno non cambia; il segnavento resta sempre disegnato.
- **Manuale, quattro righe nuove in «Cosa si vede sul mare»:** sbandamento (il mezzo cerchio in basso a sinistra), scarroccio (si legge dalla freccia «velocità»), la linea scura corta traversale vicino all'albero (albero inclinato visto dall'alto, verso sottovento) e il pallino arancione (il timoniere, che si sporge da solo).
- **Collaudo:** `collaudo_registro.py`, caso h, non deterministico (vedi COLLAUDI.md): 2 fallimenti su 11 sul PC di Ale, 0 su 20 nella sandbox; il resto, 14 casi su 15 la prima volta e poi 9 su 9, e la parte e del registratore passano.
- **Da tenere d'occhio:** in un rilancio di `collaudo_regate.py` a bastone una regata si è bloccata (Verde, tratto 2); 36 corse successive (18 sul codice nuovo, 18 su HEAD) senza blocchi. Causa non stabilita, possibile legame con l'osservazione 27, non provato. Il pacchetto non tocca il motore né le IA.

## 0.21.1 — i contatti senza colpa non contano

Del 13 ottobre 2026. Osservazione 28 di `docs/OSSERVAZIONI-GIOCANDO.md`, decisione di Ale. In `index.html` cambiano: la costante `VERSIONE`, `regTotal()`, `regText()`, il riepilogo di fine regata e le righe del registratore (`sesTick`, legenda del file). `step()` e il resto del motore non si toccano; `polare.js` e `raffiche_e_virate.js` escono identici carattere per carattere a quelli della 0.21.

- **Il conteggio.** `regTotal()` somma `reg.contactsPen` (contatti con colpa del giocatore) al posto di `reg.contacts` (tutti i contatti). Un contatto senza colpa non toglie la «pulita», la stella né il bonus +1 della Competizione. Il punto 31 (4° pulita = 3° non pulita) non si tocca.
- **Il testo.** Il contatto senza colpa resta scritto: «Errori: nessuno (1 contatto senza colpa, non conta)»; con errori veri: «Errori: 1 contatto con penalità · 2 contatti senza colpa, non contano». Il riepilogo di fine regata con «pulita» scrive la nota e poi «★ senza errori». La riga in alto si colora di rosso solo se c'è un errore vero.
- **Il registratore** (formato 1, sola lettura): il contatto senza colpa esce come evento nuovo `contatto_senza_colpa +N`, descritto nella legenda del file; il contatto con colpa come `errore contactsPen +N`; non esce più `errore contacts` (che sembrava un errore anche quando la penalità era dell'avversario). `collaudo_registro.py` e `collaudo_registratore.py` leggono `reg` e non quelle righe, quindi non cambiano.
- **Nessun salvataggio cambia.** `progress.clean` viene solo messo a `true`, mai tolto: stelle e «pulita» già salvate restano. Il cambio vale dalle regate giocate da ora.
- **Collaudo nuovo:** `tests/collaudo_contatto_senza_colpa.py` (costruito e guidato, vedi `docs/COLLAUDI.md`).
- **Correzione del seme nel collaudo nuovo:** `__seed(seme)` viene richiamato subito prima dei passi, nello stesso `evaluate` di `__sv.run` (A2 e B). Prima ogni frame del browser tra seme e passi consumava 2 `Math.random` in `draw()` e, col tempo reale, le stesse regate davano esiti diversi da un rilancio all'altro (8 regate su 12 in 5 rilanci).
- **Limite annotato** (`ROADMAP.md`, «Dopo la 1.0»): la colpa si decide solo con mure e posizione, quindi un contatto provocato da sottovento con le stesse mure costa al giocatore solo il rallentamento e 15 s all'avversario.

## 0.21 — piazzamento salvato e taratura della Competizione

Del 12 ottobre 2026. Fetta 2 di `docs/PROPOSTA-ESAME-E-BREVETTO.md` (§7). In `index.html` cambiano tre punti: la costante `VERSIONE`, il salvataggio del piazzamento in fondo a `updateRace` e il pilota sostituto nell'aggancio `__sv`, che esiste solo con `#collaudo`. `step()` è identica byte per byte alla 0.20.3 (3.726 byte); le uscite di `polare.js` e `raffiche_e_virate.js` sono identiche carattere per carattere (329 e 364 caratteri). Non toccati: `step`, `BOAT`, `bands`, `MISSIONS`, `aiControl`, `aiParams`, `targetOf`, `startSpots`, `startRace`, `raceLegs`, `contacts`, `ranking`, `QUIZ`, `openQuiz`, il testo di fine regata, record, stelle, fantasmi e `KEYV`.

- **Piazzamento salvato (decisione di Ale: strada B minima).** All'arrivo di una regata con avversari il gioco salva `progress.race[chiave] = { pos, n, pulita }`, con chiave `recK("r"+i) + ":" + livello` (per esempio `r0.2:principianti`, `r1.2:esperti`). Il campo `race` si crea se manca, come `quiz`. Con «nessuno» non si salva niente. Record, stelle e fantasmi restano con la chiave di prima, quindi non si azzera niente; il record dei tempi resta mescolato fra i livelli (annotato in `ROADMAP.md`, «Dopo la 1.0»).
- **Piazzamento definitivo.** Non si salva all'istante dell'arrivo: lì `ranking()` mette dietro chi non è ancora arrivato, anche se poi arriverà con un tempo netto migliore (`fin = R.t + pen`). Si salva quando tutte le barche sono arrivate, oppure quando `R.t` raggiunge il mio `fin`: da lì in poi chi taglia la linea ha per forza un tempo netto non migliore del mio. Di solito succede subito; con una penalità si aspettano al massimo i secondi della penalità. «Pulita» si legge al mio arrivo (`regTotal() === 0`).
- **Il migliore per chiave.** Se per quella chiave c'è già un valore, si tiene quello con più punti: 4/3/2/1 per 1°/2°/3°/4°, +1 se pulita; a parità resta quello vecchio. La formula vale per flotte di 4 barche, come oggi.
- **Limite dichiarato:** se il giocatore lascia la regata prima del salvataggio (menu, «Nuova regata», «Ricomincia», «Cambia vento», chiusura della pagina), il piazzamento si perde. Succede solo nei secondi di penalità dopo l'arrivo.
- **Il testo di fine regata non cambia.** Il suo «N° su 4» è quello dell'istante dell'arrivo e con le penalità può essere ottimistico (annotato in `ROADMAP.md`, «Dopo la 1.0»). Nel collaudo differisce dal piazzamento finale in 19 regate su 80 (semi 1-40) e in 24 su 80 (semi 41-80), con i principianti.
- **Pilota sostituto** (`__sv.pilota`, solo con `#collaudo`): la guida degli avversari principianti (`aiControl` con `aiParams("principianti")`) sulla barca del giocatore. Il pilota aggiunge i campi che le mancano (`ai`, `side`, `boardT`, `boardMax`, `rOff`, `char` «normale», `startX` = metà della posizione iniziale), le passa la lettura istantanea (`info`) e, solo durante la chiamata, segna la barca come avversaria, così `targetOf` le dà gli stessi bersagli degli avversari (tre punti per il giro di boa). Dopo 1 s di scuffia raddrizza: **ipotesi nostra**, un giocatore che preme il tasto (gli avversari si raddrizzano da soli dopo 5 s). `aiControl`, `aiParams` e `targetOf` non sono cambiati. Controllato che `applyInput()` non sovrascriva la barra in regata: con le impostazioni normali (`autoCenterComp` spento) non la tocca. Nella prova della prima fermata, 30 regate, l'unico punto che cambiava la barra era il raddrizzamento dopo una scuffia (`ctl.tiller = 0`).
- **Nuovo `tests/collaudo_competizione.py`.** Criteri scritti prima dei risultati, nella proposta e nel via di Ale, **non cambiati dopo**:
  - C0: arrivate almeno il 90% delle regate per tipo (bastone, raffiche); sotto, la misura non vale e ci si ferma;
  - C1: ogni piazzamento 1°-4° fra il 10% e il 40%, contato sulle regate arrivate dei due tipi insieme (questa interpretazione, «i due tipi insieme», è nostra, scritta nel collaudo prima di lanciarlo);
  - C2: coppia seme k (regata 1 + regata 2), almeno 3 punti in almeno il 60% delle coppie; regata non finita = 0 punti;
  - C3: finestre scorrenti di 3 semi consecutivi (1-3, 2-4, …), che **si sovrappongono** e quindi non sono indipendenti: il migliore dei 3 per ogni regata, somma almeno 3, in almeno il 90% delle finestre;
  - C4: 10 punti in al massimo il 10% delle coppie;
  - C5: regate arrivate e coppie stampate, fallisce se zero; il sostituto deve aver mosso la barra in ogni regata.

  Semi 1-40 per la misura, semi 41-80 per la conferma (mai guardati prima). Poi gli stessi semi con gli esperti, solo riportati. Ogni regata in un contesto nuovo del browser, quindi con il salvataggio vuoto, `Math.random` a seme fisso, `simTime` a zero, `fast(0)`, passi di 1/60 s, 3 minuti di preparazione. Il piazzamento si legge da `localStorage` e si confronta con un calcolo indipendente dai tempi netti: **0 differenze**. Con «nessuno» (sostituto, regata a bastone, seme 1) `progress.race` non esiste.
- **Risultati, avversari principianti** (nella sandbox; due giri completi identici riga per riga, 6 min 22 s):

  | | Semi 1-40 (misura) | Semi 41-80 (conferma) |
  | --- | --- | --- |
  | C0 arrivate, bastone | 40 su 40 (100%) | 40 su 40 (100%) |
  | C0 arrivate, raffiche | 40 su 40 (100%) | 40 su 40 (100%) |
  | C1 1° / 2° / 3° / 4° su 80 arrivate | 12 (15%) / 24 (30%) / 24 (30%) / 20 (25%) | 10 (12%) / 18 (22%) / 26 (32%) / 26 (32%) |
  | C2 coppie con almeno 3 punti | 38 su 40 (95%) | 35 su 40 (88%) |
  | C3 finestre con almeno 3 punti | 38 su 38 (100%) | 38 su 38 (100%) |
  | C4 coppie a 10 punti | 0 su 40 (0%) | 0 su 40 (0%) |
  | C5 regate arrivate, coppie, barra mossa | 80, 40, 80 regate su 80 | 80, 40, 80 regate su 80 |

  Tutti dentro le soglie. **Ma tre avvertenze:**
  - **il sostituto non ha mai finito una regata pulita: 0 su 320** (principianti ed esperti, tutti i semi). Il «+1 senza errori» **non è misurato**;
  - per questo **C2 e C3 sono misurati senza il bonus**: è una stima prudente, perché un giocatore che fa regate pulite prende più punti;
  - **C4 con zero regate pulite è soddisfatto per forza**: 10 punti richiedono due primi posti puliti, quindi **C4 non ha misurato niente**. Il massimo trovato è 8.
- **Errori del registro del sostituto**, in quante regate compare ciascuno (su 80 per gruppo):

  | Errore | Princ. 1-40 | Princ. 41-80 | Esperti 1-40 | Esperti 41-80 |
  | --- | --- | --- | --- | --- |
  | Scuffie | 40 | 39 | 41 | 41 |
  | Strambate a vela aperta | 80 | 80 | 80 | 80 |
  | Piantato | 18 | 24 | 23 | 24 |
  | Boe sbagliate | 0 | 1 | 0 | 1 |
  | Contatti | 71 | 75 | 75 | 69 |
  | Partenza anticipata | 0 | 1 | 1 | 1 |
  | Fuori linea | 16 | 14 | 9 | 16 |

  Le strambate a vela aperta compaiono in tutte le regate: è il modo in cui strambano gli avversari (lo fanno anche loro, ma per loro il registro non conta).
- **Con gli esperti** (solo riportato): arrivate 80 su 80 e 80 su 80; 1°/2°/3°/4° 13/22/22/23 (semi 1-40) e 8/25/21/26 (41-80); coppie con almeno 3 punti 38 e 36 su 40; finestre 38 su 38 e 38 su 38; coppie a 10 punti 0 e 0. Il piazzamento all'arrivo differisce da quello finale in 15 e 18 regate su 80. Con gli esperti il sostituto fa circa come con i principianti, coerente con «esperti solo poco più forti» (`PROGETTO.md`, limiti noti).
- **Pagina senza `#collaudo`** (`--tastiera`): un pilota da tastiera legge il pannello (prua, rilevamento, scotta, barra, classifica) e il conto alla rovescia disegnato sul mare, in tempo reale, 1 minuto di preparazione, regata a bastone, le due regate in parallelo. **Scelta dichiarata:** il vento è **fisso da nord** e non si legge dal pannello, perché il pannello scrive l'angolo del vento **senza segno** (`readI`). Il gioco non è stato toccato per farlo passare. Esito:
  - **con avversari**: arrivato e salvato `r0.2:principianti = { pos: 4, n: 4, pulita: false }` in 3 giri su 3 (una prova di diagnosi più i due tentativi), `window.__sv` indefinito;
  - **con «nessuno»**: **non arrivato in nessuno dei due tentativi** (12 minuti l'uno). Nel primo è rimasto in «partenza anticipata»; nel secondo è rimasto circa 5 minuti fermo prima del via a 44-48° dal vento andando all'indietro, ed era in poppa verso l'arrivo allo scadere. Esito **NON VALIDO**: **non provato in automatico, lo prova Ale a mano.** Il controllo «con "nessuno" niente» resta coperto solo dalla parte con `#collaudo`.
- **Modifiche fatte durante il lavoro, tutte al pilota da tastiera e dopo averlo visto fallire** (nessuna ai criteri C0-C5 né al sostituto):
  1. il segno del vento: prima ricavato dal pannello, sbagliato perché il pannello lo dà senza segno; ora vento fisso da nord;
  2. la barra si inverte quando la barca va all'indietro, come in `aiControl`;
  3. da piantato lasca la scotta;
  4. l'ora del via e la distanza dalla linea si ricordano fra una lettura e l'altra (prima, se il conto non era stato disegnato negli ultimi 80 ms, il pilota partiva subito);
  5. le due regate in parallelo, per stare nei 12 minuti a tentativo.
- **Durate** (sandbox): `--veloce` 8 s; misura completa 6 min 22 s; `--tastiera` 12 min.
- `tests/lancia_tutti.sh`: tre righe nuove: veloce (esito chiaro, sempre), misura (esito chiaro, lunga, saltata con `--veloce`) e tastiera (da controllare, lunga). Controllato con `bash -n`.
- **Documenti:** `docs/COLLAUDI.md`, `docs/ROADMAP.md` («Dopo la 1.0»: testo «N° su 4» ottimistico con le penalità, record dei tempi mescolato fra i livelli), `docs/PROPOSTA-ESAME-E-BREVETTO.md` (decisione B minima, esito della fetta 2).
- **Prove a mano di Ale (12 ottobre 2026).** Regata a bastone, preparazione 1 minuto, solo `r0.2:principianti`.
  - Con «nessuno»: arrivato, in `progress.race` niente. **Superata.**
  - Principianti, 4° non pulita: salvato `{pos 4, n 4, pulita false}`.
  - Poi 4° pulita: salvato `{pos 4, n 4, pulita true}` (da 1 a 2 punti). Sostituzione con un risultato migliore: **superata.**
  - Poi 3° non pulita (2 punti, parità): resta `{4, 4, true}`. A parità resta il vecchio: **superata.**
  - Poi 4° non pulita in 8 min 11 s (1 punto): resta `{4, 4, true}`. Un risultato peggiore non sostituisce il migliore: **superata.** Questo caso non è coperto da nessun collaudo automatico, perché ogni regata del collaudo parte da un salvataggio vuoto.
  - Il piazzamento salvato coincide con l'elenco finale (tempi netti, penalità comprese) in tutte le regate. Il caso «N° su 4» all'arrivo diverso dal finale non è stato riprodotto a mano: resta coperto solo dal collaudo.
  - Provato solo `r0.2:principianti`: non provati `r1.2`, gli esperti, la regata nelle raffiche.
  - Con questo, la parte «nessuno» senza `#collaudo`, NON VALIDA in automatico, è provata a mano.


## 0.20.3 — collaudo del suggerimento ripetibile

Del 12 ottobre 2026. Solo collaudi: **il gioco non cambia**. In `index.html` cambiano due righe: la costante `VERSIONE` e due voci dell'aggancio `__sv`, che esiste solo con `#collaudo` nell'indirizzo (`panel`, per scrivere il riquadro del suggerimento a comando, e `set simTime`, per far partire ogni prova dallo stesso vento). `step()` è identica byte per byte alla 0.20.2 (3.726 byte); le uscite di `polare.js` e `raffiche_e_virate.js` sono identiche carattere per carattere (329 e 364 caratteri); senza `#collaudo` `window.__sv` è indefinito (controllato dal collaudo stesso).

- **Il difetto.** `tests/collaudo_suggerimento.py` non era ripetibile: in 8 giri (4 sul codice prima della 0.20.2, 4 dopo) le uscite nel gioco libero andavano da 193 a 199 su 200, con 11 e 19 prove fallite su 800, indistinguibili dal rumore. Cause: il pilota girava in tempo reale (`setInterval` di 15 ms, simulazione mossa dal ciclo del browser a velocità 4); il riquadro si aggiornava ogni 0,1 s di tempo **reale**; le raffiche nascevano una volta sola e continuavano da una prova all'altra; `simTime`, che muove l'oscillazione del vento, non si azzerava mai. Durava circa 14 minuti.
- **Il collaudo nuovo.** Ogni prova delle parti che guidano la barca (3c, 3e-3i) gira tutta dentro una sola chiamata alla pagina: seme fisso di `Math.random`, gioco riaperto, `simTime` a zero, passi fissi di 1/60 s (`__sv.run`), riquadro scritto ogni 0,1 s simulati (`__sv.panel`) e letto solo se visibile, tasti veri. Versione veloce con i semi 1-2 (quella di sempre), versione lunga con i semi 1-20 (`--lungo`); semi decisi prima dei risultati. Criteri della 3c, scritti prima dei risultati: K0 ripetibilità (4 prove rifatte in ordine inverso danno risultati identici); K1 un testo «all'indietro» entro 0,5 s dal primo istante all'indietro; K2 da 40° in su solo il secondo testo, sotto 40° prima il primo e poi il secondo; K3 nessun ritorno al primo testo con la prua da 37° in su; K4 uscita con la regola del 5.4 (prua ad almeno 40°, barca avanti, tenuta 1 s) entro 30 s; K5 1 nodo entro 30 s e B sparito entro 0,5 s da lì; K6 la prua non va mai oltre 10° dall'altra parte del vento locale. Ogni gruppo deve aver misurato tutte le prove previste, non solo più di zero.
- **K6 misura il suggerimento con un pilota perfetto**, che spinge sempre verso il boma. Non contraddice la regola del 5.4: nel gioco l'uscita sull'altra mura resta valida (0.20.2).
- **Modifiche a criteri e piloti fatte DOPO aver visto i risultati**, in ordine:
  1. **Fine del controllo `amin`.** Prima: la prua non doveva scendere più di 3° sotto la partenza (dalla 0.20.1). Ora: tolto; l'attraversamento del vento lo controlla K6. Perché: la soglia dipendeva dalla partenza (42-43° nei casi 4 e 5, più severa dei 40° del gioco; 22° nel caso 3, più larga) e si misurava su finestre diverse nella 3c e nella 3e. Risultato che l'ha motivata: 197-199 uscite su 200 nei giri della 0.20.2, con la prua scesa a 38-41° nel caso 4 per le raffiche, mentre la barca usciva davvero.
  2. **Fine della tenuta di 3 s.** Prima: nel gioco libero l'uscita andava tenuta 3 s (aggiunta nella 0.20.2, anche quella dopo i risultati). Ora: la tenuta di 1 s della regola del 5.4, più K5 (1 nodo). Perché: un solo criterio d'uscita, quello del gioco.
  3. **Parte 3e, «passo completato» solo se la fase 1 scatta (opzione 1).** Prima: il passo 5.4 doveva completarsi in tutte le 20 prove. Ora: conta solo nelle prove in cui scatta la fase 1 del passo (barca piantata per 1 s, `index.html:647`, ricalcolata dal collaudo con la stessa condizione; se il gioco completa il passo e il ricalcolo dice di no, è un errore); le altre sono «non misurate», stampate, e devono essere esattamente quelle attese. Risultato che l'ha motivata: 2 prove su 20 fallite al primo giro (caso 5, 46°, scotta 50, due mure): il pilota cazza subito e la barca resta sotto −0,1 m/s solo 0,87 s (0,93 s a 45°) contro la soglia di 1 s, partendo da uno stato forzato dal collaudo.
  4. **Riscaldamento di 60 s.** Prima: ogni prova partiva subito dopo l'apertura del gioco libero. Ora: 60 s simulati di gioco (valore fissato prima dei risultati), poi la barca è rimessa nello stato del caso (prua, velocità, scotta, barra, sbandamento; raddrizzata e senza fasi del suggerimento); la posizione resta quella raggiunta. Difetto che l'ha motivato: con il seme e `simTime` azzerato le 4 raffiche iniziali, in posizioni fisse (`index.html:904`), non raggiungevano mai la barca durante la prova (a fine prova erano a 15-90 m): in ognuno dei 10 gruppi i 20 semi davano lo stesso tempo di uscita, la versione lunga ripeteva 20 volte le stesse 20 prove e la contro-prova P2 (isteresi tolta) dava 0 errori, cioè il collaudo era cieco sull'isteresi.
  5. **Caso 7 (controllo: barca nuova a 43° e 0,5 nodi, B mai).** Prima: ogni prova in cui la barca arretrava era «non misurata» e il conteggio doveva essere pieno. Ora: le non misurate si contano e si stampano a parte; il gruppo è valido se le prove sono tutte e B non compare in nessuna misurata; ogni prova è stampata con lo stato a 5 s. Risultato che l'ha motivata: nella lunga 68 misurate su 80; nelle altre 12 (semi 7, 15 e 19) una raffica fa arretrare la barca da 3,73-4,15 s fino a −0,23 nodi. B non compare in nessuna delle 80.
  6. **Caso 8, nuova definizione di `tA`.** Prima: `tA` era il primo istante con prua ≥ 37° e sotto 1 nodo, anche all'indietro. Ora: il primo istante, dopo l'inversione, con la barca che va avanti (`S.u > 0,05`), prua ≥ 37° e sotto 1 nodo; si stampa anche `tAu`, il primo `S.u > 0,05`, che cade sempre a 0,02 s, quando la prua è ancora a 30-36° e B per costruzione non si vede (`index.html:2040`). Risultato che l'ha motivata: nella lunga 78 su 80, perché in 2 prove (seme 7, mure a sinistra) la barca tornava ad arretrare dopo `tA` e il gioco mostrava giustamente il primo testo.
  7. **Caso 8, il pilota segue il riquadro dopo aver centrato a 37°.** Prima: dopo i 37° il pilota centrava e reagiva solo a B dopo `tA`. Ora: fa quello che legge, come il pilota della 3c (testo A: freccia verso il boma; secondo testo o B: centra e tiene ↑). Risultato che l'ha motivata: con la definizione del punto 6, 14 prove su 80 non misurate (e 2 su 8 nella veloce); tracciate: in tutte la barca torna ad arretrare (da 1,18-2,73 s, fino a −0,66/−0,91 nodi) perché il pilota non cazza, mentre il riquadro dice di cazzare (B per 1,1-1,7 s in 10 prove su 14, poi il testo A).
  8. **Caso 8, correzione del blocco di centraggio (errore del pilota).** Prima: il blocco che centra a 37° girava a ogni lettura e annullava la freccia appena premuta, così con il testo A la barra restava a −0,16 invece di andare a fondo. Ora: centra una volta sola (`!centrato`). L'errore c'era già nelle 78 prove misurate del punto 7, tutte giuste prima e dopo. Risultato che l'ha motivata: 2 prove non misurate (seme 7, 30°, mure a dritta) con la barra ferma a −0,16 per 6,5 s.
  9. **Caso 8, `t1` senza `tB`.** Prima: `t1` (1 nodo) si misurava solo dopo B. Ora: è il primo istante a 1 nodo. Il controllo di B viene prima nella catena, quindi l'esito non cambia: cambia solo il valore stampato nelle prove senza B.
- **Limite noto della scotta.** A 46° dal vento la fase 1 del 5.4 dipende da quanto cazza il giocatore. Misura su `step()` sola (barra al centro, vento 10 nodi, nessuna azione): con la scotta a 50 o 100 il boma si ferma a circa 44-46°, alpha 2°, spinta da −4,5 a −3 N, e la barca arretra (−0,28 nodi a 5 s, −0,69 a 40 s): la fase 1 scatta a 4,22 s partendo da ferma, a 13,48 s partendo da 1 nodo; con la scotta a 25 o 10 la spinta è positiva (+23,7 e +56,3 N a regime) e la fase 1 non scatta mai, anche partendo da −0,5 nodi. Annotato in `CONTENUTI-DA-VERIFICARE.md`, «Da sistemare dopo la 0.20».
- **Risultati sul codice attuale** (nella sandbox; i caratteri del gioco non sono quelli veri, quindi la misura del pannello è «NON VALIDO», come nelle versioni precedenti):
  - veloce: 3c 40 prove, K1-K6 0 errori, uscita in 2,32-6,15 s simulati; 3d 10 su 10; 3e 18 misurate e 2 non misurate (quelle attese), 0 errori; 3f 12 su 12; caso 6 8 su 8; caso 7 8 misurate, 0 non misurate, B mai; caso 8 8 su 8, tB − tA 0,00-0,07 s; 3i B sparisce a 10,0 s (4 su 4); nessun ritorno al primo testo; pannello 0 px;
  - lunga: 3c 400 prove, K1-K6 0 errori, uscita in 2,05-6,45 s; caso 6 80 su 80; caso 7 68 misurate, 12 non misurate, B mai; caso 8 80 su 80, tB − tA 0,00-0,08 s; il resto come la veloce;
  - il seme conta: 10 gruppi su 10 con almeno 2 tempi di uscita diversi (soglia 5);
  - tempi reali, collaudo intero: veloce 30,0 s, lunga 51,3 s (prima circa 14 minuti).
- **Contro-prove**, su copie fuori dal repository, con il criterio che deve fallire scritto prima di lanciarle:
  - P0, due giri della veloce: uscite identiche carattere per carattere (4.646 caratteri);
  - P1, pilota con la freccia lontano dal boma: K6 fallisce in 16 prove su 40 (casi 1 e 3, gli unici con il primo testo);
  - P2, senza isteresi (`IRONS_A - 3` → `IRONS_A`): K3 fallisce in 1 prova su 40 nella veloce e in 4 su 400 nella lunga;
  - P3, `index.html` della 0.20.1 con l'aggancio aggiunto: K1 della 3e fallisce in 20 su 20, caso 6 0 su 8 («non risultava all'indietro»), caso 8 0 misurate (non valido);
  - P4, testo B spento: casi 6 e 8 0 su 8 («B non comparso entro 0,5 s»).
- **Cosa si perde.** Il percorso in tempo reale (ciclo del browser, pilota rallentato da un computer carico) e il passo variabile del gioco: il collaudo usa sempre 1/60 s. Il pilota legge ogni 0,1 s e non sbaglia lato: è più bravo di un giocatore.
- `tests/lancia_tutti.sh` non è cambiato: lancia la versione veloce; la lunga si lancia a mano (`docs/COLLAUDI.md`).
- **Documenti:** `docs/COLLAUDI.md`, `docs/CONTENUTI-DA-VERIFICARE.md` (fase 1 del 5.4 a 46°; testo B mentre la barca si ferma).

**Correzioni ai collaudi dopo la 0.20.3** (documenti, testi di `tests/lancia_tutti.sh` e `tests/collaudo_partenze.py`; gioco, avversari e versione invariati):
- **Pannello, esito atteso.** A 1360×650 l'atteso diceva «pannello che eccede: nessuno», ma i sette passi completati noti dalla 0.20.2 eccedono. Ora a 1360×650 l'atteso è esattamente quei sette passi, eccesso massimo 79 px, e qualunque altro passo è un problema nuovo; a 1360×768 resta «nessuno». In `lancia_tutti.sh` le due dimensioni hanno ora due note separate. Il codice del collaudo non è cambiato.
- **Fasce, numeri di riferimento.** I numeri non coincidevano fra documenti, PC e sandbox:

  | | Prova 4 | Prova 5, finite su 24 | Prova 5, mediana |
  |---|---|---|---|
  | Documenti | 333,4 s | 18 | 353,2 s |
  | PC, 6 giri della suite identici | 333,3 s | 19 | 353,6 s |
  | Sandbox, 5 giri della prova 5 | 333,4 s | 21 / 18 / 20 / 20 / 20 | 354,4 / 354,6 / — / 353,6 / 353,7 s |

  Prove 1-3 uguali dappertutto. Nella sandbox la prova 5 cambia da un giro all'altro nonostante il seme fisso; la causa non è verificata. Scelta di Ale: i valori di riferimento sono quelli del suo PC, con una nota sulla sandbox, in `docs/COLLAUDI.md`, `tests/lancia_tutti.sh` e `docs/PROPOSTA-ESAME-E-BREVETTO.md`.
- **Partenze anticipate, nuovo criterio (decisione di Ale).** Il vecchio conteggio di `collaudo_partenze.py` contava gli avversari ancora segnati come anticipati circa 60 s dopo il via, in tempo reale e senza seme. A quel punto chi è partito presto è già tornato dietro la linea, quindi non contava le partenze anticipate allo sparo. Il numero «0 su 90 con gli esperti» della 0.17 veniva da lì.
  - **Etichetta rinominata** in «ancora segnate come anticipate a +60 s», calcolo invariato. Le uscite salvate prima di questa correzione dicono «partenze anticipate» (riepilogo) e «anticipate» (righe delle singole partenze).
  - **Nuova parte «anticipi allo sparo»**, sempre lanciata, anche con `--veloce`:
    - semi 1-20, 3 avversari, principianti ed esperti, 1, 3 e 5 minuti;
    - ogni prova in una pagina nuova, in una sola chiamata: seme fisso, `simTime` a zero, passi fissi di 1/60 s, giocatore fermo.
  - **Primo criterio, abbandonato:** allo sparo al massimo 10 m oltre la linea, più il ritorno dietro la linea entro 60 s. **I 10 m li aveva scelti Claude dopo aver visto i dati** (massimo 8,8 m nella prima misura, 9,4 m sui semi 1-20 della parte nuova). **Sui semi 21-100 non ha retto**: due casi con i principianti, 10,3 m (Verde, seme 24, 3 minuti) e 17,7 m (Rossa, seme 74, 5 minuti, passata sulla linea 80,6 s prima dello sparo).
    - Verde ha passato la linea a circa 49 m dal centro, fuori dalla zona del freno; quando lo sparo arriva è rientrata a 30,3 m. I 49 m vengono da una traccia fatta fuori dal repository.
    - Rossa allo sparo è a 138,2 m dal centro.
    - La riga «oltre 10 m» stampa la distanza dal centro al momento dello sparo. Il motivo è nel codice: gli avversari frenano a 7 m dalla linea solo entro 40 m dal centro (`index.html:1714`). Fuori da quella zona nessun codice limita lo sconfinamento.
  - **Criterio attuale (decisione di Ale): boccia solo il ritorno.**
    - FALLITO se una barca anticipata non torna dietro la linea entro 60 s.
    - NON VALIDO con meno di 10 anticipate o meno partenze misurate del previsto per livello. Il minimo di 10 è stato scelto prima di rilanciare.
    - Metri oltre la linea, frequenza e anticipo si stampano ma non bocciano. La riga «oltre 10 m: N su M anticipate» elenca i casi con la distanza dal centro della linea e non boccia.
    - Il codice di uscita non dipende dal verdetto.
  - **`--lungo`:** la stessa parte con i semi 1-100, per riprodurre dal repository i numeri dei semi 21-100. Il modo normale, anche con `--veloce`, resta 1-20.
  - **Numeri dei semi 1-100:** anticipate 184 su 900 con i principianti (20,4%) e 230 su 900 con gli esperti (25,6%); tutte di nuovo dietro la linea, al più tardi in 30,1 s.
  - **Prima misura a parte**, script fuori dal repository, con un altro generatore casuale, senza `simTime` a zero e con la pagina libera di avanzare fra una chiamata e l'altra: 37 su 180 con i principianti (20,6%), 51 su 180 con gli esperti (28,3%), oltre la linea 0,5-8,8 m.
  - **Parte nuova**, tre giri identici, circa 135 s nella sandbox:

    | | Principianti | Esperti |
    |---|---|---|
    | Anticipate | 40 su 180 (22,2%) | 54 su 180 (30,0%) |
    | Anticipo, min / mediana / max | 0,25 / 14,02 / 16,38 s | 4,85 / 13,71 / 19,08 s |
    | Oltre la linea | 0-9,1 m | 1,1-9,4 m |
    | Ritorno dietro la linea | 2,1-9,8 s | 2,1-13,1 s |

    Esito `OK`, sia con il primo criterio sia con quello attuale. Gli esperti anticipano più dei principianti: annotato in `docs/CONTENUTI-DA-VERIFICARE.md`, gioco non toccato.
- **Avvicinamento minimo a 5 minuti sotto i 14 m attesi** in due giri recenti della parte senza seme: 8 m nella sandbox e 3,1 m sul PC di Ale (14,4 m nella suite veloce della stessa mattina). Non è riproducibile: annotato in `docs/CONTENUTI-DA-VERIFICARE.md`, da misurare con semi fissi; nessuna causa verificata. Gioco non toccato.
- **Registro.** `collaudo_registro.py` esegue 15 verifiche: 15 su 15 nella sandbox, lanciato da solo. `tests/lancia_tutti.sh` diceva «13 su 13», ora «15 su 15», come `docs/COLLAUDI.md`. Un primo giro fatto mentre giravano altre misure ha dato 14 su 15: è fallito il contatto, poi riuscito 3 volte su 3 da solo. Quel caso va in tempo accelerato, con `fast`, e dipende dal carico del computer; la causa non è verificata.

## 0.20.2 — lezione 5: suggerimento quando la barca arretra, passo 5.4 in due fasi, arrivo a linea nel 5.5

Dell'11 ottobre 2026, dalle registrazioni di Ale `sessione-20261011-1041.txt` (lezione 5, 0.20.1) e `sessione-20261011-1259.txt` (lezione 5, prima versione della 0.20.2). **Il motore non cambia**: il blocco di `step()` è identico byte per byte alla 0.20.1, e le uscite di `polare.js` e `raffiche_e_virate.js` sono identiche carattere per carattere.

- **Il difetto.** Nella registrazione la barca va all'indietro in quattro episodi, ma il suggerimento «Stai andando all'indietro…» compare una volta sola, a 226,7 s, nel passo 5.5. **Causa:** gli altri tre episodi sono nel passo 5.4, che ha `hintKind: "none"`, e la riga che nasconde il riquadro nei passi a suggerimenti spenti lo nascondeva anche lì. Il testo veniva calcolato ma restava invisibile. **Non era il testo di fine passo**, che sta in un riquadro a parte. L'ordine delle condizioni del suggerimento era giusto.
- **Correzione:** il suggerimento «all'indietro» compare anche nei passi a suggerimenti spenti, ma solo se il passo dà la barra. Vale per 5.4, 5.7, 5.8 e per «Poggi e laschi» e «Orzi e cazzi» della lezione 3. Non compare nei passi senza barra: «Da fermi» della lezione 4 e i primi tre passi della lezione 3.
- **Suggerimento «all'indietro» in due tempi**, dopo la seconda registrazione. Lì la barca è rimasta all'indietro per 15 s, fra 178 e 194 s, con la prua a 45° e la scotta a 100. La barra era stata centrata quando la prua era a 44-45°, mentre la barca arretrava ancora. Il suggerimento di allora («Spingila verso il boma; centrala quando riparti») non diceva di cazzare. Ale ha notato: «in bolina stretta sembra non ripartire». Quando invece ha cazzato (a 106,0, 194,0 e 283,4 s), la barca è andata avanti in 2-3 s.
  - Prua sotto 45° dal vento, barca che arretra: «Stai andando all'indietro: la barra funziona al contrario. Spingila verso il boma.» (82 caratteri)
  - Prua a 45° o più, barca che arretra: «Stai andando all'indietro, ma la prua è fuori dall'angolo morto: centra la barra e cazza.» (89 caratteri)
  - La soglia è la stessa della regola d'uscita del 5.4 (45°). Resta valido il limite «solo nei passi che danno la barra».
  - **Misura sul motore.** Griglia: prua da 0° a 44° ogni 2°, due mure, partenza a 0, −0,5, −1, −1,5 e −2 nodi, vento 6, 10 e 14 nodi, scotta 100 e 50; sono 1.350 partenze per momento, con la regola d'uscita del 5.4. La barra va verso il boma finché la barca arretra, poi al centro. Per cazzare, la scotta va a 30 alla velocità del tasto ↑ (0,27 al secondo).

    | Quando si cazza | Ripartono | Uscita: mediana / massimo | Prima volta avanti: mediana / massimo | Fermi |
    |---|---|---|---|---|
    | (a) appena la prua è a 45° | 1.350 su 1.350 | 4,8 / 10,3 s | 3,9 / 9,3 s | 0 |
    | (b) quando la barca smette di arretrare | 1.350 su 1.350 | 5,8 / 20,0 s | 4,8 / 19,0 s | 0 |
    | (c) mai | 1.350 su 1.350 | 5,8 / 24,4 s | 4,8 / 23,4 s | 0 |
    | (a2) due tempi, quello del suggerimento: barra verso il boma sotto 45°, poi al centro e si cazza | 1.350 su 1.350 | 5,7 / 11,7 s | 4,7 / 10,7 s | 0 |

    Il caso della registrazione: prua a 45° e 46°, scotta 100, −0,5 nodi, vento 10 nodi, due mure.
    - **Barra al centro, non cazza:** resta ferma a −0,7 nodi dopo 60 s.
    - Barra al centro e cazza subito: esce in 4,4-4,5 s.
    - Due tempi: esce in 4,4-4,5 s.

    Tenendo la barra verso il boma finché la barca arretra si esce sempre, anche senza cazzare; cazzare però accorcia il caso peggiore da 24,4 a 10,3-11,7 s. Il testo da 104 caratteri «…Spingila verso il boma; poi centrala e cazza.» è stato scartato: nella sandbox occupa 3 righe, i due testi nuovi 2.
- **Passo 5.4 «Una virata che non riesce» in due fasi.** Prima il passo si completava appena la barca si piantava; nella registrazione è successo con la barca ancora a +0,2 nodi, prima che arretrasse.
  - Fase 1 è la condizione della 0.20.1: barca piantata, tenuta 1 s.
  - Fase 2: la prua torna ad almeno 45° dal vento e la barca va avanti, tenuta 1 s.
  - **L'uscita sull'altra mura conta**: nessuna fonte dice che sia sbagliata. Va confermata con un velista esperto o altre fonti.
- **Testi del passo 5.4.**
  - Il testo del passo diventa: «Ora senza abbrivio: lasca la vela finché la barca scende sotto 1 nodo, poi prova a virare. Se non rallenti abbastanza, orza fino alla bolina, con la vela lasca.»
  - Nel testo del passo passa anche la parte su come uscire: «Quando la barca si pianta nel vento comincia ad arretrare. Per uscirne: spingi la barra verso il boma e la prua si allontana dal vento; quando la prua è fuori dall'angolo morto, centra la barra e cazza: la barca riparte.» Nella prima versione della 0.20.2 la fine era «quando la barca smette di arretrare, centra la barra, cazza e riparti».
  - Il testo di fine passo resta come spiegazione: «La barca si è piantata nel vento: senza velocità il timone non fa effetto, e quando la barca arretra la barra funziona al contrario. Per questo si vira sempre con la barca lanciata.»
  - **Perché la frase nuova:** al traverso, con la vela tutta lascata, la barca non scende mai sotto 1 nodo. È misurato sul motore a 10 nodi di vento, partendo a 4,1 nodi:
    - 1,58 nodi a 90° dal vento (nella registrazione 1,6);
    - 1,12 nodi a 75°;
    - sotto 1 nodo da 70° in giù, dopo 6-19 s.

    Il passo comincia al traverso dopo «Ricomincia» e quando ci si torna da un passo di pausa.
- **Passo 5.5 «Risalire il vento»: l'arrivo è una linea**, come nelle prove dalla 0.19. **Rivista la decisione della 0.19** («Lezione 5 invariata», `docs/PROPOSTA-LINEA-E-VISTA.md`).
  - La linea è 110 m controvento dal punto in cui comincia il passo, 12 m per lato (`FIN_HALF`), perpendicolare alla direzione dalla partenza del passo all'arrivo.
  - Usa la stessa `finCross` delle prove, al posto della distanza di 12 m dalla boa. Passando fuori dagli estremi compare il messaggio «Fuori dalla linea: passa tra le due boe».
  - Testi: «L'arrivo è controvento: non puoi puntarlo direttamente», «Raggiungilo a zig-zag…», «Arrivo tagliato. La scia…».
  - Le tre boe della navigazione libera restano.
- **Collaudi** (nella sandbox; i caratteri del gioco non sono quelli veri).
  - `collaudo_suggerimento.py`, nuove parti 3d e 3e.
    - **3d:** una tabella fissa di 10 passi di lezione, con la barca che arretra a 1 nodo. 10 passi misurati su 10, nessuno sbagliato.
    - **3e:** il pilota delle registrazioni nel passo 5.4. Escono 12 su 12 (tre casi, due mure, scotta 100 e 50).
    - **Contro-prova sulla 0.20.1:** la 3d fallisce in 5 passi su 5 a suggerimenti spenti con la barra; nella 3e il suggerimento non compare mai, in 12 su 12.
    - **Difetto del collaudo trovato e corretto:** il pilota leggeva il testo del riquadro anche quando era nascosto, e sulla 0.20.1 «usciva» lo stesso. Ora legge solo il riquadro visibile. Le 120 uscite della parte della 0.20.1 restano 120 su 120.
  - `collaudo_suggerimento.py` con il suggerimento in due tempi. Il pilota fa quello che legge: barra verso il boma, poi barra al centro e ↑ tenuto finché resta il secondo testo. C'è un caso 4 dalla registrazione 0.20.2 (prua a 45°, scotta 100, −0,5 nodi) e una parte 3f: la barca arretra già sopra 45° (46°, 50° e 55°, due mure, nel gioco libero e nel 5.4) e il primo testo che compare deve essere il secondo.
    - Tabella dei passi: 10 su 10.
    - 5.4: 16 uscite su 16.
    - 3f: 12 casi su 12 giusti.
    - Passaggio dal primo al secondo testo letto in 120 prove su 120 (casi 1-3).
    - Pannello: 0 px con i due testi.
    - **Cambio di criterio fatto DOPO aver visto i risultati, non una soglia invariata.** Con la regola del 5.4 (almeno 45° dal vento e barca che va avanti), nel gioco libero le uscite sono state 158, 159 e 160 su 160 in tre giri. Le prove lente o senza uscita erano quasi tutte del caso 4. Tracciate: la barca ripartiva davvero, 1-3 nodi in avanti, ma navigava di bolina a 41-44° dal vento per le raffiche.
      - **Criterio nuovo, solo nel gioco libero (parte 3c):** conta come uscita anche «barca che va avanti con la prua fuori dall'angolo morto per 3 s simulati». Il limite dell'angolo morto è `IRONS_A = 40` (`index.html:1127`), lo stesso della rosa (`ANDATURE`, primo settore fino a 40°).
      - Nel 5.4 (parte 3e) e nel gioco resta la regola dei 45°.
      - Aggiunto un caso 5 a 46°. Il caso 4 resta a 45°, perché è il caso della registrazione.
      - **Risultati:** 200 uscite su 200 nel gioco libero, in 1,2-8,5 s; 20 su 20 nel 5.4.
      - **Contro-prova** con il criterio nuovo, cioè lo stesso pilota con la freccia dalla parte opposta (tre casi su una mura e il caso 3 sull'altra): non esce in 4 su 4.
    - **Controllo che fallisce ancora, non modificato:** «partenza da 45° in su: si deve vedere solo il secondo testo». Fallisce nel caso 4 (45°) in 26 prove su 40 e nel caso 5 (46°) in 1 su 40. Con le raffiche la prua scende per un attimo sotto 45° mentre la barca arretra ancora, e compare il primo testo. È uno sfarfallio del gioco sulla soglia, annotato come possibile isteresi in `DUBBI-E-RICERCHE.md`; il gioco non è stato toccato. La parte 3f (46°, 50° e 55°, letto il primo testo che compare) passa 12 su 12.
  - `collaudo_registro.py`, riscritto il caso del 5.4. Il pilota gira a passi fissi dentro la pagina:
    - fase 1 con la prua nel vento;
    - fase 2 con la barra verso il boma (4 partenze: 60° e 90° dal vento, due mure): completate 4 su 4, sulla stessa mura;
    - fase 2 con la barra lontano dal boma (4 partenze): completate 4 su 4, tutte sull'altra mura.
    - **Durata in più rispetto alla 0.20.1**, contata dal momento in cui la 0.20.1 completava il passo: 6,2 s verso il boma e 8,8-8,9 s lontano dal boma, in tempo simulato. Nella registrazione di Ale era circa 4-10 s.
    - Le partenze sulle due mure danno tempi identici, perché il motore è simmetrico e senza caso: le partenze diverse sono in pratica 2.
    - `i`: 7 su 7.
  - `collaudo_linea.py`, nuova parte 3. Un pilota bordeggia nel passo 5.5 e il collaudo ricalcola la linea per conto suo. Partenze:
    - dentro: 10 partenze (spostate di 0, ±30 e ±60 m, due mure), tutte completate con taglio fra −4,8 e +4,8 m dal centro e 4-7 virate;
    - fuori: 4 partenze, taglio a 21,7-28,2 m dal centro; il passo non si completa, compare il messaggio, poi la barca rientra e completa;
    - contrario: 4 partenze, nessun completamento.

    In tutto: 234 casi misurati, 0 sbagliati, 8 verifiche su 8. Schermata del 5.5: linea a scacchi fra due boe arancioni, scritta «Arrivo» e freccia fuori schermo «110 m».
  - `collaudo_pannello.py` misura ora ogni passo anche **da completato**, con testo di fine passo e «Avanti» visibili: 32 passi. Il 5.4 completato ha 0 px di eccesso (71 px liberi, nella sandbox). **Misura sul PC di Ale, caratteri veri, 1360×650:** sette passi completati eccedono: lezione 1 passo 7 +12 px, lezione 2 passo 4 +44, lezione 2 passo 6 +20, lezione 3 passo 5 +79, lezione 5 passo 3 +7, lezione 6 passo 2 +37, lezione 6 passo 4 +13. A 1360×768 nessuno. Gli stessi sette valori nei giri delle 14:21 e delle 21:34. Nella sandbox, coi caratteri sbagliati, se ne vedevano solo due (+3 e +7 px): quei numeri non valgono. **Non sono dovuti alla 0.20.2:** erano nascosti perché prima lo stato «completato» non veniva misurato, quindi non c'è un confronto sul PC con la 0.20.1. **Da sistemare**, nessun intervento in questa versione (`docs/CONTENUTI-DA-VERIFICARE.md`, «Da sistemare dopo la 0.20»).
  - `collaudo_lezioni.py`: 15 su 16, con il caso di attesa noto («L1 cazzare (primo tratto)» in un giro). Un primo giro lanciato insieme a un altro collaudo aveva 5 passi della lezione 1 non completati, con la barca scuffiata: rilanciato da solo è tornato come sulla 0.20.1, perché il collaudo va in tempo reale.
  - `collaudo_esame.py`: banca valida, giusta più lunga in 3 su 26. Nessuna domanda nomina la boa del 5.5.
  - `collaudo_versione.py`.
- **Domanda d'esame 22 allineata al passo 5.4.** Il passo accetta l'uscita sull'altra mura, ma due risposte sbagliate della domanda erano proprio quella uscita: «Spingi la barra lontano dal boma, come per poggiare andando avanti» e «Orzi ancora, finché il vento passa dall'altra parte». Le ho tolte; nessuna fonte dice che quell'uscita sia sbagliata. La giusta diventa «Spingi la barra verso il boma, poi centri e cazzi» (prima «Spingi la barra verso il boma e la centri quando riparti»: non diceva di cazzare, come il suggerimento di allora). Resta anche «Muovi la barra di continuo da un lato all'altro».
  - Risposte sbagliate nuove: «Cazzi e lasci la scotta di continuo, senza toccare la barra» e «Tieni ferma la prua con la barra, senza farla girare». **Sono sbagliate solo per misura nel gioco: nessuna fonte ne parla.**
  - Spiegazione: «Andando all'indietro la barra funziona al contrario: spinta verso il boma, la prua si allontana dal vento. Quando la prua è fuori dall'angolo morto si centra la barra e si cazza, e la vela torna a spingere. Finché la prua resta nel vento, la vela non può spingere la barca in avanti.» Non parla dell'altra mura.
  - **Misura sul motore**, con la griglia delle risposte sbagliate di `angolo_morto.js`: prua da 0° a 44° dal vento, due mure, da 0 a −2 nodi, vento 6, 10 e 14 nodi, scotta 100 e 50, 60 s. La regola di uscita è quella del 5.4: almeno 45° dal vento e barca che va avanti, tenuto 1 s. Ogni risposta è misurata due volte: con la scotta ferma come nella griglia, e con un giocatore che cazza a 30 quando la prua arriva a 45°.

    | Risposta | Scotta ferma | Giocatore che cazza |
    |---|---|---|
    | «Cazzi e lasci la scotta di continuo, senza toccare la barra» (ogni secondo, barra al centro) | 0 su 1.620 | 0 su 1.620 |
    | «Tieni ferma la prua con la barra, senza farla girare» (correzione graduale o barra a fondo) | 0 su 1.620 | 0 su 1.620 |
    | controllo: «Muovi la barra di continuo», cambio ogni secondo | 26 su 1.620, come nella 0.20.1 | — |

  - **Nota sulla riga di riferimento.** Con la stessa griglia anche «barra a fondo lontano dal boma, tenuta» dà 0 uscite su 1.620, in tutti e due i modi. Eppure nel 5.4 quella uscita riesce: 4 su 4 sull'altra mura in `collaudo_registro.py`, dove il pilota centra la barra dopo che la prua ha attraversato il vento. La griglia tiene la barra lontano dal boma anche dopo l'attraversamento: il boma passa dall'altra parte, la barra con lui, e la prua torna nel vento. **Questa griglia non misura l'uscita sull'altra mura.** Per questo sono state scartate, anche con 0 uscite, «barra a piccoli colpi dalla parte opposta al boma» e «barra a metà dalla parte opposta al boma».
  - **Altre candidate scartate:**
    - «Tieni la prua nel vento con la barra finché la barca riparte»: 0 su 1.620, ma quasi uguale alla «Tieni ferma la prua»;
    - «Tieni la barra al centro finché arretri, poi la spingi verso il boma»: 0 su 1.620, ma ambigua; è la sequenza che nella registrazione di Ale ha funzionato (barra al centro per 14 s, poi verso il boma);
    - «barra verso il boma tenuta anche dopo», 1.612 su 1.620;
    - «barra verso il boma finché arretra, poi lontano», 1.620 su 1.620.
  - La domanda resta «da confermare con un velista esperto o altre fonti».
  - Corretto il dato della 0.20.1 «barra lontano dal boma: non esce in nessuna delle 60 prove». Quel collaudo contava solo l'uscita sulla stessa mura e fermava la prova dopo circa 12 s; lasciata fare, la barca esce sull'altra mura. Corretto anche in `DUBBI-E-RICERCHE.md`, sez. 3.
- **Terza registrazione (`sessione-20261011-1432(3).txt`, lezione 3, passi 3.11 e 3.12): soglia unica di 40°, isteresi, testo B.** Decisioni di Ale dopo una proposta con misure. Tutto resta dentro la 0.20.2, senza una 0.20.3 separata. **Questa voce sostituisce** le soglie di 45° e i testi scritti più sopra per il suggerimento e per il 5.4.
  - **Cosa mostrava la registrazione.**
    - Nel 3.11 la barca riparte in avanti a 44° e 0,3 nodi (382,7 s) e non compare nessun aiuto. A 384,7 s Ale preme ← a 37° con 0,4 nodi in avanti.
    - Nel 3.12, a 431,5 s, la barca arretra a −1,1 nodi con il primo testo visibile, e Ale spinge per 0,7 s dalla parte opposta al boma. Quest'ultimo è un errore di lato con l'aiuto già sullo schermo: non è stato affrontato (vedi «dopo la 1.0»).
  - **Soglia unica di 40°** (`IRONS_A`): rosa, voce Andatura, registro, suggerimento e regola d'uscita del 5.4. Prima il suggerimento e il 5.4 usavano 45°. Scartati i 45° per tutto: il motore naviga fra 40° e 44° (da 1,3 a 4,7 nodi). Tabella dei costi in `FISICA-E-TARATURE.md`, «Da tenere presente»: misura sul solo motore, si esce circa 1 s più tardi, 1.404 su 1.404, nessuna ricaduta.
  - **Isteresi:** dal secondo testo si torna al primo solo sotto 37°. Lo stato sta in `S.indietro` (0 niente, 1 barra verso il boma, 2 centra e cazza, 3 avanti piano). È aggiornato a ogni passo di simulazione da `backCheck()`, fuori da `step()`, e si azzera con una barca nuova e in scuffia.
  - **Testi:**
    - fase 1, «All'indietro la barra funziona al contrario: spingila verso il boma, poi centrala e cazza.» (89 caratteri);
    - fase 2 invariata;
    - **B**, «Ora vai avanti piano: barra al centro, cazza e lascia prendere velocità.» (71 caratteri). Compare solo dopo un episodio all'indietro, con la barca che va avanti sotto 1 nodo e la prua ad almeno 37°. Si vede anche nei passi a suggerimenti spenti che danno la barra.
  - **Passo 5.4:** secondo paragrafo accorciato, per i +18 px misurati da Ale a 1360×650: «Se la barca si pianta nel vento, arretra. Per uscirne spingi la barra verso il boma: la prua si allontana dal vento. Fuori dall'angolo morto centra la barra e cazza: la barca riparte.» La regola d'uscita è ora prua ad almeno 40° e barca che va avanti, tenuta 1 s.
  - **Motore:** il blocco di `step()` è identico byte per byte; le uscite di `polare.js` e `raffiche_e_virate.js` sono identiche carattere per carattere.
  - **Collaudi**, con i criteri dichiarati nella proposta prima dei risultati. Misure nella sandbox, con caratteri non veri.
    - `collaudo_suggerimento.py`:
      - il controllo sul testo «da 40° in su solo il secondo testo», esteso al caso 2 (42°), **passa**: 0 errori su 40 nei casi 2, 4 e 5 (prima 26 su 40 nel caso 4 e 1 su 40 nel caso 5);
      - ritorni al primo testo con la prua da 37° in su: 0; sotto 37°: 0;
      - casi 1 e 3: primo testo e poi il secondo in 80 prove su 80;
      - 5.4: 20 su 20;
      - 3f: 12 su 12;
      - caso 6: 40 su 40;
      - caso 7: B mai, in 40 prove misurate su 40;
      - pannello: 0 px con i tre testi.
    - **Controllo che fallisce, non modificato:** nel gioco libero escono **198 prove su 200**. Le due che mancano sono del caso 4 (45°, mure a sinistra): scotta 100 seme 3 e scotta 50 seme 10. La barca esce, ma durante l'uscita la prua scende a 41° e a 38° dal vento: il criterio della 0.20.1 non ammette più di 3° sotto la partenza. Con l'isteresi il secondo testo resta fra 37° e 40°, e il pilota tiene la barra al centro invece di spingerla verso il boma.
    - `collaudo_registro.py`: 15 su 15. 5.4 verso il boma 4 su 4 sulla stessa mura; lontano dal boma 4 su 4 sull'altra mura; durata in più rispetto alla 0.20.1 da 5,9 a 8,7 s.
    - `collaudo_pannello.py`, sul PC di Ale (caratteri veri, 1360×650): il passo 5.4 completato è a 0 px (nel giro delle 14:21 era +18, prima dell'accorciamento). Restano i sette eccessi dello stato «completato» (lezione 1 passo 7 +12, lezione 2 passo 4 +44, lezione 2 passo 6 +20, lezione 3 passo 5 +79, lezione 5 passo 3 +7, lezione 6 passo 2 +37, lezione 6 passo 4 +13), non dovuti alla 0.20.2 e da sistemare. A 1360×768 nessuno.
    - `collaudo_versione.py`: OK.
    - `tests/fisica/angolo_morto.js`: la parte 1 è passata alla regola dei 40° e dà uscite identiche alla regola dei 45° (2.180 su 2.196). La parte 2 resta con la regola dei 45° con cui è stata misurata la domanda 22.
- **Testo B anche quando la barca smette di arretrare con la prua sotto 37° (deciso dopo il collaudo a mano, `sessione-20261011-1749(3).txt`, passo 3.11, 457-466 s).**
  - **Il difetto.** Lo stato del suggerimento si spegneva se la barca smetteva di arretrare con la prua sotto 37°. Nel 3.11 la barca smette di arretrare fra 458,5 s (32°) e 459,5 s (37°). Poi la prua sale a 37°, 41° e 38° con 0,1, 0,7 e 1,1 nodi, ma B non compare: 0 s a schermo invece di circa 1,7 s.
  - **Correzione:**
    - lo stato resta armato finché la barca non supera 1 nodo, scuffia, o passano **10 s** dalla fine dell'arretramento (`backCheck(dt)`);
    - B si mostra solo con la prua ad almeno 37°;
    - i 10 s sono un'ipotesi nostra: sul solo motore, con un pilota che segue i testi, dalla fine dell'arretramento a 1 nodo passano 1,7 s di mediana e 4,8 s al massimo (1.390 partenze misurate su 1.404; nelle altre 14 la barca non arretra mai);
    - l'isteresi non cambia; il motore resta identico byte per byte, e `polare.js` e `raffiche_e_virate.js` danno uscite identiche.
  - **Collaudi**, `collaudo_suggerimento.py`, con i criteri dichiarati prima dei risultati. Misure nella sandbox, con caratteri non veri.
    - **Caso 8:** la barca arretra con la prua a 30-36°, smette di arretrare sotto 37°, poi il pilota la fa poggiare fino a 37°. **40 riusciti su 40, 0 non misurati.** B compare entro 0,5 s da quando la prua è ad almeno 37° e la barca è sotto 1 nodo, la barca supera 1 nodo entro 30 s, e B sparisce entro 0,5 s da lì.
    - **Contro-prova:** lo stesso caso 8 sull'`index.html` di prima dà B in **0 prove su 40** misurate, 0 non misurate.
    - **Tempo massimo:** barca tenuta a +0,3 nodi con la prua a 40°. B sparisce a 10,05, 10,08, 10,07 e 10,05 s (4 su 4 fra 10 e 10,5 s).
    - Invariati:
      - caso 6, 40 su 40;
      - caso 7, B mai in 40 prove misurate;
      - 5.4, 20 su 20;
      - 3f, 12 su 12;
      - casi 1 e 3, 80 su 80;
      - nessun ritorno al primo testo con la prua da 37° in su;
      - pannello 0 px.
    - **Criterio che fallisce ancora, invariato** (`tests/collaudo_suggerimento.py:151`, dalla 0.20.1: la prua non deve scendere più di 3° sotto la partenza). In questo giro le uscite nel gioco libero sono 199 su 200, nel giro precedente 198. La prova che fallisce non è la stessa: caso 4, mure a sinistra, scotta 50, seme 6, prua scesa a 39°. Nel giro prima erano il seme 3 con scotta 100 (41°) e il seme 10 con scotta 50 (38°). I semi fissi non rendono la prova del tutto ripetibile, perché il collaudo gira in tempo reale. In questo giro il tempo per uscire va da 4,2 a 21,4 s simulati (nel giro prima da 4,4 a 9,8 s): non è un criterio e non ne ho cercato la causa.
- **Documenti:** `FISICA-E-TARATURE.md` (soglia unica e tabella dei costi), `CONTENUTI-DA-VERIFICARE.md` (testo del 5.4, rallentare orzando, uscita sull'altra mura, domanda 22, tutte «da confermare con un velista esperto o altre fonti»), `COLLAUDI.md` e `DUBBI-E-RICERCHE.md`.

## 0.20.1 — uscire dall'angolo morto: i testi dicono quello che il gioco fa

Dell'11 ottobre 2026. **Il motore non cambia**: il blocco di `step()` è identico byte per byte alla 0.20, e le uscite di `polare.js` e `raffiche_e_virate.js` sono identiche carattere per carattere.

- **Il difetto (due registrazioni di Ale, 0.19.5 e 0.20).** Il passo 5.4, il suggerimento «Stai andando all'indietro…» e la domanda d'esame 22 dicevano: centra la barra e la prua poggia da sola. Nel gioco, con la barca che arretra e la barra al centro, la prua restava ferma, e Ale ripartiva solo cazzando. **Causa:** la prua gira da sola solo con vento apparente sotto 36° **e** velocità sotto 0,5 m/s (riga 443). Nei tre casi registrati il vento apparente era di 38-41° e 45°, oppure la barca arretrava a 0,87 m/s. Riprodotti con `__sv` nel gioco libero (10 semi fissi, con e senza raffiche): prua ferma in tutte le prove con scotta 100 e 50; velocità all'indietro a regime −1,03, −0,87 e −1,68 nodi, come nei log. **Le fonti non dicono che la prua poggi da sola**: due dicono che la barca resta nell'angolo morto (`DUBBI-E-RICERCHE.md`, sez. 3). Dichiarato in `FISICA-E-TARATURE.md` (punto 7).
- **Misura del verso della barra, prima di scrivere i testi.** Regola: mentre la barca arretra, barra a fondo **dalla parte del boma**; quando smette, barra al centro. Scotta ferma.
  - Griglia sul motore, prua da 0° a 60° dal vento ogni 2° **su tutte e due le mure**, velocità iniziale 0, −0,25, −0,5, −1, −1,5 e −2 nodi, scotta 100 e 50, vento 6, 10 e 14 nodi: **2.196 partenze** (366 per vento e scotta). Ne escono (prua ad almeno 45° dal vento e barca che va avanti, entro 60 s) **2.180**. A 10 nodi il tempo per uscire ha mediana 6,7 s e massimo 22,4 s con scotta 100; mediana 3,3 s e massimo 6,4 s con scotta 50.
  - Le altre **16** sono 8 configurazioni (vento, scotta, angolo) su tutte e due le mure. Partono tutte **già fuori dall'angolo morto** (50-58° dal vento), da ferme, e restano ferme a 52-58° con la vela lascata e la scotta tenuta ferma. 12 arretrano al massimo di 0,052 nodi e 4 non arretrano mai; il suggerimento, che compare da circa 0,1 nodi all'indietro, non si accende mai. Nessuna partenza dentro l'angolo morto resta bloccata.
  - Con la barra **lontano dal boma** la prua attraversa il vento e non esce in nessuna delle 60 prove fatte nel gioco libero (tre casi, scotta 100 e 50, 10 semi). *Corretto nella 0.20.2: quel collaudo contava solo l'uscita sulla stessa mura; lasciata fare, la barca esce sull'altra.*
- **Passo 5.4 «Una virata che non riesce», testo finale:** «Per uscirne: spingi la barra verso il boma e la prua si allontana dal vento; quando la barca smette di arretrare, centra la barra, cazza e riparti.» La condizione per completare il passo non cambia.
- **Suggerimento dal vivo:** «Stai andando all'indietro: la barra funziona al contrario. Spingila verso il boma; centrala quando riparti.» (107 caratteri contro 110). Non serve limitarlo all'angolo morto.
- **Domanda d'esame 22:** giusta «Spingi la barra verso il boma e la centri quando riparti». Sbagliate:
  - «Spingi la barra lontano dal boma, come per poggiare andando avanti»;
  - «Muovi la barra di continuo da un lato all'altro»: nel gioco non fa uscire (26 partenze su 4.860, tutte con il ritmo più lento (barra che cambia lato ogni secondo); griglia 0-44° dal vento, due mure, da 0 a −2 nodi, vento 6, 10 e 14 nodi, scotta 100 e 50); nella realtà una fonte, su un catamarano;
  - «Orzi ancora, finché il vento passa dall'altra parte».

  Tolte «Centri la barra e lasci che la prua poggi da sola» e «Cazzi tutta la vela e aspetti che la barca riparta», che nel gioco a volte funziona.
- **Domanda d'esame 26 sostituita:** «Vuoi capire se sta arrivando una raffica. Dove guardi?», giusta «Sull'acqua sopravento: chiazze più scure e increspate» (passo «Raffiche e sbandamento», che lo insegna). Una prima versione sul contrappeso è stata scartata prima del commit: si sovrapponeva alla domanda 2 (il timoniere siede sopravento per fare contrappeso) e alla 24 (fra le sbagliate «Sporgersi fuori bordo»). La domanda «Come riparti?» dopo la scuffia è tolta: la regola per ripartire non è stata trovata nelle fonti. La domanda sulle scotte libere è in `DUBBI-E-RICERCHE.md`, da riprendere dopo la conferma di un velista esperto o di altre fonti. Le domande 22 e 26 sono «da confermare con un velista esperto o altre fonti».
- **Passo «Raddrizzare»:** «Nella realtà prima si lasciano libere le scotte, poi il timoniere sale sulla lama della deriva e fa leva con il proprio peso finché la barca torna dritta, e risale a bordo.» Testo finale: «Barca dritta. Regola la vela con i filetti e riparti.» Via la regola «riparti con la scotta lascata e cazza quando hai velocità». Il ripasso della lezione 6 non cambia.
- **Collaudi.**
  - Nuovo `tests/fisica/angolo_morto.js`: rifà la griglia della barra verso il boma e il conteggio della barra mossa avanti e indietro (domanda 22). Dura circa un minuto e dà gli stessi numeri scritti qui. Non è nel `lancia_tutti.sh`.
  - `collaudo_suggerimento.py` ha una parte nuova. Il pilota legge il suggerimento come un giocatore e preme le frecce vere dalla parte del boma, poi centra con lo spazio. Tre casi delle registrazioni, **due mure**, scotta 100 e 50, 10 semi, gioco libero con raffiche: **120 uscite su 120**, dopo circa 2,5-11,2 s simulati. **Contro-prova:** lo stesso pilota con la freccia dalla parte opposta non esce in 4 casi su 4 (i tre casi su una mura e il caso 3 sull'altra), quindi il controllo sa anche fallire.
  - Pannello col testo nuovo: 0 px di eccesso, ma nella sandbox i caratteri non sono quelli veri («NON VALIDO»).
  - `collaudo_esame.py`: banca valida, giusta più lunga in 3 su 26 (12%), nessun pareggio di lunghezza nelle domande 22 e 26 (restano due pareggi della 0.20, domande 10 e 14); 500 estrazioni. Il riquadro va misurato sul PC.
  - `collaudo_lezioni.py`: tutti OK.
  - `collaudo_registro.py i`: 5 su 5, compreso il passo 5.4 completato.
- Documenti: `CONTENUTI-DA-VERIFICARE.md` (voci 22 e 26, nuove righe nelle lezioni 2, 5 e 6), `MANUALE-bozza.md` §4 (riga «Uscire dall'angolo morto»), `FISICA-E-TARATURE.md` punto 7, `DUBBI-E-RICERCHE.md` sez. 3 (corretto un dato sbagliato: il «3,4-10,2 s» era misurato con la barra lontano dal boma).

## 0.20 — l'esame su tutte le lezioni, come prova nel gioco libero

Del 10 ottobre 2026. Prima fetta del traguardo 1.0 (`docs/PROPOSTA-ESAME-E-BREVETTO.md`, §7). Nessuna modifica alla fisica, ai testi delle lezioni, al ripasso né a `sperimentale/`.

- **Pulsante «Esame su tutte le lezioni» acceso** nel riquadro «Ripasso ed esame» del menu («20 domande, ne servono 16»). Il riquadro «In arrivo» dice ora solo «I tornei, altri tipi di barca.»
- **Banca minima di 26 domande** (`ESAME`, raggruppata per lezione come il ripasso): lezione 1 5, lezione 2 4, lezione 3 5, lezioni 4-6 4 ciascuna. Ogni domanda porta il titolo del passo di lezione da cui nasce. Le 29 domande del ripasso restano separate e non entrano nell'esame. Regole dei testi: nessuna cifra, niente precedenze e regole di regata, niente dubbi specifici di `CONTENUTI-DA-VERIFICARE.md`, niente testi che stanno solo nel pannello o nel glossario. La giusta è la risposta più lunga in 4 domande su 26 (15%; soglia 30%).
- **Estrazione per quote** (`QUOTE = [4, 3, 4, 3, 3, 3]`): per ogni lezione le sue domande rimescolate, le prime della quota, poi le 20 rimescolate insieme. Funziona con qualunque numero di domande per lezione, purché sia almeno la quota più una.
- **Durante l'esame** nessun colore giusto/sbagliato e nessuna spiegazione; la risposta scelta si vede in grigio e non si può cambiare. **Alla fine** «N su 20: superato» oppure «N su 20: non superato (servono 16)», poi le sbagliate raggruppate per lezione, ognuna con risposta data, risposta giusta, spiegazione e la riga «dal passo «…»»; pulsanti «Rifai l'esame» e «Chiudi».
- **Nel gioco libero l'esame non salva niente**: né punteggio né esito. Chiudere il riquadro a metà (Esc) perde l'esame in corso. Scritto nel manuale.
- Il rimescolamento delle risposte è ora una funzione `mescola()`, usata da ripasso ed esame. **Il ripasso è rimasto identico**: con lo stesso seme di `Math.random`, 65 schermate dei sei ripassi e il salvataggio finale uguali carattere per carattere fra 0.19.5 e 0.20.
- Nuovo `tests/collaudo_esame.py` (banca, 500 estrazioni a seme fisso, pagina senza `#collaudo`, `localStorage` identico, menu confrontato con la 0.19.5, riquadro con 20 sbagliate a 1360×650 e 1360×768). Nella sandbox il riquadro risulta «NON VALIDA» perché mancano i caratteri veri: la misura vera la dà il PC con `tests/lancia_tutti.sh --solo esame`.
- Documenti: le 26 domande in `CONTENUTI-DA-VERIFICARE.md` con l'esito vuoto, le domande 11 e 22 da far confermare a un velista, e la lista «Da sistemare dopo la 0.20» con le due domande del ripasso senza un passo nella loro lezione; i concetti per la 0.20.1 e seguenti nella §5 della proposta dell'esame.
