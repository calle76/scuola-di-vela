# Proposta: il circuito nazionale, con batterie da 6 barche (fermata 1)

14 novembre 2026, sera. Ale: «ok B ora e A al nazionale», poi «passa al nazionale» (`DECISIONI.md`). Allo zonale (1.2.36) si corre in batterie da 4; al nazionale la tua batteria diventa più grande, come premio della promozione, perché salire di circuito cambi qualcosa in acqua (`PROPOSTA-RIVALI-E-SPONSOR.md` §7 e §16). In `js/` non è stato scritto niente.

## Cosa c'è oggi, e cosa blocca 6 barche

Letto nel codice il 14 novembre sera (`js/regate.js`):

| Cosa | Oggi | Con 6 barche |
| --- | --- | --- |
| Aspetti delle barche (`FLEET_LOOK`) | 3: rossa, verde, blu | ne servono 5 |
| Posizioni di partenza (`startSpots`) | scatola di 60 m × 28 m dietro la linea (preparazione corta), almeno 20 m fra due barche, nessuna rotta di collisione entro 25 s; se non trova posto, ripiego a zigzag «verificato per quattro barche» | 6 barche a 20 m in 60 × 28 m ci stanno appena: va misurato quante volte scatta il ripiego, e il ripiego va verificato per 6 |
| Linea di partenza | 70 m | probabilmente basta: la regola pratica è circa 1,5 lunghezze di scafo per barca, cioè una ventina di metri per 6 derive **[da verificare]** |
| Punti del torneo | calcolati sul numero di barche (`torPunti`): reggono già | nessun cambio; i punti delle regate a tema (4/3/2/1) non c'entrano |
| Precedenze, contatti, penalità | mai provati con più di 4 barche | da misurare |
| Cono d'ombra, scritte sulle barche | provati con 4 | da misurare con 6: più coppie, più scritte da sistemare |
| Finestre del torneo | tabella di 4 righe, schede di 3 rivali | 6 righe, 5 schede: da misurare a 1360×650 |
| Velocità del gioco | mai misurata con più barche | da misurare |

## Proposta: due passi

**Passo 1 (1.2.38): regate a 6 barche.** Solo il motore intorno alla regata, nessun circuito nuovo.
- **Due aspetti nuovi:** viola e grigia, che non si confondono con il blu, il verde e le batterie gialla, bianca e arancione.
- **Partenza:** la scatola dietro la linea si allarga con il numero di barche (in larghezza, per esempio 15 m per barca); il ripiego si rifà e si verifica per 6.
- **Il torneo può avere 3 o 5 rivali.** Il torneo singolo resta a 3; quello a 5 si usa solo dal nazionale (e da un'opzione di prova, se Ale la vuole).
- **Finestre:** tabella di 6 righe, 5 linguette nelle schede dei rivali.

**Passo 2 (1.2.39): la stagione nazionale.**
- **Chi c'è (12 regatanti):** tu, i 10 rivali nazionali già approvati (`PROPOSTA-RIVALI-E-SPONSOR.md` §12, Chiara Benedetti … Riccardo Bassi) e il migliore degli altri del tuo zonale. Il giocatore ritrova un volto noto.
- **Due batterie da 6:** la tua corre in acqua, l'altra a numeri, come allo zonale.
- **4 tappe**, con posti nuovi, inventati. La classifica, le frasi e il salvataggio sono quelli dello zonale.
- **Rivali più forti.** Il gruppo nazionale ha più doti dello zonale: per area 4 doti, 4 medie e 2 difetti, invece di 3-4-3. È una scelta di Ale, vedi sotto.
- **Chi può entrare:** in carriera chi ha il «diritto al nazionale» (primi 3 dello zonale, già salvato dalla 1.2.36); nel gioco libero tutti, come sempre (principio 2).
- **I primi 3 del nazionale:** «diritto alla finale», solo scritto, come oggi per il nazionale.

## Criteri, con soglie fissate prima di provare

Passo 1:

| # | Criterio | Soglia |
| --- | --- | --- |
| N1 | Posizioni di partenza | 1000 partenze con 6 barche: vincoli rispettati in tutte; ripiego usato al massimo nell'1%; con il ripiego, distanze ≥ 20 m |
| N2 | Partenze pulite | 100 regate da 6 col pilota: contatti nei primi 25 s dopo la nascita: 0 |
| N3 | Precedenze con 6 | 100 regate da 6 col pilota: tutte finiscono (nessuna barca ferma per sempre); contatti per coppia di barche per regata al massimo il doppio di quelli con 4 barche sugli stessi semi |
| N4 | Velocità del gioco | tempo di calcolo di un passo con 6 barche al massimo 1,8 volte quello con 4 (misurato nella pagina, Chromium e Firefox) |
| N5 | Scritte e cono | `collaudo_etichette` con 6 barche: 0 scritte piene sopra uno scafo, 0 sopra la tua; il cono d'ombra calcolato per tutte le coppie |
| N6 | Pannello | 0 px di eccesso a 1360×650: tabella del torneo a 6 righe, 5 schede, riquadro delle bandiere |
| N7 | Con 4 barche niente cambia | impronta del guardiano identica al bit, `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici, `collaudo_stagione` e `collaudo_stagione_amico` OK |

Passo 2: quelli dello zonale (Z1-Z7, Z12-Z14) rifatti per 12 regatanti e batterie da 6, più:

| # | Criterio | Soglia |
| --- | --- | --- |
| N8 | Il nazionale è più duro | 2000 stagioni a numeri: il giocatore a forza 0 finisce in media più indietro al nazionale che allo zonale |
| N9 | Chi entra | carriera: senza il diritto il nazionale è chiuso, col diritto si apre; gioco libero: sempre aperto |

## Costanti nuove (nostre, senza fonte)

- 6 barche nella tua batteria, 12 regatanti al nazionale;
- gruppo nazionale 4-4-2 invece di 3-4-3;
- 15 m di larghezza per barca nella scatola di partenza;
- i colori viola e grigio.

## Fonti

F89 (ranking e regate nazionali; la regola per cui si sale dai circuiti zonali al nazionale è **[da verificare]** su una fonte scritta). La regola pratica della linea di partenza, circa 1,5 lunghezze per barca, è **[da verificare]**.

## Rischi

- **Più barche, più ingorghi** alle boe e in partenza: le precedenze dell'1b non sono mai state provate con più di 4 barche. È il rischio grosso, ed è per questo che il passo 1 viene da solo.
- **La guida degli avversari** è tarata con 4 barche (cono d'ombra, layline): con 6 potrebbe peggiorare. Il guardiano è solo informativo, quindi lo si riporterà come numero, non come esito.
- **Il PC di Ale:** 6 barche e il cono d'ombra costano di più; N4 lo misura, ma sul PC del collaudo.
- **La leggibilità:** sei barche nei 1360 px si seguono ancora (§7 diceva fino a 6-7), ma le scritte diventano tante.

## Cosa serve da Ale

1. Il via al passo 1. Il passo 2 parte dopo, con la sua fermata.
2. Tre scelte:
   - **rivali nazionali più forti** (4-4-2, consiglio) oppure uguali allo zonale;
   - **il dodicesimo** del nazionale: il migliore del tuo zonale (consiglio) oppure un undicesimo nome nuovo;
   - **un'opzione di prova** per correre il torneo a 6 anche fuori dal nazionale (consiglio sì, nel gioco libero: serve anche ai collaudi).

## Esito del passo 1 (14 novembre, sera): 1.2.38 fatta, NON chiusa (N2 non passa)

Ramo `sei-barche`. `tests/collaudo_sei_barche.py` (25 tornei a 4 e 25 a 6 sugli stessi semi 880-904, pilota per il giocatore, preparazione 60 s), `misura_etichette.py` con `SEI=1`:

| # | Esito | Soglia |
| --- | --- | --- |
| N1 | 1000 partenze da 6: vincoli violati **0**, ripiego **0**; il ripiego a due file, provato a mano con 5 e 6 barche, rispetta le distanze | ✓ |
| N2 | contatti nei primi 25 s: **34** in 100 regate da 6. **Anche con 4 barche, cioè il gioco di oggi: 16** | 0 ✗ |
| N3 | regate ferme 0 su 100; contatti per coppia per regata **0,165** con 6, **0,172** con 4: rapporto **0,96** | ≤ 2 ✓ |
| N4 | 600 passi: Chromium 55 → 78 ms (**1,42**), Firefox 59 → 97 ms (**1,64**) | ≤ 1,8 ✓ |
| N5 | 20 regate da 6: 300 090 scritte, **0** piene sopra uno scafo, **0** sopra la tua; 383 trasparenti; cambi di posto a meno di 1 s: 0 | ✓ |
| N6 | pannello di regata con 6 barche 0 px; finestra del torneo a 6 righe 0 px; 5 schede 0 px (alla prima prova la 1 sforava di 20 px: i pulsanti con 5 nomi interi andavano su due righe, ora c'è solo il cognome) | ✓ |
| N7 | impronta del guardiano `2c0e3804a20d`, identica; `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici; `collaudo_stagione` e `collaudo_stagione_amico` OK; `collaudo_versione` OK | ✓ |

**Perché N2 non passa.** La soglia «0 contatti nei primi 25 s» l'ho scritta credendo che col gioco di oggi fosse 0, e non l'avevo misurato. Non è così: con 4 barche succede in 16 regate su 100. Il caso guardato da vicino (6 barche) non dipende da dove nascono le barche: dopo 20 s un rivale vira addosso alla barca del pilota (regola 13, colpa sua). Per coppia di barche la frequenza è la stessa con 4 e con 6 (16 su 600 coppie-regata contro 34 su 1500, cioè 0,027 e 0,023). Le 6 barche quindi non peggiorano: il difetto c'è già, e sta nella guida prima del via (voce 4, «virano addosso»; voce 17). La soglia resta quella scritta.

**Strade per Ale:**
- **chiudere la 1.2.38 dichiarando N2**: il difetto è vecchio, e con 6 barche non cresce per coppia;
- **oppure prima sistemare le manovre dei rivali prima del via** (voci 4 e 17), poi rimisurare.

**Corretto strada facendo:** «penalità alla Pietro Gallo» nel messaggio di un contatto fra due rivali (dalla 1.2.33).

**Decisione di Ale (14 novembre, notte): «A, chiudi la 1.2.38».** Chiusa con N2 dichiarato: contatti nei primi 25 s in 34 regate su 100 con 6 barche (16 su 100 con 4, nel gioco di prima). Le manovre dei rivali prima del via restano nelle voci 4 e 17.
