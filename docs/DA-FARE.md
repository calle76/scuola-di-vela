# Cose da fare

**L'ordine lo decide Ale.** Una riga per voce; il dettaglio sta nella proposta o nell'osservazione indicata, e, per gli stati lunghi di prima del 17 novembre, in `archivio/DA-FARE-lunga-17nov.md`. Quando una voce è fatta si toglie (resta nel `CHANGELOG.md`; le chiuse sono in `archivio/DA-FARE-archivio-17nov.md`). Stato generale: `STATO.md`.

**Regola di Ale (22 nov): in ordine di ciò che costerà meno lavoro dopo** (prima ciò su cui si tarano le altre voci). **Ordine di oggi:** 81 bolina con poco vento (la barca, prima di tutto) → avversari 4B (x4 misurata il 23 nov: da rivedere a fine giro; la 3 è chiusa), 2 (usano la barca; la 2 aspetta registrazioni di Ale e Lucio sulla fisica completa, decisione del 10 nov: forse già bastano) → 74 storico dei rivali (comportamento dei rivali) → 49 regola 18 (fatta la versione A; resta B, rivali che danno spazio) → Coach: 69, 66 → medaglie e tempi per ultimi (7).

**Regola di Ale (17 nov):** i «via» alle correzioni grosse si danno **tutti insieme quando i crediti sono ripristinati**, con questa lista. Con pochi crediti: solo testi, collaudi, proposte. Dal 9 novembre: le voci sugli avversari si misurano sulle regate del torneo; la Scuola basta che non peggiori (`DECISIONI.md`).

**Modello consigliato** (colonna «Mod.»): **Opus** per motore, guida dei rivali, fisica e cause da cercare; **Sonnet** per testi, collaudi, proposte e correzioni piccole.

## 1. Con il via, rimandate ai crediti

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 49 | **Regola 18 (spazio alla boa) dentro Deriva:** versione A fatta nella 1.3.49 (colpa, semaforo, zona disegnata, lezione 25). **Versione B (rivali che danno spazio): proposta e misura fatte il 24 nov, consiglio «non ora»** (7 momenti utili in 90 regate), si decide con Z7 (`PROPOSTA-REGOLA-18-B.md`). Z7: rifare `conta_boa_zona.py` sulle prime regate di Ale e Lucio con la 18 | `PROPOSTA-REGOLA-18.md` | Opus |
| 4B | **Rivali che virano e orzano addosso (versione B), variante x4:** confermata il 23 nov su semi nuovi (corte 2601-2660, lunghe 2701-2760, lunghe anche in Firefox): passa M1, M4, fuori linea, non arrivati; **M3 contatti in tutto no** (+3,5% corte, +6% lunghe in Firefox; passa solo in Chromium sulle lunghe). Non adottata: **da rivedere a fine giro** | `PROPOSTA-COPPIE.md` §15; patch in `sperimentale/coppie-4b-3/` | Opus |

## 2. Proposte scritte o da scrivere: aspettano il via

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 81 | **Bolina e virata con poco vento** (riaperto il limite noto del 17 ott; Ale, 23 nov: «sì ok»): con 3-9 nodi la barca è 12-16% più lenta delle fonti (Day, Binns, F109) e la virata costa 3-4 volte la vera. Fermata 1 fatta (23 nov): vento in quota escluso, «flat» non c’entra; un braccio sbandante più lungo raddrizza la forma (sventa a 9 nodi come Day) ma resta −3/−9%, virata −10% (soglia −30%), e col braccio ricavato dai disegni della classe (3,0-3,15 m, 25 nov) col poco vento non cambia. **25 nov, tesi F121: manca spinta della vela perché la rampa 22-29° taglia la portanza; con vela 0,27, braccio 3,0 e rampa più bassa passano B4 e B6, gli altri no. Proposta scritta (`PROPOSTA-VELA-E-RAMPA-81.md`): passano 2 criteri su 8, aspetta Ale**. **Va prima dei rivali** (si tarano sulla barca) | `PROPOSTA-BOLINA-POCO-VENTO.md` | Opus |
| 66 | **Dopo le regate lunghe (1.3.26):** (a) fatto nella 1.3.27 (passo 1,5 s: 2,3-2,7 s; «in assoluto» ancora 9-10 s); (b) file «intera» di circa 2 MB (i pezzi restano sotto 1 MB): righe a 10 al secondo: Ale, 21 nov, «lasciali così»; (c) **fatto per torneo, stagione, regole 15-16, Coach, finale e Deriva superata** (flag `--lungo`, 21 nov, numeri in `COLLAUDI.md`); (+ `layline --lungo` il 21 nov: 12 casi su 12 e P2 OK; `distacchi_testo` e `penalita_testo --lungo` il 24 nov: 3762 righe, 0 a capo, e 75 barche con penalità, OK); gli altri non dipendono dalla lunghezza: **(c) chiusa**; `avversari_deriva` e `cambia_vento` costruiscono scene dirette (non il torneo) e non dipendono dalla lunghezza; (d) raffiche: in raffica la barca guadagna solo +0,2/+0,6 nodi; (e) rotta «in assoluto» 9-10 s nelle regate lunghe: provate le 7 prove col passo 2 s (21 nov), solo −19% di tempo, punto della linea diverso in 6 regate su 6 e rotta fino a +3,7%: annullato | `PROPOSTA-PERCORSO-LUNGO.md` §Esito | Opus |
| 69 | **Più espressioni del Coach** (Ale, 20 nov): oggi i volti sono pochi (serio, contento, arrabbiato). Quali espressioni nuove e quando compaiono si decide con Ale; le immagini le fa lui (come per la voce 58), poi si aggancia ai commenti già esistenti. Proposta scritta | `PROPOSTA-COACH-ESPRESSIONI.md` | Sonnet |
| 74 | **Storico dei rivali:** passo 1 (1.3.37), frase del Coach (1.3.38) e **marcatura nell'ultima regata (1.3.50)** fatti; niente nemesi né cautela senza fonte. Marcatura: K3 non misurato, K4 no (2 contatti con colpa nei corti); **Ale la tiene (24 nov)**; prova vera sulle vostre regate. Punti aperti: contatore, riga a fine torneo, scuffie/penalità, amico in rete | `PROPOSTA-MARCATURA.md` §Esito; `PROPOSTA-STORICO-RIVALI.md` | Opus |
| 82 | **Rivali che crescono, finale con albo d'oro** (idea di Ale, 24 nov): bravura 0-100 per ogni barca, nazionale rifatto ogni anno (9 + primi 3 dello zonale, scelta A del 24 nov), vale per tutti i livelli; registra la base della 56. Albo fatto nella 1.3.54. **Misurata e simulata la notte del 24 nov, gioco invariato: G2 a metà scala, G2b in conferma, S4, S5 e S6 non passano. Aspetta due scelte di Ale (scala e ricambio) e il via** | `PROPOSTA-RIVALI-CHE-CRESCONO.md` | Opus |
| 2 | **Avversari tutti insieme:** bolina e avvicinamento alla boa, uscire dal vento sporco, casi 81 e 83 di Deriva. Aspetta registrazioni di Ale e Lucio sulla fisica completa (`DECISIONI.md`, 10 nov); dall’11 al 21 nov ce ne sono 37, da guardare se bastano | `PROPOSTA-CONO-D-OMBRA.md`; `PROPOSTA-AVVERSARI-BOLINA.md` §14 | Opus |

## 3. Da guardare (collaudi e difetti senza causa nota)

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 35 | **Messaggio «Contatto» coperto da un altro** (`collaudo_registro` in Firefox su GitHub). Se compaiono le note del collaudo, dare priorità ai messaggi delle penalità | `CHANGELOG.md` 1.3.8 | Sonnet |
| 22 | **«Errore interno … property "t" of undefined» in Firefox** (Lucio, 11 nov): non si riproduce; serve una nuova comparsa | `CHANGELOG.md` 1.2.28 | — |
| 8, 18 | **Suoni:** boa poco forte e sartiame in `collaudo_suoni_si_sentono` (il bordo si sposta fra un giro e l'altro). **Sartiame giudicato a orecchio da Ale il 23 nov: resta l'originale** (`DECISIONI.md`); dal 24 nov il collaudo la soglia la riporta e basta. Resta la boa | `CHANGELOG.md` 1.2.12 | Sonnet |

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

- Voci chiuse: `archivio/DA-FARE-archivio-17nov.md` (3 il 23 nov, 23, 24, 25, 26, 28, 29, 30, 32, 33, 34, 36 «Tornei online», 37, 38, 52 e le ferme 1, 11, 13, 20).
- Voci fatte il 17 nov e tolte da qui nel riordino: **45** (T2b su GitHub, voci a frammento), **51** (1.3.20), **60** (1.3.22). Altre voci fatte: 9 prima parte (1.3.21).
- Testo intero com'era prima: `archivio/DA-FARE-lunga-17nov.md`.
