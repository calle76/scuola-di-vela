# Sessione speciale: far andare la barca come un ILCA 7 (voce 84)

*25 novembre 2026. Idea di Ale: «se ti do una giornata di ricerche e prove, puoi riprovare coi crediti ripristinati?». Riapre la voce 81 (chiusa lo stesso giorno come limite noto) **solo per ricerche e prove**. Il nome della classe resta nei documenti, mai nel gioco (principio 5).*

**Stato: sessione fatta il 25 novembre 2026 (coi crediti), esito in fondo. `js/` non toccato: alla fine c'è un rapporto, e il motore cambia solo con un altro via.** Modello: Opus.

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

B1 Day 6 nodi −5%; B2 Binns 9 nodi ±5%; B3 Binns 12 nodi ±3%; B4 Day 15 nodi al più +7%; B5 3,2 nodi a 45° −8%; B6 virata a 3,2 nodi almeno −30% di metri persi; B7 poppa e lasco entro 0,03 nodi; B8 ogni costante cambiata con una fonte. B7 vale nella prima parte (bolina). **Seconda parte, solo se la bolina passa (Ale, 25 nov: «sì come proponi tu»): anche la poppa.** Al posto di B7 vale B7b, scritto ora prima di ogni prova: VMG di poppa contro Day (F17 fig. 8) entro ±4% a 6, 10 e 15 nodi (oggi −8/−10%), senza che B1-B6 e i tre criteri di gioco smettano di passare. ±4% è un'attesa nostra. Se B7b non passa, resta la sola correzione della bolina, con B7. In più, perché il gioco resti giocabile: a 16 nodi la virata con la sola freccia riesce entro 5 s; raffica da 10 a 18 senza reagire sotto 60° (oggi 52°); angolo morto: barca ferma a 0-15° sotto 0,3 nodi dopo 30 s.

## Quando ci si ferma

- **Passa:** B1-B6, B7 (o B7b nella seconda parte) e B8, più i tre criteri di gioco. Allora proposta per il motore, e via di Ale.
- **Non passa:** rapporto con il candidato migliore e cosa gli manca, la 81 torna limite noto e **non si riapre senza una fonte nuova**.
- Tetto: una giornata. Se il punto 1 non porta niente e il punto 3 nemmeno, ci si ferma lì e lo si dice.

## Cosa costa se riesce

Lezioni (angolo morto, raffica, scuffia), rivali, tempi, medaglie, record e stagione da rimisurare (record e medaglie azzerabili); lavoro di Opus in più sessioni. Per questo, se si fa, va **prima** della 2 e della scala dei rivali (82), che si tarano sulla barca. Le regate di Ale e Lucio per la 2 e Z7 restano utili, ma con la barca nuova i tempi andrebbero rifatti.

## Esito della sessione (25 novembre 2026, `js/` non toccato)

**In breve:** trovato un candidato che porta la bolina sulle fonti e che toglie il nodo della virata a 16 nodi col braccio vero (3,0 m). **Non passa tutto: B2 manca di 0,1 punti e B8 no** (otto numeri restano ipotesi). Per la regola scritta sopra la sessione «non passa»; la decisione è di Ale.

| Criterio | Soglia | Oggi | Candidato | |
|---|---|---|---|---|
| B1 Day 6 nodi (VMG) | ±5% | −15,7% | **−1,0%** | passa |
| B2 Binns 9 nodi, 42 / 46,5 / 55 / 60° | ±5% | −15 −12 −13 −14 | +0,7 −0,8 −3,6 **−5,1** | **no, per 0,1** |
| B3 Binns 12 nodi | ±3% | −2,3 … −0,1 | −1,1 … +0,2 | passa |
| B4 Day 15 nodi | ≤ +7% | +6,5% | +1,5% | passa |
| B5 3,2 nodi a 45° (1,05 m/s) | −8% | 0,89 (−15%) | 1,11 (+5,4%: sopra la misura) | passa (il criterio non ha un limite in alto) |
| B6 virata 3,2 nodi | −1,22 m | −1,74 | −1,11 m (F109 −0,67) | passa |
| B7b VMG di poppa contro Day, 6/10/15 | ±4% | −10 −8 −9 | −3 −2 −2 | passa |
| B7 (prima parte; sostituito da B7b) | 0,03 nodi | — | traverso 12 nodi 7,18 → 7,31, 180° 4,67 → 5,05 | no |
| B8 ogni costante con fonte | sì | — | vedi sotto | **no** |
| Virata 16 nodi con la freccia | 5 s | 2,9 s | 2,3 s | passa |
| Raffica 10→18 senza reagire | < 60° | 52° | 54° | passa |
| Fermi a 0-15°, 30 s | < 0,3 nodi | sotto zero | sotto zero | passa |

In più: F121 (2, 3, 4, 5 nodi di barca) da −11 −12 −12 −5% a **+10 +6 +3 +2%** (il modello della tesi è esso stesso ottimista, quindi il poco vento del candidato è un po' sopra); B2 ±5% **non lo passa neppure Day** a 60° con 9 nodi (5,52 contro 5,9 nodi, −6,4%, fig. 4).

### Cosa era sbagliato (con la fonte)

1. **La vela spingeva il 12% meno.** I coefficienti ORC di Day valgono per la tela intera (circa 7,92 m²); il gioco li applica a 7,0. Controllo doppio: formula ORC sulle larghezze del disegno di classe (F119 pag. 35) = 7,92; Day corregge Flay ×1,125 dal triangolo (7,03) = 7,91. Le larghezze sono massimi di classe, la testa (0,12 m) è stimata a occhio.
2. **La curva della vela:** tabella ORC «low lift» (Day tab. 1) letta all'incidenza + 9°, e resistenza scomposta come Day fig. 12 (scafo, albero e timoniere 0,105; totale 0,24). Prima era una retta da zero, più una rampa.
3. **Il peso:** lo scafo è in vasca a 160 kg, la barca pesava 135. Day ha pesato 79,5 kg la barca armata, più 80 kg di timoniere.
4. **La stabilità:** F121 fig. 31 dà braccio raddrizzante 0,145 m a 9° (circa 190-230 N·m); il gioco 62. È circa 3 volte meno.
5. **Vento forte:** Day appiattisce (fino a 0,6) e svergola (0,186) la vela quando il timoniere è al limite. **Il nodo del braccio 3,0 era questo:** a 16 nodi la barca aveva due equilibri, 6° e 44° di sbandamento. Con vela piatta sta in quello giusto e vira in 2,3 s.
6. **Poppa:** galleria del vento Magnander (F124): 1,40-1,42 a 90° di scotta; deriva e timone frenano la metà in poppa (Day fig. 11, deriva mezza alzata). Nel gioco diventa automatica: **semplificazione da dichiarare**.

### Ipotesi senza fonte (perché B8 non passa)

Ampiezza della rampa `w` 8 e `a0` 2 (6-10 passano tutti i criteri che passa 8; 14 no, per B6); boma 9° come spostamento della tabella (F109 tab. 4.1 misura 13-19° al 62% della vela, compatibile); passaggio 40-60° di vento apparente dalla curva nuova alla vecchia; ritardo 0,9 s della vela piatta (2 s fa fallire la raffica: 63°); raddrizzata oltre 22,5° (linea fino a 90°); altezza del timoniere dz 0 (con 0,15 il motore reggeva, con 0,3 no, sul candidato precedente); angoli 100-140° dal vento fra cui la deriva «si alza». La resistenza della vela che sbatte (0,08) è scelta perché il totale resti quello di oggi. In tutto otto. **Ordine dei fatti, da dire:** area 7,92 e 0,08 sono stati messi **dopo** aver visto i numeri (B1 era −5,2 con l'area 7,0 e −4,9 con 7,06; con l'area 7,92 B6 falliva finché non si è tolto il doppio conteggio, 0,2 → 0,08).

### Cosa non convince

- **La virata col vento medio si allontana dalla misura quando la scotta resta ferma:** 11 nodi, −1,45 m (oggi −3,35; F109 −4,39); col pilota 1,1-1,6 m a 10-14 nodi (F106: 2,1; oggi 3,0-3,8). In F109 però il timoniere **lasca 15° per 3 s**: rifatto così −2,15 m (boma 24°) o −3,88 (34°), velocità minima 49% (F109 51%, oggi 40%). Resta un difetto possibile, non chiuso. `virata1b` criterio 1 è fuori a tutti e sei i venti (troppo veloce).
- **Angolo morto più stretto:** con 6 nodi si avanza a 1,8 nodi a 25° (oggi −0,3) e a 0,9 a 20°. Nessuna fonte lo misura, ma è probabilmente troppo poco angolo morto; lezione e messaggi da rifare.
- **Verifica alla cieca non passata, per nessuna delle due barche:** Marshall (F125): −119 e −178 N·m di raddrizzata danno −9% e −26% di VMG; oggi da 0 a −4% e da 0 a −6%, candidato −2/−4% e −4/−7% (10-16 nodi). Il vento di Marshall non si conosce.
- `orziera1b` criterio 2 fuori di poco a 14 nodi e 90° (1,29 contro 1 °/s).
- Con la scotta della regola il candidato scuffia a regime già a **18** nodi; oggi solo a 20 (a 18 sta a 34°). Con la scotta migliore a 18 va a 5,6 nodi a 45°.
- La conferma su Binns e F109 non è cieca: i numeri si vedevano a ogni prova. La sola prova nuova (Marshall) non passa.

### Prove sul gioco vero (copia, rivali non ritarati)

32 regate col pilota (semi 5001-5008, `misura_manovre`), oggi / candidato: 0 errori, contatti 31 / 31, non arrivati 42 / 40, fuori linea 12 / 10, arrivo mediano dei rivali 195,8 / 181,3 s (−7%), contatti dopo una virata di un rivale 1 / 5 (pochi casi). Motore: 432 casi per 6 passi di tempo, 0 non finiti, stesso risultato con ogni passo. Solo Chromium; lezioni, medaglie e Firefox **non provati**.

### Dove sono i file

`sperimentale/barca-84/`: `INTERVALLI.md` (scritti prima), `banco84.js` (banco), `candidato.json`, `esito_candidato.txt`, `motore84.js` (motore pronto, da `fa_motore84.py`), `scomponi84.js`, `traccia16.js`, `marshall.js`. Fonti nuove in `FONTI-PUBBLICHE.md` F124-F126; quattro file in `fonti-pdf/`. Pagine che rifiutano la lettura automatica (403): Southampton, MDPI (GPS Laser), core.ac.uk: se servono, vanno scaricate a mano.

### Consiglio

Fare la proposta per il motore con questo candidato, **se Ale accetta due cose scritte**: B2 a 60° (−5,1, dove la stessa fonte fa −6,4) e otto numeri d'ipotesi dichiarati. Prima di accenderlo: l'angolo morto (w e la lezione), la virata col vento medio, tutte le lezioni, i rivali e i tempi. Se Ale non accetta, la 81 torna limite noto.
