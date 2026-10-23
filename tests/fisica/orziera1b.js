// Barca dell'1b orziera sbandando (1.0.46, docs/PROPOSTA-ORZIERA-1B.md): criteri 2-4 della proposta e sensibilità.
// Uso: node orziera1b.js [k]   k moltiplica il termine nuovo (0 = senza; 1,3 = zCE 2,6 m; 0,9 = zCE 1,8 m; 1,54 = Izz 130; 0,67 = Izz 300).
// Il fattore si ottiene aggiungendo dopo step() (k − 1) volte il termine del motore: il resto della barca non cambia.
const { step, BOAT, RUD2, RUD2_SICURA } = require("./motore.js");
const D2R = Math.PI / 180, KN = 1.943844, f = (x, d = 1) => x.toFixed(d).replace(".", ",");
const k = process.argv[2] === undefined ? 1 : Number(process.argv[2].replace(",", "."));
function passo(S, C, E, dt){
  const phi = S.heel * D2R, o = step(S, C, E, dt); // il motore usa lo sbandamento d'inizio passo
  if (k !== 1 && S.u >= RUD2.uMin && !C.push) S.r += (k - 1) * (o.awa >= 0 ? 1 : -1) * o.drive * BOAT.zCE * Math.sin(phi) / RUD2.Izz * dt / D2R;
  return o;
}
function equilibrio(kn, twa){ // prua fissa, barra al centro, scotta migliore (come bolina.js)
  let b = null;
  for (let sh = 0; sh <= 1.0001; sh += 0.05){
    const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0, lv: 2 };
    for (let t = 0; t < 40; t += 0.05){ S.h = 0; S.r = 0; step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, 0.05); }
    if (!b || S.u > b.S.u) b = { S, sh };
  }
  return b;
}
const pilota = S => { const e = ((S.h + 540) % 360) - 180; return Math.max(-RUD2_SICURA, Math.min(RUD2_SICURA, 0.04 * e + 0.02 * S.r)); };
let ok = true; const esito = (c, s) => { if (!c) ok = false; return (c ? "ok   " : "FUORI") + " " + s; };
console.log(`Termine orziero × ${f(k, 2)}`);
console.log("Criterio 2: barra al centro, vento costante, quanto sale la prua in media nei primi 10 s (soglia 1 °/s)");
for (const kn of [6, 10, 14]) for (const twa of [45, 90]){
  const { S, sh } = equilibrio(kn, twa);
  for (let t = 0; t < 10; t += 0.02) passo(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, 0.02);
  const v = norm(S.h) / 10; // prua girata verso il vento (vento da dritta: h cresce)
  console.log("  " + esito(k === 0 || v <= 1, `${kn} nodi ${twa}°: ${f(v, 2)} °/s`));
}
function raffica(kn, twa, modo, lasca){
  const { S, sh } = equilibrio(kn, twa); let mT = 0, st = 0, mE = 0, mH = 0;
  for (let t = 0; t < 4; t += 0.02){
    const C = { sheet: Math.min(1, sh + (t > 0.5 ? lasca : 0)), tiller: modo === "pilota" ? pilota(S) : 0 };
    passo(S, C, { twd: twa, tws: 1.6 * kn / KN }, 0.02);
    mT = Math.max(mT, Math.abs(C.tiller) * RUD2.maxRudder); if (S.stall) st += 0.02; mE = Math.max(mE, norm(S.h)); mH = Math.max(mH, S.heel);
  }
  return { prua: norm(S.h), mT, st, mE, mH };
}
function norm(h){ return ((h + 540) % 360) - 180; }
console.log("Criterio 3: raffica +60% per 4 s con 10 nodi, barra al centro: quanto sale la prua (soglia almeno 5°)");
for (const twa of [45, 90]){ const r = raffica(10, twa, "centro", 0); console.log("  " + esito(k === 0 || r.prua >= 5, `${twa}°: ${f(r.prua)}°, sbandamento max ${f(r.mH)}°`)); }
console.log("Criterio 4: raffica 14→22 nodi di bolina, il pilota tiene la prua (soglie: scotta ferma barra oltre 20°, lascando sotto 10°)");
const a = raffica(14, 45, "pilota", 0), b = raffica(14, 45, "pilota", 0.3);
console.log("  " + esito(k === 0 || a.mT > 20, `scotta ferma: barra max ${f(a.mT)}°, stallo ${f(a.st, 2)} s, prua fuori al massimo ${f(a.mE)}°, sbandamento max ${f(a.mH)}°`));
console.log("  " + esito(k === 0 || b.mT < 10, `scotta lascata di 0,3: barra max ${f(b.mT)}°, stallo ${f(b.st, 2)} s, prua fuori al massimo ${f(b.mE)}°, sbandamento max ${f(b.mH)}°`));
console.log("Altre raffiche (senza soglia), barra al centro / pilota:");
for (const [kn, twa] of [[6, 45], [6, 90], [14, 90]]){
  const c = raffica(kn, twa, "centro", 0), p = raffica(kn, twa, "pilota", 0);
  console.log(`  ${kn}→${f(1.6 * kn, 0)} nodi ${twa}°: prua ${f(c.prua)}° / barra max ${f(p.mT)}°, stallo ${f(p.st, 2)} s`);
}
console.log(k === 0 ? "(senza il termine: le soglie non si applicano)" : ok ? "ESITO: OK" : "ESITO: FUORI");
