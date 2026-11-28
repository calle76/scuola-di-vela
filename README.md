# Scuola di vela

Un simulatore didattico per imparare a governare una piccola barca a vela (una deriva in singolo) e per fare le prime regate. È un progetto personale e non commerciale, nato per studiare la vela partendo da zero. Prima viene la simulazione, poi il gioco.

**Si gioca qui:** https://calle76.github.io/scuola-di-vela/ — su computer, con la tastiera (non è fatto per il telefono).

> **Attenzione.** L'attestato e tutti i contenuti del gioco non hanno alcun valore legale e non sostituiscono un corso di vela né la patente nautica. Nessuna persona esperta li ha controllati: le verifiche si fanno su fonti scritte e video, e diverse cose sono semplificate o ancora da confermare (vedi [`docs/CONTENUTI-DA-VERIFICARE.md`](docs/CONTENUTI-DA-VERIFICARE.md)).

## Cosa contiene

**La scuola**, il primo livello:

- 20 lezioni in tre gruppi (la barca; vento e raffiche; regole e partenze), ognuna con il suo ripasso;
- 5 prove a tempo con medaglie oro, argento e bronzo;
- regate contro tre barche guidate dal computer o contro il proprio «fantasma»;
- navigazione libera, esame finale (34 domande, ne servono 28) e glossario.

**Deriva**, il secondo livello, con la stessa barca:

- lezioni 21-25 (il torneo, rivedere la regata, la layline, la precedenza, lo spazio alla boa) e la prova dei giri di penalità;
- allenamento: una regata singola, scegliendo percorso, penalità, numero di barche e rivali;
- torneo di tre regate, stagione del circuito zonale e nazionale (anche con un amico, scambiandosi un file) e una finale;
- un Coach che dà suggerimenti in regata, la moviola per rivederla e la rotta ottimale a regata finita;
- alcune regole di precedenza in più, il cono d'ombra delle vele e gli sponsor in carriera.

**Gioco libero o carriera.** Nel gioco libero è tutto aperto. In carriera ci sono i meriti, l'attestato della scuola (senza valore legale) e poi Deriva. I due salvataggi sono separati.

## Come si gioca in locale

Scarica il repository (servono `index.html` e le cartelle `js/`, `fonts/` e `img/`) e apri `index.html` con un browser recente: non si installa nulla. Con lo zoom lontano Firefox su Linux può rallentare; Chrome è più fluido. Per Chrome a schermo intero:

```
google-chrome --kiosk --user-data-dir="$HOME/.config/scuola-vela-chrome" "file://$HOME/scuola-di-vela/index.html"
```

(si esce con Alt+F4; cambia il percorso se la cartella è altrove).

## Comandi

| Tasto | Cosa fa |
| --- | --- |
| ← → | Barra del timone. Si spinge dalla parte opposta a quella in cui si vuole girare; nelle impostazioni si può scegliere «girano la prua», più facile |
| Maiusc + freccia | Barra fino in fondo |
| Spazio | Barra al centro |
| ↑ ↓ (o W S) | Cazza e lasca la scotta |
| Z (tenuto) | Spinge il boma fuori |
| A | Raddrizza la barca dopo una scuffia |
| Q (tenuto) | Vista del campo |
| 1 2, rotella | Zoom avanti e indietro |
| Invio | Parte, dopo le istruzioni |
| M | Segna un momento nel file della registrazione |
| O | In regata, segna un momento da rivedere nella moviola |

Le impostazioni si aprono col pulsante ⚙: aiuti (suggerimenti, frecce del vento, semaforo delle precedenze, scotta automatica e altri), vista, suoni.

## Salvataggi

Progressi, record e fantasmi stanno nel browser, separati per ogni indirizzo: la copia in locale e quella online hanno salvataggi diversi. La carriera si può salvare in un file e ricaricare. Le regate vengono registrate nel browser e si possono scaricare.

## Cartelle e documenti

```
index.html, js/      il gioco
fonts/, img/         caratteri e immagini
tests/               collaudi automatici nel browser e prove della fisica (Node.js)
sperimentale/        prototipi e misure fuori dal gioco
docs/                documenti
CHANGELOG.md         storia delle versioni e dei difetti corretti
```

I documenti principali:

| Documento | Cosa dice |
| --- | --- |
| [`docs/STATO.md`](docs/STATO.md) | A che punto è il lavoro |
| [`docs/DA-FARE.md`](docs/DA-FARE.md) | Cosa resta da fare |
| [`docs/IL-GIOCO.md`](docs/IL-GIOCO.md) | Com'è fatto il gioco, in una pagina |
| [`docs/PROGETTO.md`](docs/PROGETTO.md) | Principi |
| [`docs/FISICA-E-TARATURE.md`](docs/FISICA-E-TARATURE.md) | Modello fisico e tarature |
| [`docs/FONTI-PUBBLICHE.md`](docs/FONTI-PUBBLICHE.md) | Fonti usate |
| [`docs/COLLAUDI.md`](docs/COLLAUDI.md) | Come rilanciare i collaudi |

Le proposte ancora aperte sono in `docs/`; quelle chiuse in `docs/archivio/`, con un [indice](docs/archivio/INDICE-PROPOSTE.md).

## Crediti

- Caratteri: Barlow Semi Condensed (© 2017 The Barlow Project Authors) e Source Serif 4 (© 2014 The Source Serif 4 Project Authors), licenza SIL Open Font License 1.1; file e testi delle licenze in `fonts/`.
- Suoni della vela e dell'acqua: registrazioni di Freesound con licenza CC0 1.0 (autori e indirizzi in `docs/FONTI-PUBBLICHE.md`, F42 e F43).
- Immagini del Coach: realizzate con strumenti di intelligenza artificiale.
- Progetto sviluppato con l'aiuto di Claude (Anthropic).

## Licenza

Vedi [`LICENSE`](LICENSE).
