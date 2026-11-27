# Rivali che attraversano la barca della giuria (segnalazione di Lucio tramite Ale, 27 nov 2026)

**Causa (codice):** `js/regate.js` 1044-1062: la barca del comitato (e spillo e boe) respinge solo il giocatore (`boeToccate`, `boeUrto`); «Gli avversari non si respingono», e la guida dei rivali non la evita.

**Misura sul gioco 1.3.75** (`misura_giuria.py --conf m4 --lungo`, giro «Misura», Chromium, semi 2261-2410, 450 regate del torneo): **34 casi** (7,6% delle regate) di uno scafo di rivale (prua, centro o poppa) dentro il poligono della barca della giuria fra −60 e +40 s; tutti fra −11 e +38 s, quasi tutti prima di aver tagliato la linea; durata di solito 2-3 s (la attraversa), tre volte 11, 21 e 34 s. Controllo del metro: un rivale messo apposta sulla giuria (3 posizioni) viene visto, a 14 m no. La regata di Lucio non è in `registrazioni/` (sua ultima: 21 nov).

## Proposta (fermata 1, aspetta il via)

Modello più semplice: per i rivali la barca del comitato diventa un ostacolo fermo come per il giocatore (stessa `statoOggetto`, stessa spinta fuori, −40% di velocità al primo tocco), **senza penalità** (come oggi per le boe dei rivali). La guida non cambia. Nessuna costante nuova.

Criteri (soglie nostre, scritte prima): stessa misura, scelta 2261-2410 e conferma 2411-2560:
- G1 rivali che restano a contatto della giuria più di 10 s di fila (incastrati, come l'oss. 79 per il pilota): al massimo 2 su 450 regate;
- G2 contatti fra barche al massimo +10%; fuori linea e non arrivati al massimo +10%; arrivo mediano dei rivali al massimo +2 s;
- G3 `collaudo_partenze` (Scuola) OK; i confronti al bit dei collaudi vanno portati alla versione nuova (cambia il moto dei rivali).

Rischio: rivali incastrati contro la giuria prima del via (la guida non sa girarle attorno): G1 lo misura. Spillo e boe non sono misurati qui.

## Correzione provata (`giuria-ostacolo.patch`, via di Ale del 27 nov sera)

- Letto nel codice: fuori dalla regata dei giri la giuria non respingeva **nemmeno il giocatore** (`boeToccate` gira solo con `R.giri`): nel torneo la attraversava anche lui. La correzione vale per tutte le barche in tutte le regate (il giocatore nella regata dei giri resta con `boeToccate` e la sua penalità).
- Prima prova sul seme 2268 (regata 3): un rivale partito in anticipo tornava indietro puntando dritto sulla giuria, respinto a ogni passo, a contatto per oltre 116 s (incastrato). **Aggiunta (dichiarata, oltre la proposta):** a contatto il rivale segue il bordo della giuria dal lato più vicino alla sua prua, mai nell'angolo morto, per AGGIRA_T = 3 s (ipotesi nostra). Con l'aggiunta: a contatto 3,7 s, poi via.
- Strumento: righe TOCCA (tocchi e secondi di fila a contatto, entro 120 s), per G1.
