# Proposta: moviola delle regate (osservazione 71, 29 ottobre 2026)

Fermata 1: nessun codice scritto. Idea di Ale: «ci vuole la moviola». Motivo concreto: il 28 ottobre Ale non era sicuro di una penalità (70) e di un giro di boa (69), e il registro dice i numeri ma non fa *vedere* cosa è successo.

## Cosa serve a chi gioca
Rivedere sullo schermo gli ultimi secondi (contatti, penalità, boe) con la stessa grafica del gioco, più lenta e anche all'indietro, senza dover confrontare righe di numeri.

## Modello più semplice
- **Registrare:** un buffer circolare in memoria con lo stato delle barche (x, y, prua, sbandamento, posizione di boma e vela, e per ogni barca la stessa cosa) a **10 campioni al secondo** per gli ultimi **60 s**: circa 600 istanti × 4 barche × 6 numeri (meno di 15.000 numeri). Solo nelle regate (modalità `race`), solo nell'1b e nel torneo.
- **Rivedere:** un pulsante «Rivedi» (tasto da scegliere, non uno dei tasti di guida) che mette il gioco in pausa e riproduce il buffer: velocità 1×, ½×, ¼×, indietro, e un cursore. La riproduzione sostituisce temporaneamente i campi di `S` di ogni barca con quelli registrati e chiama il disegno esistente; all'uscita rimette lo stato vero. Il motore non gira durante la moviola e **non viene toccato** (barca congelata).
- **Cosa si vede in più:** i marcatori delle penalità e dei contatti dal buffer degli eventi (già registrati in `R.penList`), cioè «qui è scattata la penalità alla Rossa» al secondo giusto.
- Disponibile **dopo l'arrivo** e in pausa durante la regata; non in gara (nessun vantaggio nel rivedere mentre si naviga). Aiuto disattivabile come gli altri (principio 3).

## Costanti (ipotesi nostre)
- 10 campioni/s, 60 s di memoria. A 10 Hz il disegno interpolato resta fluido anche a ¼×; se fossero pochi si passa a 20 Hz (costa il doppio, resta piccolo).

## Criteri misurabili (soglie nostre)
1. **Fedeltà:** una moviola a 1× riproduce le posizioni di ogni barca entro **0,5 m** e la prua entro **5°** rispetto alla simulazione vera, in 20 regate col pilota (semi fissi 1-20), controllate a ogni secondo.
2. **Il gioco non cambia:** con la moviola presente ma non usata, arrivi, penalità e traiettorie sono identici al bit su 20 regate; `impronta1b.js`, `polare.js`, `raffiche_e_virate.js` invariati.
3. **Costo:** il tempo medio di un passo di simulazione non sale oltre il **3%**; memoria sotto 1 MB.
4. **Uscita pulita:** dopo la moviola il gioco riprende dallo stesso istante, senza barche spostate (stato confrontato prima e dopo).
5. **Pannello** a 1360×650 senza pixel di eccesso con il pulsante; prova su Firefox e Chromium (browser di Ale e Lucio).

## Rischi
- La grafica usa lo stato globale (`S`, `R.boats[k].S`, scie, increspature): sostituirlo e rimetterlo a posto è la parte delicata; una scia disegnata dal buffer può non coincidere con quella vera (si ricostruisce dalle posizioni o si omette per ora).
- Il registratore (`registratore.js`) scrive già una riga al secondo: non va confuso con il buffer, che è solo in memoria e non si salva nel file.
- Non è una prova per il gioco: serve a capire, non cambia punteggi o penalità.

## Cosa NON è
Non rigioca la partita con scelte diverse e non cambia le penalità: mostra soltanto cosa è successo.

## Dopo il via di Ale
Fermata 2: implementare in un file nuovo o in `disegno.js`/`avvio.js` (non nel motore), nuova versione 1.0.58 con `CHANGELOG`, misurare i criteri 1-5 e riportare i numeri.
