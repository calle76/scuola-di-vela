# Proposta: dividere `index.html` in più file (fermata 1)

16 ottobre 2026. Manutenzione: il gioco non cambia. Decisa da Claude Code su delega di Ale («c'è sempre il lavoro sul codice che decidi tu quando farlo»), **prima del laboratorio e delle correzioni della barca**. Così il laboratorio nasce nel suo file e il motore fisico sta da solo.

## 1. Perché adesso

- `index.html` pesa 244 KB, in 3.000 righe. Le prossime novità aggiungono codice: il laboratorio, circa 150-180 righe; la barca corretta, che tocca il motore; il livello 2, con regole e avversari.
- Con il motore in un file suo, i collaudi della fisica lo leggono direttamente, invece di ritagliarlo da `index.html` con due «segnaposto» di testo (`tests/fisica/motore.js`).
- La garanzia c'è già: `tests/collaudo_impronta.py`.

## 2. Come

- **Il gioco diventa una cartella:** `index.html` (stile e struttura della pagina, circa 28 KB) più una cartella `js/` con i file del codice. Si apre ancora con un **doppio clic** su `index.html`: i file si caricano come script classici (`<script src="js/…">`), che il browser accetta anche da disco. **Niente moduli** (`import`/`export`): da disco il browser li blocca, e richiederebbero di riscrivere i collegamenti fra le parti.
- **Il codice si sposta, non si riscrive.** Oggi tutto sta dentro un blocco unico, `(() => { … })();`. Il blocco si toglie, e le variabili restano condivise fra i file come oggi lo sono dentro il blocco. Ogni file è un taglio del codice attuale lungo le intestazioni della mappa, con le righe nello stesso ordine.
- **Nomi:** 292 nomi diventano globali. Controllato: nessuno coincide con un nome che il browser usa già (prova su una pagina vuota di Chromium).

| File | Cosa contiene (sezioni di oggi) | KB circa |
| --- | --- | --- |
| `js/motore.js` | Motore fisico: `BOAT`, `CL`, `CD`, `step()` (puro, senza pagina) | 6 |
| `js/base.js` | Strumenti comuni subito dopo il motore: `$`, `KN`, `canvas`, `clamp`, nomi delle andature | 1 |
| `js/contenuti.js` | Lezioni, prove, ripassi, esame, glossario | 53 |
| `js/gioco.js` | Stato, raffiche, menu e progressi, quiz, modalità, comandi, simulazione, pannello | 56 |
| `js/regate.js` | Fantasma e regate (avversari, partenza, contatti, classifica) | 34 |
| `js/disegno.js` | Disegno del mare, della barca e degli strumenti | 38 |
| `js/registratore.js` | Registratore di sessione | 14 |
| `js/avvio.js` | Ciclo e aggancio dei collaudi (`#collaudo`) | 4 |

La mappa del file in `CLAUDE.md` diventa: «un file per parte; dentro, le intestazioni `// ----`».

## 3. Il rischio vero: l'ordine di caricamento

Oggi il blocco unico prepara tutte le funzioni prima di eseguire qualunque riga. Con file separati, una riga eseguita **al caricamento** di un file non vede le funzioni dei file che vengono dopo. Le righe dentro le funzioni non hanno il problema, perché girano più tardi. L'ordine della tabella è quello di oggi nel file, quindi i casi dovrebbero essere pochi. Ognuno si trova perché la pagina dà un errore al caricamento, che il collaudo dell'impronta conta («errori della pagina»). Se un caso c'è, si sposta quella riga in `avvio.js`, e lo si scrive nel rapporto.

## 4. I collaudi da adattare

- `tests/fisica/motore.js`: legge `js/motore.js` invece di ritagliare `index.html`.
- `tests/collaudo_versione.py`: cerca `VERSIONE` in `js/` invece che in `index.html`.
- **Copie modificate della pagina**, cioè l'impronta, le contro-prove del pilota e `--pagina`: oggi copiano solo `index.html`. Dopo la divisione la copia deve portarsi dietro anche `js/`, quindi si copia la cartella. Un aiuto comune in `tests/`, poche righe.
- `collaudo_carriera.py` (K5) confronta con la 1.0.1 presa da git: resta valido, perché la 1.0.1 era un file unico.
- `lancia_tutti.sh` e gli altri collaudi aprono `index.html` per indirizzo: non cambiano.

## 5. Criteri (attese nostre, scritte prima)

1. **Impronta identica al bit** a quella di oggi: 63 scene su 63, testi, stato delle barche, immagini. Riferimento preso dalla 1.0.2 com'è adesso.
2. `polare.js` e `raffiche_e_virate.js` identici carattere per carattere.
3. **Nessun errore della pagina**, né con `#collaudo` né senza.
4. Il pilota delle lezioni, versione veloce, uguale a prima: stessi casi «da guardare».
5. **Doppio clic:** la pagina si apre da disco senza server (prova del collaudo della versione, pagina senza `#collaudo`).
6. **Controllo che il metro misuri:** l'impronta è già stata contro-provata il 16 ottobre. In più, una contro-prova sull'ordine: caricare due file scambiati deve dare errori della pagina, cioè l'impronta se ne accorge.

## 6. Cosa cambia per Ale

- **Per giocare:** niente. Si apre `index.html` come sempre. Online, su GitHub Pages, funziona uguale.
- **Per distribuire il gioco** serve la cartella intera, `index.html` più `js/`, non più il solo file. Il principio «un unico file HTML» di `PROGETTO.md` e `CLAUDE.md` si riscrive: un'unica pagina, senza nulla da installare.
- **Conoscenze del progetto su claude.ai:** al posto del solo `index.html` vanno caricati i file di `js/`. Si possono caricare solo quelli che servono: per una revisione della fisica, solo `motore.js`.
- **Una conseguenza minore:** senza il blocco unico, le variabili del gioco si vedono dalla console del browser. Per un gioco personale va bene: chi apre la console può già leggere tutto il codice.

## 7. Versione

Cambia la struttura, non il gioco: **1.0.3**, con la voce nel `CHANGELOG`. Il collaudo della versione la cerca nel file nuovo.

## 8. Esito (16 ottobre 2026, 1.0.3)

Fatto come proposto, con uno scostamento: il pannello sta in `disegno.js` e non in `gioco.js`, perché così l'ordine del codice resta quello di prima. Criteri:
1. **Impronta identica al bit**, 63 scene su 63. Superato.
2. **`polare.js` e `raffiche_e_virate.js` identici**; nel prototipo del fiocco, 30 casi senza fiocco con scarto zero. Superato.
3. **Nessun errore della pagina**, con e senza `#collaudo`. Superato.
4. **Pilota veloce identico** riga per riga. Superato.
5. **Doppio clic:** `collaudo_versione.py` apre la pagina senza `#collaudo` e la trova. Superato.
6. **Contro-prova dell'ordine:** scambiare `contenuti.js` e `gioco.js` non cambia niente, perché al caricamento nessuno dei due usa l'altro, e lo scambio era innocuo. `avvio.js` prima di `regate.js` invece rompe la pagina, e l'impronta lo dice: «NON VALIDO», uscita 2. Superato, dopo aver reso l'impronta capace di dirlo invece di interrompersi.

Collaudi lanciati qui:
- **OK:** versione, carriera (57 controlli), carriera intera, pulsanti, registratore (87 controlli).
- **NON VALIDI solo per i caratteri mancanti, il resto OK:** esame, quiz, libretto, esame in carriera.
