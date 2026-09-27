# Roadmap

Aggiornata al 27 settembre 2026.

## Principi che valgono per ogni fase

- **Tutto sempre giocabile**: nessun contenuto va sbloccato nella modalità libera.
- La **carriera** sarà una modalità separata e facoltativa, con salvataggio proprio.
- **Confini legali**: niente marchi, niente titoli che sembrino ufficiali, dati esterni solo con licenza libera e citazione.
- Ogni novità si collauda **guidando davvero la barca** (vedi `COLLAUDI.md`), non solo leggendo il codice.

## Fase A — Misura degli errori, brevetto ed esame

1. **Registro degli errori** in lezioni, prove e regate: scuffie, strambate involontarie, secondi piantati nell'angolo morto, contatti, partenze anticipate, boe girate dal lato sbagliato (già contate dalla 0.14: `wrongMarks`).
2. **Fasce di tempo** per le prove (bronzo, argento, oro), tarate sui tempi degli avversari esperti **dalla 0.14 in poi** (il giro di boa vero ha allungato i tempi), con vento fisso durante i tentativi validi.
3. **Esame a risposte chiuse**: banca di 80–100 domande, 20 estratte a caso, soglia 80%. Due tipi:
   - glossario (come i quiz attuali);
   - situazioni con un piccolo disegno di barca e vento («che andatura è?», «cosa fai se entra una raffica?», «chi ha la precedenza?»).
4. **Brevetto della Scuola di vela**, a livelli (per esempio «Timoniere di deriva», poi «Regatante»), con attestato stampabile. Nessun valore legale, e deve essere scritto.

## Fase B — Tornei e classifiche personali

- Tornei di più regate contro gli avversari del computer, con il sistema a punti delle regate (1 punto al primo, 2 al secondo, e così via; vince chi ne ha meno), eventualmente con uno scarto.
- Classifica dei record personali per prova e regata.
- Avversari «esperti» più forti: virate più rapide, scelta del bordo migliore, uso delle raffiche.
- **Difetto noto degli avversari:** in circa una partenza su cinque un avversario parte in anticipo o con più di un minuto di ritardo (con 1 minuto di preparazione i ritardi sono più frequenti). Le regate si concludono comunque.

## Fase C — Più tipi di barca

Il motore è parametrico: una barca nuova è un nuovo insieme di costanti più un disegno.

| Barca (nomi generici) | Caratteristiche |
| --- | --- |
| Deriva scuola | Lenta, stabile, perdona gli errori |
| Deriva singola da regata | La barca attuale |
| Catamarano | Molto veloce, vira male, scuffia in modo diverso |
| Deriva a due vele | Fiocco con la sua scotta: serve un secondo comando |
| Cabinato | Non scuffia, sbanda, molta inerzia: base per il carteggio |

Nelle regate miste: compenso di tempo tra barche diverse, come nelle regate reali.

## Fase D — Carteggio (resta in programma)

1. Gradi e direzioni: rosa dei venti, prua in gradi, rilevamento.
2. Velocità, tempo, distanza: nodi e miglia, punto stimato.
3. Fare il punto: due rilevamenti e il loro incrocio.
4. Il segnalamento: boe laterali e cardinali, fari.
5. Nord vero e nord magnetico.

Serve una vista «carta nautica» accanto a quella di navigazione. Per coste reali: OpenStreetMap (licenza ODbL, citazione obbligatoria) e GEBCO per le profondità. Le carte nautiche ufficiali sono protette e non vanno riprodotte.

## Fase E — Modalità carriera

Percorso facoltativo: brevetto ed esame, regate di circolo, livelli più difficili; vincendo si guadagnano barche più veloci. Non toglie nulla alla modalità libera.

## Fase F — Condivisione tra amici

Classifiche comuni e fantasmi condivisi («sfida il record di un amico»).

- Su claude.ai è possibile con l'archivio condiviso delle pagine pubblicate.
- Su GitHub Pages serve un servizio esterno per i dati, per esempio un database gratuito ospitato. Va valutato a parte.
- In entrambi i casi non c'è protezione contro chi bara: va bene tra amici, non per una classifica pubblica.

## In secondo piano (non cancellato)

- Mare aperto e navigazione in solitaria su lunghe distanze, con tempo accelerato.
- Vista 3D con camera dietro la barca.
- Regate in tempo reale tra più persone.

## Decisioni prese nella versione 0.14

- Andatura nel pannello nascosta nelle lezioni 1 e 2.
- Boe da lasciare a sinistra, in prove e regate.
- Barra che torna al centro: spenta di default in prove e regate, riattivabile.

## Decisioni aperte

| Decisione | Opzioni |
| --- | --- |
| Regole di regata | Giri di penalità invece dei 15 secondi; penalità per il contatto con la boa. |
| Licenza | MIT (attuale) o una licenza non commerciale (vedi `LICENSE`). |
