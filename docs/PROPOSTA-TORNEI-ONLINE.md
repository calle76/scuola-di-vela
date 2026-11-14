# Proposta: tornei fra Ale e Lucio (fermata 1)

14 novembre 2026, pomeriggio. Ale: «metto anche l'idea del gioco online almeno per me con Lucio in tornei dedicati» (`DA-FARE.md` voce 36). Il 18 ottobre si erano già scritti quattro gradini del gioco a più persone (`PROPOSTA-REGATA-COME-FONTE.md` §8). Qui si sceglie da quale partire per i **tornei** di Deriva. In `js/` non è stato scritto niente.

## Il punto

I gradini del §8 vanno dalla sfida a distanza al due contro due online. Per un **torneo fra due amici** non serve per forza essere in acqua nello stesso momento: nella vela vera molte classifiche sommano regate corse in giorni diversi. Il tempo reale è il gradino più caro: rete, «padrone di casa», reti che non si collegano.

## Modello più semplice: il torneo per corrispondenza

1. **Un codice del torneo.** Ale crea un torneo «con un amico» e il gioco dà un codice corto, per esempio `DERIVA-7K2M`. Il codice contiene il seme: vento, campo, rivali e tratti sono uguali per chi lo usa. Lucio scrive lo stesso codice e ha lo stesso torneo.
2. **Ognuno corre quando vuole**, contro gli stessi 3 rivali del computer. Le regate sono le stesse 4, con lo stesso vento.
3. **Fine regata: un file piccolo** col tempo, la posizione e la registrazione della barca. Il registratore esiste già dalla 0.18 e registra tutte le barche dalla 1.0.52. Ci si scambia il file come si vuole: messaggio o posta. Nessun server del progetto, nessun dato personale salvato fuori.
4. **Caricando il file dell'altro:**
   - la sua barca compare come **fantasma** nella stessa regata, come oggi il fantasma del tuo record, così la si rivede in moviola accanto alla propria;
   - la classifica del torneo mette insieme te, lui e i 3 rivali.
5. **Il limite, da dire chiaro:** il fantasma non reagisce. Niente contatti né precedenze con l'amico: si sfida il suo tempo e la sua rotta, non la sua barca in acqua. È il gradino 1 del §8.

## Perché questo prima del tempo reale

- **Costa poco:** semi fissi, registratore e fantasma ci sono già. Serve solo il codice, il file e la classifica a due.
- **Funziona su qualunque rete e con orari diversi.**
- **La partita è giusta:** stesso vento, stessi rivali, stesse raffiche.
- **Prepara il tempo reale:** se un giorno si farà il gradino 3, il codice e la classifica servono uguali.

## Criteri, con soglie fissate prima di provare

| # | Criterio | Soglia |
| --- | --- | --- |
| O1 | Stesso codice, stesso torneo | due pagine diverse (anche Chromium contro Firefox) con lo stesso codice: rivali, tratti, campo e vento identici in 20 codici su 20 |
| O2 | Il fantasma dell'amico è fedele | la sua barca rivista dal file passa a meno di 0,5 m dalla traccia registrata in ogni istante, in 10 regate |
| O3 | Il file non si falsifica per sbaglio | un file di un altro torneo o di un'altra versione viene rifiutato con un messaggio chiaro, mai caricato a metà |
| O4 | Le regate non cambiano | impronta del guardiano identica, `polare.js` e `raffiche_e_virate.js` identici |
| O5 | Niente fuori dal browser | nessuna connessione di rete aperta dal gioco (controllata dal collaudo) |

O1 è il punto più delicato: il §8 diceva che due browser diversi non garantiscono gli stessi risultati al bit. Qui però non serve che le due regate siano identiche al bit. Bastano lo stesso vento e gli stessi rivali di partenza: i rivali poi reagiscono alla barca di ciascuno, che è diversa.

## Rischi

- **Barare:** chi corre per secondo conosce già il tempo dell'altro. Fra amici va bene, ma lo si dice.
- **Gli stessi rivali reagiscono in modo diverso** alle due barche: la classifica dei rivali non è una sola. Proposta: per la classifica a due conta la **tua** posizione fra te, l'amico e i rivali della **tua** regata, e il confronto diretto si fa sul tempo.
- **Versioni diverse del gioco:** se Ale e Lucio non hanno la stessa versione, il torneo non è uguale. Il codice contiene la versione e il gioco la controlla (O3).

## Cosa serve da Ale

1. Il via, oppure dire se preferisce puntare subito al tempo reale (gradino 3, molto più caro).
2. Dove sta nella carriera:
   - solo come modo a parte, «Torneo con un amico»;
   - oppure anche come tappa della stagione zonale (`PROPOSTA-STAGIONE-ZONALE.md`).
