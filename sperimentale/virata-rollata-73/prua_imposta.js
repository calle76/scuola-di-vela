// Voce 73: virata piatta con la prua imposta come in F109 fig. 4.11 (letta a occhio: con 3,2 nodi da −45° a +45° in circa 10 s, con 11 nodi in circa 5 s,
// curva a S centrata sul vento in prua a t = 0). La prua è imposta (niente timone, niente freno della pala): misura solo vela e scafo del gioco.
// Confronto con F109 fig. 4.12-4.13: metri verso il vento contro il dritto da −15 a +15 s, velocità minima e a +15 s. Uso: node sperimentale/virata-rollata-73/prua_imposta.js
const { step, norm180, BOAT } = require("../../tests/fisica/motore.js");
const DT = 0.01, KN = 1.943844, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
const F109 = { 3.2: "F109: prima +1,48, dopo −2,15, totale −0,67 m; minima ~70%, a +15 s ~85%", 11: "F109: prima +0,50, dopo −4,89, totale −4,39 m; minima ~51%, a +15 s ~93%" };
for (const [kn, Ts] of [[3.2, [6, 8, 10, 12]], [11, [3, 4, 5, 6]]]){ console.log(F109[kn]);
  for (const T of Ts){
    const prua = t => t <= -T / 2 ? -45 : t >= T / 2 ? 45 : -45 * Math.cos(Math.PI * (t + T / 2) / T);
    const S = { x: 0, y: 0, h: -45, u: 1, vl: 0, r: 0, lv: 2 }, E = { twd: 0, tws: kn / KN }; let info = { awa: 45 }, vmg0 = null, u0, prima = 0, dopo = 0, umin = 9;
    for (let i = 0; i < 7500; i++){ const t = i * DT - 60;
      const h = t < -15 ? -45 : prua(t); S.r = (prua(t + DT) - h) / DT; S.h = (h + 360) % 360;
      const yp = S.y; info = step(S, { sheet: sheetFor(info.awa), tiller: 0 }, E, DT); S.h = (h + 360) % 360;
      if (t < -15 && t > -15 - 2 * DT){ vmg0 = -(S.y - yp) / DT; u0 = S.u; }
      if (t >= -15){ const d = -(S.y - yp) - vmg0 * DT; if (t < 0) prima += d; else dopo += d; umin = Math.min(umin, S.u); } }
    console.log(`  ${kn} nodi, virata in ${T} s: prima ${prima.toFixed(2)}, dopo ${dopo.toFixed(2)}, totale ${(prima + dopo).toFixed(2)} m; minima ${(100 * umin / u0).toFixed(0)}%, a +15 s ${(100 * S.u / u0).toFixed(0)}%; velocità di partenza ${u0.toFixed(2)} m/s`); } }
