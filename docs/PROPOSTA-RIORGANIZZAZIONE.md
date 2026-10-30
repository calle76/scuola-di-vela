# Proposta: riorganizzare il gioco in «La scuola» e «Livello 1»

30 ottobre 2026. **Fermata 1: nessun codice, nessuna misura nuova.** I numeri qui sotto sono contati sul codice di oggi (`wc -l`, `grep`). Nasce da un'idea di Ale (30 ottobre 2026, ultimo messaggio): fare il livello 2 (regolamento) nel motore, poi **riorganizzare tutto, tenendo il meglio, con la barca dell'1b fin dall'inizio, meno cose, meglio ordinate**. Se approvata, **supera** `PROPOSTA-COMPLETAMENTO-1B.md` (le sette lezioni brevi si fondono nella scuola; menu, meriti e brevetto dell'1b non si fanno) e l'impianto 1a/1b/2a/2b di `VISIONE-LIVELLI-E-CARRIERA.md` §2 (19 ottobre 2026).

## 1. L'idea, come l'ha detta Ale

**Scuola (livello 0).** Barca dell'1b (la 1a si butta). Lezioni e prove con medaglie: tutta la teoria, quello che c'è oggi più le regole di precedenza, i segnali e le bandiere. Navigazione libera, due regate senza torneo (come oggi), quiz, attestato. Volendo, l'indicatore delle sufficienze acquisite (abilità, conoscenza…). Fine.

**Livello 1.** Regate con la deriva (barca dell'1b), con registratore e moviola (e «momento clou»). Niente scuola con voto: lezioni solo per quel livello (per esempio sui segnali della giuria). Se nella scuola c'era il punto di punizione e qui ci sono i giri di penalità, i giri entrano come prova fra una lezione e l'altra. Niente attestati; uno o due tornei da **superare** (soglia di punti, non da vincere).

**Perché:** la teoria tutta all'inizio è coerente con il gioco; non si introducono segnali e bandiere al livello 3 solo per non appesantire il primo.

## 2. Cosa c'è oggi (contato)

| Cosa | Numeri |
| --- | --- |
| Codice | `index.html` 440 righe, `js/` 3.692 righe in 10 file (`regate.js` 970, `gioco.js` 800, `disegno.js` 707, `contenuti.js` 398, `registratore.js` 325, `motore.js` 209, `laboratorio.js` 125, `moviola.js` 100, `avvio.js` 43, `base.js` 15). Le righe sono lunghe |
| Contenuti | 6 lezioni (32 passi pratici), 5 prove con medaglie, 6 quiz (29 domande), esame, glossario, libretto con 4 aree di merito, attestato |
| Regate | 2 dell'1a, «Regata nei salti di vento», «Regata con i giri di penalità» (1.0.61), torneo T1/T2 |
| Collaudi | 65 script Python e 18 script di fisica (`tests/fisica/`); 54 collaudi nel giro `lancia_tutti.sh` |
| Documenti | 39 file in `docs/`, 39 file in `docs/archivio/` |

**Scoperta che cambia il costo del «butta la 1a».** La barca dell'1b **non è un'altra barca**: è la 1a con rami `S.lv === 2` sopra (`motore.js` 9 rami e 32 nomi come `RUD2`, `BOMA2`, `RADD2`; `gioco.js` 6; `regate.js` 1 e 22 nomi `lv2`; `disegno.js` 1). Le costanti di base (`BOAT`, la polare) servono a tutte e due. Quindi **buttare la 1a significa**: eliminare il ramo «senza `S.lv`» e rendere il ramo `lv2` l'unico; **non** significa togliere molto codice del motore. Il guadagno vero è nella chiarezza (niente più «1a/1b», niente `lv 2` che vuol dire 1b) e nei collaudi, non nelle righe.

Dei collaudi: 8 script nominano esplicitamente l'1a (`collaudo_giri`, `registratore_barche`, `torneo`, `contatto_vero`, `regole`, `semaforo`, `misura_avversari`, `scarroccio1b`); circa 35 nominano già la barca dell'1b. **La maggior parte dei collaudi è già sull'1b o neutra.** (Conteggio con `grep`, da rifare a fondo nella fermata 2.)

## 3. La struttura proposta

| | Scuola (livello 0) | Livello 1 |
| --- | --- | --- |
| Barca | dell'1b (unica) | dell'1b |
| Lezioni | tutte le teoria: le 6 di oggi riscritte per la barca dell'1b (con dentro le sette «brevi»: timone che stalla nella lezione sul timone, Z nella partenza da fermo, ecc.), più precedenze 10-18, segnali e bandiere, partenza | solo quelle che servono al livello (segnali della giuria vista in regata, uso del registratore e della moviola) |
| Prove | le 5 di oggi con medaglie, tarate di nuovo | i giri di penalità come prova fra lezioni (dalla fetta 1 del 2a) |
| Regate | 2 senza torneo | regata dei salti di vento, regata con i giri, **uno o due tornei da superare** |
| Libero | navigazione libera | — |
| Ripasso | quiz, esame, indicatore delle aree di merito (abilità, conoscenza…) | — |
| Riconoscimento | attestato (uno solo) | nessuno; superare la soglia apre il livello dopo |
| Registrazione | già automatica (1.0.60) | registratore, moviola, momento clou (coach) |

La **soglia** del torneo usa la Competizione dei meriti già costruita; il numero si fissa col pilota (regola dei semi: soglia scelta su un gruppo, confermata su un altro mai guardato).

## 4. Cosa si tiene, cosa si riscrive, cosa si butta

**Si tiene (contenuto verificato):** motore e base fisica (`BOAT`, polare), tutta la fisica dell'1b e le sue due impronte, fonti (`FONTI-PUBBLICHE.md` F1-F40 e `fonti-pdf/`), testi di lezioni e quiz, glossario, banca dell'esame, libretto e meriti, disegno dell'attestato, registratore e moviola, tornei T1/T2 e punteggio del regolamento, giri di penalità (1.0.61), il pilota dei collaudi e la maggior parte dei collaudi.

**Si riscrive:** le lezioni, per la barca dell'1b (nuovo comportamento di orza/poggia con timone che stalla: i 32 passi vanno percorsi di nuovo dal pilota); i tempi delle medaglie delle 5 prove (`collaudo_fasce.py`: oro = tempo del pilota); le 2 regate della scuola con avversari dell'1b; menu e carriera (scuola → attestato → livello 1 → soglia); la parola «1a/1b» nel gioco, nel codice (`lv 2`) e nei documenti.

**Si butta:** la barca 1a come scelta (il ramo senza `S.lv`), il suo selettore «Barca», gli avversari dell'1a, le regate dell'1a e i loro record, le impronte dell'1a (resta `impronta1b.js`), il «Brevetto di livello 1 · Timoniere di deriva» così com'è (diventa l'attestato della scuola), la distinzione 1a/1b del menu. I salvataggi (record, medaglie, meriti) si azzerano (nessun costo, vedi memoria del progetto).

## 5. Ordine proposto

0. **Prima di tutto, una misura (nessun cambio):** come va un principiante sulla barca dell'1b (§6, M1). È il vero rischio e decide se l'idea regge così com'è.
1. **Finire nel motore il 2a** (come ha detto Ale): un giro per la boa toccata, regole 11-13 nella colpa, 21.2, segnali 5-4-1-0 con bandiere, regola 18 e 14 dove le fonti bastano, **giri di penalità anche per gli avversari** (promemoria di Ale). Sono i contenuti che la scuola e il livello 1 devono insegnare.
2. **Pulizia del codice:** il ramo `lv2` diventa l'unico; stesse uscite delle impronte dell'1b (§6, M4).
3. **Lezioni e prove della scuola** riscritte (con le fonti per ogni lezione prima del testo).
4. **Tarare medaglie e soglia del torneo** col pilota (per ultimi, come da regola di metodo).
5. **Menu, carriera, attestato.**
6. **Livello 1:** lezioni proprie, tornei da superare, coach (momento clou).
7. Documenti: `VISIONE-LIVELLI-E-CARRIERA.md`, `ROADMAP.md`, `STATO.md`, `DECISIONI.md`, `PROGETTO.md` riscritti più corti; l'impianto vecchio va in `docs/archivio/`.

Ogni passo è una o più versioni con collaudi verdi e commit a sé. Il gioco **resta giocabile e rilasciabile** a ogni passo fino al 4; la fusione di menu e carriera (5) è il momento in cui la vecchia struttura sparisce.

## 6. Criteri misurabili (soglie scritte prima, attese nostre)

- **M1, principiante sulla barca dell'1b** (passo 0, solo misura): sul testo e sui passi di oggi (lezioni 1-3), pilota «da principiante» (reazioni in ritardo di 0,3-0,6 s, tutti i comandi che servono, nessun uso di Z o di Maiusc) sulla barca dell'1b, 30 semi per passo. Attese: **scuffie in meno del 5% dei passi** nelle lezioni 1-3 (senza raffiche forti), **passo completato in almeno 25 semi su 30**. Se non lo regge, la scuola parte con aiuti accesi e una prima lezione dedicata (decisione di Ale). **Il metro dichiara anche quanti passi ha davvero valutato** (non vale «nessuna scuffia» con zero passi). **Limite dichiarato:** nessuna misura dice se un principiante vero «si diverte»: lo dirà la prova a mano di Ale e di Lucio.
- **M2, tutto raggiungibile:** il pilota completa i 32 passi riscritti e le 5 prove con medaglia (30 semi su 30 per passo), anche in una pagina caricata come la carica un giocatore (senza `#collaudo`).
- **M3, medaglie:** oro raggiungibile dal pilota in tutte le prove (almeno 25 prove su 30 sotto la banda d'oro), bronzo entro il tempo del pilota con errori tipici; nessuna banda a occhio.
- **M4, pulizia:** dopo aver tolto il ramo senza `S.lv`, `impronta1b.js` identico carattere per carattere; le uscite di `polare.js` (30 casi) e `raffiche_e_virate.js` hanno **nuovo riferimento dichiarato** (cambia il metro: oggi misura la 1a) e dei 30 casi si controlla che i valori della 1b non siano cambiati rispetto a prima.
- **M5, soglia del torneo:** pilota di prova, 40 tornei sui semi 1-20 e 101-120: soglia scelta in modo che lo superi circa il 70-80% (attesa nostra), confermata su un altro gruppo mai guardato.
- **M6, carriera intera nuova:** dalla scuola all'attestato, al livello 1, alla soglia, 1 su 1 per seme su 10 semi.
- **M7, pannello** del menu a 1360x650 senza pixel di eccesso, caso peggiore.
- **Firefox** per i collaudi nuovi (finora solo Chromium).

## 7. Rischi

- **Troppo difficile per chi comincia** (M1). Aiuti già esistenti (barra che torna al centro, «gira la prua», suggerimenti) potrebbero bastare, o servire una lezione d'avvio più dolce.
- **Gli avversari dell'1b diventano il cuore del livello 1 e della scuola.** Difetti noti: tagliano fuori dagli estremi (16% dei tagli), boe sbagliate, tre barche alla boa. Il «pazienza» del 30 ottobre va riguardato: se il passaggio di livello dipende da loro, conta.
- **Troppo in una volta:** il passo 5 tocca menu, carriera, salvataggi, 5 collaudi della carriera e quelli del libretto. Si fa solo con le fasi 1-4 verdi.
- **Teoria tutta all'inizio** è tanta da ricordare: il coach (fase 2) deve poter riportare l'errore alla lezione («rivedi la lezione 7»), altrimenti la scuola resta un deposito di nozioni.
- **Documenti vecchi** (`VISIONE`, `ROADMAP`, `CLAUDE.md`, vecchi nomi 1a/1b) restano incoerenti finché il passo 7 non è fatto.
- **Prototipo del fiocco** (`sperimentale/`) nato da una copia di `index.html` con la 1a: non lo tocca questa riorganizzazione, ma la sua regola di non-regressione («la barca senza fiocco identica a quella del gioco») va riscritta sulla barca nuova.

## 8. Decisioni di Ale (30 ottobre 2026, sera)

1. **Nomi:** la scuola è il livello 0, «La scuola»; il livello 1 si chiama **«Deriva»**; poi «Fiocco» e gli altri (i nomi al posto dei numeri).
2. **Niente più brevetti** (nemmeno un livello 1 «superato» con quel nome): i livelli successivi si aprono se la carriera lo permette (soglia del torneo). L'attestato resta uno solo, quello della scuola.
3. **Principiante:** non preoccupa. È una scuola, si impara e si gareggia contro avversari deboli. La misura M1 non è più una condizione per partire (resta come numero da riportare, non come porta). **Idea nuova:** la vela che si manovra da sola come **opzione** (il gioco ha già `autoTrim` in alcuni passi delle lezioni: da vedere cosa serve per farne un'opzione vera).
4. **Momento clou:** quando decide Claude, nel coach.

Da fare quando si riprende: aggiornare M1 (non più porta), scrivere la fermata 1 della vela automatica come opzione, poi il 2a nel motore (passo 1 dell'ordine in §5).
