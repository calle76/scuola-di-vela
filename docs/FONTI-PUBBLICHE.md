# Fonti pubbliche consultate

Aggiornato al 4 ottobre 2026. È il registro delle fonti usate per tarare e giustificare la fisica e i contenuti. L'elenco delle affermazioni ancora da controllare resta in `CONTENUTI-DA-VERIFICARE.md`; le semplificazioni del motore in `FISICA-E-TARATURE.md`; il disegno dei livelli in `VISIONE-LIVELLI-E-CARRIERA.md`.

## Regole d'uso

- **Parafrasare, non copiare.** Testi e tabelle delle fonti sono protetti. Le lezioni e le domande dell'esame si scrivono con parole nostre.
- **I nomi delle classi di barche compaiono solo in questi documenti**, mai nel gioco (principio 5 di `PROGETTO.md`). Qui servono per sapere a quale barca si riferisce un dato.
- **Dati con licenza poco chiara non entrano nel gioco** finché la licenza non è verificata (vedi le polari, sotto).
- Il logo e il nome «Scuola Vela FIV» sono marchi registrati della federazione: non usarli.
- Ogni dato qui ha lo stato **supportata da fonte** (con il livello di affidabilità) oppure **da verificare**. Una sola fonte non basta per dire «verificato».

## Elenco delle fonti

| Sigla | Fonte | Tipo | Affidabilità per il gioco |
| --- | --- | --- | --- |
| F1 | Dispense XIV Zona FIV, «La regolazione delle vele», corso istruttori di primo livello. https://xivzona.it/files/Regolazioni-delle-vele-generale-derive-tavole-y-m.pdf | Didattica federale | Buona per la pratica; nessuna misura. Il testo estratto ha qualche lettera sbagliata. |
| F2 | Manuale FIV di una classe giovanile a due, edizione 2006. http://win.ottavazona.org/download/420/Lib_420_06.pdf | Manuale federale | Buona per regolazioni e tabelle indicative (gli autori stessi le dichiarano tali). |
| F3 | Normativa Scuola Vela FIV 2021-2024, Libro II. http://vii-zona.federvela.it/sites/default/files/normativa_scuolavela2021_completa.pdf | Normativa | Buona per i livelli dei corsi. La versione 2025-2028 è sul sito federale (voce Scuola Vela); il link diretto non era raggiungibile. |
| F4 | Masuyama e Ogihara, «Science of the 470 Sailing Performance», Journal of Sailing Technology 5(1), 2020, pp. 20-46. https://onepetro.org/jst/article-pdf/5/01/20/2478407/sname-jst-2020-05.pdf | Articolo scientifico (galleria del vento, prove di traino, previsione di velocità) | Ottima ma unica: una sola barca. Il testo è stato letto da una copia; le figure con i coefficienti non sono nel testo. |
| F5 | Spiegazione della fessura (Gentry): https://en.wikipedia.org/wiki/Genoa_(sail); https://www.uksailmakers.com/2021/10/21/2021-10-21-setting-the-record-straight-on-inhaulers/; https://www.sailingscuttlebutt.com/2021/10/06/taking-a-deep-dive-into-sail-slots/ | Enciclopedia e articoli di velerie | Discreta. Nei forum c'è chi nega l'effetto: opinioni, non fonti. |
| F6 | Dati di stazza: https://en.wikipedia.org/wiki/420_(dinghy); https://en.wikipedia.org/wiki/470_(dinghy); https://en.wikipedia.org/wiki/Cadet_(dinghy) | Enciclopedia | Buona per le aree. |
| F7 | Andature portanti: https://www.sailingworld.com/how-to/downwind-under-jib-and-main/; https://www.speedandsmarts.com/toolbox/articles2/smallboat-sailing/sailing-downwind; https://www.morganscloud.com/2015/05/24/downwind-sailing-poling-out/ | Articoli divulgativi | Letti solo gli estratti di ricerca. |
| F8 | Database di polari da certificati ORC: https://www.boatpolars.com/ | Database | Riguarda barche a chiglia e sportboat; licenza dei dati non chiara. |
| F9 | Tabellina di velocità per una deriva monoposto standard, in un forum: https://sailingforums.com/threads/laser-speeds.175/ | Forum | Provenienza non verificabile. |
| F10 | Binns, Bethwaite e Saunders, 2002 (previsione di velocità per una deriva monoposto), citato in https://www.researchgate.net/figure/Polar-plots-for-the-current-simulator-performance_fig8_257246942 | Articolo | Non letto; è la fonte da leggere per calibrare. |
| F11 | Programma di una scuola vela in 5 livelli: https://www.scuolavela.com/it/scuola-vela/corsi-derive/ | Pagina di una scuola | Solo come confronto. |
| F12 | C. A. Marchaj, *Sail Performance: Techniques to Maximize Sail Power* (2002-2003, ISBN 9780071413107). | Libro | Non consultato. Dall'indice: incidenza ottimale in funzione di andatura e vento, interazione fra le vele, centro velico. |

I forum citano anche, come lettura pratica sulla regolazione delle vele, *Sail Power* di Wallace Ross (1975). Sono pareri di forum, non verifiche.

## Cosa dicono le fonti

### Il fiocco e la randa

| Tema | Cosa risulta | Stato |
| --- | --- | --- |
| Area del fiocco | Il fiocco è circa un terzo della randa: rapporti di 38% (7,45 e 2,8 m²), 39% (9,12 e 3,58 m²) e 32% (3,9 e 1,26 m²) su tre derive a due (F6). Il prototipo (2,6 su 7,0 m², 37%) è coerente. Attenzione: la pagina ufficiale di una classe riporta 10,25 m² come «randa», che è in realtà l'area totale controvento. | Supportata da fonte |
| Fessura tra le vele | L'effetto è reale ma si spiega con il flusso ascendente (upwash) della randa sul fiocco e quello discendente (downwash) del fiocco sulla randa, che ne riduce il rischio di stallo e fa stringere meglio il vento. La spiegazione «l'aria accelera nella fessura come in un Venturi» è considerata sbagliata (F5). | Supportata da fonte. Nelle lezioni non va insegnata la spiegazione dell'accelerazione. |
| Fiocco e randa come un sistema | Lascando la randa va ritoccata anche la scotta del fiocco; con vento forte la randa «rifiuta» se il fiocco è troppo chiuso vicino all'inferitura (F1). Nel modello la regolazione del fiocco non influisce sulla randa. | Supportata da fonte; non modellata |
| Regolazioni del fiocco | Quattro leve: altezza della mura, arretramento della penna, tensione della scotta, tensione della controscotta (F2). Con vento forte la scotta del fiocco va tenuta più lenta per aprire la balumina e non chiudere il canale con la randa (F2). La tabella indicativa del manuale dà la scotta del fiocco lenta con poco vento, cazzata con vento medio e forte, appena lascata con vento fortissimo. | Supportata da fonte (indicativa) |
| Fiocco coperto dalla randa | Alle andature larghe e in poppa il fiocco è coperto dalla randa. Senza spinnaker né gennaker si porta a farfalla su un tangone; con spinnaker o gennaker in poppa non influisce e si fissa (F1, F7). | Supportata da fonte. La farfalla non è nel prototipo. |
| Soglia dell'ombra | Nel 470, con lo spinnaker, il fiocco dà più spinta che senza fino a circa 100° di vento apparente, mentre da circa 120° in poi è un ostacolo e la scotta cade lasca (F4). Dalla tappa C il prototipo usa un'ombra che parte a **95°** e diventa totale a **107°** apparenti (prima: 85° e 135°, con una perdita massima del 70% invece che del 100%). | Una sola fonte, **e con lo spinnaker**, che copre il fiocco prima di quanto faccia la sola randa: i 107° potrebbero essere presto. Il 107° non è scelto per ragioni aerodinamiche, ma perché è lì che sparisce la posizione giusta del fiocco (vedi la riga sotto). |
| Boleggio | Il manuale (F2) dice che quella barca boleggia poco, per le linee d'acqua tondeggianti, e che stringere troppo il vento è quasi sempre dannoso: meglio sfruttare la velocità. L'ottimo di bolina del prototipo a 50° (invece dei 48° che ci aspettavamo) è quindi plausibile. | Supportata da fonte |
| Limite della scotta del fiocco | Nessuna fonte per i 80° del prototipo. | **Da verificare**, e ora conta di più: dalla tappa C è questo limite a fissare l'angolo (107° apparenti) in cui il fiocco smette del tutto di spingere. Si sta tarando l'aerodinamica su una geometria non verificata. |

### Equilibrio, timone, sbandamento (per la tappa C)

| Tema | Cosa risulta | Stato |
| --- | --- | --- |
| Centro velico e barra | Cazzando la scotta il centro velico si sposta verso poppa: più sbandamento e più tendenza a orzare; lascando il contrario (F1). Il motore non ha questo momento di imbardata. | Supportata da fonte |
| Momento di imbardata | Nel 470 il momento della vela è di barca ardente e cresce con lo sbandamento, perché il centro velico si sposta sottovento. Di bolina, con deriva giù e sbandamento zero, scafo e vela sono quasi in equilibrio (timone circa zero) (F4). Tre precisazioni aggiunte il 4 ottobre 2026: (1) di bolina e a sbandamento zero, il centro velico di randa più fiocco e il punto in cui si applica la forza laterale dello scafo stanno **tutti e due circa 0,2 m a proravia del centro dello scafo**, ed è per questo che la barra sta circa a zero; (2) il momento orziero cresce con lo sbandamento secondo **spinta × altezza del centro velico × seno dello sbandamento**; (3) **lo scafo sbandato orza anche da solo**, senza bisogno delle vele. | Una fonte. **Le tre precisazioni sono riferite dal revisore e sono da ricontrollare:** nel progetto non c'è una copia di F4, e il testo citato qui sopra viene da una lettura precedente, non da un documento che possiamo rileggere. |
| Timone | Oltre circa 15° la pala va in stallo e dà solo resistenza. A 6 nodi un timone a 15° dà 12 kgf di resistenza contro 19 kgf di resistenza totale dello scafo (F4). Il motore ha il timone massimo a 30°. | Una fonte; **da valutare** |
| Raddrizzamento | Nel 470 la coppia raddrizzante massima è a circa 25° di sbandamento (con trapezio circa 220 kgf·m, senza circa 60), poi cala; l'intervallo da cui si recupera è stretto e bisogna alleggerire subito (F4). La soglia di scuffia del motore è 60°. | Una fonte; **da confrontare** |
| Massa dello scafo a due | 470: scafo 120 kg, equipaggio ideale 130 kg, totale 250. Classe giovanile: scafo minimo 80 kg, equipaggio 110-145 kg, totale 190-225 (F2, F4, F6). | Supportata da fonte |
| Angolo del vento apparente | Nel 470 di bolina il vento apparente è a 25-30°, e a velocità massima al traverso (vento reale a 90°) a circa 55°; a 120° reali, circa 75° apparenti (F4). Il gioco, con una barca più lenta, dà angoli apparenti un po' più grandi (circa 34° a 48° reali, circa 60° a 90°): stessa direzione. | Coerente |

### Planata e gennaker (per il livello 3)

- Nel 470 la resistenza sale bruscamente fra 5,5 e 8 nodi; oltre gli 8 nodi si passa all'alta velocità, con una semi-planata fra 8 e 12 nodi (F4).
- Con vento forte, di bolina, se la velocità non cresce conviene poggiare di 10-15° per entrare in semi-planata (F4).
- Il miglior angolo per scendere sottovento è circa 150° con vento medio, 140-150° con vento forte (F4): in poppa non si va dritti alla boa.
- Il motore non ha la planata, quindi sopra gli 8 nodi circa le velocità non possono essere realistiche finché non c'è.

### Polari e velocità

- **Non risultano polari pubbliche di derive.** I database aperti (fino a 81 barche) derivano da certificati ORC e riguardano barche a chiglia e sportboat, con la dicitura «dati da fonti pubbliche» (F8). Prima di usare un numero nel gioco va verificata la licenza.
- Una deriva monoposto standard, secondo la tabellina del forum (F9, provenienza non verificabile), va a 6/9/12 nodi di vento: bolina 4/4,8/5; traverso 5,4/6,3/7,3; lasco 5/6,1/8; poppa 4,1/5,5/6,7 nodi.
- Confronto approssimato: a 10 nodi il gioco dà 3,4 (45°), 5,2 (90°), 4,2 (135°) e 3,5 (180°) nodi. Risulta più lento del 20-40%, soprattutto in poppa, dove una barca vera plana. Non è un difetto accertato: fonte secondaria e angoli non confrontabili.

### Livelli, ruoli, regate

- **Programma federale per le derive (F3):** Breve, Base, Intermedio, Avanzato. Il Base copre nomenclatura, orzare e poggiare, cazzare e lascare, mure, vento reale e apparente, bolina e traverso, virata, barca ferma, lasco, poppa e abbattuta. L'Intermedio aggiunge spinnaker o gennaker, vele di prua, planata e pumping, ruoli alternati, manovre di fermo barca e ripartenza, le regole di regata 10, 11, 14 e 18. L'Avanzato riguarda le regate di flotta: messa a punto, ruoli a bordo, strategia e tattica, copertura degli avversari, fisica della vela.
- **Corsi di regata su barche a chiglia (F3):** studio a rotazione dei ruoli, della comunicazione fra equipaggio e del coordinamento; navigatore e tattico solo nell'ultimo corso.
- **Una scuola in 5 livelli (F11):** Base, Perfezionamento (virata, strambata, vento apparente), Avanzato (manovre intorno alle boe, assetto), Avviamento alla regata (spinnaker, messa a punto), Agonistico (regole, partenza, tattica, ruoli a bordo).
- **Percorso agonistico reale (F2):** regate zonali (almeno quattro) e nazionali (in genere quattro) alimentano una classifica di merito per selezionare gli equipaggi ai campionati. Le regate durano 40-60 minuti.
- **Fasce di vento della classe giovanile (F2)**, in m/s e in nodi circa: 1-2 (2-4 nodi, equipaggio in barca), 3-4 (6-8, mezzo trapezio), 5-7 (10-14, trapezio), 8-10 (16-19, sovrapotenziati), oltre 10 (oltre 19). Le dispense F1 danno il vento medio da 7-8 a 14-15 nodi.
- **Regole di regata:** il corso Intermedio cita le regole 10, 11, 14 e 18. Nel regolamento sono le regole su mure opposte, stessa mura con sovrapposizione, evitare il contatto e spazio alla boa: **da verificare sul testo ufficiale** prima di scrivere le domande.

## Cosa non è stato trovato

- Il limite di apertura della scotta del fiocco (80° nel prototipo).
- La soglia dell'ombra della randa sul fiocco senza spinnaker.
- Polari pubbliche di derive; tabelle di coefficienti di portanza e resistenza delle vele leggibili nel testo (le figure del 470 non lo sono).
- A quale andatura serve il fiocco a farfalla nelle derive a due e se si usa l'asta.

## Calibrazioni future (elencate, non fatte)

1. ~~Coerenza fra vista e forza del fiocco coperto: portare `slotShade` verso 1,0 e rimisurare (tappa C, primo compito).~~ **Fatta** (tappa C, primo compito): `slotShade` 1,00, ombra da 95° a 107° apparenti. `slotShade` da solo non bastava: fra 107° e 135° il pannello diceva «non si regola» e il fiocco dava ancora il 16-10%. Restano da verificare i tre punti nuovi in `CONTENUTI-DA-VERIFICARE.md`.
2. ~~Momento di imbardata dovuto alle vele, spegnibile: la barca senza fiocco deve restare identica.~~ **Deciso il 4 ottobre 2026: non modellato nel prototipo del fiocco.** Riguarda tutta la barca — randa, fiocco, scafo sbandato — non il solo fiocco: modellare solo il fiocco dà una barca sempre poggiera, il contrario di quello che dice F4 (misure in `sperimentale/misure_tappaC2.txt`). Resta una calibrazione futura, da affrontare sull'intera barca.
3. Fiocco in virata (controvento, a collo).
4. Timone: stallo oltre circa 15° contro il massimo del motore (30°).
5. Soglia di scuffia e coppia raddrizzante, contro il 25° di sbandamento della fonte.
6. Massa dello scafo a due: da 190 a 250 kg secondo la barca presa a modello.
7. Planata (livello 3).
8. Polare del gioco a 6, 9 e 12 nodi contro i dati di una deriva monoposto, dopo aver letto F10.

## Letture suggerite

Marchaj (F12) per i dati di fisica; Wallace Ross per la pratica; il materiale federale (F1-F3) è gratuito. Per ogni affermazione che entra nelle lezioni vale comunque la regola del progetto: una persona esperta di derive la legge e risponde «vero, falso, dipende».
