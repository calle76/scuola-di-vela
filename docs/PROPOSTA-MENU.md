# Proposta: il menu nuovo, con tutte le 20 lezioni

2 novembre 2026. **Fermata 1: solo documento e bozze fotografate, nessun codice nel gioco.** È il passo 5 di `PROPOSTA-LEZIONI-SCUOLA.md` (DECISIONI: «prima tutte le lezioni, poi il menu, proposta con screenshot»). Le bozze sono montate sopra la pagina vera della 1.2.3, in Firefox a 1360×650, da uno script fuori dal gioco; le foto stanno in `docs/menu-bozze/`.

## 1. Il problema, misurato

- Oggi la Scuola ha **11 voci** (6 lezioni e 5 prove) e ci stanno giuste (`menu-bozze/oggi.png`).
- Con tutte le lezioni le voci diventano **25** (20 lezioni e 5 prove), e i ripassi da 6 a 20. Se si mostrano così come sono, la pagina è alta **1077 px** invece di 650: sfora di **426 px** (`menu-bozze/tutte_visibili_intero.png`, e `collaudo_esame_nuove.py`, riga «DA SAPERE»).

## 2. Proposta

**Ordine e numeri.** L'ordine è quello già approvato (`PROPOSTA-LEZIONI-SCUOLA.md` §5); le prove restano dove sono oggi, dopo la lezione che le prepara. Le lezioni si chiamano **Lezione 1 … Lezione 20** in quell'ordine (spariscono i nomi B1, D5, C2…). I salvataggi sono legati alla posizione interna della lezione, non al nome: **i progressi di oggi restano** (chi ha fatto la lezione 1-6 la ritrova fatta, con il numero nuovo).

**Tre gruppi** (l'idea di Ale delle pagine per argomento):

| Gruppo | Voci | Contenuto |
|---|---|---|
| 1 · La barca | 11 | La barca e il vento, Il timone, Il timone che stalla, Andature e mure, Prova 1, Prova 2, Vento reale e apparente, Virata e strambata, Spingere il boma, Prova 3, Prova 4 |
| 2 · Vento e raffiche | 5 | Raffiche e scuffia, La raddrizzata lunga, La barca che orza sbandando, I salti di vento, Prova 5 |
| 3 · Regole e partenze | 9 | Mure opposte, Stesse mure, Chi vira cede, Evitare il contatto, I segnali di partenza, La partenza anticipata, Partenza in velocità, Partenza da fermi, Boe e giri di penalità |

**Come si mostrano: due bozze.**
- **A, schede (la consiglio).** In cima al riquadro Scuola tre pulsanti, uno per gruppo, con il conto («0/11»); sotto, le voci del gruppo scelto, numerate da 1 a 25 di seguito. Il riquadro dei ripassi segue il gruppo scelto: i suoi ripassi **su due colonne** (numero e titolo), poi l'esame. Il gioco ricorda l'ultima scheda aperta e all'inizio apre quella della prima voce da fare.
  - Foto: `A2_due_colonne_libero_gruppo1.png`, `A2_due_colonne_libero_gruppo3.png`, `A2_due_colonne_carriera_gruppo3.png` (il caso peggiore: 9 ripassi e il libretto della carriera).
  - **Misura: 0 px di eccesso** in tutti e quattro i casi provati (gioco libero e carriera, gruppo 1 e gruppo 3).
  - Con i ripassi su una colonna sola, in carriera il gruppo 3 sfora di **80 px** (`A_schede_carriera_gruppo3.png`): per questo le due colonne.
- **B, tendine.** I tre gruppi uno sotto l'altro, si apre un gruppo alla volta. **Misura: sfora di 10 px** con il gruppo 1 aperto e di **39 px** con il gruppo 3, già nel gioco libero (`B_tendine_gruppo1.png`). Si potrebbe stringere, ma resta più lunga di A.

**In tutte e due:**
1. Sparisce il riquadretto «In arrivo · Altri tipi di barca» (serve lo spazio).
2. Nei ripassi su due colonne il punteggio migliore non ci sta più come testo: diventa un segno accanto al numero (per esempio «✓» con almeno l'80%), e il punteggio intero si legge passando sopra col mouse.
3. **Lezione 3 senza precedenze** (decisione del 31 ottobre): titolo «Andature e mure»; la pagina «Le mure e le precedenze» diventa «Le mure» e il paragrafo sulle precedenze diventa un rimando al gruppo 3. Esce dal quiz della lezione 3 la domanda «chi deve lasciare strada» (la stessa cosa la chiede la lezione «Mure opposte»): il quiz passa da 6 a 5 domande. Nella banca d'esame della lezione 3 nessuna domanda parla di precedenze; cambia solo il nome del passo da cui viene una domanda («Le mure»).
4. **Testi e glossario con i numeri nuovi:** le 51 voci del glossario che dicono «Lezione N» e le frasi delle lezioni che rimandano a un'altra per numero (per esempio «è una strambata, lezione 5») si aggiornano; un collaudo cerca i rimandi rimasti vecchi.
5. Il quiz alla fine delle lezioni nuove (oggi nascosto, `lQuiz`) compare come nelle altre.

**Carriera (meriti del libretto).** Oggi «Conoscenza» conta i quiz delle 6 lezioni (al più 12 punti, ne servono 6) ed «Esperienza» le lezioni fatte (al più 6, ne servono 6). Proposta: **stesse soglie, conto in proporzione**: Conoscenza = 12 × (punti dei quiz di tutte le 20 lezioni / punti massimi), Esperienza = 6 × (lezioni fatte / 20), arrotondati per difetto. Così il totale resta 46 e la soglia 29, e chi oggi ha già i meriti dalle 6 lezioni li vede calare finché non fa le nuove: è giusto, perché la scuola è più lunga, ma lo dico. Il «brevetto di livello 1» e gli altri nomi della riorganizzazione (scuola, attestato) **non** sono in questa proposta: sono il passo dopo.

## 3. Criteri (soglie scritte prima, attese nostre)

- **M1:** menu a 1360×650 senza pixel di eccesso (pagina e riquadri), con ognuno dei 3 gruppi aperto, in gioco libero e in carriera, in Chromium e Firefox: 12 casi su 12. Anche a 1360×768.
- **M2:** ogni voce dei tre gruppi apre la lezione o la prova giusta (25 su 25); numeri da 1 a 25 senza buchi; ogni lezione si chiama «Lezione N» con N da 1 a 20.
- **M3:** salvataggi: un salvataggio di oggi (lezioni 1-6 e prove fatte, record, quiz) caricato nella versione nuova dà le stesse voci fatte, gli stessi record e gli stessi punteggi dei quiz. Controprova: un salvataggio vuoto non mostra niente di fatto.
- **M4:** nessun rimando vecchio: nessun «Lezione B…», «C…», «D…» nei testi visibili; ogni «lezione N» scritta in un testo punta alla lezione che dice (controllo automatico sul titolo).
- **M5:** lezione 3 senza la parola «precedenza» e senza la domanda tolta; `collaudo_lezioni`, `collaudo_pilota_lezioni --veloce`, `collaudo_quiz`, `collaudo_esame` (ora con 34 domande) e i collaudi della carriera verdi; meriti ricontati come al §2, con i numeri attesi scritti nel collaudo.
- **M6:** pagina senza `#collaudo`: si cambia gruppo, si apre una voce per gruppo e si torna al menu, nessun errore. Regate e fisica identiche (non vengono toccate).

## 4. Rischi

- **È il cambiamento più visibile da mesi:** tutte le 20 lezioni e l'esame da 34 domande arrivano insieme. I collaudi che contano voci e domande del menu (carriera, esame, quiz) vanno quasi tutti aggiornati: li elenco nel rapporto, uno per uno.
- **Venti lezioni** sono tante per chi comincia; le schede aiutano a non vederle tutte insieme.
- **I numeri nuovi** (la vecchia «lezione 4» diventa la 5…) possono confondere chi giocava già: oggi siete in due, e i progressi restano.
- **Online** c'è ancora la 1.0.78 (`main`): questa versione resta sul ramo `pulizia`. Quando il ramo entra in `main` è una domanda per dopo.

## 5. Da decidere (Ale)

1. **Bozza A (schede, ripassi su due colonne) o B (tendine)?** Io consiglio la A: è l'unica che sta nella finestra in tutti i casi provati.

## 6. Avanzamento

- **Ale, 2 novembre 2026:** «va bene la A, vai avanti».
- **1.2.4:** fatto. M1-M6 verdi in Chromium e Firefox (`collaudo_menu.py`). Aggiunta alla proposta: i meriti contano le lezioni visibili (nel gioco tutte), perché i collaudi della carriera nascondono le nuove. Collaudi adattati elencati nel `CHANGELOG.md`.
