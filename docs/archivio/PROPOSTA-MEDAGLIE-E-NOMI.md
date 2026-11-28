# Proposta: chiudere la Scuola, medaglie e nomi

4 novembre 2026. Fermata 1, scritta e committata prima del codice. Ale, stesso giorno: «puoi continuare senza chiedere autorizzazioni». Viene dal passo 4 e dal passo 5 di `PROPOSTA-RIORGANIZZAZIONE.md` §5; le decisioni sui nomi sono già di Ale (§8, 30 ottobre), qui non se ne prende nessuna nuova sui livelli.

## 1. Cosa non va oggi

**Medaglie.** Il pilota di `collaudo_fasce.py` mette 79,2 / 124,4 / 158,7 / 286,5 s nelle prove 1-4 e una mediana di circa 302 s nella 5. Le bande d'oro sono 80 / 125 / 160 / **280** / **300**: l'oro della prova 4 oggi **il pilota non lo prende mai** e quello della 5 di rado. Sono le bande della 1.0.11, cioè della barca di prima, non ritarate quando la barca è cambiata (1.1.0).

**Nomi.** Il giocatore legge ancora gergo nostro: «Torneo dell'1b», «con la barca completa dell'1b», «Livello 2: due giri…», «Esame · livello 1», «Livello 1 superato», «Brevetto di livello 1 · Timoniere di deriva». Ale ha deciso: scuola e «Deriva» al posto dei numeri, **niente più brevetti**, un solo attestato, quello della scuola.

## 2. Il modello più semplice

**Medaglie: la regola scritta da sempre in `js/contenuti.js`, senza inventare niente.** Oro = mediana del pilota sui semi di scelta, arrotondata ai 5 s superiori; argento = oro × 1,25 e bronzo = oro × 1,6, arrotondati ai 5 s più vicini (a metà, in su). Una sola aggiunta, per rispettare M3: **se con quell'oro il pilota sta sotto la banda in meno di 25 corse su 30, l'oro sale di 5 s alla volta** finché ci arriva. Le prove che con la regola restano uguali non si toccano.

Atteso, da confermare con la misura: prove 1-3 invariate, prova 4 **290 / 365 / 465**, prova 5 **305 o 310**. I record salvati restano validi (la medaglia si calcola dal tempo migliore, non si salva).

**Nomi: solo testi, nessun meccanismo.**

| Dove | Oggi | Dopo |
| --- | --- | --- |
| Menu, riquadro, pannello del torneo | Torneo dell'1b | Torneo |
| Riquadro e istruzioni del torneo | con la barca completa dell'1b | tolto |
| Fine torneo | Meriti di Competizione dell'1b | Meriti di Competizione del torneo |
| Torneo chiuso in carriera | dopo il brevetto di livello 1 | dopo l'attestato |
| Regata dei giri | Livello 2: due giri… | Due giri… |
| Esame | Esame · livello 1 | Esame della scuola |
| Libretto | Livello 1 superato / Brevetto ottenuto il… | Scuola superata / Attestato ottenuto il… |
| Attestato | Brevetto di livello 1 · Timoniere di deriva | La scuola · superata |

Restano: «Attestato del gioco», «Nessun valore legale», `progress.brevetto` come nome interno del campo salvato (cambiarlo non darebbe niente al giocatore e toccherebbe i salvataggi e i collaudi).

**Fuori da questo compito, per non mescolare:** spostare regate e tornei nel livello «Deriva» (lavoro strutturale, avrà la sua proposta); la **soglia del torneo** (M5), che serve solo quando il torneo apre un livello; i fallimenti noti di `collaudo_competizione` (C1), che vanno con quella.

## 3. Criteri misurabili (soglie nostre, scritte prima)

Tutti in `tests/collaudo_medaglie.py` e `tests/collaudo_nomi.py`, nuovi, in Chromium e Firefox.

**Gruppi di semi (regola dei semi):** bande scelte sui semi **1-30**, confermate sui semi **101-130**, mai guardati. Vento come in `collaudo_fasce.py`: (corsa × 45°).

- **M3a, oro raggiungibile** (già scritto il 30 ottobre, `PROPOSTA-RIORGANIZZAZIONE.md` §6): pilota preciso, in ogni prova tutte le 30 corse finite e **almeno 25 su 30 entro la banda d'oro**, su tutti e due i gruppi.
- **M3b, bronzo con errori tipici** (M3 lo chiedeva senza dire cosa sono; lo diciamo ora): un secondo pilota che decide ogni 0,5 s invece che ogni 0,1, stringe la bolina a 60° invece che a 52° e tiene la scotta 0,12 più lasca del giusto. Ipotesi nostre, non misure di principianti veri. In ogni prova **almeno 25 su 30 entro il bronzo**.
- **M3c, il metro distingue:** lo stesso pilota con errori prende l'oro **al massimo in 5 su 30** per prova. Se lo prende spesso, o gli errori non sono errori o le bande non separano niente.
- **M3d, medaglia vera:** per ogni prova, a corsa finita, il pallino che il **menu** mostra è quello calcolato dal tempo. Almeno 5 casi, uno per prova.
- **N1, niente gergo:** nel testo **a schermo** di menu libero e carriera, libretto, attestato, esame, riquadro del torneo, pannello e istruzioni della regata dei giri e del torneo non compaiono «1a», «1b», «brevetto», «livello 1», «livello 2» (maiuscole o no). Almeno 8 schermate lette e testo non vuoto in ognuna.
- **N1c, controprova:** una scritta «Torneo dell'1b» inserita apposta in una pagina viene trovata dallo stesso controllo.
- **N2, attestato:** «La scuola», «superata», «Attestato del gioco» e «Nessun valore legale» ci sono.
- **N3, salvataggi vecchi:** una carriera salvata con `brevetto` già preso apre attestato e torneo come prima.
- **N4, pagina vera:** tutto N1 sul menu e l'esame anche senza `#collaudo`, 0 errori della pagina.
- **Pannello** a 1360x650 senza eccesso: `collaudo_pannello.py`, `collaudo_menu.py`.
- **Non-regressione:** `polare.js`, `raffiche_e_virate.js`, `impronta1b.js` identici: nessun numero della barca cambia.

Se una soglia non regge, si riporta com'è. M3b e M3c sono le più incerte: la definizione del pilota con errori è nostra e, se non regge, **non si ritocca per farla passare senza dirlo**.

## 4. Costanti nuove

Solo tre numeri del pilota con errori (0,5 s, 60°, +0,12), che stanno nel collaudo e non nel gioco. Nel gioco cambiano solo le bande.

## 5. Fonti

Nessuna: non sono affermazioni nautiche. Le medaglie sono una taratura sulla barca del gioco (regola di metodo: «per ultimi i tempi delle medaglie»), i nomi una decisione di Ale.

## 6. Rischi

- **Medaglie più facili per chi aveva già giocato:** un tempo di 285 s nella prova 4 oggi è argento, domani oro. Voluto: oggi quell'oro era fuori portata.
- **Il pilota non è un giocatore:** le bande dicono quanto va la barca guidata bene, non quanto è difficile guidarla. Solo il gioco di Ale lo dice.
- **Collaudi che controllano le scritte vecchie:** `collaudo_carriera`, `carriera_esame`, `carriera_intera`, `esame`, `torneo` e `libretto` vanno aggiornati nelle stesse righe, senza toccare le loro soglie.

## 7. Esito (4 novembre 2026)

Fatto: **1.2.11**, numeri in `CHANGELOG.md`. Soglie tutte rispettate e non toccate. Tre cose da ricordare:

- **Prova 5:** oro a 320 s, non «305 o 310» come atteso, perché la regola applicata a tutti e due i browser dà 320 (Chromium da solo 310). Sui semi di conferma 25 su 30 in Chromium, margine zero, e 28 in Firefox.
- **Il pilota con errori non resta mai senza medaglia** (bronzo o argento in 30 corse su 30). M3b lo chiedeva, ma vuol dire che il bronzo è largo per questo pilota: se giocando sembra regalato, si riguarda.
- **Rischi:** `collaudo_pannello.py` mancava dall'elenco del §6.
