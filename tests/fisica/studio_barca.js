// Studio della barca del gioco (docs/STUDIO-BARCA.md, 22 novembre 2026; criteri S1-S6 scritti prima). Solo misura: non cambia niente.
// Barca dell'1b (S.lv = 2), vento costante, niente numeri a caso. Parti: A polare, B virata, C abbattuta, D partenza da ferma, E frenare,
// F sbandamento e raffiche, G giri (360° e 720°), H prua al vento. Uso: node studio_barca.js [A|B|...]   (senza lettera: tutte)
const { step, norm180, BOAT, RUD2_SICURA } = require("./motore.js");
const DT = 0.01, K = 1.6, KN = 1.943844, L = BOAT.length, D2R = Math.PI / 180;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), f = (x, d = 1) => (x === null || x === undefined || !isFinite(x)) ? "—" : x.toFixed(d);
const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
const VENTI = [4, 6, 8, 10, 12, 14, 16, 18, 20];
const parti = process.argv[2] ? process.argv[2].toUpperCase() : "ABCDEFGH";
let casi = {};
const conta = (p, n = 1) => { casi[p] = (casi[p] || 0) + n; };

// barca e timoniere pulito: barra proporzionale all'errore di prua, al massimo RUD2_SICURA, a 1,6 della corsa al secondo
function barca(kn, h, u){ return { E: { twd: 0, tws: kn / KN }, S: { x: 0, y: 0, h, u, vl: 0, r: 0, lv: 2 }, info: { awa: -h }, til: 0, cap: false, t: 0 }; }
function passo(B, C){ B.info = step(B.S, C, B.E, DT); B.t += DT; if (Math.abs(B.S.heel) > BOAT.capsizeAt) B.cap = true; }
function tieni(B, h, sheet){ const e = norm180(h - B.S.h); B.til += clamp(clamp(-e / 25, -RUD2_SICURA, RUD2_SICURA) - B.til, -K * DT, K * DT);
  passo(B, { sheet: sheet === undefined ? sheetFor(B.info.awa) : sheet, tiller: B.til }); }
function barra(B, bar, sheet){ B.til += clamp(bar - B.til, -K * DT, K * DT); passo(B, { sheet: sheet === undefined ? sheetFor(B.info.awa) : sheet, tiller: B.til }); }

// ---- A. POLARE ----
const POL = {};
function equilibrio(kn, twa){ let best = null;
  for (let sh = 0; sh <= 1.0001; sh += 0.02){
    const S = { x: 0, y: 0, h: 0, u: 1, vl: 0, r: 0, lv: 2 }, E = { twd: twa, tws: kn / KN }; let info, ok = true;
    for (let t = 0; t < 60; t += 0.05){ S.h = 0; S.r = 0; info = step(S, { sheet: sh, tiller: 0 }, E, 0.05); if (Math.abs(S.heel) > BOAT.capsizeAt){ ok = false; break; } }
    if (ok && (!best || S.u > best.u)) best = { u: S.u, heel: S.heel, hike: S.hike, lee: Math.atan2(Math.abs(S.vl), S.u) / D2R, awa: Math.abs(info.awa), sh }; }
  return best; }
function parteA(){
  console.log("\n== A. POLARE (scotta migliore, prua ferma; nodi di velocità; VMG = velocità utile verso il vento o sottovento, sulla rotta vera con lo scarroccio)");
  const ANG = []; for (let a = 30; a <= 180; a += 5) ANG.push(a);
  console.log("vento | " + [30, 35, 40, 45, 50, 60, 75, 90, 110, 135, 150, 165, 180].map(a => String(a).padStart(4) + "°").join(" "));
  for (const kn of VENTI){ const R = {}; for (const a of ANG){ R[a] = equilibrio(kn, a); conta("A"); } POL[kn] = R;
    console.log(String(kn).padStart(4) + "  | " + [30, 35, 40, 45, 50, 60, 75, 90, 110, 135, 150, 165, 180].map(a => (R[a] ? (R[a].u * KN).toFixed(1) : "scuf").padStart(5)).join(" ")); }
  console.log("\nvento | bolina: VMG migliore, angolo, velocità, vento apparente, sbandamento, scarroccio, timoniere fuori | poppa: VMG migliore, angolo, velocità | massima: velocità, angolo");
  for (const kn of VENTI){ const R = POL[kn]; let up = null, dn = null, mx = null;
    for (const a of ANG){ const r = R[a]; if (!r) continue; const rot = a + (a < 90 ? r.lee : -r.lee), v = r.u * KN * Math.cos(rot * D2R);
      if (a <= 90 && (!up || v > up.v)) up = { v, a, r }; if (a >= 90 && (!dn || -v > dn.v)) dn = { v: -v, a, r }; if (!mx || r.u > mx.r.u) mx = { a, r }; }
    POL[kn].up = up; POL[kn].dn = dn;
    console.log(`${String(kn).padStart(4)}  | ${f(up.v, 2)} nodi a ${up.a}°, ${f(up.r.u * KN, 2)} nodi, apparente ${f(up.r.awa, 0)}°, sbandamento ${f(up.r.heel, 0)}°, scarroccio ${f(up.r.lee, 1)}°, fuori ${f(100 * up.r.hike, 0)}% | ${f(dn.v, 2)} nodi a ${dn.a}°, ${f(dn.r.u * KN, 2)} nodi | ${f(mx.r.u * KN, 2)} nodi a ${mx.a}°`); }
}

// ---- B e C. VIRATA E ABBATTUTA ----
// corsa: 40 s a regime sulla rotta h0, poi 60 s; la manovra parte a 5 s. Distanza utile = verso il vento (bolina) o sottovento (poppa).
function manovra(kn, twa, modo){ // modo: "dritto" | "pulito" | "tastiera" | "controllata" | "violenta" (le ultime due: regola di detectManeuvers in js/gioco.js, colpo medio 1,05)
  const B = barca(kn, -twa, 2); for (let i = 0; i < 4000; i++) tieni(B, -twa); B.cap = false; B.t = 0;
  const x0 = B.S.x, y0 = B.S.y, u0 = B.S.u, dir = twa < 90 ? 0 : 180, ux = Math.sin(dir * D2R), uy = -Math.cos(dir * D2R);
  let umin = u0, tmin = 0, fine = null, rec = null, heelMax = 0, gesto = true, lato = Math.sign(norm180(-B.S.h)), tx = null;
  const sh40 = (40 - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom); /* abbattuta «controllata»: boma a 40° (sotto i 45° della strambata violenta di gioco.js) */
  for (let i = 0; i < 6000; i++){ const t = i * DT, dopo = t >= 5;
    if (tx === null && Math.abs(norm180(-B.S.h)) > 90 && Math.sign(norm180(-B.S.h)) !== lato){ tx = t;
      if (modo === "violenta"){ B.S.u *= 0.55; B.S.heelRate += 260 * D2R * Math.pow(B.E.tws / (15 / KN), 1.6) * 1.05; } }
    if (!dopo || modo === "dritto") tieni(B, -twa, modo === "controllata" && t >= 3 ? sh40 : undefined);
    else if (modo === "pulito" || modo === "violenta") tieni(B, twa);
    else if (modo === "controllata") tieni(B, twa, tx === null || t < tx + 1 ? sh40 : undefined);
    else { if (gesto && norm180(twa > 90 ? B.S.h - 180 : B.S.h) * Math.sign(twa < 90 ? 1 : -1) > (twa < 90 ? 30 : 15)) gesto = false;
      if (gesto) barra(B, twa < 90 ? -RUD2_SICURA : RUD2_SICURA); else tieni(B, twa); }
    if (dopo && modo !== "dritto"){ const tt = t - 5; heelMax = Math.max(heelMax, Math.abs(B.S.heel));
      if (tt <= 12 && B.S.u < umin){ umin = B.S.u; tmin = tt; }
      if (fine === null && Math.abs(norm180(twa - B.S.h)) < 5) fine = tt;
      if (rec === null && tt > tmin && tt > 0.5 && B.S.u >= 0.9 * u0 && umin < 0.9 * u0) rec = tt; } }
  const d = (B.S.x - x0) * ux + (B.S.y - y0) * uy;
  return { d, u0, umin, tmin, fine, rec, heelMax, cap: B.cap }; }
function parteBC(nome, twa){
  console.log(`\n== ${nome} (da ${twa}° a ${twa}° sulle altre mure; manovra a 5 s, confronto con 60 s dritti; distanza utile ${twa < 90 ? "verso il vento" : "sottovento"})`);
  console.log("vento | timoniere: durata (prua a 5° dalla nuova rotta), minima % e dopo quanti s, ritorno al 90%, persi m / lunghezze / s, sbandamento max, scuffia");
  const out = {};
  for (const kn of VENTI){ const dr = manovra(kn, twa, "dritto"), vmg = dr.d / 60; let riga = String(kn).padStart(4) + "  | VMG " + f(vmg * KN, 2) + " nodi";
    for (const modo of (twa < 90 ? ["pulito", "tastiera"] : ["pulito", "controllata", "violenta"])){ const m = manovra(kn, twa, modo), persi = dr.d - m.d; conta(nome[0]);
      out[kn + modo] = { persi, ...m };
      riga += ` | ${modo}: ${f(m.fine)} s, minima ${f(100 * m.umin / m.u0, 0)}% a ${f(m.tmin)} s, 90% a ${f(m.rec)} s, persi ${f(persi, 1)} m = ${f(persi / L, 2)} L = ${f(persi / vmg, 1)} s, sbanda ${f(m.heelMax, 0)}°${m.cap ? ", SCUFFIA" : ""}`; }
    console.log(riga); }
  return out; }

// ---- D. PARTENZA DA FERMA ----
function parteD(){
  console.log("\n== D. PARTENZA DA FERMA (prua a 60° dal vento tenuta dal timoniere, scotta dalla regola del gioco)");
  for (const kn of [6, 10, 14]){ const B = barca(kn, -60, 0); let t50 = null, t90 = null, d10 = null; const Bv = barca(kn, -60, 2); for (let i = 0; i < 6000; i++) tieni(Bv, -60); const ureg = Bv.S.u;
    for (let i = 0; i < 6000; i++){ tieni(B, -60); const t = (i + 1) * DT; if (t50 === null && B.S.u >= 0.5 * ureg) t50 = t; if (t90 === null && B.S.u >= 0.9 * ureg) t90 = t; if (d10 === null && t >= 10) d10 = Math.hypot(B.S.x, B.S.y); }
    conta("D"); console.log(`${String(kn).padStart(4)} nodi: regime ${f(ureg * KN, 2)} nodi; 50% in ${f(t50)} s, 90% in ${f(t90)} s; in 10 s ${f(d10, 0)} m = ${f(d10 / L, 1)} lunghezze${B.cap ? "; SCUFFIA" : ""}`); }
}

// ---- E. FRENARE E STARE FERMI ----
function parteE(){
  console.log("\n== E. FRENARE (dal traverso a regime, scotta tutta lasca, prua tenuta) e STARE FERMI (velocità dopo 30 s)");
  for (const kn of [6, 10, 14]) for (const twa of [90, 60]){ const B = barca(kn, -twa, 2); for (let i = 0; i < 4000; i++) tieni(B, -twa); const u0 = B.S.u, x0 = B.S.x, y0 = B.S.y; let t1 = null, d1 = null;
    for (let i = 0; i < 3000; i++){ tieni(B, -twa, 1); const t = (i + 1) * DT; if (t1 === null && B.S.u * KN < 1){ t1 = t; d1 = Math.hypot(B.S.x - x0, B.S.y - y0); } }
    conta("E"); console.log(`${String(kn).padStart(4)} nodi, ${twa}°: da ${f(u0 * KN, 2)} nodi sotto 1 nodo in ${f(t1)} s e ${f(d1, 0)} m; dopo 30 s ${f(B.S.u * KN, 2)} nodi`); }
}

// ---- F. SBANDAMENTO E RAFFICHE ----
function parteF(){
  console.log("\n== F. SBANDAMENTO (bolina a 45°, scotta della regola) e RAFFICA IMPROVVISA senza reagire (scotta e prua ferme, 8 s)");
  for (const kn of [6, 8, 10, 12, 14, 16, 18, 20]){ const B = barca(kn, -45, 2); for (let i = 0; i < 6000; i++) tieni(B, -45);
    let rf = null;
    for (let g = 1; g <= 20 && rf === null; g++){ const C = barca(kn, -45, 2); for (let i = 0; i < 6000; i++) tieni(C, -45); const sh = sheetFor(C.info.awa); C.E.tws = (kn + g) / KN; C.cap = false;
      for (let i = 0; i < 800; i++){ C.S.h = -45; C.S.r = 0; passo(C, { sheet: sh, tiller: 0 }); } if (C.cap) rf = kn + g; }
    conta("F"); console.log(`${String(kn).padStart(4)} nodi: ${f(B.S.u * KN, 2)} nodi, sbandamento ${f(B.S.heel, 0)}°, timoniere fuori ${f(100 * B.S.hike, 0)}%${B.cap ? ", SCUFFIA a regime" : ""}; raffica che fa scuffiare: ${rf === null ? "nessuna fino a " + (kn + 20) : rf} nodi`); }
}

// ---- G. GIRI ----
function parteG(){
  console.log("\n== G. GIRI (dal traverso a regime, barra tenuta, scotta della regola): secondi per 360° e 720°, diametro del primo giro");
  for (const kn of [6, 10, 14]) for (const [nome, bar] of [["freccia 35°", RUD2_SICURA], ["Maiusc 45°", 1]]){
    const B = barca(kn, -90, 2); for (let i = 0; i < 4000; i++) tieni(B, -90); let giro = 0, hp = B.S.h, t360 = null, t720 = null; const P = [];
    for (let i = 0; i < 9000 && t720 === null; i++){ barra(B, bar); giro += Math.abs(norm180(B.S.h - hp)); hp = B.S.h; const t = (i + 1) * DT;
      if (t360 === null) P.push([B.S.x, B.S.y]); if (t360 === null && giro >= 360) t360 = t; if (t720 === null && giro >= 720) t720 = t; }
    let dia = 0; for (let i = 0; i < P.length; i += 10) for (let j = i; j < P.length; j += 10) dia = Math.max(dia, Math.hypot(P[i][0] - P[j][0], P[i][1] - P[j][1]));
    conta("G"); console.log(`${String(kn).padStart(4)} nodi, ${nome}: 360° in ${f(t360)} s, 720° in ${f(t720)} s, diametro ${f(dia, 1)} m = ${f(dia / L, 1)} lunghezze${B.cap ? ", SCUFFIA" : ""}`); }
}

// ---- H. PRUA AL VENTO ----
function parteH(){
  console.log("\n== H. PRUA AL VENTO (ferma, barra al centro, scotta a metà): quando arretra, velocità e prua dopo 20 s");
  for (const kn of [6, 10, 14]){ const B = barca(kn, 0, 0); let tb = null; for (let i = 0; i < 2000; i++){ passo(B, { sheet: 0.5, tiller: 0 }); if (tb === null && B.S.u < -0.1) tb = (i + 1) * DT; }
    conta("H"); console.log(`${String(kn).padStart(4)} nodi: arretra (oltre 0,2 nodi) dopo ${f(tb)} s; a 20 s ${f(B.S.u * KN, 2)} nodi, prua a ${f(Math.abs(norm180(B.S.h)), 0)}° dal vento`); }
}

if (parti.includes("A")) parteA();
let VIR = null, ABB = null;
if (parti.includes("B")) VIR = parteBC("B. VIRATA", 45);
if (parti.includes("C")) ABB = parteBC("C. ABBATTUTA", 150);
if (parti.includes("D")) parteD();
if (parti.includes("E")) parteE();
if (parti.includes("F")) parteF();
if (parti.includes("G")) parteG();
if (parti.includes("H")) parteH();

// ---- CRITERI ----
console.log("\n== CRITERI (docs/STUDIO-BARCA.md)");
if (VIR){ const p = [10, 12, 14].map(k => VIR[k + "pulito"].persi), t = [10, 12, 14].map(k => VIR[k + "tastiera"].persi);
  console.log(`S1 virata timoniere pulito 10/12/14 nodi: persi ${p.map(x => f(x, 1)).join(" / ")} m (soglia ≤ ${f(L, 1)} m): ${p.every(x => x <= L) ? "PASSA" : "NON PASSA"}`);
  console.log(`S2 contro 0,5 lunghezze (${f(L / 2, 1)} m) di F106: ${p.map(x => f(x / (L / 2), 1) + " volte").join(" / ")}${p.some(x => x > L) ? " (oltre il doppio)" : ""}`);
  console.log(`S3 gesto da tastiera 10/12/14 nodi: persi ${t.map(x => f(x, 1)).join(" / ")} m (segnale se > ${f(2 * L, 1)} m): ${t.some(x => x > 2 * L) ? "OLTRE" : "sotto"}`); }
if (POL[10]){ console.log(`S4 VMG di bolina 6/10/14-16 nodi: ${[6, 10, 14, 16].map(k => f(POL[k].up.v, 2)).join(" / ")} nodi (confronto con F17 fig. 8 nel documento)`);
  console.log(`S5 VMG di poppa 8/10/12/14 nodi: ${[8, 10, 12, 14].map(k => f(POL[k].dn.v, 2)).join(" / ")} nodi (F24 poppa Laser: circa 5,0 con 8-12, 6,0 con 12-15)`); }
console.log(`S6 casi per parte: ${JSON.stringify(casi)}`);
