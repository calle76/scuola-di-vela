# Stato del progetto

**Una pagina sola, riscritta a ogni fine sessione.** Serve alle chat sul sito di Claude (nelle sessioni di Claude Code il repository si legge direttamente): per quelle bastano **questo file e `CHANGELOG.md`**. Aggiornato al **20 ottobre 2026, versione 1.0.35**.

## Dove siamo

**Il livello 1 è chiuso.** Il gioco è un simulatore didattico di vela in una pagina (`index.html` più `js/`), con 6 lezioni (32 passi pratici), 5 prove, 2 regate contro tre avversari, esame, brevetto e carriera. Tutto si collauda da solo: una carriera intera, da zero all'attestato, gira con **32 passi su 32 guidati** dal pilota e dà OK.

**Fatto nella sessione del 17 ottobre** (dettagli nel `CHANGELOG.md`): partenze degli avversari rifatte (1.0.16), contatti ridotti del 38% (1.0.17), avviso sul richiamo nel riquadro e parti 2-4-6 delle partenze chiuse (1.0.18), increspature più vive dentro le raffiche (1.0.19), due domande del ripasso tornate al loro posto (1.0.20), la lezione 5 spiega che andando all'indietro la barra va al contrario (1.0.21), pulizia del codice della partenza (1.0.22), la barca che balla sull'acqua, solo disegno (1.0.23).

**Fatto dopo, nella stessa giornata (1.0.24-1.0.28):** il punto sul livello 2 e il primo pezzo della sua fisica.
- **Decisioni di Ale sul livello 2** (`VISIONE-LIVELLI-E-CARRIERA.md` §3 e §8): tutta la fisica nuova c'è dal primo momento del livello 2, le lezioni la spiegano (non la accendono) e non si spegne; ogni livello ha la sua fisica e la sua barca; nel gioco libero si passa fra i livelli e si prova tutto in qualunque ordine, la carriera si apre coi brevetti. Nel livello 2 entrano: timone che stalla, «spingi il boma», salti di vento (la linea di partenza resta perpendicolare al vento medio, sono i salti a renderla storta). Tendenza orziera in sospeso; il resto al livello 3-4.
- **Timone del livello 2, in prova** (`PROPOSTA-STALLO-TIMONE.md`, con revisione in chat): nella navigazione libera, impostazioni, «Barca: livello 2 (prova)»; dalla 1.0.25 (idea di Ale) la freccia porta la barra fino a 35°, Maiusc + freccia fino a 45°. Il livello 1 è identico al bit. Con 45° si gira più in fretta (boe, penalità, barca lenta); il costo di velocità è piccolo e non regolare fra i venti, e nasce soprattutto mollando la barra. La barca del gioco pesa la metà del 470 delle fonti e frena circa il doppio più in fretta. Avvisi che si sovrappongono: rimandati da Ale.
- **«Spingi il boma», in prova (1.0.26):** Z tenuto premuto nella barca del livello 2; si esce dall'angolo morto 3 volte più in fretta che con la sola barra, la prua gira verso il boma come dicono le fonti, serve anche per frenare e andare all'indietro. Tutti i criteri nelle soglie (`PROPOSTA-SPINGI-BOMA.md` §8).
- **Raddrizzare con A** (1.0.27); R resta libero per i livelli futuri.
- **Salti di vento, in prova (1.0.28):** barca del livello 2 nella navigazione libera e «Regata nei salti di vento» (boa a 300 m, fuori da meriti e carriera); virare sugli scarsi rende circa il 6%, il salto persistente si gioca andando verso la rotazione (`PROPOSTA-SALTI-VENTO.md` §7-8). Percorsi a trapezio e triangolo: da fare.
- **Pulizia del codice (1.0.29):** solo commenti e collaudi, gioco identico al bit. Intestazione «BARCA DEL LIVELLO 2» in `motore.js` per trovare i controlli del livello 2; collaudo K5 aggiornato. Codice 292 864 byte. **`tests/fisica/timone2.js` esce con criteri FUORI soglia (C1, C3, C4, C8 a 6 nodi): è noto (§8 di `PROPOSTA-STALLO-TIMONE.md`), si confrontano le uscite con le precedenti, non l'esito.**
- **Piccole correzioni dal gioco di Ale (1.0.30, 19 ottobre):** omino con due gambe, banderuola con il perno più al centro, W e S sempre attivi come ↑ e ↓ (scritte invariate). 
- **La prua non va più oltre la bolina dopo la virata (1.0.31, 19 ottobre, `PROPOSTA-VIRATE-AVVERSARI.md`):** nella barca del livello 2 la rotazione la frenava solo la pala; ora la pala sente anche l'acqua che le arriva di lato e l'acqua frena lo scafo che ruota (idea e stime della revisione in chat), `yawG` ritarato. Prua del giocatore dopo la virata da 67-81° a 34-40°; avversari oltre la bolina + 15° dal 97% al 17% delle virate (soglia 5%: fuori, quasi tutte manovre volute della guida). Prezzo dichiarato: la pala stalla di rado e Maiusc non costa più velocità; virate più lente con 6-8 nodi. Provata da Ale e tenuta.
- **Raddrizzata del livello 2 (1.0.32, `PROPOSTA-RADDRIZZATA.md`):** 10 s invece di 3, barca al traverso con la vela lascata, avversari 15 s; da un video di allenamento; lezione breve da scrivere.
- **Torneo dell'1b, tappa T1 (1.0.34, `PROPOSTA-TORNEI-1B.md` §7):** 4 regate a bastone con la barca dell'1b contro gli stessi tre avversari, punteggio del regolamento (punti bassi, uno scarto, parità A8), penalità sul punteggio (+1 punto) invece dei 15 s, finestra d'arrivo, salvataggio dopo ogni regata, ritiri, meriti in carriera. Tutti i criteri nelle soglie; 1a identica (cambia solo il menu).
- **Distacchi in regata (1.0.33, `PROPOSTA-DISTACCHI.md`):** secondi da te accanto a ogni barca nella classifica, e all'arrivo i secondi dalla barca davanti e dalla prima. **Da fare, in quest'ordine:** cosa influenza l'abilità (cercare nel manuale), poi trapezio e triangolo.

**Impianto dei livelli (decisione di Ale, 19 ottobre 2026, sera):** ogni livello ha una sola novità grande e due parti, «a» teoria e «b» pratica (tornei e replay). **1a** = il livello 1 di oggi, congelato; **1b** = la barca completa (oggi «barca del livello 2, in prova»), replay, tornei con le regole semplici; **livello 2** = il regolamento (segnali, precedenze, penalità a giri) con la stessa deriva; **3** = fiocco, **4** = gennaker, **5** = equipaggio da tre e tattica. Unico riferimento: `VISIONE-LIVELLI-E-CARRIERA.md` §2.

## Come si lavora (regole che non cambiano)

- **Due fermate per ogni compito:** prima una proposta scritta con criteri misurabili e soglie dichiarate; poi, dato il via, si implementa e si misura. **Le soglie non si cambiano dopo aver visto i risultati**: un numero fuori fascia si riporta com'è.
- **Prima la barca, poi il resto:** in ogni livello si chiude la fisica, si congela con l'impronta, si pulisce il codice e i documenti, e solo dopo vengono avversari, lezioni e per ultimi i tempi delle medaglie.
- **Dove un numero dipende dalla barca si deriva dalla barca** (lunghezze di `BOAT.length`, manovre simulate con lo stesso `step()`), non si scrive a mano in metri o secondi.
- **Onestà sui contenuti:** ogni affermazione nautica va verificata su fonti scritte o video (`FONTI-PUBBLICHE.md`, `CONTENUTI-DA-VERIFICARE.md`); le semplificazioni si dichiarano. Niente marchi, niente titoli che sembrino ufficiali; «brevetto», mai «patente».
- **Un solo tentativo non basta:** molte prove con semi fissi, soglia scelta su un gruppo di semi e confermata su un altro mai guardato.

## Numeri che contano oggi

- **Partenze degli avversari:** partenze con almeno un richiamo 3,8-6,7% (prima dell'83%), ritardo mediano al via 0,9-2,2 s, velocità al taglio 4,65-5,33 nodi, nessuno che non parte. Conferma su 2880 partenze con semi mai guardati.
- **Contatti fra avversari:** 128 in 80 regate complete (erano 208), barche con penalità dal 59% al 40%. Quel che resta sono sfioramenti alla boa fra mure opposte: serve il livello 2.
- **Increspature nelle raffiche:** trama nel cuore della chiazza da +267% a +340% rispetto all'acqua calma a zoom pieno, da +196% a +506% a zoom 0,5; costo del disegno +9,6%.
- **Barca:** bolina 4,7 nodi a 45° con 10 nodi di vento, 6,0 al traverso, 4,1 in poppa; virata riuscita in circa 3 s da 3,9 nodi, fallita da fermi.

## Aperto

1. **Prove giocando di Ale:** raddrizzata di 10 s dell'1b (1.0.32); distacchi in classifica (1.0.33); barca che balla, increspature, retromarcia con 15-20 nodi, disegno della vela, testi delle raffiche da dietro.
2. **Passo 5.8 «Strambata controllata»:** il pilota preciso non lo completa 4 volte su 100 (soglia: al massimo 1) per l'errore di lettura del pilota. Non è un difetto del gioco.
3. **Limiti dichiarati:** bolina dal 9 al 15% più lenta delle fonti con poco vento (`PROPOSTA-BOLINA.md` §11); nella barca dell'1b la barra a 45° (Maiusc) in virata non frena più della sola freccia, il prezzo è il controllo (`PROPOSTA-STALLO-TIMONE.md` §10, da riverificare con video); con 20 nodi fissi dopo la raddrizzata la barca non riparte (raro, solo nelle raffiche); nessuna tendenza orziera (si riprende al livello 3); avversari dell'1b oltre la bolina + 15° nel 17% delle virate, quasi tutte manovre volute.
4. **Semplificazioni da tenere a mente:** la massa non entra nella resistenza dello scafo; la linea di partenza è sempre perpendicolare al vento medio; lo scorrimento più veloce delle increspature nella raffica non ha fonti.

5. **Dal torneo (1.0.34):** il pilota prende 1,7 penalità per regata, quasi tutte prima del via (come nell'1a): con +1 punto l'una pesano molto. Nelle regate dell'1a, all'arrivo, il pannello sfora di 48 px (l'1a è congelata: da decidere). Tornando al menu a metà regata del torneo, la regata si ricorre da capo.

## Prossimo lavoro

Impianto e ordine in `VISIONE-LIVELLI-E-CARRIERA.md` §2. La barca dell'1b non ha più punti aperti.

1. **Congelare la barca dell'1b:** un collaudo che la fotografa, come l'impronta fa per l'1a.
2. **Pulizia** di codice e documenti (proposte finite, numeri vecchi dei livelli).
3. **Avversari con la barca dell'1b** (partenze, virate, boe) su molte regate.
4. **Tornei** dell'1b: T1 fatta (1.0.34); T2, il triangolo, dopo la barca congelata e gli avversari (`PROPOSTA-TORNEI-1B.md`), **lezioni brevi** dell'1b, **menu** (attestato di partecipazione, brevetto dell'1b).
5. **La regata come fonte, solo nei tornei della parte «b»** (Ale, 20 ottobre 2026): replay, momenti salienti, ripasso «ripeti da qui», domande sulle penalità, tarati su quello che insegna il livello. Rimandata a dopo i tornei; la fermata 1 e la revisione in chat sono in `PROPOSTA-REGATA-COME-FONTE.md` §9 (§9.8 = cosa resta da risolvere). Poi i **tempi delle medaglie**.
6. Poi il **livello 2** (il regolamento: segnali, precedenze, penalità a giri; `PROPOSTA-SEGNALI-PARTENZA.md` è già pronta come fermata 1).

## Dove cercare

`PROGETTO.md` principi · `ROADMAP.md` ordine dei lavori · `CHANGELOG.md` cosa è cambiato e perché · `COLLAUDI.md` come si collauda · `FISICA-E-TARATURE.md` costanti e fonti del motore · `PROPOSTA-*.md` una per compito, con criteri e misure · `OSSERVAZIONI-GIOCANDO.md` quello che Ale trova giocando.
