# Proposta: il Coach che parla durante la regata (voce 65)

*Fermata 1, 20 novembre 2026. Idea di Ale del 20 novembre: «mettere il Coach che appare con diverse espressioni durante le lunghe regate per dare consigli e commenti». Nessun codice finché non arriva il via. Dipende dalla voce 63 (`PROPOSTA-PERCORSO-LUNGO.md`): con regate da 3 minuti non c'è spazio per parlare senza disturbare.*

## Cosa c'è già

- **Dopo la regata:** il Coach nella moviola, con tre volti (contento, serio, arrabbiato), fino a 3 frasi coi numeri, calcolate sulla rotta ottimale (`js/rotta.js`, `coaFrasi`).
- **Durante la regata:** i *suggerimenti* (righe «H» nei file: filetti, raffica in arrivo, barra all'indietro…), che sono consigli di **tecnica** e si spengono nelle impostazioni; i messaggi delle regole (contatto, penalità, giri); l'orologio dei giri; il semaforo delle precedenze.
- **Gli eventi che il gioco già riconosce in regata** (quelli che scrive nel file): partenza anticipata, barca coperta e libera (cono d'ombra), contatti con e senza colpa, boa toccata, giri di penalità, boa girata, scuffia, rivali fermi o in ritardo, arrivi.

## Il modello più semplice

**Un riquadro piccolo col volto del Coach (48 px) e una riga di testo**, in alto a sinistra sul mare (nel torneo lì non c'è niente; nelle regate con le bandiere va sotto il loro riquadro). Compare **solo per un evento**, resta 6 s, e fra un commento e l'altro passano almeno 30 s, tranne per le penalità. **Solo in Deriva**, e si spegne nelle impostazioni («Coach in regata: sì/no», principio 3: gli aiuti si possono togliere).

**Il Coach parla di tattica, non di tecnica:** la tecnica resta ai suggerimenti, così le due voci non si ripetono. Ogni frase dice solo cose che il gioco sa in quel momento, coi numeri quando ci sono:

| Quando | Volto | Esempio di frase (da scrivere con le fonti) |
| --- | --- | --- |
| Partenza: tagliata entro 3 s dallo sparo | contento | «Bella partenza: sei sulla linea allo sparo.» |
| Partenza anticipata | arrabbiato | «Sei partito prima: torna dietro la linea.» |
| Coperto da una barca per più di 10 s | serio | «Sei nel cono della Rossa: vira o poggia per uscirne.» |
| Vento girato contro (scarso) di almeno 6° per 10 s | serio | «Il vento ti è scarso di 8°: è il momento di virare (lezione 11).» |
| Oltre la layline di più di 20 m | serio | «Sei oltre la layline: perdi strada.» |
| Boa girata guadagnando o perdendo posizioni | contento / serio | «Boa girata: sei passato dal 4° al 2°.» |
| Contatto con colpa, boa toccata | arrabbiato | «Contatto con colpa: fai i due giri, lontano dalle altre barche.» |
| Penalità scontata | contento | «Giri fatti: ora riparti.» |
| Ultimo lato, distacco dalla barca davanti sotto 10 s | contento | «La Verde è a 6 s: puoi prenderla.» |
| Inizio della regata di una tappa con lo sponsor | serio | «Per lo sponsor serve un podio di tappa: questa è la regata buona.» |

I volti sono i tre che ci sono già; altri (preoccupato, sorpreso) solo se Ale fa le immagini (voce 58).

**Nel file della regata** ogni commento diventa una riga (come le righe «A» del Coach di fine regata), così si può controllare cosa ha detto e quando.

## Due scelte per Ale

1. **«Scarso o buono» (voce 48, proposta già scritta, via al codice non dato):** consiglio di farla diventare una frase del Coach invece di una riga a parte sotto il vento, per non avere due voci che dicono la stessa cosa.
2. **Quanto parla:** al massimo un commento ogni 30 s (circa 8-12 in una regata da 7 minuti), oppure solo nei momenti importanti (partenza, boe, penalità: circa 4-6).

## Costanti nuove (ipotesi nostre)

Durata del commento 6 s; distanza minima fra due commenti 30 s; soglie degli eventi (coperto 10 s, scarso 6° per 10 s come `SCARSO` del Coach, layline 20 m, distacco 10 s).

## Criteri (soglie nostre, dichiarate prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| P1 | Quanto parla | su 20 regate lunghe col pilota: commenti per regata fra 4 e 12 (mediana); nessuno a meno di 30 s dal precedente, tranne le penalità |
| P2 | Dice il vero | ogni commento ricontrollato dal collaudo sui dati della regata (chi copriva, di quanti gradi era scarso, le posizioni alla boa): 0 sbagliati, e il collaudo dice quanti ne ha controllati |
| P3 | Non ripete i suggerimenti | nessun commento uguale, per argomento, a una riga «H» negli stessi 10 s |
| P4 | Spento è spento | col Coach spento, 0 commenti e regata identica al bit (posizioni, tempi) |
| P5 | Non copre | riquadro dentro il mare, mai sopra la barca del giocatore né sopra la boa vicina; pannello 1360x650 con 0 px di eccesso |
| P6 | Costo | tempo per passo di simulazione non oltre +3% |
| P7 | Come un giocatore | pagina senza `#collaudo`, una regata giocata: commenti visti, 0 errori |

## Rischi

- **Disturbo:** un Coach che parla troppo diventa rumore; per questo le soglie di P1 e la distanza minima.
- **Frasi sbagliate:** un consiglio tattico sbagliato insegna male (principio 4); per questo P2 e frasi scritte partendo dalle fonti.
- **Ordine dei lavori:** prima le regate lunghe (63), poi il Coach in regata. Con le regate di oggi (3 minuti, 2 virate) i commenti sarebbero 2-3 e quasi sempre sopra altri messaggi.

## Passi, dopo il via

1. Le frasi, con le fonti (`FONTI-PUBBLICHE.md`), da far vedere ad Ale prima del codice.
2. Il riquadro e gli eventi, dietro l'impostazione; il collaudo P1-P7.
3. Le frasi nel file della regata; documenti e versione.
