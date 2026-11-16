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
