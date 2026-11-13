# Proposta: insegnare a stare fermi prima del via (lezioni 18 e 19; fermata 1, 13 novembre 2026)

**Da dove nasce.** Lucio, 13 novembre, sulla lezione 19 «Partenza da fermi»:
- la posizione in cui comincia l'esercizio (fermi, vela tutta lascata, 10 s al via) gli pare poco realistica: se non fai niente, dopo un po' la barca va indietro;
- la lezione dovrebbe spiegare come si tiene la barca in equilibrio fra marcia avanti e marcia indietro: vela quasi in stallo, giocando con la scotta, cazzando e lascando.

**Niente codice finché Ale non dà il via.** Sono solo testi ed esercizi (`js/contenuti.js`); la fisica non si tocca.

## 1. Cosa dicono oggi le lezioni

- **Lezione 18** («Partenza in velocità»): si aspetta «quasi fermi con la vela lascata che sbatte», con la prua appena sotto la bolina; «da fermi la barca non va alla linea».
- **Lezione 19** («Partenza da fermi»): l'esercizio mette la barca ferma 12 m dietro la linea, a 60° dal vento, vela tutta lascata, 10 s al via.

Nessuna delle due dice **come** si resta fermi.

## 2. Cosa fa la barca del gioco (misurato col motore, 13 novembre)

Script di prova `fermo*.js` nella cartella di lavoro di questa sessione, non nel repo. Barca ferma all'inizio, 60 s, prua tenuta ferma.

**Vela tutta lascata, senza toccare niente** (velocità dopo 60 s; il segno meno vuol dire che va indietro):

| prua dal vento | 6 nodi | 10 nodi | 14 nodi |
| --- | --- | --- | --- |
| 40° | −0,66 | −1,08 | −1,48 |
| 45° | −0,52 | −0,86 | −1,14 |
| 50° | −0,34 | −0,58 | −0,74 |
| 55° | −0,07 | −0,16 | −0,23 |
| 60° (esercizio della lezione 19) | +0,30 | +0,49 | +0,57 |

Quindi Lucio ha ragione anche nel gioco:
- con la prua appena sotto la bolina (40-50°), come dice la lezione 18, la barca lasciata a sé **va indietro**. A 45° con 10 nodi fa 22 m indietro e 18 m sottovento in un minuto;
- a 60°, dove comincia la lezione 19, la vela lascata spinge ancora un po': la barca **va avanti piano**. Anche la frase «da fermi la barca non va alla linea» è vera solo in parte.

**Stare fermi si può già.** Fra la scotta al 50% (vela che sbatte) e al 40% (vela che comincia a portare) la velocità passa da indietro ad avanti: a 45° con 10 nodi da −0,86 a +0,51 nodi.

Prova con un pilota che usa solo i tasti della scotta, alla velocità dei tasti (0,27 al secondo): cazza se la barca va indietro, lasca se va avanti. Su 12 corse (6, 10, 14 nodi; prua 45° e 50°; barra al centro o che tiene la prua):
- velocità sempre sotto 0,07 nodi dopo i primi 10 s;
- scotta fra 42% e 50%;
- la barca però **scarroccia di lato**: 2 m in un minuto con 6 nodi, 6 m con 10 nodi, 12 m con 14 nodi.

È una prova sola per caso, senza raffiche: dice che si può, non quanto è difficile per una persona.

**Una cosa da segnalare, che non si cambia qui:** nel gioco la barca ferma con la barra al centro tiene la prua dov'è (in un minuto non si è mossa di un grado). Nessuna fonte letta dice cosa fa la prua di una deriva ferma: resta un punto aperto, da cercare (§6).

## 3. Proposta

**A. Lezione 18, un passo nuovo «Stare fermi»** dopo «Aspettare vicino alla linea», con un esercizio fuori dalla regata:
- testo, più o meno: «Lasciata a sé, la barca ferma va indietro e sottovento. Per restare ferma: prua appena sotto la bolina, vela quasi tutta lascata. Se la barca comincia ad andare indietro, cazza un poco finché la vela porta appena; se va avanti, lasca. Si cazza e si lasca di poco, continuamente. La barca scarroccia lo stesso un po' di lato: tienine conto»;
- esercizio: 10 nodi, senza raffiche, barca ferma a 45°; obiettivo **restare per 30 s entro 8 m dal punto di partenza**, sempre sotto 1 nodo. Un cerchio in acqua mostra il limite.

**B. Lezione 19, esercizio cambiato:**
- si comincia **30 s prima del via** invece di 10, a 45° invece di 60°;
- obiettivo: restare fermi (sotto 1 nodo, entro 8 m) fino al via, poi partire e tagliare la linea entro `ES_C2` s;
- il testo «Resta fermo fino al via: non cazzare prima» diventa «Tieni la barca ferma fino al via, giocando con la scotta come nella lezione 18».

**C. Riepiloghi** delle due lezioni aggiornati con una riga sullo stare fermi.

**Cosa non si fa:**
- **remare col timone** (*sculling*): vietato dalla regola 42 (F27, F87), e nel gioco non c'è;
- **la vela a collo** (boma spinto controvento) per andare indietro: F87 la cita, ma nel gioco non esiste e non la propongo.

**Costanti nuove (ipotesi nostre):** 30 s di attesa, 8 m di cerchio, 1 nodo come «fermo» (già usato nella lezione 19), 45° di prua all'inizio.

## 4. Criteri (soglie nostre, scritte prima di misurare)

- **F1, l'esercizio si può fare:** il pilota coi soli tasti della scotta lo supera in almeno 18 regate su 20 (semi 1-20), poi in almeno 18 su 20 sui semi 21-40 mai guardati. Si riportano i metri massimi di scarroccio.
- **F2, non si fa da solo:** senza toccare la scotta (vela tutta lascata) l'esercizio fallisce in almeno 18 regate su 20. Così si misura davvero lo stare fermi, e non il caso.
- **F3, la lezione 19 resta fattibile:** il pilota tiene la barca ferma fino al via e taglia la linea entro `ES_C2` in almeno 18 su 20. Se non ci sta, si riporta il tempo e non si cambia `ES_C2` senza dirlo.
- **F4, pannello** a 1360x650 senza pixel in eccesso, coi testi nuovi.
- **F5, non-regressione:** `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` identici (la fisica non cambia); `collaudo_lezioni.py` per le lezioni 18-19, guidando la barca, anche senza `#collaudo`.

## 5. Rischi

- **Troppo difficile con la tastiera:** la fascia buona della scotta è stretta, circa un terzo di secondo di tasto. Lo misura F1 col pilota alla velocità dei tasti; per una persona può essere più dura, e lo dirà la prova a mano.
- **8 m sono una scelta nostra:** con 14 nodi lo scarroccio arriva a 12 m in un minuto. L'esercizio è a 10 nodi e 30 s (circa 3 m previsti).
- **Le fonti sono poche** (§6): una affermazione con una fonte sola è una scelta dichiarata.

## 6. Fonti

- **F25** (WindCheck): esercizio di stare quasi fermi con la vela che sbatte. Già usata.
- **F27** (J. Emmett, ILCA, «Starting for Lasers», 1 maggio 2018; ora letta per intero, prima solo in parte): in attesa la barca sta appena sotto la bolina; regola 42, cosa è permesso col timone e cosa no. Non parla di scotta né di marcia indietro.
- **F87, nuova** (S. Chapin, blog «How to Sail the Laser», «Laser: stop, stay, and go», 23 agosto 2009): se la barca comincia ad andare indietro, si cazza un poco la vela per tenere la posizione (frase esatta verificata il 13 novembre); per andare indietro si mette la vela a collo, spingendo il boma controvento. Blog personale e vecchio. In calce un lettore ricorda che remare col timone per compensare la vela a collo è vietato (interpretazioni della regola 42, 2005). Con F25 e il gioco misurato (§2) dice la stessa cosa di Lucio: una fonte scritta sola, quindi è una scelta dichiarata.
- **Non letto:** M. Ingham, «How to Hold Your Position on the Starting Line», *Sailing World*, 24 agosto 2021. Dal titolo è l'articolo giusto, ma il testo non si è aperto: se Ale riesce ad aprirlo nel browser, basta incollarne il testo.
- Da cercare: cosa fa la prua di una deriva ferma (poggia? orza?), e una seconda fonte su «cazzare un poco per non andare indietro».

## 7. Cosa serve da Ale

1. **Il via.**
2. **A, B o tutte e due** (§3). Propongo tutte e due: A insegna, B fa usare quello che si è imparato.
3. Se puoi, il testo dell'articolo di *Sailing World* (§6).

## 8. Costo

Circa mezza giornata: testi, i due esercizi, il pilota per F1-F3 e il collaudo delle lezioni.
