# Proposta: distacchi più immediati nella classifica del pannello

27 ottobre 2026, fermata 1. **Nessun codice toccato.** Nata dal punto 7 del check di Ale sulla 1.0.47: «i secondi accanto alle barche sono utili e chiari, ma forse potrebbero essere più immediati». La parte sulle penalità («+30» = due da 15) è già fatta nella 1.0.51.

## 1. Com'è oggi

Una riga per barca, in ordine di classifica (`racePanel`, `js/regate.js`), per esempio `Rossa · di bolina · 2 penalità (+30 s) · −12 s`. Il numero finale (`distacco`, 1.0.33) è «quanti secondi fa quella barca era alla tua altezza», con il segno: positivo se è davanti a te, negativo se è dietro. Sulla riga del giocatore non c'è. Dopo il suo arrivo diventano le differenze dei tempi d'arrivo. Le penalità **non** sono contate in quel numero (strada fatta senza penalità), ma la classifica sì.

## 2. Il problema

Il segno più o meno va interpretato: bisogna ricordare che «+» vuol dire davanti. È lo stesso difetto delle penalità di prima: un numero da decifrare.

## 3. Proposta (la più semplice)

Solo testo, nessuna fisica e nessuna costante nuova.

- **A. Parole al posto del segno.** `12 s avanti` / `12 s dietro` al posto di `+12 s` / `−12 s`. Il «a te» si capisce perché la riga del giocatore è evidenziata. Dopo l'arrivo restano le differenze dei tempi, già scritte in parole nel messaggio d'arrivo (`arrivoDistacchi`).
- **B. Meno di mezzo secondo o nessun distacco misurabile:** niente numero, come oggi (`distacco` torna `null`).
- **C. Non cambio** l'ordine, il calcolo, i colori e la riga del giocatore.

Alternativa scartata: una barra o un disegno dei distacchi. Più lavoro di disegno e il pannello a 1360×650 non ha spazio da buttare.

## 4. Criteri (soglie nostre, scritte prima)

| | Criterio | Soglia |
| --- | --- | --- |
| D1 | Il numero in parole coincide con il segno del `distacco` vero, in ogni riga e ogni secondo | 100% su 20 regate (semi 1-20) |
| D2 | Pannello a 1360×650, anche nel caso peggiore (tutte le penalità, nomi lunghi) | 0 px di eccesso |
| D3 | Nessuna riga che va a capo | 0 righe su 20 regate |
| D4 | Fisica e arrivi identici | `polare.js`, `raffiche_e_virate.js` identici; arrivi uguali al bit |

Il controllo D1 deve aver misurato davvero: stampa il numero di righe confrontate (non vale «nessun caso sbagliato» con zero casi).

## 5. Rischi

- La riga è già lunga con le penalità («2 penalità (+30 s)»). Se D2 o D3 falliscono, si accorcia in `davanti`/`dietro` senza «s» doppie o si va a capo per scelta: lo decide Ale guardando.
- Il distacco senza penalità può sembrare in contrasto con l'ordine (una barca «12 s dietro» ma davanti in classifica perché ha meno penalità?). Non cambia con questa proposta; se Ale lo trova confuso è un secondo passo.

## 6. Collaudi da lanciare

`collaudo_distacchi.py`, `collaudo_penalita_testo.py`, `collaudo_pannello.py` (1360×650), più i due controlli veloci di non-regressione.

**Versione:** 1.0.54, solo testo del pannello.

## 7. Fermata 2 (1.0.54, 27 ottobre 2026)

Fatto come in §3, con «avanti» al posto di «davanti» e «alla pari» per zero. D3 è fallito due volte (169 e 7 letture a capo): risolto accorciando la parola e «in poppa verso l'arrivo» in «verso l'arrivo». D1 3108 confronti tutti giusti. Dettagli in `CHANGELOG.md`.
