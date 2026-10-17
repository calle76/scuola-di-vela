# Scuola di vela

Un simulatore didattico per imparare a governare una piccola barca a vela (una deriva). Il carteggio e la navigazione in mare aperto sono previsti come espansione a parte. È un progetto personale e non commerciale, nato per studiare la vela partendo da zero.

Il gioco è una pagina sola, `index.html`, con il codice nella cartella `js/`: si apre in un browser recente senza installare nulla.

> **Attenzione.** Il «Brevetto della Scuola di vela» e tutti i contenuti del gioco non hanno alcun valore legale e non sostituiscono un corso di vela né la patente nautica. I contenuti tecnici sono in fase di verifica: vedi [`docs/CONTENUTI-DA-VERIFICARE.md`](docs/CONTENUTI-DA-VERIFICARE.md).

## Come si gioca

- **In locale:** scarica il repository (servono `index.html` e le cartelle `js/` e `fonts/`) e apri `index.html` con il browser (doppio clic). Con lo zoom lontano Firefox su Linux può rallentare; Chrome è più fluido. Per avere Chrome a schermo intero anche dove F11 non regge: `google-chrome --kiosk --user-data-dir="$HOME/.config/scuola-vela-chrome" "file://$HOME/scuola-di-vela/index.html"` (si esce con Alt+F4).
- **Online:** se il repository ha GitHub Pages attivo, il gioco è all'indirizzo `https://<utente>.github.io/<nome-repository>/`.

Il gioco è pensato per computer con tastiera. Non è ottimizzato per telefono.

### Cosa contiene

| Sezione | Contenuto |
| --- | --- |
| Navigazione libera | Vento, forza e raffiche a scelta, nessun obiettivo. |
| Lezioni 1–6 | La barca e il vento; il timone; andature e filetti; vento reale e apparente; virata e strambata; raffiche e scuffia. |
| Prove 1–5 | Traverso, lasco e poppa, risalire il vento, giro di boa, percorso nelle raffiche. Fasce di tempo oro, argento e bronzo. |
| Regate | Regata a bastone e regata nelle raffiche, contro tre avversari guidati dal computer o in solitaria contro il proprio fantasma. |
| Ripasso | 29 domande a scelta multipla sulle sei lezioni. |
| Esame | 20 domande estratte da una banca separata dai ripassi; servono 16 risposte giuste. |
| Gioco libero e carriera | Due salvataggi separati. In carriera il libretto conta i meriti (abilità, conoscenza, competizione, esperienza), dice cosa manca e suggerisce cosa fare; con i meriti e l'esame superato si ottiene il brevetto di livello 1, con un attestato stampabile **senza valore legale**. |
| Registro degli errori | Scuffie, strambate a vela aperta, barca piantata nel vento, boe girate dal lato sbagliato, contatti e partenze irregolari: contati durante lezioni, prove e regate. ★ nel menu per le prove e regate completate senza errori. |
| Glossario | 45 termini nautici con definizione. |

Tutto è sempre accessibile: nessuna lezione o regata va sbloccata, nemmeno in carriera.

**Stato:** versione 1.0.3 (16 ottobre 2026), la 1.0 con correzioni e manutenzione: il livello 1 giocabile dall'inizio alla fine, ancora da rifinire (vedi `docs/ROADMAP.md`). Il livello 2 sarà dedicato alle regole di regata e di precedenza, sulla stessa barca. Le correzioni della barca (resistenza dello scafo, timone), delle regole di regata e del disegno vengono nelle versioni 1.x: vedi `docs/ROADMAP.md`.

### Comandi

| Tasto | Azione |
| --- | --- |
| ← → | Muovono la barra del timone (nelle impostazioni si può scegliere «girano la prua», più semplice) |
| ↑ ↓ | Cazza e lasca la scotta |
| Spazio | Barra al centro |
| A | Raddrizza la barca dopo una scuffia (fino alla 1.0.26 era R) |
| Invio | Parte dopo aver letto le istruzioni di una prova o di una regata |
| W S | Cazza e lasca con i pulsanti della lezione 1 (anche ↑ ↓) |
| Rotella o + − | Zoom |

Il menu principale è diviso in riquadri: Scuola (lezioni e prove nell'ordine consigliato), Regate, Navigazione libera, Ripasso ed esame.

In basso a sinistra ci sono l'indicatore di sbandamento e la rosa dell'angolo morto (vento sempre in alto, settore rosso di 40° per lato); la freccia verde mostra la direzione in cui la barca si muove davvero. Le impostazioni si aprono con il pulsante ⚙ in alto a destra. Su uno schermo piccolo conviene il tasto F11 (schermo intero).

La barra funziona come nella realtà: si spinge dalla parte opposta a quella in cui si vuole girare la prua. Una freccia gialla sulla prua mostra da che parte la barca sta girando davvero.

## Struttura del repository

```
index.html                         la pagina del gioco (stile e struttura)
js/                                il codice: motore fisico, contenuti, gioco, regate, disegno, registratore, avvio
README.md                          questo file
CHANGELOG.md                       storia delle versioni e dei difetti corretti
LICENSE                            licenza
tests/                             collaudi automatici (browser) e della fisica (Node.js)
sperimentale/                      prototipi fuori dal gioco (oggi: il fiocco)
```

Documenti in `docs/`, divisi per uso:

```
Come è fatto il gioco
  PROGETTO.md                      principi, architettura del codice, decisioni
  FISICA-E-TARATURE.md             modello fisico, costanti e risultati delle tarature
  COLLAUDI.md                      come rilanciare i collaudi automatici
  SPERIMENTALE.md                  regole per i prototipi in sperimentale/
  MANUALE-bozza.md                 cosa il gioco insegna, simula bene o semplifica

Fonti e verifiche (non c'è una persona esperta: valgono fonti scritte e video)
  FONTI-PUBBLICHE.md               fonti usate, con quello che dicono
  CONTENUTI-DA-VERIFICARE.md       affermazioni nautiche del gioco da confermare
  DUBBI-E-RICERCHE.md              domande aperte e ricerche da fare
  SCHEDATURA-FONTI.md              schede dei PDF e dei video consultati
  RICERCA-DATI-IMBARDATA.md        ricerca sui dati per un motore dinamico
  REGOLE-DI-REGATA.md              regolamento di regata vero a confronto con il gioco

Dove si va
  ROADMAP.md                       cosa fare dopo, in ordine di priorità
  PIANO-GENERALE.md                piano dei livelli fino alla 1.0 (bozza)
  VISIONE-LIVELLI-E-CARRIERA.md    visione di livelli, ruoli e carriera
  OSSERVAZIONI-GIOCANDO.md         diario delle prove di gioco

Proposte aperte
  PROPOSTA-RESISTENZA-SCAFO.md     prossimo compito di fisica: resistenza dello scafo
  PROPOSTA-LABORATORIO.md          pannello nascosto per provare profili della barca
  PROPOSTA-ESAME-E-BREVETTO.md     esame e brevetto (in parte fatta nella 0.20 e 0.21)

archivio/                          proposte chiuse o prove non adottate, tenute per memoria
```

## Salvataggi

Progressi, record, punteggi dei quiz e «fantasmi» sono salvati nel browser (`localStorage`), separatamente per ogni indirizzo: la versione aperta in locale e quella su GitHub Pages hanno salvataggi diversi.

## Crediti

- Caratteri tipografici: Barlow Semi Condensed (© 2017 The Barlow Project Authors) e Source Serif 4 (© 2014 The Source Serif 4 Project Authors), licenza SIL Open Font License 1.1. Dalla 1.0.5 i file stanno nella cartella `fonts/`, con il testo delle licenze; sono quelli distribuiti da Google Fonts, non modificati.
- Progetto sviluppato con l'aiuto di Claude (Anthropic).

## Licenza

Vedi [`LICENSE`](LICENSE).
