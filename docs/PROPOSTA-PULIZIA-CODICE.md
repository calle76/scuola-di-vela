# Proposta: pulizia del codice, resta solo la barca dell'1b

1 novembre 2026. **Fermata 1: solo documento, nessun codice toccato.** È il passo 2 dell'ordine di `PROPOSTA-RIORGANIZZAZIONE.md` §5: si fa prima delle lezioni della scuola, così le lezioni si scrivono una volta sola sulla struttura nuova. Il criterio era già scritto lì (M4). Qui c'è cosa si tocca, cosa si misura e cosa resta per i passi dopo.

## 1. Cosa c'è oggi (contato)

Nel gioco convivono due barche. La **1a** non ha `S.lv`; la **1b** ha `S.lv = 2`. La 1a è la barca di:
- lezioni e prove;
- navigazione libera, se nelle impostazioni c'è «Barca: 1a»;
- «Regata a bastone» e «Regata nelle raffiche»;
- carriera, meriti e record, che contano solo queste due regate (`RACES1`).

La 1b invece è la barca di: «Regata nei salti di vento», «Regata con i giri di penalità», torneo, e navigazione libera con «Barca: 1b».

Dove il codice distingue le due barche (grep su `S.lv`, `lv2`, `RACES1`, `boatLv`):

| File | Punti | Cosa fanno |
|---|---|---|
| `js/motore.js` | 7 | timone che stalla, raddrizzata, spingi il boma, scarroccio |
| `js/gioco.js` | 11 | selettore «Barca», tasto Z, barra fino a 35°/45°, raddrizzata, carriera e meriti (`RACES1`) |
| `js/regate.js` | circa 25 | regole 10-13 o solo la 10, contatto fra scafi o fra cerchi, guida degli avversari (`cedeAvv1b` o il ramo della 1a), semaforo, virate |
| `js/disegno.js` | 1 | angolo della barra nel disegno |
| `js/registratore.js` | 2 | scrive «barca 1a/1b» nel file |
| `index.html` | 1 | il selettore `boatLv` |
| `tests/fisica/` | 4 script | `scarroccio1b.js`, `timone2.js` e `boma2.js` mettono a confronto le due barche; `polare.js` e `raffiche_e_virate.js` misurano la 1a |
| `sperimentale/misure_fiocco.js` | 1 | confronta il prototipo del fiocco con il motore del gioco, cioè con la 1a |

## 2. Cosa propongo

**A. Motore (`js/motore.js`).** Quello che oggi vale con `S.lv === 2` diventa l'unico comportamento. Si tolgono:
- il timone della 1a;
- la raddrizzata della 1a (3 s);
- lo scarroccio della 1a (`BOAT.foilK`).

Le costanti (`RUD2`, `RADD2`, `BOMA2`, `DERIVA2`, `SALTI2`) cambiano nome e perdono il «2», in un commit a parte. È un cambio meccanico e l'impronta deve uscire identica. `S.lv` non esiste più.

**B. Gioco (`js/gioco.js`, `js/disegno.js`, `index.html`).**
- Lezioni, prove e navigazione libera passano alla 1b.
- Il selettore «Barca» sparisce.
- In navigazione libera i salti di vento restano come li ha oggi la 1b.
- I testi non cambiano, salvo togliere «Barca dell'1b» dove non c'è più una scelta.

**C. Regate (`js/regate.js`).** «Regata a bastone» e «Regata nelle raffiche» non si buttano: diventano regate della 1b, quindi con regole 10-13, contatto vero, avversari che cedono con `cedeAvv1b` e semaforo. Così la scuola ha subito le sue «2 regate senza torneo» (`PROPOSTA-RIORGANIZZAZIONE.md` §3). Si tolgono il ramo degli avversari della 1a e il contatto fra cerchi. Per ora carriera e meriti continuano a contare quelle due regate, agli stessi indici: menu e carriera si rifanno al passo 5. Record, medaglie e meriti si azzerano, senza chiedere, come già deciso.

**D. Registratore.** Nel file non scrive più «barca 1a/1b». Restano le altre righe dell'intestazione.

**E. Collaudi della fisica e prototipo.**
- Una **copia congelata del motore della 1a**, `tests/fisica/motore1a.js`, presa da `js/motore.js` di oggi e mai più toccata. Il prototipo del fiocco (`misure_fiocco.js`) si confronta con questa, così la sua regola «per una vela sola identico al gioco» resta vera: diventa «identico alla 1a della 1.0.78».
- `polare.js` e `raffiche_e_virate.js` continuano a misurare il motore del gioco, quindi la 1b, con un **riferimento nuovo dichiarato** (M4 della riorganizzazione).
- Gli script che confrontano 1a e 1b leggono la 1a dalla copia congelata.
- `CLAUDE.md` va riscritto nella frase sulla non-regressione.

**Cosa NON fa la pulizia:**
- non cambia i testi delle lezioni (passo 3);
- non ritocca i tempi delle medaglie (passo 4);
- non tocca menu, carriera e attestato (passo 5);
- non tocca il prototipo, a parte la riga che sceglie con che cosa confrontarsi.

## 3. La conseguenza vera: lezioni e prove cambiano barca

Questa è l'unica parte che il giocatore sente. I 32 passi delle lezioni e i tempi delle 5 prove sono stati provati con la 1a. Sulla 1b:
- la barra arriva a 35° (45° con Maiusc);
- il timone stalla;
- la raddrizzata è più lenta;
- dall'angolo morto non si esce da soli: serve Z (decisione del 16 ottobre).

Alcuni passi potrebbero non completarsi più, e alcune medaglie potrebbero diventare impossibili o troppo facili. Non lo so: **non è mai stato misurato** (la misura M1 della riorganizzazione non è stata fatta).

Per questo propongo una **misura 0, prima di toccare il codice**. Su una copia della pagina, con la barca dell'1b forzata e il gioco così com'è, si lanciano:
- il pilota delle lezioni (`collaudo_pilota_lezioni.py`, `collaudo_lezioni.py`);
- le prove (`collaudo_fasce.py`).

Il risultato è quanti passi su 32 completa il pilota e con quanti semi, più i tempi delle prove rispetto alle medaglie di oggi. Non cambia niente nel gioco. Serve per sapere prima quanto lavoro si sposta al passo 3, e per decidere la domanda del §6.

## 4. Criteri (soglie scritte prima, attese nostre)

- **P1, la barca dell'1b non cambia:** `tests/fisica/impronta1b.js` è identica carattere per carattere prima e dopo, e anche dopo il cambio dei nomi.
- **P2, la copia della 1a è fedele:** `polare.js` e `raffiche_e_virate.js` lanciati su `motore1a.js` danno le uscite di oggi (`polare.txt`, `raffiche_e_virate.txt`), carattere per carattere. Il prototipo del fiocco dà le stesse misure di oggi (`misure_tappaC.txt`).
- **P3, il riferimento nuovo è dichiarato:** le uscite nuove di `polare.js` e `raffiche_e_virate.js` si riportano nel CHANGELOG. Si controlla che i valori della 1b nei 30 casi siano quelli che `scarroccio1b.js` e `impronta1b.js` già davano per la 1b.
- **P4, le regate della 1b non cambiano:** `tests/arrivi_regate.py` sulle regate dei salti e dei giri e sui 2 tornei dà arrivi identici al bit.
- **P5, le due regate convertite funzionano:** bastone e raffiche con gli avversari dell'1b. In 20 semi per regata, livelli principianti ed esperti, **tutte le barche arrivano in almeno 19 regate su 20** (attesa nostra). Il metro dichiara quante regate ha davvero contato. I tempi si riportano senza soglia.
- **P6, il ramo della 1a è sparito davvero:** zero righe di codice in `js/` con `S.lv`, `lv2`, `RACES1` o `boatLv`. Oggi sono circa 48 e si contano prima e dopo, con lo stesso comando, scritto nel CHANGELOG.
- **P7, lezioni e prove sulla barca nuova:** si riportano i numeri, senza soglia: passi completati dal pilota (su 32, con 10 semi per passo), prove completate e tempi rispetto alle medaglie. Sono il punto di partenza del passo 3. Questo non è un criterio da passare: è una misura da riportare (vedi §6).
- **P8, pagina come la carica un giocatore:** senza `#collaudo`, in Chromium e Firefox, si aprono menu, una lezione, una prova, la navigazione libera e le quattro regate, e nessuna dà errori di pagina.
- **P9, pannello e menu** a 1360×650 senza pixel di eccesso (`collaudo_pannello.py`, caso peggiore compreso).
- **Non-regressione veloce:** `polare.js` e `raffiche_e_virate.js` (P2 e P3), `collaudo_versione.py`.

## 5. Rischi

- **Lezioni e prove più difficili per un principiante** (§3). È il rischio maggiore. La misura 0 lo dice prima.
- **Collaudi che cadranno perché misurano la 1a:** `collaudo_lezioni`, `collaudo_pilota_lezioni`, `collaudo_fasce`, i collaudi della carriera, `collaudo_regate`, `collaudo_triangolo`, `collaudo_partenze`, `collaudo_boma_poppa` (fa girare anche la 1a), `collaudo_impronta`. Si elencano prima di cambiare il codice: ogni caduta dev'essere fra quelle previste, oppure è un difetto. Quelli che misurano solo la 1a si adattano o si tolgono, e lo si dichiara.
- **Le due regate convertite ereditano i difetti noti degli avversari dell'1b:** tagliano fuori dagli estremi, girano male le boe. Sulla 1b si è deciso di avere pazienza, ma ora queste diventano le regate della scuola.
- **Pulizia lunga:** 4 file di gioco e circa 10 collaudi. La divido in commit separati (motore, gioco, regate, nomi, collaudi), ognuno con P1 verde.
- **La copia congelata della 1a** è codice morto tenuto apposta: lo dico nella prima riga del file.

## 6. Da decidere (Ale)

1. **Dopo la pulizia, le lezioni e le prove possono restare per un po' più difficili o incomplete, finché non arriva il passo 3?** In pratica: si fa il push della versione pulita anche se, per esempio, 5 passi su 32 non si completano più sulla 1b, oppure lo si tiene fermo sul tuo PC finché le lezioni non sono riscritte? La misura 0 dirà quanti sono.

Il resto (copia congelata della 1a, nomi senza «2», le due regate convertite e non buttate) lo propongo così come sta scritto. Se qualcosa non ti torna, dimmelo.

**Risposta di Ale (1 novembre):** «non saprei, va bene come è più comodo per te». Scelta mia: il gioco online (GitHub Pages) viene da `main`, quindi se la pulizia rompe dei passi va in un **ramo a parte** e passa in `main` solo insieme alle lezioni riscritte (passo 3). La misura 0 dice che qualcosa si rompe (§7): quindi ramo a parte.

## 7. Esito della misura 0 (1 novembre 2026)

Come è stata fatta: una copia della pagina (`tests/sorgente.py`, `copia`) con una sola riga in più all'inizio di `step()`, `S.lv = 2`. Così ogni barca è quella dell'1b e il resto del gioco è identico. Il gioco vero non è stato toccato. Su questa copia ho lanciato gli stessi collaudi che uso sulla pagina di oggi, che ha la 1a; quella di oggi l'ho rilanciata per avere il confronto.

**Pilota delle lezioni** (`collaudo_pilota_lezioni.py`, semi 1-10, 32 passi pratici, 640 corse a mani ferme, 0 errori della pagina):

| | 1a (oggi) | 1b |
|---|---|---|
| Passi completati guidando 10 volte su 10 | 30 (più 5.8 9/10 e 6.3 4/4*) | 27 |
| Passi mai completati guidando | 0 | **1**: 3.10 «Filetto sottovento», 0 su 10 |
| Passi che si completano da soli, senza toccare niente (10 su 10) | 0 (6.3 6 su 10*) | **4**: 2.4 «Barra sottovento: si orza», 3.2 «Bolina», 5.2 «Prepararsi a virare», 6.2 «Assorbire una raffica» |

\* Nella 6.3 «La scuffia» con la 1a la barca scuffia da sola 6 volte su 10, quindi il pilota guida solo nelle altre 4. Succede già oggi.

Tempi medi dei passi con la 1b: quasi tutti simili, con qualche eccezione. «Raddrizzare» passa da 4,0 a 11,0 s, perché la raddrizzata dell'1b dura 10 s. «Risalire il vento» passa da 65 a 74 s.

**Collaudo delle lezioni** (`collaudo_lezioni.py`, una corsa):
- **1a:** OK, 18 passi; c'è un «non completato» nel primo tratto di «cazzare», già noto.
- **1b:** FALLITO su 3 punti:
  - «L5 prepararsi (bolina lanciata)»;
  - «L6 raddrizzare» e «L6 raddrizzare partendo da dritta»: il collaudo aspetta 8 s, la raddrizzata dell'1b ne dura 10. È il collaudo che va adattato, non il gioco.

**Prove con le medaglie** (`collaudo_fasce.py`; tempo mediano del pilota contro il limite dell'oro di oggi):

| Prova | Oro oggi | 1a | 1b |
|---|---|---|---|
| 1 | 80 s | 79,0 | 79,2 |
| 2 | 125 s | 124,5 | 124,4 |
| 3 | 160 s | 156,8 | 158,7 |
| 4 | 280 s | 276,0 | **285,8** (oro mancato; 1 angolo morto in ogni corsa) |
| 5 | 300 s | 297,8 (24 su 24) | **302,4** (23 su 24: una non finita, 430 s nell'angolo morto col vento a 45°) |

**Cosa vuol dire:**
- Le lezioni restano quasi tutte percorribili.
- Un passo si rompe (3.10) e quattro diventano banali.
- Nelle prove 4 e 5 l'oro del pilota non basta più, e una corsa della 5 si blocca nell'angolo morto.

Sono tutte cose del passo 3 (lezioni riscritte) e del passo 4 (medaglie). La pulizia non le corregge, ma le rende visibili a chi gioca: per questo la pulizia va nel ramo a parte. Le copie dei collaudi usate qui stanno nella cartella temporanea della sessione e non entrano nel repository.

## 8. Fatto (1.1.0, 1 novembre 2026, ramo `pulizia`)

Via di Ale il 1 novembre. Esito completo, con i numeri, nel `CHANGELOG.md` alla voce 1.1.0. In breve:
- **Passati:** P1 (impronta dell'1b identica al bit), P2 (copia della 1a fedele, prototipo identico), P3 (riferimenti nuovi uguali alla 1b di prima), P4 (salti, giri e tornei identici al bit, testi esclusi), P5 (80 regate su 80 con tutte le barche arrivate), P6 (46 righe → 0), P8 (7 schermate su 7 in Chromium e Firefox, 0 errori), P9 (pannello 0 px; riquadro di bastone e raffiche 0 px).
- P7 è solo numeri: identici alla misura 0.
- **Non fatto:** il cambio dei nomi delle costanti (§2.A). Tocca 20 script e non cambia il gioco: lo rimando alla pulizia finale, e lo dico qui perché era nella proposta approvata.
- **Trovati per strada:**
  - l'introduzione della regata dei giri diceva «vento che gira, boa a 300 m», e non era vero: corretto;
  - il riquadro delle istruzioni di salti e giri sfora da prima, 84-406 px: non corretto, va col passo 3;
  - il prototipo del fiocco non era più identico alla 1a del gioco: scarto fino a 2,73 nodi;
  - `collaudo_triangolo` T2b fallisce anche su `main`.
