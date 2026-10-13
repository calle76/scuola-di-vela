# Proposta: pannello «laboratorio» a profili con nome (Scuola di vela)

Del 13 ottobre 2026. **Proposta, fermata 1: nessun codice scritto.** Scritta in sola lettura: nessun file del repository modificato. Le righe citate sono di `index.html` sul ramo `prova-saturazione`, che ha in più la saturazione del timone (`rudderSat`, non committata): dopo la riga 379 i numeri sono +5 rispetto a `main`.

Tipi delle affermazioni:
- **[codice]** = letto nel codice, con file e riga;
- **[misura]** = verificato facendo girare il motore (copia in memoria, cartella temporanea);
- **[stima]** = ragionamento senza misura.

---

## 0. In breve

- **Cos'è.** Una finestra nascosta, attiva solo con `#lab` nell'indirizzo, per provare a mano valori diversi della barca **senza modificare il codice**.
- **Non cursori liberi, ma profili con nome.** Ogni profilo ha valori, fonte e stato. I cursori servono solo a ispezionare un valore e non salvano niente.
- **Con un profilo diverso dal predefinito:**
  - un avviso visibile;
  - nessun salvataggio di record, medaglie, fantasmi, «senza errori» e piazzamenti;
  - nome del profilo e valori nella testata del registratore.
- **Fattibile senza toccare il motore:** tutti i valori di `BOAT` si leggono a ogni passo.
- **Dimensione stimata:** circa 135-180 righe in `index.html`, più un collaudo nuovo di circa 80-120 righe.

---

## 1. Dove il motore legge i valori

- **[codice]** `BOAT` è dichiarato con `const` (righe 366-388), ma le sue proprietà si possono cambiare. Nessun punto le copia altrove all'avvio: ogni uso rilegge `BOAT.x` quando gira.
- **[codice]** `BOAT` sta dentro la funzione che contiene tutto il gioco (`(() => {`, riga 360), quindi dalla pagina non si raggiunge. Il laboratorio deve stare nello stesso file e nella stessa funzione.

| Dove si legge | Righe [codice] | Valori | Quando |
|---|---|---|---|
| `step()` | 411-446 | tutti quelli della tabella del §7, più `rho` | A ogni passo: 4 per fotogramma per il giocatore (riga 1446), 3 per gli avversari (riga 1810) |
| Filetti (`readI`) | 926 | `luffA0`, `luffW` | A ogni fotogramma |
| `autoSheet` | 936-937 | `minBoom`, `maxBoom` | A ogni fotogramma |
| Strambata violenta | 1419 | `minBoom`, `maxBoom` | A ogni fotogramma |
| Scuffia del giocatore | 1450 | `capsizeAt` | A ogni fotogramma |
| Scuffia degli avversari | 1812 | `capsizeAt` | A ogni fotogramma |
| Scotta degli avversari | 1794-1795 | `minBoom`, `maxBoom` | A ogni fotogramma |
| Disegno della barra | 2437 | `maxRudder` | A ogni disegno |

- **[codice]** Un valore cambiato ha effetto al passo successivo.
- **[stima]** Per una misura pulita conviene ripartire, perché un tempo fatto con due fisiche non vale niente. Proposta: un pulsante «applica e ricomincia».
- **[codice] Numeri scritti nelle formule, che un profilo non può cambiare:**
  - in `step()`:
    - resistenza `4·u` (riga 421);
    - aumento della resistenza con lo sbandamento, 30° e 0,6 (riga 423);
    - marcia indietro massima −1,2 m/s (riga 425);
    - scarroccio, 0,4 e 60 (riga 428);
    - ritardo del timoniere, 0,9 s (riga 436);
    - prua che poggia da sola, 36°, 0,5 m/s e 6 °/s (riga 448);
    - inseguimento della rotazione `dt*4` (riga 449);
    - curve `CL` e `CD` (righe 390-395);
  - fuori da `step()`:
    - `IRONS_A` (riga 1133);
    - orziera e onde (riga 1429);
    - strambata violenta a 45° (riga 1419);
    - `GYBE_KICK`: è una variabile, ma si cambia solo con `__sv.kick`, cioè solo con `#collaudo` (riga 2827).
- **[codice]** Il passo di tempo per fotogramma arriva al massimo a 0,05 s (riga 2807). Quindi 0,0125 s per ogni passo del motore del giocatore e 0,0167 s per gli avversari. Serve per i limiti di stabilità del §7.

---

## 2. Struttura dei profili

**Cosa contiene un profilo** (proposta nostra):

| Campo | Contenuto |
|---|---|
| `id` | Nome breve senza spazi, per esempio `sat24`. Va nella testata del registratore |
| `nome` | Nome leggibile, per esempio «Saturazione 24°» |
| `barca` | Per ora una sola: «deriva singola da scuola», quella di `BOAT` |
| `versione` | La versione del gioco su cui il profilo è stato scritto, per esempio 0.21.2 |
| `valori` | **Solo le differenze** dalla barca di base |
| Per ogni valore: `fonte` | Documento e riga, oppure «scelta di progetto», oppure «senza fonte» |
| Per ogni valore: `stato` | «misura»: c'è un dato misurato e citato. «ipotesi»: scelta nostra dichiarata. «non verificato»: nessuno l'ha controllato |
| `nota` | Una frase: cosa si vuole provare |

- **Fonte e stato vanno per ogni valore**, perché un profilo mescola valori con fonti diverse. Lo stato del profilo intero è il **più debole** fra i suoi valori, calcolato e non scritto a mano.
- **Il predefinito non è scritto da nessuna parte: è `BOAT` stesso.** Il pannello lo chiama «come oggi (versione N)», leggendo `VERSIONE` (riga 869). Così non può essere diverso da quello che usa il gioco.
- **Sul ramo** «come oggi» ha `rudderSat` 15, quindi **non è** la 0.21.2. Per confrontare serve il profilo «come 0.21.2, senza saturazione» (§9).
- **Controlli quando si carica un profilo:**
  - una chiave che non esiste in `BOAT` → il profilo non si carica e il pannello dice quale riga è sbagliata;
  - valori fuori dai limiti del §7 → non si carica;
  - `rudderSat` più grande di `maxRudder` → non si carica.

**Dove scriverli.** Consiglio **una sezione propria in `index.html`**, con segni di inizio e fine («PROFILI DEL LABORATORIO» … «FINE PROFILI»), **fuori dal blocco del motore** (righe 361-455).

| Possibilità | Pro | Contro |
|---|---|---|
| **Sezione in `index.html`** (consigliata) | Resta un file solo (`PROGETTO.md`). Un profilo nuovo si aggiunge incollando un blocco di testo. Fuori dal blocco del motore, i collaudi della fisica non lo vedono | Il file cresce di qualche riga per profilo |
| File a parte, `profili.js`, caricato con `<script>` | Si cambiano i profili senza aprire `index.html` | Due file da distribuire. **[stima]** Un JSON caricato con `fetch` non funzionerebbe aprendo la pagina da disco (`file://`); uno script invece sì |

In futuro i collaudi in Node potrebbero leggere i profili come leggono il motore: `tests/fisica/motore.js` taglia il testo fra due segni. Per questo i segni servono già adesso.

**Un profilo per ogni barca, in futuro.** Il campo `barca` raggruppa i profili per barca. **Limite:** un profilo cambia solo i numeri che il motore già usa. Una barca diversa ha bisogno prima di un motore e di un disegno che la reggano:
- con il fiocco: `sperimentale/fiocco.html`;
- con due persone: un altro modello del timoniere;
- con un'altra lunghezza: un altro disegno (`hullPath`, righe 2516-2522, fisso a 4,2 m).

---

## 3. localStorage: dove si scrive e cosa bloccare

| Riga [codice] | Cosa scrive | Dipende dalla fisica? |
|---|---|---|
| 958 | `saveProgress()`, la funzione che salva tutto | — |
| 1503-1505 | Record della prova, «senza errori», fantasma | Sì |
| 1537 (`recSave`), 1523 (`saveGhosts`) | Fantasma | Sì |
| 1889-1891 | Record della regata, «pulita», fantasma | Sì |
| 1903 | Piazzamento della regata | Sì |
| 1226 | Lezione completata | **[stima]** In parte |
| 1067 | Record del quiz | No |
| 1012 | Azzeramento a mano | No |
| 1524 | Cancellazione delle chiavi della 0.19 | No |

- **[codice]** Il registro degli errori (`reg`, `regAdd` alla riga 1141) non va mai in localStorage da solo: entra solo come «senza errori» e «pulita» (righe 1505, 1891, 1903).
- **[codice]** Le impostazioni (`opt`, riga 860) non si salvano.
- **Proposta:** una condizione unica, «profilo diverso dal predefinito, o predefinito modificato con un cursore». Quando è vera si saltano le righe 1503-1505, 1537, 1889-1891 e 1903 **prima** di toccare `progress` in memoria. Bloccare solo `saveProgress` lascerebbe il record in memoria per tutta la sessione, e il menu lo mostrerebbe.
- Profili e valori del laboratorio non si salvano: ricaricando la pagina si torna al predefinito.

---

## 4. Avviso e registratore

**Avviso visibile:**
- un'etichetta fissa sopra il mare, fuori dal pannello e fuori dal canvas, per esempio «LABORATORIO · *nome* · niente record»;
- si vede anche nel menu;
- a fine prova o regata il testo aggiunge «(laboratorio: non salvato)».

**Il registro degli errori** continua a contare e a mostrarsi, perché serve a capire la prova; non si salva per costruzione (§3).

**Registratore** [codice]:
- la testata scrive «impostazioni all'inizio» da `ses.set0` (righe 2730 e 2749), che viene da `sesSet()` (righe 2637-2639);
- quando `sesSet()` cambia, il registratore scrive una riga `C` con il tempo (righe 2701-2702).

**Proposta:**
- con `#lab`, `sesSet()` aggiunge `profilo=<id>` (oppure `<id>+modificato`) e i valori diversi dalla base;
- così finiscono nella testata, e ogni cambio di profilo o di cursore diventa una riga `C`;
- senza `#lab` la stringa resta identica a oggi;
- `analizza_sessione.py` non legge il contenuto delle righe `C` [codice, righe 36-56].

---

## 5. Posizione, tasto L e filtro delle frecce

- **[codice]** Il pannello normale è l'`<aside class="panel">` della riga 277 (stile alle righe 80 e 211). Le impostazioni sono il `<dialog id="setDlg">` della riga 228.
- **Proposta:**
  - una finestra **creata da JavaScript solo con `#lab`**, assente dall'HTML del gioco normale;
  - **non modale**, in posizione fissa sopra il mare, così si vede la barca reagire;
  - l'avviso del §4 come elemento a parte.
- **[codice]** Il gestore dei tasti (righe 1335-1346) usa `KEYSEM`, R, Q, le frecce e lo spazio; L non compare. **[stima]** Il tasto M del registratore sta altrove: va controllato che L sia davvero libero.
- **[codice] Problema delle frecce.** Il gestore si ferma solo con le finestre del gioco aperte o con il fuoco in un campo di ricerca (riga 1337). Per le frecce esclude solo i `SELECT` (riga 1343). Quindi un cursore con il fuoco, premendo ← o →, si muove **e** muove la barra. Il gestore deve ignorare i tasti quando il fuoco è dentro il laboratorio.
- **[stima]** Così non cambiano né l'altezza del pannello a 1360×650 né il menu.

---

## 6. Cursori di ispezione ed esportazione

- I cursori partono dai valori del profilo. Muovendone uno, il profilo diventa «*nome* + modificato» e la barca usa subito il valore nuovo.
- **Non si salva niente.**
- **Pulsante «esporta come testo»:** produce un blocco già nel formato dei profili scritti, da incollare in una conversazione o nella sezione dei profili. Contiene:
  - `versione` (letta da `VERSIONE`), data e ora;
  - profilo di partenza;
  - i valori, con fonte e stato copiati dal profilo di partenza;
  - per ogni valore toccato a mano: fonte «ispezione a mano», stato «non verificato».

  Così un valore provato a mano non diventa mai un profilo con una fonte che non ha.
- Il testo esce in un riquadro già selezionato, da copiare con Ctrl+C. **[stima]** Non sono sicuro che la copia automatica negli appunti funzioni aprendo la pagina da disco.
- Se il registratore è acceso, il testo esportato finisce anche nel file della sessione.

---

## 7. Limiti dei cursori

**Come ho verificato [misura].** Ogni valore al minimo e al massimo, con tutti gli altri come oggi, a passo 1/240 s e al passo più lungo possibile (0,0125 s; alcuni anche 1/60). Ho misurato:
- la polare a 10 nodi a 45°, 90° e 180° dal vento;
- la virata col pilota a 10 nodi;
- una raffica improvvisa da 10 a 18 nodi di bolina, senza reagire (oggi 41°);
- la comparsa di NaN, cioè conti andati in errore.

Valori di oggi sul ramo: polare 3,4 / 5,2 / 3,5 nodi; virata 3,6 s; raffica 41°.

Nella colonna «Tipo»: «motore» vuol dire che oltre quel valore il codice si rompe o dà numeri senza senso; «prudenza» vuol dire che è una scelta nostra.

| Valore | Oggi | Min | Max | Passo | Tipo e motivo | Verifica |
|---|---|---|---|---|---|---|
| `mass` | 135 kg | 90 | 250 | 5 | **Motore:** più di 0, a 0 NaN (riga 424). **Prudenza:** la massa entra solo nell'accelerazione, non nella resistenza né nel rollio. La polare non cambia; la virata sì (5,4 s a 90, 2,9 s a 250) | Motore girato |
| `sailArea` | 7,0 m² | 4 | 10 | 0,1 | **Motore:** 0 o più (a 0 la barca sta ferma, riga 415). **Prudenza:** a 10 la raffica fa scuffiare (62°) | Codice e motore girato |
| `hullK2` | 12 | 4 | 30 | 1 | **Motore:** 0 o più (riga 421). **Prudenza:** traverso a 6,1 nodi con 4, 3,8 con 30 | Motore girato |
| `hullK4` | 0,9 | 0 | 3 | 0,1 | **Motore:** 0 o più; a 0 limita `hullK2` (traverso a 6,2 nodi). **Prudenza:** a 3, traverso a 4,3 nodi | Motore girato |
| `rudderDragK` | 45 | 0 | 120 | 5 | **Motore:** 0 o più. **Prudenza:** virata 3,1 s con 0, 4,8 s con 120 | Motore girato |
| `foilK` | 520 | 150 | 1200 | 10 | **Motore:** 0 o più, il denominatore ha +60 (riga 428). **Prudenza:** con 150 la bolina scende a 3,0 nodi | Codice e motore girato |
| `minBoom` | 14° | 0 | 30 | 1 | **Motore:** deve restare **sotto** `maxBoom`, altrimenti divisione per zero in `autoSheet` (riga 937) e nella scotta degli avversari (riga 1795): NaN con 14 e 14. **Prudenza:** almeno 10° di differenza; con 30 la bolina scende a 2,4 nodi | Motore girato |
| `maxBoom` | 85° | 60 | 90 | 1 | **Motore:** sopra `minBoom`. **Prudenza:** il commento del suggerimento in poppa (riga 2051) dà per scontato 85°; con 60 poppa a 3,3 nodi; oltre 90° senza senso fisico | Motore girato (60 e 90); oltre 90 stima |
| `luffA0` | 27° | 15 | 33 | 1 | **Prudenza:** `luffA0 + luffW` al massimo 40, cioè `IRONS_A` (riga 1133) e i 40° scritti nelle lezioni. Con 33: bolina 2,1 nodi, virata 10,1 s. Con 40 e 10: bolina 0,4 nodi, virata fallita | Codice e motore girato |
| `luffW` | 7° | 2 | 15 | 1 | **Motore:** più di 0 (divisione alla riga 416): con 0 NaN quando il vento apparente vale esattamente `luffA0`, mai capitato nelle prove. **Prudenza:** con 15, bolina 2,3 nodi e virata 6,7 s | Codice (NaN non osservato) e motore girato |
| `turnLen` | 1,05 m | 0,5 | 2,0 | 0,05 | **Motore:** più di 0, a 0 NaN (riga 446). **Vale anche all'indietro:** cambia l'uscita dall'angolo morto. **Prudenza:** virata 1,8 s con 0,5, 9,6 s con 2,0 | Motore girato |
| `maxRudder` | 30° | 15 | 45 | 1 | **Motore:** più di 0. **Vincolo:** `rudderSat` non sopra `maxRudder`. **Prudenza:** virata 8,8 s con 15, 2,5 s con 45; cambia anche il disegno della barra (riga 2437) | Motore girato |
| `rudderSat` | 15° | 5 | `maxRudder` | 1 | **Motore:** più di 0, a 0 NaN (riga 444). Non sopra `maxRudder`: con 30 e `maxRudder` 20 la virata passa da 3,6 a 9,8 s. **Prudenza:** con 5, virata 3,3 s | Motore girato |
| `zCE` | 2,0 m | 1,2 | 3,0 | 0,1 | **Motore:** nessun limite (riga 433). **Prudenza:** con 3,0 la raffica fa scuffiare (65°); con 1,2, 24° | Motore girato |
| `sailorMass` | 75 kg | 40 | 120 | 5 | **Motore:** più di 0, divisione per `rmMax` alla riga 435 (NaN possibile, non osservato a 0). **Prudenza:** con 40 la raffica arriva a 54° | Codice e motore girato |
| `hikeArm` | 1,0 m | 0,3 | 1,5 | 0,05 | Come `sailorMass`. **Prudenza:** con 0,3 la raffica fa scuffiare (62°) | Codice e motore girato |
| `formK` | 400 Nm | 300 | 1000 | 20 | **Motore:** a 0 nessun errore ma risultato senza senso: in poppa 0 nodi, scuffia anche senza raffica. **Prudenza:** raffica a 72° con 100, 60° con 200, 46° con 300 | Motore girato |
| `rollI` | 260 | 80 | 600 | 10 | **Motore:** più di 0, a 0 NaN (riga 438). Stabilità del passo: `rollDamp / rollI × passo` sotto 2, quindi `rollDamp` sotto circa 120 volte `rollI` (stima dalla formula). Un punto provato: 9000 e 80 a passo 1/60, stabile | Motore girato e stima |
| `rollDamp` | 520 | 300 | 1500 | 20 | **Motore:** 0 o più, più il vincolo di stabilità sopra. **Prudenza:** raffica a 80° con 100, 62° con 200, 52° con 300, 46° con 400; con 1500, 25° | Motore girato |
| `capsizeAt` | 60° | 30 | 80 | 1 | **Motore:** oltre 90° senza senso, perché il momento raddrizzante usa sin 2φ (riga 437); a 95 nessun errore nelle prove. Il lato opposto resta −45°, scritto nel codice (righe 1450 e 1812). **Prudenza:** con 30 la raffica fa scuffiare | Codice e motore girato |

Nei limiti proposti, i due passi di tempo (1/240 e 0,0125 s) danno risultati uguali entro 0,1 s e 1° [misura]: nessuna instabilità numerica. Minimi, massimi e passi sono **proposte nostre**.

---

## 8. Valori derivati e avviso di versione

**Valori derivati, in sola lettura accanto ai cursori.** Fattibile.

- **Guadagno a barra piccola** = sin(`maxRudder`) / sin(`rudderSat`). Non sin 30° / sin(`rudderSat`): coincidono solo con `maxRudder` a 30 [codice, riga 444].
- **Raggio minimo in avanti** = `turnLen` / sin(`maxRudder`).
  - Con la saturazione **non dipende da `rudderSat`**, perché a barra tutta la rotazione è quella di `maxRudder`. Oggi vale 2,1 m con tutti i profili del §9.
  - Più utile: il **raggio a metà barra** = `turnLen` / (sin(min(`maxRudder`/2, `rudderSat`)) × guadagno).
- **Righe** [stima]: circa 8-12.
- **Collaudi:** nessun rischio se i numeri stanno nella finestra del laboratorio, e non nel pannello o sul canvas.

**Avviso se la versione del profilo è diversa da `VERSIONE`** (riga 869). Fattibile.

- **Righe** [stima]: circa 4-6.
- **[codice] Avvertenza:** `collaudo_versione.py` cerca la **prima** occorrenza di `const VERSIONE = "…"` (riga 27 del collaudo). I profili devono scrivere la versione come campo (`versione: "0.21.2"`), **mai** come `const VERSIONE =`.
- **[codice]** Lo stesso collaudo controlla «V. » + versione nel menu (`.ver`, riga 991) e sul mare: l'avviso non deve stare né lì né sul canvas.

---

## 9. Profili iniziali

Ogni profilo scrive solo le differenze; tutti gli altri valori sono quelli di `BOAT`.

**Fonte comune dei valori di `BOAT`:** `docs/FISICA-E-TARATURE.md:3` («tarati per essere plausibili, non ricavati da misure») e la tabella alle righe 22-35. **Stato: ipotesi (taratura).**

| Profilo | Valori diversi da `BOAT` | Fonte | Stato |
|---|---|---|---|
| «Come oggi» (predefinito; il nome legge `VERSIONE`) | Nessuno. Sul ramo vuol dire `rudderSat` 15, su main la barca della 0.21.2 | `rudderSat` 15: F4, un solo 470 (`docs/FONTI-PUBBLICHE.md:20` e `:54`), più scelta di progetto. Gli altri: tabella di `FISICA-E-TARATURE.md` | Ipotesi |
| «Come 0.21.2, senza saturazione» | `rudderSat` 30 | Scelta di progetto: equivale alla formula della 0.21.2 | Misura: `polare.js`, `raffiche_e_virate.js` e `angolo_morto.js` **identici a main carattere per carattere** |
| «Saturazione 20°» | `rudderSat` 20 | F4 (un solo 470) più scelta di progetto | Ipotesi |
| «Saturazione 24°» | `rudderSat` 24 | F4 (un solo 470) più scelta di progetto | Ipotesi |

**Il 20° ha senso? Solo come punto intermedio per la prova a mano** [misura, sweep del 13 ottobre]. In ogni misura sta fra il 18° e il 24°, senza un comportamento suo:

| Misura | main | 15° | 18° | 20° | 24° |
|---|---|---|---|---|---|
| Prua minima con il colpo fisso da 0,7 s (il passo 5.2 chiede almeno 43°) | 51,9° | 32,6° | 37,2° | 39,9° | 45,0° |
| Collaudo della lezione 5 | OK | ✘ | ✘ | ✘ | OK |
| Cambi di barra nella rotta (mediana) | 2 | 12 | 8 | 7 | 4 |
| Griglia di 84 virate a 10 nodi, miglior barra | 66 | 71 | 71 | 70 | 70 |
| Aggressiva | — | nel rumore | nel rumore | nel rumore | nel rumore |

- Il passaggio della lezione 5 sta **fra 20° e 24°**; un valore come 22° non l'ho misurato.
- Se a mano 24° sembra giusto e 15° troppo nervoso, il 20° aiuta a capire dove sta il limite. Altrimenti si può togliere.
- Costa 4-5 righe.

---

## 10. Collaudi

**[codice]** L'aggancio dei collaudi controlla l'indirizzo con un'uguaglianza esatta, `location.hash === "#collaudo"` (riga 2819). Nessun collaudo legge `BOAT` (cercato in `tests/*.py`: zero risultati). Se il laboratorio esiste solo con `#lab`, i collaudi non lo vedono. I rischi:

| Rischio | Collaudi che lo scoprirebbero [codice] | Come evitarlo |
|---|---|---|
| Codice del laboratorio dentro il blocco del motore (righe 361-455) | `polare.js`, `raffiche_e_virate.js`, `angolo_morto.js`: `tests/fisica/motore.js` estrae proprio quel blocco | Laboratorio e profili fuori dal blocco |
| Condizione «niente salvataggi» vera anche senza `#lab` | `collaudo_registro.py`, `collaudo_linea.py`, `collaudo_competizione.py`, `collaudo_fantasma.py` | Falsa per costruzione senza `#lab` |
| `sesSet()` diverso senza `#lab` | `collaudo_registratore.py` | Campo aggiunto solo con `#lab` |
| Testo disegnato sul mare | `collaudo_versione.py`, `collaudo_vista.py` | Avviso in HTML, non sul canvas |
| Pannello più alto | `collaudo_pannello.py` | Finestra separata |
| Versione scritta come `const VERSIONE =` in un profilo | `collaudo_versione.py` | Versione come campo del profilo |

**Collaudo nuovo** [stima], con la pagina aperta su `#lab`. Deve verificare:
1. con un profilo diverso dal predefinito, la prova 1 completata non scrive in localStorage (il collaudo dichiara quante prove ha misurato);
2. con il predefinito il record si salva;
3. senza `#lab` la finestra non esiste;
4. le frecce su un cursore non muovono la barra;
5. un profilo scritto male non si carica;
6. un profilo esportato e reincollato ridà gli stessi valori;
7. la testata del registratore contiene il nome del profilo;
8. un profilo con una versione diversa mostra l'avviso.

---

## 11. Dimensione e rischi

**Dimensione** [stima]: circa 135-180 righe in `index.html`.
- finestra e cursori: circa 40;
- stile: circa 10;
- condizione e punti di salvataggio: circa 10;
- `sesSet()`: circa 2;
- tasto e filtro delle frecce: circa 5;
- pulsanti: circa 10;
- profili: circa 15-25;
- lettura e controlli dei profili: circa 20;
- esportazione: circa 15;
- avviso: circa 5;
- valori derivati: circa 8-12;
- avviso di versione: circa 4-6.

A questo si aggiungono il collaudo nuovo (circa 80-120 righe) e le voci in `COLLAUDI.md` e `CHANGELOG.md`.

**Rischi:**
1. **Un punto di salvataggio dimenticato:** un record fatto con una fisica diversa resta per sempre. Lo copre il collaudo del §10.
2. **Frecce che muovono barra e cursore insieme:** un difetto silenzioso. Lo coprono il filtro e il collaudo.
3. **Misure mescolate:** un valore cambiato a metà prova rende il tempo senza senso. Lo coprono «applica e ricomincia» e la riga `C` del registratore.
4. **`turnLen` e `maxRudder` toccano anche l'indietro e il disegno:** chi prova a mano può attribuire alla saturazione un effetto che viene da altro. Il pannello lo dice accanto al cursore.
5. **Un profilo con una fonte sbagliata sembra autorevole.** Per questo fonte e stato vanno per valore, e i valori toccati a mano escono sempre «non verificato».
6. **Il predefinito sul ramo è diverso dalla 0.21.2:** «come oggi» vuol dire «come questo `index.html`».
7. **Principio 5 del progetto:** il laboratorio è uno strumento di prova. Non deve comparire nel menu né sembrare una funzione del gioco.

---

## 12. Decisioni che restano ad Ale

- Profili in una sezione di `index.html` o in un file a parte.
- Se il profilo «Saturazione 20°» resta, o si prova invece un 22°.
- Se i limiti dei cursori del §7 vanno bene, o se ne vuole di più stretti.
- Se bloccare anche il salvataggio delle lezioni completate (riga 1226).
- Il tasto per aprire la finestra: L, dopo aver verificato che sia libero.
- Se il gioco continua mentre la finestra è aperta, o si ferma.
- Se il raggio derivato si mostra a barra tutta, a metà barra o in tutti e due i modi.
- Se l'avviso di versione diversa blocca il profilo o lo segnala soltanto.
- Se il laboratorio entra in una versione del gioco o resta su un ramo di prova.
- Quando passare alla fermata 2 (implementazione).
