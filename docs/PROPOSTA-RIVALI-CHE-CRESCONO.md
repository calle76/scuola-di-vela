# Proposta: rivali che crescono e finale che resta (voce 82)

*Fermata 1, 24 novembre 2026. Idea di Ale: «non c'è livello ma punteggi che fanno crescere le capacità». Nessun codice nel gioco finché non arriva il via.*

## Com'è oggi (letto nel codice il 24 nov, provato in pagina dove detto)

- **Livello:** due soli, principianti ed esperti. Torneo e stagione prendono `opt.aiLevel` quando cominciano, e se lo tengono. La scelta si vede solo nelle regate della Scuola e torna «principianti» a ogni ricarica (provato): quasi sempre si corre coi principianti.
- **Rivali:** 10 zonali e 10 nazionali, gruppi fissi. Ognuno ha due tratti (partenza, bolina: dote, media, difetto) che restano. Solo il rivale meglio piazzato dello zonale corre anche il nazionale (`stDodicesimo`).
- **Parametri di guida** (`aiTratti`): angolo di bolina e di poppa, errore di regolazione, ritardo in partenza, timone, lunghezza dei bordi. Fra i due livelli cambiano i numeri; con gli esperti c'è in più una barca aggressiva in partenza (`sorteggiaAggressiva`).
- **Batterie in cui non corri:** ordine sorteggiato coi tratti (`stEstrai`). La guida in acqua non c'entra.
- **Finale:** il miglior posto si salva (`progress.finaleFatta`) e nessuna riga lo rilegge. Dà un titolo in una frase e niente altro.

## Modello più semplice

**Tappa 1: il numero.**
1. Ogni rivale ha un numero da 0 a 100 (`progress.rivali[nome].c`). 0 = il principiante di oggi, 100 = l'esperto di oggi; in mezzo ogni parametro è la media pesata dei due: `p·(1−c/100) + e·c/100`. I tratti restano come sono.
2. All'inizio: zonali 10-30, nazionali 45-70. Ognuno ha anche un **tetto personale** (zonali 50-100, nazionali 75-100), sorteggiato una volta.
3. Cresce a fine stagione: un po' per ogni tappa corsa, un po' di più se l'ha vinta, sempre più piano vicino al tetto. Solo nelle stagioni: i tornei singoli non cambiano niente, così non si può farli crescere apposta.
4. Nella scheda: «Esperienza: poca, discreta, buona, molta» (quattro fasce), e cosa ha vinto. Il numero non si mostra.
5. La barca aggressiva si sorteggia fra i rivali in acqua con c ≥ 70; se non ce n'è, nessuna.
6. Nel torneo e nella stagione il testo «(principianti)» diventa l'elenco delle fasce. Nell'Allenamento la scelta diventa «come sono oggi / principianti / esperti».
7. **Non cambia:** le regate della Scuola (`opt.aiLevel`), la stagione con un amico (i due giochi devono avere gli stessi rivali: livello dal codice), tornei e stagioni già cominciati.

**Tappa 2: la finale che resta** (può andare prima o senza la 1).
8. **Albo d'oro:** `progress.albo`, una riga per finale corsa (chi ha vinto, il tuo posto), mostrata nel riquadro della finale col tuo miglior posto. Le finali non corse da te non ci sono (semplificazione).
9. **Campione in carica:** il nome di chi ha vinto l'ultima finale nella sua scheda, o «sei tu». Solo testo, nessuna guida diversa.

**Tappa 3: salire e scendere** (da decidere dopo aver giocato la 1). A fine stagione il primo dello zonale sale e l'ultimo del nazionale scende. I circuiti oggi sono liste fisse usate da sorteggi, stagione, finale e obiettivi degli sponsor, e il nazionale ha già un dodicesimo che viene dallo zonale: vanno ripensati insieme. È la parte più grossa. Per il giocatore resta «niente retrocessione» (`DECISIONI.md`, 14 nov).

Fuori: chi passa al fiocco. Il numero resta salvato per quando servirà.

## Perché il tetto personale

Le quattro regole dette ad Ale il 24 nov avevano tetto 100 per tutti. Le ho simulate (`tests/simula_crescita_rivali.py`, 300 mondi da 30 stagioni, soli rivali, F = peso del numero nella forza, non misurato):

| Regola (F = 4; con F = 2 e 8 cambia poco) | Titoli al più vincente | Rivali con c ≥ 90 dopo 10 / 30 stagioni | Distanza fra il più forte e il più debole dopo 30 |
| --- | --- | --- | --- |
| Solo chi vince cresce (+8 a vittoria) | 23% | 5 / 17 su 20 | 44 |
| Le quattro regole, tetto 100 | 22% | 0 / 0 | **10: tutti uguali** |
| Tetto personale | 23% | 0 / 0 | 36 |

Due cose: **il rischio «vincono sempre gli stessi» non esce** con nessuna regola (nel sorteggio delle tappe il caso pesa molto; la simulazione però non ha barche in acqua). **E le mie quattro regole appiattivano tutti.** Nella simulazione «tetto personale» la crescita è 2,4·4·q² a stagione (q = quanto manca al tetto) + 3·q a tappa vinta: sono numeri di prova.

## Criteri (soglie nostre, scritte prima)

| # | Cosa | Soglia |
| --- | --- | --- |
| G1 | I due estremi sono i livelli di oggi | parametri di c = 0 e c = 100 uguali a principianti ed esperti: 1000 rivali su 1000 per livello, stesso seme, e regate identiche al bit 40 su 40 (Chromium) |
| G2 | In mezzo si guida in mezzo | 40 regate del torneo col pilota per ogni c = 0, 25, 50, 75, 100 (semi 3801-3840): arrivo medio dei rivali che non peggiora mai di più dell'1% salendo di c; a c = 50 fra il 25% e il 75% della distanza fra i due estremi. Confermato su 3841-3880. Se la distanza fra gli estremi è sotto il 2% del tempo, il criterio non è misurabile e si dice |
| G3 | Niente di già cominciato cambia | torneo e stagione salvati prima, 20 su 20 identici; stagione con amico: calendario, batterie e regate identici 20 su 20; regate della Scuola e Allenamento «principianti» ed «esperti» identici 20 su 20 |
| G4 | La crescita resta nei limiti | 200 carriere da 10 stagioni con la funzione vera del gioco: nessuno oltre il suo tetto, nessuno scende, distanza fra il più forte e il più debole ≥ 25, rivali con c ≥ 90 al massimo 6 su 20, più vincente ≤ 40% dei titoli |
| G5 | Le batterie non corse seguono il numero | la forza del sorteggio usa c; tarata sulle regate vere (semi 3801-3840), confermata su 3841-3880: scarto fra la quota di vittorie sorteggiata e quella in acqua ≤ 10 punti |
| G6 | Non diventa imbattibile | 4 stagioni del pilota all'inizio e 4 con i rivali al decimo anno: solo riportate, perché il pilota non è un giocatore; la prova vera è di Ale e Lucio |
| G7 | Finale | 20 finali col risultato scritto dal collaudo: albo e campione giusti, visibili, ricaricati uguali, cancellati da «Azzera i progressi» |
| G8 | Pannello e non-regressione | 0 px a 1360x650 nelle schede coi testi nuovi; salvataggi vecchi 20 su 20; `polare`, `raffiche_e_virate`, `impronta1b` come prima; 0 errori in Chromium e Firefox |

## Costanti nuove (tutte ipotesi nostre)

Partenza 10-30 e 45-70; tetti 50-100 e 75-100; velocità di crescita; soglia 70 dell'aggressiva; fasce della scheda (quattro da 25). Nessuna fonte: sono scelte di gioco, non di nautica.

## Rischi

- **Guida a metà strada:** un parametro a metà non dà per forza una guida a metà (G2 lo misura). I tratti sugli esperti si vedevano poco (bolina 5 su 10, `PROPOSTA-TRATTI-RIVALI.md`).
- **Tutti i numeri del torneo cambiano un po'**, perché gli zonali partono a 10-30 e non a 0: collaudi e misure che usano i rivali del torneo vanno riguardati.
- **Salvataggi:** chi ha una carriera in corso riceve i numeri di partenza; niente conversioni (`DECISIONI.md`: lo storico si può azzerare).
- **Stima:** tappa 1 grossa (Opus), tappa 2 piccola, tappa 3 grossa.

## Cosa serve da Ale

Il via, tutto o a tappe. **Consiglio:** prima la 2 (piccola), poi la 1, la 3 solo dopo aver giocato la 1.

Trovato strada facendo, da correggere comunque: la registrazione scrive `avversari=` dal menu e non dalla regata (provato: allenamento con esperti scritto «principianti»); per questo il «principianti» delle 8 regate lunghe della voce 2 è da verificare.
