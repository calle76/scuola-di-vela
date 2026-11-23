# Proposta: lo storico duraturo dei rivali, con qualche conseguenza

*Fermata 1, 21 novembre 2026, bozza di partenza (Sonnet) da rifinire con Opus in una sessione nuova. Richiesta di Ale (21 nov): «sarebbe bello uno storico duraturo e qualche conseguenza»; prima domanda: «quanti scontri con te». Nessun codice finché non arriva il via. Riprende la domanda 9 di `PROPOSTA-RIVALI-E-SPONSOR.md` («memoria solo mostrata o anche attiva?») e la scheda dei rivali della 1.2.30 (`PROPOSTA-SCHEDA-RIVALI.md`).*

## Cosa c'è oggi

- **La scheda di ogni rivale vive solo dentro il torneo** e si perde alla fine (nessun salvataggio fra tornei): per ogni regata arrivo, partenza (davanti/dietro/fuori linea), boa 1, contatti con te (colpa tua / sua).
- I rivali sono 3, gli stessi per tutte le regate del torneo, con un carattere dichiarato (prudente, normale, aggressivo). Nella carriera/stagione ci sono nomi veri del circuito, ma anche lì il rapporto con te non si ricorda.
- La guida dei rivali **non cambia con quello che è successo**: la scheda è «solo mostrata» (deciso il 12 novembre).
- Il salvataggio di gioco sta in `localStorage` (`progress`, record, fantasmi) e si può azzerare senza migrazioni (decisione del 7 ottobre).

## Il modello più semplice (due passi separati)

### Passo 1 — lo storico, solo mostrato (nessuna conseguenza)

- Per ogni rivale **con nome** (il colore non basta: serve l'identità), un record che dura fra tornei e stagioni: regate corse contro di te, quante volte è arrivato davanti/dietro, **contatti con te** (quanti, di chi la colpa), partenze fuori linea, scuffie, penalità.
- Mostrato nella scheda del rivale («Con te: 7 regate, 4 volte davanti, 3 contatti: 2 colpa sua, 1 colpa tua») e in fondo al torneo.
- Salvato in `progress.rivali[idRivale]`, con un contatore di versione; si azzera se manca. Nessun numero a caso consumato: collaudo «guida invariata» come per la scheda.
- **Cosa serve da Ale:** vale per tutti i rivali o solo per quelli del circuito con i nomi veri? E l'amico che gioca in rete (stagione con un amico) entra nello storico?

### Passo 2 — le conseguenze (da decidere dopo aver visto il passo 1 in uso)

Tre conseguenze possibili, dalla più leggera, **da scegliere una alla volta** (consiglio solo la prima per cominciare):

| # | Conseguenza | Come si vede | Rischio |
| --- | --- | --- | --- |
| a | **Frase a inizio regata**, dal passo 1 («Verde ha avuto 3 contatti con te: tienila d'occhio»); la guida non cambia | solo testo, e il Coach lo può dire | nessuno sul gioco |
| b | **Cautela:** un rivale che ti ha toccato con colpa sua riprende a partire un poco più largo (o più cauto) nella regata dopo; mai oltre qualche metro | la scheda dice «Verde ti lascia più spazio»; si misura sul distacco alla partenza | sposta le regate a semi fissi (i collaudi vanno ricalibrati) |
| c | **Rivalità:** dopo 3 contatti il rivale diventa «nemesi» e ti marca (si piazza più spesso fra te e la boa) | scheda e Coach lo dicono | cambia davvero l'equilibrio: va misurato su molte regate, e potrebbe sembrare ingiusto |

Regola comune: **ogni cambio di comportamento si deve vedere e spiegare sulla scheda**, altrimenti sembra casuale.

## Costanti nuove (ipotesi nostre)

Nessuna nel passo 1. Nel passo 2: soglia «nemesi» 3 contatti, cautela di qualche metro (da misurare), memoria di 3 tornei (poi si scorda).

## Criteri (soglie nostre, dichiarate prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| R1 | Lo storico dice il vero | su 40 tornei a semi fissi, per ogni rivale le righe dello storico (regate, davanti/dietro, contatti, colpa) uguali al registro delle regate (`analizza_registro_torneo.py`); 0 righe diverse e almeno 500 confronti |
| R2 | Dura | chiusa e riaperta la pagina fra due tornei lo storico è identico; un salvataggio senza `progress.rivali` si apre con storico vuoto e 0 errori |
| R3 | Il passo 1 non cambia la regata | arrivi e tempi identici al bit con e senza storico, su 160 regate |
| R4 | Identità | lo stesso rivale in due tornei diversi (stesso nome) si somma; due rivali con lo stesso colore e nomi diversi no |
| R5 | Pannello | scheda e fine torneo a 1360x650 senza eccesso con 3 rivali e storico lungo |
| R6 | Come un giocatore | pagina senza `#collaudo`, due tornei di fila: lo storico cresce, 0 errori |
| R7 (solo passo 2 a) | La frase | compare solo se il numero di contatti nello storico è ≥ 2 e dice il numero giusto; 0 frasi sbagliate su 100 casi |

Il metro non deve dipendere dal gioco: R1 si ricalcola dal registro della regata e non dallo storico stesso; il collaudo stampa il numero di confronti.

## Rischi

- **Un fatto singolo sembra un carattere** (già visto per la scheda): frasi con conteggi, non etichette.
- **Salvataggi vecchi** si azzerano senza migrazione (principio del 7 ottobre).
- **Conseguenze che cambiano la regata** (b, c) toccano i collaudi a semi fissi: vanno proposte e misurate a parte.
- **Dati personali:** lo storico è solo locale al browser; nessun invio (vale per l'amico in rete: da definire, probabile che ognuno abbia il suo).

## Passi, dopo il via

1. Passo 1: struttura `progress.rivali`, raccolta dal registro del torneo, scheda e fine torneo; criteri R1-R6 (Chromium e Firefox). **Opus** per il modello dei dati e il passo 2.
2. Passo 2: una sola conseguenza (a), poi eventualmente b o c in una versione a parte.
3. Documenti, versione, `CHANGELOG.md`.

## Cosa è stato fatto (1.3.37, 21 novembre 2026): passo 1

Decisioni di Ale: l'identità del rivale è il nome (il colore non conta); nessuna conseguenza sulla guida per ora. Fatto da Sonnet, rivisto da Opus prima del commit. Rispetto alla bozza: i contatori sono nove (regate, davanti, dietro, partenza davanti/dietro, fuori linea, regate con contatti, colpa sua, colpa tua); **non** ci sono il contatore di versione, la riga «in fondo al torneo» (c'è solo nella scheda), le scuffie e le penalità dei rivali; l'amico della stagione non entra nello storico. Conta dalle regate corse dalla 1.3.37. Criteri R1-R6 in `tests/collaudo_storico_rivali.py` (R1 40 tornei; R1b casi costruiti; R7 della bozza, la frase a inizio regata, è del passo 2). Il passo 2 aspetta il via.

## Passo 2, fermata 1 (22 novembre 2026, Opus): decisione 1, la frase a inizio regata (a)

Si decide una cosa per volta; (b) e (c) solo dopo, in una versione a parte. Nessun codice finché non arriva il via.

**Cosa conta davvero il passo 1.** `st.cS` conta le **regate** in cui c'è stato almeno un contatto con colpa sua, non i contatti (due contatti nella stessa regata valgono 1). Quindi la soglia «≥ 2 contatti con colpa sua» diventa, con i dati che ci sono, **«in almeno 2 regate ti ha toccato con colpa sua»**, e la frase lo dice così. Conta solo dalle regate corse dalla 1.3.37 in poi, e comprende le regate già corse dello stesso torneo (lo storico si aggiorna a fine regata, in `torChiudi`).

**Proposta.**
- **Dove:** nel Coach durante la regata (il riquadro con volto e frase che c'è già dalla 1.3.28), volto «serio», commento normale (non forzato), col suo campanello e la sua riga «C» nel file della regata. Vale solo nelle regate di Deriva (torneo, tappe, finale) e si spegne con l'interruttore del Coach (principio 3). Alternativa scartata per ora: una riga nella finestra del torneo prima di «Corri la regata» (sempre visibile, ma è un'altra riga da far stare a 1360x650 e non si registra nel file).
- **Quando:** una volta per regata, nel conto alla rovescia a **−150 s** (la frase dello sponsor resta a −50 s: fra le due ci sono 100 s, più dei 30 s di pausa del Coach). Se il conto alla rovescia parte dopo −150, al primo istante utile.
- **Con quali numeri:** compare se un rivale in acqua ha `cS ≥ 2` (soglia di Ale). Se sono più d'uno, **uno solo**: quello con più regate «colpa sua»; a parità, il primo nell'ordine delle barche. Gli altri restano nella scheda.
- **Testo** (niente aggettivi col genere, niente giudizi; un conteggio, non un carattere): «Rossi, barca Verde: in 3 regate ti ha toccato con colpa sua. Tieni d'occhio la sua barca.»
- **Niente di nuovo nel salvataggio**; la guida non cambia e non si usano numeri a caso.

**Costanti nuove (ipotesi nostre):** `STO_SOGLIA = 2` (di Ale), `STO_T = −150` s.

**Criteri (soglie nostre, dichiarate prima):**

| # | Criterio | Soglia |
| --- | --- | --- |
| R7 | La frase dice il vero | lo storico si **ricalcola dal registro** (`tor.ris` dei tornei corsi nel collaudo, più quello costruito a mano), non da `progress.rivali`: la frase compare se e solo se il ricalcolo dà `cS ≥ 2`, con nome, barca e numero giusti. 0 sbagliate su almeno 100 casi con la frase **e** almeno 100 senza (controprova); il collaudo stampa i due conteggi |
| R7b | Una sola, al momento giusto | al più una frase dello storico per regata, fra −151 e −149 s (o al primo istante se il conto parte dopo); 0 casi fuori |
| R7c | Si spegne | col Coach spento 0 frasi su 20 regate |
| R3 | La regata non cambia | arrivi e tempi identici al bit con e senza frase, 20 regate a semi fissi |
| R5 | Riquadro | il nome più lungo dei rivali sta nel riquadro del Coach (330 px) senza uscire dal mare a 1360x650 |
| R6 | Come un giocatore | pagina senza `#collaudo`, storico costruito con 2 contatti: la frase compare, 0 errori |

Chromium e Firefox, uno per volta col freno. I casi «con frase» si costruiscono riempiendo lo storico prima del torneo (a semi fissi i contatti naturali in 2 regate sono rari); il collaudo dice quanti casi sono naturali e quanti costruiti.

**Rischi.** Un fatto contato su poche regate sembra un carattere (per questo il numero sta nella frase). Con il Coach spento la frase non c'è: chi lo spegne la vede solo nella scheda. Il nome più lungo dei rivali va controllato nel riquadro.

**Punti aperti del passo 1 (decisione 3, dopo):** contatore di versione del salvataggio; riga a fine torneo; scuffie e penalità dei rivali; amico in rete.

## Cosa è stato fatto (1.3.38, 22 novembre 2026): passo 2 a, la frase

Via di Ale: «prima la frase, nel Coach». Fatto come proposto sopra (Coach, −150 s, `cS ≥ 2`, uno solo). In più la frase dello sponsor riprova se il Coach è in pausa (prima andava persa). Criteri R7, R7b, R7c, R3, R5, R6 in `tests/collaudo_storico_frase.py`; numeri in `CHANGELOG.md` 1.3.38. Il collaudo è stato corretto dopo i primi giri senza toccare le soglie (dettagli nel CHANGELOG).

**Prossima decisione (2):** cautela (b) o nemesi (c), in una versione a parte. Ale il 22 nov ha proposto i versi: «se l'ho toccato io, lui mi schiva» (cautela al contrario rispetto alla bozza) e «se ha perso da me più volte, mi ostacola» (nemesi). Prima della proposta: fonti scritte o video su marcatura e copertura in regata.

## Passo 2, decisione 2: le fonti (23 novembre 2026, sera; Opus)

Le due idee di Ale del 22 novembre, confrontate con le fonti (`FONTI-PUBBLICHE.md` F115, F116):

- **«Nemesi»: se ha perso da me più volte, mi ostacola.** Il regolamento lo vieta così com'è. Secondo il Caso 78 di World Sailing (riportato in F115) ostacolare apposta un'altra barca in una regata di flotta è lecito **solo se serve alla propria classifica in quella manifestazione** e ha una ragionevole possibilità di riuscire; farlo per rivalsa, senza vantaggio proprio, rompe la regola 2 (correttezza). Un rivale che ti ostacola «perché ha perso da te» insegnerebbe una cosa sbagliata (principio 4).
- **La versione lecita esiste ed è una tattica vera:** la **marcatura** (coprire: restare fra l'avversario e la boa, virare quando vira lui, F116), usata contro un rivale di velocità simile che si deve battere. Non dipende dalla storia dei contatti ma dalla **classifica**: per esempio nell'ultima regata del torneo un rivale che ti sta appena davanti o dietro in classifica ti copre di bolina, se batterti gli serve.
- **«Cautela»: se l'ho toccato io, mi schiva.** Nessuna fonte trovata (ricerche del 23 nov su regolamento, sportività e comportamento dopo un contatto): è un'idea plausibile ma non documentata. Se si fa, va dichiarata come invenzione del gioco.

**Proposta di Claude (da decidere con Ale, una cosa per volta):**
1. **Niente «nemesi» per rivalsa** (vietata dalla regola 2).
2. **Al suo posto, la marcatura nell'ultima regata del torneo**, decisa dalla classifica e detta dal Coach («Verde ti marca: se ti batte, ti passa in classifica»). Tocca la guida dei rivali: va con le voci sui rivali (2, 4B), con proposta e criteri propri (arrivo dei rivali, contatti, nessuna regola rotta mentre marcano).
3. **Cautela:** non farla, o farla come invenzione dichiarata; proposta: non farla finché non c'è una fonte.

