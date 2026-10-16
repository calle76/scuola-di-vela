# Proposta: velocità della barca (resistenza dello scafo)

**Seconda stesura, 16 ottobre 2026. Proposta, fermata 1: il motore non è stato toccato.** La prima stesura (stesso giorno, nella storia di git) è stata rivista dalla chat del progetto, che ha trovato un errore di lettura della fonte (§1). Questa stesura lo corregge e cambia il modello: una **tabella** al posto dei tre numeri. Le misure sono state fatte con una copia del motore modificata solo in memoria, con script fuori dal repository.

Tipi delle affermazioni:
- **[fonte]** = letto in una fonte, con dove;
- **[misura]** = fatto girare il motore;
- **[stima]** = ragionamento senza misura;
- **[giudizio]** = opinione, da decidere.

**Scelta di partenza (Ale, 16 ottobre 2026):** si tara la barca **condotta bene**; la differenza la fa chi conduce.

---

## 0. In breve

- **Il motore frena troppo:** fra 2 e 9 nodi, da **1,45 a 2,5 volte** lo scafo misurato in vasca più l'attrito di deriva e timone. Oltre i 7 nodi la differenza cresce, perché la formula di oggi ha un termine che fa da «muro».
- **La formula di oggi non può seguire la vasca:**
  - con tre numeri tarati fino a 7 nodi, a 8-9 nodi sbaglia del 37-67%;
  - tarati fino a 9 nodi, sbaglia fino al 19%.
- **Proposta:** la resistenza dello scafo diventa una **tabella** con i valori misurati in vasca, letti fra un punto e l'altro, più un termine costante per l'attrito di deriva e timone. Riproduce la vasca per costruzione. `hullK1`, `hullK2` e `hullK4` spariscono.
- **Effetto con 10 nodi di vento:**
  - bolina da 3,4 a 3,8 nodi;
  - traverso da 5,2 a 6,0;
  - poppa da 3,5 a 4,1;
  - virata da 4,0 a 3,3 s;
  - la virata da 1,9 nodi, oggi fallita, riesce;
  - raffiche uguali (+1°).
- **Prova indipendente** (velocità utile verso il vento e sottovento, contro le previsioni di Day, che usano la stessa vasca ma una vela diversa dalla nostra):
  - **sottovento lo scafo è giusto:** il gioco sta dall'8 al 10% sotto Day, con ogni vento;
  - **di bolina no:** −22% con 6 nodi, +5% con 15. Questo indica due difetti che non riguardano lo scafo (§4) e restano compiti separati.
- **Versione 1.0.6.** I record delle prove e delle regate si azzerano (§7).

---

## 1. L'errore della prima stesura

**[fonte, Day 2017, §3.4]** Il «20%» di Day **non** è «deriva e timone». È la quota della resistenza totale data dai termini del modello di Delft più l'effetto del timone, e vale:
- **solo di bolina**, con 10 nodi e un timoniere da 80 kg;
- per il 14% è **resistenza indotta**, cioè dovuta alla spinta laterale;
- in poppa scende **sotto l'1%**;
- l'attrito di deriva e timone non c'è dentro: Day lo calcola a parte.

La prima stesura lo aggiungeva come +20% a tutte le velocità e andature. **Correzione:** nel bersaglio della resistenza entrano solo le parti che dipendono dalla velocità: lo scafo dritto (vasca) più l'attrito di deriva e timone. La resistenza indotta dipende dalla spinta laterale, non dalla velocità, e oggi nel motore **non c'è**: è un compito a parte (§5, rischio 1).

---

## 2. Fonti

**F-A, vasca.** A. H. Day, E. Nixon, «Measurement and prediction of the resistance of a Laser sailing dinghy», *Trans. RINA Part B, Int. J. Small Craft Technology* 156(B1), 2014, pp. 11-20, <https://strathprints.strath.ac.uk/46407/>. La pagina non indica una licenza.
- **[fonte]** Scafo Laser vero, dritto, senza deriva né timone, da 2 a 9 nodi. Risultati riportati ad **acqua dolce a 15 °C**: convertirli in acqua di mare moltiplicando per la densità non conta il sale due volte.

**F-B, previsione delle prestazioni.** A. H. Day, «Performance prediction for sailing dinghies», *Ocean Engineering* 136, 2017, pp. 67-79, <https://strathprints.strath.ac.uk/59980/>, manoscritto dell'autore sotto licenza **CC BY-NC-ND 4.0** (letta sulla pagina il 16 ottobre).
- **[fonte] Figura 2:** la stessa curva della vasca di F-A (timoniere da 80 kg, circa 160 kg in tutto), più leggibile. Letta a occhio, incertezza circa ±0,0003 m²:

| Nodi | 2 | 2,5 | 3 | 3,5 | 4 | 4,5 | 5 | 5,5 | 6 | 6,5 | 7 | 7,5 | 8 | 8,5 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Area di resistenza (m²) | 0,0125 | 0,0126 | 0,0132 | 0,0144 | 0,0157 | 0,0178 | 0,0207 | 0,0229 | 0,0241 | 0,0246 | 0,0243 | 0,0233 | 0,0221 | 0,0212 | 0,0206 |

  L'«area di resistenza» è la resistenza divisa per ½ ρ v².
- **[fonte] Figura 11:** ripartizione della resistenza per componente, a 5, 10 e 15 nodi di vento, di bolina e in poppa. Di bolina (deriva tutta giù, come nel gioco), l'attrito di deriva e timone più la piccola resistenza d'onda della deriva, rapportati allo scafo, danno un'area quasi costante: **circa 0,0049 m²** (0,0048 · 0,0052 · 0,0048), letta a occhio con un'incertezza di circa ±0,0005. In poppa Day alza la deriva a metà, quindi quei valori non servono.
- **[fonte] Figura 8:** velocità utile (VMG) prevista di bolina e di poppa, da 5 a 16 nodi di vento. È usata come prova (§4), non per tarare.
- **[fonte] Figura 4:** misure in mare di Binns e colleghi (2002) con 9 nodi: 42° → circa 4,65 nodi; 46,5° → 5,0; 55° → 5,6; 60° → 5,9. Fra gli autori c'è Bethwaite, quindi la «polare di Bethwaite» di `RICERCA-VELOCITA-VIRATA-RIPARTENZA.md` non è una conferma indipendente.
- **[fonte] §6.1:** Day sospetta un errore di scala nei dati di Clark (2014) e li **scarta**. Non li uso.
- **[fonte] §6.2:** di bolina il Laser naviga con vento apparente fra circa 27° (5 nodi di vento) e 33° (15 nodi).

**Uso dei dati [giudizio, da confermare].** La tabella contiene numeri letti da un grafico e scritti nel codice, con la fonte nel commento. Sono misure, non testo né figure dell'autore: la licenza NC è compatibile con un progetto non commerciale, e ND riguarda la ridistribuzione dell'opera, che non facciamo. Il principio 5 («non si copiano tabelle delle fonti») va letto come «non si copiano testi e tabelle redatte», non come «non si usano i numeri misurati»: lo segnalo perché decida Ale.

---

## 3. Il modello proposto

**Oggi** [codice, `js/motore.js`]: resistenza = `hullK1`·u + `hullK2`·u² + `hullK4`·u⁴ (4, 12, 0,9), più il freno del timone girato e lo sbandamento.

**Proposta:** resistenza dello scafo = (area dalla tabella × `hullScale` + `appDA`) × ½ × 1025 × u·|u|.
- **Tabella:** le 15 coppie del §2, lette per interpolazione lineare.
  - **Sotto i 2 nodi** l'area resta quella di 2 nodi: non ci sono dati; con l'acqua che scorre piano conta l'attrito, che segue circa v² [stima].
  - **Sopra i 9 nodi** resta quella di 9: non ci sono dati; nella vasca l'area stava ancora calando, quindi è un'ipotesi prudente [stima].
- **`appDA` = 0,0049 m²:** attrito di deriva e timone (F-B, figura 11).
- **`hullScale` = 1:** non è una taratura; serve al laboratorio per provare uno scafo più o meno frenato. In laboratorio sostituisce i cursori di `hullK1`, `hullK2`, `hullK4`, che spariscono.
- **Densità dell'acqua di mare** 1025 kg/m³.
- **Restano come sono:** il freno del timone girato (`rudderDragK`), lo sbandamento che frena (`heelDrag`), il tetto all'indietro (`backMax`).
- **Codice [stima]:** circa 8 righe in `motore.js`, una in `laboratorio.js`, e il cambio del criterio 4 di `collaudo_laboratorio.py` (oggi usa `hullK2`).

**Resistenza [misura]:**

| Nodi | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|
| Bersaglio = proposta (N) | 9 | 22 | 45 | 87 | 141 | 194 | 234 | 280 |
| Motore oggi ÷ bersaglio | 1,89 | 1,80 | 1,68 | 1,49 | 1,47 | 1,65 | 2,04 | 2,46 |

**Peso [fonte + stima].** La curva è per 160 kg in tutto; la barca del gioco pesa 135 kg (fuori dai 150-170 kg provati in vasca). La curva da 70 kg (150 kg in tutto, F-A figura 4) frena dal 2 al 5% meno di quella da 80. Usare quella da 80 vuol dire una barca a regime **un poco più lenta**, cioè prudente. Ma l'inerzia resta quella di 135 kg, quindi accelerazioni, virate e frenate sono un po' **ottimistiche**. Non si corregge qui: si dichiara.

---

## 4. Cosa cambia [misura]

Velocità con la scotta migliore, nodi (oggi → proposta):

| Vento | 45° | 60° | 90° | 120° | 135° | 150° | 180° |
|---|---|---|---|---|---|---|---|
| 6 nodi | 2,0 → 2,3 | 2,9 → 3,8 | 3,3 → 4,2 | 3,0 → 3,8 | 2,6 → 3,4 | 2,3 → 2,8 | 2,2 → 2,6 |
| 10 nodi | 3,4 → 3,8 | 4,6 → 5,4 | 5,2 → 6,0 | 4,7 → 5,4 | 4,2 → 5,0 | 3,8 → 4,4 | 3,5 → 4,1 |
| 15 nodi | 5,0 → 5,4 | 5,9 → 7,0 | 6,9 → **9,5** | 6,5 → 8,3 | 5,8 → 6,9 | 5,4 → 6,1 | 4,8 → 5,4 |

Il 9,5 al traverso con 15 nodi sta oltre la fine della tabella (9 nodi): la barca sta planando, e lì la resistenza è un'ipotesi (§3).

Con 10 nodi:

| Misura | Oggi | Proposta |
|---|---|---|
| Virata da 3,9 nodi, barra 0,8 | 4,0 s | 3,3 s |
| Virata da 1,9 nodi | fallita | riuscita in 7,6 s |
| Raffica da 10 a 16 / 18 / 20 nodi senza reagire | 27° / 41° / 55° | 28° / 42° / 55° |
| Frenata con la prua nel vento, dalla bolina | 0,7 lunghezze in 4,2 s | 1,0 lunghezze in 5,0 s |
| Angolo morto da fermi, scotta a metà | indietro dopo 1,7 s, fino a 1,8 nodi | indietro dopo 1,7 s, fino a **2,3 nodi** |

**Prova indipendente: VMG contro Day 2017, figura 8** (letta a occhio). Questi numeri non sono stati usati per scegliere niente. Formato: oggi → proposta, contro Day.

| Vento | VMG di bolina | VMG di poppa |
|---|---|---|
| 6 nodi | 1,64 → **2,07** contro 2,65 (−22%) | 2,21 → **2,66** contro 2,95 (−10%) |
| 10 nodi | 2,70 → **3,09** contro 3,6 (−14%) | 3,63 → **4,18** contro 4,55 (−8%) |
| 15 nodi | 3,56 → **3,99** contro 3,8 (**+5%**) | 5,16 → **5,72** contro 6,3 (−9%) |

**Cosa si vede [stima]:**
- **Sottovento lo scarto è quasi costante** (dall'8 al 10%): lo scafo nuovo è giusto. Il resto può venire dalla vela in poppa, o dalle tecniche dei velisti che il gioco non ha (il pompaggio, il surf sulle onde).
- **Di bolina lo scarto cambia col vento**, da −22% a +5%. Non è lo scafo, che è lo stesso in tutte e due le andature. Due cause probabili, già indicate dalla chat:
  1. **con poco vento la vela del gioco non stringe abbastanza:** porta del tutto solo sopra i 34° di vento apparente (`luffA0` + `luffW`), mentre Day dà per il Laser 27-33°;
  2. **con molto vento manca la resistenza indotta** (il 14% della resistenza di bolina con 10 nodi, secondo Day, e cresce col vento): la barca va un po' troppo forte.

  Sono due compiti separati, uno per volta.
- Rispetto alla misura GPS di bolina con 15 nodi (5,4 nodi), la proposta dà **5,4**: non è più sopra.

---

## 5. Rischi

1. **Manca la resistenza indotta** [codice]: in `step()` la spinta laterale produce solo scarroccio, mai freno. Oggi non si vedeva perché la barca era frenata da altro. Con lo scafo giusto, di bolina con vento forte la barca va il 5% oltre Day, e andrà ancora più forte quando si correggerà la vela di bolina. È il compito successivo naturale.
2. **Compensazioni nascoste:** valori tarati con lo scafo vecchio (vela, `luffA0`/`luffW`, `foilK`) possono aver assorbito l'eccesso di freno. Correggere lo scafo fa emergere altri errori, che vanno corretti uno per volta con la stessa regola.
3. **Oltre i 9 nodi** la resistenza è un'ipotesi; la barca ci arriva al traverso con 15 nodi e nelle raffiche.
4. **Peso:** resistenza da una barca di 160 kg, inerzia da una di 135 (§3).
5. **La rotazione cresce con la velocità** (la virata dipende da u / `turnLen`): a 8-9 nodi lo sterzo diventa più nervoso, anche per gli avversari e per il pilota dei collaudi.
6. **La retromarcia diventa più forte** (fino a 2,3 nodi contro 1,8): arriva al tetto `backMax`. È il compito «retromarcia», da provare in laboratorio.
7. **La virata migliora senza toccare il timone:** il compito «timone e virata» va fatto sulla barca nuova, con i video.
8. **Tutto ciò che è tarato sulla velocità:**
   - fasce delle prove;
   - avversari («sotto 0,6 m/s poggia»);
   - soglie delle lezioni (3,3 nodi per prepararsi a virare, più di 4 nodi in «Accelerando», 1 nodo per la virata che non riesce);
   - **testi di lezioni e manuale che citano velocità in nodi** (`CONTENUTI-DA-VERIFICARE.md`).
9. **Record:** un tempo fatto con la barca vecchia non è confrontabile (§7).
10. **Il prototipo del fiocco** ha una copia sua del motore e resterebbe con la resistenza vecchia: va dichiarato in `SPERIMENTALE.md` e allineato quando si riprende il fiocco.
11. **Sotto i 2 nodi non ci sono dati:** abbrivio, virata lenta e frenata cambiano dove non ci sono misure.

---

## 6. Criteri della fermata 2

**Controlli di esecuzione** (i numeri sono già stati visti: verificano che il motore cambiato sia quello misurato qui, non che sia giusto):
1. resistenza del motore uguale alla tabella più `appDA`, entro l'1%, a 2, 3, … 9 nodi;
2. `polare.js` a 6, 10 e 15 nodi uguale alla tabella del §4, al decimo;
3. VMG uguale alla tabella del §4, al centesimo.

**Rapporti** (si riportano, senza una soglia che li faccia passare o fallire):
4. VMG contro Day, come nel §4;
5. polare contro le misure in mare (Binns con 9 nodi; tracce GPS di Caraballo con 6 nodi, che sono **medie** di regata e non punte);
6. sensibilità al peso: con la curva da 70 kg al posto di quella da 80, quanto cambiano VMG e polare.

**Prove del gioco** (soglie dichiarate adesso):
7. **nessun conto in errore,** con i passi di tempo di 1/240 e 0,0125 s, e i cursori del laboratorio agli estremi (`hullScale` da 0,5 a 2,5; `appDA` da 0 a 0,01);
8. **regate:** `collaudo_regate.py` (bastone e raffiche, semi 1-6) con nessun avversario BLOCCATO; `collaudo_partenze.py` OK;
9. **prove:** `collaudo_fasce.py` dà i tempi nuovi, e le fasce si ritarano con la regola già scritta in `contenuti.js` (oro = pilota arrotondato ai 5 s superiori, argento +25%, bronzo +60%);
10. **lezioni:** pilota delle lezioni sui semi 1-20, poi conferma sui semi 21-100 mai guardati (regola dei semi). Rapporto sui sei passi da correggere: quali migliorano, quali peggiorano, quali nascono nuovi;
11. **pagina:** nessun errore con `#collaudo`, senza, e con `#lab`; pannello a 1360×650 senza eccesso; collaudi della 1.0.4 e 1.0.5 tutti OK.

**Prova guidando davvero (Ale, col laboratorio e senza):** in navigazione libera con 10 nodi, guardare
- l'abbrivio: quanto va avanti la barca con la prua messa nel vento;
- una virata lenta, partendo piano;
- l'angolo morto: quanto in fretta va all'indietro;
- un lasco con 15 nodi: se la barca sembra «scappare».

Si riporta l'impressione, non un voto: il giudizio nautico lo danno le fonti, ma un comportamento strano va segnalato.

---

## 7. Decisioni

- **Record [deciso, 16 ottobre]:** si azzerano cambiando le chiavi `KEYV`, come proposto in prima stesura e confermato dalla chat. La chat suggeriva di tenere i meriti di carriera già guadagnati, ma [codice] i meriti **non sono salvati a parte**: `meriti()` li ricalcola ogni volta dai record. Separarli vorrebbe dire una novità nel salvataggio; non la propongo.
- **Il +2% della prima stesura** non c'è più: con la tabella la bolina con 15 nodi dà 5,4 nodi, uguale alla misura GPS. Lo sbilanciamento di bolina con vento forte (+5% su Day) resta come **problema noto**, legato alla resistenza indotta (§5, rischio 1).
- **Per Ale:**
  1. il via alla fermata 2;
  2. la lettura del principio 5 sui numeri misurati (§2, ultimo paragrafo).
