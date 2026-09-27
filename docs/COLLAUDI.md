# Collaudi

Il gioco si verifica in due modi. I collaudi della **fisica** girano con Node.js e leggono il motore direttamente da `index.html`. I collaudi nel **browser** aprono il gioco in Chromium senza finestra, premono tasti e leggono lo stato tramite l'aggancio `#collaudo`.

Regola del progetto: **ogni modifica a fisica, lezioni o avversari si verifica rilanciando i collaudi pertinenti.** Diversi difetti seri sono emersi solo così (vedi `CHANGELOG.md`).

## Installazione (una volta sola)

Servono Node.js (per la fisica) e Python 3 (per il browser).

```
cd tests
pip install -r requirements.txt
python -m playwright install chromium
```

## Fisica (Node.js)

```
cd tests/fisica
node polare.js              # velocità di equilibrio a vari angoli dal vento, con 6, 10 e 15 nodi
node raffiche_e_virate.js   # virate a diverse velocità e raffiche improvvise
```

Risultati attesi con il motore attuale, con 10 nodi: circa 3,4 nodi a 45°, 5,2 a 90°, 3,5 a 180° (fino alla 0.12 erano 3,8 a 45°: l'angolo morto più largo della 0.13 li ha ridotti). Virata riuscita in circa 4 s partendo a 3,9 nodi, fallita partendo quasi fermi. Raffica a 20 nodi senza reagire: circa 61°, cioè scuffia.

## Browser (Python e Playwright)

Da eseguire nella cartella `tests`. Le immagini finiscono in `tests/output/`.

| Script | Cosa verifica | Esito atteso |
| --- | --- | --- |
| `collaudo_schermate.py` | Apre ogni passo di ogni lezione, ogni prova e la navigazione libera | `errori: []` |
| `collaudo_lezioni.py` | Completa i passi pratici guidando la barca | Tutti `OK`, salvo i due casi noti indicati nello script |
| `collaudo_quiz.py` | I sei quiz e il salvataggio del miglior punteggio | Sei righe con il punteggio, `errori: []` |
| `collaudo_regate.py N T` | N regate accelerate, tipo T (0 a bastone, 1 nelle raffiche) | Tutti gli avversari arrivano, nessuno `BLOCCATA` |
| `collaudo_partenze.py` | Ritardo degli avversari al via con 1, 3 e 5 minuti | Con 3 e 5 minuti, entro circa 12 s e nessuna partenza anticipata |
| `collaudo_strambata.py K N` | N strambate con vela aperta e K nodi | 6 nodi: nessuna scuffia; 15 nodi: scuffia sempre |
| `collaudo_rotta.py` | Esercizio «Tenere la rotta» | Senza correzioni fallisce, con correzioni riesce |
| `collaudo_fantasma.py` | Avversari esperti e salvataggio del fantasma | Tutti arrivano; fantasma salvato e visibile |
| `collaudo_giro_boa.py [casi]` | Un pilota automatico guida con barra e scotta: boa a sinistra, a dritta, sbagliata e corretta (prova 4), triangolo giusto e con la boa 2 a dritta (prova 5), prove 1–3 | Finisce solo quando la boa è girata a sinistra; `giri sbagliati` 1 nei casi sbagliati; prove 1–3 completate |

Il collaudo del giro di boa dura alcuni minuti; i casi si possono lanciare separatamente (per esempio `python collaudo_giro_boa.py ab`). Il pilota automatico è volutamente semplice: se non arriva, prima di dare la colpa al gioco controlla dove si è fermato (angolo morto, marcia indietro, scuffia).

Le regate usano il tempo accelerato, e ogni collaudo dura da pochi secondi a qualche minuto.

## Limiti dei collaudi

- I collaudi guidano la barca con comandi prestabiliti: verificano che le cose **funzionino**, non che siano **chiare o divertenti**. Per quello servono persone che giocano.
- Alcuni risultati dipendono dal caso (raffiche, avversari): un singolo esito anomalo va ripetuto prima di concludere che c'è un difetto, ma un esito anomalo che si ripete è quasi sempre un difetto vero.
- **Per confrontare due versioni servono campioni grandi.** Nella 0.14 due confronti fatti su poche regate hanno mostrato peggioramenti inesistenti: le penalità per contatto (in realtà i contatti erano diminuiti, 22 contro 44 su 12 regate) e i ritardi al via (uguali su 36 partenze). Il collaudo delle partenze fa solo due partenze da 3 minuti: per un confronto se ne misurano almeno una decina per versione, meglio se sulla versione precedente nello stesso momento.
