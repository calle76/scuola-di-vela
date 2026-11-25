// Voce 84: cosa succede a 16 nodi con la scotta della regola (boma = apparente - 17) prima e durante la virata. Uso: node traccia16.js '{P}' nodi
const { motore } = require("./banco84.js"), KN = 1.943844, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const P = JSON.parse(process.argv[2]), kn = +process.argv[3] || 16;
for (const fl0 of [1, 0.6]) for (const u0 of [1.5, 2.5]) for (const g of [17, 12, 10]){ const M = motore(P), { step, BOAT } = M, S = { x:0,y:0,h:-45,u:u0,vl:0,r:0, flat: fl0 }, E = { twd: 0, tws: kn / KN }; let info = { awa: 45 }, r = "", mx = 0;
  for (let i = 0; i < 4000; i++){ S.h = -45; S.r = 0; const sh = clamp((Math.max(BOAT.minBoom, Math.abs(info.awa) - g) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1); info = step(S, { sheet: sh, tiller: 0 }, E, .01); mx = Math.max(mx, Math.abs(S.heel)); if ([100, 300, 1000, 3999].includes(i)) r += ` | ${(i / 100).toFixed(0)}s u ${(S.u * KN).toFixed(1)} sb ${S.heel.toFixed(0)} fl ${(S.flat || 1).toFixed(2)} fuori ${S.hike.toFixed(2)}`; }
  console.log(`flat iniziale ${fl0}, u0 ${u0}, boma = app - ${g}: sb max ${mx.toFixed(0)}${r}`); }
