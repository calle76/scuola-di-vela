// Voce 84, sesto giro: tutti i controlli su M (off 7, par 0,105, scafo 0,93: regola di GIRO6.md con il pareggio sciolto per distanza da L, dichiarato) e M5 (minimo assoluto: off 5).
const { misura, stampa, motore } = require("./banco84.js"), C = require("./candidato.json"), KN = 1.943844, R = Math.PI / 180;
const fai = (off, hs) => { const P = JSON.parse(JSON.stringify(C[3].P)); P.off = off; P.boat.hullScale = hs; return P; };
const M = fai(7, .93), M5 = fai(5, .93); module.exports = { M, M5 };
if (require.main === module){
  const src = require("fs").readFileSync(__dirname + "/virate_semb.js", "utf8").split("\nconst MIS")[0];
  const virata = new Function("require", src.replace(/require\("\.\//g, 'require("' + __dirname + '/') + "\nreturn virata;")(require);
  const regate = { 6: [3.7, 2.5, 3.3, 4.2], 10: [4.5, 3.2, 4.7, 5.8], 15: [4.9, 3.7, 7.8, 9.1] }; // Pan e Sun: velocità di bolina, VMG bolina, VMG poppa, lasco (medie di regata)
  for (const [n, P] of [["M", M], ["M5", M5]]){ stampa(n + " (rotta)", misura(P));
    for (const kn of [14, 18]){ const r = virata(P, kn, 45); console.log(`  Semb ${kn} nodi: uscita ${(r.uout / r.uin * 100).toFixed(0)}% media ${(r.umean / r.uin * 100).toFixed(0)}% 80% ${r.t80 === null ? "mai" : r.t80.toFixed(1) + " s"} (misura 92 / 86 / 7,6)`); }
    const { step } = motore(P), eq = (kn, twa, sh) => { const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; for (let t = 0; t < 60; t += .05){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, .05); } return S; };
    for (const kn of [6, 10, 15]){ let up = null, dn = null, re = 0; for (let a = 36; a <= 54; a += 2) for (let sh = 0; sh <= .5; sh += .05){ const S = eq(kn, a, sh); if (Math.abs(S.heel) > 60) continue; const l = Math.atan2(Math.abs(S.vl), Math.max(.3, S.u)) / R, v = Math.hypot(S.u, S.vl), w = v * Math.cos((a + l) * R) * KN; if (!up || w > up.w) up = { w, v: v * KN }; }
      for (let a = 140; a <= 180; a += 5) for (let sh = .5; sh <= 1; sh += .05){ const S = eq(kn, a, sh), w = Math.abs(S.u * Math.cos(a * R)) * KN; if (!dn || w > dn) dn = w; }
      for (let sh = .3; sh <= 1; sh += .05){ const S = eq(kn, 110, sh); re = Math.max(re, S.u * KN); }
      const g = regate[kn]; console.log(`  regate ${kn} nodi (Pan e Sun, medie: bolina ${g[0]}, VMG ${g[1]}, poppa ${g[2]}, lasco ${g[3]}): barca bolina ${up.v.toFixed(2)}, VMG ${up.w.toFixed(2)}, VMG poppa ${dn.toFixed(2)}, lasco 110° ${re.toFixed(2)}`); } } }
