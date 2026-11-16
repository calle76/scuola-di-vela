# Proposta: file della stagione con un amico che valgono fra versioni, e «Riprendi dal mio file»

*16 novembre 2026, fermata 1. Niente è cambiato nel gioco: aspetta il via di Ale e la scelta D1.*

## Da dove viene

Il 16 novembre Ale ha trovato in Chrome la stagione con un amico ricominciata alla tappa 1 (era alla tappa 3, sulla 1.3.12), con tutti i progressi di Deriva vuoti. Il codice non c'entra: dalla 1.2.36 nessuna versione cancella `progress.stagione`, e la chiave del salvataggio non dipende dalla versione. È stato il browser (dati del sito cancellati, oppure un altro browser). Restano però due problemi veri:

1. **Il file dell'amico vale solo nella stessa versione.** `stCarica` rifiuta un file con `ver` diversa da `VERSIONE` (`js/regate.js`, «aggiornate il gioco tutti e due»). Se un amico salva una tappa sulla 1.3.15 e l'altro la carica sulla 1.3.16, il file viene rifiutato. È lo stesso fastidio che la 1.3.14 ha tolto al torneo.
2. **Se il browser perde i dati, la stagione è persa** anche quando il proprio file c'è ancora: il gioco accetta solo il file dell'amico.

## Cosa propongo (il modello più semplice)

**A. Al posto della versione del gioco, la «forma della stagione».** Una costante `ST_FORMA = 1`, scritta in ogni file (i file vecchi, che non ce l'hanno, valgono 1). Dalla 1.2.37 il modo in cui il codice diventa tappe, batterie, venti e rivali non è cambiato: l'ho controllato con `git diff v1.2.37 HEAD`, e nel frattempo sono cambiati solo i parametri del nazionale, che con un amico non si usa. Quindi tutti i file dalla 1.2.37 in poi valgono uguale. Il file si rifiuta solo se:
- la forma è diversa («la stagione con un amico è cambiata con la versione X: ricominciate con un codice nuovo»);
- il codice è diverso, o gli arrivi non tornano con la batteria. Questi due controlli ci sono già.

Chi in futuro cambia `stNuova` con il codice deve alzare `ST_FORMA`: lo scrivo in un commento accanto alla costante.

**B. «Riprendi dal mio file»**, nella finestra «Stagione con un amico» (accanto a «Crea un codice» e «Ho un codice»). Funziona così:
- legge il proprio file;
- rifà la stagione dal codice e dal ruolo (A o B) scritti dentro;
- rimette i propri arrivi tappa per tappa.

Dopo si carica il file dell'amico come sempre.
- C'è solo quando non c'è una stagione in corso (come «Con un amico»): non sovrascrive niente.
- Rifiuta: il file di un'altra cosa, la forma diversa, gli arrivi che non tornano con la batteria, e il file con tutte e 4 le tappe (stagione già finita: non c'è niente da continuare).
- **Cosa non torna** (detto a chi riprende, in una riga): il torneo della tappa a metà (si rifà la tappa), e i contatti con i rivali, che servono solo alla frase «ti sei toccato con…».
- **Ritiri.** Una tappa lasciata nel file sembra un ultimo posto. Da questa versione il file scrive anche le tappe lasciate (`rit`). Una stagione ripresa da un file vecchio, senza quel dato, non conta come «senza ritiri»: in carriera non può dare «Deriva superata per merito».

## Una scelta per Ale

**D1. «Riprendi dal mio file» anche in carriera?**
- *Consiglio: sì.* La stagione con un amico c'è anche in carriera, e perdere i dati è lo stesso fastidio.
- Il rischio: chi modifica a mano il file può darsi posti migliori, e in carriera quei posti valgono punti di Deriva. Oggi questa strada non c'è.
- L'alternativa: solo nel gioco libero.

## Criteri (soglie nostre, dichiarate prima di misurare)

- **F1, file fra versioni:** un file della stessa stagione con `ver` "1.3.12" e senza `forma` entra. La classifica che ne esce è identica, per posti e punti dei 12, a quella dello stesso file con la versione di oggi. 10 codici fissi × 2 ruoli = 20 casi, 20 su 20.
- **F2, rifiuti che restano:** sono rifiutati, ciascuno col suo messaggio:
  - il codice diverso;
  - l'arrivo che non torna con la batteria;
  - il proprio file in «Carica quello dell'amico»;
  - la `forma` 2.

  4 casi su 4. Il collaudo controlla anche che i casi siano stati provati davvero.
- **F3, ripresa:**
  - si gioca una stagione con un amico fino alla tappa 2 o 3, con risultati scritti dal collaudo passando dalle funzioni del gioco (`stChiudiTappa`) e con il pilota in una stagione su cinque;
  - poi si salva il file, si azzerano i progressi, si riprende e si carica il file dell'amico;
  - la classifica del circuito (posti e punti dei 12) e la tappa successiva (posto, vento, rivali della batteria) devono essere identiche a quelle di prima;
  - casi: 10 codici fissi × 2 ruoli, con semi diversi da quelli di F1. Soglia 20 su 20.
- **F4, quando non si può:** il pulsante manca con una stagione in corso; il file con 4 tappe viene rifiutato; una stagione ripresa da un file senza `rit` ha `ritiri` falso. 3 casi su 3.
- **F5, pannello:** la finestra «Stagione con un amico» col pulsante nuovo a 1360x650, 0 px di eccesso in Chromium e Firefox.
- **Non-regressione:** `polare.js` e `raffiche_e_virate.js` identici; `collaudo_stagione.py` e `collaudo_stagione_amico.py` verdi. Il caso «altra versione» di `collaudo_stagione_amico.py` oggi si aspetta il rifiuto e diventa «altra versione, entra», più il caso «altra forma, rifiutato».

## Costanti nuove

`ST_FORMA = 1`: un'etichetta, non un'ipotesi fisica. Nessun numero da tarare.

## Rischi

- Se una versione futura cambia la stagione col codice e si dimentica di alzare `ST_FORMA`, i due amici vedrebbero classifiche diverse senza avviso. Lo riduce il commento accanto alla costante; un controllo sicuro richiederebbe di mettere nel file anche le batterie, e si può fare se Ale preferisce.
- Con la ripresa da file vecchio si perdono le frasi sui contatti e il «senza ritiri»: dichiarato nella finestra.

## Versione

1.3.16, solo `js/regate.js` (più il `CHANGELOG.md` e `VERSIONE`). Si tocca `tests/collaudo_stagione_amico.py`. Collaudi da lanciare: quelli qui sopra; il resto col giro di Ale.
