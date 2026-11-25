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

## Esito della sessione (25-26 novembre 2026, `js/` non toccato)

Tre giri di lavoro: il primo chiuso troppo presto (20 minuti), il secondo (versione I), il terzo dopo Flay e Taylor scaricati da Ale (versione **J**, questa). **Le fonti nuove hanno ridimensionato la versione I:** l'area 7,92 era una scelta spinta e la sua «conferma doppia» non era indipendente. J usa i **valori centrali degli intervalli delle fonti**, fissati senza guardare i criteri: area 7,5 m², braccio velico 2,8 m, braccio del timoniere 0,90 m. **Non passa tutto: B2 e B8.** Decide Ale.

| Criterio | Soglia | Oggi | J | |
|---|---|---|---|---|
| B1 Day 6 nodi (VMG) | ±5% | −15,7% | −3,6% | passa |
| B2 Binns 9 nodi, 42 / 46,5 / 55 / 60° | ±5% | −15 −12 −13 −14 | −1,1 −2,5 **−5,7 −7,3** | **no** (Day stesso: circa −1 / −4 / −6) |
| B3 Binns 12 nodi | ±3% | −2,3 … −0,1 | −0,6 … +0,6 | passa |
| B4 Day 15 nodi | ≤ +7% | +6,5% | +0,6% | passa |
| B5 3,2 nodi a 45° (1,05 m/s) | −8% | −15% | +1,2% | passa |
| B6 virata 3,2 nodi | −1,22 m | −1,74 | −1,06 m (F109 −0,67) | passa |
| B7b poppa contro Day 6/10/15 | ±4% | −10 −8 −9 | −3 −2 −2 | passa |
| B8 ogni costante con fonte | sì | — | otto ipotesi | **no** |
| Virata 16 nodi con la freccia | 5 s | 2,9 s | 2,3 s (18 nodi 2,4; 20 nodi 2,9) | passa |
| Raffica 10→18 senza reagire | < 60° | 52° | 40° | passa |
| Fermi a 0-15°, 30 s | < 0,3 nodi | sotto zero | sotto zero | passa |

La regola scritta prima della scansione («il minimo d'errore su Day e F121») sceglie invece **7,06 / 2,8 / 0,87**: lì B1 è −5,6% e B2 −9,1%, quindi **la regola, applicata alla lettera, dà un candidato che non passa B1**. Le differenze d'errore fra 7,06 e 7,5 sono piccolissime (2,63 contro 2,92 punti, dentro la precisione della lettura dei grafici): J non è peggiore per la taratura, è al centro degli intervalli. Scansione: `scansione84.txt`.

### Il controllo che non dipende dalla taratura (`spinta_richiesta.js`)

Per ogni velocità misurata: spinta che serve (vasca + appendici + indotta, quote di Day fig. 11) divisa per la pressione del vento apparente, contro la spinta delle vele.

| Caso (m² di spinta) | serve | oggi | candidato 7,92 | 7,06 | Flay |
|---|---|---|---|---|---|
| Day 6 nodi | 3,06 | 1,10 | 3,15 | 2,81 | 2,00 |
| F109 3,2 nodi | 2,95 | 1,40 | 3,24 | 2,89 | 2,08 |
| Binns 9 a 46,5° | 3,80 | 2,67 | 3,71 | 3,31 | 2,58 |
| Binns 9 a 60° | 5,69 | 3,74 | 4,86 | 4,33 | 3,57 |
| Bethwaite 6 nodi | 3,64 | 1,12 | 3,16 | 2,82 | 2,00 |
| GPS olimpici ~6 nodi | 3,11 | 1,88 | 3,36 | 2,99 | 2,20 |

**La vela di oggi è debole da 2 a 3 volte col poco vento, per cinque fonti diverse.** La galleria di Flay (modello 1/6, vela che si svergola, lo scrive lui) dà meno spinta di qualunque barca in acqua: non è usabile come numero assoluto. L'area giusta sta fra 7,0 e 7,9: Binns e Bethwaite chiedono di più, F109 e GPS di meno.

### Altri controlli nuovi (Flay, Taylor)

- **Flay fig. 27:** forza laterale al 35-39% dell'albero dal fondo dello scafo, cioè braccio 2,4-2,6 m (F121: 3,0). Con un braccio più corto serve meno coppia al timoniere: le due cose si compensano (2,8 con 0,87 ≈ 3,0 con 0,956).
- **Flay fig. 23-24, 60°:** spinta e forza laterale col boma a 35°: le curve di oggi per le andature larghe danno la stessa spinta entro il 3% (7,0 contro 6,8 m²). Il passaggio 40-60° alla curva vecchia ha quindi un sostegno.
- **Taylor tab. 6.1:** coppia massima statica 653-737 N·m per velisti di 77-80 kg (braccio 0,87-0,93). Tab. 1.1: barca armata 80 kg.
- **Taylor fig. 9.7 (velista di club in acqua):** coppia del timoniere contro vento apparente: a 4,5 m/s circa 450-500 N·m (oggi 186, J 313), a 5-5,2 m/s oltre 680 (oggi 247, J 427). J più vicino, ancora sotto. Velocità del velista: fra le due barche (oggi +3/+9%, J +6/+15%: velista non di vertice).

### Quanto dipende dalle ipotesi (Monte Carlo, 200 combinazioni, intervalli larghi: area 7,06-7,92, braccio 2,4-3,1, timoniere 0,87-0,956)

B1 73%, B2 1% (23% senza i 60°), B3 53%, B4 92%, B5 100%, B6 84%, B7b 75%, virata 16 nodi 100%, raffica 100%, virata 18 nodi 93%, angolo morto 100%; tutti tranne B2 20%. **Con intervalli onesti la barca nuova non è «sicura» sui criteri stretti**; è però molto più vicina alle fonti della barca di oggi in quasi tutti i punti.

### Virata (F109 secondo per secondo, prua e scotta come nel vero)

Scarto medio delle velocità 0,046 (3,2 nodi) e 0,066 (11 nodi); oggi 0,139 e 0,138. Velocità a regime 3,2 nodi 1,06 m/s (misurato 1,06). Metri persi −1,80 e −3,45 (F109 −0,67 e −4,39; oggi −2,71 e −6,44). Col pilota e la scotta ferma la virata resta facile (circa 1-1,5 m a 10-14 nodi) e `virata1b` criterio 1 è fuori a tutti i venti.

### Sul gioco (clone del repo con il motore J)

- **Lezioni** (30 semi, 41 passi pratici): **6.3 «La scuffia» 9 su 29** (oggi 29 su 29): la barca resiste di più alle raffiche, la lezione va ritarata; 1.8 angolo morto 15 s (oggi 9), 6.2 raffica 15 s (oggi 7); 2.6 e 5.8 28 su 30. Gli altri passi come oggi.
- **Fasce delle prove:** tempi del pilota −0,5 / −4 / −13 / −13 / −6% (prove 1-5); nella prova 4 spariscono i momenti col pilota fermo nel vento. **Medaglie** (10 corse invece di 30, quindi il controllo fallisce per numero): stesse proporzioni di oggi, nella prova 5 il pilota preciso prende 10 ori su 10 invece di 7. Fasce da rifare.
- **Rivali** (96 regate più le 90 della regola 18, Chromium e Firefox, rivali non ritarati): 0 errori, arrivi 2-4% più veloci, contatti 189 → 216 (+14%), fuori linea al via 26 → 40, non arrivati 130 → 125. Il margine della partenza non li cura (provato, confermato su semi nuovi). `collaudo_regola18`: Z1 fallisce per forza (barca diversa), **Z4 fallisce: 0 contatti decisi dalla 18 in 90 regate** (oggi 2), troppo pochi casi per dire.
- Regate lunghe: 0 scuffie dei rivali; motore: 432 casi × 6 passi, 0 non finiti.
- `collaudo_torneo` (clone, J): C1 16 casi su 16, C2 160 regate concluse su 160 con 0 differenze, C3 30 su 30, C4 10 su 10; C11 solo l'uscita lenta R7 già nota sul PC; **fermato dal mio limite di 40 minuti a metà di C11, il resto non è misurato.**
- Mediana dei rapporti «spinta che serve / spinta con 7,92» su tutti i casi in acqua: area circa 7,8. Comprende Binns (dato di conferma): non usata per scegliere.

### Ipotesi senza fonte (otto)

`a0` 2 e `w` 8; il 9° che sposta la tabella; il passaggio 40-60° (ora sostenuto da Flay a 60°); il ritardo 0,9 s; la raddrizzata oltre 22,5°; `dz` 0; la deriva che «si alza» fra 100° e 140°; la vela che sbatte 0,08. Area, braccio e timoniere hanno fonte e intervallo, e J ne prende il centro.

### Correzioni di quanto detto ad Ale in questa sessione

1. «Virata troppo facile» (primo giro): era il metodo; col gesto vero la barca nuova è più vicina.
2. «Area confermata due volte» (secondo giro): falso, la vela di Flay è 5,91 m²; l'area ha una fonte sola.
3. «Robustezza 99%» (secondo giro): con intervalli onesti è molto più bassa (sopra).

### Consiglio

**Non adottare un candidato preciso adesso.** Il risultato solido è che la vela di oggi è troppo debole col poco vento (cinque fonti) e che la barca deve pesare 160 kg e raddrizzare come F121; l'area esatta (7,0-7,9) e le ipotesi della vela che fileggia non sono decise dalle fonti. Se Ale vuole andare avanti: proposta per il motore con J, B2 e B8 dichiarati non passati, e prima di accenderla lezione 6.3, fasce, medaglie, partenza dei rivali. Se no: la 81 resta limite noto, con questa ricerca scritta.
