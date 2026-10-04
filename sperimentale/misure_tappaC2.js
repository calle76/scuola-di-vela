// Tappa C, secondo compito: verifica della decisione di NON modellare il momento di imbardata.
// Legge la fisica da sperimentale/fiocco.html tramite motore_fiocco.js e NON la modifica:
// il momento del solo fiocco è calcolato e applicato QUI, fuori dal motore, come emulazione.
// Uso: node misure_tappaC2.js
const P = require("./motore_fiocco.js");
const KN = 1.943844, B = P.BOAT, D2R = Math.PI / 180;

// 1,1 m è un'IPOTESI usata solo per questo conto: nessuna fonte dà il braccio fra il centro velico
// del fiocco e il centro di deriva. Serve a stimare l'ordine di grandezza, non entra nel gioco.
const ARM = 1.1;

// regolazione automatica del prototipo (la stessa di autoSheet/autoJib): bugna a A - 17
const trim = A => ({
  sheet: Math.max(0, Math.min(1, (Math.max(B.minBoom, A - 17) - B.minBoom) / (B.maxBoom - B.minBoom))),
  jib:   Math.max(0, Math.min(1, (Math.max(B.minJib,  A - 17) - B.minJib)  / (B.maxJib  - B.minJib)))
});

// velocità di equilibrio a rotta inchiodata, cercando la regolazione migliore delle due scotte
function regime(twa, kn){
  let best = null;
  const prova = (sh, jb) => {
    const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0 };
    let inf;
    for (let t = 0; t < 90; t += 0.05){ S.h = 0; inf = P.step(S, { sheet: sh, tiller: 0, jib: jb }, { twd: twa, tws: kn / KN }, 0.05); }
    return Math.abs(S.heel) <= 60 ? { u: S.u, inf, heel: S.heel } : null;
  };
  const giro = (a, b, c, d, p) => {
    for (let sh = a; sh <= b + 1e-9; sh += p) for (let jb = c; jb <= d + 1e-9; jb += p){
      const r = prova(Math.max(0, Math.min(1, sh)), Math.max(0, Math.min(1, jb)));
      if (r && (!best || r.u > best.u)) best = { ...r, sheet: sh, jib: jb };
    }
  };
  giro(0, 1, 0, 1, 0.1);
  giro(best.sheet - 0.1, best.sheet + 0.1, best.jib - 0.1, best.jib + 0.1, 0.02);
  return best;
}

console.log("=== C2.B1 — IL MOMENTO DEL SOLO FIOCCO, A REGIME E A ROTTA INCHIODATA ===");
console.log("  P = forza laterale del fiocco x 1,1 m (fa POGGIARE).  O = spinta del fiocco x 1,6 m x sen(sbandamento) (fa ORZARE).");
console.log("  Il braccio di 1,1 m è un'IPOTESI, usata solo per questo conto: nessuna fonte lo dà. 1,6 m è zJibCE del prototipo.");
console.log("");
console.log("  nodi  reali   nodi barca  sband.   J.side    J.drive        P        O     P-O    verso    O/P");
let poggia = 0, tot = 0; const op10 = [];
for (const kn of [6, 10, 14]) for (const twa of [45, 70, 90, 110]){
  const r = regime(twa, kn), i = r.inf;
  const p = i.sideJ * ARM, o = i.driveJ * B.zJibCE * Math.sin(Math.abs(r.heel) * D2R), d = p - o;
  tot++; if (d > 0) poggia++;
  if (kn === 10) op10.push(o / p);
  console.log(`  ${String(kn).padStart(4)}  ${String(twa).padStart(4)}°   ${(r.u * KN).toFixed(2).padStart(8)}  ${r.heel.toFixed(1).padStart(5)}°  ${i.sideJ.toFixed(1).padStart(7)}N ${i.driveJ.toFixed(1).padStart(8)}N ${p.toFixed(1).padStart(8)} ${o.toFixed(2).padStart(8)} ${d.toFixed(1).padStart(7)}  ${(d > 0 ? "poggia" : "orza  ")}  ${(100 * o / p).toFixed(1).padStart(5)}%`);
}
console.log("");
console.log(`  casi in cui P-O fa poggiare: ${poggia} su ${tot}  (criterio: modello col solo fiocco SCARTATO se 12 su 12)`);
console.log(`  a 10 nodi, O rispetto a P: da ${(100 * Math.min(...op10)).toFixed(1)}% a ${(100 * Math.max(...op10)).toFixed(1)}%  (attesa del revisore: sotto il 15%)`);
console.log(`  esito B1: ${poggia === tot ? "SCARTATO — il solo fiocco fa sempre poggiare, mai orzare" : "non scartato da questo criterio"}`);

console.log("\n=== C2.B2 — EMULAZIONE: COSA FAREBBE LA BARCA CON QUEL MOMENTO E LA BARRA LIBERA ===");
console.log("  A ogni passo: barra = clamp(0,02 x (P-O), ±30°) nel verso che fa poggiare. Le vele si regolano da sole.");
console.log("  step() NON è toccato: la barra è imposta da qui, come farebbe un giocatore che non corregge.");
console.log("  10 nodi, barca libera di girare.");
console.log("");
console.log("  partenza   0 s    10 s    30 s    60 s   | supera 60° dal vento dopo");
const esiti = [];
for (const twa0 of [45, 70, 90]){
  const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0, heel: 0, heelRate: 0, hike: 0.2 };
  const E = { twd: twa0, tws: 10 / KN };
  // assestamento a rotta inchiodata, per partire dalla velocità di regime e non da ferma
  const t0 = trim(twa0);
  for (let t = 0; t < 40; t += 0.05){ S.h = 0; P.step(S, { sheet: t0.sheet, tiller: 0, jib: t0.jib }, E, 0.05); }
  S.h = 0;
  const dt = 1 / 240, letture = {}, ang = () => Math.abs(P.norm180(E.twd - S.h));
  let supera = null;
  letture[0] = ang();
  let inf = P.step(S, { sheet: t0.sheet, tiller: 0, jib: t0.jib }, E, 0);
  for (let k = 1; k <= 60 * 240; k++){
    const A = Math.abs(inf.awa), tr = trim(A);
    const p = inf.sideJ * ARM, o = inf.driveJ * B.zJibCE * Math.sin(Math.abs(S.heel) * D2R);
    // barra positiva = a dritta = prua a sinistra; col vento da dritta (awa>=0) è il verso che fa poggiare
    const gradi = Math.max(-30, Math.min(30, 0.02 * (p - o))) * (inf.awa >= 0 ? 1 : -1);
    inf = P.step(S, { sheet: tr.sheet, tiller: gradi / B.maxRudder, jib: tr.jib }, E, dt);
    const t = k * dt;
    if (supera === null && ang() > 60) supera = t;
    for (const s of [10, 30, 60]) if (Math.abs(t - s) < dt / 2) letture[s] = ang();
  }
  esiti.push({ twa0, supera, l: letture });
  console.log(`  ${String(twa0).padStart(5)}°   ${letture[0].toFixed(0).padStart(4)}°  ${letture[10].toFixed(0).padStart(5)}°  ${letture[30].toFixed(0).padStart(5)}°  ${letture[60].toFixed(0).padStart(5)}°   | ${supera === null ? "mai entro 60 s" : supera.toFixed(1) + " s"}`);
}
const da45 = esiti.find(e => e.twa0 === 45);
console.log("");
console.log(`  da 45°: supera i 60° dal vento ${da45.supera === null ? "mai entro 60 s" : "dopo " + da45.supera.toFixed(1) + " s"}  (criterio: SCARTATO se entro 10 s)`);
console.log(`  velocità di scarto media nei primi 10 s partendo da 45°: ${((da45.l[10] - da45.l[0]) / 10).toFixed(2)} °/s`);
console.log(`  esito B2: ${da45.supera !== null && da45.supera <= 10 ? "SCARTATO — con la barra al centro la barca scappa a poggiare" : "non scartato da questo criterio"}`);
