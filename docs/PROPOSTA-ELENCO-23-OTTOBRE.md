# Proposta: sette correzioni dall'elenco di Ale (23 ottobre 2026)

Stato: **proposta (fermata 1), nessun codice scritto.** La barca dell'1b (lenta, da rivedere) resta fuori: è l'ultimo lavoro, prima del congelamento.
Ordine e versioni previste: **1.0.37** punti 5, 4, 2; **1.0.38** punti 3, 6, 7; **1.0.39** punto 1. Tra una versione e l'altra solo i collaudi legati alla modifica; il giro completo lo lancia Ale alla fine.

## 5. Lezione 3, passi 8-9: il passo dopo si chiude da solo
**Causa (letta nel codice).** `ttState()` (`js/gioco.js:78`) dà «sopravento» sotto 8° di incidenza della vela e «dritti» da 8° a 27°. Il passo 8 si chiude appena l'incidenza scende sotto 8°, cioè sul confine; la barca prosegue, l'incidenza risale di poco e il passo 9 («filetti dritti», cond. `tt === "ok"`) trova la condizione già vera e si chiude dopo 1,5 s senza che il giocatore faccia niente. Stesso rischio fra i passi 9 e 10 (confine a 27°).
**Modello più semplice.** Margine nei passi, non nel motore: `readI()` espone anche `alpha` e le condizioni diventano: passo 8 `alpha < 6`; passo 9 `10 <= alpha <= 25`; passo 10 `alpha > 29`. Il filetto sullo schermo non cambia (la soglia fisica dei filetti resta 8 e 27). Nessuna costante fisica; i 2° di margine sono un'ipotesi nostra.
**Criteri.** (a) Riprodotto prima della correzione: lasca piano fino al filetto, poi fermo la scotta: il passo 9 si chiude da solo in meno di 2 s in almeno una parte dei tentativi. (b) Dopo: in 30 tentativi con semi fissi e scotta ferma al confine, il passo 9 non si chiude mai da solo (0 su 30; verificare che il controllo abbia misurato: passi 8 chiusi 30 su 30). (c) Il pilota delle lezioni percorre ancora tutta la carriera (32 passi su 32, `collaudo_carriera.py`).
**Rischio.** Il pilota delle lezioni lasca fino al confine e potrebbe non arrivare a `alpha < 6`: lo controlla il punto (c).

## 4. Lezione 3: «Le mure e le precedenze»
Il passo 6 della lezione 3 (`js/contenuti.js:118`) si chiama oggi «Le mure»; la lezione si chiama «Andature e filetti» (riga 240).
**Modello.** Titolo del passo: «Le mure e le precedenze». Titolo della lezione: «Andature, mure e filetti». Nel testo una frase che dice che chi non rispetta la precedenza paga una penalità (nelle regate del gioco 15 s, e lo dichiariamo: nelle regate vere si fanno due giri). Controllare la voce del glossario «Mure» e le domande d'esame sulle mure: ogni affermazione nautica va verificata sulle fonti (`FONTI-PUBBLICHE.md`, F15) prima di essere scritta.
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

## 1. Barca senza cerchio: scontri e soglia di attenzione
Oggi nessun cerchio: il contatto scatta a 4,2 m fra i centri (`js/regate.js:416`) e il giocatore lo vede solo a cose fatte.
**Modello.** Due anelli sottili per barca, **solo in regata e solo a barca in moto** (non nelle lezioni):
- anello **di contatto**, a 2,1 m dal centro (così due anelli che si toccano = contatto, 4,2 m);
- anello **di attenzione**, a ~8 m (la distanza oltre cui il contatto si azzera nel codice), che diventa giallo quando un'altra barca entra e la distanza sta diminuendo.
Disattivabile nelle impostazioni (principio 3: gli aiuti si possono disattivare). Se funziona, la soglia può anche attivare un messaggio breve («barca vicina: mure a sinistra, cedi»), ma questo lo propongo come passo successivo.
**Da decidere (Ale).** Anelli sempre visibili o solo quando un'altra barca è entro ~8 m? Propongo **solo entro ~8 m**, per non riempire il mare.
**Criteri.** Barca invariata nei numeri (la collisione non cambia); anelli comparsi in 100% delle regate con almeno un contatto prima del contatto (misurare quanti secondi prima); 0 px di eccesso del pannello; disattivabile.

## Verifiche comuni a ogni versione
`collaudo_versione.py`, `polare.js` e `raffiche_e_virate.js` carattere per carattere, `collaudo_pannello.py`, e in una pagina senza `#collaudo`. Al termine di ogni gruppo: `CHANGELOG.md`, `docs/COLLAUDI.md`, `VERSIONE` in `js/gioco.js`. Collaudo nuovo proposto: `collaudo_regata_intera.py`, che guida una regata col pilota fino all'arrivo e controlla ad ogni secondo pannello (0 px) e, a regata finita, il riquadro finale.
