# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola. **A fine lavoro si SOSTITUISCE «Dove siamo», non si aggiunge sopra** (la storia sta in `CHANGELOG.md` e in `archivio/STATO-storico-novembre.md`). Le cose da fare sono in `DA-FARE.md`.

*Aggiornato: 23 novembre 2026, notte (gioco alla **1.3.50**, tag `v1.3.50`; marcatura nell'ultima regata).*

## Dove siamo

- **Regola Ale (23 nov): si fa il giro di tutta `DA-FARE.md`, poi si guarda cosa resta.** Chi non passa di poco si annota e si va avanti.
- **1.3.50 (voce 74, marcatura, via di Ale a tutti i livelli):** nell'ultima regata del torneo il rivale a cui il duello con te decide la classifica ti marca di bolina (vira quando viri tu, da davanti e a meno di 42 m); riga nel testo della regata, Coach a −100 s, righe `marca` nel file. `collaudo_marcatura.py` su 80 tornei: K1, K2, K5-K9 passano; **K3 non misurato** (15 regate utili su 20; 94% contro 57%), **K4 no** (2 contatti con colpa del marcatore nei corti: uno identico senza marcatura, l'altro dalla virata normale alla layline). Il pilota sta vicino al marcatore pochi secondi: la prova vera sono le vostre ultime regate. **Da Ale: tenerla così o spegnerla** (`PROPOSTA-MARCATURA.md` §Esito).
- **1.3.49 (voce 49, versione A):** regola 18 nelle regate di Deriva (zona di 12,6 m, chi entra per primo, esterna/interna, 18.1(a), 18.3 semplificata, 43.1(b)); semaforo, zona disegnata (casella nelle Impostazioni), lezione 25 «Spazio alla boa», righe `zona`/`zona_fine` nel file. Libretto di Deriva: Conoscenza 10, Esperienza 7, quota 25 (approvata da Ale il 23 nov). `collaudo_regola18.py`: 13 casi su 13, Scuola identica; nelle regate corte 0 colpe diverse fuori dalla zona e 1-2 contatti decisi dalla 18; **nelle lunghe nessun contatto alla boa col pilota (Z4 non passa)**: la prova vera è Z7, sulle vostre regate. Resta la versione B (rivali che danno spazio).
- **1.3.47-1.3.48 (Lucio):** lezione 11, esempio con la boa a nord; lezione 17, la X sale solo per chi è oltre allo sparo (le sue note: gioco giusto, osservazione 142).
- **Voce 3 chiusa** (Ale). **Voce 4B, variante x4, confermata su semi nuovi:** passa M1, M4, fuori linea, non arrivati; **M3 (contatti in tutto) no** nelle corte (+3,5%) e nelle lunghe in Firefox (+6%). Non adottata, da rivedere a fine giro (`PROPOSTA-COPPIE.md` §15).
- **Voce 81 (bolina e virata con poco vento), fermata 1 fatta:** vento in quota escluso, «flat» non c'entra; un braccio sbandante (`zCE`) più lungo fa sventare a 9 nodi come Day, ma la barca resta −3/−9% e la virata −10% (soglia −30%); `zCE` senza fonte. **Non passa, motore invariato, da rivedere a fine giro** (`PROPOSTA-BOLINA-POCO-VENTO.md`, `sperimentale/bolina-81/`). Per riprenderla: misure dell'armo con fonte; abbrivio nella prima metà della virata (vera +1,48 m, gioco +0,3).
- **Voce 2:** nelle 8 regate lunghe di Ale e Lucio (principianti) i rivali vanno di bolina come voi (mediana 326 s contro 326 s), coperture brevi: nessuna proposta per ora (`PROPOSTA-AVVERSARI-BOLINA.md` §15, `tests/misura_bolina_registrazioni.py`). Servirebbero regate lunghe con gli esperti.
- **Il gioco:** Scuola chiusa come contenuti; Deriva con lezioni 21-25, torneo di 3 regate lunghe, stagione, finale, sponsor, regole 15-16 e 18, Coach. Com'è fatto: `IL-GIOCO.md`.
- **Da sapere:** con `#collaudo` le regate restano corte (servono `--lungo`); apertura e corsa in un solo `evaluate`, pagina nuova per regata. Collaudi qui uno per volta col freno; Firefox per i collaudi nuovi.

## A inizio sessione

1. Leggere questa pagina e `DA-FARE.md`; `git status --short` (i file non tracciati dell'ambiente si lasciano fuori).
2. **Chiedere ad Ale due cose:** se ha pushato, e **se i crediti sono tornati** (non si vede dai file): da quello dipende se si parte da una voce grossa o solo da lavori leggeri.
3. Se ci sono regate nuove, o è passato tempo: ricordargli il disco esterno (`bash tests/copia_su_disco.sh`).
4. **«Via già dato» = si può eseguire quando i crediti ci sono**; senza il via si scrive solo la proposta (le due fermate di `CLAUDE.md`).

## Decisioni di Ale ancora valide (17 novembre)

- **I «via» alle correzioni grosse si danno tutti insieme quando i crediti sono ripristinati**, con la lista completa (`DA-FARE.md`). Con pochi crediti: solo lavori leggeri (testi, collaudi, proposte). Le proposte restano scritte e ferme.
- Le altre batterie del circuito **non** si simulano: la classifica a sorteggio resta (voce 52 archiviata). Niente carriera di prova. «Rifai questo tratto» e le domande sulle penalità vanno nel livello Coach dopo Deriva. Il Coach resta a «scarso» = 6° (`DECISIONI.md`).
- Già con via, rimandate ai crediti: regola 18 in Deriva (voce 49), Allenamento (36). Domande risposte, via non dato: aiuto «scarso/buono» (48).

## Prossimi passi (giro della lista)

1. Voce 74: marcatura fatta (1.3.50); Ale decide se tenerla. Poi 36 Allenamento e 71 uscita lenta, poi Coach (42, 69, 66), poi 7. Versione B della 18 quando si arriva ai rivali.
2. **Il C11 di `collaudo_torneo` in Firefox** (voci 41 e 6): una misura per volta, col freno.

## Cosa aspetta Ale

- **Push:** `git push origin main --tags` (1.3.50 e i documenti del 23 nov notte).
- **Giro GitHub dopo il push** (Actions → «Collaudi» → «Run workflow», completo: il gioco è cambiato).
- **Giocare il torneo con la 1.3.49 e mandare le regate** (Ale: ok, 23 nov): servono contatti alla boa per Z7 della regola 18 (segnare col tasto M i momenti alla boa).
- **Chiedere a Lucio** per il finale dell'osservazione 135 e di rileggere la lezione 11 nuova.
- **Copia delle registrazioni sul disco esterno ogni tanto:** `bash tests/copia_su_disco.sh` (ultima il 17 nov).
- **File sciolti nella radice** (non tracciati): `stagione-*.json`, `Coach_*`, foto WhatsApp, `sessione-20261122-1909*.txt` (di Lucio), `regata-20261122-1617-intera.txt`: da spostare in `registrazioni/` o cancellare, decide Ale.
- **Regolamento applicato:** salvare in `fonti-pdf/` le pagine utili di https://www.racingrulesofsailing.org/ (casi per le regole 11, 15, 16, 18).

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
