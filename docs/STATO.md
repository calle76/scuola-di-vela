# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola. **A fine lavoro si SOSTITUISCE «Dove siamo», non si aggiunge sopra** (la storia sta in `CHANGELOG.md` e in `archivio/STATO-storico-novembre.md`). Le cose da fare sono in `DA-FARE.md`.

*Aggiornato: 23 novembre 2026, notte fonda, in autonomia (gioco alla **1.3.46**, tag `v1.3.46`; voci 4B e 3 misurate, non adottate).*

## Dove siamo

- **Voci 4B e 3 (23 nov, notte e mattina; via di Ale, in autonomia): non adottate, gioco ancora alla 1.3.46.** 1980 regate del torneo col pilota, corte (semi 2201-2290) e lunghe (`--lungo`, semi 2301-2360). **Voce 3:** le coppie sono rare (una ogni 7-8 regate) e la regola non le toglie sui semi nuovi (−18/−21% nelle corte, 0% nelle lunghe): proposta di chiuderla. **4B:** toglie contatti e coppie ma fa partire in anticipo molte barche (72 → 97 corte, 68 → 101 lunghe); causa trovata, le regole 15-16 nelle decisioni dei rivali prima del via; la variante x4 (solo dopo il via) lo toglie e nelle lunghe manca solo «non arrivati» +8 (= rivali dietro al pilota). Tabelle in `PROPOSTA-COPPIE.md` §15, patch in `sperimentale/coppie-4b-3/`.
- **Giro GitHub sulla 1.3.46 (run 45095888548):** rossi `collaudo_menu` M4 in Chromium e Firefox (**difetto del collaudo**: contava 7 esercizi in regata, dalla 1.3.45 sono 8; corretto, verde sul PC nei due browser) e `suoni_si_sentono` H4 boa in Chromium (5,8 dB in una delle tre letture contro 6: voce 8, già nota). Noti: `collaudo_partenze` (1). `collaudo_rotta` «da controllare» come sempre.
- **1.3.46 (voce 55):** registrazioni più ricche (semaforo, colpa dei contatti, 60 s dopo l'arrivo). **1.3.45 (voce 79):** lezione 11 rifatta (due venti diversi, esercizio col vento persistente). **1.3.44 (voce 78):** raffiche sovrapposte nelle regate lunghe contano 0,3 oltre la più forte (vento locale massimo dei rivali da 23,6 a 18,0 nodi). **1.3.41-1.3.43:** Q inquadra tutto il campo in regata; «scarso/buono» sopra la bussola; Impostazioni larghe 760 px. Prima: `CHANGELOG.md`.
- **Voci 73 e 80 chiuse (23 nov):** rollata non adottata (tre prove, 3 criteri su 9 no; patch in `sperimentale/virata-rollata-73/`; per riprenderla servono tre decisioni di Ale su B1, B2, B4); virata normale contro F109: nessun cambio. **Pagina dello studio:** `docs/pagina-studio-barca.html` (privata su https://claude.ai/artifact/FDoEW98baSGuo17ih1uQj1); Ale (23 nov): si rifà quando la barca sarà definitiva.
- **Voce 74:** restano la decisione 2 (cautela o nemesi, prima le fonti) e la 3 (contatore, riga a fine torneo, scuffie/penalità, amico in rete).
- **Il gioco:** Scuola chiusa come contenuti; Deriva nel gioco (lezioni 21-25, torneo di 3 regate lunghe, stagione, finale, sponsor, regole 15-16, Coach in regata e nella moviola). Com'è fatto: `IL-GIOCO.md`.
- **Da sapere:** con `#collaudo` le regate restano corte (servono `--lungo`); apertura e corsa in un solo `evaluate`, pagina nuova per regata (sennò PC e GitHub danno numeri diversi). Collaudi qui uno per volta col freno; Firefox per i collaudi nuovi. `tests/misura_manovre.py` misura rivali e coppie nel torneo (configurazioni nell'intestazione).

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

1. Dare i «via» con la lista di `DA-FARE.md` (4B e 3 misurate il 23 nov: aspettano una decisione; ordine consigliato ora: 71 (uscita lenta dalle regate lunghe), 66 (altri collaudi in lungo, rotta «in assoluto»), 67-69 (dopo le risposte di Ale), 49 regola 18, 4B rivali, 36 Allenamento, 42 Coach; leggeri: 55 registrazioni più ricche, 57 volto felice, 53 distacchi T2b). L'ordine lo decide Ale.
2. **Il C11 di `collaudo_torneo` in Firefox** (voci 41 e 6): una misura per volta, col freno.
3. Regate nuove di Ale e Lucio nella cartella: leggerle (formato e cosa non contengono: voce 55).

## Cosa aspetta Ale

- **Push:** `git push origin main --tags` (commit della notte del 23 nov: misura delle voci 4B e 3, collaudo del menu corretto).
- **Giro GitHub dopo il push** (Actions → «Collaudi» → «Run workflow», veloce basta: il gioco non è cambiato): fatto il 23 nov (run 45130583576): `collaudo_menu` verde, rosso solo il sartiame già noto.
- **Due decisioni** (`PROPOSTA-COPPIE.md` §15, una per volta): chiudere la voce 3? La 4B (variante x4) si giudica sulle regate lunghe o anche sulle corte?
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
