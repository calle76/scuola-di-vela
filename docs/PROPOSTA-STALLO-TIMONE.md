# Proposta: il timone che va in stallo (livello 2)

Del 17 ottobre 2026. **Fermata 1: nessun codice nel motore.** Le misure sono fatte su una copia in memoria di `js/motore.js` (script nella cartella temporanea della sessione, non nel repository). Precedenti: `archivio/PROPOSTA-SATURAZIONE-TIMONE.md` e `archivio/RAPPORTO-PROVA-SATURAZIONE.md` (13 ottobre, prova non adottata).

Tipi delle affermazioni: **[fonte]** letto in una fonte citata; **[misura]** calcolato sul motore; **[stima]** ragionamento senza misura; **[a occhio]** letto da un grafico, senza i dati.

---

## 0. In breve

1. **Le fonti ora sono due, e vere.** F4 (Masuyama e Ogihara 2020, ora letta per intero) misura in vasca lo stallo a circa 15° su un modellino 1:5; F35 (calcolo al computer a grandezza vera, 2018) lo trova a 30° (35° con 10 m/s). Tutte e due a barca dritta. La differenza è plausibile per la scala [stima], quindi lo stallo vero a barca dritta sta **fra 15° e 30°**, senza una preferenza dichiarabile (revisione in chat, §7).
2. **Le virate vere usano 45° di barra.** F4 misura virate di un 470 vero: la barra va fino a 45°, e accompagnata è il modo migliore; data di colpo fa perdere più velocità; fermata a 30° fa virare più lentamente. Si può perché, quando la barca gira, l'acqua arriva sulla pala già di traverso e la pala «sente» meno angolo di quello della barra (Day 2017, angolo effettivo).
3. **Misura principale: oggi lo stallo, aggiunto da solo, non cambierebbe quasi niente.** Il motore fa girare la barca subito (la rotazione insegue la barra in circa 0,25 s), quindi la pala non supera mai a lungo l'angolo di stallo. Con la barra da tastiera, che arriva a fondo in 0,63 s, **non stalla mai**, nemmeno con lo stallo a 15° [misura, §4].
4. **Il motore gira da 2 a 3 volte più stretto di un 470 vero**, sulla curvatura media della virata (0,33-0,46 contro 0,11-0,23 rad/m) [misura; lettura delle figure di F4, §7]. La prima stesura diceva «3 volte» confrontando un massimo con una media.
5. **Quindi la scelta vera non è «stallo sì o no», ma se ritarare la manovrabilità della barca** (quanto in fretta comincia a girare e quanto stretto gira) sulle virate misurate. È un lavoro più grosso: tocca tutte le virate, le prove, gli avversari, le lezioni. Due strade nel §5; decide Ale.

---

## 1. Le fonti

**F4** — Masuyama Y., Ogihara T., «Science of the 470 Sailing Performance», *Journal of Sailing Technology* 5(1), 2020, pp. 20-46 (`fonti-pdf/sname-jst-2020-05.pdf`). Finora letta da una copia senza figure; il PDF ora è in `fonti-pdf/`.
- Vasca, modellino 1:5 del 470, scafo trainato dritto [fonte]: forza laterale e momento del timone crescono fino a circa ±15° di barra, poi restano costanti; la resistenza continua a crescere. **Resistenza** dovuta alla barra (non forza laterale: nel testo «this drag»), a 6 nodi: 5 kgf a 10° e 12 kgf a 15°, contro 19 kgf di resistenza totale della barca dritta.
- Virate di un 470 vero, misurate (figure 5 e 6, tre virate per verso, barca a 6-7 nodi con 12-14 nodi di vento) [fonte]: rosso, barra accompagnata fino a 45°; blu, barra data in fretta fino a 45°; verde, barra accompagnata fino a 30°. Conclusioni degli autori: il blu perde più velocità; il verde resta più a lungo con la prua al vento e può perderne di più; il rosso è il modo più ragionevole.
- Dalle figure [a occhio; letture più attente nel §7]: la prua passa da una bolina all'altra (circa 80-90°) in circa 3 s; la velocità scende da circa 7 a circa 3 nodi (blu fino a 2-3, rosso circa 3, verde circa 3); torna sopra 6 nodi in circa 8-10 s. Il verde impiega circa 1-2 s in più a girare.

**F35** — «Investigation on Rudder Hydrodynamics for 470», *Proceedings* (MDPI) 2(6):308, 2018, ad accesso libero (`fonti-pdf/proceedings-02-00308-v2.pdf`). Calcolo al computer di scafo e timone del 470 a grandezza vera, barca dritta, 280 kg, pala 0,675 × 0,25 m.
- Stallo a **30°** di barra fra 2 e 8 m/s; a 10 m/s 35°, perché la scia dello scafo scopre parte della pala [fonte].
- Rapporto portanza/resistenza migliore fra 10° e 25° di barra [fonte].
- Nessun confronto con misure dichiarato nel testo [fonte]: è una simulazione.

**Day 2017** (`fonti-pdf/day2017/`, §3.3): l'angolo che la pala sente non è quello della barra; si sottraggono scarroccio e deviazione dell'acqua portata dalla deriva [fonte]. La parte dovuta alla rotazione della barca è un'aggiunta nostra, fisica di base [stima].

**Il 13 ottobre** la frase «stallo a 30-35°» era stata tolta dai documenti perché senza fonte, forse scritta da un'IA. F35 è una fonte vera con quei numeri; la frase di allora resta comunque senza provenienza.

**Barca diversa:** tutte e due le fonti riguardano un 470 (4,7 m, a due, circa 280 kg). Il gioco è una deriva singola da 4,2 m e 135 kg. I numeri servono per l'ordine di grandezza e per il comportamento, non per tarare cifra per cifra.

---

## 2. Il motore di oggi [codice]

`js/motore.js`: la barra va da −30° a +30° (`maxRudder`). La rotazione voluta è `velocità / turnLen × seno(angolo della barra)` con `turnLen` = 1,05 m; quella vera la insegue con `yawK` = 4 al secondo (circa 0,25 s). Nessuna delle due costanti ha fonte. La resistenza della barra cresce col quadrato del seno dell'angolo (`rudderDragK` 45), senza stallo. Da tastiera la barra cresce di 1,6 al secondo (`js/gioco.js`, riga 649): a fondo in 0,63 s.

Questa formula equivale a una pala che lavora sempre ad angolo effettivo quasi zero a virata avviata [stima]: per questo la pala «non stalla mai» non solo per scelta, ma per costruzione.

---

## 3. Oggi contro le virate vere [misura]

Bolina a regime, scotta 0,1, poi barra. «Virata» = prua da 45° a −44° dal vento.

| Vento | Barra | Virata | Velocità minima (entrata) | Curvatura massima |
|---|---|---|---|---|
| 6 nodi | a fondo di colpo | 3,23 s | 1,5 nodi (2,9) | 0,51 rad/m |
| 6 nodi | a fondo in 1,5 s | 3,98 s | 1,5 | 0,51 |
| 6 nodi | a metà, di colpo | 6,97 s | 1,2 | 0,26 |
| 10 nodi | a fondo di colpo | 2,23 s | 2,2 (4,4) | 0,53 |
| 10 nodi | a fondo in 1,5 s | 3,04 s | 2,1 | 0,52 |
| 10 nodi | a metà, di colpo | 4,90 s | 1,6 | 0,27 |
| 14 nodi | a fondo di colpo | 1,87 s | 2,5 (5,6) | 0,55 |
| 14 nodi | a fondo in 1,5 s | 2,74 s | 2,3 | 0,55 |
| 14 nodi | a metà, di colpo | 4,35 s | 1,6 | 0,28 |

Confronto con F4 [a occhio]:
- **Barra di colpo:** nel gioco è la virata più rapida e perde la stessa velocità della barra accompagnata; nel 470 vero perde più velocità. **Contro la fonte.**
- **Barra a metà:** nel gioco vira molto più lentamente e perde più velocità, come il verde di F4. **D'accordo.**
- **Curvatura:** 0,52 contro circa 0,18 rad/m (80° in circa 3 s a una media di circa 5 nodi): *(superato dal §7: confronto fra un massimo e una media; sulle medie il fattore è 2-3)*. In parte la barca è più corta e leggera, ma 3 volte è molto [stima].
- **Durata:** la virata del gioco (2-3 s) è vicina a quella del 470 (circa 3 s) e ai video già usati (circa 3,3 s, virata chiusa da Ale). Il gioco ci arriva girando più stretto ma andando più piano.

---

## 4. Lo stallo aggiunto da solo [misura]

Variante in memoria: l'angolo che la pala sente (barra meno l'angolo dell'acqua dovuto alla rotazione) non può superare l'angolo di stallo; oltre, la rotazione non cresce più (come in F4: la forza resta costante). Resistenza invariata. All'indietro nessun cambio. Con la barra al centro è identica a oggi.

| Stallo a | Virata 10 nodi, di colpo | Tempo in stallo | Virata con barra in 0,5 s | Tempo in stallo |
|---|---|---|---|---|
| nessuno | 2,23 s | — | 2,47 s | — |
| 25° | 2,24 s | 0,06 s | 2,47 s | 0 |
| 20° | 2,27 s | 0,13 s | 2,47 s | 0 |
| 15° | 2,33 s | 0,27 s | 2,47 s | 0 |

Stessa cosa con 6 e 14 nodi (differenze fino a 0,09 s). **Con la barra da tastiera (a fondo in 0,63 s) la pala non stalla mai.** Il motivo: la rotazione insegue la barra in 0,25 s, quindi l'acqua sulla pala si gira quasi subito. Nel 470 vero (F4) la velocità di rotazione cresce in circa 1-2 s [a occhio]: è quel ritardo che fa stallare la pala quando la barra è data di colpo.

---

## 5. Due strade

### Strada A — Ritarare la manovrabilità, con lo stallo dentro (consigliata se il livello 2 deve avere i giri di penalità veri)

Modello più semplice plausibile [stima]:
1. la pala sente l'angolo effettivo (barra meno rotazione), come nella variante del §4;
2. oltre l'angolo di stallo la forza resta costante e la resistenza cresce (F4);
3. la rotazione della barca cresce più lentamente (`yawK` più basso) e la barca gira meno stretta (`turnLen` più lungo), tarati sulle virate di F4;
4. la barra va fino a 45° invece di 30°, come nel 470 vero.

**Costanti nuove o cambiate, tutte ipotesi da tarare:** angolo di stallo (fra 15° e 30°, le due fonti; da scegliere su un gruppo di casi e confermare su un altro), `yawK`, `turnLen`, `maxRudder`, eventuale aumento della resistenza dopo lo stallo.

**Criteri misurabili** (attese nostre, dichiarate prima di misurare; virata = prua da 45° a −44°, vento 10 e 14 nodi):
- C1. Barra di colpo (in 0,1 s) contro barra da tastiera (0,63 s): velocità minima più bassa di almeno 0,3 nodi (F4, blu contro rosso).
- C2. Barra da tastiera fino a 30° contro barra da tastiera a fondo: la virata dura almeno il 20% in più (F4, verde contro rosso).
- C3. Curvatura massima fra 0,15 e 0,35 rad/m (F4 circa 0,18; barca più corta, tetto più largo).
- C4. Durata della virata con la barra da tastiera fra 2,5 e 4,0 s con 10 nodi (F4 circa 3 s; video circa 3,3 s).
- C5. Velocità minima in virata fra il 35% e il 60% di quella d'entrata (F4 circa 3 su 7, cioè circa 43%).
- C6. Non-regressione: `polare.js` e la parte raffiche di `raffiche_e_virate.js` identiche carattere per carattere (barra al centro).

**Costo:** cambiano tutte le virate e le strambate, quindi i tempi delle prove (fasce da ritarare, record azzerati), gli avversari (guida in `js/regate.js` da ritoccare), il pilota dei collaudi e le lezioni 2 e 5 (passi da ricontrollare: il 13 ottobre una barca più sensibile bloccava la lezione 5). Riapre il livello 1, che oggi è chiuso. Revisione in chat prima della fermata 2.

**Rischio principale:** la barca diventa più pigra da girare. Il 13 ottobre la strada «senza compensazione» aveva reso le virate lente fino a non riuscire con 6 nodi; qui la taratura è sulle virate vere, ma va controllato subito su tutti e tre i venti.

### Strada B — Rinviare

Si dichiara come limite noto: «la pala non stalla mai, e la barca risponde alla barra più in fretta e gira più stretta di una deriva vera (F4)». Nel livello 2 le penalità a giri si fanno lo stesso, ma senza la lezione «non sbattere la barra». Costo zero, si va avanti con «spingi il boma» e i salti di vento.

---

## 6. Decisioni che spettano ad Ale

1. Strada A o strada B.
2. Se A: va bene riaprire tempi, fasce, record e avversari del livello 1? Oppure la barca nuova vale **solo dal livello 2** (il livello 1 tiene la sua barca, come i record)? La seconda è coerente con «ogni livello ha la sua fisica» (`VISIONE-LIVELLI-E-CARRIERA.md` §8), ma vuol dire due barche da mantenere.

**Decisione di Ale (17 ottobre 2026): strada A, solo per il livello 2.** «La barca del primo livello insegnava manovre più semplici… Il primo livello è per capire le cose basilari. Nel secondo hai comportamenti più realistici.» Il livello 1 tiene la sua barca **identica al bit** (impronta e collaudi di oggi come controllo); il livello 2 usa lo stesso motore con le costanti del timone ritarate. La differenza va dichiarata (principio 4): nel livello 1 la barca risponde alla barra più in fretta e gira più stretta di una deriva vera, per scelta didattica.


---

## 7. Revisione in chat (17 ottobre 2026) e cosa ne segue

La chat ha letto la proposta (non F4). Accolte quasi tutte le osservazioni; quelle verificate qui sono segnate.

**Fonti.**
- Stallo fra 15° e 30° **senza preferenza**: il modellino stalla prima (numero di Reynolds circa 11 volte più basso), il calcolo al computer tende a stallare dopo. **Accolto.** Proposta: angolo di stallo fissato prima di misurare, 22°, e sensibilità dei criteri riportata a 15° e 30°.
- I 5 e 12 kgf sono resistenza: **verificato** sul PDF (§1 corretto). Servono per tarare la resistenza dopo lo stallo, non la forza.
- I due angoli di stallo sono angoli di barra a barca dritta, non «angoli a cui la barca stalla navigando». **Accolto.**
- La virata di un 470 contiene il lavoro di due persone (rollio, fiocco) che il gioco non ha: perdita e ripresa di velocità non dipendono solo dal timone. **Accolto**: pesa su C4 e C5.
- Momento d'inerzia della barca del gioco circa 1/2,5 di quello del 470: è giusto che cominci a girare più in fretta. **Accolto.** Da cercare: virate misurate su una deriva singola di quella taglia (fonte ancora da trovare).

**Letture delle figure 5 e 6 di F4** (ingrandite sulla griglia; una virata per caso; precisione circa ±1 s e ±5°; la lettura automatica per colore è stata scartata perché la legenda colorata dentro i grafici falsava i minimi):

| Virata | Barra: da 0 al massimo | Velocità della barra | Prua da una bolina all'altra | Curvatura media | Velocità minima / entrata |
|---|---|---|---|---|---|
| Fig. 5 rosso (accompagnata, 45°) | 0 → 41° in circa 3 s | circa 14°/s | circa 82° in 3,4 s | circa 0,16 rad/m | 3,2 / 7,4 nodi (43%) |
| Fig. 5 blu (in fretta, 45°) | 0 → 35° in circa 1 s, poi 47° | circa 35°/s | circa 90° in 2,9 s, con un tratto molto ripido | circa 0,23 rad/m | 2,8 / 6,6 (42%) |
| Fig. 5 verde (accompagnata, 30°) | 0 → 25-30° in circa 3,5 s | circa 8°/s | circa 85° in 5 s | circa 0,11 rad/m | 3,3 / 6,2 (53%) |
| Fig. 6 (tre colori) | come sopra | | | | rosso 44%, blu 29%, verde 42% |

Cosa dicono: il blu gira più in fretta ma in una figura su due perde molta più velocità; il verde gira più lentamente. La differenza fra rosso e blu nella perdita di velocità c'è solo nella figura 6: **una virata per caso non basta per un criterio stretto.**

**Motore di oggi, stessa misura** (prua da 40° a −40°, curvatura media) [misura]:

| Vento | Barra | Durata | Curvatura media | Minima / entrata |
|---|---|---|---|---|
| 10 nodi | tastiera (a fondo in 0,63 s, 48°/s) | 1,94 s | 0,46 rad/m | 50% |
| 10 nodi | 14°/s, come il rosso | 2,52 s | 0,36 | 45% |
| 10 nodi | 35°/s, come il blu | 2,01 s | 0,44 | 50% |
| 14 nodi | tastiera | 1,65 s | 0,45 | 45% |
| 14 nodi | 14°/s | 2,34 s | 0,33 | 37% |

Nel gioco la barra accompagnata perde **più** velocità di quella data in fretta: il contrario di F4 (figura 6).

**Criteri, corretti.**
- C4 e C5 sono già rispettati oggi: diventano vincoli di **non peggioramento**, non prove che il modello funziona.
- C1 in frazione della velocità d'entrata, non in nodi; e prima va deciso quale gesto da tastiera corrisponde al rosso e quale al blu (vedi sotto: la tastiera oggi è più veloce anche del blu).
- C3 sulla curvatura **media** (gradi di prua diviso metri percorsi), per gioco e fonte allo stesso modo.
- C6 allargato: **tutto il livello 1 identico al bit** (impronta e tutti i collaudi del livello 1). `polare.js` tiene davvero la barra a 0 esatto [codice, riga 9].
- Criteri nuovi: giro di penalità (durata e velocità all'uscita, serve una fonte o un video); virata riuscita con 6 nodi entrando al 70% della velocità di bolina; strambata; risposta a 5° di barra e tenuta di rotta (una barca più lenta a rispondere invita a correggere troppo); prova a mano di Ale: una virata accompagnata da tastiera si sente migliore di una sbattuta?

**Modello.**
- Va detto chiaramente: nella strada A la rotazione si calcola **sempre** dall'angolo effettivo della pala, non solo come tetto. Allora serve la distanza fra pala e centro di rotazione (costante geometrica, dal disegno della barca); a regime `turnLen` e questa distanza non sono separabili: si introduce prima l'angolo effettivo, si misura, e solo dopo si decide se `turnLen` serve ancora. **Accolto.**
- Quell'anello accorcia il tempo di risposta invece di allungarlo [stima della chat: circa 0,09 s invece di 0,25]: `yawK` va abbassato più di quanto sembri. Da misurare, anche col passo di calcolo variabile del browser.
- La resistenza della barra va calcolata sull'angolo effettivo, con l'aumento dopo lo stallo: altrimenti ogni virata a 45° costa uguale, accompagnata o no, e C2 si può invertire. **Accolto**: è proprio il meccanismo da insegnare.
- Forza costante dopo lo stallo, senza isteresi: semplificazione voluta, da dichiarare. Ordine: prima angolo effettivo e stallo, poi i 45°.
- Velocità vicina a zero e marcia indietro: serve un minimo sulla velocità; all'indietro con 45° la barca cambia comunque, va misurato (`angolo_morto.js`).

**Rischi nuovi.**
- **Il gesto con la tastiera** (il più importante): oggi un tasto tenuto porta la barra a fondo in 0,63 s, cioè 48°/s; con 45° sarebbero 72°/s, più veloce anche del blu di F4 (circa 35°/s). La scelta naturale sarebbe quella sbagliata. Va deciso **prima di tarare** come chi gioca dosa la velocità della barra.
- **Lo stallo va reso visibile o udibile**: nella realtà si sente dalla barra che si alleggerisce; senza un segnale si vede solo «la barca è più lenta».
- **Il livello 1 premia l'abitudine che il livello 2 punisce** (barra sbattuta = virata più rapida e senza costi): va spiegato nel gioco, nella lezione del livello 2, non solo nei documenti.
- **Identità al bit del livello 1 con codice in comune**: il ramo del livello 1 resta scritto com'è, testualmente; impronta confrontata prima e dopo ogni modifica.

**Costo, aggiornato dopo la decisione «solo livello 2»:** due insiemi di costanti; pilota dei collaudi tarato due volte; avversari del livello 2 che accompagnano la barra; disegno e indicatore della barra fino a 45°; durata dei giri di penalità. Il livello 1 non si riapre.

**Decisione di Ale (17 ottobre 2026): gesto A.** Nel livello 2 la freccia tenuta muove la barra piano, circa come la virata accompagnata di F4 (circa 15°/s: a fondo, 45°, in circa 3 s); **Maiusc + freccia** la muove in fretta, da quando si preme Maiusc. Maiusc oggi non è usato dal gioco [codice]. Da decidere in fermata 2, con i numeri: la velocità esatta con Maiusc (oggi 48°/s), e cosa fanno nel livello 2 la barra trascinata col mouse (`dragTiller`, può muoverla di colpo) e l'aiuto «la barra torna al centro».

---

## 8. Fermata 2: cosa è stato fatto e cosa è uscito (17 ottobre 2026, versione 1.0.24)

**Fatto.**
- `js/motore.js`: timone del livello 2 (`RUD2`, `rud2Alpha`), solo per una barca con `S.lv === 2` che va avanti ad almeno 0,5 m/s. La pala sente l'angolo effettivo (barra meno l'acqua che le arriva di traverso perché la barca gira, con la pala a `xR` = 1,9 m dal centro di rotazione, stima); oltre `stallA` = 22° la forza resta quella dello stallo; la rotazione nasce dalla forza della pala, `dr/dt = −yawG·u·(u·F + yawRho·r)`; la resistenza della pala usa l'angolo effettivo con `dragK` = 184 (F4: 12 kgf a 15° e 6 nodi; continua a crescere dopo lo stallo, come in F4); la barra arriva a 45°. Sotto 0,5 m/s e all'indietro resta il timone del livello 1 (barra fino a 30°): la retromarcia e l'uscita dall'angolo morto non cambiano.
- **Il livello 1 è identico al bit:** impronta del gioco 63 scene su 63 uguali al riferimento salvato prima di toccare il codice; `polare.js`, `raffiche_e_virate.js`, `retromarcia.js`, `raffiche_portanti.js`, `bolina.js` uguali carattere per carattere.
- Nel gioco, **solo in prova**: nelle impostazioni della navigazione libera la scelta «Barca: livello 1 / livello 2 (prova)». Con la barca del livello 2 la freccia muove la barra a 20°/s, **Maiusc + freccia** a 1,6 della corsa al secondo (come nel livello 1); il cursore trascinato col mouse non va più veloce di Maiusc; quando la pala stalla il suggerimento lo dice. Il livello 2 come schermata non esiste ancora.
- Misure: `tests/fisica/timone2.js` (criteri, sensibilità, griglia di taratura); `tests/collaudo_timone2.py` nel browser (dentro `lancia_tutti.sh`).

**Due scelte fatte durante la taratura, dichiarate.**
- **Barra lenta a 20°/s invece di circa 15°/s.** Con 15°/s la virata durava da 5 a 9 s su tutta la griglia (C4 fuori ovunque): la barca del gioco perde velocità prima che la barra arrivi a fondo. 20°/s sta fra il rosso (circa 14) e il blu (circa 35) di F4.
- **C3 tolto dalla scelta dei valori**, prima della conferma: con una curvatura media sotto 0,30 rad/m (quella del 470) nessuna combinazione teneva insieme virata entro 4,5 s e velocità minima sopra il 35%. La barca del gioco pesa la metà del 470 e frena circa il doppio più in fretta (come aveva previsto la revisione in chat). Regola di scelta fissata prima della conferma: più criteri superati fra C1, C2, C4 e C5 con 10 e 14 nodi, a parità la curvatura più bassa. Scelti `yawG` 0,6 e `yawRho` 0 (lo smorzamento dello scafo risulta zero: la rotazione la frena solo la pala).

**Risultati** (`node timone2.js`; venti di taratura 10 e 14 nodi, di conferma 6, 8, 12 e 16 mai guardati):

| Criterio | 10 | 14 | 6 | 8 | 12 | 16 |
|---|---|---|---|---|---|---|
| C1 la barra veloce perde almeno 5 punti in più | ok (45 contro 38%) | ok (43 / 36) | **fuori** (34 / 33) | **fuori** (39 / 35) | ok (47 / 40) | **fuori** (38 / 41) |
| C2 fermarsi a 30° allunga almeno del 20% | ok (+21%) | **fuori** (+17%) | ok | ok | **fuori** (+19%) | **fuori** (+19%) |
| C3 curvatura media 0,12-0,30 rad/m | **fuori** (0,34) | **fuori** (0,32) | **fuori** (0,39) | **fuori** (0,36) | **fuori** (0,33) | **fuori** (0,33) |
| C4 virata lenta 2,5-4,5 s | ok (3,60) | ok (3,23) | **fuori** (4,73) | ok (3,99) | ok (3,39) | ok (3,39) |
| C5 minima 35-60% dell'entrata | ok (45%) | ok (43%) | **fuori** (34%) | ok (39%) | ok (47%) | ok (38%) |

- C6 (livello 1 identico al bit): **ok**. C7 (virata con 6 nodi entrando al 70%): **ok**, 5,76 s. C8 (strambata al massimo 1,5 volte il livello 1): **fuori** con 6, 10 e 14 nodi (circa 1,6-1,7 volte: la barra lenta impiega più tempo ad arrivare). C9 (risposta a 5° di barra entro 1 s): **ok** (0,17-0,49 s).
- Giro di penalità (nessuna soglia, nessuna fonte): con barra lenta 12,0 / 8,4 / 7,1 s con 6 / 10 / 14 nodi; con barra veloce 11,6 / 7,4 / 5,9 s; si esce alla stessa velocità.
- Sensibilità allo stallo: con 15° stalla anche la barra lenta e C1 cade quasi ovunque (C5 fuori con 6, 8 e 10 nodi); con 30° la pala stalla appena e C1 cade ovunque. **L'effetto c'è solo intorno a 22° e con vento medio: è fragile.**

**La cosa più importante, e sgradita: dove nasce la differenza fra barra lenta e veloce.** Un primo giro contava stallo e velocità minima anche dopo la virata, quando il collaudo molla la barra (in fretta, uguale per i due gesti). Separando le due fasi: **mentre la prua gira, con 10 e 14 nodi, la barra veloce non stalla quasi mai** (0,07 e 0 s) e la velocità minima è la stessa (50 contro 51%, 43 contro 49%). La differenza nasce **dopo**: la barca girata in fretta ha più rotazione addosso, e quando si molla la barra la pala stalla dall'altra parte e frena (1,8 contro 1,2 s di stallo con 10 nodi). È coerente con F4 (chi gira più in fretta perde più velocità), ma **non è il «non sbattere la barra» che si voleva insegnare**. Lo stallo mentre la prua gira compare solo con `yawG` 0,3 o meno, e allora la virata dura 4-5 s e la barca scende al 21-31% della velocità: C4 e C5 fuori. Il gioco nel browser dà lo stesso quadro (`collaudo_timone2.py`, 12 virate guidate coi tasti: tutte riuscite; avviso di stallo in tutte e 6 quelle con la barra veloce, ma anche in 4 delle 6 lente, con 6 e 10 nodi, perché la barra che torna al centro da sola fa stallare la pala uscendo dalla virata).

**Lettura.** Il modello è più vicino alla fisica di prima (la barca gira 3,6 s invece di 2,5 con 10 nodi, curvatura 0,34 contro 0,46 rad/m, la barra fino a 45° come nel 470 vero), ma **l'obiettivo didattico non è raggiunto**: con la barca leggera del gioco, «accompagnare la barra» e «girare abbastanza in fretta da non fermarsi» tirano in direzioni opposte. Due strade per il seguito, da decidere: (a) cercare dati di virate su una deriva singola di questa taglia (più pertinenti di F4) e ritarare; (b) ricontrollare la frenata della barca prua al vento, che la rende più leggera di quanto F4 lasci girare (dubbio già aperto il 13 ottobre: 1-1,6 lunghezze contro 3-4). La barca del livello 2 resta **in prova** nella navigazione libera, per sentirla giocando.

---

## 9. 1.0.25: la freccia fino a 35°, Maiusc fino a 45° (idea di Ale giocando, 17 ottobre 2026)

**Cosa ha detto Ale provando la 1.0.24** (osservazione 56): con Maiusc la barca sembra quella del livello 1, senza la barca gira più lenta, «ma nessun'altra conseguenza»; gli avvisi non si leggono (rimandati). **La sua proposta:** la differenza non sia la velocità della mano ma l'angolo: la sola freccia porta la barra veloce (come nel livello 1) fino a un angolo sicuro; con Maiusc si va fino in fondo, per girare più stretto (boa, penalità, barca lenta) o per una manovra rischiosa; freccia e Maiusc insieme da subito sono «una tirata» che frena.

**Fatto:** la barra va sempre a 1,6 al secondo; la sola freccia si ferma a 35° (`RUD2_SICURA`), Maiusc + freccia arriva a 45°. Il motore non cambia. **35° è una regola del gioco, senza fonte**: in barca vera non c'è un fermo, c'è la mano che sente la barra. Scelto perché lì, con 10 e 14 nodi, la pala non stalla mentre la prua gira; 30° e 25° rendono la virata lenta (3,8 e 4,7 s con 10 nodi).

**Criteri ridefiniti per i gesti nuovi** (C1: con Maiusc da subito si perdono almeno 5 punti di velocità in più che con la sola freccia; C2: con 45° la virata è almeno il 10% più rapida; C3-C5 sulla sola freccia). **Dichiarato: le soglie sono state scritte dopo aver visto le tabelle mostrate ad Ale in chat**, quindi non sono una prova alla cieca.

| Criterio | 10 | 14 | 6 | 8 | 12 | 16 |
|---|---|---|---|---|---|---|
| C1 Maiusc da subito perde almeno 5 punti in più | ok (49 / 38%) | ok (44 / 36) | ok (50 / 33) | ok (50 / 35) | ok (47 / 40) | **fuori** (36 / 41) |
| C2 con 45° almeno il 10% più rapida | ok (2,72 / 3,28 s) | ok (2,22 / 2,67) | ok | ok | ok | ok |
| C3 curvatura 0,12-0,30 rad/m | **fuori** (0,36) | **fuori** (0,37) | **fuori** | **fuori** | **fuori** | **fuori** (0,39) |
| C4 virata 2,5-4,5 s | ok (3,28) | ok (2,67) | **fuori** (4,89) | ok | ok | ok |
| C5 minima 35-60% | ok | ok | ok | ok | ok | ok (36%) |

- Freccia fino a 35°, 1 s di pausa, poi Maiusc: con 10 e 14 nodi 2,99 e 2,52 s, minima 45% e 46%: più rapida della sola freccia e quasi senza perdita in più. **È l'«accompagnare la barra»**, che nasce da solo dal motore: mentre si aspetta la barca comincia a girare e a 45° la pala non stalla più. Con 6 e 8 nodi non aiuta (34% e 39%).
- Barca lenta (entrata al 50% della bolina, 10 nodi): sola freccia 5,9 s, con 45° 4,6 s: piano, serve tutta la barra.
- C7 ok (6,56 s). C8 fuori solo con 6 nodi (3,29 s contro 2,19). C9 ok. Giro di penalità: con Maiusc 11,6 / 7,4 / 5,9 s con 6 / 10 / 14 nodi, con la sola freccia 14,5 / 9,5 / 7,6 s.
- **Nel browser** (`collaudo_timone2.py`, 12 virate coi tasti, poi i tasti lasciati e la barra che torna al centro da sola) **la perdita in più con Maiusc è più piccola**: 38 contro 51% con 6 nodi, 47 contro 49% con 10, e con 15 nodi Maiusc perde **meno** (46 contro 42%). In Node la barra viene mollata in fretta, nel gioco torna al centro piano: la perdita dipende anche da come si molla la barra. Con la sola freccia la pala non stalla con 10 e 15 nodi; con 6 nodi sì, 0,57 s.

**Lettura.** La regola dà una scelta che si sente (45° gira più in fretta, utile a boe, penalità e barca lenta), ma il costo di velocità è piccolo e non regolare fra i venti. La perdita vera della virata «sbattuta» resta legata soprattutto al momento in cui si molla la barra.

