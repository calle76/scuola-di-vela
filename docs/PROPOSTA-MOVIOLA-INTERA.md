# Proposta: la moviola di tutta la regata (fermata 1)

1 novembre 2026, gioco alla 1.0.75. Solo documento: nessun codice toccato.

## 1. Perché

Ale, 1 nov (osservazione 73): «proviamo tutta la regata, così almeno, se ci sono dubbi e siamo in fase di test, possiamo dare una migliore versione dei fatti».

Oggi «Rivedi» mostra solo pezzi di 18 s: i 10 s prima e gli 8 s dopo ogni tasto O e ogni contatto con penalità, al massimo 12 (1.0.58, `js/moviola.js`). Quello che succede fuori da quei pezzi non si può rivedere. Ci sono poi due limiti:
- la partenza non si rivede mai, perché la moviola registra solo dopo lo sparo;
- i contatti automatici sono al massimo 6.

Nella prova del 1 novembre il contatto con la Verde, avvenuto prima della partenza, non era rivedibile.

## 2. Il modello più semplice

**Registrazione.** Si usa la stessa copia già fatta oggi, 10 volte al secondo: posizione, prua, sbandamento, velocità, boma e scuffia di ogni barca. Cambiano due cose:
- la copia comincia **con il conto alla rovescia** (dalle bandiere a −5 minuti) e finisce all'arrivo del giocatore o al ritiro;
- la copia non si butta più dopo 10 s: si tiene tutta.

Il gioco non cambia: la moviola continua a leggere soltanto, non chiama `Math.random` e non scrive nulla.

**Momenti.** Il tasto O e i contatti con penalità non fanno più pezzi a parte: diventano **segni sulla regata intera**, come i capitoli di un video.
- Si tengono tutti i contatti con penalità, senza più il limite di 6. Ci sono anche quelli fra avversari, e anche quelli prima della partenza.
- Si tengono anche i tocchi di boa.
- Un segno costa solo un orario e una scritta.

**Riproduzione.** A fine regata «Rivedi» apre la barra della moviola:
- il cursore copre **tutta la regata**, dal conto alla rovescia all'arrivo;
- i segni compaiono come tacche sul cursore;
- in alto c'è il momento in corso, per esempio «Contatto con la Verde, −2:14».

**Memoria.** Una regata di 10 minuti con 5 minuti di preparazione fa circa 9.000 copie da 4 barche. In memoria sono pochi MB.
- Limite dichiarato: 60 minuti, cioè 36.000 copie. Oltre, si tengono gli ultimi 60 minuti e il testo lo dice.
- **Ipotesi nostre**, da misurare: tutte e due le costanti, 10 copie al secondo e 60 minuti.

**Cosa resta com'è.**
- La moviola sta solo in memoria. Lasciata la regata, si perde, come oggi.
- Il racconto completo, da scaricare e da far leggere a me, resta la **registrazione per il coach**, che è un'altra cosa.
- Le scie delle barche restano nascoste durante la moviola, come oggi.

## 3. I tasti

**Durante la regata:** nessun tasto nuovo.

| Tasto | Cosa fa | Cambia? |
| --- | --- | --- |
| **O** | Mette un segno sulla moviola: «qui voglio rivedere». Se la registrazione per il coach è accesa, lo scrive anche nel file | no |
| **M** | Mette un marcatore nel file della registrazione per il coach, con la tua nota | no |
| Contatto con penalità, tocco di boa | Mettono un segno da soli | sì: tutti, anche prima del via |

**Durante la moviola** (la barca non si guida):

| Tasto | Cosa fa | Oggi |
| --- | --- | --- |
| **Spazio** | Pausa / riprendi | uguale |
| **← →** | Indietro / avanti di 5 secondi | oggi cambiano pezzo |
| **↑ ↓** | Segno precedente / successivo: salta a 10 s prima del segno | nuovo |
| **1 2 3** | Velocità 1×, ½×, ¼× (rallentatore) | uguale |
| **4 5** | Velocità 4× e 8×, per scorrere la regata | nuovo |
| **R** | Torna all'inizio della regata | oggi: inizio del pezzo |
| **Esc** | Chiude e torna alla schermata finale | uguale |
| Cursore con il mouse | Va in qualunque punto della regata | oggi: solo dentro il pezzo |

Le frecce ← → cambiano significato: oggi passano da un pezzo all'altro, domani si muovono nel tempo. I pulsanti «◀ Prima» e «Dopo ▶» restano, e saltano fra i segni.

## 4. Criteri (soglie: attese nostre, dichiarate prima)

| | Criterio | Soglia |
|---|---|---|
| V1 | **Fedeltà:** la moviola rimette le barche dove erano. Si confrontano posizione e prua lette dal vivo con quelle della moviola, in punti a caso di tutta la regata, partenza compresa | come oggi in `collaudo_moviola.py`: al più 0,5 m e 5° (oggi misurato 0,019 m e 0,28° in Chromium, 0,114 m e 0,17° in Firefox); almeno 500 confronti su 12 regate per browser |
| V2 | **Il gioco non cambia:** con la moviola nuova e con quella della 1.0.75, arrivi, penalità e posizioni finali sono identici al bit | 12 regate su 12 |
| V3 | **Copertura:** la moviola comincia entro 0,2 s dalle prime bandiere e finisce entro 0,2 s dall'arrivo del giocatore | 12 su 12 |
| V4 | **Segni:** ogni O premuto e ogni contatto con penalità, anche prima del via e fra avversari, ha il suo segno, entro 0,2 s | tutti, con almeno 20 segni contati |
| V5 | **Tasti:** ← → spostano di 5 s, ↑ ↓ portano a 10 s prima del segno, 4 e 5 vanno a 4× e 8×, R torna all'inizio, Esc chiude | tutti, con i tasti veri |
| V6 | **Uscita pulita:** chiusa la moviola, stato e scie sono identici a prima | come oggi |
| V7 | **Costo:** tempo del passo di simulazione con la moviola accesa contro la 1.0.75 | al più +3% (stessa soglia della registrazione, E2) |
| V8 | **Memoria:** copie tenute in una regata di 60 minuti | al più 36.000 |
| V9 | **Barra a 1360×650:** il testo dei tasti non sfora | 0 px |
| V10 | **Pagina senza `#collaudo`:** Rivedi si apre e mostra tutta la regata | sì |

Si misura in Chromium e Firefox. `collaudo_moviola.py` si aggiorna, perché oggi conta i pezzi; ne prende il posto un collaudo della regata intera, con un riferimento della 1.0.75 per V2 e V7.

## 5. Rischi

1. **Le frecce cambiano significato.** Chi era abituato a ← → per cambiare pezzo trova un'altra cosa. Rimedio: la riga dei tasti nella barra lo dice.
2. **Costo del calcolo.** Oggi la copia c'è già, quindi tenerla non dovrebbe costare. Lo controlla V7. Su GitHub E2 e Q7 sono misure di tempo rumorose: V7 andrà fra le voci `~~` dei fallimenti noti, se oscilla.
3. **Regate lunghe.** Oltre 60 minuti si perde l'inizio. È dichiarato nel testo; una regata del gioco dura 4-15 minuti.
4. **Ricaricare la pagina** fa perdere la moviola, come oggi.

## 6. Cosa serve da Ale

1. Il via (fermata 2).
2. Una scelta, se non va bene il consiglio:
   - **includere la partenza** (consiglio: sì, è dove capitano molti contatti);
   - **tasti ← → per spostarsi di 5 s** (consiglio: sì; in alternativa restano per i segni, e i 5 s si fanno con il mouse).
