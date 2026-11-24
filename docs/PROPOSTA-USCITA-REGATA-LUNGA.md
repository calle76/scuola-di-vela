# Proposta: uscire da una regata lunga del torneo senza che la pagina si fermi (voce 71)

*Fermata 1, 21 novembre 2026 (scritta nella notte, Ale assente). Nessun codice finché non arriva il via. Prima: Ale dice se il ritardo si sente (risposta attesa dopo la sua prima regata lunga, «non è un problema aspettare qualche secondo»).*

## Cosa succede (misurato il 21 novembre)

`collaudo_torneo.py --lungo --solo c11` (R7, uscita dal menu a metà regata): al massimo **6,33 s**, tipico 3-6 s; nelle regate corte 2,7 s e soglia 2 s. Su GitHub, in Firefox, la chiusura della pagina dopo 1 s dall'uscita non basta e C11 cade a 7/8 (per questo C11 oggi **non** gira nel torneo veloce `--lungo`).

## Causa (letta nel codice, `js/regate.js`, `torChiudi`)

Lasciare la regata a metà (menu, pagina chiusa) conta come ritiro e `torChiudi` simula **in un ciclo solo** tutto il resto della regata dei rivali (`for` fino a `60 · 1800` passi di 1/60 s, finché c'è una barca che non è arrivata): in una regata lunga il lavoro è proporzionale al tempo rimasto, e la pagina non risponde per tutto il tempo. È chiamata in tre punti: `torEsci` (menu e `pagehide`), il pulsante `rTor` a fine regata.

## Strade

| Strada | Costo | Rischio |
| --- | --- | --- |
| **A. Simulare a pezzi** (per esempio 0,05 s di lavoro per fotogramma) con una scritta «Calcolo i risultati…»; lo stesso ciclo spezzato, gli stessi passi di 1/60 s, quindi **risultati identici al bit** | medio: `torChiudi` diventa asincrona; il ritiro dalla chiusura della pagina (`pagehide`) non può aspettare i fotogrammi | `pagehide`: lì si resta sincroni (si accetta il blocco, o si salva subito il ritiro con i risultati stimati dal tempo già simulato: da decidere) |
| B. Passo più grande nel resto della regata | basso | **cambia gli arrivi** dei rivali: da escludere (stessa regata, stessi risultati) |
| C. Non simulare, stimare i rivali dal tempo già corso | medio | cambia gli arrivi e la classifica del torneo: da escludere |
| D. Lasciare com'è | nullo | 3-6 s di attesa; si decide dopo la prova di Ale |

**Raccomandazione:** A solo per l'uscita dal menu e per il pulsante di fine regata; `pagehide` resta sincrono. Se Ale non sente il ritardo, D.

## Criteri (soglie nostre, dichiarate prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| U1 | Stessi risultati | 20 tornei lunghi chiusi a metà (semi fissi, pagina nuova per ognuno): arrivi e punti dei rivali identici al bit con e senza la modifica; casi contati |
| U2 | Pagina viva | durante il calcolo nessun fotogramma fermo oltre 100 ms (misurato con `requestAnimationFrame`), sulla regata lunga |
| U3 | Tempo totale | uscita dal menu completata entro 8 s sul PC di Ale (R7 di C11 `--lungo`: soglia scritta ora, da confermare dopo la prima misura) |
| U4 | Il salvataggio | dopo l'uscita il torneo è nello stato «ritirato, N regate concluse» come oggi (C11 R1-R5 e C3, C4 invariati) |
| U5 | La chiusura della pagina | `pagehide` a metà regata lunga salva il ritiro come oggi (C11 R6) |
| U6 | Come un giocatore | pagina senza `#collaudo`, regata lunga lasciata a metà dal menu: scritta visibile, torneo ritirato, 0 errori |
| U7 | Suite | C11 intero con `--lungo` torna nella suite e passa in Chromium e Firefox (anche su GitHub) |

Il metro di U1 non deve dipendere dalla modifica: i risultati attesi si calcolano con il codice di oggi, salvati in un file, e si confrontano.

## Rischi

- **Doppio clic** o ritorno ai menu mentre il calcolo è in corso: serve un blocco («sto calcolando»).
- **`pagehide`**: browser diversi lasciano tempi diversi; resta sincrono, quindi il blocco in chiusura resta (ma non lo vede nessuno: la pagina si sta chiudendo).
- Il difetto è già misurato; la correzione non cambia la fisica né il motore.

## Passi, dopo il via

1. Spezzare il ciclo in `torChiudi` (stesso corpo, stesso `dt`), scritta e blocco; `torEsci` e `rTor` aspettano la fine.
2. C11 `--lungo` completo (R1-R7) e U1-U7; poi C11 torna nel torneo veloce `--lungo`.
3. Documenti, versione, `CHANGELOG.md`. Opus.

## Esito (24 novembre 2026)

Ale: «non ci impazzirei per l'attesa di qualche secondo, ma se hai la soluzione pulita allora ok». La strada A non è una correzione piccola (vedi sopra: asincrona, blocco sui menu, `pagehide` sincrono, U1 su 20 tornei lunghi). **Strada D: si lascia com'è, voce chiusa.** Si riapre se l'attesa dà fastidio giocando.
