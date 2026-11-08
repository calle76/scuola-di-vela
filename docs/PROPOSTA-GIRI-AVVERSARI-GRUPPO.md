# Proposta: gli avversari fanno i giri anche in gruppo (osservazione 99, fermata 1)

**8 novembre 2026, su `main` (1.2.17). Fermata 1: nessuna riga del gioco cambiata.** Ale: «vai con la 99».

## 1. In breve

Un avversario con un debito di giri comincia a girare solo dopo il via, dopo aver passato la linea, con **nessuna barca entro 4 lunghezze** e ad almeno 25 m da boe e arrivo (`giroAI`, `GIRO_AI_VIA`). In gruppo aspetta a lungo, e i debiti presi prima del via (la maggior parte) restano tutti fino a dopo la partenza. Il regolamento chiede i giri «appena possibile» e, se l'infrazione è prima del via, prima del via (F15 44.2; F74, Perry). Proposta: **giri anche prima del via** (non nell'ultimo mezzo minuto) e **3 lunghezze libere invece di 4**.

## 2. Un errore da correggere prima

Il «22% di avversari arrivati con giri non fatti» scritto stamattina (`PROPOSTA-GIRI-GIOCATORE.md` §10, `DECISIONI.md`, `CHANGELOG.md` 1.2.16) era sbagliato: contava anche le righe del giocatore. Il numero giusto: **6 su 120 (5%)** sulla 1.2.15, **5 su 120 (4%)** sulla 1.2.17, Chromium, semi 361-380; con `misura_avversari.py` e con lo strumento nuovo lo stesso numero. Ale ha scelto B (avversari ancora a +15 s) su quel numero: la scelta va riproposta (§7).

## 3. Cosa succede oggi (misura, `tests/misura_giri_avversari_liberi.py`, semi 361-380, principianti ed esperti, 40 regate per browser)

| | Chromium | Firefox |
| --- | --- | --- |
| debiti presi dagli avversari (di cui prima del via) | 61 (43) | 50 (30) |
| tempo con un debito senza girare: prima del via | 53% | 42% |
| … bloccati da una barca entro 4 lunghezze | 39% | 49% |
| … dopo il via ma prima di passare la linea | 7% | 6% |
| … vicino a boa o arrivo | 2% | 3% |
| dopo il via, barca più vicina: mediana | 2,4 L | 2,6 L |
| dopo il via, nessuno entro 3 L / 4 L | 28% / 5% del tempo | 38% / 5% |
| **attesa dopo il via prima dei giri** (mediana; 75%; massimo) | **21 s; 77 s; 204 s** | **42 s; 100 s; 185 s** |
| arrivati con giri non fatti | 5 su 120 (4%) | 2 su 120 (2%) |

Lo strumento guarda una volta al secondo e solo finché la barca non gira: i momenti liberi brevi gli sfuggono (per questo la riga «ha avuto almeno un secondo con nessuno entro 4 L» che stampa non si usa).

Nella regata di Ale delle 10:03 (osservazione 99) due avversari sono arrivati con 4 giri non fatti ciascuno: è il caso peggiore, non quello tipico.

## 4. Il modello più semplice

In `giroAI` (`js/regate.js`), due cambi:
1. **Giri anche prima del via**, se mancano più di `GIRO_AI_PRIMA` = 30 s allo sparo e la barca è dietro la linea (non `ocs`): stesse condizioni di via libera. Nell'ultimo mezzo minuto no (la barca si prepara a partire, e girare lì vuol dire mettersi in mezzo alle altre); il debito resta e si sconta dopo il via come oggi.
2. **Via libera a 3 lunghezze** (`GIRO_AI_VIA` da 4 a 3; `GIRO_AI_STOP`, 2 lunghezze, non cambia).

Non cambia: come gira (sequenza di prue, verso, 21.2), la distanza da boe e arrivo, il +15 s per giro non fatto (in attesa della scelta del §7).

## 5. Criteri (soglie nostre, scritte prima di misurare)

Semi 361-380 per la scelta, conferma sui **381-400** mai guardati; Chromium e Firefox; prima e dopo.

- **K1, aspettano meno:** attesa dopo il via, mediana **al massimo 10 s** e 75% **al massimo 40 s**, in tutti e due i browser.
- **K2, giri fatti:** arrivati con giri non fatti **al massimo 2%** (oggi 4% e 2%).
- **K3, non si toccano di più:** colpe degli avversari e contatti del giocatore al massimo **+10%**.
- **K4, si gira bene:** `collaudo_giri_avversari.py` (80 regate) verde, in particolare G5 (fermi), G6 (scuffie), G7 (giri durante i quali si prende un altro debito, soglia 15%).
- **K5, la partenza non peggiora:** avversari in partenza anticipata e ritardo mediano al via (`collaudo_partenze.py`, numeri della 1.2.15) non peggiori di oggi più il 10%.
- **K6, barca invariata:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.
- **Da riportare:** dove si fanno i giri (prima del via, di bolina, di poppa).

## 6. Costanti nuove

`GIRO_AI_PRIMA = 30` s: ipotesi nostra (il tempo in cui gli avversari si avvicinano alla linea per partire: l'avvicinamento comincia a 45 s, la simulazione della partenza a 30 s). `GIRO_AI_VIA` da 4 a 3 lunghezze: ipotesi nostra, scelta perché dopo il via la barca più vicina sta in media a 2,4-2,6 lunghezze e a 4 lunghezze libere si arriva solo il 5% del tempo.

## 7. Da decidere con Ale: la squalifica per gli avversari

Con il numero giusto (4-5% oggi, 2% in Firefox) la soglia che Ale aveva messo per passare alla squalifica («meno del 5%») è già quasi raggiunta. Quindi:
- **A.** Squalifica anche per gli avversari **insieme a questa correzione**, quando K2 è raggiunto (al massimo 2%). **Consigliato**: stessa regola per tutti, e con questa correzione chi non fa i giri è raro.
- **B.** Resta com'è (+15 s per gli avversari), si decide dopo aver giocato.

## 8. Rischi

- **Giri prima del via in mezzo alla flotta:** sono in attesa a 1,5-6 lunghezze dalla linea; il via libera a 3 lunghezze e lo stop a 2 restano. K3 e K5 controllano.
- **3 lunghezze sono poche:** un giro dura circa 20 s, un'altra barca può arrivare; lo stop a 2 lunghezze interrompe il giro (G7 controlla).
- **Vale anche per la Scuola** (stessa guida): cambiano i risultati della regata con i giri e i collaudi che la usano.

## 9. Fonti

F15, regola 44.2 (giri appena possibile dopo essersi allontanati); F74 (Perry): con un'infrazione prima del via la penalità si fa prima del via, non dopo. «3 lunghezze» e «30 s» sono scelte nostre.

## 10. Fermata 2 (8 novembre 2026, Ale: «ok, vai con la A»): **K1 e K3 non raggiunti**

Ale ha dato il via e scelto A (squalifica anche per gli avversari se K2 è raggiunto). Fatto in `js/regate.js`: giri prima del via salvo negli ultimi 30 s, `GIRO_AI_VIA` 3, squalifica in `giriMancantiAI`; `collaudo_giri_avversari` G9 aggiornato alla squalifica. Misure con `misura_giri_avversari_liberi.py` (aggiunti i contatti del giocatore), prima su una copia congelata della 1.2.17, dopo su una copia della modifica.

| | Chromium 361-380 | Firefox 361-380 | Chromium 381-400 | Firefox 381-400 | Soglia |
| --- | --- | --- | --- | --- | --- |
| K1 attesa dopo il via, mediana | 21 → 18 s | 42 → 12 s | 30 → 42 s | 49 → 26 s | ≤ 10 s: **no** |
| K1 attesa, 75% | 77 → 38 s | 100 → 58 s | 68 → 68 s | 85 → 52 s | ≤ 40 s: **no** |
| K2 arrivati con giri non fatti | 4% → 0% | 2% → 1% | 1% → 0% | 2% → 2% | ≤ 2%: sì |
| K3 colpe degli avversari | 61 → 60 | 50 → 49 | 47 → 49 | 50 → 41 | +10%: sì |
| K3 contatti con colpa del giocatore | 28 → 32 (+14%) | 26 → 26 | 23 → 27 (+17%) | 22 → 20 | +10%: **no** (Chromium) |
| tempo con un debito dopo il via (s, in tutto) | 2254 → 1046 | 2421 → 1294 | 2035 → 1331 | 2537 → 1148 | riportato |
| barca più vicina dopo il via, mediana | 2,4 → 2,0 L | 2,6 → 1,9 L | 2,0 → 1,8 L | 2,3 → 1,9 L | riportato |

K4-K6 non misurati: con K1 e K3 fuori soglia non servono a decidere.

**Cosa ne ricavo.** I giri prima del via funzionano: il tempo con un debito dopo il via si dimezza e i giri non fatti spariscono quasi del tutto. Ma chi prende un debito dopo il via aspetta ancora: anche 3 lunghezze libere in gruppo ci sono solo il 3-10% del tempo (le barche, ora, stanno più vicine: 1,8-2,0 lunghezze). Abbassare ancora la soglia vuol dire girare con le barche addosso. La cosa che fanno i velisti veri è un'altra: **allontanarsi** dal gruppo (la 44.2 dice «dopo essersi ben allontanata»), poggiando o lasciando passare, e poi girare. Oggi l'avversario con un debito continua la sua rotta col gruppo e aspetta che il gruppo si allarghi.

I contatti del giocatore su Chromium (+4 e +4 su 23-28) sono numeri piccoli e in Firefox non salgono; non li spiego, li riporto come sono.

**Stato:** la modifica è nel lavoro di `js/regate.js` e `tests/collaudo_giri_avversari.py`, **non committata**. Da decidere con Ale.

## 11. Decisione di Ale e seconda versione (fermata 1)

Ale (8 novembre): «ok, vai con la 3»: tolta la prima versione (`js/regate.js` e `collaudo_giri_avversari.py` di nuovo identici al commit 98f2b9b), proposta nuova: **chi ha una penalità prima si allontana dal gruppo, poi gira**, come chiede la 44.2 («dopo essersi ben allontanata dalle altre barche»). La squalifica degli avversari (scelta A) entra quando K2 è raggiunto.

**Modello** (in `giroAI`, `js/regate.js`):
1. **Giri prima del via**, salvo negli ultimi `GIRO_AI_PRIMA` = 30 s (dalla prima versione, che funzionava: tempo con un debito dopo il via dimezzato). Prima del via la barca **non** cerca spazio (rovinerebbe l'attesa sulla linea): gira solo se lo spazio c'è.
2. **Dopo il via, cercare spazio.** Con un debito, se la via non è libera (una barca entro `GIRO_AI_VIA` lunghezze) e la barca non è entro 25 m da una boa o dall'arrivo, invece di tenere la rotta del gruppo la barca prova poche prue: quella che voleva, la stessa poggiata o orzata di 20°, 40° e 60° (mai dentro l'angolo morto né oltre 172° dal vento), e in bolina anche la virata. Sceglie quella che, con la previsione che la guida ha già (`passaggio`, 15 s in linea retta), passa più lontano da tutte le barche; a pari distanza (entro mezza lunghezza) la più vicina alla rotta voluta. Appena la via è libera, gira come oggi.
3. **Non per sempre:** al massimo `GIRO_AI_CERCA` = 45 s di ricerca per debito; poi torna a tenere la rotta e ad aspettare come oggi (così una barca non va lontano dal percorso).
4. Via libera a **3 lunghezze** (`GIRO_AI_VIA`), stop a 2 (`GIRO_AI_STOP`) come oggi.
5. **Squalifica** di chi arriva con giri da fare (scelta A), solo se K2 è raggiunto; se no resta +15 s.

Mentre cerca spazio la barca non sta scontando (la 21.2 vale solo durante i giri) e cede come sempre (`cedeAvv1b` resta prima). Non cambia: come gira, il verso, la distanza da boe e arrivo.

**Criteri:** gli stessi del §5, **soglie non cambiate** (K1 attesa dopo il via mediana ≤ 10 s e 75% ≤ 40 s; K2 giri non fatti ≤ 2%; K3 colpe degli avversari e contatti del giocatore ≤ +10%; K4 `collaudo_giri_avversari` verde, aggiornato alla squalifica solo se K2; K5 partenze; K6 barca), in più:
- **K7, non si va lontano:** tempo d'arrivo mediano degli avversari che hanno avuto un debito, al massimo +10% rispetto a oggi; avversari non arrivati 0; boe dal lato sbagliato non più di oggi.
- **Da riportare:** quante volte si cerca spazio, quanto dura, quante volte si arriva ai 45 s senza trovarlo.

Il prima è già misurato (copia congelata della 1.2.17, §10: semi 361-380 per la scelta, 381-400 per la conferma, Chromium e Firefox).

**Costanti nuove:** `GIRO_AI_PRIMA` = 30 s (§6), `GIRO_AI_CERCA` = 45 s, scarti di 20°, 40° e 60° (come gli scarti per cedere, `SCARTI` 15-60°), tutte ipotesi nostre.

**Rischi:** chi cerca spazio poggiando può andare addosso a una terza barca (K3); in bolina, poggiando, perde terreno (K7); 45 s possono non bastare in una flotta stretta (lo diciamo con il dato «arrivati ai 45 s»).
