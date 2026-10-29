# Scuola di vela — istruzioni per Claude Code

Progetto personale e non commerciale: un simulatore didattico di vela, in un'unica pagina (`index.html` più i file di `js/`, dalla 1.0.3), da giocare sul computer con la tastiera. Chi lavora con te non è né un velista né un programmatore di professione: spiega in italiano semplice, riporta i numeri così come escono (anche quelli sgraditi) e non chiedergli di giudicare la plausibilità nautica; la giudicano solo le fonti scritte e i video (`docs/FONTI-PUBBLICHE.md`): non ci sarà una persona esperta a cui chiedere.

## Da leggere prima di lavorare

- Sempre: `docs/PROGETTO.md` (principi), `CHANGELOG.md` (stato delle versioni; la storia fino alla 0.24 è in `docs/archivio/`, da aprire solo se serve), `docs/COLLAUDI.md` **senza** la tabella «Browser»: di quella si legge solo la riga del collaudo che serve (`grep -n "collaudo_nome" docs/COLLAUDI.md`).
- **Il codice non si legge mai tutto.** Dalla 1.0.3 è diviso: `index.html` (stile e struttura) e `js/` (`motore.js`, `base.js`, `contenuti.js`, `gioco.js`, `regate.js`, `disegno.js`, `registratore.js`, `moviola.js`, `avvio.js`, `laboratorio.js`, caricati in quest'ordine; la prima riga di ogni file dice cosa contiene). Si apre solo il file che serve, e dentro si legge prima la mappa:
  `grep -nE "^  // ([A-ZÀ-Ú]{4,}|-{3,})" js/nome.js`
  Le intestazioni `// ====` (sezioni) e `// ---- … ----` (sottosezioni) sono la mappa: chi aggiunge una parte nuova le aggiorna. Una riga eseguita al caricamento di un file non vede le funzioni dei file caricati dopo: il codice nuovo che deve partire all'avvio va in `avvio.js`.
- Sul metodo: `docs/METODO.md` (fasi, traguardi, revisione a fine tappa); `docs/DECISIONI.md` (decisioni prese e quanto costa cambiarle) prima di aprire un livello o una proposta grossa, e ogni decisione nuova di Ale ci va con una riga.
- Sul prototipo del fiocco: `docs/SPERIMENTALE.md`, `docs/FISICA-E-TARATURE.md`, `docs/FONTI-PUBBLICHE.md`, `docs/CONTENUTI-DA-VERIFICARE.md`.
- Su livelli, ruoli e carriera: `docs/VISIONE-LIVELLI-E-CARRIERA.md` e `docs/ROADMAP.md`.
- Lo stato corrente sta nei documenti, non qui: non fidarti di quello che ricordi.

## Principi (da `docs/PROGETTO.md`)

1. Simulatore prima che gioco: la fisica deve essere plausibile.
2. Tutto sempre giocabile in modalità libera.
3. Gli aiuti si possono disattivare.
4. Onestà sui contenuti: ogni affermazione nautica va verificata e le semplificazioni si dichiarano.
5. Nessun marchio di classi o costruttori nel gioco, nessun titolo che sembri ufficiale (il logo e il nome «Scuola Vela FIV» sono marchi registrati). Dati esterni solo con licenza libera e citazione (eccezione dal 16 ottobre 2026: valori numerici misurati, letti da pubblicazioni scientifiche e citati, si possono usare nel motore). Si parafrasa, non si copiano testi o tabelle delle fonti. «Brevetto», mai «patente»; sempre «nessun valore legale».
6. Solo computer con tastiera.

## Come si lavora

- **Due fermate per ogni compito.** Fermata 1: scrivi una proposta (modello più semplice plausibile, criteri misurabili con soglie dichiarate come attese nostre, costanti nuove con quali sono ipotesi, fonti, rischi) e fermati, senza codice nel motore. Fermata 2: solo dopo il via implementa, misura e riporta, poi fermati.
- **Le soglie non si cambiano dopo aver visto i risultati** senza dirlo. Un numero fuori fascia si riporta com'è.
- **Un solo tentativo non basta**, nemmeno per dire che una cosa non succede: molti tentativi con semi fissi, e dì quanti.
- **Il metro di misura non deve dipendere da ciò che si misura.** Un controllo scritto come «nessun caso sbagliato» è vero anche con zero casi: verifica che abbia misurato davvero.
- **Collauda guidando davvero la barca** (pilota automatico, aggancio `#collaudo`) e anche in una pagina caricata come la carica un giocatore, senza `#collaudo`.
- **Non-regressione.** La barca senza fiocco deve restare identica a quella del gioco (30 casi di `polare.js`, uscite di `polare.js` e `raffiche_e_virate.js` carattere per carattere, prove 1-3).
- **Pannello** a 1360x650 senza pixel di eccesso, anche nel caso peggiore.
- **A ogni versione del gioco aggiorna la costante `VERSIONE` (in `js/gioco.js`) e la voce del `CHANGELOG.md`**; `tests/collaudo_versione.py` controlla che coincidano.
- **Ogni versione aggiorna `CHANGELOG.md`.** I prototipi non sono versioni: stanno in `sperimentale/`, non toccano `index.html` né `js/`, e vanno sotto «Sperimentale».
- Nei prototipi segna ogni riga cambiata con `// FIOCCO`. A ogni compito chiuso aggiorna i documenti in `docs/`.
- **Risparmio di crediti.** Lancia solo i collaudi direttamente legati alla modifica; i controlli veloci di non-regressione (`polare.js`, `raffiche_e_virate.js`) restano sempre da lanciare. Non aspettare la suite completa né i collaudi lunghi. A fine lavoro indica il comando `tests/lancia_tutti.sh` (con `--veloce` se basta), che l'utente lancia sul suo PC incollando il riepilogo. Se un collaudo è indispensabile per capire se la modifica funziona, lancialo tu.

## Git

- **I commit li fai tu, il push lo fa l'utente** (Ale, 17 ottobre 2026; prima faceva entrambi lui). Il push da qui non funziona: git chiede le credenziali di GitHub, che in questo ambiente non ci sono. A fine lavoro quindi: commit fatto da te, e all'utente il comando `git push`. Si committa solo a collaudi verdi e versione chiusa, aggiungendo i file **uno per uno** e dicendo sempre quali sono entrati e con che messaggio. Prima di committare, `git status --short` per controllare che non entri niente dell'ambiente.
- **Mai `git add -A` né `git add .`**: i file `.gitmodules`, `.bashrc` e `.mcp.json` e la cartella `.codex/` li monta l'ambiente e vanno lasciati fuori.
- Prima di chiudere, controlla che `index.html` e `js/` non risultino modificati nelle sessioni sul prototipo.

## Stile

Rispondi in italiano. Rapporti brevi e chiari: cosa hai fatto, cosa hai misurato (con i numeri), cosa non convince, cosa serve da lui. Niente giri di parole.
