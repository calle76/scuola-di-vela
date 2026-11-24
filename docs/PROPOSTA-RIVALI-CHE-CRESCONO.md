# Proposta: rivali che crescono, circuiti che si rifanno ogni anno (voce 82)

*Seconda stesura, notte del 24 novembre 2026, dopo le domande di Ale («vorrei che fosse una dinamica chiara, che valesse ora per tutti i livelli»; «ma come sono le regole nella realtà?»; «vai, A»). La prima (bravura in Deriva e scambi fra circuiti) è superata da questa. **Fermata 1: nessun codice nel gioco finché Ale non dà il via alle tappe.** Già fatta: la tappa 2 della prima stesura (albo d'oro, 1.3.54; esito in fondo).*

## Com'è oggi (letto nel codice il 24 nov)

- Due soli livelli di guida, principianti ed esperti, presi da un menu che nelle regate di Deriva non si vede: quasi sempre principianti.
- 10 rivali zonali e 10 nazionali, gruppi fissi. Il nazionale è in 12: tu, i dieci e il migliore dello zonale (`stDodicesimo`). Lo zonale è in 11.
- Le batterie in cui non corri si estraggono coi tratti (`stEstrai`).
- Sponsor a contratto (1-2 stagioni): decide lui in quale circuito corri. «Niente retrocessione automatica» (Ale, 14 nov).

## Come funziona nella realtà (F117-F118, lette la notte del 24 nov)

- **Non ci sono promozioni e retrocessioni fra singoli: ci si qualifica ogni anno.** ILCA 6 maschile 2026: le prime due Italia Cup hanno 140 posti, 30 ai primi della classifica nazionale dell'anno prima e 110 alle zone; poi le regate sono aperte. Optimist 2026: al campionato italiano 150 posti, 138 dalle selezioni zonali, gli altri a chi ha diritti internazionali o è campione in carica. Nelle norme nazionali FIV la parola «retrocessione» non c'è (cercata, non letta per intero).
- Chi non è fra i posti garantiti ripassa dallo zonale. Le selezioni zonali ILCA sono aperte a tutti. Se qualcuno rinuncia si scorre la classifica.
- Cambio di barca: nell'ILCA le zonali di fine stagione valgono già per l'anno dopo. Campionato italiano delle classi in doppio (scheda 420): ammissione libera.
- Promozioni e retrocessioni esistono nella lega tedesca **a squadre** (F88).
- **Non trovato:** regole per cui uno sponsor fa salire o lascia a piedi; quanta bravura si porta da una barca all'altra.

## Modello più semplice

**Bravura (quanto sei bravo) e posto (dove corri) sono due cose separate.**

1. **Bravura `c`: 0-100 per ogni barca** (`progress.rivali[nome].c = { deriva: 34, fiocco: 12 }`). 0 = il principiante di quella barca, 100 = l'esperto; in mezzo ogni parametro di guida è la media pesata. I tratti restano come sono.
2. **Tetto personale**, uno per persona e per tutta la carriera. Si cresce a fine stagione, sempre più piano vicino al tetto, un po' di più per ogni tappa vinta. Solo nelle stagioni.
3. **Cambio di barca:** chi sale porta il 40% della bravura (o quella che aveva già su quella barca, se è più alta). Chi torna ritrova la sua meno 10 (ruggine), una volta sola.
4. **Ogni livello ha due circuiti da 12:** zonale (tre batterie da 4) e nazionale (due da 6). In Deriva 24 posti con te dentro: 23 rivali, **3 nomi nuovi** da approvare. Il «dodicesimo» sparisce.
5. **Il nazionale si rifà ogni anno:** i migliori 9 del nazionale e i primi 3 dello zonale. Gli ultimi tre del nazionale tornano a qualificarsi dallo zonale. Vale per tutti, te compreso.
   - Sei fra i primi tre dello zonale ma scegli uno sponsor zonale: il posto passa al quarto.
   - **Sei negli ultimi tre del nazionale con un contratto nazionale ancora in corso: resti, con un posto riservato (scelta A di Ale, 24 nov).** In quel caso i migliori 8 rivali e non 9, così i posti restano 12. Finito il contratto, vale la regola di tutti.
6. **Fra i livelli** (quando ci sarà il Fiocco): a fine stagione uno sponsor chiama uno dei primi tre rivali del nazionale, senza bisogno di 100; l'ultimo dello zonale del Fiocco resta a piedi e torna nello zonale di Deriva. Se sali o scendi tu, uno in più fa il viaggio opposto: i posti restano sempre 24 per livello. Fino ad allora in cima non sale nessuno.
7. **I circuiti dove non corri** fanno la loro stagione a numeri (ordine estratto, i più bravi hanno più probabilità). Poi una riga: chi ha vinto, chi si è qualificato, chi è tornato allo zonale.
8. **Il tuo valore**, sulla stessa scala, stimato dai rivali che batti; è solo un'informazione, non cambia niente in acqua. Si registra una riga per stagione per te e per ogni rivale (circuito, posto, bravura a fasce): è la base della curva dei progressi (voce 56). Le fasce: poca, discreta, buona, molta esperienza.
9. **La barca aggressiva** in partenza: sorteggiata fra i rivali in acqua con `c` ≥ 70; nessuno, nessuna.
10. **Non cambiano:** regate della Scuola, stagione con un amico (stessi rivali dal codice), tornei e stagioni già cominciati.

**Semplificazioni da dichiarare nel gioco:** nella realtà quasi tutti i posti vengono dalle zone (110 su 140), qui 3 su 12; chi corre il nazionale corre anche gli zonali, qui no; lo sponsor che chiama o lascia a piedi e il posto riservato dal contratto sono invenzioni nostre (in un campionato giovanile ILCA la FIV può aggiungere fino a 3 atleti, F117); la quota di bravura che si porta è un'ipotesi.

## Misure di stanotte, prima di toccare il gioco (soglie scritte prima, commit a parte)

**In acqua** (`tests/misura_bravura.py`, regate lunghe del torneo col pilota, senza cambiare il gioco: i parametri dei rivali si scrivono nel torneo prima di aprire la regata; stesso seme, stessi tratti e stesso vento per ogni `c`):

| # | Cosa | Soglia |
| --- | --- | --- |
| G2 | Il numero si sente: 40 regate per ciascun `c` = 0, 25, 50, 75, 100 (semi 3801-3840), conferma su 3841-3880 | tempo medio d'arrivo dei rivali: da 0 a 100 almeno il 2% del tempo (se no «non misurabile» e la proposta va ripensata); mai peggio di più dell'1% salendo; a 50 fra il 25% e il 75% della distanza |
| G2b | Si sente in gara: regate a 6 barche con i cinque rivali a `c` = 0, 25, 50, 75, 100 mescolati | chi ha `c` più alto arriva davanti in almeno il 65% delle coppie 0-100, e la quota cresce con la distanza (0-25 < 0-50 < 0-100) |
| G5 | Peso F del numero nella forza del sorteggio, stimato da G2b su 3801-3840 | confermato su 3841-3880: scarto fra quota di vittorie stimata e vista ≤ 10 punti per ciascun `c` |

**A numeri** (`tests/simula_carriere_rivali.py`, 300 mondi da 30 stagioni, due livelli da 24 posti, tu in Deriva come uno dei 24, F da G5; regole scritte sopra):

| # | Cosa | Soglia |
| --- | --- | --- |
| S1 | I posti tornano sempre | 0 circuiti diversi da 12, 0 persone in due posti o in nessuno, su tutte le stagioni |
| S2 | Non vince sempre lo stesso | titoli al più vincente di ogni circuito nazionale ≤ 40% in media su 30 stagioni |
| S3 | Ritrovi i rivali, ma cambiano | rivali dello stesso circuito dopo 3 stagioni fra il 30% e l'80%; almeno 14 rivali diversi passati dal nazionale di Deriva in 10 stagioni |
| S4 | Restano diversi | distanza fra il più forte e il più debole del livello ≥ 25 alla stagione 30; media nazionale sopra la media zonale di almeno 10 alle stagioni 5, 10, 30 |
| S5 | Chi torna giù non sparisce | chi torna dal Fiocco allo zonale di Deriva si qualifica al nazionale entro 2 stagioni almeno il 50% delle volte |
| S6 | Lo zonale non diventa un muro | media dello zonale di Deriva ≤ 55 alla stagione 10 e alla 30; un giocatore da 50 si qualifica al nazionale entro 3 stagioni fra il 30% e il 90% delle volte (partendo alla stagione 1 e alla 10). Da 0 e da 100: solo riportati |

## Criteri per il codice (dopo il via)

| # | Cosa | Soglia |
| --- | --- | --- |
| G1 | I due estremi sono i livelli di oggi | parametri di `c` = 0 e 100 uguali a principianti ed esperti: 1000 rivali su 1000 per livello, stesso seme; regate identiche al bit 40 su 40 |
| G3 | Niente di già cominciato cambia | tornei, stagioni e contratti salvati prima, 20 su 20 identici; stagione con amico 20 su 20; Scuola e Allenamento «principianti» ed «esperti» 20 su 20 |
| G4 | Le regole del gioco sono quelle scritte qui | 200 carriere da 10 stagioni con le funzioni vere del gioco: S1-S4 di nuovo, più: scelta A, rinuncia al posto, quarto che entra, ognuna provata almeno 10 volte con un ricalcolo indipendente |
| G6 | Non diventa imbattibile | 4 stagioni del pilota all'inizio e 4 al decimo anno: solo riportate; la prova vera è di Ale e Lucio |
| G7 | Il tuo valore | su stagioni costruite con rivali noti, stima entro 15 punti dal vero nell'80% dei casi dopo una stagione; riga per stagione salvata e riletta uguale |
| G8 | Pannello e non-regressione | 0 px a 1360x650 nelle finestre nuove; salvataggi vecchi 20 su 20; `polare`, `raffiche_e_virate`, `impronta1b` come prima; 0 errori in Chromium e Firefox |

## Costanti nuove (tutte ipotesi nostre, senza fonte)

Partenza zonali 10-40 e nazionali 45-75; tetti zonali 50-100, nazionali 75-100; crescita 2,4·4·q² a stagione (q = quanto manca al tetto, in frazione) + 3·q per tappa vinta; 40% al cambio barca; ruggine 10; 9 + 3 posti; soglia 70 dell'aggressiva; fasce da 25.

## Rischi

- **Parametri a metà non danno per forza una guida a metà** (G2).
- **I numeri di oggi del torneo cambiano:** gli zonali non partono da 0. Collaudi e misure vanno riguardati.
- **Circuiti da 12:** lo zonale passa da 11 a 12 e le batterie da 4-4-3 a 4-4-4; finale, obiettivi degli sponsor, frasi e salvataggi usano questi numeri.
- **Salvataggi:** la carriera in corso riceve i numeri di partenza.

## Tappe del lavoro (dopo il via)

1. La bravura e la crescita (grossa). 2. Circuiti da 12 che si rifanno ogni anno, righe di fine stagione, scelta A (grossa). 3. Il tuo valore e la curva (media). 4. Il passaggio fra livelli: si scrive solo la regola e i dati salvati; il codice quando c'è il Fiocco.

## Esito della tappa 2 (1.3.54, 24 novembre 2026)

Fatta come scritta. G7 passa (`collaudo_finale.py` F6): 20 finali su 20 con vincitore e posto giusti, 19 su 19 con campione e scheda giusti, riquadro e schede 0 px a 1360x650. Il posto del giocatore si legge come «miglior posto» e, per le finali dell'albo, solo il vincitore: il posto di ogni finale è salvato (`pos`) ma non mostrato, per non allungare il riquadro. Numeri in `CHANGELOG.md` 1.3.54.
