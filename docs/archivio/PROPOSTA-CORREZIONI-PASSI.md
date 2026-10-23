# Proposte: correzioni dei passi delle lezioni

Una sezione per passo, nell'ordine in cui si fanno. Elenco dei passi da correggere: `PROPOSTA-PILOTA-LEZIONI.md` §10, più il passo 1.8 rotto dalla 1.0.11.

## 1. Passo 1.8 «Orzare e l'angolo morto» (fermata 1, 16 ottobre 2026)

### Il difetto

Il testo dice: «tieni premuto → … Continua finché la barca non si ferma quasi del tutto, poi rilascia». Dalla 1.0.11 la vela porta fino a 29° di vento apparente, la barca arriva al vento più veloce e, con la barra tenuta, **attraversa il vento e vira** invece di fermarsi. Il pilota che fa quello che dice il testo completa il passo **0 volte su 80** (prima 74 su 80). Ale, orzando a piccoli colpi, l'ha completato in 10 s fermandosi con la prua a 11-19° dal vento.

È il comportamento giusto della barca: con l'abbrivio e la barra tenuta, la prua passa il vento (lo dice anche la lezione 3: «la barca lo supera grazie all'abbrivio»). Sbagliato è il testo.

### Proposta: cambia solo il testo

Condizione del passo invariata (`twa < 40` e meno di 1,5 nodi per 0,5 s). Motore invariato. Testo nuovo:

> Ora premi **→**: la prua gira a dritta, verso il vento. Si dice *orzare*. Quando la prua è quasi nel vento (la lancetta della rosa entra nel rosso), rilascia: la vela sbatte, non spinge più e la barca rallenta fino a fermarsi.

La parte fra parentesi serve a chi ha la rosa accesa (lo è di norma); chi l'ha spenta ha comunque «quasi nel vento».

**Da decidere (Ale):** aggiungere anche una frase per chi tiene troppo: «Se tieni premuto troppo a lungo, la prua attraversa il vento e la barca vira: premi *Ricomincia*.» Costa una riga nel pannello.

### Misura già fatta (pilota modificato, gioco non toccato)

Copia del pilota con una sola riga cambiata: invece di tenere finché la barca è sotto 1 nodo, rilascia quando legge la prua sotto 40° dal vento (lettura con errore ±5°, come sempre). Poi mani ferme fino al tempo limite (60 s).

| Semi | Giocatore preciso | Giocatore impreciso (tiene da 0,3 a 1,5 s in più) |
| --- | --- | --- |
| 1-20 | **20 su 20**, mediana 7,0 s | 12 su 20 |
| 21-100 | **80 su 80**, mediana 7,1 s | 45 su 80 |

Quando l'impreciso fallisce, la barca ha virato: finisce dall'altra parte a 32-57° dal vento, ancora in moto (per esempio 3,1 nodi). Il passo dopo, «Ripartire», si completa guidando 99 su 100 e non si completa mai da solo (0 su 100, anche dopo un colpo lungo).

**Attenzione:** questi numeri li ho già visti su entrambi i gruppi di semi. Per la regola dei semi la conferma della fermata 2 va fatta su un gruppo nuovo, i semi 101-200.

### Criteri per la fermata 2 (soglie nostre, scritte ora)

1. Pilota aggiornato al testo nuovo («rilascia quando la prua entra nel rosso»), semi 101-200: preciso completa **almeno 97 su 100**; a mani ferme 0 su 100.
2. Impreciso: si riporta il numero, **senza soglia**. Tenere troppo e virare è realistico; il passo non deve impedirlo.
3. «Ripartire» non si completa da solo più di 2 volte su 100.
4. Pannello a 1360×650: eccesso **0 px** sul passo 1.8 (`collaudo_pannello.py`), con e senza la frase facoltativa.
5. `collaudo_registro.py`, parte lezioni: torna 15 su 15. Oggi tiene → finché il passo si completa, quindi con la barca che vira fallisce; va cambiato anche lui per rilasciare nel rosso (cambio del collaudo dichiarato).
6. Non-regressione: `polare.js` e `raffiche_e_virate.js` identici carattere per carattere (il motore non cambia).
7. Prova senza `#collaudo`: una pagina da giocatore, tastiera vera, passo 1.8 completato rilasciando nel rosso, 3 tentativi su 3.

### Costanti nuove

Nessuna.

### Fonti

Nessuna affermazione nautica nuova: «la vela sbatte, non spinge e la barca si ferma» c'è già (`CONTENUTI-DA-VERIFICARE.md`, riga 4 della L1); «con l'abbrivio la prua attraversa il vento» c'è già nella lezione 3.

### Rischi

- Il giocatore impreciso vira 4 volte su 10. Se ad Ale sembra troppo frustrante, la frase facoltativa aiuta; una barra che torna al centro più in fretta, invece, sarebbe un cambio del gioco e qui non lo propongo.
- Versione del gioco: cambia un testo, quindi nuova versione 1.0.12 (`VERSIONE` e `CHANGELOG.md`).

### Esito (fermata 2, 16 ottobre 2026): fatto nella 1.0.12

Ale ha scelto il testo **con** la frase facoltativa, l'ha provato giocando («funziona») e ha deciso di non fare la conferma sui semi 101-200: i criteri 1, 3, 5 e 7 **non sono stati misurati**. Misurati: pannello eccesso 0 px (32 passi, criterio 4) e non-regressione identica (criterio 6). Pilota e `collaudo_registro.py` aggiornati al testo nuovo, da verificare nel prossimo giro completo.

## 2. Passo 1.9 «Ripartire» (fermata 1, 16 ottobre 2026)

### Cosa succede oggi (gioco 1.0.12, pilota semi 1-20, 40 corse)

- **Guidando** come dice il testo (poggiare fino al traverso): **20 su 20**, mediana 4,2 s.
- **A mani ferme** (30 s senza tasti): il passo **non si completa mai** (0 su 40), ma la barca esce da sola dall'angolo morto **40 volte su 40** e finisce in bolina (32-57° dal vento, 1,6-5,2 nodi, filetti dritti). È l'osservazione 45.
- La causa è una regola del motore **senza fonte**: barca quasi ferma (sotto 0,5 m/s) con vento apparente sotto 36°, la prua poggia da sola fino a 6 °/s (`ironsA`, `ironsU`, `ironsYaw`). In `DUBBI-E-RICERCHE.md` (domanda 1) due fonti dicono il contrario: la barca **resta** nell'angolo morto se non si fa qualcosa (una sola delle due riguarda una deriva).

### Misura su una copia con `ironsYaw` = 0 (fuori dal progetto, `js/` non toccato)

- 1.9 a mani ferme: la barca **resta nel vento e arretra a circa 2 nodi** (prua a 2-20° dal vento).
- 1.9 guidando come dice il testo: **0 su 20**. Andando all'indietro la barra funziona al contrario: premendo «poggia» la barca si ferma a 24-30° dal vento, a 0 nodi.
- 5.4 «Una virata che non riesce» (uscita con la barra verso il boma): 20 su 20, mediana 34,8 s, uguale al gioco di oggi (34,7 s).
- Si rompe a catena anche 1.12 «Troppo cazzata» (0 su 20), perché arriva dal 1.9 saltato.

Quindi togliere la regola senza fonte rende la lezione 1 impossibile da fare con quello che insegna: le fonti, per i principianti, insegnano a uscire spingendo il boma insieme alla barra, e il gioco non ha quel comando.

### Due strade

- **A. Non cambiare niente ora** (consigliata). Il passo funziona: guidando 100%, da solo 0%. La regola senza fonte resta, già dichiarata come semplificazione in `FISICA-E-TARATURE.md` punto 7; aggiungo i numeri di oggi in `DUBBI-E-RICERCHE.md` e chiudo l'osservazione 45 come «semplificazione dichiarata». Il problema vero passa al compito della barca piantata (retromarcia che «parte troppo presto», 2 nodi all'indietro, comando «spingi il boma» nel livello 2).
- **B. Correggere la fisica adesso:** togliere o ridurre la prua che poggia da sola, rivedere la retromarcia e riscrivere la lezione 1 su come si esce dall'angolo morto. È un compito grosso di fisica: proposta a parte con revisione in chat, e tocca le lezioni 1 e 5, gli avversari, le prove e le fasce.

### Decisione di Ale ed esito (16 ottobre 2026, versione 1.0.13)

**Ale:** «A, e rallentiamo un po' la retromarcia, tutto qui, senza fare mille test».

- **1.9:** nessun cambio; osservazione 45 chiusa come semplificazione dichiarata, numeri in `DUBBI-E-RICERCHE.md` (domanda 1).
- **Retromarcia:** nuova costante `backDrag` = 1,5 (ipotesi, nessuna fonte): all'indietro lo scafo frena una volta e mezza. Banco `retromarcia.js`, massimo all'indietro con la prua al vento: 0,95 / 2,33 / 3,40 / 4,30 → **0,81 / 1,99 / 2,96 / 3,79 nodi** con 6 / 10 / 15 / 20 nodi; regime con la prua tenuta nel vento 1,57 / 2,60 / 3,73 / 4,66 → 1,34 / 2,24 / 3,26 / 4,15. Tempo per arrivare a −0,5 nodi **invariato** (con 10 nodi 1,6 s da ferma): «parte troppo presto» resta aperto.
- **Controlli:** `polare.js` e `raffiche_e_virate.js` identici; `angolo_morto.js` stesse uscite (364 su 366 per caso), tempi di uscita da 0,1 a 0,3 s più lunghi; pilota veloce (semi 1-3) lezioni 1 e 5 tutto completato, 5.4 in 35,0 s (prima 34,7 s sui semi 1-20).

## 3. Passo 2.4 «Barra sottovento: si orza» (fermata 1, 16 ottobre 2026)

### Il difetto

Il testo dice di fermarsi «quando la lancetta della rosetta è a metà strada tra il rosso e l'orizzontale», cioè a circa 65° dal vento (il rosso finisce a 40°, l'orizzontale è a 90°). Il passo accetta da 43° a 67°: il bersaglio sta a 2° dal bordo, e chi legge la lancetta con qualche grado di errore lo supera e deve tornare indietro.

### Proposta: cambia solo il testo

«a metà strada» → «**a un terzo della strada** tra il rosso e l'orizzontale», cioè circa 57°, al centro della finestra 43-67°. È lo stesso modo di dire del passo 2.5 («un terzo della strada tra l'orizzontale e il basso»). Condizione e motore invariati.

### Misura già fatta (pilota con lettura ±5°, gioco 1.0.13)

| Semi | Oggi (bersaglio 65°) | Bersaglio 57° |
| --- | --- | --- |
| 1-20 | 20 su 20, **5 riprese**, mediana 5,1 s | 20 su 20, **0 riprese**, 4,5 s |
| 21-100 | 79 su 80, **29 riprese**, 5,3 s | **80 su 80, 0 riprese**, 6,1 s |

A mani ferme 0 in entrambi i casi. «Già fatto dopo un colpo lungo» resta 2 su 20 e 3 su 80: è l'osservazione 49 (tenendo troppo la freccia nel passo 2.3 la prua è già in bolina), che non dipende dal testo e la lascio così: è ciò che succede davvero tenendo la barra.

### Criteri alla fermata 2

Pannello a 1360×650 eccesso 0 px; `polare.js` e `raffiche_e_virate.js` identici (il motore non cambia); `collaudo_versione.py`. Pilota aggiornato a 57°.

### Esito (16 ottobre 2026, versione 1.0.14)

Ale: «si». Testo cambiato; misure quelle della tabella sopra (pilota aggiornato a 57°).

## 4. Passo 4.3 «Accelerando» (16 ottobre 2026): niente da correggere

Nel pilota del 16 ottobre (1.0.5) fermandosi ai primi filetti dritti la barca restava a 3,7 nodi e il passo, che ne chiede più di 4, si completava solo cazzando ancora (una ripresa in 80 corse su 80). **Sul gioco 1.0.14 il difetto non c'è più:** pilota normale 20 su 20 e 80 su 80, **0 riprese**, mediana 7,0 s; con le riprese tolte dal pilota (si ferma ai primi filetti dritti e basta) 20 su 20, a 4,6 nodi. L'hanno corretto la resistenza della vasca (1.0.6) e la vela che stringe (1.0.11). Il testo di fine passo («apparente tra 60° e 70°») resta vero: con 10 nodi al traverso, fra 4 e 5,5 nodi di barca, l'apparente è fra 61° e 68° (triangolo dei venti, senza scarroccio). Nessun cambio, nessuna versione.

## 5. Passo 6.2 «Assorbire una raffica» (fermata 1, 16 ottobre 2026)

### Il difetto

Oggi (1.0.14, semi 1-20) il passo si completa **a mani ferme 16 volte su 20**: la condizione chiede «in raffica» (vento almeno +12%), sbandamento sotto 20° e più di 2 nodi per 3 s, e già al bordo di una raffica moderata la barca resta sotto i 20° da sola. Il passo non insegna il gesto che chiede.

### Proposta (provata su una copia, `js/` non toccato)

1. **Una raffica media garantita**, come quella forte del passo 6.3 (`bigGust`), ma del +45% (12 → circa 17 nodi). Nasce 45 m sopravento **dove la barca arriverà** (spostata di lato quanto la barca si muove nel tempo che la raffica impiega ad arrivare): nata dritta sopravento, la barca di bolina se ne allontanava di lato e la raffica non la prendeva quasi mai. La raffica forte del 6.3 resta com'è.
2. **Condizione nel cuore della raffica e di bolina:** vento almeno +30% (non +12%), prua entro 75° dal vento (il confine «bolina» del pannello), sbandamento sotto 20°, più di 2 nodi, per 3 s. Il testo non cambia.

Costanti nuove (ipotesi nostre, nessuna fonte): +45% della raffica, soglia +30%.

### Misure (pilota, semi 1-20 per scegliere e 21-100 per confermare)

| | Oggi | Proposta |
| --- | --- | --- |
| guidando (di bolina, lasca sopra 15°) | 4 su 4 corse guidate (le altre già fatte da sole), 38 s | **20 su 20 e 80 su 80**, mediana 11,3 s |
| a mani ferme | **16 su 20** | **0 su 20 e 0 su 80** |
| contro-prova: di bolina, senza mai lascare | — | **1 su 20** (gli altri sbandano fino a 21-43°, uno scuffia) |

**Controllo del metro:** con la raffica nata dritta sopravento il passo a mani ferme dava 0 su 100, ma solo perché la raffica non arrivava. Con la raffica sulla strada della barca e senza la condizione di bolina dava 98 su 100: a mani ferme la barca resta al traverso (87°, 8 nodi) con la vela troppo cazzata e non sbanda. Con la condizione di bolina, 0 su 100 con la raffica che arriva davvero.

## 6. Passo 6.3 «La scuffia»: proposta di non cambiarlo

Si completa a mani ferme in una parte delle corse (oggi 4 su 20; con la proposta del §5, 15 su 20 e 47 su 80, perché si arriva dal 6.2 con la vela regolata). Il passo chiede «vela tutta cazzata e in raffica non lascare»: chi non fa niente **non lascia**, e la raffica forte (+80%) lo fa scuffiare comunque. È quello che il passo vuole mostrare: non reagire a una raffica forte fa scuffiare. Guidando 20 su 20 (oggi) e 33 su 33 (proposta).

### Esito (16 ottobre 2026, versione 1.0.15)

Ale: «si». Il codice provato sulla copia è stato portato nel gioco senza differenze (più un commento); 6.3 invariato.

## 7. Casi minori 1.11, 1.12, 2.5: non si cambiano (Ale, 16 ottobre 2026)

«Già fatto dopo un colpo lungo» (semi 21-100): 1.11 «La scotta: cazzare» 4 su 80, 1.12 «Troppo cazzata» 2 su 80, 2.5 «Barra sopravento: si poggia» 5 su 80; anche 2.4 3 su 80 (osservazione 49). Chi tiene troppo il comando nel passo **prima** porta già vela o prua dove chiede il passo dopo: succede anche in barca. Per evitarlo bisognerebbe bloccare i comandi fra un passo e l'altro, e il gioco sarebbe meno vero. **Semplificazione dichiarata.** «A piccoli colpi» è già in evidenza nei testi dei passi 2.4 e 2.5 dalla 1.0.2 (osservazione 49), e i passi 1.11 e 3.2 dicono «poco alla volta». Il colpo lungo nasce però nel passo prima (per esempio 2.3 «Barra a dritta», che chiede solo di spostare la barra): l'avvertenza c'è dove si deve dosare, non dove si fa l'errore.

Con questo le correzioni dei passi trovati dal pilota (`PROPOSTA-PILOTA-LEZIONI.md` §10) sono chiuse.
