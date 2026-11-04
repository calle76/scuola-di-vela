# Proposta: finire i suoni (seconda fetta)

4 novembre 2026. Segue `PROPOSTA-SUONI.md` (§4, seconda fetta) e `PROPOSTA-SUONI-REGISTRATI.md`. Ale, 3 novembre: «devi finire anche i suoni»; 4 novembre: «procedi pure completando i suoni nel gioco, non chiedere autorizzazioni». **Fermata 1 e fermata 2 di seguito, per sua scelta:** questo documento e le sue soglie sono scritti e committati prima di toccare il gioco.

## 1. Cosa manca

Sono registrate solo la vela e l'acqua sotto la prua. Restano da fare: il vento, che è ancora rumore sintetico (lo stesso difetto che Ale ha sentito nel mare), e tutta la seconda fetta: gabbiani, sartiame, sciabordio di fondo, scricchiolio, gorgoglio della pala. Manca anche un collaudo che **ascolti davvero** l'uscita del gioco: finora i collaudi leggono solo i comandi dati, e la 1.2.7 ha mostrato che un suono può partire senza sentirsi.

**Non cambiano:** manovre, tromba, arrivi, contatti, boe, suoni di passo e di prova. Il fruscio del boma spinto (Z) resta sintetico.

## 2. Le registrazioni

Tutte da Freesound, tutte **CC0** (licenza letta sulla pagina di ciascuna, il 4 novembre 2026). Letti 28 candidati: durata, livello, gravi e acuti, sbalzi, spettrogramma. **Non posso ascoltarli:** il giudizio finale è di Ale.

| Uso | Freesound | Cosa dice la pagina | Perché |
|---|---|---|---|
| Vento | [659004](https://freesound.org/people/Tom_Kaszuba/sounds/659004/), Tom_Kaszuba | Vento sulla riva dell'oceano | Il più regolare (sbalzi di 0,6 dB da un secondo all'altro), nessun colpo |
| Sartiame | [463373](https://freesound.org/people/dangale/sounds/463373/), dangale | Vento che fischia nelle sartie delle barche di un porto, prima di una tempesta | Il fischio è una riga netta nello spettrogramma; il rombo sotto si toglie col filtro |
| Sciabordio | [637206](https://freesound.org/people/kyles/sounds/637206/), kyles | Acqua che batte su uno scafo di vetroresina, con qualche colpetto dello scafo | L'unico registrato proprio sullo scafo di una barca |
| Gabbiani | [510917](https://freesound.org/people/Lydmakeren/sounds/510917/), Lydmakeren; [496203](https://freesound.org/people/poodaddy69/sounds/496203/), poodaddy69 | «Gabbiani», senza altri dettagli | Versi distinti e ritagliabili; il fondo si toglie col filtro |
| Scricchiolio | [145721](https://freesound.org/people/Rmutt/sounds/145721/), Rmutt | Cima d'ormeggio di un traghetto che lavora sulla bitta | Corda sotto carico: gli scricchiolii sono a gruppi, separati |
| Gorgoglio | [574866](https://freesound.org/people/TRP/sounds/574866/), TRP | Acqua che gorgoglia sotto una piccola barca in moto | La descrizione più vicina a quello che serve |

**Scartati, con il motivo:** 263786 (ritagliato da «un suono scaricato da Internet»: la catena della licenza non è chiara); 738675 (città e aereo nel fondo); 538204 (ticchettii regolari di drizza sopra il vento); 234361 (contiene una voce); 113361 e 113362 (un rimorchio per cavalli, quasi solo gravi); 213566 (riga fissa che non sembra acqua in moto); 706471 (vento tra i cespugli); 317397 (risacca evidente).

**Semplificazioni da dichiarare:** nessuna registrazione è fatta su una deriva. Il fischio del sartiame viene da barche ormeggiate in un porto, lo scricchiolio da una cima di traghetto, il vento da una riva. Le «onde lontane» della vecchia proposta non si fanno: lo sciabordio basta, e un suono in meno è un rischio in meno.

## 3. Come suonano nel gioco

Tutte le curve e i numeri sono **ipotesi nostre, a orecchio**, senza fonti. Il caso viene sempre da `sRand`, non da `Math.random`.

| Suono | Quando | Volume e altri comandi |
|---|---|---|
| **Vento** | sempre (giro di 20 s) | volume come oggi (0,03 + 0,42 × min(1,5; aws/10)^1,5, aws in m/s); filtro passa-basso 1.000 + 350 × aws Hz; velocità del giro 0,9 + 0,2 × min(1, aws/10) |
| **Sciabordio** | sempre (giro di 20 s) | 0,10 + 0,08 × min(1, vento reale/8 m/s); a barca scuffiata resta |
| **Sartiame** | vento apparente sopra 12 nodi (giro di 12 s) | 0,22 × min(1, (nodi − 12)/10); velocità del giro 0,9 + 0,2 × lo stesso rapporto |
| **Scricchiolio** | sbandamento oltre 18°, non scuffiata | uno ogni 2,5-6 s a caso; volume 0,40 + 0,40 × min(1, (sbandamento − 18)/15) (scritto prima: 0,25 + 0,25); altezza ±8% |
| **Gorgoglio** | pala in stallo (`S.stall`, lo stesso stato del messaggio nel pannello) | 0,80 × min(1, velocità/3 m/s) (scritto prima: 0,35), giro di 10 s |
| **Gabbiani** | sempre, mai in pausa, nel menu o nella moviola | uno ogni 25-70 s a caso; volume 0,30-0,60 (scritto prima: 0,15-0,35); posizione a caso fra sinistra e destra (stereo); altezza ±6% |

**Decisione diversa dalla vecchia proposta:** i gabbiani non sono più frequenti vicino a boe e giuria. È più semplice, e così il suono non dice dov'è la boa: un velista non si orienta coi gabbiani.

**Nuove informazioni per il giocatore, da dichiarare:** il gorgoglio dice che la pala è in stallo, ma il pannello lo dice già. Sartiame e scricchiolio dicono solo vento e sbandamento, che si leggono già. Nessun suono anticipa la raffica: seguono il vento **sulla barca**, come il vento di oggi.

**File:** gli stessi `js/suoni-dati.js` (un solo file, rifatto da `tests/prepara_suoni.py`) e `js/suoni.js`. Bitrate 32 kbit/s per i suoni continui, 48 per i gabbiani. L'acqua e i colpi di vela devono restare **identici al byte** a quelli di oggi.

**Decodifica a due tempi:** prima acqua e colpi, come oggi; finiti quelli, tutto il resto. Così il tempo della prima decodifica non peggiora. Se la seconda fallisce: il vento resta sintetico e gli altri suoni nuovi tacciono, senza errori.

## 4. Criteri (soglie scritte prima, attese nostre)

Sono **G1-G6**. In `tests/collaudo_suoni.py`, con la barca vera, Chromium e Firefox:

- **G1, la simulazione non cambia:** S1 verde; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.
- **G2, i suoni seguono i numeri** (registro interno, 10 finestre a semi diversi dove c'è il caso):
  - vento, sciabordio, sartiame e gorgoglio: ogni lettura uguale alla formula del §3, almeno 1.000 letture;
  - sartiame: 0 in tutte le letture sotto i 12 nodi apparenti, sopra 0 in almeno 100 letture;
  - gorgoglio: la barca guidata deve andare **davvero** in stallo (almeno 30 letture con `S.stall`), e il volume è 0 in tutte quelle senza stallo;
  - scricchiolii: in 60 s a 25° di sbandamento, in ciascuna delle 10 finestre, entro il 25% degli attesi (60/4,25 = 14,1); 0 a 10°;
  - gabbiani: in 40 minuti entro il 20% degli attesi (2.400/47,5 = 50,5), in ciascuna delle 10 finestre; 0 in pausa e nel menu;
  - controprova: scuffiata, 0 scricchiolii e gorgoglio 0.
- **G3, funziona dovunque:** nelle pagine con e senza `#collaudo`, tutto decodificato e nessun errore. Con la **seconda** decodifica rotta apposta: acqua e colpi registrati, vento sintetico, nessun errore. S1-S6 e R2-R4 restano verdi.
- **G4, costo:**
  - lettura dei suoni al più +10% di un fotogramma (come S4);
  - prima decodifica al più 300 ms (come R4), seconda al più 1.500 ms;
  - **`js/suoni-dati.js` al più 700 KB.** Cambia la soglia di R4 (300 KB), e lo dico: quella era per due suoni, qui i suoni sono otto. Il limite è fissato sulla stima, prima di costruire il file.
- **G5, l'acqua e i colpi non cambiano:** i due testi base64 identici a quelli della 1.2.8.

In un collaudo nuovo, `tests/collaudo_suoni_si_sentono.py`, **solo Chromium** (in Firefox senza schermo l'audio resta sospeso), il suono vero del gioco registrato al volume «bassi» in tempo reale, ogni misura **3 volte**, con la barca guidata:

- **G6, si sente davvero:**
  - gabbiano: al traverso a 10 nodi, un verso alza la banda 1,5-5 kHz di almeno **6 dB** sul tratto prima;
  - scricchiolio: a 25° di sbandamento, un gruppo alza la banda 1-5 kHz di almeno **4 dB** sul tratto prima;
  - sartiame a 20 nodi, sciabordio a barca ferma con 4 nodi, gorgoglio in stallo: col suono acceso rispetto a spento, nella loro banda, almeno **+2 dB**;
  - colpi di vela con la prua al vento: spicco sopra i 1.000 Hz almeno **9,1 dB** a 10 nodi e **3,7 dB** a 15, cioè i valori attesi della 1.2.8 meno il margine di 1,5 dB: il vento nuovo non deve coprirli;
  - **il volume generale non cambia di nascosto:** stessa scena, 10 nodi al traverso, livello complessivo entro **±3 dB** dalla 1.2.8;
  - **non satura:** a volume «alto», caso peggiore (20 nodi con la prua al vento e un gabbiano), picco al più **−0,5 dB**.
  - **Controprova del metro:** a suoni «spenti» la registrazione deve risultare silenziosa (sotto −70 dB), e il collaudo fallisce se l'audio non è acceso, invece di passare a vuoto.

**R5, licenze:** i sette file in `FONTI-PUBBLICHE.md` (F44-F50) con autore, pagina, licenza, giorno e cosa è stato tagliato. Nessun file CC BY-NC.

**Ascolto:** che piacciano lo giudica Ale. Le registrazioni del gioco vanno nella pagina d'ascolto, che non entra nel repository.

## 5. Rischi

- **Troppi suoni insieme:** l'ambiente può diventare un brusio. Se succede, si toglie o si abbassa.
- **Il peso:** da 206 KB a circa 640 KB, cioè circa 430 KB in più da scaricare, una volta sola.
- **Il fischio del sartiame viene da una tempesta in porto:** potrebbe suonare drammatico per una deriva. Per questo parte solo sopra i 12 nodi, ed è basso.
- **Collaudo in tempo reale:** dipende dal computer e dura minuti. Per questo le soglie di G6 sono larghe. Se sul computer di GitHub l'audio non parte, il collaudo fallisce e lo dice: si vedrà al primo giro.

## 6. Avanzamento

- **4 novembre 2026:** proposta scritta prima del codice.
- **Soglia cambiata prima di misurare la versione nuova, lo dico.** Lo script con cui ieri erano usciti 10,6 e 5,2 dB non è stato conservato. Il metro riscritto (livello ogni 50 ms sopra 1 kHz, 95° percentile meno mediana) sulla **1.2.8** dà 7,1 dB a 10 nodi e 4,4 a 15 (3 giri ciascuno, da 6,9 a 7,4 e da 4,3 a 4,6). Con le soglie 9,1 e 3,7 la 1.2.8 stessa fallirebbe a 10 nodi. Stessa regola di prima, «la 1.2.8 meno 1,5 dB», ma con lo stesso metro: **5,6 dB a 10 nodi e 2,9 a 15**. Riferimento del volume al traverso a 10 nodi: −40,7 dB (3 giri, da −41,0 a −40,5).
- **Primo giro di G6, sui volumi scritti al §3 (uno solo, 3 volte per suono, 6 per i gabbiani). Falliti:** gabbiani [10,3; 7,5; 8,0; 6,3; 2,1; 3,7] dB contro 6; scricchiolii [3,2; 6,8; 9,1] contro 4; gorgoglio [1,2; 0,8; 3,0] contro +2; a «alto» picco [−0,4; −1,3; −0,6] contro −0,5. **Le soglie non cambiano, cambiano i volumi** (al §3, con i valori di prima). Il livello «alto» scende da 0,8 a 0,6, per fare posto ai suoni nuovi: non era previsto nella proposta.
- **1.2.9:** dopo la correzione dei volumi, G1-G6 verdi: `collaudo_suoni.py` in Chromium e Firefox, `collaudo_suoni_si_sentono.py` due giri in Chromium. Numeri nel `CHANGELOG.md`. Resta il giudizio di Ale all'ascolto: le registrazioni del gioco sono in cima a `sperimentale/suoni-registrati/ascolto.html`.
- **Primo giro su GitHub (zip del 4 novembre, solo i collaudi dei suoni):** `collaudo_suoni.py` verde in Chromium e Firefox. `collaudo_suoni_si_sentono.py` fallito in Chromium per `ffmpeg` mancante, dopo aver confermato audio acceso e controprova a −140 dB: le misure di G6 su GitHub restano da fare. Aggiunto `ffmpeg` a `collaudi.yml`.
- **Ale, 4 novembre, dopo aver giocato:** non lo convincono il suono del tasto Z e il boma che sbatte in virata. Tutti e due sono ancora sintetici: al §1 erano esclusi da questa fetta.

## 7. Terza parte: tutti i suoni sintetici che restano (1.2.10)

Ale, 4 novembre, dopo aver giocato: non lo convincono il tasto Z e il boma che sbatte in virata; alla proposta di rifarli con registrazioni: «sì, trova tutti i suoni». **Letto così:** Z, virata, strambata, scuffia, raddrizzata, contatto, boa, tromba, arrivo. Restano sintetici solo i segnali di passo e di prova, che non sono rumori del mondo. Soglie scritte qui prima del codice.

**Registrazioni** (Freesound, tutte CC0, lette sulla pagina il 4 novembre; non ascoltate da me). Letti altri 25 candidati.

| Suono | Freesound | Cosa dice la pagina |
|---|---|---|
| Z (tela) | 870603, CHallSmith | Lenzuolo pesante di cotone scosso |
| Virata e strambata (boma) | 630432, KaleidacousticsAudio | Boma di una barca a vela che cigola in navigazione, microfono a contatto |
| Virata e strambata (colpo) | 799644, KudoShimon | Colpi su legno, vestiti e altro |
| Contatto | 637207, kyles | Colpi su vetroresina di una barca sull'acqua |
| Boa | 538009, bruno.auzet | Una barchetta che urta un parabordo (un vecchio copertone), onde e vento |
| Scuffia | 469608, Sheyvan; 442773, qubodup | Tuffo grande; 442773 è un montaggio di altri suoni CC0 |
| Raddrizzata | 110593, korbel | Acqua che si muove vicino a una barca |
| Tromba e arrivo | 131930, mcpable | Tromba ad aria di una piattaforma petrolifera, in Alberta |

**Scartati, con il motivo:** 342446 (boe di metallo enormi); 414208 (tromba «fatta con Audacity»); 568012 (tromba con colpi e un racconto che non c'entra); 55027 e 865175 (quasi solo gravi, e il primo è già rielaborato); 617019 (vestito in mano, voluto come divisa militare); 161717 (collage).

**Semplificazioni da dichiarare:** il lenzuolo non è una vela; il colpo non è un boma; il parabordo non è una boa; la tromba è di una piattaforma, non di una barca giuria. Il tempo della tromba lunga passa da 2,0 a circa 1,7 s, la durata del suono registrato. La regola 26 non fissa una durata.

**Come suonano** (ipotesi nostre): Z è un giro di 8 s, volume 0,15 + 0,35 × min(1, aws/10), solo mentre il boma è spinto. La virata è il cigolio del boma più un colpo debole; la strambata un colpo forte col vento più il cigolio. Gli altri sono il loro ritaglio. Stessa decodifica a due tempi: se la seconda fallisce restano i suoni sintetici di prima.

**Criteri:**
- **H1:** S1 verde; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; G2-G5 verdi; **tutti gli altri suoni identici al byte a quelli della 1.2.9.**
- **H2:** con i suoni decodificati, virata, strambata, scuffia, raddrizzata, contatto, boa, tromba, tromba lunga e arrivo non creano **nessun oscillatore** (la nota finta è sparita davvero); con la seconda decodifica rotta apposta sì (la controprova che il conteggio funziona).
- **H3:** Z: il giro segue la formula in ogni lettura, almeno 500; a Z rilasciato 0.
- **H4, si sente** (collaudo che ascolta, volume «bassi», 3 volte per suono): ognuno dei nove eventi alza la banda 200-5.000 Hz di almeno **6 dB** sul tratto prima, al traverso a 10 nodi; Z vero (tasto premuto), acceso contro spento, almeno **+2 dB** nella banda 500-5.000 Hz.
- **H5, non satura:** a «alto», 20 nodi con la prua al vento, strambata, contatto e gabbiano insieme: picco al più **−0,5 dB**.
- **H6, costo:** `js/suoni-dati.js` al più **900 KB** (la soglia sale di nuovo: 700 era per gli otto suoni di prima); seconda decodifica al più 1.500 ms, come G4.
- **Ascolto:** lo giudica Ale.
