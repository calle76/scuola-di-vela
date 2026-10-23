# Proposta: la prua che va oltre la bolina dopo la virata (livello 2), giocatore e avversari

19 ottobre 2026, fermata 1. **Nessun codice nel motore.** Aggiunta solo la misura `tests/fisica/virate2.js` (legge il motore, non lo cambia).

## 0. In breve

Nella barca del livello 2, dopo la virata, la prua continua a girare ben oltre la bolina: 60-81° dal vento per il giocatore che centra la barra, **97-111° per gli avversari**. Nel livello 1 e nel 470 vero (F4) si ferma a circa 45°, al più 10-15° oltre. La causa è nel motore, non nella mano di Ale né (solo) nella guida degli avversari: con `yawRho` = 0 la rotazione la frena **solo la pala**, e la pala frena col quadrato della velocità e in più stalla, cioè non frena quasi niente proprio a fine virata, quando la barca va a 1-2 nodi e gira in fretta. Proposta: aggiungere lo smorzamento dell'acqua sullo scafo che ruota, che non dipende dalla velocità (la costante c'è già, `BOMA2.Kq`), e ritarare `yawG` perché la virata resti lunga come oggi.

## 1. Cosa dicono le registrazioni [misura]

`sessione-20261018-2228(1).txt` (la prima registrazione è il suo inizio, identico): «Regata nei salti di vento», barca del livello 2, 10 nodi, 21 virate.

- Ale tiene → (o ←) circa 2-4 s con la sola freccia (barra 78%, cioè 35°), poi centra con lo spazio quando la prua è già 30-60° oltre il vento.
- **Dopo aver centrato la prua gira ancora 20-45°**: massimo 65-92° dal vento in 14 virate su 21 (bolina: 45-50°). Esempio t=52: 34° → 62° → 83° → 92° con la barra a 0.
- **In 4 (t=735, 991, 1053, 1272) arriva a 115-180°**, cioè in poppa. A t=735 Ale tiene la barra a −78% (cioè contro la rotazione) per 6 s a 1,0 nodi e la prua passa lo stesso da 95° a 180°.

## 2. Cosa dice la fonte [fonte, letta sulla figura]

F4 (Masuyama e Ogihara 2020, figure 5 e 6, sei virate di un 470 vero, 6-7 nodi di barca): dopo la virata la prua arriva a **55-60° al massimo** e torna a circa 45° entro 1-2 s; la barra torna a circa 0 (al più −5/−15° per un istante) e non serve tenerla contro. Velocità minima 2-3 nodi. Il 470 è più pesante (circa il doppio) e a due: vale per l'ordine di grandezza, non cifra per cifra.

## 3. Misura nel motore di oggi [misura, `node tests/fisica/virate2.js`]

Bolina a regime, poi barra a 1,6/s fino a 35° (livello 2, sola freccia) o 30° (livello 1); quando la prua è 0°, 20° o 35° oltre il vento la barra va a 0 di colpo (lo spazio). Valori: prua massima dal vento sulla mura nuova.

| Vento | Centra a | Livello 1 | Livello 2 | Livello 2, secondi per smettere di girare | Livello 2 con barra contro |
|---|---|---|---|---|---|
| 6 | 20° oltre | 34° | 67° | 4,4 | 32° |
| 10 | 20° oltre | 32° | **71°** | 3,2 | **94°** |
| 10 | 35° oltre | 43° | 68° | 2,4 | 88° |
| 14 | 20° oltre | 32° | **81°** | 2,8 | **96°** |

(Tabella completa con 0° e 35° nell'uscita dello script.) Due cose sgradite: **la barra contro peggiora** con 10 e 14 nodi (la pala è già in stallo per la sola rotazione, la barra in più aggiunge solo resistenza: la barca rallenta e la pala frena ancora meno); e sotto 0,5 m/s il motore passa al timone del livello 1, che ferma la rotazione in 0,25 s: a 1,0 nodi (0,51 m/s, il caso di t=735) si è appena sopra quel confine e la barra non serve quasi a niente (circa 3°/s² di frenata).

**Avversari** (la guida di `regate.js`: `tillerFor`, `react`, `sheetFor`; il bersaglio passa da una bolina all'altra):

| Vento | Principiante liv. 1 | liv. 2 | Esperto liv. 1 | liv. 2 |
|---|---|---|---|---|
| 6 | 51° | 80° | 46° | 66° |
| 10 | 51° | **97°** | 46° | **109°** |
| 14 | 51° | **101°** | 46° | **111°** |

Tornano in bolina da soli, ma per qualche secondo vanno al traverso: è il «rosse e blu a 90° dalla boa» visto da Ale. Nel livello 1 nessun superamento. La guida non va cambiata per prima: frena la rotazione con `s.r · 0.02`, che funziona se la barca smette di girare quando la barra torna al centro, come nel livello 1 e nel 470.

## 4. Modello proposto (il più semplice plausibile)

Nel ramo `lv2` di `step()`, oltre alla pala, l'acqua frena lo scafo che ruota, indipendentemente dalla velocità:

`dr/dt = −yawG·u·(u·F + yawRho·r) − (Kq / Izz)·r·|r|`

- `Kq` = 1230 N·m·s²: **esiste già** (`BOMA2.Kq`, stima da carena, pala e deriva, usata da «spingi il boma»). Si sposta in un posto comune, stesso valore.
- `Izz` **costante nuova, stima senza fonte**: momento d'inerzia d'imbardata di barca e timoniere. Ordine di grandezza `mass · (L/4)²` ≈ 150 kg·m²; da verificare con la sensibilità (100 e 220).
- `yawG` **si ritara** (oggi 0,6, ipotesi) perché la virata con la sola freccia resti nei criteri C4 di oggi: lo smorzamento rallenta anche la virata.
- Fuori dal livello 2 non cambia niente; il confine a 0,5 m/s resta, ma con lo smorzamento la rotazione arriva lì già piccola.

Scartate: alzare `yawRho` (frena col prodotto u·r, cioè niente a barca lenta, dove serve); togliere lo stallo alla parte dovuta alla rotazione (non è fisica); correggere solo gli avversari (resterebbe il giocatore, e la barca verrebbe prima del resto: «prima la barca, poi il resto»).

## 5. Criteri (soglie dichiarate ora, attese nostre ricavate da F4)

Taratura su 10 e 14 nodi, **conferma su 6, 8, 12 e 16 mai guardati**.

- **V1** giocatore, sola freccia, centra a 20° e a 35° oltre il vento: prua massima **≤ 60°** dal vento.
- **V2** rotazione sotto 2°/s **entro 1,5 s** dal momento in cui si centra.
- **V3** la barra contro non peggiora: prua massima con barra contro ≤ senza.
- **V4** C4 di `timone2.js` (virata con la sola freccia 2,5-4,5 s) e C5 (velocità minima 35-60%) restano nelle soglie dove lo sono oggi; per gli altri criteri di `timone2.js` si riportano i numeri prima e dopo.
- **V5** avversari, livello 2: prua massima dopo la virata **≤ up + 15°** (principiante ≤ 66-69°, esperto ≤ 61-63°) in Node; e nel browser, nella «Regata nei salti di vento» senza giocatore, misurata su ogni virata: **semi 1-20 per guardare, 21-60 per confermare**, quante virate superano up + 15° (attesa: al più il 5%), con il numero di virate misurate (non zero).
- **V6** livello 1 identico al bit: impronta, `polare.js` e `raffiche_e_virate.js` carattere per carattere.
- **V7** `boma2.js` e `salti2.js` nelle soglie; giro di penalità (oggi 7,4-11,6 s con Maiusc) riportato prima e dopo.

Se V5 non regge con la sola fisica, solo allora si propone un ritocco della guida per il livello 2 (con fermata a parte).

## 6. Rischi

- `Izz` e `Kq` sono stime: la sensibilità dirà se il risultato dipende da loro più di quanto si possa difendere.
- Lo smorzamento allunga anche il giro di penalità e potrebbe portare C4 fuori con 6 nodi (già fuori oggi).
- «Spingi il boma» usa il ramo del livello 1: non cambia, ma va controllato (V7).
- Le figure di F4 sono di un 470 a due, con rollio e fiocco che il gioco non ha.

## 7. Dopo questo compito (non ora)

Dall'elenco di Ale del 18 ottobre: posizione dopo la raddrizzata e tempo per girare; distacchi in regata; cosa influenza abilità e conoscenza; il punto 6 manca. Poi trapezio e triangolo.

---

## 8. Revisione in chat (19 ottobre 2026) e misura della variante proposta dalla chat

La chat ha letto questa proposta e `PROPOSTA-STALLO-TIMONE.md`. Osservazioni accolte, con quello che ne segue.

**Verificato nel codice:** la pala usa davvero solo `u²` (`js/motore.js`, riga 175: `−yawG·u·(u·F + …)`), anche se l'acqua le arriva pure di lato per la rotazione. **Variante A (chat, punto 1.3), zero costanti nuove:** la pala sente `V² = u² + (r·xR)²`. È fisica di base [stima], con `xR` che esiste già. Misurata su una copia del motore fuori da `js/` (cartella temporanea), senza toccare il gioco:

| | Oggi | Variante A |
|---|---|---|
| Giocatore, prua massima (6/10/14 nodi, centra a 20° e 35° oltre) | 67-81° | **50-59°** (V1 ≤ 60: ok) |
| Secondi per smettere di girare | 2,1-4,4 | 1,6-3,3 (V2 ≤ 1,5: **fuori**) |
| Con la barra contro (10 e 14 nodi) | 88-96° | 62-67° (peggio che senza: **fuori**) |
| Avversari principianti / esperti | 80-101° / 66-111° | **51-55° / 59-62°** (V5 ≤ up+15, cioè 61° per l'esperto con up 46: al limite) |
| `timone2.js` | — | virate e giri di penalità quasi uguali (C4 2,93 contro 2,94 s con 16 nodi); C8 con 6 nodi rientra (3,18 s); C1 e C3 fuori come oggi |

**Dichiarato:** la variante è stata misurata su tutti i venti, quindi in Node non esistono più venti «mai guardati» per V1 e V5. Restano mai guardati i semi delle regate nel browser (V5, semi 21-60).

**Altre osservazioni accolte:**
- **Pala contata due volte** (1.2): `BOMA2.Kq` comprende la pala, che nel livello 2 è già calcolata. Se serve lo smorzamento dello scafo (variante B), si usa la **sola parte dello scafo, circa 600 N·m·s²** [stima della chat: scafo circa 750, pala circa 700, deriva poco; totale coerente con 1230].
- **Izz** (2.2): 200 kg·m² come valore centrale, con sensibilità 130-300 (comprende la massa d'acqua trascinata da pala e deriva); fissato **prima** di misurare, non tarato. Il lato pericoloso è quello alto (più inerzia, più rotazione dopo la virata).
- **Calcolo stabile** (1.5): `r = r / (1 + k·|r|·dt)`, che non inverte mai il verso della rotazione.
- **`yawRho`** (1.4): con l'uscita a 1-2 nodi non vale zero; resta una possibilità, ma solo stimata, non tarata.

**Criteri cambiati dopo la revisione (prima della fermata 2, ma dopo aver visto la variante A: dichiarato):**
- **V3 più forte:** con la barra contro la prua massima scende di almeno 5° con 10 e 14 nodi, e aiuta anche con l'uscita a circa 1 nodo.
- **Nuove misure da riportare:** la sovra-rotazione (prua massima meno prua quando si centra; attesa 15-25°); la sovra-rotazione in funzione della velocità di uscita, da 0,3 a 1,0 m/s, senza scalini al confine dei 0,5 m/s; C3 e C9 prima e dopo; l'oscillazione di rotta del pilota in bolina.
- **V5 nella regata nei salti:** la prua si misura rispetto al vento di quel momento.
- **Prova di Ale:** rifare la stessa regata registrandola; da confrontare con le 14 virate su 21 oltre 65° di oggi.

**Ordine proposto per la fermata 2:**
1. Variante A nel motore (solo `S.lv === 2`).
2. Se V2 e V3 restano fuori: variante B, cioè A più lo smorzamento del solo scafo (`Kq_scafo` 600, `Izz` 200, forma stabile), con la sensibilità di `Izz` 130-300. Da decidere, misurando, se applicarlo anche sotto 0,5 m/s nel livello 2 (oggi lì vale il timone del livello 1: va controllato che retromarcia e «spingi il boma» non cambino).
3. **Se con valori plausibili V2 o V3 non reggono, il limite si dichiara** e non si gonfiano le costanti (chat, 4.2): la causa probabile è fisica che manca, soprattutto il momento della randa che dopo la virata riporta la barca in bolina.
4. Gli avversari si ritoccano solo se V5 resta fuori con la barca corretta.

---

## 9. Fermata 2: cosa è stato fatto e cosa è uscito (19 ottobre 2026, versione 1.0.31, non ancora committata)

**Fatto** (`js/motore.js`, solo il ramo `lv2` di `step()`): la pala sente `V² = u² + (r·xR)²`; dopo la pala, `r /= 1 + hullKq/Izz·|r|·dt` con `hullKq` 600 e `Izz` 200 (stime della chat, non tarate); `yawG` da 0,6 a **1,5**. Il ramo sotto 0,5 m/s, la retromarcia e «spingi il boma» non cambiano.

**Come è stato scelto `yawG`.** Variante A (solo V²) misurata per prima: V1 ok, V2 e V3 fuori (§8). Variante B con `yawG` 0,6: la virata dura 6-8,5 s e la barca scende al 14-26% (C4 e C5 fuori ovunque), quindi si ritara `yawG`, come previsto. Regola della 1.0.24, fissata allora: più criteri fra C1, C2, C4 e C5 con 10 e 14 nodi, a parità la curvatura più bassa. Griglia 1,3 / 1,5 / 1,75 / 2 / 2,5 / 3: 4, 6, 6, 6, 6, 6 su 8; scelto 1,5 (curvatura 0,29). **Dichiarato:** un primo conteggio sbagliato dello script sommava anche i venti di conferma; ne ho visto solo il totale, poi rifatto sui soli 10 e 14. Applicare lo smorzamento anche sotto 0,5 m/s (variante B2) non cambia quasi niente: scartato, così retromarcia e angolo morto restano identici.

**Risultati.**

| Criterio | Esito | Numeri (oggi → 1.0.31) |
|---|---|---|
| V1 prua massima ≤ 60° (giocatore, centra a 20° e 35° oltre) | **ok** | 67-81° → 34-40° |
| V2 rotazione ferma entro 1,5 s | **ok** | 2,1-4,4 s → 0,6-0,8 s |
| V3 barra contro: almeno 5° di meno | **fuori** | aiuta al più di 1,2°; ora la prua va oltre di soli 4-15° dal momento in cui si centra, e resta poco da correggere |
| Sovra-rotazione (attesa della chat 15-25°) | sotto l'attesa | 33-60° → 4-15° |
| Uscita lenta 0,3-1,0 m/s, senza scalini | **ok** | prima a 0,8 m/s saltava a 72°; ora 31-35° per tutte le velocità |
| V4 C4 virata 2,5-4,5 s | **fuori con 6 e 8 nodi** | 6: 4,89 → 6,11 s (già fuori); 8: 3,85 → 4,89 s (nuovo fuori); 10, 12, 14, 16 ok (4,25 / 3,93 / 3,69 / 4,49 s) |
| V4 C5 minima 35-60% | **fuori con 16 nodi** | 36% → 25% (16 nodi); gli altri ok |
| C1 (Maiusc perde più velocità) | **fuori ovunque** | prima ok su 5 venti su 6; ora con Maiusc si perde **meno** |
| C3 curvatura 0,12-0,30 | **ok ovunque** | 0,36-0,39 → 0,29 (prima sempre fuori) |
| C8 strambata | ok ovunque | prima fuori con 6 nodi |
| C9 risposta a 5° di barra | ok | 0,17-0,49 → 0,05-0,17 s: barca più pronta (rischio 4.3 della chat) |
| Oscillazione del pilota in bolina (Node) | — | 0,1-0,4° → 0,0-0,1° |
| Giro di penalità (sola freccia / Maiusc) | — | 10 nodi 9,5 / 7,4 → 12,4 / 10,0 s; 6 nodi 14,5 / 11,6 → 18,7 / 15,3 s; 14 nodi 7,6 / 5,9 → 10,3 / 8,1 s |
| Stallo della pala, barra a fondo in 0,6 s | — | 0-1,08 s → 0-0,28 s: l'avviso diventa raro |
| V5 avversari in Node | **ok** | 66-111° → esattamente la bolina (46°, 51°) |
| V5 avversari nel browser (`collaudo_virate2.py`), conferma semi 21-60 | **fuori** | virate oltre la bolina + 15°: 97,1% → **17,1%** (1003 virate misurate); mediana +58,9° → +0,3°. Guardati 1-20: 96,3% → 12,3% (479). Misura in più (aggiunta dopo aver visto i semi 1-2): prua quando la rotazione si ferma, 96,1% → 7,3% |
| V6 livello 1 identico al bit | **ok** | impronta OK sul riferimento rigenerato sulla 1.0.30 (quello della 1.0.27 era vecchio: falliva anche sulla 1.0.30 senza modifiche); `polare.js`, `raffiche_e_virate.js` identici |
| V7 `boma2.js`, `salti2.js` | **ok** | `boma2.js` identico; `salti2.js` nelle soglie, vedi sotto |

**V5 nel browser: perché resta il 17%.** Nelle 8 virate «oltre» dei semi 1-2, tutte avevano un'altra barca a 7-20 m (la guida la evita a 14-22 m) o stavano arrivando alla boa; in metà la prua si ferma a 48-53° e gira di nuovo dopo 8-9 s, cioè una manovra voluta della guida, non la prua che va oltre. La soglia del 5% resta e il risultato è fuori.

**`salti2.js`: difetto del pilota di prova, trovato e corretto.** Col motore nuovo il pilota di `salti_bolina.js` non arrivava alla boa in 17 bolinate «sui salti» su 40: vicino alla boa virava due volte di fila, la seconda a 1,5 nodi, e restava nell'angolo morto (prima la prua che girava da sola lo faceva passare). `salti2.js` restava OK contando 23 bolinate su 40, con un guadagno gonfiato (15,5%). Corretto il pilota (non vira sotto 1,2 m/s) e `salti2.js` ora vuole tutte le bolinate arrivate. Con lo stesso pilota: 1.0.30 7,0% / 5,4%, 1.0.31 **6,2% / 8,1%**, 40 su 40, S2 40 su 40.

**`collaudo_timone2.py` nel browser: FALLITO (6 su 12 controlli).** Tutte le virate riescono (10 nodi: sola freccia 3,93 s e 42%, Maiusc 3,05 s e 47%), ma con Maiusc la pala non stalla più, e i 6 controlli «la pala stalla e il suggerimento lo dice» falliscono.

**Lettura.** La prua dopo la virata ora si comporta come nel 470 vero (si ferma dove si centra la barra) e gli avversari non vanno più al traverso: il difetto visto da Ale è risolto. Il prezzo:
1. **Lo stallo della pala quasi sparisce e Maiusc non costa più velocità** (C1 fuori ovunque): la lezione «non sbattere la barra» della 1.0.24-1.0.25, già debole, ora non ha più effetto nelle virate.
2. **Virate più lente con poco vento** (8 nodi 4,9 s) e giri di penalità più lunghi del 30% circa.
3. Avversari nel browser al 17% contro il 5% della soglia, per le manovre volute della guida.

Decisione di Ale: tenere la 1.0.31 così (aggiornando `collaudo_timone2.py` e dichiarando i limiti), oppure tornare alla 1.0.30.

**Prova di Ale e decisione (19 ottobre 2026).** Registrazione `sessione-20261019-1612.txt` (gioco 1.0.31, stessa regata, 10 virate): prua massima nei 12 s dopo la virata fra 48° e 57° in 7 virate su 10 (il 18 ottobre oltre 65° in 14 su 21). Le tre più larghe (66°, 89°, 168°) sono fatte con la barra ancora tenuta (la terza prima del via, quasi fermo, barra tenuta 10 s); dopo lo spazio la prua va oltre di 5° al più. Avviso di stallo 2 volte. **Ale: si tiene la 1.0.31.** `collaudo_timone2.py` aggiornato: lo stallo nelle 12 virate si riporta e non si pretende; un controllo nuovo lo crea apposta (barca al 30%, barra a fondo di colpo: 0,53 s di stallo, avviso presente).
