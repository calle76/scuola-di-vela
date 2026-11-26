// Voce 84, giro K: angolo del boma scelto dalla barca a bolina (miglior VMG) contro F109 tab. 4.1 (vela a meta' altezza: 13° con 3,2 nodi, 19° con 11 nodi).
// Uso: node boma_schutt.js  (legge candidato.json: OGGI e J)
const { motore } = require("./banco84.js"), KN = 1.943844, R = Math.PI / 180, C = require("./candidato.json");
for (const c of C.slice(0, 2)){ const M = motore(c.P), { step, BOAT } = M; const r = [];
  for (const kn of [3.2, 6, 11, 15]){ let b = null;
    for (let twa = 36; twa <= 54; twa += 2) for (let sh = 0; sh <= 0.5001; sh += 0.025){ const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; let inf, ul = 0; for (let i = 0; i < 1200; i++){ S.h = 0; inf = step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, 0.05); if (i % 100 === 99){ if (i > 300 && Math.abs(S.u - ul) < 5e-4) break; ul = S.u; } }
      const v = S.u * Math.cos(twa * R) * KN; if (Math.abs(S.heel) < 60 && (!b || v > b.v)) b = { v, twa, sh, boom: BOAT.minBoom + sh * (BOAT.maxBoom - BOAT.minBoom), awa: inf && inf.awa, tw: S.tw84 || S.tw || 0, fl: S.flat }; }
    r.push(`${kn} nodi: boma ${b.boom.toFixed(1)}° (TWA ${b.twa}°, AWA ${b.awa !== undefined ? Math.abs(b.awa).toFixed(1) : "?"}°, vela piatta ${b.fl !== undefined ? b.fl.toFixed(2) : "-"}, svergolamento ${(+b.tw).toFixed(2)})`); }
  console.log("## " + c.n + "\n  " + r.join("\n  ")); }
