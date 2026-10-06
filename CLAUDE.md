# Scuola di vela — istruzioni per Claude Code

Progetto personale e non commerciale: un simulatore didattico di vela, in un unico file HTML (`index.html`), da giocare sul computer con la tastiera. Chi lavora con te non è né un velista né un programmatore di professione: spiega in italiano semplice, riporta i numeri così come escono (anche quelli sgraditi) e non chiedergli di giudicare la plausibilità nautica; la giudicano le fonti (`docs/FONTI-PUBBLICHE.md`) e, in futuro, una persona esperta.

## Da leggere prima di lavorare

- Sempre: `docs/PROGETTO.md` (principi), `CHANGELOG.md` (stato delle versioni), `docs/COLLAUDI.md`.
- Sul prototipo del fiocco: `docs/SPERIMENTALE.md`, `docs/FISICA-E-TARATURE.md`, `docs/FONTI-PUBBLICHE.md`, `docs/CONTENUTI-DA-VERIFICARE.md`.
- Su livelli, ruoli e carriera: `docs/VISIONE-LIVELLI-E-CARRIERA.md` e `docs/ROADMAP.md`.
- Lo stato corrente sta nei documenti, non qui: non fidarti di quello che ricordi.

## Principi (da `docs/PROGETTO.md`)

1. Simulatore prima che gioco: la fisica deve essere plausibile.
2. Tutto sempre giocabile in modalità libera.
3. Gli aiuti si possono disattivare.
4. Onestà sui contenuti: ogni affermazione nautica va verificata e le semplificazioni si dichiarano.
5. Nessun marchio di classi o costruttori nel gioco, nessun titolo che sembri ufficiale (il logo e il nome «Scuola Vela FIV» sono marchi registrati). Dati esterni solo con licenza libera e citazione. Si parafrasa, non si copiano testi o tabelle delle fonti. «Brevetto», mai «patente»; sempre «nessun valore legale».
6. Solo computer con tastiera.

## Come si lavora

- **Due fermate per ogni compito.** Fermata 1: scrivi una proposta (modello più semplice plausibile, criteri misurabili con soglie dichiarate come attese nostre, costanti nuove con quali sono ipotesi, fonti, rischi) e fermati, senza codice nel motore. Fermata 2: solo dopo il via implementa, misura e riporta, poi fermati.
- **Le soglie non si cambiano dopo aver visto i risultati** senza dirlo. Un numero fuori fascia si riporta com'è.
- **Un solo tentativo non basta**, nemmeno per dire che una cosa non succede: molti tentativi con semi fissi, e dì quanti.
- **Il metro di misura non deve dipendere da ciò che si misura.** Un controllo scritto come «nessun caso sbagliato» è vero anche con zero casi: verifica che abbia misurato davvero.
- **Collauda guidando davvero la barca** (pilota automatico, aggancio `#collaudo`) e anche in una pagina caricata come la carica un giocatore, senza `#collaudo`.
- **Non-regressione.** La barca senza fiocco deve restare identica a quella del gioco (30 casi di `polare.js`, uscite di `polare.js` e `raffiche_e_virate.js` carattere per carattere, prove 1-3).
- **Pannello** a 1360x650 senza pixel di eccesso, anche nel caso peggiore.
- **Ogni versione aggiorna `CHANGELOG.md`.** I prototipi non sono versioni: stanno in `sperimentale/`, non toccano `index.html`, e vanno sotto «Sperimentale».
- Nei prototipi segna ogni riga cambiata con `// FIOCCO`. A ogni compito chiuso aggiorna i documenti in `docs/`.
- **Risparmio di crediti.** Lancia solo i collaudi direttamente legati alla modifica; i controlli veloci di non-regressione (`polare.js`, `raffiche_e_virate.js`) restano sempre da lanciare. Non aspettare la suite completa né i collaudi lunghi. A fine lavoro indica il comando `tests/lancia_tutti.sh` (con `--veloce` se basta), che l'utente lancia sul suo PC incollando il riepilogo. Se un collaudo è indispensabile per capire se la modifica funziona, lancialo tu.

## Git

- **Non fare commit né push**: li fa l'utente. A fine compito indica i comandi `git add` con i percorsi uno per uno.
- **Mai `git add -A` né `git add .`**: i file `.gitmodules`, `.bashrc` e `.mcp.json` e la cartella `.codex/` li monta l'ambiente e vanno lasciati fuori.
- Prima di chiudere, controlla che `index.html` non risulti modificato nelle sessioni sul prototipo.

## Stile

Rispondi in italiano. Rapporti brevi e chiari: cosa hai fatto, cosa hai misurato (con i numeri), cosa non convince, cosa serve da lui. Niente giri di parole.
