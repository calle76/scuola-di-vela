# Per Fable, 16 novembre 2026

Scritto da Claude nella notte del 15 novembre, su richiesta di Ale. Ale ha una giornata di lavoro con Fable: questo foglio dice cosa fare, in che ordine, cosa leggere e cosa non toccare. Le regole di sempre stanno in `CLAUDE.md` (due fermate, soglie scritte prima, commit a collaudi verdi, push di Ale, italiano semplice).

## Da dove si parte

- **Versione:** 1.3.9 (tag `v1.3.9`). In un giorno, il 15 novembre, sono entrate dieci versioni (1.3.0-1.3.9): menu a due livelli, lezioni 21-23, prova dei giri, Coach con volti, punti di Deriva e «Deriva superata», finale, sponsor. È tanto codice nuovo scritto in fretta: per questo il lavoro qui sotto.
- **Leggere prima:** `docs/STATO.md`, `CHANGELOG.md` dalla 1.3.0 alla 1.3.9 (lì ci sono le misure e le cose cambiate dopo averle viste), `docs/COLLAUDI.md` (senza la tabella «Browser»).
- **Giro GitHub più recente:** 43725225511, sulla 1.3.6: rossi solo `collaudo_suoni_si_sentono` in Chromium (voce 18, noto) e `collaudo_registro` in Firefox (voce 35, sistemato nella 1.3.8). Le versioni 1.3.7-1.3.9 non sono ancora passate da GitHub. Leggere i giri: `gh run list --workflow collaudi.yml` (con `XDG_CACHE_HOME=$TMPDIR/ghc`; fuori dalla protezione dei comandi se serve).
- **Collaudi:** `.venv-collaudi/bin/python tests/NOME.py`, in Firefox con `BROWSER=firefox`. Sul PC di Ale al più 2 processi insieme (`nice`). Il giro intero: `tests/lancia_tutti.sh --veloce` (circa 40 minuti) o su GitHub.
- **Lavorare su un ramo:** `git switch -c fable-16nov`. Mai `git add -A`. Il push lo fa Ale.

## 1. Rompere apposta il gioco e vedere chi se ne accorge (la cosa più utile)

I collaudi controllano di aver misurato (il «metro», dal 31 ottobre), ma nessuno ha mai misurato se diventano rossi quando la cosa che sorvegliano si rompe. Il 15 novembre è successo il contrario due volte (collaudi rossi per una ragione sbagliata, collaudi dimenticati): serve sapere quali sono deboli.

**Come:** un difetto alla volta, in una copia (`git stash` vietato in questo ambiente: meglio `git worktree add ../mutazione` o una copia con `git archive`), poi i collaudi che dovrebbero accorgersene, poi via il difetto. Mai committare un difetto.

Difetti da provare (proposta; Fable può aggiungerne):

| # | Dove | Difetto | Chi dovrebbe accorgersene |
| --- | --- | --- | --- |
| M1 | `js/regate.js`, `torPunti` | la penalità sul punteggio non si somma | `collaudo_torneo`, `collaudo_penalita_testo` |
| M2 | `js/regate.js`, `torSerie` | lo scarto non si toglie | `collaudo_torneo` |
| M3 | `js/regate.js`, `giriPenalita` | un giro vale anche senza strambata | `collaudo_giri`, `collaudo_prova_giri` |
| M4 | `js/regate.js`, colpa nei contatti | colpa invertita fra mure a dritta e a sinistra | `collaudo_regole`, `collaudo_contatto_senza_colpa`, `collaudo_registro` |
| M5 | `js/gioco.js`, `meritiD` | la «stagione senza ritiri» non serve per il merito | `collaudo_deriva_superata` |
| M6 | `js/regate.js`, `spFineStagione` | con tutti gli obiettivi non arriva il gradino sopra | `collaudo_sponsor` |
| M7 | `js/rotta.js`, `coaClou` | la finestra del clou presa 10 s più tardi | `collaudo_coach` (K4) |
| M8 | `js/moviola.js`, `rivChiudi` | niente ritorno alla schermata di fine regata (il difetto vero del 15 novembre) | `collaudo_moviola` (V6) |
| M9 | `js/contenuti.js`, `lezioniEsame` | una lezione della Scuola esce dall'esame | `collaudo_esame`, `collaudo_deriva_lezioni` |
| M10 | `index.html` | un margine in più nel pannello delle lezioni | `collaudo_pannello_lezioni` |
| M11 | `js/regate.js`, finale | i rivali della finale presi dal 2° al 6° invece che dal 1° al 5° | `collaudo_finale` (F1) |
| M12 | `js/motore.js` | resistenza dello scafo +5% | `polare.js`, `impronta1b.js` |

**Cosa consegnare:** `docs/MUTAZIONI.md` con una riga per difetto: quali collaudi sono diventati rossi, quali no, e per ogni difetto non visto una proposta (fermata 1) di controllo nuovo. Le correzioni dei collaudi dopo il via di Ale.

## 2. Revisione del codice delle 1.3.x

`git diff v1.2.41 v1.3.9 -- js/ index.html`. Dove guardare di più:
- `js/rotta.js`, sezione «coach»: le frasi e i loro numeri, il clou in metri di percorso, il tempo perso coperti;
- `js/gioco.js`, menu (`showMenu`), punti di Deriva (`meritiD`), «Deriva superata»;
- `js/regate.js`: stagione (tappe lasciate, `derivaTappa`, `zonalePulita`), finale, sponsor (`spFineStagione`, `spStato`, `spOfferteDa`);
- salvataggi vecchi: che cosa succede a chi apre la 1.3.9 con una carriera della 1.2.39 a metà stagione (nazionale in corso senza sponsor, torneo in corso).

Riportare i difetti in ordine di gravità; i difetti chiari e piccoli si correggono subito (memoria del progetto), il resto con una proposta.

## 3. Un pilota «da giocatore» (solo proposta)

Oggi quasi tutti i collaudi in regata guidano la barca con la guida degli avversari (`__sv.pilota`), che naviga in gruppo, scuffia e vira troppo vicino alla boa (voce 1b). Effetti visti il 15 novembre: il Coach dice «c'erano altre barche» in 17 regate su 20; il volto arrabbiato in 10 su 20 per le scuffie; la finale fra i primi 3 in 0-2 su 10. Serve un pilota più pulito (layline, niente gruppo, scotta regolata) per misurare Coach e quota del merito. Solo la fermata 1: proposta, criteri, rischi.

## Cose aperte da non decidere da soli (sono di Ale)

- La regola dell'«affollato» del Coach (`PROPOSTA-COACH.md`, Esito).
- La quota del merito (19 su 21, provvisoria fino alla tappa 7).
- I nomi della finale (Baia delle Sette Vele) e degli sponsor (`PROPOSTA-SPONSOR.md`, Esito).
- La voce 4 (rivali che virano addosso): proposta scritta, senza via.
