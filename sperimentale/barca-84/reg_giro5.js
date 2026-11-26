// Voce 84, quinto giro §5 (GIRO5.md): lo smorzamento della resistenza indotta `reg` sul candidato L.
// Vincolo: quota dell'indotta a 5 nodi fra 9 e 12% (Day fig. 11: 10,5%; conto come scomponi84.js). Scelta: errore più piccolo sulle virate F109 (somma degli scarti a 3,2 e 11 nodi).
// Conferma, non usata per scegliere: 12 virate di Semb (F137), 14 nodi (misura: uscita 92%, media 86%, 80% dopo 7,6 s); 18 nodi solo informativo.
const { motore } = require("./banco84.js"), { prova, CASI } = require("./virata_f109.js"), { L } = require("./giro5.js"), KN = 1.943844, R = Math.PI / 180;
const src = require("fs").readFileSync(__dirname + "/virate_semb.js", "utf8").split("\nconst MIS")[0];
const virata = new Function("require", src.replace(/require\("\.\//g, 'require("' + __dirname + '/') + "\nreturn virata;")(require);
function quota(P){ const M = motore(P), { step, BOAT, hullDrag } = M; let b = null;
  for (let a = 38; a <= 50; a++) for (let sh = 0; sh <= .3; sh += .02){ const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; let i; for (let t = 0; t < 60; t += .05){ S.h = 0; i = step(S, { sheet: sh, tiller: 0 }, { twd: a, tws: 5 / KN }, .05); }
    const v = S.u * Math.cos(a * R); if (!b || v > b.v) b = { v, S, i }; }
  const u = b.S.u, side = b.i.side, hd = hullDrag(u), Ri = side * side * u * u / (Math.PI * .5 * BOAT.rhoW * BOAT.TE ** 2 * (u * u + P.reg) ** 2); return Ri / (hd + Ri) * 100; }
for (const reg of [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4]){ const P = Object.assign({}, L, { reg }), M = motore(P), q = quota(P);
  const f = CASI.map(c => prova(M, c, 9).rms), s14 = virata(P, 14, 45), s18 = virata(P, 18, 45), pc = (r, x) => (r[x] / r.uin * 100).toFixed(0) + "%";
  console.log(`reg ${reg}: quota indotta 5 nodi ${q.toFixed(1)}% ${q >= 9 && q <= 12 ? "(ammesso)" : "(fuori)"} | F109 scarti ${f.map(x => x.toFixed(3)).join(" + ")} = ${(f[0] + f[1]).toFixed(3)} | Semb 14 nodi uscita ${pc(s14, "uout")} media ${pc(s14, "umean")} 80% ${s14.t80 === null ? "mai" : s14.t80.toFixed(1) + " s"} | 18 nodi uscita ${pc(s18, "uout")} media ${pc(s18, "umean")} 80% ${s18.t80 === null ? "mai" : s18.t80.toFixed(1) + " s"}`); }
