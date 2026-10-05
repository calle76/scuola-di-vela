# Dubbi e ricerche

Aggiornato al 5 ottobre 2026. È l'elenco vivo dei piccoli dubbi e delle idee rimandate, da riprendere in sessioni di ricerca dedicate. Non serve risolverli per andare avanti: il progetto procede, e ogni semplificazione è dichiarata (vedi `FISICA-E-TARATURE.md`, sezione «Stato finale del prototipo del fiocco», e `MANUALE-bozza.md`).

Come si usa:

- Ogni voce ha uno **stato** e il **tipo di sessione** che serve per chiuderla: *web* (ricerca online), *libro* (un testo da consultare), *esperto* (una persona che naviga), *codice* (una sessione di Claude Code), *prova* (giocare e guardare).
- Quando un dubbio si chiude, non si cancella: si barra e si scrive la data e la fonte.
- Le affermazioni nautiche del gioco vero stanno in `CONTENUTI-DA-VERIFICARE.md`; qui ci sono quelle che hanno un seguito di lavoro.
- Una sola fonte non basta per dire «verificato».

## Da fare per primi (proposta di priorità)

1. **Far leggere `CONTENUTI-DA-VERIFICARE.md` a un velista esperto** (sessione *esperto*): risponde «vero, falso, dipende» a ogni riga. Chiude in una volta molti dubbi delle lezioni.
2. **Controllare la fonte sul momento di imbardata** (sessione *web*): il centro velico a circa 0,2 m a prua del centro scafo, il momento orziero che cresce con lo sbandamento, lo scafo sbandato che orza da solo. Due affermazioni risultano nel testo, la terza solo in parte.
3. **Leggere l'articolo di Binns, Bethwaite e Saunders del 2002** (sessione *web*): previsione di velocità per una deriva monoposto; serve per calibrare la polare.
4. **Studiare By The Lee** (sessione *codice*, sola lettura): come un simulatore dinamico organizza equilibrio, centro velico e smorzamento.
5. **Titoli delle regole di regata 10, 11, 14 e 18** (sessione *web*): prima di scrivere le domande dell'esame.

## 1. Lezioni e regate del gioco vero

Lista completa in `CONTENUTI-DA-VERIFICARE.md`. Quelle che hanno un dubbio dichiarato:

| Dubbio | Stato | Per chiuderlo |
| --- | --- | --- |
| Strambata e abbattuta: sono sinonimi? Alcuni testi chiamano abbattuta la manovra voluta e strambata quella involontaria | Aperto | *esperto* o *libro* |
| Posizione dei filetti sulla randa: sulla balumina o vicino all'inferitura? La regola di lettura è confermata, la posizione no | Aperto | *esperto* |
| Colori dei filetti (rosso a sinistra, verde a destra): scelta del gioco | Dichiarata, da confermare | *esperto* |
| Da quale andatura i filetti della randa non si usano più, e su che cosa si regola la vela al loro posto. Dalla 0.17 il pannello dice «in poppa i filetti non servono» a scotta tutta lascata | Aperto | *esperto* |
| Il limite oltre cui nel gioco i filetti dritti non esistono più (**112° di vento apparente**, cioè circa **135° di vento reale**) è figlio di una barca lenta: il boma arriva al massimo a 85° (`BOAT.maxBoom`) e oltre quell'angolo l'incidenza supera lo stallo. Su un 470 le fonti danno circa **75° apparenti a 120° reali** (F4), contro i **97,5°** del nostro motore: una barca più veloce tiene il vento apparente molto più avanti e i filetti lavorano più a poppa. Da capire se il confine va spostato, e se per farlo serve una barca più veloce o un limite di scotta diverso | Aperto | *esperto*, poi *codice* |
| Comandi di manovra («Pronti a virare?», «Viro!»…): varianti tra scuole | Aperto | *esperto* |
| Orziera: verificare il termine usato nell'esercizio di rotta | Aperto | *esperto* |
| Confini delle andature (angolo morto circa 40°, testi «circa 45° per lato») | Allineato alle dispense come convenzione didattica | *esperto*, per le derive reali |
| Procedura di partenza reale (5 minuti; il gioco permette anche 1 e 3) | Da verificare | *web* o *esperto* |
| Boe lasciate sempre a sinistra: le istruzioni di regata reali lo stabiliscono di volta in volta | Dichiarata | *esperto* |
| Toccare una boa in regata comporta una penalità: nel gioco non è ancora gestito | Aperto | *codice*, dopo la verifica della regola |
| Penalità di 15 secondi per un contatto invece dei giri di penalità | Semplificazione dichiarata | *esperto*, poi *codice* |
| Regole di precedenza da inserire nelle domande dell'esame: il corso federale cita le regole 10, 11, 14 e 18 | Titoli da verificare sul testo ufficiale | *web* |

## 2. Il fiocco e la barca a due (prototipo, tappe A, B e C)

Il prototipo è chiuso con le semplificazioni dichiarate. I dubbi che restano:

| Dubbio | Cosa sappiamo | Per chiuderlo |
| --- | --- | --- |
| **Limite di apertura della scotta del fiocco (80° nel prototipo)** | Nessuna fonte; su questo si appoggia tutta la zona in cui il fiocco non si regola (oltre circa 107° apparenti) | *esperto* |
| **Soglia dell'ombra della randa sul fiocco** (95°-107° apparenti) | Una sola fonte, con spinnaker: il fiocco aiuta fino a circa 100° e da circa 120° è un ostacolo. Senza spinnaker non è noto | *libro* (Marchaj) o *esperto* |
| **Il fiocco coperto dà zero, non resistenza** | Le fonti lo chiamano «un ostacolo»: una vela che sbatte frena. Il modello azzera la spinta ma non la rende negativa | *esperto* |
| **Il fiocco a farfalla** (dal lato opposto alla randa) | È la manovra vera in poppa; con spinnaker o gennaker il fiocco si fissa. Da quale andatura serve, e se sulle derive a due si usa l'asta, non risulta | *esperto*; poi *codice* per modellarla |
| **L'upwash della randa sul fiocco** | Spiega perché il fiocco fa stringere meglio il vento; non modellato, per questo l'ottimo di bolina resta a 50° e non a 48°. La spiegazione «Venturi» è sbagliata | *libro*; poi *codice* |
| **Quanto spinge un fiocco a collo** | Nessuna fonte, né in gradi al secondo né in newton | *libro* o *esperto* |
| **Il ginocchio nella velocità fra 126° e 132° di vento reale** (fino a 0,16 nodi per grado) | Dovuto alla rampa stretta dell'ombra; da giudicare giocando | *prova* |
| **Il limite del vento per il livello 2** (stimato in 12-15 nodi) | È una stima: a 20 nodi di raffica si scuffia e a 15 la virata non riesce; il confine non è stato misurato | *codice* (misura), con le lezioni |

## 3. Equilibrio, timone e raddrizzamento

Dalla fonte su una deriva olimpica a due (una sola barca):

| Dubbio | Cosa sappiamo | Per chiuderlo |
| --- | --- | --- |
| **Momento d'imbardata dovuto alle vele** (randa che fa orzare, fiocco che fa poggiare, scafo sbandato che orza da solo) | Non modellato: il motore gira solo col timone. Modellare il solo fiocco dà una barca sempre poggiera, contro la fonte | *web* (ricontrollare la fonte), poi *codice* con un motore più dinamico |
| **Timone in stallo oltre circa 15°** | Nel motore non stalla mai: barra a fondo (30°) gira 1,93 volte più in fretta che a 15° ed è sempre la scelta migliore | *esperto*; cambiarlo tocca tutte le virate e i tempi del gioco |
| **Coppia raddrizzante di una deriva a due** | Circa 60 kgf·m senza trapezio e circa 220 col trapezio (una barca); il prototipo vale 83,7 kgf·m a 22,6° | *esperto* |
| **Massa e resistenza dello scafo** | Nel motore la massa non entra nella resistenza: una barca più pesante andrebbe più veloce. Nessun dato per ritarare | *web* (polari di derive) |
| **Peso dell'equipaggio come comando** | Oggi il timoniere si sporge da solo, con 0,9 s di ritardo; nella realtà è una manovra (lezione 2.5) | *codice*, con il prodiere |
| **Planata** (livello 3) | Non c'è: sopra gli 8 nodi circa le velocità non possono essere realistiche | *libro*, poi *codice* |

Gennaker e planata richiedono un prototipo dedicato prima di progettare le lezioni 3.x. Le lezioni 2.3 (errore di coordinamento) e 2.5 (peso come comando) non dipendono da fisica che manca: si possono progettare con il motore attuale.

Pagina di domande per un velista (`domande-per-un-velista.pdf`): quando torna compilata, gli esiti vanno in `CONTENUTI-DA-VERIFICARE.md`.

## 4. Velocità e polari

| Dubbio | Cosa sappiamo | Per chiuderlo |
| --- | --- | --- |
| Polari pubbliche di derive | Non risultano. I database aperti vengono da certificati ORC e riguardano barche a chiglia e sportboat; la licenza dei dati non è chiara | *web* |
| Confronto del gioco con una deriva monoposto standard | Una tabellina in un forum (provenienza non verificabile): a 10 nodi il gioco risulta più lento del 20-40%, soprattutto in poppa, dove una barca vera plana | *web* (articolo del 2002), poi *codice* |
| Coefficienti di portanza e resistenza delle vele leggibili nel testo | Le figure dello studio sulla deriva olimpica non lo sono | *libro* |

## 5. Modelli e dati esistenti

| Idea | Stato | Per chiuderla |
| --- | --- | --- |
| **By The Lee** (simulatore di vela in JavaScript, licenza Apache-2.0): riferimento per una dinamica minima nel nostro motore | Ricordata come riferimento; letto solo il README | *codice*, sola lettura: come organizza equilibrio, centro velico, smorzamento |
| Python-VPP, sailboat-playground, simulatore su atterwind.info | Licenze non verificate | *web*, solo se serve |
| **Scala del realismo**: gradino 1 motore cinematico dichiarato (oggi); gradino 2 pochi pezzi mirati con dati di fonte (barra «pesante» da sbandata, stallo del timone); gradino 3 motore dinamico completo | Idea | Decidere dopo il parere di un velista sul livello 1 |

## 6. Livelli, ruoli e carriera

Decisioni ancora aperte (vedi `VISIONE-LIVELLI-E-CARRIERA.md` e `ROADMAP.md`):

- Gli aiuti (barra che torna al centro, «gira la prua», suggerimenti) valgono per i meriti in carriera?
- Rosa dei candidati dell'equipaggio: profili, quanto cambiano, valore del tetto del bonus.
- Come si danno gli ordini all'equipaggio (tasti e presentazione) e il preavviso minimo di ogni manovra.
- Il fiocco a collo come errore di coordinamento nel registro degli errori: tempi e regola (lezione 2.3).
- Livelli 4 e oltre: ruoli, regole, quali barche entrano davvero. Quanti ruoli servono per il brevetto dal livello 3.
- Tarature dei numeri dei meriti, durata dei tornei, bonus del primo torneo in un ruolo nuovo, soglie della competizione.
- Il gennaker asimmetrico come soluzione più diffusa rispetto allo spinnaker con tangone: non verificato (*libro* o *esperto*).
- Esistenza e funzione del tattico su equipaggi di più persone (*esperto*).
- Tasti con due vele: A e D sulla randa nel prototipo; l'idea di A S D W per la barca a una vela va ripensata.
- Quiz con domande in più, perché il ripasso non coincida con l'esame.

## 7. Cose tecniche

- Il pannello delle lezioni ha margine zero: un cursore in più per il fiocco non ci sta e andrà ripensato per le lezioni a due vele.
- Il paragrafo troncato nelle impostazioni (la classe del pannello è riusata nel dialogo dove il testo è lungo), difetto trovato in `index.html`.
- Playwright non è installato in modo permanente: i collaudi usano una copia temporanea.
- Font Barlow Semi Condensed e Source Serif 4: se mancano, le misure del pannello sono più pessimistiche del vero.
- Il giudizio di chi gioca sulla tappa C1 non è ancora arrivato: va chiesto dopo aver giocato il prototipo.
- Le conoscenze del progetto vanno ricaricate quando cambiano i documenti (`CONTENUTI-DA-VERIFICARE.md` per ultimo).

## 8. Persone da coinvolgere

- **Un velista esperto**, per `CONTENUTI-DA-VERIFICARE.md` e per giocare il livello 1 e il prototipo. Due domande: dove senti che la barca non risponde come la tua, e quali due differenze ti darebbero più fastidio.
- **Lucio**, per provare il prototipo con tre domande: dove una posizione giusta del fiocco c'è la trovi? Il messaggio nel pannello ti dice cosa fare? Qualcosa ti confonde?
