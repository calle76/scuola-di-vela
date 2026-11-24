# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola. **A fine lavoro si SOSTITUISCE «Dove siamo», non si aggiunge sopra** (la storia sta in `CHANGELOG.md` e in `archivio/STATO-storico-novembre.md`). Le cose da fare sono in `DA-FARE.md`.

*Aggiornato: 25 novembre 2026 (gioco alla **1.3.55**, tag `v1.3.55`; rivali a scelta nell'Allenamento).*

## Dove siamo

- **Regola Ale (23 nov): si fa il giro di tutta `DA-FARE.md`, poi si guarda cosa resta.** Chi non passa di poco si annota e si va avanti.
- **1.3.55 (voce 83, via di Ale):** nell'Allenamento si scelgono i rivali fra i 20; A7 nuovo verde in Chromium e Firefox, senza scelte identico alla 1.3.54.
- **Difetti dei collaudi corretti (24 nov, gioco invariato):** `collaudo_marcatura` K2 e `collaudo_storico_rivali` R3, stessa causa (fotogrammi disegnati fra due `evaluate` consumano numeri a caso). R3 ora vale anche in Firefox: 20 su 20 con e senza attesa; con la marcatura accesa è rosso (19 su 20), come deve. Casi noti delle lezioni (3.3, 3.5) aggiunti a `lancia_tutti.sh`: stessi numeri in ogni giro dall'8 nov.
- **Voce 82, rivali che crescono (proposta riscritta, scelta A di Ale, misurata la notte del 24 nov; `js/` non toccato):** il numero in acqua si sente (4,6% e 5,5% del tempo da 0 a 100) **ma quasi tutto fra 0 e 50**; G2 a metà scala (94%) e G2b in conferma (0-100 sotto 0-50) non passano. Simulazione, 300 mondi: circuiti giusti, titoli 15%, ritorno dei rivali e distanze passano; **S4 alla 10 e alla 30, S5 (46% su 50) e S6 (56 su 55) no**; tre varianti non bastano. `PROPOSTA-RIVALI-CHE-CRESCONO.md`, ultima parte. La scala si stira dopo la 81 e le voci 4B e 2 (proposta del 25 nov: dipende dalla barca). **Aspetta Ale: ordine e scala; ricambio (chi smette, nomi nuovi) o no; i 3 nomi; poi il via.**
- **1.3.54 (voce 82, tappa 2, via di Ale):** albo d'oro e campione in carica della finale; la registrazione scrive il livello vero della regata (prima quello del menu): il «principianti» delle 8 regate lunghe della voce 2 resta da verificare. Il resto della voce 82 è nel punto sopra.
- **1.3.53 (voci 41 e 6, via di Ale il 24 nov):** il ritiro si salva anche chiudendo la scheda di colpo; regate lunghe in Firefox da 0-4 su 20 a 20 su 20. `collaudo_ritiro_provvisorio.py` (nuovo) verde in Chromium e Firefox.
- **1.3.52 (voce 42):** il Coach non conta due volte la scuffia e non conta quella prima del via (6 frasi su 8 nelle registrazioni); `collaudo_coach` K14 verde in Chromium, Firefox e regate lunghe.
- **1.3.51 (voce 36, allenamento):** in Deriva una regata singola come quelle del torneo, con scelta di percorso, penalità, barche, rivali; le regate dei salti e dei giri escono dal menu. A1 40 su 40 identiche al torneo, A2 16 su 16, A4-A5 OK. **Idea di Ale (24 nov): chiedere a lui e Lucio regate «su misura»** con questo riquadro: per Z7 triangolo, 6 barche, giri; per la voce 2 bastone, 4 barche, esperti.
- **1.3.50 (voce 74, marcatura, via di Ale a tutti i livelli):** nell'ultima regata del torneo il rivale a cui il duello con te decide la classifica ti marca di bolina (vira quando viri tu, da davanti e a meno di 42 m); riga nel testo della regata, Coach a −100 s, righe `marca` nel file. `collaudo_marcatura.py` su 80 tornei: K1, K2, K5-K9 passano; **K3 non misurato** (15 regate utili su 20; 94% contro 57%), **K4 no** (2 contatti con colpa del marcatore nei corti: uno identico senza marcatura, l'altro dalla virata normale alla layline). Il pilota sta vicino al marcatore pochi secondi: la prova vera sono le vostre ultime regate. **Ale la tiene (24 nov).** Voce 71 (uscita lenta) chiusa da Ale: si lascia com'è.
- **Giro GitHub del 24 nov notte (run 45298592556, completo sulla 1.3.50 e `f37f21d`), letto per intero:** 240 voci OK, 3 rosse. `collaudo_storico_rivali` R3 (nuova, Chromium): 18 su 20, perché la marcatura cambia apposta le ultime regate; marcatura spenta 20 su 20: collaudo corretto. `collaudo_regola18` Z5 in Firefox 3 → 4 (+33%, soglia +30%): identico al giro prima. `collaudo_suoni_si_sentono` sartiame in Chromium: noto (voce 18). `collaudo_torneo` C11 in Firefox: 1 torneo su 40 (voce 41). `collaudo_esame_nuove` di nuovo verde.
- **Esploratore del 23 nov (run 45166551760, sulla 1.3.46):** 0 eccezioni, 0 numeri non finiti, 0 errori; barche non arrivate 52 in 1440 corse (Chromium) e 39 in 1600 (Firefox), il giro prima (1.3.11, altri semi) 45 e 42 in 1600. «Annullato» solo perché in un pezzo su 20 (Chromium semi 71-80) l'installazione del browser è rimasta ferma 2 ore: guasto di GitHub, semi non misurati.
- **1.3.49 (voce 49, versione A):** regola 18 nelle regate di Deriva (zona di 12,6 m, chi entra per primo, esterna/interna, 18.1(a), 18.3 semplificata, 43.1(b)); semaforo, zona disegnata (casella nelle Impostazioni), lezione 25 «Spazio alla boa», righe `zona`/`zona_fine` nel file. Libretto di Deriva: Conoscenza 10, Esperienza 7, quota 25 (approvata da Ale il 23 nov). `collaudo_regola18.py`: 13 casi su 13, Scuola identica; nelle regate corte 0 colpe diverse fuori dalla zona e 1-2 contatti decisi dalla 18; **nelle lunghe nessun contatto alla boa col pilota (Z4 non passa)**: la prova vera è Z7, sulle vostre regate. Resta la versione B (rivali che danno spazio).
- **Voce 3 chiusa** (Ale). **Voce 4B, variante x4, confermata su semi nuovi:** passa M1, M4, fuori linea, non arrivati; **M3 (contatti in tutto) no** nelle corte (+3,5%) e nelle lunghe in Firefox (+6%). Non adottata, da rivedere a fine giro (`PROPOSTA-COPPIE.md` §15).
- **Voce 81 (bolina e virata con poco vento), fermata 1 fatta:** vento in quota escluso, «flat» non c'entra; un braccio sbandante (`zCE`) più lungo fa sventare a 9 nodi come Day, ma la barca resta −3/−9% e la virata −10% (soglia −30%); `zCE` senza fonte. **Non passa, motore invariato, da rivedere a fine giro** (`PROPOSTA-BOLINA-POCO-VENTO.md`, `sperimentale/bolina-81/`). **25 nov:** braccio 3,0 m con fonte (tesi F121); l'acqua del gioco va bene, manca la spinta della vela perché la rampa 22-29° (senza fonte) taglia la portanza col poco vento. Con vela 0,27, braccio 3,0, rampa 15° e boma 5° passano la virata (B6, −34%) e i 15 nodi, il poco vento migliora ma B1, B2, B3, B5 (di 0,6 punti), B7 no. **Fermata 1 scritta:** `PROPOSTA-VELA-E-RAMPA-81.md` (rampa 15, vela 0,27, braccio 2,4): scarto col poco vento circa dimezzato, 12 e 15 nodi come oggi, 2 criteri vecchi su 8, raffiche più dure. Svergolamento (Day) provato il 25 nov sul banco: non risolve. Rampa 15 da sola: virata col poco vento −37% (passa), raffiche e 12-15 nodi invariati, ma a 11 nodi la virata si allontana da F109; con la rollata (tasto X, voce 73) B1 passa. **Aspetta Ale (consiglio: limite noto).** Resta non guardato l'abbrivio nella prima metà della virata (vera +1,48 m, gioco +0,28, con la variante R +0,46).
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
- Domande risposte, via non dato: aiuto «scarso/buono» (48).

## Prossimi passi (giro della lista)

1. Il giro è quasi finito: la 69 aspetta le immagini di Ale, la 49 B le regate alla boa (`PROPOSTA-REGOLA-18-B.md`: consiglio «non ora», 7 momenti utili in 90 regate), la 7 i suoi tempi. Poi **rivedere quello che è rimasto**: 4B, 81, 2.

## Cosa aspetta Ale

- **Giro GitHub completo sulla 1.3.55** (run 45463715322, `6d3df80`, letto per intero il 24 nov, anche «da controllare»): 2 rossi, tutti e due già visti. `collaudo_suoni_zoom` V5 in Chromium (picco 0,52 dB in 1 prova su 6, soglia −0,5; sulla 1.3.53 era 0,28) e `collaudo_regola18` Z5 in Firefox 3 → 4. `collaudo_marcatura` verde. «Da controllare»: `collaudo_registrazione` E2 +11,2% e `collaudo_riquadro_bandiere` Q7 10,1% in Chromium (misure di tempo, sulla 1.3.53 +9,7% e 12,2%); lezioni semi 1-100 identiche nei due giri e nei due browser, 3.3, 3.5 e 5.8 già noti (elenco aggiornato); `collaudo_rotta`, `_competizione`, `_fasce` come da riferimento.
- **Giocare il torneo con la 1.3.49 o dopo e mandare le regate** (Ale: ok, 23 nov): servono contatti alla boa per Z7 della regola 18 (segnare col tasto M i momenti alla boa).
- **Chiedere a Lucio** per il finale dell'osservazione 135 e di rileggere la lezione 11 nuova.
- **Copia delle registrazioni sul disco esterno ogni tanto:** `bash tests/copia_su_disco.sh` (ultima il 17 nov).
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
