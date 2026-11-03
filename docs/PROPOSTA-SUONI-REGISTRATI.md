# Proposta: la vela e l'acqua con suoni registrati

3 novembre 2026. **Fermata 1: documento, pagina d'ascolto e misure; nessun codice nel gioco.** Segue `PROPOSTA-SUONI.md` (1.2.5).

## 1. Da dove si parte

Ale, 3 novembre, dopo aver giocato la 1.2.5: «il mare è un fruscio piatto, ma soprattutto la vela quando sbatte è un ticchettio irreale. si possono cercare registrazioni migliori».

Oggi i due suoni sono rumore generato dal browser e filtrato (`js/suoni.js`):
- l'**acqua** è un rumore con un filtro che si apre con la velocità: è sempre uguale, quindi suona piatto;
- la **vela** è un rumore acuto acceso e spento a ritmo regolare: non ha l'attacco secco della tela che schiocca, e suona come un ticchettio.

Questa proposta cambia **solo questi due suoni**. Il vento, le manovre, la tromba e gli altri suoni brevi restano come sono. Cambia invece una decisione della 1.2.5, «suoni generati dal browser, senza file» (`DECISIONI.md`, costo basso): qui entrano due registrazioni.

## 2. Le registrazioni trovate

Cercate su **Freesound** (freesound.org), l'archivio più grande di suoni con licenze Creative Commons. Ogni suono ha la sua licenza, scritta nella sua pagina. Ho tenuto solo **CC0** (si usa senza condizioni) e **CC BY** (si cita l'autore). Ho scartato le **CC BY-NC**: «non commerciale» non è una licenza libera, quindi è fuori dal principio 5. Ho scartato anche i siti a pagamento e i suoni fatti con l'intelligenza artificiale.

Ho letto 15 candidati: durata, livello, quanto pesano gravi e acuti, colpi al secondo e spettrogramma. Non posso ascoltarli: la scelta finale è tua, con la pagina d'ascolto (§5).

**Proposti (tutti CC0):**

| Uso | Freesound | Cosa c'è | Perché |
|---|---|---|---|
| Vela | [377492](https://freesound.org/people/13FPanska_Mokrolusky_Tomas/sounds/377492/), «Sailing boat - sail», 8,5 s | 16 colpi di tela: 9 forti (da 37 a 61 dB sopra il fondo) e 7 deboli (da 12 a 26 dB), su un fondo quasi silenzioso | Nello spettrogramma i colpi sono netti e separati: si possono ritagliare uno per uno |
| Acqua | [852108](https://freesound.org/people/myLoop/sounds/852108/), «Sailboat Bow», 75 s | Acqua tagliata dalla prua di una barca a vela sull'Ammersee, vento costante, lago calmo | La tessitura più ricca e regolare fra le sei acque misurate (sbalzi di 4,5 dB da un secondo all'altro); rombo del vento sul microfono sotto i 120 Hz, che si toglie con un filtro |

**Scartati, con il motivo:**
- 554439 (vela vera, CC0): nello spettrogramma ha una banda continua di insetti sugli acuti, e i colpi sono meno netti;
- 645974 (vela vera a vento leggero, CC BY): buona, ma i colpi arrivano a gruppi lunghi mescolati al resto; tenuta come riserva, si dovrebbe citare l'autore;
- 448975, 138981, 870601, 690002: teli, tappeti e bandiere, non vele; quasi solo suoni gravi (il tappeto ha gli acuti 38 dB sotto il totale) o colpi poco distinti;
- 438838 (onda di prua, CC0) e 435668 (onde contro la prua nell'oceano, CC BY): buone, ma a ritmo d'onda fisso, che si sentirebbe ripetuto; 435668 è mare aperto con spruzzi, più di quanto fa una deriva su acqua calma;
- 512129, 371172, 760338, 667414: registrati in pozzetto o in cabina di barche grandi, sotto i 300 Hz per quasi tutta l'energia.

**Una cosa da dichiarare:** nessuna delle registrazioni è di una deriva. 377492 dice solo «barca a vela, vela»; 852108 è una barca a vela con cabina, su un lago. Per il suono della tela e dell'acqua a pochi nodi la differenza non dovrebbe sentirsi, ma è una semplificazione.

## 3. Il modello più semplice

**Un file nuovo, `js/suoni-dati.js`**, caricato prima di `suoni.js`, con i suoni scritti come testo (base64), in formato Ogg Opus mono a 48 kbit/s:
- un **giro d'acqua** di 20 s, preso da 852108, con il rombo sotto i 120 Hz tolto e la fine raccordata con l'inizio, così non si sente lo stacco;
- i **16 colpi di vela** di 377492, ritagliati da 0,04 s prima a 0,46 s dopo il picco, con il fondo sotto i 150 Hz tolto.

**Perché dentro un file `.js` e non come file audio:** il gioco si apre anche con un doppio clic su `index.html`. Così il browser vieta di leggere altri file dalla cartella, mentre i file `.js` li carica. **Provato oggi:** un pezzo di 3 s scritto così in un `.js`, aperto da file locale, si decodifica in Chromium e in Firefox, sia in Opus sia in MP3. In Opus a 48 kbit/s pesa 17,6 KB, cioè circa 6 KB al secondo.

**Peso stimato:** acqua circa 120 KB, colpi circa 50 KB; in base64 un terzo in più, **circa 230 KB**, contro 468 KB di tutto `js/` oggi.

**Da dove si prendono:** dalle anteprime pubbliche di Freesound (MP3 di qualità alta: 192 kbit/s per 377492, 151 per 852108), che si scaricano senza account. Gli originali richiedono un account gratuito e sarebbero un po' più puliti, ma alla fine il suono si riduce comunque a 48 kbit/s. La licenza è la stessa.

**Come suonano nel gioco** (`js/suoni.js`; le curve sono **ipotesi nostre**, fatte a orecchio):
- **Acqua:** il giro gira in continuazione, a un volume che cresce con la velocità come oggi (0,04 + 0,4 × min(1, velocità/3)). Con la barca veloce l'acqua gira un po' più in fretta (da 0,85 a 1,12 volte) e il filtro lascia passare più acuti (da 1.200 a 6.000 Hz). A barca scuffiata resta al minimo, come oggi.
- **Vela:** quando la vela fileggia (la stessa condizione di oggi: angolo morto o troppo lascata), il gioco fa partire **colpi veri**, scelti a caso fra i 16:
  - 7 volte su 10 un colpo forte, altrimenti uno debole;
  - ogni colpo con altezza diversa di ±5% e volume da −4 a +2 dB, perché non si riconosca la ripetizione;
  - **colpi al secondo = 1 + 0,35 × vento apparente in nodi**: 2,4 a 4 nodi, 4,5 a 10, 6,3 a 15 (ipotesi nostra);
  - intervallo fra un colpo e l'altro a caso, fra 0,6 e 1,4 volte quello medio;
  - volume come oggi (0,28 × min(1, vento apparente/8)).
- **Il caso** viene dal generatore dei suoni (`sRand`), non da `Math.random`: la simulazione non se ne accorge.
- **Fruscio del boma spinto (Z):** resta quello di oggi.
- **Prima che i file siano decodificati, o se la decodifica fallisce:** restano i suoni sintetici di oggi. La decodifica parte al primo tasto, insieme all'audio.

## 4. Criteri (soglie scritte prima, attese nostre)

- **R1, la simulazione non cambia:** arrivi e barca identici al bit con i suoni accesi e spenti (come S1); `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.
- **R2, i suoni seguono i numeri** (registro interno, come S3):
  - volume e velocità del giro d'acqua crescono sempre con la velocità della barca, su letture da 0 a 6 nodi;
  - i colpi di vela in 60 s crescono sempre col vento apparente, a 4, 8, 12 e 16 nodi, e restano entro il 20% dei valori del §3;
  - **controprova:** con la vela regolata, 0 colpi in 60 s; a barca scuffiata, 0 colpi.
- **R3, funziona da file locale e dal sito:** Chromium e Firefox, pagina aperta con e senza `#collaudo`. Il registro dice «registrati» (decodifica riuscita), nessun errore. Con la decodifica fatta fallire apposta tornano i suoni sintetici, senza errori.
- **R4, costo:**
  - lettura dei suoni per fotogramma al massimo +10%, come S4;
  - decodifica al primo tasto al massimo 300 ms;
  - `js/suoni-dati.js` al massimo 300 KB.
- **R5, licenze:** i due file in `FONTI-PUBBLICHE.md` (F42, F43), con autore, pagina, licenza CC0, giorno dello scaricamento e cosa è stato tagliato. Nessun file CC BY-NC.
- **R6:** i collaudi dei suoni (`collaudo_suoni.py`, S1-S6) restano verdi.
- **Ascolto:** se la vela e l'acqua suonano vere lo giudichi solo tu, giocando. Le fonti non possono dirlo.

## 5. La pagina d'ascolto

`sperimentale/suoni-registrati/ascolto.html`: aprila con un doppio clic. Ci sono:
- le **prove** costruite col modello del §3: la vela a 1,5, 3 e 5 colpi al secondo; l'acqua lenta e veloce; acqua e vela insieme;
- **sei originali** (8-15 s ciascuno), compresi gli scartati più vicini, per confrontare.

Tutto è portato allo stesso volume percepito, solo per confrontare alla pari: nel gioco sarebbe più basso, sotto il vento. Le prove sono fatte fuori dal gioco, con `ffmpeg` e un piccolo script. **Verificato:** i 12 suoni si caricano in Chromium e Firefox, e la pagina sta larga 390 px senza scorrere di lato.

La cartella, cioè la pagina e i suoi file audio (1,4 MB), **non va nel repository**: serve solo per questa scelta e resta sul tuo computer.

## 6. Rischi

- **Ripetizione:** 16 colpi possono riconoscersi dopo qualche minuto. Il caso nell'altezza, nel volume e nel ritmo serve a questo. Se non basta, si aggiungono colpi da 645974 (CC BY, con l'autore citato).
- **Lo stacco del giro d'acqua:** se si sente, si allunga il giro a 30 s (circa 60 KB in più).
- **Un suono vero ma fuori posto:** un colpo da barca grande su una deriva piccola. Se suona troppo pesante, si alza l'altezza dei colpi.
- **Il peso della pagina:** circa 230 KB in più da scaricare dal sito. È meno della metà di `js/` di oggi.
- **Collaudi su GitHub:** i computer di GitHub non hanno casse. Come oggi, i collaudi leggono il registro interno, non il suono che esce.

## 7. Da decidere (Ale)

1. **Ascoltando la pagina: la vela (prove 1-3) e l'acqua (prove 4-5) ti sembrano giuste per il gioco?** Puoi rispondere «sì», «sì ma…» (per esempio più o meno colpi, acqua più forte), oppure «no, prova con…» uno degli originali. Se mi dai il via, procedo con la fermata 2.
