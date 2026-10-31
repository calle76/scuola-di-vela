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

## 8. Controprove scritte prima di lanciarle (1 novembre 2026, notte)

Tabella in `tests/controprove.py` (la riga `--elenco` la stampa). Scritte tutte prima del primo lancio:

```
polare-mut       mutante  fisica/confronta.js polare.js            area della vela della 1a +10%
polare-neu       neutra   fisica/confronta.js polare.js            commento nel motore
raffiche-mut     mutante  fisica/confronta.js raffiche_e_virate.js massa della barca +10%
raffiche-neu     neutra   fisica/confronta.js raffiche_e_virate.js commento nel motore
impronta1b-mut   mutante  fisica/impronta1b.js                     barca dell'1b: acqua contro lo scafo che ruota 400 → 401 (la stessa di --cambia)
impronta1b-neu   neutra   fisica/impronta1b.js                     commento nel motore
regole-mut11     mutante  collaudo_regole.py                       regola 11 rovesciata: cede la barca sottovento invece della sopravento
regole-mut13     mutante  collaudo_regole.py                       regola 13 spenta: chi vira non cede più
regole-neu       neutra   collaudo_regole.py                       commento in regate.js
giri-mut         mutante  collaudo_giri.py 12                      un giro solo estingue tutto il debito (la 44.2 ne vuole due)
giri-neu         neutra   collaudo_giri.py 12                      commento in regate.js
boa-mut          mutante  collaudo_boa.py 12                       toccare una boa non dà il giro di penalità (regola 31)
boa-neu          neutra   collaudo_boa.py 12                       commento in regate.js
regola21-mut     mutante  collaudo_regola21.py 12                  regole 21.1 e 21.2 spente: chi sconta o torna dietro la linea non cede
regola21-neu     neutra   collaudo_regola21.py 12                  commento in regate.js
giriavv-mut      mutante  collaudo_giri_avversari.py 12            gli avversari non fanno mai i giri (12 regate invece di 40, per il tempo)
giriavv-neu      neutra   collaudo_giri_avversari.py 12            commento in regate.js (12 regate)
segnali-mut      mutante  collaudo_segnali.py                      la X resta su anche quando le barche richiamate sono tornate (29.1)
segnali-neu      neutra   collaudo_segnali.py                      commento in regate.js
contatto-mut     mutante  collaudo_contatto_vero.py                nell'1b il contatto scatta a 4,4 m fra i centri anche senza scafi che si toccano
contatto-neu     neutra   collaudo_contatto_vero.py                commento in regate.js
semaforo-mut     mutante  collaudo_semaforo.py                     semaforo con i colori scambiati
semaforo-neu     neutra   collaudo_semaforo.py                     commento in regate.js
pannello-mut     mutante  collaudo_pannello.py 1360 650            40 px in più in cima al pannello
pannello-neu     neutra   collaudo_pannello.py 1360 650            commento nella pagina
```

Cambi rispetto al §4, decisi prima di lanciare: T5 (tre corse con semi diversi) **non si applica** ai collaudi di questa fetta, che girano a passi fissi con semi fissati dentro lo script: ripeterli dà lo stesso risultato al bit, quindi una corsa sola. `collaudo_giri_avversari.py` nelle controprove gira con 12 regate invece di 40 (tempo). Le neutre sono 12 (una per collaudo), i mutanti 13 (due per `collaudo_regole.py`, regola 11 e regola 13).

## 10. Proposte per trovare errori più piccoli (fermata 1, da fare dopo)

Le controprove del §8 sono difetti **grossi** (regola spenta, colori scambiati). Un collaudo che li prende può non prendere uno sbaglio piccolo. Cinque proposte, in ordine di quanto rendono per quello che costano. Le soglie sono attese nostre.

1. **Controprove sottili (fetta 2).** Le stesse 12 righe, ma con le «ipotesi nostre» spostate poco: `GIRO_GRADI` 360 → 330, `VIRATA_MIN` 42 → 38, `X_MAX` 240 → 200, `BOA_R` 0,9 → 0,7, `SEM_ON` 8 → 6, `GIRO_AI_VIA` 4 → 3, distanza di contatto dell'1a 4,2 → 4,0 m. Molte **non** verranno prese: per ognuna si decide se il collaudo va allargato (un caso al confine) o se la costante è libera e lo si dichiara. Criterio: un elenco completo «protetta / non protetta» per ogni costante dichiarata ipotesi nostra in `js/regate.js`. Costo: come la fetta 1, circa 1 ora di macchina.
2. **Casi al confine.** Per ogni regola con una soglia, due casi messi a mano subito sotto e subito sopra (giro di 355° che non conta e di 361° che conta; X a 239 s su e a 241 s giù, già fatto in `collaudo_segnali.py`; boa toccata a 0,1 m e non toccata a 0,1 m oltre). È il modo più economico per proteggere una soglia: un caso al confine prende anche uno spostamento dell'1%.
3. **Testi contro costanti.** Un collaudo veloce che legge i testi del gioco (`js/contenuti.js`, `js/regate.js`) e controlla che ogni numero detto al giocatore coincida con la costante del codice: «due giri» con il debito di 2, «+15 s» con `GIRO_SEC`, «4 minuti» con `X_MAX`, i nodi del menu con quelli delle prove. Gli sbagli di oggi nei metri (14 nodi inesistenti) erano di questo tipo. Costo: mezza sessione, un secondo di macchina.
4. **Impronta delle regate.** Come `impronta1b.js` per la barca: 6 regate a passi fissi con semi fissi, e per ogni barca la posizione ogni 10 s salvata in git; a ogni versione si confronta al centimetro. Prende qualunque cambiamento nella guida degli avversari, anche piccolo, e obbliga a dire «è voluto». `collaudo_impronta.py` esiste già ma ha il riferimento vecchio: va rigenerato (è nell'elenco della pulizia del codice).
5. **Controprove a tappeto (mutation testing).** Uno script che cambia da solo, una alla volta, ogni costante numerica di `js/regate.js` (±20%) e lancia il giro `--veloce`: la mappa di cosa nessun collaudo protegge. È il più completo ma costa decine di ore di macchina: solo se un giorno i collaudi girano su GitHub Actions, di notte, non sul PC di Ale.

Consiglio: 3 e 2 subito dopo la pulizia del codice (poco costo, molti sbagli piccoli presi), poi 1; 4 con la pulizia; 5 solo con GitHub Actions.

## 9. Esiti (1 novembre 2026, notte; fermata 2)

**A — conteggio dei casi.** `tests/metro.py`; 97 `all(` in 25 collaudi chiari diventati `metro.tutti(` (un primo tentativo con il nome `tutti` si scontrava con una variabile di `collaudo_boa.py`: corretto in `metro.tutti`). I 15 `not any(` dei collaudi chiari rivisti a mano: tutti hanno accanto un conteggio o lavorano su elenchi fissi, nessuno cambiato. Giro dei 31 lanci toccati (3 alla volta, Chromium): 28 OK, 3 FALLITI noti con gli stessi numeri del giro del 30 ottobre (virate2 identico riga per riga; competizione misura con piccole differenze nei tempi dovute alle versioni 1.0.71-1.0.73, stesso esito). Nessun controllo sotto il minimo. **T1: 100%.**

**T2, prova a vuoto** (`… 0`): giri, boa, giri_avversari, moviola, registrazione cadono (5 su 5; tre cadono con un errore Python invece che con un controllo, ma il codice d'uscita è 1 lo stesso). `collaudo_regola21.py 0` resta verde perché il numero non decide i casi (griglie fisse da 120 e 90 posizioni, 30 regate per K6 con la variabile `REGATE`): non è un buco, è un'etichetta.

**B — chiari.** 59 su 64 (13 convertiti). Tutti verdi sul gioco vero: lezioni (18 passi), regate bastone e raffiche (18 arrivi ciascuna), strambata 6 nodi (nessuna scuffia, 10 strambate su 10) e 15 nodi (scuffia sempre), pannello 1360×650 e 1360×768 (89 misure), fantasma, registro (15 su 15), schermate (28), giro di boa (8 casi), polare e raffiche (identici). **Trovato in `collaudo_lezioni.py`:** passo 1.8 NON COMPLETATO dal 16 ottobre (vedi CHANGELOG), corretto nel collaudo.

**C — controprove** (`tests/controprove.py`; uscite in `tests/output/controprove/`).

| | Mutanti presi | Neutre verdi |
|---|---|---|
| Prima fetta (12 collaudi) | 13 su 13 | 11 su 12 (+1 con 40 regate: verde) |
| Aggiunte per i collaudi convertiti (lezioni, giro di boa, strambata) | 2 su 3 | 3 su 3 |
| **Totale** | **15 su 16 (94%)** | **15 su 16 al primo lancio; 16 su 16 con la riga corretta** |

- **T3** (almeno 90% dei mutanti presi, con il controllo giusto): 15 su 16, **sì**. Il controllo che cade è quello della regola cambiata in tutti i casi guardati (regole: i casi 11 e 13; giri: B1; boa: A1; regola21: K1; giri_avversari: G2 e, a zero casi, G1 e G3-G7; segnali: G1; contatto: i casi «scafi a 3,0 m»; semaforo: 34 contatti col colore sbagliato; pannello: eccesso; lezioni: passo 1.8; giro di boa: «giri sbagliati=0»).
- **Mutante non preso:** `strambata-mut`, soglia di scuffia `BOAT.capsizeAt` 60° → 90° nel ciclo del gioco. A 15 nodi la strambata violenta porta lo sbandamento oltre 90° comunque: il collaudo controlla l'esito («scuffia sempre»), non la soglia. Controllato a parte sulla stessa copia: `collaudo_registro.py` cade (14 su 15, «lezione 6, scuffia richiesta»), `collaudo_lezioni.py` e `raffiche_e_virate.js` no (la soglia non è nel motore che leggono i collaudi della fisica). Quindi la soglia **è** protetta nel giro, da un collaudo solo.
- **T4** (zero falsi allarmi): **no al primo lancio**, 1 su 16: `giriavv-neu` a 12 regate cade per il minimo di casi di G4 (7 su 15). È il metro che funziona, con un numero di regate scelto male da me; la riga con 40 regate (aggiunta dopo, dichiarato) è verde.
- **T5**: non applicato, dichiarato al §8 prima di lanciare (collaudi a passi fissi).
- **T6**: gioco non toccato (`git status` pulito su `index.html` e `js/`); polare e raffiche identici.

**Cosa resta debole** (in ordine di peso): (1) le soglie numeriche, come quella di scuffia, sono protette dall'esito e non dal valore: le proposte 1-2 del §10; (2) 5 collaudi restano ambigui; (3) tre collaudi a zero prove cadono con un errore Python invece che con un messaggio chiaro (non grave: cadono); (4) tutto misurato in Chromium; le controprove in Firefox non sono state lanciate.
