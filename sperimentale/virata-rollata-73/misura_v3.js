// Voce 73 passo B, prova v3 (23 nov 2026): v2 + spinta dei vortici ROLL.cv (argomento). Serve rollata_v3.patch. Colonna in più: velocità massima nei 15 s dopo il vento in prua / prima (regola 42.3(b): mai sopra 100%).
// Uso (dalla radice del repo): node sperimentale/virata-rollata-73/misura_v3.js [cv]
// Barca a regime 40 s di bolina a 45°, poi virata da tastiera (barra fino a 30° oltre il vento, poi timoniere pulito; freccia o Maiusc), 60 s.
// Metri persi contro 60 s dritti (positivo = perso). Gesto: X giù quando la prua passa il vento (+ spostamento), X su quando lo sbandamento arriva a H gradi.
const { step, norm180, BOAT, RUD2_SICURA, ROLL } = require("../../tests/fisica/motore.js"); ROLL.cv = +(process.argv[2] || 0);
const DT = 0.01, K = 1.6, KN = 1.943844, L = BOAT.length, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
let casi = 0;
function corsa(kn, lim, H, sposta = 0, tacca = true){
  const S = { x: 0, y: 0, h: -45, u: 1, vl: 0, r: 0, lv: 2 }, E = { twd: 0, tws: kn / KN };
  let info = { awa: 45 }, til = 0, gesto = true, tp = null, giu = null, su = null, cap = false, heelMax = 0, u0 = 0, ufine = null, umax = 0;
  const ctl = (h, bar) => { if (bar === undefined){ const e = norm180(h - S.h); bar = clamp(-e / 25, -RUD2_SICURA, RUD2_SICURA); } til += clamp(bar - til, -K * DT, K * DT); };
  let y0 = 0;
  for (let i = 0; i < 10000; i++){ const t = i * DT - 40;
    if (i === 4000){ y0 = S.y; u0 = S.u; }
    let roll = false;
    if (t >= 0 && tacca){
      if (tp === null && norm180(-S.h) < 0) tp = t;
      if (H !== null){
        if (giu === null && tp !== null && t >= tp + sposta) giu = t;
        if (giu === null && sposta < 0 && tp === null && t >= 0 && norm180(-S.h) < 30 && norm180(-S.h) > 0 && t >= 0){ /* prima del vento: stima col tempo della corsa senza X */ }
        roll = giu !== null && su === null; if (roll && S.heel >= H){ su = t; roll = false; } }
      if (gesto && norm180(S.h) > 30) gesto = false;
      gesto ? ctl(0, -lim) : ctl(45);
      if (ufine === null && Math.abs(norm180(45 - S.h)) < 5) ufine = S.u; if (tp !== null && t < tp + 15) umax = Math.max(umax, S.u);
    } else ctl(-45);
    info = step(S, { sheet: sheetFor(info.awa), tiller: til, roll }, E, DT);
    if (S.heel > BOAT.capsizeAt || S.heel < -45) cap = true;
    if (t > 0) heelMax = Math.max(heelMax, S.heel);
  }
  casi++;
  return { d: -(S.y - y0), cap, heelMax, tp, giu, su, rapp: ufine === null ? null : ufine / u0, mx: umax / u0 };
}
const f = (x, d = 1) => x === null || !isFinite(x) ? "—" : x.toFixed(d);
console.log("cv = " + ROLL.cv); console.log("F109 (Laser, in acqua): 3,2 nodi virata piatta −0,67 m, rollata +2,37 m (guadagna); 11 nodi piatta −4,39 m, rollata −1,95 m.");
console.log("vento barra | dritto m | senza X persi m | con X (H = sbandamento al rilascio): persi m, velocità a fine virata / prima, sbandamento max");
for (const kn of [3.2, 4, 6, 8, 10, 11, 12, 14, 16]) for (const [nome, lim] of [["freccia", RUD2_SICURA], ["Maiusc", 1]]){
  const dr = corsa(kn, lim, null, 0, false), sx = corsa(kn, lim, null);
  let riga = `${String(kn).padStart(4)} ${nome.padEnd(7)} | ${f(dr.d)} | ${f(dr.d - sx.d)}${sx.cap ? " SCUFFIA" : ""} |`;
  for (const H of [20, 30, 40, 55]){ const r = corsa(kn, lim, H); riga += ` H${H}: ${f(dr.d - r.d)} m ${f(r.rapp === null ? null : 100 * r.rapp, 0)}%/${f(100 * r.mx, 0)}% ${f(r.heelMax, 0)}°${r.cap ? " SCUFFIA" : ""};`; }
  console.log(riga); }
console.log("\nspostamento di X dopo il passaggio del vento (H = 40): persi m");
for (const kn of [3.2, 6, 11]){ const dr = corsa(kn, 1, null, 0, false); let riga = `${String(kn).padStart(4)} Maiusc |`;
  for (const s of [0, 0.5, 1, 1.5, 2]){ const r = corsa(kn, 1, 40, s); riga += ` +${s} s: ${f(dr.d - r.d)}${r.cap ? " S" : ""};`; } console.log(riga); }
console.log(`\ncorse: ${casi}`);
