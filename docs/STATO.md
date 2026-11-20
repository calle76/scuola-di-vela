# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola. **A fine lavoro si SOSTITUISCE «Dove siamo», non si aggiunge sopra** (la storia sta in `CHANGELOG.md` e in `archivio/STATO-storico-novembre.md`). Le cose da fare sono in `DA-FARE.md`.

*Aggiornato: 21 novembre 2026, sessione in autonomia mentre Ale era fuori (gioco alla **1.3.29**, tag `v1.3.29`, su `main`).*

## Dove siamo

- **Il gioco:** Scuola chiusa come contenuti. Deriva nel gioco, non ancora «finita»: lezioni 21-25, torneo (ora **3 regate lunghe, circa 10 minuti**), stagione, finale, sponsor dall'entrata in Deriva, regole 15 e 16, cono d'ombra, raffiche come zone sull'acqua, rotta ottimale, Coach nella moviola **e durante la regata**. Com'è fatto: `IL-GIOCO.md`.
- **Versioni del 20-21 nov:**
  - 1.3.23: Coach contento, orologio dei giri nel torneo, carriera e attestato in un file, benvenuto e sponsor all'entrata in Deriva;
  - 1.3.24: rotta ottimale e lato della boa;
  - 1.3.25: lezione «da rivedere», lezione 11 «In regata»;
  - 1.3.26: regate lunghe;
  - 1.3.27: rotta ottimale nelle regate lunghe sempre calcolata e più veloce;
  - 1.3.28: Coach durante la regata;
  - 1.3.29: triangolo delle regate lunghe da 440 m, collaudi ripassati in Chromium e Firefox.
- **Da sapere:** con `#collaudo` le regate restano corte, quindi i collaudi vecchi non provano le regate lunghe (lo fanno `collaudo_percorso_lungo`, `collaudo_coach --lungo`, `collaudo_coach_regata`). La rotta «in assoluto» (tasto V) su una regata lunga ci mette ancora 9-10 s. I file «intera» delle regate pesano circa 2 MB: decide Ale (voce 66). Le frasi del Coach in regata sono da leggere.
- **Collaudi:** lanciati qui in Chromium, col freno; Firefox per i collaudi nuovi e il giro completo su GitHub.

## A inizio sessione

1. Leggere questa pagina e `DA-FARE.md`; `git status --short` (i file non tracciati dell'ambiente si lasciano fuori).
2. **Chiedere ad Ale due cose:** se ha pushato, e **se i crediti sono tornati** (non si vede dai file): da quello dipende se si parte da una voce grossa o solo da lavori leggeri.
3. Se ci sono regate nuove, o è passato tempo: ricordargli il disco esterno (`bash tests/copia_su_disco.sh`).
4. **«Via già dato» = si può eseguire quando i crediti ci sono**; senza il via si scrive solo la proposta (le due fermate di `CLAUDE.md`).

## Decisioni di Ale ancora valide (17 novembre)

- **I «via» alle correzioni grosse si danno tutti insieme quando i crediti sono ripristinati**, con la lista completa (`DA-FARE.md`). Con pochi crediti: solo lavori leggeri (testi, collaudi, proposte). Le proposte restano scritte e ferme.
- Le altre batterie del circuito **non** si simulano: la classifica a sorteggio resta (voce 52 archiviata). Niente carriera di prova. «Rifai questo tratto» e le domande sulle penalità vanno nel livello Coach dopo Deriva. Il Coach resta a «scarso» = 6° (`DECISIONI.md`).
- Già con via, rimandate ai crediti: regola 18 in Deriva (voce 49), Allenamento (36). Domande risposte, via non dato: aiuto «scarso/buono» (48).

## Prossimi passi, quando tornano i crediti

1. Dare i «via» con la lista di `DA-FARE.md` (64 e 54 fatti nella 1.3.23; ordine consigliato ora: 66 (collaudi portati alle regate lunghe, rotta «in assoluto» più veloce, decisione sui file), 49 regola 18, 4B rivali regate lunghe (prima la proposta `PROPOSTA-PERCORSO-LUNGO.md`), 49 regola 18, 4B rivali, 36 Allenamento, 42 Coach; leggeri: 55 registrazioni più ricche, 57 volto felice, 53 distacchi T2b). L'ordine lo decide Ale.
2. **Il C11 di `collaudo_torneo` in Firefox** (voci 41 e 6): una misura per volta, col freno.
3. Regate nuove di Ale e Lucio nella cartella: leggerle (formato e cosa non contengono: voce 55).

## Cosa aspetta Ale

- **Push:** `git push origin main --tags` (dopo ogni sessione; dalla 1.3.23 alla 1.3.29 sono da pushare).
- **Chiedere a Lucio** per il finale dell'osservazione 135: «in quella regata (21:20) sei arrivato primo?» e a che secondo succede la situazione.
- **Copia delle registrazioni sul disco esterno ogni tanto:** `bash tests/copia_su_disco.sh` (ogni due settimane circa e dopo regate nuove; a inizio sessione ricordargli di collegare il disco; ultima copia il 17 nov, 74 file verificati). Lo script copia anche i `stagione-*.json`; **non** copre i salvataggi del browser (carriera: voce 54).
- **File sciolti nella radice del repo** (non tracciati): `stagione-*.json` (i vostri salvataggi; sono copiati dallo script), `Coach_*.png/jpeg` (gli originali; i jpg usati dal gioco sono in `img/`), `regata-…(1).txt` (duplicati identici: si possono cancellare). Decide Ale.
- **Regolamento applicato:** salvare in `fonti-pdf/` le pagine utili di https://www.racingrulesofsailing.org/ (da qui il sito risponde 403): casi per le regole 11, 15, 16, 18.
- Giocare e mandare le registrazioni: «Scarica l'ultima regata»; per un momento che sorprende, tasto **M** o scrivere il secondo.

## Come si lavora qui

- Due fermate per ogni compito: proposta, poi codice dopo il via (`METODO.md`, `CLAUDE.md`). Soglie scritte prima. I commit li faccio io (file uno per uno, mai `git add -A`), il push lo fa Ale.
- **Come si lancia un collaudo:** `.venv-collaudi/bin/python tests/freno.py 64 55 .venv-collaudi/bin/python tests/collaudo_nome.py [argomenti]` (Firefox: `BROWSER=firefox` davanti); i test fisici `node tests/fisica/polare.js`, `raffiche_e_virate.js`, `impronta1b.js`; controlli veloci `.venv-collaudi/bin/python tests/collaudo_versione.py` e `tests/controllo_commenti.py`. In background con `run_in_background`, non con `&`; un comando per volta (i composti con `&&` a volte vengono rifiutati). Solo 18 script su 130 (per esempio `collaudo_cono.py`, `collaudo_rotta_assoluta.py`, `misura_rotta_ottimale.py`, `misura_lato_boa.py`, i guardiani) accettano `RADICE=cartella` per girare su una copia del gioco; gli altri leggono sempre `index.html` del repo.
- `gh` legge i giri GitHub (token di sola lettura nel portachiavi; serve uscire dalla protezione dei comandi). Online: https://calle76.github.io/scuola-di-vela/ (quella dell'ultimo push).
- Per scrivere fuori dal repo (disco esterno, cartelle in `/home/callle`) serve uscire dalla protezione dei comandi: solo con percorsi esatti e con l'ok esplicito di Ale.
- Mai `//` a metà riga in `js/` (usare `/* */`); lanciare `tests/controllo_commenti.py`.

## Dove sta cosa

- Il gioco in una pagina: `IL-GIOCO.md`. Principi: `PROGETTO.md`. Metodo: `METODO.md` e `CLAUDE.md`.
- Decisioni di Ale e quanto costa cambiarle: `DECISIONI.md`. Difetti visti giocando: `OSSERVAZIONI-GIOCANDO.md` (ultima: 137). Collaudi: `COLLAUDI.md`. Fonti: `FONTI-PUBBLICHE.md`; cose da verificare: `CONTENUTI-DA-VERIFICARE.md`.
- Le proposte (`PROPOSTA-*.md`) hanno in fondo l'esito di ogni fermata; quelle finite sono in parte in `archivio/`.
- Storia: `CHANGELOG.md` (versioni), `archivio/STATO-storico-novembre.md` (stato giorno per giorno dall'8 al 17 nov), `archivio/DA-FARE-archivio-17nov.md` (voci chiuse).
- **Le registrazioni delle regate** (`regata-….txt`, di Ale e Lucio) stanno in `registrazioni/`, nel repo ma fuori da git (`.gitignore`). Le 8 regate intere usate da `tests/rigioca_regata.py`: 04/11 21:12, 06/11 15:50, 17:59, 18:33, 07/11 16:42, 16:55, 17:07, 17:25.
