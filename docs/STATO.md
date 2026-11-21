# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola. **A fine lavoro si SOSTITUISCE «Dove siamo», non si aggiunge sopra** (la storia sta in `CHANGELOG.md` e in `archivio/STATO-storico-novembre.md`). Le cose da fare sono in `DA-FARE.md`.

*Aggiornato: 20-21 novembre 2026, notte, sessione in autonomia (gioco alla **1.3.31**, tag `v1.3.31`; questa sessione ha toccato solo collaudi e documenti, non `index.html` né `js/`).*

## Dove siamo

- **Il gioco:** Scuola chiusa come contenuti. Deriva nel gioco, non ancora «finita»: lezioni 21-25, torneo (3 regate lunghe, circa 10 minuti), stagione, finale, sponsor, regole 15 e 16, cono d'ombra, raffiche come zone, rotta ottimale, Coach nella moviola e durante la regata. Com'è fatto: `IL-GIOCO.md`. Ultime versioni: 1.3.26 regate lunghe, 1.3.28 Coach in regata, 1.3.29 triangolo da 440 m, 1.3.30-1.3.31 lezione 11 e frase del Coach (`CHANGELOG.md`).
- **Giro completo su GitHub (run 44804439764, sulla 1.3.31, Chromium e Firefox):** 5 pezzi su 8 rossi, ma **nessun difetto del gioco**: i fallimenti erano dei collaudi o già noti.
  - **Nuovi, già corretti nei collaudi:** `orologio_giri` e `riquadro_bandiere` in Chromium («canvas contaminata»: dalla 1.3.28 la foto del Coach da file impedisce di leggere i pixel; riprodotto sul PC; ora spengono il Coach); `torneo --giocatore` (C7) in tutti e due i browser (aspettava 4 regate, dalla 1.3.26 sono 3); `coach (regate lunghe)` in tutti e due (cadeva quando la rotta ottimale non compare: ora conta il caso, K0, al più 2 su 20).
  - **Non nuovi:** `suoni_si_sentono` sartiame in Chromium (2,0 contro «almeno 2»: già visto il 20 nov mattina, voci 8 e 18); T2b, E2, Q7, partenze, virate2, avversari_deriva come in `fallimenti_noti.txt`; `competizione`, `rotta`, `fasce`, `pilota_lezioni` da controllare come prima.
  - **Da rivedere al prossimo giro:** `percorso_lungo` P4 in Firefox (bolina in raffica 42% contro soglia 40%); sul PC non si riproduce (29% Firefox, 32% Chromium). Soglia non cambiata.
  - I rossi del giro del 20 nov mattina (`sponsor`, `deriva_superata`) ora sono verdi.
- **Voce 66(c) fatta** per torneo, stagione, regole 15-16 e Coach (flag `--lungo`; numeri in `COLLAUDI.md`): tutto passa tranne **C11 R7, l'uscita dal menu in 3-6 s** nelle regate lunghe (soglia 2 s): causa letta in `torChiudi`, nuova voce **71**. Nella suite completa ci sono ora 3 collaudi in lungo.
- **Proposte nuove (fermata 1, senza codice):** voci 67 (bandiere del via nei 3 minuti: prima va chiarito con Ale cosa non funziona), 68 (suggerimento del Coach visibile più a lungo), 69 (più espressioni del Coach). Voce 70 (volume dei suoni legato allo zoom): in lista, proposta da scrivere.
- **Da sapere:** con `#collaudo` le regate restano corte, quindi i collaudi senza `--lungo` non provano le regate lunghe. La rotta «in assoluto» (V) su una regata lunga ci mette ancora 9-10 s. Le frasi del Coach in regata: Ale le sta leggendo.
- **Collaudi:** lanciati qui in Chromium, col freno (picco 73 °C); Firefox per i collaudi nuovi e il giro completo su GitHub. I tentativi molto lunghi (circa 45 minuti) si interrompono: si spezzano (`--solo`).

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
- **Indagine «GitHub contro PC» (21 nov):** la stessa regata (seme, codice, versione dei browser) esce diversa fra il PC (Xeon X5660, senza AVX/FMA) e GitHub già nella prima regata di `percorso_lungo` (P2); sul PC è identica a ogni ripetizione, anche aspettando tempi diversi (prove del 21 nov), quindi il tempo vero non c'entra. Sospetti: le funzioni matematiche del browser, diverse fra Chromium e Firefox anche sullo stesso PC. Prova pronta: `tests/impronta_macchina.py` (solo numeri). Dopo il push: Actions → Collaudi → Run workflow, campo «solo» = `impronta_macchina`; poi si confronta con `tests/output` del PC (uscite salvate in `/tmp/claude-1000/ind/`). Finché non è chiusa, P4 (percorso_lungo), K0 (coach lungo) e T2b non si cambiano.
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
