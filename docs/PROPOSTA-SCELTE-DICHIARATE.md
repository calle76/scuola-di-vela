# Proposta: dichiarare le scelte del gioco nelle lezioni della Scuola (voce 9; fermata 1, 13 novembre 2026)

**Stato: proposta. Nessun codice toccato. Aspetta il via di Ale.**

Viene dalla voce 9 di `DA-FARE.md` e dal controllo della Scuola sulle fonti (`CONTENUTI-DA-VERIFICARE.md`, sezione del 4 novembre, tabelle ❌ e 🎮). Principio 4 di `PROGETTO.md`: le semplificazioni si dichiarano. Sono **solo testi** in `js/contenuti.js`: nessun numero del motore cambia.

## 1. Le frasi da cambiare

Testi letti in `js/contenuti.js` il 13 novembre (numeri di riga del ramo `scheda-rivali`, uguali a `main` in questo file). Per ognuna: cosa dice oggi, cosa dicono le fonti, la frase proposta (circa della stessa lunghezza, per non sforare il pannello).

| # | Dove | Oggi | Fonti | Proposta |
| --- | --- | --- | --- | --- |
| 1 | Lezione 5, strambata controllata (riga 204) | «si cazza la vela finché il boma è a circa 45° dal centro barca» | Nessuna dice 45°; Dispensa, F61, F65: boma al centro o vicino; F64 (derive): l'errore più comune è cazzare troppo. Non concordano | «si cazza la vela (in questo gioco finché il boma è a circa 45° dal centro; le scuole non sono d'accordo su quanto)» |
| 2 | Lezione 5, esercizio (riga 210) | «cazza finché il boma è a 45° o meno» | come sopra | invariata: è l'istruzione dell'esercizio, e la 1 dice già che è la regola del gioco |
| 3 | Lezione 3, filetti (riga 124) | «Sulla randa ci sono due nastrini, i filetti: rosso sul lato sinistro, verde sul lato destro» | Sulla randa i filetti stanno di solito sulla balumina, uno a ogni stecca (F66, F67); quelli sui due lati sono tipici del fiocco (F61). Colori: scelta nostra | «In questo gioco la randa ha due nastrini, i filetti, uno per lato: rosso a sinistra e verde a destra (sulle vele vere stanno anche sul bordo d'uscita e hanno colori diversi)» |
| 4 | Lezione 8, scuffia (righe 229 e 235) | «Oltre circa 60° di sbandamento la barca si è rovesciata» | Soglia del motore, nessuna fonte. Il regolamento chiama scuffiata la barca con la testa d'albero in acqua (regola 22) | «In questo gioco, oltre circa 60° di sbandamento la barca si rovescia» (riga 229); riga 235: «Se sbandi troppo (qui oltre circa 60°) si scuffia» |
| 5 | Lezione 3 e domanda d'esame, traverso (righe 111 e 736) | «il boma a una quarantina di gradi dal centro barca» | Numero del nostro motore; nessuna fonte | «circa a metà (nel gioco il boma sta a una quarantina di gradi)»; la domanda resta, la spiegazione dice «nel gioco» |
| 6 | Lezione 18 e domanda d'esame (righe 520, 540, 659, 664, 836) | «una o due lunghezze dietro» la linea | Numero nostro. F28: circa 30 s di navigazione dalla linea, poi si accelera | Lezione: «vicino alla linea (in questo gioco, una o due lunghezze dietro)». **Domanda d'esame da togliere o da cambiare:** chiede un numero nostro come se fosse un fatto. Propongo di chiedere il principio: «Dove conviene aspettare il via?» → «Vicino alla linea, quasi fermo» |
| 7 | Lezioni 12-14, parole del regolamento | «lasciare strada», «libera dietro/avanti», «sovrapposte», «precedenza» | F39 (testo italiano): «tenersi discosta», «libera dalla poppa/prua», «ingaggiate», «diritto di rotta» | Una riga nel primo passo della lezione 12: «Il regolamento usa parole più tecniche: tenersi discosta, ingaggiate, diritto di rotta. Qui usiamo quelle di tutti i giorni». E le parole del regolamento nel glossario, accanto alle nostre |

## 2. Cosa resta fuori

- Le voci 🎮 già dichiarate o innocue: limite dei filetti a 112° (numero del motore, il principio è confermato), la X al massimo 4 minuti, «dietro la linea» senza i prolungamenti, i messaggi della virata che non riesce, la trama dell'acqua nella raffica.
- La seconda parte di «lasciare strada» (con barche ingaggiate l'altra deve poter cambiare rotta da tutti e due i lati): riguarda le regole 15-16, rimandate.
- Le voci 🔶 (una fonte sola): si cercano fonti, non si cambiano testi.

## 3. Criteri (soglie nostre, scritte prima)

- **D1, pannello:** a 1360x650 nessun pixel in eccesso in nessun passo delle lezioni toccate (3, 5, 8, 12, 18), misurato sul pannello intero, anche col caso più lungo.
- **D2, lezioni ancora fattibili:** `collaudo_lezioni.py` passa le lezioni toccate guidando la barca; esame: `collaudo_esame` con la domanda cambiata.
- **D3, non-regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici (non si tocca il motore).
- **D4, ogni frase cambiata ha la sua riga** in `CONTENUTI-DA-VERIFICARE.md` (da 🎮 a «dichiarata nella 1.2.x»).

## 4. Domande per Ale

1. **Il via.**
2. **La domanda d'esame sulle «una o due lunghezze» (6):** si cambia col principio, come propongo, o si toglie?
3. **Le parole del regolamento (7):** solo la riga nella lezione 12, o anche nel glossario?

## 5. Costo

Due-tre ore: testi, glossario, collaudi delle lezioni toccate.
