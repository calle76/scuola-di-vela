# Proposta: le bandiere del via con il conto da 3 minuti come con quello da 5 (voce 67)

*Fermata 1, 20 novembre 2026. Richiesta di Ale: «le bandiere del via che funzionino tutte e tre nei 3 minuti come nei 5». Nessun codice finché non arriva il via. **Prima va chiarito cosa non funziona**: dal codice non lo vedo (sotto). Collegata a `PROPOSTA-SEGNALI-PARTENZA.md` e `PROPOSTA-RIQUADRO-BANDIERE.md`.*

## Cosa fa il codice oggi (letto, non ancora provato guidando)

Il conto alla rovescia si sceglie fra 1, 3 e 5 minuti (`#cdSel`, di partenza 3). Le bandiere (`bandiereAl`, `js/regate.js`):

| Conto | Classe | P (preparatorio) | Blu (dopo il via) | X (richiamo) |
| --- | --- | --- | --- | --- |
| 5 min | alzata a −300 s, giù al via | alzata a −240 s, giù a −60 s (3 min) | dallo sparo | allo sparo se una barca è oltre la linea |
| 3 min | alzata a −180 s | alzata a −120 s, giù a −60 s (1 min) | come sopra | come sopra |
| 1 min | alzata a −60 s | mai | come sopra | come sopra |

La sequenza da 3 minuti è una scelta nostra (ipotesi dichiarata), non del regolamento, che descrive solo i 5 minuti. **Le bandiere compaiono solo nelle regate con `R.segnali`**, cioè oggi solo la «Regata con i giri di penalità» della Scuola. Nelle regate di Deriva (torneo, stagione, finale) **non ci sono bandiere**: ci sono i messaggi di testo. Con 3 minuti anche la P c'è, per 60 s invece di 180.

## Le possibili letture della richiesta

Non so a quale si riferisce Ale. Le elenco in ordine di probabilità (mia stima, non misurata):

1. **«Tutte e tre» = classe, P e X.** Nel conto da 5 minuti si vedono tutte e tre bene; nel conto da 3 la P resta alzata solo 60 s (nei 5 minuti 180 s) e può passare inosservata, e la X compare solo se c'è una barca oltre la linea. Se è questo, il difetto è la **durata della P nei 3 minuti**.
2. **Le bandiere non compaiono nelle regate di Deriva** (dove il conto è di 3 minuti): se Ale le vuole lì, è un lavoro più grosso (riquadro e giuria anche nel torneo, `R.segnali`).
3. **Il riquadro delle bandiere** (le bandiere in grande, in alto a sinistra) lascia visibile ogni cambio solo `RQ_PERM = 10` s: forse nei 3 minuti, con cambi più ravvicinati, una sostituisce l'altra.
4. **Un difetto vero** (una bandiera non appare o non scompare in un caso), che si vede solo guidando. Il collaudo `collaudo_segnali.py` oggi controlla la sequenza da 5 e da 3? **Da verificare**; non l'ho aperto.

## Domande ad Ale (una per volta, quando ha un momento)

1. Quale bandiera non vedi, e in quale regata (Scuola con i giri? torneo?)?
2. Con 3 minuti oggi la P sale a −2 minuti e scende a −1 minuto. Ti aspetti che resti alzata più a lungo, oppure una sequenza diversa?

## Il modello più semplice (se la lettura 1 è quella giusta)

Cambiare solo **quando sale la P** nei 3 minuti: **P a −150 s** (invece di −120) e giù a −60 s: P alzata per 90 s. Ipotesi nostra, da una proporzione (3/5 di 180 s = 108 s). Le bandiere nei 5 e nell'1 minuto non cambiano. Nessun file nuovo, nessuna costante nuova oltre al −150.

## Criteri (soglie nostre, dichiarate prima, da confermare dopo la risposta di Ale)

| # | Criterio | Soglia |
| --- | --- | --- |
| B1 | Sequenza 5 min invariata | classe −300 → 0, P −240 → −60, blu dopo lo sparo: 0 differenze su 12 prove (come oggi) |
| B2 | Sequenza 3 min nuova | classe −180 → 0, P −150 → −60, blu dopo lo sparo; confronto fra la sequenza letta dal collaudo (calcolata a parte, non da `bandiereAl`) e quella del gioco: 0 differenze su 20 prove |
| B3 | La X | in 20 prove con una barca oltre la linea allo sparo, la X sale in tutti e 3 i conti, per ogni barca oltre la linea; nelle 20 senza, non sale |
| B4 | I messaggi seguono le bandiere | per ogni cambio di bandiera c'è un messaggio entro 1 s (come oggi) in tutti e 3 i conti |
| B5 | Riquadro | pannello 1360x650 con 0 px di eccesso; `collaudo_riquadro_bandiere.py` invariato |
| B6 | Come un giocatore | pagina senza `#collaudo`, conto da 3 e da 5 minuti giocati davvero: le bandiere compaiono in tutti e 3 i momenti, 0 errori |

Il metro di B2 e B3 non deve dipendere dal gioco: le sequenze attese si scrivono nel collaudo, e il collaudo dice quante prove ha contato (almeno 20).

## Rischi

- **Interpretazione sbagliata:** senza la risposta di Ale potrei sistemare una cosa che non era il problema. Per questo la proposta si ferma qui.
- **Cambio della sequenza da 3 minuti:** non c'è una fonte per i 3 minuti; la regola di riferimento (F15 26) descrive i 5. Resta un'ipotesi dichiarata (principio 4).
- **Regate di Deriva senza bandiere (lettura 2):** è un lavoro separato e va proposto a parte.

## Passi, dopo la risposta di Ale e il via

1. Guardare guidando le tre sequenze (1, 3, 5 minuti) e confermare dov'è il difetto; riportare cosa si vede.
2. Cambiare solo ciò che serve; criteri B1-B6.
3. Documenti, versione, `CHANGELOG.md`.
