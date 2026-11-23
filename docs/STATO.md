# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola. **A fine lavoro si SOSTITUISCE «Dove siamo», non si aggiunge sopra** (la storia sta in `CHANGELOG.md` e in `archivio/STATO-storico-novembre.md`). Le cose da fare sono in `DA-FARE.md`.

*Aggiornato: 23 novembre 2026, notte, in autonomia (gioco alla **1.3.46**, tag `v1.3.46`).*

## Dove siamo

- **1.3.41 (voce 76, via di Ale del 22 nov):** in regata Q tenuto inquadra tutto il campo (linea, boe, barche), prima e dopo il via; nelle prove come prima; niente minimappa. `collaudo_campo_q.py` Q1-Q5 OK in Chromium e Firefox (240 inquadrature, 0 fuori; regate identiche al bit con e senza Q).
- **1.3.40 (voce 75):** niente raffiche ammucchiate al via delle regate lunghe (vento al via 0,96 della media, prima 1,77; 0 scuffie a comandi fermi su 80). **1.3.39:** il riquadro «Raddrizza» non resta sul resoconto. **1.3.38 (voce 74, passo 2a):** il Coach nomina il rivale che ti ha toccato in 2 regate. Prima: 1.3.32-1.3.37 (Coach più a lungo, volume con lo zoom, bandiere del via, freccia dell'obiettivo, storico dei rivali): `CHANGELOG.md`.
- **Studio della barca (voce 73, commit 7105a2c):** `STUDIO-BARCA.md` e `tests/fisica/studio_barca.js` (25 s, Node). Virata 0,7-0,9 lunghezze con 10-14 nodi (F106: media circa 1); con poco vento 0,7 contro 0 (manca la virata rollata); bolina lenta con poco vento (−20% a 6 nodi contro F17); sopra 16-18 nodi la virata non riesce con la regola della scotta. Le correzioni (rollata, vento forte, bolina lenta) vanno in una **sessione nuova con Opus** e solo col via; lo script è il metro prima/dopo.
- **1.3.42 (voci 48 e 77, via di Ale del 22 nov):** in regata col vento che gira, di bolina, sopra la bussola «scarso N°», «buono N°» o «nella media» (numero e soglie della lezione 11; opzione «Scarso/buono» come la layline, nel torneo spenta). Il Coach ora dice anche «se continua a girare dalla stessa parte, no»: la misura dal punto della barca gli dà ragione (88-90% contro 68% a caso), tranne col salto persistente (65-73%). `collaudo_aiuto_scarso.py` OK in Chromium e Firefox.
- **1.3.46 (voce 55, 23 nov, in autonomia): registrazioni più ricche.** Nel file il semaforo (colore e barca, anche se spento sullo schermo), la colpa di ogni contatto e fino a 60 s dopo il proprio arrivo (si chiude prima se esci, apri la rotta ottimale o scarichi). `collaudo_registrazioni_ricche` OK in Chromium e Firefox; collaudi vecchi adattati (Coach K12, registrazione A/F3/F5).
- **1.3.45 (voce 79, 23 nov, in autonomia): lezione 11 rifatta.** 9 passi: «Due venti diversi» (oscillante o persistente, come si riconoscono dal numero), la riga «scarso / buono» negli esercizi al posto di «vira adesso», l'esercizio nuovo «Vai verso il salto» (vento persistente, layline disegnate: chi vira sugli scarsi non passa), «Vicino alla boa», 3 domande nuove. `collaudo_lezione_salti` OK in Chromium e Firefox.
- **1.3.44 (voce 78, 23 nov, in autonomia):** nelle regate lunghe le raffiche sovrapposte contano 0,3 oltre la più forte: raffiche rare come in mare (99° con 2 minuti da 1,40 a 1,28, tipiche quasi uguali), vento locale massimo dei rivali da 23,6 a 18,0 nodi. Regate corte, lezioni e prove identiche. Così il passo A della 73 non serve più.
- **Voce 74:** restano la decisione 2 (cautela o nemesi, prima le fonti) e la 3 (contatore, riga a fine torneo, scuffie/penalità, amico in rete).
- **1.3.43 (22 nov sera): corretti i rossi del giro GitHub sulla 1.3.42 (run 45037412599).** Finestra Impostazioni: «Scarso/buono» andava a capo con la Layline (+36 px, torneo fuori di 1 px); ora finestra larga 760 px, «Scarso/buono» nascosta in navigazione libera; altezze uguali alla 1.3.41 (i «+2 px» di Frecce e Vista non si ritrovano). Collaudi corretti: `collaudo_vista` (in regata Q mostra tutto il campo), `collaudo_menu` M4 (commenti `/* */`), `collaudo_coach` K0 (**difetto del collaudo**: leggeva il pulsante «Rotta ottimale» prima dell'aggiornamento del pannello; solo Chromium, già dalla 1.3.31; ora 0 su 20). Cono, registratore, suoni, menu_livelli, aiuto_scarso, menu, vista OK in Chromium e Firefox; coach OK in Chromium. **`collaudo_aiuto_scarso` scalda: 81 °C col freno 64/55, 61 °C col 58/50.**
- **Giro GitHub sulla 1.3.43 (run 45058628198):** i sei corretti verdi (anche `suoni_zoom` V5). Rossi solo i noti: sartiame in `suoni_si_sentono` (Chromium, +1,6/+1,4/+3,6 dB contro +2) e C11 di `collaudo_torneo` in Firefox («torneo non chiuso» alla quarta regata, 1 caso; voci 41 e 6). E2 e Q7 solo tempi. Voce 73: **fermata 1 fatta (22 nov sera), `PROPOSTA-BARCA-73.md`.** Passo A (scotta dei rivali con la lasca) **rimandato insieme alla voce 78** (misura: rivali sbandati oltre 12° il 15,7% del tempo, 0 scuffie, 5 virate bloccate su 842, raffiche locali fino a 23,6 nodi). Passo C solo diagnosi.
- **Voci 73 e 80 chiuse (23 nov, in autonomia).** Rollata non adottata (tre prove, 3 criteri su 9 no; patch in `sperimentale/virata-rollata-73/`); virata normale contro F109: nessun cambio; bolina lenta con poco vento: limite noto confermato da F109. **Pagina dello studio:** `docs/pagina-studio-barca.html`, pubblicata (privata) su https://claude.ai/artifact/FDoEW98baSGuo17ih1uQj1: per farla vedere a Lucio va condivisa dal menu «Share».
- **Il gioco:** Scuola chiusa come contenuti; Deriva nel gioco (lezioni 21-25, torneo di 3 regate lunghe, stagione, finale, sponsor, regole 15-16, Coach in regata e nella moviola). Com'è fatto: `IL-GIOCO.md`.
- **Da sapere:** con `#collaudo` le regate restano corte (servono `--lungo`); apertura e corsa in un solo `evaluate`, pagina nuova per regata (sennò PC e GitHub danno numeri diversi). Collaudi qui uno per volta col freno; Firefox per i collaudi nuovi.

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

1. Dare i «via» con la lista di `DA-FARE.md` (64 e 54 fatti nella 1.3.23; ordine consigliato ora: 71 (uscita lenta dalle regate lunghe), 66 (altri collaudi in lungo, rotta «in assoluto»), 67-69 (dopo le risposte di Ale), 49 regola 18, 4B rivali, 36 Allenamento, 42 Coach; leggeri: 55 registrazioni più ricche, 57 volto felice, 53 distacchi T2b). L'ordine lo decide Ale.
2. **Il C11 di `collaudo_torneo` in Firefox** (voci 41 e 6): una misura per volta, col freno.
3. Regate nuove di Ale e Lucio nella cartella: leggerle (formato e cosa non contengono: voce 55).

## Cosa aspetta Ale

- **Push:** `git push origin main --tags` (dopo ogni sessione; dalla 1.3.23 alla 1.3.31 e i collaudi di questa notte sono da pushare).
- **Giro completo su GitHub dopo il push (1.3.44-1.3.46)** (Actions → «Collaudi» → «Run workflow», completo): vento delle regate lunghe, lezione 11 nuova, registrazioni più ricche; due collaudi nuovi (`collaudo_lezione_salti`, `collaudo_registrazioni_ricche`), già nella suite; poi si leggono i rossi come al solito. Sul PC E2 di `collaudo_registrazione` resta rosso come sempre (tempi col freno).
- **Giro completo su GitHub dopo il push** (commit della notte del 21 nov): conferma che P4, K0 e T2b escono come sul PC; poi si leggono i rossi come al solito.
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
