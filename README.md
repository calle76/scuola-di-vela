# Scuola di vela

Un simulatore didattico per imparare a governare una piccola barca a vela (una deriva) e, più avanti, a navigare con la carta nautica. È un progetto personale e non commerciale, nato per studiare la vela partendo da zero.

Il gioco è un unico file, `index.html`: si apre in un browser recente senza installare nulla.

> **Attenzione.** Il «Brevetto della Scuola di vela» e tutti i contenuti del gioco non hanno alcun valore legale e non sostituiscono un corso di vela né la patente nautica. I contenuti tecnici sono in fase di verifica: vedi [`docs/CONTENUTI-DA-VERIFICARE.md`](docs/CONTENUTI-DA-VERIFICARE.md).

## Come si gioca

- **In locale:** scarica il repository e apri `index.html` con il browser (doppio clic).
- **Online:** se il repository ha GitHub Pages attivo, il gioco è all'indirizzo `https://<utente>.github.io/<nome-repository>/`.

Il gioco è pensato per computer con tastiera. Non è ottimizzato per telefono.

### Cosa contiene

| Sezione | Contenuto |
| --- | --- |
| Navigazione libera | Vento, forza e raffiche a scelta, nessun obiettivo. |
| Lezioni 1–6 | La barca e il vento; il timone; andature e filetti; vento reale e apparente; virata e strambata; raffiche e scuffia. |
| Prove 1–5 | Traverso, lasco e poppa, risalire il vento, giro di boa, percorso nelle raffiche. |
| Regate | Regata a bastone e regata nelle raffiche, contro tre avversari guidati dal computer o in solitaria contro il proprio fantasma. |
| Ripasso | 29 domande a scelta multipla sulle sei lezioni. |
| Glossario | 45 termini nautici con definizione. |

Tutto è sempre accessibile: nessuna lezione o regata va sbloccata.

### Comandi

| Tasto | Azione |
| --- | --- |
| ← → | Muovono la barra del timone (nelle impostazioni si può scegliere «girano la prua», più semplice) |
| ↑ ↓ | Cazza e lasca la scotta |
| Spazio | Barra al centro |
| R | Raddrizza la barca dopo una scuffia |
| A D W S | Orza, poggia, cazza, lasca (solo nella lezione 1) |
| Rotella o + − | Zoom |

La barra funziona come nella realtà: si spinge dalla parte opposta a quella in cui si vuole girare la prua. Una freccia gialla sulla prua mostra da che parte la barca sta girando davvero.

## Struttura del repository

```
index.html                         il gioco (file unico: fisica, contenuti, grafica)
README.md                          questo file
CHANGELOG.md                       storia delle versioni e dei difetti corretti
LICENSE                            licenza
docs/PROGETTO.md                   architettura del codice e decisioni di progetto
docs/FISICA-E-TARATURE.md          modello fisico, costanti e risultati delle tarature
docs/ROADMAP.md                    cosa fare dopo, in ordine di priorità
docs/CONTENUTI-DA-VERIFICARE.md    affermazioni nautiche da controllare su un manuale
docs/COLLAUDI.md                   come rilanciare i collaudi automatici
tests/                             collaudi automatici (browser) e della fisica (Node.js)
```

## Salvataggi

Progressi, record, punteggi dei quiz e «fantasmi» sono salvati nel browser (`localStorage`), separatamente per ogni indirizzo: la versione aperta in locale e quella su GitHub Pages hanno salvataggi diversi.

## Crediti

- Caratteri tipografici: Barlow Semi Condensed e Source Serif 4, da Google Fonts (licenza SIL Open Font License).
- Progetto sviluppato con l'aiuto di Claude (Anthropic).

## Licenza

Vedi [`LICENSE`](LICENSE).
