# Proposta: sette correzioni dall'elenco di Ale (23 ottobre 2026)

Stato: **proposta (fermata 1), nessun codice scritto.** La barca dell'1b (lenta, da rivedere) resta fuori: è l'ultimo lavoro, prima del congelamento.
Ordine e versioni previste: **1.0.37** punti 5, 4, 2; **1.0.38** punti 3, 6, 7; **1.0.39** punto 1 (parti A e B, separabili). Tra una versione e l'altra solo i collaudi legati alla modifica; il giro completo lo lancia Ale alla fine.

## 5. Lezione 3, passi 8-9: il passo dopo si chiude da solo
**Causa (letta nel codice).** `ttState()` (`js/gioco.js:78`) dà «sopravento» sotto 8° di incidenza della vela e «dritti» da 8° a 27°. Il passo 8 si chiude appena l'incidenza scende sotto 8°, cioè sul confine; la barca prosegue, l'incidenza risale di poco e il passo 9 («filetti dritti», cond. `tt === "ok"`) trova la condizione già vera e si chiude dopo 1,5 s senza che il giocatore faccia niente. Stesso rischio fra i passi 9 e 10 (confine a 27°).
**Modello più semplice.** Margine nei passi, non nel motore: `readI()` espone anche `alpha` e le condizioni diventano: passo 8 `alpha < 6`; passo 9 `10 <= alpha <= 25`; passo 10 `alpha > 29`. Il filetto sullo schermo non cambia (la soglia fisica dei filetti resta 8 e 27). Nessuna costante fisica; i 2° di margine sono un'ipotesi nostra.
**Criteri.** (a) Riprodotto prima della correzione: lasca piano fino al filetto, poi fermo la scotta: il passo 9 si chiude da solo in meno di 2 s in almeno una parte dei tentativi. (b) Dopo: in 30 tentativi con semi fissi e scotta ferma al confine, il passo 9 non si chiude mai da solo (0 su 30; verificare che il controllo abbia misurato: passi 8 chiusi 30 su 30). (c) Il pilota delle lezioni percorre ancora tutta la carriera (32 passi su 32, `collaudo_carriera.py`).
**Rischio.** Il pilota delle lezioni lasca fino al confine e potrebbe non arrivare a `alpha < 6`: lo controlla il punto (c).

## 4. Lezione 3: «Le mure e le precedenze»
Il passo 6 della lezione 3 (`js/contenuti.js:118`) si chiama oggi «Le mure»; la lezione si chiama «Andature e filetti» (riga 240).
**Modello.** Titolo del passo: «Le mure e le precedenze». Titolo della lezione (anche nel menu, `js/contenuti.js:240`): «Andature, mure e precedenze» (decisione di Ale, 23 ottobre; i filetti restano nel testo e nella descrizione). Nel testo una frase che dice che chi non rispetta la precedenza paga una penalità (nelle regate del gioco 15 s, e lo dichiariamo: nelle regate vere si fanno due giri). Controllare la voce del glossario «Mure» e le domande d'esame sulle mure: ogni affermazione nautica va verificata sulle fonti (`FONTI-PUBBLICHE.md`, F15) prima di essere scritta.
**Da decidere (Ale).** Nel gioco la colpa si decide con due regole: mure diverse (chi ha il vento a sinistra cede) **e** stesse mure (cede la barca sopravento, `js/regate.js:421`). La lezione insegna solo la prima. Propongo una frase in più per la seconda, così il gioco non punisce qualcosa che la scuola non ha spiegato (principio 4). Se invece vuoi la lezione solo con la prima, lo dichiaro nel CHANGELOG come limite noto.
**Criteri.** Pannello a 1360x650 con 0 px nei passi della lezione 3 (`collaudo_pannello.py`); `collaudo_quiz.py` e `collaudo_esame.py` verdi se tocco il glossario o le domande.

## 2. Il timoniere ha un braccio solo
Oggi (`js/disegno.js:496-499`) c'è un solo braccio, dalla spalla alla prolunga della barra.
**Modello.** Una seconda spalla dall'altro lato del busto e un secondo braccio con la mano sulla scotta (pozzetto, vicino al centro barca). Solo disegno, nessuna fisica. Posizione della mano e spessori sono a occhio: li giudichi tu giocando (come la 1.0.23).
**Criteri.** Barca identica nei numeri (`polare.js`, `raffiche_e_virate.js`, impronta del motore); solo i pixel del disegno cambiano, quindi riferimento dell'impronta da rigenerare **solo se** include il disegno: lo controllo prima di dirlo.

## 3. Vento e bussola nello stesso angolo, senza la versione
Oggi `drawWindBox` scrive il vento in alto a sinistra, `drawCompass` sta in alto a destra e `drawVersionTag` sta sotto la bussola (`js/disegno.js:246-248`).
**Modello.** La riga «Vento reale da … nodi» passa sotto la bussola, allineata a destra, dove oggi c'è la versione; la versione sul mare sparisce (resta nel menu, nel registratore e nel `CHANGELOG`). L'angolo in alto a sinistra resta libero.
**Rischio.** `collaudo_versione.py` controlla proprio il testo «V. …» sul mare: va cambiato per controllare il menu, e lo dichiaro. Lo spazio sotto la bussola va controllato a 1360x650 e con lo zoom dei pulsanti.
**Criteri.** Vento e bussola leggibili e senza sovrapposizioni a 1360x650 e a una finestra più piccola; `collaudo_versione.py` aggiornato e verde.

## 6. Lasco: «verde» a vela tutta aperta, ma cazzando un po' si va più veloci
**Misura (motore del gioco, scotta da 0 a 1, velocità di equilibrio in nodi; `*` = filetti «dritti», `l` = «sottovento», `w` = «sopravento»).**

| vento | angolo | scotta 0,6 | 0,7 | 0,8 | 1,0 (tutta aperta) |
|---|---|---|---|---|---|
| 10 nodi | 110° | 5,66 `*` | 5,33 `*` | 4,81 `*` | 3,47 `w` |
| 10 nodi | 125° | 4,66 `l` | 4,92 `l` | 5,18 `*` | 4,62 `*` |
| 15 nodi | 110° | 9,05 `*` | 8,02 `*` | 6,91 `*` | 4,97 `w` |
| 15 nodi | 125° | 6,24 `l` | 6,75 `l` | 7,47 `*` | 6,58 `*` |
| 15 nodi | 140° | 5,91 `l` | 5,81 `l` | 5,90 `l` | 6,31 `l` |

Quindi ha ragione Ale: a 125° e 10 nodi, da 1,0 a 0,7 si guadagna il 6% ma il pannello lo dà «troppo cazzata» (rosso); a 110° e 15 nodi la banda «dritti» è larga (da 0,6 a 0,9) e la velocità cala del 34% fra un bordo e l'altro. La banda dei filetti (incidenza 8-27°) non coincide con il massimo di velocità, che sta verso il lato cazzato. A 140° i filetti non dicono mai «dritti» e il massimo è a vela tutta aperta (già gestito dal messaggio «vento da dietro»).
**Modello più semplice.** Non si cambia la fisica né dove si agitano i filetti. Si cambia il **suggerimento «sail»** (il messaggio del pannello): da «Vela gonfia e regolata» / «troppo cazzata» a una frase che dice la verità misurata, per fasce: dentro la banda ma lontano dal massimo, «Regolata, ma cazzando un po' vai più veloce». Il «lee» a vela quasi aperta in lasco (oltre 105°) non dice più «rosso: lasca» quando cazzare farebbe guadagnare velocità. Il massimo si calcola dalla scotta che dà più velocità all'angolo e al vento di quel momento (come `autoSheet()` ma con la tabella misurata); costo: una tabella nuova o una formula, da decidere dopo aver visto più angoli.
**Criteri (attese nostre).** (a) A 15 angoli (90-150°) e 3 venti, il messaggio non è mai «troppo cazzata/rosso» quando una scotta più cazzata dà più velocità di almeno 3%; (b) non è mai «regolata/verde» quando una scotta diversa dà più del 10% in più; (c) i filetti e il motore sono identici (impronta, `polare.js`, `raffiche_e_virate.js`). Se il numero esce fuori fascia, lo riporto.
**Rischio.** I passi della lezione 3 usano `hintKind: "sail"`; i testi cambiano, il pannello deve restare a 650 px.

## 7. Pannello che sfora ancora di 17 px (scuffia a regata non finita)
Caso seme 256, salti di vento, `esplora.py --rigioca`: `status` da 198 px più la riga di scuffia. **Modello.** Cercare una riga da accorciare (la riga `hint` da 54 px con la scuffia) invece di nascondere altro. **Criterio.** 0 px in tutti i 95+100 casi di `--rigioca`.

## 1. Contatto vero fra gli scafi, e anello facoltativo di precedenza (rivisto dopo le risposte di Ale)
**Il difetto, come l'hai descritto.** Oggi il contatto scatta quando i **centri** di due barche sono a meno di 4,2 m (`js/regate.js:416`): un cerchio invisibile di raggio 2,1 m attorno a ogni barca. Lo scafo disegnato è lungo 4,2 m e largo 1,44 m (`hullPath`, `js/disegno.js:587`). Quindi due barche affiancate «si toccano» a 4,2 m di distanza, quando fra gli scafi ci sono ancora 2,8 m d'acqua; in fila, invece, il cerchio è giusto. Il contatto deve venire dal disegno.
**Parte A, contatto vero (da fare).** Il contatto scatta quando i due **contorni degli scafi** si sovrappongono (poligono dello scafo, gli stessi punti del disegno, ruotati con la prua). Chi decide la colpa non cambia (mure diverse, o sopravento a parità di mure). L'urto (velocità ×0,6 e spinta di separazione) si calcola dalla penetrazione fra i contorni invece che dalla distanza dei centri; il contatto si azzera quando i contorni sono separati di oltre 2 m (oggi 8 m fra i centri, valore da ricontrollare).
**Effetti che non so ancora e vanno misurati prima di fidarsi:**
- i contatti diventano più rari: gli avversari, tarati con il cerchio largo, potrebbero stringere di più la linea e la boa e produrre meno penalità e partenze diverse;
- il torneo (punteggi), le partenze e gli 82 sfioramenti alla boa (`PROPOSTA-PARTENZE.md` §8.6) vanno rimisurati;
- il riferimento dell'impronta e `collaudo_competizione.py` cambiano: lo dico, non lo nascondo.
**Criteri (attese nostre).** (a) Nessun contatto a meno di 2 m fra i contorni più vicini, in migliaia di istanti campionati (e il controllo deve avere visto contatti: n > 0); (b) ogni contorno che si sovrappone di oltre 5 cm produce un contatto entro 1 s (misura su molte regate con semi fissi, quante ne dico); (c) numero medio di contatti per regata prima e dopo, riportato com'è, senza soglia; (d) `polare.js` e `raffiche_e_virate.js` identici (il motore non cambia).
**Parte B, anello di precedenza (facoltativo, dal livello 1b).** Un anello attorno alla barca del giocatore, **solo in regata e solo con un'altra barca entro ~8 m**: **rosso se in caso di contatto la colpa sarebbe tua** (mure a sinistra contro mure a dritta, o sopravento con le stesse mure), **verde se la colpa sarebbe dell'altra**. Usa la stessa funzione che decide la colpa oggi in `contacts()`, così non si possono contraddire. Si attiva nelle impostazioni (spento di default, principio 3), e compare solo nelle regate dell'1b, dove le precedenze sono la parte portante; nell'1a, congelata, non cambia niente. Non nasce rotondo per forza: se vuoi, lo disegno come alone del contorno dello scafo, che segue il contorno vero di cui al punto A.
**Domande aperte per Ale.** (1) Anello rosso/verde solo per la tua barca, o anche attorno a ciascun avversario? Propongo solo la tua. (2) Quando le barche non convergono (si allontanano o sono in fila lontane) l'anello sparisce: vuoi anche questo? Propongo sì: compare solo se la distanza sta diminuendo.
**Rischio più grosso.** La parte A cambia l'andamento delle regate dell'1a (che è congelata: avvicinarsi senza sfiorare è un cambio di regola) e dell'1b. Il contatto «vero» è anche più fedele alla realtà (principio 1), ma la scelta di toccare l'1a è tua: se non vuoi, la parte A vale solo nell'1b.

## Verifiche comuni a ogni versione
`collaudo_versione.py`, `polare.js` e `raffiche_e_virate.js` carattere per carattere, `collaudo_pannello.py`, e in una pagina senza `#collaudo`. Al termine di ogni gruppo: `CHANGELOG.md`, `docs/COLLAUDI.md`, `VERSIONE` in `js/gioco.js`. Collaudo nuovo proposto: `collaudo_regata_intera.py`, che guida una regata col pilota fino all'arrivo e controlla ad ogni secondo pannello (0 px) e, a regata finita, il riquadro finale.

## Decisioni di Ale (23 ottobre 2026)
- Punto 4: sì alla seconda regola nella lezione; titolo della lezione sulle precedenze. **Fatto nella 1.0.37.**
- Punto 1: anello rosso/verde (rosso: la colpa sarebbe tua; verde: dell'altra) solo attorno alla barca del giocatore, solo con un'altra barca vicina che si avvicina, facoltativo, dall'1b. Contatto vero fra gli scafi **solo nell'1b**; l'1a resta con il cerchio (distanza di sicurezza dichiarata), e l'introduzione dell'1b lo dice: «da questo livello i contatti sono quelli veri… ora puoi avere un aiuto visivo». Collaudi dei contatti: controllare che nell'1b ci siano contatti da misurare (controllo non vuoto) e un collaudo nuovo che verifichi la regola diversa nei due livelli.
- Stato: 1.0.37 (punti 5, 4, 2) e 1.0.38 (3, 6, 7) fatte; 1.0.39 (1) da fare.
