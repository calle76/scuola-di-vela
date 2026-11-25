# Proposta: barche affiancate che si tengono (fermata 1)

**7 novembre 2026, su `main` (1.2.15). Fermata 1: nessuna riga del gioco cambiata.** 8 novembre: misura sulla prevenzione e modello rivisto ai §10-11; fermata 2 al §12: K1 non raggiunto, gioco invariato. Ale: «vai con la proposta sulle barche affiancate». Osservazione 94 (boa delle 17:07) e parte della 93 (partenza delle 17:25).

## 1. In breve

Quando due o tre barche navigano affiancate e vicine, si tengono a vicenda: chi deve cedere non vira mai per togliersi, e chi ha la precedenza poggia un poco per non toccare, trascinandosi dietro l'altra. Si liberano solo quando scade il limite di 25 s messo a suo tempo proprio per questo (`SCARTO_MAX`). Alla boa delle 17:07 è costato circa 25 s a tre barche, finite 70 m oltre la boa. Proposta: **chi deve cedere può anche virare**, se la virata la porta dove vuole andare e passa libera da tutte le barche vicine.

## 2. Che cosa succede (letto nel codice, verificato sul file delle 17:07)

Alla boa di bolina delle 17:07 tre barche arrivano mure a sinistra, affiancate a 2-7 m: Rossa sottovento, Blu in mezzo, Verde sopravento. Rossa ha la precedenza (regola 11), Blu cede a Rossa, Verde cede a Blu.

1. **Chi cede non può virare.** In `cedeAvv1b` (`js/regate.js`) le rotte provate per cedere sono tutte sulle mure che la barca ha: virare non è fra le scelte. Verde, la più esterna, a t=97 vorrebbe virare verso la boa (punto di passaggio 1), ma cedendo a Blu resta mure a sinistra.
2. **Chi ha la precedenza poggia.** Rossa ha Blu entro 1,5 lunghezze (`ULTIMO`): la regola «scarta all'ultimo» la fa poggiare di 15° (da 46° a 61° dal vento). Blu e Verde, cedendo, la seguono. Il gruppo va al lasco verso destra.
3. **Si liberano a tempo.** Dopo 25 s di scarto (`SCARTO_MAX`, t≈115) Rossa smette, vira, e le altre la seguono. Il commento nel codice dice già che il limite era nato perché «due barche parallele e vicine si tenevano a vicenda».

Nella regata vera la più esterna, che non ha nessuno sopra, vira per prima; poi la seconda, poi la terza. Le regole lo permettono: chi deve tenersi discosto lo può fare come vuole, anche virando, purché durante la virata stia lontano dalle altre (regole 11 e 13, definizione «tenersi discosto», F15).

## 3. Quanto succede (numeri di partenza)

Scena nuova nello strumento `tests/scene_strane.py`: **S8, coppia che si tiene** = una barca cede a X da almeno 10 s, X è entro 12,6 m (3 lunghezze) e le prue differiscono meno di 20°. Provata su un caso costruito (scatta) e uno simile con le prue a 90° (tace).

- **Nelle tue regate del 7 novembre:** 7, 2, 3 e 2 episodi (16:42, 16:55, 17:07, 17:25), prima e dopo il via.
- **Nel rigioco** (8 tue regate intere, la tua barca rifà la tua rotta, semi 561-580, 160 corse per browser):

| | Chromium | Firefox |
| --- | --- | --- |
| **S8 dopo il via, a corsa** | **0,55** (in 66 corse su 160) | **0,50** (62 su 160) |
| S8 prima del via, a corsa | 1,18 | 1,29 |
| Contatti a corsa (di cui prima del via) | 1,99 (0,89) | 1,89 (0,81) |
| S3 contatti di chi cede | 1,05 | 0,88 |
| S1 stretta (chi cede passa sotto 6,3 m) | 2,71 | 2,53 |

Prima del via le coppie sono più frequenti, ma lì le barche aspettano quasi ferme e virare non c'entra: è la parte di osservazione 93 che va in un'altra proposta (lo scivolare oltre l'estremità in attesa).

## 4. Il modello più semplice

In `cedeAvv1b`, per **chi deve cedere**, una scelta in più prima dei cambi di rotta: **virare** (o strambare, in poppa), cioè la prua che la barca vorrebbe già dalla sua guida quando quella è sulle altre mure.

- Si prova solo se la guida della barca vuole davvero cambiare mure (la sua rotta voluta è sulle altre mure), non per cedere e basta.
- Si sceglie solo se la nuova prua, valutata con la stessa previsione delle altre scelte (`passaggio`), passa ad almeno 2 lunghezze da **tutte** le barche vicine. Con una barca sopravento entro questa distanza la virata non si sceglie: così si libera prima la più esterna, poi le altre, come in acqua.
- Solo dopo il via, solo con abbrivio (almeno `U_ABBRIVIO`, 1,6 m/s, la soglia che c'è già: sotto, la barca si pianterebbe).
- Non cambia chi ha la precedenza, non cambia `chiCede`, non cambia `SCARTO_MAX` (resta come rete).

**Cosa non si tocca qui** (se K1 non basta, è la prossima proposta, da decidere con te): la regola «scarta all'ultimo» di chi ha la precedenza, che con una barca parallela a 2-3 m poggia anche se l'altra non si avvicina. Toccarla vuol dire decidere quando due scafi a meno di una lunghezza sono un pericolo, e oggi non ho un modo misurato per dirlo.

## 5. Criteri (soglie nostre, scritte prima di misurare)

Soglie scelte sui **semi 561-580** (già usati sopra per il «prima»); poi conferma sui **semi 581-600, mai guardati**. Chromium e Firefox. Prima e dopo sugli stessi semi, il prima su una copia congelata del codice.

- **K1, coppie dopo il via (S8 dopo il via):** almeno **-40%** in tutti e due i browser.
- **K2, non toccarsi di più:** contatti in tutto, S3 e S1 stretta al massimo **+10%**.
- **K3, la virata serve:** la scelta «virare per cedere» presa almeno 20 volte su 160 corse; nessuna barca piantata in più dopo il via (S7 al massimo come oggi più 0,02 a corsa).
- **K4, gli avversari corrono ancora** (`tests/misura_avversari.py`, semi 361-380, prima e dopo): non arrivate 0; penalità al massimo +10%; arrivo mediano **non peggiore** di oggi (ci aspettiamo che migliori); boe dal lato sbagliato non più di oggi.
- **K5, casi costruiti** (`collaudo_avversari1b.py`, `collaudo_avversari_deriva.py`): nessuno peggiora.
- **K6, barca invariata:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.
- **Da riportare, senza soglia:** la regata delle 17:07 rigiocata (quanto si allarga il gruppo alla boa); S8 prima del via; i secondi persi alla boa.

Un numero fuori soglia si riporta com'è.

## 6. Costanti nuove

Nessuna. Si usano quelle che ci sono: 2 lunghezze di passaggio libero, `U_ABBRIVIO`, la previsione di `passaggio` a 15 s.

## 7. Fonti

Regolamento di regata (F15): regola 11 (sopravento tiene discosto), regola 13 (durante la virata si tiene discosto), definizione «tenersi discosto». Che la barca più esterna viri per prima è la conseguenza delle regole, non una fonte esterna: lo dichiaro come ragionamento nostro.

## 8. Rischi

- **Virate in mezzo al gruppo:** la previsione di `passaggio` va dritta per 15 s e non sa che la barca rallenta virando. Per questo la soglia è 2 lunghezze, non meno, e K2 controlla i contatti.
- **Più virate in tutto**, che costano velocità: lo dice K4 (arrivo mediano).
- **Il rigioco esagera:** la tua barca non reagisce. Conta il confronto prima e dopo.
- **Vale anche per la Scuola** (decisione del 6 novembre): cambiano gli arrivi di tutte le regate con avversari e del torneo; `collaudo_competizione` e `collaudo_giri_avversari` vanno rilanciati.

## 9. Fermata 2, prima parte (7 novembre sera): **K1 non raggiunto, lavoro sospeso**

Ale: «via». Rigioco delle 8 regate di Ale, semi di scelta 561-580, 160 corse per browser; il prima su una copia congelata di `main` (5019b2e). Contatore nuovo in `tests/rigioca_regata.py`: `virCede`, quante volte chi cede sceglie di virare.

**Versione A, come al §4** (la virata si sceglie se passa a 2 lunghezze da tutte): S8 dopo il via 0,55 → 0,54 (Chromium, -2%), 0,50 → 0,47 (Firefox, -6%); virate scelte 179 e 178. **Perché non basta:** negli episodi S8 dopo il via la distanza mediana è 6,4 m e 69 su 86 sono sotto 8,4 m: due barche affiancate sono già sotto le 2 lunghezze, quindi la condizione non si avvera proprio dove serve.

**Versione B, cambiata dopo aver visto i numeri (dichiarato):** la virata vale anche se nessuna barca si avvicina più di adesso e restano tutte ad almeno una lunghezza. Codice, in `cedeAvv1b` prima del ciclo degli scarti:

```js
b.virCede = false;
if (devo && R.t >= 0 && s.u >= U_ABBRIVIO && sgn(norm180(twd - desired)) === -side){
  const lib = passaggio(b, desired), ora = Math.min(...R.boats.filter(o => o !== b && o.fin === null && !o.dnf && !o.S.capsized).map(o => Math.hypot(o.S.x - s.x, o.S.y - s.y)));
  if (lib >= 2 * L || (lib >= ora - 0.1 && lib >= L)){ b.virCede = true; return desired; }
}
```

| | Chromium: prima → B | Firefox: prima → B | Soglia | Esito |
| --- | --- | --- | --- | --- |
| K1 S8 dopo il via, a corsa | 0,55 → 0,42 (**-24%**) | 0,50 → 0,37 (**-26%**) | -40% | **no** |
| K2 contatti a corsa | 1,99 → 2,02 (+2%) | 1,89 → 1,84 (-3%) | +10% | sì |
| K2 S3 | 1,05 → 1,07 (+2%) | 0,88 → 0,84 (-5%) | +10% | sì |
| K2 S1 stretta | 2,71 → 2,70 | 2,53 → 2,42 | +10% | sì |
| K3 virate scelte | 391 | 330 | almeno 20 | sì |
| K3 S7 ferme, a corsa | 0,21 → 0,24 (**+0,03**) | 0,21 → 0,21 | al massimo +0,02 | **no** in Chromium |

K4 misurato sulla versione A (`misura_avversari.py`, semi 361-380, prima → A): non arrivate 0 → 0; penalità 123 → 123 e 110 → 113 (+3%); arrivo mediano 342 → 320,5 s e 341 → 341 s; boe sbagliate 2 → 0 e 0 → 0. Sulla versione B non ancora misurato.

**Stato:** `js/regate.js` è tornato identico a `main` (nessuna correzione nel gioco). Conferma sui semi 581-600 non guardata. **Da decidere con Ale:** la versione B dimezza circa un quarto delle coppie ma non arriva alla soglia; la parte che resta è probabilmente la regola «scarta all'ultimo» di chi ha la precedenza (§4, «cosa non si tocca qui»), che tiene il gruppo insieme poggiando.

## 10. Prevenire invece di curare: quante coppie si potevano evitare prima (8 novembre 2026, misura senza toccare il gioco)

Idea di Ale dal video F73 (Round Robin, min 3:34; trascrizione sezione 13): due barche affiancate e vicine sono un errore fatto prima, da evitare anche per chi ha la precedenza (regola 14). Prima di scrivere il modello ho misurato **quante coppie si potevano vedere arrivare qualche secondo prima**.

Strumento nuovo `tests/misura_coppie.py` (e `SALVA=cartella` in `rigioca_regata.py`, per tenere le tracce delle corse). Per ogni coppia S8 dopo il via guarda l'istante t0 in cui chi cede comincia a cedere. Le categorie le ho scritte prima di guardare i numeri:
- **A**, nata da una manovra: nei 10 s prima una delle due ha cambiato mure o lato;
- **B**, prevedibile: 5 s prima erano a 3 lunghezze o più e la previsione in linea retta (15 s) già passava sotto 2 lunghezze;
- **C**, già vicine: 5 s prima erano sotto 3 lunghezze;
- **D**, il resto.

**Cambi allo strumento fatti dopo aver visto le 8 regate vere e prima del rigioco (dichiarati):** in A il passaggio della linea si chiama «partenza» e non «boa»; C si divide in «ripresa» (la stessa barca cedeva alla stessa barca nei 30 s prima) e «nuova».

**Rigioco:** le 8 regate di Ale, Chromium, semi 561-580, 160 corse. In tutto 88 coppie dopo il via, cioè 0,55 a corsa, come al §3: la misura torna.

| | coppie | |
| --- | --- | --- |
| A nate da una manovra | 32 (36%) | 28 dalla partenza, 18 da una virata, 5 da un giro di boa (una coppia può averne più d'una) |
| **B prevedibili 5 s prima** | **1 (1%)** | |
| C già vicine, ripresa | 43 (49%) | |
| C già vicine, nuova | 5 (6%) | |
| D resto | 7 (8%) | |

- **Le coppie non sono incontri nuovi.** In 73 casi su 88 la stessa barca cedeva già alla stessa barca nei 30 s prima. Risalendo la catena (buchi fino a 30 s), 28 coppie cominciano prima del via, 15 nei primi 30 s, 41 fra 30 e 120 s e 4 dopo. Metà delle coppie si forma entro 48 s dal via.
- **Quando la catena comincia, le barche sono già vicine:** a metà dei casi sono a 8,4 m dopo il via e a 15,5 m prima. 5 s prima dell'inizio, le coppie dopo il via a 3 lunghezze o più erano 24 su 60, e la previsione in linea retta ne vedeva arrivare solo **7**. Le altre si avvicinano cambiando prua (virate, raffiche, scarti), non andando dritte.
- **Stesse mure:** 87 su 88. Chi cede sta **sopravento** in 58 casi (davanti 33, dietro 25) e **dietro e sottovento** in 29 (regola 12); 1 caso è diverso.
- **Dopo t0** vira per prima chi cede in 41 casi (dopo 17 s, a metà dei casi) e chi ha la precedenza in 38 (dopo 21 s); in 9 nessuna delle due vira entro 40 s.
- **Regate vere di Ale** (8 file): solo 8 coppie dopo il via, 4 A (dalla partenza o da una virata) e 4 C ripresa. Stesso quadro, troppo poche per contare da sole.

**Cosa ne ricavo.** «Guardare qualche secondo avanti» in linea retta, come fa già `cedeAvv1b` con i suoi 15 s, avrebbe visto al massimo 8 coppie su 88 (9%), lontano dal -40% di K1. Le coppie nascono da barche che partono o virano già vicine sulle stesse mure, e poi restano lì perché chi deve tenersi discosto si scosta del minimo (15°) e resta parallelo. La prevenzione utile, nello spirito del video, quindi non è «vedere prima» ma **«non restarci»**: chi deve tenersi discosto sulle stesse mure se ne va subito, invece di aspettare che il bordo finisca.

## 11. Modello rivisto (fermata 1, seconda versione): chi deve tenersi discosto sulle stesse mure se ne va

In `cedeAvv1b`, per chi deve cedere, dopo il via, con abbrivio (`U_ABBRIVIO`) e con l'altra barca **sulle stesse mure**:

1. **Si libera virando** (strambando, in poppa) **anche se il suo bordo non è finito**, quando la virata passa libera con la condizione della versione B (§9): a 2 lunghezze da tutte, oppure nessuna più vicina di adesso e tutte ad almeno una lunghezza. Fino a ieri la virata valeva solo se la guida voleva già virare. Dopo, il bordo ricomincia (`cambiaBordo`), così non si torna subito indietro.
2. **Non entro 30 m dal bersaglio**, dove decide già la regola «vicino al bersaglio» (`near`): lì virare per liberarsi farebbe sbagliare la boa.
3. Se la virata non passa libera, resta lo scarto di oggi; `SCARTO_MAX` resta come rete.

Non cambia: chi ha la precedenza, `chiCede`, la regola «scarta all'ultimo», le prue prima del via. Le coppie che nascono prima del via (28 su 88) restano alla proposta sull'osservazione 93.

**Criteri:** gli stessi K1-K6 del §5, soglie **non cambiate** (K1 almeno -40% di coppie dopo il via in tutti e due i browser), semi 561-580, poi conferma sui 581-600 mai guardati. In più, da riportare senza soglia: virate a regata per barca, prima e dopo.

**Costanti nuove:** nessuna (2 lunghezze, `U_ABBRIVIO` e i 30 m di `near` esistono già).

**Rischi:** più virate, che costano tempo (K4, arrivo mediano); una barca che si libera sopravento può finire addosso a una terza (K2); e K1 potrebbe non arrivare a -40%, perché un terzo delle coppie viene dalla partenza e una parte dai casi in cui la virata non passa libera. **La mia stima, non misurata: fra -30% e -45%.**

**Fonti:** F15, regole 11, 12 e 13 e definizione «tenersi discosto». F73 (sezione 13 della trascrizione): affiancate e vicine è una situazione da non avere. Che chi deve tenersi discosto lo faccia virando via è un'applicazione nostra, dichiarata.

## 12. Fermata 2 del modello rivisto (8 novembre 2026): **K1 non raggiunto, il gioco resta com'era**

Ale: «vai avanti». Rigioco delle 8 regate di Ale, semi 561-580, 160 corse per browser. Il «prima» è il codice di `main` (178cb8b, uguale a 5019b2e nei file di `js/`): su Chromium riproduce esattamente i numeri del §3 e del §9.

**Prima versione, come al §11: aveva un difetto.** Le coppie scendevano molto (Chromium 0,55 → 0,26, Firefox 0,50 → 0,25), ma K5 non passava: `collaudo_avversari1b`, scenario 5 (tre barche alla boa), da 10 su 10 a 8 su 10. Con una stampa di controllo, su una copia del gioco, ho visto la causa. La strambata non segna la barca come «in manovra» (`b.virando`), e a virata cominciata nemmeno la guida lo fa subito. Così la regola nuova cambiava bordo a ogni fotogramma (`cambiaBordo`), e la guida rimbalzava fra le due mure. **Il calo delle coppie veniva da questo rimbalzo, non dalla regola.**

**Correzione (difetto, non modello):** la regola scatta solo se la guida vuole ancora le mure che la barca ha (`b.side === side`), quindi una volta per manovra. Ho provato prima un'altra condizione, «chi prende già la boa sulle mure che ha non vira via», ma non cambiava niente ed è stata tolta. Con la correzione `collaudo_avversari1b` torna 10 su 10 in tutti gli scenari. Ho rifatto tutte le misure su una copia congelata di questa versione.

| | Chromium: prima → dopo | Firefox: prima → dopo | Soglia | Esito |
| --- | --- | --- | --- | --- |
| **K1 S8 dopo il via, a corsa** | 0,55 → 0,57 (**+4%**) | 0,50 → 0,59 (**+18%**) | -40% | **no** |
| K2 contatti a corsa | 1,99 → 1,98 | 1,89 → 1,95 (+3%) | +10% | sì |
| K2 S3 | 1,05 → 1,07 | 0,88 → 0,89 | +10% | sì |
| K2 S1 stretta | 2,71 → 2,56 | 2,53 → 2,36 | +10% | sì |
| K3 virate scelte | 320 | 387 | almeno 20 | sì |
| K3 S7 ferme, a corsa | 0,21 → 0,27 (**+0,06**) | 0,21 → 0,23 | al massimo +0,02 | **no** in Chromium |
| K4 non arrivate (`misura_avversari`, semi 361-380) | 0 → 0 | 0 → 0 | 0 | sì |
| K4 penalità | 123 → 118 | 110 → 104 | +10% | sì |
| K4 arrivo mediano | 342 → 344,5 s (**+0,7%**) | 341 → 301 s | non peggiore | **no** in Chromium (di poco) |
| K4 boe sbagliate | 2 → 0 | 0 → 0 | non più di oggi | sì |
| K5 `collaudo_avversari1b` | 10/10 in tutti gli scenari | (non lanciato) | nessuno peggiora | sì |
| K5 `collaudo_avversari_deriva` | identico al prima (casi 81 6/10, 83 7/10) | identico al prima (81 6/10) | nessuno peggiora | sì (fallisce già sul codice di oggi) |
| K6 `polare`, `raffiche_e_virate`, `impronta1b` | identici | | identici | sì |

Cambi di mure dopo il via, per barca (senza soglia): 5,4 prima, 5,8 con la prima versione (Chromium).

**Perché non basta** (`misura_coppie.py` sulle corse dopo, Chromium): chi cede ora vira per primo più spesso (63 casi su 92, prima 41 su 88), ma le coppie si riformano. Quelle nate da un cambio di mure salgono da 18 a 28, e chi ha la precedenza vira anche lei (13 contro 8): le due barche si ritrovano vicine sulle mure nuove. La virata libera la barca solo per qualche secondo.

**Decisione presa da me secondo le regole:** K1 non è raggiunto, quindi la correzione non resta. `js/regate.js` è identico a `main` (diff vuoto); `polare.js`, `raffiche_e_virate.js` e `impronta1b.js` sono identici. La conferma sui semi 581-600 non serve: il «prima» è stato misurato, il «dopo» della prima versione è stato scartato senza guardarlo.

**Cosa ne ricavo per la prossima volta:** in questo gioco una coppia non si scioglie con una manovra di una barca sola, perché la guida delle due barche le riporta vicine (bordi a tempo, stessa boa). Se si riprende, la strada da provare è che chi si libera **resti libero**: dopo la virata, un bordo minimo o una rotta che non torni verso l'altra. Va misurato prima, con lo stesso `misura_coppie.py`.

## 13. Terzo modello: chi si libera resta libero (fermata 1, 13 novembre 2026, sera)

Ale ha chiesto cos'era la voce 3 e ha detto «vai avanti»; questa è la proposta da riprendere, **senza codice**. Parte da quello che il §12 ha misurato. La virata di chi cede funziona (63 casi su 92), ma poi la coppia si riforma per due motivi:
- le coppie nate da un cambio di mure salgono da 18 a 28;
- anche chi ha la precedenza vira (13 casi contro 8), e le due barche si ritrovano vicine sulle mure nuove.

**Modello** (il §11 com'era, più due regole):
1. **Bordo minimo dopo la virata che libera.** Chi ha virato per liberarsi non rivira per `T_LIBERO` secondi, anche se il suo bordo a tempo scade. Restano le eccezioni di sempre: vicino al bersaglio (`near`, 30 m) e sulla layline.
2. **Chi ha la precedenza non la insegue.** Per `T_LIBERO` secondi dopo che l'altra si è liberata virando, chi aveva la precedenza non vira verso di lei. In pratica rimanda la sua virata a tempo, se dopo la virata passerebbe a meno di 3 lunghezze (12,6 m) dalla barca appena liberata. È la stessa prova della voce 4 (`PROPOSTA-MANOVRE-ADDOSSO.md`, parte A), con una distanza più larga.

**Costante nuova:** `T_LIBERO`, ipotesi nostra, senza fonte. Si sceglie fra 10, 15 e 20 s sui semi 561-580; la conferma è sui 581-600, mai guardati.

**Criteri:** gli stessi K1-K6 del §5, con le soglie **non cambiate**: K1 almeno -40% di coppie dopo il via, in tutti e due i browser. Da riportare senza soglia:
- le coppie nate da un cambio di mure, prima e dopo;
- quante volte chi aveva la precedenza vira entro `T_LIBERO`.

**Con la voce 4.** Le due proposte toccano la stessa guida, e la parte A della voce 4 da sola potrebbe già togliere una parte delle coppie riformate. Se Ale dà il via a tutte e due, si misurano tre versioni sugli stessi semi: solo la 4, solo la 3, tutte e due. Così si vede quanto vale ciascuna, ed entra solo quello che passa i criteri.

**Rischi:**
- un bordo minimo più lungo può portare oltre la layline: lo controlla K4, l'arrivo mediano;
- K1 potrebbe ancora non arrivare a -40%, perché 28 coppie su 88 nascono prima del via e restano alla voce 2.

## 15. Voci 4B e 3 insieme: fermata 2 (23 novembre 2026, notte; Ale: «parti con 4B e 3 insieme, vai in autonomia»)

**Scritto prima di misurare.** Codice (gioco 1.3.46, `js/regate.js`): la voce 3 come al §11 più §13, accanto alla 4B già scritta e spenta (`MANOVRE`); interruttore `COPPIE` (spento) e `__sv.coppie(on, T_LIBERO)` per le misure; in più `__sv.manovre(on, max, false)` toglie alla 4B l'attesa alla partenza (la «strada 2» dell'esito della 4B, `PROPOSTA-REGOLE-15-16.md`: scritta dopo aver visto i semi 2201-2230, quindi va dichiarata e conta solo come variante). **Tutte e due valgono solo nelle regate di Deriva (`R.r1516`)**: la Scuola resta identica (decisione del 9 novembre, «la Scuola basta che non peggiori»).

**Cosa cambia nel metro, dichiarato:** i K1-K6 del §5 si misuravano col rigioco delle regate della Scuola di Ale; ora la voce 3 vale solo in Deriva, quindi si misura come la 4B, sulle regate del torneo col pilota (`tests/misura_manovre.py`), dove S8 è già contata («coppie»). Lo strumento ora apre **una pagina nuova per ogni regata** (prima una per configurazione) e conta `liberate` (virate per liberarsi) e `insegue` (chi aveva la precedenza vira lo stesso entro `T_LIBERO`). Controllo fatto prima: con tutto spento le regate del seme 2201 sono identiche a quelle della 1.3.46 (`RADICE` = copia del commit c422bad).

**Criteri (soglie dei §5 e della 4B, non cambiate; base = tutto spento sugli stessi semi):**
- **Voce 3 da sola:** K1 coppie almeno −40%; K2 contatti (M3) al massimo +10%; K3 `liberate` almeno 20, piantati al massimo base +2; K4 arrivo mediano dei rivali non peggiore della base; fuori linea e non arrivati al massimo base +2 (come M5).
- **4B da sola:** M1-M5 come scritti (M1 −50%, M2 −30% se nella base ci sono almeno 15 casi, M3 non più della base, M4 entro +2%, M5 al massimo base +2).
- **Insieme:** tutte e due le liste; dove si sovrappongono vale la più severa (contatti non più della base, arrivo mediano non peggiore).
- **M6 / K5-K6:** Scuola identica (guardiano degli avversari), `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici.

**Semi:** scelta 2201-2230 (120 regate per configurazione; già guardati per la 4B il 16 novembre), conferma 2231-2260 mai guardati, Chromium; la configurazione scelta anche in Firefox sulla conferma. `T_LIBERO` fra 10, 15 e 20 s e `RINVIO_MAX` fra 4, 8 e 12 s si scelgono sui semi di scelta: la configurazione che passa tutti i suoi criteri con più margine su K1 (voce 3) o M1 (4B).

**Correzione del metro (23 nov, dopo le prime due configurazioni, prima di confrontarle):** il campo «coppie» di `misura_manovre.py` conta le coppie diverse per regata **anche prima del via**, mentre K1 parla di coppie dopo il via. Aggiunto `coppie_dopo_via`: episodi S8 (chi cede alla stessa barca da 10 s, entro 12,6 m, prue a meno di 20°) che arrivano ai 10 s dopo lo sparo. **K1 si giudica su `coppie_dopo_via`.** Le due configurazioni già fatte (base e `T_LIBERO` 10) si rifanno.

### Esito (23 novembre 2026, notte): **nessuna configurazione passa, il gioco resta la 1.3.46**

Chromium, semi di scelta 2201-2230, 120 regate del torneo col pilota per configurazione, una pagina nuova per regata; 1440 regate in tutto, picco 65 °C col freno 64/55. Uscite in `sperimentale/coppie-4b-3/misura_scelta1.txt` e `misura_scelta2.txt`. In grassetto i criteri non passati.

| | coppie dopo il via (K1 ≤ 10) | M1 (≤ 16) | M2 | M3 contatti | M4 arrivo (s) | piantati | fuori | non arrivati | liberate / insegue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | 18 | 33 | 11 | 119 | 188,7 | 0 | 36 | 144 | — |
| voce 3, `T_LIBERO` 10 | **11 (−39%)** | 20 | 11 | 107 | 187,1 | 0 | 35 | 130 | 353 / 4 |
| voce 3, 15 | **14 (−22%)** | 22 | 11 | 107 | 186,6 | 0 | 35 | 132 | 327 / 3 |
| voce 3, 20 | **11 (−39%)** | 19 | 11 | 100 | 186,6 | 0 | 35 | 128 | 307 / 11 |
| 4B, rinvio 4 | 9 | 16 (−52%) | 0 | 109 | 190,9 (+1,2%) | 0 | **39 (+3)** | 144 | — |
| 4B, 8 | 10 | 16 (−52%) | 0 | 109 | 191,7 (+1,6%) | 0 | **39 (+3)** | 146 | — |
| 4B, 12 | 10 | **21 (−36%)** | 0 | 112 | 191,2 (+1,3%) | 0 | **39 (+3)** | 146 | — |
| 4B senza attesa al via (v4, variante dichiarata) | 4 | 14 (−58%) | 6 | 107 | 192,0 (+1,7%) | 0 | **54 (+18)** | 136 | — |
| 4B 4 + voce 3 10 | 9 | **19** | 0 | 107 | **189,2** | 0 | **42** | **147** | 302 / 13 |
| 4B 4 + voce 3 20 | 11 | **19** | 0 | 103 | **190,8** | 0 | **42** | **157** | 266 / 19 |
| 4B 8 + voce 3 10 | 9 | **18** | 0 | 105 | 188,4 | 0 | **42** | 145 | 298 / 12 |
| 4B 8 + voce 3 20 | 9 | **17** | 0 | 102 | **189,8** | 0 | **42** | **157** | 261 / 17 |

- **M2** ha 11 casi nella base (meno di 15): non misurabile su questi semi, come scritto.
- **Voce 3 da sola:** passa tutto (contatti −10/−16%, arrivo mediano 1,6-2,1 s meglio, non arrivati meno) **tranne K1, per un episodio**: 11 coppie contro le 10 che servivano. La soglia non si tocca.
- **4B da sola:** col rinvio di 4 o 8 s passa M1, M3, M4, piantati e non arrivati; **non passa il «fuori» per una barca** (39 contro 38). Il «fuori» sale sempre (39-42) quando c'è l'attesa alla partenza; senza l'attesa (v4) sale molto di più (54): non è l'attesa da sola la causa. Rumore del «fuori» con tutto spento su altri gruppi di semi (16 nov): 36-43.
- **Insieme** va peggio di ciascuna da sola: M1 risale (17-19), «fuori» 42 in tutte e quattro, arrivo mediano peggiore in tre su quattro.
- La 4B da sola toglie già metà delle coppie dopo il via (18 → 9-10): le virate rimandate fanno anche partire meno barche appaiate.
- La conferma (semi 2231-2260) **non è stata guardata**: resta libera per una prova futura.

**Diagnosi delle 11 coppie che restano con la voce 3 (10 s)** (`diagnosi_c10.txt`, `diag_coppie.py`, stessi semi): 5 su rotta diretta (traverso o lasco, 63-120° dal vento), dove la regola non vale perché non si va a bordi; 5 si riformano da 1 a 7 s dopo una virata per liberarsi (la virata non basta: l'altra barca o una terza è di nuovo lì); 1 in poppa, con la strambata che non passava libera. In 4 su 11 l'altra barca è quella del pilota, che non conosce la regola «non inseguire».

**Stato:** `js/` identico alla 1.3.46. Codice in `sperimentale/coppie-4b-3/voce3_e_4b.patch` (si applica con `git apply`; le configurazioni `c*` e `v*` di `misura_manovre.py` la richiedono). **Da decidere con Ale:** (1) lasciare le due voci ferme; (2) la sola voce 3 con 10 s manca K1 di un episodio su 18 casi: si potrebbe allargare il metro (più semi, sempre gli stessi criteri) prima di dire che non passa, come previsto per M1-M2 sotto i 15 casi; (3) una voce 3 anche per la rotta diretta (metà delle coppie che restano), che chiede una fermata 1 nuova.

### Seconda misura (23 novembre 2026, mattina; Ale: «prova sulle regate lunghe oltre a nuovi semi su quelle corte»), scritta prima di misurare

- **Configurazioni** (scelte sui semi 2201-2230, prima di guardare i nuovi): base, voce 3 con 10 s e con 20 s (pari su K1), 4B col rinvio di 4 s, 4B 8 s + voce 3 10 s (la combinazione migliore).
- **Regate corte, semi nuovi 2231-2290** (240 regate per configurazione; i 2231-2260 erano la conferma mai guardata).
- **Regate lunghe** (`--lungo`, come il torneo vero: 3 regate da circa 10 minuti), **semi 2301-2360** (180 regate per configurazione), mai guardati.
- **Criteri e soglie: gli stessi del §15**, base = tutto spento sugli stessi semi. Se nella base un criterio ha meno di 15 casi si dichiara non misurabile.
- Il codice si misura su una copia del gioco con la patch applicata (`RADICE`), `js/` del repository resta com'è.

#### Risultati della seconda misura (Chromium; uscite in `sperimentale/coppie-4b-3/misura_corte_2231-2290.txt` e `misura_lunghe_2301-2360.txt`; picco 67 °C col freno)

**Regate corte, semi nuovi 2231-2290 (240 regate per riga).** In grassetto i criteri non passati.

| | coppie dopo il via (K1 ≤ 20) | M1 (≤ 21) | M2 (≤ 12) | M3 contatti | M4 arrivo (s) | fuori (≤ 74) | non arrivati (≤ 273) | liberate / insegue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | 34 | 42 | 18 | 249 | 188,4 | 72 | 271 | — |
| voce 3, 10 s | **27 (−21%)** | 43 | 18 | 248 | **188,6** | 68 | **287** | 721 / 11 |
| voce 3, 20 s | **28 (−18%)** | 43 | 18 | 245 | **188,6** | 68 | **290** | 638 / 24 |
| 4B, 4 s | 22 | **25 (−40%)** | 0 | 189 | **193,7 (+2,8%)** | **97** | 267 | — |
| 4B 8 s + voce 3 10 s | 14 | **26 (−38%)** | 0 | 184 | **193,2 (+2,5%)** | **93** | **289** | 618 / 18 |

**Regate lunghe (`--lungo`), semi 2301-2360 (180 regate per riga, 3 per torneo).**

| | coppie dopo il via (K1 ≤ 13) | M1 (≤ 14) | M2 | M3 contatti | M4 arrivo (s) | fuori (≤ 70) | non arrivati (≤ 174) | liberate / insegue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | 22 | 29 | 13 (non misurabile) | 193 | 583,4 | 68 | 172 | — |
| voce 3, 10 s | **22 (0%)** | 28 | 13 | 193 | 580,3 | 68 | 173 | 701 / 4 |
| voce 3, 20 s | **24 (+9%)** | 26 | 13 | 193 | 581,4 | 68 | **191** | 626 / 34 |
| 4B, 4 s | 13 (−41%) | **19 (−34%)** | 0 | 161 | 583,1 (−0,1%) | **101** | **182** | — |
| 4B 8 s + voce 3 10 s | **15** | **19** | 0 | 154 | **586,1** | **100** | **181** | 578 / 19 |

**Lettura:**
- **Le coppie sono rare** e nelle regate lunghe lo sono ancora di più per minuto: 22 in 180 regate da circa 10 minuti (una ogni 8 regate, come nelle corte, che durano un terzo).
- **La voce 3 non regge sui semi nuovi:** nelle corte −18/−21% (sui semi di scelta −39%), **nelle lunghe niente** (22 → 22 e 24), pur virando per liberarsi 600-700 volte. Il −39% dei semi di scelta era in buona parte caso, su 18 coppie.
- **La 4B toglie davvero i contatti** (−24% nelle corte, −17% nelle lunghe; quelli dopo una virata −34/−40%) e anche le coppie (−35/−41%), ma **fa partire in anticipo molte più barche**: fuori linea 72 → 97 nelle corte e 68 → 101 nelle lunghe. È l'effetto che sui semi di scelta sembrava di una barca sola (36 → 39).
- **Esito: né la voce 3 né la 4B si adottano**; la voce 3 si può chiudere (difetto raro, e la regola non lo toglie). Per la 4B la diagnosi qui sotto cerca quale pezzo fa uscire le barche.

#### Diagnosi della 4B: perché fa partire in anticipo (stessi semi corti 2231-2290, poi i lunghi 2301-2360; `diagnosi_fuori_linea.txt`)

Copie del gioco con un pezzo della 4B tolto alla volta (diagnosi, non modelli da adottare):

| | fuori linea (base 72) | M1 (base 42) | M3 (base 249) | M4 (base 188,4) | non arrivati (base 271) |
| --- | --- | --- | --- | --- | --- |
| 4B intera | 97 | 25 | 189 | 193,7 | 267 |
| x1: rinvio della virata solo dopo il via | 97 (uguale al bit: prima del via il rinvio non scatta mai) | 25 | 189 | 193,7 | 267 |
| x2: senza rinvio della virata | 97 | 28 | 198 | 194,4 | 273 |
| x3: solo le regole 15-16 nelle decisioni dei rivali (né rinvio né attesa) | **114** | 26 | 193 | 195,8 | 259 |
| **x4: 4B intera, ma regole 15-16 nelle decisioni dei rivali solo dopo il via** | **63** | 22 (−48%) | 240 | 192,5 (+2,2%) | 293 (+22) |
| x4 nelle regate lunghe (base: fuori 68, M1 29, M3 193, M4 583,4, non arrivati 172) | **57** | 13 (−55%) | 193 | 584,7 (+0,2%) | 180 (+8) |

- **Causa trovata:** le barche escono dalla linea perché prima del via i rivali decidono chi cede **con le regole 15 e 16** (`chiCede1516`): x3, solo quel pezzo, ne fa uscire 114 contro 72. L'attesa alla partenza ne toglie un po' (97). Il rinvio delle virate non c'entra.
- **x4** (le regole 15-16 nelle decisioni dei rivali solo dopo lo sparo) riporta il «fuori» sotto la base, in tutte e due le lunghezze. Nelle corte manca M1 (−48% contro −50%) e M4 (+2,2% contro +2%), e i contatti in tutto tornano quasi come la base (240: era proprio quel pezzo a toglierli). **Nelle lunghe passa tutto tranne «non arrivati» (+8 su 540).**
- **Cosa vuol dire «non arrivati»** (letto nel codice, `js/regate.js` riga 1185): nel torneo la regata si chiude quando arriva la barca del pilota; sono i rivali ancora in acqua in quel momento, cioè quelli dietro al pilota. +8 vuol dire rivali un po' più lenti rispetto al pilota, non barche che non finiscono.
- I semi 2231-2360 sono ormai stati guardati tutti: una prova di x4 da adottare va confermata su semi nuovi (per esempio 2601-2660 corti e 2701-2760 lunghi).
- Patch della variante: `sperimentale/coppie-4b-3/variante_x4_1516_dopo_il_via.patch` (si applica sopra `voce3_e_4b.patch`).

**Per Ale, una cosa alla volta:**
1. **Voce 3: proposta di chiuderla.** Difetto raro (una coppia ogni 7-8 regate) e la regola non lo toglie sui semi nuovi né nelle lunghe.
2. **4B: x4 è la strada più promettente.** Serve decidere se la 4B si giudica sulle regate lunghe (quelle del torneo vero), dove x4 manca solo i «non arrivati» (+8), o anche sulle corte, dove manca tre soglie di poco. Poi conferma su semi nuovi.

**Voce 3 chiusa da Ale il 23 novembre 2026, pomeriggio** (`DECISIONI.md`): il gioco resta senza la regola «chi si libera resta libero».

### Conferma della variante x4 su semi nuovi (23 novembre 2026, pomeriggio; Ale: «fai tutte le prove necessarie»), scritta prima di misurare

- **Cosa si misura:** la 4B intera col rinvio di 4 s (`m4`) più la variante x4 (regole 15-16 nelle decisioni dei rivali solo dopo lo sparo), cioè `voce3_e_4b.patch` + `variante_x4_1516_dopo_il_via.patch` su una copia del gioco 1.3.48 (`RADICE`; `js/regate.js` della 1.3.48 è identico a quello della 1.3.46). Voce 3 spenta. Base = tutto spento (`off`) sugli stessi semi, nella stessa copia.
- **Semi mai guardati:** corte 2601-2660 (240 regate per configurazione), lunghe (`--lungo`) 2701-2760 (180 regate per configurazione). Chromium. Poi, se il tempo e la temperatura lo permettono, la x4 e la base anche in Firefox sulle lunghe.
- **Criteri e soglie: quelli della 4B del §15, non cambiati:** M1 almeno −50%; M2 almeno −30% se nella base ci sono almeno 15 casi (altrimenti non misurabile); M3 contatti non più della base; M4 arrivo mediano dei rivali entro +2%; piantati, fuori linea e non arrivati al massimo base +2.
- **Come si riporta:** esito separato per corte e lunghe (la domanda di Ale su quali regate giudicarla resta sua). Ogni criterio fuori soglia si scrive com'è.

#### Risultati della conferma (Chromium; uscite in `sperimentale/coppie-4b-3/conferma_x4_corte_2601-2660.txt` e `conferma_x4_lunghe_2701-2760.txt`; picco 64 °C col freno)

| | M1 (−50%) | M2 (−30%) | M3 contatti (≤ base) | M4 arrivo (+2%) | piantati | fuori (base +2) | non arrivati (base +2) | coppie dopo il via |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| corte, base | 49 | 18 | 260 | 188,7 | 0 | 74 | 312 | 34 |
| corte, x4 | 20 (−59%) | 1 (−94%) | **269 (+3,5%)** | 190,0 (+0,7%) | 0 | 65 | 303 | 19 |
| lunghe, base | 37 | 13 (non misurabile) | 200 | 585,1 | 0 | 108 | 175 | 20 |
| lunghe, x4 | 15 (−59%) | 0 | 198 | 587,5 (+0,4%) | 0 | 81 | 164 | 20 |

- **Regate lunghe (quelle del torneo vero): passano tutti i criteri.** Le partenze anticipate, il difetto della 4B intera, scendono sotto la base (108 → 81).
- **Regate corte: passano tutti tranne M3**, i contatti in tutto: 269 contro 260 (+9). Non si cerca la causa ora (Ale, 23 nov: prima il giro di tutta la lista).

**Firefox, regate lunghe, stessi semi 2701-2760** (`conferma_x4_lunghe_2701-2760_firefox.txt`; picco 65 °C, 36 pause del freno): base M1 33, M2 14 (non misurabile), M3 192, M4 585,8, fuori 100, non arrivati 178; x4 M1 14 (−58%), M2 0, **M3 204 (+6%)**, M4 591,5 (+1,0%), fuori 82, non arrivati 167. In Firefox anche le lunghe mancano M3.

**Esito della conferma:** la x4 passa M1, M4, piantati, fuori linea e non arrivati in tutte e tre le misure; **M3 (contatti in tutto) passa solo in Chromium sulle lunghe** (198 contro 200) e non passa nelle corte (+3,5%) né in Firefox sulle lunghe (+6%). Per le soglie scritte la x4 **non si adotta**; resta in lista per il giro finale (Ale, 23 nov: «quando finiremo il giro di tutti i punti vedremo cosa rimane»).

## 16. Terza misura della x4, sulla 1.3.55 (Ale, 25 nov: «vai con C, fai tutti i test che vuoi in autonomia»), scritta prima di misurare

**Perché una misura nuova.** La conferma del §15 è sulla 1.3.48; dopo sono arrivate la regola 18 (1.3.49) e la marcatura (1.3.50), che toccano i contatti. In più M3 («contatti in tutto non più della base») su 180 regate ha un caso di circa ±20-30 contatti: +9 e +12 non dicono né che peggiora né che non peggiora. Il metro cambia **dopo aver visto quei numeri**, e si dichiara: le soglie vecchie si riportano accanto.

- **Cosa si misura:** x4 = `MANOVRE` col rinvio di 4 s (`m4`) più la riga «regole 15-16 nelle decisioni solo dopo lo sparo», su una copia della 1.3.55. La patch della voce 3 **non serve** (la x4 è una riga sola sopra il codice già spento nel gioco: `variante_x4_1516_dopo_il_via_1.3.55.patch`, `git apply --check` pulito). Con `MANOVRE` spento la copia è il gioco di oggi. `js/` del repository non si tocca.
- **Solo regate lunghe** (Ale, 25 nov: le corte non esistono più fuori dalla Scuola; la 4B vale solo in Deriva). Le corte non si rimisurano.
- **Semi mai guardati, gruppi separati:** Chromium 4001-4200, Firefox 4201-4400 (200 tornei = 600 regate per configurazione in ciascuno). Base e x4 alternate sulla stessa regata, pagina nuova per ognuna. Strumento: `tests/misura_x4.py` (la corsa è quella di `misura_manovre.py`).
- **Criteri.** Ricampionamento dei tornei (4000 volte, coppie base/x4), limite superiore al 95% dell'aumento relativo:
  - **N1 (era M3), sui due browser insieme (1200 regate per configurazione):** contatti in tutto, limite superiore **al massimo +10%**. Il 10% è la soglia già scritta per i contatti in K2 (§5), non scelta su questi numeri.
  - **N2 fuori linea e N3 non arrivati:** stesso modo, limite superiore al massimo +10%, sui due insieme.
  - **M1 almeno −50% e M2 almeno −30% (se la base ha almeno 15 casi), M4 arrivo mediano entro +2%, piantati al massimo base +2:** come prima, **in ciascun browser**.
- **Da riportare senza soglia:** M3 vecchio (≤ base), fuori e non arrivati vecchi (base +2) per browser; contatti col pilota; contatti per colpa e regola; coppie dopo il via; risultati separati per principianti (semi dispari) ed esperti (pari).
- **Regola d'arresto:** i semi sono questi, non se ne aggiungono dopo aver guardato. Se una corsa non finisce in tempo, si riporta quanti tornei completi ci sono e il criterio si dichiara su quelli.
- **Esito:** se passa tutto, si propone ad Ale di accenderla (il codice nel gioco aspetta il suo via); se N1 non passa, proposta di chiudere la 4B (consiglio già detto ad Ale).
