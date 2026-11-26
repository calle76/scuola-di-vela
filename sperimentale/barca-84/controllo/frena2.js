const fs = require("fs"), { step } = new Function(fs.readFileSync(process.argv[2], "utf8") + "\nreturn { step };")(), KN = 1.943844;
for (const kn of [12, 18]){ let b = { u: 0, sh: 0 }; for (let sh = 0; sh <= 1; sh += .05){ const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; let ok = true; for (let t = 0; t < 50; t += .05){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: 45, tws: kn / KN }, .05); if (Math.abs(S.heel) > 60) { ok = false; break; } } if (ok && S.u > b.u) b = { u: S.u, sh }; }
  const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; for (let t = 0; t < 30; t += .05){ S.h = 0; step(S, { sheet: b.sh, tiller: 0 }, { twd: 45, tws: kn / KN }, .05); }
  let r = `${kn} nodi (bolina con scotta ${b.sh.toFixed(2)}, sband ${S.heel.toFixed(0)}, fuori bordo ${S.hike.toFixed(2)}) poi prua a 20° e vela lascata: `;
  for (let t = 0; t <= 6.001; t += .05){ S.h = 0; step(S, { sheet: 1, tiller: 0 }, { twd: 20, tws: kn / KN }, .05); if (Math.abs(t % 0.5) < .025) r += `${t.toFixed(1)}s ${(S.u*KN).toFixed(1)}kn ${S.heel.toFixed(0)}°  `; }
  console.log(r); }
