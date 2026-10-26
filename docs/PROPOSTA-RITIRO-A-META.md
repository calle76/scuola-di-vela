# Proposta: regata del torneo lasciata a metà = ritiro (fermata 1)

26 ottobre 2026. Decisione di Ale in `DECISIONI.md` (26 ott): uscire a metà regata del torneo, dal menu o chiudendo il browser anche per sbaglio, vale come «Ritirati dalla regata»; il torneo continua. Oggi (1.0.34) la regata si rifà da capo, quindi una regata andata male si può ripetere. Questa è la fermata 1: nessun codice scritto.

## Modello più semplice

Il ritiro esiste già (`rRet`: `me.dnf = me.ret = true`, poi `torChiudi` fa arrivare gli avversari con la simulazione accelerata e salva). Non si inventa niente: si chiama lo stesso percorso in più punti.

1. **Dal menu** a regata iniziata (`showMenu`, quando `mode === "race"`, `R.tor` e la fase non è «done»): ritiro come con «Ritirati dalla regata», senza chiedere conferma (il menu ha già il suo avviso, vedi sotto).
2. **Pagina chiusa o ricaricata** (evento `pagehide`): stesso ritiro, scritto subito nel salvataggio. Il salvataggio è `localStorage` sincrono, quindi nel `pagehide` regge.
3. **Quando comincia a contare:** dal momento in cui si preme «Corri la regata», non dal via. Altrimenti si vedrebbe il vento nel conto alla rovescia e si uscirebbe per rifare (stesso trucco di oggi).
4. **Avviso:** prima di uscire dal menu a regata in corso, un `confirm`: «Uscire dalla regata? Conta come ritirata: prendi 5 punti.» Alla chiusura della pagina il browser non lascia un messaggio nostro: niente avviso, vale la decisione di Ale (anche per sbaglio).
5. **Testi** da cambiare: la frase «se chiudi la pagina, la regata interrotta si ricorre da capo» (riquadro del torneo) e il commento in testa a «torneo dell'1b» in `regate.js`; `PROPOSTA-TORNEI-1B.md` §9 (limite dichiarato), `STATO.md`, `DECISIONI.md` (la riga diventa «fatta»).

Costo di calcolo: `torChiudi` simula fino a 1800 s con tre barche. Lo misuro nel caso peggiore (uscita a pochi secondi dal via, con la finestra d'arrivo ancora aperta): se supera 2 s sul PC di Ale lo riporto, non lo nascondo.

## Limite dichiarato

Se il browser viene ucciso senza `pagehide` (blocco del PC, batteria, processo terminato), l'uscita non viene registrata e la regata si ricorre da capo come oggi. Non c'è modo di evitarlo senza salvare ogni secondo e inventare i tempi degli avversari. Lo scrivo nei documenti.

## Criteri misurabili (soglie nostre, fissate prima di misurare)

| # | Criterio | Soglia |
|---|----------|--------|
| R1 | Uscita dal menu a metà regata (4 momenti: conto alla rovescia, dopo il via, alla boa, prima dell'arrivo) × 10 tornei | 40 su 40: `tor.ris` cresce di 1, il giocatore ha 5 punti, `ret` vero, le altre barche hanno un tempo o `°` per la finestra |
| R2 | Pagina chiusa nei 4 momenti × 10 tornei, poi riaperta | 40 su 40: salvataggio uguale al caso R1 con lo stesso seme |
| R3 | Dopo l'uscita il torneo prosegue e si conclude (4 regate, di cui 1 ritirata) | 10 su 10 tornei completati, `torneoFatto` coerente con la classifica |
| R4 | Uscita a metà della **quarta** regata | 10 su 10: il torneo si chiude con piazzamento e meriti, nessun torneo rimasto in sospeso |
| R5 | Regata finita normalmente, o già ritirata col pulsante, poi menu/chiusura | 10 su 10: nessun secondo risultato (niente regata contata due volte) |
| R6 | Non-regressione | `polare.js`, `raffiche_e_virate.js` carattere per carattere, `tests/fisica/impronta1b.js` identica (il motore non si tocca); C1, C4, C6, C7 di `collaudo_torneo.py` come prima |
| R7 | Tempo dell'uscita dal menu nel caso peggiore | ≤ 2 s (attesa nostra) |
| R8 | Pannello a 1360×650 | 0 px di eccesso (C6) |

R2 è il punto debole: Playwright potrebbe non far partire `pagehide` con `page.close()`. Se non parte, lo dico e provo `page.close(run_before_unload=True)` o `location.reload()`; non scrivo il criterio come «verde» finché non vedo il controllo misurare davvero (deve esserci almeno un caso in cui `tor.ris` è cresciuto, non solo «nessun errore»).

## Collaudo da cambiare

`collaudo_torneo.py` C3 oggi controlla il contrario: «chiusura a metà della regata 2 non cambia il salvataggio». Diventa R1-R5. Le chiusure dopo una regata finita (regate 1, 2, 3) restano com'erano. C7 (`--giocatore`) chiude la pagina dopo la regata 2 a regata finita: non cambia.

Costanti nuove: nessuna. Fonti: nessuna nuova (A5.2 già usata: chi si ritira prende iscritti + 1). Ipotesi nostra: «conta dal clic su Corri», non dal via.

## Rischi

- Chi ricarica la pagina per sbaglio durante la regata perde i punti di quella regata: è la scelta di Ale, ma i punti sono 5 su 5, quindi pesa.
- Il ritiro in `pagehide` simula la regata mentre la pagina si chiude: se il browser interrompe lo script prima della fine, il salvataggio potrebbe restare a metà. Per questo scrivo prima il risultato del giocatore (ritirato) e uso la simulazione solo per i tempi degli avversari; da verificare in R2.

## Cosa serve da Ale

Il via, e due conferme (le ho già scelte io come predefinite):
1. Il ritiro conta **dal clic su «Corri la regata»**, non dal via. Va bene?
2. Avviso con conferma dal menu, nessun avviso alla chiusura della pagina. Va bene?

Versione prevista: 1.0.50 (solo `regate.js`, `gioco.js` per il menu; motore e barca non toccati).
