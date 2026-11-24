// Voce 81, seconda proposta (docs/PROPOSTA-VELA-E-RAMPA-81.md): varianti di vela, braccio e rampa, con svergolamento facoltativo (zTw). Copia del motore in memoria.
// Uso: node sperimentale/bolina-81/esplora81.js '[["nome",{"luffA0":15,"sailCL2":0.042,"zCE":2.4},0]]'  (terzo numero 1 = braccio che cala di zTw col timoniere al limite)
const fs = require("fs"), src0 = fs.readFileSync(require("path").join(__dirname, "../../js/motore.js"), "utf8");
function motore(twist){ let s = src0; if (twist){ const a = "const mHeel = side * BOAT.zCE * Math.cos(phi);"; if (!s.includes(a)) throw 1; s = s.replace(a, "const mHeel = side * (BOAT.zCE - BOAT.zTw * Math.max(0, Math.min(1, ((S.hike||0) - 0.8) / 0.2))) * Math.cos(phi);"); }
  return new Function(s + "\nreturn { step, BOAT, hullDrag, CL, CD };")(); }
const KN = 1.943844, R = Math.PI / 180;
const DAY = { 6: 2.25 / 0.85, 10: 3.29 / 0.91, 15: 4.07 / 1.07 }, BI9 = [[42,4.65],[46.5,5.0],[55,5.6],[60,5.9]], BI12 = [[42,5.0],[46.5,5.4],[50,5.65],[55,6.0],[60,6.3]], PEN = [[3.28,2],[4.94,3],[6.91,4],[10.5,5]];
for (const [n, v, tw] of JSON.parse(process.argv[2])){ const M = motore(tw), { step, BOAT } = M; Object.assign(BOAT, v);
  const eq = (kn, twa, sh) => { const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; for (let t = 0; t < 60; t += 0.05){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, 0.05); if (Math.abs(S.heel) > 60) return null; } return S; };
  const best = (kn, twa, hi = 1) => { let b = null; for (let sh = 0; sh <= hi + 1e-6; sh += 0.02){ const s = eq(kn, twa, sh); if (s && (!b || s.u > b.u)) b = s; } return b || { u: 0 }; };
  const vm = kn => { let b = null; for (let a = 30; a <= 60; a++){ const s = best(kn, a, 0.5), x = s.u * Math.cos(a * R); if (!b || x > b.v) b = { v: x, a }; } return b; };
  const p = x => (x >= 0 ? "+" : "") + Math.round(x * 100);
  let r = n + " | Day"; for (const k of [6, 10, 15]){ const b = vm(k); r += ` ${k}n ${p(b.v * KN / DAY[k] - 1)} (${b.a}°)`; }
  r += " | B9"; for (const [a, m] of BI9) r += " " + p(best(9, a, .5).u * KN / m - 1); r += " | B12"; for (const [a, m] of BI12) r += " " + p(best(12, a, .5).u * KN / m - 1);
  r += " | Pen"; for (const [w, b] of PEN) r += " " + p(best(w, 45, .5).u * KN / b - 1);
  r += " | 3,2n45 " + best(3.2, 45, .5).u.toFixed(2); r += " | stringe 6n: " + [25, 30, 35, 38, 40].map(a => a + "°" + (best(6, a, .5).u * KN).toFixed(2)).join(" "); r += " | poppa 12n 90/135/180 " + [90, 135, 180].map(a => (best(12, a).u * KN).toFixed(2)).join("/");
  console.log(r); }
