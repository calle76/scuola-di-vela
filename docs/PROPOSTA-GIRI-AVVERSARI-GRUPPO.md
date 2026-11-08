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
