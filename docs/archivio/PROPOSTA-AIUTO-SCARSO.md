# Proposta: l'aiuto «scarso / buono» in regata

*Fermata 1, 16 novembre 2026 sera. Nessun codice nel gioco finché non arriva il via di Ale.*

## Da dove viene

Ale, 16 novembre sera: «nella pratica del gioco come faccio a capire se cambiare mura? mentre faccio le regate come applico queste tattiche?». Nella lezione 11 un suggerimento in basso dice «Sei scarso di 10°: vira adesso»; in regata non c'è niente, e il conto a mente (Prua contro vento medio, circa 50° normale, 60° scarso, 40° buono) mentre si timona è scomodo. Proposta in chat, «ok» di Ale.

## Cosa si vede (modello più semplice)

- In basso a destra, sotto la scritta del vento medio che c'è già (per esempio «N (000°), 10 nodi»), una riga piccola: **«scarso 10°»** (arancione), **«buono 8°»** (verde) o **«nella media»** (bianco).
- Il numero è **lo stesso che usa la lezione 11** (`base.scarso` in `js/gioco.js`): di quanti gradi il vento, dove sei, è girato verso la tua prua rispetto al vento medio. Soglie uguali alla lezione: scarso da 7°, buono da 3°.
- Compare **solo** se il vento gira (regata nei salti di vento, torneo) e **solo di bolina** (barca fra 35° e 75° dal vento, come nella lezione). In poppa, al lasco e prima del via no.
- **Non dice «vira».** Dice com'è il vento: la decisione resta al giocatore. Con il vento che gira sempre dalla stessa parte (una regata su tre) l'aiuto continuerà a dire «scarso» sulla stessa mura: è proprio il segnale che il vento non torna (cautela 2 della risposta di Ale), e lì virare a ogni scarso è sbagliato.
- **Si spegne** nelle Impostazioni, come la layline: «Scarso/buono: no / regate / anche torneo».

## Semplificazione da dichiarare

Il gioco conosce il vento vero e il vento medio esatto; un velista vero ricava lo scarso dalla bussola e da una media che si è fatto a occhio prima del via (F41, l'allenatore citato nella lezione 11). L'aiuto quindi è più preciso di quanto può essere un velista: va detto nel testo dell'opzione («il gioco conosce il vento medio; in mare lo stimi con la bussola») e nella lezione 11 (una riga nel riepilogo, se il pannello la tiene).

## Costanti

Nessuna nuova: 7° e 3° sono quelle della lezione 11 (scelte nella 1.1.8 e 1.2.26), 35-75° è la bolina della lezione. Colori: quelli già usati per i suggerimenti.

## Criteri (soglie: attese nostre)

| | Cosa | Soglia |
| --- | --- | --- |
| S1 | **Con l'aiuto spento il gioco non cambia**: `impronta1b.js` al bit, `polare.js` e `raffiche_e_virate.js` identici; 20 regate del torneo con semi fissi, stesse classifiche e stesse registrazioni con l'aiuto acceso e spento (l'aiuto disegna, non tocca la barca) | 0 differenze su 20 |
| S2 | **Il numero mostrato è quello della lezione**: pilota automatico nella regata nei salti di vento, 10 semi, un campione al secondo di bolina; confronto fra il numero scritto e `base.scarso` arrotondato | 0 differenze, con almeno 500 campioni misurati (altrimenti il collaudo fallisce) |
| S3 | **Compare solo dove deve**: 0 fotogrammi con la scritta nelle regate della Scuola (vento fisso), in poppa/lasco, prima del via, nelle lezioni; e almeno 1 fotogramma con la scritta in ciascuna delle tre forme (scarso, buono, media) | 0 fuori posto; tutte e tre le forme viste |
| S4 | **Spazio**: a 1360x650 la scritta non copre bussola, «R», vento e layline; la finestra delle Impostazioni con la riga nuova resta senza pixel di eccesso (`collaudo_pannello.py`, `collaudo_menu_livelli.py`), Chromium e Firefox | 0 px |
| S5 | **Il consiglio è buono** (misura del contenuto, non del codice): pilota da giocatore (`tests/pilota_giocatore.js`) nella regata nei salti di vento solo con vento oscillante, 20 semi di scelta + 20 di conferma mai guardati; versione A vira quando l'aiuto dice scarso ≥7°, versione B vira a tempo come oggi. Attesa: A arriva prima di B in almeno 13 regate su 20 sui semi di conferma | 13/20; se non passa si riporta com'è e si ridiscute il testo, non le soglie |

S5 è l'unico che può dire «la tattica nel gioco non rende»: se succede, prima di toccare l'aiuto si guarda perché (virate troppo lente? oscillazioni troppo corte, 60-75 s per mezza oscillazione contro i circa 4 minuti dell'esempio della fonte?).

## Domande per Ale (una per volta)

1. **Torneo:** l'aiuto parte acceso anche nel torneo, o come la layline solo nelle regate a tema («regate»)? Proposta: come la layline.
2. **Carriera:** vale anche lì (è un aiuto disattivabile, principio 3)? Proposta: sì.

## Rischi

- La scritta in basso a destra è in un angolo già pieno (vento, bussola, «R», layline): S4 potrebbe chiedere di spostarla vicino alla Prua del pannello, che però ha meno spazio.
- Chi impara a guardare solo l'aiuto non impara la bussola: per questo si spegne e la lezione 11 continua a insegnare il conto a mano.
- S5 costa tempo di calcolo (80 regate col pilota): sul PC di Ale una misura per volta, col freno.

## Lavoro stimato

Codice: una funzione di disegno in `js/disegno.js`, una riga nelle Impostazioni (`index.html`, `js/gioco.js`), un collaudo nuovo (`collaudo_aiuto_scarso.py`, S2-S3). Versione nuova del gioco (1.3.18).

## Fermata 2 (22 nov 2026, via di Ale: «ok completiamo l'argomento», dopo la misura della voce 77)

Fatto come scritto, con queste differenze **dichiarate prima di vedere i risultati del collaudo**:

- **Posto:** sotto la scritta del vento non c'è spazio (sta sul bordo in basso); la riga sta **sopra la bussola**, centrata su di lei, nello spazio libero.
- **Opzione:** «Scarso/buono» nelle Impostazioni, accanto a «Layline», con gli stessi tre valori e lo stesso predefinito («regate»). Il titolo dell'opzione dice la semplificazione («il gioco conosce il vento medio; in mare lo stimi con la bussola»). La riga nel riepilogo della lezione 11 non si aggiunge (la lezione insegna già il conto a mano).
- **S1** in Firefox su 5 regate invece di 20 (come per la vista Q, deciso con Ale il 22 nov: la proprietà è del codice, Chromium la prova su 20). Si aggiungono `impronta1b.js`, `polare.js`, `raffiche_e_virate.js`.
- **S2:** il metro è il vento sulla barca letto dal collaudo con `windAt` prima del passo (quello che il gioco mette in `local`), vento medio e prua: stessa formula di `base.scarso`, letta fuori dal disegno; si confronta con la scritta davvero disegnata.
- **S4:** margine misurato nella pagina fra la scritta e «N», bussola e scritta del vento (almeno 2 px), più `collaudo_pannello.py` e `collaudo_menu_livelli.py` per la riga nuova delle Impostazioni.
- **S5 non si lancia:** il contenuto lo ha già misurato la voce 77 (`PROPOSTA-COACH-SCARSO-VERIFICA.md`, 120 regate): col vento scarso di almeno 7° la rotta ottimale vira subito nell'88-92% dei momenti, col buono nel 41-43%. Se Ale vuole anche S5 (80 regate col pilota da giocatore), si fa a parte.
- **Insieme (voce 77, proposta A):** la frase del Coach diventa «Il vento ti è scarso di N°: se oscilla, conviene virare; se continua a girare dalla stessa parte, no (lezione 11).»

## Esito (1.3.42, 22 nov; `tests/collaudo_aiuto_scarso.py`, soglie non cambiate)

| | Chromium | Firefox |
| --- | --- | --- |
| S1 torneo identico al bit, aiuto acceso e spento | 20 su 20 | 5 su 5 |
| S2 numero scritto contro il conto | 0 diversi su 2139 | 0 su 2155 |
| S3 fuori posto (regata nei salti / Scuola / lezione 11 / torneo con «regate») | 0 su 4509 / 0 / 0 / 0 | 0 su 4507 / 0 / 0 / 0 |
| S3 forme viste | scarso, buono, nella media | uguale |
| S4 margine da bussola e «N» | 4,0 px | 4,0 px |

**S2 alla prima stesura è fallito per un difetto del metro**, non del gioco: il collaudo leggeva il vento prima che il passo spostasse le raffiche (6 diversi su 2139, tutti di 1° all'arrotondamento). Corretto il metro (vento nel punto e nell'istante del passo), soglia invariata, rilanciato: 0. `collaudo_pannello`, `collaudo_menu_livelli` e `collaudo_coach_regata` OK in Chromium; fisica identica. S5 non lanciato (vedi sopra).
