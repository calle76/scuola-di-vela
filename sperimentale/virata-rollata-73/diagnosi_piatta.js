// Voce 73: virata piatta con poco vento contro F109 fig. 4.12-4.13 (3,2 nodi: +1,48 m prima del vento, −2,15 m dopo; velocità minima circa 70% di quella di prima).
// Uso: node sperimentale/virata-rollata-73/diagnosi_piatta.js   (motore del gioco; non serve la patch)
const { step, norm180, BOAT, RUD2_SICURA } = require("../../tests/fisica/motore.js");
const DT = 0.01, K = 1.6, KN = 1.943844, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
for (const kn of [3.2, 11]) for (const [nome, lim, vel] of [["freccia", RUD2_SICURA, 1.6], ["Maiusc", 1, 1.6], ["barra 20°", 20 / 45, 1.6], ["barra 15°", 15 / 45, 1.6], ["barra 10°", 10 / 45, 1.6]]){
  const S = { x: 0, y: 0, h: -45, u: 1, vl: 0, r: 0, lv: 2 }, E = { twd: 0, tws: kn / KN }; let info = { awa: 45 }, til = 0, gesto = true, tp = null, y0, u0, vmg0, prima = 0, dopo = 0, umin = 9, durata = null;
  for (let i = 0; i < 7000; i++){ const t = i * DT - 40;
    if (i === 4000){ y0 = S.y; u0 = S.u; }
    let bar;
    if (t < 0){ const e = norm180(-45 - S.h); bar = clamp(-e / 25, -RUD2_SICURA, RUD2_SICURA); }
    else { if (gesto && norm180(S.h) > 30) gesto = false; if (gesto) bar = -lim; else { const e = norm180(45 - S.h); bar = clamp(-e / 25, -RUD2_SICURA, RUD2_SICURA); } }
    til += clamp(bar - til, -(t >= 0 && gesto ? vel : K) * DT, (t >= 0 && gesto ? vel : K) * DT);
    const yp = S.y; info = step(S, { sheet: sheetFor(info.awa), tiller: til }, E, DT);
    if (i === 3999) vmg0 = -(S.y - yp) / DT;
    if (t >= 0){ if (tp === null && norm180(-S.h) < 0) tp = t; const d = -(S.y - yp) - vmg0 * DT; if (tp === null) prima += d; else dopo += d; umin = Math.min(umin, S.u);
      if (durata === null && Math.abs(norm180(45 - S.h)) < 5) durata = t; }
  }
  console.log(`${kn} nodi ${nome}: prua al vento a ${tp === null ? "mai (non vira)" : tp.toFixed(1) + " s"}, a 5° dalla nuova bolina a ${durata === null ? "—" : durata.toFixed(1)} s; prima del vento ${prima >= 0 ? "+" : ""}${prima.toFixed(2)} m, dopo ${dopo.toFixed(2)} m, totale ${(prima + dopo).toFixed(2)} m; minima ${(100 * umin / u0).toFixed(0)}%`);
}
