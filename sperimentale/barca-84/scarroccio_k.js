// Voce 84: scarroccio e forza laterale di bolina (miglior VMG) contro F121 fig. 11 (angolo di deriva 3,7/4,0/4,65 gradi a 2-3/4/5 nodi; forza laterale CFD).
const { motore } = require("./banco84.js"), KN = 1.943844, R = Math.PI / 180, C = require("./candidato.json");
for (const c of [C[0], C[3]]){ const { step } = motore(c.P); console.log("## " + c.n.slice(0, 30));
  for (const kn of [3.2, 6, 8, 11, 15]){ let b = null;
    for (let twa = 36; twa <= 54; twa += 2) for (let sh = 0; sh <= .5; sh += .05){ const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; let inf; for (let t = 0; t < 60; t += .05){ S.h = 0; inf = step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, .05); } const v = S.u * Math.cos(twa * R); if (Math.abs(S.heel) < 60 && (!b || v > b.v)) b = { v, u: S.u * KN, lee: inf.leeway, side: inf.side, heel: S.heel }; }
    console.log(`  ${kn} nodi: velocita' ${b.u.toFixed(2)} nodi, scarroccio ${Math.abs(b.lee).toFixed(1)}°, forza laterale ${Math.abs(b.side).toFixed(0)} N, sbandamento ${b.heel.toFixed(0)}°`); } }
