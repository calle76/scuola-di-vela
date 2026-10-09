# Ricerca dati per un'imbardata dinamica

Stato: ricerca del 9 ottobre 2026, dopo lo studio By The Lee (conclusione: l'ostacolo sono i dati, non il codice).
Scopo: capire quali numeri servirebbero per passare da un motore cinematico (il timone dà direttamente una velocità di rotazione) a uno con momenti e inerzia, e quali di questi numeri esistono in fonti pubbliche.
Regola del progetto: le risposte di un'IA non sono fonti. Qui sotto ogni numero è marcato col tipo di fonte.

## 1. Dove stanno i centri (vela e deriva)

- Regola di progetto, statica: l'anticipo (distanza tra centro velico e centro di deriva) è il 12–19 % della lunghezza al galleggiamento. È una regola di disegno di yacht, non una misura dinamica.
- Derive a vela singola: circa 10 % (una sola fonte, un forum: indicativa, non verificabile).
- Non trovato: effetto del fiocco sullo spostamento del centro velico per una deriva a due; valori misurati su derive olimpiche.

## 2. Inerzia d'imbardata

- Raggio di giro d'imbardata: circa 24–25 % della lunghezza al galleggiamento (valore per yacht).
- Non trovato: un valore per derive. Senza questo, la velocità angolare reale in virata non si può calcolare.

## 3. Timone

- Fonte F4 (studio su deriva olimpica a due): il timone lavora bene fino a circa ±15° di angolo. Oltre, la forza laterale smette di crescere e la resistenza continua a salire (stallo).
  - A 6 nodi: circa 5 kgf a 10°, 12 kgf a 15°; resistenza totale circa 19 kgf; momento raddrizzante massimo circa 220 kgf·m a 25° di sbandamento.
- Un lavoro CFD contraddice: stallo a 30–35°. Probabile differenza tra angolo del timone e angolo d'incidenza dell'acqua (a barca che sbanda o scivola di lato i due non coincidono). NON risolto.
- Timonata normale in bolina: 2–5°; oltre 8° è troppa (indicazione di manuali di regata).
- Il timone massimo del gioco è 30°: plausibile solo se lo stallo vero è 30–35°; se è 15° il gioco lo sopravvaluta.

## 4. Ricontrollo della fonte F4

Riletta: i numeri sopra sono confermati come riportati nella scheda F13/F4 di FONTI-PUBBLICHE.md. Nessuna correzione.

## 5. Che cosa manca ancora

- Anticipo e inerzia misurati su una deriva a due.
- Effetto del fiocco (cazzato/lascato) sul centro velico.
- Stallo del timone misurato, non simulato.
- Un velista che dica come reagisce davvero la barca a barra lasciata libera e a barra a fondo.

## 6. Che cosa si può fare concretamente

Una sola modifica piccola e con fonte: **effetto stallo del timone**. Oltre ±15° l'effetto di rotazione smette di crescere e la resistenza continua a salire, quindi «barra tutta a fondo» non è più sempre la scelta migliore (oggi lo è). Va prima chiarita la contraddizione al punto 3 (domanda per il velista: da che angolo di barra la barca «non gira di più»?).

L'imbardata dinamica completa resta rimandata: servono dati del punto 5.

## 7. Libri e articoli (ricerca del 9 ottobre 2026)

Verificato: esistenza e dati bibliografici. NON verificato: contenuto, salvo dove scritto. I titoli dei libri elencati sotto come «da controllare» sono ricordati, non letti.

Articoli tecnici
- Keuning, Vermeulen, de Ridder (2005), «A Generic Mathematical Model for the Maneuvering and Tacking of a Sailing Yacht», 17th Chesapeake Sailing Yacht Symposium, SNAME, pp. 143-163. Esiste (pagina TU Delft: https://research.tudelft.nl/en/publications/a-generic-mathematical-model-for-the-maneuvering-and-tacking-of-a/). Riassunto e PDF non visti; non so se sia gratuito. È lo yacht, non la deriva. Primo candidato per costanti di inerzia e timone, da usare come scala e dichiarare come stima.
- Stessa area, solo titoli letti: «A mathematical model for the tacking maneuver of a sailing yacht» e «The yaw balance of sailing yachts upright and heeled» (TU Delft).
- Marchaj, articolo su equilibrio della barra e stabilità direzionale statica degli yacht in bolina (Aeronautical Journal, Cambridge). Solo titolo letto.

Aperti e non utili
- Taylor, Banks, Turnock (2016, Chesapeake): Laser (deriva monoposto), ma riguarda il momento di raddrizzamento dato dal peso del timoniere. Niente inerzia d'imbardata, timone o anticipo. Misure del Laser: LWL 3,81 m, larghezza 1,37 m, vela 7,06 m².
- Articolo sulla virata dell'AC45 (catamarano 13,4 m, 1.500 kg): equazioni d'imbardata senza valore dell'inerzia; solo angoli di barra provati (20-25°, 6-8 s).
- Università della Tasmania, dati su derive in simulatore e in acqua (2015): classi e misure non indicate; accesso solo su richiesta al referente.

Libri (da controllare l'indice prima di comprare)
- Marchaj, «Aero-Hydrodynamics of Sailing» e «Sail Performance»: forze delle vele, equilibrio, timone, interazione randa-fiocco. Contenuto per derive NON confermato.
- Larsson, Eliasson, «Principles of Yacht Design» (4ª ed.): esiste ed è in commercio; fonte della regola dell'anticipo e dei raggi di giro. Indice non letto. Yacht, non derive.
- Bethwaite, «High Performance Sailing»: derive e skiff, probabilmente qualitativo. Indice non trovato.

Altra strada: i regolamenti di classe (per esempio 470) danno masse minime, lunghezze, posizione dell'albero e superfici, quindi permettono di stimare l'anticipo e un'inerzia approssimata, dichiarata come stima.

Conclusione: nessun numero nuovo utilizzabile per ora. Passo successivo possibile: ottenere il testo completo dell'articolo Delft 2005 (a cura di Ale, il sandbox non raggiunge quei siti).

## Domande per il questionario al velista

1. A barra tutta a fondo la barca gira più in fretta o frena soltanto? Da quale angolo circa?
2. A barra lasciata libera in bolina la barca tende a orzare o a poggiare? Con e senza fiocco?
3. In una deriva a due, quanto sposta il fiocco la tendenza a orzare/poggiare?
