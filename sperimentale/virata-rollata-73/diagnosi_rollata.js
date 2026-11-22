// Voce 73 passo B (22 nov 2026), non adottato. Serve il motore con rollata.patch applicata (git apply sperimentale/virata-rollata-73/rollata.patch).
// Uso: node sperimentale/virata-rollata-73/diagnosi_rollata.js "$PWD" (dalla radice del repo). Barca a regime 40 s, poi virata con Maiusc.
// Diagnosi: con 4, 6, 12 nodi (Maiusc), quanto vale ogni pezzo del gesto. Varianti: X giusto; solo raddrizzata (sbandamento messo a 20° di colpo al rilascio, fase 1 gratis);
// X giusto senza vento del rollio (vRoll azzerato: resta solo l'effetto dello sbandare); velocità minima e media in 10 s dopo il passaggio.
const M = require(process.argv[2] + "/tests/fisica/motore.js"), { step, norm180, BOAT, RUD2_SICURA } = M;
const DT = 0.01, KN = 1.943844, L = BOAT.length, K = 1.6, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
function corsa(kn, lim, modo){
  const S = { x: 0, y: 0, h: -45, u: 0, vl: 0, r: 0, lv: 2 }, E = { twd: 0, tws: kn / KN }; let info = { awa: 45 }, til = 0, gesto = true, tp = null, tr = null, roll = false, umin = 9;
  const ctl = (h, bar) => { if (bar === undefined){ const e = norm180(h - S.h); bar = clamp(-e / 25, -RUD2_SICURA, RUD2_SICURA); } til += clamp(bar - til, -K * DT, K * DT); };
  for (let i = 0; i < 10000; i++){ const t = i * DT - 40;
    if (t < 0){ ctl(-45); info = step(S, { sheet: sheetFor(info.awa), tiller: til }, E, DT); continue; }
    if (i === 4000) { var y0 = S.y; }
    if (modo !== "senza"){
      if (tp === null && norm180(-S.h) < 0) tp = t;
      roll = tp !== null && tr === null; if (roll && -info.awa > BOAT.luffA0 + BOAT.luffW){ tr = t; roll = false; if (modo === "solo"){ S.heel = 20; S.heelRate = 0; } }
      if (modo === "solo") roll = roll ? false : (tr !== null && S.rollT === undefined && t - tr < DT * 1.5);
    }
    if (gesto && norm180(S.h) > 30) gesto = false;
    gesto ? ctl(0, -lim) : ctl(45);
    info = step(S, { sheet: sheetFor(info.awa), tiller: til, roll }, E, DT);
    if (t > 0 && t < 15) umin = Math.min(umin, S.u);
  }
  return { d: -(S.y - y0), umin, tp, tr };
}
for (const kn of [4, 6, 12]){
  const base = corsa(kn, 1, "senza");
  for (const m of ["senza", "giusto", "solo"]){ const r = corsa(kn, 1, m); console.log(kn, m, "guadagno su senza X:", ((r.d - base.d) / L).toFixed(2), "L", "minima", (r.umin * KN).toFixed(2), "giù", r.tp && r.tp.toFixed(2), "su", r.tr && r.tr.toFixed(2)); } }
