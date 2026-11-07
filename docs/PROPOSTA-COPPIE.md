# Proposta: barche affiancate che si tengono (fermata 1)

**7 novembre 2026, su `main` (1.2.15). Fermata 1: nessuna riga del gioco cambiata.** Ale: «vai con la proposta sulle barche affiancate». Osservazione 94 (boa delle 17:07) e parte della 93 (partenza delle 17:25).

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
