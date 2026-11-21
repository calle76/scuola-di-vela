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
