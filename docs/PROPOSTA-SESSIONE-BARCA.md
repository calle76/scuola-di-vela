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

**In breve:** il candidato (versione I) porta la bolina sulle fonti e toglie il nodo della virata a 16 nodi col braccio vero (3,0 m). **Non passa tutto:** B2 per 0,2 punti e solo a 60°; B8 perché restano otto numeri d'ipotesi. Per la regola scritta sopra la sessione «non passa»; decide Ale. La prima chiusura (20 minuti) era incompleta: questa è la versione dopo la ripresa, e **corregge due cose dette prima** (la virata «troppo facile» e lo svergolamento, sotto).

| Criterio | Soglia | Oggi | Candidato I | |
|---|---|---|---|---|
| B1 Day 6 nodi (VMG) | ±5% | −15,7% | **−1,8%** | passa |
| B2 Binns 9 nodi, 42 / 46,5 / 55 / 60° | ±5% | −15 −12 −13 −14 | +0,2 −1,1 −3,8 **−5,2** | **no, per 0,2** |
| B3 Binns 12 nodi | ±3% | −2,3 … −0,1 | −1,3 … 0 | passa |
| B4 Day 15 nodi | ≤ +7% | +6,5% | −0,4% | passa |
| B5 3,2 nodi a 45° (1,05 m/s) | −8% | −15% | +3,6% | passa (il criterio non ha un limite in alto) |
| B6 virata 3,2 nodi | −1,22 m | −1,74 | −1,14 m (F109 −0,67) | passa (limite: −1,218) |
| B7b VMG di poppa contro Day, 6/10/15 | ±4% | −10 −8 −9 | −3 −2 −2 | passa |
| B7 (prima parte; sostituito da B7b) | 0,03 nodi | — | traverso 12 nodi 7,18 → 7,31, 180° 4,67 → 5,05 | no |
| B8 ogni costante con fonte | sì | — | otto ipotesi | **no** |
| Virata 16 nodi con la freccia | 5 s | 2,9 s | 2,4 s (18 nodi 2,7, 20 nodi 4,8) | passa |
| Raffica 10→18 senza reagire | < 60° | 52° | 44° | passa |
| Fermi a 0-15°, 30 s | < 0,3 nodi | sotto zero | sotto zero | passa |

F121 (2, 3, 4, 5 nodi di barca): +8 +5 +3 +2% (oggi −11 −12 −12 −5; la tesi è ottimista). **B2 non lo passa neppure Day** a 60° (5,52 contro 5,9 nodi, −6,4%, fig. 4). Ripartizione delle resistenze in acqua (scafo/appendici/indotta) a 5 nodi: 66/24/11 (Day 67/21/11); a 10 nodi 68/17/15 (Day 66/16/18).

### Quanto dipende dalle ipotesi (Monte Carlo, 170 combinazioni, seme 21, `montecarlo_I.txt`)

Ogni parametro estratto dentro il suo intervallo. Criteri passati: **B1 100%, B4 100%, B5 100%, angolo morto 100%, virata 16 nodi 99%, raffica 99%, B7b 95%, B3 91%, virata 18 nodi 81%, B6 58%, B2 10% (89% senza i 60°)**; tutti tranne B2 51%. Le due cose da guardare sono B6 (dipende da `a0` e `w`) e B2. Le prime due versioni provate davano 31% e 26%: il terzo tentativo è il migliore, ma **è stato scelto dopo aver visto i primi**.

### Cosa era sbagliato (con la fonte)

1. **La vela spingeva il 12% meno.** I coefficienti ORC di Day valgono per la tela intera (circa 7,92 m²); il gioco li applica a 7,0. Controllo doppio: formula ORC sulle larghezze del disegno di classe (F119 pag. 35) = 7,92; Day corregge Flay ×1,125 dal triangolo (7,03) = 7,91. Incertezze: larghezze massime di classe, testa a occhio, manica dell'albero (forse 7,7: compresa nell'intervallo del Monte Carlo).
2. **La curva della vela:** tabella ORC «low lift» (Day tab. 1) letta all'incidenza + 9°, e resistenza scomposta come Day fig. 12 (scafo, albero e timoniere 0,105).
3. **Il peso:** lo scafo è in vasca a 160 kg, la barca pesava 135 (Day: 79,5 la barca armata, 80 il timoniere).
4. **La stabilità:** F121 fig. 31, braccio raddrizzante 0,145 m a 9° (190-230 N·m); il gioco 62.
5. **Vento forte:** vela piatta (fino a 0,6) e svergolata (0,186, poi di più: in Day TWIST va fino a 1) quando il timoniere è al limite. **Il nodo del braccio 3,0 era questo:** a 16 nodi la barca aveva due equilibri (6° e 44° di sbandamento).
6. **La resistenza indotta a bassa velocità:** smorzamento 0,1 al posto di 0,4 (Day fig. 11: 10,5% a 5 nodi; 0,1 dà 11%, 0,4 dava 9%). Allarga l'angolo morto.
7. **Poppa:** vela 1,40-1,42 a 90° (F124); deriva mezza alzata (Day fig. 11), che nel gioco diventa automatica: **semplificazione da dichiarare**.

### Controlli nuovi (dopo la ripresa)

- **Virata secondo per secondo (F109 fig. 4.10-4.12 e tab. 4.1), prua e scotta come nel vero:** scarto medio delle velocità 0,052 (3,2 nodi) e 0,069 (11 nodi); oggi 0,139 e 0,138. Metri persi: −1,89 e −3,45 (F109 −0,67 e −4,39; oggi −2,71 e −6,44). **Corregge la mia prima frase «virata troppo facile»:** era il pilota con la scotta ferma, che nel vero lasca 15° per 3 s. Resta vero che con la scotta ferma e il pilota il gioco perde poco (circa 1-1,6 m a 10-14 nodi; F106: 2,1) e che `virata1b` criterio 1 è fuori a tutti e sei i venti.
- **Il timoniere che cambia lato** (provato): non spiega niente (−3,24 → −3,23 m), e oltre 1 s di traversata fa scuffiare. Scartato.
- **Scarroccio:** F109 5-8°, gioco 2-3° (oggi e candidato). Non corretto (deriva più debole abbassa la bolina).
- **Bethwaite a 6 nodi** (forum, fonte indiretta, riga mai usata): bolina / traverso / lasco / poppa −10 / −20 / −30 / −31% (oggi −17 / −22 / −33 / −37). Le poppe risentono del surf (lo dice Day). Il passaggio 40-60° sta meglio a 12 nodi di traverso (+2%, contro +10/+15%).
- **Marshall** (F125, attesa scritta prima): −119 / −178 N·m danno −9 / −26% di VMG; candidato −3/−5% e −5/−8%, oggi 0/−4% e 0/−6%. **Non passa, per nessuna delle due.**

### Ipotesi senza fonte (otto)

`a0` 2 e `w` 8 (rampa della vela che fileggia; B6 tiene con `a0` da 2 a circa 3, non con 4); il 9° che sposta la tabella (F109 tab. 4.1: 13-19° al 62% della vela, compatibile); il passaggio 40-60° di vento apparente; il ritardo 0,9 s; la raddrizzata oltre 22,5°; l'altezza del timoniere `dz` 0; gli angoli 100-140° fra cui la deriva «si alza»; la resistenza della vela che sbatte (0,08, tenuta uguale al totale di oggi). **Ordine dei fatti, da dire:** area, 0,08, `reg` e svergolamento extra sono stati messi dopo aver visto numeri che non passavano, sempre perché una fonte o un controllo lo indicava.

### Cosa non convince e cosa va rimisurato

- **Lezione 6.3 «La scuffia»:** il pilota la completa 13 volte su 26 (oggi 29 su 29): la barca resiste di più, serve più vento. **6.2 raffica** 29 su 30 ma 20 s invece di 7; **1.8 angolo morto** 14 s invece di 9, **2.6** e **5.8** 28 su 30. Su 41 passi pratici, 30 semi, tutti gli altri come oggi.
- **Rivali** (96 regate, versione I: 32 + 32 corte e 12 lunghe in Chromium, 20 corte in Firefox; semi 5301-5308, 5501-5508, 5301-5304 lunghi, 5401-5405; rivali non ritarati): 0 errori, arrivi 0,6-3,6% più veloci, contatti 99 → **124** (+25%), fuori linea al via 26 → **46**, non arrivati 130 → 125. Il margine di partenza +2 s sembrava curarli (semi 5301-5308: contatti 37 → 29, fuori 19 → 15) ma **la conferma su semi mai usati (5501-5508) no**: contatti 34 oggi, 43 senza margine, 37 con +2 s; fuori linea 11, 12, 14. Quindi il rumore è grande e servono più regate prima di dire altro. Regate lunghe, 0 scuffie su 334 virate, virate bloccate 5 (oggi 4 su 336); rivali sbandati oltre 12° il 4,2% del tempo (oggi 11,6%).
- **Angolo morto:** con 6 nodi, a 20° 0,37 nodi, a 25° 0,97, a 30° 2,31 (oggi −0,96 / −0,31 / 0,70): più stretto di oggi, più largo della prima versione. Nessuna fonte lo misura.
- Partenza da ferma più lenta col vento (2 nodi a 60°: 10 nodi 4,8 s contro 2,9; 6 nodi 8,5 contro 7,0).
- `orziera1b`: criterio 2 fuori a 14 nodi e 90° (1,29 contro 1 °/s) e criterio 4 perché la raffica a scotta ferma non sovrasta più (barra massima 6°, soglia oltre 20°).
- F109 a regime: +3% con 3,2 nodi e +7% con 11 (2,53 contro 2,37 m/s).
- Conferma su Binns e F109 non cieca. Motore: 432 casi × 6 passi, 0 non finiti, stesso risultato con ogni passo. `collaudo_stare_fermi` e `collaudo_esercizi_regata` verdi sulla copia in Firefox; `collaudo_torneo` e `collaudo_regola18` **non misurati** sulla copia (il primo è stato fermato, l'altro chiede git). Le medaglie e le fasce non sono provate.

### Dove sono i file

`sperimentale/barca-84/`: `INTERVALLI.md`, `banco84.js`, `candidato.json` (versione I), `esito_candidato.txt`, `motore84.js` (da `fa_motore84.py`), `montecarlo84.js` e i due esiti, `virata_f109.js`, `bethwaite.js`, `marshall.js`, `scomponi84.js`, `traccia16.js`. Fonti F124-F127. Pagine che rifiutano la lettura: Southampton, MDPI, core.ac.uk, Tasmania, Chalmers ODR.

### Consiglio

Fare la proposta per il motore con la versione I, **se Ale accetta due cose scritte**: B2 a 60° (−5,2; la stessa fonte fa −6,4) e le otto ipotesi. Ordine: prima le lezioni 6.2-6.3 e il vento dell'angolo morto, poi la partenza dei rivali e i contatti, poi tempi, medaglie e record (azzerabili). Se Ale non accetta, la 81 torna limite noto.
