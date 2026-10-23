# Proposta: ricontrollo di pala e deriva della barca dell'1b (prima di congelarla)

Stato: **fermata 1, nessun codice nel gioco** (23 ottobre 2026, notte). Richiesta di Ale dopo aver letto le regole di classe di una deriva singola da 4,2 m: «si ricontrolla»; le misure si usano **con citazione** (decisione di Ale, 23 ottobre 2026), senza nomi di classi nel gioco.

## Fonti
- **F37** (in `FONTI-PUBBLICHE.md`): regole di classe di una deriva singola da 4,2 m, edizione in vigore dal 10 agosto 2026 (`ILCA_CR_10-August-2026.pdf` nella cartella del progetto, fuori da git), disegno E.3 di pagina 28. **Pala:** corda 203 mm, bordo d'attacco al massimo 635 mm, bordo d'uscita al massimo 527 mm, spessore al massimo 20 mm. **Deriva:** corda 341 mm, al massimo 680 mm sotto la chiglia, spessore al massimo 33 mm. Peso dello scafo, vela e lunghezze stanno nel manuale di costruzione, non in queste regole. I «78°» della C.8.3 sono l'inclinazione della pala sulla testa del timone, non l'angolo di barra.
- **F17** (Day 2017, eq. 11-12, già in `fonti-pdf/`): pendenza della portanza di deriva e pala `5,7·A/(1,8 + √(A² + 4))` con allungamento efficace `A = 2·b/c` (lo scafo fa da specchio), aumento per lo scafo `1 + 1,8·Tc/b`, acqua sulla pala al 90% della velocità della barca.
- **F4 / F35** (470): pala del 470 0,675 × 0,25 m = 0,169 m², da cui oggi `dragK` = 184.

## Conti di controllo (stime con le misure sopra; pala immersa = bordo d'uscita, 0,527 m, stima; pescaggio dello scafo `Tc` 0,15 m, stima)

| Cosa | Dalla fonte | Nel motore | Esito |
|---|---|---|---|
| Area della pala | 0,107 m² (0,63 di quella del 470) | `dragK` 184 tarato sul 470 | **da scalare: 117** |
| Autorità della pala `yawG` (1/m²), `Izz` 130-300, con e senza effetto dello scafo | 1,1-4,0 (2,6 col valore centrale di `Izz` 200 e l'effetto dello scafo, 1,7 senza) | 1,5 | dentro la fascia, sul lato basso |
| Distanza della pala dal centro di rotazione `xR` | circa 2,1-2,3 m (metà scafo più un quarto della corda; il punto di spinta della deriva del 470 è 0,2 m davanti al centro, F4) | 1,9 | stima più corta; la posizione della deriva non è nelle regole |
| Profondità efficace per la resistenza indotta `TE` | scafo 0,15 + deriva 0,68 = circa 0,83 m | 0,80 (ipotesi tarata nella 1.0.11) | **conferma** |
| Attrito di deriva e pala `appDA` (attrito ITTC 1957 più fattore di forma, spessore 10% della corda) | 0,0044-0,0048 m² (2,3 e 1,5 m/s) | 0,0049 (Day 2017, fig. 11) | **conferma** |
| Scarroccio di bolina (6 / 10 / 15 nodi) | 2,4 / 2,9 / 4,1° con deriva e pala (2,8 / 3,5 / 5,0° con la sola deriva) | 1,8 / 1,6 / 1,9° (`foilK` 520) | **il gioco scarroccia circa la metà** |

## Proposta
1. **`dragK` da 184 a 117**, scalato con l'area della pala (solo barca dell'1b, `RUD2`). Non è una taratura: è la stessa misura di F4 riportata alla pala di questa barca. Anteprima (motore fuori dal gioco, gesto da tastiera, `tests/fisica/virata1b.js`): freccia 4,0 / 2,8 / 2,5 / 2,7 s con 6 / 10 / 14 / 16 nodi, minima 55 / 51 / 44 / **36%**: **a 16 nodi la virata rientra** nel criterio della 1.0.43 (era 34%). La pala frena un po' meno in ogni manovra.
2. **`yawG`, `TE`, `appDA`: nessun cambio.** I primi due conti confermano i valori di oggi; `yawG` sta nella fascia (che è larga perché `Izz` è una stima).
3. **`xR`: nessun cambio, limite dichiarato.** Con la posizione della deriva sconosciuta il conto non è più preciso della stima di oggi.
4. **Scarroccio: da decidere (Ale).** `foilK` è in comune con l'1a, che è congelata: cambiarlo per la sola 1b vuol dire un ramo nuovo nel motore (la forza laterale della deriva calcolata con F17, come per la pala). Con il doppio di scarroccio la barca stringe meno il vento: la bolina, già più lenta delle fonti con poco vento (limite dichiarato), perderebbe circa il 2-3% di guadagno al vento [stima, da misurare]. Consiglio: **passo separato, dopo il punto 1**, con la sua fermata 1 e il confronto con la VMG di bolina di F24 e di F17.

## Criteri per il punto 1 (attese nostre, scritte prima)
1. Virata della 1.0.43 (criterio 1: freccia 2,5-3,5 s con 8-16 nodi, al massimo 4,5 s con 6, minima 35-60%, prua non oltre 60°) su tutti i venti 6-16 nodi. I numeri dell'anteprima sopra li ho già visti: **non sono una prova alla cieca**, lo dichiaro.
2. 1a identica: `polare.js`, `raffiche_e_virate.js`, `retromarcia.js`, `angolo_morto.js` carattere per carattere (`dragK` di `RUD2` vale solo nell'1b).
3. Riportati senza soglia: `timone2.js` (C1-C9, giri di penalità), `salti2.js`, `boma2.js`; nel browser `collaudo_timone2.py`, `collaudo_salti2.py`, `collaudo_torneo.py --veloce`, `collaudo_semaforo.py`, `collaudo_contatto_vero.py`.

## Rischi
- La pala frena meno anche nelle correzioni piccole: la barca dell'1b sarà un filo più veloce nelle regate con molte manovre. Lo misuro sui tempi del torneo col pilota.
- Il tratto immerso della pala (0,527 m) è una stima: con il bordo d'attacco intero (0,635 m) l'area sarebbe 0,129 m² e `dragK` 141. Riporto la sensibilità.

## Decisione di Ale e fermata 2 (23 ottobre 2026): punto 1 fatto, versione 1.0.44
Ale: «sì punto 1, lo scarroccio come passo dopo». `dragK` 117 nel motore; criterio 1 ok su tutti i venti; 1a identica; `salti2.js` tutto nelle soglie. Numeri e collaudi nel `CHANGELOG.md`, 1.0.44. **Prossimo: lo scarroccio dell'1b** (punto 4), con la sua fermata 1.

## Ordine deciso da Ale (23 ottobre 2026) prima del congelamento della barca dell'1b
1. Scarroccio dell'1b (punto 4 sopra), con la sua fermata 1. **Fatto: 1.0.45** (`PROPOSTA-SCARROCCIO-1B.md`).
2. **Barca orziera sbandando** (F38, F4), con la sua fermata 1: il termine deve valere zero a barca dritta (rischio del 4 ottobre, `VISIONE-LIVELLI-E-CARRIERA.md`).
3. Congelamento della barca, poi le regole 15 e 16 (T e G da rimisurare se la barca cambia ancora).
