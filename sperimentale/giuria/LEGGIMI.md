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

## Esito della prima versione (ostacolo per tutti): non adottata

Gioco → prova, scelta 2261-2410 / conferma 2411-2560 (450 regate ciascuno): rivali incastrati più di 10 s 0 / 1 (22 s; G1 sì); contatti 579 → 573 / 496 → 495; fuori linea 239 → 235 / 200 → 199; non arrivati 517 → 512 / 465 → 474; arrivo mediano 587,1 → 585,6 / 587,9 → 587,5 s; coppie dopo il via 35 → 36 / 28 → 26 (G2 sì). **Ma il pilota dei collaudi (la barca «Tu») resta incastrato contro la giuria 110, 115 e 26 s** sulla conferma: non sa girarle attorno, e i collaudi col pilota rischiano di bloccarsi (come l'oss. 79). Le righe «dentro la giuria» con la prova (23 e 20, quasi tutte sotto 1,5 s) sono in parte del metro: lo strumento orienta la giuria col vento locale, il gioco col vento generale.

## Seconda versione (`giuria-ostacolo-rivali.patch`): solo i rivali, come nella proposta

Il giocatore resta com'era. Limite noto, dichiarato: fuori dalla regata dei giri la sua barca attraversa ancora la giuria. Criteri invariati.

**Regata di Lucio del 26 nov 22:07** (`registrazioni/regata-20261126-2207-intera.txt`, allenamento triangolo, 1.3.62): la Verde (Davide Lunardi) sta sopra la giuria da −52 a −31 s, a 0,6 nodi (giuria ricostruita a x −35, y 0 dal vento di 180° e dalla linea di 70 m). Le altre barche non la toccano.

## Terza versione (`giuria-ostacolo-v3.patch`): ostacolo per tutti, e anche il pilota la aggira (Ale: «il pilota è una cosa, io o un altro giocatore siamo un'altra»)

La seconda (solo rivali) è stata fermata prima della fine. Ora la giuria respinge tutte le barche in tutte le regate (il giocatore nella regata dei giri resta con `boeToccate` e la sua penalità); chi è guidato da `aiControl` (rivali e pilota dei collaudi) a contatto segue il bordo per AGGIRA_T = 3 s. Sui semi in cui il pilota restava incastrato (PC, Chromium): 2416 da 110,2 a 3,7 s, 2425 da 26,5 a 8,5 s, 2480 da 114,8 a 2,7 s. Seme 2435: Elena Zanin resta 22 s accanto alla giuria fra 62 e 80 s, quasi ferma a 27-44° dal vento (piantata mentre prova a partire), poi riparte da sola. Criteri invariati; G1 ora conta anche il pilota.

## Spillo e boe (27 nov sera, dopo la 1.3.76; via di Ale)

**Misura sulla 1.3.76** (`misura_boe.py`, semi 2261-2410, 450 regate): un rivale passa attraverso lo spillo 95 volte in 75 regate, attraverso le boe 29 volte in 28 regate (boa di bolina, 4-6 minuti dopo il via); durata mediana 1,5 s, massimo 10 s. Partenze anticipate: 235 rivali su 1350 oltre la linea allo sparo, tutti rientrati (0 OCS in classifica; nelle regate vere 2-2,6% nei campionati, F147): solo annotato.

**Correzione (`boe-ostacolo.patch`):** `giuriaOstacolo` vale per spillo, comitato e boe (stesso modo: spinta, −40%, nessuna penalità, il giocatore nella regata dei giri resta con `boeToccate`; chi è guidato da `aiControl` segue il bordo per 3 s). Criteri scritti prima, come per la giuria: passaggi attraverso spillo e boe 0; a contatto con un oggetto più di 10 s di fila (rivali e pilota) al massimo 2 su 450 regate; contatti, fuori linea e non arrivati al massimo +10%; arrivo mediano e bolina degli esperti al massimo +2 s; coppie dopo il via al massimo +20%. Scelta 2261-2410, conferma 2411-2560.
