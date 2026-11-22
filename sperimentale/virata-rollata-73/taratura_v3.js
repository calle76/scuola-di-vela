// Voce 73 passo B, prova v3: spinta dei vortici nella raddrizzata, ROLL.cv. Serve rollata_v3.patch (motore e tests/fisica/motore.js che esporta ROLL).
// Taratura su F109 con 3,2 nodi (rollata contro piatta: +3,04 m; sbandamento 55°, sotto la scuffia del gioco a 60°), controllo senza ritocchi con 11 nodi (+2,44 m, sbandamento 30°).
// Gesto: virata da tastiera con Maiusc, X giù quando la prua passa il vento, X su a H gradi. Uso: node sperimentale/virata-rollata-73/taratura_v3.js
const M = require("../../tests/fisica/motore.js"), { step, norm180, BOAT, ROLL } = M;
const DT = 0.01, K = 1.6, KN = 1.943844, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
function corsa(kn, H, lim = 1){
  const S = { x: 0, y: 0, h: -45, u: 1, vl: 0, r: 0, lv: 2 }, E = { twd: 0, tws: kn / KN };
  let info = { awa: 45 }, til = 0, gesto = true, tp = null, su = null, y0 = 0, u0 = 0, ufine = null, umax = 0, cap = false;
  for (let i = 0; i < 10000; i++){ const t = i * DT - 40; if (i === 4000){ y0 = S.y; u0 = S.u; }
    let roll = false, bar;
    if (t >= 0){ if (tp === null && norm180(-S.h) < 0) tp = t;
      if (H !== null){ roll = tp !== null && su === null; if (roll && S.heel >= H){ su = t; roll = false; } }
      if (gesto && norm180(S.h) > 30) gesto = false;
      if (gesto) bar = -lim; else { const e = norm180(45 - S.h); bar = clamp(-e / 25, -45 / 45 * 35 / 45, 35 / 45); }
      if (ufine === null && Math.abs(norm180(45 - S.h)) < 5) ufine = S.u; if (tp !== null && t < tp + 15) umax = Math.max(umax, S.u);
    } else { const e = norm180(-45 - S.h); bar = clamp(-e / 25, -35 / 45, 35 / 45); }
    til += clamp(bar - til, -K * DT, K * DT);
    info = step(S, { sheet: sheetFor(info.awa), tiller: til, roll }, E, DT);
    if (S.heel > BOAT.capsizeAt || S.heel < -45) cap = true; }
  return { d: -(S.y - y0), u0, ufine, umax, cap }; }
const delta = (kn, H) => { const p = corsa(kn, null), r = corsa(kn, H); return { g: r.d - p.d, r, p }; };
console.log("cv  | 3,2 nodi H55: guadagno sulla piatta m (F109 +3,04), velocità a fine virata %, massima dopo il vento % | 11 nodi H30: guadagno (F109 +2,44), fine %, massima %");
for (const cv of [0, 1, 2, 3, 4, 5, 6, 8]){ ROLL.cv = cv; const a = delta(3.2, 55), b = delta(11, 30);
  console.log(`${String(cv).padEnd(3)} | ${a.g.toFixed(2)} m, ${(100 * a.r.ufine / a.r.u0).toFixed(0)}%, ${(100 * a.r.umax / a.r.u0).toFixed(0)}%${a.r.cap ? " SCUFFIA" : ""} | ${b.g.toFixed(2)} m, ${(100 * b.r.ufine / b.r.u0).toFixed(0)}%, ${(100 * b.r.umax / b.r.u0).toFixed(0)}%${b.r.cap ? " SCUFFIA" : ""}`); }
