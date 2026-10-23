# Proposta: scarroccio della barca dell'1b (Day 2017, eq. 11-12)

Stato: **fatta, versione 1.0.45** (23 ottobre 2026; scelta 1 di Ale, «vai con la 1, Day»). Esito in fondo. Punto 1 dell'ordine deciso da Ale prima del congelamento (`PROPOSTA-PALA-DERIVA-1B.md`, in fondo).

## Cosa fa oggi il motore [codice, `js/motore.js`, `step()`]
Velocità laterale cercata: `side / (foilK·(u² + 0,4) + 60)`, con `foilK` 520, in comune fra 1a e 1b. Non viene da una fonte e ha la forma sbagliata: lo scarroccio cala con il cubo della velocità invece che con il quadrato. Con 1,5 m/s dà quasi lo stesso di Day, con 2,4 m/s (bolina con 10 nodi) circa 1,6 volte meno.

## Modello proposto (solo barca dell'1b, `S.lv === 2`)
Day 2017, eq. 11-12 (F17), barca dritta: la deriva e la pala reggono la spinta laterale come due ali, `side = ½·ρ·K·u²·λ`, quindi velocità laterale `side / (½·ρ·K·u)`.
- `K` = somma di pendenza della portanza × aumento per lo scafo × area, con le misure di F37: deriva 1,176 m², pala 0,527 m² (acqua sulla pala al 90%, F17). `½·ρ·K` = 873 N·s/m². **Non è una taratura**: viene tutto dalle misure.
- **A barca ferma** la formula darebbe scarroccio infinito: al posto di `u` uso `√(u² + u0²)`, con `u0` = 0,307 m/s **ricavato** perché da ferma la barca scarrocci come oggi (268 N·s/m). Ipotesi nostra, dichiarata.
- **Lasciato fuori, dichiarato:** la scia della deriva sulla pala (Day non dà il coefficiente `a0`: lo metto a zero, cioè lo scarroccio minimo del modello; con la sola deriva è il massimo); l'effetto dello sbandamento (`1 − 0,382·φ` e l'angolo di deriva dello scafo `λ0`: sbandamento di bolina 4,7-5°, provato, cambia 0,1°); l'acqua di traverso sulla pala nel timone (`rud2Alpha` non vede lo scarroccio).
- Costanti nuove: una, `DERIVA2 = { q: 873, u0: 0.307 }` nella sezione «BARCA DEL LIVELLO 2». L'1a non cambia.

## Misure in anteprima [banco fuori dal repository, motore cambiato solo in memoria]
Banco di `bolina.js` (60 s a prua fissa, scotta a passi di 0,02, angoli 32-70°), barca dell'1b, ma **VMG calcolata sulla rotta vera** (prua + scarroccio). Il banco non usa numeri casuali: un giro basta.

| | 5 nodi | 6 nodi | 10 nodi | 15 nodi |
|---|---|---|---|---|
| Scarroccio di bolina, oggi | 2,1° | 2,3° | 2,1° | 1,6° |
| Scarroccio di bolina, proposta | 2,3° | 2,5° | 3,3° | 3,0° |
| Scarroccio, sola deriva (estremo) | 3,3° | 3,6° | 4,7° | 4,7° |
| VMG di bolina oggi, nodi | 1,84 | 2,16 | 3,18 | 3,96 |
| VMG proposta (differenza) | 1,83 (−0,5%) | 2,12 (−1,9%) | 3,08 (−3,1%) | 3,83 (−3,3%) |
| Day fig. 8 / F24 (virate comprese) | | 2,65 / 3,0 | 3,6 / 3,2 | 3,8 / 3,8-4,0 |

Altri numeri della proposta con 10 nodi: scarroccio 2,2° a 60° e 1,1° al traverso (oggi 1,2° e 0,5°); velocità al traverso 5,98 nodi (oggi 6,01), in poppa a 135° uguale; angolo della VMG migliore uguale (44-47°). Da ferma al traverso: uguale (0,046-0,047 m/s).

**Cosa non torna, riportato com'è:**
- Con 15 nodi la VMG si avvicina a Day (da +4% a +1%); con 6 e 10 nodi si allontana (da −18% a −20% e da −12% a −14%): la bolina con poco vento, già lenta (limite dichiarato, `PROPOSTA-BOLINA.md` §11), peggiora ancora un po'.
- **Il metro di oggi non vede lo scarroccio:** `bolina.js` calcola la VMG con la sola prua (`u·cos`), e così i numeri del `PROPOSTA-BOLINA.md` (2,25 / 3,29 / 4,07): sulla rotta vera, oggi, sono 2,16 / 3,18 / 3,96. Il confronto con Day era quindi ottimista di circa il 3% già prima. L'1a è congelata: non lo cambio, lo scrivo nei documenti.
- La stima della proposta di pala e deriva (2,4 / 2,9 / 4,1°) non coincide con l'equilibrio misurato qui (2,5 / 3,3 / 3,0°): quella usava forze stimate, questa la barca che naviga. Vale questa.

## Criteri per la fermata 2 (attese nostre, scritte prima)
1. **Il motore ridà il banco:** scarroccio e VMG della riga «proposta» al decimo di grado e al centesimo di nodo (banco portato in `tests/fisica/scarroccio1b.js`).
2. **Costo in bolina:** VMG sulla rotta vera al massimo il 4% sotto quella di oggi con ogni vento 5-15 nodi.
3. **1a identica:** `polare.js`, `raffiche_e_virate.js`, `retromarcia.js`, `angolo_morto.js` carattere per carattere.
4. **Virata dell'1b:** criterio 1 della 1.0.43 su tutti i venti 6-16 nodi (`virata1b.js`).
5. **Avversari dell'1b** (`collaudo_torneo.py --veloce`, semi fissi, quanti lo dico in fermata 2): nessun aumento di boe mancate e ritiri; tempo medio di regata del pilota riportato, atteso entro +4%.
6. Riportati senza soglia: `timone2.js`, `salti2.js`, `boma2.js`, `collaudo_semaforo.py`, `collaudo_contatto_vero.py`; lo scarroccio nel pannello (oggi «2°», diventerà «3°» di bolina).

## Rischi
- Avversari che puntano le boe con la prua: con più scarroccio possono arrivare sotto la boa e doverla riprendere (criterio 5).
- `u0` è un'ipotesi: conta solo sotto 1 m/s (partenze, barca piantata); da ferma la barca resta come oggi per costruzione.
- La scia della deriva sulla pala è scelta a zero: se fosse grande lo scarroccio sarebbe fino a 1,4° in più (riga «sola deriva»). La riprendo con la barca orziera (punto 2), dove la pala porta carico.

## Seconda ricerca (23 ottobre 2026, chiesta da Ale): una misura in vasca
- **F35** (Masuyama, 470, *Journal of Sailing Technology* 2020, già in `fonti-pdf/`), fig. 12 e 14: **forza laterale misurata** di scafo + deriva + pala (modello in scala 1:5) in funzione dello scarroccio. Letta a occhio: `Y'` circa 0,0075 per grado (0,076 a 10°), con `Y' = Y / (½·ρ·V²·L·D)`, `L` 4,4 m, `D` 1,08 m. Cioè `K` misurato 2,04 m².
- Lo stesso conto di Day, fatto per il 470 (deriva dalle sue regole di classe, `470_CR_2025`, corda circa 0,38 m, circa 0,93 m sotto lo scafo, stima; pala 0,675 × 0,25 m, F4), dà 2,57 m². **La misura è il 79% di Day**: Day senza scia sovrastima la forza laterale di circa il 20%.
- Riportata alla nostra barca: `K` 1,35 m² invece di 1,70.
- **Web:** nessuna misura di scarroccio di una deriva trovata. Solo indicazioni generiche senza metodo: «la maggior parte delle barche da regata, di bolina con vento medio, scarroccia 3-5°» ([SailZing](https://sailzing.com/understand-leeway-to-improve-upwind-performance/)); lo scarroccio cresce con molto e con pochissimo vento ([Starpath](https://www.starpath.com/resources2/Navigation_with_Leeway.pdf)). Da non usare come fonte, solo come conferma dell'ordine di grandezza.

| Banco, bolina | 5 nodi | 6 nodi | 10 nodi | 15 nodi |
|---|---|---|---|---|
| Scarroccio: oggi / Day / 470 scalato | 2,1 / 2,3 / 3,1° | 2,3 / 2,4 / 3,0° | 2,1 / 3,2 / 4,0° | 1,6 / 2,9 / 4,0° |
| VMG: oggi / Day / 470 scalato | 1,84 / 1,83 / 1,80 | 2,16 / 2,13 / 2,09 | 3,18 / 3,09 / 3,02 | 3,96 / 3,84 / 3,76 |
| Perdita col 470 scalato | −2,2% | −3,2% | −5,0% | −5,1% |

(Le righe «Day» qui sono senza il fattore dello sbandamento, per confrontarle con la misura a barca dritta; cambiano di 0,1° rispetto alla tabella sopra.)

**Cosa pesa sulla misura:** il modello in scala 1:5 lavora con acqua «più viscosa» in proporzione e di solito porta meno di una barca vera, quindi spinge verso più scarroccio; la scia della deriva sulla pala invece c'è davvero, e la versione di Day sopra la mette a zero. La verità sta quasi certamente **fra le due righe: 3,2-4,0° con 10 nodi**. Pendenza letta a occhio: ±10%.

**Attenzione al criterio 2:** era scritto prima di questa ricerca, per il modello di Day (perdita al massimo del 4%). Con il 470 scalato la perdita è del 5% con 10 e 15 nodi: **fuori**. Non cambio la soglia.

## Decisione per Ale
1. **Day, deriva più pala** (`K` 1,70): tutto dalle formule, perdita 2-3%, criterio 2 dentro. Lo scarroccio più piccolo plausibile.
2. **470 misurato, scalato** (`K` 1,35): l'unica misura, comprende la scia; perdita fino al 5%, criterio 2 fuori come scritto. Lo scarroccio più grande plausibile.
3. Lasciare lo scarroccio di oggi (circa la metà) come limite dichiarato e passare alla barca orziera.

Consiglio: **1**, dichiarando la fascia 3,2-4,0° come incertezza. Pesa di meno sulla bolina con poco vento, che è già il punto debole, e resta dentro i criteri scritti prima. La 2 diventa la sensibilità da riportare in fermata 2.

## Fermata 2 (23 ottobre 2026): versione 1.0.45
Ale: «vai con la 1, Day». Modello come scritto sopra, **senza** il fattore dello sbandamento (lasciato fuori nel paragrafo «Modello proposto»); per questo il confronto del criterio 1 è con la riga «Day» della seconda tabella, non con la riga «proposta» della prima, che lo comprendeva (0,1° di differenza). Lo dichiaro.

| Criterio | Esito |
|---|---|
| 1. Il motore ridà il banco | **ok**: 2,3 / 2,4 / 3,2 / 2,9°, VMG 1,83 / 2,13 / 3,09 / 3,84 (`tests/fisica/scarroccio1b.js`) |
| 2. VMG al massimo −4% | **ok**: −0,5 / −1,4 / −2,8 / −3,0% con 5 / 6 / 10 / 15 nodi |
| 3. 1a identica | **ok**: `polare.js`, `raffiche_e_virate.js`, `retromarcia.js`, `angolo_morto.js` carattere per carattere |
| 4. Virata dell'1b | **ok** su tutti i venti 6-16 nodi (`virata1b.js`) |
| 5. Avversari dell'1b | **ok**: 20 tornei, semi 1-20, 80 regate (`tests/misura_scarroccio.py`): non arrivate 2 → 0, boe sbagliate 4 → 3; tempo medio pilota +0,7%, avversari +1,0% (atteso entro +4%) |
| 6. Senza soglia | `timone2.js` C5 a 16 nodi 34 → 35% (dentro), resto come prima; `salti2.js` e `boma2.js` nelle soglie; nel browser torneo (veloce e giocatore), semaforo, contatto vero, versione OK |
