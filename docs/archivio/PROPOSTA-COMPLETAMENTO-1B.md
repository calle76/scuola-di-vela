# Proposta: completare il livello 1b (lezioni brevi, replay, menu, esame e brevetto)

> **In attesa di essere superata** da `PROPOSTA-RIORGANIZZAZIONE.md` (30 ottobre 2026): se Ale approva la scuola e il livello 1, le sette lezioni si fondono nella scuola e menu, meriti e brevetto dell'1b non si fanno. Le decisioni prese su questa proposta restano in `DECISIONI.md`, ma quelle su brevetto e menu decadono.

30 ottobre 2026. **Fermata 1: nessun codice.** Punto di partenza: `VISIONE-LIVELLI-E-CARRIERA.md` §2 e §6, `ROADMAP.md` (ordine), `STATO.md` «Prossimo lavoro» punti 4 e 5, `PROPOSTA-TORNEI-1B.md`, `PROPOSTA-REGATA-COME-FONTE.md` §9-10. La barca dell'1b è congelata (23 ottobre): questa proposta **non tocca il motore**.

## Cosa c'è e cosa manca (letto nei documenti)

| Parte dell'1b | Stato |
| --- | --- |
| Barca completa, congelata con due impronte | Fatta |
| Regate: «Regata nei salti di vento», contatto vero, `chiCede` (10-13), semaforo | Fatte |
| Torneo T1 (bastone) e T2 (triangolo), meriti di Competizione | Fatti (1.0.34-1.0.56) |
| Registrazione automatica e «Rivedi» (moviola) | Fatte (1.0.58, 1.0.60) |
| **Lezioni brevi** | Mancano |
| **Replay semplice** | In parte: «Rivedi» c'è, «ripeti da qui» no |
| **Menu dell'1b, esame, attestato e brevetto** | Mancano: oggi esame e brevetto sono solo del livello 1a, e il torneo dell'1b si apre con quel brevetto |
| **Tempi delle medaglie** | Non applicabili finché l'1b non ha prove (vedi §4) |

## 1. Le lezioni brevi (sette)

Elenco già deciso in `VISIONE` §2: **1** timone che stalla (freccia e Maiusc), **2** spingi il boma (Z), **3** salti di vento (virare sugli scarsi), **4** raddrizzata lunga (A), **5** barca che orza sbandando, **6** contatto vero e chi cede (regole 12 e 13), **7** come funziona il torneo.

**Modello più semplice.** Stessa struttura delle lezioni di oggi (`contenuti.js`: passi con testo, passi pratici con `cond` e `hold`, ripasso a risposte chiuse). Ogni lezione breve ha **da 2 a 4 passi**, di cui **uno solo pratico**, e un quiz di **4 domande**. Le lezioni 6 e 7 sono quasi solo di testo (la 6 con un passo guidato su un contatto costruito). Sono lezioni «dell'1b»: partono con la barca dell'1b (`lv 2`).

**Fonti.** Il testo si scrive in fermata 2 e **solo dopo** aver elencato per ogni lezione la fonte: le fisiche dell'1b hanno già le loro (stallo del timone: `archivio/PROPOSTA-STALLO-TIMONE.md`; spingi il boma: `archivio/PROPOSTA-SPINGI-BOMA.md`; scarroccio: Day 2017; orziera sbandando: F4; regole 12 e 13: F15). Per i salti di vento e la raddrizzata lunga le fonti vanno cercate in `FONTI-PUBBLICHE.md` e `CONTENUTI-DA-VERIFICARE.md`. **Dove una fonte non c'è, quel passo non si scrive** (principio 4) e lo dico. Parafrasi, mai copia.

**Da verificare nel codice prima di cominciare** (non l'ho fatto): se i passi delle lezioni possono dichiarare la barca dell'1b (oggi `freeEnv.lv` è delle sole regate e della navigazione libera) e come `collaudo_pilota_lezioni.py` guida i comandi nuovi (Z, A, Maiusc).

## 2. Replay

Per decisione di Ale (20 ottobre) il replay vale **solo nelle regate dei tornei** e «si ripete la situazione, non la regata al bit». «Rivedi» c'è già. **Proposta: per l'1b il replay è quello che c'è** (spezzone di 18 s, riproduzione a fine regata), verificando solo che si apra anche a fine regata del torneo. **«Ripeti da qui» (istantanea e ripristino) e le domande sugli incidenti non entrano nell'1b**: vanno con la fase 2 del coach e con il 2b. Motivo: servono un'istantanea dello stato del gioco e la sua prova di non scrittura (criteri S4 e S5 di `PROPOSTA-REGATA-COME-FONTE.md`), cioè un lavoro grosso che sposterebbe di molto la chiusura dell'1b.

## 3. Menu, esame, attestato e brevetto

**Menu.** Una sezione «1b» che raccoglie le sette lezioni, la «Regata nei salti di vento» e il torneo; in carriera si apre col brevetto del livello 1 (come il torneo oggi). Nel gioco libero è tutto aperto. **Vincolo:** il pannello del menu a 1360x650 senza pixel di eccesso nel caso peggiore.

**Meriti dell'1b (tutti numeri provvisori, ipotesi nostre da tarare col pilota, come per il livello 1):**

| Area | Punti | Massimo | Minimo (ipotesi) |
| --- | --- | --- | --- |
| Abilità | regate dell'1b chiuse senza penalità: 1 punto ciascuna su 4 del torneo | 4 | 2 |
| Conoscenza | 7 quiz brevi: 2 punti se giusto almeno l'80%, 1 se almeno il 60% | 14 | 7 |
| Competizione | torneo: 1° = 6, 2° = 4, 3° = 3, 4° = 2, +1 senza penalità (già in gioco) | 7 | 3 |
| Esperienza | 1 punto per lezione completata | 7 | 7 |

Il totale richiesto si fissa **dopo** le misure col pilota (regola dei semi: soglia scelta su un gruppo, confermata su un altro mai guardato). **Esame dell'1b:** 15 domande estratte da una banca di circa 28 (4 per lezione), soglia 80%, ripasso mirato se non superato: stesso meccanismo dell'1a, riusato com'è.

**Il punto che serve decidere (nome e posto del brevetto).** `VISIONE` §2 (19 ottobre) dice: alla fine di ogni «a» un attestato di partecipazione, alla fine di ogni «b» un brevetto («da regatante», da rivedere). Ma la 1.0 dà già, alla fine dell'1a, il «Brevetto di livello 1 · Timoniere di deriva» e il torneo si apre con quello. Due strade:
- **A (consigliata):** si tiene il brevetto dell'1a com'è e si aggiunge un **secondo brevetto, «Regatante», alla fine dell'1b**: sono i «brevetti progressivi» già proposti a settembre. Costo: un attestato in più; nessun collaudo dell'1a cambia.
- **B:** si rispetta alla lettera il 19 ottobre: l'attestato dell'1a si rinomina «attestato di partecipazione» e il brevetto passa all'1b. Costo: testi, porta del torneo e i collaudi `carriera`, `carriera_esame`, `carriera_intera` da riscrivere.

In entrambi i casi: «nessun valore legale» scritto, «brevetto» mai «patente», nessun marchio, nessun titolo che sembri ufficiale (principio 5). Il nome «Regatante» è generico, ma lo ricontrollo contro `PROGETTO.md` in fermata 2.

## 4. I tempi delle medaglie

Le medaglie sono delle **prove** (tempi di una manovra), e l'1b **non ha prove**: ha regate e torneo, che si valutano con il piazzamento. **Proposta: l'1b non ha medaglie** e il punto «tempi delle medaglie» della roadmap si chiude per l'1b con questa decisione. Se Ale vuole prove con la barca dell'1b, è un lavoro a parte (prove nuove, bande di tempo col pilota, ultime nell'ordine). Non ho verificato se le cinque prove dell'1a si possano giocare con la barca dell'1b.

## 5. Ordine e fette (un commit a sé, collaudi verdi)

| Fetta | Contenuto | Versione |
| --- | --- | --- |
| 1 | Lezioni 1-4 (comandi della barca: stallo, Z, raddrizzata, orziera) con quiz | 1.0.62 |
| 2 | Lezioni 5-7 (salti di vento, chi cede, torneo) con quiz | 1.0.63 |
| 3 | Menu 1b, meriti, esame | 1.0.64 |
| 4 | Brevetto (strada A o B), attestato, carriera intera | 1.0.65 |

## 6. Criteri misurabili (soglie scritte prima, attese nostre)

1. **Ogni passo pratico delle sette lezioni si completa guidando la barca** col pilota, su **30 semi su 30** per passo.
2. **Nessun passo si completa da solo:** con il pilota che non fa nulla, 0 completati su 30 semi, **e** il collaudo riporta quanti passi ha davvero valutato (devono essere tutti quelli pratici: un «nessun caso sbagliato» con zero casi non vale).
3. **Quiz non superabili a caso:** risposte casuali, 1000 prove per quiz, quiz superato (almeno l'80%) in meno del 5% delle prove; risposte tutte giuste: superato in 1000 su 1000.
4. **Esame dell'1b:** tutte giuste → superato; tutte sbagliate → non superato e ripasso mirato sulle lezioni giuste; i criteri E1-E6 dell'1a restano verdi.
5. **Carriera intera dell'1b** con il pilota, in una pagina caricata come la carica un giocatore (senza `#collaudo`): dal brevetto del livello 1 al brevetto dell'1b, 1 su 1 per seme, su 10 semi.
6. **Non-regressione:** il motore non cambia, quindi `polare.js` (30 casi), le uscite di `polare.js` e `raffiche_e_virate.js` e le due impronte devono essere **identiche carattere per carattere**; `collaudo_carriera_intera.py` dell'1a invariato (strada A).
7. **Pannello** del menu e delle lezioni a 1360x650 senza pixel di eccesso, anche con il testo più lungo.
8. Collaudi anche su Firefox per i nuovi (solo Chromium finora, vedi memoria del progetto).

## 7. Rischi

- Il testo delle lezioni dipende dalle fonti: se per un argomento non ce ne sono, la lezione resta più corta.
- Le quattro aree con numeri nuovi possono rendere il brevetto troppo facile o impossibile: per questo la taratura col pilota viene prima e Ale la prova a mano dopo.
- La scelta A/B tocca i salvataggi (azzerabili, non è un costo) e i collaudi della carriera (costo vero solo con B).

## 8. Decisioni per Ale

1. Strada **A** o **B** per il brevetto (§3).
2. Replay dell'1b = quello che c'è, senza «ripeti da qui» (§2): sì o no.
3. Nessuna medaglia nell'1b (§4): sì o no.
4. Numero e titoli delle sette lezioni: confermi l'elenco o ne vuoi altre.
