# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola. **A fine lavoro si SOSTITUISCE «Dove siamo», non si aggiunge sopra** (la storia sta in `CHANGELOG.md` e in `archivio/STATO-storico-novembre.md`). Le cose da fare sono in `DA-FARE.md`.

*Aggiornato: 17 novembre 2026, fine sessione (gioco alla **1.3.22**, tag `v1.3.22`, su `main`).*

## Dove siamo

- **Il gioco:** la Scuola (barca a una vela, 20 lezioni) è chiusa come contenuti. Deriva è nel gioco ma non ancora «finita»: lezioni 21-25, torneo e stagione (circuito zonale e nazionale, finale, sponsor a contratto in carriera), regole 15 e 16 col semaforo giallo, cono d'ombra, rotta ottimale (anche «in assoluto», tasto V), Coach nella moviola col volto (tre espressioni), stagione con un amico per file (`ST_FORMA`, «Riprendi dal mio file»). Com'è fatto: `IL-GIOCO.md`.
- **Oggi (17 nov) niente di nuovo nel motore.** Chiuse cinque versioni di solo testo: 1.3.18 (lezione 24), 1.3.19 (lezione 21), 1.3.20 (presentazione della stagione: dice che solo l'ordine nella tua batteria è vero), 1.3.21 (sette scelte del gioco dichiarate «in questo gioco…»), 1.3.22 (numeri nostri nei testi allineati alle fonti). Letti i dati di Lucio e di Ale (osservazioni 133-137).
- **Un difetto vero trovato e non ancora corretto:** la rotta ottimale può girare la boa dal lato sbagliato (osservazioni 134 e 137, voce 50): costa 2-4 s al giocatore in 7 regate su 48, fino a 21 s alle altre barche. Proposta scritta, aspetta il via.
- **Collaudi:** Ale li fa girare **su GitHub**, non sul PC. A fine lavoro non si dice «lancia `lancia_tutti.sh` sul tuo PC». Le misure lunghe le faccio io, **una per volta col freno termico** (`python3 tests/freno.py 64 55 comando…`: il PC è arrivato a 85 °C). Fallimenti noti in `tests/fallimenti_noti.txt` (T2b del triangolo ha voci a frammento per GitHub).

## Decisioni di Ale ancora valide (17 novembre)

- **I «via» alle correzioni grosse si danno tutti insieme quando i crediti sono ripristinati**, con la lista completa (`DA-FARE.md`). Con pochi crediti: solo lavori leggeri (testi, collaudi, proposte). Le proposte restano scritte e ferme.
- Le altre batterie del circuito **non** si simulano: la classifica a sorteggio resta (voce 52 archiviata). Niente carriera di prova. «Rifai questo tratto» e le domande sulle penalità vanno nel livello Coach dopo Deriva. Il Coach resta a «scarso» = 6° (`DECISIONI.md`).
- Già con via, rimandate ai crediti: regola 18 in Deriva (voce 49), Allenamento (36). Domande risposte, via non dato: aiuto «scarso/buono» (48).

## Prossimi passi, quando tornano i crediti

1. Dare i «via» con la lista di `DA-FARE.md` (ordine consigliato: 50 rotta ottimale, 49 regola 18, 4B rivali, 36 Allenamento, 42 Coach; leggeri: 54 file della carriera, 55 registrazioni più ricche, 57 volto felice, 53 distacchi T2b).
2. **Il C11 di `collaudo_torneo` in Firefox** (voci 41 e 6): una misura per volta, col freno.
3. Regate nuove di Ale e Lucio nella cartella: leggerle (formato e cosa non contengono: voce 55).

## Cosa aspetta Ale

- **Push:** `git push origin main --tags` (dopo ogni sessione; la 1.3.22 e i riordini sono da pushare).
- **Chiedere a Lucio** per il finale dell'osservazione 135: «in quella regata (21:20) sei arrivato primo?» e a che secondo succede la situazione.
- **Copia delle registrazioni sul disco esterno ogni tanto:** `bash tests/copia_su_disco.sh` (a inizio sessione ricordargli di collegare il disco; ultima copia il 17 nov, 74 file verificati). Non coperti: i `stagione-*.json` (lo script li copia), i salvataggi del browser (carriera: voce 54).
- **Regolamento applicato:** salvare in `fonti-pdf/` le pagine utili di https://www.racingrulesofsailing.org/ (da qui il sito risponde 403): casi per le regole 11, 15, 16, 18.
- Giocare e mandare le registrazioni: «Scarica l'ultima regata»; per un momento che sorprende, tasto **M** o scrivere il secondo.

## Come si lavora qui

- Due fermate per ogni compito: proposta, poi codice dopo il via (`METODO.md`, `CLAUDE.md`). Soglie scritte prima. I commit li faccio io (file uno per uno, mai `git add -A`), il push lo fa Ale.
- **Come si lancia un collaudo:** `.venv-collaudi/bin/python tests/freno.py 64 55 .venv-collaudi/bin/python tests/collaudo_nome.py [argomenti]` (Firefox: `BROWSER=firefox` davanti); i test fisici `node tests/fisica/polare.js`, `raffiche_e_virate.js`, `impronta1b.js`; controlli veloci `.venv-collaudi/bin/python tests/collaudo_versione.py` e `tests/controllo_commenti.py`. In background con `run_in_background`, non con `&`; un comando per volta (i composti con `&&` a volte vengono rifiutati). Con `RADICE=cartella` un collaudo gira su una copia del gioco.
- `gh` legge i giri GitHub (token di sola lettura nel portachiavi; serve uscire dalla protezione dei comandi). Online: https://calle76.github.io/scuola-di-vela/ (quella dell'ultimo push).
- Per scrivere fuori dal repo (disco esterno, cartelle in `/home/callle`) serve uscire dalla protezione dei comandi: solo con percorsi esatti e con l'ok esplicito di Ale.
- Mai `//` a metà riga in `js/` (usare `/* */`); lanciare `tests/controllo_commenti.py`.

## Dove sta cosa

- Il gioco in una pagina: `IL-GIOCO.md`. Principi: `PROGETTO.md`. Metodo: `METODO.md` e `CLAUDE.md`.
- Decisioni di Ale e quanto costa cambiarle: `DECISIONI.md`. Difetti visti giocando: `OSSERVAZIONI-GIOCANDO.md` (ultima: 137). Collaudi: `COLLAUDI.md`. Fonti: `FONTI-PUBBLICHE.md`; cose da verificare: `CONTENUTI-DA-VERIFICARE.md`.
- Le proposte (`PROPOSTA-*.md`) hanno in fondo l'esito di ogni fermata; quelle finite sono in parte in `archivio/`.
- Storia: `CHANGELOG.md` (versioni), `archivio/STATO-storico-novembre.md` (stato giorno per giorno dall'8 al 17 nov), `archivio/DA-FARE-archivio-17nov.md` (voci chiuse).
- **Le registrazioni delle regate** (`regata-….txt`, di Ale e Lucio) stanno in `registrazioni/`, nel repo ma fuori da git (`.gitignore`). Le 8 regate intere usate da `tests/rigioca_regata.py`: 04/11 21:12, 06/11 15:50, 17:59, 18:33, 07/11 16:42, 16:55, 17:07, 17:25.
