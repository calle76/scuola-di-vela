# Proposta: pulizia dopo il congelamento della barca dell'1b

Stato: **via di Ale alle quattro decisioni, tutte come consigliate** (23 ottobre 2026; per B4: «se un collaudo dura 5 minuti ok, ma sono tutti assieme che ci impiegano tempo», quindi i tre entrano solo fra i lunghi). **Parti A e B fatte** (esiti in fondo; B = versione 1.0.47). Punto «pulizia» della `ROADMAP.md`, dopo il congelamento (`PROPOSTA-CONGELAMENTO-1B.md`). Rete di sicurezza: le due impronte.

**Regola della pulizia:** il gioco non cambia, salvo i testi elencati in B1, dichiarati qui prima di misurare. La storia non si riscrive: `CHANGELOG.md` e le proposte finite restano come sono state scritte, anche dove dicono «livello 2» per l'1b.

## Cosa ho trovato

- **34 proposte in `docs/`, 30 finite.** Restano aperte solo: `PROPOSTA-REGOLE-PRECEDENZA-1B.md` (regole 15-16, prossime), `PROPOSTA-TORNEI-1B.md` (tappa T2), `PROPOSTA-REGATA-COME-FONTE.md` (dopo i tornei), `PROPOSTA-SEGNALI-PARTENZA.md` (livello 2, il regolamento). Le altre sono fatte, superate o chiuse con una scelta di Ale.
- **Il giocatore vede due nomi per la stessa barca:** nelle impostazioni «Barca: livello 2 (prova)» (con il suggerimento «Livello 2, in prova…», `index.html:306`) e nel menu la «Regata nei salti di vento» con «Barca del livello 2» (`js/regate.js:61`); accanto, «Torneo dell'1b» e «Semaforo… (regate dell'1b)». Non è più «in prova»: è congelata.
- **Nel codice «livello 2» = 1b:** 24 righe in `motore.js`, `gioco.js`, `regate.js` (commenti, più il testo del menu di B1); nomi `lv2`, `S.lv === 2`, `RUD2`, `BOMA2`, `SALTI2`, `RADD2` (circa 100 punti). Intestazione della mappa: `// ==== BARCA DEL LIVELLO 2 (1.0.24-1.0.28) ====` (ma dentro c'è anche 1.0.32-1.0.46).
- **Nessuna funzione inutilizzata** trovata (controllo: nomi definiti in `js/` che compaiono una volta sola: zero). Non propongo di togliere codice.
- **Tre collaudi fuori dal giro** di `lancia_tutti.sh` senza un motivo scritto: `collaudo_raddrizzata.py`, `collaudo_virate2.py`, `collaudo_distacchi.py` (sono in `COLLAUDI.md`).
- **`docs/STATO.md` è fermo al 20 ottobre (1.0.35):** mancano 1.0.36-1.0.46 e il congelamento.
- Documenti vivi con «livello 2» per l'1b: `STATO.md`, `ROADMAP.md`, `FISICA-E-TARATURE.md`, `COLLAUDI.md`, `MANUALE-bozza.md`, `DUBBI-E-RICERCHE.md`, `CONTENUTI-DA-VERIFICARE.md`, `FONTI-PUBBLICHE.md`.

## Parte A: documenti (nessuna versione del gioco)

**A1. Le 30 proposte finite vanno in `docs/archivio/`** con `git mv` (la storia di ogni file resta):
BOLINA, CENTRO-VELICO-1B, CONGELAMENTO-1B, CONTATTO-VERO, CORREZIONI-PASSI, DISEGNO-VELA, DISTACCHI, DIVISIONE-CODICE, ELENCO-23-OTTOBRE, ESAME-E-BREVETTO, INCRESPATURE, LABORATORIO, MOTO-SUL-MARE, ORZIERA-1B, PALA-DERIVA-1B, PARTENZE, PILOTA-LEZIONI, PROVA3, RADDRIZZATA, RAFFICHE-PORTANTI, RESISTENZA-SCAFO, RETROMARCIA, SALTI-VENTO, SCARROCCIO-1B, SCHERMATA-FINALE, SPINGI-BOMA, STALLO-TIMONE, VELOCITA, VIRATA-1B, VIRATE-AVVERSARI.
Anche le ricerche finite: `RICERCA-DATI-IMBARDATA.md`, `RICERCA-RETROMARCIA.md`, `RICERCA-VELOCITA-VIRATA-RIPARTENZA.md`. `RICERCA-CONTENUTI-LIVELLI.md` e `PIANO-GENERALE.md` restano (citati dalla visione), con una riga in testa «numeri dei livelli superati: vale `VISIONE` §2».
I riferimenti `docs/PROPOSTA-X.md` nei documenti vivi, nei commenti di `js/` e in `tests/` diventano `docs/archivio/PROPOSTA-X.md`. Il `CHANGELOG.md` no (è storia; una riga in testa dice dove sono finite).

**A2. Nei documenti vivi «livello 2» diventa «1b» dove si parla della barca dell'1b**, a mano (non con un sostituisci-tutto: «livello 2» oggi è anche il regolamento, il livello che verrà).

**A3. `STATO.md` riscritto** sulla 1.0.46 + pulizia, una pagina.

## Parte B: codice (versione 1.0.47)

**B1. Testi che il giocatore vede** (gli unici cambiamenti del gioco):
- impostazioni: «livello 1» / «livello 2 (prova)» → «1a» / «1b»; suggerimento «Livello 2, in prova: …» → «Barca dell'1b: …» (stesso resto del testo);
- menu: «Barca del livello 2, bolina di 300 m…» → «Barca dell'1b, bolina di 300 m…».

**B2. Solo commenti:** «livello 2» → «1b» nei commenti; intestazione `// ==== BARCA DELL'1B (nel codice lv 2; 1.0.24-1.0.46) ====`; riferimenti ai documenti spostati (A1).

**B3. I nomi nel codice NON si cambiano** (`lv2`, `S.lv === 2`, `RUD2`…): circa 100 punti in 4 file, rischio di sbagliare senza nessun guadagno per chi gioca. L'intestazione della mappa dice che `lv 2` vuol dire 1b. [giudizio]

**B4. I tre collaudi fuori dal giro entrano in `lancia_tutti.sh`**, come «lunghi» se durano più di 5 minuti (soglia nostra), così `--veloce` resta corto.

## Criteri (soglie nostre)

1. **Impronta del gioco** (`collaudo_impronta.py`, scene dell'1a e dell'1b): identica al bit, tranne le scene che mostrano i testi di B1. Riferimento fatto qui, dalla 1.0.46 di oggi, con lo stesso browser (copia con `fonts/`). Se l'impronta non vede quei testi (impostazioni, descrizione del menu), lo dico e li controllo con una schermata.
2. **`impronta1b.js` identica; `polare.js` e `raffiche_e_virate.js` identiche carattere per carattere.**
3. **Nessun riferimento rotto:** per ogni file spostato, zero citazioni del vecchio percorso nei file vivi. Perché il controllo misuri davvero, riporto anche quante citazioni ho cambiato (attese: più di 50).
4. **`collaudo_versione.py` OK; pannello 1360×650** (`collaudo_pannello.py`) e altezza del menu (`collaudo_esame.py`, `collaudo_quiz.py`, lezione della 1.0.35), perché cambia un testo del menu.
5. Dimensione del codice prima e dopo, riportata (oggi 325 539 byte fra `index.html` e `js/`).

## Rischi

- Un sostituisci-tutto sbagliato nei percorsi: lo evito spostando un file alla volta e contando le citazioni prima e dopo.
- I tuoi salvataggi non cambiano (nessuna chiave nuova).
- Mentre lanci collaudi sul tuo PC non tocco `js/`, `tests/` e `CHANGELOG.md`: la parte A si può fare subito, la parte B dopo il tuo giro di `esplora.py`.

## Decisioni per Ale

1. Archiviare le 30 proposte finite e le 3 ricerche? (consiglio: sì)
2. Nomi visibili «1a» / «1b» nelle impostazioni e nel menu? (consiglio: sì; è l'unico cambiamento del gioco)
3. Lasciare i nomi interni `lv2` e simili? (consiglio: sì, lasciarli)
4. I tre collaudi nel giro? (consiglio: sì)

Modello per la fermata 2: basta Sonnet.

## Esito della parte A (23 ottobre 2026)

- **A1:** 33 file in `docs/archivio/` (30 proposte, 3 ricerche) con `git mv`; in `docs/` restano 22 documenti. Riferimenti cambiati: **106 nei documenti di `docs/` e 9 fra `README.md` e `RIPARTI-DA-QUI.md`** (attese più di 50: il controllo ha misurato davvero). Citazioni rimaste del vecchio percorso nei documenti vivi: **0**. Restano da cambiare, nella parte B: i commenti di `js/` (circa 40) e di `tests/` (circa 45), e la riga in testa al `CHANGELOG.md`. Le proposte archiviate non sono state toccate: dove citano una proposta rimasta aperta col nome nudo, il rimando ora punta alla cartella sbagliata (storia, lasciato così).
- **A2:** 43 righe in 10 documenti, una per una: 28 parlano della barca dell'1b («1b»), 12 del fiocco («livello 3»), 3 storiche annotate «(oggi: 1b)»; le righe sul regolamento restano «livello 2». `VISIONE` §2 dice anche che nei documenti più vecchi il fiocco è «livello 2»; `PIANO-GENERALE.md` ha in testa l'avviso dei numeri superati.
- **A3:** `STATO.md` riscritto sulla 1.0.46, con i nomi dei livelli spiegati in testa.

## Esito della parte B (23 ottobre 2026, versione 1.0.47)

- **Criterio 1 (impronta):** 67 scene, 64 identiche; nelle 3 diverse (menu, salti di vento principianti ed esperti) cambiano 6 valori su 5081, tutti i testi di B1. **Ok.** Le impostazioni, che l'impronta non vede, misurate a parte: 0 px di scorrimento prima e dopo, finestra 580 → 524 px.
- **Criterio 2:** `impronta1b.js`, `polare.js`, `raffiche_e_virate.js` identici alla 1.0.46. **Ok.**
- **Criterio 3:** 77 rimandi corretti nei commenti di `js/` e `tests/`, tutti dentro commenti (controllato riga per riga), 0 rimasti. **Ok.**
- **Criterio 4:** `collaudo_versione.py`, `collaudo_pannello.py` 1360×650, `collaudo_esame.py`, `collaudo_quiz.py`, più `collaudo_timone2.py` e `collaudo_raddrizzata.py`: OK.
- **Criterio 5:** codice 325 539 → 325 737 byte (+198, commenti più lunghi per i percorsi `archivio/`).
- **Un incidente, riparato:** un primo script sui commenti di `js/` aveva svuotato le righe con «livello» (errore mio sulle catture delle espressioni regolari); i tre file sono stati riportati all'ultimo commit con `git show` (controllo: `git diff` vuoto) e i commenti cambiati a mano, uno per uno.
- **Lasciato:** i commenti di `tests/` che dicono ancora «livello 2» per l'1b (circa 40, nessun effetto); «Brevetto di livello 1» ed «Esame · livello 1» (parlano del livello, non della barca).
