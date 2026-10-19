# Proposta: i segnali di partenza (livello 1b)

**Aggiornamento (Ale, 19 ottobre 2026): l'1a è congelato; questa proposta vale per l'1b** (regate e lezioni dell'1b). Da rivedere prima della fermata 2: niente lezione 7 nell'1a, la lezione va fra quelle dell'1b, e le bandiere solo nelle regate dell'1b.

19 ottobre 2026, fermata 1. Nessun codice. Primo pezzo delle lezioni nuove dell'1a (`RICERCA-CONTENUTI-LIVELLI.md` §8): quello che si vede in regata ha la sua lezione, e viceversa.

## Fonte

F15, regola 26 e «Race Signals» (copia locale, edizione 2025-2028), parafrasati:
- **avviso** a 5 minuti: si alza la **bandiera di classe**, un suono;
- **preparatorio** a 4 minuti: si alza la **bandiera P**, un suono (da qui si è «in regata»);
- **un minuto**: si ammaina la P, un suono lungo;
- **partenza**: si ammaina la bandiera di classe, un suono;
- i tempi contano sulle bandiere, non sui suoni; l'avviso può essere a un altro tempo se lo dicono bando o istruzioni;
- **X** = richiamo individuale, esposta subito dopo la partenza finché le barche richiamate sono tornate dietro la linea, al massimo 4 minuti;
- **bandiera blu** = chi la espone è un estremo della linea d'arrivo; **arancione** = un estremo della linea di partenza.

## Oggi [codice]

- Preparazione di 1, 3 (predefinita) o 5 minuti (`cdSel`, `opt.countdown`); messaggi «Segnale di avviso: partenza tra…», «Un minuto», «30 secondi», «10 secondi», «Partenza!» (`updateRace`, `js/regate.js`).
- La barca giuria ha una bandierina gialla prima del via e blu dopo (`drawRaceWorld`). Il giallo non corrisponde a nessun segnale vero; il blu sì (arrivo).
- Il richiamo individuale c'è solo come messaggio con i nomi.
- Il gioco non ha suoni.

## Proposta

**1. Le bandiere sulla barca giuria, in tutte le regate.**

| Momento | Bandiere esposte | Messaggio (sostituisce quelli di oggi) |
| --- | --- | --- |
| dall'avviso al preparatorio | classe | «Avviso: alzata la bandiera di classe» |
| dal preparatorio a un minuto | classe + P | «Preparatorio: alzata la bandiera P» |
| ultimo minuto | classe | «Un minuto: ammainata la P» |
| dopo la partenza | blu (arrivo); più **X** finché c'è una barca richiamata, al massimo 4 minuti | «Partenza!» e, se serve, il richiamo di oggi |

- **Sequenze per la preparazione scelta:** 5 minuti = la sequenza del regolamento (5-4-1-0). 3 minuti = **sequenza breve «per istruzioni di regata»** (avviso a 3, preparatorio a 2, un minuto a 1). 1 minuto = solo l'ultimo minuto (avviso e preparatorio già fatti; si vede la sola bandiera di classe). Lo dice la lezione.
- **La bandiera di classe è nostra** (nessun marchio, principio 5): un disegno semplice di una barca stilizzata.
- Bandiere disegnate grandi abbastanza da leggersi a ogni zoom (come le boe, con una misura minima in pixel). I «30 secondi» e «10 secondi» restano: non sono segnali ufficiali ma aiutano.
- Fuori: richiamo generale (primo ripetitore), differimento (AP), annullamento (N), percorso ridotto (S): il gioco non li usa, li nomina il manuale.

**2. Lezione 7 «La regata», primo passo: i segnali.** Lezione nuova dell'1a, che più avanti avrà anche i passi su precedenze e penalità (stesso posto, come chiesto da Ale: vedi una bandiera in regata, trovi la lezione). Per ora 3 passi di sola spiegazione, con le bandiere disegnate nel testo:
1. «La sequenza di partenza» (avviso, preparatorio, un minuto, partenza; si guardano le bandiere, non si ascoltano i suoni);
2. «Il richiamo» (X; torna dietro la linea e riparti);
3. «Le linee» (arancione alla partenza, blu all'arrivo).

**Conseguenze sulla carriera:** Esperienza da 6 a 7 lezioni (serve ancora «tutte»); il totale minimo si alza di 1 (29 → 30). Il ripasso 7 arriva quando la lezione 7 sarà completa (con precedenze e penalità), non ora.

## Criteri (soglie nostre, dichiarate ora)

- **G1** bandiere esposte giuste a ogni istante, per 1, 3 e 5 minuti, controllate a ogni decimo di secondo su 3 regate per preparazione; 0 errori.
- **G2** X esposta dopo la partenza solo se c'è almeno una barca richiamata, tolta quando sono tutte tornate o a 4 minuti; contati i casi con e senza richiamo (almeno 5 di ciascuno, semi fissi).
- **G3** lezione 7: i 3 passi si aprono, pannello a 1360×650 senza pixel in più; la lezione si completa.
- **G4** carriera intera col pilota delle lezioni (`collaudo_carriera_intera.py`) ancora OK, con 7 lezioni.
- **G5** impronta: cambiano solo le scene attese (regate: disegno della barca giuria e messaggi; menu: la lezione 7; libretto: numeri dell'Esperienza). Elencate prima di lanciare.
- **G6** pagina senza `#collaudo`: regata e lezione 7 si aprono, nessun errore.

## Rischi

- Le bandiere piccole sul mare: si giudica giocando se si leggono.
- La carriera già finita di Ale perde l'Esperienza piena (6 su 7): va bene (salvataggi azzerabili), ma l'attestato già preso resta.

## Decisioni per Ale

1. La lezione nuova è la **7 «La regata»** (che poi avrà anche precedenze e penalità), o i segnali vanno dentro una lezione esistente?
2. Le sequenze brevi per 3 e 1 minuto, come sopra, vanno bene?
