// Bolina (1.0.11, docs/PROPOSTA-BOLINA.md): VMG, quote di resistenza indotta, Binns, quanto vicino al vento, partenza da ferma.
// Uso: node bolina.js [barca]   con barca = nuova (predefinita) | 1010 (la barca della 1.0.10) | soloA | soloB   ·   node bolina.js polare [barca]
const M = require("./motore.js"), { step, BOAT, hullDrag } = M;
const VECCHIA = { TE: 0, minBoom: 14, luffA0: 27, sailCL2: 0.12 }; // la 1.0.10: senza resistenza indotta, vela di prima
const barche = { nuova: {}, "1010": VECCHIA, soloA: { minBoom: 14, luffA0: 27, sailCL2: 0.12 }, soloB: { TE: 0 } };
const arg = process.argv.slice(2), polare = arg[0] === "polare", nome = arg[polare ? 1 : 0] || "nuova";
if (!barche[nome]) { console.log("barca sconosciuta: " + nome); process.exit(1); }
Object.assign(BOAT, barche[nome]);
const KN = 1.943844, f = (x, d = 2) => x === null ? "mai (30 s)" : x.toFixed(d).replace(".", ",");

if (polare){ // come polare.js, per confrontare quattro motori carattere per carattere
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
  process.exit(0);
}

// equilibrio a prua fissa per 60 s (come polare.js), con la scotta data
function eq(kn, twa, sh){
  const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0 }; let o;
  for (let t = 0; t < 60; t += 0.05){ S.h = 0; o = step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / 1.944 }, 0.05); if (Math.abs(S.heel) > 60) return null; }
  return { S, o };
}
const migliore = (kn, twa) => { let b = null; for (let sh = 0; sh <= 1.0001; sh += 0.02){ const e = eq(kn, twa, sh); if (e && (!b || e.S.u > b.S.u)) b = e; } return b; };
// resistenza indotta e resistenza in acqua ricalcolate con le stesse formule di step() (motore.js), allo stato di equilibrio
function quote(e){
  const { S, o } = e, side = o.side; // barra al centro: il freno del timone vale zero
  const Ri = BOAT.TE > 0 ? side * side * S.u * Math.abs(S.u) / (Math.PI * 0.5 * BOAT.rhoW * BOAT.TE * BOAT.TE * (S.u * S.u + 0.4) ** 2) : 0;
  const res = hullDrag(S.u);
  const tot = res * (1 + Math.pow(Math.abs(S.heel) / 30, 2) * 0.6) + Ri;
  const ruh = leggiArea(S.u) * BOAT.hullScale * 0.5 * BOAT.rhoW * S.u * S.u;
  return { Ri, tot, ruh };
}
function leggiArea(u){ // area della vasca senza appDA: hullDrag con appDA = 0
  const a = BOAT.appDA, h = BOAT.hullScale; BOAT.appDA = 0; BOAT.hullScale = 1; const d = hullDrag(u); BOAT.appDA = a; BOAT.hullScale = h;
  return d / (0.5 * BOAT.rhoW * u * Math.abs(u));
}

console.log(`Barca: ${nome} (TE ${BOAT.TE}, minBoom ${BOAT.minBoom}, luffA0 ${BOAT.luffA0}, luffW ${BOAT.luffW}, sailCL2 ${BOAT.sailCL2})`);
console.log("VMG di bolina: nodi (angolo dal vento reale, vento apparente, Ri sul totale in acqua, Ri sullo scafo nudo)");
let r = " ";
for (const kn of [5, 6, 10, 15]){
  let b = null;
  for (let twa = 32; twa <= 70; twa++){ const e = migliore(kn, twa); const v = e.S.u * Math.cos(twa * Math.PI / 180); if (!b || v > b.v) b = { v, twa, e }; }
  const q = quote(b.e);
  r += ` ${kn} nodi ${f(b.v * KN)} (${b.twa}°, ${f(Math.abs(b.e.o.awa), 1)}°, ${f(100 * q.Ri / q.tot, 1)}%, ${f(q.Ri / q.ruh)});`;
}
console.log(r);
r = "VMG di poppa:";
for (const kn of [6, 10, 15]){ let b = 0; for (let twa = 130; twa <= 180; twa += 2) b = Math.max(b, -migliore(kn, twa).S.u * Math.cos(twa * Math.PI / 180)); r += ` ${kn} nodi ${f(b * KN)};`; }
console.log(r);
r = "Binns 9 nodi a 42° / 46,5° / 55° / 60° (misure 4,65 / 5,0 / 5,6 / 5,9):"; for (const t of [42, 46.5, 55, 60]) r += " " + f(migliore(9, t).S.u * KN); console.log(r);
r = "Binns 12 nodi a 42° / 46,5° / 50° / 55° / 60° (misure ~5,0 / 5,4 / 5,65 / 6,0 / 6,3):"; for (const t of [42, 46.5, 50, 55, 60]) r += " " + f(migliore(12, t).S.u * KN); console.log(r);
r = "Quanto vicino al vento, 10 nodi, a 26° / 28° / 30° / 32° / 34° / 36° / 40° / 45°:";
for (const t of [26, 28, 30, 32, 34, 36, 40, 45]){ let b = -9; for (let sh = 0; sh <= 1.0001; sh += 0.02){ const e = eq(10, t, sh); if (e) b = Math.max(b, e.S.u); } r += " " + f(b * KN, 1); }
console.log(r);
// partenza da ferma a 60° dal vento con 10 nodi, scotta migliore per quell'angolo, passi di 1/240 s
let sh60 = 0, u60 = -9; for (let sh = 0; sh <= 1.0001; sh += 0.02){ const e = eq(10, 60, sh); if (e && e.S.u > u60){ u60 = e.S.u; sh60 = sh; } }
const S = { x: 0, y: 0, h: 0, u: 0, vl: 0, r: 0 }; let t2 = null, t3 = null;
for (let i = 0; i < 30 * 240; i++){ S.h = 0; step(S, { sheet: sh60, tiller: 0 }, { twd: 60, tws: 10 / 1.944 }, 1 / 240); const k = S.u * 1.944; if (t2 === null && k >= 2) t2 = i / 240; if (t3 === null && k >= 3) t3 = i / 240; }
console.log(`Partenza da ferma a 60° con 10 nodi: 2 nodi in ${f(t2, 1)} s, 3 nodi in ${f(t3, 1)} s`);
