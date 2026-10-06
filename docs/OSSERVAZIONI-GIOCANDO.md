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
