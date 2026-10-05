# Proposta: registratore di sessione

**Esito (5 ottobre 2026): approvata, via (c), un passo solo, con queste decisioni.**

1. Interruttore spento a ogni apertura della pagina (non salvato). Versione 0.18.
2. Il tasto M non scatta, e nessun tasto viene registrato, mentre il focus è in un campo di testo (per esempio «Nota»): si controlla l'elemento col focus. Il collaudo lo prova digitando una nota con la lettera m e altre lettere dei comandi.
3. Avviso alla chiusura della pagina se c'è una registrazione non scaricata. La copia di sicurezza vera resta rimandata.
4. Il file contiene solo ciò che serve: nessun dato personale, nessun tasto oltre a quelli del gioco, nessun testo digitato tranne la nota.

Il resto è come proposto qui sotto. Esito delle misure: `CHANGELOG.md`, versione 0.18.

## Scopo

Mentre una persona gioca, il gioco registra ciò che succede. Alla fine un pulsante scarica un file di testo, che la persona consegna per capire dove la barca rallenta, quale messaggio compariva e dove una lezione confonde. Un tasto (M) mette un marcatore «qui qualcosa non va»; a fine sessione si può scrivere una nota.

## Cosa c'era nel codice

- Quasi tutto si registra **leggendo** cose che già esistono, senza toccare le funzioni del gioco:
  - i contatori della barca (`S.tacks`, `S.gybesV`, `S.gybesC`, `S.capsizes`, `S.markIdx`);
  - il registro degli errori (`reg`);
  - il messaggio a comparsa (`S.toast`);
  - il suggerimento (`#hint`) e l'errore interno (`#errBox`);
  - lezione e passo (`mode`, `lessonIdx`, `stepIdx`, `stepDone`);
  - impostazioni (`opt`, `env`);
  - i tasti (`keys`, `semHeld`), cioè esattamente quelli che il gioco usa.
- Il tasto M era libero. Nel gioco non c'era un numero di versione.
- `rec` è già il fantasma e «registro» è il registro degli errori: il nuovo codice usa il prefisso `ses`.

## Le tre vie confrontate

- **(a) Stato da 4 a 10 volte al secondo, più gli eventi.** Circa 60 caratteri per riga di stato: da 0,86 a 2,2 MB l'ora, cioè da 290 000 a 720 000 token (ipotesi: 3 caratteri per token). Troppo per leggerlo intero in chat.
- **(b) Seme e comandi, poi si rigioca.** Oggi è impossibile:
  - 19 chiamate a `Math.random` senza seme, una delle quali nel disegno (tremolio, a ogni fotogramma);
  - un passo di tempo diverso a ogni fotogramma;
  - comandi anche col mouse.

  Renderla possibile richiederebbe un passo fisso, che cambia l'integrazione e quindi la fisica. Inoltre il file andrebbe rigiocato prima di poterlo leggere. Bocciata. Nei collaudi la riproduzione esatta invece si ottiene già: `Math.random` con seme, sostituito da Playwright, più `__sv.run` a passi fissi.
- **(c) Scelta.** Eventi e messaggi completi, stato una volta al secondo, marcatori, riassunto in testa. Stima: 230-330 KB l'ora, cioè 80 000-110 000 token. Lo stato a 5 Hz attorno ai marcatori è rimandato: si aggiunge solo se un secondo si rivela troppo grossolano.

## Cosa si registra

- **Stato**, una volta al secondo e solo mentre la simulazione gira: posizione, prua, velocità, sbandamento, vento reale e apparente, barra, scotta, andatura.
- **Eventi:** virata, strambata (controllata o a vela aperta), scuffia, raddrizzata, boe, arrivo, passo completato, errori del registro, avvio di lezioni, prove e regate, apertura e chiusura dei dialoghi, cambi di impostazioni.
- **Testi:**
  - il suggerimento, quando il testo cambia e resta almeno 0,3 s;
  - i messaggi a comparsa;
  - la regola della regata;
  - l'errore interno.
- **Tasti:** frecce, spazio, Cazza e Lasca (W, S), R come evento «raddrizza», M come marcatore.
- **Tempo:** l'orologio della registrazione conta il tempo vero passato in gioco, così si vede anche quanto si resta a leggere un passo di lezione.

## Dove cambia `index.html`

- Un blocco «REGISTRATORE» prima di «CICLO».
- Righe sparse:
  - la costante della versione;
  - una chiamata in `tick`;
  - una in `__sv.run`;
  - le righe HTML nelle impostazioni.
- Non si toccano il motore, `simulate`, `panel`, `toast`, `regAdd` e l'ascoltatore dei tasti. Il registratore non chiama `Math.random` e non scrive variabili del gioco.

## Verifiche promesse

1. `git diff` vuoto sulla zona del motore. Uscite di `polare.js` e `raffiche_e_virate.js` identiche carattere per carattere.
2. **Traiettoria identica al bit**, registratore acceso e spento: `Math.random` con seme, `__sv.run` a passi fissi, 10 semi, prove 1-3 e navigazione libera con raffiche forti. Soglia: 0 differenze. Variante con un numero casuale consumato di proposito a metà corsa, per mostrare che il metro vede la differenza.
3. Tempo per fotogramma, acceso contro spento. Soglia nostra: meno di 0,05 ms in più.
4. Pannello a 1360×650 e 1360×768 con 0 pixel di eccesso, compresa la finestra delle impostazioni.
5. Collaudo del registratore su 5 sessioni, più una pagina senza `#collaudo`:
   - interruttore spento di partenza, nessuna registrazione;
   - marcatori ritrovati, controllati contro i momenti in cui il collaudo li ha premuti;
   - tasti ritrovati;
   - nota presente, e nessun marcatore né tasto in più digitandola;
   - riassunto del gioco confrontato con quello dello script;
   - il collaudo fallisce se i casi misurati sono zero.
6. `tests/analizza_sessione.py` con il suo controllo `--prova`.

## Ipotesi dichiarate

Una riga di stato al secondo; 0,3 s di persistenza dei messaggi; 60 caratteri per riga e 3 caratteri per token; circa 150 000 token leggibili in una chat; 0,05 ms per fotogramma; «velocità scesa di oltre metà in 5 s» come rallentamento.

## Quando non farlo

Se a giocare è solo l'autore, che può raccontare cosa è successo. Conviene quando ci sono persone vere pronte a giocare.
