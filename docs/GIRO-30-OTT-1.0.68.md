# Giro dei collaudi del 30-31 ottobre 2026 sulla 1.0.68

Relazione scritta il 31 ottobre mattina, mentre Ale non c'era. Nessun codice del gioco è stato toccato. Commit di questa relazione: solo file di `docs/`.

## 1. Il giro pulito (cartella `tests/output/lancia_tutti/20261030-203357`)

Giro completo, sequenziale, Chromium, repository pulito sul commit `a29fbb7` (1.0.68): **61 collaudi, 20:33-23:26, circa 2 ore e 53 minuti**. (Il giro del 29 ottobre ne aveva 56 in 2 ore e 27.)

**Falliti: 8.**

| Collaudo | Esito | Noto? |
|---|---|---|
| `collaudo_avversari1b.py` | scenario 5, 7 su 10 | **noto** (giro del 29 ottobre) |
| `collaudo_competizione.py (misura)` | ESITO: FALLITO | **noto** |
| `collaudo_partenze.py` | «esperti 6,7% non meno dei principianti 5,0%» | **noto** |
| `collaudo_torneo.py (misura)` | C11 R7, uscita dal menu 2,89 s (soglia 2 s) | **noto**: misura di tempo, fallita anche il 29 ottobre |
| `collaudo_virate2.py` | ESITO: FALLITO | **noto** |
| `collaudo_quiz.py` | pagina dietro il menu scorre di 68 px a 1360×650 | **NUOVO** |
| `collaudo_esame.py` | idem, e menu 575 → 718 px | **NUOVO** |
| `collaudo_salti2.py` | menu del gioco libero, pagina 66 px | **NUOVO** |

Verdi (erano falliti il 29 ottobre): `collaudo_carriera.py`, `collaudo_registrazione.py (8 regate)`.

I tre nuovi hanno **una sola causa**, trovata e misurata: la descrizione della «Regata con i giri di penalità» nel menu (vedi sotto, §2 e `PROPOSTA-MENU-1360X650.md`). Non c'entrano il motore né i giri degli avversari.

## 2. Il menu che scorre di 68 px: bisezione

Il collaudo del quiz (9 secondi) lanciato su ogni versione: 1.0.60 verde; **1.0.61 +29 px** (la voce nuova); 1.0.62 +49 (descrizione più lunga); **1.0.65 +68 px** (descrizione ancora più lunga); 1.0.66-1.0.68 uguali. Prove in una copia temporanea: descrizione di una riga → 10 px; **una riga più `padding` delle righe da 6 a 4 px → 0 px, collaudi verdi**; descrizione vuota → 0 px. Dettagli, rimedi (R1-R4) e criteri nella proposta `docs/PROPOSTA-MENU-1360X650.md` (commit `7f4e4a7`). **Serve la scelta di Ale.**

## 3. Il giro interrotto delle 19:22 e il carico

Nel primo giro (cartella `20261030-192255`, interrotto alle 20:33) erano falliti anche `collaudo_segnali.py` (G2, bandiera X) e `collaudo_contatto_vero.py` (1a: 0,29 m invece di 0,25). **Non si riproducono:** verdi nel giro pulito e verdi lanciati a mano sia sul codice della 1.0.67 (`beebd10`) sia della 1.0.68. Causa probabile, non dimostrata: in quelle ore io facevo girare i miei collaudi (giri degli avversari, 40 regate) **sullo stesso PC**, e collaudi con tempi e frame lasciano fuori misura quando la macchina è carica. In più, in quel giro cambiavano i file mentre i collaudi giravano (1.0.68 e collaudo nuovo). **Regola per il futuro:** mentre gira `lancia_tutti.sh` su un repository, non lancio nulla di pesante e non modifico i file (l'ho scritto nella memoria di lavoro).

## 4. Prova parallela (`--veloce --parallelo 3`)

Lanciato `tests/lancia_tutti.sh --veloce --parallelo 3` sulla 1.0.68 (cartella `20261031-070114`): **49 collaudi, 24 minuti (1441 s)**, 12 saltati perché lunghi. Nel giro sequenziale le stesse 49 voci fanno circa 37 minuti (stima dai tempi dei file, non da un cronometro).

**Esiti: identici su 49 su 49** rispetto al giro sequenziale (tutti i falliti coincidono: `esame`, `quiz`, `salti2`, `partenze`; nessun collaudo cambia stato). Compresi i collaudi a tempo (`torneo (veloce)`, `competizione (veloce)`): verdi. **Cautela dichiarata:** una parte del giro è stata disturbata da un mio secondo lanciatore parallelo (3 corsie in più per circa 10 minuti), che ha caricato il PC più di quanto previsto; è quindi una prova **più dura** del normale, e ha comunque dato gli stessi esiti. Il guadagno (24 minuti contro 37) è minore di quanto sperassi perché alcuni collaudi lunghi (`partenze` 590 s) dominano il tempo totale e il parallelismo non li accorcia. Non ho provato `--parallelo 5` (la macchina ha 6 core; non ho voluto altro carico dopo il disturbo).

**Conclusione:** `--parallelo 3` è affidabile per il giro `--veloce` (stessi esiti). Per il giro completo con i lunghi (`torneo (misura)` 34 min, `distacchi` 18, `competizione (misura)` 15) il parallelo accorcerebbe poco: valgono quei 67 minuti in sequenza. Per ridurre davvero servono altre due cose (proposta nel §5).

## 5. Proposte (nessuna applicata)

1. **Misure lunghe solo quando servono.** `torneo (misura)`, `distacchi`, `competizione (misura)` sono tarature, non controlli di regressione: lanciarle solo quando cambiano torneo, avversari o competizione. Il giro completo scenderebbe a circa 85 minuti in sequenza.
2. **Giro quotidiano = `--veloce --parallelo 3`**: circa 24 minuti.
3. **`collaudo_quiz.py` (9 s) dopo ogni modifica a menu o descrizioni**, per non ripetere l'errore del 2a.
4. **GitHub Actions** per il giro completo, in cloud e in parallelo, anche con Firefox (da proporre, fermata 1).

## 6. Cosa serve da Ale

- `git push` (commit nuovi: tutta la sessione, ultimi `a29fbb7`, `7f4e4a7` e questa relazione).
- La scelta sul menu (R1-R4 in `PROPOSTA-MENU-1360X650.md`), consiglio R2.
- La risposta alla domanda aperta sul boma in poppa (via per la fermata 2) e il tuo test a mano sulla 1.0.67/1.0.68 (lista data in chat).
- Firefox: il giro completo con `BROWSER=firefox` non è stato fatto; se vuoi lo faccio io in una mezz'ora di parallelo.
