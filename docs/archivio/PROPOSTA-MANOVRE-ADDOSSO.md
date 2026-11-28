# Proposta: rivali che virano o poggiano addosso a una barca vicina (fermata 1)

13 novembre 2026, sera. Voce 4 di `DA-FARE.md`; osservazioni 101, 102, 105 e 106 (`OSSERVAZIONI-GIOCANDO.md`). Nella proposta di riordino della lista è fra le voci «avanti, dopo», perché la carriera ha bisogno di rivali che regatano in modo credibile. È la fermata 1: in `js/` non è stato scritto niente.

## Cosa succede oggi

Un rivale decide **quando** cambiare rotta senza guardare chi ha vicino. Guarda le altre barche solo dopo, in `cedeAvv1b` (`js/regate.js`), e lì decide soltanto chi cede, con le regole 10-13.

Tre momenti in cui succede:
1. **Virata a tempo** (`cambiaBordo`). Il bordo dura un tempo sorteggiato; quando scade, il rivale vira anche se un'altra barca è a pochi metri sulla sua nuova rotta. Sono i casi 102 (virate subito dopo il via) e 106 (Blu vira davanti a Verde e la tocca un secondo dopo la fine della virata).
2. **Partenza** (`goStart`). Per prendere velocità, il rivale poggia sulla rotta verso la linea anche se lì c'è una barca ferma. È il caso 101 (Blu poggia da 55° a 86° addosso ad Ale, contatto a -2,3 s).
3. **Orzata dopo aver ceduto vicino alla boa.** È il caso 105: Blu passa sotto la boa, poi orza di colpo sotto Ale.

Le regole vere per i primi due sono la 13 (chi vira deve stare lontano dalle altre finché non ha finito) e la 15 (chi ottiene la precedenza con una sua manovra deve lasciare all'altra il tempo di scansarsi). Il gioco le ha rimandate (Ale, 23 ottobre, `PROPOSTA-REGOLE-PRECEDENZA-1B.md`), quindi oggi la colpa può cadere sulla barca che subisce. Per Ale è una penalità ingiusta.

## Modello più semplice

**Non si tocca chi ha la colpa**: le regole 15 e 16 restano rimandate. Si cambia solo la guida: prima di una manovra, il rivale guarda se la nuova rotta gli porta addosso una barca.

- **A. Virata a tempo rimandata.** Quando scade il bordo, prima di virare si usa la stessa previsione che il rivale già usa per cedere (`passaggio(b, rotta)`, a velocità costante): se sulla rotta dopo la virata un'altra barca passerebbe a meno di 2 lunghezze, la virata si rimanda di 1 s e si riprova, al massimo per `RINVIO_MAX` secondi. Vicino al bersaglio (30 m) e sulla layline non cambia niente: lì si vira dove si deve.
- **B. Partenza.** Prima di dire «parto» (`goStart`), la stessa prova sulla rotta di partenza: con una barca a meno di 2 lunghezze, il rivale aspetta mezzo secondo e riprova. Non oltre lo sparo: allo zero parte comunque.
- **C. Orzata alla boa (caso 105):** non entra in questa proposta. Nasce dal cedere che porta sotto la boa (osservazioni 80-81), che fa parte della voce 2.

**Costante nuova:** `RINVIO_MAX` = 8 s, ipotesi nostra, nessuna fonte. Si sceglie fra 4, 8 e 12 s sui semi di scelta.

## Criteri, con soglie nostre fissate prima di misurare

Misura sulle 4 regate del torneo, principianti ed esperti, col pilota per il giocatore e la stessa base di oggi (1.2.30, o la 1.2.31 se nel frattempo è chiusa). Semi di scelta 2201-2230, conferma 2231-2260, mai usati.

| # | Criterio | Soglia |
| --- | --- | --- |
| M1 | Contatti dopo il via in cui il rivale aveva **virato** nei 5 s prima | almeno −50% |
| M2 | Contatti fra -5 s e il via in cui il rivale aveva appena **deciso di partire** | almeno −30% |
| M3 | Contatti in tutto | non più di oggi |
| M4 | Arrivo mediano dei rivali | entro +2% |
| M5 | Barche piantate, partenze anticipate, rivali non arrivati | non più di oggi + 2 |
| M6 | Scuola | identica al bit: le regate della Scuola non hanno rivali che usano questa guida; si controlla col guardiano degli avversari |

**Il metro deve misurare davvero:** M1 e M2 contano casi, quindi prima di tutto si guarda che nella base ce ne siano. Se nella base sono meno di 15, il criterio si dichiara non misurabile su quei semi e si allargano i semi, senza cambiare la soglia.

## Rischi

- **Rivali che non virano più in gruppo.** Con tre barche vicine la virata si rimanda sempre e una barca resta sul bordo sbagliato fino a `RINVIO_MAX`. Lo misura M4.
- **Partenze più tardi.** B fa partire dopo chi ha una barca accanto. Lo misurano M4 e la partenza del giocatore, che non deve cambiare.
- **La previsione a velocità costante sbaglia quando la barca accelera.** È la causa probabile del caso 92. Qui si usa solo per *non* manovrare, quindi l'errore porta al più a una virata rimandata.

## Cosa serve da Ale

Il via, oppure dire se va prima o dopo la voce 2. Le due voci toccano la stessa guida, e la voce 2 aspetta le registrazioni di Lucio. Versione prevista: quella dopo i nomi (1.2.33 o successiva), solo `js/regate.js`.
