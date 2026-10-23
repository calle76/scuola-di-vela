// Finestra T delle regole 15 e 16 (1.0.43, docs/PROPOSTA-REGOLE-PRECEDENZA-1B.md): quanto prima del contatto la barca che deve cedere
// deve saperlo per scansarsi con la barca dell'1b. Barca B (precedenza) su rotta dritta; barca A in rotta di collisione, dopo REAZIONE s
// mette la barra a fondo (RUD2_SICURA, la sola freccia) e gira di 15, 30, 45 o 90° da una parte o dall'altra (la migliore delle otto). T del caso = il minimo tempo al contatto da cui A la evita.
// Geometrie sorteggiate per seme: vento 6/10/15 nodi, incrocio a mure opposte (bolina contro bolina) o affiancamento da dietro (stesse mure).
// Uso: node finestra.js <primo seme> <ultimo seme>. Esce il 90° percentile (la regola della proposta) e la distribuzione.
const { step, norm180, BOAT, RUD2_SICURA } = require("./motore.js");
const DT = 0.01, REAZIONE = 1, D2R = Math.PI / 180, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
// contorno degli scafi: stessi punti di HULL_PTS in js/regate.js (copia; prua in y = -2,1)
const HULL = (() => { const bez = (p0, p1, p2, p3) => { const o = []; for (let i = 1; i <= 10; i++){ const t = i / 10, u = 1 - t;
  o.push([u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0], u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]]); } return o; };
  return [[0, -2.1], ...bez([0, -2.1], [0.55, -1.5], [0.72, -0.2], [0.68, 0.7]), [0.56, 2.1], [-0.56, 2.1], [-0.68, 0.7], ...bez([-0.68, 0.7], [-0.72, -0.2], [-0.55, -1.5], [0, -2.1])]; })();
const world = S => { const h = S.h * D2R, c = Math.cos(h), s = Math.sin(h); return HULL.map(([x, y]) => [S.x + x * c - y * s, S.y + x * s + y * c]); };
function tocca(A, B){ const pa = world(A), pb = world(B);
  for (const poly of [pa, pb]) for (let i = 0; i < poly.length; i++){ const [x0, y0] = poly[i], [x1, y1] = poly[(i + 1) % poly.length], l = Math.hypot(x1 - x0, y1 - y0);
    if (l < 1e-9) continue; const nx = (y1 - y0) / l, ny = -(x1 - x0) / l; let a0 = 1e9, a1 = -1e9, b0 = 1e9, b1 = -1e9;
    for (const [x, y] of pa){ const d = x * nx + y * ny; a0 = Math.min(a0, d); a1 = Math.max(a1, d); }
    for (const [x, y] of pb){ const d = x * nx + y * ny; b0 = Math.min(b0, d); b1 = Math.max(b1, d); }
    if (Math.min(a1, b1) - Math.max(a0, b0) <= 0) return false; } return true; }
// barca a regime su una prua fissa (40 s), per velocità e scarroccio realistici
function regime(h, E){ const S = { x: 0, y: 0, h, u: 1.5, vl: 0, r: 0, lv: 2 }; let info = { awa: 45 };
  for (let t = 0; t < 40; t += DT){ S.h = h; S.r = 0; info = step(S, { sheet: sheetFor(info.awa), tiller: 0 }, E, DT); } return S; }
const tieni = (S, h) => clamp(norm180(S.h - h) / 18 + S.r * 0.02, -1, 1); // guida che tiene la prua (come tillerFor in regate.js)
// A parte a tau secondi dal contatto (in linea retta); dopo REAZIONE s barra a fondo di segno sg finché la prua è girata di dh gradi,
// poi tiene la prua nuova (sg = 0: nessuna manovra). true = si toccano
function prova(c, tau, sg, dh){
  const E = c.E, A = { ...c.A }, B = { ...c.B }, ia = { awa: 45 }, ib = { awa: 45 };
  const vel = S => [Math.sin(S.h * D2R) * S.u + Math.cos(S.h * D2R) * S.vl, -Math.cos(S.h * D2R) * S.u + Math.sin(S.h * D2R) * S.vl];
  const [bx, by] = vel(B), [ax, ay] = vel(A), fx = Math.sin(B.h * D2R), fy = -Math.cos(B.h * D2R);
  const Px = bx * tau + fx * c.off, Py = by * tau + fy * c.off; // punto d'incontro: dove sarà B fra tau s, spostato di off m lungo il suo scafo
  B.x = 0; B.y = 0; A.x = Px - ax * tau; A.y = Py - ay * tau;
  let ia2 = ia, ib2 = ib, nuova = null;
  for (let t = 0; t < tau + 6; t += DT){
    if (sg && t >= REAZIONE && nuova === null && Math.abs(norm180(A.h - c.A.h)) >= dh) nuova = A.h;
    const ta = !sg || t < REAZIONE ? tieni(A, c.A.h) : nuova === null ? sg * RUD2_SICURA : tieni(A, nuova);
    ia2 = step(A, { sheet: sheetFor(ia2.awa), tiller: ta }, E, DT); ib2 = step(B, { sheet: sheetFor(ib2.awa), tiller: tieni(B, c.B.h) }, E, DT);
    if (tocca(A, B)) return true; }
  return false; }
function caso(seme){
  let s = seme * 7919 + 13; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const kn = [6, 10, 15][Math.floor(rnd() * 3)], E = { twd: 0, tws: kn / 1.944 }, tipo = rnd() < 0.5 ? "incrocio" : "affiancamento";
  const hB = 44 + rnd() * 6; // B di bolina mure a dritta (vento da nord, prua a ovest del vento: h negativa)
  const B = regime(-hB, E);
  const A = tipo === "incrocio" ? regime(44 + rnd() * 6, E)           // A mure a sinistra, di bolina
                                : regime(-(hB + 5 + rnd() * 20), E);  // A stesse mure e sopravento, 5-25° più poggiata: converge su B
  return { seme, kn, tipo, E, A, B, off: (rnd() * 2 - 1) * 1.6 }; }
function Tcaso(c){
  if (!prova(c, 6, 0)) return null; // senza manovra non si toccherebbero: geometria scartata
  const evita = tau => [1, -1].some(sg => [15, 30, 45, 90].some(dh => !prova(c, tau, sg, dh))); // la manovra migliore fra 8
  let T = null; for (let tau = 8; tau >= 0.2; tau -= 0.1){ if (!evita(tau)) { T = +(tau + 0.1).toFixed(1); break; } }
  return T === null ? 0.2 : T; }
const [a, z] = process.argv.slice(2).map(Number), out = [];
for (let k = a; k <= z; k++){ const c = caso(k), T = Tcaso(c); if (T !== null) out.push({ seme: k, kn: c.kn, tipo: c.tipo, T }); }
const ord = out.map(o => o.T).sort((p, q) => p - q), pc = q => ord[Math.min(ord.length - 1, Math.ceil(q * ord.length) - 1)];
for (const o of out) console.log(`seme ${o.seme}  ${o.kn} nodi  ${o.tipo.padEnd(13)}  T ${o.T.toFixed(1)} s`);
console.log(`casi validi ${out.length} su ${z - a + 1}; T mediana ${pc(0.5)} s, 90° percentile ${pc(0.9)} s, massimo ${ord[ord.length - 1]} s`);
for (const t of ["incrocio", "affiancamento"]){ const v = out.filter(o => o.tipo === t).map(o => o.T).sort((p, q) => p - q);
  if (v.length) console.log(`  ${t}: ${v.length} casi, mediana ${v[Math.floor(v.length / 2)]} s, 90° percentile ${v[Math.min(v.length - 1, Math.ceil(0.9 * v.length) - 1)]} s`); }
