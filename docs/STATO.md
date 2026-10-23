# Stato del progetto

**Una pagina sola, riscritta a ogni fine sessione.** Serve alle chat sul sito di Claude (nelle sessioni di Claude Code il repository si legge direttamente): per quelle bastano **questo file e `CHANGELOG.md`**. Aggiornato al **23 ottobre 2026, versione 1.0.46**, durante la pulizia (`PROPOSTA-PULIZIA-1B.md`).

## Dove siamo

**Livello 1: l'1a è chiusa e congelata, la barca dell'1b è congelata (23 ottobre 2026).** Il gioco è un simulatore didattico di vela in una pagina (`index.html` più `js/`), con 6 lezioni (32 passi pratici), 5 prove, 2 regate dell'1a contro tre avversari, esame, attestato e carriera; nell'1b la «Regata nei salti di vento» e il torneo (tappa T1).

**Nomi dei livelli** (`VISIONE-LIVELLI-E-CARRIERA.md` §2, decisione di Ale del 19 ottobre 2026): ogni livello ha una parte «a» (teoria) e una «b» (pratica: tornei e replay). **1a** = le basi, barca semplice; **1b** = barca completa; **livello 2** = il regolamento, con la stessa barca dell'1b; **3** = fiocco; **4** = gennaker; **5** = equipaggio da tre e tattica. Solo nel livello 1 «a» e «b» hanno barche diverse. Nei documenti vecchi e nel `CHANGELOG.md` fino alla 1.0.46 «livello 2» vuol dire spesso la barca dell'1b, e nei più vecchi il fiocco; nel codice la barca dell'1b è ancora `lv 2` (`S.lv === 2`, `RUD2`, `BOMA2`, `SALTI2`, `RADD2`).

**Barca dell'1b** (dalla 1.0.24 alla 1.0.46, proposte in `archivio/`): timone che stalla (freccia fino a 35°, Maiusc fino a 45°), «spingi il boma» con Z, salti di vento, raddrizzata di 10 s al traverso, pala che sente l'acqua di lato e scafo frenato in rotazione (virate degli avversari), virata più agile (1.0.43), pala della sua taglia (1.0.44), scarroccio da deriva e pala (1.0.45, Day 2017), orziera sbandando (1.0.46, F4). **Congelata** con due impronte: `tests/fisica/impronta1b.js` (fisica in Node, riferimento in git, nel giro veloce) e le scene dell'1b in `collaudo_impronta.py` (riferimento sul PC di Ale).

**Regate dell'1b** (1.0.39-1.0.42): contatto vero fra gli scafi (anche nell'1a gli scafi non si compenetrano più dalla 1.0.42), chi cede con una funzione sola `chiCede` (regole 10, 11, 12, 13), semaforo rosso/verde facoltativo sullo scafo del giocatore. Torneo T1 (1.0.34): 4 regate a bastone, punteggio del regolamento, penalità +1 punto.

**Altro dalla 1.0.36:** schermata finale di regata sopra il mare; lezione 3 «Andature, mure e precedenze» e filetti con margine; vento e bussola in alto a destra; suggerimento del lasco misurato; timoniere con due braccia e due spalle.

## Come si lavora (regole che non cambiano)

- **Due fermate per ogni compito:** prima una proposta scritta con criteri misurabili e soglie dichiarate; poi, dato il via, si implementa e si misura. **Le soglie non si cambiano dopo aver visto i risultati**: un numero fuori fascia si riporta com'è.
- **Prima la barca, poi il resto:** in ogni livello si chiude la fisica, si congela con l'impronta, si pulisce il codice e i documenti, e solo dopo vengono avversari, lezioni e per ultimi i tempi delle medaglie.
- **Dove un numero dipende dalla barca si deriva dalla barca** (lunghezze di `BOAT.length`, manovre simulate con lo stesso `step()`), non si scrive a mano in metri o secondi.
- **Onestà sui contenuti:** ogni affermazione nautica va verificata su fonti scritte o video (`FONTI-PUBBLICHE.md`, `CONTENUTI-DA-VERIFICARE.md`); le semplificazioni si dichiarano. Niente marchi, niente titoli che sembrino ufficiali; «brevetto», mai «patente».
- **Un solo tentativo non basta:** molte prove con semi fissi, soglia scelta su un gruppo di semi e confermata su un altro mai guardato.

## Numeri che contano oggi

- **Barca dell'1a:** bolina 4,7 nodi a 45° con 10 nodi di vento, 6,0 al traverso, 4,1 in poppa; virata riuscita in circa 3 s da 3,9 nodi, fallita da fermi.
- **Barca dell'1b:** virata con la sola freccia 4,0 / 2,9 / 2,5 s con 6 / 10 / 14 nodi; scarroccio di bolina 2,3-3,2°, VMG da −0,5 a −3% rispetto a prima.
- **Regate dell'1b:** 2,4 contatti a regata nei salti di vento; torneo col pilota 0,95 penalità a regata, piazzamento medio 2,7.
- **Partenze degli avversari (1a):** partenze con almeno un richiamo 3,8-6,7%, ritardo mediano al via 0,9-2,2 s.

## Aperto

1. **Limiti congelati con la barca dell'1b** (`FISICA-E-TARATURE.md`): Maiusc in virata non frena più della freccia; con 20 nodi fissi dopo la raddrizzata non riparte; centro velico più basso del vero (2,0 m contro circa 2,6); lo scafo sbandato non orza da solo; scia della deriva sulla pala a zero; tre criteri della 1.0.46 fuori di poco; `timone2.js` C1 e C3 fuori come da sempre.
2. **Limiti dell'1a:** bolina dal 9 al 15% più lenta delle fonti con poco vento; la VMG di `bolina.js` non conta lo scarroccio (circa +3%, dichiarato).
3. **Collaudi:** `collaudo_partenze.py` criterio (1) oscilla fra OK e FALLITO per 1-3 partenze (rumore, soglie non toccate: da guardare con Ale); `collaudo_virate2.py` avversari oltre la bolina + 15° nel 16% delle virate (soglia 5%); `collaudo_timone2.py` a volte fallisce di un fotogramma con molti collaudi in parallelo.
4. **Prove giocando di Ale:** torneo dell'1b, raddrizzata di 10 s, distacchi, barca che balla, retromarcia con 15-20 nodi. Nelle regate dell'1a, all'arrivo, il pannello sfora di 48 px (1a congelata: da decidere). Tornando al menu a metà regata del torneo, la regata si ricorre da capo.
5. **Semplificazioni:** la massa non entra nella resistenza dello scafo; la linea di partenza è sempre perpendicolare al vento medio.

## Prossimo lavoro

Ordine in `ROADMAP.md`.

1. **Pulizia** (in corso, `PROPOSTA-PULIZIA-1B.md`): proposte finite in `archivio/`, nomi dei livelli nei documenti, `STATO.md`; poi la 1.0.47 con «1a» / «1b» nelle impostazioni e nel menu e tre collaudi nel giro lungo.
2. **Avversari con la barca dell'1b** (partenze, virate, boe) su molte regate.
3. **Regole 15 e 16 e il giallo del semaforo** (`PROPOSTA-REGOLE-PRECEDENZA-1B.md`, finestra T = 5,2 s misurata, soglia G da decidere), poi 17, 23 e 18, «contatto serio».
4. **Tornei dell'1b, tappa T2** (triangolo, `PROPOSTA-TORNEI-1B.md`), lezioni brevi e menu dell'1b.
5. **La regata come fonte**, solo nei tornei della parte «b» (`PROPOSTA-REGATA-COME-FONTE.md` §9), poi i tempi delle medaglie.
6. **Livello 2** (il regolamento: segnali, precedenze, penalità a giri; `PROPOSTA-SEGNALI-PARTENZA.md` è la fermata 1 da rivedere).
