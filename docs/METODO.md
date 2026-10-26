# Metodo di lavoro

Scritto il 25 ottobre 2026. Raccoglie la successione di lavoro che il progetto ha scoperto strada facendo e le dà i nomi che usa lo sviluppo professionale di giochi. Vale anche per i progetti futuri. Le regole di dettaglio per Claude Code restano in `CLAUDE.md`; le decisioni prese stanno in `DECISIONI.md`.

## 1. Il principio

**Si decide prima quello da cui dipendono più cose, perché cambiarlo dopo costa di più.**

Esempio del progetto: la 1.0.6 ha cambiato la resistenza dello scafo e gli avversari hanno cominciato a superare la linea allo sparo (dal 22-32% all'83%), perché frenavano a una distanza fissa; la 1.0.11 (bolina) ha reso da correggere tre passi delle lezioni. Da lì la regola «prima la barca, poi il resto» (17 ottobre 2026).

## 2. Le fasi

| Fase | Cosa si fa | Cosa è vietato | Nel progetto |
| --- | --- | --- | --- |
| **Idea** | Una pagina: cos'è il gioco, per chi, i principi che non si toccano (i «pilastri») | — | `PROGETTO.md` |
| **Preproduzione** | Prototipi usa e getta per togliere prima il rischio più grosso | Costruirci sopra contenuti | `sperimentale/` (fiocco) |
| **Fetta verticale** | Un pezzo piccolo ma completo, dall'inizio alla fine | Allargarsi ad altri livelli | La 1.0 (livello 1 fino all'attestato) |
| **Sistemi** | Fisica e regole del livello, poi congelamento con l'impronta | Scrivere lezioni o tarare medaglie | Barca dell'1b, 1.0.24-1.0.46 |
| **Produzione** | Avversari, manovre, lezioni, menu sopra i sistemi congelati | Toccare la fisica senza una ragione forte e dichiarata | 1b dopo il 23 ottobre |
| **Alfa** | Tutte le funzioni del livello ci sono, anche grezze | Aggiungere funzioni nuove | da definire per l'1b (§5) |
| **Beta** | Tutti i contenuti ci sono; si correggono solo difetti e testi | Aggiungere contenuti | da definire per l'1b (§5) |
| **Taratura** | Numeri, difficoltà, tempi delle medaglie | Cambiare sistemi o contenuti | «Per ultimi i tempi delle medaglie» |
| **Uscita** | Versione pubblicata per chi gioca (Lucio) | — | Tag della versione, `main` |

Ogni livello nuovo ripete la successione da «Preproduzione» in poi.

## 3. Quando decidere

Si decide **all'ultimo momento responsabile**: il più tardi possibile, ma prima che il costo di non aver deciso cominci a salire. In pratica:

- **Decisioni ad alto costo di cambiamento: presto.** Piattaforma e motore; comandi; unità e convenzioni (gradi, metri, nodi, verso degli angoli); formato dei salvataggi; modello fisico di base; contenuti come dati e non come codice; struttura dei livelli; regole legali.
- **Decisioni a basso costo: tardi.** Testi, numeri, soglie, aspetto grafico, ordine delle lezioni, punteggi.

Ogni decisione presa va in `DECISIONI.md` con il suo costo di cambiamento. Prima di aprire un livello nuovo si rileggono le righe ad alto costo.

## 4. Revisione a fine tappa

Dopo ogni congelamento, traguardo o livello: mezz'ora, tre domande, risposte scritte in fondo a questo file (§7).

1. Cosa ha funzionato e va tenuto?
2. Cosa ci ha fatto rifare lavoro, e perché?
3. Quale regola aggiungiamo (a `CLAUDE.md`, a questo file o a `DECISIONI.md`)?

## 5. Traguardi con nome

Ogni livello ha tre traguardi, decisi **prima** di cominciare la produzione:

- **alfa:** l'elenco delle funzioni che devono esserci;
- **beta:** l'elenco dei contenuti che devono esserci;
- **uscita:** taratura fatta, collaudi verdi, prova a mano, tag.

**Proposta per l'1b [da decidere con Ale]**, dall'ordine di `ROADMAP.md`:
- *1b alfa:* avversari con la barca dell'1b, torneo T2, replay semplice, menu, attestato e brevetto dell'1b;
- *1b beta:* lezioni brevi dell'1b scritte e giocabili;
- *1b uscita:* tempi delle medaglie, collaudi, prova a mano di Ale e di Lucio.

## 6. Abitudini che rendono il lavoro fluido

- **Un solo fronte aperto** alla volta; il resto va in `STATO.md`, «Prossimo lavoro».
- **`main` sempre giocabile:** si committa solo con collaudi verdi e versione chiusa (`CLAUDE.md`, «Git»). Niente rami per compito: per un progetto con una persona e Claude Code complicherebbero più di quanto aiutano (decisione del 26 ottobre 2026).
- **Strumenti interni prima del lavoro ripetitivo:** laboratorio, registratore, pilota dei collaudi. Se un controllo si fa a mano più di tre volte, si chiede a Claude Code uno strumento.
- **Un giocatore con gli occhi nuovi** a ogni beta: Lucio non verifica la vela, ma se si perde in una lezione la lezione non è chiara.
- **Grafici invece di tabelle** quando si confrontano due versioni (Python con matplotlib).
- **La lista delle cose da fare sta nel repository** (`STATO.md`), così la leggono anche le chat; in `RIPARTI-DA-QUI.md` resta solo quello che non può andare su GitHub.

## 7. Revisioni fatte

(vuoto: la prima si fa alla fine della produzione dell'1b, oppure subito sul congelamento del 23 ottobre)
