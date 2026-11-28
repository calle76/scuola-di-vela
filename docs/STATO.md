# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina. **A fine lavoro si SOSTITUISCE «Dove siamo», non si aggiunge sopra** (la storia sta in `CHANGELOG.md` e in `archivio/`). Le cose da fare sono in `DA-FARE.md`.

*Aggiornato: 28 novembre 2026 (gioco alla **1.3.80**, tag `v1.3.80`). La pagina di prima del riordino, intera: `archivio/STATO-28nov.md`.*

## Dove siamo

- **Il gioco:** Scuola chiusa come contenuti; Deriva con lezioni 21-25, torneo di 3 regate lunghe, stagione, finale, sponsor, regole 15-16 e 18, Coach. Com'è fatto: `IL-GIOCO.md`.
- **Ultime versioni:** 1.3.76-77 barca della giuria solida per tutti (`sperimentale/giuria/LEGGIMI.md`); 1.3.78-80 la Blu ora vede chi le sta quasi parallelo e ha la precedenza (voce 98, oss. 154; effetto piccolo nel torneo; regola 17 non entrata; `sperimentale/regola-17/LEGGIMI.md`).
- **Giro GitHub completo sulla 1.3.80** (run 46138924562, letto per intero). Rossi già noti: `moto_mare` (solo disegno, due browser), `giri_avversari` G12 (1 segmento su 270-290, due browser), `avversari1b` scenario 5 in Firefox (7 su 10). `suoni_si_sentono` H5 rosso una volta, verde rilanciato. Da controllare: C11 2,42 s, lezioni 5.8, 6.2, 6.3 (casi noti).
- **Riordino dei documenti (28 nov):** fatti lista, stato, proposte, `README.md` e documenti superati (ora in `archivio/`). Resta solo, volendo, il `CHANGELOG.md` vecchio in archivio. Chiuse le voci 8, 10 e 66.
- **Fermi o lasciati così (Ale):** oss. 147; oss. 150 (rara); voce 87 con la 88 (onde); partenze anticipate (fonte F147).

## Cosa aspetta Ale

- **Voce 82:** ordine e scala, ricambio dei rivali sì o no, 3 nomi, poi il via.
- **Regate di Ale e Lucio** (Deriva, Allenamento, rivali esperti): tipo A bastone, sul punteggio, 4 barche, 2 a testa (voce 2); tipo B triangolo, giri, 6 barche, 3 a testa (regola 18, Z7). Tasto M sui momenti alla boa, scaricare dopo ogni regata (restano le ultime 5), a mano una riga per ogni M e chi ha giocato.
- **Lucio:** il finale dell'oss. 135 e rileggere la lezione 11.
- **Fonti:** le pagine utili di https://www.racingrulesofsailing.org/ (regole 11, 15, 16, 18) in `fonti-pdf/`.
- **Disco esterno:** `bash tests/copia_su_disco.sh` (ultima il 25 nov).
- **Idea di Ale non in lista (25 nov):** i rivali guardano l'ingaggio, non solo la distanza, prima di virare.

## A inizio sessione

1. Leggere questa pagina e `DA-FARE.md`; `git status --short` (i file non tracciati dell'ambiente si lasciano fuori).
2. **Chiedere ad Ale se i crediti sono tornati:** da quello dipende se si parte da una voce grossa o da lavori leggeri.
3. Se ci sono regate nuove, o è passato tempo: ricordargli il disco esterno.
4. «Via già dato» = si esegue quando i crediti ci sono; senza il via si scrive solo la proposta.

## Come si lavora qui

- Due fermate per ogni compito (`METODO.md`, `CLAUDE.md`), soglie scritte prima. Commit e push li faccio io (file uno per uno, mai `git add -A` né `--force`). Le scelte tecniche le fa Claude e le dichiara. **Si fa il giro di tutta `DA-FARE.md`, poi si guarda cosa resta.**
- **Collaudo:** `.venv-collaudi/bin/python tests/freno.py 64 55 .venv-collaudi/bin/python tests/collaudo_nome.py` (Firefox: `BROWSER=firefox` davanti). Veloci: `node tests/fisica/polare.js`, `raffiche_e_virate.js`, `impronta1b.js`, `tests/collaudo_versione.py`, `tests/controllo_commenti.py`. In background con `run_in_background`, un comando per volta.
- Con `#collaudo` le regate restano corte (serve `--lungo`); apertura e corsa in un solo `evaluate`, pagina nuova per regata. Solo alcuni script accettano `RADICE=cartella` (copia del gioco); gli altri leggono `index.html` del repo.
- A ogni cambio della guida dei rivali i confronti al bit dei collaudi passano alla versione nuova (ora `v1.3.80`).
- **GitHub:** `gh workflow run collaudi.yml` (`allowed_domains` github.com e api.github.com); registri di un pezzo: `gh api --allow-escape-sequences repos/calle76/scuola-di-vela/actions/jobs/ID/logs`. Online: https://calle76.github.io/scuola-di-vela/
- Scrivere fuori dal repo solo con percorsi esatti e l'ok di Ale. Mai `//` a metà riga in `js/`.

## Decisioni di Ale ancora valide

- I «via» alle correzioni grosse si danno tutti insieme quando i crediti sono ripristinati. Con pochi crediti: testi, collaudi, proposte.
- Altre batterie del circuito: restano a sorteggio. «Rifai questo tratto» e domande sulle penalità: nel Coach dopo Deriva. Coach «scarso» = 6° (`DECISIONI.md`).

## Dove sta cosa

- `IL-GIOCO.md`, `PROGETTO.md`, `METODO.md`, `DECISIONI.md`, `OSSERVAZIONI-GIOCANDO.md` (ultima: 154), `COLLAUDI.md`, `FONTI-PUBBLICHE.md`, `CONTENUTI-DA-VERIFICARE.md`.
- Proposte: in `docs/` solo quelle di voci aperte; le altre in `archivio/`, elenco in `archivio/INDICE-PROPOSTE.md`.
- **Registrazioni delle regate** (`regata-….txt`): `registrazioni/`, fuori da git. Le 8 intere di `tests/rigioca_regata.py`: 04/11 21:12; 06/11 15:50, 17:59, 18:33; 07/11 16:42, 16:55, 17:07, 17:25.
