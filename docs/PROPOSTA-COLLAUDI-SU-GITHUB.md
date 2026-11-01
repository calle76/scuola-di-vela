# Proposta: i collaudi su GitHub (fermata 1)

1 novembre 2026, gioco alla 1.0.73. Solo documento: nessun file di `.github/`, dei collaudi o del gioco è stato toccato.

## 1. Il problema

Il giro completo dei collaudi (`tests/lancia_tutti.sh`, 64 collaudi) occupa il PC di Ale per circa un'ora per browser, e i browser sono due. Mentre gira il PC non si può usare per altro. Per questo il giro completo si fa di rado, e un errore può restare nascosto per settimane: l'ha mostrato il passo 1.8 delle lezioni, rotto dal 16 ottobre e visto solo il 1 novembre (`PROPOSTA-TEST-DEI-TEST.md`).

## 2. Cos'è GitHub Actions, in breve

GitHub presta un computer (Linux) per qualche ora. Gli si dà un file di istruzioni, messo nel repository in `.github/workflows/`: «scarica il codice, installa Playwright e i browser, lancia i collaudi». Il computer parte quando lo si chiede: con un pulsante, a ogni push, o a un'ora fissa. Alla fine GitHub mostra verde o rosso nella scheda **Actions** del repository, e se qualcosa fallisce manda una mail ad Ale.

Il repository è pubblico (`DECISIONI.md`, 1 nov), quindi **non costa niente e non ha limiti di minuti** sui computer standard. Un singolo lavoro può durare al massimo 6 ore, e ne possono girare fino a 20 insieme.

## 3. Il modello più semplice

**Un file solo**, `.github/workflows/collaudi.yml`, che fa questo:

1. Scarica il repository con **tutta la storia**: quattro collaudi (`boma_poppa`, `carriera`, `esame`, `riquadro_bandiere`) confrontano con versioni vecchie prese da git.
2. Installa Node 20, la stessa versione principale del PC (oggi v20.19.2), e Python con `playwright==1.60.0` (come `tests/prepara_ambiente.sh`).
3. Installa Chromium e Firefox con le librerie di sistema (`playwright install --with-deps chromium firefox`).
4. Lancia `tests/lancia_tutti.sh` **diviso in pezzi che girano insieme**: per esempio 2 browser × 4 pezzi = 8 computer in parallelo.
5. Mette il riepilogo nella pagina del giro e salva le uscite complete come allegato da scaricare (cartella `tests/output/lancia_tutti/`).

**Quando parte:**
- con il pulsante «Run workflow» nella scheda Actions;
- a ogni `git push` su `main`.

Niente partenza notturna a orario fisso per ora: ogni push di Ale basta.

**Una sola modifica ai collaudi:** a `lancia_tutti.sh` si aggiunge l'opzione `--parte K/N`. Lancia solo un collaudo ogni N, partendo dal K-esimo, e senza l'opzione tutto resta come oggi. Il codice di uscita c'è già: `lancia_tutti.sh` esce con 1 se qualcosa è FALLITO.

**Cosa non fa:**
- non tocca il gioco;
- non scrive niente nel repository (permesso «solo lettura»);
- non usa password né chiavi;
- non sostituisce il giro sul PC finché i criteri sotto non sono passati.

## 4. Criteri (soglie: attese nostre, dichiarate prima)

| | Criterio | Soglia |
|---|---|---|
| G1 | Sullo stesso commit, i collaudi «chiari» danno su GitHub lo stesso esito (OK/FALLITO) del giro completo di Ale sul suo PC, browser per browser | 59 su 59 uguali, o ogni differenza spiegata una per una |
| G2 | `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici carattere per carattere al riferimento in git | 3 su 3 |
| G3 | Ripetibilità: 3 giri sullo stesso commit danno gli stessi esiti | 3 su 3 uguali |
| G4 | Il giro rosso si vede: su un ramo di prova con un errore messo apposta (uno dei mutanti di `tests/controprove.py`, per esempio `giri-mut`) GitHub segna rosso e manda la mail | rosso e mail, 1 su 1 |
| G5 | Durata del giro completo con tutti e due i browser, dal push al verde o rosso | al più 60 minuti |
| G6 | Nessun file scritto nel repository dal giro | 0 |

G5 è la più incerta. Ieri ho stimato circa 3 ore per browser senza pezzi paralleli: è una stima, non una misura. Se la soglia non è rispettata lo dico con il numero, e la scelta è aumentare i pezzi o tenere solo `--veloce` a ogni push.

## 5. Rischi

1. **Push del file rifiutato.** Se Ale fa il push con un token personale di GitHub, per un file in `.github/workflows/` il token deve avere il permesso «workflow». Altrimenti GitHub rifiuta con «refusing to allow a Personal Access Token to create or update workflow». Rimedio: aggiungere quel permesso al token (Settings → Developer settings), oppure creare il file dalla pagina web di GitHub. Lo si scopre al primo push.
2. **Collaudi a tempo più lenti.** I computer di GitHub hanno 4 processori, più lenti del PC. I collaudi che aspettano con un limite di tempo (`competizione` tastiera, i `wait_until`) potrebbero scadere. Se succede si riporta, e i limiti non si allungano senza dirlo.
3. **Pixel del pannello.** I caratteri del gioco sono nella cartella `fonts/` (niente Google Fonts), ma il disegno del testo dipende anche dal sistema. `collaudo_pannello.py` e i collaudi che leggono pixel potrebbero misurare 1-2 pixel diversi. Va visto con G1.
4. **Numeri di Firefox.** Su Firefox le regate escono diverse da Chromium negli ultimi bit (`COLLAUDI.md`, 28 ott). Fra il PC e GitHub il Firefox è lo stesso (lo fissa Playwright 1.60.0), ma il processore no. I due fallimenti di Firefox già accettati (G1 103/104, contatto 0,29 m) potrebbero cambiare di poco.
5. **Versione di Node.** `impronta1b.js` dice che il riferimento va rigenerato se cambia Node. Si fissa Node 20, ma la versione minore di GitHub può essere diversa da v20.19.2. G2 lo controlla.
6. **Log pubblici.** Con il repository pubblico, anche i risultati dei giri sono visibili a chiunque. Non contengono nulla di privato.
7. **Doppio lavoro.** Finché G1-G4 non passano, il giro sul PC resta il riferimento.

## 6. Cosa serve da Ale

1. Il via (fermata 2).
2. Dopo il mio commit: `git push`. Se viene rifiutato per il rischio 1, mi incolli il messaggio e ti dico come fare.
3. Il riepilogo del suo giro completo sul PC (quello di oggi), che serve per G1.
4. Guardare una volta la scheda **Actions** su GitHub e dirmi verde o rosso. Il dettaglio lo leggo io dagli allegati, se me li scarichi, oppure me lo incolli.

## 7. Dopo, se funziona

- Il giro sul PC diventa facoltativo. CLAUDE.md e `COLLAUDI.md` si aggiornano: «a fine lavoro: `git push`, poi guarda Actions».
- Si apre la porta alla proposta 5 del test dei test (controprove a tappeto, decine di ore di macchina, `PROPOSTA-TEST-DEI-TEST.md` §10), come lavoro a parte lanciato a mano.
- Si potrà aggiungere una partenza notturna, se serve.

## 8. Fermata 2 (1 novembre 2026, via di Ale: «via, fai la fermata 2»)

Fatto:
- `.github/workflows/collaudi.yml`, come al §3: 2 browser × 4 pezzi, `--parallelo 2` per pezzo (i computer hanno 4 processori), limite di 4 ore per pezzo. Un push nuovo ferma il giro ancora in corso. G6 è un passo del giro stesso.
- `tests/lancia_tutti.sh --parte K/N`, provato qui:
  - con `--dry-run`, 4 pezzi da 16 collaudi che insieme coprono esattamente i 64 di oggi;
  - `--parte 5/4` rifiutato con uscita 2;
  - `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` OK.

Non misurato: G1-G5. Da qui GitHub non si può lanciare: il primo giro parte dopo il `git push` di Ale. Le soglie restano quelle del §4.

Scelta non scritta al §3: Node è fissato a 20.19.2 esatto e non a «20», per evitare il rischio 5. Python a 3.13, come il venv del PC (3.13.5).

**Cambiato prima del primo push (Ale, 1 nov: «facciamo molti push a ogni sessione, non vorrei far partire i collaudi decine di volte»).** Niente più partenza a ogni push. Il giro parte:
- di notte (cron 02:00 UTC, cioè le 3 italiane d'inverno e le 4 d'estate; GitHub può ritardarlo), solo se nelle ultime 24 ore c'è stato almeno un commit su `main`;
- oppure a mano, con il pulsante.

Le notti senza commit si fermano dopo il controllo, che dura pochi secondi. GitHub spegne i giri notturni se il repository resta fermo 60 giorni: si riaccendono dalla scheda Actions.

## 9. Primo giro su GitHub (1 novembre 2026, lanciato a mano da Ale, commit 2cfdc06)

Confronto con il giro completo di Ale sul PC: Chromium in `tests/output/lancia_tutti/20261101-031157`, Firefox in `20261101-041521`. Le uscite di GitHub sono negli allegati, scaricati da Ale.

- **G5 durata: 23 minuti** dal via alla fine, i due browser insieme. I pezzi durano da 9 a 23 minuti. Soglia 60: rispettata.
- **G2 fisica:** `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` OK in tutti e due i browser.
- **G6:** passo verde in tutti gli 8 pezzi, quindi il giro non ha scritto nulla nel repository.
- **G1 stessi esiti:** su 64 collaudi per browser, i fallimenti già noti cadono uguali su GitHub e sul PC:
  - Chromium: avversari1b scenario 5 (7 su 10), partenze, virate2 e competizione misura;
  - Firefox: gli stessi, più torneo misura, contatto_vero (0,29 m) e giri_avversari G1 (103 su 104).
  - I numeri delle regate sono identici, per esempio partenze 6,7% / 5,0% in Chromium e 6,7% / 1,7% in Firefox su tutti e due i computer.

  **Differenze: 4 collaudi su 64**, nessuna del gioco:
  1. `collaudo_moviola.py` (tutti e due i browser): **errore del collaudo**. Apriva il gioco da un percorso fisso, `/home/callle/scuola-di-vela`, che su GitHub non esiste. Vuol dire anche che, lanciato da una copia (le controprove), collaudava il gioco originale. Corretto: ora il percorso parte dalla cartella del collaudo. Rilanciato qui: OK. Stesso difetto corretto in `misura_partenze_torneo.py`, che non è nel giro.
  2. `collaudo_torneo.py (misura)` Chromium: fallito sul PC (C11, uscita dal menu 3,00 s contro 2 s), OK su GitHub.
  3. `collaudo_registrazione.py` Firefox: E2 fallito su GitHub (+5,2% contro 3%), OK sul PC (+0,1%).
  4. `collaudo_riquadro_bandiere.py` Firefox: Q7 fallito sul PC (0,330 ms, 3,8%), OK su GitHub (0,130 ms, 4,0%).

  Le differenze 2-4 sono tutte **misure di tempo**: secondi dell'orologio vero o costo del calcolo. Dipendono dal carico del computer in quel momento, quindi cambiano da un giro all'altro su tutti e due i computer. Le soglie non sono state toccate.
- **Altre differenze nelle uscite, con collaudi verdi:** 1-2 pixel nei riquadri del libretto (365 contro 363); tempi di gioco di 1 s nel giro di boa; qualche centesimo nel boma spinto; un byte nel file del registratore. Vengono da caratteri disegnati in modo leggermente diverso e da collaudi che misurano tempi veri. Nessuna è fuori soglia.
- **G3 (tre giri uguali) e G4 (rosso su un errore messo apposta): non ancora fatti.**

Proposta per la prossima fermata, da approvare: un elenco di «fallimenti noti», così il giro diventa rosso solo per un fallimento nuovo. I collaudi a misura di tempo (C11, E2, Q7 e simili), su GitHub, si segnano «da controllare» invece che «fallito», senza cambiare le soglie.

Le azioni di GitHub (`checkout@v4` e le altre) danno un avviso: Node 20 è superato e GitHub le fa già girare con Node 24. Non le ho aggiornate: l'avviso non cambia gli esiti, e un numero di versione sbagliato fermerebbe il giro. Si aggiornano in una fermata a parte.

## 10. Fallimenti noti (fermata 2, via di Ale: «via per i fallimenti noti», 1 novembre 2026)

**Regola.** Un collaudo uscito con errore è **NOTO** solo se valgono tutte e due le condizioni:
- la sua uscita contiene tutte le righe scritte per lui in `tests/fallimenti_noti.txt`, identiche, per quel browser;
- non ha nessun'altra riga di fallimento: un controllo `NO` o `FALLITO`, un elenco di casi sbagliati non vuoto, `Traceback` o `…Error:`.

Le regate girano a passi fissi con semi fissi, quindi gli stessi numeri escono uguali a ogni giro e su tutti e due i computer. Per virate2, che stampa solo «ESITO: FALLITO», la voce contiene anche le due righe della conferma con i numeri e la riga degli errori della pagina.

**Misure di tempo (voci `~~`).** Un collaudo è «misura di tempo» se ogni controllo fallito contiene uno dei frammenti scritti: `C11 `, `E2 passo di simulazione`, `Q7 costo del disegno`. Solo con `GITHUB_ACTIONS=true` va in DA CONTROLLARE; sul PC resta FALLITO con la nota. Il riassunto (ESITO, casi sbagliati) non conta, perché ripete i controlli singoli.

**L'elenco (dal giro di Ale sul PC, uguale a quello su GitHub).**
- In Chromium e Firefox: avversari1b, partenze, virate2, competizione misura.
- Solo Firefox: contatto_vero (0,29 m) e giri_avversari G1 (103 su 104).
- Misure di tempo: torneo misura C11, registrazione E2, riquadro bandiere Q7.

**Misurato.**
- **Uscite vere del 1 novembre:** 26 su 26 classificate come atteso.
  - 18 NOTI: 9 PC e 9 GitHub, cioè 4 collaudi in Chromium e 5 in Firefox (contatto_vero e giri_avversari solo in Firefox).
  - 6 misure di tempo.
  - 2 moviola su GitHub rimaste FALLITO («errore di Python»).
- **5 uscite cambiate apposta:** tutte FALLITO, con il motivo giusto.
  1. Un numero della conferma di virate2 cambiato (82 → 83).
  2. Un `NO` in più.
  3. L'uscita di Firefox letta come Chromium.
  4. Torneo con C11 più un controllo C3 sbagliato.
  5. Un collaudo che non è nell'elenco.
- **Giro finto completo** (copia con collaudi che ristampano le uscite vere):
  - virate2 e partenze NOTO, uscita 0;
  - torneo FALLITO sul PC e DA CONTROLLARE con `GITHUB_ACTIONS=true`, uscita 0;
  - moviola FALLITO, uscita 1;
  - avversari1b fatto passare: OK, con la riga «ora passano».
- **Collaudi vuoti:** anche uno script rotto (errore di sintassi) è stato preso come FALLITO.

**Atteso al prossimo giro su GitHub, con la moviola corretta:** verde in tutti gli 8 pezzi, con i noti e le misure di tempo elencati. È un'attesa, non una misura. G3 (tre giri uguali) e G4 (rosso su un errore messo apposta) restano da fare.

## 11. Secondo giro su GitHub (1 novembre 2026, commit 22cd490, lanciato a mano da Ale)

**Verde in tutti gli 8 pezzi**, come atteso al §10. Durata **23 minuti**, dalle 07:16 alle 07:39 UTC. I pezzi durano da 10 a 23 minuti. Gli esiti sono letti dall'elenco pubblico dei giri di GitHub. I riepiloghi con i noti e le misure di tempo non li ho letti: servono gli allegati.

Restano da fare:
- G3: tre giri uguali. Ne mancano uno o due, che arrivano da soli con i giri notturni.
- G4: rosso su un errore messo apposta, da lanciare a mano su un ramo di prova.

Dopo, il giro sul PC diventa facoltativo (§7).
