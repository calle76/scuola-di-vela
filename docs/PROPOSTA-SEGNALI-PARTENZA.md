# Proposta: i segnali di partenza (livello 2a)

**Aggiornamento (Ale, 19 ottobre 2026, sera): vale per il livello 2a** (il regolamento, con la stessa deriva dell'1b; `VISIONE-LIVELLI-E-CARRIERA.md` §2). Da rivedere prima della fermata 2: niente lezione 7 nell'1a (congelato); la lezione va fra quelle del 2a, le bandiere nelle regate del livello 2.

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

## Fetta 3 del 2a (31 ottobre 2026): le bandiere nella regata dei giri — scritta prima di toccare il codice

Per decisione di Ale (30-31 ottobre, autonomia sul 2a) questa è la prima parte della proposta di sopra, senza le lezioni (vengono dopo, dentro «La scuola»). Vale **solo nella «Regata con i giri di penalità»** (flag `segnali`), come le fette 1-2: le altre regate, 1a compresa, e le loro schermate non cambiano e l'impronta resta com'è. Ale (19 ottobre) aveva detto «le bandiere nelle regate del livello 2»: l'estensione alle altre regate dell'1b si decide quando il 2a diventa la regola.

**Modello più semplice.** Una funzione sola, `bandiere(t)`, dice quali bandiere sono su: classe, P, X, blu. Messaggi e disegno la leggono, il collaudo la confronta con una tabella scritta a parte.
- Preparazione **5 min:** classe da −300, P da −240, P giù a −60, classe giù a 0 (sequenza 5-4-1-0 del regolamento). **3 min:** classe da −180, P da −120, P giù a −60 («sequenza breve», ipotesi nostra, come nella proposta di sopra). **1 min:** solo classe da −60 (avviso e preparatorio già fatti, ipotesi nostra).
- Dopo il via: **blu** (la linea ora è d'arrivo, come oggi la bandierina blu). **X** esposta se al via c'era almeno una barca oltre la linea (richiamo individuale, 29.1): resta finché una di quelle barche non è tornata dietro la linea o arrivata o ritirata, e **al massimo 240 s** dallo sparo.
- Disegno sulla barca giuria: fino a quattro bandierine sul ponte, leggibili a ogni zoom (misura minima in pixel). La bandiera di classe è nostra (nessun marchio): bianca con una vela blu. P = blu con riquadro bianco, X = bianca con croce blu (bandiere internazionali di segnalazione, non marchi); blu = campo blu.
- Messaggi: «Avviso: alzata la bandiera di classe, partenza tra N minuti», «Preparatorio: alzata la bandiera P», «Un minuto: ammainata la P», e come oggi «30 secondi», «10 secondi», «Partenza!». I tempi contano sulle bandiere; il gioco non ha suoni (dichiarato).
- Registratore: evento `bandiere` a ogni cambio.

**Costanti, ipotesi nostre:** le sequenze di 3 e 1 minuto, le misure e le posizioni delle bandiere. 4 minuti di X e le sequenze di 5 minuti vengono dal regolamento.

**Criteri (soglie scritte prima; il metro è una tabella indipendente nel collaudo):**
1. **G1** con preparazione di 1, 3 e 5 minuti, 3 regate ciascuna (semi fissi), le bandiere esposte a ogni decimo di secondo da −preparazione a +5 s coincidono con la tabella: 0 errori su tutti i controlli (se ne riporta il numero: devono essere almeno 5000).
2. **G2** X esposta solo con almeno una barca richiamata: almeno 5 regate con richiamo (si porta un avversario oltre la linea poco prima dello sparo) e 5 senza; con richiamo X si alza allo sparo e si abbassa quando l'ultima barca è tornata, o a 240 s se nessuna torna; senza richiamo non compare mai.
3. **G3** i messaggi di avviso, preparatorio e un minuto compaiono ciascuno una volta e solo per i tempi dovuti, per 1, 3 e 5 minuti.
4. **G4** disegno: nelle altre regate (1a e 1b) la schermata a −30 s è identica al pixel alla 1.0.64; nella regata dei giri le bandiere si vedono (pixel diversi sulla barca giuria) e la schermata si guarda a occhio.
5. **G5** non-regressione: 20 regate dell'1a e dell'1b identiche al bit alla 1.0.64; `polare.js` e `raffiche_e_virate.js` invariati; `collaudo_giri.py` e `collaudo_boa.py` verdi.
6. **G6** registratore (evento `bandiere`) e pagina senza `#collaudo`: la regata si apre, le bandiere ci sono, nessun errore di pagina; pannello a 1360×650 senza pixel di eccesso.

**Rischi.** Bandiere piccole sul mare: si giudica giocando. L'X sulla barca giuria può restare su più del necessario se una barca richiamata resta ferma oltre la linea (limite del regolamento: 4 minuti).

**Esito (31 ottobre 2026, 1.0.65):** fatta e misurata, vedi `CHANGELOG.md`. Soglie non cambiate; quattro difetti del mio collaudo corretti prima di dichiarare l'esito. La lezione e l'estensione alle altre regate dell'1b restano da fare.
