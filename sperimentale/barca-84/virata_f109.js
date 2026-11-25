// Voce 84: virata piatta di F109 secondo per secondo (Schutt 2017 fig. 4.10-4.13, letta a occhio: +/-0,03 della velocita', +/-2 gradi). Prua imposta, scotta come F109 tab. 4.1: 3,2 nodi ferma; 11 nodi lascata di 15 gradi da 0 a 3 s.
// Uso: node virata_f109.js '[{"n":..,"P":..,"src":"file motore" opzionale}]'
const fs = require("fs"), { motore } = require("./banco84.js"), KN = 1.943844, R = Math.PI / 180;
const it = (T, x) => { if (x <= T[0][0]) return T[0][1]; for (let i = 1; i < T.length; i++) if (x <= T[i][0]) return T[i-1][1] + (T[i][1] - T[i-1][1]) * (x - T[i-1][0]) / (T[i][0] - T[i-1][0]); return T[T.length-1][1]; };
const HL = [[-6,-45],[-5,-44],[-4,-40],[-3,-33],[-2,-23],[-1,-11],[0,0],[1,11],[2,21],[3,30],[4,37],[5,42],[6,46],[7,49],[8,51],[10,50],[12,48],[15,46]];
const HM = [[-3,-43],[-2.5,-42],[-2,-38],[-1.5,-32],[-1,-24],[-.5,-12],[0,0],[.5,13],[1,24],[1.5,32],[2,38],[2.5,41],[3,43]];
const CASI = [["3,2 nodi", 3.2, HL, t => 0, 1.06, { t: [-2,0,1,2,3,5,8,10,14.95], u: [.96,.87,.77,.71,.71,.71,.80,.78,.84] }, [1.48, -2.15]], ["11 nodi", 11, HM, t => t > 0 && t < 3 ? 15 : 0, 2.37, { t: [-2,0,1,2,3,5,8,10,14.95], u: [.965,.80,.59,.54,.59,.74,.88,.91,.94] }, [.5, -4.89]]];
const CASI2 = CASI;
function prova(M, caso, boom0){ const [n, kn, H, ease, u0v, ser] = caso, { step, BOAT } = M, DT = .01, S = { x:0,y:0,h:-45,u:1,vl:0,r:0 }, E = { twd: 0, tws: kn / KN }; let h0 = H[0][1], v0 = 0, u0 = 1, prima = 0, dopo = 0, er = [], hm = 0, lee = 0, info;
  const boomSh = b => Math.max(0, Math.min(1, (b - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom)));
  const p = t => it(H, t); let heel0 = 0;
  for (let i = 0; i < 7502; i++){ const t = i * DT - 60, h = t < -15 ? h0 : p(t), r = (p(t + DT) - p(t)) / DT; S.r = t < -15 ? 0 : r; S.h = (h + 360) % 360; const yp = S.y;
    const til = S.u > .05 ? Math.max(-1, Math.min(1, -Math.atan2(S.r * R * 1.9, S.u) / R / 45)) : 0;
    info = step(S, { sheet: boomSh(boom0 + ease(t)), tiller: til }, E, DT); S.h = (h + 360) % 360;
    if (t < -15){ v0 = -(S.y - yp) / DT; u0 = S.u; heel0 = S.heel; lee = Math.atan2(Math.abs(S.vl), S.u) / R; } else { const d = -(S.y - yp) - v0 * DT; if (t < 0) prima += d; else dopo += d; hm = Math.max(hm, Math.abs(S.heel)); }
    ser.t.forEach((tt, j) => { if (Math.abs(t - tt) < DT / 2) er[j] = S.u / u0; }); }
  const rms = Math.sqrt(er.reduce((a, x, j) => a + (x - ser.u[j]) ** 2, 0) / er.length);
  return { u0, er, rms, prima, dopo, heel0, hm, lee }; }
module.exports = { prova, CASI };
if (require.main === module) for (const v of JSON.parse(process.argv[2])){ const M = v.src ? new Function(fs.readFileSync(v.src, "utf8") + "\nreturn { step, BOAT };")() : motore(v.P); console.log("## " + v.n);
  for (const c of CASI){ const a = prova(M, c, v.boom || 9), f = c[6];
    console.log(`  ${c[0]}: u0 ${a.u0.toFixed(2)} (F109 ${c[4]}, ${((a.u0 / c[4] - 1) * 100).toFixed(0)}%) scarroccio ${a.lee.toFixed(1)}° sband ${a.heel0.toFixed(0)} max ${a.hm.toFixed(0)} | prima ${a.prima.toFixed(2)} (${f[0]}) dopo ${a.dopo.toFixed(2)} (${f[1]}) tot ${(a.prima + a.dopo).toFixed(2)} (${(f[0] + f[1]).toFixed(2)}) | u/u0 ${a.er.map(x => x.toFixed(2)).join(" ")} (F109 ${c[5].u.join(" ")}) scarto ${a.rms.toFixed(3)}`); } }
