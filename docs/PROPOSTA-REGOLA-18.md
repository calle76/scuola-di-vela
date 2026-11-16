# Proposta: la regola 18 (spazio alla boa) nelle regate di Deriva

*Fermata 1, 16 novembre 2026 sera. Voce 49 di `DA-FARE.md`. Nessun codice nel gioco finché non arriva il via di Ale.*

## Da dove viene

Ale, 16 novembre sera: «la regola 18 [...] non viene mai considerata?», poi «implementare il livello Deriva con la regola 18 si può?» e «tenendo queste distanze non si possono risolvere problemi alle boe?». Il 31 ottobre Ale aveva deciso «la 18 è l'ultima fatica, dopo Deriva» (`DECISIONI.md`): questa proposta la anticipa dentro Deriva, ed è un cambio di decisione da confermare (domanda 1).

**Prima misura** (`tests/conta_boa_zona.py`, 41 regate registrate di Ale, solo boa 1): 52 contatti, 12 entro 25 m dalla boa, 9 di questi con almeno due barche nella zona (6 con tre o più), 10 su 12 col giocatore; 15 giri su 130 con un'altra barca ingaggiata all'ingresso nella zona. La 18 riguarda circa un contatto su sei: è un miglioramento della boa, non la soluzione di tutti i contatti.

## Cosa dice la regola (F15, regole 18 e 43.1, parafrasate)

- **Zona:** l'area entro tre lunghezze di scafo dalla boa. Nel gioco 3 × 4,2 m = **12,6 m** (la lunghezza è quella dello scafo del gioco; il «tre» è del regolamento).
- **18.2(a):** quando la prima di due barche entra nella zona, se sono **ingaggiate** (sovrapposte), quella **all'esterno** deve dare spazio alla boa a quella all'interno; se non lo sono, quella che non è ancora nella zona deve darlo a quella che c'è già. L'obbligo resta anche se poi l'ingaggio si rompe o ne nasce uno nuovo.
- **Quando non vale (18.1):** fra barche con mure opposte di bolina; fra chi arriva alla boa e chi se ne allontana; alle boe di partenza mentre si parte (preambolo della Sezione C).
- **Quando finisce:** quando lo spazio è stato dato (la barca ha girato la boa), o se chi ne ha diritto passa con la prua nel vento o esce dalla zona (18.2(b)).
- **18.3, virare nella zona:** chi vira da mure a sinistra a mure a dritta dentro la zona di una boa da lasciare a sinistra non ha diritto allo spazio verso una barca mure a dritta che sta già arrivando alla boa, e non deve costringerla a orzare sopra la bolina.
- **43.1(b):** chi sta navigando nello spazio a cui ha diritto non è penalizzato se, per colpa di chi doveva darglielo, infrange una regola della Sezione A (10-13), la 15 o la 16.

## Le boe del gioco (correzione di quanto detto in chat)

Nel gioco **non ci sono boe da girare in poppa**: il bastone ha la sola boa 1, di bolina, e poi si torna alla linea. Il triangolo del torneo ha la boa 1 (di bolina) e la boa 2 (al lasco). Quindi:
- **boa 1:** la 18 vale solo fra barche con le **stesse mure** (con mure opposte di bolina no) e c'è la 18.3; è la boa dei 12 contatti misurati;
- **boa 2 del triangolo:** la 18 vale tutta, senza eccezioni di mure; è il caso più semplice e più «da manuale».

Proposta: tutte e due le boe insieme, perché la regola nel codice è una sola; la boa 2 serve come caso pulito per le prove.

## Modello più semplice (versione A: la regola per la colpa e il semaforo)

Come per le regole 15 e 16 nella 1.3.10:
1. **Solo nelle regate di Deriva** (stesso interruttore `R.r1516`); nella Scuola restano le 10-13.
2. Per ogni coppia di barche vicine a una boa da girare si ricorda **chi deve lo spazio a chi**, deciso nel momento in cui la prima entra nella zona (ingaggio misurato con la stessa funzione delle regole 11 e 12, `dietroA`, sui contorni degli scafi).
3. **Il debito finisce** quando chi ne ha diritto ha girato la boa (cambio di lato, già contato dal gioco), esce dalla zona, o passa con la prua nel vento.
4. **Eccezioni:** mure opposte con tutte e due di bolina; 18.3 come detto sopra; boe di partenza e di arrivo escluse.
5. **Contatto:** se avviene mentre il debito è aperto, la colpa è di chi doveva lo spazio (regola 18), anche se per le 10-16 l'altra doveva cedere (43.1(b)).
6. **Semaforo:** verde se lo spazio ti è dovuto, rosso se lo devi tu.
7. **Registrazione:** una riga nuova nel file, `E zona Nome1 deve_spazio Nome2` all'apertura del debito e `E zona_fine` alla chiusura, per poterlo controllare sulle regate di Ale.
8. **Lezione 25 «Spazio alla boa»** in Deriva (solo testo, come la 24): zona, ingaggio all'ingresso, interna ed esterna, le eccezioni, cosa fa il gioco. Le parole del regolamento accanto alle nostre: «sovrapposte (nel regolamento: ingaggiate)».

**La guida degli avversari non cambia** in questa versione: imparano a dare e prendere spazio nella versione B, a parte (come la 15-16). Conseguenza da misurare: finché non la imparano, gli avversari all'esterno possono prendere penalità che oggi non prendono.

## Semplificazioni da dichiarare

- «Navigare nello spazio a cui si ha diritto» non si giudica: nel gioco basta che il debito sia aperto (scelta come quella del 23 ottobre per la 15-16: dentro la finestra la colpa è di chi doveva).
- Non si fanno: 18.1(a)(2) (mure opposte quando una sola delle due deve virare alla boa), 18.2(d) (ingaggio interno preso da dietro quando l'esterna non può più dare spazio), 18.2(e) (dubbio: nel gioco le posizioni sono esatte), 18.4 (strambata alla boa), la regola 19 (ostacoli), le boe dell'arrivo.

## Costanti

| Costante | Valore | Da dove |
| --- | --- | --- |
| Zona | 12,6 m (3 lunghezze da 4,2 m) | regolamento e scafo del gioco |
| Uscita dalla zona | 12,6 m + 1 m | ipotesi nostra (per non aprire e chiudere a ogni sobbalzo) |
| Mure opposte «di bolina» | entrambe fra 35° e 75° dal vento | come la bolina della lezione 11 (ipotesi già in uso) |
| Coppie seguite | entro 40 m | come `PREC_VICINE` della 15-16 |

## Criteri (soglie: attese nostre, scritte prima)

| | Cosa | Soglia |
| --- | --- | --- |
| Z1 | **La Scuola non cambia:** `impronta1b.js` al bit, `polare.js` e `raffiche_e_virate.js` identici; regate della Scuola con semi fissi uguali a prima | 0 differenze |
| Z2 | **Casi scritti a mano dal testo della regola** (almeno 12: ingaggiate all'ingresso interna/esterna alla boa 2; non ingaggiate; mure opposte di bolina alla boa 1; virata nella zona 18.3; ingaggio rotto dopo l'ingresso; chi ha diritto esce dalla zona; dopo il giro; boa di partenza) | 12 su 12 giusti, colpa e colore del semaforo |
| Z3 | **Fuori dalla zona niente cambia:** 40 regate del torneo col pilota, semi fissi; ogni contatto a più di 13,6 m da una boa ha la stessa colpa di prima | 0 differenze, con almeno 50 contatti fuori zona misurati |
| Z4 | **La regola lavora davvero:** nelle stesse 40 regate, almeno un debito aperto e almeno un contatto deciso dalla 18 | > 0 tutti e due (altrimenti il collaudo fallisce) |
| Z5 | **Avversari senza la versione B:** penalità degli avversari alla boa, prima e dopo, sui semi di Z3 (attesa: aumentano di poco) | si riporta il numero; se crescono di più del 30%, A non esce da sola e aspetta B |
| Z6 | **Spazio:** lezione 25 e Impostazioni senza pixel di eccesso a 1360x650, Chromium e Firefox | 0 px |
| Z7 | **Sulle regate di Ale:** rifatto `conta_boa_zona.py` dopo le prime regate giocate con la 18; i contatti alla boa con due o più barche nella zona hanno una regola scritta (18 o 10-16) | 100% con la regola scritta |

## Rischi

- **Gli avversari non conoscono la regola** finché non c'è la versione B: possono prendere penalità strane alla boa (Z5 lo misura). È lo stesso percorso della 15-16, dove la B non è ancora riuscita (1.3.11 spenta).
- **La boa 1 è complicata** (mure opposte, 18.3): i casi di Z2 servono a non sbagliare.
- **Il giocatore** è in 10 contatti alla boa su 12: la regola cambia soprattutto la colpa nei suoi contatti. Va spiegato bene (lezione 25 e messaggio del contatto «regola 18: dovevi dare spazio alla boa»).

## Domande per Ale (una per volta)

1. **Confermi** che la 18 entra dentro Deriva, cambiando la decisione del 31 ottobre?
2. **Disegnare la zona** (un cerchio tenue di tre lunghezze attorno alle boe) come aiuto disattivabile, come la layline? Proposta: sì, acceso nelle regate a tema.
3. **Versione A da sola prima della B** (come la 15-16), se Z5 passa? Proposta: sì.

## Lavoro stimato

Codice in `js/regate.js` (sezione nuova dopo le regole 15 e 16, come quella), lezione 25 in `js/contenuti.js`, una riga di registrazione in `js/registratore.js`; collaudo nuovo con i casi a mano (Z2) e misura col pilota (Z3-Z5). Una versione (1.3.18 o successiva). La versione B (avversari) è un lavoro a parte, con proposta propria.

## Risposte di Ale

1. **Sì, la 18 entra dentro Deriva** (16 novembre 2026, sera).
2. **Sì, zona disegnata** come aiuto disattivabile, come la layline (16 novembre 2026, sera).
3. **Sì, versione A prima della B**, se Z5 passa. **Via di Ale**, ma il lavoro aspetta i crediti rigenerati, tra qualche giorno (16 novembre 2026, sera).
