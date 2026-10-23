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
