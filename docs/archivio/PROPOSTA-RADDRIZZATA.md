# Proposta: la barca dopo la raddrizzata

19 ottobre 2026, fermata 1. Nessun codice.

## Oggi [codice]

`js/gioco.js`: premuto A, dopo **3 s** la barca è dritta a **60° dal vento**, dalla parte del lato su cui era scuffiata, con la scotta a 0,8 e 0,3 m/s di velocità. Gli avversari (`js/regate.js`): dritti **5 s** dopo la scuffia, sempre a 60°. Mentre è rovesciata la barca scivola sottovento a 0,25 m/s e non gira.

## Fonte [video]

F-nuova: video di un allenatore inglese sulla scuffia (YouTube `T7lUaEafLv8`, trascrizione e tre fotogrammi forniti da Ale il 19 ottobre 2026). Fonte divulgativa, una sola.
- Si raddrizza tirando con **la schiena al vento**: il timoniere sta sopravento, l'albero sottovento; così la vela sale e **sbatte libera** e si riparte subito. Al contrario (albero verso il vento) il vento entra sotto la vela e la barca riscuffia.
- Gli schemi sono sezioni trasversali con il vento di fianco: la barca raddrizzata ha **il vento al traverso** [lettura degli schemi, non detta a parole].
- Fatta bene, **15-20 s** dalla scuffia alla barca che naviga di nuovo; la barca rovesciata del tutto si raddrizza in meno di 15 s.

## Proposta (il modello più semplice)

1. Dopo la raddrizzata la barca è **al traverso** (90° dal vento) invece che a 60°, con **la scotta tutta lascata** (vela che sbatte) e velocità zero. Il resto lo fa il giocatore: cazza e parte.
2. **Durata:** da 3 s a **10 s** dopo aver premuto A (più il tempo che il giocatore impiega a premerlo, così il totale cade nei 15-20 s del video). Avversari: da 5 s a 15 s dalla scuffia.
3. **Solo nel livello 2** (`S.lv === 2`), come le altre novità: il livello 1 è chiuso e congelato con l'impronta. Da decidere con Ale.

Rimandato: la scuffia sopravento in poppa e la barca rovesciata del tutto (servirebbe un disegno nuovo).

## Criteri (soglie nostre, dichiarate ora)

- **R1** prua dopo la raddrizzata a 90° ± 5° dal vento, su tutte e due le mure, con 6, 10, 15 e 20 nodi.
- **R2** con la scotta tutta lascata la barca non riscuffia nei 10 s seguenti, in nessuno degli 8 casi (4 venti × 2 mure).
- **R3** tempo dal tasto A alla barca a 2 nodi, cazzando subito: riportato, nessuna soglia.
- **R4** livello 1 identico al bit (impronta); `polare.js` e `raffiche_e_virate.js` identici.
- **R5** «Regata nei salti di vento» (`collaudo_salti2.py`): tutte le barche arrivano.

## Rischi

- Una sola fonte, divulgativa; la durata del video comprende il nuotare fino alla deriva, che il gioco non mostra.
- 10 s fermi possono sembrare lunghi giocando: si giudica provando.

## Fermata 2 (19 ottobre 2026, versione 1.0.32)

**Decisione di Ale:** solo livello 2, con una lezione breve dedicata più avanti.

**Fatto.** `js/motore.js`: `RADD2` (10 s, 15 s per gli avversari, 90°) e `raddT(S)` (3 s nel livello 1). `js/gioco.js`: nel livello 2 la barca torna dritta dopo 10 s a 90° dal vento locale, ferma, scotta a 1; `js/disegno.js`: la barca che si tira su e lo sbandometro seguono la durata nuova; `js/regate.js`: avversari del livello 2 dritti 15 s dopo la scuffia, a 90° dal vento vero (con i salti, il medio `env.twd` dava 83°: trovato dal collaudo e corretto).

**Misure** (`tests/collaudo_raddrizzata.py`, tasti veri, 16 casi più 2 avversari):
- **R1 ok**, 8 casi su 8 nel livello 2: dritta dopo 10 s, 90° dal vento, ferma, scotta 1; livello 1 invariato (3 s, 59-61°, scotta 0,8).
- **R2 ok**, 8 su 8: nessuna riscuffia nei 10 s seguenti, sempre a 90°.
- **R3** (cazzando fino alla regolazione del gioco): a 2 nodi in 3,5 / 1,3 / 1,5 s con 6 / 10 / 15 nodi; con 20 nodi non ci arriva in 30 s, **né nel livello 2 né nel livello 1** (comportamento che c'era già, da guardare a parte). Nel livello 1: 6,2 / 2,4 / 1,7 s.
- **R4 ok**: impronta identica al riferimento della 1.0.30; `polare.js` e `raffiche_e_virate.js` identici.
- **R5 ok**: `collaudo_salti2.py` 12 regate su 12 con tutte le barche arrivate. Avversario fatto scuffiare apposta: livello 2 ancora rovesciato a 14,5 s, dritto a 15,5 s a 90°; livello 1 dritto dopo 5 s a 60°.

**Difetti del collaudo trovati e corretti prima del risultato:** velocità di R1 letta mezzo secondo dopo invece che all'istante (la vela che sbatte spinge già a 0,2-0,5 nodi); R3 teneva ↑ per 30 s, cazzando a ferro al traverso; la prua dell'avversario letta da `b.info`, che mentre la barca è rovesciata non si aggiorna.

**Limite dichiarato (Ale, 19 ottobre 2026):** con 20 nodi fissi la barca non riparte dopo la raddrizzata (anche nell'1a). Nel gioco il vento di base arriva al più a 15 nodi; 20-25 nodi si hanno solo al centro di una raffica forte, per pochi secondi, e dopo i 10 s della raddrizzata la raffica è di solito passata. Caso raro e passeggero: non si corregge.
