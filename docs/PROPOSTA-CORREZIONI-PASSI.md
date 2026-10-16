# Proposte: correzioni dei passi delle lezioni

Una sezione per passo, nell'ordine in cui si fanno. Elenco dei passi da correggere: `PROPOSTA-PILOTA-LEZIONI.md` §10, più il passo 1.8 rotto dalla 1.0.11.

## 1. Passo 1.8 «Orzare e l'angolo morto» (fermata 1, 16 ottobre 2026)

### Il difetto

Il testo dice: «tieni premuto → … Continua finché la barca non si ferma quasi del tutto, poi rilascia». Dalla 1.0.11 la vela porta fino a 29° di vento apparente, la barca arriva al vento più veloce e, con la barra tenuta, **attraversa il vento e vira** invece di fermarsi. Il pilota che fa quello che dice il testo completa il passo **0 volte su 80** (prima 74 su 80). Ale, orzando a piccoli colpi, l'ha completato in 10 s fermandosi con la prua a 11-19° dal vento.

È il comportamento giusto della barca: con l'abbrivio e la barra tenuta, la prua passa il vento (lo dice anche la lezione 3: «la barca lo supera grazie all'abbrivio»). Sbagliato è il testo.

### Proposta: cambia solo il testo

Condizione del passo invariata (`twa < 40` e meno di 1,5 nodi per 0,5 s). Motore invariato. Testo nuovo:

> Ora premi **→**: la prua gira a dritta, verso il vento. Si dice *orzare*. Quando la prua è quasi nel vento (la lancetta della rosa entra nel rosso), rilascia: la vela sbatte, non spinge più e la barca rallenta fino a fermarsi.

La parte fra parentesi serve a chi ha la rosa accesa (lo è di norma); chi l'ha spenta ha comunque «quasi nel vento».

**Da decidere (Ale):** aggiungere anche una frase per chi tiene troppo: «Se tieni premuto troppo a lungo, la prua attraversa il vento e la barca vira: premi *Ricomincia*.» Costa una riga nel pannello.

### Misura già fatta (pilota modificato, gioco non toccato)

Copia del pilota con una sola riga cambiata: invece di tenere finché la barca è sotto 1 nodo, rilascia quando legge la prua sotto 40° dal vento (lettura con errore ±5°, come sempre). Poi mani ferme fino al tempo limite (60 s).

| Semi | Giocatore preciso | Giocatore impreciso (tiene da 0,3 a 1,5 s in più) |
| --- | --- | --- |
| 1-20 | **20 su 20**, mediana 7,0 s | 12 su 20 |
| 21-100 | **80 su 80**, mediana 7,1 s | 45 su 80 |

Quando l'impreciso fallisce, la barca ha virato: finisce dall'altra parte a 32-57° dal vento, ancora in moto (per esempio 3,1 nodi). Il passo dopo, «Ripartire», si completa guidando 99 su 100 e non si completa mai da solo (0 su 100, anche dopo un colpo lungo).

**Attenzione:** questi numeri li ho già visti su entrambi i gruppi di semi. Per la regola dei semi la conferma della fermata 2 va fatta su un gruppo nuovo, i semi 101-200.

### Criteri per la fermata 2 (soglie nostre, scritte ora)

1. Pilota aggiornato al testo nuovo («rilascia quando la prua entra nel rosso»), semi 101-200: preciso completa **almeno 97 su 100**; a mani ferme 0 su 100.
2. Impreciso: si riporta il numero, **senza soglia**. Tenere troppo e virare è realistico; il passo non deve impedirlo.
3. «Ripartire» non si completa da solo più di 2 volte su 100.
4. Pannello a 1360×650: eccesso **0 px** sul passo 1.8 (`collaudo_pannello.py`), con e senza la frase facoltativa.
5. `collaudo_registro.py`, parte lezioni: torna 15 su 15. Oggi tiene → finché il passo si completa, quindi con la barca che vira fallisce; va cambiato anche lui per rilasciare nel rosso (cambio del collaudo dichiarato).
6. Non-regressione: `polare.js` e `raffiche_e_virate.js` identici carattere per carattere (il motore non cambia).
7. Prova senza `#collaudo`: una pagina da giocatore, tastiera vera, passo 1.8 completato rilasciando nel rosso, 3 tentativi su 3.

### Costanti nuove

Nessuna.

### Fonti

Nessuna affermazione nautica nuova: «la vela sbatte, non spinge e la barca si ferma» c'è già (`CONTENUTI-DA-VERIFICARE.md`, riga 4 della L1); «con l'abbrivio la prua attraversa il vento» c'è già nella lezione 3.

### Rischi

- Il giocatore impreciso vira 4 volte su 10. Se ad Ale sembra troppo frustrante, la frase facoltativa aiuta; una barra che torna al centro più in fretta, invece, sarebbe un cambio del gioco e qui non lo propongo.
- Versione del gioco: cambia un testo, quindi nuova versione 1.0.12 (`VERSIONE` e `CHANGELOG.md`).

### Esito (fermata 2, 16 ottobre 2026): fatto nella 1.0.12

Ale ha scelto il testo **con** la frase facoltativa, l'ha provato giocando («funziona») e ha deciso di non fare la conferma sui semi 101-200: i criteri 1, 3, 5 e 7 **non sono stati misurati**. Misurati: pannello eccesso 0 px (32 passi, criterio 4) e non-regressione identica (criterio 6). Pilota e `collaudo_registro.py` aggiornati al testo nuovo, da verificare nel prossimo giro completo.
