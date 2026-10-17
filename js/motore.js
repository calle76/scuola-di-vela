// Scuola di vela, motore.js — Motore fisico: BOAT, CL, CD, step(). Puro: non tocca la pagina (lo leggono anche i collaudi della fisica, tests/fisica/motore.js).
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/PROPOSTA-DIVISIONE-CODICE.md.
// Motore fisico di una deriva singola da circa 4,2 m. Unità SI, angoli in gradi dove indicato.
const D2R = Math.PI / 180;
const norm180 = a => ((a + 180) % 360 + 360) % 360 - 180;
const norm360 = a => ((a % 360) + 360) % 360;

const BOAT = {
  mass: 135,          // kg, barca + timoniere
  length: 4.2,        // m, lunghezza fuori tutto (1.0.16: la fascia d'attesa degli avversari si misura in lunghezze di barca)
  sailArea: 7.0,      // m²
  rho: 1.225,
  hullScale: 1,       // 1.0.6: moltiplica l'area di resistenza dello scafo misurata in vasca (HULL_DA); 1 = la vasca, solo per il laboratorio
  appDA: 0.0049,      // m², attrito di deriva e timone come area di resistenza (Day 2017, fig. 11, bolina)
  rhoW: 1025,         // kg/m³, acqua di mare
  rudderDragK: 45,
  foilK: 520,         // resistenza laterale della deriva
  maxBoom: 85,
  minBoom: 9,         // 1.0.11: era 14; con α = 20° la vela porta del tutto da 29° di vento apparente (docs/PROPOSTA-BOLINA.md)
  luffA0: 22,         // gradi di vento apparente sotto cui l'inferitura comincia a sgonfiarsi (1.0.11: era 27)
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
  ironsA: 36,         // barca ferma nel vento: sotto questi gradi di vento apparente
  ironsU: 0.5,        //   e sotto questa velocità (m/s) la prua poggia da sola
  ironsYaw: 6,        //   fino a questi gradi al secondo
  backDrag: 1.5,      // 1.0.13: all'indietro lo scafo frena di più (specchio di poppa e pala al contrario); ipotesi, nessuna fonte; 1 = la vasca come in avanti
  sailCL2: 0.08,      // 1.0.11: peso di CL² nella resistenza della vela (era 0,12): CD 0,34 di bolina, galleria del vento più timoniere (Day 2017, §2.1 e §2.5)
  TE: 0.80            // m, 1.0.11: profondità efficace di scafo e deriva per la resistenza indotta (ipotesi: dà il 14% di Day 2017 §3.4 con 10 nodi); 0 = senza
};

// 1.0.24: timone del livello 2 (docs/PROPOSTA-STALLO-TIMONE.md). Vale solo per una barca con S.lv === 2 che va avanti ad almeno uMin;
// sotto, all'indietro e nel livello 1 il timone resta quello di sempre (barra fino a 30°, rotazione che insegue la barra).
// La pala sente l'angolo effettivo (barra meno l'acqua che le arriva di traverso perché la barca gira), stalla oltre stallA
// (la forza resta quella dello stallo, la resistenza continua a crescere: Masuyama e Ogihara 2020, F4) e la rotazione nasce dalla
// forza della pala contro lo smorzamento dello scafo: dr/dt = −yawG·u·(u·F + yawRho·r), a regime curvatura = δ / (xR + yawRho).
const RUD2 = {
  maxRudder: 45,      // gradi: nelle virate misurate del 470 la barra arriva a 45° (F4, fig. 5 e 6)
  xR: 1.9,            // m, distanza della pala dal centro di rotazione (stima: poppa di una barca da 4,2 m)
  yawRho: 0,          // m, smorzamento dello scafo come lunghezza: 0 = la rotazione la frena solo la pala (tarato, docs/PROPOSTA-STALLO-TIMONE.md §8)
  yawG: 0.6,          // 1/m², quanto in fretta la pala fa girare la barca (ipotesi, tarata con 10 e 14 nodi: §8)
  stallA: 22,         // gradi di angolo effettivo: F4 15° (modellino 1:5), F35 30° (calcolo a grandezza vera); fissato prima di misurare
  dragK: 184,         // N·s²/m²: resistenza della pala, 12 kgf a 15° e 6 nodi (F4, pala del 470); usa l'angolo effettivo
  uMin: 0.5           // m/s: sotto, il timone del livello 1 (come ironsU: niente sovrapposizione con la prua che poggia da sola)
};
const RUD2_LENTA = 20 / 45; // barra al secondo nel livello 2 con la sola freccia (20°/s: F4, virate accompagnate circa 14°/s, in fretta circa 35)
function rud2Alpha(S, tiller){ // angolo effettivo della pala (gradi), stesso segno della barra
  return tiller * RUD2.maxRudder + Math.atan2(S.r * D2R * RUD2.xR, S.u) / D2R;
}

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
function CD(a){ const s = Math.sin(Math.max(0, a) * D2R), cl = CL(a); return 0.06 + 1.15 * s * s + BOAT.sailCL2 * cl * cl; }

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
  const lv2 = S.lv === 2 && S.u >= RUD2.uMin, a2 = lv2 ? rud2Alpha(S, C.tiller) : 0;
  const rud = lv2 ? 0 : C.tiller * BOAT.maxRudder; // livello 2: la barra conta solo attraverso a2
  const res = hullDrag(S.u) * (S.u < 0 ? BOAT.backDrag : 1) +
              (lv2 ? RUD2.dragK * S.u * S.u * Math.sin(Math.abs(a2) * D2R) ** 2 :
              BOAT.rudderDragK * S.u * Math.abs(S.u) * Math.sin(Math.abs(rud) * D2R) ** 2);
  const heelDrag = 1 + Math.pow(Math.abs(S.heel || 0) / 30, 2) * 0.6;
  // 1.0.11: resistenza indotta, Delft (Day 2017, eq. 15) Ri = Fh² / (π·½ρ·V²·TE²), con u² + 0,4 come nello scarroccio: a bassa velocità la deriva non regge
  // la spinta laterale e la formula pura fermerebbe la barca (docs/PROPOSTA-BOLINA.md §3). TE costante: in Delft cala sbandando e cambia col Froude.
  const Ri = BOAT.TE > 0 ? side * side * S.u * Math.abs(S.u) / (Math.PI * 0.5 * BOAT.rhoW * BOAT.TE * BOAT.TE * (S.u * S.u + 0.4) ** 2) : 0;
  S.u += (drive - res * heelDrag - Ri) / BOAT.mass * dt;
  // 1.0.8: nessun tetto all'indietro (docs/PROPOSTA-RETROMARCIA.md): vela che sbatte contro la resistenza della tabella, la stessa della marcia avanti
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
  if (lv2){ // livello 2: la forza della pala (che stalla oltre stallA) contro lo smorzamento dello scafo
    const F = Math.max(-RUD2.stallA, Math.min(RUD2.stallA, a2)) * D2R;
    S.r += -RUD2.yawG * S.u * (S.u * F + RUD2.yawRho * S.r * D2R) * dt / D2R;
    S.stall = Math.abs(a2) > RUD2.stallA;
  } else {
  if (S.lv === 2) S.stall = false;
  // virata: la barra a dritta porta la pala a sinistra -> la prua gira a sinistra
  let rTarget = -(S.u / BOAT.turnLen) * Math.sin(rud * D2R) / D2R; // gradi/s
  // barca ferma nel vento: la prua poggia da sola
  if (A < BOAT.ironsA && Math.abs(S.u) < BOAT.ironsU) rTarget += (awa >= 0 ? -1 : 1) * BOAT.ironsYaw * (1 - Math.abs(S.u) / BOAT.ironsU);
  S.r += (rTarget - S.r) * Math.min(1, dt * BOAT.yawK);
  }
  S.h = norm360(S.h + S.r * dt);
  S.x += bv[0] * dt; S.y += bv[1] * dt;
  S.boomSide = awa >= 0 ? -1 : 1; // -1: boma a sinistra
  S.boom = boom;
  return { heel: S.heel, hike: S.hike, awa, aws, alpha, awFrom, drive, side, twa: norm180(E.twd - S.h), leeway: Math.atan2(S.vl, Math.max(0.3, Math.abs(S.u))) / D2R };
}
