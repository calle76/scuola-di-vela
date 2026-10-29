# Proposta: modalità coach e registratore (fermata 1, 29 ottobre 2026)

Nessun codice. Riunisce e sostituisce `PROPOSTA-MOVIOLA.md` (ritirata come proposta a sé: la moviola è una parte del coach) e dà seguito a `PROPOSTA-REGATA-COME-FONTE.md` §10 e a `DECISIONI.md` («Modalità coach», 27 ottobre). Idea di Ale del 29 ottobre: la modalità coach serve a più cose, tutte costruite sulle regate registrate.

> **Stato (29 ottobre 2026):** per decisione di Ale («se non costa nulla falla») la parte «rivedere» è già fatta nella 1.0.58 in forma ridotta: tasto O o contatto → spezzone di 18 s in memoria → «Rivedi» a fine regata. **Fase 1 fatta nella 1.0.60** (registrazione automatica, un file per regata, a pezzi da 5 minuti, dal conto alla rovescia all'arrivo, ultime 5 regate in IndexedDB; misure nel `CHANGELOG.md`). Restano il momento clou automatico (fase 2), la domanda sulla penalità (3) e il passo da ripetere (4).
>
> **Cambiamenti rispetto a questa proposta (idee di Ale del 29 ottobre):** si registra anche prima del via (da −180 s); il file è a pezzi, il primo fino a 120 s di regata e poi 300 s, ciascuno con intestazione e un fotogramma in comune; il criterio 4 diventa «sotto 2 MB **per pezzo**» (misurato: massimo 0,56 MB); nessun seme nell'intestazione, perché il gioco non ne ha.

## A cosa serve (parole di Ale, 29 ottobre 2026)
1. **Il momento clou** della regata: una scena carina da rivedere a fine regata (sorpasso, contatto, giro di boa).
2. **Nei livelli con meno lezioni**, il coach vale come lezione e pratica:
   - una **domanda su una penalità assegnata** («perché la Rossa ha preso la penalità?») con la scena da rivedere;
   - un **passo da ripetere** nelle stesse condizioni *ma non esatte*: «ripetiamo questa situazione: sorpasso, virata, giro boa». Nella realtà non sarebbe mai identica.
3. **Debugging:** le registrazioni raccolte Ale me le manda, una regata per file.

## Il principio nuovo: ripetere una situazione, non rigiocare una copia
La ripetizione **non** ricarica lo stato registrato. Dalla registrazione si ricava una *descrizione della situazione* (tipo: sorpasso, virata, giro di boa, partenza; mure, distanze, angolo e forza del vento, barche coinvolte) e il gioco ne costruisce una **nuova** dello stesso tipo, con variazioni dentro margini dichiarati:
- vento: direzione ±5-8°, forza ±1 nodo, raffiche e salti con un seme nuovo;
- onde e disturbi sulla barca (`yawNoise`): seme nuovo, mai uguali;
- posizioni delle barche: qualche metro in più o in meno, stesse mure e stesso tipo di conflitto;
- gli avversari reagiscono alle tue scelte (nessuna copia dei loro movimenti).
Così non serve l'«istantanea completa» che il §E temeva (stato nascosto in funzioni, generatore casuale): basta saper *costruire* la situazione. Il rischio si sposta: bisogna che la situazione nuova insegni la stessa cosa.

## Fasi (ognuna una fermata 2 a parte, ognuna con il via di Ale)
1. **Registrazione ricca**, un file per regata, che parte e si ferma da sola (scelta già presa il 27 ottobre). Campioni più fitti della riga al secondo di oggi (10 al secondo per le posizioni di tutte le barche, ipotesi nostra), più gli eventi con il motivo. Non tocca il motore né `Math.random` (come il registratore di oggi).
2. **Momento clou:** scelta automatica dell'evento più significativo (punteggio sugli eventi: contatto, penalità, sorpasso, giro di boa) e riproduzione di 10-15 s, anche rallentata (½×, ¼×), con la grafica del gioco, dopo l'arrivo.
3. **Domanda sulla penalità:** dalla scena del contatto, domanda e spiegazione. Prerequisito già scritto nel §D: finché la colpa si decide solo da mure e sopravento, le domande si limitano ai casi dove il giudizio è giusto (mure diverse; regole 10-13 dell'1b e verifica del 29 ottobre sulle mure col vento dietro in `REGOLE-DI-REGATA.md`).
4. **Passo da ripetere:** la parte delicata, per ultima.

## Dove stanno i file (aperto)
Memoria del browser (IndexedDB) per le ultime regate del coach; per il debugging il file scaricato dal browser (Firefox: niente File System Access). Si registra solo nel browser; va dichiarato con una riga (privacy).

## Criteri misurabili (soglie nostre, da confermare con i semi)
1. **Un file per regata:** 20 regate di fila, nessun byte della regata precedente nel file successivo.
2. **Il gioco non cambia:** con il registratore ricco acceso o spento, traiettorie, arrivi e penalità identici al bit su 20 regate; `impronta1b.js`, `polare.js`, `raffiche_e_virate.js` invariati.
3. **Fedeltà della riproduzione (fase 2):** posizione entro 0,5 m e prua entro 5° rispetto alla simulazione vera, in 20 regate.
4. **Costo:** passo di simulazione al massimo +3%; file di una regata sotto 2 MB.
5. **Ripetizione (fase 4):** su 30 situazioni generate per ogni tipo, almeno il 90% mantiene la proprietà che deve insegnare (per esempio il conflitto di mure c'è ancora e il pilota lo risolve), e almeno 3 su 4 sono diverse dalle altre per vento e posizioni oltre una soglia da fissare prima di misurare.
6. Pannello a 1360×650 senza pixel di eccesso; prove su Firefox e Chromium.

## Rischi
- La grafica usa lo stato globale (`S`, `R.boats[k].S`, scie): sostituirlo e rimetterlo a posto è delicato.
- Una situazione variata può non insegnare più quello che doveva (per questo il criterio 5).
- Il momento clou scelto male annoia: all'inizio pochi tipi di evento, scelti con regole semplici.
- Il registratore di oggi resta com'è finché la fase 1 non è approvata.

## Decisioni per Ale
- Via alla fase 1 (registrazione ricca, un file per regata)?
- Margini della variazione (vento ±5-8°, ±1 nodo) vanno bene come partenza?
- Dove i file: confermato il doppio browser + file scaricato?
