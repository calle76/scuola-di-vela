# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola. **A fine lavoro si SOSTITUISCE «Dove siamo», non si aggiunge sopra** (la storia sta in `CHANGELOG.md` e in `archivio/STATO-storico-novembre.md`). Le cose da fare sono in `DA-FARE.md`.

*Aggiornato: 27 novembre 2026, notte fonda (gioco alla **1.3.65**, tag `v1.3.65`).*

- **1.3.65 (voce 93):** al lasco lascare una vela troppo cazzata non fa più rallentare (forza normale dalla forma di una piastra misurata, F146); polare identica; lezione 6.3 guidando di nuovo sempre completata.
- **1.3.64 (voce 94):** il semaforo non lampeggia più sulla soglia della regola 16 (accesa resta almeno 1 s).
- **1.3.63 (voce 89):** la vela libera non porta, «Stare fermi» verde.
- **Voce 85 chiusa:** la strambata a vela aperta costa già nel gioco (`tests/misura_strambata.py`: 36° con 10 nodi, scuffia 20/20 con 15); il quinto giro aveva misurato solo il motore. **Voce 91 chiusa.**
- **Voce 2:** contro un timoniere «miope» gli esperti perdono circa 10 s per bolina (confermato su semi nuovi): proposta di chiudere la parte bolina.
- **Regola di Ale (27 nov):** le scelte tecniche (costanti senza fonte, tempi) le fa Claude e le dichiara.
- I 7 confronti al bit dei collaudi confrontano con la 1.3.65: **a ogni cambio di barca vanno portati alla versione nuova.**

## Dove siamo

- **Regola Ale (23 nov): si fa il giro di tutta `DA-FARE.md`, poi si guarda cosa resta.** Chi non passa di poco si annota e si va avanti.
- **Voce 82, rivali che crescono (proposta riscritta, scelta A di Ale, misurata la notte del 24 nov; `js/` non toccato):** il numero in acqua si sente (4,6% e 5,5% del tempo da 0 a 100) **ma quasi tutto fra 0 e 50**; G2 a metà scala (94%) e G2b in conferma (0-100 sotto 0-50) non passano. Simulazione, 300 mondi: circuiti giusti, titoli 15%, ritorno dei rivali e distanze passano; **S4 alla 10 e alla 30, S5 (46% su 50) e S6 (56 su 55) no**; tre varianti non bastano. `PROPOSTA-RIVALI-CHE-CRESCONO.md`, ultima parte. La scala si stira dopo la voce 2 (la 4B è nella 1.3.56: la misura della scala va rifatta) (proposta del 25 nov: dipende dalla barca). **Aspetta Ale: ordine e scala; ricambio (chi smette, nomi nuovi) o no; i 3 nomi; poi il via.**
- **Il gioco:** Scuola chiusa come contenuti; Deriva con lezioni 21-25, torneo di 3 regate lunghe, stagione, finale, sponsor, regole 15-16 e 18, Coach. Com'è fatto: `IL-GIOCO.md`.
- **Da sapere:** con `#collaudo` le regate restano corte (servono `--lungo`); apertura e corsa in un solo `evaluate`, pagina nuova per regata. Collaudi qui uno per volta col freno; Firefox per i collaudi nuovi.
- **Versioni dalla 1.3.49 alla 1.3.60** (regola 18, marcatura, allenamento, ritiro, albo d'oro, 4B, Stare fermi, barca M, ripartenza): `CHANGELOG.md`. Voci chiuse: 3, 35, 81 (limite noto), 89, 91.

## A inizio sessione

1. Leggere questa pagina e `DA-FARE.md`; `git status --short` (i file non tracciati dell'ambiente si lasciano fuori).
2. **Chiedere ad Ale due cose:** se ha pushato, e **se i crediti sono tornati** (non si vede dai file): da quello dipende se si parte da una voce grossa o solo da lavori leggeri.
3. Se ci sono regate nuove, o è passato tempo: ricordargli il disco esterno (`bash tests/copia_su_disco.sh`).
4. **«Via già dato» = si può eseguire quando i crediti ci sono**; senza il via si scrive solo la proposta (le due fermate di `CLAUDE.md`).

## Decisioni di Ale ancora valide (17 novembre)

- **I «via» alle correzioni grosse si danno tutti insieme quando i crediti sono ripristinati**, con la lista completa (`DA-FARE.md`). Con pochi crediti: solo lavori leggeri (testi, collaudi, proposte). Le proposte restano scritte e ferme.
- Le altre batterie del circuito **non** si simulano: la classifica a sorteggio resta (voce 52 archiviata). Niente carriera di prova. «Rifai questo tratto» e le domande sulle penalità vanno nel livello Coach dopo Deriva. Il Coach resta a «scarso» = 6° (`DECISIONI.md`).
- Domande risposte, via non dato: aiuto «scarso/buono» (48).

## Prossimi passi (27 nov, notte fonda)

1. **Giro GitHub completo sulla 1.3.65** (lo lancia Ale) e lettura per intero.
2. Voce 92 (collaudi tarati sulla barca vecchia: giri, esercizi, partenze, non partite, suggerimento a 140°, lezione 11, moto del mare, segnali B3, avversari_deriva 81/83).
3. Voce 2: chiudere la parte bolina (proposta), poi casi 81 e 83 di Deriva.

## Cosa aspetta Ale

- **Voce 88, passo 1 sul banco (26 nov, `js/` non toccato):** `sperimentale/onde-88/BANCO-ONDE.md`. Sopra M con 5 km: passano O3, O6 (bolina −6,3% con 10 nodi, −12,4% con 15), O8, O9; **non passano O1** (sotto 8 nodi la bolina perde già 4,5-5,9%), **O2** (10 nodi −0,5%, 15 nodi a 135°/180° −2,4/−3,3%), **O4 a 15 nodi** (+17%), **O5** (il pilota sull'onda non guadagna), **O7** (VMG 15 nodi 3,24 contro 3,7). **Ale (26 nov): ferma.** Si passa alla voce 2.
- **Regate di Ale e Lucio con la 1.3.57 (Deriva, Allenamento, rivali esperti):** tipo A bastone, sul punteggio, 4 barche, 2 a testa (voce 2); tipo B triangolo, giri, 6 barche, 3 a testa (Z7). M sui momenti alla boa, scaricare dopo ogni regata (restano le ultime 5), a mano: una riga per ogni M e chi ha giocato.
- **Giro GitHub sulla 1.3.56 (run 45623760335, letto per intero, anche «da controllare»):** 240 OK, 9 rossi, tutti nuovi (sulla 1.3.55 erano 2, ora verdi). Con la 4B spenta passano `avversari1b` scenario 5 (Chromium 7 contro 9 su 10; Firefox 7 contro 10 nel giro prima, non rilanciato), `non_partite` salti (seme 3), `regola21` K3 (Firefox) e K4 (Chromium), `distacchi_testo` (corretto nella 1.3.58). Pochi casi, non rilanciati: `giri_avversari` G4 (9 su 10) e `regola18` Z4, in Firefox; `registro` «contatto» noto. **Da Ale: giro completo sulla 1.3.58.** Nella 4B resta da guardare `avversari1b` (tre rivali alla boa), insieme a Z7; gli altri rossi della 4B no (da decidere se adattare i collaudi).
- **Idea di Ale (25 nov), non in lista:** i rivali guardano l'ingaggio, non solo la distanza, prima di virare; oggi virano comunque dopo 4 s di attesa. Da misurare solo se la riprende.
- **Giro GitHub completo sulla 1.3.55** (run 45463715322, `6d3df80`, letto per intero il 24 nov, anche «da controllare»): 2 rossi, tutti e due già visti. `collaudo_suoni_zoom` V5 in Chromium (picco 0,52 dB in 1 prova su 6, soglia −0,5; sulla 1.3.53 era 0,28) e `collaudo_regola18` Z5 in Firefox 3 → 4. `collaudo_marcatura` verde. «Da controllare»: `collaudo_registrazione` E2 +11,2% e `collaudo_riquadro_bandiere` Q7 10,1% in Chromium (misure di tempo, sulla 1.3.53 +9,7% e 12,2%); lezioni semi 1-100 identiche nei due giri e nei due browser, 3.3, 3.5 e 5.8 già noti (elenco aggiornato); `collaudo_rotta`, `_competizione`, `_fasce` come da riferimento.
- **Giocare il torneo con la 1.3.49 o dopo e mandare le regate** (Ale: ok, 23 nov): servono contatti alla boa per Z7 della regola 18 (segnare col tasto M i momenti alla boa).
- **Chiedere a Lucio** per il finale dell'osservazione 135 e di rileggere la lezione 11 nuova.
- **Copia delle registrazioni sul disco esterno ogni tanto:** `bash tests/copia_su_disco.sh` (ultima il 25 nov).
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
