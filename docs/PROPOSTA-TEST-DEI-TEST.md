# Proposta: il «test dei test» (fermata 1)

31 ottobre 2026, gioco alla 1.0.73. Solo documento: nessun codice del gioco né dei collaudi è stato toccato.

## 1. La domanda di Ale

«I test sono affidabili?» Risposta onesta di oggi: **in parte, e non sappiamo quanto.** Un collaudo verde dice che non ha visto errori, non che li avrebbe visti. Quattro buchi già noti:

1. **Controlli a vuoto.** Un controllo scritto come «tutti i casi vanno bene» è verde anche con zero casi. È già successo (Q4e del riquadro, a zero casi). Una prima ricerca automatica (grossolana: guarda solo la riga del controllo) trova **23 controlli su 61** con `all(...)` senza un conteggio visibile, in 10 file: `boa`, `carriera_esame`, `contatto_senza_colpa`, `esame`, `giri` (D3), `moviola` (5), `quiz`, `registrazione` (6), `regola21` (2), `semaforo` (3). Sono candidati, non errori sicuri: molti avranno il conteggio altrove.
2. **Metro sbagliato.** Errori miei nei metri trovati il 31 ottobre: Q2b, i 14 nodi che nel menu non esistono. Nessun collaudo se n'era accorto da solo.
3. **18 collaudi su 64 sono «ambigui»**: stampano numeri che una persona deve confrontare a mano. Nella pratica nessuno li confronta riga per riga.
4. **Nessuno ha mai provato che un collaudo «chiaro» cade davanti al difetto per cui è stato scritto.** Le eccezioni sono poche: `impronta1b.js --cambia`, le contro-prove dentro `collaudo_laboratorio.py`, `collaudo_esame.py`, `collaudo_suggerimento.py`.

## 2. Il modello più semplice plausibile

Tre pezzi, in quest'ordine (dal più economico).

### A. Conteggio dei casi (in tutti i collaudi «chiari»)
Una funzione comune in `tests/metro.py`: `tutti(nome, casi, prova, minimo=1)`. Stampa sempre `(n casi)` e dà FALLITO se i casi sono meno del minimo, oltre che se uno sbaglia. Si passa sui 23 candidati e poi su tutti gli altri controlli con `all(...)`. Il minimo di ogni controllo si scrive **prima** di lanciarlo (di solito: il numero di prove richieste dal comando, o 1 se il caso è raro).

### B. Gli ambigui diventano chiari dove si può
- `polare.js` e `raffiche_e_virate.js`: CLAUDE.md chiede già «carattere per carattere». Si salva la loro uscita di oggi in git (`tests/fisica/polare.txt`, `raffiche_e_virate.txt`) e il collaudo la confronta: uguale → OK, diversa → FALLITO. Come `impronta1b.txt`.
- `collaudo_pannello.py` (due misure): CLAUDE.md chiede «senza pixel di eccesso» → FALLITO se l'eccesso è più di 0 px.
- Gli altri 14 si guardano uno per uno: chi ha un atteso scritto in `COLLAUDI.md` diventa chiaro; chi è solo una misura (partenze, regate, strambata, fasce…) resta «misura» e lo si dice nel nome della riga, così nessuno lo scambia per un controllo.

### C. Controprove: un difetto messo apposta in una copia, il collaudo deve cadere
Uno script nuovo, `tests/controprove.py`, con una tabella: *collaudo → sostituzione nel codice → quale controllo deve cadere*. Per ogni riga:
1. copia `index.html`, `js/`, `fonts/` e `tests/` in una cartella temporanea (`$TMPDIR`), così i collaudi, che trovano la pagina da soli, aprono la copia **senza modificarne nessuno**;
2. applica la sostituzione con `sorgente.copia` (che esiste già e controlla che il pezzo da cambiare compaia una volta sola);
3. lancia il collaudo e legge l'esito.

Due tipi di controprova:
- **mutante**: un difetto vero (regola spenta, segno invertito, soglia spostata del 20-50%, funzione che esce subito). Il collaudo **deve** dare FALLITO, e deve cadere il controllo indicato, non uno qualunque.
- **neutra**: una modifica che non cambia il comportamento (un commento, un nome interno). Il collaudo **deve** restare OK: serve a vedere che non cade per qualunque cosa.

Il gioco vero (`index.html`, `js/`) non si tocca mai: si lavora solo sulla copia.

## 3. Prima fetta delle controprove (12 collaudi)

I collaudi che proteggono di più: la non-regressione e il livello 2a appena fatto.

| Collaudo | Mutante (da scrivere nel dettaglio prima di lanciare) | Neutra |
|---|---|---|
| `polare.js` (dopo B) | una costante della barca +10% | commento in `motore.js` |
| `raffiche_e_virate.js` (dopo B) | idem, altra costante | idem |
| `impronta1b.js` | già fatta (`--cambia`): si riporta solo nel quadro | — |
| `collaudo_regole.py` | regola 11 non applicata (sopravvento e sottovento scambiati) | sì |
| `collaudo_giri.py` | un giro solo estingue il debito | sì |
| `collaudo_boa.py` | toccare la boa non dà il giro | sì |
| `collaudo_regola21.py` | la 21.2 non toglie i diritti a chi sta girando | sì |
| `collaudo_giri_avversari.py` | gli avversari non fanno i giri (restano i +15 s) | sì |
| `collaudo_segnali.py` | la X non si abbassa più (o non sale) | sì |
| `collaudo_contatto_vero.py` | distanza di contatto 5 cm → 50 cm | sì |
| `collaudo_semaforo.py` | colore del semaforo invertito | sì |
| `collaudo_pannello.py` 1360x650 (dopo B) | una riga di testo in più nel pannello | sì |

Le sostituzioni esatte si scrivono in questo documento **prima** di lanciare, partendo da cosa dice la regola o la proposta, non da come è fatto il collaudo (così chi sceglie il difetto non sceglie solo quelli che sa già presi). Una controprova che non cade non si toglie: si riporta come buco.

Gli altri collaudi chiari (circa 34) vengono dopo, a pezzi, quando si tocca la parte che proteggono.

## 4. Criteri misurabili (soglie: attese nostre, dichiarate prima)

| | Cosa | Soglia |
|---|---|---|
| T1 | Controlli con `all(...)` nei collaudi chiari che stampano il numero di casi e cadono a zero casi | 100% |
| T2 | Prova a vuoto: ogni collaudo toccato da A, lanciato con zero prove (per esempio `collaudo_giri.py 0`), dà FALLITO | 100% di quelli che accettano il numero di prove |
| T3 | Controprove mutanti della prima fetta che fanno cadere il collaudo, e il controllo giusto | almeno 10 su 11 (90%); quelle che non cadono si elencano |
| T4 | Controprove neutre che fanno cadere il collaudo (falsi allarmi) | 0 su 11 |
| T5 | Collaudi con il caso: ogni mutante lanciato **2 volte** con i semi del giro (gli stessi del `lancia_tutti.sh`) e una terza con un gruppo di semi mai usato | deve cadere in tutte e 3 |
| T6 | Non-regressione: con il codice vero, i collaudi toccati danno lo stesso esito di prima; `polare.js` e `raffiche_e_virate.js` identici carattere per carattere | identico |

**Il metro non dipende da ciò che si misura:** T3 conta solo sulle controprove scritte prima; T2 e T4 controllano il metro stesso (che cada a vuoto, che non cada per niente).

## 5. Costanti e ipotesi nuove

Nessuna costante del gioco. Ipotesi: che un difetto «grosso» (regola spenta, soglia +20-50%) sia rappresentativo dei difetti veri. Non è garantito: un collaudo che prende i difetti grossi può non prendere quelli sottili. Lo si dice nel rapporto.

## 6. Costi e rischi

- **Tempo.** A e B: una sessione, lanciando solo i collaudi toccati. C, prima fetta: 11 mutanti × 3 corse + 11 neutre ≈ 44 corse; i collaudi della tabella durano da pochi secondi (`impronta1b.js`) a circa 10 minuti (`giri_avversari`, 40 regate). Stima: **1 ora e mezza – 2 ore** di macchina in background, una volta sola; poi si rilancia solo la riga del collaudo che si cambia. Con `giri_avversari` si può usare un numero di regate più basso nel mutante (si dice quale).
- **Non entra nel giro di tutti i giorni**: `controprove.py` è uno strumento da lanciare quando si scrive o si cambia un collaudo, non a ogni versione.
- **Copia in `$TMPDIR`**: va cancellata alla fine (lo fa lo script).
- **Rischio di sembrare più sicuri di quel che si è**: un 11 su 11 dice che quei collaudi prendono *quei* difetti, non tutti.
- **Mentre gira `lancia_tutti.sh` di Ale non si lancia niente** (regola nota): le controprove si lanciano solo a cartella ferma.
- Il gioco non cambia: nessuna versione nuova, niente `VERSIONE`. Si aggiornano `COLLAUDI.md` (sezione nuova «Controprove» e la tabella dei chiari/ambigui), `lancia_tutti.sh` (polare, raffiche, pannello diventano chiari) e una riga in `DECISIONI.md`.

## 7. Cosa serve da Ale

Il via per la fermata 2, con l'ordine A → B → C (prima fetta). Se preferisce, si può fermare dopo A e B (circa metà del lavoro, il pezzo che rende di più per quello che costa) e decidere C dopo aver visto i numeri.
