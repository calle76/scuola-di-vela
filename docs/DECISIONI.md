# Registro delle decisioni

Iniziato il 25 ottobre 2026. Una riga per ogni decisione presa, con la data e il **costo se la si cambia**. Prima di aprire un livello nuovo si rileggono le righe ad **alto** costo. Il metodo è in `METODO.md` §3.

Costo di cambiamento:
- **alto:** cambiarla tocca fisica, lezioni, collaudi o abitudini di chi gioca;
- **medio:** tocca più parti, ma senza rifare il lavoro fatto;
- **basso:** si cambia in una versione piccola.

**I costi della prima stesura sono una stima di Claude (25 ottobre 2026), da confermare da Ale riga per riga.** Dove questo registro e un altro documento dicono cose diverse, vale l'altro documento finché la riga qui non è corretta.

## Piattaforma

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| Gioco nel browser: `index.html` più `js/`, script classici e non moduli, si apre con un doppio clic | 16 ott (1.0.3) | alto | Tutti i collaudi e la pubblicazione ci si appoggiano | `archivio/PROPOSTA-DIVISIONE-CODICE.md` |
| Solo computer con tastiera | inizio | alto | Comandi, pannello e lezioni sono pensati per la tastiera | `PROGETTO.md` |
| Browser di riferimento: Firefox, per Ale e per Lucio (decisione di Ale, 28 ott 2026). Niente funzioni solo-Chrome (File System Access, ecc.); i file del registratore si salvano con lo scarico del browser e con IndexedDB | 28 ott | medio | Da qui in poi si progetta e si prova su Firefox; i collaudi automatici oggi girano su Chromium e vanno affiancati da Firefox (`playwright install firefox`) | `PROPOSTA-REGATA-COME-FONTE.md` §10 |
| Percorso a triangolo e linea d'arrivo del torneo 1b: restano come sono (linea di partenza e arrivo da 70 m, senza fonte, dichiarata come semplificazione). Dal livello 2 le regate si rendono più realistiche (decisione di Ale, 28 ott 2026) | 28 ott | basso | Solo `LINE_HALF` e i testi | `OSSERVAZIONI-GIOCANDO.md` 65 |
| Partenza degli avversari dell'1b: nel livello 1 qualche avversario può tagliare la linea oltre gli estremi (16% dei tagli nelle misure, 2 su 12 nella registrazione di Ale) o partire in ritardo, perché in attesa scivola di lato circa 25 m al minuto. Resta com'è e si dichiara come semplificazione; dal livello 2 si rivede la guida dell'attesa (decisione di Ale, 29 ott 2026: «2»). Provato un rimedio, non adottato: spostava le uscite in partenze anticipate (9,6% → 20%) | 29 ott | basso | Solo la guida dell'attesa in `js/regate.js` | `PROPOSTA-DERIVA-ATTESA-1B.md`, `OSSERVAZIONI-GIOCANDO.md` 59-61, 67 |
| Pubblicazione su GitHub Pages da `main` (attiva, verificata da Ale il 26 ott: https://calle76.github.io/scuola-di-vela/) | set | medio | Cambia solo come arriva il gioco a chi gioca | `README.md` |
| Pannello senza eccedenze a 1360×650 | ott | medio | Ogni testo nuovo va misurato | `CLAUDE.md` |

## Fisica

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| Motore cinematico didattico, non un previsore; un effetto entra solo se si sente guidando e ha una fonte | inizio | alto | È la base di tutto il resto | `PROGETTO.md` |
| Si tara la barca condotta bene; la differenza la fa chi guida | 16 ott | alto | Fasce, avversari e lezioni dipendono dalla velocità | `ROADMAP.md` |
| Prima la barca, poi avversari, lezioni e per ultimi i tempi delle medaglie | 17 ott | — (regola di metodo) | — | `ROADMAP.md`, `METODO.md` |
| Barca dell'1a congelata | 17-22 ott | alto | Impronta, lezioni, prove, esame | `STATO.md` |
| Barca dell'1b congelata | 23 ott | alto | Impronte, avversari, torneo | `archivio/PROPOSTA-CONGELAMENTO-1B.md` |
| I numeri che dipendono dalla barca si derivano dalla barca, non si scrivono a mano | ott | medio | Sostituirli dopo vuol dire trovarli tutti | `STATO.md` |
| Valori numerici misurati da pubblicazioni scientifiche, citati, si possono usare nel motore | 16 ott | basso | — | `CLAUDE.md` |

## Comandi

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| Barra su ← →; comando principale di ogni ruolo su W S; secondo comando su E D; Q vista; A raddrizza; Z spingi il boma; R libero | 7 e 17 ott | alto | Abitudini di chi gioca, testi delle lezioni, domande, collaudi da tastiera | `VISIONE-LIVELLI-E-CARRIERA.md` §12 |
| Dal livello 2 in poi i tasti non si stravolgono a ogni livello | 6 ott | alto | — | memoria del progetto |
| Zoom sui tasti 1 e 2, senza pulsanti sul mare | 26 ott (1.0.48) | basso | — | `CHANGELOG.md` |
| Moviola («Rivedi») sul tasto **O**; **M** resta al marcatore del registratore. I tasti della mano sinistra (W S A Q Z 1 2, E D riservati) non si toccano | 29 ott (1.0.59) | basso | Un solo punto in `moviola.js` e nei testi | `CHANGELOG.md` |
| Si lavora su `main`, senza rami; tag solo all'uscita di un livello | 26 ott | basso | — | `METODO.md` §6 |

## Livelli e ruoli

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| Ogni livello ha una parte «a» (teoria) e una «b» (pratica); 1a basi, 1b barca completa, 2 regolamento con la stessa barca, 3 fiocco, 4 gennaker, 5 equipaggio da tre e tattica | 19 ott | alto | Documenti, menu, carriera, ordine dei lavori | `VISIONE-LIVELLI-E-CARRIERA.md` §2 |
| Nell'1b le regole si fermano alle 10-13; copertura del vento e protesta passano al livello 2 | 23 ott | medio | Avversari e domande dell'1b | `STATO.md` |
| Avversari dell'1b: chi deve cedere cede, chi ha la precedenza tiene la rotta (piantate 36 → 2, penalità 73 → 97) | 26 ott (1.0.49) | medio | Guida degli avversari e pilota dei collaudi | `PROPOSTA-AVVERSARI-1B.md` |
| Avversari dell'1a lasciati come sono: meno bravi, come chi comincia | 26 ott | basso | — | `PROPOSTA-AVVERSARI-1B.md` §10 |
| Torneo: uscire a metà regata (menu o chiusura del browser, anche per sbaglio) vale come «Ritirati» per quella regata; il torneo continua. Fatto nella 1.0.50 (prima la regata si rifaceva da capo, scelta della 1.0.34); conta dal clic su «Corri la regata» | 26 ott | basso | Salvataggio del torneo e `collaudo_torneo.py` C3 | `STATO.md` «Aperto» 4 |
| Nessun aiuto a schermo per i salti di vento: si leggono dalla prua nel pannello | 26 ott | basso | — | `archivio/PROPOSTA-SALTI-VENTO.md` |
| Si guida sempre un solo ruolo; nel torneo il ruolo resta lo stesso fino alla fine | ott | alto | Equipaggio del computer, meriti, tornei | `VISIONE-LIVELLI-E-CARRIERA.md` |
| Nessun numero fisso di novità per livello | 4 ott | basso | — | `VISIONE-LIVELLI-E-CARRIERA.md` §1 |
| Replay e «regata come fonte» solo nella parte «b» dei livelli | 20 ott | medio | Registrazione e istantanee | `PROPOSTA-REGATA-COME-FONTE.md` §9.7 |
| Vela di portanza del livello 4: gennaker asimmetrico [da verificare su fonti] | ott | medio | Fisica del livello 4, non ancora scritta | memoria del progetto |
| **Modalità coach**: in ogni regata il registratore parte da solo e si spegne all'arrivo (un file per regata, M sempre possibile); nella navigazione libera, nelle prove e nelle lezioni non registra, salvo registrazione forzata a mano. La registrazione serve al coach (rivivere una situazione, «perché la Rossa ha preso la penalità?») e al debugging | 27 ott | medio | Registratore, memoria del browser o cartella, replay e domande dei livelli futuri | `PROPOSTA-REGATA-COME-FONTE.md` §10 (fermata 1 da scrivere) |
| Avversari dell'1b: **non si correggono ora** (penalità, boe dal lato sbagliato, tre barche alla boa, partenze); priorità al livello 2 (2a regolamento, 2b protesta) | 30 ott (Ale: «pazienza») | basso ora, medio dopo (i tornei del livello 2 giocano contro questi avversari) | La guida è in parte in comune con l'1a, che resta congelata | `ROADMAP.md`, `STATO.md` punti 4b e 5 |
| Registrazione automatica di ogni regata, dal conto alla rovescia all'arrivo, a pezzi (primo fino a 120 s, poi 300 s), 10 righe al secondo, ultime 5 regate in IndexedDB; la registrazione a mano ha la precedenza | 29 ott (1.0.60, idee di Ale: pre-via e pezzi da 5 minuti) | medio | Formato 3 del file, `analizza_sessione.py`, le fasi 2-4 del coach leggeranno questi pezzi | `PROPOSTA-COACH-REGISTRATORE.md` |
| Modalità coach, più usi (Ale, 29 ott 2026): momento clou da rivedere; nei livelli con meno lezioni domanda su una penalità e passo da ripetere; registrazioni raccolte per il debugging. **La ripetizione non è una copia: stessa situazione, condizioni non identiche** (vento, onde, posizioni variati dentro margini). La moviola non è una funzione a sé | 29 ott | medio | Registratore, generatore delle situazioni, lezioni dei livelli futuri | `PROPOSTA-COACH-REGISTRATORE.md` |
| Torneo dell'1b con percorsi misti, come nelle serie vere (regola 27.1: il percorso lo sceglie il comitato): regata 1 bastone, 2 triangolo, 3 bastone coi salti di vento, 4 triangolo | 27 ott | medio | Percorso, guida degli avversari, distacchi, disegno | `PROPOSTA-TORNEI-1B.md` §8.6 |
| `collaudo_contatto_vero.py` fuori soglia su Firefox nell'1a (0,29 m contro 0,25 m): si lascia com'è, l'1a non si tocca (l'1b è a posto) | 27 ott | basso | Solo il collaudo | `CHANGELOG.md` 1.0.56 |
| Soglia di 2 s per uscire dal menu a metà regata del torneo (collaudo C11 R7, 2,71 s il 27 ott): non si inseguono i decimi, basta che funzioni | 27 ott | basso | Solo il collaudo | `CHANGELOG.md` 1.0.50 |
| Completare l'1b (30 ott, Ale): brevetto **strada A** (si tiene il «Brevetto di livello 1» dell'1a e se ne aggiunge uno, «Regatante», alla fine dell'1b; «attestato di partecipazione» già scartato); replay dell'1b = «Rivedi» com'è; nessuna medaglia nell'1b; sette lezioni brevi confermate | 30 ott | medio | Menu, meriti, esame, carriera | `PROPOSTA-COMPLETAMENTO-1B.md` |
| Promemoria di Ale (30 ott): nell'1b anche gli avversari devono fare i giri di penalità (oggi +15 s, `PROPOSTA-LIVELLO-2A.md`); le lezioni sulle precedenze si completano col livello 2, stessa barca | 30 ott | medio | Guida degli avversari (in comune con l'1a congelata) | `PROPOSTA-LIVELLO-2A.md` |
| Medaglie solo nella parte «a» di ogni livello (idea di coerenza di Ale, 30 ott): da confermare nel livello 2 | 30 ott | basso | Dove stanno le prove | — |
| **Riorganizzazione** (Ale, 30 ott 2026, `PROPOSTA-RIORGANIZZAZIONE.md`): «La scuola» (livello 0, barca dell'1b, la 1a si butta, tutta la teoria con precedenze, segnali e bandiere, prove con medaglie, 2 regate senza torneo, quiz, un attestato) e livello 1 «Deriva» (regate, registratore e moviola, lezioni proprie, tornei da superare con una soglia); poi «Fiocco». Nomi al posto dei numeri. **Niente più brevetti**: i livelli si aprono se la carriera lo permette. Si fa dopo aver chiuso il 2a nel motore | 30 ott | alto | Menu, carriera, lezioni, collaudi, documenti | `PROPOSTA-RIORGANIZZAZIONE.md` |
| Giri di penalità degli avversari (regata dei giri): iniziano dopo lo sparo, semplificazione dichiarata (il regolamento li vuole «appena possibile», anche prima del via) | 31 ott (Ale: «semplificata e dichiarata, procedi») | medio | Guida degli avversari; per giri anche prima del via serve una guida di partenza che sappia uscire e rientrare | `PROPOSTA-GIRI-AVVERSARI.md` |
| Principiante: non è una porta (scuola, si gareggia contro avversari deboli); idea: la vela che si manovra da sola come opzione | 30 ott | basso | Lezioni e comandi | `PROPOSTA-RIORGANIZZAZIONE.md` §8 |
| Questa riorganizzazione **supera** la riga di oggi su brevetto «strada A» e menu dell'1b (`PROPOSTA-COMPLETAMENTO-1B.md`) | 30 ott | — | — | — |

## Carriera, meriti, salvataggi

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| Bivio gioco libero / carriera, con salvataggi e fantasmi separati | 14 ott (0.22) | alto | Formato dei salvataggi e tutti i punti che scrivono | `archivio/PROPOSTA-ESAME-E-BREVETTO.md` §11 |
| Fantasmi e record sono prove di gioco: si azzerano quando cambiano regole o tempi, senza migrazioni | 7 ott | basso | **Abbassa il costo** delle decisioni sui salvataggi finché il gioco è in prova | memoria del progetto |
| Gioco libero tutto sbloccato e navigabile fra i livelli; in carriera un livello si apre coi brevetti | 17 ott | medio | Menu e carriera | `VISIONE-LIVELLI-E-CARRIERA.md` §8 |
| Quattro aree di merito (abilità, competizione, conoscenza, esperienza) con minimi; esame obbligatorio; poi brevetto | ott | medio | Libretto, esame, attestato | `VISIONE-LIVELLI-E-CARRIERA.md` |
| Numeri dei meriti provvisori, da tarare giocando | 9 ott | basso | — | `PIANO-GENERALE.md` |
| Classifica (punteggio minimo del regolamento) separata dai meriti | 14 ott | medio | Torneo e libretto | `archivio/PROPOSTA-ESAME-E-BREVETTO.md` |
| Esame non superato: ripasso completo delle lezioni sbagliate, con qualsiasi punteggio, poi si riprova | 14 ott (0.24) | basso | — | `archivio/PROPOSTA-ESAME-E-BREVETTO.md` |
| Gli aiuti accesi o spenti valgono uguale per i meriti | 14 ott | basso | — | `archivio/PROPOSTA-ESAME-E-BREVETTO.md` |

## Contenuti e confini legali

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| «Brevetto», mai «patente»; sempre «nessun valore legale»; niente marchi né titoli che sembrino ufficiali | inizio | alto | Rischio legale | `PROGETTO.md` |
| Nessuna persona esperta: le affermazioni nautiche si verificano su fonti scritte e video | 13 ott | medio | Ogni contenuto nuovo ha bisogno di fonti | `CLAUDE.md` |
| Le spiegazioni lunghe vanno nel manuale, non a video | 7 ott | basso | — | memoria del progetto |
| I PDF raccolti in `fonti-pdf/` non diventano domande di quiz o d'esame | 12 ott | basso | — | `SCHEDATURA-FONTI.md` |

## Decisioni aperte ad alto costo

Da prendere **prima** di cominciare il livello a cui servono.

| Decisione | Serve a | Dove |
| --- | --- | --- |
| Come si danno gli ordini all'equipaggio e con quanto preavviso | Livello 3 | `VISIONE-LIVELLI-E-CARRIERA.md` §11 |
| Quanti ruoli servono per il brevetto dal livello 3 | Livello 3 | idem |
| Come entra il fiocco a farfalla | Livello 3 | idem |
| Barche vere (per categoria) dei livelli 4 e oltre | Livello 4 | idem |
| Gioco a più persone: quale gradino e se sì | Prima di toccare registrazione e istantanee | `PROPOSTA-REGATA-COME-FONTE.md` §8 |
