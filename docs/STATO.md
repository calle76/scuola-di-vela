# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola: si aggiorna a ogni fine lavoro (8 novembre 2026, decisione di Ale). Le cose da fare, in ordine, sono in `DA-FARE.md`.

*Aggiornato: 16 novembre 2026, sera (1.3.17); prima, giornata con Fable (`PER-FABLE.md`).*

## Versione

- **Alla prossima apertura (scritto il 16 novembre a fine sessione):** 1) chiedere ad Ale se ha fatto `git push origin main --tags` (c'è anche la 1.3.16), se ha ritrovato i dati in Firefox o in Carriera, e se lui e l'amico hanno ancora i file `.json` della stagione da riprendere e cancellato i quattro rami vecchi su GitHub; 2) voce 42 di `DA-FARE.md`: proposta (fermata 1) per la terza mano del Coach, a partire dalla scuffia dentro la finestra di «altre barche» (osservazione 131); 3) voce 41: rifare sul PC in Firefox il C11 di `collaudo_torneo`, una misura per volta col freno a 64 °C, per capire se i 4 casi su 40 del giro sulla 1.3.15 sono il caso; 4) le regate nuove di Ale, se ce ne sono nella cartella (ora hanno le frasi del Coach).
- **16 novembre sera, Ale:** ora gioca la **carriera** per vedere quello che il gioco libero non mostra, e tiene i crediti per le correzioni urgenti. L'Allenamento (voce 36) ha il via ma è rimandato a una notte con i crediti rigenerati; secondo Ale sarà l'impostazione anche per gli altri livelli.
- **Un ramo solo:** il 16 novembre `fable-16nov` è stato fuso in `main` (avanzamento semplice, via di Ale); da qui si lavora su `main`.
- **16 novembre, tarda sera (Ale):** crediti finiti, si riprende fra qualche giorno. Pronti col via: **regola 18 in Deriva, versione A** (`PROPOSTA-REGOLA-18.md`, voce 49, tre domande risposte) e l'Allenamento (voce 36). Aiuto «scarso / buono» (voce 48): domande risposte, via al codice non ancora dato.
- **17 novembre, sessione di raccolta dati (nessuna versione, `js/` non toccato):** lette le regate di Lucio del 16 sera, la classifica di Ale e la foto della rotta ottimale (osservazioni 133-136). **Trovato un difetto vero:** la rotta ottimale può girare la boa dalla parte sbagliata (24 regate su 90, voce 50 di `DA-FARE.md`, proposta da scrivere). I 2 punti di Ale in una tappa sono un conto giusto (voce 51); il finale di Lucio non è nel file del 21:20 (osservazione 135: serve il secondo o la regata).
- **Ultima versione chiusa: 1.3.22** (17 novembre, tag `v1.3.22`): sette numeri nostri dichiarati o allineati nei testi (voce 60); la 1.3.21 (stesso giorno): le sette scelte del gioco dichiarate nelle lezioni («in questo gioco…», voce 9, via di Ale); la 1.3.20 (stesso giorno): la presentazione della stagione dice che solo l'ordine nella tua batteria è vero (voce 51); la 1.3.19 è il primo passo della lezione 21 con la proposta di Lucio; la 1.3.18 (stesso giorno) è il primo passo della lezione 24. Ale (17 nov): i «via» alle correzioni (rotta ottimale, voce 50, e le altre) si daranno **tutti insieme quando i crediti saranno ripristinati**, con la lista completa; le proposte restano scritte e ferme.
- **17 novembre, voce 45 (solo collaudi):** `tests/fallimenti_noti.txt` ha due voci a frammento per `collaudo_triangolo` (T2b): su GitHub un numero diverso dà «da controllare» invece di rosso; sul PC valgono sempre le righe esatte. Se T2b cambiasse molto, su GitHub non lo si vedrebbe dal rosso: si guarda l'uscita del giro.
- **17 novembre, riordino (Ale, «1 ok, 2 ok, 4 ok, 5 ok»):** le voci fatte, archiviate o ferme di `DA-FARE.md` sono in `docs/archivio/DA-FARE-archivio-17nov.md` (18 righe); cinque proposte finite spostate in `docs/archivio/` (menu a 1360x650, pulizia 1b, completamento 1b, cedere, deriva attesa 1b; rimandi aggiornati nei documenti, non nel `CHANGELOG.md` né nei commenti di `js/` e `tests/`); cancellate le copie di `tests/output/controprove/` (129 MB, si rifanno con `tests/controprove.py`). **I collaudi Ale non li lancia sul PC ma su GitHub:** a fine lavoro non si dice più «lancia tests/lancia_tutti.sh sul tuo PC» ma si lascia il giro a GitHub; le misure lunghe le faccio io, una alla volta, col freno. Restano da spostare circa 25 proposte finite che hanno rimandi nei commenti di `js/` e `tests/` (serve una versione dedicata).
- **Versione precedente: 1.3.17** (16 novembre sera, tag `v1.3.17`): lezione 11 con un esempio coi numeri e la frase «nelle regate della Scuola il vento non gira»; lezione 15 corretta sulle regole 14-16 (le 15 e 16 dalle regate di Deriva in poi). Ale ha segnalato https://www.racingrulesofsailing.org/ (casi del regolamento applicati alle regate) da consultare: da qui il sito risponde 403, Ale salverà le pagine utili in `fonti-pdf/`.
- **1.3.16** (16 novembre pomeriggio, tag `v1.3.16`, in autonomia col via di Ale): **stagione con un amico più serena agli aggiornamenti.** I file dell'amico valgono fra versioni (forma della stagione `ST_FORMA`, non più la versione del gioco), e «Riprendi dal mio file» rifà la stagione dal proprio file dopo aver perso i dati del browser (anche in carriera, D1). Tutti i criteri passano (`PROPOSTA-STAGIONE-FILE.md`, Esito). Nato dalla stagione di Ale persa in Chrome alla tappa 3: non è stato il gioco, sono stati i dati del browser.
- **1.3.15** (16 novembre, tag `v1.3.15`): il volto arrabbiato del Coach è un'immagine nuova, fatta da Ale con Gemini (F104).
- **Giro su GitHub sulla 1.3.15** (43868042746, 16 novembre): i collaudi nuovi e corretti passano nei due browser (`collaudo_giri_avversari` col G3, `collaudo_torneo_versione`, `collaudo_coach`). Rossi: `collaudo_triangolo` T2b in Firefox (numero che cambia, voce 45) e `collaudo_suoni_si_sentono` in Chromium (sartiame, e per la prima volta H5). Da guardare: C11 di `collaudo_torneo` in Firefox, 4 tornei su 40 contro 1 del giro prima (voce 41). L'esploratore del mattino (su `main`) è passato.
- **1.3.14** (16 novembre, tag `v1.3.14`, ramo `fable-16nov`): **una versione nuova non chiude più il torneo in corso** (richiesta di Ale: non riuscivano a finirne uno) e **le frasi del Coach finiscono nel file della regata**, se a regata finita si apre la «Rotta ottimale» prima di scaricare. Nella stessa sessione: voce 46 chiusa (il G3 di `collaudo_giri_avversari` in Firefox era un difetto del collaudo, non dei rivali) e le 4 regate del torneo di Ale del 16 mattina lette (osservazioni 125-128: la regola dei 20 s dell'«affollato» va nel senso voluto; le frasi dette non si sanno) e altre 4 giocate da Ale sulla 1.3.14 con le frasi nel file (129-132: «altre barche» e clou tornano coi numeri in 4 regate su 4; nella regata 4 la finestra di «altre barche» contiene la scuffia, da proporre nella terza mano del Coach, voce 42).
- **1.3.13** (16 novembre, tag `v1.3.13`, ramo `fable-16nov`): **il Coach, seconda mano** (`PROPOSTA-COACH-2.md` §8): «c'erano altre barche» solo con 20 s su 60 e non nei primi 15 s dopo il via (da 16-18 regate su 20 a 3-10), frase delle virate da 3 virate, «oltre la layline» sulla prima virata lunga. C1 passa; **C2 non passa** (i due piloti si distinguono sui semi di scelta, 10 contro 3, non su quelli di conferma, 6 contro 5); C4 non passa di una regata (7 su 10). Da guardare con le regate registrate di Ale.
- **1.3.12** (16 novembre, tag `v1.3.12`, ramo `fable-16nov`): cinque difetti piccoli trovati rileggendo le 1.3.x; il più serio: coi salvataggi di prima della 1.3.9 e una stagione in corso, chi aveva il diritto al nazionale restava senza offerte dello sponsor (`CHANGELOG.md` 1.3.12).
- **Giornata con Fable (16 novembre), tre lavori di `PER-FABLE.md`:**
  - **difetti messi apposta** (`MUTAZIONI.md`): 11 difetti su 12 visti da almeno un collaudo; M3 (giro senza strambata) non lo vede nessuno, e con ogni probabilità non può succedere; quattro proposte P1-P4 sui collaudi; **via di Ale a P1, P3 e P4 (P2 no), fatte**: controllo del giro senza strambata in `collaudo_giri` (D0b), controprova del Coach che ora parte dalla copia, uscita dal menu del torneo rimisurata se lenta;
  - **giro su GitHub sulla 1.3.12** (43761612866): un rosso nuovo, `collaudo_giri_avversari` G4, in tutti e due i browser. Confronto fatto: nella 1.3.9 i casi «due giri di fila» sono 19, dalla 1.3.10 sono 12 (ne servivano 15), perché con le regole 15 e 16 i contatti con colpa dei rivali calano da 175 a 147 su 120 regate; la durata dei giri è in soglia (21,3 s) e i debiti sono tutti scontati (121 su 121). Non è un difetto del gioco: minimo dei casi portato da 15 a 10, scritto nel collaudo (confermato da Ale il 16 novembre). Gli altri rossi sono noti (triangolo coi numeri di GitHub, suoni, C11 in Firefox);
  - **revisione del codice**: la 1.3.12 qui sopra; niente da segnalare su regole 15-16, finale, prova dei giri, menu;
  - **pilota «da giocatore»**: via di Ale, **fatto e misurato** (`PROPOSTA-PILOTA-GIOCATORE.md` §8; `tests/pilota_giocatore.js`, `tests/misura_pilota_giocatore.py`; il gioco non cambia). Scuffie 2 regate su 20 (prima 6-7), virate alla boa 0,7 (prima 1,7), 20 arrivi su 20. **Non passano** l'«affollato» (16 su 20: in metà dei casi è il gruppo dei primi 15 s dopo il via) e gli errori messi apposta (il Coach non li dice: guarda solo l'ultima virata, mostra tre frasi, e «hai virato N volte» esce solo da 4 virate). **Deciso da Ale (16 nov sera):** il pilota resta uno strumento a parte; il Coach va migliorato → `PROPOSTA-COACH-2.md` (fermata 1, **aspetta il via**): «altre barche» solo con 20 s su 60 e non nei primi 15 s dopo il via (misurato senza toccare il gioco: da 18 e 16 regate su 20 a 10 e 3), frase delle virate da 3 virate, tre frasi al massimo; il volto non cambia in nessuna variante.
- **1.3.11** (16 novembre, tag `v1.3.11`): versione B dei rivali (voce 4) scritta ma **spenta**: misurata la notte del 16, non passa M1 (−30/−45% contro −50%) né M5 (+13 rivali fuori linea, dalla partenza); resta spenta, decisione di Ale sulle strade (`PROPOSTA-REGOLE-15-16.md`, in fondo).
- **1.3.10** (notte del 16 novembre, tag `v1.3.10`): **regole 15 e 16 nelle regate di Deriva**, semaforo giallo, lezione 24; nel torneo un terzo dei contatti ora è colpa di chi prende la precedenza manovrando. Prossima la versione B (voce 4, guida dei rivali).
- **1.3.9** (notte del 15 novembre, tag `v1.3.9`, in autonomia): **gli sponsor a contratto** (tappa 4), quattro gradini, offerte a fine contratto, il nazionale con uno sponsor nazionale, giudizio leggero dopo ogni tappa.
- **1.3.8** (notte del 15 novembre, tag `v1.3.8`): i messaggi annotati per `collaudo_registro` (voce 35, giro GitHub sulla 1.3.6).
- **1.3.7** (notte del 15 novembre, tag `v1.3.7`, in autonomia): **la finale** (tappa 3), a Baia delle Sette Vele (nome approvato da Ale il 16 nov), coi primi 6 del nazionale.
- **1.3.6** (15 novembre, tag `v1.3.6`): il Coach dice le scuffie ed è arrabbiato anche per quelle (prova di Ale); `collaudo_menu` e `collaudo_cono` rimessi in ordine dopo il giro GitHub sulla 1.3.3.
- **1.3.5** (15 novembre, tag `v1.3.5`): **Deriva in carriera, con punti propri e «Deriva superata»** (primi 3 dello zonale, o merito con quota provvisoria 19/21). **La cornice di Deriva (tappa 2 del piano) è finita.**
- **1.3.4** (15 novembre, tag `v1.3.4`): **il volto del Coach**, tre espressioni fatte da Ale con ChatGPT (arrabbiato con una penalità o la partenza anticipata, contento se va bene, serio altrimenti).
- **1.3.3** (15 novembre, tag `v1.3.3`): **il Coach nella moviola**, al posto del riassunto della rotta ottimale: al massimo tre frasi con un numero misurato, cliccabili (momento clou in metri di percorso, coperto, layline, partenza, penalità, «quasi perfetta»). K1-K9 passano; da decidere la regola dell'«affollato», che col pilota scatta in 17 regate su 20 (`PROPOSTA-COACH.md`, Esito). Il volto c'è dalla 1.3.4.
- **1.3.2** (15 novembre, tag `v1.3.2`, in autonomia): **la prova 6 di Deriva, «I giri di penalità», con le medaglie** (240/300/385 s, scelte sui semi 1-30 e confermate sui 101-130). Due giri dovuti dal via, contati come nelle regate; 15 s per ogni giro non fatto. Fuori dai meriti della Scuola (`CHANGELOG.md` 1.3.2).
- **1.3.1** (15 novembre, tag `v1.3.1`): **lezioni di Deriva 21 (torneo), 22 (rivedere) e 23 (layline)**, con ripassi, 6 voci di glossario ed esercizi in regata per la 22 e la 23; fuori da meriti ed esame della Scuola. D4, D5, D8 passano (`CHANGELOG.md` 1.3.1; nella 23 il primo pilota del collaudo era fuori soglia sui semi di conferma, 7 su 10, per la guida degli avversari alla boa: corretto il pilota e confermato su semi nuovi). La prova dei giri passa alla 1.3.2.
- **1.3.0** (15 novembre, tag `v1.3.0`): **menu a due livelli, «La scuola» e «Deriva»**, prima versione della cornice di Deriva (tappa 2). Nel gioco libero due pulsanti nuovi in alto; Deriva ha le regate nei salti di vento e con i giri di penalità e il torneo (con la stagione); in carriera il menu non cambia, Deriva resta nascosta fino alla 1.3.3. Nessun contenuto nuovo. Collaudo nuovo `collaudo_menu_livelli.py` (0 px di eccesso in 12 combinazioni, Chromium e Firefox); 20 collaudi ritoccati per passare da «Deriva» (`CHANGELOG.md` 1.3.0).
- **1.2.41** (15 novembre, tag `v1.2.41`): **giro dei collaudi su GitHub rimesso in ordine.** Tre difetti veri dello schermo (finestra delle impostazioni che scorreva di 23 px, righe lunghe della classifica del torneo che andavano a capo, lezione 11.3 che scorreva di 44 px), collaudi aggiornati ai nomi dei rivali, tutti e due i browser in ogni pezzo del giro, fallimenti noti aggiornati; in più, su richiesta di Ale, la rotta ottimale con B lascia solo barra e pulsanti, senza «Arrivato!» né orologio, e la scritta della boa non copre più la boa (`CHANGELOG.md` 1.2.41). Da qui `gh` legge i giri da solo (token di sola lettura nel portachiavi del PC: serve uscire dalla protezione dei comandi). Aperti: voce 40, C11 di `collaudo_torneo` in Firefox su GitHub, sartiame di `collaudo_suoni_si_sentono`.
- **1.2.40** (15 novembre, tag `v1.2.40`): **rotta ottimale in assoluto, a richiesta** (pulsante «Migliore in assoluto» o tasto V nella rotta ottimale; criteri dichiarati per scelta di Ale, `PROPOSTA-ROTTA-ASSOLUTA.md` §10-11).
- **1.2.39** (14 novembre notte): **il circuito nazionale.** Nella finestra della stagione si sceglie zonale o nazionale; al nazionale 12 regatanti (tu, i 10 nazionali, il primo del tuo zonale), due batterie da 6, rivali più forti (4-4-2); in carriera serve il diritto, nel gioco libero è sempre aperto; i primi 3 hanno il diritto alla finale, solo scritto. Tutti i criteri passano (`PROPOSTA-NAZIONALE.md`, esito del passo 2); a numeri il nazionale è più duro di poco (posto relativo 0,544 contro 0,507). Prima, lo stesso giorno:
  - 1.2.38: regate a 6 barche, di prova (N2 dichiarato, scelta A di Ale);
  - 1.2.37: stagione con un amico (codice e file);
  - 1.2.36: stagione del circuito zonale;
  - 1.2.35: testi dei rivali;
  - 1.2.34: scritte sopra le barche.

  Da pushare: `git push origin main --tags` (da qui non si vede se i tag dalla 1.2.30 sono già su GitHub; il comando non fa danni se lo sono).
- **Notte 14-15 novembre, in autonomia:**
  - piano di chiusura di Deriva: le 5 decisioni prese con Ale (`PIANO-CHIUSURA-DERIVA.md`, `DECISIONI.md`);
  - **1.2.40 rotta in assoluto: chiusa il 15 novembre** (tag `v1.2.40`), a richiesta col tasto V per scelta di Ale; P1, A1, A2, P3, A3 dichiarati (`PROPOSTA-ROTTA-ASSOLUTA.md` §10-11);
  - proposte scritte per le tappe 2-4 (fermata 1): `PROPOSTA-DERIVA-CIRCUITI.md`, `PROPOSTA-FINALE.md`, `PROPOSTA-SPONSOR.md`.
- **Prossimo:** il 16 novembre Ale lavora con Fable (`PER-FABLE.md`). Poi tappa 5 (rivali che regatano meglio: prima la proposta unica regole 15-16 più voce 4, `PROPOSTA-REGOLE-15-16.md`, che aspetta il via e la scelta di G), 6 (punti da sistemare), 7 (uscita: quota del merito, prova a mano). Decisi il 16 nov: nomi di finale e sponsor approvati; «affollato» del Coach com'è, da riguardare con le regate registrate di Ale.
- **L'elenco proposto in chat** per chiudere Deriva:
  - rotta in assoluto con punto ideale, direzione e traccia viola (voce 26, §9, richiesta di Lucio);
  - poi cornice della carriera di Deriva, finale, sponsor semplici, rivali che regatano meglio, punti da sistemare;
  - poi il livello del fiocco.

  Scritto come piano: `PIANO-CHIUSURA-DERIVA.md`.
- Il **guardiano degli avversari** è solo informativo (`PROPOSTA-GUARDIANO-AVVERSARI.md` §9).
- **Proposte in attesa del via** (fermata 1): carriera in profondità (`PROPOSTA-RIVALI-E-SPONSOR.md` §16); storia e conseguenze dei rivali (voce 35).
- **Online** (https://calle76.github.io/scuola-di-vela/): quella dell'ultimo push di Ale. La 1.2.18 e i 123 tag sono pushati (8 novembre sera).
- La **Scuola** (1b, barca con la sola randa) è **chiusa come contenuti** (Ale, 13 novembre): restano cose da sistemare rigiocando. **Deriva** come livello non è ancora aperto (lezioni 21-22, punti, prova, regola di passaggio, momento clou), ma molti suoi pezzi sono già nel gioco fuori dalla Scuola: torneo, rivali, cono d'ombra, rotta ottimale, layline. Cosa diventa la cornice di Deriva (forse il primo circuito zonale) è da decidere: `DA-FARE.md` voce 12.

## 13 novembre, sera

- **1.2.31 chiusa e fusa in `main`.** Ale ha scelto A e ha proposto le manovre al posto della poppa. Le manovre, cioè la prontezza e la precisione del timone, sono state provate e tolte: nel gioco spostano l'arrivo di pochi secondi, in nessuna direzione chiara (`PROPOSTA-TRATTI-RIVALI.md` §12-14). Restano due tratti con fasce doppie. Conferma sui semi 2161-2190: 8 criteri su 8; guardiano degli avversari OK, ma G9 (taglio) +0,47 su +0,5, di poco (§15).
- **Fonti lette con Ale (F86-F102):**
  - circuiti zonale e nazionale, ranking della classe Snipe e della FIV, lega tedesca;
  - partenza e lato favorito, layline;
  - Chieffi, dalle trascrizioni dei video passate da Ale: vento mediano, pressione e salti, cono in poppa di 2 lunghezze a 10-12 nodi.

  Cosa farne: DA-FARE voce 31. La ricerca dei nomi dei rivali è rifatta: Matteo Carraro diventa Matteo Bortolin (approvato).
- **Proposte nuove (fermata 1):** voce 4, rivali che virano addosso (`PROPOSTA-MANOVRE-ADDOSSO.md`); voce 3, chi si libera resta libero (`PROPOSTA-COPPIE.md` §13). Voce 32: rotta ottimale più leggibile (osservazione 122, era rimasta fuori dalla lista).

## 13 novembre, pomeriggio

- **1.2.30 chiusa e fusa in `main`** (S1 40 tornei 0 differenze, S5 Chromium e Firefox senza `#collaudo`: `PROPOSTA-SCHEDA-RIVALI.md` §11). Per il caldo c'è un freno che sospende i collaudi sopra i 64 °C (`tests/freno.py`: `python3 tests/freno.py 64 55 comando...`).
- **1.2.31 (tratti dei rivali) NON chiusa, ramo `tratti-rivali`** (cartella di lavoro separata, commit `e5235bf`): la conferma su semi nuovi non passa. Partenza passa di poco, la bolina solo per i principianti, la poppa no; le raffiche sono state tolte prima, perché quelle del torneo sono troppo deboli. Con le fasce raddoppiate, partenza e bolina si vedono. **Aspetta la scelta di Ale fra A, B e C** (`PROPOSTA-TRATTI-RIVALI.md` §9-11; consiglio A: due tratti, partenza e bolina, fasce doppie, poi una conferma nuova).
- **Proposte nuove (fermata 1):** carriera a circuiti zonale e nazionale, sponsor come materiale e obiettivi, venti nomi di rivali (approvati da Ale), nome del giocatore (`PROPOSTA-RIVALI-E-SPONSOR.md` §11-13; DA-FARE voci 28 e 30). Fonti F88-F92.
- **Lista:** voce 24 chiusa (punto 7, F91-F92); consiglio di riordino in fondo a `DA-FARE.md`, da fare con Ale (voce 29).
- **Stasera:** leggere con Ale gli articoli F88-F90 e rifare la ricerca dei nomi uno per uno.

## Cosa aspetta Ale

- **Giocare la 1.2.16-1.2.18 e mandare le registrazioni** («Scarica l'ultima regata»; note con «#» nel file): giri di penalità senza limite di 20 s, orologio dei giri, avversari che scontano subito, squalifica per i giri non fatti.
- **Il giro dei collaudi su GitHub** della 1.2.18 (scheda Actions → «Collaudi» → «Run workflow», completo), poi gli zip nella cartella del repo.
- **L'ordine delle cose da fare** in `DA-FARE.md`.

## Cosa è stato fatto l'8 novembre

- 1.2.16: giri di penalità del giocatore senza limite di 20 s (riparte dopo 8 s fermi); squalifica per i giri non fatti; lezione 20 aggiornata.
- 1.2.17: orologio dei giri nel riquadro (rosso che si riempie di verde, «0/2»).
- 1.2.18: avversari che scontano subito, anche prima del via, scostandosi il minimo; squalifica anche per loro.
- Proposta «coppie che si tengono»: chiusa senza correzione (`PROPOSTA-COPPIE.md` §12).
- Tag di versione per tutte le versioni dalla 0.18; release e issue su GitHub rifiutate (`DECISIONI.md`).

## Cosa è stato fatto l'8 novembre, notte

- Lette le 6 regate di Ale dell'8 sera (1.2.18, Chromium, 8 marcatori M): osservazioni 100-107 in `OSSERVAZIONI-GIOCANDO.md`, voci 2-5 e 14 di `DA-FARE.md` (ordine deciso da Claude su delega di Ale). File spostati in `registrazioni/`.
- Proposta partenza (`PROPOSTA-PARTENZA-ESTREMITA.md`), fermata 2: **non adottata**. Il riposizionamento in attesa toglie quasi tutte le barche oltre l'estremità allo sparo (conferma: 316 → 41 su 2160), ma i contatti salgono del 15% contro una soglia del 10%. Strumento nuovo: `tests/misura_partenza_estremita.py`.

## Cosa è stato fatto il 9 novembre, mattina

- Decisione di Ale: gli avversari si migliorano per le regate da Deriva in poi, cioè il torneo (`DECISIONI.md`).
- **1.2.19**: in attesa del via gli avversari non scivolano più oltre lo spillo. Nel torneo le barche oltre l'estremità allo sparo passano dal 14,3% al 2,0%, i contatti salgono del 6,2% (`PROPOSTA-PARTENZA-ESTREMITA.md` §10-13).
- Osservazioni 108-109: due regate dei giri dell'8 sera.
- **1.2.20**: gli avversari non si piantano più a destra della prima boa («giro diretto»). Nel torneo, conferma sui semi 891-920: fermate vicino alla boa 70 → 30, boa toccata 49 → 49, contatti 259 → 253 (`PROPOSTA-BOA-PIANTATA.md` §8-10). La prima prova (allargare le soglie) non era passata.

## Cosa è stato fatto il 9 novembre, pomeriggio

- Decisione di Ale: nelle regate non didattiche la fisica c'è tutta (raffiche e salti insieme, poi il cono d'ombra); il tipo di gara lo dice il formato. Le regate a tema restano didattiche.
- **1.2.21**: torneo ampliato. Regate 1-2 col punteggio, 3-4 coi giri di penalità, vento sempre misto. Avversari squalificati 0,3-1,4%, contatti per regata da −26% a +9% (`PROPOSTA-TORNEO-AMPLIATO.md` §7).
- Ricerca sul cono d'ombra: la letteratura c'è (F75, F76; `RICERCA-CONO-D-OMBRA.md`).
- **1.2.22**: rotta ottimale a regata finita (fuori dalla Scuola), con le layline e «dove hai perso». Mai più lenta di una barca vera su 1821 casi, calcolo circa 1 s (`PROPOSTA-ROTTA-OTTIMALE.md` §8). Nella stessa versione due difetti trovati dai collaudi: avversari bloccati nella regata nelle raffiche (dalla 1.2.20, `PROPOSTA-BOA-PIANTATA.md` §11) e prua della moviola alla raddrizzata (dalla 1.2.21).
- Decisioni di Ale: layline in quattro pezzi (il primo è nella 1.2.22), VMG come idea in Deriva e come strumento con Tattica, nomi dei livelli «Gennaker» e «Tattica».

## Cosa è stato fatto il 9 novembre, sera

- **1.2.23**: layline in acqua, disattivabile (riga «Layline» nelle impostazioni; nel torneo parte spenta). Gli avversari con la layline misurati e non adottati (virate −6% al massimo, soglia −10%). Lezione della layline scritta per Deriva (`PROPOSTA-LAYLINE.md`).
- Letto il giro su GitHub della 1.2.22: niente di nuovo tranne `collaudo_segnali` G2 in Firefox (il collaudo aveva troppe poche regate senza richiamo: corretto il collaudo, non il gioco) e la voce vecchia di `collaudo_partenze` in `tests/fallimenti_noti.txt` (aggiornata).

## Cosa è stato fatto la notte fra il 9 e il 10 novembre

- Diagnosi degli avversari con la rotta ottimale (`PROPOSTA-AVVERSARI-ROTTA.md`): la bolina pesa il 64% del tempo perso, la poppa il 15%.
- **1.2.24**: avversari in poppa all'angolo della polare (poppa persi −41% in conferma); layline in acqua lunghe metà bolina (osservazione 110); «layline» nell'intestazione della registrazione.
- Osservazioni 110-113 dalle regate di Ale del 9 sera (layline, partenza di Rossa, confusione alla boa 1 nel triangolo).
- Proposta bolina (`PROPOSTA-AVVERSARI-BOLINA.md`, virare sugli scarsi): **non adottata**. Al meglio −14,6% di tempo perso in bolina contro la soglia di −15%; la seconda prova dichiarata va peggio. Patch in `sperimentale/avversari-bolina-scarsi/`. Proposto prima di altro: una diagnosi delle cause in bolina (virate alla boa, angolo dei principianti, regolazione della vela).

## Cosa è stato fatto il 10 novembre, mattina (avversari in bolina; il gioco resta la 1.2.24)

- **Diagnosi** (`PROPOSTA-AVVERSARI-BOLINA.md` §8):
  - gli ultimi 40 m prima della boa 1 sono il 41% del tempo perso nella prima bolina;
  - angolo e regolazione valgono il 18%, ma sono la differenza voluta fra livelli.
- **Provate e non adottate:**
  - giro diretto da più lontano (§9-10): nessun effetto;
  - correzione del rimbalzo fra punti di passaggio (§11-12): il difetto era vero ma non costava tempo, e in conferma peggiora.
- **Provata e non adottata anche la layline di dritta** (§13-14, semi 1431-1460): la regola scatta in quasi tutti i passaggi, ma peggiora tutto (ultimi 40 m 11,1 → 12,8-13,0 s, arrivo +2,5-3,5 s, boa toccata 22 → 44-55). Chi arriva da sinistra incrocia la layline quasi sul punto 0: non c'era niente da anticipare. Patch in `sperimentale/avversari-layline-dritta/`.
- **Ale: bolina degli avversari ferma** (`DECISIONI.md`); si riprende con nuove registrazioni. Pulizia di file e cartelle fatta (commit `907413c`).
- **Ale: il cono d'ombra prima degli avversari** (`DECISIONI.md`): guardiano → cono d'ombra → registrazioni di Ale e Lucio → avversari tutti insieme.
- **Collaudo guardiano degli avversari** (`PROPOSTA-GUARDIANO-AVVERSARI.md`, `tests/collaudo_guardiano_avversari.py`): 96 regate del torneo contro il riferimento della 1.2.24, circa 6 minuti, fra i lunghi. Boccia la poppa della 1.2.23 e la layline di dritta, lascia passare le modifiche neutre. Vede solo i peggioramenti grossi (il rumore sposta l'arrivo di circa 1 s).
- **Letto il giro su GitHub della 1.2.24** (10 novembre): niente del gioco. Tre collaudi:
  - `collaudo_moviola` in Firefox: il pilota resta indietro dopo un contatto e chiude fuori tempo, come succedeva in Chromium dalla 1.2.15. Voce dei fallimenti noti aggiornata.
  - `collaudo_registratore_barche` in Firefox «NON VALIDO»: nessuna barca ferma nelle regate vere, perché gli avversari non si piantano quasi più. Corretto il collaudo: le fermate le misurano i 10 casi costruiti.
  - `collaudo_suoni_si_sentono` in Chromium: boa e sartiame poco sopra o sotto la soglia, già aperto (`DA-FARE.md` voce 8).
- **Sessione sui collaudi** (Ale: prima del cono d'ombra):
  - sei collaudi che nessuno lanciava sono entrati nel giro (86 in tutto); `collaudo_triangolo` era rotto dalla 1.2.21 per un campo cambiato nel torneo, riparato; `collaudo_avversari_deriva` e il T2b del triangolo falliscono in modo noto dalla nascita;
  - `collaudo_moviola` V3 non dipende più dall'arrivo del pilota;
  - censimento dei collaudi che dipendono dal caso in fondo a `COLLAUDI.md`: resta stretto solo il V4 della moviola.
- **Giro completo su GitHub dopo la sessione** (10 novembre, 87 collaudi, 49 minuti, 1.2.24): **nessun fallito** nei due browser. Noti: partenze, virate2, triangolo T2b, avversari di Deriva. `collaudo_suoni_si_sentono` questa volta passa (boa 7,9-10,6 dB su 6; sartiame 2,2-4,8 su 2): resta ballerino, voce 8 aperta. Il guardiano in Firefox non è identico al bit al riferimento (scritto in Chromium) ma sta nelle soglie. È il punto di partenza per il cono d'ombra.
- **Esploratore:** ora gioca anche le 4 regate del torneo (regate 100-103). Aspetta il giro lungo di Ale su GitHub (semi 1-100, 4 scimmie da 600 s, due browser).
- **1.2.25, il cono d'ombra delle vele nel torneo** (`PROPOSTA-CONO-D-OMBRA.md` §10; via di Ale: «procedi fino alla fine»):
  - meno vento a chi è coperto, numeri da F75; cono disegnato sul mare, disattivabile (casella solo nel torneo); la fisica non si spegne; Scuola identica al bit;
  - criteri K1-K15 tutti passati; `tests/collaudo_cono.py` nuovo, nel giro;
  - **gli avversari non peggiorano:** su 576 regate arrivano circa 2 s prima (±0,6) e si toccano il 17% in meno; la causa non è dimostrata;
  - non reagiscono ancora al cono: arriva col lavoro sugli avversari.
- **Esploratore sulla 1.2.24** (giro su GitHub, 3200 corse e 8 scimmie, due browser): nessun errore, nessun numero rotto; nel torneo non arriva circa il 2% degli avversari (finestra d'arrivo chiusa o squalifica). È la fotografia di prima del cono.
- **Giro su GitHub e esploratore sulla 1.2.25 letti (11 novembre, zip nella cartella del repo, non committati):** 88 collaudi per browser, nessun fallito del gioco. Da registrare (voci 15-21 di `DA-FARE.md`): avversario fermo 753 s nella regata dei salti (Chromium, seme 28); nel torneo la regata coi giri (102) ha più non arrivati (3,5% e 2,8%) delle altre; suoni, sartiame 2,2/1,9/4,3 dB; T2b in Firefox confrontato troppo alla lettera; timone2 in Firefox errore di apertura di Playwright; lezioni 5.8 e 6.3 sopra la soglia. **Seguito (11 novembre):** T2b in Firefox: era il file dei noti scritto con i numeri del PC (139 su 173, in locale identico due volte di fila) mentre GitHub dà 135 su 173; aggiunta una seconda voce, verificata con `noti.py`. `timone2` in Firefox: passa 3 su 3 in locale, da guardare. Lezioni 5.8 (5 su 100) e 6.3: valori già noti (CHANGELOG 1.2.12; 6.3 a mani ferme è migliorata, 3 su 100 contro 18 su 80), non un problema. Lezione 11 nuova: 100/100 guidando, 0/100 a mani ferme. Voce 15 fatta (1.2.27: avversario fermo vicino alla boa, causa trovata e corretta; il pc è arrivato a 73 °C, misure fermate, campione di 9 semi). Restano le voci 16-18 e 20 di `DA-FARE.md`. Rumore noto: E2 e Q7 (misure di tempo su GitHub).
- **Registrazioni di Ale sulla 1.2.27 lette (11 novembre sera, torneo regata 1 alle 14:36 e regata 2 alle 19:49, spostate in `registrazioni/`):** osservazioni 117-122. Niente di rotto, cono poco frequente (2-8 coperture per barca), bolina degli avversari da 97 a 138 s, in regata 1 due avversari su tre partiti anticipati. Due idee da proporre: etichette sui segni della moviola e zoom/schermo intero nella rotta ottimale. Mancano le registrazioni di Lucio.
- **Aspetta Ale:** push, giro dei collaudi e dell'esploratore su GitHub sulla 1.2.25, e **giocare il torneo col cono** mandando le registrazioni (ora hanno gli eventi `coperta` e `libera`).
- **Poi:** gli avversari tutti insieme (bolina, boa, uscire dal vento sporco), con le registrazioni.

## Dove sta cosa

- Il gioco in una pagina: `IL-GIOCO.md`. Principi: `PROGETTO.md`. Metodo (due fermate, soglie prima): `METODO.md` e `CLAUDE.md`.
- Decisioni di Ale e quanto costa cambiarle: `DECISIONI.md`. Difetti visti giocando: `OSSERVAZIONI-GIOCANDO.md`. Collaudi: `COLLAUDI.md`. Fonti: `FONTI-PUBBLICHE.md`.
- Le proposte (`PROPOSTA-*.md`) hanno in fondo l'esito di ogni fermata.
- **Le registrazioni delle regate** (`regata-….txt`, scaricate da Ale e Lucio) stanno in `registrazioni/`, nella cartella del repo ma fuori da git (`.gitignore`). Le nuove si mettono lì. Le 8 regate intere usate da `tests/rigioca_regata.py`: 04/11 21:12, 06/11 15:50, 17:59, 18:33, 07/11 16:42, 16:55, 17:07, 17:25.
