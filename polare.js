// Diagramma polare: velocità di equilibrio a vari angoli dal vento, con la scotta migliore. Uso: node polare.js
const { step } = require("./motore.js");
for (const kn of [6, 10, 15]){
  let riga = `Vento ${kn} nodi: `;
  for (const twa of [20, 25, 30, 45, 60, 90, 110, 135, 150, 180]){
    let best = 0;
    for (let sh = 0; sh <= 1.0001; sh += 0.02){
      const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0 };
      for (let t = 0; t < 60; t += 0.05){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / 1.944 }, 0.05); if (Math.abs(S.heel) > 60) break; }
      if (Math.abs(S.heel) <= 60) best = Math.max(best, S.u);
    }
    riga += `${twa}°=${(best * 1.944).toFixed(1)} `;
  }
  console.log(riga);
}
