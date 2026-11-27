# Cose da fare

**L'ordine lo decide Ale.** Una riga per voce; il dettaglio sta nella proposta o nell'osservazione indicata, e, per gli stati lunghi di prima del 17 novembre, in `archivio/DA-FARE-lunga-17nov.md`. Quando una voce è fatta si toglie (resta nel `CHANGELOG.md`; le chiuse sono in `archivio/DA-FARE-archivio-17nov.md`). Stato generale: `STATO.md`.

**Regola di Ale (22 nov): in ordine di ciò che costerà meno lavoro dopo** (prima ciò su cui si tarano le altre voci). **Ordine di oggi:** (84 accesa nella 1.3.59, 81 con lei; 4B accesa nella 1.3.56, 3 chiusa) → avversari 2 (usano la barca; la 2 aspetta registrazioni di Ale e Lucio sulla fisica completa, decisione del 10 nov: forse già bastano) → 74 storico dei rivali (comportamento dei rivali) → 49 regola 18 (fatta la versione A; resta B, rivali che danno spazio) → Coach: 69, 66 → medaglie e tempi per ultimi (7).

**Regola di Ale (17 nov):** i «via» alle correzioni grosse si danno **tutti insieme quando i crediti sono ripristinati**, con questa lista. Con pochi crediti: solo testi, collaudi, proposte. Dal 9 novembre: le voci sugli avversari si misurano sulle regate del torneo; la Scuola basta che non peggiori (`DECISIONI.md`).

**Modello consigliato** (colonna «Mod.»): **Opus** per motore, guida dei rivali, fisica e cause da cercare; **Sonnet** per testi, collaudi, proposte e correzioni piccole.

## 1. Con il via, rimandate ai crediti

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 92 | **Collaudi da adattare alla barca M:** fatti nelle 1.3.62-1.3.66 (pannello, Deriva superata, Coach, semaforo, confronti al bit, suggerimento, giri, lezione dei salti, segnali, percorso lungo, competizione «dai tempi», `giri_avversari` a 300 regate). Corretti dopo il giro sulla 1.3.68 (run 45957380469): `registro`, `contatto_vero`. **Restano** (stesso giro): `partenze`, `avversari1b` 5 (Firefox) e `avversari_deriva` 81 (rivali, voce 2), `regola21` K3 in Firefox (intermittente), `moto_mare` in Firefox (seme fisso, 3,8-4,6 px contro 4,4, solo disegno), `giri_avversari` G12 Chromium (1 su 267 sul bordo della soglia) | `CHANGELOG.md` 1.3.62-1.3.66 | Sonnet |
| 49 | **Regola 18 (spazio alla boa) dentro Deriva:** versione A fatta nella 1.3.49 (colpa, semaforo, zona disegnata, lezione 25). **Versione B (rivali che danno spazio): proposta e misura fatte il 24 nov, consiglio «non ora»** (7 momenti utili in 90 regate), si decide con Z7 (`PROPOSTA-REGOLA-18-B.md`). Z7: rifare `conta_boa_zona.py` sulle prime regate di Ale e Lucio con la 18; dalla 1.3.56 (4B accesa) guardare anche i contatti entro 12,6 m dalla boa, col pilota 7 → 13, e `collaudo_avversari1b` scenario 5 (tre rivali alla boa: 9-10 → 7 su 10) | `PROPOSTA-REGOLA-18.md` | Opus |

## 2. Proposte scritte o da scrivere: aspettano il via

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 66 | **Dopo le regate lunghe (1.3.26):** (a) fatto nella 1.3.27 (passo 1,5 s: 2,3-2,7 s; «in assoluto» ancora 9-10 s); (b) file «intera» di circa 2 MB (i pezzi restano sotto 1 MB): righe a 10 al secondo: Ale, 21 nov, «lasciali così»; (c) **fatto per torneo, stagione, regole 15-16, Coach, finale e Deriva superata** (flag `--lungo`, 21 nov, numeri in `COLLAUDI.md`); (+ `layline --lungo` il 21 nov: 12 casi su 12 e P2 OK; `distacchi_testo` e `penalita_testo --lungo` il 24 nov: 3762 righe, 0 a capo, e 75 barche con penalità, OK); gli altri non dipendono dalla lunghezza: **(c) chiusa**; `avversari_deriva` e `cambia_vento` costruiscono scene dirette (non il torneo) e non dipendono dalla lunghezza; (d) raffiche: in raffica la barca guadagna solo +0,2/+0,6 nodi; (e) rotta «in assoluto» 9-10 s nelle regate lunghe: provate le 7 prove col passo 2 s (21 nov), solo −19% di tempo, punto della linea diverso in 6 regate su 6 e rotta fino a +3,7%: annullato | `PROPOSTA-PERCORSO-LUNGO.md` §Esito | Opus |
| 69 | **Più espressioni del Coach** (Ale, 20 nov): oggi i volti sono pochi (serio, contento, arrabbiato). Quali espressioni nuove e quando compaiono si decide con Ale; le immagini le fa lui (come per la voce 58), poi si aggancia ai commenti già esistenti. Proposta scritta | `PROPOSTA-COACH-ESPRESSIONI.md` | Sonnet |
| 74 | **Storico dei rivali:** passo 1 (1.3.37), frase del Coach (1.3.38) e **marcatura nell'ultima regata (1.3.50)** fatti; niente nemesi né cautela senza fonte. Marcatura: K3 non misurato, K4 no (2 contatti con colpa nei corti); **Ale la tiene (24 nov)**; prova vera sulle vostre regate. Punti aperti: riga a fine torneo (l'unico consigliato), contatore, scuffie/penalità, amico in rete | `PROPOSTA-MARCATURA.md` §Esito; `PROPOSTA-STORICO-RIVALI.md` | Opus |
| 82 | **Rivali che crescono, finale con albo d'oro** (idea di Ale, 24 nov): bravura 0-100 per ogni barca, nazionale rifatto ogni anno (9 + primi 3 dello zonale, scelta A del 24 nov), vale per tutti i livelli; registra la base della 56. Albo fatto nella 1.3.54. **Misurata e simulata la notte del 24 nov, gioco invariato: G2 a metà scala, G2b in conferma, S4, S5 e S6 non passano. Aspetta due scelte di Ale (scala e ricambio) e il via** | `PROPOSTA-RIVALI-CHE-CRESCONO.md` | Opus |
| 2 | **Avversari tutti insieme:** avvicinamento alla boa, uscire dal vento sporco, casi 81 e 83 di Deriva. **Parte bolina chiusa (Ale, 27 nov):** contro un timoniere «miope» gli esperti perdono circa 10 s per bolina, i principianti 25-27 (voluto); si riapre solo se nelle regate di Ale e Lucio gli esperti risultano troppo facili da battere di bolina. **Vento sporco chiuso (27 nov).** **Caso 81: passo 1 fatto, via al passo 2** (§13 di `PROPOSTA-AVVERSARI-DERIVA.md`: tempo dell'accostata in `passaggio()`). Restano 81 (6 su 10; provato «chi cede frena»: 0 su 10, scartato, `PROPOSTA-AVVERSARI-DERIVA.md` §12), 83 (PC 10 su 10, GitHub Chromium 7) e il vento sporco | `PROPOSTA-AVVERSARI-BOLINA.md` §17-18 | Opus |
| 88 | **Onde nel motore: ferma** (Ale, 26 nov, dopo il banco: non passano O1, O2, O4 a 15 nodi, O5, O7). Si riprende con una misura vera di una deriva in onda o insieme alle voci 86-87 | `sperimentale/onde-88/BANCO-ONDE.md` §Esito | Opus |
| 87 | **Lezione «andare a S» in poppa** (idea di Ale del 26 nov): lasco, strapoggio, strambata, e quando conviene. Dalla 1.3.68 lo strapoggio c'è (fino a circa 15° oltre la poppa con la vela aperta) ma **non rende più della poppa piena**: il guadagno delle S è non stazionario (F109), il motore non lo dà. La lezione può insegnare a scendere più profondi senza strambare, non a guadagnare velocità | proposta da scrivere | Sonnet |

## 3. Da guardare (collaudi e difetti senza causa nota)

| # | Cosa | Dove | Mod. |
| --- | --- | --- | --- |
| 22 | **«Errore interno … property "t" of undefined» in Firefox** (Lucio, 11 nov): non si riproduce; serve una nuova comparsa. Provato il 25 nov (Firefox 150): fra 74 forme di codice, quel testo esatto esce solo da `(a || b).t`, `(c ? a : b).t` e simili, e nel codice della 1.2.27 e di oggi non ce n'è nessuna (0 su 246 `.t` nella 1.2.27): causa ancora ignota | `CHANGELOG.md` 1.2.28 | — |
| 8 | **Suoni:** boa più forte nella 1.3.67 (voce 18 chiusa: 9,8-11,8 dB contro la soglia di 6); sartiame giudicato da Ale il 23 nov, resta l'originale | `CHANGELOG.md` 1.3.67 | Sonnet |

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
| 31 | **Dalle fonti F86-F102:** cono d'ombra in poppa forse troppo lungo; idee per bolina, lezioni e circuiti. Da proporre quando si riprende la voce 2 | `FONTI-PUBBLICHE.md` F86-F102 |
| 17 | **Pilota incastrato prima del via** (oss. 79, 1.0.64; 3 casi in 3200 corse): **non riprodotto il 27 nov** con la barca di oggi (barca puntata sul comitato a 35°-90° dal vento: tocca, scivola e va oltre; `non_partite` verdi nel giro sulla 1.3.65). Si riprende se ricompare | oss. 79 |
| 7 | **Oro della prova 5** (315/395/505 s): aspetta i tempi della prova a mano di Ale | `CHANGELOG.md` 1.2.11-1.2.12 |
| 95 | **Rivali e strapoggio** (Ale, 27 nov): dalla 1.3.68 il giocatore può scendere fino a circa 15° oltre la poppa senza strambare; i rivali no (poppa a 142-155°, strambano cazzando). Prima misurare se a loro conviene (non c'è velocità in più, solo strambate in meno), poi semmai insegnarlo nella loro guida (voce 2) | `PROPOSTA-STRAPOGGIO-86.md` |
| 1b | **Avversari: virate in più vicino alla boa** (circa 1,7 per passaggio): ferma con la bolina | `PROPOSTA-LAYLINE.md` §5 |

## 5. Le fai tu, Ale

| # | Cosa |
| --- | --- |
| 10 | **Giudizio dei suoni** all'ascolto |
| 14 | **Copia di sicurezza fuori da GitHub:** registrazioni copiate il 25 nov sul disco esterno; da ripetere ogni tanto con `bash tests/copia_su_disco.sh` |
| — | La domanda a Lucio sul finale (oss. 135), le pagine di `racingrulesofsailing.org` in `fonti-pdf/` |

## Archivio

- Voci chiuse: `archivio/DA-FARE-archivio-17nov.md` (3 il 23 nov, 23, 24, 25, 26, 28, 29, 30, 32, 33, 34, 36 «Tornei online», 37, 38, 52 e le ferme 1, 11, 13, 20).
- Voci fatte il 17 nov e tolte da qui nel riordino: **45** (T2b su GitHub, voci a frammento), **51** (1.3.20), **60** (1.3.22). Altre voci fatte: 9 prima parte (1.3.21).
- Testo intero com'era prima: `archivio/DA-FARE-lunga-17nov.md`.
