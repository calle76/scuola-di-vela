# Voce 84: intervalli dei parametri (scritti il 25 novembre 2026 PRIMA di ogni misura col banco nuovo)

`js/` non si tocca: il banco compila in memoria una copia di `js/motore.js` con righe sostituite.

| Parametro | Oggi | Intervallo | Fonte |
|---|---|---|---|
| Massa totale `mass` | 135 | **160** (fisso) | Day: 79,5 kg pesati (scafo, albero, boma, deriva, timone) + 80; la resistenza dello scafo del gioco è già quella a 160 kg |
| Timoniere `sailorMass` | 75 | 80 (80-85: Day aggiunge 5 kg di vestiti) | Day §6.1; Goodison 78-83 in Day |
| Braccio del timoniere `hikeArm` | 1,0 | 0,95-0,956 | Day §4 (95% del 55% di 1,83 m); F121 0,95. Schütz 2011 (ISBS): 0,79 m con atleti di 1,71 m e 64 kg, più basso |
| Stabilità di forma | 400·sin2φ/2 | curva GZ di F121 fig. 31 (0 / 4,5 / 9 / 13,5 / 18 / 22,5° = 0 / 0,083 / 0,145 / 0,190 / 0,223 / 0,247 m) × peso, meno il timoniere più alto del baricentro (Day eq. 18; altezza 0-0,3 m, **ipotesi**) | F121; oltre 22,5° **ipotesi** |
| Braccio sbandante `zCE` | 2,0 | 2,9-3,1 | F121 (2,68 m sull'acqua + deriva al 43-45%) |
| Portanza della vela | retta fino a 20° | tabella ORC «low lift» usata da Day (tab. 1: 7° 0,862, 9° 1,052, 12° 1,164, 28° 1,347) letta a α + 9° | Day tab. 1; il 9° è il boma minimo del gioco, **ipotesi** |
| Vela che fileggia | rampa su vento apparente 22-29° | rampa sull'incidenza α, da a0 (0-3°) a a0+w (w 6-14°) | principio da Day §2.4 (SPILL: lascare = ridurre l'angolo); **numeri ipotesi** |
| Resistenza della vela (bolina) | 0,06 + 1,15·sin²α + 0,08·CL² | viscosa tab. 1 + CL²·(1/(π·AR)+0,005) + parassita, 0,25-0,27 in tutto a 28° | Day §2.1 e §2.5 (0,20 senza timoniere + 0,05-0,07) |
| Resistenza in poppa | 1,15 | vela 1,38-1,44 a 90° + scafo e timoniere | Magnander 2022-2023, CC BY (F120) |

**Taratura:** Day 6, 10, 15 nodi e F121. **Conferma:** Binns 9 e 12, F109. Tutti già visti: la conferma non è alla cieca.

## Aggiunte dopo le prime misure (dichiarate)

- **Area di riferimento della vela: 7,92 m²** (era 7,0; 7,06 è l'area nominale di classe, circa il triangolo luff·base/2 = 7,03). Formula ORC di Magnander eq. 2.73 senza il termine MUW (7/8 dell'inferitura, che il disegno di classe non quota): 5,13/8·(2,74 + 2·2,33 + 2·1,72 + 1,5·0,965 + 0,5·0,12) = 7,92; larghezze **massime** del disegno F119 pag. 35; testa 0,12 stimata a occhio. Conferma indipendente: Day corregge Flay da 1,53 a 1,36 passando dal triangolo alla tela, cioè ×1,125 → 7,91. I coefficienti ORC della tab. 1 di Day si riferiscono a questa area. Le curve delle andature larghe restano quelle di oggi, scalate 7,0/7,92.
- Spostato `b1`, `b2` (passaggio dalla curva nuova alla vecchia fra 45° e 75° di vento apparente): **senza fonte**, dichiarato.
- Parassita 0,105 = 0,063 scafo e albero + 0,042 timoniere, da Day fig. 12 (23-26% e 15-17% del totale 0,24).
- Vela piatta minima 0,6 e svergolamento 0,186 da Day §2.3-2.4 (il secondo è il valore a 15 nodi); la regola con cui il timoniere li usa è **ipotesi**: τ = 0,9 s (il ritardo che il timoniere ha già nel gioco), sbandamento massimo accettato 3° (Day fig. 9).

## Verifica alla cieca (scritta PRIMA del conto): Marshall, ISBS

Laser in acqua, due velisti, di bolina: 119 N·m di raddrizzata in meno → −0,6 km/h (−0,32 nodi) e 2° più largo; 178 N·m in meno → −1,7 km/h (−0,92 nodi) e 6° più largo. Vento non detto. Attesa nostra: perdita di VMG della barca, con 12, 14 e 16 nodi, entro un fattore 2 da quella di Marshall (circa −9% e −26%, tenendo 5,2 nodi a 43°), nello stesso ordine (178 peggio di 119). Si fa anche con la barca di oggi.
