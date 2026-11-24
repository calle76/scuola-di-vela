// svergolamento come Day 2017 eq. 4-5 (copia in memoria): t sale quando il timoniere e' al limite; braccio = zA + zH*(1-t) (zH = 1,867 m, 36,4% dell'inferitura; a t=0 fa 3,0); resistenza indotta in piu' 8*t^2*CL^2/(pi*AR)
const fs = require("fs"), path = require("path"), src0 = fs.readFileSync(path.join(__dirname, "../../js/motore.js"), "utf8");
const KN = 1.943844, R = Math.PI / 180;
function motore(o){ let s = src0;
  if (o.tw){ const rep = (a, b) => { if (!s.includes(a)) throw a; s = s.replace(a, b); };
    rep("const drive = push ? push.Fx : L * Math.sin(A * D2R) - Dg * Math.cos(A * D2R);", "const TWI = S.tw || 0, DgT = Dg + q * 8 * TWI * TWI * Math.pow(CL(alpha) * lf, 2) / (Math.PI * BOAT.arT); const drive = push ? push.Fx : L * Math.sin(A * D2R) - DgT * Math.cos(A * D2R);");
    rep("const side = push ? push.Fy * (awa >= 0 ? -1 : 1) : L * Math.cos(A * D2R) + Dg * Math.sin(A * D2R);", "const side = push ? push.Fy * (awa >= 0 ? -1 : 1) : L * Math.cos(A * D2R) + DgT * Math.sin(A * D2R);");
    rep("const mHeel = side * BOAT.zCE * Math.cos(phi);", "const mHeel = side * (BOAT.zCE - BOAT.zH * (S.tw || 0)) * Math.cos(phi);");
    rep("const hikeTarget =", "const over = Math.max(0, Math.min(1, (mHeel - BOAT.formK * 0.08) / (BOAT.sailorMass * 9.81 * BOAT.hikeArm) - BOAT.twOn)); const tT = Math.min(BOAT.twMax, (S.tw || 0) + (over > 0 ? over : ((mHeel - BOAT.formK * 0.08) / (BOAT.sailorMass * 9.81 * BOAT.hikeArm) < BOAT.twOn - 0.05 ? -1 : 0)) * BOAT.twK * dt); S.tw = Math.max(0, tT); const hikeTarget ="); }
  const M = new Function(s + "\nreturn { step, BOAT, RUD2, RUD2_SICURA, DERIVA2, BOMA2, SALTI2, newShift, stepShift, CL, CD, norm180, norm360, hullDrag };")(); Object.assign(M.BOAT, { zH: 1.867, arT: 3.4, twOn: 0.95, twMax: 0.3, twK: 1 }, o.v); return M; }
module.exports = motore;
if (require.main === module){
const DAY = { 6: 2.25 / 0.85, 10: 3.29 / 0.91, 15: 4.07 / 1.07 }, BI9 = [[42,4.65],[46.5,5.0],[55,5.6],[60,5.9]], BI12 = [[42,5.0],[46.5,5.4],[50,5.65],[55,6.0],[60,6.3]];
for (const o of JSON.parse(process.argv[2])){ const { step, BOAT } = motore(o);
  const eq = (kn, twa, sh) => { const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; for (let t = 0; t < 60; t += 0.05){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, 0.05); if (Math.abs(S.heel) > 60) return null; } return S; };
  const best = (kn, twa, hi = 0.5) => { let b = null; for (let sh = 0; sh <= hi + 1e-6; sh += 0.02){ const s = eq(kn, twa, sh); if (s && (!b || s.u > b.u)) b = s; } return b || { u: 0 }; };
  const vm = kn => { let b = null; for (let a = 34; a <= 56; a++){ const s = best(kn, a), x = s.u * Math.cos(a * R); if (!b || x > b.v) b = { v: x, a, s }; } return b; };
  const p = x => (x >= 0 ? "+" : "") + Math.round(x * 100);
  let r = o.n.padEnd(26) + "| Day"; for (const k of [6, 10, 15, 20]){ const b = vm(k); r += DAY[k] ? ` ${k}n ${p(b.v * KN / DAY[k] - 1)}` : ` ${k}n ${(b.v * KN).toFixed(2)}`; r += `(t${(b.s.tw || 0).toFixed(2)})`; }
  r += " | B9"; for (const [a, m] of BI9) r += " " + p(best(9, a).u * KN / m - 1); r += " | B12"; for (const [a, m] of BI12) r += " " + p(best(12, a).u * KN / m - 1);
  console.log(r); } }
