# Proposta: disegno della vela vista dall'alto (osservazione 41)

16 ottobre 2026. **Fermata 1:** il gioco non è stato toccato. La prova è stata fatta su una copia, in una cartella temporanea.

## Il difetto

**[codice]** In `drawBoat` (`js/disegno.js`, sottosezione «barca», «randa e boma») il contorno della vela va:
1. dall'albero, con una curva, fino a un punto vicino alla **fine del boma**;
2. da lì, con un tratto dritto, alla fine del boma;
3. lungo il boma, di nuovo all'albero.

Vista dall'alto la parte alta della vela risulta quindi lunga quanto il boma: un cuneo largo anche in cima.

**Come dovrebbe essere [giudizio, geometria]:** la randa è un triangolo, con la base sul boma e la cima (la penna) in testa d'albero. Dall'alto la balumina (il bordo libero) torna dalla fine del boma **verso l'albero**, gonfia sottovento per il grasso della vela e lo svergolamento.

## La proposta

Il contorno diventa:
1. dall'albero alla fine del boma, con la base appena gonfia sottovento;
2. dalla fine del boma alla penna, con la balumina gonfia sottovento;
3. dalla penna all'albero (un tratto cortissimo: sbandando, la penna si sposta sottovento).

- **Le stecche** si appoggiano alla balumina nuova.
- **I filetti restano esattamente dove sono** (stessi punti di oggi).
- **Il grasso, lo svergolamento e la vela che sbatte** usano gli stessi valori di oggi.
- **Codice:** circa 8 righe cambiate in `disegno.js` (vela, albero, segnavento). La fisica non cambia.

**Prima e dopo** (di bolina, al traverso e al lasco): `tests/output/vela/confronto.png`, generata con `confronto.html` nella stessa cartella. La cartella non va in git.

## Seconda prova, dopo l'osservazione di Ale (stesso giorno)

**Ale:** sbandando, la cima dell'albero va da una parte e la vela sembra attaccata a qualcos'altro; la vela deve inclinarsi seguendo l'albero.

**[codice] La causa:** l'albero disegnato finisce a 5,5 × seno dello sbandamento sottovento, mentre la cima della vela si spostava solo di 2,6 × seno (sia oggi sia nella prima prova). Inoltre il segnavento restava alla base dell'albero, che dall'alto coincide con la cima solo a barca dritta.

**Correzione provata:** un solo punto, la **testa d'albero** (5,5 × seno dello sbandamento sottovento). Lì finisce l'albero disegnato, lì è attaccata la penna della vela, e lì sta il segnavento. Sbandando, l'albero si sdraia e si porta dietro la vela e il segnavento.

Schermate: `tests/output/vela/confronto2.png` (bolina dritta e a 15°, traverso a 15° e 30°; in alto oggi, in basso la proposta).

## Criteri della fermata 2

1. **Cambiano solo le immagini del mare:**
   - `collaudo_impronta.py`, con riferimento preso subito prima, deve dare diverse **solo** le scene con l'immagine del mare;
   - stato delle barche, testi e registro identici al bit;
   - si riporta quante scene cambiano.
2. **Niente altro cambia:** `polare.js` e `raffiche_e_virate.js` identici; pannello a 1360×650 senza eccesso.
3. **Il giudizio a occhio è di Ale,** sulle schermate e giocando:
   - anche con la barca sbandata;
   - con la vela che sbatte;
   - durante la strambata.
4. **Versione 1.0.7** e voce nel `CHANGELOG.md`.

## Rischi

- **Un tratto disegnato fuori posto in casi non provati.** Barca sbandata molto, boma che passa da un lato all'altro, scuffia (in scuffia il disegno è un altro, «albero e vela distesi sull'acqua», e non si tocca): si guardano nelle schermate della fermata 2.
- **Il gonfiore della balumina è una scelta a occhio** (×1,6 sul grasso più lo svergolamento): si regola guardando le schermate, non c'è una fonte.

## Decisione di Ale (16 ottobre 2026)

Via alla fermata 2 con la seconda prova: vela, albero e segnavento attaccati alla stessa testa d'albero. Sul segnavento:
- Ale lo trova innaturale quando finisce disegnato sopra la vela; ma deve seguire la cima dell'albero, non restare fermo;
- se giocando disturba, si rende più leggibile oppure si toglie, insieme ai testi della lezione 4 e del glossario che lo nominano.

Sullo sbandamento: Ale nota che fra 15° e 30° il disegno cambia poco. Con la vela attaccata all'albero si vedrà meglio; se non basta, diventa un'osservazione a parte.
