const fs = require("fs"), { step } = new Function(fs.readFileSync(process.argv[2], "utf8") + "\nreturn { step };")(), KN = 1.943844;
for (const [kn, twa] of [[16, 60], [16, 90], [20, 50]]){ const S = { x:0,y:0,h:0,u:0,vl:0,r:0 }; let r = `${kn} nodi ${twa}° vela cazzata da ferma: `;
  for (let t = 0; t <= 30.001; t += .05){ S.h = 0; const I = step(S, { sheet: 0, tiller: 0 }, { twd: twa, tws: kn / KN }, .05); if (Math.abs(t % 5) < .025) r += `${t.toFixed(0)}s ${(S.u*KN).toFixed(1)}kn sband ${S.heel.toFixed(0)}° vela ${S.flat.toFixed(2)}  `; }
  console.log(r); }
