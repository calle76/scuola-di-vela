// Scarroccio della barca dell'1b (1.0.45, docs/archivio/PROPOSTA-SCARROCCIO-1B.md): equilibrio a prua fissa come bolina.js, ma VMG sulla rotta vera (prua + scarroccio).
// Uso: node scarroccio1b.js [470]   con 470: sensibilità con la forza laterale del 470 misurata in vasca e scalata (F35 fig. 12, K 1,35 m² invece di 1,70)
const { step, DERIVA2 } = require("./motore.js");
if (process.argv[2] === "470"){ const k = 2.042 / 2.574; DERIVA2.q *= k; DERIVA2.u0 /= k; } // stessa barca ferma: q·u0 resta 268
const KN = 1.943844, f = (x, d = 2) => x.toFixed(d).replace(".", ",");
function eq(lv, kn, twa, sh){
  const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0 }; if (lv === 2) S.lv = 2; let o;
  for (let t = 0; t < 60; t += 0.05){ S.h = 0; o = step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / 1.944 }, 0.05); if (Math.abs(S.heel) > 60) return null; }
  return { S, o };
}
const migliore = (lv, kn, twa) => { let b = null; for (let sh = 0; sh <= 1.0001; sh += 0.02){ const e = eq(lv, kn, twa, sh); if (e && (!b || e.S.u > b.S.u)) b = e; } return b; };
for (const lv of [1, 2]){
  let r = `Barca ${lv === 2 ? "dell'1b" : "dell'1a"}, bolina: VMG sulla rotta vera (angolo dal vento, scarroccio, velocità, sbandamento)`;
  for (const kn of [5, 6, 10, 15]){
    let b = null;
    for (let twa = 32; twa <= 70; twa++){ const e = migliore(lv, kn, twa), cog = twa + Math.abs(e.o.leeway), v = Math.hypot(e.S.u, e.S.vl) * Math.cos(cog * Math.PI / 180); if (!b || v > b.v) b = { v, twa, e }; }
    r += `\n  ${kn} nodi: ${f(b.v * KN)} (${b.twa}°, ${f(Math.abs(b.e.o.leeway), 1)}°, ${f(b.e.S.u * KN)} nodi, ${f(Math.abs(b.e.S.heel), 1)}°)`;
  }
  r += "\n  10 nodi, scarroccio a 45° / 60° / 90°:"; for (const t of [45, 60, 90]) r += " " + f(Math.abs(migliore(lv, 10, t).o.leeway), 1) + "°";
  r += "; velocità a 90° / 135°:"; for (const t of [90, 135]) r += " " + f(migliore(lv, 10, t).S.u * KN);
  const S = { x: 0, y: 0, h: 0, u: 0, vl: 0, r: 0 }; if (lv === 2) S.lv = 2;
  for (let t = 0; t < 20; t += 0.05){ S.h = 0; S.u = 0; step(S, { sheet: 1, tiller: 0 }, { twd: 90, tws: 10 / 1.944 }, 0.05); }
  console.log(r + `\n  ferma al traverso con 10 nodi, vela lascata: velocità laterale ${f(Math.abs(S.vl), 3)} m/s`);
}
