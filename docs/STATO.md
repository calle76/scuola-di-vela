# A che punto siamo

**Da leggere per primo, in ogni sessione e in ogni chat.** Una pagina sola: si aggiorna a ogni fine lavoro (8 novembre 2026, decisione di Ale). Le cose da fare, in ordine, sono in `DA-FARE.md`.

*Aggiornato: 10 novembre 2026, sera.*

## Versione

- **Ultima versione chiusa: 1.2.27** (tag `v1.2.27`, da pushare: avversario che rimbalzava per sempre vicino alla boa, `PROPOSTA-BOA-PIANTATA.md` §12-13). Prima: 1.2.26 (tag `v1.2.26`; 11 novembre: lezione 11 sui salti di vento riscritta e col suggerimento «sei scarso di N°», segnalata da Ale perché non si capiva e l'esercizio non si superava; pilota 10/10). Prima: 1.2.25 (tag `v1.2.25`). Novità nel `CHANGELOG.md`.
- **Online** (https://calle76.github.io/scuola-di-vela/): quella dell'ultimo push di Ale. La 1.2.18 e i 123 tag sono pushati (8 novembre sera).
- Il livello in gioco è la **Scuola** (1b, barca con la sola randa); **Deriva** è in attesa (`DA-FARE.md`).

## Cosa aspetta Ale

- **Giocare la 1.2.16-1.2.18 e mandare le registrazioni** («Scarica l'ultima regata»; note con «#» nel file): giri di penalità senza limite di 20 s, orologio dei giri, avversari che scontano subito, squalifica per i giri non fatti.
- **Il giro dei collaudi su GitHub** della 1.2.18 (scheda Actions → «Collaudi» → «Run workflow», completo), poi gli zip nella cartella del repo.
- **L'ordine delle cose da fare** in `DA-FARE.md`.

## Cosa è stato fatto l'8 novembre

- 1.2.16: giri di penalità del giocatore senza limite di 20 s (riparte dopo 8 s fermi); squalifica per i giri non fatti; lezione 20 aggiornata.
- 1.2.17: orologio dei giri nel riquadro (rosso che si riempie di verde, «0/2»).
- 1.2.18: avversari che scontano subito, anche prima del via, scostandosi il minimo; squalifica anche per loro.
- Proposta «coppie che si tengono»: chiusa senza correzione (`PROPOSTA-COPPIE.md` §12).
- Tag di versione per tutte le versioni dalla 0.18; release e issue su GitHub rifiutate (`DECISIONI.md`).

## Cosa è stato fatto l'8 novembre, notte

- Lette le 6 regate di Ale dell'8 sera (1.2.18, Chromium, 8 marcatori M): osservazioni 100-107 in `OSSERVAZIONI-GIOCANDO.md`, voci 2-5 e 14 di `DA-FARE.md` (ordine deciso da Claude su delega di Ale). File spostati in `registrazioni/`.
- Proposta partenza (`PROPOSTA-PARTENZA-ESTREMITA.md`), fermata 2: **non adottata**. Il riposizionamento in attesa toglie quasi tutte le barche oltre l'estremità allo sparo (conferma: 316 → 41 su 2160), ma i contatti salgono del 15% contro una soglia del 10%. Strumento nuovo: `tests/misura_partenza_estremita.py`.

## Cosa è stato fatto il 9 novembre, mattina

- Decisione di Ale: gli avversari si migliorano per le regate da Deriva in poi, cioè il torneo (`DECISIONI.md`).
- **1.2.19**: in attesa del via gli avversari non scivolano più oltre lo spillo. Nel torneo le barche oltre l'estremità allo sparo passano dal 14,3% al 2,0%, i contatti salgono del 6,2% (`PROPOSTA-PARTENZA-ESTREMITA.md` §10-13).
- Osservazioni 108-109: due regate dei giri dell'8 sera.
- **1.2.20**: gli avversari non si piantano più a destra della prima boa («giro diretto»). Nel torneo, conferma sui semi 891-920: fermate vicino alla boa 70 → 30, boa toccata 49 → 49, contatti 259 → 253 (`PROPOSTA-BOA-PIANTATA.md` §8-10). La prima prova (allargare le soglie) non era passata.

## Cosa è stato fatto il 9 novembre, pomeriggio

- Decisione di Ale: nelle regate non didattiche la fisica c'è tutta (raffiche e salti insieme, poi il cono d'ombra); il tipo di gara lo dice il formato. Le regate a tema restano didattiche.
- **1.2.21**: torneo ampliato. Regate 1-2 col punteggio, 3-4 coi giri di penalità, vento sempre misto. Avversari squalificati 0,3-1,4%, contatti per regata da −26% a +9% (`PROPOSTA-TORNEO-AMPLIATO.md` §7).
- Ricerca sul cono d'ombra: la letteratura c'è (F75, F76; `RICERCA-CONO-D-OMBRA.md`).
- **1.2.22**: rotta ottimale a regata finita (fuori dalla Scuola), con le layline e «dove hai perso». Mai più lenta di una barca vera su 1821 casi, calcolo circa 1 s (`PROPOSTA-ROTTA-OTTIMALE.md` §8). Nella stessa versione due difetti trovati dai collaudi: avversari bloccati nella regata nelle raffiche (dalla 1.2.20, `PROPOSTA-BOA-PIANTATA.md` §11) e prua della moviola alla raddrizzata (dalla 1.2.21).
- Decisioni di Ale: layline in quattro pezzi (il primo è nella 1.2.22), VMG come idea in Deriva e come strumento con Tattica, nomi dei livelli «Gennaker» e «Tattica».

## Cosa è stato fatto il 9 novembre, sera

- **1.2.23**: layline in acqua, disattivabile (riga «Layline» nelle impostazioni; nel torneo parte spenta). Gli avversari con la layline misurati e non adottati (virate −6% al massimo, soglia −10%). Lezione della layline scritta per Deriva (`PROPOSTA-LAYLINE.md`).
- Letto il giro su GitHub della 1.2.22: niente di nuovo tranne `collaudo_segnali` G2 in Firefox (il collaudo aveva troppe poche regate senza richiamo: corretto il collaudo, non il gioco) e la voce vecchia di `collaudo_partenze` in `tests/fallimenti_noti.txt` (aggiornata).

## Cosa è stato fatto la notte fra il 9 e il 10 novembre

- Diagnosi degli avversari con la rotta ottimale (`PROPOSTA-AVVERSARI-ROTTA.md`): la bolina pesa il 64% del tempo perso, la poppa il 15%.
- **1.2.24**: avversari in poppa all'angolo della polare (poppa persi −41% in conferma); layline in acqua lunghe metà bolina (osservazione 110); «layline» nell'intestazione della registrazione.
- Osservazioni 110-113 dalle regate di Ale del 9 sera (layline, partenza di Rossa, confusione alla boa 1 nel triangolo).
- Proposta bolina (`PROPOSTA-AVVERSARI-BOLINA.md`, virare sugli scarsi): **non adottata**. Al meglio −14,6% di tempo perso in bolina contro la soglia di −15%; la seconda prova dichiarata va peggio. Patch in `sperimentale/avversari-bolina-scarsi/`. Proposto prima di altro: una diagnosi delle cause in bolina (virate alla boa, angolo dei principianti, regolazione della vela).

## Cosa è stato fatto il 10 novembre, mattina (avversari in bolina; il gioco resta la 1.2.24)

- **Diagnosi** (`PROPOSTA-AVVERSARI-BOLINA.md` §8):
  - gli ultimi 40 m prima della boa 1 sono il 41% del tempo perso nella prima bolina;
  - angolo e regolazione valgono il 18%, ma sono la differenza voluta fra livelli.
- **Provate e non adottate:**
  - giro diretto da più lontano (§9-10): nessun effetto;
  - correzione del rimbalzo fra punti di passaggio (§11-12): il difetto era vero ma non costava tempo, e in conferma peggiora.
- **Provata e non adottata anche la layline di dritta** (§13-14, semi 1431-1460): la regola scatta in quasi tutti i passaggi, ma peggiora tutto (ultimi 40 m 11,1 → 12,8-13,0 s, arrivo +2,5-3,5 s, boa toccata 22 → 44-55). Chi arriva da sinistra incrocia la layline quasi sul punto 0: non c'era niente da anticipare. Patch in `sperimentale/avversari-layline-dritta/`.
- **Ale: bolina degli avversari ferma** (`DECISIONI.md`); si riprende con nuove registrazioni. Pulizia di file e cartelle fatta (commit `907413c`).
- **Ale: il cono d'ombra prima degli avversari** (`DECISIONI.md`): guardiano → cono d'ombra → registrazioni di Ale e Lucio → avversari tutti insieme.
- **Collaudo guardiano degli avversari** (`PROPOSTA-GUARDIANO-AVVERSARI.md`, `tests/collaudo_guardiano_avversari.py`): 96 regate del torneo contro il riferimento della 1.2.24, circa 6 minuti, fra i lunghi. Boccia la poppa della 1.2.23 e la layline di dritta, lascia passare le modifiche neutre. Vede solo i peggioramenti grossi (il rumore sposta l'arrivo di circa 1 s).
- **Letto il giro su GitHub della 1.2.24** (10 novembre): niente del gioco. Tre collaudi:
  - `collaudo_moviola` in Firefox: il pilota resta indietro dopo un contatto e chiude fuori tempo, come succedeva in Chromium dalla 1.2.15. Voce dei fallimenti noti aggiornata.
  - `collaudo_registratore_barche` in Firefox «NON VALIDO»: nessuna barca ferma nelle regate vere, perché gli avversari non si piantano quasi più. Corretto il collaudo: le fermate le misurano i 10 casi costruiti.
  - `collaudo_suoni_si_sentono` in Chromium: boa e sartiame poco sopra o sotto la soglia, già aperto (`DA-FARE.md` voce 8).
- **Sessione sui collaudi** (Ale: prima del cono d'ombra):
  - sei collaudi che nessuno lanciava sono entrati nel giro (86 in tutto); `collaudo_triangolo` era rotto dalla 1.2.21 per un campo cambiato nel torneo, riparato; `collaudo_avversari_deriva` e il T2b del triangolo falliscono in modo noto dalla nascita;
  - `collaudo_moviola` V3 non dipende più dall'arrivo del pilota;
  - censimento dei collaudi che dipendono dal caso in fondo a `COLLAUDI.md`: resta stretto solo il V4 della moviola.
- **Giro completo su GitHub dopo la sessione** (10 novembre, 87 collaudi, 49 minuti, 1.2.24): **nessun fallito** nei due browser. Noti: partenze, virate2, triangolo T2b, avversari di Deriva. `collaudo_suoni_si_sentono` questa volta passa (boa 7,9-10,6 dB su 6; sartiame 2,2-4,8 su 2): resta ballerino, voce 8 aperta. Il guardiano in Firefox non è identico al bit al riferimento (scritto in Chromium) ma sta nelle soglie. È il punto di partenza per il cono d'ombra.
- **Esploratore:** ora gioca anche le 4 regate del torneo (regate 100-103). Aspetta il giro lungo di Ale su GitHub (semi 1-100, 4 scimmie da 600 s, due browser).
- **1.2.25, il cono d'ombra delle vele nel torneo** (`PROPOSTA-CONO-D-OMBRA.md` §10; via di Ale: «procedi fino alla fine»):
  - meno vento a chi è coperto, numeri da F75; cono disegnato sul mare, disattivabile (casella solo nel torneo); la fisica non si spegne; Scuola identica al bit;
  - criteri K1-K15 tutti passati; `tests/collaudo_cono.py` nuovo, nel giro;
  - **gli avversari non peggiorano:** su 576 regate arrivano circa 2 s prima (±0,6) e si toccano il 17% in meno; la causa non è dimostrata;
  - non reagiscono ancora al cono: arriva col lavoro sugli avversari.
- **Esploratore sulla 1.2.24** (giro su GitHub, 3200 corse e 8 scimmie, due browser): nessun errore, nessun numero rotto; nel torneo non arriva circa il 2% degli avversari (finestra d'arrivo chiusa o squalifica). È la fotografia di prima del cono.
- **Giro su GitHub e esploratore sulla 1.2.25 letti (11 novembre, zip nella cartella del repo, non committati):** 88 collaudi per browser, nessun fallito del gioco. Da registrare (voci 15-21 di `DA-FARE.md`): avversario fermo 753 s nella regata dei salti (Chromium, seme 28); nel torneo la regata coi giri (102) ha più non arrivati (3,5% e 2,8%) delle altre; suoni, sartiame 2,2/1,9/4,3 dB; T2b in Firefox confrontato troppo alla lettera; timone2 in Firefox errore di apertura di Playwright; lezioni 5.8 e 6.3 sopra la soglia. **Seguito (11 novembre):** T2b in Firefox: era il file dei noti scritto con i numeri del PC (139 su 173, in locale identico due volte di fila) mentre GitHub dà 135 su 173; aggiunta una seconda voce, verificata con `noti.py`. `timone2` in Firefox: passa 3 su 3 in locale, da guardare. Lezioni 5.8 (5 su 100) e 6.3: valori già noti (CHANGELOG 1.2.12; 6.3 a mani ferme è migliorata, 3 su 100 contro 18 su 80), non un problema. Lezione 11 nuova: 100/100 guidando, 0/100 a mani ferme. Voce 15 fatta (1.2.27: avversario fermo vicino alla boa, causa trovata e corretta; il pc è arrivato a 73 °C, misure fermate, campione di 9 semi). Restano le voci 16-18 e 20 di `DA-FARE.md`. Rumore noto: E2 e Q7 (misure di tempo su GitHub).
- **Aspetta Ale:** push, giro dei collaudi e dell'esploratore su GitHub sulla 1.2.25, e **giocare il torneo col cono** mandando le registrazioni (ora hanno gli eventi `coperta` e `libera`).
- **Poi:** gli avversari tutti insieme (bolina, boa, uscire dal vento sporco), con le registrazioni.

## Dove sta cosa

- Il gioco in una pagina: `IL-GIOCO.md`. Principi: `PROGETTO.md`. Metodo (due fermate, soglie prima): `METODO.md` e `CLAUDE.md`.
- Decisioni di Ale e quanto costa cambiarle: `DECISIONI.md`. Difetti visti giocando: `OSSERVAZIONI-GIOCANDO.md`. Collaudi: `COLLAUDI.md`. Fonti: `FONTI-PUBBLICHE.md`.
- Le proposte (`PROPOSTA-*.md`) hanno in fondo l'esito di ogni fermata.
- **Le registrazioni delle regate** (`regata-….txt`, scaricate da Ale e Lucio) stanno in `registrazioni/`, nella cartella del repo ma fuori da git (`.gitignore`). Le nuove si mettono lì. Le 8 regate intere usate da `tests/rigioca_regata.py`: 04/11 21:12, 06/11 15:50, 17:59, 18:33, 07/11 16:42, 16:55, 17:07, 17:25.
