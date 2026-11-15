# Proposta: regole 15 e 16 in Deriva, e rivali che guardano prima di manovrare (fermata 1)

16 novembre 2026, notte. Unisce due proposte già scritte: `PROPOSTA-REGOLE-PRECEDENZA-1B.md` (regole 15 e 16, 23 ottobre, rimandate da Ale «al livello dopo») e `PROPOSTA-MANOVRE-ADDOSSO.md` (voce 4, 13 novembre). È la prima parte della tappa 5 del piano («rivali che regatano meglio»). **Solo proposta: in `js/` niente finché Ale non dà il via.**

## Perché insieme

Le osservazioni 101, 102, 105 e 106: un rivale vira o poggia addosso a una barca vicina, e la penalità può cadere su chi la manovra la subisce. Due cose diverse:
- **la colpa:** il gioco ha le regole 10-13; senza la 15 e la 16 chi prende la precedenza con una sua manovra, o cambia rotta verso l'altra, non ha mai torto. Caso 106: la Blu finisce la virata davanti alla Verde e la tocca un secondo dopo (la 13 non vale più, la 15 sì); caso 101: la Blu poggia addosso ad Ale prima del via (regola 16);
- **la guida:** i rivali decidono quando virare e partire senza guardare chi hanno vicino (voce 4).

Solo la colpa: i rivali prenderebbero più penalità senza capire perché. Solo la guida: le manovre addosso calano, ma quando capitano la colpa resta ingiusta. Insieme si completano.

## Dove

**Solo nelle regate di Deriva** (salti di vento, giri di penalità, torneo, stagione, finale) e nella lezione nuova. **La Scuola non cambia:** le sue due regate e le sue lezioni restano con le regole 10-13 (decisione del 23 ottobre, che resta valida per la Scuola).

## Cosa si fa

**Versione A, la colpa (regole 15 e 16, F15 parafrasate), dal modello del 23 ottobre:**
- **Regola 15.** Per ogni coppia di barche si ricorda quando la precedenza di base (regole 10-13) è passata dall'una all'altra, e per manovra di chi. Contatto entro **T** secondi da quel cambio, e precedenza presa con una manovra propria: cede chi l'ha presa.
- **Regola 16.** Chi ha la precedenza da più di T secondi e negli ultimi T secondi ha cambiato prua di almeno **G** gradi *verso* l'altra: cede lei. La 16.2 (poggiare di bolina sulla mure a sinistra che passa a poppa) è un caso di questa.
- **Semaforo:** il **giallo** tratteggiato: «hai la precedenza, ma se urti adesso la penalità è tua» (scelte di Ale del 23 ottobre: sì).
- **Testi:** fine regata e introduzione delle regate di Deriva («regola 15: avevi appena preso la precedenza virando e non le hai dato il tempo di scansarsi»; «regola 16: avevi la precedenza ma hai cambiato rotta verso di lei»).
- **Lezione 24, «Prendere la precedenza»** (Deriva): le regole 15 e 16 col semaforo giallo, ripasso di 4 domande, voci di glossario; senza esercizio in regata nella prima versione (costruire la scena a mano è la parte delicata: si aggiunge dopo, se serve).

**Versione B, la guida (voce 4), come scritta il 13 novembre:**
- **Virata a tempo rimandata:** prima di virare il rivale prova la rotta dopo la virata con la previsione che usa già per cedere; con una barca a meno di 2 lunghezze rimanda di 1 s e riprova, al più `RINVIO_MAX` s (4, 8 o 12, scelto sui semi). Vicino al bersaglio e sulla layline vira comunque.
- **Partenza:** stessa prova prima di partire; con una barca vicina aspetta mezzo secondo; allo sparo parte comunque.
- Il caso 105 (orzata dopo aver ceduto sotto la boa) resta con la voce 2.
- In più, i rivali **conoscono** le regole 15 e 16 quando decidono chi cede (la stessa `chiCede`): chi ha appena preso la precedenza non la pretende.

## Costanti

- **T = 5,2 s**, già misurato e confermato (`PROPOSTA-REGOLE-PRECEDENZA-1B.md`: 90° percentile del tempo per scansarsi con la barca del gioco, semi 1-50, conferma 51-100 a 4,8 s).
- **G: da decidere (Ale).** Misurato il 23 ottobre in due modi:
  - **(a) 9°:** il 95° percentile delle sole correzioni di rotta (barche senza nessuno vicino): ogni cambio di rotta vero verso l'altra conta. Più fedele al testo della regola («cambia rotta»), più penalità a chi ha la precedenza.
  - **(b) 53°:** il 95° percentile di tutti i cambi di prua, manovre comprese: conta solo una manovra grossa (una poggiata secca, una virata). Meno penalità, ma una poggiata di 30° addosso all'altra non conterebbe.

  **Consiglio (a), arrotondato a 10°**, perché dentro la finestra la colpa è comunque di chi ha la precedenza solo se c'è contatto, e la guida nuova (B) fa manovrare meno addosso.
- `RINVIO_MAX`: 4, 8 o 12 s, scelto sui semi di scelta (voce 4).
- Tempo di reazione 1 s, «verso l'altra», «chi va più veloce» come autore del cambio d'affiancamento: ipotesi nostre (23 ottobre).

## Criteri (soglie nostre, scritte prima)

**Versione A:**

| # | Criterio | Soglia |
| --- | --- | --- |
| R1 | Casi a mano | almeno 6 per la 15 e 6 per la 16 (dal 23 ottobre: virata davanti con contatto dentro e appena fuori T; precedenza ricevuta per manovra altrui, nessuna colpa; affiancamento da dietro; orzata e poggiata verso l'altra; cambio sotto G; allontanandosi; più vecchio di T; 16.2), 4 per il giallo: tutti con l'esito atteso; i controlli di oggi di `collaudo_regole.py` verdi |
| R2 | Semaforo coerente | colore un passo prima del contatto = penalità, 0 contraddizioni, con almeno un contatto col giallo visto |
| R3 | La Scuola non cambia | le sue regate, lezioni e penalità identiche al bit; fisica identica |
| R4 | Effetti riportati, senza soglia | in 200 regate del torneo col pilota: quanti contatti cambiano colpevole per la 15 e per la 16, penalità per barca, piazzamento medio |
| R5 | Lezione 24 | fuori da meriti ed esame della Scuola; nessuna domanda né voce di glossario doppia; nei punti di Deriva il ripasso conta (Conoscenza da 6 a 8, totale 23: la quota provvisoria del merito si riscrive in proporzione, 21 su 23, e lo si dice) |
| R6 | Pannello e pagina | 0 px di eccesso a 1360x650; Chromium e Firefox senza `#collaudo`, 0 errori |

**Versione B** (dal 13 novembre; base: la versione A chiusa; semi di scelta 2201-2230, conferma 2231-2260):

| # | Criterio | Soglia |
| --- | --- | --- |
| M1 | Contatti dopo il via in cui il rivale aveva virato nei 5 s prima | almeno −50% |
| M2 | Contatti fra -5 s e il via in cui il rivale aveva appena deciso di partire | almeno −30% |
| M3 | Contatti in tutto | non più di prima |
| M4 | Arrivo mediano dei rivali | entro +2% |
| M5 | Barche piantate, partenze anticipate, rivali non arrivati | non più di prima + 2 |
| M6 | La Scuola | identica al bit (guardiano degli avversari) |

Se nella base i casi di M1 o M2 sono meno di 15, il criterio si dichiara non misurabile su quei semi e si allargano i semi, senza cambiare la soglia.

## Rischi

- **Più penalità a chi ha la precedenza**, per qualche secondo dopo ogni virata: è la regola vera, ma i rivali principianti virano spesso vicino agli altri. B deve abbassarle; R4 e M3 lo dicono.
- **Rivali che non virano più in gruppo** (B): con tre barche vicine la virata si rimanda fino a `RINVIO_MAX`. M4.
- **Semplificazione dichiarata:** dentro la finestra la colpa è di chi ha la precedenza, qualunque cosa abbia fatto l'altra (una barca potrebbe approfittarne; nella realtà violerebbe la 14). Scelta di Ale del 23 ottobre.
- **Il Coach e i collaudi del torneo** contano penalità e contatti: vanno rimisurati (`collaudo_coach`, `collaudo_torneo`, `collaudo_finale`, `collaudo_sponsor`).
- Le misure di B sono lunghe (ore): da fare di notte, al più 2 processi sul PC di Ale.

## Fonti

F15 (regole 15, 16, 43.1 e definizione di «spazio»), parafrasate; i casi pubblicati di World Sailing sulle regole 15 e 16 per i casi a mano (citati col numero, non copiati).

## Cosa serve da Ale

1. Il via (A e poi B).
2. **G: 10° (consiglio) o 53°.**
3. Va bene la lezione 24 senza esercizio in regata, per ora?
