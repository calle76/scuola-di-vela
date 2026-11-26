// Voce 84, sesto giro (GIRO6.md): griglia off × par × scafo sul candidato K (area 7,92). Taratura: Day 6/10/15 e F121 (metro sulla rotta). Controllo: Binns 9/12, F109 3,2 nodi, VMG 20 nodi.
const { misura } = require("./banco84.js"), C = require("./candidato.json"), out = [];
for (const off of [5, 7, 9, 11, 13]) for (const par of [.06, .075, .09, .105]) for (const hs of [.93, .965, 1]){
  const P = JSON.parse(JSON.stringify(C[3].P)); P.off = off; P.par = par; P.boat.hullScale = hs; const o = misura(P, 2);
  const t = Math.sqrt([...o.day.map(d => d[0]), ...o.pen].reduce((s, x) => s + x * x, 0) / 7), c = Math.sqrt([...o.b9, ...o.b12, (o.b5 / 1.05 - 1) * 100].reduce((s, x) => s + x * x, 0) / 10);
  out.push({ off, par, hs, t, c, day: o.day.map(d => +d[0].toFixed(1)), pen: o.pen.map(x => +x.toFixed(1)), b9: o.b9.map(x => +x.toFixed(1)), b12: o.b12.map(x => +x.toFixed(1)), b5: +((o.b5 / 1.05 - 1) * 100).toFixed(1), v20: +o.v20.toFixed(2) });
  console.error(`${off} ${par} ${hs} taratura ${t.toFixed(2)}`); }
require("fs").writeFileSync(__dirname + "/scansione6.json", JSON.stringify(out));
out.sort((a, b) => a.t - b.t); console.log("ordine per errore di TARATURA (Day, F121); «controllo» = Binns 9/12 e F109, non usato per scegliere");
for (const r of out.slice(0, 15)) console.log(`off ${r.off} par ${r.par} scafo ${r.hs} | taratura ${r.t.toFixed(2)} controllo ${r.c.toFixed(2)} | Day ${r.day} F121 ${r.pen} | Binns9 ${r.b9} Binns12 ${r.b12} 3,2n ${r.b5} | 20n ${r.v20}`);
