# Proposta: misurare gli avversari sulle regate vere di Ale (fermata 2 fatta, esiti al §6)

**7 novembre 2026, ramo `deriva`. Solo strumenti di prova: il gioco non cambia, non è una versione.** Ale: «partiamo da 1 e 2, scarico le regate quando gioco».

## 1. Perché

Il pilota dei collaudi è la guida degli avversari: vede tutto, non sbaglia, si scansa come loro, e conta solo quello per cui ho scritto un contatore. Esempio: il tocco di Rossa ad Ale (osservazione 92) è capitato nell'unica regata di quel file; col pilota capita in 1-2 regate su 240, anche quando tiene la rotta. Non sappiamo quanto di questa distanza sia caso.

## 2. Il modello più semplice

**Parte B, le scene strane (si fa per prima).** `tests/scene_strane.py` legge i file del registratore e stampa le scene trovate, con tempo e barche. Il registratore gira già durante le simulazioni (`__sv.run` chiama `sesTick`, il testo si ottiene da `__sv.ses`): **un solo lettore per le regate di Ale e per quelle simulate**, così il metro è lo stesso.

| Scena | Da | Definizione (costanti: ipotesi nostre) |
| --- | --- | --- |
| S1 cede ma si avvicina | 81 | «cede:X» da almeno 2 s, e la distanza da X scende sotto 8,4 m (due lunghezze) |
| S2 curva grande per cedere | 92 | «cede:X» e la prua gira di oltre 60° in 5 s |
| S3 contatto cedendo | 81, 92 | contatto con X entro 5 s da un «cede:X» |
| S4 contatto senza che nessuno ceda | 82, 84 | contatto fra due barche, nessuna «cede» l'altra nei 5 s prima |
| S5 ritorno di bolina | 80 | scende (oltre 100° dal vento), poi entro 12 s sotto 60°, con una barca entro 12,6 m |
| S6 strambate ravvicinate | 85 | due in meno di 5 s |
| S7 ferma | 88, 90 | evento `avv_fermo` del registratore (sotto 0,5 nodi per 5 s dopo il via) |

**Parte A, rigiocare le regate.** `tests/rigioca_regata.py` apre la stessa regata con lo stesso vento e la stessa preparazione del file; a ogni passo mette la barca del giocatore dove è stata la barca vera, interpolando fra i punti registrati; gli avversari guidano da soli, con semi diversi. Poi passa il risultato a `scene_strane.py`. Si può confrontare il codice prima e dopo una correzione con la stessa guida umana.

**Semplificazione dichiarata:** la barca rigiocata non reagisce a ciò che fanno gli avversari, e dopo un urto torna sulla rotta registrata. Quindi vale per contare che cosa fanno gli avversari, non per dire chi vince.

## 3. Criteri (soglie nostre, scritte prima di misurare)

- **R1, trova il caso vero:** sulla regata delle 18:33, S2 e S3 trovano Rossa fra t=119 e t=124. Se no, il rilevatore è sbagliato.
- **R2, ogni scena è provata:** per ognuna da S1 a S7 almeno un caso che la fa scattare (vero, se c'è un file, se no costruito) e uno simile che non la fa scattare. Le scene provate solo su un caso costruito si dichiarano.
- **R3, si può leggere:** sulla regata delle 18:33 al massimo 15 scene. Delle prime 10 riletta secondo per secondo, almeno 8 corrispondono alla definizione.
- **R4, il rigioco è fedele:** distanza fra barca rigiocata e file, dove non c'è stato un urto, mediana al massimo 0,3 m e massimo al massimo 2 m. Vento e preparazione uguali al file: se non si possono rifare, il rigioco si rifiuta.
- **R5, il rigioco misura davvero:** 40 semi nei due browser sulla regata delle 18:33, si riportano le scene per seme. Il controllo è valido solo se le 40 corse arrivano in fondo e almeno una scena compare in almeno 20 corse su 40 (se no, non ha visto niente).
- **R6, il gioco non cambia:** `git diff` vuoto su `index.html` e `js/`; `polare.js` e `raffiche_e_virate.js` identici.
- **Da riportare, senza soglia:** scene per regata di Ale, del rigioco e del pilota, su semi 481-500; poi, se serve una soglia, conferma sui semi 501-520 mai guardati.

Un numero fuori soglia si riporta com'è.

## 4. Rischi

- **Poche regate:** oggi c'è un solo file nel repo. Con 1-2 regate il rigioco dice poco: Ale ne scarica una ogni volta che gioca.
- **Scene che dipendono da come è scritto il registratore:** una riga ogni 0,1 s e lo stato «cede» come lo dichiara il gioco. Se manca qualcosa, si aggiunge al file solo con una proposta a parte.
- **Una scena non è un errore:** S2 può essere una manovra giusta. Le scene dicono dove guardare, non cosa correggere.
- **Il mio giudizio sulle scene non è quello di Ale:** le peggiori gli si indicano col tempo, da vedere alla moviola; è facoltativo.

## 5. Cosa non si fa

Il pilota «umano» con errori e ritardi: solo se dopo queste due parti servirà ancora. Nessuna correzione degli avversari entra in questo lavoro: i contatti prima del via hanno una proposta loro, che userà questi strumenti.

## 6. Esiti (7 novembre 2026, via di Ale: «ok vai»)

Strumenti: `tests/scene_strane.py` (con `--prova`), `tests/rigioca_regata.py`. Regate di Ale usate: 04/11 21:12 (1.2.12, `main`), 06/11 15:50, 17:59 e 18:33 (ramo `deriva`). Le altre ripristinate sono vuote, a metà o della 1.0.64. Rigioco: semi 481-520, Chromium e Firefox, 320 corse. **Soglie non cambiate.**

| | Soglia | Esito |
| --- | --- | --- |
| R1 Rossa alle 18:33 | trovata fra 119 e 124 | **sì**: S2 a 121,3, S1 a 121,7, S3 a 123,1 |
| R2 ogni scena provata | scatta su un caso, tace su uno simile | **sì** per S1-S7 sui casi costruiti; casi veri per S1-S6 (S5 e S6 nella regata del 04/11, le osservazioni 80 e 85); **S7 solo su un caso costruito** |
| R3 leggibile | al massimo 15 scene; 8 su 10 giuste | **11 scene**; **10 su 10** rilette dalle righe del file con un conteggio a parte (una a 8,7 m invece di 8,4: il fotogramma accanto) |
| R4 fedeltà | mediana ≤ 0,3 m, massimo ≤ 2 m | **0,00 e 0,14 m** in tutte le 320 corse |
| R5 misura davvero | 40 corse in fondo, una scena in metà | **sì**: S1 in 40 su 40 ovunque |
| R6 gioco invariato | `git diff` vuoto, fisica identica | **sì** |

**Cosa dicono, senza soglia:**

- **Contatti con la barca di Ale:** nelle sue 4 regate 4 (2, 1, 1, 0); nel rigioco 0,70-1,73 a corsa. Con il pilota al suo posto, dopo il via, 0,32 a regata (`misura_strambate.py`). La barca rigiocata non si scansa, quindi il rigioco sta un po' sopra il vero; il pilota sta sotto.
- **La scena più frequente è S1, «cede ma si avvicina»:** 7-10 a corsa, e 5-11 in ogni regata vera. S2 scatta quasi sempre fra 61° e 65°: la curva più larga che la guida si concede (60°) più un po'.
- **S5, S6 e S7 sono rare** (fino a 0,23 a corsa): le correzioni della proposta avversari reggono anche con la guida di Ale.

**Limiti:** quattro regate, due con 60 s di preparazione e due con 180. La regata del 04/11 è stata giocata con la guida della 1.2.12: la sua rotta va bene, gli avversari sono quelli di oggi.
