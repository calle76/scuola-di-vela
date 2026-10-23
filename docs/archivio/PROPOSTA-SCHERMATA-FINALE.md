# Proposta: schermata finale di regata fuori dal pannello

Stato: **proposta (fermata 1), nessun codice scritto.** Idea di Ale, 20 ottobre 2026. Versione prevista: 1.0.36.

## Perché
`tests/esplora.py --rigioca` (20 ottobre 2026, versione 1.0.35) ha mostrato che a regata finita il pannello laterale sfora a 1360x650:
- 24 regate su 24 già note come sforanti sforano ancora (da 4 a 150 px); 71 su 100 regate di controllo sforano (misura ogni secondo; il «1%» del primo rapporto era troppo basso perché guardava ogni 10 s).
- Cause: il riquadro `status` (una riga per barca, 178-198 px), il riquadro `rDone` (riepilogo, 72-160 px) e, nelle regate «salti di vento», barra e titolo più alti (58 e 46 px invece di 38 e 26).
- `.panel` ha `overflow-y:auto`: il giocatore vede una barra di scorrimento. La regola del progetto è zero pixel di eccesso, anche nel caso peggiore.

## Modello più semplice
A regata finita (arrivo del giocatore, o ritiro) compare una **schermata finale sopra il mare**, nello stile di quelle già esistenti (es. quella di scuffia, `capOverlay`), con:
- il risultato in grande («2° su 4 in 7 min 24 s»), penalità comprese;
- la classifica con una riga per barca (le righe oggi in `status`);
- errori e record (oggi in `rDone`);
- i pulsanti Ricomincia, Cambia vento, Classifica (Ritirati non serve a regata finita).

Il pannello, a regata finita, torna com'è durante la regata: senza `status` lungo e senza `rDone`. Resta solo, se serve, una riga corta.

## Criteri (attese nostre)
1. Pannello a 1360x650 con **0 px di eccesso** in tutte le 24 regate sforanti, nelle 100 di controllo e in un caso peggiore costruito a mano (barra a due righe, 4 righe lunghe, riepilogo lungo con record ed errori).
2. La schermata finale sta in 1360x650 senza scorrere, anche nel caso peggiore.
3. Dalla schermata si arriva a Ricomincia, Cambia vento e Classifica, con tastiera (principio 6).
4. Barca senza fiocco identica: `polare.js` (30 casi) e `raffiche_e_virate.js` carattere per carattere, prove 1-3.
5. `collaudo_torneo.py`, `collaudo_pannello.py`, `collaudo_riquadro_regata.py` ancora verdi (il torneo dell'1b usa il finale di regata).

Se un numero esce fuori fascia, si riporta com'è.

## Costanti e ipotesi
Nessuna costante fisica. Ipotesi di progetto da confermare: la schermata copre il mare, non il pannello; si chiude con un tasto o con un pulsante.

## Rischi
- `rDone` e `status` sono letti da altri collaudi (torneo, riquadro regata): vanno cercati con `grep` prima di spostarli.
- Il torneo (T1) mostra già punteggi a fine regata: la schermata nuova deve convivere con quella, senza duplicarla.
- Va fatta anche la prova in una pagina caricata come la carica un giocatore, senza `#collaudo`.

## Come si verifica (fermata 2)
`python3 tests/esplora.py --rigioca` con `~/venv-vela/bin/python` (stesso comando di oggi: i 24 casi + 100 di controllo devono dare 0 px), poi i collaudi del punto 5 e `tests/lancia_tutti.sh --veloce` sul PC di Ale. Aggiornare `VERSIONE` in `js/gioco.js`, `CHANGELOG.md` e `docs/COLLAUDI.md`.
