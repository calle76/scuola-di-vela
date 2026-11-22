# Proposta: verificare il consiglio del Coach «vento scarso, conviene virare»

*Fermata 1, 22 novembre 2026 (Opus). Domanda di Ale e Lucio (21-22 nov): «le indicazioni del Coach sul virare e prendere vento migliore sono valide?». Questa proposta è una **misura**: non cambia il gioco. Se la misura dice che il consiglio sbaglia spesso, si propone a parte come correggerlo.*

## Cosa dice oggi il Coach (1.3.28)

Di bolina, lontano dalla boa (più di 80 m), se il vento sulla barca è girato contro di almeno 7° rispetto al vento medio della regata per 8 s: «Il vento ti è scarso di N°: se oscilla, conviene virare (lezione 11).» (costanti `CR_SCARSO` e `CR_SCARSO_T` in js/rotta.js).

**Cosa dice la fonte (F41, Dellenbaugh, una sola, divulgativa):** se il vento oscilla, si vira sugli scarsi e si resta sulle mure buone; se gira sempre dalla stessa parte (persistente), si va verso il salto; vicino alla boa e alle layline le regole cambiano. Il testo del Coach dice «se oscilla», quindi è d'accordo con la fonte; il dubbio è **quando** il Coach lo dice: il gioco sa il vento medio, ma lo scarso che vede può essere un salto persistente (una regata su tre nelle regate coi salti) o lo spostamento di una raffica, che passa presto.

## Prima misura, sulle vostre regate (21 nov, 1.3.37, 6 regate lunghe)

- Il Coach ha detto «scarso» **14 volte**; avete virato entro 20 s in **9**.
- Quanto è durato lo scarso dopo il consiglio (direzione del vento sulla barca, dalla prua e dall'angolo al vento delle righe S, oltre 2° dalla media della regata): **mediana 37 s**; sotto 15 s in **3 casi su 14**.
- Una virata costa circa 6 s (voce 73: recupero 5,8 s). Uno scarso che dura molto più di una virata vale la virata; uno che dura 10 s no.
- Limite di questa misura: 14 casi sono pochi, e la «media della regata» si calcola dopo, con tutta la regata.

## Il modello più semplice della misura

Un collaudo che corre molte regate lunghe col pilota (semi fissi) e, per ogni consiglio «scarso»:
1. **durata**: per quanti secondi lo scarso resta (oltre 2°) dopo il consiglio;
2. **rotta ottimale**: se la rotta ottimale calcolata a fine regata (isocrone, js/rotta.js) vira entro 30 s dal consiglio;
3. **tipo di vento**: salto oscillante o persistente, e se lo scarso è dentro una raffica.

Il metro non dipende dal Coach: durata dal vento registrato, rotta ottimale da un altro calcolo del gioco (le isocrone, che il Coach non usa).

## Criteri (soglie nostre, dichiarate prima)

Semi 1101-1120 per guardare, 1121-1140 per confermare (regola dei semi).

| # | Criterio | Soglia (attesa nostra) |
| --- | --- | --- |
| K1 | Lo scarso dura abbastanza | almeno il 75% dei consigli con scarso che dura 15 s o più (2,5 volte il costo di una virata) |
| K2 | D'accordo con la rotta ottimale | la rotta ottimale vira entro 30 s dal consiglio in almeno il 60% dei casi |
| K3 | Salti persistenti | si riporta quanti consigli cadono in regate a salto persistente e quanti di questi la rotta ottimale **non** segue; se più di un terzo, proposta per cambiare la frase o la condizione |
| K4 | Ha misurato davvero | almeno 100 consigli contati; il collaudo stampa quanti |

## Rischi

- La rotta ottimale non tiene conto delle altre barche: un consiglio giusto per la tattica può non coincidere con lei (lo si dice nei risultati).
- Se K1 o K2 falliscono, la correzione (per esempio aspettare più secondi, o non parlare dentro una raffica) va proposta a parte.

## Esito della misura (22 nov, via di Ale; `tests/misura_coach_scarso.py`, Chromium, 1.3.40)

| | semi 1101-1120 (60 regate) | semi 1121-1140 (60 regate) |
| --- | --- | --- |
| consigli | 147 | 158 |
| K1 scarso dura 15 s o più (soglia 75%) | 84% | 90% |
| K2 rotta ottimale vira entro 30 s (soglia 60%) | 48% | 38% |
| K3 consigli con salto persistente / non seguiti | 41 / 20 | 61 / 34 |
| in raffica al momento del consiglio | 78 | 89 |

**Moneta** (aggiunta dopo la prima misura, su domanda di Ale, solo riportata): secondi di bolina lontano dalla boa, rotta ottimale che vira nei 30 s dopo: qualunque 48% e 45%; con lo scarso 42% e 39%; col buono 41% e 36%. **Con questo metro il consiglio non vale più di un momento a caso.** K1 passa, K2 non passa, K4 passa (305). Le due misure danno gli stessi consigli (147 e 158): ripetibile.

**Limite del metro (detto prima di decidere):** la rotta ottimale parte dal taglio della linea del giocatore e va più veloce: nello stesso istante è altrove, dove le raffiche cambiano la direzione del vento. **Metro migliore, proposto ad Ale:** dal punto e dall'istante della barca, «la rotta ottimale per la prossima boa comincia con una virata entro 30 s?», per i consigli e per 10 momenti a caso per regata (la moneta). Poi: se il Coach non batte la moneta, si toglie «conviene virare» e resta il fatto («il vento ti è scarso di N°»).
