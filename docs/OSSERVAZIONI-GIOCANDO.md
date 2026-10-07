# Osservazioni giocando

Diario delle prove di gioco, con la data. Non sono verifiche nautiche: sono le impressioni di chi gioca, e dicono cosa si è visto e cosa ne facciamo. Le voci si aggiungono in fondo.

## 5 ottobre 2026: prototipo del fiocco (`sperimentale/fiocco.html`), vento 10 nodi

| # | Cosa si è visto | Cosa ne facciamo |
| --- | --- | --- |
| 1 | Al traverso e al lasco la posizione giusta del fiocco si trova, e il pannello dà l'indicazione (lascare o cazzare) | Il giudizio di chi gioca sulla tappa C1 è arrivato: positivo |
| 2 | Al gran lasco il pannello dice «regolazione stretta» oppure «non si può regolare». Non è chiaro cosa significhi «regolazione stretta» | «Stretta» vuol dire che la finestra utile è meno di 10°. Quando il fiocco entra nel gioco il messaggio va riscritto in modo più chiaro, per esempio «Fiocco: si regola solo fra X° e Y°». Il prototipo non si cambia |
| 3 | Da 120° a 140° di vento reale non si sente nessuno strappo nella velocità | Chiude il dubbio sul «ginocchio» (voce in `DUBBI-E-RICERCHE.md` e `CONTENUTI-DA-VERIFICARE.md`): giudicato giocando, non si nota |
| 4 | Virata di bolina partendo da circa 4 nodi: col fiocco cazzato la velocità minima scende a 0,6 nodi e la barca rischia di piantarsi; col fiocco tutto lascato scende a 1,2 nodi | Registrato. Non è un difetto accertato: è coerente con l'idea che in virata il fiocco si lasca. Da usare per la lezione 2.3 e da far giudicare a un velista. Il prototipo non si cambia |
| 5 | La disposizione dei cursori nel pannello (timone, randa, fiocco) confonde | Metterli come sulla barca vista dall'alto con la prua in su: **fiocco in alto, randa nel mezzo, timone in basso**. Da fare quando il fiocco entra nel gioco (pannello di `index.html`), controllando che stia in 1360×650 |

## 5 ottobre 2026: gioco vero (`index.html`)

| # | Cosa si è visto | Cosa ne facciamo |
| --- | --- | --- |
| 6 | Il messaggio «Raffica in arrivo: preparati a lascare» (riga circa 1896 di `index.html`, mostrato in rosso come avviso, quando la raffica davanti è più forte del 20% del vento locale) non è sempre vero: lascare non è sempre necessario, e se si vuole andare più veloci la raffica si cerca. Va bene per la sicurezza ma a volte è eccessivo; dipende dalla raffica | Rendere il messaggio dipendente dalla situazione, per esempio «Raffica in arrivo: se la barca sbanda troppo, lascia; altrimenti è un'occasione per andare più veloci». Aggiungere la domanda al velista («in una raffica si lascia sempre?»). Da fare in una versione futura del gioco |

## 6 ottobre 2026: gioco vero

| # | Cosa si è visto | Cosa ne facciamo |
| --- | --- | --- |
| 7 | Nel ripasso, con un solo errore il messaggio dice «Quasi tutto giusto: rileggi la spiegazione della domanda sbagliata», ma non è chiaro dove sia la spiegazione; e «Ripeti il ripasso» rifà tutte le domande | A fine ripasso un elenco delle domande sbagliate con la risposta giusta e la spiegazione, e un pulsante «Ripassa solo le sbagliate», in una versione futura |
| 8 | Con molti errori il ripasso dice «Conviene rifare la lezione, o almeno i passi sugli argomenti sbagliati», senza dire quali | Stessa soluzione della riga sopra: l'elenco delle domande sbagliate dice anche a quali argomenti appartengono |
| 9 | Lezione 1, pulsanti Cazza e Lasca: la vela tornava al centro e la scritta di passo completato spariva | Risolto nella 0.18.1 |
| 10 | Pannello fuori da 1360x650 sul PC dell'utente con i caratteri veri | Risolto nella 0.18.2 |

## 7 ottobre 2026: gioco vero

| # | Cosa si è visto | Cosa ne facciamo |
| --- | --- | --- |
| 11 | Prova 2, dalla registrazione dell'utente: strambata violenta non prevista, causata dall'essere finito dal lato sopravento della linea che porta alla boa | Il testo della prova ora dice cosa fare se strambare serve per forza (fatto in 0.18.4) |
| 12 | Orziera: il testo del pannello attribuiva la tendenza a salire da sola a onde e raffiche come unica causa | Testo del pannello più generico, glossario ampliato con tutte le cause (fatto in 0.18.4) |
| 13 | Idea: linea d'arrivo tra due boe al posto della boa nelle prove senza giro di boa | Fatto nella 0.19 (proposta e decisioni in `PROPOSTA-LINEA-E-VISTA.md`); nella 0.19.2 linea a scacchi e scritta «Arrivo» in una pillola leggibile |
| 14 | Idea: tasto per spostare la barca verso il margine dello schermo opposto alla boa, tenuto premuto, con ritorno al centro al rilascio; le raffiche restano visibili | Fatto nella 0.19.2: tasto Q tenuto premuto, nelle prove e nelle regate (proposta in `PROPOSTA-LINEA-E-VISTA.md`, parte B). Per il livello 4 col tattico resta da valutare una vista che mette in pausa il gioco |
| 15 | Filetto sopravento e vela che sbatte: controllo (senza modificare il motore) di quanto distano le due soglie. Nel disegno coincidono sempre (stesso stato `ttState()`, differenza 0°). Nella forza, la resistenza aggiunta parte 2° di incidenza dopo (soglia 6° invece di 8°): a bolina larga (65°) questo equivale a 3,76° di boma, al traverso (90°) a 4,34° di boma — sopra i 3° indicati. Al lasco (120°) nessuna delle due soglie si raggiunge mai, nemmeno a scotta tutta lascata (incidenza minima misurata ≈12°) | Nessuna modifica fatta. Proposta minima, da confermare con un velista: nel disegno, slegare la deformazione della vela (randa) dal medesimo stato del filetto e farla iniziare alla soglia della resistenza aggiunta già esistente nel motore (incidenza 6° invece di 8°), così il filetto si agita prima e la vela si vede sbattere qualche grado dopo, invece che insieme |
| 16 | Dal 7 ottobre sera: la vista spostata non bastava, l'arrivo era a 230 m e si vedevano 95 m; a zoom lontano il gioco rallentava per le increspature | Fatto nella 0.19.3: Q allontana anche l'inquadratura finché l'arrivo o la boa entrano nello schermo; zoom minimo da 0,4 a 0,1; increspature che sfumano e spariscono a zoom lontano (nessun rallentamento); raffiche sempre visibili come chiazze scure; segnalino della barca e distanza accanto alla freccia |
| 17 | Idea (7 ottobre): mostrare le raffiche come zone scure con una freccia e un numero (forza e salto di direzione). In barca vera si vede solo la chiazza scura; frecce e numeri sono informazione da strumenti | Ordine proposto: livello 1 solo chiazza; aiuto facoltativo (spento di default, non conta per i meriti) con freccia e «+x nodi», utile nella lezione 6; livello 3 strumenti vicino alla barca; livello 4 carta del tattico. Nessun codice per ora |
