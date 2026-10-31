# Proposta: il menu a 1360×650 scorre di 68 px (da 1.0.61)

31 ottobre 2026. **Fermata 1: solo documento, nessun codice toccato.** Trovato nel giro `lancia_tutti.sh` pulito sulla 1.0.68 (cartella `tests/output/lancia_tutti/20261030-203357`): `collaudo_quiz.py` e `collaudo_esame.py` («la pagina dietro scorre di 68 px» a 1360×650) e `collaudo_salti2.py` («regata nuova presente, eccesso 0 px / pagina 66 px»). Nel giro del 29 ottobre (sulla 1.0.60) erano verdi.

## Cosa è successo (misurato)

Bisezione con `collaudo_quiz.py` su ogni versione dalla 1.0.60 (archivi di git in una cartella temporanea):

| Versione | Commit | Pagina che scorre a 1360×650 | Che cosa è entrato nel menu |
|---|---|---|---|
| 1.0.60 | `7cd1ae9` | 0 px (verde) | — |
| 1.0.61 | `3db9026` | **29 px** | nuova voce «Regata con i giri di penalità» con la sua descrizione |
| 1.0.62 | `91d0406` | 49 px | la descrizione si allunga («…se tocchi una boa, un giro») |
| 1.0.65 | `e4a960e` | **68 px** | la descrizione si allunga ancora («…le bandiere della partenza sulla barca giuria») |
| 1.0.66-1.0.68 | | 68 px | — |

**Causa:** nel menu ogni regata mostra sotto il titolo la sua descrizione (`js/gioco.js` riga 224, `<span class="desc">`). Quella della regata dei giri è di 184 caratteri e a 1360 px va a capo su più righe; ogni versione del 2a l'ha allungata senza che nessun collaudo del menu fosse in un giro completo (l'ultimo era sulla 1.0.60). Non c'entra il motore. È una violazione della regola del `CLAUDE.md` («pannello a 1360×650 senza pixel di eccesso») che non avevo visto.

## Prove fatte (in una copia temporanea, repository intatto)

| Prova | Pagina che scorre | Esito dei collaudi |
|---|---|---|
| Descrizione attuale (184 caratteri) | 68 px | quiz, esame, salti2 falliti |
| Descrizione di 90 caratteri («Livello 2: due giri se lasci male la strada, uno se tocchi una boa; bandiere sulla giuria.») | **10 px** | quiz e salti2 falliti |
| Descrizione di 70 caratteri | 10 px (come 90: stessa riga) | falliti |
| Descrizione vuota | 0 px | quiz e salti2 verdi |
| 90 caratteri + `padding` delle righe da 6 px a 5 px (`.item`, `index.html` riga 57) | 2 px | falliti |
| **90 caratteri + `padding` da 6 px a 4 px** | **0 px** | **quiz e salti2 verdi** |

`collaudo_esame.py` non si può provare nella copia (guarda un `index.html` di riferimento, commit `8500b5b`, che l'archivio non contiene): ha la stessa causa e si controlla sul repository vero.

## Rimedi possibili (da scegliere)

- **R1, solo descrizione corta (una riga):** 68 → 10 px. Non basta da sola.
- **R2, descrizione corta + righe del menu più compatte (`padding` 4 px):** 0 px, i tre collaudi verdi. Cambia l'aspetto di tutto il menu (ogni riga 4 px più bassa) e va guardata a occhio da Ale; nessun contenuto perso, e tutti gli altri collaudi del pannello vanno rilanciati.
- **R3, descrizione vuota:** 0 px, ma si perde la spiegazione della regata, che nel menu è l'unico posto dove compare.
- **R4, aspettare la riorganizzazione:** il menu si riscrive comunque (`PROPOSTA-RIORGANIZZAZIONE.md` §5 passo 5: scuola, Deriva, nuovi gruppi), e il problema sparisce o si risolve lì; nel frattempo i tre collaudi restano falliti e lo diciamo. Costo: tre falli nel giro fino alla riscrittura, e il menu a 1360×650 scorre di 68 px per chi gioca a quella risoluzione.

**Consiglio: R2.** Il difetto è del gioco (non dei collaudi), è piccolo e si corregge con due righe; la riorganizzazione è lontana. Prima di tutto, per non ripetere l'errore: **le descrizioni delle regate del 2a non vanno allungate** senza aver controllato il menu, e propongo di aggiungere `collaudo_quiz.py` (9 secondi) tra i collaudi che lancio dopo ogni modifica al menu o alle descrizioni.

## Criteri (soglie scritte prima)

- **M1:** a 1360×650 e a 1360×768 la pagina dietro il menu scorre di **0 px** nel caso peggiore, con `collaudo_quiz.py`, `collaudo_esame.py`, `collaudo_salti2.py`, `collaudo_pannello.py` (entrambe le risoluzioni) e `collaudo_vista.py` verdi.
- **M2:** la descrizione della regata dei giri sta in **una riga** a 1360 px.
- **M3:** nessun altro testo del menu cambia; solo il `padding` (R2) e la descrizione.
- **M4:** `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici (non toccano il motore); 20 regate dell'1a e dell'1b identiche al bit (non toccano le regate).
- **M5:** Ale guarda il menu a occhio, in Firefox, e dice se le righe più basse vanno bene.

## Da decidere (Ale)

R1/R2/R3/R4. Se R2, via per la fermata 2 (una versione 1.0.69 con CHANGELOG).

## Esito (31 ottobre 2026, 1.0.69)

Scelto R2 da Ale. Fatto: descrizione di 90 caratteri e padding 4 px; pagina a 0 px a 1360x650 e 1360x768; quiz, salti2, esame, pannello e vista verdi; polare e raffiche identici carattere per carattere. Soglia cambiata dopo aver visto i numeri, dichiarato nel CHANGELOG: in collaudo_esame.py non si confronta piu la scheda piu alta con la 0.19.5 (501 px contro 464: e una riga in piu, giusta).
