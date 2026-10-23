# Proposta: prima la resistenza dello scafo, poi il timone

**Superata il 16 ottobre 2026 da `PROPOSTA-VELOCITA.md`** (resistenza da tabella della vasca, versione 1.0.6). Il «circa il doppio» qui sotto, ricontrollato, è da 1,45 a 2,5 volte; il «+20% per deriva e timone» del §2 era una lettura sbagliata di Day 2017 (vedi `PROPOSTA-VELOCITA.md` §1).

Del 13 ottobre 2026. **Proposta, fermata 1: nessun codice.** Nasce dalla prova della saturazione del timone (`archivio/PROPOSTA-SATURAZIONE-TIMONE.md`, `archivio/RAPPORTO-PROVA-SATURAZIONE.md`) e dalla prima ricerca web sulle fonti.

Tipi delle affermazioni:
- **[codice]** = letto nel codice, con file e riga;
- **[misura]** = verificato facendo girare il motore o letto da una misura pubblicata;
- **[stima]** = ragionamento senza misura;
- **[giudizio]** = opinione, da decidere.

**Premessa (13 ottobre 2026).** Non ci sarà una persona esperta a giudicare il simulatore. La credibilità viene solo da fonti scritte e da video che chiunque può ricontrollare. Una fonte sola = scelta di progetto dichiarata; due o più fonti concordi = «verificato su fonti».

---

## 0. In breve

1. **Il gioco resta con la barca della 0.21.2.** La saturazione del timone resta sul ramo `prova-saturazione` e non entra in una versione per ora.
2. **Il prossimo compito di fisica è la resistenza dello scafo**, perché è l'unico punto in cui abbiamo una misura vera sulla barca più simile alla nostra: secondo quella misura il motore frena circa il doppio.
3. **Il timone si riguarda dopo**, con misure prese dai video: durata delle virate e angolo della barra.

---

## 1. Perché non la barca «nervosa» [giudizio, con i numeri]

La saturazione compensata (`rudderSat` 15, a barra tutta la rotazione di oggi) rende la barca quasi due volte più sensibile sotto 15° di barra. Nessuna fonte lo sostiene: è un effetto collaterale della compensazione.

| | 0.21.2 | Saturazione 15° | Saturazione 24° |
|---|---|---|---|
| Rotazione con poca barra, rispetto a oggi | 1× | 1,93× | 1,23× |
| Cambi di barra nell'esercizio della rotta, mediana [misura, emulazione] | 2 | 12 | 4 |
| Collaudo della lezione 5, colpo di freccia da 0,7 s [misura] | OK | ✘ | OK |
| Virata col pilota a 10 nodi [misura] | 4,41 s | 3,60 s | 4,03 s |
| Quanto costa la barra a fondo rispetto alla barra migliore, 10 nodi [misura] | la barra a fondo è la migliore | +0,44 s | piccolo |

- **[giudizio]** Il guadagno didattico («barra a fondo è un errore») è piccolo per quello che costa.
- **[misura, fonte]** I tempi di virata non aiutano a scegliere. L'unico dato scritto trovato è «uno o due secondi con la prua nel vento» (Jon Emmett, ILCA), compatibile con entrambe le barche.
- **Se un giorno si vuole la saturazione,** il 24° è il compromesso più prudente: più vicino alla barca di oggi, lezione 5 a posto, barra a fondo non più la migliore (a 10 nodi vince la barra a 0,8 nella griglia di 84 virate).

---

## 2. Cosa dicono le fonti sulla resistenza [misura]

### F-nuova A: Day e Nixon (2014), Laser in vasca

A. H. Day, E. Nixon, «Measurement and prediction of the resistance of a Laser sailing dinghy», *Transactions RINA Part B, International Journal of Small Craft Technology* 156(B1), 2014, pp. 11-20, DOI 10.3940/rina.ijsct.2014.bl.151.
- Testo dell'autore accettato per la pubblicazione, libero sul sito dell'Università di Strathclyde: <https://strathprints.strath.ac.uk/46407/>.
- Il sito non dichiara una licenza: si usano solo i numeri, citando la fonte, senza copiare figure né testo.

**Come è stata fatta la prova:**
- scafo Laser vero (4,2 m, la lunghezza della barca del gioco), dritto, **senza deriva né timone**;
- risultati riportati ad acqua dolce a 15 °C;
- dislocamento 150, 160 e 170 kg: scafo con armo circa 80 kg, più timoniere 70, 80 o 90 kg.

**Confronto con il motore** [misura]. Curva «80 kg» della figura 4 (area di resistenza), letta a occhio dall'immagine della pagina, incertezza di lettura circa ±0,0003 m². Motore: scafo dritto, barra al centro, formula alla riga 421 di `index.html` (`4·u + hullK2·u² + hullK4·u⁴`, con `hullK2` 12 e `hullK4` 0,9).

| Nodi | Laser in vasca, solo scafo | Motore | Motore ÷ vasca |
|---|---|---|---|
| 2 | 6,8 N (0,7 kgf) | 17,8 N | 2,6 |
| 3 | 16,1 N | 39,9 N | 2,5 |
| 4 | 33,6 N (3,4 kgf) | 75,2 N (7,7 kgf) | 2,2 |
| 5 | 69,9 N | 129,1 N | 1,8 |
| 6 | 117 N (11,9 kgf) | 208 N (21,2 kgf) | 1,8 |

Avvertenze:
- **[stima]** Nella vasca mancano deriva e timone. Secondo Day (2017, sotto) contano per circa il 20% della resistenza dell'acqua. Anche aggiungendoli, il motore resterebbe **circa 1,5-2 volte** più frenato.
- Ho usato la densità dell'acqua di mare; con l'acqua dolce della prova le cifre della vasca calano del 2,5% circa, quindi il rapporto cresce un poco.
- **La barca del gioco non è un Laser:** è una «deriva da scuola» di 135 kg con scafo non specificato. Il Laser è la barca documentata più simile, non la stessa.
- **[stima]** Lo scarto più grande è sotto i 3 nodi (rapporto 2,5-2,6), proprio dove si gioca l'abbrivio in virata.

### F-nuova B: Day (2017), previsione delle prestazioni del Laser

A. H. Day, «Performance prediction for sailing dinghies», *Ocean Engineering* 136, 2017, pp. 67-79. Testo dell'autore libero su <https://strathprints.strath.ac.uk/59980/>.

**Velocità misurate**, figura 4: misure di Binns e colleghi (2002), vento 9 nodi, timoniere da 80 kg, lette a occhio [misura]:

| Angolo dal vento reale | Laser misurato |
|---|---|
| 42° | circa 4,6 nodi |
| 46° | circa 5,0 nodi |
| 55° | circa 5,6 nodi |
| 60° | circa 5,9 nodi |

- **Il motore con 10 nodi** (`polare.js`): 3,4 nodi a 45°, 4,6 nodi a 60°. Circa il 25-30% più lento, con un nodo di vento in più.
- **Limite:** nella figura 3 lo stesso Day mostra un'altra serie misurata sul Laser (Clark 2014, 12,5 nodi) molto più lenta, e scrive di una «discrepanza molto sostanziale» fra le due serie. Le misure vere danno quindi una **fascia**, non un numero da tarare.
- Day riporta anche che deriva, timone e la resistenza legata al timone valgono circa il 20% della resistenza dell'acqua (riga 1099 del testo estratto).

---

## 3. Cosa ne ricavo [stima]

- La resistenza circa doppia spiega insieme quattro cose viste nel gioco:
  - la barca si ferma in 1-1,6 lunghezze con la prua nel vento, contro le 3-4 citate da Cockerill (citazione non ancora rintracciata);
  - la virata a 1,9 nodi fallisce;
  - la virata col timone «sembra» debole;
  - la polare è lenta di bolina.
- La saturazione compensata, in parte, **curava il sintomo**: la barca perde velocità in virata perché frena troppo, non perché il timone giri poco.
- Correggere la resistenza cambia **tutto il gioco**: polare, fasce delle prove, regate, avversari, lezioni, sbandamento in raffica (più velocità vuol dire più vento apparente). È una ritaratura, non una correzione di un errore, e va trattata come tale.

---

## 4. Il compito proposto: resistenza dello scafo

### 4.1 Fermata 1 (da fare): proposta con criteri

Da scrivere prima di toccare il motore:
- **Modello più semplice:** si cambiano solo `hullK2` e `hullK4` (righe 370-371 di `index.html`), e se serve il termine lineare `4·u` (riga 421), che oggi è scritto nella formula. La forma della formula non cambia.
- **Criteri, come attese nostre da dichiarare prima dei risultati.** Proposta di partenza da discutere:
  - resistenza del motore fra 1,0 e 1,4 volte la vasca fra 2 e 6 nodi (solo scafo più circa 20% per deriva e timone);
  - polare a 9-10 nodi dentro la fascia fra Clark (2014) e Binns (2002);
  - nessuna instabilità nei conti;
  - la barca resta giocabile: virate, raffiche, scuffia a 15 nodi in strambata come oggi (da verificare, non da imporre).
- **Regola dei semi:** soglie scelte su un gruppo di condizioni, confermate su un altro mai guardato.
- **Rischi da dichiarare:**
  - la barca più veloce sbanda di più in raffica (vento apparente più forte), quindi la tabella delle raffiche cambia;
  - le fasce delle prove si accorciano: tutte da ritarare, e i record vecchi diventano non confrontabili (`KEYV`);
  - avversari e partenze sono tarati sulla barca di oggi (per esempio «sotto 0,6 m/s poggia»);
  - le soglie di velocità nelle lezioni (3,3 nodi per «prepararsi a virare», 1 nodo per la virata che non riesce) potrebbero non avere più senso.

### 4.2 Strumenti

- **Laboratorio** (`PROPOSTA-LABORATORIO.md`): un profilo «resistenza vasca Laser», con valori, fonte F-nuova A e stato «ipotesi», per provarlo a mano prima di cambiare il gioco.
- **Collaudi:** quelli del §7 di `archivio/PROPOSTA-SATURAZIONE-TIMONE.md`, più un collaudo della frenata: lunghezze percorse con la prua nel vento, partendo dalla bolina e dal traverso, come nella misura del 13 ottobre.

### 4.3 Documenti da aggiornare quando si fa

- `docs/FONTI-PUBBLICHE.md`: le due fonti nuove, con numero (proposta: F16 e F17; F14 e F15 sono state usate il 13 ottobre per il richiamo individuale e per il regolamento di regata).
- `docs/FISICA-E-TARATURE.md`: tabella delle costanti e risultati.
- `docs/CONTENUTI-DA-VERIFICARE.md`.
- `CHANGELOG.md`, con `VERSIONE`.

---

## 5. Dopo: il timone, con i video

**[stima]** Io non posso guardare i video: le misure le fa Ale.
- **Elenco dei video candidati:** `/home/callle/scuola-di-vela-prove/video-da-misurare.html` (13 video, fuori dal repository).
- **Strumenti:** Kinovea (gratuito), oppure VLC con il tasto «E» per avanzare di un fotogramma.

**Protocollo proposto:**
1. 3-5 video di persone diverse, filtrati prima: barca intera in vista, telecamera ferma, vento intuibile.
2. Per ogni virata:
   - secondi dalla prua che comincia a girare alla rotta nuova;
   - secondi con la prua nel vento;
   - se c'è una ripresa da bordo o da poppa, l'angolo massimo della barra rispetto all'asse della barca, a occhio, in fasce di 10°.
3. Per l'abbrivio, se c'è una scena adatta: lunghezze di scafo percorse con la prua nel vento fino a fermarsi.
4. Si annotano autore, titolo, collegamento, minuto e secondo, vento stimato, e se la virata è «rollata» (con il peso del corpo, che il gioco non simula).
5. Si riporta la fascia (minimo e massimo), mai un numero solo. Una fonte = scelta dichiarata; due o più concordi = verificato su fonti.

Con quei numeri si decide se la saturazione serve, e a quale angolo. Il 22° misurato il 13 ottobre è il punto di passaggio della lezione 5: prua minima 42,5° contro i 43° richiesti dal passo.

---

## 6. Fonti trovate il 13 ottobre 2026 (ricerca web)

- Day e Nixon (2014), Laser in vasca: <https://strathprints.strath.ac.uk/46407/>; PDF: <https://strathprints.strath.ac.uk/46407/7/Day_Nixon_IJSCT_2014_Measurement_and_prediction_of_the_resistance_of_a_laser_sailing.pdf>
- Day (2017), previsione delle prestazioni: <https://strathprints.strath.ac.uk/59980/>; PDF: <https://strathprints.strath.ac.uk/59980/1/Day_OE_2017_Performance_prediction_for_sailing_dinghies.pdf>
- Jon Emmett, «Tacking for Lasers», ILCA, 30 maggio 2018: <https://ilcasailing.org/tacking/>
- «Tacking a Laser», ILCA, 13 maggio 2017 (solo indicazioni qualitative): <https://ilcasailing.org/tacking-a-laser/>
- Schutt e Williamson (2015), virata rollata, abstract APS (nessuna durata nell'abstract): <https://meetings-archive.aps.org/dfd/2015/l16/8>
- Profilo NACA 0012, stallo intorno a 15° a bassi numeri di Reynolds, **profilo bidimensionale, non pala reale**: <https://ijatr.polban.ac.id/ijatr/article/view/134>, <https://aerospaceweb.org/question/airfoils/q0259c.shtml>

**Non usabili come fonti:** forum (35° come stallo per barche più grandi; 2,3-2,5 s per una virata rollata, posti come domanda).

**Non trovato:** la citazione di Cockerill sulle 3-4 lunghezze; riprese dall'alto (drone) di un Laser in virata.

---

## 7. Decisioni per Ale

- Se il gioco resta con la 0.21.2 e la saturazione resta sul ramo di prova.
- Se il prossimo compito di fisica è la resistenza dello scafo (fermata 1 del §4.1).
- Se registrare le due fonti nuove in `FONTI-PUBBLICHE.md` già adesso.
- Se fare il laboratorio prima della resistenza, per provarla a mano.
- Quali video misurare, e quando.
- Questo file sta sul ramo `pulizia-documenti`, creato da `main`: si porta su `main` con quel ramo.
