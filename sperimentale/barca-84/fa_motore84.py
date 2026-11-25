# Voce 84: scrive motore84.js (candidato) partendo da js/motore.js, che resta com'e'. Uso: python3 sperimentale/barca-84/fa_motore84.py
import pathlib
q = pathlib.Path(__file__).parent; s = (q / "../../js/motore.js").read_text()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a); s = s.replace(a, b)
rep("mass: 135, ", "mass: 160, "); rep("sailArea: 7.0, ", "sailArea: 7.5, "); rep("zCE: 2.0, ", "zCE: 2.8, "); rep("sailorMass: 75, ", "sailorMass: 80, "); rep("hikeArm: 1.0, ", "hikeArm: 0.90, ")
rep("// state: {x,y,h", '''/* V84: vela di bolina da tabella ORC (Day 2017 tab. 1 e fig. 12), letta all'incidenza + 9 gradi; raddrizzata dello scafo F121 fig. 31; vela piatta e svergolata col timoniere al limite (Day 2.3-2.4) */
const V84 = { orc: [[0, 0, 0.043], [7, 0.862, 0.026], [9, 1.052, 0.023], [12, 1.164, 0.023], [28, 1.347, 0.033]], a0: 2, w: 8, par: 0.105, ki: 1 / (Math.PI * 6.1), b1: 40, b2: 60, k0: 7.0 / 7.5, fg: 0.08, cdn: 1.394,
  gz: [[0, 0], [4.5, 0.083], [9, 0.145], [13.5, 0.19], [18, 0.223], [22.5, 0.247], [90, 0]], k08: 32, flMin: 0.6, flTau: 0.9, hT: 3, tw: 0.186, zH: 1.867, app: [0.0049, 0.0026], dw: [100, 140] };
function tab84(T, x, c){ if (x <= T[0][0]) return T[0][c]; for (let i = 1; i < T.length; i++) if (x <= T[i][0]) return T[i - 1][c] + (T[i][c] - T[i - 1][c]) * (x - T[i - 1][0]) / (T[i][0] - T[i - 1][0]); return T[T.length - 1][c]; }
const liscio84 = t => { t = Math.max(0, Math.min(1, t)); return t * t * (3 - 2 * t); };
const svergola84 = fl => V84.tw * (1 - fl) / (1 - V84.flMin);
function forma84(h){ return Math.sign(h) * 9.81 * BOAT.mass * tab84(V84.gz, Math.abs(h), 1); }
function vela84(al, A, lf, fl, tw){ const V = V84, k0 = V.k0, t = liscio84((A - V.b1) / (V.b2 - V.b1)), r = Math.max(0, Math.min(1, (al - V.a0) / V.w)), be = Math.min(28, al + 9);
  const cl1 = (al <= 19 ? tab84(V.orc, be, 1) : CL(al) * 1.347 / 1.35) * r * fl;
  const cd1 = (al <= 19 ? tab84(V.orc, be, 2) : 0.033 + 1.15 * (Math.sin(al * D2R) ** 2 - Math.sin(19 * D2R) ** 2)) + V.par + cl1 * cl1 * ((1 + 8 * tw * tw) * V.ki + 0.005);
  const cd0 = CD(al) * k0 + (V.cdn - CD(90) * k0) * liscio84((al - 60) / 30), sb = al < 6 ? (V.fg + (0.2 * k0 - V.fg) * t) * (1 - al / 6) : 0;
  return [cl1 * (1 - t) + CL(al) * lf * k0 * t, cd1 * (1 - t) + cd0 * t + sb]; }

// state: {x,y,h''')
rep("const L = q * CL(alpha) * lf, Dg = q * (CD(alpha) + (alpha < 6 ? 0.2 * (1 - alpha / 6) : 0));", "if (S.flat === undefined) S.flat = 1; const [cl84, cd84] = vela84(alpha, A, lf, S.flat, S.tw84 || 0); const L = q * cl84, Dg = q * cd84;")
rep("CN = CL(al) * Math.cos(al * D2R) + CD(al) * Math.sin(al * D2R);", "CN = V84.k0 * (CL(al) * Math.cos(al * D2R) + CD(al) * Math.sin(al * D2R));")
rep("function hullDrag(u){", "function hullDrag(u, app = BOAT.appDA){"); rep("return (a * BOAT.hullScale + BOAT.appDA)", "return (a * BOAT.hullScale + app)")
rep("const res = hullDrag(S.u) *", "const app84 = V84.app[0] + (V84.app[1] - V84.app[0]) * Math.max(0, Math.min(1, (Math.abs(norm180(E.twd - S.h)) - V84.dw[0]) / (V84.dw[1] - V84.dw[0])));\n  const res = hullDrag(S.u, app84) *")
rep("const mHeel = side * BOAT.zCE * Math.cos(phi);", "const mHeel = side * (BOAT.zCE - V84.zH * (S.tw84 || 0)) * Math.cos(phi);")
rep("BOAT.formK * 0.08)", "V84.k08)"); rep("+ BOAT.formK * Math.sin(2 * phi) / 2;", "+ forma84(S.heel);")
rep("  const hikeTarget =", """  if (S.tw84 === undefined) S.tw84 = 0; /* vela piatta e svergolata col timoniere al limite (Day 2.3-2.4): insieme fino a 0,6 e 0,186, poi svergola ancora fino a 1 */
  const pieno84 = Math.max(1, Math.abs(side) / Math.max(0.3, ch) / S.flat), av84 = rmMax + V84.k08 + forma84(V84.hT), tb84 = svergola84;
  const f84 = Math.max(V84.flMin, Math.min(1, av84 / (pieno84 * (BOAT.zCE - V84.zH * tb84(S.flat)))));
  const t84 = f84 > V84.flMin + 1e-9 ? tb84(f84) : Math.max(V84.tw, Math.min(1, (BOAT.zCE - av84 / (V84.flMin * pieno84)) / V84.zH));
  const k84 = Math.min(1, dt / V84.flTau); S.flat += (f84 - S.flat) * k84; S.tw84 += (t84 - S.tw84) * k84;
  const hikeTarget =""")
rep("(S.u * S.u + 0.4) ** 2", "(S.u * S.u + 0.1) ** 2")
(q / "motore84.js").write_text(s)
