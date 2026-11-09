# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola: si aggiorna a ogni fine lavoro (8 novembre 2026, decisione di Ale). Le cose da fare, in ordine, sono in `DA-FARE.md`.

*Aggiornato: 9 novembre 2026, sera.*

## Versione

- **Ultima versione chiusa: 1.2.22** (tag `v1.2.22`; da pushare con la 1.2.20 e la 1.2.21; la 1.2.19 è pushata). Novità nel `CHANGELOG.md`.
- **Online** (https://calle76.github.io/scuola-di-vela/): quella dell'ultimo push di Ale. La 1.2.18 e i 123 tag sono pushati (8 novembre sera).
- Il livello in gioco è la **Scuola** (1b, barca con la sola randa); **Deriva** è in attesa (`DA-FARE.md`).

## Cosa aspetta Ale

- **Giocare la 1.2.16-1.2.18 e mandare le registrazioni** («Scarica l'ultima regata»; note con «#» nel file): giri di penalità senza limite di 20 s, orologio dei giri, avversari che scontano subito, squalifica per i giri non fatti.
- **Il giro dei collaudi su GitHub** della 1.2.18 (scheda Actions → «Collaudi» → «Run workflow», completo), poi gli zip nella cartella del repo.
- **L'ordine delle cose da fare** in `DA-FARE.md`.

## Cosa è stato fatto l'8 novembre

- 1.2.16: giri di penalità del giocatore senza limite di 20 s (riparte dopo 8 s fermi); squalifica per i giri non fatti; lezione 20 aggiornata.
- 1.2.17: orologio dei giri nel riquadro (rosso che si riempie di verde, «0/2»).
- 1.2.18: avversari che scontano subito, anche prima del via, scostandosi il minimo; squalifica anche per loro.
- Proposta «coppie che si tengono»: chiusa senza correzione (`PROPOSTA-COPPIE.md` §12).
- Tag di versione per tutte le versioni dalla 0.18; release e issue su GitHub rifiutate (`DECISIONI.md`).

## Cosa è stato fatto l'8 novembre, notte

- Lette le 6 regate di Ale dell'8 sera (1.2.18, Chromium, 8 marcatori M): osservazioni 100-107 in `OSSERVAZIONI-GIOCANDO.md`, voci 2-5 e 14 di `DA-FARE.md` (ordine deciso da Claude su delega di Ale). File spostati in `registrazioni/`.
- Proposta partenza (`PROPOSTA-PARTENZA-ESTREMITA.md`), fermata 2: **non adottata**. Il riposizionamento in attesa toglie quasi tutte le barche oltre l'estremità allo sparo (conferma: 316 → 41 su 2160), ma i contatti salgono del 15% contro una soglia del 10%. Strumento nuovo: `tests/misura_partenza_estremita.py`.

## Cosa è stato fatto il 9 novembre, mattina

- Decisione di Ale: gli avversari si migliorano per le regate da Deriva in poi, cioè il torneo (`DECISIONI.md`).
- **1.2.19**: in attesa del via gli avversari non scivolano più oltre lo spillo. Nel torneo le barche oltre l'estremità allo sparo passano dal 14,3% al 2,0%, i contatti salgono del 6,2% (`PROPOSTA-PARTENZA-ESTREMITA.md` §10-13).
- Osservazioni 108-109: due regate dei giri dell'8 sera.
- **1.2.20**: gli avversari non si piantano più a destra della prima boa («giro diretto»). Nel torneo, conferma sui semi 891-920: fermate vicino alla boa 70 → 30, boa toccata 49 → 49, contatti 259 → 253 (`PROPOSTA-BOA-PIANTATA.md` §8-10). La prima prova (allargare le soglie) non era passata.

## Cosa è stato fatto il 9 novembre, pomeriggio

- Decisione di Ale: nelle regate non didattiche la fisica c'è tutta (raffiche e salti insieme, poi il cono d'ombra); il tipo di gara lo dice il formato. Le regate a tema restano didattiche.
- **1.2.21**: torneo ampliato. Regate 1-2 col punteggio, 3-4 coi giri di penalità, vento sempre misto. Avversari squalificati 0,3-1,4%, contatti per regata da −26% a +9% (`PROPOSTA-TORNEO-AMPLIATO.md` §7).
- Ricerca sul cono d'ombra: la letteratura c'è (F75, F76; `RICERCA-CONO-D-OMBRA.md`).
- **1.2.22**: rotta ottimale a regata finita (fuori dalla Scuola), con le layline e «dove hai perso». Mai più lenta di una barca vera su 1821 casi, calcolo circa 1 s (`PROPOSTA-ROTTA-OTTIMALE.md` §8). Nella stessa versione due difetti trovati dai collaudi: avversari bloccati nella regata nelle raffiche (dalla 1.2.20, `PROPOSTA-BOA-PIANTATA.md` §11) e prua della moviola alla raddrizzata (dalla 1.2.21).
- Decisioni di Ale: layline in quattro pezzi (il primo è nella 1.2.22), VMG come idea in Deriva e come strumento con Tattica, nomi dei livelli «Gennaker» e «Tattica».

## Dove sta cosa

- Il gioco in una pagina: `IL-GIOCO.md`. Principi: `PROGETTO.md`. Metodo (due fermate, soglie prima): `METODO.md` e `CLAUDE.md`.
- Decisioni di Ale e quanto costa cambiarle: `DECISIONI.md`. Difetti visti giocando: `OSSERVAZIONI-GIOCANDO.md`. Collaudi: `COLLAUDI.md`. Fonti: `FONTI-PUBBLICHE.md`.
- Le proposte (`PROPOSTA-*.md`) hanno in fondo l'esito di ogni fermata.
- **Le registrazioni delle regate** (`regata-….txt`, scaricate da Ale e Lucio) stanno in `registrazioni/`, nella cartella del repo ma fuori da git (`.gitignore`). Le nuove si mettono lì. Le 8 regate intere usate da `tests/rigioca_regata.py`: 04/11 21:12, 06/11 15:50, 17:59, 18:33, 07/11 16:42, 16:55, 17:07, 17:25.
