# Proposta: laboratorio della barca (Scuola di vela)

**Seconda stesura, 16 ottobre 2026. Proposta, fermata 1: nessun codice scritto.** Sostituisce quella del 13 ottobre, che citava le righe di `index.html` sul ramo `prova-saturazione` (resta nella storia di git). Le righe citate qui sono di `main` alla 1.0.3, con il codice diviso in `js/`.

Tipi delle affermazioni:
- **[codice]** = letto nel codice, con file e riga;
- **[stima]** = ragionamento senza misura;
- **[ipotesi]** = scelta nostra, da decidere.

---

## 0. In breve

- **Cos'è.** Una finestra con cursori sui valori della barca, attiva solo aprendo la pagina con `#lab` in fondo all'indirizzo. Serve a provare a mano valori diversi **senza modificare il codice**, a confronto con i video, prima dei compiti sulla barca (velocità, virata, retromarcia, ripartenza: `RICERCA-VELOCITA-VIRATA-RIPARTENZA.md`).
- **Con `#lab` il gioco non salva mai niente**, nemmeno con i valori di oggi: né record, né medaglie, né fantasmi, né lezioni, quiz, esame o carriera. Si chiude in due righe, nelle due sole funzioni che scrivono i progressi (§3), così non c'è un punto di salvataggio che si possa dimenticare.
- **Senza `#lab` il gioco è identico al bit** (lo misura `collaudo_impronta.py`).
- **Novità rispetto al 13 ottobre:** cinque numeri che oggi sono scritti dentro `step()` diventano voci di `BOAT`, **con gli stessi valori**, perché sono proprio quelli che decidono retromarcia e ripartenza (§1). È l'unico tocco al motore, e non deve cambiare niente: `polare.js` e `raffiche_e_virate.js` identici carattere per carattere.
- **Dove:** un file nuovo, `js/laboratorio.js`, caricato per ultimo. Dimensione stimata: circa 100-130 righe, più circa 5 righe negli altri file e un collaudo nuovo di circa 80-100 righe.
- **È una versione del gioco (1.0.4)**, perché tocca `index.html` e `js/`.

---

## 1. I valori da provare, e quelli che oggi non si possono toccare

**[codice]** `BOAT` (`js/motore.js:8-29`) è dichiarato con `const`, ma le sue proprietà si possono cambiare, e `step()` le rilegge a ogni passo. Quindi un cursore che cambia `BOAT.hullK2` cambia subito la barca, senza toccare il motore. Vale anche per gli avversari, che usano lo stesso `step()` (`js/regate.js:293-311`): **in regata un valore cambiato cambia tutte le barche** (detto nella finestra).

**[codice] Numeri scritti dentro `step()`, che nessun cursore raggiungerebbe:**

| Riga | Cosa fa | Valore | Serve per |
|---|---|---|---|
| `motore.js:62` | Termine lineare della resistenza, `4·u` | 4 | Velocità a vento leggero (`PROPOSTA-RESISTENZA-SCAFO.md` §4 lo indica già come candidato) |
| `motore.js:66` | Velocità massima all'indietro | 1,2 m/s (2,3 nodi) | Retromarcia |
| `motore.js:85` | Barca ferma nel vento: la prua poggia da sola, sotto 36° di vento apparente e sotto 0,5 m/s, fino a 6 °/s | 36°, 0,5 m/s, 6 °/s | Ripartenza dall'angolo morto («Ripartire»: la barca esce da sola in 80 corse su 80, `PROPOSTA-PILOTA-LEZIONI.md` §10) |
| `motore.js:86` | Quanto in fretta la rotazione segue la barra | 4 /s | Virata |

**Proposta:** spostarli in `BOAT` con nomi propri e **gli stessi valori** (`hullK1: 4`, `backMax: 1.2`, `ironsA: 36`, `ironsU: 0.5`, `ironsYaw: 6`, `yawK: 4`), lasciando la formula com'è. Sono sei voci; quella dei 36° e quella dei 0,5 m/s vanno insieme ai 6 °/s, perché da soli non si capiscono. **[stima]** Il risultato in virgola mobile non cambia (stesse operazioni sugli stessi numeri); lo conferma la non-regressione (§6, criterio 1).

**Non si spostano** [ipotesi]: lo sbandamento che frena (`motore.js:64`), i limiti dello scarroccio (`:70`), il ritardo del timoniere (`:77`), il lato opposto della scuffia a −45° (`gioco.js:703`, `regate.js:311`). Nessuno dei prossimi compiti li riguarda; si aggiungono quando servono, con la stessa regola.

**Valori che il laboratorio mostra** (tutti gli altri restano come sono): `hullK1`, `hullK2`, `hullK4`, `rudderDragK`, `turnLen`, `maxRudder`, `yawK`, `backMax`, `ironsA`, `ironsU`, `ironsYaw`, `luffA0`, `luffW`, `mass`, `sailArea`. Sono quelli di velocità, virata, retromarcia e ripartenza. Gli altri valori di `BOAT` (sbandamento, scuffia, scotta) **non entrano** [ipotesi]: non servono ai prossimi compiti, e meno cursori vuol dire meno modi di rompere la barca senza accorgersene.

---

## 2. Profili

**Un profilo** è un elenco di valori diversi da `BOAT`, con un nome, la versione del gioco su cui è stato scritto e, **per ogni valore**, la fonte e lo stato («misura», «ipotesi», «non verificato»). Lo stato del profilo è il più debole fra i suoi valori, calcolato e non scritto a mano.

- **Il predefinito è `BOAT` stesso**, chiamato «come oggi (versione N)», con N letto da `VERSIONE` (`gioco.js:16`). Non può essere diverso dal gioco.
- **All'inizio c'è solo il predefinito.** I profili di saturazione del 13 ottobre non servono più (la saturazione è rimasta sul ramo `prova-saturazione`). Ogni profilo nuovo nascerà da un compito sulla barca, con le sue fonti: un profilo senza fonte non entra.
- **Dove:** in testa a `js/laboratorio.js`, fra due segni «PROFILI DEL LABORATORIO» e «FINE PROFILI». Un profilo nuovo si aggiunge incollando un blocco.
- **Controlli al caricamento:** una chiave che non esiste in `BOAT`, o un valore fuori dai limiti del §5, e il profilo non si carica (la finestra dice quale).
- **La versione si scrive come campo** (`versione: "1.0.4"`), mai come `const VERSIONE =`, perché `collaudo_versione.py` cerca la prima occorrenza di quella scritta in tutto il codice.

**Esportazione.** Un pulsante «esporta» scrive in un riquadro già selezionato (si copia con Ctrl+C) un profilo nel formato del file: versione, data e ora, valori diversi da `BOAT`. Ogni valore toccato a mano esce con fonte «prova a mano» e stato «non verificato»: così un numero provato col cursore non diventa mai un profilo con una fonte che non ha. Se il registratore è acceso, il testo esportato finisce anche nel file della sessione.

**Tolti dalla stesura del 13 ottobre** (si aggiungono se servono): l'avviso di versione diversa (con un solo profilo non serve; la versione si vede accanto al nome), i valori derivati sul raggio di virata (erano per la saturazione), il caricamento di un profilo incollato nella pagina (si incolla nel file).

---

## 3. Niente salvataggi con `#lab`

**[codice]** Tutto quello che il gioco salva passa da tre punti:
- `saveProgress()` (`gioco.js:156`): lezioni, prove, regate, piazzamenti, quiz, esame, brevetto, nome dell'attestato;
- `saveGhosts()` (`regate.js:10`): fantasmi;
- la scelta fra gioco libero e carriera (`gioco.js:251`), che non dipende dalla barca.

**Proposta:** con `#lab`, `saveProgress()` e `saveGhosts()` escono subito (una condizione per riga). I progressi si **leggono** come sempre, così il menu e i lucchetti della carriera restano quelli del giocatore; quello che si fa durante la sessione resta in memoria e sparisce ricaricando la pagina.

Rispetto al 13 ottobre è più semplice e più sicuro: lì si proponeva di bloccare sei punti uno per uno, e il predefinito salvava. **Prezzo:** con `#lab` nemmeno un giro con la barca di oggi lascia un record. Per giocare «davvero» si toglie `#lab`.

**Avviso** sopra il mare, in HTML e non sul canvas: «LABORATORIO · *profilo* · niente salvataggi». Si vede anche nel menu.

---

## 4. Finestra, tasti e registratore

- **Finestra** creata da `laboratorio.js` solo con `#lab`, assente dall'HTML del gioco. **Non modale**, fissa sopra il mare, così si vede la barca reagire mentre si sposta un cursore; il gioco **non si ferma** [ipotesi]. Si apre e si chiude con il tasto **L**: [codice] il gestore dei tasti (`gioco.js:588-600`) usa W, S, R, Q, le frecce e lo spazio; il registratore usa M (`registratore.js:168`). L è libero.
- **Frecce.** [codice] Il gestore dei tasti per le frecce esclude solo i `SELECT` (`gioco.js:596`): un cursore con il fuoco si muoverebbe **e** girerebbe la barra. Si aggiunge una condizione alla riga 590: tasti ignorati quando il fuoco è dentro la finestra del laboratorio.
- **Pannello e menu non cambiano**, quindi nemmeno la misura a 1360×650.
- **Registratore.** [codice] La testata scrive le impostazioni da `sesSet()` (`registratore.js:17` e `:128`) e ogni cambio diventa una riga `C` con il tempo (`:81-82`). Con `#lab`, `sesSet()` aggiunge `profilo=<nome>` (o `<nome>+modificato`) e i valori diversi da `BOAT`; senza `#lab` la stringa resta identica. Così ogni registrazione dice con quale barca è stata fatta, e ogni cursore mosso lascia una riga col tempo.
- **Collaudi.** [codice] L'aggancio dei collaudi si attiva con `location.hash === "#collaudo"` (`avvio.js:25`). Per poter guidare la barca nel laboratorio serve un indirizzo che accenda tutti e due: si propone `#collaudo-lab`, accettato sia dall'aggancio sia dal laboratorio. Le pagine con `#collaudo` o senza niente restano come oggi.
- **Ordine dei file.** `laboratorio.js` va dopo `avvio.js`, così vede tutto (`BOAT`, `VERSIONE`, `opt`, il registratore). Senza `#lab` non fa niente. Le due righe in `saveProgress()` e `saveGhosts()` leggono l'indirizzo direttamente, non una variabile del laboratorio, così funzionano anche se il file mancasse.

---

## 5. Limiti dei cursori

**Dalla 1.0.6** i cursori `hullK1`, `hullK2`, `hullK4` non ci sono più: la resistenza dello scafo è una tabella della vasca, e il laboratorio ha `hullScale` (da 0,5 a 2,5) e `appDA` (da 0 a 0,01 m²). Limiti rimisurati sulla barca nuova: nessun conto in errore (`PROPOSTA-VELOCITA.md`, criterio 7); esempi aggiornati in `LABORATORIO-GUIDA-AI-VALORI.md`.

I limiti sono **scelte nostre di prudenza**: servono a non rompere i conti, non dicono cosa è plausibile. Quelli della stesura del 13 ottobre erano misurati sul ramo con la saturazione: **alla fermata 2, prima di scrivere la finestra, si rimisurano tutti su `main`** con lo stesso metodo (ogni valore al minimo e al massimo, gli altri come oggi, passo 1/240 s e 0,0125 s: polare a 10 nodi a 45°, 90° e 180°, virata col pilota a 10 nodi, raffica da 10 a 18 nodi, conti andati in errore), e la tabella va nel rapporto.

| Valore | Oggi | Min | Max | Vincolo del codice |
|---|---|---|---|---|
| `mass` | 135 kg | 90 | 250 | più di 0 (divisione, `motore.js:65`) |
| `sailArea` | 7,0 m² | 4 | 10 | 0 o più |
| `hullK1` | 4 | 0 | 12 | 0 o più |
| `hullK2` | 12 | 4 | 30 | 0 o più |
| `hullK4` | 0,9 | 0 | 3 | 0 o più |
| `rudderDragK` | 45 | 0 | 120 | 0 o più |
| `turnLen` | 1,05 m | 0,5 | 2,0 | più di 0 (divisione, `:83`) |
| `maxRudder` | 30° | 15 | 45 | più di 0; cambia anche il disegno della barra (`disegno.js:424`) |
| `yawK` | 4 /s | 1 | 10 | più di 0; con `yawK × passo` oltre 1 la formula è già limitata dal `min(1, …)` |
| `backMax` | 1,2 m/s | 0 | 2,0 | 0 o più |
| `ironsA` | 36° | 25 | 45 | — |
| `ironsU` | 0,5 m/s | 0,1 | 1,0 | più di 0 (divisione, `:85`) |
| `ironsYaw` | 6 °/s | 0 | 15 | 0 o più |
| `luffA0` | 27° | 15 | 33 | `luffA0 + luffW` al massimo 40, cioè `IRONS_A` (`gioco.js:383`) e i 40° delle lezioni |
| `luffW` | 7° | 2 | 15 | più di 0 (divisione, `:57`) |

**Avvertenze nella finestra, accanto al cursore:** `turnLen` e `maxRudder` cambiano anche la marcia indietro; `luffA0` e `luffW` cambiano quando la vela si sgonfia, quindi anche i filetti e i messaggi dell'angolo morto; `ironsA` sopra `luffA0 + luffW` vuol dire che la prua poggia da sola anche con la vela che porta.

---

## 6. Criteri della fermata 2

Soglie dichiarate adesso, come attese nostre.

1. **Non-regressione del motore:** `polare.js` e `raffiche_e_virate.js` identici carattere per carattere dopo lo spostamento dei sei numeri in `BOAT`.
2. **Gioco identico senza `#lab`:** `collaudo_impronta.py` identico al bit, 63 scene su 63, riferimento preso dalla 1.0.3 appena prima.
3. **Niente salvataggi con `#lab`:** con `#collaudo-lab`, prova 1 completata col pilota e regata 1 finita, semi 1-5 ciascuna (10 corse): `localStorage` uguale byte per byte prima e dopo. **Contro-prova** con `#collaudo`, stesse corse: `localStorage` cambiato in tutte e 10 (altrimenti il criterio non ha misurato niente). Il collaudo dichiara quante corse ha finito davvero.
4. **Un cursore cambia la barca:** con `#collaudo-lab`, `hullK2` da 12 a 6, la velocità al traverso con 10 nodi dopo 30 s cresce di almeno il 5%; con il cursore riportato a 12 torna uguale entro 0,01 nodi.
5. **Frecce:** con il fuoco su un cursore, 10 pressioni di ← lasciano la barra a 0 **e** spostano il cursore (contro-prova che i tasti sono arrivati).
6. **Profili sbagliati:** una chiave inesistente e un valore fuori limite non si caricano (2 casi su 2).
7. **Esportazione:** il testo esportato, riletto come profilo, ridà gli stessi valori (3 profili con 1, 3 e 15 valori cambiati).
8. **Registratore:** con `#lab` la testata contiene `profilo=`; senza, `collaudo_registratore.py` passa invariato.
9. **Pagina vera:** aperta come la apre un giocatore, prima senza niente e poi con `#lab` (senza `#collaudo`): nessun errore della pagina; la finestra c'è solo con `#lab`.

Collaudo nuovo: `tests/collaudo_laboratorio.py` (criteri 3-9), con una voce in `lancia_tutti.sh` e in `COLLAUDI.md`.

---

## 7. Rischi

1. **Un valore cambiato a metà prova** rende il tempo senza senso. Non si salva comunque, e la riga `C` del registratore dice quando è successo.
2. **Un cursore che tocca più cose di quelle che dice il nome** (`turnLen`, `maxRudder`, `luffA0`): chi prova a mano attribuisce l'effetto alla cosa sbagliata. Lo coprono le avvertenze del §5.
3. **In regata il valore cambia anche gli avversari** (§1). Per le prove sulla barca conviene la navigazione libera.
4. **Un numero trovato a mano sembra una taratura.** Esce sempre «non verificato», e diventa un valore del gioco solo con un compito sulla barca, una fonte e le due fermate.
5. **Principio 5:** il laboratorio non compare nel menu e non sembra una funzione del gioco.

---

## 8. Decisioni che restano ad Ale

- Se con `#lab` non si salva **niente**, nemmeno con la barca di oggi (proposta), o se il predefinito deve salvare come nella stesura del 13 ottobre.
- Se il gioco continua mentre la finestra è aperta (proposta) o si ferma.
- Quando passare alla fermata 2.

---

## 9. Esito della fermata 2 (16 ottobre 2026, versione 1.0.4)

Via di Ale con le due proposte del §8: con `#lab` non si salva niente, e il gioco continua a finestra aperta.

**Scostamenti dalla proposta, dichiarati:**
- la condizione `LAB` sta in `base.js` (legge l'indirizzo, carica prima di tutto), non ripetuta nelle due funzioni di salvataggio: funziona anche senza `laboratorio.js`, come chiedeva il §4;
- `collaudo_impronta.py` ora si può importare (una riga), per riusarne i piloti di prova e regata nel collaudo nuovo.

**Criteri del §6:**

| Criterio | Esito |
|---|---|
| 1. Fisica identica | `polare.js`, `raffiche_e_virate.js` e anche `angolo_morto.js` identici carattere per carattere |
| 2. Gioco identico senza `#lab` | impronta `6d04cc5bd6d4` prima e dopo, 63 scene su 63, 0 diverse |
| 3. Niente salvataggi | 10 corse finite su 10, `localStorage` cambiato in 0; contro-prova 10 su 10, cambiato in 10 |
| 4. Il cursore cambia la barca | `hullK2` 12 → 6: da 4,88 a 5,59 nodi (+14%); di nuovo 12: 4,885 contro 4,885 |
| 5. Frecce | col fuoco sul cursore: barra 0, cursore da 1,05 a 0,5; contro-prova sul mare: barra −0,67 |
| 6. Profili sbagliati | 3 su 3 rifiutati; uno giusto caricato |
| 7. Esportazione | 1, 3 e 15 valori riletti uguali; valore a mano «prova a mano», «non verificato» |
| 8. Registratore | `profilo=oggi+modificato hullK2=7` col laboratorio, niente senza; `collaudo_registratore.py` OK |
| 9. Pagina vera | senza niente e con `#lab`: 0 errori; finestra solo con `#lab`; il tasto L la nasconde |

**Difetto nel collaudo, trovato e corretto:** il primo giro dava il criterio 6 fallito, perché il caso «`luffA0` 33» con `luffW` 7 fa esattamente 40, che è permesso. Il controllo era giusto, il caso no: ora è 33 + 8.

**Limiti dei cursori, misurati sul motore della 1.0.4** (script fuori dal repository; ogni valore agli estremi, gli altri come oggi; vento 10 nodi). Polare a 45°/90°/180° con la scotta migliore; virata da 3,9 nodi con barra 0,8; sbandamento massimo con una raffica da 10 a 18 nodi senza reagire; angolo morto: barca ferma con la prua a 10° dal vento, scotta a metà, barra al centro (secondi prima di andare indietro oltre 0,5 nodi, velocità più bassa, prua dopo 10 s). «—» = non succede (virata non riuscita in 12 s, o mai all'indietro). Nessun conto in errore. I passi di 1/240 e 0,0125 s danno risultati uguali entro 0,1 s e 1°.

| Valore | Polare (nodi) | Virata | Raffica | Indietro dopo | Minimo | Prua a 10 s |
|---|---|---|---|---|---|---|
| **oggi** | 3,4 / 5,2 / 3,5 | 4,0 s | 41° | 1,8 s | −1,8 | 21° |
| `mass` 90 / 250 | uguale / uguale | 6,6 / 2,9 s | 41° / 41° | 1,2 / 3,3 s | −1,9 / −1,2 | 17° / 33° |
| `sailArea` 4 / 10 | 3,0/4,0/3,0 · 3,6/5,9/3,9 | 3,5 / 4,7 s | 23° / 62° | 3,3 / 1,2 s | −0,9 / −2,2 | 34° / 17° |
| `hullK1` 0 / 12 | 3,5/5,3/3,7 · 3,2/4,8/3,3 | 3,7 / 4,7 s | 41° / 40° | 1,7 / 1,9 s | −2,1 / −1,4 | 20° / 22° |
| `hullK2` 4 / 30 | 3,9/6,1/4,2 · 2,7/3,8/2,7 | 3,3 / 5,9 s | 42° / 40° | 1,7 / 1,8 s | −2,3 / −1,3 | 21° / 22° |
| `hullK4` 0 / 3 | 3,6/6,2/3,8 · 3,2/4,3/3,2 | 3,8 / 4,5 s | 41° / 40° | 1,8 s | −1,8 / −2,0 | 21° |
| `rudderDragK` 0 / 120 | uguale | 3,4 / 5,3 s | 41° | 1,8 s | −1,8 | 21° |
| `turnLen` 0,5 / 2 | uguale | 1,4 s / — | 41° | 1,8 s | −1,8 | 21° |
| `maxRudder` 15 / 45 | uguale | — / 2,5 s | 41° | 1,8 s | −1,8 | 21° |
| `yawK` 1 / 10 | uguale | 4,6 / 3,9 s | 41° | 1,7 / 1,8 s | −1,8 | 21° |
| `backMax` 0 / 2 | uguale | 4,0 s | 41° | — / 1,8 s | 0,0 / −1,8 | 38° / 21° |
| `ironsA` 25 / 45 | uguale | 4,0 s | 41° | 1,8 s | −1,8 | 21° / 21° |
| `ironsU` 0,1 / 1 | uguale | 4,0 / 3,8 s | 41° | 1,7 / 1,8 s | −1,9 / −1,2 | 12° / 33° |
| `ironsYaw` 0 / 15 | uguale | 4,0 s | 41° | 1,7 / 1,8 s | −1,9 / −1,1 | 10° / 36° |
| `luffA0` 15 / 33 | 3,8/5,2/3,5 · 2,1/5,2/3,5 | 3,3 / 4,9 s | 41° / 31° | 1,8 s | −1,5 / −1,8 | 22° / 21° |
| `luffW` 2 / 15 | 3,8/5,2/3,5 · 2,3/5,2/3,5 | 3,7 / 4,4 s | 41° / 30° | 1,8 s | −1,8 | 21° |

**Cosa si nota, senza giudicarlo** (lo faranno i compiti sulla barca, con le fonti):
- partendo ferma con la prua a 10° dal vento, la barca va all'indietro oltre mezzo nodo **dopo 1,8 s** e arriva a −1,8 nodi; il limite `backMax` (1,2 m/s, cioè 2,3 nodi) in questo caso non viene mai raggiunto, quindi per la retromarcia «che parte troppo presto» (Ale) contano di più altri valori;
- con la barra al centro la barca **non esce** dall'angolo morto in 30 s: la prua si ferma intorno ai 21°;
- `ironsA` fra 25 e 45 non cambia niente in questa prova; probabilmente il vento apparente resta sempre sotto i 25°, ma non l'ho misurato.
