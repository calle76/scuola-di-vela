# Proposta: partenze e avversari del livello 1 (fermata 1, 16 ottobre 2026)

Voce 4 della ROADMAP, osservazione 47. **Ale (16 ottobre 2026):** gli avversari fanno bene a partire quasi fermi, come nelle regate vere; è sbagliato il consiglio del riquadro («l'ideale è tagliarla lanciato proprio allo zero»). Il resto è da rivedere.

Il compito si divide in parti, una alla volta. Questa proposta riguarda solo la **parte 1: la partenza degli avversari e il consiglio del riquadro**. Le altre sono in fondo, con quello che già si sa.

## 1. Cosa succede oggi (misure del 16 ottobre)

**Avversari oltre la linea allo sparo** (`collaudo_partenze.py`, parte «anticipi allo sparo», semi 1-20, 360 partenze di avversari, giocatore fermo), dai giri completi di Ale salvati in `tests/output/lancia_tutti/`:

| Versione | Principianti | Esperti |
| --- | --- | --- |
| fino alla 1.0.4 (giri del 12-16 ottobre mattina) | 22,2% | 30-32% |
| dalla 1.0.6 (giri del 16 ottobre pomeriggio e sera) | **82,8-85,0%** | **82,8-83,9%** |

Oltre la linea, mediana 1,8 m (principianti) e 2,6 m (esperti), massimo 11-13 m; tornano dietro in 3,5-4,2 s (mediana); ritardo al via, mediana 8-10 s. **Il salto è passato inosservato:** il collaudo è «da controllare», e il suo unico controllo automatico («ogni anticipata di nuovo dietro la linea entro 60 s») è rimasto OK.

**Causa.** Nella 1.0.6 il codice degli avversari non è cambiato: è cambiata la barca (resistenza della vasca, minore a bassa velocità). Gli avversari smettono di avanzare quando sono a 7 m dalla linea (`js/regate.js:217`: prua a 62° dal vento, vela tutta lascata). Misura sul motore, 10 nodi, partendo lanciata:

| | da 4 nodi | da 5 nodi |
| --- | --- | --- |
| barca della 1.0.4 | 5,5 m verso il vento, 14 s | 6,2 m, 15 s |
| barca di oggi | **10,2 m**, 29 s | **11,3 m**, 30 s |

I 7 m bastavano alla barca vecchia, non a questa. **Controprova sulla causa scartata:** la stima della velocità con cui partono verso la linea (1,9 m/s, `js/regate.js:213`) portata a 2,3 e 2,7 m/s lascia anticipate l'81-84% e il 61-66%: non è lei.

## 2. Proposta per la parte 1 (seconda stesura, dopo la revisione in chat: §6)

**Il modello più semplice vicino alle fonti:** aspettare quasi fermi una o due lunghezze dietro la linea, poi cazzare con l'anticipo che serve per essere **a piena velocità allo zero** (Couranz: una lunghezza dietro, si cazza circa 8 s prima; Dellenbaugh: alla linea in bolina, a piena velocità, a zero; ILCA: si accelera meglio da appena sotto la bolina).

**Misure sul motore che la reggono** (vela tutta lascata, prua fissa, regime; + = verso la linea):

| Vento | prua 55°: verso la linea / di lato | prua 62°: verso la linea / di lato |
| --- | --- | --- |
| 6 nodi | −0,05 / −0,01 m/s | +0,07 / +0,20 |
| 10 nodi | −0,12 / −0,01 | +0,08 / +0,34 |
| 15 nodi | −0,24 / +0,01 | +0,04 / +0,45 |
| 20 nodi | −0,38 / +0,08 | −0,08 / +0,49 |

A 55° la barca arretra (di più col vento forte: 23 m al minuto con 20 nodi) e non scivola di lato; a 62° avanza appena ma scivola di lato verso un estremo. Da ferma a 55°, cazzando e poggiando a 50°, con 10 nodi: 4,1 nodi dopo 6 s (4,5 m percorsi verso il vento), 4,5 dopo 8 s (7,4 m); con 6 nodi 2,4 nodi dopo 8 s; con 15 nodi 5,8 dopo 8 s.

**Regola:**
1. **Avvicinamento come oggi**, fino alla **fascia d'attesa**: da 4 a 8 m dietro la linea (una o due lunghezze; ipotesi nostra appoggiata a Couranz).
2. **In attesa** (vela tutta lascata): più indietro della fascia, prua a 62° (avanza piano); dentro la fascia o più avanti, prua a 55° (arretra appena, senza scivolare di lato). **Il freno vale su tutta la linea e sui suoi prolungamenti**, non solo entro 5 m dagli estremi come oggi (`js/regate.js:217`, il caso dei 17,7 m del seme 74). Lo scivolamento di oggi (10-11 m) è coperto perché il freno parte dove la barca non è ancora lanciata: si entra nella fascia arrivando da dietro, a bassa velocità.
3. **Quando partire:** quattro volte al secondo l'avversario **simula in anticipo la propria partenza** con lo stesso `step()` (copia del suo stato, vento del punto, cazza e poggia verso la bolina larga) e misura in quanti secondi taglierebbe la linea. Parte quando quel tempo, più un **margine del carattere**, arriva al tempo che manca allo sparo. Così vale con ogni vento e da ogni distanza (osservazione della chat sui «4 s fissi»), senza tabelle.
4. **Caratteri e livello:** margine ed errore sul momento di partire (ipotesi nostre): esperti margine 0,5 s ed errore ±0,5 s; principianti margine 1 s ed errore ±2 s; prudente +1 s; aggressiva come esperta. Così gli esperti anticipano **meno** dei principianti (oggi è il contrario).

Costanti nuove, tutte **ipotesi nostre**: fascia 4-8 m, prue 55° e 62° (misurate qui sopra), margini ed errori dei caratteri. Si sceglie sui semi 1-20 e si conferma sui 21-100 mai guardati.

**Riquadro delle istruzioni** (`js/regate.js:149`): via «l'ideale è tagliarla lanciato proprio allo zero»; al suo posto: «Allo scadere del conto alla rovescia devi essere dietro la linea: conviene aspettare vicino alla linea, quasi fermo con la vela lascata, e cazzare negli ultimi secondi per essere già veloce allo zero.» Fonti scritte (§6) in `FONTI-PUBBLICHE.md` e `CONTENUTI-DA-VERIFICARE.md`.

**Pannello del giocatore** («Alla linea: … s alla velocità attuale», `js/regate.js:470`): oggi il tempo compare sopra 0,2 m/s verso la linea e, appena sopra, dà numeri alti (20 m a 0,21 m/s = 95 s). Proposta minima: mostrarlo solo se è sotto 60 s. Il giocatore che aspetta fermo vede solo i metri, come oggi.

## 3. Criteri (soglie nostre, seconda stesura, prima di provare)

Si misurano con 6, 10 e 15 nodi (15 è il massimo impostabile), senza e con raffiche, semi 1-20 per scegliere e 21-100 per confermare.

1. **Richiami per partenza** (almeno un avversario oltre la linea allo sparo, 3 avversari): **al massimo 30% con i principianti e 20% con gli esperti**, e esperti meno dei principianti. Si riporta anche la quota per barca. La realtà non la conosciamo: sono attese nostre. (La 1.0.4, per barca 22-32%, dava richiami in circa la metà delle partenze: l'osservazione 47 è nata lì, quindi quel livello non va preso come buono.)
2. **Ritardo al via** (mediana, dallo sparo al taglio): **al massimo 3 s** con 1, 3 e 5 minuti.
3. **Velocità al taglio** (mediana): **almeno il 75%** della velocità di regime della barca a 50° dal vento con quel vento (10 nodi: 4,6 nodi → almeno 3,5).
4. Nessun avversario non partito entro 60 s dallo sparo.
5. Regate a bastone e nelle raffiche (`collaudo_regate.py`, semi 1-6): 18 arrivi su 18, nessuna BLOCCATA.
6. **Controllo del metro:** il collaudo stampa quante barche ha visto davvero nella fascia d'attesa nell'ultimo minuto e le velocità al taglio; senza barche in fascia l'esito non vale.
7. `polare.js` e `raffiche_e_virate.js` identici; pannello del riquadro senza eccesso.
8. `collaudo_partenze.py` diventa **FALLITO** se non rispetta i criteri 1, 2 o 3.

Senza soglia, si riportano: posizione allo sparo lungo la linea (quanti fuori dagli estremi) e spostamento laterale in attesa; contatti fra avversari nelle regate; `collaudo_competizione.py` C1.

## 4. Rischi

- **Barche ferme vicine si toccano di più:** si misura; la correzione è la parte 3.
- **Prua a 55° vicino all'angolo morto:** con una raffica che gira la barca può piantarsi; per questo i criteri si misurano anche con le raffiche (criterio 4).
- **La simulazione in anticipo costa calcolo:** circa 10 s simulati a 1/60 s per avversario, quattro volte al secondo: circa 7.000 passi al secondo con 3 avversari. Da misurare nel browser; se pesa, due volte al secondo.
- **Il giocatore** non ha questo aiuto: il riquadro dice il metodo, i numeri li legge nel pannello.

## 5. Le altre parti (dopo, una alla volta)

- **Parte 2, estremi della linea:** avversari che partono fuori dagli estremi e devono rientrare. Da misurare dopo la parte 1, perché cambia dove aspettano.
- **Parte 3, contatti fra avversari:** nella regata a bastone (semi 1-6, giro di Ale) prendono una penalità per contatto in 13 piazzamenti su 18. Da misurare dopo la parte 1.
- **Parte 4, rientro dopo l'anticipo:** domanda di Ale nell'osservazione 47 («deve aspettare o può rientrare subito?»). Regola 29.1 (`REGOLE-DI-REGATA.md`): basta tornare dalla parte di pre-partenza e ripartire, senza attese; la 21.1 (dare acqua a chi non sta rientrando) è livello 2.
- **Parte 5, pilota da tastiera fermo all'indietro prima del via** (`collaudo_competizione.py --tastiera`, NON VALIDO dalla 1.0.11): è un collaudo, non il gioco. Probabilmente la stessa causa (barca che a 41-49° dal vento con la vela lascata arretra); da guardare con la parte 1.
- **Parte 6, `collaudo_competizione.py` C1** (pilota sostituto ultimo nel 46-48% delle regate, fascia 10-40%): lo spostano le penalità dei contatti. Si rimisura dopo le parti 1 e 3.

## 6. Revisione in chat (16 ottobre 2026) e cosa è cambiato

- **25% «accettato» era falso** (l'osservazione 47 è della 1.0, prima del salto) e **contato per barca**: con 3 avversari il 25% per barca dà almeno un richiamo in circa il 58% delle partenze. → criterio 1 per partenza, 30% / 20%.
- **«Poco dopo lo zero, a bassa velocità» contraddiceva le fonti.** → si parte per essere a piena velocità allo zero; criterio 3 sulla velocità al taglio.
- **4 s fissi non tengono conto della distanza.** → simulazione in anticipo con `step()`.
- **Misure solo a 10 nodi.** → tabella a 6-20 nodi qui sopra; criteri a 6, 10 e 15 nodi e con raffiche.
- **FALLITO anche per il ritardo.** → criterio 8.
- **Freno solo vicino agli estremi.** → freno su tutta la linea e prolungamenti.
- **Caratteri appiattiti; esperti oggi anticipano più dei principianti.** → margini per carattere e livello, criterio «esperti meno dei principianti».
- **Partenza nelle raffiche, scivolamento laterale, pannello del giocatore:** aggiunti (criteri, riporto, §2).
- **Fonti scritte trovate dalla chat** (da registrare in `FONTI-PUBBLICHE.md` alla fermata 2): Kim Couranz, *Let's Get This Race Rolling* (SpinSheet); Dave Dellenbaugh, *Practice drills for better starts* (WindCheck); MIT Sailing, *Sailboat racing* (avvicinarsi lentamente alla linea fra 30 s e 1 minuto prima); SailJuice, *Starting Episode 3: The Dinghy Start* (video RaceQs); ILCA, *Starting for Lasers* (Emmett: si accelera meglio da appena sotto la bolina). Non ancora lette da Claude Code: alla fermata 2 si controlla che dicano quanto riportato.

## 7. Fermata 2, esito (17 ottobre 2026): parte 1 chiusa nella 1.0.16

**Regola finale** (codice in `js/regate.js`, costante `BOAT.length` in `js/motore.js`): nessun numero in metri scritto a mano.

1. **Fascia d'attesa in lunghezze di barca** (`BOAT.length` = 4,2 m): da una a due lunghezze dietro la linea, punto d'attesa a 1,5 lunghezze.
2. **Punto di ritrovo a 6 lunghezze** (25 m) dietro la linea fino a 45 s dal via; l'avvicinamento vero comincia lì. Così l'attesa vicino alla linea dura mezzo minuto e non tre.
3. **Attesa e ritrovo spostati di lato** di `tan(bolina+4°)` per ogni metro che resta da guadagnare: la scivolata della risalita porta la barca dove deve tagliare, fra le boe.
4. **Avvicinamento con la logica generale** degli avversari, che sa fare i bordi (vedi «difetti trovati» sotto).
5. **Quando lascare:** due volte al secondo `glideY()` simula con lo stesso `step()`, su una copia dello stato, dove la barca si fermerebbe lascando adesso; si lasca quando quel punto cade dentro la fascia.
6. **Quando partire:** quattro volte al secondo `startTime()` simula in quanti secondi taglierebbe cazzando adesso; si parte quando quel tempo più il margine del carattere arriva al conto alla rovescia. Margini (ipotesi nostre): esperti 0,5 ± 0,5 s, principianti 1,5 ± 1,5 s, prudente +1 s.
7. **In attesa** (vela tutta lascata): prua a **55°** dal vento, **45°** sotto mezza lunghezza dalla linea. Il freno vale su tutta la linea e sui prolungamenti.
8. **Riquadro delle regate** e **pannello** come al §2.

**Cambio dichiarato rispetto al §2:** la prua di attesa a **62°** per chi sta più indietro della fascia **è stata tolta**. Misura: a 62° la barca avanza di 0,04-0,08 m/s ma scivola di lato 0,3-0,5 m/s, cioè una trentina di metri in un'attesa lunga, e finisce fuori dagli estremi; a 55° il lato è 0,01 m/s. Deciso dopo aver visto le misure, non prima.

**Difetti trovati per strada** (nessuno dei tre era nella proposta):
- il contatore dei bordi (`boardT`) scadeva durante l'attesa, così **allo sparo tutti viravano subito**, perdendo metà della velocità proprio prima della linea. Ora resta a zero fino al taglio e la prua della partenza si tiene finché non si taglia;
- **chi era segnato anticipato** continuava a tenere la prua della partenza e se ne andava di bolina senza mai partire (37 avversari su 720). Ora esce dal blocco della partenza e rientra con la logica generale, che punta la linea, come prima della 1.0.16;
- puntando il punto d'attesa **con una prua sola** la barca scivolava fino a 90 m di lato e aspettava lì, fuori dagli estremi, dove il taglio non conta: il freno guardava solo la distanza dalla linea, non quella dal punto.

**Misure finali** (`collaudo_partenze.py`, criteri del §3; semi 1-20 per scegliere, **21-100 mai guardati** per confermare, 2880 partenze di avversari):

| | principianti | esperti | soglia |
| --- | --- | --- | --- |
| partenze con un richiamo, bastone 10 nodi | 6,7% | 5,4% | 30% / 20%, esperti meno |
| partenze con un richiamo, raffiche 12 nodi | 4,6% | 3,8% | 30% / 20%, esperti meno |
| ritardo mediano al via (1, 3, 5 min) | 1,9-2,2 s | 0,9-1,1 s | 3 s |
| velocità mediana al taglio (bastone / raffiche) | 4,85 / 5,33 nodi | 4,65 / 5,12 | 3,72 / 4,20 |
| non partiti entro 60 s | 0 | 0 | 0 |
| passati dalla fascia d'attesa | 718-719 su 720 | 718-719 su 720 | almeno metà |

Esito **OK** sui semi di conferma. Sui semi 1-20 l'unico criterio fuori era «esperti meno dei principianti» nelle raffiche, **3,3% contro 3,3%**: pari, cioè 2 richiami su 60 contro 2 su 60, differenza non misurabile con 20 semi; con 80 semi si separa. Nessuna anticipata fuori dagli estremi. Calcolo 3,1 ms per secondo simulato (massimo 5,8). Regate a bastone e raffiche (semi 1-6): 18 arrivi su 18, nessuna BLOCCATA. `polare.js` e `raffiche_e_virate.js` identici; pannello e riquadro 0 px di eccesso a 1360×650.

**Non misurato:** contatti fra avversari (parte 3) e `collaudo_competizione.py` (parte 6).

**Fonti** (elenco e stato in `FONTI-PUBBLICHE.md`, F25-F30): regge il metodo «aspettare quasi fermi una o due lunghezze sotto la linea e accelerare per essere a piena velocità allo zero» (WindCheck, F25, contenuto confermato il 17 ottobre). L'articolo di SpinSheet da cui veniva il numero «si cazza circa 8 s prima» **non è stato ritrovato** (F26): quel numero non è usato nel codice e non compare nel gioco. ILCA, MIT e SailJuice non sono stati letti. Per avversari che *scelgono* le mosse in partenza esiste un modello pubblicato (teoria dei giochi e Monte-Carlo tree search, F30, solo abstract letto): materiale per il livello 2.

**Conferma di Ale (17 ottobre 2026):** in questa classe di barche si parte da fermi, non lanciati; le barche grandi e pesanti che partono lanciate restano una nota per i livelli futuri.

**Idea di Ale tenuta in riserva (17 ottobre 2026):** se la deriva in attesa tornasse a dare problemi, invece di far manovrare la barca si può aiutarla da fuori — vento ridotto oppure resistenza dell'acqua moltiplicata mentre aspetta (ancora virtuale, come `backDrag`). Con le misure di questa versione non serve, e sarebbe un aiuto che il giocatore non ha: da dichiarare.
