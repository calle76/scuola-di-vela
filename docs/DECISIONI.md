# Registro delle decisioni

Iniziato il 25 ottobre 2026. Una riga per ogni decisione presa, con la data e il **costo se la si cambia**. Prima di aprire un livello nuovo si rileggono le righe ad **alto** costo. Il metodo è in `METODO.md` §3.

Costo di cambiamento:
- **alto:** cambiarla tocca fisica, lezioni, collaudi o abitudini di chi gioca;
- **medio:** tocca più parti, ma senza rifare il lavoro fatto;
- **basso:** si cambia in una versione piccola.

**I costi della prima stesura sono una stima di Claude (25 ottobre 2026), da confermare da Ale riga per riga.** Dove questo registro e un altro documento dicono cose diverse, vale l'altro documento finché la riga qui non è corretta.

## Piattaforma

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| Gioco nel browser: `index.html` più `js/`, script classici e non moduli, si apre con un doppio clic | 16 ott (1.0.3) | alto | Tutti i collaudi e la pubblicazione ci si appoggiano | `archivio/PROPOSTA-DIVISIONE-CODICE.md` |
| Solo computer con tastiera | inizio | alto | Comandi, pannello e lezioni sono pensati per la tastiera | `PROGETTO.md` |
| Pubblicazione su GitHub Pages da `main` (attiva, verificata da Ale il 26 ott: https://calle76.github.io/scuola-di-vela/) | set | medio | Cambia solo come arriva il gioco a chi gioca | `README.md` |
| Pannello senza eccedenze a 1360×650 | ott | medio | Ogni testo nuovo va misurato | `CLAUDE.md` |

## Fisica

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| Motore cinematico didattico, non un previsore; un effetto entra solo se si sente guidando e ha una fonte | inizio | alto | È la base di tutto il resto | `PROGETTO.md` |
| Si tara la barca condotta bene; la differenza la fa chi guida | 16 ott | alto | Fasce, avversari e lezioni dipendono dalla velocità | `ROADMAP.md` |
| Prima la barca, poi avversari, lezioni e per ultimi i tempi delle medaglie | 17 ott | — (regola di metodo) | — | `ROADMAP.md`, `METODO.md` |
| Barca dell'1a congelata | 17-22 ott | alto | Impronta, lezioni, prove, esame | `STATO.md` |
| Barca dell'1b congelata | 23 ott | alto | Impronte, avversari, torneo | `archivio/PROPOSTA-CONGELAMENTO-1B.md` |
| I numeri che dipendono dalla barca si derivano dalla barca, non si scrivono a mano | ott | medio | Sostituirli dopo vuol dire trovarli tutti | `STATO.md` |
| Valori numerici misurati da pubblicazioni scientifiche, citati, si possono usare nel motore | 16 ott | basso | — | `CLAUDE.md` |

## Comandi

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| Barra su ← →; comando principale di ogni ruolo su W S; secondo comando su E D; Q vista; A raddrizza; Z spingi il boma; R libero | 7 e 17 ott | alto | Abitudini di chi gioca, testi delle lezioni, domande, collaudi da tastiera | `VISIONE-LIVELLI-E-CARRIERA.md` §12 |
| Dal livello 2 in poi i tasti non si stravolgono a ogni livello | 6 ott | alto | — | memoria del progetto |
| Zoom sui tasti 1 e 2, senza pulsanti sul mare | 26 ott (1.0.48) | basso | — | `CHANGELOG.md` |
| Si lavora su `main`, senza rami; tag solo all'uscita di un livello | 26 ott | basso | — | `METODO.md` §6 |

## Livelli e ruoli

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| Ogni livello ha una parte «a» (teoria) e una «b» (pratica); 1a basi, 1b barca completa, 2 regolamento con la stessa barca, 3 fiocco, 4 gennaker, 5 equipaggio da tre e tattica | 19 ott | alto | Documenti, menu, carriera, ordine dei lavori | `VISIONE-LIVELLI-E-CARRIERA.md` §2 |
| Nell'1b le regole si fermano alle 10-13; copertura del vento e protesta passano al livello 2 | 23 ott | medio | Avversari e domande dell'1b | `STATO.md` |
| Avversari dell'1b: chi deve cedere cede, chi ha la precedenza tiene la rotta (piantate 36 → 2, penalità 73 → 97) | 26 ott (1.0.49) | medio | Guida degli avversari e pilota dei collaudi | `PROPOSTA-AVVERSARI-1B.md` |
| Avversari dell'1a lasciati come sono: meno bravi, come chi comincia | 26 ott | basso | — | `PROPOSTA-AVVERSARI-1B.md` §10 |
| Torneo: uscire a metà regata (menu o chiusura del browser, anche per sbaglio) vale come «Ritirati» per quella regata; il torneo continua. Fatto nella 1.0.50 (prima la regata si rifaceva da capo, scelta della 1.0.34); conta dal clic su «Corri la regata» | 26 ott | basso | Salvataggio del torneo e `collaudo_torneo.py` C3 | `STATO.md` «Aperto» 4 |
| Nessun aiuto a schermo per i salti di vento: si leggono dalla prua nel pannello | 26 ott | basso | — | `archivio/PROPOSTA-SALTI-VENTO.md` |
| Si guida sempre un solo ruolo; nel torneo il ruolo resta lo stesso fino alla fine | ott | alto | Equipaggio del computer, meriti, tornei | `VISIONE-LIVELLI-E-CARRIERA.md` |
| Nessun numero fisso di novità per livello | 4 ott | basso | — | `VISIONE-LIVELLI-E-CARRIERA.md` §1 |
| Replay e «regata come fonte» solo nella parte «b» dei livelli | 20 ott | medio | Registrazione e istantanee | `PROPOSTA-REGATA-COME-FONTE.md` §9.7 |
| Vela di portanza del livello 4: gennaker asimmetrico [da verificare su fonti] | ott | medio | Fisica del livello 4, non ancora scritta | memoria del progetto |

## Carriera, meriti, salvataggi

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| Bivio gioco libero / carriera, con salvataggi e fantasmi separati | 14 ott (0.22) | alto | Formato dei salvataggi e tutti i punti che scrivono | `archivio/PROPOSTA-ESAME-E-BREVETTO.md` §11 |
| Fantasmi e record sono prove di gioco: si azzerano quando cambiano regole o tempi, senza migrazioni | 7 ott | basso | **Abbassa il costo** delle decisioni sui salvataggi finché il gioco è in prova | memoria del progetto |
| Gioco libero tutto sbloccato e navigabile fra i livelli; in carriera un livello si apre coi brevetti | 17 ott | medio | Menu e carriera | `VISIONE-LIVELLI-E-CARRIERA.md` §8 |
| Quattro aree di merito (abilità, competizione, conoscenza, esperienza) con minimi; esame obbligatorio; poi brevetto | ott | medio | Libretto, esame, attestato | `VISIONE-LIVELLI-E-CARRIERA.md` |
| Numeri dei meriti provvisori, da tarare giocando | 9 ott | basso | — | `PIANO-GENERALE.md` |
| Classifica (punteggio minimo del regolamento) separata dai meriti | 14 ott | medio | Torneo e libretto | `archivio/PROPOSTA-ESAME-E-BREVETTO.md` |
| Esame non superato: ripasso completo delle lezioni sbagliate, con qualsiasi punteggio, poi si riprova | 14 ott (0.24) | basso | — | `archivio/PROPOSTA-ESAME-E-BREVETTO.md` |
| Gli aiuti accesi o spenti valgono uguale per i meriti | 14 ott | basso | — | `archivio/PROPOSTA-ESAME-E-BREVETTO.md` |

## Contenuti e confini legali

| Decisione | Data | Costo | Perché costa | Dove |
| --- | --- | --- | --- | --- |
| «Brevetto», mai «patente»; sempre «nessun valore legale»; niente marchi né titoli che sembrino ufficiali | inizio | alto | Rischio legale | `PROGETTO.md` |
| Nessuna persona esperta: le affermazioni nautiche si verificano su fonti scritte e video | 13 ott | medio | Ogni contenuto nuovo ha bisogno di fonti | `CLAUDE.md` |
| Le spiegazioni lunghe vanno nel manuale, non a video | 7 ott | basso | — | memoria del progetto |
| I PDF raccolti in `fonti-pdf/` non diventano domande di quiz o d'esame | 12 ott | basso | — | `SCHEDATURA-FONTI.md` |

## Decisioni aperte ad alto costo

Da prendere **prima** di cominciare il livello a cui servono.

| Decisione | Serve a | Dove |
| --- | --- | --- |
| Come si danno gli ordini all'equipaggio e con quanto preavviso | Livello 3 | `VISIONE-LIVELLI-E-CARRIERA.md` §11 |
| Quanti ruoli servono per il brevetto dal livello 3 | Livello 3 | idem |
| Come entra il fiocco a farfalla | Livello 3 | idem |
| Barche vere (per categoria) dei livelli 4 e oltre | Livello 4 | idem |
| Gioco a più persone: quale gradino e se sì | Prima di toccare registrazione e istantanee | `PROPOSTA-REGATA-COME-FONTE.md` §8 |
