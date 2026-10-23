# Proposta: contatto vero fra gli scafi (1b) e anello di precedenza

Stato: **proposta (fermata 1), nessun codice nel gioco.** Idea e decisioni di Ale, 23 ottobre 2026 (`PROPOSTA-ELENCO-23-OTTOBRE.md`, punto 1). Due versioni separate: **1.0.39** (parte A, contatto vero) e **1.0.40** (parte B, anello facoltativo).

## Perché
Oggi (`js/regate.js`, `contacts()`) il contatto scatta quando i **centri** di due barche sono a meno di 4,2 m: un cerchio invisibile di raggio 2,1 m attorno a ogni barca. Lo scafo disegnato è lungo 4,2 m e largo circa 1,4 m (`hullPath`, `js/disegno.js`). Il contatto scatta quindi con gli scafi ancora separati.

## Misure di oggi (23 ottobre 2026, versione 1.0.38, semi 1-15, principianti ed esperti, giocatore guidato da `__sv.pilota`, 90 regate)
Regate 0 e 1 sono dell'1a, la 2 («salti di vento») è dell'1b.

| | contatti attuali per regata | distanza fra gli scafi al momento del contatto (mediana) | contatti con gli scafi a meno di 1 m |
|---|---|---|---|
| regata 0 (1a) | 4,2 (30 corse su 30 ne hanno almeno uno) | 1,5 m (da 0,0 a 2,8) | 27 su 126 |
| regata 1 (1a) | 4,8 (29 su 30) | 1,6 m (da 0,05 a 2,8) | 30 su 144 |
| regata 2 (1b) | 4,6 (30 su 30) | 1,6 m (da 0,04 a 2,9) | 21 su 138 |

In pratica solo 1 contatto su 5 oggi è «quasi vero»; gli altri 4 su 5 scattano con 1-3 m d'acqua fra gli scafi.

**E col contatto vero?** Ho rigiocato le stesse 90 regate in un mondo senza nessuna regola di contatto (le barche si attraversano), contando gli episodi in cui i due contorni disegnati si sovrappongono davvero:

| | sovrapposizioni vere per regata | rispetto ai contatti di oggi |
|---|---|---|
| regata 0 | 3,5 (30 su 30) | −17% |
| regata 1 | 3,5 (29 su 30) | −27% |
| regata 2 (1b) | 2,6 (28 su 30) | −44% |

Quindi i contatti non spariscono: nell'1b, regata 2, restano circa 2,6 a regata invece di 4,6, e in 28 regate su 30 ce n'è almeno uno (conferma quello che vedi giocando, soprattutto in partenza e alla boa). È un numero approssimato: in un mondo senza regola le barche non si urtano né rallentano e le traiettorie si possono allontanare da quelle reali. Lo script è `tests/misura_contatti.py` (nessuna soglia, rilanciabile dopo la modifica).

## Parte A, 1.0.39: contatto vero, solo nell'1b
**Modello più semplice.**
- Nell'1b (`R.lv2`, che comprende le regate dei salti di vento e il torneo) il contatto scatta quando i due contorni degli scafi si sovrappongono. Il contorno è un poligono di 24 punti, campionato dagli stessi punti di `hullPath`, ruotato con la prua. Filtro veloce: si controlla solo se i centri sono a meno di 4,4 m (due scafi non si toccano oltre la somma delle mezze lunghezze).
- Test di sovrapposizione fra poligoni convessi (assi separatori); la penetrazione dà anche la direzione e la lunghezza dello spostamento per separarli, al posto di «4,6 m fra i centri».
- Il resto non cambia: colpa decisa da mure e sopravento, velocità ×0,6, penalità (15 s, +1 punto nel torneo), «stesso contatto finché si separano di 8 m», avvisi.
- Nell'1a (`!R.lv2`) resta il cerchio di 4,2 m, come oggi: dichiarato come distanza di sicurezza. L'1a è congelata.
- Il contorno è solo lo scafo: boma e vela, che sporgono, non toccano (limite dichiarato).
- Nel testo d'introduzione delle regate dell'1b una frase: «Da questo livello i contatti sono quelli veri, scafo contro scafo. Prima avevi imparato a stare lontano perché il contatto scattava prima del contatto vero.»

**Costanti e ipotesi.** Nessuna costante fisica nuova. Ipotesi nostre: 24 punti bastano; filtro a 4,4 m; il reset a 8 m fra i centri resta quello di oggi; spostamento = penetrazione + 0,3 m (come l'attuale push «+0,3»).

**Criteri (attese nostre).**
1. Nell'1b nessun contatto scatta con gli scafi a più di 5 cm di distanza al passo precedente: 0 su tutti i contatti di 90 regate (semi 1-15; n deve essere > 0, lo riporto).
2. Nell'1b nessuna sovrapposizione oltre 5 cm resta senza contatto: dopo ogni passo, per ogni coppia con penetrazione > 5 cm esiste il contatto: 0 casi su 90 regate.
3. Contatti per regata nell'1b dopo la modifica: riportati come escono, senza soglia (attesa: tra 2 e 4,6, vedi sopra).
4. **L'1a identica al bit:** l'impronta delle regate 1 e 2 dell'1a (principianti ed esperti) uguale alla 1.0.38 (stato delle barche, registro, testi); `polare.js` e `raffiche_e_virate.js` identici.
5. Pannello 0 px (`esplora.py --rigioca`, 195 regate); `collaudo_torneo.py`, `collaudo_competizione.py`, `collaudo_aggressiva.py`, `collaudo_contatto_senza_colpa.py`, `collaudo_registro.py`, `collaudo_pannello.py` verdi (con soglie cambiate solo se dichiarato).
6. Collaudo nuovo `collaudo_contatto_vero.py`: l'1a usa il cerchio e l'1b lo scafo (stessa coppia di barche a 3 m fra i centri: nell'1a contatto, nell'1b no; a 1,2 m fra i centri affiancate o a prue incrociate: contatto in tutte e due).
7. Prova anche in pagina senza `#collaudo`.

**Rischi.**
- Gli avversari, tarati con il cerchio largo, a regate dell'1b sentiranno meno contatti: più rischio che stringano di più la linea e la boa. Lo misuro: numero di penalità degli avversari prima e dopo, classifica del torneo (punti medi per barca), partenze anticipate.
- Il torneo (punteggi, penalità) cambia perché cambiano i contatti: i numeri di `collaudo_torneo.py` e quelli di `PROPOSTA-TORNEI-1B.md` §7 vanno rimisurati e riportati.
- I collaudi che cercano un contatto a una distanza precisa possono non trovarlo: controllo uno per uno e controllo che nell'1b ci siano contatti da misurare (n > 0).
- Una regola di colpa che oggi scatta «presto» (mure sbagliate a 4 m) può non scattare più per niente se le barche si evitano: va bene, è il comportamento voluto.
- Il riferimento dell'impronta cambia solo per l'1b: nell'1a deve restare uguale (criterio 4).

## Parte B, 1.0.40: anello di precedenza (facoltativo, solo 1b)
**Modello.**
- Un alone sottile attorno allo scafo del giocatore (contorno dello scafo allargato di circa 0,3 m), solo in regata dell'1b, solo con un'altra barca a meno di 8 m che si avvicina (distanza in calo rispetto a 1 s prima).
- **Rosso** se in caso di contatto la colpa sarebbe del giocatore, **verde** se dell'altra. Lo decide la stessa funzione che oggi sta dentro `contacts()` (estratta in una funzione sola, `chiCede(A, B)`, usata da tutti e due): non possono contraddirsi.
- Compare con 8 m o meno e sparisce oltre 10 m o dopo 2 s in cui la distanza cresce (per non lampeggiare).
- Facoltativo nelle impostazioni, **spento di default** (principio 3). Nell'1a e fuori dalle regate non esiste.
- Solo attorno alla barca del giocatore, non agli avversari.

**Criteri (attese nostre).**
1. Il colore all'ultimo istante prima di ogni contatto del giocatore è quello della colpa assegnata: 100% dei contatti nei quali l'anello era visibile (conto quanti e riporto quanti contatti erano senza anello: se più del 20% senza anello, la regola «8 m e in avvicinamento» è da rivedere, ma non è una soglia che cambio dopo averla vista senza dirlo).
2. Con l'opzione spenta l'immagine del mare è identica a prima (confronto canvas).
3. Pannello 0 px; barca e regate identiche (l'anello non cambia la simulazione).
4. Prova in pagina senza `#collaudo`.

**Rischi.** Un'impostazione in più nella finestra delle impostazioni (nessun effetto sul pannello, è un dialogo); un anello che copre altri elementi vicino alla barca; colori leggibili da chi non distingue il rosso dal verde (propongo, oltre al colore, di cambiare lo spessore: rosso più spesso).

## Collaudi, tutti da scrivere nella 1.0.39/1.0.40
`collaudo_contatto_vero.py` (regola diversa nei due livelli, criteri 1, 2, 6), `collaudo_anello.py` (1.0.40, colore uguale alla colpa), `collaudo_regata_intera.py` (regata intera col pilota, pannello ogni secondo e riquadro finale), (`tests/misura_contatti.py`, già scritto: la misura di questa proposta). I primi tre entrano in `lancia_tutti.sh`.

## Da decidere (Ale)
Niente di bloccante: tutte le tue risposte sono già in questo testo (parte A solo nell'1b, anello solo per il giocatore, solo con barche vicine e in avvicinamento). Due cose da confermare:
1. Due versioni separate (1.0.39 e 1.0.40) come scritto qui, o una sola? Propongo due, perché la parte A cambia i risultati delle regate e conviene misurarla da sola.
2. Il boma e la vela non fanno contatto, solo lo scafo: va bene come limite dichiarato?

## Aggiunta (Ale, 23 ottobre 2026): l'anello e le regole di precedenza che arriveranno
**Il problema.** Oggi la colpa si decide solo con due regole (mure diverse; stesse mure e sopravento), a prescindere da chi ha cambiato rotta (`ROADMAP.md`, 13 ottobre 2026). Un verde che significasse «ho ragione» sarebbe falso: nel regolamento (F15) chi ha la precedenza deve comunque evitare il contatto se può (regola 14) e non può cambiare rotta addosso a chi deve cedere (regola 16); le altre regole (17, 18 boe, ecc.) arriveranno con il livello del regolamento.
**Cosa cambia nella parte B.**
1. L'anello dice **«precedenza»**, non «ragione»: rosso = devi lasciare strada; verde = hai la precedenza, **ma devi comunque evitare il contatto**. Il testo dell'impostazione lo dice, e il gioco dichiara che oggi punisce solo chi non cede (le regole 14 e 16 non sono ancora nel gioco: se il giocatore con la precedenza punta una barca, oggi la penalità va all'altra).
2. L'anello non decide niente: legge la funzione `chiCede(A, B)`, che oggi ritorna solo la barca che cede. Per le regole future la funzione ritorna anche il **motivo** (quale regola) e, quando servono, altri stati: un terzo colore (ambra: «hai la precedenza ma stai cambiando rotta verso l'altra barca, regola 16») entra senza toccare il disegno, aggiungendo il caso nella funzione. Lo stesso valore serve alla penalità, al testo di fine regata e all'anello, quindi tutte e tre cambiano insieme.
3. Dove arriveranno le regole nuove: nel livello del regolamento (`VISIONE-LIVELLI-E-CARRIERA.md` §2), con una fermata 1 per ognuna.
**Visibilità.** L'alone è un contorno sottile, non pieno, e compare solo con un'altra barca entro 8 m che si avvicina: controllo con una immagine ingrandita e con lo zoom minimo che non copra boma, vela e boe; spento di default.
**Limite già noto che l'anello renderebbe visibile** (`ROADMAP.md`, 13 ottobre 2026): con le stesse mure `contacts()` dà torto a chi è più sopravento senza guardare se le barche sono affiancate; chi tampona da dietro non affiancato potrebbe vedere un verde sbagliato. Prima della 1.0.40 lo provo con casi misurati (barca che arriva da dietro, stesse mure, non affiancata) e riporto cosa risulta; se la regola è sbagliata si decide con Ale se correggerla (regola 12 e 11 di F15) o dichiararla.

## Provato il 23 ottobre 2026 (prima di cominciare): stesse mure, barche non affiancate
12 casi messi a mano (vento da nord, due barche con la stessa prua, B davanti, dietro o di lato ad A, a 3,5 m in fila o a 3,0 m affiancate; si guarda a chi va la penalità). **Affiancate: la colpa va sempre alla barca sopravento (giusto, regola 11 di F15).** **In fila e non affiancate** (regola 12: chi è «clear astern» cede a chi è davanti): di bolina (prue 045° e 315°) la penalità va **alla barca davanti** in 4 casi su 4 (sbagliato), con la prua 135° (poppa larga) va a quella dietro in 2 su 2 (giusto per caso: dietro è anche più sopravento). Quindi la regola `ya < yb` (sopravento) è sbagliata per chi tampona di bolina senza essere affiancato. Con il contatto vero in 1b i tamponamenti di bolina diventano più riconoscibili. **Da decidere con Ale nella 1.0.40** (insieme alla funzione `chiCede`): aggiungere la regola 12 nell'1b, o dichiararlo come limite; nell'1a resta così (congelata).
