# Proposta: il suggerimento del Coach in regata resta più a lungo (voce 68)

*Fermata 1, 20 novembre 2026. Richiesta di Ale: «sparisce troppo in fretta». Nessun codice finché non arriva il via. Estende `PROPOSTA-COACH-IN-REGATA.md` (1.3.28).*

## Cosa c'è oggi (letto nel codice, `js/rotta.js`)

- Un commento resta visibile `CR_DUR = 6` s, con dissolvenza di 0,8 s in uscita (`crDisegna`). Fra un commento e il successivo passano almeno `CR_PAUSA = 30` s.
- **Le frasi forzate** (penalità, giri fatti, contatto con colpa, partenza anticipata) **non rispettano la pausa** e **sostituiscono subito** il commento in corso (`crDi` con `forza`). Quindi un commento può sparire prima dei 6 s, se ne arriva uno forzato. Questa seconda causa non è ancora misurata.
- Le frasi più lunghe hanno circa 130 caratteri: lette in 6 s, con la barca da guidare, sono poche.

## Il modello più semplice

1. **Durata che dipende dalla lunghezza della frase**, non fissa: `durata = CR_BASE + caratteri / CR_LETTURA`, con un minimo e un massimo. Una frase corta resta poco, una lunga di più. Ipotesi nostre (da misurare, non da fonti): `CR_BASE = 5` s, `CR_LETTURA = 15` caratteri al secondo, minimo 8 s, massimo 14 s. Per una frase da 130 caratteri: circa 13,7 s; per una da 60: circa 9 s.
2. **Un commento forzato non cancella quello in corso prima di 4 s** (`CR_MIN_VISTO`, ipotesi nostra): se ne arriva uno forzato prima, resta in coda e compare appena passano i 4 s. Le penalità arrivano comunque entro pochi secondi, e restano nel pannello e nei messaggi delle regole.
3. La pausa fra due commenti resta 30 s **contata dall'inizio** del commento, come oggi, per non far parlare il Coach di meno. Effetto: con la durata più lunga lo spazio vuoto fra due commenti si accorcia da 24 s a circa 16-22 s (da dire ad Ale).

## Due scelte per Ale

1. **Durata fissa (per esempio 12 s) o proporzionale alla frase?** Consiglio la proporzionale: la fissa è più semplice, ma le frasi corte restano troppo.
2. **Una frase da rileggere:** un modo per rivedere l'ultimo suggerimento (per esempio tenere un tasto) è fuori da questa proposta; si può valutare dopo.

## Costanti nuove (tutte ipotesi nostre, senza fonte)

`CR_BASE` 5 s, `CR_LETTURA` 15 car/s, minimo 8 s, massimo 14 s, `CR_MIN_VISTO` 4 s. `CR_DUR` (6 s) sparisce.

## Criteri (soglie nostre, dichiarate prima)

| # | Criterio | Soglia |
| --- | --- | --- |
| D1 | Durata a schermo | su 20 regate lunghe col pilota (semi fissi), ogni commento non forzato visibile almeno `min(14, 5 + caratteri/15)` s e almeno 8 s; la durata si legge nel file della regata (riga «C» e fine) |
| D2 | Il forzato non taglia | nessun commento sostituito prima di 4 s; ogni commento forzato compare entro 4 s dall'evento (esclusa la partenza anticipata, che resta immediata se non c'è un commento in corso) |
| D3 | Regata invariata | col Coach acceso o spento, posizioni e tempi identici al bit (come P4 della 1.3.28) |
| D4 | Non copre | riquadro dentro il mare, pannello 1360x650 con 0 px di eccesso, anche con la frase più lunga |
| D5 | Non troppi | commenti per regata ancora fra 4 e 12 (mediana), come P1 della 1.3.28 |
| D6 | Come un giocatore | pagina senza `#collaudo`, una regata giocata: frasi viste, 0 errori |

Il metro di D1 non deve dipendere da ciò che misura: si ricalcola la durata dalla lunghezza del testo nel collaudo, non dalla costante del gioco, e si controlla che i casi misurati siano almeno 50.

## Rischi

- **Frasi sovrapposte al lavoro del giocatore:** un riquadro che resta 14 s copre il mare più a lungo. Sta in alto a sinistra, sotto il riquadro delle bandiere (P5 della 1.3.28 resta valido).
- **Coda:** con tre frasi forzate di fila la coda può allungarsi; si tiene solo l'ultima per tipo.

## Passi, dopo il via

1. Costanti e coda in `crDi`/`crDisegna`, dietro la stessa impostazione del Coach.
2. `collaudo_coach_regata.py`: criteri D1-D6; tutte le soglie del collaudo vecchio ricalcolate per la nuova durata (dichiarandolo).
3. Documenti, versione, `CHANGELOG.md`.
