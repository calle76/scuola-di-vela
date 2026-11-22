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

## 2. Proposte scritte o da scrivere: aspettano il via

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 73 | **PRIMA DI TUTTO (Ale, 22 nov: «prima la barca e poi il resto»): correggere la barca secondo lo studio** (`STUDIO-BARCA.md`): virata rollata con poco vento (0,7 lunghezze contro 0), vento forte sopra 16-18 nodi (la virata non riesce con la regola della scotta), bolina lenta con poco vento (−20% a 6 nodi, causa da cercare). Fermata 1: proposta con obiettivi dichiarati; metro prima/dopo `tests/fisica/studio_barca.js`. Sessione nuova | `STUDIO-BARCA.md` | Opus |
| 79 | **Dopo la 73: rifare la lezione 11 (salti di vento)** (Ale, 22 nov: «non ho capito le basi»; nella sua regata ha virato su uno scarso persistente, 84 m persi): passo «due venti diversi» (come si riconoscono dal numero), esercizio nuovo «vai verso il salto» col vento persistente e la layline, riga scarso/buono negli esercizi, 3 domande nuove. Prima una seconda fonte | `PROPOSTA-LEZIONE-11.md` | Opus |
| 78 | **Raffiche del gioco contro misure vere (NOAA, F105):** fatta la misura (22 nov): tipiche come in mare, le rare un po' troppo forti (99° 1,40-1,59 contro 1,27-1,49; il lago Erie 1,85). Correzione possibile (solo raffiche sommate) da proporre col via | `PROPOSTA-RAFFICHE-VERE.md` | Opus |
| 66 | **Dopo le regate lunghe (1.3.26):** (a) fatto nella 1.3.27 (passo 1,5 s: 2,3-2,7 s; «in assoluto» ancora 9-10 s); (b) file «intera» di circa 2 MB (i pezzi restano sotto 1 MB): righe a 10 al secondo: Ale, 21 nov, «lasciali così»; (c) **fatto per torneo, stagione, regole 15-16, Coach, finale e Deriva superata** (flag `--lungo`, 21 nov, numeri in `COLLAUDI.md`); (+ `layline --lungo` il 21 nov: 12 casi su 12 e P2 OK); `avversari_deriva` e `cambia_vento` costruiscono scene dirette (non il torneo) e non dipendono dalla lunghezza; restano gli altri collaudi che usano il torneo o le regate di Deriva, uno per volta (da elencare: finale, sponsor, carriera intera, guardiano avversari, Deriva superata…); (d) raffiche: in raffica la barca guadagna solo +0,2/+0,6 nodi; (e) rotta «in assoluto» 9-10 s nelle regate lunghe: provate le 7 prove col passo 2 s (21 nov), solo −19% di tempo, punto della linea diverso in 6 regate su 6 e rotta fino a +3,7%: annullato | `PROPOSTA-PERCORSO-LUNGO.md` §Esito | Opus |
| 69 | **Più espressioni del Coach** (Ale, 20 nov): oggi i volti sono pochi (serio, contento, arrabbiato). Quali espressioni nuove e quando compaiono si decide con Ale; le immagini le fa lui (come per la voce 58), poi si aggancia ai commenti già esistenti. Proposta scritta | `PROPOSTA-COACH-ESPRESSIONI.md` | Sonnet |
| 74 | **Storico dei rivali: passo 1 (1.3.37) e frase del Coach (2a, 1.3.38) fatti; resta la decisione 2** (cautela «l'ho toccato io, mi schiva» o nemesi «ha perso da me, mi ostacola», versione a parte, prima le fonti); punti aperti: contatore di versione, riga a fine torneo, scuffie e penalità, amico in rete | `PROPOSTA-STORICO-RIVALI.md` | Opus |
| 71 | **Uscita da una regata lunga del torneo: la pagina resta ferma 3-6 s** (misurato il 21 nov col C11 `--lungo`: R7 6,33 s al massimo contro 2 s; nelle regate corte 2,7 s). Causa letta nel codice: `torChiudi` (`js/regate.js`) simula di colpo, in un ciclo solo, tutto il resto della regata dei rivali (fino a 1800 s). Da decidere: simulare a pezzi fra un fotogramma e l'altro, o accorciare il resto; **non** cambiare il passo (cambierebbe gli arrivi). Il C11 intero in lungo non è nella suite finché non si decide. Proposta scritta (21 nov); prima Ale dice se il ritardo si sente | `PROPOSTA-USCITA-REGATA-LUNGA.md` | Opus |
| 55 | **Registrazioni più ricche:** stato del semaforo, registrazione dopo il proprio arrivo, chi ha la precedenza, contatti con colpa. Soglia di peso del file da dichiarare | oss. 135-136 | Sonnet |
| 42 | **Coach, terza mano:** la finestra di «altre barche» può contenere una scuffia e la perdita è detta due volte | `PROPOSTA-COACH-2.md` §8; oss. 131 | Opus per la proposta |
| 9 | **Verificare su fonti i 45° prima della strambata e la posizione dei filetti** (seconda parte della voce; le scelte dichiarate sono nella 1.3.21) | `CONTENUTI-DA-VERIFICARE.md` | Sonnet |
| 2 | **Avversari tutti insieme:** bolina e avvicinamento alla boa, uscire dal vento sporco, casi 81 e 83 di Deriva. Aspettano registrazioni di Lucio | `PROPOSTA-CONO-D-OMBRA.md`; `PROPOSTA-AVVERSARI-BOLINA.md` §14 | Opus |
| 3 | **Barche affiancate che si tengono** («chi si libera resta libero»), insieme alla 4B | `PROPOSTA-COPPIE.md` §12-13 | Opus |

## 3. Da guardare (collaudi e difetti senza causa nota)

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 41, 6 | **`collaudo_torneo` C11 in Firefox:** 4 tornei su 40 chiusi a metà non risultano conclusi (1 su 40 nel giro prima); forse è il ritiro che non si salva alla chiusura. Da rifare sul PC, una misura per volta col freno | oss. 86; `COLLAUDI.md` | Opus |
| 35 | **Messaggio «Contatto» coperto da un altro** (`collaudo_registro` in Firefox su GitHub). Se compaiono le note del collaudo, dare priorità ai messaggi delle penalità | `CHANGELOG.md` 1.3.8 | Sonnet |
| 22 | **«Errore interno … property "t" of undefined» in Firefox** (Lucio, 11 nov): non si riproduce; serve una nuova comparsa | `CHANGELOG.md` 1.2.28 | — |
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
