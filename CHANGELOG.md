# Diario delle modifiche

Tutte le versioni fino alla 0.16 sono del 26–29 settembre 2026; la 0.17 è del 1 ottobre 2026. I difetti sono riportati con la causa, perché ricordare come sono nati aiuta a non ripeterli.

## Sperimentale

Prove che **non sono versioni del gioco**: vivono in `sperimentale/` e non toccano `index.html`. Verificato a ogni passo che, per una barca a una vela sola, polare, virate e raffiche restino identiche a quelle del gioco.

- **Prototipo del fiocco** (`sperimentale/fiocco.html`), in vista di una futura deriva a due. Tappa A: il fiocco come seconda superficie portante, con scotta propria (tasti Q ed E), filetti e disegno. Tappa B: la randa che copre il fiocco alle andature larghe, e il pannello che dice chiaramente dove il fiocco non si regola. Costanti, semplificazioni e fonti in `FISICA-E-TARATURE.md` e `CONTENUTI-DA-VERIFICARE.md`. Non ci sono ancora l'upwash della randa sul fiocco, il fiocco a collo in virata e la manovra a farfalla.
- **Prototipo del fiocco, tappa C, primo compito: la vista e la forza del fiocco coperto adesso dicono la stessa cosa.** In tappa B il pannello diceva «qui non si regola (coperto dalla randa)» mentre il fiocco dava ancora dal 10% al 19% della spinta. Portare solo `slotShade` a 1,0 non bastava: fra 107° e 135° di vento apparente ne restava il 16-10%, perché lì l'ombra era ancora parziale. Ritarate tre costanti: `slotA0` 85→**95**, `slotW` 50→**12**, `slotShade` 0,70→**1,00**. L'ombra ora è nulla fino a 95° apparenti e totale da 107°, che non è un numero scelto ma l'angolo oltre il quale non esiste più una posizione del fiocco con i filetti dritti. `jibShadedAt` perde la soglia propria e diventa «`jibRange` nullo»: strumento e messaggio del pannello non possono più contraddirsi. **Misure:** quota di spinta del fiocco da 108° a 180° apparenti, grado per grado, **0,00%** (soglia dichiarata 3%); nessuna ombra fino a 95°; bolina +10,9% contro larghe +6,3% (il confronto regge); polare senza nuovi denti; nessuna bistabilità su sei andature larghe partendo da ferma e lanciata; non-regressione senza fiocco a scarto zero e uscite di `polare.js` e `raffiche_e_virate.js` identiche carattere per carattere. **Prezzo dichiarato:** la curva si irrigidisce fra 126° e 132° reali (massima variazione 0,163 nodi/° contro 0,085 in tappa B), e la prova 2 «Lasco e poppa» torna esattamente al tempo del gioco (149 s contro 145/142 della tappa B), perché su un percorso portante il fiocco ora non dà più niente. **Difetto nel collaudo, trovato e corretto:** la verifica «senza `#collaudo`» cliccava il titolo del menu invece del pulsante, il gioco non partiva e la prova passava leggendo «—» dappertutto; ora controlla di essere partita e di aver attraversato davvero le andature che dice di misurare.
- **Prototipo del fiocco, tappa C, secondo compito: il momento di imbardata dovuto alle vele non si modella, e la semplificazione è dichiarata.** Si era proposto di modellare il solo contributo del fiocco, lasciando alla randa l'equilibrio implicito nel motore. Misurato fuori dal motore, senza toccare `step()`: su 12 casi (6, 10 e 14 nodi × 45°, 70°, 90° e 110° reali) quel momento fa poggiare **12 volte su 12**, e il termine che dovrebbe far orzare sbandando non arriva mai a ribaltarlo (dal 3% al 23% dell'altro). F4 dice il contrario: barca piatta e vele regolate, la barra sta circa al centro; sbandando, la barca orza. Emulando quel momento con la barra libera, a 10 nodi la barca partita a 45° dal vento è a 75° dopo 10 s e a 124° dopo 60, cioè circa 3 °/s di scarto: ingiocabile. Il momento riguarda **tutta la barca** — randa, fiocco, scafo sbandato — e non si aggiunge a metà. Il motore non è stato toccato (`git diff` vuoto su `fiocco.html` e `index.html`). Il termine che farà girare la prua col fiocco a collo starà nel terzo compito e dovrà funzionare anche a barca ferma, dove questo valeva zero.
- **Prototipo del fiocco, tappa C, terzo compito: il fiocco a collo in virata non si modella, e la semplificazione è dichiarata.** Provati due modelli fuori dal motore, senza toccare `step()` (`git diff` vuoto su `fiocco.html` e `index.html`). Quello senza memoria del lato del fiocco è peggio di niente: resiste nella prima metà della virata e le riuscite scendono da 75 a 69 su 84. Quello con un filo di memoria funziona (`backRate` 12 °/s, `backT` 1,2 s; virata di bolina a 10 nodi da 4,35 a 3,79 s col fiocco cazzato, da 75 a 78 riuscite su 84, da 179 a 188 su 200 tentativi con seme fisso), ma è stato scartato lo stesso: in un motore cinematico è una **taratura**, con due costanti senza nessuna fonte e il verso scritto nel codice, quindi «col fiocco cazzato si vira meglio» è vero per costruzione; le soglie dei criteri erano state scritte dopo aver visto i numeri del banco, contro le regole dei prototipi; la memoria del lato del fiocco **sostituisce l'equipaggio** e andrebbe rifatta con il prodiere e le due scotte della barca a due (tappa C4); il guadagno è modesto (col fiocco lascato da 136 a 138 su 200); e si perderebbe un comportamento in navigazione libera, perché col fiocco cazzato non ci si potrebbe più fermare nell'angolo morto. **Oggi in virata il fiocco conta solo per la resistenza della vela che sbatte**, non perché vada a collo. Modello, criteri, rischi e numeri restano in `sperimentale/PROPOSTA-C3.md`, `banco_tappaC3.js` e `banco_tappaC3.txt` come registro della decisione.
- **Prototipo del fiocco, tappa C chiusa, quarto compito: la barca a due non si modella e il sovrainvelamento si dichiara.** Il prototipo resta con lo scafo e il timoniere del gioco a una vela (135 kg, un velista da 75 kg) e il 37% di vela in più: una raffica da 20 nodi fa scuffiare e a 15 nodi la virata non riesce. Il banco di confronto proposto (quattro configurazioni da 135 a 250 kg, 108 raffiche, 12 soglie di scuffia, 132 equilibri di polare, 288 virate, 36 giri nel browser) **non è stato eseguito**, perché i conti che già avevamo bastavano a decidere, e `step()` e `sperimentale/fiocco.html` **non sono stati toccati** (`git diff` vuoto). Tre ragioni: (1) la coppia raddrizzante del prototipo vale **83,7 kgf·m** al massimo, a 22,6° di sbandamento, contro i **circa 60 kgf·m** che la fonte dà a una deriva a due **senza** trapezio, quindi quella barca sarebbe **meno** stabile di questa, e l'unica configurazione che risolve il sovrainvelamento è quella **col trapezio** (circa 220 kgf·m), che per il livello 2 sarebbe una **seconda novità principale**; (2) nel motore la **massa non entra nella resistenza dello scafo**, quindi una barca più pesante andrebbe a regime più **veloce** perché sbanda meno, e per ritarare `hullK2` e `hullK4` non c'è fonte (polari pubbliche di derive non risultano, F10 non letta); (3) il **peso dell'equipaggio dovrebbe diventare un'azione del prodiere** (lezione 2.5), non l'automatismo da 0,9 s di oggi. Annotata anche, senza cambiarlo, l'incoerenza del timone: a 6 nodi il motore dà 21,2 kgf di resistenza dello scafo contro i 19 della fonte (vicina) ma solo 2,9 kgf di timone a 15° contro 12, e arriva a 10,9 solo vicino a 30°; soprattutto **la pala non stalla mai**, così la barra a fondo fa girare 1,93 volte più in fretta che a 15° ed è sempre la scelta migliore, mentre nella realtà no. Conseguenza per il gioco: **il livello 2 va giocato con vento da leggero a medio** (sopra i 12-15 nodi circa, limite da decidere con le lezioni). Con questo la tappa C è chiusa: proposta e criteri in `sperimentale/PROPOSTA-C4.md`, decisione e stato finale del prototipo in fondo a `FISICA-E-TARATURE.md`.


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

## 0.19.5 — il ripasso mostra le domande sbagliate

Del 7 ottobre 2026. Nessuna modifica alla fisica né a `sperimentale/`.

- **Schermata finale del ripasso**: se ci sono errori, elenco delle domande sbagliate (testo, risposta data, risposta giusta, spiegazione) in una zona che scorre. Messaggi: «Quasi tutto giusto: ecco la domanda sbagliata con la spiegazione.» (un errore) e «Conviene rifare la lezione, o almeno i passi sugli argomenti sbagliati: ecco le domande sbagliate.» (più errori).
- **«Ripassa solo le sbagliate»**: ripropone solo quelle domande. «Rifai il ripasso» rifà tutte. **«Rivedi la lezione»** riapre la lezione (usa `startLesson`, già esistente).
- **Il punteggio migliore** («migliore: X su N») si aggiorna solo con un ripasso completo, mai con il giro parziale.
- `tests/collaudo_quiz.py` riscritto: risponde sbagliato apposta (1 e 4 errori), controlla elenco, giro parziale e record; fallisce se misura zero casi.
- **Correzione del riquadro** (visto a 1360×768 con i caratteri veri: con 6 errori «Chiudi» andava a capo ed era tagliato dal bordo): il riquadro è ora una colonna flessibile alta al massimo il 90% della finestra; intestazione e messaggio fissi, elenco che scorre in mezzo (via il calcolo fisso `90vh − 250px`), pulsanti sempre dentro, anche a capo. Punteggio ridotto da 2,4 a 1,45 rem (circa 60%), margini verticali dell'intestazione un po' più stretti. `collaudo_quiz.py` controlla i caratteri veri (altrimenti «NON VALIDA») e misura i pulsanti rispetto al riquadro a 1360×650 e 1360×768 con 6 e 1 errore; ha ora un ESITO OK/FALLITO (in `lancia_tutti.sh` passa fra quelli con esito chiaro). Nella sandbox, senza caratteri veri, il codice di prima dava già 6,4 px di eccesso nella copia di prova e quello nuovo 0,0; la misura vera la dà il PC con `tests/lancia_tutti.sh --solo quiz`.
- Il riquadro e il pannello con i caratteri veri vanno misurati dall'utente (nella sandbox i caratteri non sono quelli veri).

## 0.19.4 — giro di testi e piccole correzioni

Del 7 ottobre 2026 (sera). Nessuna modifica alla fisica, alle raffiche del motore né a `sperimentale/`.

- **Messaggio sulla raffica**: «Raffica in arrivo: se la barca sbanda troppo, lasca; altrimenti è un'occasione per andare più veloci.» Non è più un allarme: classe vuota, cioè il colore normale del testo (le classi esistenti erano solo «good» verde e «bad» arancione/rosso).
- **«Sbandi troppo»** con la scotta già tutta lasca (`I.sheet > 0.99`) non dice più l'impossibile: «Sbandi troppo e la vela è già tutta lasca: prova a orzare un poco.» Con la scotta non al massimo il testo resta com'era. Riga da far confermare a un velista in `docs/CONTENUTI-DA-VERIFICARE.md`.
- **Registratore**: l'etichetta nelle impostazioni **non cambia** (nessun testo in più a video); che la registrazione resta accesa finché non la si spegne, anche a fine prova, è spiegato nel manuale (bozza). Alla riaccensione l'evento scrive i secondi veri di pausa («registrazione_accesa pausa 70s»), in testa al file c'è il totale delle pause, e `tests/analizza_sessione.py` lo ricalcola e lo confronta.
- **Collaudi**: `collaudo_suggerimento.py` misura anche i due testi nuovi nel pannello e prova i due casi di sbandamento (scotta 1,0 contro 0,6); `collaudo_registratore.py` (parte a) prova spegnimento e riaccensione con una pausa nota (3,3 s attesi, scritti 3).
- Documenti: osservazioni 18-22 del 7 ottobre sera, riga sulle raffiche nel manuale (bozza) con la regola dei comandi, idea del campo di vento esteso in `ROADMAP.md`, regola dei comandi corretta in `VISIONE-LIVELLI-E-CARRIERA.md`.

## 0.19.3 — vista del percorso e zoom lontano senza rallentare

Del 7 ottobre 2026 (sera). Problema misurato dall'utente: l'arrivo della prova 1 è a 230 m (prova 2 circa 255 m), ma allo zoom minimo (0,4) si vedevano circa 120 m in altezza, e con Q, barca all'80%, circa 95 m davanti; a zoom lontano il gioco rallentava.

- **Zoom minimo da 0,4 a 0,1** (pulsanti, rotellina; costante `ZMIN`). Conto: sullo schermo 1 m = min(larghezza, altezza del mare) / 48 × zoom pixel; il mare è 970×650 a 1360×650 e 970×768 a 1360×768. Per vedere un obiettivo a 300 m davanti con la barca al margine (80% dell'altezza) e 50 px di margine serve uno zoom al massimo di 0,116 a 1360×650 e 0,117 a 1360×768. Scelto **0,1**: con la barca al margine si vedono circa 347 m davanti a 1360×650 (352 a 1360×768); con la barca al suo posto («prua in alto», 60% dell'altezza) circa 288 m in alto e 358 m di lato, abbastanza per avere l'obiettivo sullo schermo anche senza Q in tutte le prove e regate misurate.
- **Q = vista del percorso.** Oltre allo spostamento della barca (0.19.2), l'inquadratura si allontana (`VIEW_ZK` 7,5/s, circa 0,4 s al 95%: ipotesi nostra) finché l'obiettivo sta a 50 px dal bordo (`VIEW_M`, ipotesi nostra), mai sotto lo zoom minimo; al rilascio tornano posizione e zoom di prima (lo zoom scelto dal giocatore non si tocca: il tasto ha un suo fattore `zoomQ`). Stesse condizioni: prove e regate sì, lezioni no, senza obiettivo nessun effetto. Fattore misurato: da 0,145 (prova 1) a 1.
- **Increspature.** Sfumano fra zoom 0,5 e 0,35 e sotto non si disegnano (`RIP_Z1`, `RIP_Z0`, ipotesi nostre); in più i tratti per cella scendono da 4 a 1 allontanando, in proporzione all'area, così sullo schermo la densità resta simile. Tempo per fotogramma con il disegno vero (prova 5, 1360×650, mediane di 60 fotogrammi, nella sandbox):

  | Zoom | 0.19.2 | 0.19.3 |
  |---|---|---|
  | 1 | 16,3-16,7 ms | 16,0-17,7 ms |
  | 0,8 | 15,2-17,5 | 15,6-15,8 |
  | 0,64 | 16,9-17,1 | 15,2-17,2 |
  | 0,51 | 19,0-21,9 | 12,7-14,8 |
  | 0,41 | 22,9-23,3 | 15,3-16,1 |
  | 0,33 | (minimo 0,4) | 11,6-11,8 |
  | minimo | 22,9-23,0 (0,4) | 8,4-8,7 (0,1) |

  Il primo tentativo (solo dissolvenza) lasciava 23 ms a zoom 0,4: da qui i tratti per cella; con l'arrotondamento per eccesso il costo avrebbe avuto un picco fra 0,5 e 0,7, quindi l'arrotondamento è normale. Misurare il solo tempo JavaScript non basta (1,5 ms a zoom 1, 0,3 al minimo): il costo vero è disegnare i pixel, che la misura ora comprende leggendo un pixel dopo ogni fotogramma.
- **Raffiche.** Erano già chiazze scure a gradiente, disegnate per conto loro; le increspature dentro una raffica erano in più più scure e più lunghe. Senza increspature restano le chiazze, visibili a ogni zoom (schermate `L_prova5_zoom_minimo.png`, `L_prova5_zoom0.4.png`). Non le ho cambiate.
- **A zoom lontano:** se la barca è sotto 14 px, attorno c'è un triangolo bianco a contorno orientato come la prua (non copre la barca). Boe con un raggio minimo di 3 px; la linea a scacchi era già di 3 px per quadretto; la pillola ha misura fissa.
- **Distanza accanto alla freccia fuori schermo:** «230 m», ai 5 m, dalla barca all'obiettivo, in bianco 13 px. In regata, prima del via, può differire da «Alla linea» dell'orologio, che è la distanza dalla linea in perpendicolare, non dal suo centro.
- **`collaudo_vista.py`**: 161 casi, 0 sbagliati. Nuovi: obiettivo dentro lo schermo con Q (28 casi: prove 1-5, regata 1 prima del via e verso la boa, prua e nord in alto, 1360×650 e 1360×768) e al solo zoom minimo (28 casi), posizione letta dalla trasformazione del mondo intercettata nel disegno; tempo per fotogramma al minimo 8,5 ms contro 16,0 a zoom 1 (soglia dichiarata prima: al massimo 1,10 volte); raffiche disegnate al minimo zoom (5 su 5, contate come chiamate a `createRadialGradient`, una per raffica e unica nel gioco); increspature a zero celle al minimo. Il ritorno chiede anche lo zoom del tasto tornato a 1: da 390 a 806 ms su 32 rilasci (soglia 1 s). Traiettoria identica e banco come nella 0.19.2. Sulla 0.19.2 fallisce: 159 casi, 85 sbagliati, 2 gruppi con zero casi. **Difetti del collaudo trovati e corretti:** il conto delle raffiche leggeva il contatore in due chiamate, fra le quali il browser disegnava un fotogramma in più (12 chiazze per 6 raffiche); sulla versione di prima il collaudo si fermava con un errore di Python invece di dire «FALLITO».
- **`collaudo_schermate.py`**: ogni prova in una pagina nuova; in più zoom minimo e partenza con Q di ogni prova, regata 1 con Q.
- **Documenti:** proposta, manuale (Q = vista del percorso; zoom), osservazioni 16 e 17 (17: idea delle raffiche con freccia e numero, solo documenti), `ROADMAP.md` (idea delle raffiche), `CONTENUTI-DA-VERIFICARE.md` (salto di direzione nelle raffiche, da far confermare), `COLLAUDI.md`.
- **Verificato nella sandbox:** `collaudo_vista.py` tutto OK; `collaudo_linea.py` 216 casi, 0 sbagliati, 8 su 8; `collaudo_lezioni.py`, `collaudo_schermate.py`, `collaudo_versione.py` OK; `collaudo_registratore.py` tutte le verifiche OK; `collaudo_pannello.py` a 1360×650 e 1360×768 eccesso 0 px, riga dei tasti 0 px. Pannello e registratore escono con 1 solo perché nella sandbox mancano i caratteri veri. `polare.js` e `raffiche_e_virate.js` identici carattere per carattere. Da misurare sul PC dell'utente: tempi di disegno, pannello con i caratteri veri, aspetto.

## 0.19.2 — tasto vista (Q) e linea d'arrivo a scacchi

Del 7 ottobre 2026. Parte B di `docs/PROPOSTA-LINEA-E-VISTA.md`, approvata col tasto Q invece di V; osservazioni 13 e 14.

- **Linea d'arrivo e scritta «Arrivo».** La linea d'arrivo delle prove, e quella delle regate dopo il via, è a scacchi bianchi e neri: due file di quadretti di 3 px sullo schermo a ogni zoom (prima della linea attiva, nelle prove 4 e 5, è a metà trasparenza). Prima del via la linea di partenza delle regate resta tratteggiata. La scritta («Arrivo», e «Linea di partenza» in regata) è una pillola scura semitrasparente con testo bianco in Barlow Semi Condensed 700 a 14 px, a misura fissa sullo schermo, con una bandierina a scacchi accanto ad «Arrivo». Sta accanto alla boa verso cui punta la freccia fuori schermo, se punta alla linea, altrimenti a quella più vicina alla barca; prova tre posizioni (oltre la boa, sopra, sotto) e prende la prima che non copre la barca né le boe (e la barca giuria) e, se la boa è sullo schermo, resta dentro lo schermo. Si disegna solo dopo che `document.fonts.load` ha caricato Barlow 600 e 700. Testi, linea e taglio non cambiano.
- **Perché la scritta di prima sembrava diversa.** Nel codice «Arrivo» aveva lo stesso carattere delle etichette delle boe (`600 13px "Barlow Semi Condensed"`), non un carattere sbagliato: era però più sottile e più piccola delle altre scritte sul mare con sfondo (700), bianca senza sfondo sopra le increspature, e il gioco non aspettava mai il caricamento dei caratteri, quindi finché Barlow non è caricato il canvas usa un carattere di sistema senza avvisare. Quale delle due cose si vedesse sul PC dell'utente non si può verificare nella sandbox, dove Google Fonts non si carica.
- **Tasto vista, Q tenuto premuto.** Sposta la barca sullo schermo dalla parte opposta all'obiettivo (arrivo, boa o, prima del via, la linea), del 60% della mezza larghezza e della mezza altezza, con la barca fra il 20% e l'80% dello schermo; arrivo e ritorno morbidi (`VIEW_K` 12/s, 95% in 0,25 s: ipotesi nostre). Vale con «prua in alto» e «nord in alto». Solo nelle prove e nelle regate; non nelle lezioni; senza obiettivo (navigazione libera, dopo l'arrivo) non fa nulla. Funziona con Bloc Maiusc; col focus in un campo di testo non fa nulla. Nessun alias, nessun altro tasto cambiato. Niente pausa, zoom, fisica o tempo toccati: lo spostamento sta solo nel disegno. Aprire una voce azzera i tasti tenuti, come per le frecce.
- **`goal()`**: una funzione sola per l'obiettivo, usata da freccia fuori schermo, rilevamento del pannello e tasto vista. Due differenze visibili, volute: in regata, dopo l'arrivo, il rilevamento mostra «—» (prima continuava a puntare all'arrivo); nella navigazione libera il rilevamento resta quello della boa 1, come prima, anche se lì non c'è un obiettivo.
- **Increspature del mare**: invece di allargare il raggio dello spostamento (proposta), si disegnano attorno al centro dello schermo invece che alla barca: con la barca spostata le celle restano le stesse. A zoom 0,4 (finestra 1360×650, mare 970×650): 1122 celle senza Q e 1156 con Q («prua in alto»), 1156 e 1089 («nord in alto»), limite 2500. Col raggio allargato sarebbero state circa 1652 e 1943.
- **Legenda**: «Q vista» compare nella riga dei tasti del pannello solo nelle prove e nelle regate e solo se la riga non si taglia (il controllo lo fa il gioco a ogni aggiornamento del pannello, con i caratteri che ha davvero); altrimenti compare sul mare, sopra i pulsanti + e −. Nella sandbox, con il carattere di sistema, la riga è già piena (357 px su 357) e «Q vista» va sul mare; con i caratteri veri lo misura l'utente.
- **Registratore**: Q entra fra i tasti registrati come «Q(vista)» e nella legenda del file.
- **Aggancio per i collaudi**: `__sv.frame(dt)` (un passo di simulazione più il disegno), `viewOff`, `rippleCells`, `goal`, `cam()`, `gusts()`.
- **Nuovo `tests/collaudo_vista.py`**: 102 casi, 0 sbagliati (direzione con le due viste 32 casi; ritorno sotto 2 px fra 319 e 404 ms su 32 rilasci; nessun effetto 5; Bloc Maiusc 1; stato identico al bit con e senza Q 12, con 6 semi su prova 5 e regata 2; banco che vede un numero casuale in più 12 su 12; increspature 2; pagina vera senza `#collaudo` 6 su 6). Sulla 0.19.1 fallisce (56 casi misurati, 52 sbagliati, 2 gruppi con zero casi). **Difetti del collaudo trovati al primo giro e corretti:** (1) aprire una voce azzera i tasti tenuti, quindi Q era attivo solo al primo fotogramma, e corse successive nella stessa pagina partivano da stato diverso: la prova 5 risultava «diversa con Q» per colpa del metro, non del gioco; ora ogni corsa sta in una pagina nuova e Q si preme dopo l'apertura; (2) il banco non vedeva differenze perché in 6 s il numero casuale in più cambia solo una raffica nuova lontana dalla barca, e nella regata 1 (senza raffiche) la simulazione non usa numeri casuali: ora lo stato confrontato comprende le raffiche e si usa la regata 2.
- **Difetto nel controllo dei caratteri, trovato e corretto:** `document.fonts.check` dà vero anche quando le facce del carattere non esistono (nella sandbox `document.fonts` è vuoto e i collaudi scrivevano lo stesso «caratteri caricati: True»). `collaudo_pannello.py`, `collaudo_suggerimento.py` e `collaudo_registratore.py` ora chiedono anche una faccia Barlow con stato `loaded`; nella sandbox risultano quindi non validi, come devono.
- **Altri collaudi:** `collaudo_pannello.py` misura anche la riga dei tasti (prova 1, prova 5, navigazione libera, regata) e dice se «Q vista» ci sta. `collaudo_schermate.py` salva le schermate della linea d'arrivo (`tests/output/L_*.png`). `collaudo_vista.py` aggiunto a `tests/lancia_tutti.sh`.
- **Documenti:** proposta (parte B fatta), manuale (Q vista; regola dei tasti nuova), osservazioni 13 e 14, regola dei tasti aggiornata anche in `VISIONE-LIVELLI-E-CARRIERA.md` e `ROADMAP.md`, riga in `CONTENUTI-DA-VERIFICARE.md` (la linea a scacchi è un simbolo del gioco).
- **Verificato nella sandbox:** `collaudo_vista.py` tutto OK; `collaudo_linea.py` 216 casi, 0 sbagliati, 8 su 8; `collaudo_lezioni.py` errori nessuno; `collaudo_schermate.py` errori nessuno; `collaudo_versione.py`; `collaudo_registratore.py` tutte le verifiche OK, eccesso 0 px, ma esce con 1 perché senza caratteri veri; `collaudo_pannello.py` a 1360×650 e 1360×768 eccesso 0 px e riga dei tasti 0 px, ma **non valido** perché senza caratteri veri; `polare.js` e `raffiche_e_virate.js` identici carattere per carattere. Da misurare sul PC dell'utente: pannello e riga dei tasti con i caratteri veri, aspetto delle schermate.

## 0.19.1 — finestra delle impostazioni in 1360×650, due correzioni di testo

Del 7 ottobre 2026. Il tasto «vista», già previsto per la parte B della proposta della 0.19, diventa la **0.19.2**.

- **Finestra delle impostazioni in navigazione libera, a 1360×650.** Misurato sul PC dell'utente (non nella sandbox, dove dà 0): sforava di 3 px in 3 sessioni su 3. Il `gap` fra le voci dirette di `.set-body > .opts` scende da 6 a 4 px (`index.html`): nel caso peggiore (navigazione libera, «Registra la sessione» attiva, nota e marcatori visibili) ci sono 12 voci e quindi 11 spazi, per **−22 px** di altezza, contro i −18 px calcolati come necessari per un margine di almeno 15 px. Nessun testo, opzione o casella tolta; nessuna grafica cambiata oltre allo spazio fra le righe. A 1360×768 e nelle lezioni l'eccesso era già 0 ed era già confermato il margine su quel caso.
- **`collaudo_registratore.py` (parte b) e `docs/COLLAUDI.md`:** la misura della finestra delle impostazioni e del pannello ora controlla anche che i caratteri veri del gioco siano caricati (come `collaudo_pannello.py` e `collaudo_suggerimento.py`) e stampa l'eccesso massimo in pixel; se i caratteri mancano lo dice e il collaudo esce con 1.
- **Descrizione corretta, non il motore:** `tests/lancia_tutti.sh` e `docs/COLLAUDI.md` dicevano «raffica a 20 nodi senza reagire circa 61°», ma `raffiche_e_virate.js` dà 55°. Verificato con `git show a64b3cf:index.html` che l'uscita (27°/41°/55° senza reagire, 16°/23°/31° lascando) è identica a quella attuale: solo la descrizione era sbagliata, ed è l'unica cosa corretta.
- **Verificato:** `collaudo_registratore.py` (parti b: caratteri e eccesso riportati; non ancora confermato a 1360×650 sul PC dell'utente, che vedeva lo sfondamento), `collaudo_pannello.py` a 1360×650 e 1360×768, `collaudo_lezioni.py`, `collaudo_schermate.py`, `collaudo_versione.py`: tutti OK nella sandbox; `polare.js` e `raffiche_e_virate.js` identici carattere per carattere. Da confermare: `tests/lancia_tutti.sh --solo registratore` sul PC dell'utente.

## 0.19 — linea d'arrivo nelle prove

Del 7 ottobre 2026. Decisione di settembre (osservazione 13). Proposta, banco e decisioni: `docs/PROPOSTA-LINEA-E-VISTA.md`; la parte B (tasto «vista») è rimandata alla 0.19.1.

- **Cosa cambia.** In tutte le prove l'arrivo non è più una boa da raggiungere entro 12 m, ma una **linea fra due boe piccole**: centrata dove prima c'era la boa d'arrivo, perpendicolare all'ultimo lato, larga 24 m (12 per lato, `FIN_HALF`, ipotesi nostra). Il cronometro si ferma all'istante esatto del taglio (interpolato fra due passi). Conta solo il taglio dal lato del percorso verso l'arrivo, fra le due boe comprese; passando fuori dagli estremi compare «Fuori dalla linea: passa tra le due boe», senza errore nel registro. Le boe non fanno da ostacolo e toccarle non è punito, come nelle regate. Conta il centro della barca: nella realtà la prua, circa 2 m prima (dichiarato).
- **Prove 1-3:** nessuna linea di partenza, il cronometro parte all'avvio come prima. **Prove 4 e 5:** la barca nasce sulla linea, che è partenza e arrivo come in regata; le boe restano da girare a sinistra, e il passaggio sulla linea prima del giro di boa non conta. Lezione 5, navigazione libera e regate invariate.
- **Testi:** descrizioni e istruzioni delle prove dicono «arrivo» invece di «boa» (nella prova 2 resta la frase della 0.18.4 sulla strambata); «Boa girata: ora verso l'arrivo»; nel pannello «Rilevamento boa» diventa «Rilevamento». Glossario: voce nuova «Linea d'arrivo». Riga nuova in `CONTENUTI-DA-VERIFICARE.md` (si arriva tagliando la linea dall'ultima boa; nella realtà conta la prua).
- **Registratore:** l'evento «boa» conta solo le boe girate; l'arrivo è solo l'evento «arrivo» (prima, nelle prove 1-3, l'arrivo contava anche come «boa»).
- **Salvataggi:** chiavi nuove in `KEYV` per le cinque prove (`m0.2`, `m1.2`, `m2.2`, `m3.3`, `m4.4`). Al primo avvio record, stelle e fantasmi delle chiavi vecchie delle prove si cancellano, senza migrazione, e il menu dice una volta sola «Le prove sono cambiate: i tempi salvati sono stati azzerati». Completamenti e regate restano.
- **Fasce** ricalcolate con la regola della 0.16 sui tempi del pilota di `collaudo_fasce.py` con la linea (8 venti per le prove 1-4, 24 corse a seme fisso per la prova 5):

  | Prova | Pilota prima | Pilota dopo | Fasce prima | Fasce dopo |
  |---|---|---|---|---|
  | 1 | 87,3 | 92,1 (+4,8) | 90/110/140 | 95/120/150 |
  | 2 | 136,2 | 142,6 (+6,4) | 140/175/220 | 145/180/230 |
  | 3 | 184,7 | 196,4 (+11,7) | 185/235/300 | 200/250/320 |
  | 4 | 327,0 | 333,4 (+6,4) | 330/410/525 | 335/420/535 |
  | 5, mediana | 347,6 (18 finite su 24) | 353,2 (18 finite su 24) | 355/440/565 | 355/440/565 |

  Le prove 1-4 danno lo stesso tempo con tutti gli 8 venti e coincidono al decimo con il banco della Fermata 1 (soglia ±0,5 s: è un controllo di riproducibilità, non di validità). La prova 3 sale di più perché gli ultimi 12 m sono di bolina. Prova 5: stessi semi prima e dopo; le corse non finite sono 6 in entrambe, con gli stessi venti tranne uno (prima vento 0, dopo vento 135). Una corsa resta lentissima in entrambe (842,6 e 847,9 s).
- **`collaudo_fasce.py`:** ogni corsa parte in una pagina nuova con `Math.random` a seme fisso (seme = numero della corsa + 1), così la prova 5 è riproducibile e due versioni si confrontano sugli stessi semi; stampa quante corse sono finite.
- **Nuovo collaudo `tests/collaudo_linea.py`:**
  - **Parte 1:** 5 prove × 8 venti, barca messa vicino alla linea che poi naviga con la fisica del gioco; la geometria della linea la ricalcola il collaudo per conto suo. **216 casi, 0 sbagliati:**
    - 40 tagli giusti: arrivo, tempo uguale all'istante interpolato, scarto massimo 2,2·10⁻¹⁶ s;
    - 40 tagli al contrario: niente arrivo;
    - 40 fuori dagli estremi: messaggio, poi rientro e arrivo;
    - 40 appena dentro un estremo (sopra una boa, da 11,90 a 12,00 m dal centro): arrivo, nessun errore;
    - 40 appena fuori (fino a 12,24 m): niente arrivo;
    - 16 nelle prove 4 e 5 prima del giro di boa: niente arrivo.
  - **Parte 2, pagina senza `#collaudo`: 8 verifiche su 8.** Dati vecchi cancellati con il messaggio una volta sola, regate e completamenti conservati, «Arrivo» disegnato nella prova 1 aperta dal menu.
  - Fallisce se un tipo di caso ha zero misure. Sulla 0.18.4 fallisce: 96 casi misurati, 160 sbagliati, 3 tipi con zero casi, 5 verifiche su 8.
  - **Difetto del collaudo, trovato al primo giro e corretto:** nella prova 3 il taglio «giusto» partiva 6 m prima della linea con la rotta a 60° dal vento. La barca si spostava di lato di 12,6 m e tagliava fuori dagli estremi: il gioco diceva giustamente «Fuori dalla linea» e i casi risultavano sbagliati (8 su 40). Ora parte a 3 m.
- **Altri collaudi adattati:** `collaudo_pannello.py` misura anche il riquadro delle istruzioni di ogni prova e regata nella pagina senza `#collaudo`, con l'oro atteso nell'orologio aggiornato. `collaudo_giro_boa.py`: nome del caso f. `tests/lancia_tutti.sh`: nuovo collaudo (esito chiaro) e nota di `collaudo_fasce.py` coi nuovi tempi. `collaudo_registratore.py` cercava nel file la scritta fissa «# gioco 0.18» e con la 0.19 falliva: ora legge `VERSIONE` da `index.html`.
- **Verificato:**
  - `collaudo_linea.py` tutto OK.
  - `collaudo_fasce.py`: tabella sopra.
  - `collaudo_giro_boa.py`: prove 1-3 finite in 92, 156 e 197 s col pilota in tempo reale; i casi sbagliati non finiscono, con 1 giro sbagliato.
  - `collaudo_registratore.py`:
    - parte b: nelle 5 sessioni della prova 3, file e gioco danno 10 virate, 0 boe e 1 arrivo;
    - parte c: 50 corse identiche su 50;
    - parte a rilanciata dopo la correzione: 9 su 9.
  - `collaudo_pannello.py` a 1360×650 e 1360×768: caratteri veri caricati, eccesso 0 px, riquadro delle istruzioni 0 px in 6 misure.
  - `collaudo_lezioni.py`, `collaudo_schermate.py`, `collaudo_versione.py`: OK.
  - `polare.js` e `raffiche_e_virate.js` identici carattere per carattere.
  - Il layout a 1360×650/768 lo conferma il PC dell'utente.

## 0.18.4 — giro di testi: strambata, orziera

- Prova 2 «Lasco e poppa»: il testo dice ora anche cosa fare se la strambata è inevitabile («cazza prima tutta la vela, così la strambata è controllata»), dopo che una registrazione ha mostrato una strambata violenta non prevista.
- Lezione 2, passo «Tenere la rotta»: la prima frase sull'orziera è più generica («la barca tende a salire da sola verso il vento», senza attribuirla a una causa sola) e rimanda al glossario.
- Glossario, voce «Orziera» (nuova): elenca le cause che possono sommarsi — vento e raffiche, onde, sbandamento, vele troppo cazzate, posizione e peso dell'equipaggio — e come si corregge.
- **Solo controllo, nessuna modifica al motore:** misurato fuori da `step()` (banco separato, `tests/fisica/motore.js` non toccato) quanto distano la soglia di `ttState()` che dà «wind» (filetto sopravento, incidenza 8°) e quella della resistenza aggiunta della vela nella forza (incidenza 6°). Nel disegno le due soglie coincidono sempre (stesso stato, differenza 0°). Nella forza la differenza è di 2° di incidenza, cioè 3,76° di boma a bolina larga (65° veri) e 4,34° al traverso (90° veri) — sopra i 3° indicati; al lasco (120° veri) nessuna delle due soglie è raggiungibile nemmeno a scotta tutta lascata (incidenza minima ≈12°). Dettagli in `docs/OSSERVAZIONI-GIOCANDO.md`, voce 15 del 7 ottobre 2026. Nessuna modifica fatta.
- Verificato non-regressione: `collaudo_lezioni.py`, `collaudo_quiz.py`, `collaudo_schermate.py`, `collaudo_pannello.py` (1360×650 e 1360×768), `collaudo_suggerimento.py`, `collaudo_versione.py`; `polare.js` e `raffiche_e_virate.js` non toccati (identici). Il layout del pannello a 1360×650/768 lo conferma il PC dell'utente.

## 0.18.3 — versione del gioco a schermo

- La costante `VERSIONE` (che il registratore di sessione già scriveva nel file) non arrivava più a schermo da 0.18.2: aggiornata a «0.18.3» insieme a questa voce.
- **Dove si vede**, sempre letto da `VERSIONE` (nessun testo scritto a mano altrove): nel menu, discreta a fianco del titolo «Scuola di vela»; sul mare, in alto a destra sotto la bussola e sopra i pulsanti dello zoom — l'unico angolo libero a 1360×650 e 1360×768 (non copre il quadrante prua e vento in basso a sinistra, la scritta del vento e il «● REG» in alto a sinistra, la bussola in alto a destra, i pulsanti dello zoom in basso a destra).
- **Nuovo collaudo** `tests/collaudo_versione.py`: la versione nel menu e quella sul mare coincidono con `VERSIONE`, e `VERSIONE` coincide con il numero più alto dei titoli di `CHANGELOG.md` (ignorando i titoli «Sperimentale» e il testo dopo il numero). Fallisce se uno dei due confronti non viene eseguito e fallisce sulla versione precedente a questa modifica (dove la costante era ferma a «0.18»).
- Verificato non-regressione: `collaudo_pannello.py` (1360×650 e 1360×768, 0 px di eccesso), `collaudo_schermate.py`, `collaudo_lezioni.py`, `collaudo_registratore.py` tutti OK; `polare.js` e `raffiche_e_virate.js` non toccati (identici).

## 0.18.2 — pannello a 1360×650 con i caratteri veri

- **Difetto, misurato sul PC dell'utente con `tests/collaudo_suggerimento.py` a 1360×650 (caratteri veri):** il pannello eccedeva di **+47 px** nella lezione 3 passo 13 («Riepilogo», l'ultimo: il pulsante «Prosegui: Prova 1: Al traverso» va a capo sotto Indietro/Ricomincia/Fai il ripasso e la legenda dei tasti sfora), di **+4 px** nella lezione 1 passo 10 («Troppo cazzata») e di **+2 px** nella lezione 2 passo 4 («Barra sottovento»). Con tutti e tre i testi del consiglio l'eccesso era identico: non dipendeva dal testo del suggerimento ma dal resto del pannello.
- **Perché i collaudi di Claude Code non lo vedevano.** I font del gioco (Barlow Semi Condensed, Source Serif 4) arrivano da Google Fonts via `<link>`: senza rete verso quel servizio il browser li sostituisce con un carattere di sistema, con uno spazio occupato diverso. Caricandoli davvero (stessa rete, stesso Chromium di Playwright) l'eccesso misurato resta comunque **0 px**: i font non spiegano tutta la differenza. Misurando passo per passo si è trovato che nella lezione 3 passo 13 il pulsante «Prosegui» **va già a capo su una seconda riga anche in questo ambiente**, con soli ~7 px di margine prima di sforare; restringendo apposta la larghezza utile del pannello di appena 12 px (meno di una scrollbar classica, circa 15-17 px, che l'headless Linux di questo ambiente non riserva mentre un browser vero su un altro sistema può riservare) basta per farlo sforare di 12 px, e di 40 px per sforare di 36. Il margine era quindi già sottilissimo: bastano differenze di carattere o di scrollbar fra sistemi diversi per far saltare fuori numeri come +47, +4 e +2. **Non è stato possibile riprodurre esattamente +47/+4/+2 px in questo ambiente**: la correzione sotto è fatta sulle cifre dell'utente ma non verificata da lui con le sue cifre.
- **Corretto**, solo spaziature (nessun testo didattico tolto): riquadri del pannello `.panel` da `10px`/gap `9px` a `8px`/gap `7px`; righe di pulsanti `.row` da gap `8px` a `6px` e padding dei pulsanti nel pannello da `5px 12px` a `4px 10px`; margine sopra la riga dei pulsanti della lezione da `12px` a `8px`. Nessuna griglia o grafica toccata.
- **Numeri (in questo ambiente, con i caratteri veri):** lezione 3 passo 13, prima restringendo la larghezza di soli 12 px si eccedeva già di 12 px; dopo la correzione occorrono almeno 32 px di restringimento prima di eccedere (margine quasi triplicato). `collaudo_pannello.py` e `collaudo_suggerimento.py` a 1360×650 e 1360×768: eccesso massimo 0 px, come prima della correzione — non essendo riuscito a riprodurre il difetto originale, non si può dire che il margine guadagnato basti per i +47 px del PC dell'utente: lo deve confermare lui con `tests/collaudo_suggerimento.py`.
- **Collaudi resi affidabili.** `collaudo_pannello.py` e `collaudo_suggerimento.py` ora controllano con `document.fonts.check` che i caratteri del gioco siano davvero caricati, lo scrivono in chiaro (`caratteri del gioco caricati: True/False`) e dichiarano la misura non valida (uscita 1) se mancano, invece di passare leggendo un eccesso di 0 px che non vuol dire niente.
- Verificato non-regressione: `collaudo_pulsanti.py` OK; `polare.js` e `raffiche_e_virate.js` non toccati (identici).
- **Seconda correzione, misurata dall'utente dopo la prima:** con `tests/collaudo_suggerimento.py` a 1360×650 e caratteri veri confermati (`True`), i due casi minori (lezione 1 passo 10, lezione 2 passo 4) sono spariti; resta **un solo caso**, lezione 3 passo 13 («Riepilogo»), con un eccesso sceso da **+47 a +25 px**, identico con tutti e tre i testi di prova.
- **Causa:** nel passo 13 la riga dei pulsanti (Indietro, Ricomincia, Fai il ripasso, «Prosegui: Prova 1: Al traverso») va a capo perché il pulsante «Prosegui» è lungo, e il testo didattico del passo è anch'esso lungo.
- **Corretto:** la funzione che genera l'etichetta «Prosegui: …» (`itemName`) non ripete più il titolo della lezione o della prova successiva, già indicato nel titolo del passo che si apre: da «Prosegui: Prova 1: Al traverso» a «Prosegui: Prova 1», da «Prosegui: Lezione 4: Vento reale e apparente» a «Prosegui: Lezione 4». Un solo punto nel codice, quindi la correzione vale automaticamente per **tutti** i passi finali di lezione che portano a una prova o a una lezione successiva (lezioni 1-6), non solo per la lezione 3. Nessun testo didattico tolto, nessuna grafica toccata.
- **Calcolo (struttura del pannello, non misura — la misura resta 0 px in questa sandbox): l'etichetta accorciata non basta a risolvere il caso della lezione 3.** I tre pulsanti Indietro/Ricomincia/Fai il ripasso occupano da soli circa 299 px su 357 disponibili (pannello di 390 px a 1360 px di finestra): qualunque etichetta ragionevole del quarto pulsante va comunque a capo, accorciata o no. Confrontando sezione per sezione il pannello con l'etichetta lunga e con quella corta, le due altezze restano **identiche** fino a restringere la larghezza utile di circa 60 px — molto oltre la soglia di circa 32-40 px a cui si manifesta l'eccesso reale misurato dall'utente. Quell'eccesso viene dal **testo del passo** (due paragrafi), che guadagna una riga in più ogni circa 24 px di restringimento: è lì, non nel pulsante, che si consuma il margine mancante.
- **Dove la correzione aiuta davvero:** nei passi finali di lezione 5 e lezione 6, dove la prova successiva ha un nome più lungo («Prova 3: Risalire il vento», «Prova 5: Percorso nelle raffiche»), il margine prima che il pulsante «Prosegui» vada a capo *una seconda volta* (tre righe invece di due) sale da 60 a 91 px di restringimento (lezione 5) e da 41 a 60 px (lezione 6): un vantaggio reale, ma su un fronte diverso da quello misurato nella lezione 3.
- **Dichiarato:** con questa sola correzione la lezione 3 passo 13 non raggiunge il margine di almeno 40 px richiesto; il calcolo indica che l'eccesso resta vicino ai +25 px misurati dall'utente. Per colmarlo servirebbe accorciare il testo didattico del passo (due paragrafi), una modifica di contenuto che esce da «solo CSS e disposizione» e non è stata fatta: resta da decidere.
- Verificato non-regressione: `collaudo_suggerimento.py`, `collaudo_pannello.py` (1360×650 e 1360×768), `collaudo_lezioni.py`, `collaudo_pulsanti.py` tutti OK; `polare.js` e `raffiche_e_virate.js` non toccati (identici).
- **Terza correzione: il testo del passo 13, accorciato.** I due paragrafi («Le andature... Si naviga mure a dritta o mure a sinistra.» / «Ogni andatura vuole la sua regolazione... poi passa alle prove 1 e 2, dove il vento non arriva più sempre da nord.») sono diventati un solo paragrafo: «Le andature, dalla più vicina alla più lontana dal vento: bolina, traverso, lasco, gran lasco, poppa. Ognuna vuole la sua regolazione, e i filetti te la indicano. Ora passa alle prove: il vento non arriverà più sempre da nord.» Nessun quiz, voce di glossario o collaudo faceva riferimento alle frasi tolte. Verificato: `collaudo_suggerimento.py`, `collaudo_pannello.py` (1360×650 e 1360×768), `collaudo_lezioni.py`, `collaudo_pulsanti.py`, `collaudo_quiz.py` tutti OK in questa sandbox (eccesso 0 px, come prima di questa correzione); **non essendo riuscito a riprodurre qui l'eccesso di +25 px dell'utente, solo il suo collaudo con `tests/collaudo_suggerimento.py` sul suo PC può confermare se il testo più corto lo ha davvero colmato.**

## 0.18.1 — pulsanti didattici Cazza e Lasca

- **Difetto.** Nella lezione 1, i pulsanti sullo schermo «Cazza» e «Lasca» (passi «La scotta: lascare» e «La scotta: cazzare»), cliccati più volte di seguito nello stesso punto dello schermo senza rimirare il pulsante a ogni clic (come capita cliccando in fretta), smettevano di funzionare o facevano sparire la scritta di passo completato. Con i tasti W/S non capitava.
- **Causa.** Quando il passo si completa compare la scritta «passo completato» (`#lFeedback`) e il pulsante «Avanti» (`#lNext`) sopra ai pulsanti Cazza/Lasca, nel riquadro della lezione: quel testo aggiunge altezza e **sposta in basso** i due pulsanti, che stanno più sotto nella stessa colonna del pannello. Un clic successivo nello stesso punto dello schermo non cade più sul pulsante ma su quello che gli è scorso sotto. Misurato con un vero clic del mouse fermo nello stesso punto, ripetuto: a 1360×650, passo «lascare», lo spostamento è di **88 px** e il clic finisce sulla scritta di suggerimento (inerte, nessun danno misurato a questa risoluzione); con un carattere più grande (accessibilità, scala solo il testo e non il pannello) lo spostamento basta a far cadere il clic sul pulsante **«Avanti»**, che avanza il passo e **annulla la scritta di passo completato** del passo corrente — a 24 px di base, clic di prova: `#13 stepDone=True elemento=lNext` seguito da `#14 stepDone=False`. I tasti non ne risentono perché non dipendono dalla posizione sullo schermo.
- **Corretto.** `#lFeedback` e `#lNext`, solo nei passi con pulsanti Cazza/Lasca attivi, riservano da subito lo spazio che occuperanno da completati (invisibili con `visibility:hidden`, non `display:none`): completare il passo non cambia più l'altezza del riquadro, quindi i due pulsanti non si spostano più. Negli altri passi (nessun pulsante sullo schermo, nessun rischio di questo tipo) il comportamento resta quello di prima, a costo zero di spazio. Tasti e fisica non toccati.
- **Numeri.** Collaudo nuovo `tests/collaudo_pulsanti.py`: 22 clic fermi sul pulsante Lasca (passo «lascare») e 22 su Cazza (passo «cazzare»), a 1360×650. Prima della correzione: dopo il completamento il clic finisce sulla scritta di suggerimento, la scotta si ferma a 0,967/0,492 invece di arrivare a fine corsa — fallisce (`exit 1`). Dopo: il clic resta sul pulsante, la scotta arriva a 1,000/0,000, il passo completato resta completato — passa (`exit 0`). Il riquadro appena riservato eccedeva di 3 px nel caso peggiore della lezione 1 passo «lascare» (`collaudo_suggerimento.py`); tolti 2 px di margine e 2×2 px di margine interno a `.feedback` (invisibile a vista) per tornare a **0 px di eccesso**, confermato anche a 1360×768.
- Verificato non-regressione: `collaudo_lezioni.py`, `collaudo_schermate.py`, `collaudo_suggerimento.py`, `collaudo_registratore.py` tutti OK; `collaudo_pannello.py` a 1360×650 e 1360×768 senza eccesso; `polare.js` e `raffiche_e_virate.js` non toccati (identici).

## 0.18 — registratore di sessione

Del 5 ottobre 2026. Proposta, confronto delle tre vie e decisioni: `docs/PROPOSTA-REGISTRATORE.md`.

- **Cosa fa.** Nelle impostazioni (⚙) c'è la casella «Registra la sessione», **spenta a ogni apertura della pagina** (non viene salvata). Da accesa:
  - il gioco annota eventi, messaggi, tasti e lo stato della barca una volta al secondo;
  - il tasto **M** mette un marcatore «qui qualcosa non va»;
  - sul mare compare la spia «● REG» (diventa «● REG · M1» per un attimo dopo M);
  - «Scarica» crea un file di testo nel browser, senza nessuna connessione;
  - il campo «Nota» elenca i marcatori presi, così si scrive a quale ci si riferisce;
  - chiudendo la pagina con una registrazione non scaricata, il browser chiede conferma.
- **Il file**, testo semplice:
  - in testa: versione, impostazioni, nota e un riassunto (eventi, tempo per andatura, suggerimenti con quante volte e quanti secondi, tempo per passo di lezione, marcatori), poi una legenda;
  - poi una riga per ogni cosa: stato, evento, passo di lezione, suggerimento, messaggio a comparsa, regola di regata, errore interno, tasto, marcatore, impostazioni.
  - **Contenuto:** solo i tasti del gioco (frecce, spazio, W, S; R come evento «raddrizza»; M come marcatore). L'unico testo digitato è la nota; nessun dato personale.
  - **Il tempo** è quello vero di gioco, pause di lettura comprese; il menu non conta.
- **Peso misurato:** circa **290 KB per un'ora** (media di 5 sessioni da circa 3 minuti, proiettata). Stima della proposta: 230-330 KB.
- **Come è fatto.** Un blocco unico prima di «CICLO» (`ses`, `sesTick`), più quattro punti sparsi:
  - la costante `VERSIONE`;
  - una chiamata in `tick`;
  - una in `__sv.run`;
  - l'HTML e il CSS nelle impostazioni.

  Il registratore **legge soltanto**: confronta a ogni fotogramma contatori, registro degli errori, messaggi, testi del pannello, tasti e impostazioni con quelli del fotogramma prima. Non chiama `Math.random` e non scrive variabili del gioco. Motore, `simulate`, `panel`, `toast`, `regAdd` e l'ascoltatore dei tasti non sono toccati.
- **Tasto M e campi di testo.** M e la registrazione dei tasti non scattano mai se il focus è in un campo di testo: nota, ricerca del glossario e simili. Lo controlla l'elemento col focus.
- **Nuovo script** `tests/analizza_sessione.py`. Legge un file e stampa: eventi, tempo per andatura, suggerimenti più visti, passi di lezione, rallentamenti (velocità scesa di oltre metà in 5 s, soglia nostra) e i dieci secondi attorno a ogni marcatore. Poi confronta eventi, suggerimenti e marcatori con il riassunto scritto dal gioco: sono due conti indipendenti. Controllo `--prova` su un file d'esempio, compreso un riassunto sbagliato apposta: superato.
- **Nuovo collaudo** `tests/collaudo_registratore.py`, quattro parti.
  - **(a) Pagina vera, senza `#collaudo`: 9 verifiche su 9, ripetuto 5 volte.**
    - aggancio assente;
    - interruttore spento all'apertura;
    - M da spento non mette marcatori;
    - accesa col clic, il file contiene 1 marcatore, i tasti `→ giù`/`→ su`, la versione e lo stato;
    - avviso alla chiusura presente con registrazione non scaricata, assente se non si è mai registrato.
  - **(b) 5 sessioni**, venti 45°, 90°, 135°, 180° e 225°, finestre alternate 1360×650 e 1360×768. Il pilota gioca la prova 3 (finita in 185 s ogni volta), poi la lezione 2. Il collaudo:
    - preme M due volte e ↑, ← una volta;
    - digita la nota «m w s r mamma: …» e poi ←, M dentro il campo;
    - scarica il file e lo legge.

    Esiti in tutte e 5:
    - 2 marcatori nella posizione in cui sono stati premuti (scarto ≤ 0,05 m, cioè l'arrotondamento a un decimale);
    - i 4 tasti nell'ordine;
    - nessun marcatore né tasto in più digitando la nota (che contiene anche ← e M finiti nel campo, come devono);
    - 7 virate, 1 boa e 1 arrivo come nei contatori del gioco (confronto in parte circolare, perché il registratore legge proprio quei contatori);
    - passi 2.1-2.4 tutti presenti;
    - righe di stato con al massimo 1,10 s di distanza (circa 193 righe);
    - riassunto del gioco uguale a quello ricalcolato dallo script.

    Il tempo per andatura dello script, stimato dalle righe di stato, è più alto di quello del gioco (bolina stretta 173-176 s contro 165), perché l'orologio della registrazione conta anche il tempo vero fra un pezzo e l'altro del pilota: è dichiarato approssimato.
  - **(c) Fisica identica al bit** (sotto).
  - **(d) Costo** (sotto).
- **Tre errori del metro, trovati e corretti prima di accettare i numeri.**
  - Il primo controllo sui marcatori sommava gli scarti di x e y contro 0,05 m, ma il file scrive ogni coordinata con un decimale. Falliva con scarti di 0,06-0,085 m che erano solo arrotondamento.
  - Il primo controllo sulla nota cercava il testo digitato intatto, ma il collaudo stesso, premendo ← e M dentro il campo, lo modificava. Ora confronta col valore vero del campo.

  - L'avviso alla chiusura si provava chiudendo la scheda (`page.close(run_before_unload=True)`), e passava **2 volte su 6**. Il gioco era giusto: il gestore blocca l'evento, la pagina è caricata, l'utente ha interagito e `ses.dirty` era vero **9 volte su 9**. È il browser senza finestra che, chiudendo la scheda, non mostra l'avviso in modo affidabile: **3 su 4** anche su una pagina minima con lo stesso gestore. Uscendo dalla pagina con una navigazione, l'avviso compare **4 volte su 4** con una registrazione non scaricata e **0 su 4** senza. Il collaudo ora usa la navigazione: 5 giri su 5 superati.

  In tutti e tre i casi il gioco era giusto.
- **Fisica identica al bit, registratore acceso e spento.** `Math.random` con seme sostituito dal collaudo, `__sv.run` a passi fissi di 1/60 s, 10 semi per caso. Casi: prove 1, 2 e 3 (200 s) e navigazione libera con raffiche forti a 10 e 15 nodi (150 s, 13 scuffie in tutto a 15 nodi). Confronto su posizione, prua, velocità e sbandamento a ogni passo. **50 corse su 50 identiche.**
  - **Il metro vede le differenze:** consumando di proposito un numero casuale in più a metà corsa, le traiettorie divergono **20 volte su 20** in navigazione libera, dove si usano circa 255 numeri casuali a corsa.
  - **Dove il metro non può vedere quella differenza:** nelle prove 1-3 non si usa nessun numero casuale, quindi lì la variante resta identica.
  - **Difetto del banco, trovato con un controllo:** la prima versione faceva tutte le corse nella stessa pagina e dava **0 su 10** identiche in navigazione libera. Ripetendo due volte la stessa corsa **a registratore spento** il risultato era lo stesso, quindi la colpa era del banco. Causa: con le raffiche la direzione del vento oscilla con `simTime`, che conta dall'apertura della pagina e non si azzera cambiando modalità; ogni corsa partiva con un vento diverso. Ora ogni corsa parte in una pagina nuova, e il controllo «spento ripetuto due volte» resta nel collaudo (50 su 50).
- **Costo** (navigazione libera, raffiche forti, `__sv.run` da 20 000 passi, 3 ripetizioni, misurato due volte):
  - spento 3,6-5,2 µs per passo, acceso 9,0-10,4: circa **+5,5 µs per passo**, contro la soglia nostra di 50;
  - fotogrammi al secondo invariati: **59,7-60,6** acceso e spento.

  Il registratore costa circa il doppio del passo di simulazione da solo, ma in assoluto è un centesimo di fotogramma.
- **Non-regressione.**
  - Zona del motore identica riga per riga (91 righe);
  - uscite di `polare.js` e `raffiche_e_virate.js` **identiche carattere per carattere** a quelle salvate prima della modifica;
  - `git diff` vuoto su `sperimentale/`;
  - `collaudo_pannello.py` «nessuno» e tutti `True`, a 1360×650 e a 1360×768;
  - `collaudo_schermate.py` `errori: []`;
  - `collaudo_lezioni.py` tutti `OK`, salvo il «primo tratto» di «cazzare», che è un caso di attesa previsto dallo script;
  - `collaudo_suggerimento.py` nessun caso sbagliato, pannello a 0 px.
- **La finestra delle impostazioni non ci stava già prima, e col registratore peggiorava.**
  - **Prima della modifica:** in navigazione libera, dove ha in più le tre scelte del vento, scorreva di **48 px a 1360×650** (difetto preesistente, mai misurato) e di 0 a 1360×768.
  - **Con le righe del registratore:** **117 px** e **11 px**.
  - **Perché il collaudo b non lo vedeva:** misurava la finestra solo in lezione, dove quelle tre righe non ci sono. Ora misura anche la navigazione libera.
  - **Correzione, solo CSS, testi invariati salvo la casella del registratore:**
    - le tre scelte del vento su una riga;
    - 6 px fra le righe invece di 10;
    - 12 px di spazio in fondo invece di 20;
    - casella del registratore su una riga, con «il file resta sul tuo computer» spostato nel segnaposto della nota;
    - elenco dei marcatori su una riga, con il testo intero al passaggio del mouse.
  - **Risultato nel caso peggiore** (navigazione libera, nota e marcatori visibili): **0 px** a 1360×650 (577 px di contenuto su 585 disponibili, 8 px di margine) e a 1360×768.
  - **Caratteri:** misure fatte senza i caratteri del gioco installati (caratteri di riserva più larghi), quindi pessimistiche.

## 0.17.1 — correzione di «scadere»

- **Difetto.** Il gioco usava «scadere» per la prua che gira da sola allontanandosi dal vento (lezione 5, suggerimento dal vivo, glossario). **Causa:** due glossari pubblici (marinasveva.com, scuolavelaargentario.com) definiscono «scadere» come essere spinti sottovento da scarroccio o corrente, non la prua che gira: il termine giusto è «poggiare». **Corretto** nei testi di lezione 5 e del suggerimento dal vivo (ora «lascia che la prua poggi da sola»); tolta la voce di glossario «Scadere», introdotta nella 0.17 e ridondante con «Scarroccio» già presente. Nessun cambiamento alla fisica.
- Aggiornati `tests/collaudo_suggerimento.py` (testo atteso) e i documenti in `docs/`.

## 0.17 — «Tenere la rotta» che si vinceva da sé, partenza di regata rifatta, testi delle lezioni più precisi

### Lezione 2, «Tenere la rotta»: il passo si completava senza toccare nulla

- **Difetto.** Giocando, la barca teneva la rotta da sola e il passo si completava. **Causa:** nel passo convivono due disturbi di forza molto diversa, l'orziera (2 °/s costanti verso il vento) e le spinte delle onde (3–6 °/s per 0,8 s, una ogni 1,8–3,4 s). Ogni spinta d'onda vale 2,4–4,8°, cioè da una volta e mezza a tre volte l'orziera, e **il suo segno è casuale**. La condizione chiede 8 secondi entro 6°: in 8 secondi l'orziera accumula 16°, e in quegli stessi 8 secondi cadono tre o quattro spinte che, se escono tutte col segno «poggia», la cancellano. Quando capita il passo si completa **esattamente all'ottavo secondo**, cioè subito, mentre il giocatore legge il testo. Verifica col segno forzato: onde che poggiano sempre, completato a 8,0 s; onde che orzano sempre, non completato. Se non si vince nei primi 8 secondi non si vince più, perché dopo la deriva ha già portato la prua fuori: allargando la finestra da 30 a 60 secondi i completamenti non cambiano.
- **Decisione:** orziera da 2 a 3 °/s, onde invariate. `yawNoise: true` è usato in un solo passo, quindi è l'unico toccato.
- **Numeri.** Si completa da sé: 0.16 nel browser **5 su 60**, circa una volta su otto, con tenuta di 8,0 s; 0.17 Monte Carlo sul motore **0 su 3000**, 0.17 nel browser **1 su 1000** (tenuta massima 8,0 s). Il Monte Carlo è stato ripetuto su sette prue di ingresso con gli stessi semi: è lo stesso esperimento ripetuto, quindi il numero è 0 su 3000, non 21 000. **Il caso raro è reso molto improbabile, non escluso**, e il Monte Carlo sul motore estratto lo sottostima rispetto al browser: causa non indagata.
- Il passo resta fattibile correggendo: un pilota pronto completa 6 su 6 in 8,0 s, che è il minimo possibile, identico alla 0.16 misurata nello stesso momento. Un pilota lento, che guarda la rotta due volte al secondo: 12 su 12 in entrambe le versioni, mediana 8,0 s, caso peggiore da 18,5 a 25,1 s.
- **Difetto di metodo.** `collaudo_rotta.py` faceva **un solo** tentativo senza correzioni e concludeva che il passo non si completava da sé. Con una probabilità di una volta su otto, un tentativo singolo mostra quasi sempre il fallimento: il collaudo non era sbagliato, era sotto-campionato. Riscritto con molti tentativi a passi fissi (`__sv.run`), entrando dal traverso e dalle andature larghe, e stampa i **secondi in rotta di fila raggiunti al massimo**, che è il margine vero. Aggiunto il punto in `COLLAUDI.md`: un solo tentativo non basta nemmeno per dire che una cosa **non** succede.

### Partenza di regata: posizioni casuali e caratteri degli avversari

- **Difetto.** Il giocatore nasceva sempre in (10, 45) mure a sinistra e la Blu in (28, 50) mure a dritta: rotta di collisione frontale, e in caso di contatto la penalità di 15 s era sempre del giocatore, perché mure a sinistra. **Causa:** posizioni iniziali fisse. Misurato: distanza minima all'avvio **18,1 m** e avvicinamento minimo **4,9 m a 6 secondi**, identici a ogni partenza. Il contatto scatta sotto i 4,2 m, quindi mancavano 0,7 m.
- **Decisioni:** posizioni casuali per tutti, giocatore compreso, dietro la linea, ben distanziate e senza coppie in rotta di collisione; tre caratteri degli avversari (prudente, normale, aggressiva), estratti a sorte a ogni partenza; una sola aggressiva e solo con gli esperti; il carattere di ogni barca scritto nel riquadro delle istruzioni.
- **Posizioni** (`startSpots`): le barche si piazzano una alla volta, scartando chi sta a meno di 20 m da un'altra o si avvicinerebbe sotto i 14 m entro 25 secondi; se una non trova posto si riparte da zero, fino a 40 giri, con un ripiego a zigzag calcolato a mano. Banda x ±30 m, y 38–74 m dalla linea, **26–54 m quando la preparazione è di un minuto**. Risultato: distanza minima all'avvio da 18,1 m fisso a **19,8–28,8 m**, avvicinamento minimo da 4,9 m a **14,9–18,7 m**. Campionatore verificato fuori dal browser: **0 configurazioni fuori vincolo su 20 000** per ciascuna preparazione, con una e con quattro barche.
- **Caratteri.** La *prudente* evita le altre da 22 m invece di 14, anche quando ha la precedenza. La *normale* si comporta come prima. L'*aggressiva* attende dall'altro lato della linea, così ci arriva mure a dritta con la precedenza in mano, e punta le barche mure a sinistra entro 40 m per costringerle a manovrare. Rispetta lo spirito delle regole 14 e 16: sotto 15 m (`AGGRO_OFF`) smette di stringere e sotto 14 m cerca comunque di non urtare, così una manovra per evitarla esiste sempre. La regola 16 vera **non** è stata aggiunta: la colpa di un contatto la decidono solo mure e sopravento, come prima.
- **L'aggressiva resta evitabile.** Il collaudo riprova lo stesso incontro con manovre diverse, salvando e rimettendo lo stato della regata, e la manovra parte **un secondo dopo** l'inizio dell'incontro. Con `AGGRO_OFF` a 15, 18 e 22 m il risultato è **40 incontri su 40** evitabili in tutti e tre i casi, su quattro distanze d'incontro (18, 24, 30, 38 m): scelto **15 m**, il valore più basso che basta, quindi nessuna modifica. In un campione indipendente precedente, a 15 m un incontro su 40 non aveva via d'uscita ritardata: con 40 incontri per valore la differenza fra 0 e 1 è dentro il rumore, quindi **il tasso di fallimento è basso ma non dimostrato nullo**. Le manovre provate sono solo le due estreme, barra tutta da un lato, mentre un giocatore vero può anche virare o rallentare.
- **Ritardi al via.** La **finestra di misura è la stessa** per 0.16 e 0.17 (stesso script, stessa formula: preparazione più circa 60 s di gioco dopo il via), ma si confrontano **solo le mediane**: le barche che non tagliano la linea entro la finestra vengono escluse dal conteggio, sono per definizione le più in ritardo, e il loro numero cambia fra le versioni, il che abbassa la media. Il confronto è principianti contro principianti, perché la 0.16 era misurata solo al livello predefinito. Mediane con 1, 3 e 5 minuti di preparazione, 10 partenze per tipo: 0.16 **9,4 / 9,3 / 8,7 s**, 0.17 principianti **3,7 / 3,0 / 3,4 s**, 0.17 esperti **4,4 / 5,8 / 6,1 s**.
- **Causa dei ritardi a un minuto, trovata misurando:** la distanza iniziale dalla linea. Correlazione fra distanza e ritardo **+0,75**, con 5,4 s di mediana per chi nasceva vicino contro **24,9 s** per chi nasceva lontano. Avvicinando la banda a 26–54 m la correlazione è scesa a +0,28 e il divario a 3,5 contro 4,2 s.
- **Partenze anticipate degli avversari.** Prima del via non superano la linea se sono a meno di **7 m** da essa (era 4 m): con le posizioni casuali e la prudente che evita da 22 m, qualcuna ci scivolava oltre. Restano **3 partenze anticipate su 90 con i principianti** (2 con un minuto di preparazione, 1 con tre) e **0 su 90 con gli esperti**: accettate così, perché è plausibile che un principiante anticipi e il gioco lo gestisce già, facendolo tornare dietro la linea.
- **Record delle regate invariati.** Il percorso non cambia — linea, boa e distanze sono identiche — e cambia solo da dove parte il giocatore dietro la linea: i tempi restano confrontabili e `KEYV` non si tocca.
- **Nuovo collaudo** `collaudo_aggressiva.py`. `collaudo_partenze.py` esteso: prende il numero di partenze e il livello degli avversari, e misura anche distanza minima all'avvio, avvicinamento minimo, caratteri assegnati e la correlazione fra distanza dalla linea e ritardo.
- **Collaudi:** 10 regate (6 a bastone, 4 nelle raffiche) con tutti gli avversari all'arrivo e nessuna bloccata; fantasma con gli esperti 3 corse su 3, fantasma salvato; pannello a 1360×650 senza eccedenze e i quattro `True` del riquadro, anche col testo più lungo dei caratteri; riquadro coerente con i caratteri veri, 0 aggressive su 6 partenze con i principianti e 6 su 6 con gli esperti; lezioni tutte completate.
- **Due misure buttate via, entrambe per lo stesso errore: il metro di misura legato a ciò che si voleva misurare.** La prima versione del collaudo dell'aggressiva poggiava **sempre**, e a 18 m poggiare è spesso la manovra sbagliata, perché il giocatore si trova sopravento e poggiando le va incontro: 4 contatti su 10 che sembravano colpa del gioco. La seconda faceva partire la manovra dalla condizione «l'aggressiva mi sta puntando», che dipende da `AGGRO_OFF`: con la soglia a 22 m e un incontro a 18 m la manovra non partiva mai, e le quattro righe davano numeri identici. Entrambe le avvertenze sono ora in `COLLAUDI.md`.
- **Difetto introdotto e corretto nella stessa sessione:** con la banda ravvicinata, il campionatore delle posizioni non riusciva a sistemare quattro barche e ricadeva sul ripiego **3823 volte su 20 000**, e il ripiego era scritto male, con barche fino a **0,2 m** l'una dall'altra, cioè molto peggio del difetto che si stava correggendo. La prima verifica non lo vedeva perché controllava solo la distanza minima, che il vecchio ripiego rispettava, e non che le posizioni fossero dentro la banda sorteggiata.

### Il riquadro delle istruzioni non compariva mai nel gioco vero

- **Difetto.** Entrando in una regata dal menu, o con «Ricomincia», il riquadro iniziale con «Parti» non compariva e il conto alla rovescia partiva subito. Lo stesso in tutte e cinque le prove, dal menu e con «Ricomincia la prova»: il cronometro partiva senza che il giocatore avesse letto nulla. Le lezioni non hanno riquadro all'avvio e non erano toccate.
- **Conseguenza peggiore del riquadro mancante:** i menu **Avversari** e **Preparazione** stanno solo dentro il riquadro, e solo nella sua prima apertura (`bRaceOpts` è nascosto quando `first` è falso, `index.html:1078`). Riaprendo le istruzioni col pulsante «Istruzioni» non ricompaiono. Quindi dalla 0.15 alla 0.17 **il giocatore non aveva alcun modo di cambiare il livello degli avversari o la durata della preparazione**: restavano per sempre su «principianti» e «3 minuti». Tutte le misure di quelle impostazioni erano state fatte dai collaudi, che le scrivono direttamente sui menu a tendina. Ora funzionano: verificato nel gioco vero che scegliendo «5 minuti» o «nessuno, solo il fantasma» la regata ricomincia e il testo del riquadro cambia di conseguenza.
- **Causa.** L'aggancio dei collaudi è scritto senza graffe:

  ```js
  if (location.hash === "#collaudo") window.__sv = { ... };
    briefSkip = true;   // indentato come se fosse dentro l'if, ma non lo è
  ```

  Il corpo dell'`if` senza graffe è la sola istruzione che lo segue, cioè l'assegnazione di `window.__sv`. La riga `briefSkip = true`, indentata come se fosse dentro, è un'istruzione a sé e **viene eseguita sempre**, anche senza `#collaudo` nell'indirizzo. Con `briefSkip` vero, `showBrief(..., first)` esegue `if (first && briefSkip) return hideBrief()` e chiude il riquadro nello stesso istante in cui lo apre. Corretto mettendo le graffe.
- **Non è un difetto della 0.17.** Nasce con la 0.15, la versione che ha introdotto il riquadro (commit `1bef876`): è lì che `briefSkip = true` è stato aggiunto fuori dall'`if`. Verificato aprendo nel browser `index.html` di `1bef876` (0.15), `53f5d55` (0.16) e `328e210` (0.17): in tutte e tre, entrando nella prima regata dal menu, `briefOv.hidden` resta `true`. Il commit 0.17 non tocca quelle righe (`git log -L2366,2370:index.html` lo conferma). Quindi il riquadro non si è mai visto nel gioco pubblicato, in nessuna delle tre versioni.
- **Perché i collaudi non se n'erano accorti.** `collaudo_pannello.py` collaudava il riquadro **dopo** aver scritto `__sv.skipBrief = false`, cioè dopo aver riportato a mano la variabile al valore che il gioco vero avrebbe dovuto già avere. Il collaudo verificava quindi il comportamento del riquadro *dato* che la variabile è falsa, e non il valore della variabile: l'unica cosa rotta era proprio quella, e per costruzione nessun collaudo poteva vederla, perché tutti caricano `index.html#collaudo` e `#collaudo` rende lecito il salto. I quattro `True` stampati erano veri e inutili.
- **Nuovo controllo.** `collaudo_pannello.py` apre una seconda pagina **senza `#collaudo`** e fa lo stesso giro su sei voci: la regata 1 e tutte e cinque le prove. Per ognuna entra dal menu, poi rifà il giro con «Ricomincia», e pretende che `briefOv` sia visibile, che il pulsante dica «Parti» e che `bRaceOpts` (Avversari e Preparazione) sia visibile in regata e nascosto nelle prove. Nelle prove controlla anche il cronometro: col riquadro aperto per **2,5 secondi** l'orologio del pannello deve restare a `0:00`, dopo «Parti» deve segnare `0:01` e dopo «Ricomincia» deve tornare a `0:00`. Il confronto è sulla riga intera, fascia d'oro compresa (`Tempo 0:00 · oro entro 1:30`), così una fascia che cambiasse di nascosto farebbe fallire il controllo.
- Verificato che il controllo **fallisce sulla versione rotta**: sei righe `riquadro dal menu False | con Ricomincia False` e, per le prove, `orologio fermo False | parte con Parti False | riparte da zero False`, con undici righe in `errori`. Sulla versione corretta tutte `True` e `errori: []`, a 1360×650 e 1360×768. Il riquadro si chiude con Invio e non con un clic su `#bGo`: sulla versione rotta il clic aspetterebbe invano un pulsante nascosto invece di stampare l'esito.
- **Fasce e record non ne risentono.** `S.time += dt` sta dentro `simulate` (`index.html:1358`), e `simulate` non viene chiamata quando `briefing` è vero (`index.html:2357`): il tempo prima di «Parti» non entra nel cronometro, quindi non entra né nel record (`Math.round(S.time)`) né nella fascia (`S.time <= bd[k]`). Lo stesso vale per `recSample`, che registra il fantasma. Confermato nel gioco vero: le cinque fasce d'oro stampate sono quelle della 0.16 (1:30, 2:20, 3:05, 5:30, 5:55) e l'orologio parte da zero dopo «Parti», non da 2,5 s.
- **Che altro dipende da `briefSkip` o da `showBrief`.** `briefSkip` è letto in un solo punto, `showBrief`, e scritto in due: la riga corretta e il setter `__sv.skipBrief`. `showBrief` è chiamato in quattro punti: avvio prova (`first` vero), avvio regata (`first` vero) e i due pulsanti «Istruzioni» (`first` falso, quindi mai salvati dal salto: funzionavano anche prima). `briefing` è letto nel gate di `tick` e nella gestione dei tasti, dove blocca i comandi finché il riquadro è aperto, ed è azzerato da `showCards`, che gira all'inizio di ogni `start*`. Verificato il caso che poteva incastrarsi: regata col riquadro aperto → Menu → lezione, e → Menu → navigazione libera; in entrambi il riquadro si chiude e la scena si anima, perché `showCards` azzera `briefing` prima di `showBrief`. Nessun altro collaudo è toccato: tutti caricano `index.html#collaudo` e solo `collaudo_pannello.py` scrive `skipBrief`.
- **Una ruvidezza rimasta, non corretta.** Cambiando Avversari o Preparazione dentro il riquadro la regata ricomincia e il riquadro si riapre, e `showBrief` sposta il fuoco su «Parti»: chi usa la tastiera deve tornare al menu a tendina per cambiare anche l'altro. Da tenere presente se si rimette mano al riquadro.
- **Regola che ne esce**, aggiunta in `COLLAUDI.md`: un collaudo che prima di misurare rimette a mano un'impostazione del gioco non collauda più quell'impostazione. Il valore di partenza va verificato in una pagina caricata come la carica un giocatore, senza `#collaudo`.

### In gran lasco e in poppa il pannello diceva di lascare una vela già tutta lascata

- **Difetto.** Con la scotta tutta lascata e il vento da dietro, il pannello diceva «Si agita il filetto sottovento: lasca, oppure orza.» (suggerimento sui filetti) oppure «La vela è in stallo: troppo cazzata.» (suggerimento semplice). Un consiglio sbagliato tre volte: non c'è più niente da lascare, «troppo cazzata» è falso, e «orza» porta via dall'andatura.
- **Causa: geometria del motore, non una taratura.** Il boma arriva al massimo a 85° (`BOAT.maxBoom`), l'incidenza è `apparente − boma` e i filetti vanno in stallo oltre 27° (`ttState`). Quindi **oltre 112° di vento apparente nessuna posizione della randa dà i filetti dritti**, e a scotta tutta lascata l'unico stato possibile è «lee». Banco sul motore (91 andature per 101 posizioni di scotta, equilibrio a prua fissa): ultimo vento **reale** con filetti dritti possibili **135° a 6 nodi, 134° a 10 e a 12, 133° a 15**; primo vento reale con «lee» a scotta tutta lascata **136° / 135° / 135° / 134°**. Il messaggio nuovo comincia quindi esattamente al confine fra lasco e gran lasco (135° nella tabella `ANDATURE`): non è un numero scelto.
- **Decisione:** una riga dopo la scelta fra `ttMsg` e `sailMsg`. Se i filetti dicono «lee» **e** `I.sheet > 0,99`, tutti e due i messaggi diventano «Vento da dietro: la vela è già tutta aperta. In poppa i filetti non servono.», in **verde**, perché la vela è regolata come va regolata e un'arancione fissa per tutto il lato portante sembrerebbe un errore. `flog` e `wind` non sono toccati: lì poggiare e cazzare restano consigli giusti (a scotta tutta lascata «wind» esce sotto 93° apparenti, «flog» sotto 30,5°, «lee» solo oltre 112°). La soglia 0,99 vuol dire «scotta esattamente al massimo»: il cursore dà 1,00 solo a 100, la freccia ↓ è limitata a 1 e `autoSheet` arriva a 1 esatto, quindi non esistono valori intermedi sopra 0,99.
- **Numeri nel gioco vero, senza `#collaudo`** (navigazione libera a 10 nodi con raffiche, scotta tutta lascata, guidando con la tastiera e leggendo solo il pannello): **287 letture** in gran lasco o poppa con il boma a 85°, di cui **256 col testo nuovo**, **31** coperte da «Raffica in arrivo: preparati a lascare.» e **0** col consiglio sbagliato di prima.
- **Numeri col banco:** a scotta 1,00, **10 andature su 10** in «lee» (da 135° a 180°) mostrano il testo nuovo, e le 7 andature in cui i filetti dicono «wind» o «ok» (da 100° a 130°) non lo mostrano; con la scotta a **0,90–0,99, 25 casi su 25** tengono il consiglio di prima, perché lì lascare serve ancora. Lo stesso vale per il suggerimento semplice, provato nel passo «Poppa» della lezione 3 (3 casi su 3).
- **Lezione 5, «Strambata controllata»: il testo chiedeva una cosa che a quell'andatura non si può fare.** Il passo chiede `twa > 115` **e** filetti dritti, senza limite in alto, ma dopo la strambata la barca si trova in gran lasco o in poppa, dove i filetti dritti non esistono: bisogna orzare fino al lasco, e il testo si fermava a «poi lasca e regola». Aggiunta la frase «**poi lasca e regola: i filetti tornano dritti quando orzi fino al lasco**». Misura su dieci tentativi per andatura: puntando il **lasco (125°)** il passo si completa **6 volte su 10**, e sono esattamente le 6 in cui la strambata del pilota è uscita controllata (le altre 4 sono uscite violente, ed è un difetto del banco, non del gioco); puntando il **gran lasco (150°)** **0 volte su 10**, pur con 2 strambate controllate su 10, e in tutti e dieci i tentativi il pannello mostra il testo nuovo. Nella fascia utile il passo si completa puntando 120°, 125°, 132° e 134° (4,5–7,2 s) e non si completa da 136° in su.
- **La fascia di «Poggi e laschi» (twa 105–140) non è stata cambiata.** Da 135° in su i filetti dritti non esistono, ma il passo si completa perché basta un punto della fascia e il testo dice «poggia fino al lasco»: misurato, completa puntando 110°, 120°, 130° e 134° (in 2,0–2,8 s) e non completa in 30 s puntando 140°. Stringere la fascia non cambierebbe nulla di misurabile.
- **Tutti i passi che usano `I.tt` restano completabili**, guidati davvero con un pilota automatico (barra proporzionale e scotta, come in `collaudo_giro_boa.py`): **10 passi su 10** completati in 0,8–2,2 s (lezione 1 «lascare», «cazzare», «troppo cazzata»; lezione 3 i tre dei filetti, «poggi e laschi», «orzi e cazzi»; lezione 4 «accelerando»; lezione 5 «prepararsi a virare»). **Cinque di questi passi non erano coperti da nessun collaudo** (`collaudo_lezioni.py` salta «Filetti dritti», «Poggi e laschi», «Orzi e cazzi», «Accelerando» e «Strambata controllata»). Nessun passo chiede filetti dritti oltre 140° di vento reale.
- **Pannello invariato.** Il testo nuovo (76 caratteri) occupa **54 px**, esattamente come i due che sostituisce, perché sta dentro l'altezza minima della riga del suggerimento; il testo più lungo che il gioco già mostra («Stai andando all'indietro…», 100 caratteri) arriva a 59–74 px. Caso peggiore misurato scrivendo i testi dentro il suggerimento in **31 punti** in cui è visibile: **0 pixel di eccesso** a 1360×650 e a 1360×768.
- **Non-regressione.** `polare.js` e `raffiche_e_virate.js` danno uscite **identiche carattere per carattere** a quelle della versione precedente (il motore non è toccato); `collaudo_lezioni.py` tutti `OK`, `collaudo_schermate.py` `errori: []`, `collaudo_pannello.py` «nessuno» e i sei `True` a 1360×650 e 1360×768; `git diff` vuoto su `sperimentale/`.
- **Collaudo nuovo, `collaudo_suggerimento.py`.** Fa i due sweep (scotta 1,00 e scotta 0,90–0,99) a passi fissi con `__sv.run`, prova anche il suggerimento semplice, misura il caso peggiore del pannello, **dichiara quanti casi ha misurato per ogni lato e si dichiara non valido se sono zero**. Verificato che **fallisce sulla versione di prima**: 13 casi sbagliati (10 col consiglio sui filetti, 3 col suggerimento semplice) e uscita 1; sulla versione nuova 0 casi sbagliati e uscita 0.
- **Difetto del banco, trovato e corretto durante la misura.** Il primo pilota lasciava la scotta appena la prua passava i 180°, mentre il boma passa un attimo dopo, perché conta il vento apparente: la strambata usciva **violenta**, `gybesC` non aumentava e alcune righe risultavano «non completato» per colpa del metro, non del gioco (125° e 130° nel primo sweep, 132° nella traccia che ne ha trovato la causa). Corretto tenendo la scotta cazzata finché `S.boomSide` non è cambiato davvero. Resta che il pilota sbaglia la strambata in modo irregolare da un tentativo all'altro, quindi il passo è stato misurato su **dieci tentativi per andatura**, non su uno.
- **Limite dichiarato.** I 112° apparenti (circa 135° reali) sono figli di una barca lenta: su un 470 le fonti danno circa **75° apparenti a 120° reali** (F4), contro i **97,5°** del nostro motore. Una barca più veloce tiene il vento apparente molto più avanti e i filetti lavorano più a poppa: il confine è nostro, non della vela. Annotato in `docs/DUBBI-E-RICERCHE.md` e in `docs/CONTENUTI-DA-VERIFICARE.md` (lezione 3), da far giudicare a un velista insieme all'affermazione «in poppa i filetti non servono».
- **Due messaggi del pannello restano da sistemare, e non in questo punto.** «Sbandi troppo: lasca la scotta» chiede l'impossibile quando la scotta è già al massimo, ed è lo stesso difetto appena corretto; vince sul messaggio nuovo perché viene dopo. «Raffica in arrivo: preparati a lascare» va reso condizionale: lascare non è sempre necessario, e chi vuole andare più veloce la raffica la cerca. Nelle 287 letture del gioco vero è il secondo che ha coperto il testo nuovo 31 volte.

### Punto 8: ambiente dei collaudi stabile

- **Problema.** Playwright non era installato in modo permanente per il python3 di sistema, e ogni macchina rischia di scaricare una versione non allineata al Chromium già in cache: `chromium-1223` corrisponde a `playwright==1.60.0` (la 1.58 vuole la 1208, la 1.63 la 1243).
- **Fatto.** Nuovo script `tests/prepara_ambiente.sh`, con `--dry-run`: crea un venv in `.venv-collaudi/` (aggiunta a `.gitignore`), ci installa `playwright==1.60.0`, controlla che `chromium-1223` sia già nella cache di Playwright e, se manca, stampa il comando per scaricarlo senza eseguirlo, poi apre `index.html` in headless e legge il titolo, stampando `OK` o l'errore. Non tocca `index.html` né `sperimentale/`, non usa `sudo`, non installa nulla fuori dal progetto.
- **Verificato con `--dry-run`:** stampa le quattro righe attese (`.gitignore`, venv, pip, cache) senza creare né installare nulla; `bash -n` sullo script non trova errori di sintassi.
- **Non eseguita l'installazione vera** in questa sessione: lo script è apposta per farla lanciare all'utente. Un tentativo di prova nell'ambiente di lavoro di Claude Code ha comunque mostrato che l'installazione vera funziona finché si raggiunge PyPI (bloccato lì dalla sandbox di rete di quell'ambiente, non dallo script).
- `docs/COLLAUDI.md` aggiornato: come si usa lo script, come si lancia ogni collaudo con il python del venv (`.venv-collaudi/bin/python tests/nome_collaudo.py`), perché 1.60.0, e cosa fare se il browser in cache cambia.
- Nuovo `tests/lancia_tutti.sh` (con `--veloce` e `--dry-run`): lancia tutti i collaudi e stampa una riga di esito ciascuno; dove lo script non dà un codice di uscita legato al risultato, segna «DA CONTROLLARE» invece di inventare un OK. Pensato per una verifica indipendente sul PC dell'utente, non per ogni modifica di Claude Code (vedi «Risparmio di crediti» in `CLAUDE.md`).
- `tests/lancia_tutti.sh` migliorato, dopo l'uso reale sul PC dell'utente: salva l'uscita completa di ogni collaudo in `tests/output/lancia_tutti/<data-ora>/<nome>.txt`; il rapporto finale mostra i FALLITI con le ultime 15 righe e i DA CONTROLLARE con le ultime 4 (i numeri da confrontare), non solo il nome; nuove opzioni `--solo TESTO` (rilancia solo i collaudi il cui nome contiene TESTO) e `--parallelo N` (fino a N insieme; i due `collaudo_regate.py` condividono `race_results.txt` e non girano mai insieme, anche con `--parallelo`); il codice di uscita torna 0 anche con collaudi «da controllare» o saltati, non solo quando tutto è OK.

### Punti 4-7: testi delle lezioni più precisi

- **Lezione 2, «Barra sottovento» e «Barra sopravento»: il testo citava gradi che il pannello, in quei due passi, non mostra** (la riga «Andatura» resta nascosta fino alla lezione 3, e non c'è la rosa grande). Sostituiti i gradi con un riferimento alla rosetta dell'angolo morto, sempre visibile lì: «fermati quando la lancetta è a metà strada tra il rosso e l'orizzontale» (orza) e «...scesa un terzo della strada tra l'orizzontale e il basso» (poggia). **Tarato con un pilota che segue il testo alla lettera, a piccoli colpi di barra** (non una spinta lunga: una pressione continua fino al bersaglio sbanda per inerzia molto oltre, fuori dalla finestra del passo — orza: atterra a twa 19-35° contro i 43-67° richiesti; poggia: 147-178° contro 110-145°). A piccoli colpi (120 ms, pausa 900 ms), fermandosi a metà strada orza atterra **58° (5 prove, 58,0-58,1°)**, un terzo di strada poggia atterra **122° (6 prove, 122,1-123,1°)**: entrambi comodamente dentro la finestra del `cond`, con margine. Il passo "Barra a piccoli colpi" non era ancora un consiglio esplicito del gioco: lo diventa qui e anticipa, senza nominarlo, quanto la lezione già dice da sola («timonare bene vuol dire usare poca barra», passo «Tenere la rotta»).
- **Lezione 3, «Bolina», «Traverso», «Lasco e gran lasco» e «Poppa»: aggiunto il bordo tratteggiato sul settore di arrivo** nella rosa delle andature (`drawRose`, nuovo parametro `target`), distinto dall'evidenziazione già esistente del settore dove si trova la prua adesso. Solo sul lato della mura corrente (stessa regola della prua attuale), tranne angolo morto e poppa che non hanno un lato. Testo dei quattro passi adattato per nominare il bordo tratteggiato.
- **`drawLabels`: anello vuoto al posto del pallino pieno**, che copriva l'oggetto indicato (filetti, timone, boma…). Un rigo: da `ctx.fill()` a `ctx.stroke()` su un cerchio di raggio 5. Controllato a occhio su "Come si timona" (barra, timone), "Le mure" e "I filetti": l'oggetto resta visibile dentro l'anello.
- **Lezione 5, «Una virata che non riesce»: spiegato «lascia che la prua scada»** (gira da sola, lentamente, allontanandosi dal vento) e allineato alla stessa formula già usata dal suggerimento dal vivo («...lascia scadere la prua», `collaudo_suggerimento.py`, non toccato). Nuova voce di glossario «Scadere». Il comportamento era già dichiarato come semplificazione in `FISICA-E-TARATURE.md`, ma non è una frase di un velista: una riga aggiunta sia in `CONTENUTI-DA-VERIFICARE.md` sia in `DUBBI-E-RICERCHE.md`.
- **Collaudi:** `collaudo_lezioni.py` tutte OK (invariato); `collaudo_schermate.py` `errori: []`; `collaudo_pannello.py` nessuna eccedenza a 1360×650 e 1360×768; `collaudo_suggerimento.py` 0 casi sbagliati (la riga del suggerimento non è cambiata). `git diff` vuoto su `polare.js`, `raffiche_e_virate.js` e `sperimentale/`. Vista anche una pagina senza `#collaudo`: lezione 2 (click e tasti veri, nessun errore JS), lezione 3 «Bolina» (settore tratteggiato visibile), glossario (voce «Scadere» trovabile cercando).

## 0.16 — Menu a riquadri, fasce di tempo, lezione 1 con il timone, rosa e freccia della velocità
- **Decisioni (fase A, 29 settembre):** menu principale a riquadri, tutto visibile senza scorrere; fasce di tempo oro, argento e bronzo per le prove; lezione 1 con le frecce del timone al posto dei pulsanti Orza e Poggia; rosa dell'angolo morto; freccia della velocità; pannello ridotto fuori dalle lezioni. Carteggio e mare aperto escono dal menu: diventeranno un'espansione o un gioco a parte. Nei titoli del gioco si dice «brevetto», non «patente».
- **Menu a riquadri.** Tre colonne: Scuola (le 11 voci in ordine, una riga ciascuna, descrizione al passaggio del mouse); Regate e Navigazione libera; Ripasso ed esame (i sei quiz e, in grigio, «Esame su tutte le lezioni», in arrivo) e In arrivo (una riga: esame, tornei, altri tipi di barca). A 1360×650 sta tutto nella finestra, con circa 60 pixel di margine. I nomi interni dei pulsanti non cambiano, quindi i collaudi li trovano ancora.
- **Fasce di tempo delle prove** (campo `bands` di `MISSIONS`, in secondi): oro uguale al tempo di un pilota automatico, argento +25%, bronzo +60%, arrotondati ai 5 s superiori. Prova 1: 1:30, 1:50, 2:20. Prova 2: 2:20, 2:55, 3:40. Prova 3: 3:05, 3:55, 5:00. Prova 4: 5:30, 6:50, 8:45. Prova 5: 5:55, 7:20, 9:25. Si vedono nel menu (pallino accanto al record), nel riquadro delle istruzioni, nel pannello («oro entro 1:30», poi argento, poi bronzo) e all'arrivo (fascia del tentativo appena fatto). Nessun salvataggio nuovo: la fascia del menu si ricava dal record. Valgono anche con gli aiuti accesi. Il vento delle prove ha già forza fissa; cambiarne la direzione ruota il percorso e non cambia i tempi (verificato: 8 venti, 8 tempi identici). Da ritoccare dopo averci giocato: nella prova 1 il pilota regola la vela all'istante e l'oro potrebbe essere troppo stretto.
- **Taratura.** Pilota automatico dei collaudi con due correzioni: in poppa cazza solo quando sta per strambare (prima teneva la vela mezza cazzata per tutta la poppa) e in poppa piena tiene le mure invece di strambare per sbaglio. Tempi: 87, 136, 185, 327 s; prova 5 tra 342 e 353 s, mediana 351 (nelle raffiche il pilota si pianta spesso: 7 tentativi su 24 non finiti, esclusi).
- **Difetto di metodo trovato durante la taratura:** i primi tempi, presi con il tempo accelerato e cinque browser aperti insieme su un solo processore, erano falsati (108 s invece di 87 nella prova 1): il pilota reagiva più di rado del previsto. Nuovo comando dell'aggancio `#collaudo`, `__sv.run(dt, n)`, che fa avanzare la simulazione a passi fissi: i tempi non dipendono più dal computer.
- **Lezione 1 con il timone.** Via i pulsanti Orza e Poggia e i tasti A e D. Nei passi «Poggiare», «Orzare e l'angolo morto» e «Ripartire» si usano le frecce ← →, che funzionano come nel resto del gioco (barra, oppure «girano la prua» se scelto nelle impostazioni). Il testo dice quale freccia premere, calcolata all'apertura del passo secondo il lato da cui arriva il vento e l'impostazione delle frecce; con la barra aggiunge che la barra va dall'altra parte e che il perché si vede nella lezione 2. Mentre la prua gira, la riga di stato dice «Stai orzando» o «Stai poggiando». Nel passo «Poggiare» c'è l'avviso sulla strambata. Cazza e Lasca restano pulsanti e rispondono anche a ↑ ↓ oltre che a W e S.
- **Due difetti trovati collaudando la lezione 1:** rilasciata la freccia, la barra tornava al centro lentamente e la prua continuava a girare; nel passo «lascare» la barca arrivava a 118° dal vento, dove la vela tutta aperta non sbatte, e il passo non si completava. Correzioni: nella lezione 1 la barra torna al centro in fretta, come con i vecchi pulsanti; «Ripartire» chiede il vento tra 70° e 105° per un secondo; nei passi della scotta la barra resta disponibile per correggere la rotta.
- **Comportamento voluto da tenere d'occhio:** tenendo premuta la freccia troppo a lungo nel passo «Poggiare», la barca stramba a vela aperta e il registro la conta. Con i vecchi pulsanti non si poteva strambare.
- **Rosa dell'angolo morto**, a destra dell'indicatore di sbandamento (al suo posto dove lo sbandamento non c'è): vento sempre dall'alto, settore rosso di 40° per lato (la stessa costante del registro, `IRONS_A`, e lo stesso limite della voce «Andatura»), lancetta della prua che diventa rossa nel settore. Compare in prove, regate, navigazione libera e nei passi pratici delle lezioni, non nelle pause né dove c'è già la rosa grande delle andature. Impostazione «Rosa dell'angolo morto», accesa di norma. Usa il vento locale: nelle raffiche la lancetta oscilla un poco.
- **Freccia della velocità**, verde chiaro: dal centro della barca nella direzione del moto vero (avanti più scarroccio; all'indietro esce dalla poppa), più lunga con la velocità (la parte che sporge dallo scafo è proporzionale), nascosta sotto 0,3 nodi, da scuffiati e nelle pause. La scritta «velocità» sta dal lato opposto al vento. Si accende e spegne con le frecce del vento.
- **Pannello ridotto** in prove, regate e navigazione libera: Velocità, Andatura, Prua, Rilevamento boa. Vento reale, vento apparente, sbandamento e scarroccio ora si vedono sullo schermo (rosa, frecce, indicatore) e tornano con l'impostazione «Tutti gli strumenti nel pannello», spenta di norma. Le lezioni non cambiano.
- **Nuovo collaudo:** `collaudo_fasce.py` (taratura delle fasce, a passi fissi). Aggiornati `collaudo_lezioni.py` e `collaudo_registro.py` alle frecce nella lezione 1; in «Ripartire» il pilota ora rilascia la freccia come un giocatore.
- **Collaudi:** registro 13 verifiche su 13 (in quattro gruppi: qui ogni comando ha un limite di 5 minuti); lezioni tutte completate in tre passate; pannello senza eccedenze a 1360×650 e 1280×800; schermate, quiz, rotta, strambata (6 nodi nessuna scuffia, 15 nodi sempre), fantasma, giro di boa (casi a, b, f) e 6 regate senza differenze. Partenze non rilanciate: avversari e fisica non sono cambiati.
- **Difetto noto, non corretto:** con la prua nel vento le scritte «reale» e «apparente» delle frecce del vento si sovrappongono.

## 0.15 — Registro degli errori e pannello ordinato
- **Decisioni (fase A):** registro degli errori in lezioni, prove e regate; nelle lezioni non conta l'errore che il passo chiede apposta. Contatore sempre visibile durante il gioco. Segno ★ nel menu per le prove e le regate completate almeno una volta senza errori. Pannello leggibile tutto senza scorrere su uno schermo 1360×768, anche senza schermo intero.
- **Registro degli errori.** Voci e definizioni:
  - scuffia;
  - strambata a vela aperta (boma oltre 45°, la soglia del colpo del boma). Il gioco non può sapere se una strambata era voluta, quindi non la chiama «involontaria»;
  - piantato nell'angolo morto: prua a meno di 40° dal vento e velocità sotto 1 nodo per almeno 3 secondi di fila; si contano gli episodi e i secondi. Non conta prima della partenza delle regate né da scuffiati. Taratura: una virata partita a 3,1 nodi resta 1,9 s sotto 1 nodo e non conta; una partita a 2,3 nodi ne resta 4,2 e conta. Il pilota automatico dei collaudi, in 27 virate nelle prove 3, 4 e 5, non ne ha contata nessuna;
  - boa girata dal lato sbagliato (ogni attraversamento della semiretta nel verso sbagliato);
  - contatto (solo regate), separando quelli con penalità;
  - partenza anticipata e linea tagliata fuori dagli estremi (solo regate).
- Il registro si chiude all'arrivo e riparte a ogni nuovo tentativo. I record restano tempi: il registro non li modifica.
- **Lezioni:** campo `allow` nei passi che chiedono l'errore (lezione 1 «Orzare e l'angolo morto», lezione 5 «Una virata che non riesce» e «Strambata violenta», lezione 6 «La scuffia»). Un episodio di barca piantata iniziato in un passo che lo chiede non conta nemmeno se prosegue nel passo dopo.
- **Pannello riordinato** in prove, regate e navigazione libera: strumenti su tre colonne, suggerimento, barra e scotta, poi stato (tempo e record nelle prove, che prima non si vedevano; classifica nelle regate; errori), poi i comandi. Nelle lezioni l'ordine resta quello di prima, con spazi più compatti; dalla lezione 3 in poi spariscono le scritte agli estremi dei cursori.
- **Istruzioni di prove e regate** in un riquadro sul mare, a gioco fermo. Il cronometro della prova e il conto alla rovescia della regata partono con «Parti» o Invio; prima il conto alla rovescia scorreva mentre si leggeva. Il pulsante «Istruzioni» le riapre, sempre a gioco fermo. Avversari e Preparazione si scelgono nel riquadro.
- **Impostazioni** in una finestra aperta dal pulsante ⚙; mentre è aperta il gioco è fermo, come con il glossario.
- Legenda dei tasti su una riga: «R raddrizza» resta sul pulsante e nel messaggio di scuffia. «Ricomincia il passo» diventa «Ricomincia».
- **Misure** (con i caratteri veri del gioco): a 1360×650, cioè 1360×768 meno le barre del browser, il pannello sta tutto nella finestra in ogni passo di lezione, prova e regata. Nei riepiloghi finali delle lezioni il margine è zero: con F11 (schermo intero) ci sono circa 118 pixel in più.
- **Nuovi collaudi:** `collaudo_registro.py` (provoca ogni errore guidando la barca: 13 verifiche) e `collaudo_pannello.py` (altezza del pannello e riquadro delle istruzioni). Nei collaudi automatici il riquadro delle istruzioni è saltato; `collaudo_partenze.py` e `collaudo_fantasma.py` impostano Avversari e Preparazione direttamente, perché ora stanno nel riquadro.
- **Collaudi:** registro 13 verifiche su 13 (due volte); 10 regate su 10 concluse con tutti gli avversari; partenze confrontate con la 0.14.1 nello stesso momento su 36 partenze ciascuna: ritardo medio 8,2 s contro 8,3, due ritardi oltre un minuto in entrambe (difetto noto), nessuna partenza anticipata; lezioni, schermate, quiz, rotta, strambata, fantasma e giro di boa invariati.
- **Lacuna trovata durante il lavoro:** nelle prove il tempo non era mostrato da nessuna parte mentre si navigava, solo all'arrivo.

## 0.14.1 — Prova 5 con tre andature
- **Decisione:** nella prova 5 la boa 2 è spostata a sinistra della boa 1, alla stessa altezza. Il percorso diventa bolina, traverso (90° dal vento), gran lasco (circa 146°): tre andature diverse, come prometteva il testo originale. Lunghezza da circa 590 a 636 m.
- Testo della prova aggiornato; record e fantasma della prova 5 ripartono da zero (chiave `m4.3`).
- Collaudi: triangolo con le boe a sinistra completato; con la boa 2 a dritta non si completa e compare il messaggio del lato sbagliato.

## 0.14 — Giro di boa, andatura nascosta, barra ferma in gara
- **Decisioni (fase A):** andatura nascosta nel pannello delle lezioni 1 e 2; boe da lasciare a sinistra in prove e regate; barra che non torna al centro in prove e regate, riattivabile.
- **Andatura nel pannello:** nascosta nelle lezioni 1 e 2, perché le andature si spiegano nella lezione 3.
- **Barra:** l'impostazione «La barra torna al centro da sola» vale ora per la modalità in corso. Lezioni e navigazione libera: attiva, come prima. Prove e regate: spenta, perché un regatante tiene la barra ferma; la barra spaziatrice la riporta al centro. Si può riattivare.
- **Giro di boa:** prima una boa contava appena ci si passava entro 12 m (prove) o 15 m (regate), senza girarla davvero. Ora le boe intermedie vanno girate lasciandole a sinistra: conta l'attraversamento, in senso antiorario, della semiretta che parte dalla boa verso l'esterno della curva del percorso. Chi la gira dal lato sbagliato deve tornare indietro e rifare il giro, come nella regola del filo teso; il gioco lo segnala. Una freccia curva mostra il verso di giro. La boa di arrivo delle prove e l'unica boa delle prove 1–3 restano punti da raggiungere.
- **Prova 5:** il triangolo girava in senso orario (boe a dritta); ora è specchiato. **Difetto di contenuto trovato:** il testo diceva «traverso» per il secondo lato, che in realtà era un lasco a circa 126° dal vento. Testo corretto.
- **Record e fantasmi** delle prove 4 e 5 e delle regate ripartono da zero (chiavi nuove): con il giro vero i tempi non sono confrontabili. Le voci completate restano completate.
- **Avversari:** girano la boa passando per tre punti (sotto a destra, oltre a sinistra; un terzo punto solo per riprovare dopo un giro mancato), con un giro leggermente diverso per ciascuno.
- **Difetti trovati nei collaudi e corretti:**
  - avversari che passavano sopra la boa senza girarla: il cambio di rotta scattava ancora sotto la boa, da dove la bolina li portava dritti sulla boa;
  - avversari che tentavano di virare dal traverso al traverso opposto, perdevano l'abbrivio a metà e ricominciavano all'infinito. Ora prima orzano fino alla bolina, poi virano, poi poggiano;
  - barca ferma tra 40° e 44° dal vento che non ripartiva mai, perché la regola «piantata: poggia» scattava solo sotto 40°. Ora 44°, tranne in partenza, dove 44° faceva poggiare troppo presto vicino alla linea (resta 40°, salvo chi torna dietro la linea dopo una partenza anticipata).
- **Tempi degli avversari** (regata a bastone): bolina da 124 a 150 s, poppa da 84 a 93 s. Circa 12 s dipendono dalla vecchia scorciatoia del cerchio di 15 m, il resto dal giro vero. Le fasce di tempo della fase A vanno tarate sui tempi nuovi.
- **Nuovo collaudo** `collaudo_giro_boa.py`: un pilota automatico guida la barca con barra e scotta e verifica il giro dal lato giusto, dal lato sbagliato, sbagliato e poi corretto, il triangolo, e le prove 1–3 invariate. Aggancio `#collaudo` esteso con barra, scotta e boe.
- **Collaudi:** 19 regate su 19 concluse con tutti gli avversari (prima delle correzioni circa una su dieci si bloccava); contatti tra avversari non aumentati (22 in 12 regate contro 44 della 0.13); ritardi al via uguali alla 0.13 su 36 partenze; lezioni, strambata, quiz, rotta, schermate e fantasma invariati.

## 0.13 — Angolo morto realistico
- **Decisione:** angolo morto allineato alle dispense di vela (45° per lato come convenzione didattica, circa 35° per le derive). Prima la barca avanzava fino a 25–30° dal vento, più di qualsiasi fonte.
- Fisica: la vela si sgonfia quando il vento apparente è troppo stretto (`luffA0` 27°, `luffW` 7°), angolo minimo del boma 14°. Ora la barca è ferma sotto circa 33° dal vento, arranca fino a 40° e risale meglio a 45–48°.
- Timone leggermente più efficace (`turnLen` 1,05 m): con l'angolo morto più largo la virata lanciata durava 6 secondi; ora circa 4, come una deriva vera.
- Cerchio delle andature: angolo morto fino a 40°. Aggiornate le condizioni delle lezioni 1, 2, 3 e 5, i testi (bolina «tra 45° e 75°»), il glossario (angolo morto, bolina) e gli angoli di bolina degli avversari.
- Collaudi: tutte le lezioni completabili; 6 regate su 6 concluse; strambata invariata. Resta il difetto noto delle partenze degli avversari (vedi ROADMAP, fase B).

## 0.12 — Revisione generale
- Lezione 2, «Tenere la rotta»: onde che spostano la prua e barca orziera. Prima l'esercizio si completava senza fare nulla.
- Lezione 4: vento apparente indicato «tra 60° e 70°», coerente con il pannello.
- Lezione 6: testo del raddrizzamento coerente con la simulazione.
- Lezioni 1–3: solo la freccia del vento reale (il vento apparente si spiega nella lezione 4).
- Scotta più lenta di circa un quarto: la finestra di «vela regolata» era sotto il secondo di pressione.
- Più spazio tra i comandi di barra e scotta.

## 0.11 — Strambata corretta
- **Difetto:** qualsiasi strambata con la vela aperta faceva scuffiare, anche con 6 nodi. **Causa:** il colpo del boma era sommato in gradi/s a una velocità di sbandamento espressa in radianti/s, quindi era 57 volte più forte. **Correzione:** unità corrette e colpo proporzionale al vento (19° di sbandamento con 6 nodi, 39–58° con 10, scuffia con 15).
- «Vela a metà» spiegato: boma a una quarantina di gradi dal centro barca.
- Lezione 3: spiegato cosa succede superando i 180° in poppa.
- Messaggio specifico quando si scuffia per una strambata.

## 0.10 — Partenze e aiuti al timone
- Preparazione della regata a scelta: 1, 3 (predefinita) o 5 minuti; segnali adattati.
- Distanza e tempo alla linea durante l'attesa.
- Regata in solitaria contro il proprio fantasma.
- Freccia sulla prua che mostra da che parte gira la barca, e scritta «Barra a … → la prua gira a …».
- **Difetto:** gli avversari partivano con 5–70 secondi di ritardo. **Cause:** attendevano sottovento alla linea e dovevano risalire controvento; poi, attendendo vicino alla linea, tentavano virate da fermi e si piantavano. **Correzione:** attesa di fianco e sottovento, arrivo di bolina larga senza virare; regola «mai virare da fermi», valida solo prima di iniziare la virata.
- **Difetto introdotto e corretto:** la regola «mai virare da fermi», applicata anche a metà virata, faceva girare gli avversari attorno alla boa senza fine.

## 0.9 — Fantasma e regate
- Fantasma del record nelle prove e nelle regate, registrato rispetto al vento.
- Regata a bastone e regata nelle raffiche contro tre avversari, con partenza, partenza anticipata, precedenze e penalità, classifica.
- **Difetti trovati nei collaudi:** avversari che si scontravano di continuo (fino a 17 contatti a regata); avversari piantati nell'angolo morto durante le manovre per evitarsi; avversari che viravano avanti e indietro vicino alla boa; linea superata fuori dagli estremi senza conseguenze. Tutti corretti.

## 0.8 — Ripasso e verifica
- 29 domande di ripasso sulle sei lezioni.
- Scheda dei contenuti da verificare.

## 0.7 — Scuola sul nuovo motore
- Sei lezioni ricostruite sul simulatore: la barca e il vento, il timone, andature e filetti, vento reale e apparente, virata e strambata, raffiche e scuffia.
- Cinque prove con vento da direzioni diverse; navigazione libera; glossario ampliato.
- **Difetti trovati nei collaudi:** nella lezione 1, tenendo premuto Orza la barca virava, strambava e scuffiava; la scuffia «volontaria» della lezione 6 poteva richiedere più di un minuto. Corretti.

## 0.6 — Nuovo motore (campo prova)
- Vento apparente, portanza e resistenza della vela, filetti, barra reale, scarroccio.
- Sbandamento con timoniere che si sporge, raffiche visibili, scuffia e raddrizzamento.
- **Difetti:** raffiche invisibili (più grandi dell'area inquadrata); pannello che «saltava» cambiando altezza sotto i cursori; gioco bloccato dopo una scuffia su schermi piccoli. Corretti.

## 0.5 — Menu e glossario
- Menu con progressi salvati, glossario, vento da direzioni diverse nelle prove.

## 0.4 — Virata e strambata
- Lezione sulle due manovre; virata che fallisce senza abbrivio.

## 0.3 — Le andature
- Cerchio delle andature attorno alla barca.

## 0.2 — Lezione guidata
- Prima lezione passo passo, dopo che il primo prototipo si era rivelato incomprensibile per chi parte da zero.

## 0.1 — Primo prototipo
- Vista dall'alto, una vela, comandi Orza, Poggia, Cazza, Lasca, quattro prove.
