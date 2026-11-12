# Rivali, sponsor e carriera: idee da discutere

Proposta del 12 novembre 2026, nata in chat da domande di Ale. **Nessun codice toccato. Nessuna decisione presa.**

Stati usati come negli altri documenti, ma senza **[deciso]**: **[proposta]** (idea di Claude da accettare, cambiare o scartare), **[aperto]** (domanda per Ale), **[da verificare]** (da controllare nel codice o giocando prima di fidarsi).

## Istruzioni per Claude Code

1. Copia questo file in `docs/PROPOSTA-RIVALI-E-SPONSOR.md`. Non cambiare il testo.
2. Non toccare il codice e non scrivere nulla in `DECISIONI.md`: finché Ale non risponde alle domande della sezione 10, niente è deciso.
3. In `DA-FARE.md` aggiungi un rimando in fondo alla voce 23 («Idea: avversari con capacità diverse»): «Materiale più ampio (pool di rivali, sponsor, memoria, numero di barche) in `PROPOSTA-RIVALI-E-SPONSOR.md`, da discutere con Ale». Non creare voci nuove.
4. Prima di commit, rileggi la sezione 2 contro il codice e segnala se qualcosa è cambiato (per esempio se `FLEET_LOOK` ha ancora tre voci, se i punti della regata valgono ancora per 4 barche, se gli avversari scuffiano ancora mai).
5. Aggiorna il `CHANGELOG` solo se cambi altro; un documento di proposta non è una versione.

## 1. Come leggere questo documento

Niente qui è deciso. I temi sono tre: rivali (pool, caratteri, dinamiche), sponsor come passaggio di livello, quanti rivali si possono gestire. Le domande per Ale sono raccolte alla sezione 10.

## 2. Punto di partenza (letto sul repository il 12 novembre 2026, versione 1.2.28)

- **Rivali in regata:** tre barche (Rossa, Verde, Blu), guidate da regole scritte con la stessa fisica del giocatore. Aspetto grafico: `FLEET_LOOK` in `js/regate.js`, tre voci.
- **Caratteri:** dalla 0.17 comportamenti di partenza diversi (prudente, normale, aggressivo) e posizioni di partenza casuali; livelli di avversario (principianti, esperti).
- **Cosa non fanno:** non guardano le mosse degli altri in partenza e non scuffiano mai (0 su circa 50 registrazioni, `DA-FARE.md` voce 23). Dalla 1.2.25 nel torneo c'è il cono d'ombra delle vele, ma non lo evitano e non lo usano.
- **Rotta migliore:** dalla 1.2.22, a regata finita e fuori dalla Scuola, c'è la rotta ottimale con layline e «dove hai perso». La diagnosi dei rivali che ne è nata (`PROPOSTA-AVVERSARI-ROTTA.md`): in bolina perdono il 64% del tempo perso, in poppa il 15%.
- **Precedenze:** le regole 10-13 ci sono già nell'1b e gli avversari cedono (dalla 1.0.49); protesta e resto del regolamento sono del livello 2.
- **Carriera:** quattro aree di merito (abilità, competizione, conoscenza, esperienza), esame obbligatorio che consegna il brevetto, tornei provvisori da 4 regate con uno scarto.
- **Principi:** tutto sempre giocabile nel gioco libero; la carriera è una modalità a parte; nomi generici, nessuna classe né marchio reale.
- **Idea già in `DA-FARE.md` voce 23:** a inizio torneo, per ogni avversario, tratti estratti a caso e indipendenti (tendenza all'errore, lettura del vento e scelta del lato, aggressività).

## 3. Pool di rivali e sorteggio

**[proposta]** Il gioco tiene un pool di 8-12 rivali, ognuno con una scheda; ogni torneo ne pesca tre. Un pool piccolo e curato batte cento schede quasi uguali, perché il giocatore deve riuscire a riconoscerli.

Una scheda contiene: nome generico (un colore, come oggi), fascia, carattere in partenza, qualche valore di prestazione, una frase di presentazione. Esempi di tipi, solo per dare l'idea:

| Rivale (esempio) | Carattere | Punto forte | Debolezza |
| --- | --- | --- | --- |
| Rossa | Partenzista | Stringe la linea, parte in testa | Errori ai giri di boa |
| Verde | Regolare | Pochi errori, mai fuori giri | Mai brillante |
| Blu | Bolinista | Veloce di bolina | Lenta in poppa |
| Gialla | Vento forte | Va bene nelle raffiche | Perde con vento leggero |
| Arancio | Rischiosa | Sceglie il bordo estremo, a volte vince | A volte crolla |
| Viola | Veterana | Virate rapide, poche penalità | Partenza lenta |

Regole di sorteggio possibili:

- Si pesca solo dalla fascia del torneo (sezione 6).
- Mai tre rivali dello stesso carattere, altrimenti il torneo è monotono.
- Se c'è un rivale ricorrente, ricompare almeno uno di quelli già incontrati.
- Il sorteggio si registra col seme, così una regata si può ripetere uguale.

**[aperto]** I tre rivali restano gli stessi per le 4 regate del torneo (si impara a conoscerli) o cambiano ogni volta?
**[aperto]** Il giocatore vede i rivali prima del sorteggio (sceglie il torneo anche per chi c'è) o li scopre alla partenza?

## 4. Caratteristiche dei rivali

Due gruppi: valori da cambiare nell'IA attuale e capacità nuove. **[da verificare]** nel codice quali parametri esistono già.

| Caratteristica | Cosa cambia in acqua | Richiede |
| --- | --- | --- |
| Partenza (prudente, aggressiva) | Quanto stringe la linea e quando parte | Esiste (0.17) |
| Velocità di bolina o di poppa | Moltiplicatore sulla velocità della barca | Solo un valore |
| Virata | Rapidità e velocità persa | Solo un valore |
| Costanza | Quanto spesso sbaglia (virata mancata, giro di boa largo) | Valore e casualità col seme |
| Tendenza all'errore grave | Strambata con vela aperta, scuffia in raffica | Voce 23 di `DA-FARE.md` |
| Bordo preferito | Da che lato risale per primo | Regola semplice |
| Vento leggero o forte | Va meglio o peggio secondo i nodi | Valore legato al vento |
| Rischio al giro di boa | Quanto si avvicina alla boa e agli altri | Valore |
| Leggere le raffiche | Va dove entra il vento | Campo di vento esteso |
| Coprire e uscire da una copertura | Toglie vento a chi è sottovento, o sa liberarsi | Cono d'ombra (c'è dalla 1.2.25) e un'IA che reagisca |
| Scegliere le mosse in partenza | Cerca la posizione, non solo aspetta | Modello nuovo (`ROADMAP.md`, F30) |
| Marcare il giocatore | Reagisce a come navighi | IA che osserva gli altri |

Tre principi per scegliere i tratti, **[proposta]**:

1. Un tratto entra solo se si può misurare giocando, come le prove da 90 partenze della 0.17.
2. Il giocatore deve poterlo capire: se non si vede, sembra casualità.
3. Un rivale debole non deve sbagliare in modo irreale: la debolezza ha una causa nautica (virata lenta, poppa scarsa), non un'ingenuità gratuita.

**[aperto]** I tratti sono scritti sulla scheda fin dall'inizio o si scoprono osservando il rivale e valgono come punti di Conoscenza?

## 5. Sponsor come passaggio di livello

**[proposta]** Lo sponsor è un ingaggio, non un'economia: offre una barca e una fascia di tornei in cambio di obiettivi. Il dilemma è quello descritto da Ale: accettare subito uno sponsor modesto (barca più lenta, obiettivi ragionevoli) o restare nel livello, fare altre regate e aspettare un'offerta migliore (barca più veloce, obiettivi più alti).

| Sponsor (inventato) | Barca | Fascia di tornei | Obiettivo |
| --- | --- | --- | --- |
| Modesto | Vele e scafo meno curati | Bassa | Podio nel torneo |
| Medio | Barca standard del livello | Media | Una regata pulita e un podio |
| Ambizioso | Barca al meglio | Alta | Vincere il torneo |

**Il punto debole del dilemma.** Se aspettare non costa nulla, conviene sempre aspettare e la scelta sparisce. Costi possibili, da combinare **[proposta]**:

- Le offerte scadono dopo qualche torneo.
- Un rivale può prendersi lo sponsor prima del giocatore (sezione 6).
- Senza sponsor non c'è la barca del livello successivo: si resta dove si è.

**Barca più lenta.** In un torneo dove gli altri hanno la barca normale, la barca più lenta è una sconfitta annunciata. **[proposta]** Lo sponsor modesto iscrive a tornei di fascia bassa con avversari adatti, e la differenza di barca resta piccola (stato di vele e scafo), con la stessa fisica di base.

**Obiettivi.** Tipi possibili: piazzamento, regata senza errori con colpa, tempo sul percorso, niente penalità. Gli sponsor possono avere gusti diversi (uno premia la pulizia, uno solo la vittoria), così la scelta dipende dallo stile. **[da verificare]** I numeri vanno tarati giocando, come i punti della regata.

**Se si fallisce.** Opzioni: avvertimento e un torneo di proroga; perdita della barca e ritorno alla fascia precedente; i meriti e il brevetto restano sempre del giocatore.

**Rapporto con meriti ed esame.** Lo sponsor guarda l'area competizione; l'esame resta obbligatorio per il brevetto. Nel gioco libero lo sponsor non esiste e tutte le barche sono disponibili.

**[aperto]** Il contratto dura un torneo o più?
**[aperto]** Un minimo di economia (iscrizioni, costi) o nessun denaro? La seconda scelta tiene il gioco più semplice.
**[aperto]** Il livello si sblocca con i traguardi e lo sponsor dà la barca, o basta lo sponsor? Se bastasse lo sponsor, i traguardi perdono peso.

## 6. Rivali con le stesse dinamiche

**[proposta]** I rivali vivono nello stesso sistema del giocatore, ma a numeri: in acqua se ne vedono tre, ma tutto il pool ha una fascia, una forma e uno sponsor, e si muove anche quando non si gioca contro di lui.

Stato di un rivale (poche righe salvate nel browser):

- fascia attuale e forma recente;
- sponsor (sì o no);
- storico contro il giocatore: incontri, risultati, contatti con colpa di uno o dell'altro, ultima regata.

**Esiti dei tornei non giocati.** Modello di forza più un po' di rumore, dello stesso tipo di quello dell'app F1 (Plackett-Luce). Costa poco e non serve simulare la regata in acqua.

**Salita e discesa.** A fine stagione (ogni N tornei, da tarare) i migliori salgono di fascia e i peggiori scendono; uno sponsor può ingaggiare un rivale o mollarlo, come col giocatore. Un rivale che sale sparisce dal livello del giocatore e si ritrova solo salendo; uno sponsor preso da lui non è più disponibile.

**Memoria.** Ogni rivale ricorda cosa è successo. Cosa se ne fa il gioco: solo lo storico mostrato sulla scheda, oppure anche un piccolo cambio di comportamento (più cauto o più duro con chi lo ha toccato). Nel secondo caso il cambio deve vedersi e spiegarsi sulla scheda, altrimenti sembra ingiusto o casuale.

**Salvataggi.** Come per record e fantasmi (7 ottobre 2026), lo storico dei rivali è materiale di gioco: si può azzerare quando cambiano le regole, senza migrazioni.

**[aperto]** Memoria solo mostrata o anche attiva sul comportamento?
**[aperto]** Un rivale «nemesi» che il gioco designa dopo qualche scontro e che ricompare più spesso?
**[aperto]** I rivali sono tutti scritti da Ale (con una breve storia) o in parte generati?

## 7. Quanti rivali

Di tre non si è obbligati a restare, ma il tetto sensato è di circa 7 barche in acqua; oltre, i rivali devono essere virtuali. I limiti sono nell'impianto attuale e nella leggibilità, non nella potenza del computer (**[da verificare]**: le prestazioni con più barche non sono state misurate).

Cosa blocca oggi:

- Gli aspetti grafici delle barche sono tre (`FLEET_LOOK`).
- I punti della regata (4/3/2/1, più 1 se pulita) sono scritti per quattro barche; il codice stesso annota che vanno rivisti se la flotta cambia.
- La linea di partenza è di 70 m (`LINE_HALF` 35) e le barche devono stare ad almeno 20 m l'una dall'altra (`START_GAP`): oltre 4-5 barche servono una linea più lunga o più file.
- A 1360x768 più di 6-7 barche non si seguono.
- Con più barche gli ingorghi ai giri di boa aumentano; le regole di precedenza dell'1b non sono state provate con più di 4 barche.

Scaglioni proposti, **[proposta]**:

| Livello | Barche in acqua | Condizione |
| --- | --- | --- |
| 1 | 4 (3 rivali) | Com'è oggi |
| 2 | 5-6 | Dopo il regolamento completo del livello 2 |
| 3 e oltre | Fino a 7 | Dopo i punti rifatti (la copertura del vento c'è già) |
| Qualunque | Pool intero | Rivali virtuali, solo a numeri |

Più barche non significa più divertimento: tre rivali ben distinti valgono più di sei quasi uguali. Il pool grande serve alla varietà tra tornei, non alla folla in acqua.

**[aperto]** Una flotta numerosa (6-7 barche) come evento speciale, o sempre 4-6?
**[aperto]** Rivedere i punti della regata perché valgano per qualunque numero di barche, prima di aggiungerne?

## 8. Limiti e vincoli

- **Tutto sempre giocabile.** Sponsor, ingaggi e rivali che salgono e scendono vivono solo nella carriera. Nel gioco libero tutto resta sbloccato e il pool è a disposizione.
- **Confini legali prudenti.** Sponsor, rivali e squadre sono inventati, con nomi generici: niente marchi, classi, costruttori o velisti reali.
- **Solo computer.** Schede e informazioni pensate per 1360x768.
- **Ogni modifica va collaudata guidando davvero la barca.** Ogni tratto di un rivale, ogni soglia di sponsor e ogni scaglione di flotta va misurato giocando, come le 90 partenze della 0.17. Più tratti, più collaudi: è il costo vero di un pool grande.
- **Il gioco racconta cosa fa e cosa no.** Ogni semplificazione (il ritiro di uno sponsor, la forma dei rivali fuori acqua) va scritta nel manuale per Lucio.
- **Novità per livello.** Nessuna regola rigida sul numero; ma sponsor e pool sono due novità grandi, e conviene non metterle nello stesso livello insieme al regolamento completo.

**[aperto]** In quale livello entra il primo sponsor? Se al livello 2, ci sono già barca nuova e regolamento come novità.

## 9. Altre idee

Tutte **[proposta]**, da scartare senza problemi.

1. **Scheda che si compila osservando.** Di un rivale nuovo si sa poco; dopo qualche regata la scheda si riempie. Dà punti di Conoscenza.
2. **Briefing prima della regata.** Chi c'è, che vento è previsto, quale lato favorisce chi: informazioni da elaborare.
3. **Campi e meteo con specialisti.** Un campo con vento leggero favorisce certi rivali, uno rafficato altri.
4. **Il coach parla dei rivali.** Il commento di fine regata dice cosa ha fatto bene chi ha battuto il giocatore. Si collega a `PROPOSTA-REGATA-COME-FONTE.md`.
5. **Tornei a invito.** Un torneo speciale si apre solo con un rivale ricorrente o certi meriti.
6. **Rivali che crescono tra una stagione e l'altra.**
7. **Compagni di squadra.** Dai livelli con più ruoli, uno dei rivali può diventare compagno in un torneo; si lega al gioco a più persone e ai formati già considerati (match race, due contro due).

**[aperto]** Quali ti attirano e quali sono rumore? Anche un «nessuna» aiuta a tarare il resto.

## 10. Domande aperte per Ale

**Rivali e pool**

1. I tre rivali restano gli stessi per le 4 regate del torneo o cambiano ogni volta?
2. Si vedono prima del sorteggio, scegliendo il torneo anche per chi c'è, o si scoprono alla partenza?
3. I tratti sono sulla scheda fin dall'inizio o si scoprono osservando?
4. I rivali sono tutti scritti da Ale, con una breve storia, o in parte generati?

**Sponsor**

5. Il contratto dura un torneo o più?
6. Un minimo di economia (iscrizioni, costi) o nessun denaro?
7. Il livello si sblocca con i traguardi e lo sponsor dà la barca, oppure basta lo sponsor?
8. In quale livello entra il primo sponsor?

**Memoria e rivalità**

9. La memoria dei rivali è solo mostrata sulla scheda o cambia anche il comportamento?
10. Un rivale «nemesi» designato dal gioco?

**Flotta e idee**

11. Una flotta numerosa come evento speciale, o sempre 4-6?
12. Rivedere i punti della regata per qualunque numero di barche, prima di aggiungerne?
13. Quali delle sette idee della sezione 9 attirano?

**Da dove cominciare, [proposta].** La scheda del rivale e i tratti realizzabili subito (sezioni 3 e 4, già vicini alla voce 23) non toccano la fisica e si collaudano come le partenze della 0.17. Sponsor e rivali che salgono e scendono conviene discuterli dopo, quando torneo e meriti saranno più stabili.
