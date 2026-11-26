# Voce 88, passo 1: il banco delle onde (26 novembre 2026)

Via di Ale (26 nov): passo 1 sul banco, sopra la barca M (accesa nella 1.3.59), spazio d'acqua 5 km per tutti. `js/` non vede le onde: `fa_motore88.py` scrive `motore88.js` = `js/motore.js` + le onde di `docs/PROPOSTA-ONDE.md`. `banco88.js` misura.

## Come si leggono i criteri (scritto PRIMA di lanciare `banco88.js`)

Soglie di `PROPOSTA-ONDE.md`, invariate. Qui solo come si misurano, perché la proposta non lo diceva.

- **Corsa:** prua ferma (come il banco 84), 240 s a passi di 0,05 s, media dopo i primi 40 s; vento costante; scotta = la migliore in acqua piatta per quell'angolo (passo 0,02), la stessa con le onde. Onde da `onde88crea` (SPM 1984, 5 km), dirette dove va il vento.
- **Semi:** 1-10 per la misura, 11-20 per la conferma (mai guardati prima). Un criterio passa se passa sui due gruppi; si riportano tutti e due.
- **Velocità** = velocità vera (avanti + scarroccio); **VMG** sulla rotta (componente della velocità vera lungo il vento), come il metro del quinto giro della 84.
- **O1:** 6 e 7 nodi, angoli 45, 60, 90, 110, 135, 150, 180: media dei 10 semi entro ±1% dell'acqua piatta, a ogni angolo.
- **O2:** 10, 12, 15 nodi, angoli 135, 150, 180: media dei 10 semi fra 0 e +12% sull'acqua piatta, per ogni caso (9 casi).
- **O3:** 9 e 12 nodi a 135° e 180°: media dei semi sotto i dati di Bethwaite/Binns (lasco 6,1 / 8,0; poppa 5,5 / 6,7 nodi).
- **O4:** 12 e 15 nodi a 180°: la mediana fra i semi della velocità massima della corsa almeno +20% sull'acqua piatta. (150° solo riportato.)
- **O5:** 10, 12, 15 nodi. Riferimento: la VMG di poppa migliore con le onde e prua ferma fra 135° e 180° (passo 5°). Pilota sull'onda (regola scritta qui, IPOTESI): parte dall'angolo migliore a prua ferma `a0`; quando la forza dell'onda spinge in avanti (la poppa si alza) punta a `min(180, a0 + 20)`, altrimenti torna ad `a0`; la prua gira al massimo di 15°/s; scotta fissa, la migliore in acqua piatta per `a0`. Passa se la VMG media dei semi del pilota supera quella a prua ferma, ai tre venti.
- **O6:** VMG di bolina sulla rotta, migliore fra 36° e 54° di prua (passo 1°), con e senza onde: perdita fra 3 e 15% con 10 nodi, fra 8 e 25% con 15.
- **O7:** la VMG di O6 con 15 nodi e onde: almeno 3,7 nodi.
- **O8:** stesso seme due volte (15 nodi, 150° e 45°, semi 1-3): stati finali e somma di controllo di tutti i passi uguali al bit. Moviola e registrazioni sono del passo 2 (nel gioco): qui non si misurano.
- **O9:** già misurato prima del resto: `o9/` (copie di `impronta1b.js`, `polare.js`, `raffiche_e_virate.js` col caricatore su `motore88.js`): impronta 25 corse su 25 identiche, polare e raffiche identiche.

## Cosa il banco non sa (dichiarato)

Niente sbandamento, imbardata o beccheggio dovuti all'onda; niente velocità orbitale dell'acqua sul timone e sulla deriva; la forza laterale dell'onda (quando la prua non è in linea con le onde) è scartata. Il pilota di O5 gira la prua senza timone.

---

# Esito (26 novembre 2026, scritto dopo le misure)

`banco88_misura.txt` (semi 1-10) e `banco88_conferma.txt` (semi 11-20): **numeri quasi uguali nei due gruppi** (le 5 onde con fasi diverse, mediate su 200 s, danno quasi la stessa media). **Un errore mio corretto dopo il primo lancio:** in O5 la VMG di poppa usciva col segno sbagliato e si sceglieva l'angolo peggiore; corretto il metro, non la soglia, e rilanciata la misura.

| | Esito | Numeri (misura; la conferma differisce al più di 1 punto) |
|---|---|---|
| O1 sotto 8 nodi niente | **no** | 6 nodi: bolina 45° −4,5%, 60° −2,0%, 135° −1,2%; 7 nodi: 45° −5,9%, **150° +11,1%**, 180° +3,6%. La resistenza in più di bolina c'è già con onde da 10-12 cm; a 7 nodi a 150° la barca si aggancia all'onda |
| O2 poppa e lasco 0…+12% | **5 su 9 no** | 10 nodi −0,4/−0,6% (appena sotto zero); 12 nodi +1,4 / +3,1 / +7,1%: ok; 15 nodi 135° −3,3% e 180° −2,4% (la barca va più veloce delle onde e le passa: frenano), 150° +4,5% ok |
| O3 sotto Bethwaite/Binns | ok | 9 nodi 4,78 e 3,79 (contro 6,1 e 5,5); 12 nodi 6,04 e 5,48 (contro 8,0 e 6,7) |
| O4 punta +20% in poppa | 12 nodi ok, **15 no** | 12 nodi +28%; 15 nodi +17% (150°: +26%) |
| O5 timonare sull'onda rende | **no** | col pilota scritto prima: 10 nodi −2,0%, 12 nodi 0% (l'angolo migliore è già 180°, il pilota non può poggiare di più), 15 nodi −0,8%. Il pilota della regola è troppo semplice per dire se la tecnica rende: non dice che non rende |
| O6 bolina frena | ok | 10 nodi −6,3%, 15 nodi −12,4% (VMG 3,51 → 3,29 e 3,70 → 3,24; angolo migliore 3-6° più largo) |
| O7 bolina 15 nodi ≥ 3,7 | **no** | 3,24: il rischio scritto nella proposta si è avverato |
| O8 ripetibile | ok | 6 coppie al bit; semi diversi, tracce diverse |
| O9 onde spente = M | ok | impronta 25 su 25, polare e raffiche identiche |

## Cosa dice

1. **Le onde da sole, a prua ferma, cambiano poco la media** (−3…+7% in poppa) e molto le punte (+12…+28%): come la prova grezza.
2. **Di bolina frenano quanto stimato** (−6 / −12%), ma con 15 nodi M più le onde scende a 3,24 nodi di VMG, sotto la media delle regate (3,7). Le tre spiegazioni della proposta restano (resistenza in più troppo alta: Caw allargato da onde di 4 cm; M un po' lenta col vento forte; onde di mare lunghe nelle regate). **Caw non è stato ritoccato.**
3. **Sotto gli 8 nodi le onde contano ancora** (O1): il modello fa crescere la resistenza col quadrato dell'altezza senza la «soglia» che l'ORC ha dovuto mettere (F143). Una soglia così sarebbe una taratura nuova.
4. **Il guadagno del surf col timone non è dimostrato** (O5): la regola del pilota (poggiare di 20° quando l'onda spinge) non rende. Serve un pilota migliore (o la prova a mano) prima di dire che la tecnica non rende: è il lavoro della voce 87.

**Decisione di Ale** (niente si accende nel gioco): (a) andare avanti così nel gioco dichiarando O1, O2, O4, O5, O7; (b) rivedere la resistenza in più (soglia sotto 8-10 nodi come l'ORC, Caw più basso: tarature, da controllare su dati non usati); (c) fermare la voce 88 finché non c'è una misura su una deriva in onda.
