// Scuola di vela, motore.js — Motore fisico: BOAT, CL, CD, step(). Puro: non tocca la pagina (lo leggono anche i collaudi della fisica, tests/fisica/motore.js).
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/PROPOSTA-DIVISIONE-CODICE.md.
// Motore fisico di una deriva singola da circa 4,2 m. Unità SI, angoli in gradi dove indicato.
const D2R = Math.PI / 180;
const norm180 = a => ((a + 180) % 360 + 360) % 360 - 180;
const norm360 = a => ((a % 360) + 360) % 360;

const BOAT = {
  mass: 135,          // kg, barca + timoniere
  sailArea: 7.0,      // m²
  rho: 1.225,
  hullScale: 1,       // 1.0.6: moltiplica l'area di resistenza dello scafo misurata in vasca (HULL_DA); 1 = la vasca, solo per il laboratorio
  appDA: 0.0049,      // m², attrito di deriva e timone come area di resistenza (Day 2017, fig. 11, bolina)
  rhoW: 1025,         // kg/m³, acqua di mare
  rudderDragK: 45,
  foilK: 520,         // resistenza laterale della deriva
  maxBoom: 85,
  minBoom: 14,
  luffA0: 27,         // gradi di vento apparente sotto cui l'inferitura comincia a sgonfiarsi
  luffW: 7,           // ampiezza della transizione: sopra luffA0+luffW la vela porta del tutto
  turnLen: 1.05,       // m, lunghezza efficace per la virata
  yawK: 4,            // 1/s, quanto in fretta la rotazione segue la barra (1.0.4: era nella formula)
  maxRudder: 30,
  zCE: 2.0,           // m, altezza del centro velico
  sailorMass: 75,     // kg
  hikeArm: 1.0,       // m, braccio massimo del timoniere sporto fuori
  formK: 400,         // Nm, stabilità di forma dello scafo
  rollI: 260,         // kg·m², inerzia di rollio
  rollDamp: 520,      // smorzamento
  capsizeAt: 60,      // gradi
  backMax: 1.2,       // m/s, velocità massima all'indietro (1.0.4: era nella formula)
  ironsA: 36,         // barca ferma nel vento: sotto questi gradi di vento apparente
  ironsU: 0.5,        //   e sotto questa velocità (m/s) la prua poggia da sola
  ironsYaw: 6         //   fino a questi gradi al secondo
};

// 1.0.6: resistenza dello scafo dritto da una tabella misurata in vasca, al posto di k1·u + k2·u² + k4·u⁴ (docs/PROPOSTA-VELOCITA.md).
// Area di resistenza (resistenza / ½ρv², m²) di uno scafo da 4,2 m di circa 160 kg, senza deriva né timone, letta a occhio da
// A. H. Day, «Performance prediction for sailing dinghies», Ocean Engineering 136, 2017, fig. 2 (= Day e Nixon 2014, fig. 4, curva 80 kg).
// Sotto i 2 nodi e sopra i 9 l'area resta quella dell'estremo: lì non ci sono misure.
const HULL_DA = [[2, 0.0125], [2.5, 0.01262], [3, 0.0132], [3.5, 0.01443], [4, 0.01567], [4.5, 0.01775], [5, 0.0207], [5.5, 0.0229],
  [6, 0.02405], [6.5, 0.02455], [7, 0.02432], [7.5, 0.02325], [8, 0.02205], [8.5, 0.02122], [9, 0.0206]]; // [nodi, m²]
function hullDrag(u){ // N, con il segno di u (all'indietro si usa la stessa tabella)
  const kn = Math.abs(u) * 1.943844, T = HULL_DA;
  let a = T[kn <= T[0][0] ? 0 : T.length - 1][1];
  for (let i = 1; i < T.length; i++) if (kn > T[i - 1][0] && kn <= T[i][0]){ a = T[i - 1][1] + (T[i][1] - T[i - 1][1]) * (kn - T[i - 1][0]) / (T[i][0] - T[i - 1][0]); break; }
  return (a * BOAT.hullScale + BOAT.appDA) * 0.5 * BOAT.rhoW * u * Math.abs(u);
}

function CL(a){ // a: angolo di incidenza (gradi, >=0)
  if (a <= 0) return 0;
  if (a < 20) return 1.35 * a / 20;
  return Math.max(0.55, 1.35 - (a - 20) * 0.022);
}
function CD(a){ const s = Math.sin(Math.max(0, a) * D2R), cl = CL(a); return 0.06 + 1.15 * s * s + 0.12 * cl * cl; }

// state: {x,y,h,u,r,boomSide,boom}  controls: {sheet 0..1, tiller -1..1 (+ = barra a dritta)}  env: {twd (da), tws m/s}
function step(S, C, E, dt){
  const h = S.h * D2R;
  const fwd = [Math.sin(h), -Math.cos(h)], stbd = [Math.cos(h), Math.sin(h)];
  // vento reale (vettore verso cui soffia)
  const tdir = (E.twd + 180) * D2R, tw = [Math.sin(tdir) * E.tws, -Math.cos(tdir) * E.tws];
  // velocità barca: avanti + scarroccio
  const bv = [fwd[0] * S.u + stbd[0] * S.vl, fwd[1] * S.u + stbd[1] * S.vl];
  const aw = [tw[0] - bv[0], tw[1] - bv[1]];
  const aws = Math.hypot(aw[0], aw[1]);
  const awFrom = norm360(Math.atan2(-aw[0], aw[1]) / D2R); // direzione DA cui arriva
  const awa = norm180(awFrom - S.h);                         // + = vento da dritta
  const A = Math.abs(awa);
  // boma: limitato dalla scotta, il vento lo spinge sottovento
  const sheetMax = BOAT.minBoom + C.sheet * (BOAT.maxBoom - BOAT.minBoom); // anche cazzata a ferro la randa non sta a 0°
  const boom = Math.min(sheetMax, Math.max(0, A - 2));
  const alpha = A - boom;
  const ch = Math.cos((S.heel || 0) * D2R);
  const q = 0.5 * BOAT.rho * BOAT.sailArea * aws * aws * ch; // la vela inclinata prende meno vento
  const lf = Math.max(0, Math.min(1, (A - BOAT.luffA0) / BOAT.luffW)); // vento apparente troppo stretto: la vela si sgonfia (angolo morto)
  const L = q * CL(alpha) * lf, Dg = q * (CD(alpha) + (alpha < 6 ? 0.2 * (1 - alpha / 6) : 0)); // vela che sbatte: più resistenza
  const drive = L * Math.sin(A * D2R) - Dg * Math.cos(A * D2R);
  const side = L * Math.cos(A * D2R) + Dg * Math.sin(A * D2R); // spinge sottovento
  const rud = C.tiller * BOAT.maxRudder;
  const res = hullDrag(S.u) +
              BOAT.rudderDragK * S.u * Math.abs(S.u) * Math.sin(Math.abs(rud) * D2R) ** 2;
  const heelDrag = 1 + Math.pow(Math.abs(S.heel || 0) / 30, 2) * 0.6;
  S.u += (drive - res * heelDrag) / BOAT.mass * dt;
  S.u = Math.max(-BOAT.backMax, S.u);
  // scarroccio: la deriva resiste molto, meno a bassa velocità
  const leewardSign = awa >= 0 ? -1 : 1; // vento da dritta -> scarroccia verso sinistra
  const latTarget = leewardSign * side / (BOAT.foilK * (S.u * S.u + 0.4) + 60);
  S.vl += (Math.max(-0.8, Math.min(0.8, latTarget)) - S.vl) * Math.min(1, dt * 2);
  // sbandamento: momento sbandante della vela contro timoniere sporto fuori e forma dello scafo
  S.heel = S.heel || 0; S.heelRate = S.heelRate || 0; S.hike = S.hike === undefined ? 0.2 : S.hike;
  const phi = S.heel * D2R;
  const mHeel = side * BOAT.zCE * Math.cos(phi);
  const rmMax = BOAT.sailorMass * 9.81 * BOAT.hikeArm;
  const hikeTarget = Math.max(0, Math.min(1, (mHeel - BOAT.formK * 0.08) / rmMax)); // punta a tenere la barca quasi piatta
  S.hike += (hikeTarget - S.hike) * Math.min(1, dt / 0.9); // il timoniere reagisce con un certo ritardo
  const mRight = rmMax * S.hike * Math.cos(phi) + BOAT.formK * Math.sin(2 * phi) / 2;
  const acc = (mHeel - mRight) / BOAT.rollI - BOAT.rollDamp / BOAT.rollI * S.heelRate;
  S.heelRate += acc * dt;
  S.heel += S.heelRate / D2R * dt;
  // virata: la barra a dritta porta la pala a sinistra -> la prua gira a sinistra
  let rTarget = -(S.u / BOAT.turnLen) * Math.sin(rud * D2R) / D2R; // gradi/s
  // barca ferma nel vento: la prua poggia da sola
  if (A < BOAT.ironsA && Math.abs(S.u) < BOAT.ironsU) rTarget += (awa >= 0 ? -1 : 1) * BOAT.ironsYaw * (1 - Math.abs(S.u) / BOAT.ironsU);
  S.r += (rTarget - S.r) * Math.min(1, dt * BOAT.yawK);
  S.h = norm360(S.h + S.r * dt);
  S.x += bv[0] * dt; S.y += bv[1] * dt;
  S.boomSide = awa >= 0 ? -1 : 1; // -1: boma a sinistra
  S.boom = boom;
  return { heel: S.heel, hike: S.hike, awa, aws, alpha, awFrom, drive, side, twa: norm180(E.twd - S.h), leeway: Math.atan2(S.vl, Math.max(0.3, Math.abs(S.u))) / D2R };
}
