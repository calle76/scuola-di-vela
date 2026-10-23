# Proposta: le regole di precedenza dell'1b e il semaforo sullo scafo

Stato: **proposta (fermata 1), nessun codice scritto.** Richiesta di Ale, 23 ottobre 2026: «tutte le regole possibili introdotte»; semaforo rosso/verde sul bordo dello scafo, giallo per «hai la precedenza ma ne stai abusando». Testo delle regole: F15 (`fonti-pdf/RRS-2025-2028-World-Sailing.pdf`), parafrasato qui, non copiato.

## Cosa fa oggi il gioco (1.0.39)
`contacts()` decide la colpa solo con due regole: **mure diverse** (cede chi ha il vento a sinistra, regola 10) e **stesse mure** (cede la barca più sopravento, ma senza guardare se le barche sono affiancate: regola 11 solo in parte). Il contatto avviene sempre senza danno e porta sempre 15 s (+1 punto nel torneo) a chi cede. Provato il 23 ottobre: di bolina, senza affiancamento, la penalità va alla barca davanti (4 casi su 4), mentre la regola 12 dice che cede quella dietro.

## Inventario: quali regole di F15 si possono mettere
«Fattibile» = si può scrivere con lo stato che il gioco ha già (posizione, prua, vento nel punto, boe), senza motore nuovo.

| Regola (parte 2) | Cosa dice, in breve | Fattibile? | Cosa serve |
|---|---|---|---|
| **10** mure opposte | cede la barca mure a sinistra | già c'è | — |
| **11** stesse mure, affiancate | cede la sopravento | in parte | serve la definizione di «affiancate» |
| **12** stesse mure, non affiancate | cede quella dietro | sì | stessa definizione: chi è «dietro» (tutto lo scafo dietro la linea al traverso dalla poppa dell'altra) |
| **13** durante la virata | dopo aver passato la prua al vento, la barca cede a tutti finché non è di nuovo di bolina; le regole 10, 11 e 12 non valgono | sì | un indicatore per barca «sta virando» (il gioco sa già quando la prua attraversa il vento) |
| **14** evitare il contatto | tutti devono evitarlo se ragionevolmente possibile; chi ha la precedenza solo dopo che è chiaro che l'altra non cede; **senza danno chi ha la precedenza è esonerato** (regola 43) | in parte | nel gioco non c'è il «danno»: va dichiarato o modellato (vedi sotto) |
| **15** acquisire la precedenza | chi la acquisisce con una sua azione deve prima dare spazio all'altra | sì, con ipotesi | finestra di tempo dopo il cambio di chi ha la precedenza |
| **16** cambiare rotta | chi ha la precedenza e cambia rotta deve dare spazio all'altra; di bolina chi è mure a dritta non poggia se la mure a sinistra deve cambiare subito | sì, con ipotesi | variazione di prua della barca con precedenza verso l'altra negli ultimi secondi |
| **17** rotta corretta | chi arriva da dietro e si affianca sottovento entro 2 lunghezze non può orzare oltre la sua rotta corretta | sì, più complessa | la «rotta corretta» (verso la boa) è già calcolata per gli avversari; per il giocatore va dedotta |
| **18** spazio alla boa | entro 3 lunghezze (12,6 m) dalla boa, chi è dentro l'affiancamento all'entrata ha diritto allo spazio | sì, ma grossa | zona attorno alla boa gialla, chi è dentro e chi fuori all'entrata; non vale alle boe di partenza |
| **19, 20** ostacoli, spazio per virare | | no per ora | nel gioco non ci sono ostacoli |
| **23** barca scuffiata | si evita una barca scuffiata | sì | oggi `contacts()` salta le barche scuffiate (le attraversa): da decidere |
| 31 toccare una boa, 42 propulsione, 44 giri | | rimandate | livello del regolamento (penalità a giri) |

**Cosa NON si può onestamente mettere:** le regole che si decidono con un giudizio («ragionevolmente possibile», «spazio necessario in condizioni normali»): vanno tradotte con soglie dichiarate come ipotesi nostre, e ogni soglia si riporta e si sceglie su un gruppo di semi e si conferma su un altro (regola dei semi).

## Un'unica funzione: `chiCede(A, B)`
Oggi il verdetto sta dentro `contacts()`. Lo estraggo in una funzione sola, che ritorna per la coppia: la barca che deve cedere, la **regola** (10, 11, 12, 13, 15, 16, 17, 18) e il **motivo** in una frase. Penalità, testo di fine regata e semaforo la leggono tutti e tre: non possono contraddirsi. Ogni regola nuova è un caso in più della funzione, con la sua fermata 1 e i suoi collaudi.

## Il semaforo sullo scafo del giocatore (decisione di Ale)
Il bordo dello scafo del giocatore, più spesso (circa 0,12 m invece di 0,05), nei colori della funzione:
- **rosso:** devi lasciare strada (regole 10, 11, 12, 13, 18 quando cedi);
- **verde:** hai la precedenza e non stai facendo nulla di scorretto;
- **giallo:** hai la precedenza **ma ne stai abusando**: hai appena cambiato rotta verso l'altra (16), l'hai acquisita da pochi secondi (15), sei sopravento e orzi oltre la rotta corretta (17); in caso di contatto la penalità sarebbe tua.
Sempre facoltativo nelle impostazioni (spento di default), solo regate dell'1b, solo con un'altra barca entro 8 m che si avvicina. Secondo segnale oltre al colore: rosso più spesso e giallo tratteggiato (leggibile anche senza i colori). Il verde dice «hai la precedenza», **non «puoi urtare»**: lo scrive il testo dell'impostazione. Solo attorno alla barca del giocatore.
I colori rosso e verde sono già usati dai filetti (sulla vela) e dagli scafi di Rossa e Verde (pieni): il bordo si distingue perché è un contorno su scafo bianco; lo controllo con uno screenshot ingrandito prima di chiudere.

## Ordine proposto (ogni passo con la sua fermata 1 e le sue misure)
1. **1.0.40: la funzione e il semaforo con quello che c'è già**, più le regole che non servono finestre di tempo: **11 e 12 giuste** (definizione di affiancate/dietro con i contorni degli scafi, già disponibili dalla 1.0.39) e **13** (durante la virata). Semaforo rosso/verde. Testi di fine regata con il numero della regola.
2. **1.0.41: 15 e 16, e il giallo.** Modello a finestra: dopo un cambio di chi ha la precedenza dovuto a una manovra sua (virata, strambata, poggiata), la barca con la precedenza deve dare spazio per un tempo; se ha cambiato rotta verso l'altra nei secondi precedenti, la colpa è sua. Le soglie (secondi, gradi, distanza) sono ipotesi nostre: scelte su un gruppo di semi, confermate su un altro.
3. **1.0.42: 17 e 23**, poi **18 (la boa)**, che è la più grossa e riguarda dove oggi si concentrano i contatti (partenza e giro di boa).
4. **Il «danno» (regola 14).** Oggi tutti i contatti sono senza danno e quindi chi ha la precedenza sarebbe sempre esonerato. Proposta: definire «contatto serio» (velocità relativa al momento dell'urto oltre una soglia nostra) e in quel caso la penalità va anche a chi, avendo la precedenza, poteva evitarlo. Soglia da scegliere con i dati dei contatti; è una decisione di Ale perché cambia la pesantezza del gioco.
Ogni regola introdotta ha una lezione o un riquadro che la spiega **prima** che il gioco la applichi (principio 4: non punire ciò che non è stato spiegato), nel livello del regolamento.

## Criteri generali (attese nostre, valgono per ogni passo)
1. **Casi scritti a mano da F15:** per ogni regola almeno 6 coppie (barche, prue, vento) con l'esito atteso dal testo; la funzione deve dare 6 su 6 per regola. Il metro (le coppie) è scritto nel collaudo, non letto dal gioco, e deve aver visto casi di tutte le regole.
2. **Coerenza:** in tutte le regate dell'1b (semi 1-20), per ogni contatto il semaforo un istante prima, la penalità e il testo dicono la stessa cosa (0 contraddizioni su n contatti, n > 0).
3. **Barca e 1a invariate:** `polare.js`, `raffiche_e_virate.js`, impronta delle scene dell'1a identica alla versione precedente.
4. **Effetti sulle regate:** contatti con penalità per regata, penalità per barca e piazzamenti del torneo prima e dopo, riportati senza soglia.
5. Pannello 0 px; prova in pagina senza `#collaudo`; collaudi sui contatti (`torneo`, `competizione`, `aggressiva`, `contatto_senza_colpa`, `registro`, `contatto_vero`) ancora verdi o cambiati con la ragione dichiarata.

## Rischi
- Le regole di giudizio (15, 16, 17) tradotte in soglie possono dare penalità che a un velista sembrano ingiuste in casi limite: non ci sarà una persona esperta a giudicarle; le soglie si scelgono sui testi di F15 e su casi pubblicati (se si trovano), e il limite si dichiara.
- Più regole = più penalità: il torneo (punteggi con +1 punto a ogni contatto con colpa) diventa più duro; va rimisurato a ogni passo.
- Le regole 17 e 18 hanno molte eccezioni nel testo: se ne implementa il nucleo, e la parte lasciata fuori si dichiara.

## Decisioni di Ale (23 ottobre 2026, sera)
Ordine e versioni come sopra: **sì**. Regola 14 con il «contatto serio»: **sì**. Barche scuffiate (regola 23) come ostacolo nell'1b: **sì**. Sono cose che si porteranno anche nei livelli successivi.

## 1.0.40, dettaglio (fermata 1)
**Cosa entra:** la funzione `chiCede(A, B)`, le regole 11 e 12 giuste, la 13, il semaforo rosso/verde. Niente giallo (è la 1.0.41), niente 15-18. Solo nell'1b (`R.lv2`): l'1a resta com'è, identica al bit.

**Definizioni (da F15, parafrasate, con i contorni degli scafi già disponibili dalla 1.0.39).**
- **Dietro / davanti:** la barca X è «dietro» a Y se tutto lo scafo di X sta dietro la linea al traverso che passa per il punto più a poppa dello scafo di Y. Si calcola proiettando i punti dei due contorni sulla direzione della prua di Y. **Affiancate** = nessuna delle due è dietro all'altra.
- **Sopravento:** fra due barche affiancate con le stesse mure, è sopravento quella che sta dal lato da cui arriva il vento rispetto all'altra (lato delle mure).
- **Regola 12:** stesse mure e non affiancate: cede quella dietro.
- **Regola 13:** una barca è «in virata» da quando la prua passa il vento fino a quando è di nuovo di bolina (angolo al vento vero ≥ 42°, ipotesi nostra) o dopo 10 s (limite di sicurezza, ipotesi nostra). Finché è in virata cede a tutte le altre; le regole 10, 11, 12 non valgono. Se lo sono in due, cede quella che sta a sinistra dell'altra (lato sinistro) o, se non si può dire, quella dietro.
- Le definizioni usano solo lo scafo (boma e vela fuori, come per il contatto): limite dichiarato.
- Le regole 10-12 valgono per mure; il caso «mure opposte» resta com'è (cede chi ha il vento a sinistra).

**Dove si spiegano.** Nell'1b non ci sono ancora lezioni; l'introduzione di ogni regata dell'1b (il riquadro «Istruzioni») dice in due frasi le regole in vigore (10, 11, 12, 13) e la voce «Mure» del glossario viene completata. **La lezione 3 dell'1a non si tocca:** dice già la regola 10 e la 11 con «affiancate», e resta vera. Il testo di fine regata dice il numero della regola e il motivo («regola 12: eri dietro, dovevi lasciare strada»).

**Semaforo.** Bordo dello scafo del giocatore: rosso se `chiCede` direbbe che deve cedere, verde se l'altra. Compare solo con un'altra barca (non finita, non scuffiata) entro 8 m e in avvicinamento (distanza in calo rispetto a 1 s prima); sparisce oltre 10 m o dopo 2 s di allontanamento. Spessore 0,12 m (rosso) e 0,08 m (verde), invece di 0,05. Impostazione «Semaforo di precedenza sullo scafo (regate dell'1b)», spenta di default, che dice: «verde = hai la precedenza, non il permesso di urtare».

**Costanti nuove e quali sono ipotesi.** 42° e 10 s della regola 13; distanza 8 m, rilascio a 10 m, 2 s; spessori del bordo. Tutte ipotesi nostre. Nessuna costante fisica.

**Criteri (attese nostre).**
1. **Casi a mano da F15:** almeno 6 coppie per regola (10, 11, 12, 13) con l'esito atteso dal testo, scritte nel collaudo (non lette dal gioco), compresi i casi di confine: dietro per pochi centimetri, affiancate per pochi centimetri, virata finita da poco. `chiCede` deve dare l'esito atteso in 24 casi su 24.
2. **Coerenza:** in tutte le regate dell'1b (salti di vento e torneo, semi 1-15, principianti ed esperti) il colore del semaforo un passo prima di ogni contatto del giocatore è quello della penalità assegnata: 0 contraddizioni su n contatti con n > 0 (riporto n e quanti senza semaforo visibile).
3. **Barca e 1a invariate:** `polare.js` e `raffiche_e_virate.js` carattere per carattere; impronta delle 63 scene identica alla 1.0.39 con la copia che include `fonts/`; con l'impostazione spenta l'immagine del mare dell'1b identica alla 1.0.39.
4. **Effetti sulle regate (nessuna soglia, riportati com'escono):** quanti contatti cambiano colpevole rispetto alla regola di oggi, penalità per barca e per regata, piazzamenti medi del torneo. Se cambiano tanto lo dico e si decide insieme.
5. Pannello 0 px (`esplora.py --rigioca`), `collaudo_torneo.py`, `collaudo_competizione.py`, `collaudo_aggressiva.py`, `collaudo_contatto_senza_colpa.py`, `collaudo_registro.py`, `collaudo_contatto_vero.py` verdi (o cambiati con la ragione dichiarata); prova anche in pagina senza `#collaudo`.

**Rischi.** (1) Gli avversari sono guidati con «mure a sinistra cede» e «evita chi sta davanti»: con la regola 12 chi arriva da dietro cede, e ci possono essere più penalità agli avversari che tamponano; lo misuro. (2) La regola 13 dà torto a chi è in virata: i principianti virano spesso vicino ad altri; più penalità al giocatore nel torneo. (3) Il confine «affiancate» è sensibile al contorno: va provato con i casi di confine.

**Collaudi nuovi:** `collaudo_regole.py` (24 casi a mano, criterio 1; entrerà in `lancia_tutti.sh`), `collaudo_semaforo.py` (criterio 2 e impostazione spenta).

**Stato: 1.0.40 fatta il 23 ottobre 2026** (misure e collaudi nel CHANGELOG). La 1.0.41 e la 1.0.42 sono servite a correzioni dal check visivo e la 1.0.43 alla virata dell'1b: i numeri dell'«Ordine proposto» scalano di tre (15 e 16 = 1.0.44; 17, 23, 18 = 1.0.45).

## 1.0.44 (scritta come 1.0.43), dettaglio (fermata 1): regole 15 e 16, e il giallo

Stato: **proposta, nessun codice scritto** (23 ottobre 2026, notte). Solo nell'1b (`R.lv2`); l'1a resta com'è.

**Cosa dicono le regole (F15, parafrasate).**
- **15:** chi acquisisce la precedenza deve, all'inizio, dare all'altra lo spazio per lasciarle strada; non vale se la precedenza le arriva per una manovra dell'altra.
- **16.1:** chi ha la precedenza e cambia rotta deve dare all'altra lo spazio per lasciarle strada. **16.2:** di bolina, se la mure a sinistra sta passando sotto (a poppa) della mure a dritta, questa non deve poggiare se così l'altra deve cambiare rotta subito.
- «Spazio» (definizione di F15) = lo spazio che serve per manovrare **prontamente e da buon marinaio**. La barca che non ha avuto spazio ed è stata costretta a urtare è esonerata (regola 43.1): nel gioco la penalità passa a chi aveva la precedenza.

**Il modello più semplice plausibile: una finestra di tempo, giudicata al momento del contatto.** `chiCede(A, B)` oggi dice chi cede per le regole 10-13 (la «precedenza di base»). Si aggiunge un controllo dopo:
1. **Regola 15.** Per ogni coppia di barche si ricorda l'istante in cui la precedenza di base è passata dall'una all'altra e **chi l'ha causato**: la barca che in quel passo ha cambiato mure o è uscita dalla virata (finisce la regola 13); se il cambio viene dall'affiancamento (12 ↔ 11), la barca che va più veloce delle due; se cambiano mure tutte e due nello stesso passo, nessuna. Se il contatto avviene entro **T secondi** dal cambio e la barca con la precedenza l'ha acquisita per una manovra sua, cede lei (regola 15). Se l'ha acquisita per una manovra dell'altra, niente: resta la base.
2. **Regola 16.** Se la barca con la precedenza (e la aveva già da più di T secondi) negli ultimi **T secondi** ha cambiato prua di almeno **G gradi**, e la virata della prua l'ha portata **verso** l'altra (la direzione in cui vede l'altra si è avvicinata alla prua), cede lei (regola 16). La 16.2 (poggiare di bolina sulla mure a sinistra che passa a poppa) è un caso di questo stesso controllo: la riporto come «16» e lo dichiaro.
3. Il **giallo** del semaforo: la precedenza di base è del giocatore, ma il controllo 15 o 16 la farebbe passare a lui. In altre parole: «hai la precedenza, ma se urti adesso la penalità è tua». Stesse regole di comparsa del rosso e del verde (barca entro 8 m che si avvicina). Secondo segnale oltre al colore: bordo **tratteggiato** (rosso pieno e più spesso, verde pieno sottile). Il testo dell'impostazione si allunga di una riga nel suggerimento al passaggio del mouse («giallo = hai la precedenza ma l'hai appena presa o hai appena cambiato rotta verso l'altra: dalle spazio»).
Penalità, testo di fine regata e semaforo leggono lo stesso risultato di `chiCede` (che ritorna anche `base`, la regola 10-13 di partenza): non possono contraddirsi.

**Da dove vengono T e G.**
- **T (secondi) = tempo di reazione + tempo di manovra della barca dell'1b.** Il tempo di reazione è un'ipotesi nostra (1 s, «prontamente»); il tempo di manovra **si misura con la barca** (stesso `step()` dell'1b): una barca su rotta di collisione con una che ha appena preso la precedenza davanti a lei, che dopo il tempo di reazione mette la barra a fondo (poggia o orza, la migliore delle due); T è il minimo «tempo al contatto» da cui riesce a evitarla. Le geometrie (angolo d'incontro, velocità, vento 6/10/15 nodi) sono sorteggiate: **T si sceglie sui semi 1-50** (il valore che copre il 90% dei casi, attesa nostra) **e si conferma sui semi 51-100** (deve venire entro ±0,5 s). Attesa a occhio prima di misurare: 2-4 s.
- **G (gradi):** deve stare sopra le correzioni normali di rotta, altrimenti ogni barca con la precedenza sarebbe sempre «in colpa». Si misura il cambio di prua in T secondi delle barche con la precedenza che **non** stanno manovrando (non in virata né in strambata), nelle regate dell'1b: **G = il 95° percentile sui semi 1-10, confermato sui semi 11-20** (entro ±3°). Attesa a occhio: 10-20°.

**Costanti nuove, tutte ipotesi nostre:** tempo di reazione 1 s; la regola «90% dei casi» per T e «95° percentile» per G; «chi va più veloce» come autore del cambio d'affiancamento; «verso l'altra» come condizione della 16.1 (il testo vale per ogni cambio di rotta, ma allontanandosi non si causa un contatto). Nessuna costante fisica.

**Semplificazioni da dichiarare.** (1) Dentro la finestra ogni contatto è colpa di chi ha la precedenza, qualunque cosa abbia fatto l'altra: non giudico se l'altra ha manovrato «da buon marinaio» (una barca potrebbe approfittarne urtando apposta; nella realtà violerebbe la 14). (2) Un salto di vento che cambia le mure senza che la barca giri conta come una sua manovra (raro). (3) Il controllo vale solo al contatto: senza contatto nessuna penalità, come oggi.

**Fonti in più da leggere alla fermata 2:** i casi pubblicati di World Sailing sulle regole 15 e 16 (`racingrulesofsailing.org/cases`, testo protetto: si parafrasano e si citano col numero) per scrivere i casi a mano; si aggiungono a `FONTI-PUBBLICHE.md`.

**Dove si spiegano.** L'introduzione delle regate dell'1b aggiunge una frase: «Chi prende la precedenza con una sua manovra, o cambia rotta verso l'altra, deve lasciarle il tempo di scansarsi (regole 15 e 16).» Testi di fine regata: «regola 15: avevi appena preso la precedenza virando e non le hai dato il tempo di scansarsi»; «regola 16: avevi la precedenza ma hai cambiato rotta verso di lei».

**Criteri (attese nostre, scritte prima di misurare).**
1. **Casi a mano** (da F15 e dai casi pubblicati), scritti nel collaudo: almeno 6 per la 15 (fra cui: virata davanti a una mure a sinistra con contatto entro T e appena dopo T; mure a sinistra che vira davanti a una mure a dritta, che riceve la precedenza per manovra altrui e quindi non è in colpa; affiancamento da dietro sottovento), almeno 6 per la 16 (orzata e poggiata verso l'altra, cambio sotto G, cambio allontanandosi, cambio più vecchio di T, 16.2 di bolina) e almeno 4 per il giallo. Esito atteso in tutti; i 35 controlli di oggi di `collaudo_regole.py` restano verdi.
2. **Coerenza del semaforo:** come nella 1.0.40 (colore un passo prima del contatto = penalità, 0 contraddizioni su n > 0), **e il metro deve aver visto almeno un contatto col giallo**; se il pilota non ne produce, li produco con scene a mano e lo dico.
3. **Barca e 1a invariate:** `polare.js` e `raffiche_e_virate.js` carattere per carattere; impronta delle 63 scene identica a una copia della 1.0.42 (con `fonts/`).
4. **Effetti sulle regate, riportati senza soglia:** quanti contatti cambiano colpevole per la 15 e per la 16 (su n), penalità per barca, torneo col pilota (penalità a regata e piazzamento medio). Gli avversari **non** conoscono ancora 15 e 16: l'aggressiva prima del via punta le barche mure a sinistra (regola 16 sì, nel suo comportamento): mi aspetto più penalità per lei, lo misuro.
5. Pannello 0 px (`esplora.py --rigioca`), finestra delle impostazioni senza scorrere, collaudi sui contatti verdi (`torneo`, `competizione --veloce`, `aggressiva`, `contatto_senza_colpa`, `registro`, `contatto_vero`, `semaforo`), prova in pagina senza `#collaudo`.

**Rischi.** (1) T troppo lungo rende la regola 10 quasi inutile dopo ogni virata (chi vira davanti è sempre in colpa per qualche secondo); troppo corto la 15 non scatta mai: per questo T viene dalla barca e non da un numero scelto. (2) L'autore del cambio d'affiancamento «chi va più veloce» può sbagliare quando la barca davanti rallenta (per esempio dopo una virata): lo conto nei casi a mano. (3) Più penalità a chi ha la precedenza: i principianti che virano vicino alle altre (già penalizzati dalla 13) ora lo saranno anche appena finita la virata.

**Collaudi:** `collaudo_regole.py` esteso (criterio 1), `collaudo_semaforo.py` esteso (criterio 2 col giallo), uno strumento nuovo `tests/misura_finestra.js` (o dentro `misura_regole.py`) per T e G.

**Per Ale, da decidere prima del via:** (a) se la 16.2 basta come caso della 16.1 (consiglio sì); (b) se il giallo tratteggiato va bene come secondo segnale; (c) se va bene che dentro la finestra la colpa sia sempre di chi ha la precedenza (semplificazione 1). **Risposte di Ale (23 ottobre 2026): sì, sì, sì.**

**Misure di T e G (fermata 2, prima del codice nel gioco).**
- **T** (`tests/fisica/finestra.js`; la barca che deve cedere, dopo 1 s, gira di 15, 30, 45 o 90° con la sola freccia da una parte o dall'altra, la migliore delle otto): semi 1-50, 50 casi validi su 50, mediana 3,4 s, **90° percentile 5,2 s** (incrocio 4,3 s, affiancamento 6,2 s). Conferma sui semi 51-100: 4,8 s, entro ±0,5 s. **T = 5,2 s**, più lungo della mia attesa (2-4 s): lo allungano gli affiancamenti con poco angolo di convergenza. Prima di questa versione la manovra era «barra a fondo e tenuta» e negli affiancamenti mandava la barca nell'angolo morto (T fino a 8 s non evitabile): corretto prima di scegliere.
- **G** (`tests/misura_finestra.py`, T = 5,2 s, regata dei salti di vento, principianti ed esperti): **la regola scritta sopra dà G = 53,2°** sui semi 1-10 (8631 campioni), confermato sui semi 11-20 (55,2°). Ma la popolazione non è quella che intendevo: le barche vicine a un'altra non fanno «correzioni normali», fanno manovre vere (prima del via 95° = 59-62°; dopo il via 40-43°, giri di boa e scansate comprese), cioè proprio i cambi di rotta che la regola 16 deve guardare. Le sole correzioni di rotta (barca senza nessuna entro 30 m, dopo il via, oltre 20 m dalla boa, niente cambio di mure): **95° percentile 8,5°** sui semi 1-10 (43 605 campioni), **9,3°** sui semi 11-20. **Il metro di G è da decidere con Ale:** cambiarlo dopo aver visto i numeri va detto (lo dico qui).
