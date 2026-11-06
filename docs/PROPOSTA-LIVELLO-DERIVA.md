# Proposta: il livello «Deriva»

4 novembre 2026. **Fermata 1: solo questo documento e due bozze fotografate, nessuna riga nel gioco.** È il passo 6 di `PROPOSTA-RIORGANIZZAZIONE.md` §5. Serve il via di Ale.

## 1. In breve

Deriva è il secondo livello, con la **stessa barca** della Scuola. Si impara a gareggiare: regate più difficili, un torneo da superare, rivedere le proprie regate. Quasi tutto **esiste già** nel gioco, mescolato nel menu con la Scuola: il lavoro è soprattutto metterlo in ordine e dargli un traguardo.

**Barca, fisica e avversari non cambiano.** Il motore non si tocca.

## 2. La scoperta: la soglia decisa il 30 ottobre così non si può avere

`PROPOSTA-RIORGANIZZAZIONE.md` §6 (M5) chiede una soglia del torneo superata dal pilota «circa il 70-80%» delle volte. Dal giro della 1.2.10 (`collaudo_torneo.py`, 40 tornei a browser, avversari principianti):

| Semi | Browser | 1° | 2° | 3° | 4° | Fra i primi tre |
| --- | --- | --- | --- | --- | --- | --- |
| 1-20 | Chromium | 1 | 5 | 3 | 11 | 9 su 20 |
| 101-120 | Chromium | 4 | 1 | 8 | 7 | 13 su 20 |
| 1-20 | Firefox | 1 | 4 | 2 | 13 | 7 su 20 |
| 101-120 | Firefox | 2 | 3 | 9 | 6 | 14 su 20 |
| **Totale** | | **8** | **13** | **22** | **37** | **43 su 80 (54%)** |

Col piazzamento i gradini possibili sono solo 1°, 2°, 3°, 4°. «Vincere» è il 10%, «fra i primi due» il 26%, «fra i primi tre» il 54%, «finire» il 100%. **Nessun gradino dà 70-80%.** Il pilota prende anche circa 4,5 penalità a torneo, e il 4° posto è il più frequente: lo stesso squilibrio che il collaudo di Competizione (C1) segnala da tempo.

Si potrebbe usare una soglia sui punti della serie (per esempio «al massimo 13 punti»), scelta per dare il 75%. **La sconsiglio:** il numero sarebbe preciso ma si potrebbe superare arrivando ultimi, e a chi gioca non direbbe niente.

**Proposta: «arriva fra i primi tre», tentativi senza limite.** È chiaro e coincide con i meriti già costruiti (3° = 3 punti di Competizione, gli stessi che bastano nella Scuola). Il 70-80% del 30 ottobre diventa il valore **entro due tentativi** (criterio D7). Questa è una **modifica dichiarata** della soglia scritta allora, fatta prima di misurare i semi nuovi.

## 3. Cosa c'è dentro

Bozze: `menu-bozze/D_deriva_carriera.png`, `menu-bozze/D_scuola_libero.png` (fatte a mano sopra il menu vero, a 1360x650, eccesso 0 px; la riga sotto il titolo va a capo e nel gioco va accorciata).

| | La scuola | Deriva |
| --- | --- | --- |
| Lezioni | le 20 di oggi | **2 nuove:** 21 «Come funziona il torneo», 22 «Rivedi la tua regata» |
| Prove con medaglie | le 5 di oggi | nessuna |
| Regate | bastone, raffiche | salti di vento, giri di penalità |
| Torneo | nessuno | **il torneo di oggi, da superare** |
| Ripassi | quiz ed esame | i 2 quiz nuovi, **nessun esame** |
| Coach | nessuno | **registratore e moviola, che ci sono già, e il momento clou, da fare** (proposta a sé, §5) |
| Traguardo | attestato | «Deriva superata»; nessun attestato |
| Navigazione libera | sì | sta nella Scuola, sempre aperta |

**Il menu:** due pulsanti nuovi in alto, «La scuola» e «Deriva». **Nel gioco libero** è tutto sempre aperto (principio 2). **In carriera** Deriva si apre con l'attestato, com'è già oggi per il torneo. Superata Deriva, il gioco lo dice e basta: «Fiocco» non esiste ancora, e nel menu non compare.

**Lezione 21, il torneo:** solo teoria e quiz di 4 domande: punti bassi, scarto, penalità sul punteggio, finestra d'arrivo. Sono le regole già nel gioco.

**Lezione 22, rivedere:** il tasto O che segna un momento, «Rivedi» a fine regata, le regate registrate. Un esercizio con il meccanismo già fatto per le lezioni: una regata breve vicino alla boa in cui si segna un momento con O.

## 4. Dove mi discosto da quanto scritto il 30 ottobre, e perché

| Scritto allora | Proposta ora | Perché |
| --- | --- | --- |
| Uno o due tornei | **uno** | È quello che esiste e che è collaudato; il secondo si aggiunge senza rifare niente |
| Giri di penalità come prova fra le lezioni | **tolta** | Li insegna già con un esercizio la lezione «Boe e giri di penalità»; e «nessuna medaglia» fuori dalla Scuola (`DECISIONI.md`, 30 ottobre) |
| Lezione sui segnali della giuria | **tolta** | C'è già nella Scuola (gruppo D) |
| Momento clou | **in Deriva, come scritto allora** | Corretto il 6 novembre, decisione di Ale: «il coach e il clou è nel livello deriva. Tutte le altre implementazioni del coach arrivano col fiocco». Qui avevo scritto «dopo, col Fiocco»: era sbagliato |

**Fuori da questa proposta:** giri di penalità nel torneo o in altre regate (il torneo resta con la penalità sul punteggio, regola 44.3, decisa il 20 ottobre); regola 18 («ultima fatica», dopo Deriva); correzione degli avversari.

## 5. Traguardi (`METODO.md` §5) e versioni

- **Alfa, 1.3.0:** menu a due livelli, voci spostate, carriera che apre Deriva. Nessun contenuto nuovo.
- **Beta, 1.3.1:** lezioni 21 e 22 con quiz e collaudi.
- **Uscita, 1.3.2:** soglia nel torneo e nel libretto, misura D7, giro completo, prova a mano di Ale e di Lucio.

Dopo ogni fetta, collaudi verdi e commit.

**Momento clou (aggiunto il 6 novembre):** è codice nuovo, quindi ha una sua proposta con le due fermate (`PROPOSTA-COACH-REGISTRATORE.md`, fase 2, criterio 3). Quando si riparte con Deriva si decide in quale fetta entra e cosa ne dice la lezione 22. Domanda sulla penalità e passo da ripetere (fasi 3 e 4) restano col livello del Fiocco.

**Aggiornamento del 4 novembre, decisione di Ale: Deriva aspetta che la Scuola sia giocata (`CHECK-SCUOLA-1.2.11.md`), e ogni lavoro su Deriva resta nascosto o in `sperimentale/`.** Quindi 1.3.0, 1.3.1 e 1.3.2 non sono più versioni visibili una dopo l'altra: chi apre il gioco vede il menu di oggi finché Ale non dice di mostrare Deriva. Come farlo si propone quando si riparte; idea più semplice: le lezioni con `nascosta: true`, come già fatto per le lezioni nuove, e il menu a due livelli solo con `#deriva` nell'indirizzo. Oggi il menu mostra già regate dei salti e dei giri e torneo: restano dove sono.

## 6. Criteri misurabili (soglie nostre, scritte prima)

Tutti in Chromium e Firefox.

- **D1, nulla cambia sotto:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.
- **D2, spazio:** menu senza eccesso in ogni combinazione di livello, modo e gruppo, a 1360x650 e 1360x768, col libretto al massimo.
- **D3, tutto al suo posto:** ogni voce apre la sua lezione, regata o torneo. Nel gioco libero tutto aperto; in carriera Deriva chiusa senza attestato e aperta con. Anche nella pagina senza `#collaudo`, 0 errori.
- **D4, la Scuola resta com'è:** in carriera meriti e conti identici a oggi; l'esame resta di 34 domande con 28 per passare; le lezioni 21 e 22 non entrano in meriti, esame e «di 25 completate». `collaudo_carriera_intera.py` verde.
- **D5, lezione 22:** esercizio completato guidando 10 su 10, a mani ferme 0 su 10, semi 1-10, confermato sui semi 11-20.
- **D6, la soglia:** 1°, 2° e 3° superano; 4° e torneo ritirato no (controprova). Il risultato resta alla ricarica; un salvataggio di oggi con un 3° già fatto risulta superato. Nel gioco libero il torneo non apre né chiude niente.
- **D7, la misura:** semi **201-240, mai guardati**, 40 tornei a browser, principianti. A coppie di semi consecutivi (20 coppie, due tentativi).
  - Un tentativo: fra i primi tre fra il 40% e il 70% dei tornei.
  - Due tentativi: almeno una riuscita in almeno 14 coppie su 20 (70%).
- **Nomi:** `collaudo_nomi.py` esteso alle schermate nuove.

Il pilota non è un giocatore: D7 dice che il traguardo è raggiungibile, non quanto è difficile. Quello lo dice solo chi gioca. Un numero fuori fascia si riporta com'è.

## 7. Costanti nuove

Una sola: il piazzamento richiesto, **3°**, ipotesi nostra da confermare giocando. Si salva nulla di nuovo: «superata» si ricava dal miglior piazzamento già salvato (`progress.torneoFatto`).

## 8. Fonti

La lezione 21 usa F15 (appendice A sui punteggi, 44.3 sulla penalità), già citata nel codice del torneo, parafrasata. La finestra d'arrivo si dichiara come ipotesi nostra. La lezione 22 parla solo del gioco, nessuna affermazione nautica.

## 9. Rischi

- **Un tentativo è lungo:** 4 regate da circa 4 minuti, cioè 16-20 minuti di gioco. Con 54% di riuscita, chi guida come il pilota lo rifà spesso. Il torneo si salva dopo ogni regata.
- **Il passaggio dipende dagli avversari**, con i difetti noti (`DECISIONI.md`: barche che si cedono a vicenda, 9 corse su 3.216; tre barche alla boa). Il primo difetto però avvantaggia chi gioca: le due barche finiscono lontane e il giocatore non cede come il pilota. Se giocando il torneo sembra ingiusto, torna la domanda sugli avversari.
- **I semi variano molto:** fra i primi tre dal 35% al 70% a seconda del gruppo. Quaranta tornei danno un ordine di grandezza, non un numero preciso.
- **La carriera di chi ha già un salvataggio:** le regate che oggi non contano in carriera compaiono in Deriva dopo l'attestato; nessun punto cambia (D4).
- **Documenti vecchi** (`VISIONE`, `ROADMAP`, `STATO`) ancora con la vecchia numerazione: si riscrivono al passo 7, dopo Deriva.

## 10. Decisioni per Ale

Una sola adesso: **la soglia del torneo, §2.** Tutto il resto è scelto da Claude e si cambia a basso costo, salvo che Ale dica altrimenti.
