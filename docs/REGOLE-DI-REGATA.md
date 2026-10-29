# Regole di regata: il regolamento vero e il gioco

Del 13 ottobre 2026. Confronto fra il regolamento di regata in vigore e quello che fanno oggi le regate del gioco (0.21.5), per decidere quali regole e sanzioni vere mettere nel gioco. **Nessuna modifica al gioco in questo documento.**

## Fonte

**F15:** World Sailing, *The Racing Rules of Sailing 2025-2028* (RRS), edizione di giugno 2024, © World Sailing Limited.
- **Copia locale:** `fonti-pdf/RRS-2025-2028-World-Sailing.pdf`, esclusa da git. L'abbiamo trovata sul sito della federazione asiatica di vela: <https://www.asiansailing.org/wp-content/uploads/2024/07/RRS-2025-2028-Final.pdf>.
- **Copia ufficiale:** World Sailing la indica da scaricare dalla pagina <https://sailing.org/inside-world-sailing/rules-regulations/racingrules/>, che però non dà un collegamento diretto al PDF.
- **Correzioni:** esistono correzioni successive, in vigore dal 1° gennaio 2025, e il riassunto di US Sailing (versione 2, 30 gennaio 2026) parla soprattutto di refusi. Non le abbiamo confrontate riga per riga.
- **Traduzione italiana:** in Italia il regolamento si chiama «Regolamento di Regata World Sailing» (RRS). Una traduzione della Federazione in PDF non è stata trovata.

**Diritti (principio 5):** il testo è di World Sailing. Qui e nel gioco **si parafrasa e si cita il numero della regola**, non si copia il testo. Le regole si applicano ovunque si regati: citarle non crea titoli ufficiali, e nel gioco resta «nessun valore legale».

## Le regole che contano per il gioco

Ogni riga: cosa dice la regola (parafrasi), cosa fa il gioco oggi (con il punto del codice), che cosa manca.

### Definizioni

| Termine | Regolamento (parafrasi) | Gioco oggi |
|---|---|---|
| **Partenza** | Si parte quando, dopo essere stati interamente dalla parte di pre-partenza della linea allo sparo o dopo, una parte dello scafo attraversa la linea verso il percorso | Conta il centro della barca che taglia la linea fra le due boe (`raceLegs`) |
| **Arrivo** | Si arriva quando una parte dello scafo attraversa la linea d'arrivo venendo dal percorso | Conta il centro della barca (scelta già dichiarata: nella realtà conta la prua, circa 2 m prima) |
| **In regata** | Dal segnale preparatorio fino all'arrivo, quando la barca si è allontanata dalla linea e dalle sue boe | Dopo l'arrivo gli avversari vanno nella zona di sosta (0.21.4) |
| **Sovrapposizione** | Due barche sono sovrapposte se nessuna è «libera dietro» l'altra (cioè interamente dietro la linea perpendicolare alla poppa dell'altra) | Non usata: la colpa con le stesse mure guarda solo chi è più sopravento |
| **Zona** | L'area attorno a una boa entro tre lunghezze di scafo | Non esiste |

### Precedenze (parte 2)

| Regola | Regolamento (parafrasi) | Gioco oggi | Cosa manca |
|---|---|---|---|
| **10** Mure opposte | Chi è mure a sinistra lascia strada a chi è mure a dritta | Così (`contacts()`) | — |
| **11** Stesse mure, sovrapposte | Chi è sopravento lascia strada a chi è sottovento | Ha torto chi è più sopravento (`contacts()`) | Va applicata solo se le barche sono sovrapposte |
| **12** Stesse mure, non sovrapposte | Chi è libera dietro lascia strada a chi è libera davanti | Non distinta dalla 11 | Una barca che tampona da dietro oggi può avere ragione se è più sottovento |
| **13** Durante la virata | Dopo aver passato la prua al vento, finché non è di bolina, la barca lascia strada a tutte; in quel momento le 10-12 non valgono | Non considerata | — |
| **14** Evitare il contatto | Se ragionevolmente possibile, ogni barca evita il contatto, anche quella con la precedenza (che però può aspettare finché è chiaro che l'altra non si scansa) | Il contatto si conta, ma la colpa va sempre a una sola barca | Penalità anche a chi aveva ragione ma poteva evitarlo: difficile da giudicare in automatico |
| **15, 16** Acquisire la precedenza, cambiare rotta | Chi acquisisce la precedenza o cambia rotta deve lasciare all'altra lo spazio per scansarsi | L'aggressiva smette di stringere sotto 15 m (`AGGRO_OFF`): «lo spirito delle regole 14 e 16» (`PROGETTO.md`) | — |
| **18** Spazio alla boa | Nella zona (3 lunghezze), chi è all'esterno lascia spazio a chi è all'interno; ci sono eccezioni (per esempio di bolina fra mure opposte) | Non esiste | Complessa: da rimandare |
| **21.1** Chi torna dopo una partenza anticipata | Lascia strada a chi non lo sta facendo, finché non è tornata | Non considerata | — |
| **21.2** Chi sconta una penalità | Lascia strada a chi non la sta scontando | Non esiste (non ci sono giri) | Serve con i giri di penalità |
| **22** Barca scuffiata | Se possibile, le altre la evitano | I contatti con barche scuffiate non si contano (`contacts()`) | — |
| **23.1** Chi non è in regata | Se ragionevolmente possibile, non intralcia chi è in regata | Zona di sosta dopo l'arrivo (0.21.4) | — |

### Partenza, percorso, arrivo (parte 3)

| Regola | Regolamento (parafrasi) | Gioco oggi | Cosa manca |
|---|---|---|---|
| **26** Procedura di partenza | Avviso a 5 minuti (bandiera di classe), preparatorio a 4 (bandiera P, I, Z, U o nera), un minuto (preparatorio ammainato), partenza a 0; i tempi contano sui segnali visivi | Preparazione di 1, 3 o 5 minuti, messaggi a 1 minuto, 30 e 10 secondi | Segnali a 5-4-1-0 con le bandiere: soprattutto didattica |
| **28** Fare il percorso | La barca deve fare il percorso, e può correggere un errore finché non è arrivata | Boa dal lato sbagliato: si rimedia girandola di nuovo (`roundCheck`) | — |
| **29.1** Richiamo individuale | Se allo sparo una parte dello scafo è dalla parte del percorso, il comitato espone subito la **bandiera X** con un suono; resta esposta finché le barche sono tornate dalla parte di pre-partenza della linea **o dei suoi prolungamenti**, ma **al massimo 4 minuti** dopo lo sparo | Messaggio con i nomi (0.21.5); la barca torna e riparte | Bandiera X disegnata (facoltativa) |
| **30** Penalità di partenza (bandiere I, Z, U, nera) | Regole più severe nell'ultimo minuto: giro attorno a un'estremità, 20% di penalità sul punteggio, squalifica | Non esistono | Da rimandare |
| **31** Toccare una boa | In regata non si tocca la boa del lato che si sta facendo (né quella di partenza prima di partire, né quella d'arrivo dopo l'arrivo) | Toccare la boa non è punito | **Un giro di penalità** |

### Penalità (parte 4)

| Regola | Regolamento (parafrasi) | Gioco oggi | Cosa manca |
|---|---|---|---|
| **44.1** Scontare la penalità | Chi può aver violato una regola della parte 2 sconta **due giri**; chi ha toccato una boa (regola 31) **un giro**. Le istruzioni di regata possono prevedere un'altra penalità (per esempio sul punteggio). Se ha causato danni o ha avuto un vantaggio grande nonostante la penalità, si ritira | +15 s al tempo del colpevole (`contacts()`) | **Due giri al posto dei 15 s** |
| **44.2** Come si fanno i giri | Appena possibile, dopo essersi allontanata dalle altre, la barca fa i giri **nello stesso verso**, e **ogni giro comprende una virata e una strambata**. Vicino all'arrivo, prima di arrivare lo scafo deve tornare tutto dalla parte del percorso | — | Riconoscere i giri del giocatore, farli fare agli avversari |
| **44.3** Penalità sul punteggio | Alternativa (bandiera gialla), solo se prevista dalle istruzioni. Se le istruzioni non dicono quanto vale, il 20% dei punti di chi non arriva, al decimo; i punti delle altre barche non cambiano (due barche possono avere lo stesso punteggio); mai oltre i punti di chi non arriva | Dalla 1.0.34, **solo nel torneo dell'1b**: +1 punto per contatto con colpa (20% di 5), con il tetto di 5; la decide il gioco al contatto, senza bandiera gialla | Nelle altre regate restano i 15 s, senza fonte |

## Cosa cambierebbe nel gioco [stima]

Proposta di priorità, da decidere:

1. **Due giri al posto dei 15 s** (44.1, 44.2), per il giocatore e per gli avversari.
   - **Giocatore:** il gioco conta già virate e strambate (`detectManeuvers`). Due giri nello stesso verso, ciascuno con una virata e una strambata, si riconoscono dalla rotazione cumulata della prua (720°) e dai due contatori.
   - **Avversari:** una manovra nuova in `aiControl`, cioè allontanarsi e poi girare due volte. È la parte più costosa.
   - **Se il giocatore non sconta i giri:** nella realtà rischia la protesta e la squalifica. Nel gioco, per esempio, «squalificato» all'arrivo, oppure i 15 s come ripiego. Da decidere.
   - **Aiuti disattivabili (principio 3):** tenere la penalità a tempo come aiuto per chi inizia.
2. **Un giro per aver toccato la boa** (31, 44.1): il gioco deve prima sapere quando la boa è toccata (oggi le boe non fanno da ostacolo).
3. **Regole 11, 12 e 13 nella colpa dei contatti:** distinguere sovrapposte e libere dietro, e chi sta virando. Tocca `contacts()` e il comportamento degli avversari.
4. **Procedura 5-4-1-0 con le bandiere** (26), ed eventualmente la bandiera X disegnata (29.1).
5. **Dopo:** spazio alla boa (18), penalità di partenza (30), evitare il contatto anche con ragione (14).

**Effetti comuni da tenere presenti:**
- **tempi delle regate:** due giri costano circa 15-25 s a 10 nodi [stima, non misurata], più dei 15 s di oggi;
- **record e piazzamenti** non più confrontabili con quelli di prima (`KEYV`);
- **collaudi da ritarare:** `collaudo_competizione.py`, `collaudo_contatto_senza_colpa.py`, `collaudo_registro.py`;
- **testi da rivedere:** istruzioni delle regate, glossario, domande d'esame sulle regate.

## Cose da correggere nei documenti

- **`FONTI-PUBBLICHE.md`, F14** diceva che la bandiera X resta esposta «al massimo 2 minuti»: era il testo di un'istruzione di regata locale. Il regolamento dice **4 minuti** (o un minuto prima di una partenza successiva). Corretto il 13 ottobre 2026.
- **`CONTENUTI-DA-VERIFICARE.md`:** le righe sulla partenza anticipata e sul richiamo individuale ora si appoggiano al testo ufficiale (F15).
- **Il dubbio sul prolungamento della linea si chiude solo in parte:** per *tornare* basta essere dalla parte di pre-partenza della linea o dei suoi prolungamenti (29.1). Se allo sparo conti anche chi è oltre il prolungamento, fuori dagli estremi, il testo non lo dice in modo esplicito: resta aperto.

## Le mure col vento esattamente dietro (osservazione 70, verificato il 29 ottobre 2026)

F15, definizioni: *Tack, Starboard or Port*: la barca è sulle mure corrispondenti al suo lato sopravento. *Leeward and Windward*: il lato sottovento è quello lontano dal vento; **solo** navigando «by the lee» (con il vento dal lato del boma) o esattamente in poppa è il lato su cui sta la randa. Quindi a 7° dalla poppa piena (come la Rossa a twa −173°) il vento viene ancora da un lato preciso: sono mure a sinistra, e la randa sta a destra. `tackOf` (`js/regate.js`, segno di `vento − prua`) dà proprio questo, e la penalità alla Rossa del 28 ottobre era giusta. Il caso non coperto è il *by the lee* (boma dal lato da cui viene il vento) e la poppa esattamente piena (twa = ±180°): lì le RRS guardano il lato della randa, il gioco guarda ancora il vento. Capita solo per pochi gradi e per brevi istanti; non cambia nessun risultato misurato. Resta una semplificazione da dichiarare (non applicata al codice).

