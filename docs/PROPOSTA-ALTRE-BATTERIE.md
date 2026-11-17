# Proposta: far correre davvero le altre batterie del circuito

*Fermata 1, 17 novembre 2026. Voce 52 di `DA-FARE.md`.*

**ARCHIVIATA il 17 novembre 2026 (Ale): non si fa.** «Non complichiamo e appesantiamo il gioco se non serve davvero. Se la classifica va bene com'è la teniamo, se c'è qualcosa da migliorare si fa.» La classifica a sorteggio resta. Numeri che l'hanno sostenuta: l'ordine dentro la tua batteria è sempre quello vero; la fortuna sposta il tuo posto di tappa di circa ±2 (deviazione standard 1,7-2,0 sui 4 posti), quindi circa ±4 punti su una stagione di 4 tappe; la forza dei rivali conta (media a fine stagione 19,6 punti con due doti, 28,3 con due difetti, `PROPOSTA-STAGIONE-ZONALE.md` Z1). Si riapre solo se una classifica sembra sbagliata in una stagione vera.

## Da dove viene

Ale, 17 novembre: «non simuli le regate avversarie [...] vorrei far correre davvero gli altri». Oggi (`js/regate.js`, `stEstrai`, `stRiempi`) le altre batterie non corrono: per ogni tappa si estrae a caso un ordine dei 12 (pesi quasi uguali, `ST_B` = 0,2) e ai 4 posti usciti per la tua batteria si mette il tuo ordine vero. Il «racconto» («nella blu ha vinto Fontana») è quindi inventato. Osservazione 133.

## Modello più semplice

1. **Dopo la tua ultima regata della tappa**, il gioco fa correre le altre batterie con lo stesso motore e le stesse regole del torneo: stesse 4 regate, stessi 4 venti della tappa, 4 barche (nel nazionale, una batteria da 6) tutte guidate dal gioco, ognuna coi suoi tratti (doti e difetti dei rivali). Nessun giocatore.
2. **Ogni batteria ha la sua serie** con lo stesso conto del torneo (`torSerie`: punti = posto, somma di 4 regate).
3. **Come si mettono insieme le batterie** (come nelle flotte separate, F103 *[da verificare sul testo intero]*): si ordinano tutti i 12 per punti di serie (meno è meglio); a parità, per miglior regata e poi per tempo totale. I punti di tappa sono il posto in questo ordine. Somma sempre 78.
4. Non c'è più estrazione. `ST_B` e i pesi spariscono (restano solo per le tappe già fatte nelle stagioni salvate).

## Cosa costa (misurato oggi, PC di Ale, Chromium, 3 regate di prova)

- Una regata a 4 senza interfaccia: **3-4 s di calcolo** (212 s di regata, 3 prove: 3,7 / 3,2 / 2,9 s; dalle 4 barche arrivano tutte).
- Una tappa zonale = 2 batterie × 4 regate = **8 regate, circa 30 s**. Nazionale: 1 batteria × 4 regate da 6 barche, circa 20-25 s (stima, non misurata). Firefox più lento e il PC si scalda: da misurare col freno termico.
- Il calcolo gira a pezzi, senza bloccare lo schermo, con una barra («Si corrono le altre batterie…»).

## Cosa può andare storto

- **Il motore oggi ha sempre un giocatore** (`R.boats[0]`, tratti, registratore, suoni, rotta ottimale). Una regata di soli rivali è la parte più grossa del lavoro: prima si prova col trucco già usato dai collaudi (la barca del giocatore guidata dalla guida dei rivali, `__sv.pilota`), poi si decide se serve un modo «senza giocatore».
- **I rivali regatano così così** (voci 1b, 2, 3, 4 di `DA-FARE.md`: virate in più alla boa, barche che si tengono, ballo di arrivo). Tutto quello che non va ora nella loro guida comparirà nelle classifiche: la forza dei tratti potrebbe contare meno di oggi.
- **Con un amico** le due pagine non danno per forza lo stesso risultato (due browser, due arrotondamenti, regate caotiche). Oggi tutto esce da un codice e si ricalcola uguale; con le regate vere no. Proposta: ognuno salva nel suo file l'ordine delle altre batterie come l'ha calcolato lui (le batterie di Ale e di Lucio restano vere); la batteria «degli altri» può differire fra le due classifiche, e il gioco lo dice. Si alza `ST_FORMA` a 2: i file vecchi vengono rifiutati con un messaggio chiaro.
- **Carriera:** «Deriva superata» (primi 3 dello zonale) e i contratti dello sponsor dipendono dai punti: vanno rimisurati (probabilità che il pilota «da giocatore» sia nei primi 3, prima e dopo).
- **Il tempo:** ~30 s di attesa a fine tappa. Se a Ale pesa, la scelta è calcolare mentre si guarda la classifica.

## Criteri (soglie nostre, dichiarate prima; semi di scelta 1-20, conferma 101-120)

| # | Criterio | Soglia |
| --- | --- | --- |
| B1 | Conti | 12 posti per tappa, somma 78 (zonale e nazionale), 40 tappe su 40 |
| B2 | Le batterie finiscono | almeno il 95% delle regate delle altre batterie con tutte le barche arrivate |
| B3 | La tua regata non cambia | tua batteria identica al bit con e senza le altre batterie, stesso seme, 20 su 20 |
| B4 | La forza conta, ma non decide | su 200 stagioni: punti medi dei rivali con due doti minori di quelli con due difetti di almeno 4 punti; ogni rivale vince almeno 1 stagione su 200; nessuno ne vince più di 35% |
| B5 | Tempo | zonale al massimo 40 s su PC di Ale in Chromium, 60 s in Firefox; schermo che non si blocca *[soglia sul blocco da fissare dopo la prima misura: oggi non ho un numero]* |
| B6 | Amico | file scambiati: la tua classifica coerente col file dell'amico, 20 su 20 (come Z9); file di forma vecchia rifiutati |
| B7 | Salvataggio | chiusura della pagina a metà calcolo: tappa non scritta a metà, si ricalcola alla riapertura |
| B8 | Carriera | probabilità del pilota «da giocatore» di essere nei primi 3 dello zonale riportata, prima e dopo (numero, non soglia) |

## Versione semplice (Ale, 17 nov: «semplifichiamo, ma teniamo più coerenza possibile»)

Le quattro domande sono chiuse con la scelta più semplice che resta coerente con le regate vere; Ale può correggerle:

1. **Batterie unite per punti di serie** (punto 3 sopra): stesso conto del torneo per tutti, nessuna regola nuova.
2. **Calcolo subito a fine tappa, con una barra di attesa** (circa 30 s): niente sottofondo, niente stato a metà (B7 si riduce a «chiusa la pagina, si rifà»).
3. **Con l'amico, ognuno la sua batteria «degli altri»**, dichiarato in una riga nel gioco; le batterie di Ale e di Lucio restano vere nelle due classifiche.
4. **Guida dei rivali com'è oggi**, senza aspettare le voci 2-4: i loro difetti si vedranno nelle classifiche e serviranno a misurarli.

Coerenza tenuta: stesso motore, stessi venti, stesse regole, stessi tratti dei rivali, stesso conto dei punti. Tolto: sorteggio, `ST_B`, sottofondo, accordo fra le due pagine sulla batteria degli altri.

## Passi

1. (Dopo il via) provare una regata di soli rivali col trucco del pilota, misurare tempo e arrivi (B2, B5).
2. Scrivere la fusione e le nuove classifiche, tenere le vecchie per le tappe già fatte.
3. Rimisurare B1-B8, poi file con l'amico e carriera.
4. Versione nuova con lezione/testo che spieghi in due righe come si formano i punti.
