# Proposta: il registratore di sessione registra tutte le barche (fermata 1)

26 ottobre 2026. Nasce dal check di Ale sulla 1.0.47 («si richiede registratore che registri tutte le imbarcazioni, non solo la mia»): quando una barca avversaria si pianta o esce dalla boa di partenza, nel file di sessione non c'è niente da leggere. Fermata 1: nessun codice scritto.

## Cosa serve a cosa

**Serve a capire cosa fanno gli avversari**, come strumento di diagnosi nelle sessioni di Ale: «la Blu si è piantata a 1:40» deve potersi ritrovare nel file, con posizione, velocità e a chi stava cedendo. **Non è il replay** (`PROPOSTA-REGATA-COME-FONTE.md`: istantanee complete, da proporre dopo i tornei, decisione del 20 ottobre). Le righe nuove sono solo testo da leggere, non servono a ripristinare niente.

## Modello più semplice

Il registratore (`js/registratore.js`, 175 righe) scrive già una riga `S` al secondo per la barca del giocatore, più eventi. Si aggiunge, per ogni altra barca della regata in corso (`R.boats`, dalla seconda in poi), con la stessa regola di prima: **solo lettura, nessuna chiamata a `Math.random`, nessuna scrittura nelle variabili del gioco**.

1. **Riga `B`, una al secondo per barca**, insieme alla `S` del giocatore: `B t nome x y prua nodi twa lato stato`, dove `lato` è il lato della regata (0 prima del via, 1 bolina, 2 poppa), e `stato` una sigla fra: `-` (nulla), `ocs` (partenza anticipata), `scuf` (scuffiata), `arr` (arrivata), `dnf` (non arrivata o ritirata), `via` (sta eseguendo la partenza), più `cede:Nome` se in quel secondo cede a un'altra barca (`b.cedeA`, dalla 1.0.49).
2. **Eventi `E` nuovi**, uno per volta e per barca: `Nome fermo` quando la barca resta sotto 0,5 nodi per 5 s di regata già partita (e `Nome riparte` quando torna sopra 1 nodo), `Nome lato N`, `Nome boa` (giro di boa), `Nome arrivo Ns`, `Nome ocs`, `Nome scuffia`, `Nome penalità +1` (da `pen` o `pp` che aumentano).
3. **Contatto fra due barche qualsiasi:** `E t contatto Nome1 Nome2` al primo passo in cui gli scafi si toccano (stessa funzione `hullOverlap` che usa il gioco, solo letta) e si registra una volta finché si staccano. Oggi i contatti del giocatore sono già negli eventi, quelli fra avversari no.
4. **Formato 2:** intestazione `formato 2`, legenda nuova per `B` e per gli eventi nuovi. `tests/analizza_sessione.py` legge ancora il formato 1 e, per il 2, aggiunge per ogni avversario: tempo fermo, contatti, penalità, quanto tempo ha passato a cedere.

Dimensione: tre avversari × 1 riga al secondo per una regata di 5 minuti sono 900 righe in più (circa 45 kB). Cresce con la durata: si misura (criterio G6).

## Criteri misurabili (soglie nostre, fissate prima di misurare)

| # | Criterio | Soglia |
|---|----------|--------|
| G1 | **Sola lettura.** 20 regate (semi 1-20: bastone 1a, salti di vento 1b, una del torneo) giocate dal pilota **con e senza** registrazione: posizioni, prue, velocità, tempi d'arrivo e penalità di tutte le barche identici | 0 differenze su 20 |
| G2 | **Le righe `B` dicono il vero.** Ogni secondo di ogni avversario, nelle stesse 20 regate: x, y, prua, nodi nella riga uguali ai valori veri della barca a quell'istante (arrotondati come la riga) | 0 differenze, e il numero di righe `B` = secondi di regata × avversari ±1 (se fosse zero il controllo non ha misurato: NON VALIDO) |
| G3 | **Contatti fra avversari.** Costruiti a mano: due avversari messi a 1 m, 10 casi → 1 evento ciascuno, nessun evento se si staccano a 5 m. In 20 regate vere: il numero di eventi `contatto` coincide con quello contato dal collaudo, passo per passo, con le sole posizioni delle barche (nessun contatto lasciato fuori) | 10 su 10; 0 differenze su 20 |
| G4 | **Barca ferma.** Costruiti: un avversario bloccato a velocità zero per 8 s → evento `fermo` dopo 5 s ±1 e `riparte` quando si sblocca, 10 casi; barche che navigano normalmente in una regata di prova → nessun `fermo` | 10 su 10; 0 falsi su 20 regate in cui nessuna barca è mai sotto 0,5 nodi per 5 s (verificato dal collaudo con le velocità vere) |
| G5 | **Il file si legge.** `analizza_sessione.py` legge il formato 2 e il formato 1 d'esempio; il riassunto che scrive il gioco coincide con quello che ricalcola l'analizzatore (eventi per barca, penalità) | 0 differenze, controllo sul file d'esempio già incluso e su 5 file nuovi |
| G6 | **Dimensione** (cambiata prima di misurare, su osservazione di Ale: le regate dei livelli successivi saranno più lunghe di 5 minuti) | al massimo 20 kB per minuto di regata con tre avversari (stima: 9 kB al minuto) |
| G7 | **Pagina vera**, senza `#collaudo`: registrazione accesa dall'interruttore, una regata, scarica il file, contiene righe `B` di tutti e tre | 3 avversari su 3 |
| G8 | **Non regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; `collaudo_registratore.py` (parti a, b, c…) come prima per le righe del giocatore; pannello a 1360×650 senza eccesso (la spia REG non cambia) | 0 differenze, 0 px |

G3 usa nel collaudo la funzione `hullOverlap` del gioco per decidere cosa è un contatto, perché è la definizione di contatto del gioco (1.0.42); lo dico perché il metro non è del tutto indipendente. Il controllo sul riepilogo (G5) e le posizioni costruite a mano lo compensano.

## Costanti nuove (tutte ipotesi nostre, nessuna fonte)

| Costante | Valore | Perché |
|----------|--------|--------|
| Barca «ferma» | sotto 0,5 nodi per 5 s dopo il via | Una barca in bolina stretta che sta per virare scende a 1-2 nodi; sotto 0,5 per 5 s è piantata, come i 36 casi della 1.0.48 |
| «Riparte» | sopra 1 nodo | Isteresi, per non riempire il file di ferma/riparte vicino alla soglia |
| Intervallo righe `B` | 1 s | Come la riga `S` del giocatore |

## Rischi

- **File più grande e più lungo da leggere:** per questo c'è il riassunto per barca di `analizza_sessione.py`.
- **Formato 2:** i file vecchi restano leggibili; chi ha script suoi sui file (nessuno, per quanto so) dovrebbe tenere conto della riga `B`.
- **Il registratore non conosce i motivi della guida**, solo ciò che si vede (posizione, a chi cede). Per spiegare *perché* una barca si pianta potrebbe servire un secondo passo con campi della guida (`goStart`, `waitX`, …), solo se il primo non basta.
- **Costo di calcolo:** un controllo di contatto per coppia a ogni passo, 6 coppie; è lo stesso lavoro che fa già `regate.js` (misurato in G1: nessuna differenza di risultato, e il tempo di un passo non peggiora oltre il 5%, soglia nostra).

## Cosa serve da Ale

Il via, e due conferme (ho già scelto io una risposta):
1. **Tutte le regate**, anche le due dell'1a, o solo le regate dell'1b? Scelgo **tutte**: il registratore è lo stesso e l'1a non cambia (G1).
2. **Il campo `cede:Nome`** (a chi sta cedendo l'avversario) nelle righe `B`: lo tengo. Va bene?

Versione prevista: 1.0.52 (`registratore.js` e `analizza_sessione.py`; motore, barca e regate non toccati). Modello consigliato: **Sonnet**.
