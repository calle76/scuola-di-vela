// Voce 84: scansione area x braccio velico x braccio del timoniere. Taratura: Day 6/10/15 (VMG) e F121 (4). Conferma: Binns 9 (4), Binns 12 (5), F109 3,2 nodi. Uso: node scansione84.js
const { misura, esito } = require("./banco84.js"), fs = require("fs"), C = JSON.parse(fs.readFileSync(__dirname + "/candidato.json"))[1].P; delete C.ease84;
const out = []; for (const A of [7.06, 7.3, 7.5, 7.7, 7.92]) for (const z of [2.4, 2.6, 2.8, 3.0]) for (const h of [.87, .91, .956]){
  const P = JSON.parse(JSON.stringify(C)); P.boat.sailArea = A; P.boat.zCE = z; P.boat.hikeArm = h; P.k0 = 7 / A; P.cdn = 1.32 * 7.92 / A; const o = misura(P, 1);
  const t = Math.sqrt([...o.day.map(d => d[0]), ...o.pen].reduce((s, x) => s + x * x, 0) / 7), c = Math.sqrt([...o.b9, ...o.b12, (o.b5 / 1.05 - 1) * 100].reduce((s, x) => s + x * x, 0) / 10);
  out.push({ A, z, h, t, c, e: esito(o), day: o.day.map(d => +d[0].toFixed(1)), b9: o.b9.map(x => +x.toFixed(1)), b12: o.b12.map(x => +x.toFixed(1)), b6: +o.b6[0][0].toFixed(2), raff: +o.raff[1][0].toFixed(0), vir: o.vira[5].t && +o.vira[5].t.toFixed(1) }); }
out.sort((a, b) => a.t - b.t); console.log("ordine per errore di TARATURA (Day, F121); conferma = errore su Binns 9/12 e F109");
for (const r of out.slice(0, 12)) console.log(`A ${r.A} zCE ${r.z} tim ${r.h} | taratura ${r.t.toFixed(2)} conferma ${r.c.toFixed(2)} | Day ${r.day} Binns9 ${r.b9} Binns12 ${r.b12} B6 ${r.b6} raff18 ${r.raff} vir16 ${r.vir} | ${r.e.replace(/ si/g, "").replace(/  +/g, " ")}`);
console.log("... le peggiori"); for (const r of out.slice(-2)) console.log(`A ${r.A} zCE ${r.z} tim ${r.h} taratura ${r.t.toFixed(2)} conferma ${r.c.toFixed(2)}`);
const byc = [...out].sort((a, b) => a.c - b.c)[0]; console.log(`migliore in CONFERMA (solo da sapere): A ${byc.A} zCE ${byc.z} tim ${byc.h} conferma ${byc.c.toFixed(2)} taratura ${byc.t.toFixed(2)}`);
