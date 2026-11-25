# Sessione speciale: far andare la barca come un ILCA 7 (voce 84)

*25 novembre 2026. Idea di Ale: «se ti do una giornata di ricerche e prove, puoi riprovare coi crediti ripristinati?». Riapre la voce 81 (chiusa lo stesso giorno come limite noto) **solo per ricerche e prove**. Il nome della classe resta nei documenti, mai nel gioco (principio 5).*

**Stato: in attesa dei crediti. `js/` non si tocca: alla fine c'è un rapporto, e il motore cambia solo con un altro via.** Modello: Opus.

## Da dove si riparte (misurato, non si rifà)

- Scafo, misure e resistenza in acqua sono già quelli del Laser (F16, F17, F121). **Manca spinta alla vela col poco vento:** bolina −10/−16% con 3-9 nodi, giusta a 12, +6% a 15; virata con 3,2 nodi 1,74 m persi invece di 0,67; poppa −8/−10%.
- Provati e scartati: braccio 2,4-3,0, svergolamento semplice (Day), rampa da sola, rampa con resistenza e braccio, rollata (tre prove). Numeri in `PROPOSTA-VELA-E-RAMPA-81.md` e `PROPOSTA-BARCA-73.md`.
- Il nodo: il braccio vero è circa 3,0 m (F121), ma con 2,8-3,0 la virata a 16 nodi fallisce e le raffiche rovesciano. Col 2,0 di oggi questo difetto resta nascosto.

## Cosa c'è di nuovo da provare (ordine)

1. **Altre fonti** (prima di toccare numeri): una seconda misura della virata a 10-12 nodi, polari misurate in acqua o tracce GPS, curve di portanza e resistenza della vela, quanto il timoniere raddrizza davvero e in quanto tempo. Licenze e citazioni come sempre.
2. **La curva intera della vela al posto della rampa:** finora si sono cambiate costanti della rampa; non risulta provata una curva CL/CD presa da una fonte. Da ricontrollare nel banco prima di cominciare.
3. **Perché a 16 nodi, col braccio 3,0, la virata fallisce:** cercare la causa nella manovra (tempo e forza del timoniere, pala del timone, vela che sbatte) invece di accorciare il braccio. È l'ipotesi che vale di più: se cade quel blocco, il braccio vero diventa usabile.
4. **Tutti i parametri insieme**, non uno o tre per volta, con il metodo di sotto.
5. **I 9 nodi oltre i 46°** (−6/−11% senza causa): guardarli per ultimi, con la barca nuova.

## Metodo

- Si lavora sul banco (`sperimentale/bolina-81/`), col motore copiato. Ogni parametro sta dentro un intervallo scritto con la sua fonte **prima** della ricerca; chi è senza fonte si dichiara.
- **Si tara su una parte dei dati e si conferma sull'altra:** si tara su Day (6, 10, 15 nodi) e F121; si conferma su Binns (9, 12) e F109. **Limite:** quei dati li abbiamo già visti tutti; una conferma davvero nuova può venire solo dalle fonti del punto 1.
- Una prova per volta, col freno termico; i risultati negativi si scrivono.

## Criteri (le soglie della prima proposta, `PROPOSTA-BOLINA-POCO-VENTO.md`: non si allentano)

B1 Day 6 nodi −5%; B2 Binns 9 nodi ±5%; B3 Binns 12 nodi ±3%; B4 Day 15 nodi al più +7%; B5 3,2 nodi a 45° −8%; B6 virata a 3,2 nodi almeno −30% di metri persi; B7 poppa e lasco entro 0,03 nodi; B8 ogni costante cambiata con una fonte. B7 va discusso con Ale prima di cominciare: tiene la poppa com'è, ma contro Day è lenta dell'8-10%. In più, perché il gioco resti giocabile: a 16 nodi la virata con la sola freccia riesce entro 5 s; raffica da 10 a 18 senza reagire sotto 60° (oggi 52°); angolo morto: barca ferma a 0-15° sotto 0,3 nodi dopo 30 s.

## Quando ci si ferma

- **Passa:** B1-B6 e B8 più i tre criteri di gioco. Allora proposta per il motore, e via di Ale.
- **Non passa:** rapporto con il candidato migliore e cosa gli manca, la 81 torna limite noto e **non si riapre senza una fonte nuova**.
- Tetto: una giornata. Se il punto 1 non porta niente e il punto 3 nemmeno, ci si ferma lì e lo si dice.

## Cosa costa se riesce

Lezioni (angolo morto, raffica, scuffia), rivali, tempi, medaglie, record e stagione da rimisurare (record e medaglie azzerabili); lavoro di Opus in più sessioni. Per questo, se si fa, va **prima** della 2 e della scala dei rivali (82), che si tarano sulla barca. Le regate di Ale e Lucio per la 2 e Z7 restano utili, ma con la barca nuova i tempi andrebbero rifatti.
