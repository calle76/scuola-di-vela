# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola. **A fine lavoro si SOSTITUISCE «Dove siamo», non si aggiunge sopra** (la storia sta in `CHANGELOG.md` e in `archivio/STATO-storico-novembre.md`). Le cose da fare sono in `DA-FARE.md`.

*Aggiornato: 22 novembre 2026, sera (gioco alla **1.3.39**, tag `v1.3.39`).*

## Dove siamo

- **Pomeriggio del 21 nov (via di Ale alle voci 68 e 70):** **1.3.32** (voce 68: il commento del Coach resta 8-14 s in proporzione alla frase, i forzati non lo tagliano prima di 4 s; D1 60 e 57 commenti, D2 48 e 45 coppie, D2b diretta OK, P4 uguale al bit, Chromium e Firefox) e **1.3.33** (voce 70: un solo interruttore Suoni acceso/spento a 0,6; onde e gabbiani calano con lo zoom fino a 0,35 a zoom 0,1; `collaudo_suoni_zoom.py` V1, V5-V9 e grafo audio OK in Chromium, V1/V7-V9 OK in Firefox). A zoom 100% i suoni sono ~8,7 dB più forti del vecchio «basso»: da sentire. **Riserva:** `collaudo_suoni_si_sentono` sul PC dà fallimenti sparsi (sartiame/boa già noti, voci 8/18; prove a 0 dB con le pause del freno; un giro a 74 °C, sopra il mio limite di 72); sulla 1.3.32 passa con 0 pause. Da vedere sul giro di GitHub.
- **1.3.34 (richieste di Ale dopo la prova a orecchio):** allontanando lo zoom cala **tutto**, tranne i segnali (tromba, contatto, boa, arrivo); e un **campanello leggerissimo** quando compare il Coach (sintetico, 1760/2637 Hz, volumi 0,09 e 0,045: da giudicare a orecchio). Grafo audio esatto OK, C2 picco 9,7 dB sotto la tromba, C3 +6,9 dB (mediana), C1 un campanello per ognuno dei 60 commenti; Chromium e Firefox.
- **1.3.35 (voce 67):** bandiere del via nel torneo, nella stagione e nella finale (classe −180 s, P −120 s, X, blu), con i messaggi delle bandiere al posto di quelli di testo; il codice c'era già, serviva `segnali: true`. `collaudo_segnali_deriva.py` B1-B7 OK (9.251 letture, la X 3+3, arrivi identici), `collaudo_orologio_giri` O9 aggiornato. **Proposte nuove (senza codice, aspettano il via):** voce 72 (freccia dell'obiettivo più visibile) e voce 74 (storico dei rivali).
- **1.3.36 (voce 72, via di Ale):** freccia dell'obiettivo da 22 a 34 px con contorno, nome («Linea», «Boa 1», «Arrivo») e pulsazione oltre 150 m, che evita i riquadri; `collaudo_freccia.py` F1-F7 OK in Chromium e Firefox (46 casi dei nomi, 32 della non-sovrapposizione con controprova, 8 regate identiche al bit). 
- **1.3.37 (voce 74, passo 1, via di Ale; fatto da Sonnet e rivisto da Opus prima del commit):** lo storico dei rivali con nome, solo mostrato nella scheda («Storico, N regate insieme…»), dentro `progress.rivali[nome].st`; la regata non cambia (20 su 20 identiche al bit). `collaudo_storico_rivali.py` R1-R6 OK (855 + 600 confronti, 0 diversi). **Passo 2 (le conseguenze) aspetta il via di Ale e va a Opus.**
- **1.3.38 (voce 74, passo 2 a, via di Ale del 22 nov):** il Coach, a 150 s dal via, nomina il rivale che ti ha toccato con colpa sua in almeno 2 regate (uno solo; la guida non cambia). `collaudo_storico_frase.py` OK in Chromium e Firefox: 0 frasi sbagliate su 232 regate (110 con, 122 senza), 20 regate identiche al bit con e senza frase (Chromium). Corretto insieme: la frase dello sponsor non si perde più se il Coach è in pausa. **Prossima decisione (2):** cautela («l'ho toccato io, mi schiva») o nemesi («ha perso da me, mi ostacola»), versione a parte, prima le fonti.
- **1.3.39 e segnalazioni di Lucio e Ale (22 nov):** corretto il riquadro «Raddrizza» rimasto sul resoconto dopo una scuffia sulla linea d'arrivo (`collaudo_scuffia_arrivo.py` OK in Chromium e Firefox; sulla 1.3.38 A1 0 su 10). **Tre proposte nuove che aspettano il via:** 75 scuffia appena dopo «Parti» (vento al via 1,6-1,9 volte la media in 40 semi su 40: causa trovata in `setGusts`), 76 campo e boa prima del via, 77 verifica del consiglio «scarso» del Coach (prima misura: 11 su 14 sensati). Registrazioni del 17-21 nov spostate in `registrazioni/` (79 regate).
- **Giro su GitHub del 22 nov (run 44980038984, sul commit 2008a6e = 1.3.37 coi collaudi corretti):** vista, Q6b e B6 ora verdi. Rossi: H4 «boa» (noto, voci 8/18) e, nuovo, `collaudo_registro` caso «contatto» solo in Chromium (in 180 s veri il pilota del collaudo non ha toccato nessuno; caso a tempo reale già caduto in passato; Firefox 15 su 15): da riguardare al prossimo giro, nessun difetto del gioco.
- **Voce 73 chiusa:** le virate del pilota sono identiche fra 1.3.25 e oggi (37 virate, minimo 47%, recupero 5,8 s; il motore non cambia dalla 1.1.0); in regata lunga 149 virate, minimo 48%, 39 scuffie in 20 regate (raffiche a zone, 1.3.26). Voci nuove: 72 (freccia dell'arrivo più visibile, no zoom più largo), 56 resta in coda (curva dei progressi); lo «storico duraturo dei rivali con conseguenze» è un'idea di Ale da proporre (Opus, sessione nuova).
- **Regate di Lucio (21 nov):** nel repo ci sono la 1 e la 3 del torneo (4° e 4°); la 2, che ha vinto, manca. Lucio dice: con i lati lunghi la vista Q non mostra il campo alla partenza, e la barca gli sembra più difficile (non confermato dalle misure).
- **Il gioco:** Scuola chiusa come contenuti. Deriva nel gioco, non ancora «finita»: lezioni 21-25, torneo (3 regate lunghe, circa 10 minuti), stagione, finale, sponsor, regole 15 e 16, cono d'ombra, raffiche come zone, rotta ottimale, Coach nella moviola e durante la regata. Com'è fatto: `IL-GIOCO.md`. Ultime versioni: 1.3.26 regate lunghe, 1.3.28 Coach in regata, 1.3.29 triangolo da 440 m, 1.3.30-1.3.31 lezione 11 e frase del Coach (`CHANGELOG.md`).
- **Giro completo su GitHub (run 44804439764, sulla 1.3.31, Chromium e Firefox):** 5 pezzi su 8 rossi, ma **nessun difetto del gioco**: i fallimenti erano dei collaudi o già noti.
  - **Nuovi, già corretti nei collaudi:** `orologio_giri` e `riquadro_bandiere` in Chromium («canvas contaminata»: dalla 1.3.28 la foto del Coach da file impedisce di leggere i pixel; riprodotto sul PC; ora spengono il Coach); `torneo --giocatore` (C7) in tutti e due i browser (aspettava 4 regate, dalla 1.3.26 sono 3); `coach (regate lunghe)` in tutti e due (cadeva quando la rotta ottimale non compare: ora conta il caso, K0, al più 2 su 20).
  - **Non nuovi:** `suoni_si_sentono` sartiame in Chromium (2,0 contro «almeno 2»: già visto il 20 nov mattina, voci 8 e 18); T2b, E2, Q7, partenze, virate2, avversari_deriva come in `fallimenti_noti.txt`; `competizione`, `rotta`, `fasce`, `pilota_lezioni` da controllare come prima.
  - **Da rivedere al prossimo giro:** `percorso_lungo` P4 in Firefox (bolina in raffica 42% contro soglia 40%); sul PC non si riproduce (29% Firefox, 32% Chromium). Soglia non cambiata.
  - I rossi del giro del 20 nov mattina (`sponsor`, `deriva_superata`) ora sono verdi.
- **Voce 66(c) fatta** per torneo, stagione, regole 15-16, Coach, finale e Deriva superata (flag `--lungo`; numeri in `COLLAUDI.md`): tutto passa tranne **C11 R7, l'uscita dal menu in 3-6 s** nelle regate lunghe (soglia 2 s): causa in `torChiudi`, voce **71** (proposta scritta; C11 non gira nel torneo veloce lungo). Mancano ancora, uno per volta: sponsor, carriera intera, avversari_deriva, moviola, rotta_assoluta, layline, cambia_vento, cono.
- **Notte del 21 nov (Ale assente): la differenza GitHub/PC era dei collaudi, non del gioco.** `tests/impronta_macchina.py` mostra che la regata da sola è identica al bit su PC e GitHub (Chromium e Firefox, tutta la regata). Causa: apertura e corsa in due `evaluate` (il ciclo della pagina consuma i numeri a caso del seme) e più regate nella stessa pagina (lo stato resta). Corretti: `percorso_lungo` (P2 e P4 in pagina nuova: bastone 32%, triangolo 36% Chromium; 32%/28% Firefox), `coach --lungo` (K0 0/20 Chromium, 1/20 Firefox), `triangolo` (T2b a 3 s dal giro, voce 53 chiusa: 160/170 Chromium, 161/166 Firefox, ripetibile). **Voce 40 chiusa**: il pulsante «Rotta ottimale» manca solo se il giocatore non è arrivato. Tutto da confermare con un giro su GitHub (i numeri devono uscire come sul PC).
- **Proposte (fermata 1, senza codice):** 67 (bandiere del via in tutte le regate coi 3 minuti: da riscrivere sulla lettura chiarita da Ale il 21 nov), 68 (suggerimento del Coach più a lungo), 69 (più espressioni), 70 (`PROPOSTA-VOLUME-ZOOM.md`), 71 (`PROPOSTA-USCITA-REGATA-LUNGA.md`: prima Ale dice se il ritardo si sente).
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
