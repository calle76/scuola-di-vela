# Banco delle precedenze: tante situazioni piccole, comportamento e giuria

28 novembre 2026, sera. Idea di Ale: «un collaudo/simulatore di tantissime situazioni diverse in cui le barche devono gestire le precedenze; registrare come si comportano e, nei contatti, come si comporta la giuria; piccoli file come le regate grandi, passati in rassegna con statistiche e problemi». **Fermata 1: solo proposta, nessun codice.** Da discutere nella sessione di brainstorming.

## Perché

Oggi un difetto delle precedenze si trova solo quando capita ad Ale o a Lucio (oss. 154, 155: voci 98, 99). Le scene costruite sono poche e fisse (`collaudo_avversari1b` 5 tipi, `collaudo_regole_15_16` 19 casi); le misure grandi del giro «Misura» contano i contatti ma non guardano le singole situazioni.

## Cosa si costruisce (modello più semplice)

1. **Generatore** (`tests/banco_precedenze.py`): scene da 20-30 s con 2 o 3 barche, tutte guidate dalla guida dei rivali (il giocatore spostato lontano, come in `avversari1b`), in una regata di Deriva con vento costante (regole 15, 16 e 18 accese). Ogni scena da un seme: famiglia e parametri sorteggiati.
   Famiglie: **F1** incrocio con mure diverse; **F2** stesse mure affiancate; **F3** sorpasso da dietro (sopravento e sottovento); **F4** virata o strambata davanti a un'altra; **F5** arrivo alla boa in zona (regola 18); **F6** partenza sulla linea. Parametri: distanze 2-30 m, angoli, velocità 50-110% della polare, vento 8-16 nodi, andatura (bolina, traverso, poppa).
   Variante «col giocatore»: la barca 0 guidata dal pilota dei collaudi con una rotta fissa, per vedere la giuria quando a sbagliare è il giocatore.
2. **Un file piccolo per scena**, nel formato delle registrazioni (righe S, B, E), più una riga di riassunto: chi ha ceduto e da quando, contatti con colpa e regola, semaforo mostrato, tempo perso per barca, manovre strane.
3. **Due pagelle.**
   - *Comportamento:* contatto sì/no; chi doveva cedere ha ceduto (e quanto prima del punto più vicino); chi aveva la precedenza ha tenuto la rotta (regola 16); tempo perso rispetto alla stessa barca da sola; piantate (sotto 0,5 nodi per 5 s); barche che finiscono lontano (oltre 40 m dalla rotta di prima); virate o strambate inutili; zig-zag di chi «ci ripensa» (sezione sotto).
   - *Giuria:* colpa e regola a ogni contatto, confrontate con il riferimento qui sotto.
4. **Riferimento per la giuria** (nessun giudice esperto, `CLAUDE.md`):
   - *scene pulite* (geometria semplice, esito chiaro dalle regole di F15): l'esito atteso si scrive prima, da una tabella costruita sulle regole 10-18 parafrasate, come i casi R1 di oggi;
   - *tutte le altre*: **controlli di coerenza** scritti prima, per esempio: (c1) colpa mai a una barca che andava dritta ed è stata urtata da dietro da una barca con le stesse mure; (c2) il semaforo mostrato nei 2 s prima del contatto dice la stessa cosa della colpa; (c3) la 15 solo dentro T15 da un cambio di precedenza; (c4) la colpa non cambia spostando l'istante del contatto di un passo; (c5) a parità di scena specchiata (destra/sinistra) la colpa va alla barca specchiata;
   - i casi che nessuna delle due strade sa giudicare si segnano «dubbi» e non si giudicano.
5. **Lettore** (`tests/banco_leggi.py`): statistiche per famiglia (contatti ogni 100 scene, colpe per regola, controlli falliti, manovre strane) e l'elenco dei casi peggiori con il loro file. Claude guarda a mano i peggiori e porta ad Ale solo i problemi veri.
6. **Dove gira:** migliaia di scene sul giro «Misura» di GitHub (accetta già `--semi`); sul PC solo poche scene per provare lo strumento, col freno.

## Manovra strana da contare: lo zig-zag di chi «ci ripensa»

Domanda di Ale (28 nov): un rivale dietro o a fianco va a zig-zag strettissimo. Causa letta nel codice e vista nel file 28/11 14:34: a ogni istante la guida (`cedeAvv1b`) rifà la previsione a velocità costante; appena scostata, la previsione dice «passi» e torna verso la rotta voluta, poi di nuovo «non passi». Fra 385 e 392 s la Blu passa da «cede a Tu» a «non cede» 5 volte in 7 s, la prua segue (119° → 139° → 110° → 135° → 76°) e la velocità scende da 5,6 a 4,3 nodi. Freni già presenti: chi cede continua finché non ci si allontana; la 16 accesa resta almeno `T16_TENUTA` (1 s).

Nel banco, per ogni barca e scena (scritto ora, prima di misurare):
- **cambi di idea:** quante volte lo stato «cede a X» si accende o si spegne verso la stessa barca in 10 s; **zig-zag** = almeno 3 cambi in 10 s con la prua che gira ogni volta di almeno 10° (`G16`);
- **costo:** velocità persa e tempo perso rispetto alla stessa barca nella stessa scena da sola;
- **dove:** famiglia, distanza dalla boa, angolo fra le prue.

Il banco dice quanto è frequente e dove; la correzione (più memoria della decisione presa) diventa una voce a sé, con le due fermate e le misure come le altre.

## Domanda da tenere aperta: la regola 17 (voce 100)

Il 28 novembre la regola 17 è risultata quasi assente nelle regate simulate (5 casi su 900 regate, nessuno con colpa al pilota: `sperimentale/voce-100/LEGGIMI.md`). Ma quelle regate le guida il pilota dei collaudi, che non sorpassa mai di proposito da sottovento. Il banco la riguarda apposta:

- nella famiglia **F3** (sorpasso da dietro) una sotto-famiglia **F3s**: chi supera da sottovento entro 2 lunghezze, rivale o giocatore, con la sopravento che tiene la rotta;
- per ogni scena F3s si annota: contatto, colpa e regola date dal gioco, e la colpa che darebbe la 17 (la sottovento che sta sopra la sua rotta propria di più di `G17`, 5°, come nella proposta della voce 100);
- **criterio scritto ora:** la 17 «si sente mancare» se in F3s almeno 1 contatto su 10 cambierebbe colpa con la 17, o se le scene F3s col giocatore danno al giocatore sopravento una colpa che la 17 toglierebbe in almeno 1 caso su 20. Sotto queste soglie la voce 100 si chiude.

## Criteri (soglie nostre, da confermare nel brainstorming)

- **Lo strumento vede:** su 1000 scene, almeno 50 contatti; in ogni famiglia almeno 5 (altrimenti la famiglia si rifà più stretta, dichiarandolo).
- **Le scene pulite si scrivono prima:** almeno 20 per famiglia, con l'esito atteso, prima di lanciare la prima misura.
- **Ripetibile:** stessa scena, stesso seme, stesso esito al byte in Chromium; Chromium e Firefox confrontati e le differenze contate (oggi lo scenario 5 cambia fra i due).
- **Non tocca il gioco:** `index.html` e `js/` invariati; serve solo, se manca, un aggancio di misura in `#collaudo`.
- Il banco **trova** problemi, non li corregge: ogni problema trovato diventa una voce di `DA-FARE.md` con le due fermate.

## Costanti nuove (ipotesi nostre)

Durata della scena 20-30 s; «lontano» 40 m (la stessa distanza di «vicino alla boa» della guida); piantata 0,5 nodi per 5 s (come `avversari1b`).

## Rischi

- Le scene costruite non sono regate vere: completano le registrazioni di Ale e Lucio, non le sostituiscono.
- La giuria si controlla solo contro le regole scritte e la coerenza, non contro una persona.
- Troppe segnalazioni: il lettore ordina per gravità e Claude ne porta poche.
- Costo: medio-grande (Opus), due tappe. Tappa 1: generatore con F1 e F2, file, lettore, controlli c1-c3; si guarda se trova problemi veri. Tappa 2: F3-F6, variante col giocatore, c4-c5.

## Fonti

F15 (World Sailing, RRS 2025-2028), regole 10-18, già usate dal gioco; nessun testo copiato.
