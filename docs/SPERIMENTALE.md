# Prototipi sperimentali (`sperimentale/`)

Aggiornato al 4 ottobre 2026. Regole di lavoro per gli esperimenti di fisica che vivono fuori dal gioco. Oggi c'è un solo prototipo, quello del fiocco; la sua storia e le sue misure sono in `FISICA-E-TARATURE.md`, le fonti in `FONTI-PUBBLICHE.md`, il disegno dei livelli in `VISIONE-LIVELLI-E-CARRIERA.md`.

## A cosa servono

Verificare un'idea prima di portarla in `index.html`: se la fisica di una cosa nuova (per esempio un secondo vela) regge, si costruisce sopra; se non regge, lo si scopre prima di aver costruito ruoli, lezioni e tornei.

## Regole

- **`index.html` non si tocca.** Il prototipo è una copia con le righe cambiate marcate `// FIOCCO`, così il passaggio al gioco è meccanico.
- **Una sola fonte per la fisica.** `motore_fiocco.js` legge `step()` direttamente dal prototipo, senza una copia; lo stesso vale per la regola di lettura dei filetti, usata dal pannello e dal banco di prova.
- **Misure e collaudi.** `misure_fiocco.js` produce le misure (`misure_tappa*.txt`); `collaudo_fiocco.py` guida il prototipo in un browser (`collaudo_tappa*.txt` e `output/`). Ogni tappa riscrive gli stessi due script e salva un file di risultati nuovo: i file delle tappe precedenti restano come erano.
- **Una soglia derivata va ricontrollata quando cambia ciò da cui deriva.** Nella tappa C `jibShadedAt` è passata da «metà della pressione perdibile» a «non esiste una posizione giusta», che è vera anche nell'angolo morto: la riga del rapporto che cercava la prima andatura con il fiocco coperto rispondeva 30° invece di 108°. Il modello era giusto, il rapporto no.
- **Non-regressione.** Per una barca senza fiocco, la polare, le virate e le raffiche devono restare identiche a quelle del gioco (scarto zero sui 30 casi di `polare.js`; uscite di `polare.js` e `raffiche_e_virate.js` uguali carattere per carattere).
- **Salvataggi separati.** Il prototipo usa chiavi proprie (`scuolaVelaSim.v1-fiocco` e `scuolaVelaGhost.v1-fiocco`), per non mescolarsi con quelle del gioco.
- **Non è una versione.** Nessun numero di versione; nel `CHANGELOG.md` va sotto il titolo «Sperimentale».
- **Criteri dichiarati prima.** I criteri di riuscita si scrivono prima come attese nostre e non si cambiano dopo aver visto i risultati senza dirlo. I numeri che escono dalla fascia si riportano così come sono.
- **Collaudare guidando davvero la barca**, con l'aggancio `#collaudo` e il pilota automatico, non solo leggendo il codice.
- **Il pannello** resta in 1360×650 anche nel caso peggiore. Nelle lezioni il prototipo del fiocco usa la sola randa, perché il pannello delle lezioni non ha spazio per il cursore del fiocco.
- **Chi gioca non deve giudicare la plausibilità nautica.** Si chiede solo se, dove una posizione giusta esiste, la trova, e se i messaggi nel pannello dicono cosa fare. La plausibilità la giudicano le fonti e, quando serve, una persona esperta.
- **Nei comandi git** non usare `git add -A`: file come `.gitmodules`, `.bashrc` e `.mcp.json` li monta l'ambiente e vanno lasciati fuori. Indicare i percorsi uno per uno.
- **Da quale versione di `index.html` è stata fatta la copia.** `sperimentale/fiocco.html` è nato nel commit `1b6fb33` ("Prototipo fiocco: tappa A, salvataggi separati"); il genitore di quel commit, cioè la versione di `index.html` da cui `fiocco.html` è partito, è `e616212`. Confrontando quella versione di `index.html` con `fiocco.html` di oggi: 237 righe differiscono (49 tolte, 188 aggiunte); delle 188 aggiunte, 67 portano il marcatore `// FIOCCO` sulla stessa riga, le altre 121 sono dentro blocchi marcati (corpo di funzioni introdotte per il fiocco come `sailF`, `drawTT`, `jibRange`, `ttOf`, `jibShadedAt`, il disegno della vela di prua, l'HTML del cursore del fiocco) o righe di un commento a più righe marcato solo in testa. Nessuna differenza è fuori da queste due categorie. **Regola per portare il fiocco nel gioco:** si applicano le differenze fra la versione `e616212` di `index.html` e `fiocco.html` sull'`index.html` attuale con `git apply --3way`; non si ricopia il file.

## Tappe del prototipo del fiocco

**Tutte chiuse al 4 ottobre 2026.** Il prototipo non cambia più: lo stato finale, cosa fa e cosa non fa, è riassunto in fondo a `FISICA-E-TARATURE.md`.

| Tappa | Contenuto | Stato |
| --- | --- | --- |
| A | Il fiocco come seconda vela con scotta propria e filetti, senza interazione | Chiusa e approvata |
| B | La randa che copre il fiocco alle andature larghe; messaggi del pannello anche per il fiocco | Chiusa e approvata dopo il giudizio di chi gioca |
| C1 | Coerenza fra vista e forza del fiocco coperto: ombra totale da 107° apparenti, cioè dove il pannello dice che il fiocco non si regola | Chiusa; il giudizio di chi gioca non è ancora arrivato |
| C2 | Momento di imbardata dovuto alle vele | Chiusa: **non modellato, semplificazione dichiarata** |
| C3 | Fiocco in virata (a collo) | Chiusa: **non modellato, semplificazione dichiarata** |
| C4 | Massa e coppia raddrizzante di una barca a due: solo confronto | **Non cambiata: sovrainvelamento dichiarato** |

La manovra a farfalla (fiocco dal lato opposto) non è nel prototipo.

Sul C2: misurato fuori dal motore che il momento del **solo** fiocco farebbe una barca sempre poggiera, il contrario di quello che dicono le fonti, e ingiocabile (circa 3 °/s di scarto con la barra al centro). Il momento di imbardata riguarda tutta la barca e non si aggiunge a metà. Numeri in `misure_tappaC2.txt`, ragioni in `FISICA-E-TARATURE.md`.

Sul C3: deciso di **non** modellare il fiocco a collo. In un motore cinematico sarebbe una taratura (due costanti senza fonte e il verso scritto nel codice), il meccanismo sostituisce l'equipaggio e andrebbe rifatto con il prodiere della barca a due, e il guadagno misurato è modesto: da 75 a 78 virate riuscite su 84. In virata il fiocco conta solo per la resistenza della vela che sbatte. Il modello provato, i criteri e tutti i numeri restano in `PROPOSTA-C3.md`, `banco_tappaC3.js` e `banco_tappaC3.txt` come registro della decisione.

Sul C4: deciso di **non** dare al prototipo la massa e la coppia raddrizzante di una barca a due, e di **dichiarare il sovrainvelamento**. Il banco di confronto non è stato eseguito perché i numeri che già abbiamo bastavano a decidere: (1) la coppia raddrizzante del prototipo vale 83,7 kgf·m al massimo contro i circa 60 che la fonte dà a una deriva a due **senza** trapezio, quindi quella barca sarebbe meno stabile di questa, e l'unica configurazione che risolve il sovrainvelamento è col trapezio (circa 220 kgf·m), che per il livello 2 sarebbe una seconda novità principale; (2) nel motore la massa non entra nella resistenza dello scafo, quindi una barca più pesante andrebbe più veloce, e per ritarare la resistenza non c'è fonte; (3) il peso dell'equipaggio dovrebbe diventare un'azione del prodiere, non l'automatismo di oggi. Proposta, criteri e conti restano in `PROPOSTA-C4.md`; la decisione e la nota sul timone in `FISICA-E-TARATURE.md`.

## Tasti del prototipo

| Comando | Tasti |
| --- | --- |
| Barra | frecce ← → |
| Randa | A lasca, D cazza (anche ↓ e ↑) |
| Fiocco | Q lasca, E cazza |
