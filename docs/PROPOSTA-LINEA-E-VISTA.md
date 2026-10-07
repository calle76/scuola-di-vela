# Proposta: linea d'arrivo nelle prove e tasto «vista»

**Parte A approvata come 0.19 con queste decisioni; parte B (tasto vista) rimandata alla 0.19.2.**

Decisioni del 7 ottobre 2026 sulla parte A:

1. Prove 1, 2, 3: linea d'arrivo; niente linea di partenza, il cronometro parte all'avvio come prima.
2. Prove 4 e 5: la barca non si sposta, nasce sulla linea (come in regata); l'arrivo diventa la linea; le boe 1 e 2 restano da girare; il passaggio sulla linea prima del giro di boa non conta.
3. Lezione 5 e navigazione libera: invariate.
4. Salvataggi: chiavi nuove in `KEYV` per le cinque prove (`m0.2`, `m1.2`, `m2.2`, `m3.3`, `m4.4`); i dati vecchi delle prove si cancellano al primo avvio e compare una sola volta il messaggio «Le prove sono cambiate: i tempi salvati sono stati azzerati». Nessuna migrazione.
5. Fasce con la regola della 0.16 sui tempi del pilota con la linea: 95/120/150, 145/180/230, 200/250/320, 335/420/535, 355/440/565. Prova 5 misurata prima e dopo con 24 semi fissi, senza soglia.
6. Testi come in A5, mantenendo nella prova 2 la frase della 0.18.4 sulla strambata. Voce di glossario «Linea d'arrivo» e riga in `CONTENUTI-DA-VERIFICARE.md`.
7. Soglie della Fermata 2: prove 1-4 entro ±0,5 s dalla tabella di A3; se una prova sale di più di 25 s ci si ferma. Sono un **controllo di riproducibilità** (il codice fa quello che faceva il banco); la validità la danno i casi di `collaudo_linea.py`.
8. Nuovo `collaudo_linea.py`; refactor `goal()` non fatto (serve solo alla parte B).

Quello che segue è la proposta così come è stata scritta alla Fermata 1 (con le parti superate dalle decisioni indicate come tali).

## Parte A: linea d'arrivo

### A1. Prove e lezioni

| Voce | Prima della 0.19 | Posizione (vento da nord, m) | Proposta |
|---|---|---|---|
| Prova 1 Al traverso | boa da raggiungere (entro 12 m) | (230, 0) | linea d'arrivo |
| Prova 2 Lasco e poppa | boa da raggiungere | (60, 260) | linea d'arrivo |
| Prova 3 Risalire il vento | boa da raggiungere | (0, −220) | linea d'arrivo |
| Prova 4 Il giro di boa | Boa da girare + «Arrivo» da raggiungere | (0, −200); arrivo (0, 20) = partenza | boa resta da girare; arrivo → linea |
| Prova 5 Percorso nelle raffiche | Boa 1 e 2 da girare + «Arrivo» | (0, −200), (−150, −200); arrivo (0, 20) | boe restano; arrivo → linea |
| Lezione 5 «Risalire il vento» | boa da raggiungere entro 12 m | 110 m controvento | invariata |
| Navigazione libera | 3 boe senza obiettivo | — | invariata |
| Regate | già una linea | — | invariate |

Alla Fermata 1 si era proposto anche di spostare la partenza delle prove 4 e 5 di 15 m dietro la linea: **scartato** (decisione 2).

### A2. Geometria e rilevamento

- Centro della linea sull'ultima voce di `marks` (dove prima c'era la boa d'arrivo).
- Perpendicolare all'**ultimo lato** (dal punto precedente, partenza o ultima boa girata, all'arrivo): una regola sola per tutte le prove, indipendente dal vento. «Perpendicolare al vento» non va per la prova 1 (la linea sarebbe parallela alla rotta). Nella prova 4 coincide con la perpendicolare al vento, come in regata; nella prova 5 è ruotata di circa 34°.
- Larghezza 24 m (12 per lato, `FIN_HALF`, ipotesi nostra: stessa tolleranza laterale del cerchio di prima). In regata è di 70 m perché c'è una flotta.
- Disegno: due boe piccole arancioni agli estremi, tratteggio come la linea delle regate, scritta «Arrivo» accanto a una boa.
- Taglio: segmento fra la posizione al passo prima e quella attuale; conta solo dal lato del percorso verso l'arrivo e solo fra le due boe, estremi compresi. Al contrario non conta mai.
- Fuori dagli estremi: niente arrivo, messaggio «Fuori dalla linea: passa tra le due boe», nessun errore nel registro (la stella non cambia).
- Toccare una boa: niente, come la boa di bolina delle regate (semplificazione già dichiarata).
- Punto della barca: il centro, come in regata. Nella realtà conta la prua, circa 2 m prima: circa 1 s, dichiarato.
- Tempo: interpolato all'istante esatto del taglio. La differenza rispetto al passo intero è al massimo 1/60 s (0,05 s nel caso peggiore), su un tempo arrotondato al secondo. Le regate non si toccano.
- `markIdx` non aumenta all'arrivo: l'evento «boa» del registratore conta solo le boe girate.

### A3. Fasce: banco della Fermata 1

`collaudo_fasce.py` puntato su copie modificate di `index.html` (8 venti, 24 tentativi per la prova 5, senza seme fisso):

| Prova | Prima | Linea | Linea + partenza a y=35 (scartata) |
|---|---|---|---|
| 1 | 87,3 | 92,1 | 92,1 |
| 2 | 136,2 | 142,6 | 142,6 |
| 3 | 184,7 | 196,4 | 196,4 |
| 4 | 327,0 | 333,4 | 345,8 |
| 5 (mediana) | 349,2 | 354,3 | 364,1 |

Regola della 0.16 (oro = tempo del pilota arrotondato ai 5 s superiori, argento +25%, bronzo +60%): 95/120/150, 145/180/230, 200/250/320, 335/420/535, 355/440/565.

### A4. Impatto

- Record, stelle e fantasmi: chiavi nuove in `KEYV` per le cinque prove.
- `collaudo_fasce.py`: il pilota punta già al centro della linea (ultima voce di `marks`); aggiunto il seme fisso.
- `collaudo_giro_boa.py`: cambia il nome del caso f.
- `collaudo_fantasma.py`, `collaudo_schermate.py`, `collaudo_lezioni.py`, `collaudo_registro.py`, `analizza_sessione.py`: nessuna modifica.
- `collaudo_pannello.py`: «Rilevamento boa» diventa «Rilevamento»; controllo nuovo sul riquadro delle istruzioni di ogni prova; oro atteso nell'orologio aggiornato.
- `collaudo_registratore.py`: nella prova 3 0 «boa» e 1 «arrivo»; il controllo confronta coi contatori del gioco e non cambia.

### A5. Testi

| Dove | Prima | Dopo |
|---|---|---|
| Prova 1, descrizione | Raggiungi una boa con il vento di fianco. | Taglia l'arrivo con il vento di fianco. |
| Prova 1, testo | …La boa si raggiunge al traverso… e raggiungi la boa. | …L'arrivo è al traverso… e passa tra le due boe dell'arrivo. |
| Prova 2 | Raggiungi una boa sottovento. / La boa è sottovento: … | Raggiungi l'arrivo sottovento. / L'arrivo è sottovento: … (resto invariato) |
| Prova 3 | Raggiungi una boa controvento. / La boa è esattamente controvento. | Raggiungi l'arrivo controvento. / L'arrivo è esattamente controvento. |
| Prova 4 | …poi torna all'arrivo con il vento da dietro. | …poi torna a tagliare la linea da cui sei partito, con il vento da dietro. |
| Prova 5 | …poi gran lasco fino all'arrivo. | …poi gran lasco fino alla linea d'arrivo. |
| Messaggio | Boa girata: ora verso arrivo | Boa girata: ora verso l'arrivo |

Glossario: «Linea d'arrivo». Quiz: nessuna domanda cita l'arrivo. Fonti: la definizione d'arrivo non è in `FONTI-PUBBLICHE.md`; riga aggiunta a `CONTENUTI-DA-VERIFICARE.md`. La perpendicolarità all'ultimo lato è una scelta del gioco e non è scritta nei testi.

### A6. Freccia fuori schermo

Nelle prove la freccia punta alla voce attiva di `marks`, che nell'ultimo lato è il centro della linea: nessun codice in più. (Nelle prove non usa `targetOf`, che è delle regate.)

## Parte B: tasto «vista» (rimandata alla 0.19.2)

- **Tasto V**, tenuto premuto. Livello 1: ← → ↑ ↓ W S Spazio R M; riservati A D e Q E Z C (Q E nel prototipo del fiocco). Restano liberi B F G H I J K L N O P T U X Y e le cifre.
- **Spostamento:** la barca va dalla parte opposta alla direzione in cui si vede l'obiettivo sullo schermo (vale anche con «prua in alto»), del 60% della mezza larghezza e della mezza altezza (ipotesi), tenuta fra il 20% e l'80% dello schermo; arrivo e ritorno morbidi in circa 0,25 s (ipotesi). Campo verso l'obiettivo a 1360×650: da 485 a 776 px in orizzontale, da 325 a 520 in verticale.
- **Dove:** prove e regate (anche prima del via, verso la linea); non nelle lezioni; senza obiettivo (navigazione libera, dopo l'arrivo) non fa nulla. Niente pausa, zoom, fisica o tempo toccati.
- **Funzione `goal()`** usata da freccia, rilevamento e vista: sostituisce due espressioni uguali già nel codice. Da fare con la parte B.
- **Legenda:** la riga dei tasti è su una riga sola con «…» se troppo lunga: «V vista» non aumenta l'altezza ma può tagliare la riga. Criterio: con i caratteri veri nessun taglio ed eccesso 0 px; ripiego, scritta «V vista» sul mare sopra i pulsanti + e −.
- **Registratore:** V fra i tasti registrati («V(vista)») e nella legenda del file.
- **Disegno:** le increspature si disegnano attorno alla barca: con la barca spostata il raggio va allargato dello spostamento (a zoom 0,4 circa 2300 celle contro il limite di 2500, da misurare).
- **Livello 4:** lo spostamento sta solo nel disegno; una futura vista tattica con pausa sarebbe una condizione in più nella pausa del ciclo.
- **Collaudo `collaudo_vista.py`:** direzione giusta (prodotto scalare negativo) con le due viste, ritorno sotto 2 px entro 1 s, traiettoria identica con V tenuto e no (seme fisso, passo `__sv.frame(dt)` che disegna anche, controllo del banco e variante che consuma un numero casuale in più), pagina vera senza `#collaudo` intercettando il disegno.
- **Non farlo:** lo zoom − dà già 2,5 volte il campo; V serve a vedere l'obiettivo senza perdere il dettaglio della barca.
