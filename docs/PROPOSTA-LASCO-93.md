# Proposta: al lasco lascare un poco non deve rallentare (voce 93; fermata 1, 27 novembre 2026, Opus; gioco invariato)

**Da dove nasce:** marcatore M1 di Ale nella regata del 27 nov alle 00:58 (oss. 145): «mi dice di lascare ma vado più forte se cazzo».

## 1. Cosa fa la barca (motore della 1.3.63, banco in node)

A 134° dal vento con 14 nodi, partendo da 6,3 nodi, velocità dopo 30 s per scotta: 15% 6,27; 25% 6,23; 40% 6,09; **60% 5,87**; 80% 6,44; 100% 7,27 nodi. Lascando a piccoli passi da una vela troppo cazzata la barca rallenta fino a metà corsa: il suggerimento «lasca» è giusto sul punto d'arrivo ma chi lo segue un poco vede il contrario. **C'era già nella barca vecchia** (1.3.58: 5,68 → 5,48 → 6,52).

## 2. La causa (letta nel codice e misurata)

Oltre 60° di vento apparente la vela usa le curve vecchie `CL` e `CD` (`js/motore.js`) e, da 60° di incidenza, una resistenza che sale verso `cdn` = 1,32. La forza perpendicolare alla vela, CN = CL·cos α + CD·sen α:

| incidenza | 20° | 30° | 40° | 50° | 55° | 60° | 70° | 85° |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CN del gioco | 1,22 | 1,06 | 0,96 | **0,92** | **0,92** | 0,97 | 1,14 | 1,33 |

Con vento apparente a 110° la spinta in avanti scende da 1,22 (20°) a **0,74** (55-60°) e risale a 0,91 (90°). La buca fra 45° e 65° viene dal raccordo fra la curva di portanza (che cala fino a 0,55) e la resistenza da piastra che arriva solo da 60°.

**Cosa dicono le misure su piastre e vele investite di traverso** (da leggere e citare prima del codice): per una piastra piana il coefficiente normale dopo lo stallo resta circa fra 1,1 e 1,3 da 40° a 90° (Hoerner, *Fluid-Dynamic Drag* e *Fluid-Dynamic Lift*; Flachsbart 1932, riportato da Hoerner); per le vele di poppa le misure in galleria di Magnander (F120, già usate per la poppa della barca M) vanno nello stesso senso. **I numeri esatti non sono ancora letti:** prima di toccare il motore vanno trovati e messi in `FONTI-PUBBLICHE.md`.

## 3. Proposta (modello più semplice plausibile)

Fra lo stallo e 90° di incidenza la forza normale non scende sotto quella misurata per una piastra: **CN(α) = max(CN del gioco, CN della piastra)**, con la curva della piastra presa dalla fonte. Solo per il vento apparente oltre 60° (dove oggi si usano le curve vecchie); la bolina e la tabella ORC non cambiano.

Costanti nuove: nessuna inventata, se la curva della piastra viene da una fonte; altrimenti un CN costante (ipotesi dichiarata, per esempio 1,15) che si sceglie **prima** di misurare.

## 4. Criteri (soglie nostre, scritte prima di misurare)

- **L1, la buca sparisce:** con 10 e 14 nodi a 100°, 120°, 134° e 150°, partendo da scotta 0,1, la velocità a regime non scende di più dell'1% passando da una scotta alla successiva (passi di 0,1) finché non si arriva alla scotta migliore.
- **L2, la velocità migliore cambia poco:** polare a 90°-180° entro ±3% (la migliore regolazione è già oltre la buca); bolina (fino a 60°) identica.
- **L3, i suggerimenti:** a 134° con 14 nodi e scotta al 15%, «lasca» porta più velocità già al primo passo di scotta (0,25).
- **L4, il resto non peggiora:** medaglie, lezioni col pilota (3.3, 3.4 lasco e gran lasco, 6.3), raffiche e strambate; `rotta-dati.js` rigenerato e riportato.

## 5. Rischi

- Cambio della barca (lista intera): tabella delle velocità, medaglie, rivali di poppa.
- I rivali al lasco regolano con `ai.trim` intorno alla scotta giusta: non dovrebbero accorgersene, ma va misurato.

## 6. Cosa serve da Ale

Il via a cercare la fonte (Hoerner o una misura su piastra libera) e poi alla correzione. Senza fonte: scegliere se accettare un CN costante come ipotesi dichiarata.

## 7. Fonti trovate il 27 nov (ancora da leggere per intero)

- ESDU 70015 (portanza e resistenza di piastre piane per allungamento e incidenza), con le misure di Fail, Lawford e Eyre e di Winter (fino a 60°); Holmes e altri per la piastra quadrata. Citate in *Energies* 8 (2015) 2438: https://www.scribd.com/document/445858219/energies-08-02438-pdf
- Piastra piana in canale ad acqua da 0° a 110°, forza normale e tangenziale misurate: https://arxiv.org/pdf/2302.09602
- Piastra quadrata, Re 210 000, tutto il campo dopo lo stallo (e la nota che l'1,17 della piastra quadrata di traverso è il 9% sopra un'altra misura): https://arxiv.org/pdf/2506.18719
- NACA TN 3361: resistenza vicino a 2,0 a 90° per allungamento infinito (https://ntrs.nasa.gov/api/citations/19930084501/downloads/19930084501.pdf). **L'allungamento conta molto** (circa 1,2 per una piastra quadrata, 2,0 per una infinita): per la vela (allungamento circa 2-3) il valore va scelto con la fonte, non a occhio.
