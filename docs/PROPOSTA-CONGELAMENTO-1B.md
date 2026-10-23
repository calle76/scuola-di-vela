# Proposta: congelare la barca dell'1b

Stato: **fatto** (23 ottobre 2026, Ale: «ok 1 + 2»). **La barca dell'1b è congelata.** Esito in fondo. Punto 3 dell'ordine deciso da Ale (`PROPOSTA-PALA-DERIVA-1B.md`, in fondo), dopo scarroccio (1.0.45), barca orziera (1.0.46) e centro velico (resta 2,0 m).

## Cosa vuol dire «congelata»
Come l'1a: da qui in poi la barca dell'1b (tutto quello che dipende da `S.lv === 2` in `step()`, timone, boma spinto, raddrizzata, salti di vento) **cambia solo per difetti trovati giocando**, con la sua fermata 1. Serve a 1b, 2a e 2b: avversari, tornei e regole si costruiscono sopra una barca che non si muove più.

## Oggi cosa la protegge
- `collaudo_impronta.py` fotografa **solo l'1a** (lezioni, prove, regate 1 e 2, menu): la «Regata nei salti di vento», il torneo e la barca dell'1b nel gioco libero non ci sono. Un cambio all'1b oggi non lo vede nessuno.
- I banchi in Node dell'1b (`virata1b.js`, `scarroccio1b.js`, `orziera1b.js`, `timone2.js`, `boma2.js`, `salti2.js`) stampano numeri arrotondati e si confrontano a mano.

## Proposta: due fotografie, la seconda dentro l'impronta che c'è già
1. **Impronta della fisica in Node** (`tests/fisica/impronta1b.js`, nuovo, pochi secondi). Guida `step()` con la barca dell'1b in un elenco fisso di manovre (bolina, traverso e poppa con 6 / 10 / 16 nodi, virata e strambata con freccia e Maiusc, raffica senza reagire e lascando, boma spinto, barca ferma, salti di vento oscillanti e persistenti con un seme) e fa una somma di controllo di tutti gli stati **a precisione piena**, passo per passo. Il riferimento (un file di poche righe) **entra in git**: non dipende dal browser, lo controllo io a ogni modifica in un secondo, e Ale non deve rigenerare niente.
2. **Impronta del gioco estesa all'1b** (`collaudo_impronta.py`, scene nuove): la «Regata nei salti di vento» con principianti ed esperti, una regata del torneo, il gioco libero con la barca dell'1b guidato con barra, Maiusc, Z e A (raddrizzata). Le scene dell'1a restano quelle di oggi, con gli stessi nomi. Il riferimento sta sul PC di Ale come oggi (dipende dal browser): **lo rigenera una volta**, dopo il commit.

Niente collaudo nuovo nel browser: le scene si aggiungono all'impronta che esiste già.

## Criteri (attese nostre)
1. **Misura davvero:** in ogni scena nuova la barca si muove; nelle regate nuove ci sono arrivi, almeno un contatto e almeno una virata; nell'impronta in Node almeno una scuffia, uno stallo della pala e un boma spinto. Il collaudo lo dice con dei numeri, non solo «uguale».
2. **Contro-prova:** con una costante dell'1b cambiata apposta in una copia (`RUD2.hullKq` 400 → 401) tutte e due le impronte danno FALLITO; con una costante solo dell'1a cambiata (`BOAT.foilK` 520 → 521) l'impronta in Node dell'1b resta identica.
3. **Ripetibile:** due giri di fila sullo stesso codice danno la stessa impronta (in Node e nel browser).
4. **1a invariata:** le scene di oggi dell'impronta restano identiche a una copia della 1.0.46.

## Limiti che si congelano con la barca (scritti in `FISICA-E-TARATURE.md` e nello `STATO.md`)
Maiusc in virata non frena più della freccia; con 20 nodi fissi dopo la raddrizzata non riparte; centro velico più basso del vero (niente svergolamento della vela); lo scafo sbandato non orza da solo; scia della deriva sulla pala a zero; i tre criteri fuori di poco della 1.0.46; `timone2.js` C1 e C3 fuori come da sempre (§8 di `PROPOSTA-STALLO-TIMONE.md`).

## Cosa costa in tempo
Io lancio: l'impronta in Node (secondi), l'impronta nel browser due volte (riferimento e confronto) più la contro-prova. Ale: **solo** `collaudo_impronta.py riferimento` sul suo PC dopo il push. Il giro completo `--veloce` lo farebbe dopo la pulizia del codice, che è il passo seguente (è proprio quello a cui serve l'impronta).

## Rischi
- La «Regata nei salti di vento» e il torneo sono lunghe (fino a 900 s di regata): l'impronta nel browser si allunga. Se pesa troppo, la regata del torneo si ferma a 400 s come le regate dell'1a.
- Una somma di controllo a precisione piena può cambiare con una versione diversa di Node se cambiano `Math.sin` e simili. Lo segnalo nel collaudo: se capita, si rigenera dicendolo, dopo aver visto che i numeri arrotondati dei banchi sono uguali.

## Decisione per Ale
Va bene così (1 + 2)? In alternativa, più leggero: solo la 1 (Node, in git), e l'impronta del browser estesa più avanti con la pulizia.

## Fermata 2 (23 ottobre 2026)
Nessun cambio al gioco (`js/` identico alla 1.0.46).
1. **`tests/fisica/impronta1b.js`** (nuovo, in `lancia_tutti.sh` anche con `--veloce`) e il riferimento `impronta1b.txt` in git: 25 corse, 51 802 passi in meno di un secondo; misura stallo della pala (336 passi), boma spinto (360), una scuffia, 6 cambi di mure (criterio 1, ok). Contro-prova: `RUD2.hullKq` 401 → 23 corse diverse su 25 (le due uguali stanno sotto la velocità del timone dell'1b), FALLITO; `BOAT.foilK` 521 (solo 1a) → identica (criterio 2, ok). Due giri uguali (criterio 3, ok).
2. **`collaudo_impronta.py`**: 4 scene nuove (regata nei salti principianti ed esperti, torneo regata 1, gioco libero con l'1b); 67 scene. Misurato nell'1b: 3 regate, 4 arrivi entro 400 s, 36 virate; gioco libero: barca dell'1b, boma spinto, scuffia e raddrizzata con A (criterio 1, ok; lo stallo della pala non capita negli istanti fotografati: lo vede l'impronta in Node). Contro-prova su copie: `hullKq` 401 → diverse esattamente le 4 scene dell'1b; `foilK` 521 → diverse solo lezioni, prove e regate dell'1a, le 4 scene dell'1b identiche (criterio 2, ok). Due giri uguali (criterio 3, ok). Le scene dell'1a sono quelle di prima e `js/` non è cambiato (criterio 4, ok).
3. **Il riferimento dell'impronta nel browser** l'ho riscritto qui (`tests/output/impronta/riferimento.json`, fuori da git) per le prove: Ale lo rigenera sul codice di questo commit con `collaudo_impronta.py riferimento`.

### Limiti che si congelano con la barca
Maiusc in virata non frena più della freccia (`PROPOSTA-STALLO-TIMONE.md` §10); con 20 nodi fissi dopo la raddrizzata non riparte; centro velico più basso del vero, niente svergolamento della vela (`PROPOSTA-CENTRO-VELICO-1B.md`); lo scafo sbandato non orza da solo e la scia della deriva sulla pala è a zero (`PROPOSTA-ORZIERA-1B.md`, `PROPOSTA-SCARROCCIO-1B.md`); 1.0.46 fuori di poco su tre criteri (barra al centro 1,06 °/s con 14 nodi al traverso, virata con 16 nodi minima 34%, un arrivo mancato del pilota su 80); `timone2.js` C1 e C3 fuori come da sempre; bolina con poco vento più lenta delle fonti (eredità dell'1a); il peso del timoniere non aiuta a girare.

**Da qui la barca dell'1b cambia solo per difetti trovati giocando**, con la sua fermata 1, e allora si rigenera `impronta1b.txt` dicendolo.
