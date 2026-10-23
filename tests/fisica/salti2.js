// Salti di vento del livello 2 (1.0.28, docs/archivio/PROPOSTA-SALTI-VENTO.md §4): criteri S1 e S2 sul generatore del gioco (newShift, stepShift),
// bolina di 300 m con la barca del livello 2 e il pilota di salti_bolina.js. Semi 1-40 di taratura, 121-160 di conferma mai guardati (41-80 e 81-120 usati con le versioni scartate del modello: §7).
// S1 (salti oscillanti): «sui salti» batte «due bordi» in media di almeno il 5% e in almeno 2 regate su 3.
// S2 (salto persistente): partire verso la parte da cui ruota il vento batte partire dall'altra parte in almeno 3 regate su 4.
// Uso: node salti2.js      esce con 1 se un criterio è fuori soglia o se ha misurato zero regate.
const { newShift, stepShift } = require("./motore.js");
const bolina = require("./salti_bolina.js");
const D = 300;
function rng(seed){ let s = seed * 7919 % 2147483647 || 1; return () => (s = s * 16807 % 2147483647) / 2147483647; }
function vento(kind, seed){ // twdAt(t) per un t che cresce: avanza il generatore a passi di 0,02 s
  const rnd = rng(seed), st = newShift(kind, rnd); let tt = 0, v = stepShift(st, 0, rnd);
  const f = t => { while (tt + 0.02 <= t + 1e-9){ tt += 0.02; v = stepShift(st, 0.02, rnd); } return v; };
  f.rate = st.rate; return f;
}
let tutti = true;
for (const [nome, semi] of [["taratura", [1, 40]], ["conferma", [121, 160]]]){
  let n = 0, vinte = 0, sd = 0, ss = 0, nP = 0, giuste = 0, gd = 0, gs = 0;
  for (let k = semi[0]; k <= semi[1]; k++){
    const d = bolina(10, D, vento("osc", k), "dritto"), s = bolina(10, D, vento("osc", k), "salti");
    if (d.t !== null && s.t !== null){ n++; sd += d.t; ss += s.t; if (s.t < d.t) vinte++; }
    const w = vento("pers", k), verso = Math.sign(w.rate);
    const a = bolina(10, D, vento("pers", k), "dritto", 5, 0.02, verso), b = bolina(10, D, vento("pers", k), "dritto", 5, 0.02, -verso);
    if (a.t !== null && b.t !== null){ nP++; gd += a.t; gs += b.t; if (a.t < b.t) giuste++; }
  }
  const guad = n ? (sd - ss) / sd : 0;
  const S1 = n === (semi[1] - semi[0] + 1) && guad >= 0.05 && vinte >= n * 2 / 3, S2 = nP === (semi[1] - semi[0] + 1) && giuste >= nP * 3 / 4; // 1.0.31: tutte le bolinate devono arrivare (prima bastava una)
  console.log(`${nome} (semi ${semi[0]}-${semi[1]}):`);
  console.log(`  S1 ${S1 ? "ok   " : "FUORI"} salti oscillanti: due bordi ${(sd / n).toFixed(1)} s, sui salti ${(ss / n).toFixed(1)} s, guadagno ${(guad * 100).toFixed(1)}% (almeno 5%); vince ${vinte} su ${n} (almeno 2 su 3)`);
  console.log(`  S2 ${S2 ? "ok   " : "FUORI"} salto persistente: verso la rotazione ${(gd / nP).toFixed(1)} s, dall'altra parte ${(gs / nP).toFixed(1)} s; meglio ${giuste} su ${nP} (almeno 3 su 4)`);
  tutti = tutti && S1 && S2;
}
console.log(tutti ? "ESITO: tutti i criteri nelle soglie" : "ESITO: almeno un criterio FUORI soglia");
process.exit(tutti ? 0 : 1);
