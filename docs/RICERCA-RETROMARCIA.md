# Ricerca: la retromarcia di una deriva

16 ottobre 2026, ricerca sul web fatta da Claude Code su richiesta di Ale, dopo la 1.0.6. Completa il §3 di `RICERCA-VELOCITA-VIRATA-RIPARTENZA.md` (la ricerca della chat, che non aveva trovato numeri). Parafrasi, non citazioni; per ogni fonte il tipo e l'affidabilità.

**In sintesi:**
- **la retromarcia è vera e si insegna;**
- **nessuna fonte dà la velocità all'indietro né quanto in fretta parte;**
- la spinta della vela che sbatte, nel gioco, sta dentro i valori misurati in galleria del vento sulle bandiere. Quello che oggi limita la velocità all'indietro è un **tetto senza fonte** (`backMax`).

## 1. Cosa dicono le fonti didattiche

| Fonte | Tipo, affidabilità | Cosa dice |
|---|---|---|
| Australian Sailing, «Drills for Skills: Sailing Backwards» (sailing.org.au) | Federazione, alta | Esercizio per scuole: fermarsi nell'angolo morto, spingere fuori il boma, barra verso il boma, la barca ruota; poi barra al centro e si cazza. Peso sopravento. Nessun numero. |
| Scheda «Sailing Backwards» per istruttori di deriva (instructortoolkit.co.uk) | Didattica, media | Barca ferma con la prua al vento, timone al centro, deriva a metà, boma spinto fuori a circa 90°, solo piccole correzioni di timone. Serve per uscire da pontili e spazi stretti. Nessun numero. |
| US Sailing, «Getting in and out of irons» (ussailing.org) | Federazione, alta | Quando il vento passa sul lato sopravento si lascia la vela spinta e si cazza. Nessun numero. |
| Guida di un circolo per una deriva in singolo (MYC, «How to get out of irons», 2021) | Circolo, media | Una vela che sbatte è il motore in retromarcia. Boma e barra dalla stessa parte: la barca va all'indietro e gira; al traverso barra al centro e si cazza. Le derive leggere e i velisti leggeri si piantano più facilmente, soprattutto con vento oltre i 15 nodi. |
| Classe di un catamarano, «Reverse logic: getting out of irons» (2011) | Classe, media | All'indietro si esce dall'angolo morto «abbastanza in fretta». La barca che va all'indietro non ha diritti di precedenza. |
| «The Final Beat», allenamento alle partenze | Allenatore, media | All'indietro si esce da un brutto posto sulla linea: boma fuori il più possibile, peso avanti per sollevare lo specchio di poppa, barra al contrario. Bisogna imparare quanto in fretta parte e quanto va forte la barca. Con meno di 30 s è troppo tardi. |

## 2. Numeri trovati (pochi e deboli)

- **Nessuna misura** di velocità all'indietro né del tempo prima che la barca parta all'indietro.
- **Forum (affidabilità bassa):** una deriva in singolo «può addirittura planare all'indietro» con vento forte; un altro intervento parla di «circa 2 nodi» per una barca che va di poppa al vento (frase incompleta, barca non chiara).

## 3. Controllo fisico: quanto spinge la vela che sbatte

- **[fonte]** Prove in galleria del vento su bandiere che sventolano (Raynaud e Mulleners, «On the wake and flapping dynamics of different aspect ratio flags», arXiv 2602.06237, 2026, licenza CC BY 4.0; e Virot, Amandolese e Hémon, *Journal of Fluids and Structures*, 2013): il coefficiente di resistenza medio va da 0 a circa 0,55, a seconda della forma e del peso della bandiera.
- **[misura, motore della 1.0.6]** Nel gioco la vela che sbatte con la prua al vento ha un coefficiente di **0,26**: con 10 nodi spinge all'indietro con circa **30 N**. È dentro la fascia delle bandiere.
- **[misura]** Con quella spinta e lo scafo della vasca, la barca andrebbe all'indietro fino a **3,5 nodi**. Oggi si ferma a **2,3 nodi** solo per il tetto `backMax` (1,2 m/s), che **non ha una fonte**.
- **[stima]** La vasca è misurata con la prua avanti. Andando di poppa, lo specchio di poppa e il timone frenano di più (studi sugli scafi con specchio di poppa: a bassa velocità dietro lo specchio si forma una zona d'acqua trascinata, Chalmers). Nessun numero trovato per uno scafo che va all'indietro.

## 4. Regola di regata

- **[fonte]** World Sailing, regolamento di regata 2025-2028, regola 21.3 (copia locale `fonti-pdf/RRS-2025-2028-World-Sailing.pdf`): una barca che si muove all'indietro, o di lato verso il vento, spingendo una vela al contrario, deve tenersi lontana da quelle che non lo fanno. Conferma l'opinione del forum citata nella ricerca precedente. Da riportare in `REGOLE-DI-REGATA.md`.

## 5. Cosa ne ricava Claude Code (da usare nella proposta)

1. **La retromarcia in sé è giusta:** le fonti la descrivono come un comportamento normale, e la spinta della vela che sbatte è plausibile.
2. **Quanto forte va** dipende da due cose senza numeri: il tetto `backMax` e il freno dello scafo all'indietro. Oggi conta solo il tetto. Una strada senza tarare a occhio: togliere il tetto e dare allo scafo all'indietro un freno maggiore, dichiarato come ipotesi.
3. **Quanto presto parte** (l'impressione di Ale): dipende da quanto in fretta la barca si ferma (la vasca, ora giusta) e dalla spinta della vela che sbatte (plausibile). Nessuna fonte dice «troppo presto» o «troppo tardi»: va misurato nel gioco e confrontato con i video.
4. **Il metodo per ripartire che tutte le fonti insegnano** (boma e barra dalla stessa parte) il gioco non lo permette: senza il comando «spingi il boma», la retromarcia nel gioco succede solo da sola, mai di proposito. È la voce già in roadmap; insieme alla retromarcia è il cuore del compito.

## Fonti

- Australian Sailing, «Drills for Skills – Sailing Backwards»: https://www.sailing.org.au/news/drills-for-skills-sailing-backwards
- Scheda per istruttori, «Sailing Backwards»: https://www.instructortoolkit.co.uk/instructor-resources/dinghy-instructor-resources/sailing-backwards/
- US Sailing, «Getting in and out of irons»: https://www.ussailing.org/news/getting-in-and-out-of-irons/
- MYC, «Sunfish – How to get out of Irons» (2021): https://myc.org/wp-content/uploads/2021/02/Sunfish-How-to-get-out-of-Irons.pdf
- Paper Tiger Catamaran Association, «Reverse logic – getting out of irons» (2011): https://www.papertigercatamaran.org/ptcia/media/pdf/reverse_logic_-_getting_out_of_irons.pdf
- The Final Beat, «Practising starting»: https://thefinalbeat.com/categories/starting/practising-starting
- Forum: https://www.yachtsandyachting.com/Forum/printer_friendly_posts.asp?TID=12182 ; https://forums.ybw.com/threads/backwards-sailing.64563/ (affidabilità bassa)
- Raynaud e Mulleners (2026), arXiv 2602.06237: https://arxiv.org/abs/2602.06237
- Virot, Amandolese, Hémon (2013), «Fluttering flags: An experimental study of fluid forces»: https://hal-polytechnique.archives-ouvertes.fr/hal-00995149
- Chalmers, scafi con specchio di poppa a bassa velocità: https://research.chalmers.se/en/project/7969
- World Sailing, *The Racing Rules of Sailing 2025-2028*, regola 21.3 (copia locale).
