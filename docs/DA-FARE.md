# Cose da fare

**L'ordine lo decide Ale.** Una riga per voce; il dettaglio sta nella proposta o nell'osservazione indicata, e, per gli stati lunghi di prima del 17 novembre, in `archivio/DA-FARE-lunga-17nov.md`. Quando una voce è fatta si toglie (resta nel `CHANGELOG.md`; le chiuse sono in `archivio/DA-FARE-archivio-17nov.md`). Stato generale: `STATO.md`.

**Regola di Ale (17 nov):** i «via» alle correzioni grosse si danno **tutti insieme quando i crediti sono ripristinati**, con questa lista. Con pochi crediti: solo testi, collaudi, proposte. Dal 9 novembre: le voci sugli avversari si misurano sulle regate del torneo; la Scuola basta che non peggiori (`DECISIONI.md`).

**Modello consigliato** (colonna «Mod.»): **Opus** per motore, guida dei rivali, fisica e cause da cercare; **Sonnet** per testi, collaudi, proposte e correzioni piccole.

## 1. Con il via, rimandate ai crediti

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 49 | **Regola 18 (spazio alla boa) dentro Deriva:** lezione, regola per il giocatore come la 15-16 (zona disegnata, ingaggio, colpa, semaforo), poi rivali che danno e prendono spazio. Tocca circa 9 contatti su 52 | `PROPOSTA-REGOLA-18.md` | Opus |
| 36 | **Allenamento** al posto delle due regate di Deriva: una regata singola come quelle del torneo, con scelta di percorso, penalità, barche e livello | `PROPOSTA-ALLENAMENTO.md` | Sonnet (Opus per la regata singola) |
| 4B | **Rivali che virano e orzano addosso (versione B, guida dei rivali):** la A (regole 15-16) è nella 1.3.10; la B è scritta ma **spenta** (non passa M1 e M5) | `PROPOSTA-REGOLE-15-16.md` | Opus |
| 48 | **Aiuto «scarso / buono»** in regata: una riga sotto il vento, di bolina col vento che gira, disattivabile. Domande risposte; via al codice non dato | `PROPOSTA-AIUTO-SCARSO.md` | Sonnet |

## 2. Proposte scritte o da scrivere: aspettano il via

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 50 | **Rotta ottimale: giro della boa dal lato sbagliato.** Costa 2-4 s al giocatore in 7 regate su 48, fino a 21 s alle altre barche. Un controllo in `rotLato` | `PROPOSTA-ROTTA-GIRO-BOA.md`; oss. 134 e 137 | Opus |
| 53 | **Distacchi del triangolo (T2b):** il difetto è soprattutto del metro (letto a 10 s). Si cambia il collaudo (lettura a 3 s), non il gioco | `PROPOSTA-DISTACCHI-TRIANGOLO.md` | Sonnet |
| 54 | **«Salva / Carica la mia carriera» in un file** (paura di perdere i dati del browser). Piccola | come «Riprendi dal mio file» (`PROPOSTA-STAGIONE-FILE.md`) | Sonnet |
| 63 | **Regate troppo corte e raffiche non percepite** (Ale, 18 nov): lati da 140 m, 3 minuti, una sola virata, ritorno dritto di poppa; nelle raffiche non si vede differenza di velocità. Idea: lati da 400-500 m (giro 6-8 min), raffiche come zone sull'acqua, controllare nei `regata-*.txt` quanto il vento e la velocità cambiano davvero. Costi: telecamera, ritaratura rivali, record non confrontabili. Prima la proposta | da scrivere (`PROPOSTA-PERCORSO-LUNGO.md`) | Opus |
| 64 | **Entrata in Deriva e attestato** (Ale, 18 nov; sponsor prima rifiutato, ora richiesto): all'arrivo al livello Deriva compaiono lo sponsor e la presentazione del Coach («cosa si fa in questo livello»); un **attestato in un file** che permette di ripartire sempre dall'inizio di Deriva senza rifare la Scuola (Carriera → Deriva → «hai l'attestato?» sì). Serve per provare i grandi cambiamenti. Legata alla 54; l'attestato dice «nessun valore legale» | da scrivere; `PROPOSTA-STAGIONE-FILE.md`, `PROPOSTA-RIVALI-E-SPONSOR.md` | Sonnet |
| 55 | **Registrazioni più ricche:** stato del semaforo, registrazione dopo il proprio arrivo, chi ha la precedenza, contatti con colpa. Soglia di peso del file da dichiarare | oss. 135-136 | Sonnet |
| 57 | **Volto felice del Coach:** oggi non compare mai (0 su 11 nelle regate del 15-17 nov). Riconfermato da Ale il 17 nov: 4 regate in repo (`regata-20261116-*`, `stagione-*.json`), arriva primo e il Coach non sorride. Contento anche con un primo posto, un record o una perdita piccola; altre espressioni da decidere | `js/rotta.js` `coaUmore`; `PROPOSTA-COACH.md` | Sonnet |
| 42 | **Coach, terza mano:** la finestra di «altre barche» può contenere una scuffia e la perdita è detta due volte | `PROPOSTA-COACH-2.md` §8; oss. 131 | Opus per la proposta |
| 9 | **Verificare su fonti i 45° prima della strambata e la posizione dei filetti** (seconda parte della voce; le scelte dichiarate sono nella 1.3.21) | `CONTENUTI-DA-VERIFICARE.md` | Sonnet |
| 2 | **Avversari tutti insieme:** bolina e avvicinamento alla boa, uscire dal vento sporco, casi 81 e 83 di Deriva. Aspettano registrazioni di Lucio | `PROPOSTA-CONO-D-OMBRA.md`; `PROPOSTA-AVVERSARI-BOLINA.md` §14 | Opus |
| 3 | **Barche affiancate che si tengono** («chi si libera resta libero»), insieme alla 4B | `PROPOSTA-COPPIE.md` §12-13 | Opus |

## 3. Da guardare (collaudi e difetti senza causa nota)

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 41, 6 | **`collaudo_torneo` C11 in Firefox:** 4 tornei su 40 chiusi a metà non risultano conclusi (1 su 40 nel giro prima); forse è il ritiro che non si salva alla chiusura. Da rifare sul PC, una misura per volta col freno | oss. 86; `COLLAUDI.md` | Opus |
| 40 | **«Rotta ottimale» non compare in 3 regate su 100** (semi 2415, 2420 di `collaudo_rotta_assoluta.py`); indizio: riaprirla due volte | `PROPOSTA-ROTTA-ASSOLUTA.md` §10 | Opus |
| 35 | **Messaggio «Contatto» coperto da un altro** (`collaudo_registro` in Firefox su GitHub). Se compaiono le note del collaudo, dare priorità ai messaggi delle penalità | `CHANGELOG.md` 1.3.8 | Sonnet |
| 22 | **«Errore interno … property "t" of undefined» in Firefox** (Lucio, 11 nov): non si riproduce; serve una nuova comparsa | `CHANGELOG.md` 1.2.28 | — |
| 61 | **Giri di penalità: manca l'orologio** che invita a farli e li conta (segnalato da Ale il 17 nov, con immagine). Da capire se manca sempre o solo in certi casi (Deriva, torneo, Scuola) | oss. da scrivere; `PROPOSTA-GIRI-GIOCATORE.md` | Opus |
| 62 | **Scuola, ripassi: sbagliando le domande non si attivano le lezioni corrispondenti** (segnalato da Ale il 17 nov) | da cercare in `js/contenuti.js` / `js/gioco.js` | Sonnet |
| 8, 18 | **Suoni:** boa poco forte e sartiame in `collaudo_suoni_si_sentono` (il bordo si sposta fra un giro e l'altro) | `CHANGELOG.md` 1.2.12 | Sonnet |

## 4. In sospeso, in coda o idee

| # | Cosa | Dove |
| --- | --- | --- |
| 56 | **Curva dei progressi** (in coda). «Rifai questo tratto»: nel livello Coach dopo Deriva, non ora | `DECISIONI.md` |
| 59 | **Coach: domande sulle penalità e situazioni da ripetere:** nel livello Coach dopo Deriva | `PROPOSTA-COACH-REGISTRATORE.md` fasi 3-4 |
| 58 | **Un volto per tutti i partecipanti** (rivali, giocatore, amico). Le immagini le fa Ale; prima nelle schede dei rivali e nelle classifiche | `PROPOSTA-SCHEDA-RIVALI.md` |
| 35b | **Storia e conseguenze dei rivali:** storico anche fra rivali, conseguenze sul comportamento, compatibilità per la squadra | `PROPOSTA-RIVALI-E-SPONSOR.md` |
| 39 | **Piano di chiusura di Deriva:** tappe 1-4 fatte (rotta in assoluto, cornice, finale, sponsor); mancano 5 (rivali che regatano meglio: voci 4B, 2, 3), 6 (punti da sistemare) e 7 (uscita) | `PIANO-CHIUSURA-DERIVA.md` |
| 12 | **Livello Deriva** come livello a sé (soglia del torneo, momento clou): da ripensare coi circuiti | `PROPOSTA-LIVELLO-DERIVA.md` §10 |
| 43 | **Pilota «da giocatore»:** resta a parte; una partenza sua senza contatti, quando serve al Coach | `PROPOSTA-PILOTA-GIOCATORE.md` §8-9 |
| 27 | **Lezioni 18-19: stare fermi prima del via** (proposta, in sospeso) | `PROPOSTA-LEZIONE-STARE-FERMI.md` |
| 31 | **Dalle fonti F86-F102:** cono d'ombra in poppa forse troppo lungo; idee per bolina, lezioni e circuiti. Da proporre quando si riprendono le voci 2 e 27 | `FONTI-PUBBLICHE.md` F86-F102 |
| 17 | **Pilota incastrato prima del via nel torneo** (3 casi in 3200 corse): noto, da riprendere | oss. 79 |
| 7 | **Oro della prova 5** (315/395/505 s): aspetta i tempi della prova a mano di Ale | `CHANGELOG.md` 1.2.11-1.2.12 |
| 1b | **Avversari: virate in più vicino alla boa** (circa 1,7 per passaggio): ferma con la bolina | `PROPOSTA-LAYLINE.md` §5 |

## 5. Le fai tu, Ale

| # | Cosa |
| --- | --- |
| 10 | **Giudizio dei suoni** all'ascolto |
| 14 | **Copia di sicurezza fuori da GitHub:** registrazioni copiate il 17 nov sul disco esterno; da ripetere ogni tanto con `bash tests/copia_su_disco.sh` |
| — | **Push** (`git push origin main --tags`), la domanda a Lucio sul finale (oss. 135), le pagine di `racingrulesofsailing.org` in `fonti-pdf/` |

## Archivio

- Voci chiuse: `archivio/DA-FARE-archivio-17nov.md` (23, 24, 25, 26, 28, 29, 30, 32, 33, 34, 36 «Tornei online», 37, 38, 52 e le ferme 1, 11, 13, 20).
- Voci fatte il 17 nov e tolte da qui nel riordino: **45** (T2b su GitHub, voci a frammento), **51** (1.3.20), **60** (1.3.22). Altre voci fatte: 9 prima parte (1.3.21).
- Testo intero com'era prima: `archivio/DA-FARE-lunga-17nov.md`.
