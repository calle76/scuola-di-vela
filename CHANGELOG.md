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

