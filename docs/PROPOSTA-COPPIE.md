# Proposta: barche affiancate che si tengono (fermata 1)

**7 novembre 2026, su `main` (1.2.15). Fermata 1: nessuna riga del gioco cambiata.** 8 novembre: misura sulla prevenzione e modello rivisto ai §10-11 (fermata 1, seconda versione, aspetta il via). Ale: «vai con la proposta sulle barche affiancate». Osservazione 94 (boa delle 17:07) e parte della 93 (partenza delle 17:25).

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
