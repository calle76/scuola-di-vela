// Voce 84: Marshall (ISBS): meno raddrizzata, quanta VMG si perde. Uso: node marshall.js
const { motore } = require("./banco84.js"), KN = 1.943844, R = Math.PI / 180;
const F = JSON.parse(require("fs").readFileSync(__dirname + "/candidato.json"))[1].P;
for (const [n, P, m0] of [["oggi", {}, 75], ["candidato", F, 80]]) for (const kn of [10, 12, 14, 16]){ let r = [];
  for (const d of [0, 119, 178]){ const Q = JSON.parse(JSON.stringify(P)); Q.boat = Q.boat || {}; Q.boat.hikeArm = (Q.boat.hikeArm || 1) - d / (m0 * 9.81); const { step } = motore(Q); let b = null;
    for (let a = 38; a <= 56; a += 1) for (let sh = 0; sh <= .4; sh += .02){ const S = { x:0,y:0,h:0,u:1.5,vl:0,r:0 }; for (let t = 0; t < 40; t += .05){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: a, tws: kn / KN }, .05); } if (Math.abs(S.heel) > 60) continue; const v = S.u * Math.cos(a * R) * KN; if (!b || v > b.v) b = { v, a, u: S.u * KN }; } r.push(b); }
  console.log(`${n} ${kn} nodi: ` + r.map((b, i) => [0, -119, -178][i] + ` N·m u ${b.u.toFixed(2)} a ${b.a}° VMG ${b.v.toFixed(2)} (${((b.v / r[0].v - 1) * 100).toFixed(0)}%)`).join(" | ")); }
console.log("Marshall: -119: -0,32 nodi e +2 gradi (circa -9%); -178: -0,92 nodi e +6 gradi (circa -26%)");
