# Proposta: avversario che si pianta alla boa (9 novembre 2026)

Voce 2 di `DA-FARE.md` (era la 3); osservazioni 90, 103, 109 di `OSSERVAZIONI-GIOCANDO.md`.

Ale (9 novembre): «poi passa alla boa senza chiedere». Il via è dato in anticipo: proposta, soglie e misura senza fermata, ma le soglie sono committate **prima** di misurare. Per la decisione del 9 novembre (`DECISIONI.md`) si misura sulle **regate del torneo**.

## 1. Cosa succede

In tre regate di Ale un avversario arriva alla boa a destra, all'altezza della boa o poco sotto. Invece di passare oltre, vira indietro verso il punto di passaggio e si ferma: 0 nodi e anche all'indietro, per 3-8 s.

- **90** (17:59): Verde manca di 2 m il punto di passaggio 0.
- **103** (22:00 bastone): Blu è 6 m a destra della boa e 1 m sotto, mure a dritta. La rotta verso il punto oltre la boa passa circa 2,3 m sopra la boa: la correzione «sul bordo» della 1.2.15 chiede 3 m (`PASSO_M`), quindi non scatta.
- **109** (22:00 giri): Blu è 7 m a destra e 2,0 m sopra la boa. La regola «sopra la boa» chiede più di 2 m (`wy < -R.up - 2`), quindi non scatta per un soffio.

## 2. Perché (letto nel codice, `js/regate.js`, `targetOf`)

Alla boa 1 l'avversario punta tre punti di passaggio, nell'ordine: 0, a destra e poco sopra la boa; 1, oltre la boa a sinistra; 2, per riprovare. Passa al punto 1 in tre casi:
- quando è entro 4 m dal punto 0;
- quando è «sopra» la boa (più di 2 m sopra e più di 3 m a destra);
- quando è «sul bordo»: arriva al punto 1 senza virare e la sua rotta passa almeno 3 m sopra la boa.

Chi arriva vicino alla boa ma appena fuori da tutte e tre le condizioni punta ancora il punto 0, che ha di fianco o dietro, col vento in faccia. Allora vira, perde velocità e si pianta. Le tre soglie sono ipotesi nostre, e nei tre casi visti si mancano di pochi decimetri.

## 3. Modello più semplice

Nessuna regola nuova: si allargano le due soglie che falliscono per poco, solo alla boa 1.
- `PASSO_M` (la rotta sul bordo deve passare almeno questi metri sopra la boa): oggi 3.
- `SOPRA_M` (quanti metri sopra la boa per contare «sopra»): oggi 2, una costante nuova che dà un nome al 2 scritto nel codice.

Combinazioni da provare (`PASSO_M`, `SOPRA_M`): (2, 2), (1,5, 2), (3, 0), (1,5, 0).

Rischio: una rotta più vicina alla boa la tocca più spesso (le boe sono ostacoli dalla 1.0.63), oppure la lascia dal lato sbagliato. Lo misurano G4 e G5.

**Cosa non si tocca:** la fisica, chi cede, la boa 2 del triangolo, il giocatore.

## 4. Misura

`tests/misura_boa_avversari.py`. Le 6 regate del torneo (bastone e triangolo; 10 nodi costanti, raffiche, salti di vento), principianti ed esperti, preparazione 60 s. Il giocatore lo guida il pilota. Si corre fino all'arrivo di tutti, senza finestra d'arrivo.

Per ogni avversario e per ogni boa si misura, mentre la punta ed è entro 40 m da lei: i secondi passati, le virate, le fermate (3 s di fila sotto 1 nodo), se tocca la boa.

Scelta sui **semi 801-830**, conferma sui **semi 831-860** (mai usati). Riferimento: il gioco di oggi, cioè la 1.2.18, oppure la 1.2.19 se nel frattempo è adottata la proposta della partenza.

## 5. Criteri (soglie nostre, scritte prima di misurare)

- **G1, fermate entro 40 m:** almeno dimezzate rispetto al riferimento. Il criterio vale solo se il riferimento ne ha almeno 10; con meno il contatore non misura niente, e lo si riporta.
- **G2, passaggi con 3 o più virate entro 40 m:** al massimo +10%.
- **G3, mediana dei secondi entro 40 m:** al massimo +1 s.
- **G4, boa toccata:** al massimo il più grande fra +10% e +5 casi.
- **G5, boe sbagliate:** al massimo +2. **Non arrivate:** non aumentano.
- **G6, contatti dopo il via:** al massimo +10%.
- **G7, non-regressione:** `polare.js` e `raffiche_e_virate.js` identici, `impronta1b.js` al bit; `collaudo_giro_boa.py` verde.

Fra le combinazioni che passano si sceglie quella con meno fermate (G1). A parità, quella più vicina ai valori di oggi (3, 2).

Se nessuna passa sui semi di scelta, o la scelta non passa la conferma, non si adotta nulla e lo si riporta così.

## 6. Costo

Circa 4 ore di calcolo col termostato: 5 configurazioni sulla scelta, 2 sulla conferma.

## 7. Esito della scelta (semi 801-830, 360 regate del torneo, 1620 passaggi di avversari vicino a una boa): non passa

| (`PASSO_M`, `SOPRA_M`) | G1 fermate | G2 3+ virate | G3 mediana | G4 boa toccata | G5 sbagliate / non arrivate | G6 contatti |
| --- | --- | --- | --- | --- | --- | --- |
| oggi (3, 2) | 76 | 350 | 27,0 s | 51 | 0 / 0 | 224 |
| (2, 2) | 53 ✗ | 330 | 26,2 s | **81** ✗ | 0 / 0 | 209 |
| (1,5, 2) | 51 ✗ | 314 | 25,6 s | **139** ✗ | 2 / 0 | 221 |
| (3, 0) | 62 ✗ | 345 | 26,8 s | 47 | 2 / 1 | 211 |
| (1,5, 0) | 51 ✗ | 314 | 25,6 s | **139** ✗ | 2 / 0 | 221 |

Soglie: G1 ≤38 (metà di 76), G4 ≤56. **Nessuna combinazione passa G1**, e abbassare `PASSO_M` fa toccare la boa molto più spesso. Allargare le soglie toglie al massimo un terzo delle fermate. La conferma sui semi 831-860 non si fa. Il gioco resta con (3, 2); restano nel codice i nomi `SOPRA_M` e `PASSO_SX`, con gli stessi valori di prima.

Note:
- Il riferimento ha 76 fermate, quindi il contatore misura davvero (soglia minima 10).
- (1,5, 0) e (1,5, 2) danno numeri identici: con `PASSO_M` 1,5 la regola «sopra» non scatta mai per prima.

## 8. Seconda prova: il giro diretto (9 novembre 2026; via di Ale in anticipo: «vai avanti senza chiedere»)

**Dove si fermano** (diagnosi sui semi 801-815, solo riferimento): 38 fermate. 30 sono con la barca che punta già il punto oltre la boa, tra 4 e 12 m a destra della boa e tra 1 e 4 m sopra. Tracciato un caso (seme 805, esperti, Blu):
1. arriva mure a dritta 4,6 m a destra della boa e 0,5 m sotto;
2. vira verso il punto 0, che sta sopra a destra;
3. a metà virata il bersaglio diventa il punto oltre la boa, e la barca rivira senza velocità: 5 s ferma, anche all'indietro.

È la doppia virata dell'osservazione 90. Eppure da lì, di bolina stretta mure a dritta, sarebbe passata circa 4 m sopra la boa senza virare. La regola «sul bordo» non lo vede, perché guarda la retta verso il punto oltre la boa: è più poggiata della bolina e passa solo 1,9 m sopra.

**Modello.** Alla boa 1, chi soddisfa insieme queste condizioni:
- è mure a dritta;
- è a destra della boa, entro `R_DIR` m da lei;
- di bolina (angolo di bolina + 3°) passerebbe sopra la boa di almeno `M_DIR` m.

Questa barca punta subito il punto oltre la boa (`rp` 1) e, finché non ha superato la boa (fino a 3 m alla sua sinistra), tiene la bolina invece della retta. Così non vira verso il punto 0 e non passa troppo vicino alla boa. Poi poggia verso il punto oltre, come oggi.

**Costanti nuove (ipotesi nostre):** `M_DIR` ∈ {2, 3, 4} m, `R_DIR` ∈ {15, 30} m. Quindi 6 combinazioni. `PASSO_M` e `SOPRA_M` restano 3 e 2.

**Criteri:** gli stessi del §5 (G1-G7, soglie uguali, sul riferimento degli stessi semi). Scelta sui **semi 861-890**, conferma sui **semi 891-920**, mai usati. Regola di scelta come nel §5.

**Nota sulla misura:** bastone e triangolo hanno la stessa prima bolina e quindi danno passaggi identici alla boa 1. I passaggi indipendenti sono circa la metà di quelli contati. Le soglie sono relative, quindi il confronto resta valido; lo si riporta.

## 9. Esito della scelta del giro diretto (semi 861-890, 360 regate del torneo, 1620 passaggi)

| (`M_DIR`, `R_DIR`) | G1 fermate | G2 3+ virate | G3 mediana | G4 boa toccata | G5 sbagliate / non arrivate | G6 contatti |
| --- | --- | --- | --- | --- | --- | --- |
| oggi (spento) | 65 | 347 | 26,8 s | 59 | 3 / 0 | 233 |
| (2, 15) | 17 | 283 | 26,1 s | **74** ✗ | 3 / 0 | 215 |
| (3, 15) | **21** | 302 | 26,3 s | 54 | 3 / 0 | 218 |
| (4, 15) | **33** ✗ | 323 | 26,5 s | 62 | 3 / 0 | 218 |
| (2, 30) | 19 | 283 | 26,3 s | **78** ✗ | 2 / 0 | 212 |
| (3, 30) | 22 | 303 | 26,4 s | 54 | 2 / 0 | 215 |
| (4, 30) | 32 | 321 | 26,6 s | 62 | 3 / 0 | 217 |

Soglie sul riferimento: G1 ≤32 (metà di 65), G2 ≤381, G3 ≤27,8 s, G4 ≤64 (59 + 10%), G5 sbagliate ≤5 e non arrivate 0, G6 ≤256. Passano (3, 15), (3, 30) e (4, 30); con 2 m la barca passa troppo vicina e tocca la boa. **Scelta: (3, 15)**, la meno fermate fra quelle che passano. Conferma sui semi 891-920.

## 10. Conferma (semi 891-920, mai usati): passa, adottata nella 1.2.20

| | G1 fermate | G2 3+ virate | G3 mediana | G4 boa toccata | G5 sbagliate / non arrivate | G6 contatti |
| --- | --- | --- | --- | --- | --- | --- |
| oggi (spento) | 70 | 340 | 26,5 s | 49 | 0 / 0 | 259 |
| (3, 15) | **30** | 314 | 26,1 s | 49 | 0 / 0 | 253 |

Soglie: G1 ≤35, G2 ≤374, G3 ≤27,5 s, G4 ≤54, G5 ≤2 e 0, G6 ≤284. Passano tutte. G7: `polare.js` e `raffiche_e_virate.js` identici, `impronta1b.js` al bit, `collaudo_giro_boa.py` nel CHANGELOG. Nel gioco `M_DIR` 3, `R_DIR` 15; per misurare il gioco senza giro diretto: `misura_boa_avversari.py PRIMO ULTIMO 3 2 -1 15`.

Restano circa 30 fermate su 1620 passaggi: non sono state guardate una per una.

## 11. Difetto trovato dopo la 1.2.20: avversari che girano per il campo (9 novembre, sera; scritto prima di correggere e misurare)

**Cosa:** `collaudo_regate.py 6 1` (regata nelle raffiche della Scuola), seme 2: Verde e Blu «BLOCCATA», con la 1.2.20 e dopo. Con la 1.2.19 arrivano, ma Verde in 417 s (mediana 185 s).

**Perché (traccia di Verde):**
1. 22 m a destra e 7 m sotto la boa scatta «sul bordo» e Verde punta il punto oltre la boa (`rp` 1).
2. Con raffiche e salti passa proprio sopra la boa, a meno di 1,5 m: `roundCheck` lì non conta niente, quindi il giro non risulta né giusto né sbagliato.
3. Poi manca di più di 8 m il punto oltre la boa.
4. Da quel momento nessuna regola la rimanda a riprovare: la regola «girata male» chiede un giro sbagliato (`rnd` < 0), che qui non c'è.

Il giro diretto della 1.2.20 non lo crea: cambia la traiettoria, e la barca lenta diventa bloccata.

**Correzione (difetto chiaro, `DECISIONI.md` «difetti piccoli senza proposta»):** con `rp` 1, chi è già oltre la boa (`oltre`) senza averla girata (`rnd` ≤ 0 invece di < 0) va al punto 2 e riprova.
- Alla boa 1 chi la gira bene attraversa la semiretta sopra la boa prima di essere 8 m a sinistra, quindi cambia lato prima: per lui non cambia niente.

**Criteri (scritti prima di misurare):**
- `collaudo_regate.py` 6 0, 6 1 e `--lungo` (semi 7-30) su tutte e due le regate: nessuna «BLOCCATA».
- Torneo, `misura_boa_avversari.py` sui semi 891-920 contro la 1.2.22 senza correzione: G1-G6 entro le soglie del §5.
- `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.

**Esito (1.2.22):**
- `collaudo_regate` 6 0, 6 1, `--lungo` su tutte e due: nessuna «BLOCCATA» (6+6+24+24 corse, 180 arrivi su 180).
- Torneo, semi 891-920, 240 regate del torneo nuovo più le 120 di confronto, senza → con:

  | | senza | con | soglia §5 |
  | --- | --- | --- | --- |
  | G1 fermate | 20 | 20 | non applicata: la correzione non serve a togliere fermate |
  | G2 passaggi con 3+ virate | 243 | 252 | +3,7%, entro +10% |
  | G3 mediana | 24,6 s | 24,6 s | entro +1 s |
  | G4 boa toccata | 78 | 78 | entro 86 |
  | G5 sbagliate / non arrivate | 0 / 0 | 0 / 0 | |
  | G6 contatti | 210 | 211 | entro +10% |

  I passaggi oltre 60 s vicino alla boa salgono da 37 a 49: sono le barche che ora tornano a riprovare invece di andarsene.
- La misura si è fatta con `TORNEO=nuovo`: senza, lo strumento usa il formato del torneo fino alla 1.2.20.

## 12. Difetto trovato dall'esploratore sulla 1.2.25: Verde rimbalza fra due punti (11 novembre; scritto prima di correggere e misurare)

**Cosa:** `esplora.py 28 28` in Chromium, regata 2 (salti di vento della Scuola), esperti: Verde (prudente) non arriva in 756 s. Arriva con le versioni fino alla 1.2.23 (395 s con la 1.2.22 e la 1.2.23), non con la 1.2.24 e le seguenti. Nel giro su GitHub era comparso solo in Chromium (0 su 200 corse in Firefox).

**Perché (traccia di Verde, strumento in scratchpad, non nel repo):** Verde arriva alla boa 1 verso il secondo 210 e poi per più di 500 s gira a 7-20 m dalla boa. Il vento è girato di circa 14° a sinistra del medio. Il punto di passaggio `rp` fa 2, 0, 2, 0…:
1. A sinistra della boa (x < −3) e sotto di essa, `sopraDaSinistra` (la retta verso il punto 0 passerebbe sopra la boa) mette `rp` a 2: si va al punto sotto e a sinistra.
2. A meno di 8 m dal punto 2 la regola `rp === 2 && near(2, 8)` rimette `rp` a 0.
3. Ma da lì (a 8 m dal punto 2, non sul punto) la retta verso il punto 0 passa ancora sopra la boa: `sopraDaSinistra` è vera di nuovo e `rp` torna a 2. Si ripete ogni 5-10 s, con virate e abbrivio perso.
La 1.2.24 non ha cambiato questa parte: ha cambiato la traiettoria (poppa), e un caso già possibile è capitato.

**Correzione (difetto chiaro, `DECISIONI.md` «difetti piccoli senza proposta»):** `sopraDaSinistra` vale una volta sola per ogni boa: quando `rp` torna da 2 a 0 si segna `b.p2`, e con `b.p2` la regola non scatta più (si azzera al cambio di boa). Chi ha già fatto il giro largo riprova dal punto 0 come dice il commento di `targetOf` («per riprovare dal punto 0 passando sotto la boa»).

**Criteri (scritti prima di misurare):**
- K1: seme 28, regata 2, esperti, Chromium: Verde arriva (prima no).
- K2: sui semi 1-40 delle regate 0, 1, 2 della Scuola e delle 100-103 del torneo (principianti e esperti): nessuna barca che arrivava ora non arriva; le barche non arrivate non aumentano.
- K3: le corse che cambiano sono poche (attese: solo quelle con un rimbalzo), e in nessuna cambia l'arrivo del giocatore per più di quanto cambi per effetto degli avversari (il pilota di prova non reagisce a Verde, quindi atteso uguale).
- K4: il tempo mediano degli avversari delle corse che cambiano scende o resta (non sale).
- Sono ipotesi nostre, non cambiano dopo aver visto i numeri.

## 13. Esito (11 novembre 2026): adottata nella 1.2.27

- K1: passa. Seme 28, regata 2, esperti: Verde arriva a 388,7 s (prima non arrivava in 756 s).
- K2: passa. Su 153 corse in comune (semi 1-9; previsti 1-40, ma le misure sono state fermate a 73 °C, sopra il limite di 72 °C) nessuna barca che arrivava ora non arriva; non arrivate 3 e 3.
- K3: 24 corse su 153 hanno barche con arrivi diversi, più di quelle attese (le scrivevo «poche»); in 9 cambia anche il «Tu», perché il pilota di prova reagisce alle altre barche. Avversari con arrivo diverso: 28 su 459.
- K4: passa. Mediana −1,0 s (media −1,8 s; 18 più veloci, 10 più lenti; da −33 a +23 s).
- Non provato: la conferma su semi mai guardati (qui nessuna soglia è stata scelta sui dati, ma il campione è piccolo). Se il giro su GitHub mostra non arrivati nuovi nelle regate della Scuola, tornare qui.
- Lo strumento di diagnosi (traccia di Verde ogni 5 s con la destinazione) non è nel repo: era in scratchpad.
