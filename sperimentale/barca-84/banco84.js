// Voce 84: banco unico (copia del motore in memoria, js/ non cambia). Uso: node banco84.js '[{"n":"nome","P":{...}}]' [veloce]
const fs = require("fs"), path = require("path"), src0 = fs.readFileSync(path.join(__dirname, "../../js/motore.js"), "utf8");
const PRUA = !!process.env.BANCO_PRUA, KN = 1.943844, R = Math.PI / 180, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const ORC = [[0,0,.043],[7,.862,.026],[9,1.052,.023],[12,1.164,.023],[28,1.347,.033],[60,1.239,.113],[90,1.125,.383],[120,.838,.969],[150,.296,1.316],[180,-.112,1.345]];
const GZ = [[0,0],[4.5,.083],[9,.145],[13.5,.19],[18,.223],[22.5,.247],[90,0]];
const interp = (T, x, c) => { if (x <= T[0][0]) return T[0][c]; for (let i = 1; i < T.length; i++) if (x <= T[i][0]) return T[i-1][c] + (T[i][c] - T[i-1][c]) * (x - T[i-1][0]) / (T[i][0] - T[i-1][0]); return T[T.length-1][c]; };
function motore(P){ let s = src0; const rep = (a, b) => { if (!s.includes(a)) throw new Error("manca: " + a); s = s.replace(a, b); };
  if (P.vela){ rep("const L = q * CL(alpha) * lf, Dg = q * (CD(alpha) + (alpha < 6 ? 0.2 * (1 - alpha / 6) : 0));", "const [cl_, cd_] = X.vela(alpha, A, CL, CD, lf, S.flat, S.tw || 0); const L = q * cl_, Dg = q * (cd_ + (alpha < 6 ? (X.fg + (0.2 * X.k0 - X.fg) * X.tt(A)) * (1 - alpha / 6) : 0));");
    rep("CN = CL(al)", "CN = CL(al)"); }
  if (P.flat && !P.tw2) rep("const hikeTarget =", "{ const av = rmMax + X.k08 + X.forma(X.hT), m1 = Math.max(1, Math.abs(side) / Math.max(0.3, ch) * (BOAT.zCE - 1.867 * X.tw(S.flat)) / (S.flat || 1)); const fT = Math.max(X.flMin, Math.min(1, av / m1)); S.flat = (S.flat === undefined ? 1 : S.flat); S.flat += (fT - S.flat) * Math.min(1, dt / X.flK); } const hikeTarget =");
  if (P.flat && P.tw2) rep("const hikeTarget =", "{ const av = rmMax + X.k08 + X.forma(X.hT); if (S.flat === undefined) S.flat = 1; const pieno = Math.max(1, Math.abs(side) / Math.max(0.3, ch) / S.flat); const tb = fl => X.twB * (1 - fl) / (1 - X.flMin); const fT = X.twB ? Math.max(X.flMin, Math.min(1, av / (pieno * (BOAT.zCE - 1.867 * tb(S.flat))))) : Math.max(X.flMin, Math.min(1, av / (pieno * BOAT.zCE))); const tT = Math.max(fT > X.flMin + 1e-9 ? tb(fT) : X.twB, fT > X.flMin + 1e-9 ? 0 : Math.max(0, Math.min(X.tw2, (BOAT.zCE - av / (X.flMin * pieno)) / 1.867))); S.flat += (fT - S.flat) * Math.min(1, dt / X.flK); S.tw = (S.tw || 0) + (tT - (S.tw || 0)) * Math.min(1, dt / X.flK); } const hikeTarget =");
  if (P.reg) rep("(S.u * S.u + 0.4) ** 2", "(S.u * S.u + " + P.reg + ") ** 2");
  if (P.q) rep("DERIVA2 = { q: 873,", "DERIVA2 = { q: " + P.q + ",");
  if (P.lato) rep("const phi = S.heel * D2R;", "{ const l = awa >= 0 ? -1 : 1; if (S.latoV && l !== S.latoV && A < 90){ S.heel = -S.heel; S.heelRate = -S.heelRate; S.hike = -S.hike * X.restaHike; S.tCross = X.tCross; } S.latoV = l; if (S.tCross > 0) S.tCross -= dt; } const phi = S.heel * D2R;");
  if (P.lato) rep("S.hike += (hikeTarget - S.hike) * Math.min(1, dt / 0.9);", "S.hike += ((S.tCross > 0 ? Math.min(0, hikeTarget) : hikeTarget) - S.hike) * Math.min(1, dt / 0.9);");
  if (P.tw) rep("const mHeel = side * BOAT.zCE * Math.cos(phi);", "const mHeel = side * (BOAT.zCE - 1.867 * (X.tw2 ? (S.tw || 0) : X.tw(S.flat))) * Math.cos(phi);");
  if (P.appDW){ rep("const res = hullDrag(S.u)", "{ let z = Math.max(0, Math.min(1, (Math.abs(norm180(E.twd - S.h)) - X.dw[0]) / (X.dw[1] - X.dw[0]))); BOAT.appDA = X.app0 + (X.app1 - X.app0) * z; } const res = hullDrag(S.u)"); }
  if (P.gz) rep("+ BOAT.formK * Math.sin(2 * phi) / 2;", "+ X.forma(S.heel);");
  if (P.k08 !== undefined) rep("BOAT.formK * 0.08)", "X.k08)");
  const X = { k08: P.k08, twB: P.twB || 0, tw2: P.tw2 || 0, restaHike: P.restaHike === undefined ? 0 : P.restaHike, tCross: P.tCross || 0, fg: P.fg === undefined ? 0.2 : P.fg, k0: P.k0 || 1, tt: A => { const t = clamp((A - P.b1) / (P.b2 - P.b1), 0, 1); return t * t * (3 - 2 * t); }, hT: P.hT || 5, hT2: P.hT2 || 9, tw: fl => (P.tw || 0) * (1 - (fl === undefined ? 1 : fl)) / (1 - (P.flMin || 0.6)), flMin: P.flMin || 0.6, flK: P.flat, flOn: P.flOn || 0.97, app0: 0.0049, app1: P.appDW, dw: P.dw || [100, 140], S: null,
    forma: h => { const a = Math.abs(h), g = interp(P.gzTab || GZ, a, 1); return Math.sign(h) * 9.81 * (M.BOAT.mass * g - M.BOAT.sailorMass * (P.dz || 0) * Math.sin(a * R)); },
    vela: (al, A, CL, CD, lf, fl = 1, twS = 0) => { const k0 = P.k0 || 1, cl0 = CL(al) * lf * k0, cd0 = CD(al) * k0; // curve di oggi
      const r = clamp((al - P.a0) / P.w, 0, 1), be = Math.min(28, al + 9);
      const cl1 = (al <= 19 ? interp(ORC, be, 1) : CL(al) * 1.347 / 1.35) * r * fl, cd1 = (al <= 19 ? interp(ORC, be, 2) : 0.033 + (P.sep || 1.15) * (Math.sin(al * R) ** 2 - Math.sin(19 * R) ** 2)) + P.par + cl1 * cl1 * ((1 + 8 * (P.tw2 ? twS : X.tw(fl)) ** 2) / (Math.PI * P.AR) + 0.005);
      let t = clamp((A - P.b1) / (P.b2 - P.b1), 0, 1); t = t * t * (3 - 2 * t);
      let cdp = cd0; if (P.cdn){ const z = clamp((al - 60) / 30, 0, 1); cdp = cd0 + (P.cdn - CD(90) * k0) * z * z * (3 - 2 * z); }
      return [cl1 * (1 - t) + cl0 * t, cd1 * (1 - t) + cdp * t]; } };
  const M = new Function("X", s + "\nreturn { step, BOAT, RUD2, RUD2_SICURA, DERIVA2, CL, CD, norm180, norm360, hullDrag };")(X);
  Object.assign(M.BOAT, P.boat || {}); Object.assign(M.RUD2, P.rud || {}); return M; }
const DAY = { 6: 2.65, 10: 3.62, 15: 3.80 }, DWN = { 6: 2.95, 10: 4.55, 15: 6.3 };
const BI9 = [[42,4.65],[46.5,5.0],[55,5.6],[60,5.9]], BI12 = [[42,5.0],[46.5,5.4],[50,5.65],[55,6.0],[60,6.3]], PEN = [[3.28,2],[4.94,3],[6.91,4],[10.5,5]];
function misura(P, veloce){ const M = motore(P), { step, BOAT, RUD2, RUD2_SICURA, norm180 } = M, o = {};
  const eq = (kn, twa, sh) => { const S = { x:0,y:0,h:0,u:1,vl:0,r:0 }; let ul = 0; for (let i = 0; i < 1200; i++){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: twa, tws: kn / KN }, 0.05); if (Math.abs(S.heel) > 60) return null; if (i % 100 === 99){ if (i > 300 && Math.abs(S.u - ul) < 5e-4) break; ul = S.u; } } return S; };
  const best = (kn, twa, hi = 0.5) => { let b = null, bs = 0; const prova = sh => { const s = eq(kn, twa, sh); if (s && (!b || s.u > b.u)){ b = s; bs = sh; } }; const st = hi / 10; for (let sh = 0; sh <= hi + 1e-6; sh += st) prova(sh); const c = bs; for (const d of [-.5, -.25, .25, .5]) if (c + d * st >= 0) prova(c + d * st); if (b) b.sh = bs; return b || { u: 0 }; };
  // 26 nov, quinto giro (GIRO5.md §1): VMG e angoli sulla ROTTA (prua + scarroccio), come Day, Binns e i GPS; BANCO_PRUA=1 ridà il metro vecchio (solo la prua)
  const lee = st => Math.atan2(Math.abs(st.vl || 0), Math.max(.3, Math.abs(st.u))) / R, vera = st => Math.hypot(st.u, st.vl || 0);
  const vmg = (kn, a0, a1, p) => { let b = null; for (let a = a0; a <= a1; a += p){ const s = best(kn, a, a > 90 ? 1 : .5), v = PRUA ? Math.abs(s.u * Math.cos(a * R)) * KN : Math.abs(vera(s) * Math.cos((a + lee(s)) * R)) * KN; if (!b || v > b.v) b = { v, a, s }; } return b; };
  const bestR = (kn, a) => { if (PRUA) return best(kn, a); let prima = null; for (let h = a; h >= a - 10; h -= 1){ const s = best(kn, h); if (!s.u) continue; const c = { r: h + lee(s), v: vera(s), s };
      if (c.r <= a){ if (!prima) return Object.assign({}, s, { u: c.v }); const t = (a - c.r) / (prima.r - c.r); return Object.assign({}, prima.s, { u: c.v + (prima.v - c.v) * t }); } prima = c; } return { u: 0 }; };
  o.day = [6, 10, 15].map(k => { const b = vmg(k, 36, 54, 1); return [(b.v / DAY[k] - 1) * 100, b.a, b.s.heel, b.s.hike, b.s.sh]; });
  o.pen = PEN.map(([w, b]) => (bestR(w, 45).u * KN / b - 1) * 100);
  o.b9 = BI9.map(([a, m]) => (bestR(9, a).u * KN / m - 1) * 100); o.b12 = BI12.map(([a, m]) => (bestR(12, a).u * KN / m - 1) * 100);
  o.b5 = bestR(3.2, 45).u;
  o.v20 = vmg(20, 40, 52, 4).v;
  if (veloce === 2) return o;
  // B6 prua imposta a 3,2 nodi (10 s) e 11 nodi (5 s)
  const sheetFor = awa => clamp((Math.max(BOAT.minBoom, Math.abs(awa) - 17) - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
  o.sheetFor = undefined;
  const allinea = S => S.u > 0.05 ? clamp(-Math.atan2(S.r * R * 1.9, S.u) / R / 45, -1, 1) : 0;
  const ease = P.ease84 || null; o.b6 = [[3.2, 10, 0], [11, 5, 0], [11, 5, 1]].map(([kn, T, lasca]) => { const prua = t => t <= -T / 2 ? -45 : t >= T / 2 ? 45 : -45 * Math.cos(Math.PI * (t + T / 2) / T), DT = .01;
    const S = { x:0,y:0,h:-45,u:1,vl:0,r:0 }, E = { twd: 0, tws: kn / KN }; let info = { awa: 45 }, v0 = 0, prima = 0, dopo = 0, umin = 9, u0 = 1;
    for (let i = 0; i < 7500; i++){ const t = i * DT - 60, h = t < -15 ? -45 : prua(t); S.r = (prua(t + DT) - h) / DT; S.h = (h + 360) % 360; const yp = S.y; const shE = lasca && ease && t > ease[0] && t < ease[1] ? clamp((ease[2] - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1) : -1; info = step(S, { sheet: shE >= 0 ? Math.max(shE, 0) : sheetFor(info.awa), tiller: allinea(S) }, E, DT); S.h = (h + 360) % 360;
      if (t < -15){ v0 = -(S.y - yp) / DT; u0 = S.u; } else { const d = -(S.y - yp) - v0 * DT; if (t < 0) prima += d; else dopo += d; umin = Math.min(umin, S.u); } } return [prima + dopo, prima, umin / u0]; });
  if (!veloce){ o.lasco = [90, 110, 135, 180].map(a => best(12, a, 1).u * KN); o.dwn = [6, 10, 15].map(k => (vmg(k, 140, 180, 5).v / DWN[k] - 1) * 100); }
  // virata col gesto
  const vira = (kn, bar) => { const DT = .01, E = { twd: 0, tws: kn / KN }, S = { x:0,y:0,h:-45,u:1.5,vl:0,r:0 }; let info = { awa: 45 }; for (let t = 0; t < 40; t += DT){ S.h = -45; S.r = 0; info = step(S, { sheet: sheetFor(info.awa), tiller: 0 }, E, DT); }
    const u0 = S.u, h0 = S.heel; let um = u0, tf = null, til = 0, pk = 0, hm = 0; for (let t = 0; t < 20; t += DT){ const a = norm180(-S.h); if (tf === null && a < -30) tf = t; if (tf !== null) pk = Math.min(pk, a); til += clamp((tf !== null ? 0 : -bar) - til, -1.6 * DT, 1.6 * DT); info = step(S, { sheet: sheetFor(info.awa), tiller: til }, E, DT); hm = Math.max(hm, Math.abs(S.heel)); if (tf === null) um = Math.min(um, S.u); } return { t: tf, m: um / u0, pk: -pk, u0: u0 * KN, h0: Math.abs(h0), hm }; };
  o.vira = [6, 8, 10, 12, 14, 16, 18, 20].map(k => vira(k, RUD2_SICURA));
  const raff = (g, sh, lasca) => { const S = { x:0,y:0,h:0,u:1.5,vl:0,r:0 }; for (let t = 0; t < 30; t += .02){ S.h = 0; step(S, { sheet: sh, tiller: 0 }, { twd: 45, tws: 10 / 1.944 }, .02); } let m = 0; for (let t = 0; t < 6; t += .02){ S.h = 0; step(S, { sheet: lasca && t > .5 ? .5 : sh, tiller: 0 }, { twd: 45, tws: g / 1.944 }, .02); m = Math.max(m, S.heel); } return m; };
  o.raff = [16, 18, 20].map(g => [raff(g, .1), raff(g, .1, 1)]);
  // angolo morto: prua tenuta 0, 5, 10, 15 gradi da ferma, vela cazzata, velocita' max in avanti fra 25 e 30 s
  o.morto = [6, 10, 14].map(k => Math.max(...[0, 5, 10, 15].map(a => { const S = { x:0,y:0,h:0,u:0,vl:0,r:0 }; for (let t = 0; t < 30; t += .02){ S.h = 0; step(S, { sheet: 0, tiller: 0 }, { twd: a, tws: k / KN }, .02); } return S.u * KN; })));
  o.parti = [6, 10].map(k => { const S = { x:0,y:0,h:0,u:0,vl:0,r:0 }; let t2 = null; for (let t = 0; t < 30; t += .01){ S.h = 0; const inf = step(S, { sheet: .12, tiller: 0 }, { twd: 60, tws: k / KN }, .01); if (t2 === null && S.u * KN >= 2) t2 = t; } return t2; });
  o.stringe = [20, 25, 30, 35].map(a => (eq(6, a, 0) || { u: 0 }).u * KN);
  return o; }
const f = (x, d = 0) => (x >= 0 ? "+" : "") + x.toFixed(d);
function esito(o){ const e = []; const c = (n, b) => e.push(n + (b ? " si" : " NO"));
  c("B1", Math.abs(o.day[0][0]) <= 5 || o.day[0][0] >= -5 && o.day[0][0] < 5); c("B2", o.b9.every(x => Math.abs(x) <= 5)); c("B3", o.b12.every(x => Math.abs(x) <= 3)); c("B4", o.day[2][0] <= 7); c("B5", o.b5 / 1.05 - 1 >= -.08);
  if (o.b6) c("B6", o.b6[0][0] >= -1.74 * .7); if (o.lasco){ c("B7", [7.19, 4.66].every((v, i) => Math.abs(o.lasco[i ? 3 : 0] - v) <= .03) && Math.abs(o.lasco[2] - 5.62) <= .03); c("B7b", o.dwn.every(x => Math.abs(x) <= 4)); }
  if (o.vira){ const v = o.vira[5]; c("vir16", v.t !== null && v.t <= 5); c("raff18", o.raff[1][0] < 60); c("morto", o.morto.every(x => x < .3)); } return e.join("  "); }
function stampa(n, o){ console.log(`## ${n}\n  ${esito(o)}\n  Day ${o.day.map((d, i) => [6,10,15][i] + "n " + f(d[0], 1) + "% (" + d[1] + "°, sb " + (d[2]||0).toFixed(0) + "°, fuori " + Math.round(d[3] * 100) + "%)").join("  ")} | 20n ${o.v20.toFixed(2)}\n  Binns9 ${o.b9.map(x => f(x, 1)).join(" ")} | Binns12 ${o.b12.map(x => f(x, 1)).join(" ")} | F121 ${o.pen.map(x => f(x)).join(" ")} | 3,2n ${o.b5.toFixed(2)} (${f((o.b5 / 1.05 - 1) * 100, 1)}%)`);
  if (o.b6) console.log(`  virata imposta 3,2n ${o.b6[0][0].toFixed(2)} m (prima ${f(o.b6[0][1], 2)}, min ${(o.b6[0][2] * 100).toFixed(0)}%)  11n ${o.b6[1][0].toFixed(2)} (prima ${f(o.b6[1][1], 2)}; F109 -4,39) lascando: ${o.b6[2][0].toFixed(2)} (min ${(o.b6[2][2]*100).toFixed(0)}%, senza lascare ${(o.b6[1][2]*100).toFixed(0)}%; F109 51%)`);
  if (o.lasco) console.log(`  12n 90/110/135/180: ${o.lasco.map(x => x.toFixed(2)).join(" ")} | poppa Day ${o.dwn.map(x => f(x)).join(" ")}`);
  if (o.vira) console.log(`  virata freccia ${o.vira.map((v, i) => [6,8,10,12,14,16,18,20][i] + "n " + (v.t === null ? "MAI" : v.t.toFixed(1) + "s") + " " + (v.m * 100).toFixed(0) + "% (u " + v.u0.toFixed(1) + ", sb " + v.h0.toFixed(0) + "→" + v.hm.toFixed(0) + ")").join(", ")}\n  raffica 10→16/18/20 senza/lascando ${o.raff.map(r => r.map(x => x.toFixed(0)).join("/")).join("  ")} | fermo 0-15° max ${o.morto.map(x => x.toFixed(2)).join(" ")} | ferma→2 nodi a 60°, 6/10 nodi ${o.parti.map(x=>x===null?'mai':x.toFixed(1)).join('/')} s | 6n a 20/25/30/35° ${o.stringe.map(x => x.toFixed(2)).join(" ")}`); }
module.exports = { motore, misura, esito, stampa, ORC, GZ };
if (require.main === module) for (const v of JSON.parse(process.argv[2])) stampa(v.n, misura(v.P, +process.argv[3] || 0));
