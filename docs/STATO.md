# Stato del progetto

**Una pagina sola, riscritta a ogni fine sessione.** Serve alle chat sul sito di Claude (nelle sessioni di Claude Code il repository si legge direttamente): per quelle bastano **questo file e `CHANGELOG.md`**. Aggiornato al **17 ottobre 2026 (sera), versione 1.0.24**.

## Dove siamo

**Il livello 1 è chiuso.** Il gioco è un simulatore didattico di vela in una pagina (`index.html` più `js/`), con 6 lezioni (32 passi pratici), 5 prove, 2 regate contro tre avversari, esame, brevetto e carriera. Tutto si collauda da solo: una carriera intera, da zero all'attestato, gira con **32 passi su 32 guidati** dal pilota e dà OK.

**Fatto nella sessione del 17 ottobre** (dettagli nel `CHANGELOG.md`): partenze degli avversari rifatte (1.0.16), contatti ridotti del 38% (1.0.17), avviso sul richiamo nel riquadro e parti 2-4-6 delle partenze chiuse (1.0.18), increspature più vive dentro le raffiche (1.0.19), due domande del ripasso tornate al loro posto (1.0.20), la lezione 5 spiega che andando all'indietro la barra va al contrario (1.0.21), pulizia del codice della partenza (1.0.22), la barca che balla sull'acqua, solo disegno (1.0.23).

**Fatto dopo, nella stessa giornata (1.0.24):** il punto sul livello 2 e il primo pezzo della sua fisica.
- **Decisioni di Ale sul livello 2** (`VISIONE-LIVELLI-E-CARRIERA.md` §3 e §8): tutta la fisica nuova c'è dal primo momento del livello 2, le lezioni la spiegano (non la accendono) e non si spegne; ogni livello ha la sua fisica e la sua barca; nel gioco libero si passa fra i livelli e si prova tutto in qualunque ordine, la carriera si apre coi brevetti. Nel livello 2 entrano: timone che stalla, «spingi il boma», salti di vento (la linea di partenza resta perpendicolare al vento medio, sono i salti a renderla storta). Tendenza orziera in sospeso; il resto al livello 3-4.
- **Timone del livello 2, in prova** (`PROPOSTA-STALLO-TIMONE.md`, con revisione in chat): nella navigazione libera, impostazioni, «Barca: livello 2 (prova)»; freccia = barra lenta, Maiusc + freccia = veloce. Il livello 1 è identico al bit. **L'obiettivo didattico non è raggiunto:** la differenza fra barra lenta e veloce compare solo con vento medio, nasce mollando la barra e non sbattendola, e sparisce con lo stallo a 15° o 30°. La barca del gioco pesa la metà del 470 delle fonti e frena circa il doppio più in fretta.

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

1. **Prove giocando di Ale:** barca che balla sull'acqua, timoniere, baffi alla prua e scuffia (1.0.23: ampiezze ipotesi da ritoccare guardando); increspature (1.0.19), retromarcia con 15-20 nodi, disegno della vela (1.0.7), testi delle raffiche da dietro da accorciare.
2. **Passo 5.8 «Strambata controllata»:** il pilota preciso non lo completa 4 volte su 100 (soglia: al massimo 1) perché strambo con il boma a 49° invece di 45° o meno, per l'errore di lettura del pilota. Non è un difetto del gioco; la soglia del collaudo resta com'è.
3. **Limite noto dichiarato (17 ottobre):** bolina dal 9 al 15% più lenta delle fonti con poco vento, +7% con 15 nodi; cause escluse e parziali in `PROPOSTA-BOLINA.md` §11. Il braccio sbandante `zCE` è fra i dubbi, per il livello 3.
4. **Semplificazioni dichiarate da tenere a mente:** il timone non stalla mai; la massa non entra nella resistenza dello scafo; la linea di partenza è sempre perpendicolare al vento; lo scorrimento più veloce delle increspature nella raffica non ha fonti (aiuto visivo).

## Prossimo lavoro

1. **Ale prova giocando la barca del livello 2** (navigazione libera, ⚙, «Barca: livello 2 (prova)»; Maiusc + freccia per la barra veloce): si sente la differenza fra accompagnare e sbattere la barra? La barca è piacevole o pigra?
2. **Timone del livello 2, seguito** (`PROPOSTA-STALLO-TIMONE.md` §8): o si cercano virate misurate su una deriva singola da circa 4 m e si ritara, o si ricontrolla prima la frenata della barca prua al vento (1-1,6 lunghezze contro 3-4, dubbio del 13 ottobre), che è la causa di fondo.
3. Poi gli altri pezzi della barca del livello 2: «spingi il boma», salti di vento; poi la fisica fra le barche (copertura del vento), le regole, le lezioni. Ordine: «prima la barca, poi il resto».

## Dove cercare

`PROGETTO.md` principi · `ROADMAP.md` ordine dei lavori · `CHANGELOG.md` cosa è cambiato e perché · `COLLAUDI.md` come si collauda · `FISICA-E-TARATURE.md` costanti e fonti del motore · `PROPOSTA-*.md` una per compito, con criteri e misure · `OSSERVAZIONI-GIOCANDO.md` quello che Ale trova giocando.
