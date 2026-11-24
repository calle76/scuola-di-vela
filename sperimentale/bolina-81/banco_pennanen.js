// Voce 81 (25 nov 2026): confronto con Pennanen 2015 (F121, fig. 23-29): vento vero a 45 gradi per 2, 3, 4 e 5 nodi di barca, e resistenza totale. Copia del motore in memoria. Uso: node sperimentale/bolina-81/banco_pennanen.js
const M = require("../../tests/fisica/motore.js"), { step, BOAT, hullDrag, CL, CD, norm180 } = M;
const KN = 1.943844, B0 = Object.assign({}, BOAT), R = Math.PI / 180;
function eq(kn, twa, sh){ const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; for (let t = 0; t < 90; t += 0.05){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, 0.05); if (Math.abs(S.heel) > 60) return null; } return S; }
function forze(S, kn, twa, sh){ // ricalcolo delle forze all'equilibrio, come in step
  const v = kn / KN, tw = [-Math.sin(twa * R) * v, Math.cos(twa * R) * v].map(x=>x); // vento verso cui soffia, in assi terra con prua 0 = nord (y negativo avanti)
  const aw = [tw[0] - S.vl, tw[1] + S.u], aws = Math.hypot(...aw), awa = Math.abs(norm180(Math.atan2(-aw[0], aw[1]) / R)), A = awa;
  const boom = Math.min(BOAT.minBoom + sh * (BOAT.maxBoom - BOAT.minBoom), Math.max(0, A - 2)), al = A - boom;
  const q = 0.5 * BOAT.rho * BOAT.sailArea * aws * aws * Math.cos((S.heel||0) * R), lf = Math.max(0, Math.min(1, (A - BOAT.luffA0) / BOAT.luffW));
  const L = q * CL(al) * lf, D = q * CD(al), side = L * Math.cos(A * R) + D * Math.sin(A * R), drive = L * Math.sin(A * R) - D * Math.cos(A * R);
  const Ri = side * side * S.u * S.u / (Math.PI * 0.5 * BOAT.rhoW * BOAT.TE ** 2 * (S.u * S.u + 0.4) ** 2), RiPuro = side * side / (Math.PI * 0.5 * BOAT.rhoW * BOAT.TE ** 2 * S.u * S.u);
  return { A, aws: aws * KN, al, cl: CL(al) * lf, cd: CD(al), drive, side, hull: hullDrag(S.u), Ri, RiPuro, lw: Math.atan2(Math.abs(S.vl), S.u) / R, heel: S.heel, hike: S.hike };
}
const PEN = [[3.28, 2, 9.5], [4.94, 3, 21.7], [6.91, 4, 42.7], [10.5, 5, 91.5]];
const V = { "oggi": {}, "vela 0,27": { sailCL2: 0.042 }, "vela 0,27 braccio 3,0": { sailCL2: 0.042, zCE: 3.0 }, "vela 0,27 braccio 3,0 rampa 15 boma 5": { luffA0: 15, minBoom: 5, sailCL2: 0.042, zCE: 3.0 } };
for (const [n, v] of Object.entries(V)){ Object.assign(BOAT, B0, v); console.log("## " + n);
  for (const [w, ub, rp] of PEN){ let b = null; for (let sh = 0; sh <= 0.6; sh += 0.01){ const s = eq(w, 45, sh); if (s && (!b || s.u > b.s.u)) b = { s, sh }; }
    const f = forze(b.s, w, 45, b.sh); console.log(`vento ${w} nodi: gioco ${(b.s.u * KN).toFixed(2)} nodi, tesi ${ub} (${((b.s.u * KN / ub - 1) * 100).toFixed(0)}%) | app. ${f.A.toFixed(1)}° ${f.aws.toFixed(1)} nodi alfa ${f.al.toFixed(0)} CL ${f.cl.toFixed(2)} CD ${f.cd.toFixed(3)} | spinta ${f.drive.toFixed(1)} N, lato ${f.side.toFixed(0)} N, scafo+app ${f.hull.toFixed(1)}, indotta ${f.Ri.toFixed(1)} | scarroccio ${f.lw.toFixed(1)}° sband. ${f.heel.toFixed(1)}° fuori ${(f.hike * 100).toFixed(0)}%`); } }
Object.assign(BOAT, B0); console.log("## a parita' di velocita' (vento della tesi, TWA 45, scotta migliore per la spinta), resistenze e spinta del gioco");
for (const [w, ub, rp] of PEN){ const u = ub / KN; let best = null;
  for (let sh = 0; sh <= 0.6; sh += 0.01){ const S0 = { u, vl: 0, heel: 0, hike: 0 }; let f = forze(S0, w, 45, sh); for (let k = 0; k < 6; k++){ S0.vl = -f.side / (M.DERIVA2.q * Math.hypot(u, M.DERIVA2.u0)); f = forze(S0, w, 45, sh); } if (!best || f.drive > best.f.drive) best = { f, sh }; }
  const f = best.f; console.log(`${ub} nodi, vento ${w}: spinta gioco ${f.drive.toFixed(1)} N (tesi ${rp}); resistenza gioco ${(f.hull + f.Ri).toFixed(1)} = scafo+appendici ${f.hull.toFixed(1)} + indotta ${f.Ri.toFixed(1)} (formula pura ${f.RiPuro.toFixed(1)}), tesi ${rp}; lato ${f.side.toFixed(0)} N, CL ${f.cl.toFixed(2)} CD ${f.cd.toFixed(3)} app ${f.A.toFixed(1)}° scarr. ${f.lw.toFixed(1)}°`); }
