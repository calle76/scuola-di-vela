# Difetti messi apposta: chi se ne accorge

15 novembre 2026, gioco alla 1.3.11. Chiesto da `PER-FABLE.md` §1. Nessun difetto è entrato nel gioco: ognuno vive solo in una copia (`tests/output/controprove/…`), fatta da `tests/controprove.py`.

## Come si è misurato

- I 12 difetti M1-M12 sono 18 righe nuove di `tests/controprove.py` (nomi `f16-m…`): una riga per ogni coppia difetto-collaudo. Ogni riga copia gioco e collaudi, mette il difetto nella copia, lancia il collaudo e guarda se diventa rosso.
- Accanto, 14 **prove neutre** (`f16n-…`): la stessa copia con solo un commento in più. Devono restare verdi: se una diventa rossa, il rosso del difetto non vale come prova.
- Per rifarle: `.venv-collaudi/bin/python tests/controprove.py --solo f16 --parallelo 2` (circa 2 ore e mezza: il torneo da solo dura un'ora per riga).
- Un solo giro per riga, in Chromium. Il freno della temperatura era a 70 °C, ma il picco è stato **78 °C** (sopra il limite di 72): con due tornei insieme il freno non basta, la prossima volta uno alla volta.

## Risultato in breve

**11 difetti su 12 visti da almeno un collaudo. Uno (M3) non lo vede nessuno.** Riga per riga: 15 coppie difetto-collaudo rosse su 18; 13 prove neutre verdi su 14.

| # | Difetto | Collaudo | Esito | Che cosa ha detto |
| --- | --- | --- | --- | --- |
| M1 | la penalità sul punteggio non si somma | `collaudo_torneo` | **rosso** | C1: 5 errori su 16 («gioco [2, 1, 3, 4], atteso [3, 1, 3, 4]»), più le classifiche di C2 |
| M1 | | `collaudo_penalita_testo` | verde | vedi nota 1 |
| M2 | lo scarto non si toglie | `collaudo_torneo` | **rosso** | C1: 6 errori su 16 (scarti tutti a −1), più C2 |
| M3 | un giro vale anche senza strambata | `collaudo_giri` | verde | vedi nota 2 |
| M3 | | `collaudo_prova_giri` | verde | vedi nota 2 |
| M4 | colpa invertita fra mure a dritta e a sinistra | `collaudo_regole` | **rosso** | «cede B (regola 10), atteso A (10)» |
| M4 | | `collaudo_contatto_senza_colpa` | **rosso** | «senza colpa: 1 contatto, 0 penalità» |
| M4 | | `collaudo_registro` | verde | vedi nota 3 |
| M5 | il merito non chiede la stagione senza ritiri | `collaudo_deriva_superata` | **rosso** | D6b: tappa lasciata, eppure «superata per merito» |
| M6 | con tutti gli obiettivi non arriva il gradino sopra | `collaudo_sponsor` | **rosso** | S2: 75 passaggi sbagliati su 151 |
| M7 | finestra del clou 10 s più tardi | `collaudo_coach` | **rosso** | K4 caduto in 4 regate (seme 2605): il clou del Coach è 10 s esatti dopo quello ricalcolato (lanciato a mano, vedi nota 4) |
| M8 | niente ritorno alla schermata di fine regata | `collaudo_moviola` | **rosso** | V6: schermata finale non di nuovo visibile |
| M9 | una lezione della Scuola esce dall'esame | `collaudo_esame` | **rosso** | «17 domande invece di 20» |
| M9 | | `collaudo_deriva_lezioni` | **rosso** | D4: 31 domande, ne servono 25 |
| M10 | 30 px di margine in più nel pannello delle lezioni | `collaudo_pannello_lezioni` | **rosso** | lezione 1.7: pannello 1 px di eccesso |
| M11 | rivali della finale dal 2° al 6° | `collaudo_finale` | **rosso** | F1: 0 su 200 |
| M12 | resistenza dello scafo +5% | `polare.js` | **rosso** | uscita diversa dal riferimento |
| M12 | | `impronta1b.js` | **rosso** | 25 corse diverse su 25 |

I collaudi rossi sono rossi **per la ragione giusta**: in ogni riga il controllo caduto è quello che parla del difetto.

## Note sui verdi

1. **M1 e `collaudo_penalita_testo`: non è un buco.** Quel collaudo controlla che il testo dica «N penalità (+X pt)», non che i punti siano sommati. Era sbagliata l'attesa nella tabella di `PER-FABLE.md`, non il collaudo. La somma la sorveglia `collaudo_torneo`, e la vede.
2. **M3: nessuno lo vede, e con ogni probabilità non lo vedrebbe nemmeno un giocatore.** Il difetto toglie la condizione «almeno una strambata» dal conto dei giri. Ma una barca che gira di 360° nello stesso verso passa per forza da poppa, quindi stramba sempre: lo dice già `collaudo_giri` (D0: «rotazione di 360° senza virata e senza strambata: non esiste»). La condizione nel codice è una cintura di sicurezza che oggi non scatta mai. Vedi la proposta P1.
3. **M4 e `collaudo_registro`: buco piccolo.** Il suo caso «contatto» conta i contatti e controlla che penalità e registro coincidano; il contatto che gli capita è senza colpa del giocatore sia prima sia dopo il difetto (0 penalità in tutti e due). Il difetto lo vedono già due collaudi; vedi la proposta P2.
4. **M7 e la prova neutra del Coach: la controprova non partiva.** `collaudo_coach.py` in una copia si ferma dopo 1 secondo, per due ragioni che non c'entrano col difetto: prende il codice di riferimento con `git archive` dalla cartella in cui si trova (nella copia non c'è), e `controprove.py` non copia la cartella `img/` coi volti (K10 li vuole caricati). Per avere il risultato ho corretto le due cose **solo nelle copie** e lanciato il collaudo a mano, prima col difetto e poi senza. Vedi la proposta P3.
5. **Prova neutra del torneo rossa (1 su 14).** `collaudo_torneo` senza nessun difetto è caduto su C11 («uscita dal menu 3,79 s, soglia 2 s»). È un tempo misurato con l'orologio vero, e il PC era carico (due tornei insieme, 1021 pause del freno). I rossi di M1 e M2 valgono lo stesso, perché sono caduti su C1 e C2, che sono conti e non tempi. Resta che C11 è fragile sotto carico: vedi la proposta P4.

## Proposte (fermata 1: niente è stato cambiato nei collaudi)

| # | Che cosa | Costo | Parere |
| --- | --- | --- | --- |
| P1 | **M3.** Un controllo nuovo in `collaudo_giri.py` che chiama il conto dei giri con uno stato costruito a mano: 360° accumulati e una virata, ma nessuna strambata. Atteso: il giro non conta. Soglia: 10 casi su 10 (5 per verso) | 1 secondo, una decina di righe | da fare: costa poco e sorveglia una regola scritta nel pannello («ciascuno con una virata e una strambata») |
| P2 | **M4.** In `collaudo_registro.py` un secondo contatto costruito: giocatore con mure a sinistra contro un rivale con mure a dritta. Atteso: 1 contatto con penalità nel registro. Soglia: 5 su 5 | 10-20 secondi | si può anche non fare: `collaudo_regole` e `collaudo_contatto_senza_colpa` il difetto lo vedono già |
| P3 | **Controprova del Coach.** (a) `controprove.py` copia anche `img/`; (b) `collaudo_coach.py` e gli altri tre collaudi che usano `git archive` (`collaudo_esame_nuove`, `collaudo_regole_15_16`, `collaudo_scotta_automatica`) cercano la radice del repository invece della propria cartella | due righe | da fare: senza, le righe `f16-m7-coach` e `f16n-coach` restano rosse per una ragione sbagliata |
| P4 | **C11 del torneo sotto carico.** Il tempo di uscita dal menu si misura tre volte e si prende il migliore; la soglia di 2 s non cambia | poche righe | da decidere: è lo stesso tipo di fragilità già vista su GitHub (voce 18) |

## Che cosa non dice questa misura

- Un difetto per zona, scelto da noi: dice che quei 12 controlli scattano, non che ogni riga del gioco è sorvegliata.
- Un solo giro e solo Chromium.
- M7 non è passato dallo strumento ma da un lancio a mano sulle copie (nota 4).
