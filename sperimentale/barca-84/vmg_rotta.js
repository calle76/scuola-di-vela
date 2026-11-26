// Voce 84, rilettura (26 nov): il banco calcola la VMG con la prua (u·cos angolo di prua) e mette la barca a un angolo di PRUA dato.
// Day (F17, «speed, track, heel, leeway») e i GPS (Binns, regate) misurano velocità e angolo sulla ROTTA, scarroccio compreso.
// Qui: stessa ricerca del banco, ma VMG = velocità sulla rotta × cos(angolo di prua + scarroccio); Binns all'angolo di rotta dato.
const { motore } = require("./banco84.js"), C = require("./candidato.json"), { gzTab } = require("./gz470.js"), KN = 1.943844, R = Math.PI / 180;
const DAY = { 6: 2.65, 10: 3.62, 15: 3.80 }, BI9 = [[42,4.65],[46.5,5.0],[55,5.6],[60,5.9]], BI12 = [[42,5.0],[46.5,5.4],[50,5.65],[55,6.0],[60,6.3]];
function stato(step, kn, twa, sh){ const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; let inf; for (let t = 0; t < 60; t += .05){ S.h = 0; inf = step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, .05); }
  if (Math.abs(S.heel) > 60) return null; const lee = Math.abs(Math.atan2(S.vl, Math.max(.3, S.u))) / R, v = Math.hypot(S.u, S.vl); return { u: S.u, v, lee, rotta: twa + lee }; }
function misura(P){ const { step } = motore(P), shs = []; for (let sh = 0; sh <= .5001; sh += .025) shs.push(sh);
  const migliore = (kn, twa, f) => { let b = null; for (const sh of shs){ const s = stato(step, kn, twa, sh); if (s && (!b || f(s) > f(b))) b = s; } return b; };
  const day = [6, 10, 15].map(k => { let bp = null, br = null; for (let a = 36; a <= 54; a++){ const s = migliore(k, a, x => x.u); const vp = s.u * Math.cos(a * R) * KN, vr = s.v * Math.cos(s.rotta * R) * KN; if (!bp || vp > bp) bp = vp; if (!br || vr > br) br = vr; }
    return [(bp / DAY[k] - 1) * 100, (br / DAY[k] - 1) * 100]; });
  const binns = (kn, T) => T.map(([a, m]) => { const sp = migliore(kn, a, x => x.u); let sr = null; for (let h = a - 6; h <= a; h += .5){ const s = migliore(kn, h, x => x.v); if (s && Math.abs(s.rotta - a) < .3 && (!sr || s.v > sr.v)) sr = s; } // prua tale che la rotta sia a
    return [(sp.u * KN / m - 1) * 100, sr ? (sr.v * KN / m - 1) * 100 : NaN]; });
  return { day, b9: binns(9, BI9), b12: binns(12, BI12) }; }
const f = x => (x >= 0 ? "+" : "") + x.toFixed(1);
if (process.argv[2] !== "sspa") for (const [n, P] of [["oggi", C[0].P], ["K", C[3].P], ["K + forma 470", Object.assign({}, C[3].P, { gzTab })]]){ const o = misura(P);
  console.log(`## ${n}\n  Day 6/10/15 (B1 ≥ −5, B4 ≤ +7): con la prua ${o.day.map(d => f(d[0])).join(" ")} | con la rotta ${o.day.map(d => f(d[1])).join(" ")}`);
  console.log(`  Binns 9 (B2 ±5): con la prua ${o.b9.map(d => f(d[0])).join(" ")} | con la rotta ${o.b9.map(d => f(d[1])).join(" ")}`);
  console.log(`  Binns 12 (B3 ±3): con la prua ${o.b12.map(d => f(d[0])).join(" ")} | con la rotta ${o.b12.map(d => f(d[1])).join(" ")}`); }
// solo per stimare la distanza (dopo aver visto il risultato, non è una scelta): scafo della vasca SSPA (×0,93)
if (process.argv[2] === "sspa") { const P = Object.assign({}, C[3].P, { boat: Object.assign({}, C[3].P.boat, { hullScale: .93 }) }), o = misura(P);
  console.log(`## K con lo scafo ×0,93\n  Day con la rotta ${o.day.map(d => f(d[1])).join(" ")} | Binns 9 ${o.b9.map(d => f(d[1])).join(" ")} | Binns 12 ${o.b12.map(d => f(d[1])).join(" ")}`); }
