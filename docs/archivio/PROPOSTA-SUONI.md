# Proposta: i suoni del gioco

2 novembre 2026. **Fermata 1: solo documento, nessun codice.** Idea di Ale: «una cosa che abbiamo sempre trascurato: i suoni! un po' di mare, un po' di gabbiani, segnali del gioco, ambientazione, vento».

## 1. Da dove si parte

Il gioco oggi è **muto**: nel codice non c'è niente di audio (`grep` su `js/` e `index.html`). Il testo della regata con le bandiere lo dice: «Il gioco non ha suoni: i tempi contano sulle bandiere» (`js/regate.js`, `introRegata`).

## 2. Il modello più semplice

**Suoni generati dal browser, non registrati.** La Web Audio API costruisce i suoni da pochi pezzi (fruscio filtrato, tono, inviluppo). Così:
- **niente file e niente licenze** (principio 5): l'unica eccezione proposta sono i gabbiani, nella seconda fetta (§4);
- **i suoni seguono i numeri del gioco**: il vento suona più forte col vento apparente, l'acqua con la velocità della barca;
- la pagina non carica niente in più.

**Un file solo, `js/suoni.js`, che ascolta e non tocca.** A ogni fotogramma legge lo stato che il gioco ha già (velocità, vento apparente, vela che sbatte, contatori di virate e strambate, scuffia, contatti, boe, bandiere, arrivi) e suona quando un numero cambia. **Non chiama niente della simulazione e non usa `Math.random`**: il suo fruscio ha un generatore di numeri suo. Quindi la simulazione non cambia per costruzione, e i collaudi a seme fisso restano identici al bit (criterio S1).

**Quando suona:**
- solo dopo il primo tasto o clic (lo chiede il browser: va bene, si gioca con la tastiera);
- mai quando la finestra è nascosta, in pausa o nei collaudi accelerati;
- mai nel laboratorio.

## 3. Prima fetta: ambiente, manovre, incidenti, segnali

| Momento | Suono | Legato a (ipotesi nostre i numeri) |
|---|---|---|
| Vento | fruscio largo, più forte e più acuto col vento | vento apparente sulla barca; nelle raffiche sale quando la raffica **arriva sulla barca**, non prima |
| Acqua sullo scafo | fruscio basso e «bagnato» | velocità della barca; a barca ferma resta solo uno sciabordio lento |
| Vela che sbatte | colpi rapidi di tela | quando la vela fileggia, letto dallo stesso stato con cui il gioco la disegna (da individuare nel codice alla fermata 2); più fitti col vento forte |
| Boma che passa | virata: fruscio e tonfo morbido; strambata: colpo secco, più forte con più vento | contatori di virate e strambate già nel gioco |
| Spingere il boma (Z) | fruscio di tela tenuta | finché Z è premuto e la vela prende il vento al contrario |
| Scuffia | tonfo e spruzzo | passaggio a «scuffiata» |
| Raddrizzata | acqua che scola | fine della raddrizzata |
| Contatto con un'altra barca | colpo sordo di scafi | un contatto nuovo (la stessa coppia una volta sola, come le penalità) |
| Boa toccata | colpo più leggero e cavo | il contatto con la boa (nella regata con i giri è quello che dà il giro di penalità) |
| Segnali della partenza | tromba della giuria (regola 26): **un** suono all'avviso, **uno** al preparatorio, **uno lungo** a un minuto, **uno** al via | lo stesso istante in cui il gioco alza o ammaina la bandiera (con 3 e con 1 minuto di preparazione, i suoni delle bandiere che il gioco mostra) |
| Richiamo individuale | **un** suono quando sale la X (regola 29.1) | |
| Arrivo | un suono breve per ogni barca che taglia la linea | **non è nel regolamento**: è un uso comune, da dire come scelta del gioco |
| Lezioni e prove | un suono breve e discreto: passo completato, prova finita, medaglia | gli stessi momenti del messaggio di oggi |

Niente musica, niente voci: costano molto e allontanano dal simulatore.

**Impostazioni:** nelle ⚙ una riga «Suoni» con spento / basso / medio / alto, ricordata nel browser. Una sola riga, per non far crescere il pannello.

**Testi da cambiare:** la frase della regata «Il gioco non ha suoni…» diventa «I suoni accompagnano le bandiere, ma i tempi contano sulle bandiere (regola 26)». La lezione 16 resta com'è, perché dice già la regola: «contano le bandiere, non i suoni».

**Un aiuto da non creare per sbaglio:** in barca la raffica si vede sull'acqua, non si sente prima. Per questo il vento sale solo quando la raffica arriva sulla barca. Così il suono non dà informazioni che un velista non ha, e non serve un interruttore per gli aiuti.

## 4. Seconda fetta (dopo, se la prima piace)

- **Gabbiani**, ogni tanto, più spesso vicino alla barca giuria e alle boe. Costruiti dal browser vengono finti: servono **registrazioni con licenza libera** (per esempio CC0), citate in `FONTI-PUBBLICHE.md` come gli altri dati esterni. È l'unico punto con file e licenze.
- Sartiame che fischia col vento forte; mare di fondo con onde lontane; scricchiolio della barca molto sbandata; gorgoglio della pala in stallo.

## 5. Criteri (soglie scritte prima, attese nostre)

- **S1, la simulazione non cambia:** con i suoni accesi e spenti `arrivi_regate.py` (20 regate e 2 tornei) identico al bit alla versione di prima; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; `collaudo_esercizi_regata` e `collaudo_pilota_lezioni --veloce` verdi.
- **S2, un suono per ogni evento, al momento giusto:** con un registro interno dei suoni (solo con `#collaudo`), su regate e lezioni guidate dal pilota a semi fissi (10 semi):
  - ogni virata, strambata, scuffia, raddrizzata, contatto, boa toccata e arrivo dà **esattamente un** suono, entro 0,1 s dall'evento: 100% dei casi, e dichiaro quanti;
  - i segnali di partenza: 4 suoni con 5 minuti (a −300, −240, −60 lungo, 0 s), quelli delle bandiere mostrate con 3 e 1 minuto, entro 0,1 s;
  - la X: un suono solo se qualcuno è in anticipo; **controprova**: partenza senza anticipi, nessun suono della X; barca ferma a mani ferme, nessun suono di manovra.
- **S3, i suoni continui seguono i numeri:** il volume del vento cresce sempre col vento apparente (prova da 0 a 20 nodi), quello dell'acqua con la velocità; il suono della vela c'è quando la vela fileggia e non quando è regolata (passi di lezione 1 e 4 sui filetti).
- **S4, costo:** tempo per fotogramma in più al massimo **10%**, in Chromium e Firefox; nessun errore nella pagina, anche in un browser senza audio (il gioco funziona muto).
- **S5, comportamento:** nessun suono prima del primo tasto, con la finestra nascosta, in pausa o in «spento»; la scelta resta dopo il ricaricamento.
- **S6:** pannello e impostazioni a 1360×650 senza pixel di eccesso; pagina senza `#collaudo` senza errori.
- **Ascolto:** che i suoni siano gradevoli e non stanchino lo giudichi tu, giocando. Non è un giudizio nautico: lì contano solo le fonti, e servono solo per i segnali della partenza (F15).

## 6. Rischi

- **Stancano:** un vento continuo dopo dieci minuti dà fastidio. Per questo un volume basso di partenza, e l'ambiente più basso degli eventi.
- **Browser diversi:** Firefox e Chromium mescolano l'audio in modo un po' diverso; i collaudi misurano i comandi dati (volumi, istanti), non il suono che esce.
- **Collaudi su GitHub:** i computer di GitHub non hanno casse; il gioco deve funzionare muto e i collaudi leggono il registro interno, non l'audio.
- **Suoni finti:** un suono sintetico brutto è peggio del silenzio. Se un suono non convince, si toglie invece di insistere.

## 7. Da decidere (Ale)

1. **All'inizio i suoni sono accesi (volume basso) o spenti?** Io li accenderei bassi: chi gioca li scopre subito e li spegne con un clic.

## 8. Avanzamento

- **Ale, 2 novembre 2026:** «accesi bassi, vai avanti».
- **1.2.5:** prima fetta fatta; S1-S6 verdi in Chromium e Firefox (`collaudo_suoni.py`), con il metodo di S4 cambiato dopo il primo giro (detto nel `CHANGELOG.md`). Non provata la finestra nascosta. Resta la seconda fetta (§4: gabbiani con licenza libera, sartiame, onde, scricchiolii, gorgoglio della pala).
- **3 novembre 2026:** Ale, dopo aver giocato: «il mare è un fruscio piatto, ma soprattutto la vela quando sbatte è un ticchettio irreale». Proposta per vela e acqua registrate (CC0, Freesound): `PROPOSTA-SUONI-REGISTRATI.md` (fermata 1).
- **4 novembre 2026, 1.2.9:** seconda fetta fatta, senza le onde lontane: `PROPOSTA-SUONI-FINE.md`.
