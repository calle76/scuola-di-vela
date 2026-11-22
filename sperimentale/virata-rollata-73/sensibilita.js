// Voce 73, fermata 1 della virata contro F109: una costante del motore cambiata solo in memoria (js/motore.js non si tocca), poi
// (a) virata con la prua imposta come in F109 (3,2 nodi in 10 s, 11 nodi in 5 s), metri contro il dritto da −15 a +15 s e velocità minima;
// (b) effetto collaterale: VMG di bolina a regime (45° e 55°) con 4 e 11 nodi. Uso: node sperimentale/virata-rollata-73/sensibilita.js
const fs = require("fs"), path = require("path");
const SRC = fs.readFileSync(path.join(__dirname, "..", "..", "js", "motore.js"), "utf8");
const motore = rep => { let s = SRC; for (const [a, b] of rep){ if (!s.includes(a)) throw new Error("non trovato: " + a); s = s.replace(a, b); }
  return new Function(s + "\nreturn { step, BOAT };")(); };
const DT = 0.01, KN = 1.943844, clamp = (v, a, b) => Math.max(a, Math.min(b, v)), D2R = Math.PI / 180;
function prova(M){ const { step, BOAT } = M, sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1); const out = {};
  for (const [kn, T] of [[3.2, 10], [11, 5]]){ const prua = t => t <= -T / 2 ? -45 : t >= T / 2 ? 45 : -45 * Math.cos(Math.PI * (t + T / 2) / T);
    const S = { x: 0, y: 0, h: 315, u: 1, vl: 0, r: 0, lv: 2 }, E = { twd: 0, tws: kn / KN }; let info = { awa: 45 }, vmg0, u0, tot = 0, umin = 9;
    for (let i = 0; i < 7500; i++){ const t = i * DT - 60, h = t < -15 ? -45 : prua(t); S.r = (prua(t + DT) - h) / DT; S.h = (h + 360) % 360;
      const yp = S.y; info = step(S, { sheet: sheetFor(info.awa), tiller: 0 }, E, DT); S.h = (h + 360) % 360;
      if (t < -15 && t > -15 - 2 * DT){ vmg0 = -(S.y - yp) / DT; u0 = S.u; }
      if (t >= -15){ tot += -(S.y - yp) - vmg0 * DT; umin = Math.min(umin, S.u); } }
    out["v" + kn] = tot; out["m" + kn] = umin / u0; }
  for (const kn of [4, 11]) for (const twa of [45, 55]){ const S = { x: 0, y: 0, h: 360 - twa, u: 1, vl: 0, r: 0, lv: 2 }; let o = { awa: twa };
    for (let i = 0; i < 6000; i++){ o = step(S, { sheet: sheetFor(o.awa), tiller: 0 }, { twd: 0, tws: kn / KN }, 0.01); S.h = 360 - twa; S.r = 0; }
    out["p" + kn + "_" + twa] = S.u * Math.cos((twa + Math.atan2(Math.abs(S.vl), S.u) / D2R) * D2R) * KN; }
  return out; }
const VAR = [
  ["motore del gioco", []],
  ["vela che sbatte: niente +0,2 di resistenza", [["(alpha < 6 ? 0.2 * (1 - alpha / 6) : 0)", "0"]]],
  ["angolo morto più stretto: luffA0 15°", [["luffA0: 22,", "luffA0: 15,"]]],
  ["angolo morto più largo nella transizione: luffW 14°", [["luffW: 7,", "luffW: 14,"]]],
  ["scafo −20% (hullScale 0,8)", [["hullScale: 1,", "hullScale: 0.8,"]]],
  ["massa +20% (162 kg: acqua trascinata, ipotesi)", [["mass: 135,", "mass: 162,"]]],
  ["indotta spenta (TE 0)", [["TE: 0.80", "TE: 0"]]] ];
const f = (x, d = 2) => x.toFixed(d);
console.log("F109: 3,2 nodi −0,67 m (minima ~70%); 11 nodi −4,39 m (minima ~51%). Polare: VMG in nodi a 45° e 55°.");
let base = null;
for (const [nome, rep] of VAR){ const r = prova(motore(rep)); if (!base) base = r;
  const dp = k => (r[k] === base[k] ? "" : ` (${r[k] > base[k] ? "+" : ""}${f(100 * (r[k] / base[k] - 1), 1)}%)`);
  console.log(`${nome.padEnd(52)} | 3,2 nodi ${f(r["v3.2"])} m, minima ${f(100 * r["m3.2"], 0)}% | 11 nodi ${f(r.v11)} m, minima ${f(100 * r.m11, 0)}% | VMG 4 nodi ${f(r.p4_45)}${dp("p4_45")} / ${f(r.p4_55)}${dp("p4_55")}, 11 nodi ${f(r.p11_45)}${dp("p11_45")} / ${f(r.p11_55)}${dp("p11_55")}`); }
