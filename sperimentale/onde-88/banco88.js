// Voce 88, passo 1: banco delle onde sopra la barca M (criteri O1-O8 come scritti in BANCO-ONDE.md prima di lanciarlo; O9 in o9/).
// Uso: node banco88.js [misura|conferma]   (misura = semi 1-10, conferma = semi 11-20). Una misura per volta col freno.
const fs = require("fs"), path = require("path");
const src = fs.readFileSync(path.join(__dirname, "motore88.js"), "utf8");
const { step, onde88crea, norm180, norm360 } = new Function(src + "\nreturn { step, onde88crea, norm180, norm360 };")();
const KN = 1.943844, R = Math.PI / 180, FETCH = 5000, DT = 0.05;
const gruppo = process.argv[2] || "misura", SEMI = gruppo === "conferma" ? [11,12,13,14,15,16,17,18,19,20] : [1,2,3,4,5,6,7,8,9,10];
const TWD = 180; // vento da sud; prua = TWD + angolo (mura fissa)
// una corsa: o.kn, o.a (angolo dal vento), o.sh (scotta), o.seme (null = acqua piatta), o.pilota (O5), o.T
function corsa(o){
  const T = o.T || 240, tws = o.kn / KN, W = o.seme == null ? null : onde88crea(tws, TWD, FETCH, o.seme);
  const S = { x: 0, y: 0, h: norm360(TWD + o.a), u: 1, vl: 0, r: 0 }, up = [Math.sin(TWD * R), -Math.cos(TWD * R)];
  let su = 0, sv = 0, n = 0, mx = 0, cap = false, firma = 0, hP = o.a;
  for (let t = 0; t < T - 1e-9; t += DT){
    if (o.pilota){ const voluto = (S.fOnda || 0) > 0 ? Math.min(180, o.a + 20) : o.a; hP += Math.max(-15 * DT, Math.min(15 * DT, voluto - hP)); }
    S.h = norm360(TWD + (o.pilota ? hP : o.a));
    if (W) W.t = t;
    step(S, { sheet: o.sh, tiller: 0 }, { twd: TWD, tws, onde: W }, DT);
    if (Math.abs(S.heel) > 60){ cap = true; break; }
    const h = S.h * R, bv = [Math.sin(h) * S.u + Math.cos(h) * S.vl, -Math.cos(h) * S.u + Math.sin(h) * S.vl], v = Math.hypot(bv[0], bv[1]);
    firma = (firma * 31 + S.x * 7 + S.y * 13 + S.u * 17 + S.heel) % 1e9;
    if (t >= 40){ su += v; sv += bv[0] * up[0] + bv[1] * up[1]; n++; if (v > mx) mx = v; }
  }
  return { v: su / Math.max(1, n) * KN, vmg: sv / Math.max(1, n) * KN, max: mx * KN, cap, firma, S };
}
const memo = {};
function scotta(kn, a){ const ch = kn + ":" + a; if (memo[ch] !== undefined) return memo[ch];
  let b = -1, bs = 0; const hi = a < 90 ? 0.5 : 1;
  for (let sh = 0; sh <= hi + 1e-6; sh += 0.02){ const r = corsa({ kn, a, sh, seme: null, T: 50 }); if (!r.cap && r.v > b){ b = r.v; bs = sh; } }
  return memo[ch] = bs; }
const media = xs => xs.reduce((s, x) => s + x, 0) / xs.length, mediana = xs => { const z = [...xs].sort((p, q) => p - q), m = z.length >> 1; return z.length % 2 ? z[m] : (z[m - 1] + z[m]) / 2; };
const pc = (x, y) => `${x >= y ? "+" : ""}${((x / y - 1) * 100).toFixed(1)}%`;
function caso(kn, a, pil){ const sh = scotta(kn, a), piatta = corsa({ kn, a, sh, seme: null });
  const rr = SEMI.map(s => corsa({ kn, a, sh, seme: s, pilota: pil })); return { sh, piatta, rr, v: media(rr.map(r => r.v)), vmg: media(rr.map(r => r.vmg)), max: mediana(rr.map(r => r.max)), cap: rr.filter(r => r.cap).length }; }
const esiti = []; const chk = (nome, ok, testo) => { esiti.push([nome, ok]); console.log(`${ok ? "ok     " : "NO     "} ${nome} ${testo}`); };
console.log(`=== banco onde, gruppo «${gruppo}» (semi ${SEMI[0]}-${SEMI[SEMI.length - 1]}), fetch ${FETCH / 1000} km ===`);
for (const kn of [6, 7, 9, 10, 12, 15]){ const W = onde88crea(kn / KN, TWD, FETCH, 1); console.log(`onde con ${kn} nodi: Hs ${W.Hs.toFixed(2)} m, Tp ${W.Tp.toFixed(2)} s, lunghezze ${W.comps.map(c => (2 * Math.PI / c.k).toFixed(1)).join("/")} m`); }
// O1
for (const kn of [6, 7]){ const righe = []; let ok = true;
  for (const a of [45, 60, 90, 110, 135, 150, 180]){ const c = caso(kn, a); const d = c.v / c.piatta.v - 1; if (Math.abs(d) >= 0.01 || c.cap) ok = false; righe.push(`${a}°: ${c.piatta.v.toFixed(2)} → ${c.v.toFixed(2)} (${pc(c.v, c.piatta.v)})`); }
  chk("O1", ok, `${kn} nodi: ${righe.join("; ")}`); }
// O2, O3, O4
const BETH = { 9: { 135: 6.1, 180: 5.5 }, 12: { 135: 8.0, 180: 6.7 } };
for (const kn of [9, 10, 12, 15]) for (const a of [135, 150, 180]){ const c = caso(kn, a), g = c.v / c.piatta.v - 1;
  const riga = `${kn} nodi ${a}°: piatta ${c.piatta.v.toFixed(2)}, onde ${c.v.toFixed(2)} (${pc(c.v, c.piatta.v)}, semi ${Math.min(...c.rr.map(r => r.v)).toFixed(2)}-${Math.max(...c.rr.map(r => r.v)).toFixed(2)}), punta mediana ${c.max.toFixed(2)} (${pc(c.max, c.piatta.v)}), scuffie ${c.cap}`;
  if (kn !== 9) chk("O2", g >= 0 && g <= 0.12 && !c.cap, riga); else console.log("        " + riga);
  if (BETH[kn] && BETH[kn][a]) chk("O3", c.v < BETH[kn][a], `${kn} nodi ${a}°: ${c.v.toFixed(2)} contro Bethwaite/Binns ${BETH[kn][a]}`);
  if ((kn === 12 || kn === 15) && a === 180) chk("O4", c.max >= 1.2 * c.piatta.v, `${kn} nodi 180°: punta mediana ${pc(c.max, c.piatta.v)} (soglia +20%)`); }
// O5
// 26 nov, corretto dopo il primo lancio: la VMG di poppa è -vmg (il metro misura controvento); prima sceglieva l'angolo peggiore
for (const kn of [10, 12, 15]){ let b = null;
  for (let a = 135; a <= 180; a += 5){ const c = caso(kn, a); if (!b || -c.vmg > -b.c.vmg) b = { a, c }; }
  const pil = caso(kn, b.a, true), vp = -pil.vmg, vf = -b.c.vmg;
  chk("O5", vp > vf, `${kn} nodi: VMG di poppa a prua ferma ${vf.toFixed(3)} (a ${b.a}°, piatta ${(-b.c.piatta.vmg).toFixed(3)}), pilota sull'onda ${vp.toFixed(3)} (${pc(vp, vf)}), scuffie ${pil.cap}`); }
// O6, O7
for (const kn of [10, 15]){ let bp = null, bo = null;
  for (let a = 36; a <= 54; a++){ const c = caso(kn, a); if (!bp || c.piatta.vmg > bp.v) bp = { a, v: c.piatta.vmg }; if (!bo || c.vmg > bo.v) bo = { a, v: c.vmg, cap: c.cap }; }
  const p = 1 - bo.v / bp.v, [lo, hi] = kn === 10 ? [0.03, 0.15] : [0.08, 0.25];
  chk("O6", p >= lo && p <= hi, `${kn} nodi: VMG di bolina piatta ${bp.v.toFixed(3)} (${bp.a}°), con le onde ${bo.v.toFixed(3)} (${bo.a}°): perdita ${(p * 100).toFixed(1)}% (soglia ${lo * 100}-${hi * 100}%), scuffie ${bo.cap}`);
  if (kn === 15) chk("O7", bo.v >= 3.7, `15 nodi: VMG di bolina con le onde ${bo.v.toFixed(3)} (soglia 3,7)`); }
// O8
{ let ok = true, n = 0; for (const a of [150, 45]) for (const s of [1, 2, 3]){ const sh = scotta(15, a), r1 = corsa({ kn: 15, a, sh, seme: s }), r2 = corsa({ kn: 15, a, sh, seme: s }); n++;
    if (r1.firma !== r2.firma || JSON.stringify(r1.S) !== JSON.stringify(r2.S)) ok = false; }
  const div = corsa({ kn: 15, a: 150, sh: scotta(15, 150), seme: 1 }).firma !== corsa({ kn: 15, a: 150, sh: scotta(15, 150), seme: 2 }).firma;
  chk("O8", ok && n === 6 && div, `${n} coppie uguali al bit; semi diversi danno tracce diverse: ${div}`); }
const no = esiti.filter(e => !e[1]).map(e => e[0]);
console.log(`ESITO: ${esiti.length} controlli, ${esiti.length - no.length} ok, non passano: ${no.length ? [...new Set(no)].join(", ") : "nessuno"}`);
