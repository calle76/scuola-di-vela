// Banco voce 81 (fermata 1, 23 nov 2026): copia del motore in memoria, js/ non cambia. Uso: node sperimentale/bolina-81/banco81.js '{"nome":{"zCE":3.2}}'
const M = require("../../tests/fisica/motore.js"), { step, BOAT } = M;
const KN = 1.943844, B0 = Object.assign({}, BOAT);
function eq(kn, twa, sh){ const S = { x:0,y:0,h:0,u:1,vl:0,r:0 };
  for (let t = 0; t < 60; t += 0.05){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, 0.05); if (Math.abs(S.heel) > 60) return null; } return S; }
const best = (kn, twa) => { let b = null; for (let sh = 0; sh <= 1.0001; sh += 0.02){ const S = eq(kn, twa, sh); if (S && (!b || S.u > b.u)) b = S; } return b; };
const vmg = kn => { let b = null; for (let twa = 36; twa <= 60; twa++){ const S = best(kn, twa); const v = S.u * Math.cos(twa * Math.PI / 180); if (!b || v > b.v) b = { v, twa, S }; } return b; };
const DAY = { 6: 2.25 / 0.85, 10: 3.29 / 0.91, 15: 4.07 / 1.07 };
const BI9 = [[42,4.65],[46.5,5.0],[55,5.6],[60,5.9]], BI12 = [[42,5.0],[46.5,5.4],[50,5.65],[55,6.0],[60,6.3]];
const p = x => (x >= 0 ? "+" : "") + Math.round(x * 100);
const varianti = JSON.parse(process.argv[2]);
for (const [nome, v] of Object.entries(varianti)){
  Object.assign(BOAT, B0, v);
  let r = nome.padEnd(22);
  for (const kn of [6, 10, 15]){ const b = vmg(kn); r += ` Day${kn} ${p(b.v * KN / DAY[kn] - 1)}% (fuori ${Math.round((b.S.hike || 0) * 100)}%)`; }
  r += " | B9"; for (const [t, m] of BI9) r += " " + p(best(9, t).u * KN / m - 1);
  r += " | B12"; for (const [t, m] of BI12) r += " " + p(best(12, t).u * KN / m - 1);
  r += " | fuori a 46,5°:"; for (const kn of [6, 8, 9, 10, 12]) r += ` ${kn}n ${Math.round((best(kn, 46.5).hike || 0) * 100)}`;
  console.log(r);
}
