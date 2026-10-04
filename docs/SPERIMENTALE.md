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

## Tappe del prototipo del fiocco

| Tappa | Contenuto | Stato |
| --- | --- | --- |
| A | Il fiocco come seconda vela con scotta propria e filetti, senza interazione | Fatta e approvata |
| B | La randa che copre il fiocco alle andature larghe; messaggi del pannello anche per il fiocco | Fatta e approvata dopo il giudizio di chi gioca |
| C1 | Coerenza fra vista e forza del fiocco coperto: ombra totale da 107° apparenti, cioè dove il pannello dice che il fiocco non si regola | Fatta, da approvare |
| C2 | Momento di imbardata dovuto alle vele | Da fare |
| C3 | Fiocco in virata (a collo) | Da fare |
| C4 | Massa dello scafo a due: solo confronto | Da fare |

La manovra a farfalla (fiocco dal lato opposto) non è nel prototipo.

## Tasti del prototipo

| Comando | Tasti |
| --- | --- |
| Barra | frecce ← → |
| Randa | A lasca, D cazza (anche ↓ e ↑) |
| Fiocco | Q lasca, E cazza |
