# Proposta: le lezioni del 2a (regolamento, segnali, giri di penalità)

31 ottobre 2026. **Fermata 1: solo documento, nessun codice, nessun testo di lezione.** Le fette 1-5 del 2a hanno messo nel motore (solo nella «Regata con i giri di penalità») i giri di penalità, la boa toccata, le bandiere, la 21.1/21.2 e i giri degli avversari. Questa proposta dice **cosa deve insegnare la scuola** su quel materiale, da dove vengono le affermazioni e come si verifica che la lezione funzioni. Rinvia al `PROPOSTA-RIORGANIZZAZIONE.md` per il dove: tutte le lezioni vanno nella **scuola** (livello 0), con la barca dell'1b, e si scrivono quando la scuola si riscrive (§5 passo 3), non prima: scriverle ora sulla struttura vecchia (1a/1b, sei lezioni) vorrebbe dire riscriverle.

## 0. Il quadro completo delle lezioni della scuola (correzione di Ale, 31 ottobre 2026)

La prima stesura di questo documento parlava solo di regolamento. **Le lezioni della scuola sono più di quelle sul regolamento.** Tutto l'elenco, come risulta da `PROPOSTA-RIORGANIZZAZIONE.md` §3 e da `PROPOSTA-COMPLETAMENTO-1B.md` §1:

| Gruppo | Lezioni | Stato |
|---|---|---|
| **A. Le sei di oggi, riscritte per la barca dell'1b** | 1 La barca e il vento; 2 il timone; 3 **andature e mure** (senza «precedenze», che vengono dopo nel gruppo D); 4 vento reale e vento apparente; 5 virata e strambata; 6 raffiche e scuffia (`js/contenuti.js`, `LESSONS`) | Testi e quiz esistono (si tengono); i passi pratici vanno percorsi di nuovo dal pilota con la barca nuova. Nella lezione 3 si toglie la parte sulle precedenze |
| **B. La fisica dell'1b** | 1 timone che stalla (freccia e Maiusc); 2 **spingi il boma (tasto Z)** per uscire dall'angolo morto; 3 salti di vento (virare sugli scarsi); 4 raddrizzata lunga (tasto A); 5 barca che orza sbandando | Mai scritte. Fonti già citate in `PROPOSTA-COMPLETAMENTO-1B.md` |
| **C. Partenza e tecnica** | 1 **partenza in velocità**; 2 **partenza da fermi** | Da scrivere; il motore c'è. Contenuto da definire con le misure già fatte sulle partenze (`archivio/PROPOSTA-PARTENZE.md`) |
| **D. Il regolamento (2a)** | Le sette di §1 qui sotto | Da scrivere; il motore c'è |

**Corretto il 31 ottobre su indicazione di Ale:** (1) il gruppo A ha i titoli veri del gioco; nella prima stesura avevo scritto «il vento a bordo», che non è il titolo, ed è la lezione «Vento reale e apparente»; (2) le precedenze escono dalla lezione 3 e restano solo nel gruppo D; (3) il gruppo C è di due lezioni; (4) **il gruppo «E» (poppa e strambata) è tolto**: la strambata è già la lezione 5 del gruppo A, e la correzione del boma in poppa (`PROPOSTA-BOMA-IN-POPPA.md`) cambia soltanto quello che quella lezione mostra, non crea una lezione.

La lezione 6 delle «sette brevi» dell'1b (contatto vero e chi cede) entra nel gruppo D; la 7 (come funziona il torneo) passa al livello Deriva perché la scuola non ha tornei. Totale: 6 + 5 + 2 + 7 = **20 lezioni**, ciascuna di 2-4 passi con un solo passo pratico e un quiz di 4 domande (il modello di `PROPOSTA-COMPLETAMENTO-1B.md`). È tanto per chi comincia: l'ordine mette A e B prima, il regolamento (D) dopo.

**«Contatto vero» e danno.** «Contatto vero» non vuol dire con danno: è il contatto fra i contorni degli scafi (1.0.39, `hullOverlap`) al posto del contatto fra cerchi. Il **danno** è un'altra cosa e il gioco non lo ha. Il regolamento (F15) dice: regola 14, ogni barca evita il contatto se ragionevolmente possibile, anche quella con la precedenza (che può aspettare finché è chiaro che l'altra non si scansa); regola 43.1(c), la barca con la precedenza è **esonerata** dalla 14 se il contatto **non causa danno o lesioni**. Quindi, se c'è danno, anche la barca che aveva ragione può avere torto: Ale lo ricordava giusto. Nel gioco oggi chi deve lasciare strada ha sempre torto e l'altra mai. Per modellare il danno servirebbe una soglia («che cosa è un danno» in un gioco senza scafi che si rompono, per esempio una velocità relativa) che **non ha fonte**: sarebbe un'ipotesi nostra. Non è nella lezione 4, che resta solo teoria dichiarata; se Ale lo vuole è una fetta a sé con fermata 1 (regola 14 «contatto serio»).

Il resto di questo documento tratta il gruppo D; per il gruppo B valgono i criteri di `PROPOSTA-COMPLETAMENTO-1B.md` §«Criteri», da riscrivere sulla scuola quando si comincia.

## 1. Cosa insegnare nel regolamento (sette lezioni brevi, gruppo D)

Ogni lezione: una pagina di teoria con il disegno (come «Le mure e le precedenze» di oggi, lezione 3) e, dove serve, una prova pratica. Le regole si **parafrasano** e si cita il numero (principio 5); il testo di ogni lezione si scrive solo dopo aver riletto la regola nel PDF (`fonti-pdf/RRS-2025-2028-World-Sailing.pdf`, F15), come da `CLAUDE.md`.

| # | Lezione | Regole F15 | Che cosa vede/fa il giocatore | Il motore c'è? |
|---|---|---|---|---|
| 1 | Mure opposte: chi ha la precedenza | 10 | Disegno con due barche; poi regata con il semaforo acceso (rosso/verde) | Sì (1.0.40, `chiCede`) |
| 2 | Stesse mure: sovrapposte e libere dietro | 11, 12 | Disegno con la linea al traverso della poppa; semaforo in regata | Sì |
| 3 | Chi vira lascia strada | 13 | Disegno; regata con avversari che virano vicino | Sì |
| 4 | Evitare il contatto e non togliere spazio | 14, 15, 16 | **Solo teoria** (nel gioco non c'è la penalità a chi aveva ragione ma poteva evitare) | Dichiarato: no |
| 5 | I segnali di partenza | 26, 29.1 | Disegno delle bandiere (classe, P, X, blu) e prova: una partenza con 5 minuti e la barca giuria in vista, poi un quiz | Sì (1.0.65) |
| 6 | La partenza anticipata | 29.1, 21.1 | Prova: partire in anticipo di proposito, tornare dietro la linea, lasciare strada | Sì (1.0.65, 1.0.66) |
| 7 | Toccare una boa e i giri di penalità | 31, 44.1, 44.2, 21.2 | Prova: toccare la boa, fare i giri con virata e strambata **nel verso che si preferisce, purché sempre lo stesso**; poi vedere che chi gira lascia strada. Il consiglio «da un lasco o a bassa velocità conviene poggiare per prima» è una **scelta del gioco** (la regola non lo dice): si scrive come consiglio, non come regola | Sì (1.0.61-1.0.68) |

**Non si insegna (e il perché):** spazio alla boa (18) e penalità di partenza I, Z, U, nera (30) non sono nel motore e `REGOLE-DI-REGATA.md` le dà come «da rimandare»; la 17 e la 23 sono marginali per questo gioco. Insegnare una regola che il gioco poi non applica sarebbe una promessa non mantenuta (principio 4): se si vuole citarle, una riga di glossario «esiste, non è nel gioco».

## 2. Come si fanno le prove senza una barca di scena

Il gioco non ha una barca ferma in un punto, fatta apposta per una lezione: l'unico modo di avere altre barche è la regata. Quindi le prove delle lezioni 1-3 e 7 usano la **regata con gli avversari e il semaforo acceso**, con un obiettivo da leggere nel pannello («passa 3 volte da mure a dritta lasciando strada»), non una scena costruita. Costa poco e si basa su ciò che c'è; il limite è che la situazione non si ripete a comando. Una barca di scena sarebbe una funzione nuova (e collaudi nuovi): **non la propongo ora**, la tengo come ipotesi se le prove in regata non bastano.

## 3. Criteri (soglie scritte prima, attese nostre)

- **L1, le fonti:** per ogni lezione, prima del testo, una riga con la regola e il paragrafo del PDF letto. 7 lezioni su 7. Dove la regola ha eccezioni che il gioco non applica (per esempio la 18 nella 10-12 alla boa) si scrive.
- **L2, la lezione dice quello che fa il gioco:** per ogni frase della teoria che descrive una situazione del gioco, un collaudo con il pilota che la provoca e controlla il messaggio del gioco (come `collaudo_regola21.py`): **100%** delle frasi coperte, e se non si può provocare la frase si toglie.
- **L3, le prove sono raggiungibili:** il pilota di prova completa ogni prova pratica: **almeno 25 su 30 semi**; dove il pilota non basta (precedenze con avversari) si usa il metro di `collaudo_regola21.py` sul semaforo.
- **L4, pagina senza `#collaudo`:** ogni lezione si apre e si finisce da menu come la carica un giocatore, senza errori di pagina, anche con Firefox.
- **L5, pannello** a 1360×650 senza pixel di eccesso con il testo più lungo.
- **L6, il testo è leggibile:** frasi corte; ogni termine nuovo (sopravento, sottovento, sovrapposta, libera dietro) nel glossario, 100%.

## 4. Rischi

- **Troppa teoria in una volta** (già segnalato nella riorganizzazione): sette lezioni brevi, una pagina ciascuna.
- **Le prove in regata sono lunghe** e le situazioni non si ripetono: il giocatore potrebbe non vedere mai la situazione che la lezione spiega. Rimedio: obiettivi di conteggio sul pannello, e se non bastano la barca di scena.
- **Le fonti sono in inglese** e la traduzione italiana ufficiale non c'è: i termini italiani (mure, sopravento, «libera dietro») sono quelli del glossario del gioco; la corrispondenza con le definizioni F15 si scrive nelle note, non nella lezione.
- **Le regole nel gioco sono più semplici del regolamento** (14, 15, 16, 18, 30): ogni lezione dichiara cosa il gioco fa e cosa no.

## 5. Quando

Dopo la pulizia del codice e prima delle medaglie (`PROPOSTA-RIORGANIZZAZIONE.md` §5, passo 3). Prima servono le tre cose decise da Ale il 31 ottobre: giocare e dare i test, l'elenco di ciò che manca alla Scuola e a Deriva, la pulizia del codice.

## 6. Da decidere (Ale)

1. Le sette lezioni vanno bene come elenco, o ne togli/aggiungi? In particolare la 4 (solo teoria, dichiarata).
2. Prove in regata con il semaforo (senza barca di scena) per cominciare: va bene?
