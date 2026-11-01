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
