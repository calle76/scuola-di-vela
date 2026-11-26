# Voce 91: poco timone in raffica con la barca M (studio, 27 novembre 2026, Opus; gioco invariato)

**Il difetto** (`sperimentale/barca-84/controllo/CONTROLLO.md`): `orziera1b.js` criterio 4, raffica 14 → 22 nodi di bolina a scotta ferma, il pilota tiene la prua con **6,9° di barra** al massimo (1.3.58: 35°; soglia nostra: oltre 20°). Lascando 0,3: 3,3°.

## 1. La causa non è quella supposta

Si pensava che la vela che si appiattisce da sola togliesse l'orziera. Misurato sul banco (`orziera1b.js`, raffica col pilota), la 1.3.61 contro la 1.3.58 (motore dal tag):

| | 1.3.61 (M) | 1.3.58 |
| --- | --- | --- |
| momento che fa orzare, massimo (spinta × altezza × sen sbandamento) | 293 N·m | 314 N·m |
| sbandamento massimo | 37° (poi torna a 6° in 3 s) | 65° (resta oltre 59°) |
| velocità dopo 3,5 s | 4,7 nodi | **1,0 nodi** |
| barra massima | 6,4° | 35° (cresce mentre la barca rallenta) |

**Il momento è quasi uguale.** I 35° della barca vecchia venivano dal fatto che sbandava fin quasi alla scuffia e si fermava, e un timone lento morde poco. La barca M sbanda meno, si raddrizza da sola (vela piatta e svergolata) e tiene la velocità: il timone basta. Il criterio 4 era tarato su quella barca, non su una misura.

## 2. Fonti cercate (27 nov)

Nessuna dà gradi di barra in raffica per una deriva. Dicono il meccanismo:
- sbandando il centro velico va sottovento e nasce un momento che il timone deve bilanciare (Chalmers, ILCA 7; Wikipedia «Weather helm»);
- **lo scafo sbandato e asimmetrico aggiunge momento** (serie sistematica di Delft, DSYHS, con misure in vasca di momento di imbardata a vari sbandamenti): nel motore è lasciato fuori dalla 1.0.46 perché F4 non dà numeri;
- sbandando la parte orizzontale della forza del timone cala (serve più barra), e con la raffica la vela cresce più del timone fino all'orzata (blog di Nauticed).

## 3. Prove su copia (gioco invariato)

- **Forza del timone × cos(sbandamento)** (terzo punto delle fonti): barra massima 6,9 → **8,8°**; polare identica. Da solo non basta per i 20°.
- Restano: (a) il momento dello scafo sbandato dalla DSYHS (Keuning e altri), da leggere: dà numeri per scafi di barche a chiglia, da riportare a una deriva con un'ipotesi; (b) cambiare il criterio.

## 4. Cosa propongo

**Non toccare la barca ora.** Due strade, da scegliere con Ale:
1. **Tenere M com'è e riscrivere il criterio 4** sul rapporto fra scotta ferma e lascata (oggi 6,9 / 3,3 = 2,1: la scotta ferma chiede il doppio del timone) e su quanto sale la prua a barra ferma (criterio 3: 13,9°, già verde). Il numero 20° non aveva una fonte.
2. **Aggiungere il momento dello scafo** e il `cos` sul timone, dopo aver letto le misure DSYHS: è un cambio della barca (lista intera, rotta, medaglie), con una costante di passaggio fra yacht e deriva senza fonte.

Consiglio la 1: la differenza vera fra le due barche è che M non si ferma in raffica, e non c'è una misura che dica che serve più timone di così.

Fonti: [Weather helm](https://en.wikipedia.org/wiki/Weather_helm), [Chalmers 546299 (ILCA 7)](https://research.chalmers.se/publication/546299/file/546299_Fulltext.pdf), [TU Delft, prove in vasca](https://repository.tudelft.nl/file/File_1ad6a777-655e-42a2-bd85-5616e37c927c), [Nauticed, raffiche e orzate](https://sailing-blog.nauticed.org/how-to-handle-wind-gusts-and-rounding-up/).
