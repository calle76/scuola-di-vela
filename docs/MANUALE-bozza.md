# Scuola di vela: il manuale (bozza)

Bozza al 4 ottobre 2026, da rifinire. Questo manuale dice cosa il gioco **insegna**, cosa **simula bene** e cosa **non fa o semplifica**. Non promette niente che il gioco non faccia. È pensato per diventare la sintesi finale dei «giornalini» del progetto.

Ogni punto ha due parti: **«Nel gioco»** e **«In barca vera»**. Dove non c'è una fonte sufficiente, lo scrive.

> Nessun valore legale: i brevetti e i contenuti di questo gioco non sostituiscono un corso di vela né la patente nautica.

## 1. Che cos'è

Un simulatore didattico per imparare a governare una piccola barca a vela, da giocare sul computer con la tastiera. Si parte da zero. Il gioco **non è una previsione delle prestazioni di una barca reale**: i suoi numeri sono tarati per essere plausibili e far imparare comportamenti corretti.

Sei lezioni, cinque prove a tempo con medaglie, regate contro il computer, un registro degli errori, quiz di ripasso, un esame su tutte le lezioni e un glossario. Gli aiuti si possono disattivare: chi vuole più realismo li spegne.

## 2. I comandi (livello 1)

| Cosa | Tasti |
| --- | --- |
| Barra del timone | frecce ← → |
| Barra al centro | Spazio |
| Randa: lascare e cazzare | frecce ↓ ↑ |
| Raddrizzare la barca dopo uno sbandamento forte | R |
| Pulsanti della lezione 1 | W e S |
| Vista del percorso: tenuto premuto, sposta la barca verso il bordo dello schermo opposto all'arrivo o alla boa e, se serve, allontana l'inquadratura finché l'arrivo o la boa si vedono; al rilascio tornano posizione e zoom di prima (solo nelle prove e nelle regate) | Q |
| Avvicinare e allontanare l'inquadratura | pulsanti + e − sul mare, rotellina del mouse (dalla 0.19.3 si allontana fino a circa 480 m di campo in altezza a 1360×650) |

**Cosa si vede sul mare** (scritto il 13 ottobre 2026 leggendo il codice del disegno, `drawBoat`, `drawWindArrows`, `drawSpeedArrow`, `drawTurnHint`; i colori sono quelli del gioco):

- **Freccia bianca «reale»:** il vento reale; arriva dal mare e punta verso la barca.
- **Freccia gialla «apparente»:** il vento apparente, dallo stesso lato; nelle prime tre lezioni non c'è.
- **Freccia verde chiaro «velocità»:** parte dal centro della barca e punta dove la barca si muove davvero (scarroccio compreso); più è lunga, più la barca è veloce; sotto 0,3 nodi non si vede.
- **Piccola freccia gialla in cima all'albero (segnavento):** la punta indica da dove arriva il vento apparente, quindi sembra opposta alla freccia gialla grande.
- **Freccia gialla curva davanti alla prua:** compare mentre la prua sta girando e indica il lato verso cui gira. Ha lo stesso giallo delle frecce «apparente»; non ha scritte.
- **Filetti rosso e verde sulla vela:** uno per lato; si agita quello che mostra la vela mal regolata (lezione 3).
- **Rosa dell'angolo morto, in basso:** l'arco rosso è l'angolo morto; la lancetta diventa rossa quando la prua ci entra.
- **Freccia arancione al bordo dello schermo:** dove si trova la boa o l'arrivo quando sono fuori schermo; le boe sono arancioni (grigie quando sono già girate); l'arco giallo chiaro con la punta, attorno a una boa, è il verso del giro.
- **Sbandamento:** il mezzo cerchio in basso a sinistra, con la lancetta bianca e la scritta «sbandamento N°»; le zone colorate vanno dal verde (sbandamento contenuto) al rosso scuro (barca quasi sdraiata).
- **Scarroccio:** lo scivolamento laterale non ha un indicatore proprio. Si vede dalla freccia verde chiaro «velocità», che non è allineata con la prua: la differenza è lo scarroccio. Il numero in gradi sta nel pannello, alla voce «Scarroccio».
- **Linea scura corta, traversale, vicino all'albero:** è l'albero inclinato visto dall'alto, verso sottovento. Più è lunga, più la barca sbanda.
- **Pallino arancione:** è il timoniere. Si sporge sopravvento da solo per contrastare lo sbandamento; il suo peso conta nella fisica ma non si regola con un comando.
- **Tratti grigio scuro:** boma, albero (si vede come una linea quando la barca sbanda), pala e barra del timone sotto la poppa. Non sono frecce.

Dalla 0.18 il gioco può registrare la sessione per segnalare problemi (impostazioni ⚙, «Registra la sessione»; il tasto M segna un momento): è spenta di norma e il file resta sul computer, senza nessuna connessione. Una volta accesa, la registrazione resta accesa finché non la spegni tu: non si ferma alla fine di una prova. Se la spegni e la riaccendi, nel file le pause sono scritte in secondi veri.

Alla fine di un ripasso, se ci sono errori, il gioco elenca le domande sbagliate con la risposta data, quella giusta e la spiegazione. «Ripassa solo le sbagliate» riporta solo quelle domande e non cambia il punteggio migliore, che si aggiorna soltanto con un ripasso completo.

**L'esame** (dalla 0.20; menu, riquadro «Ripasso ed esame»). È una verifica interna al gioco: ogni domanda nasce da un passo delle lezioni, non c'è niente da studiare fuori. Venti domande a scelta multipla, estratte a caso ogni volta in quote fisse per lezione (lezione 1: 4, lezione 2: 3, lezione 3: 4, lezioni 4, 5 e 6: 3 ciascuna); si supera con almeno 16 giuste. Durante l'esame il gioco non dice se una risposta è giusta, non mostra spiegazioni e non lascia cambiare la risposta data: le spiegazioni arrivano tutte alla fine, con le domande sbagliate raggruppate per lezione e, per ciascuna, il passo della lezione da cui viene. Due avvertenze:

- **Nel gioco libero l'esame è una prova e non si salva niente**: né il punteggio né l'esito. Brevetto, attestato e libretto arriveranno con la carriera.
- **Chiudere il riquadro a metà (tasto Esc) fa perdere l'esame in corso**: si ricomincia da capo, con domande nuove.

**Gli avversari nelle regate** (riquadro prima della partenza, menu «Avversari»). Sono sempre tre barche, Rossa, Verde e Blu, e ognuna ha un carattere che il riquadro scrive prima del via.

- **Principianti:** ogni barca è *prudente* (sta alla larga dalle altre) o *normale*, a caso. Possono capitare anche tre caratteri uguali.
- **Esperti:** di bolina stringono di più il vento (45-48° contro 49-54° dei principianti) e regolano la vela con meno errore. Una sola barca, scelta a caso, è *aggressiva in partenza* (cerca la linea con la precedenza); le altre due sono prudenti o normali. L'aggressiva c'è **solo** con gli esperti.
- **Nessuno:** sei da solo; dalla seconda regata gareggi contro il fantasma del tuo record.
- **Cambiare il livello rifà la partenza:** posizioni, caratteri e conto alla rovescia ricominciano da capo, con lo stesso vento.

**Gioco libero e carriera** (dalla 0.22; selettore in alto nel menu). Sono due salvataggi separati, nello stesso browser, ognuno con i suoi tempi, i suoi ripassi e i suoi fantasmi. Quello che fai in uno non conta nell'altro. «Azzera i progressi» cancella solo la modalità in uso, fantasmi compresi. Se si cancellano i dati del sito nel browser, si perdono tutti e due.

**La carriera: cosa serve per superare il livello 1** (dalla 0.23 il libretto; numeri provvisori, da tarare giocando). Nel menu, in carriera, il **libretto** mostra quattro punteggi, ognuno con quanti punti servono (in rosso finché non li hai, poi in verde). Sotto, una riga dice **tutto quello che manca**, e un'altra suggerisce **cosa potresti fare adesso**: il suggerimento cambia ogni volta che torni al menu, così si alternano lezioni, prove, ripassi e regate. Si può fare tutto in qualsiasi ordine, e prove, regate e ripassi si possono rifare quante volte si vuole: **conta sempre il risultato migliore**.

| Punteggio | Come si guadagna | Massimo | Serve almeno |
| --- | --- | --- | --- |
| Abilità | Prove a tempo: bronzo 1, argento 2, oro 3, e 1 in più se la prova è stata completata almeno una volta senza errori | 20 | 8 |
| Conoscenza | Ripassi: 2 punti con almeno l'80% di risposte giuste, 1 con almeno il 60% | 12 | 6 |
| Competizione | Le due regate, con gli avversari (principianti o esperti): 1° 4 punti, 2° 3, 3° 2, 4° 1 | 8 | 3 |
| Esperienza | 1 punto per ogni lezione completata | 6 | 6 (tutte) |
| Totale | La somma | 46 | 29 |

- In più serve **l'esame scritto superato** (16 risposte giuste su 20). In carriera **il voto dell'esame superato è definitivo**: non si rifà per migliorarlo. Se non lo superi, il gioco ti dice in quali lezioni hai sbagliato: fai il ripasso di ognuna fino in fondo (con qualsiasi punteggio) e l'esame si riapre. Un esame lasciato a metà non conta.
- **L'attestato** compare da solo la prima volta che torni al menu con tutto fatto, in qualsiasi ordine. Puoi scriverci il tuo nome (facoltativo) e stamparlo; poi lo riapri dal libretto. **Non ha nessun valore legale.**
- **Regate senza errori:** il libretto le conta a parte («Regate senza errori: 1 su 2»). Non danno punti e non cambiano il piazzamento: un 3° posto resta un 3° posto.
- **Errori:** al livello 1 non tolgono punti. Contano solo per la «senza errori» (★) e, nelle prove, per il punto in più.
- **Navigazione libera** e tutto quello che si gioca in «Gioco libero» non contano per la carriera.
- **Gli aiuti** (suggerimenti, frecce, rosa dell'angolo morto, barra che torna al centro, frecce che girano la prua…) si possono accendere o spegnere: **non cambiano i punti**. Nessun aiuto guida la barca al posto tuo.
- **Semplificazioni della 1.0:** la Competizione viene dalle due regate singole, non da un torneo; c'è un brevetto solo (livello 1); la banca dell'esame è piccola (26 domande, quindi due esami di seguito hanno molte domande in comune); i numeri del libretto sono provvisori e si tareranno giocando.
- I punti del libretto sono **meriti**, non una classifica: la classifica dei tornei, quando arriveranno, userà i punti del regolamento di regata (1 al primo, 2 al secondo…, vince chi ne ha meno).

## 3. I comandi nei livelli successivi

Oggi esiste solo il livello 1, con i tasti della tabella sopra. Dal livello 2 (fiocco, due ruoli) ogni ruolo comanda quello che deve comandare, senza un numero fisso di comandi, con questa regola (decisa il 7 ottobre 2026): per ogni ruolo il comando principale è su W S; le altre coppie verticali (E D, poi altre da scegliere evitando R) solo se il ruolo ha più comandi; A e Z restano liberi per funzioni speciali; Q è il tasto vista (dalla 0.19.2). Barra con ← →, Spazio, R e M restano come sono. In sintesi: ← → barra; W S comando principale del ruolo (randa, o fiocco per il prodiere); E D seconda coppia solo se il ruolo ha più comandi; Q vista del percorso (tenuto premuto, prove e regate); A e Z liberi per funzioni speciali; R raddrizza la barca e non va riusato; il livello 1 resta com'è (tabella sopra).

## 4. Cosa il gioco fa bene

- **Il vento apparente.** Il vento che senti a bordo è la combinazione del vento reale e del vento dovuto al moto: accelerando si sposta verso prua. Su questo lavora la vela.
- **L'angolo morto.** Con la prua troppo vicina al vento la vela non spinge e la barca si pianta. In questa barca la barca non avanza sotto circa 33° dal vento e arranca fino a circa 40°.
- **Le andature.** Bolina, traverso, lasco, gran lasco e poppa, con la velocità che cambia di conseguenza: la barca è più veloce al traverso e al lasco che in poppa.
- **La regolazione della vela con i filetti.** Due filetti sulla randa mostrano se la vela è troppo lasca, troppo cazzata o regolata, e il gioco dice cosa fare.
- **L'abbrivio e lo scarroccio.** La barca ha una velocità che sale e scende con la massa e la resistenza, e a bassa velocità scivola di lato.
- **Virata e strambata.** Si vira con la barca lanciata; senza velocità la barca si pianta e poi arretra. La strambata con la vela tutta aperta può scuffiare.
- **Lo sbandamento e la scuffia.** Il vento fa sbandare; il timoniere si sporge per contrastarlo, con un piccolo ritardo, per questo le raffiche improvvise fanno sbandare. Oltre 60° la barca scuffia.
- **Il timone.** Gira la barca in proporzione alla velocità; ferma non funziona; all'indietro funziona al contrario.

## 4. Cosa il gioco semplifica o non fa

| Cosa | Nel gioco | In barca vera | Quanto conta per chi impara |
| --- | --- | --- | --- |
| **La barca che gira da sola per effetto delle vele** | Con la barra al centro la barca va dritta (salvo il disturbo apposta nella lezione 2) | Secondo le fonti consultate, cazzando la randa la barca tende a orzare, e sbandando orza ancora di più: si sente la barra «pesante» | Alto: è una sensazione che un velista riconosce subito |
| **La barra a fondo** | È sempre la scelta migliore | Oltre circa 15° il timone frena senza girare di più (una sola fonte) | Medio: si può imparare un'abitudine sbagliata |
| **Uscire dall'angolo morto** | Si esce solo col timone: mentre la barca arretra, barra verso il boma, poi barra al centro e si cazza. Il boma non si può spingere a mano; con la barra al centro la barca può restare a lungo all'indietro | Tre fonti descrivono la randa «a collo»: si spinge il boma fuori e la barra dalla stessa parte, la barca arretra e la prua si allontana dal vento, poi si centra, si cazza e si riparte (US Sailing; guida Sunfish di un circolo; associazione di classe di un catamarano; vedi `DUBBI-E-RICERCHE.md`, sez. 3). Da ricontrollare sulle pagine originali | Medio |
| **La planata** | Non c'è: con vento fresco la barca è più lenta di una deriva vera | Sopra circa 8 nodi di velocità una deriva a due olimpica passa a un regime di alta velocità (una fonte) | Medio: conta di più dal livello 3 |
| **Il peso del timoniere** | Si sporge da solo, con un ritardo | Gestire il peso è una parte importante della conduzione | Medio: diventerà un'azione del prodiere |
| **Onde e corrente** | Non ci sono, salvo piccoli disturbi nella lezione 2 | Cambiano la guida e la velocità | Basso |
| **Il raddrizzamento** | Con un pulsante, in 3 secondi | È una manovra fisica che richiede equilibrio e tempo | Basso |
| **Le raffiche** | Chiazze che viaggiano col vento; si vedono fino a circa 115 m sopravento alla barca, e gli avversari lontani non sentono le tue | In barca vera il campo di vento esiste su tutta l'area e si vede da lontano, con una struttura più complessa sull'acqua | Basso per le prove; da rifare per regate e tattico |
| **Una sola vela** | Solo la randa nel gioco; il fiocco c'è solo nel prototipo | Le derive a due hanno anche il fiocco, e le più veloci un gennaker o uno spinnaker | Per questo ci sono i livelli successivi |
| **Penalità e regole di regata** | Il contatto costa 15 secondi a chi ha torto (mure a sinistra contro mure a dritta, o sopravento con le stesse mure); un contatto senza colpa tua resta scritto ma non conta negli errori né toglie la ★; toccare una boa non è ancora punito | In regata ci sono i giri di penalità e regole più ricche | Medio |

Nota onesta sulla velocità: confrontando con una tabella trovata in un forum (provenienza non verificabile) per una deriva monoposto standard, a 10 nodi di vento il gioco risulta più lento del 20-40%, soprattutto in poppa, dove una barca vera plana. Non è un difetto accertato: i dati sono incerti e i confronti approssimativi.

## 6. Il fiocco (livello 2, per ora solo prototipo)

Il fiocco non è ancora nel gioco: vive in un prototipo separato, `sperimentale/fiocco.html`.

**Cosa fa**

- È una seconda vela vera, con la sua scotta (tasti Q ed E), i suoi filetti e il suo disegno. Spinge e sbanda insieme alla randa, un po' meno perché è più bassa.
- Alle andature larghe la randa gli toglie il vento: fino a 95° di vento apparente lavora pieno, fra 95° e 107° perde pressione, da 107° non spinge più.
- Il pannello dice cosa fare e, dove non c'è niente da fare, lo ammette. Se la scotta ha una posizione con i filetti dritti, il pannello dice se cazzare o lascare; dove non esiste dice che il fiocco lì non si regola.
- La barca senza fiocco resta identica a quella del gioco, verificato a ogni tappa.

**Cosa non fa**

| Cosa | Perché | In barca vera |
| --- | --- | --- |
| Il fiocco a farfalla (dal lato opposto alla randa, in poppa) | Non modellato: il pannello lo dice | Con la randa che lo copre, il fiocco si porta dall'altra parte, spesso con un'asta; con spinnaker o gennaker si fissa |
| Il fiocco a collo in virata | Sarebbe una taratura senza fonte, che andrebbe rifatta col prodiere | Un fiocco ancora cazzato dal lato vecchio spinge la prua; se ne occupa l'equipaggio. Nel gioco diventerà un errore di coordinamento |
| Il momento d'imbardata dovuto alle vele | Il motore gira solo col timone. Modellare il solo fiocco dava una barca sempre poggiera, contro la fonte | La randa fa orzare, il fiocco fa poggiare |
| Una barca a due con più massa | Una deriva a due senza trapezio sarebbe meno stabile del prototipo; il trapezio sarebbe una seconda novità per il livello 2 | Una deriva a due ha più massa e un equipaggio di due |
| L'upwash della randa sul fiocco | Non modellato: il fiocco non migliora la bolina | Il flusso della randa fa lavorare meglio il fiocco. La spiegazione «accelerazione come in un tubo» è sbagliata |
| Lo stallo del timone, la planata | Non nel motore | Vedi sopra |

**Il prototipo è sovrainvelato.** Con una raffica da 20 nodi si scuffia e a 15 nodi la virata non riesce. Il livello 2 va giocato con vento da leggero a medio (il limite esatto è una stima da misurare).

## 7. Come sono stati verificati i numeri

- Ogni modifica si collauda guidando davvero la barca con un pilota automatico, con molti tentativi e semi fissi.
- Le fasce di tempo delle prove (bronzo, argento, oro) sono tarate sul tempo del pilota automatico.
- Le soglie dei criteri si scrivono prima di misurare e non si cambiano dopo, senza dirlo. I numeri che escono dalla fascia si riportano così come sono.
- Le affermazioni nautiche sono confrontate con fonti pubbliche (dispense e manuali federali, uno studio scientifico su una deriva olimpica a due). Una sola fonte non basta per dire «verificato». L'elenco di ciò che resta da controllare è in `CONTENUTI-DA-VERIFICARE.md` e in `DUBBI-E-RICERCHE.md`.

## 8. Quanto è realistico: tre gradini

| Gradino | Cosa | Stato |
| --- | --- | --- |
| 1 | Motore cinematico, con le semplificazioni dichiarate qui sopra | **Oggi** |
| 2 | Pochi pezzi mirati con dati di fonte: la barra «pesante» da barca sbandata, lo stallo del timone | Idea |
| 3 | Un motore dinamico completo (scafo, deriva, timone e vele che producono forze e momenti), con un simulatore esistente come modello da studiare | Idea |

## 9. Per chi scrive questo manuale

- Si aggiorna a ogni versione chiusa: una voce nuova per ogni novità.
- Non promette più di quanto il gioco fa: solo ciò che è verificato o dichiarato come semplificazione. Il resto sta in `DUBBI-E-RICERCHE.md`.
- Dove una frase «In barca vera» ha una sola fonte, lo scrive.
- Le fonti pubbliche sono parafrasate, non copiate; nessun nome di classe o costruttore nel gioco; il logo e il nome «Scuola Vela FIV» non si usano.
