# Proposta: le raffiche alle andature portanti (osservazione 52)

16 ottobre 2026. **Fermata 1:** il gioco non è stato toccato. Le misure vengono da un banco fuori dal gioco, sul motore vero (`tests/fisica/motore.js`).

## Il difetto

**Ale (osservazione 52):** nella prova 5, dopo la boa, al lasco e al gran lasco, in raffica il pannello continua a dire di lascare, ma la vela è già lascata. Non è spiegato cosa fare con le raffiche da dietro.

**[codice]** Oggi i suggerimenti sulle raffiche (`js/disegno.js`, pannello) sono uguali a tutte le andature:
- «Raffica in arrivo: se la barca sbanda troppo, lasca; altrimenti è un'occasione per andare più veloci.»
- con più di 25° di sbandamento: «Sbandi troppo: lasca la scotta» (più «oppure orza di poco» sotto 80° dal vento);
- con più di 25° e la vela tutta lasca: «prova a orzare un poco», **a qualunque andatura**. Al traverso e al lasco è il consiglio sbagliato (vedi sotto).

La lezione 6 parla solo della bolina.

## Cosa dicono le fonti

| Fonte | Tipo, affidabilità | Cosa dice (parafrasi) |
|---|---|---|
| D. Dellenbaugh, «Sailing downwind», Speed & Smarts (già F7) | Allenatore e autore, media-alta | In raffica alle portanti si poggia «sotto la vela» e si tiene la barca piatta; se si è già sporti fuori e si sbanda ancora, si lasca. Se la barca rolla: sbanda sottovento, si poggia; sbanda sopravento, si orza. Col vento che entra dal lato sbagliato della vela (oltre la poppa) si rischia la strambata involontaria: si orza, oppure si stramba. |
| National 125 Association, «Speed» (125assoc.com) | Classe di una deriva a due, media | Al lasco una raffica aumenta lo sbandamento, quindi si poggia: il contrario di quel che si fa di bolina. Quando il vento cala si orza. |
| National 12, note di allenamento sul lasco (national12.org) | Classe di una deriva a due, media | All'arrivo della raffica l'equipaggio va sopravento; un po' di sbandamento sopravento aiuta a poggiare e ad accelerare. |
| Yachting Monthly, vento apparente | Rivista, media | Chi regata, al lasco, in raffica poggia per tenere la barca sotto la vela; chi fa crociera tende invece a orzare. |
| Wikipedia, «Planing (boat)» (CC BY-SA) | Enciclopedia, media | Sulle derive: in raffica si poggia un poco e si lasca; quando la raffica passa si orza un poco. |
| Sailing World, controllo al lasco stretto (uguale su Quantum Sails e Spinsheet) | Rivista, media | Appena lo sbandamento cresce si lasca, all'inizio con decisione; poggiando all'arrivo della raffica la barca resta piatta; quando la raffica è diventata velocità si orza di nuovo. Scritto per barche con lo spinnaker. |
| Cal Sailing Club, «downwind sailing and the evils of rounding up» | Circolo, media | In raffica la barca tende a orzare da sola; il rischio di straorzare e scuffiare è più alto vicino al gran lasco. |
| Forum (Yachts and Yachting, YBW, boatdesign, SailNet) | Bassa | Quasi tutti: davanti al traverso si orza, dietro al traverso si poggia. Uno (SailNet) sostiene che su una deriva si orza anche al lasco. Poggiare troppo rischia la strambata. |

**In sintesi [fonti]:**
- **Bolina:** si lasca, e si può orzare di poco. È già nel gioco.
- **Traverso e lasco:** in raffica **si poggia un poco e si lasca**; la barca resta piatta e la raffica diventa velocità; passata la raffica si orza e si cazza. **Orzare fa sbandare di più.**
- **Gran lasco e poppa:** la vela è quasi tutta aperta e la barca sbanda poco; poggiando troppo si rischia la **strambata involontaria**.
- **Disaccordo dichiarato:** una voce di forum e la pratica di crociera dicono di orzare. Le fonti più vicine a una deriva (Dellenbaugh, due classi) dicono di poggiare.

## Il motore è d'accordo? [misura]

Banco: barca a regime con 10 nodi e la scotta che dà la velocità massima, poi raffica a 16 o 20 nodi; reazione dopo 0,3 s, in 1 s: niente, lascare (+30% di scotta), poggiare di 20°, orzare di 20°, lascare e poggiare. Sbandamento massimo in 8 s.

| Raffica, angolo dal vento | niente | lasca | poggia | orza | lasca e poggia |
|---|---|---|---|---|---|
| 16 nodi, 90° | 20° | 14° | 14° | 20° | 13° |
| 16 nodi, 110° | 12° | 9° | 9° | 13° | 8° |
| 20 nodi, 90° | 35° | 27° | **25°** | **41°** | 24° |
| 20 nodi, 110° | 20° | 14° | 15° | 21° | 12° |
| 20 nodi, 60° (bolina larga) | 61° (scuffia) | 49° | 52° | 58° | 55° |
| 20 nodi, 135° e 160° | 2-6° | 2-5° | 3-5° | 6-17° | 3-5° |

- **Al traverso e al lasco poggiare toglie sbandamento quanto lascare, e orzare non aiuta** (con 20 nodi al traverso lo peggiora: 41° contro 35°). Il motore dice la stessa cosa delle fonti, **senza bisogno di toccarlo**.
- **Al gran lasco e in poppa la raffica fa sbandare poco** (al massimo 6°, orzando 17°): lì il problema non è lo sbandamento.
- **Limite della misura:** la prua è girata a mano, non con la barra; la velocità dopo la manovra non è confrontabile fra i casi.

## La proposta

**Solo testi.** Il motore non si tocca. I gruppi di andature sono quelli che il gioco mostra già nel pannello (`ANDATURE` in `js/base.js`).

| Situazione | Bolina (fino a 75°) | Traverso e lasco (75°-135°) | Gran lasco e poppa (oltre 135°) |
|---|---|---|---|
| Raffica in arrivo | «Raffica in arrivo: se la barca sbanda troppo, lasca un poco oppure orza di poco.» | «Raffica in arrivo: poggia un poco e lasca, così la barca resta piatta e accelera.» | «Raffica in arrivo: tieni la barca piatta e la rotta; non poggiare troppo, rischi la strambata.» |
| Sbandi oltre 25° | «Sbandi troppo: lasca la scotta, oppure orza di poco.» (come oggi) | «Sbandi troppo: lasca la scotta e poggia un poco.» | come traverso e lasco |
| Sbandi oltre 25°, vela tutta lasca | «…prova a orzare un poco.» (come oggi) | «Sbandi troppo e la vela è già tutta lasca: poggia un poco.» | come traverso e lasco |

- Il confine per «oppure orza di poco» passa da 80° a **75°**, cioè lo stesso confine fra bolina larga e traverso che il pannello mostra.
- **Lezione 6:** nel passo «Riepilogo» si aggiunge una frase: «Al traverso e al lasco, in raffica poggia anche un poco: orzare ti farebbe sbandare di più.» Se il pannello a 1360×650 non ci sta, la frase va nel passo «Raffiche e sbandamento», che non ha comandi.
- **Fonti** in `FONTI-PUBBLICHE.md` (nuove voci) e le tre affermazioni nuove in `CONTENUTI-DA-VERIFICARE.md`, con il disaccordo dichiarato.
- **Fuori da questo compito:** una domanda del ripasso o dell'esame sulle raffiche al lasco (si può aggiungere dopo, se Ale vuole); il rollio in poppa; il peso del timoniere (nel gioco è automatico).
- Versione **1.0.9**.

## Criteri della fermata 2 (soglie: attese nostre)

1. **Il motore regge il consiglio, su casi non ancora guardati.** Banco `tests/fisica/raffiche_portanti.js`. **Soglie (scelte dopo aver visto la tabella sopra, quindi da confermare su un gruppo nuovo, secondo la regola dei semi):** al traverso e al lasco, «poggia» sbanda almeno **2° meno** di «niente», e «orza» non sbanda meno di «niente − 1°». Gruppo di conferma, mai guardato: raffiche da 14 e 18 nodi, a 80°, 100° e 125°, mure a dritta e a sinistra (12 casi). Si riporta ogni caso; se uno fallisce, ci si ferma.
2. **Ogni testo nel posto giusto, misurato davvero:** collaudo nel gioco (`collaudo_suggerimento.py` esteso) che mette la barca in ognuna delle tre fasce, su tutte e due le mure, con la raffica davanti e con lo sbandamento forzato oltre 25° (con e senza la vela tutta lasca): 3 × 3 × 2 = 18 casi. Soglia: 18 su 18 col testo atteso, e il collaudo dice quanti casi ha misurato (zero casi = fallito).
3. **Pannello a 1360×650 senza eccesso** con il testo più lungo, e lezione 6 «Riepilogo» (`collaudo_pannello.py`). Soglia: 0 px.
4. **Niente altro cambia:** `polare.js` e `raffiche_e_virate.js` identici; impronta del gioco: cambiano solo testi del pannello (si riporta in quante scene), mai lo stato delle barche.
5. **Pagina caricata come la carica un giocatore:** nessun errore.
6. **Il giudizio giocando è di Ale**, nella prova 5 e in navigazione libera con raffiche.

## Rischi

- **Poggiare al gran lasco porta alla strambata involontaria**, che nel gioco può far scuffiare. Per questo oltre 135° il suggerimento non dice di poggiare.
- **Il confine a 135° è netto:** passandolo, il testo cambia di colpo. Accettabile: lo stesso succede già col nome dell'andatura.
- **Le fonti non sono di una federazione.** Una federazione (FIV, RYA, US Sailing) non è stata trovata online su questo punto; la dispensa FIV F1 parla solo di vang alle portanti.
- **Il pannello ha poco margine** (2 px nel passo 5 della lezione 3; la lezione 6 va misurata).

## Fonti

- D. Dellenbaugh, «Sailing downwind», Speed & Smarts: https://www.speedandsmarts.com/toolbox/articles2/smallboat-sailing/sailing-downwind
- National 125 Association, «Speed»: https://125assoc.com/speed.asp
- National 12, «High speed reaching»: https://national12.org/hints/coaching/coaching_reaching.shtml
- Yachting Monthly, «Apparent wind: how to predict it and use it to your advantage»: https://www.yachtingmonthly.com/sailing-skills/apparent-wind-how-to-predict-it-and-use-it-to-your-advantage-87841
- Wikipedia, «Planing (boat)»: https://en.wikipedia.org/wiki/Planing_(boat)
- Sailing World / Quantum Sails, «4 steps for maintaining control on a tight reach»: https://www.quantumsails.com/news/index.php/2015/11/4-steps-for-maintaining-control-on-a-tight-reach/
- Cal Sailing Club, «downwind sailing and the evils of rounding up»: https://cal-sailing.org/blogfrontpage/recent-blog-posts/entry/downwind-sailing-and-the-evils-of-rounding-up
- Forum (affidabilità bassa): https://www.yachtsandyachting.com/Forum/forum_posts.asp?TID=9190 ; https://forums.ybw.com/threads/handling-gusts-when-sailing-on-a-broad-reach.275616/ ; https://www.boatdesign.net/goto/post?id=225091 ; https://www.sailnet.com/threads/handling-gusts.99583/

## Cosa serve da Ale

Sono contenuti, quindi decide Ale:
1. **I cinque testi nuovi** della tabella (gli altri restano come oggi): vanno bene così o vanno cambiate delle parole?
2. **La frase della lezione 6.**
3. Il via alla fermata 2.
