// Scuola di vela, motore.js — Motore fisico: BOAT, CL, CD, step(). Puro: non tocca la pagina (lo leggono anche i collaudi della fisica, tests/fisica/motore.js).
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/archivio/PROPOSTA-DIVISIONE-CODICE.md.
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
  minBoom: 9,         // 1.0.11: era 14; con α = 20° la vela porta del tutto da 29° di vento apparente (docs/archivio/PROPOSTA-BOLINA.md)
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

// ==== BARCA DELL'1B (nel codice lv 2; 1.0.24-1.0.46) ====
// Tutto ciò che vale solo con S.lv === 2, cioè la barca dell'1b (l'1a non ha S.lv e resta identico al bit): RUD2 (timone), RADD2 (raddrizzata), BOMA2 (spingi il boma), DERIVA2 (scarroccio), SALTI2 con
// newShift/stepShift (salti di vento), poi in step() i rami `lv2` (con la barca orziera sbandando, 1.0.46) e `push`. Fuori da qui: gioco.js (scelta «Barca», salti di vento, barra con Maiusc,
// Z per il boma), regate.js (regate con rc.lv2), disegno.js (angolo della barra nel disegno). Per trovarli: grep -nE "S\.lv|lv2|RUD2|RADD2|raddT|BOMA2|SALTI2|DERIVA2".

// 1.0.24: timone dell'1b (docs/archivio/PROPOSTA-STALLO-TIMONE.md). Vale solo per una barca con S.lv === 2 che va avanti ad almeno uMin;
// sotto, all'indietro e nell'1a il timone resta quello di sempre (barra fino a 30°, rotazione che insegue la barra).
// La pala sente l'angolo effettivo (barra meno l'acqua che le arriva di traverso perché la barca gira), stalla oltre stallA
// (la forza resta quella dello stallo, la resistenza continua a crescere: Masuyama e Ogihara 2020, F4) e la rotazione nasce dalla
// forza della pala contro lo smorzamento dello scafo: dr/dt = −yawG·u·(u·F + yawRho·r), a regime curvatura = δ / (xR + yawRho).
// 1.0.31 (docs/archivio/PROPOSTA-VIRATE-AVVERSARI.md): la pala sente anche l'acqua che le arriva di lato perché la poppa ruota, V² = u² + (r·xR)²
// al posto di u², e l'acqua frena lo scafo che ruota (−hullKq/Izz·r·|r|, anche a barca lenta). Prima la prua girava 20-45° oltre la bolina.
const RUD2 = {
  maxRudder: 45,      // gradi: nelle virate misurate del 470 la barra arriva a 45° (F4, fig. 5 e 6)
  xR: 1.9,            // m, distanza della pala dal centro di rotazione (stima: poppa di una barca da 4,2 m)
  yawRho: 0,          // m, smorzamento dello scafo come lunghezza: 0 = la rotazione la frena solo la pala (tarato, docs/archivio/PROPOSTA-STALLO-TIMONE.md §8)
  yawG: 1.5,          // 1/m², quanto in fretta la pala fa girare la barca (ipotesi, tarata con 10 e 14 nodi; 1.0.31: era 0,6, ritarata con lo smorzamento dello scafo)
  hullKq: 400,        // N·m·s², acqua contro il solo scafo che ruota: 1.0.31 600 (stima della revisione in chat; BOMA2.Kq 1230 comprende anche la pala); 1.0.43 400, scelto con i venti 10 e 14 (docs/archivio/PROPOSTA-VIRATA-1B.md)
  Izz: 200,           // kg·m², 1.0.31: inerzia d'imbardata con l'acqua trascinata da pala e deriva (stima, fissata prima di misurare; sensibilità 130-300)
  stallA: 22,         // gradi di angolo effettivo: F4 15° (modellino 1:5), F35 30° (calcolo a grandezza vera); fissato prima di misurare
  dragK: 117,         // N·s²/m²: resistenza della pala, usa l'angolo effettivo. F4: 12 kgf a 15° e 6 nodi con la pala del 470 (0,169 m², era 184); 1.0.44: scalata alla pala di una deriva singola da 4,2 m, 0,107 m² (regole di classe, docs/archivio/PROPOSTA-PALA-DERIVA-1B.md)
  uMin: 0.5           // m/s: sotto, il timone dell'1a (come ironsU: niente sovrapposizione con la prua che poggia da sola)
};
const RUD2_SICURA = 35 / 45; // 1.0.25: nell'1b la sola freccia porta la barra fino a 35° (quasi senza stallo), Maiusc + freccia fino a 45°; regola del gioco, nessuna fonte
// 1.0.32: raddrizzata dell'1b (docs/archivio/PROPOSTA-RADDRIZZATA.md): più lunga e con la barca al traverso, vela tutta lascata che sbatte,
// come negli schemi di un video di allenamento (raddrizzare con la schiena al vento, 15-20 s in tutto). 1a: 3 s e 60°, come sempre.
const RADD2 = { t: 10, tAI: 15, twa: 90 }; // secondi dal tasto A (giocatore), secondi dalla scuffia (avversari), gradi dal vento
function raddT(S){ return S.lv === 2 ? RADD2.t : 3; }
const BOOM_ISTERESI = 5; // 1.0.71: gradi da dietro (vento apparente a ±180°) entro i quali il boma tiene il lato che aveva; ipotesi nostra, nessuna fonte (docs/PROPOSTA-BOMA-IN-POPPA.md)
// 1.0.26: «spingi il boma» dell'1b (docs/archivio/PROPOSTA-SPINGI-BOMA.md). Con C.push e S.lv === 2 il boma resta a BOMA2.angle dalla parte
// dove si trovava quando si è cominciato a spingere; la vela è una piastra investita dal vento (forza normale CN = CL cos α + CD sin α)
// applicata al centro velico lungo il boma, quindi spinge indietro, di lato e fa girare la prua verso il boma. Costanti: stime senza fonte.
const BOMA2 = {
  angle: 80,          // gradi del boma spinto: le fonti dicono «circa 90°», «tutto fuori»; maxBoom è 85°
  xMast: 0.8,         // m, albero a prua del centro della barca (stima, deriva da 4,2 m)
  dCE: 0.9,           // m, centro velico lungo il boma dall'albero (stima: circa un terzo del boma)
  Kq: 1230            // N·m·s², acqua contro lo scafo che ruota: ½·ρ·1,2·(carena, pala, deriva per il cubo della distanza) (stima)
};
// 1.0.28: salti di vento dell'1b (docs/archivio/PROPOSTA-SALTI-VENTO.md §7). Puro: lo stato st lo tiene chi chiama, rnd() dà numeri fra 0 e 1.
// «osc»: oscillazione attorno al vento medio con ampiezza e periodo propri di ogni regata (fasce amp e half), ogni mezza oscillazione
// diversa di ±jit; «pers»: rotazione sempre dalla stessa parte (persRate gradi al secondo, fino a persMax) più una piccola oscillazione.
// Fasce: ipotesi dentro gli ordini di grandezza delle fonti, con il periodo accorciato per la bolina del gioco (dichiarato).
const SALTI2 = { amp: [12, 15], half: [60, 75], jit: 0.1, persRate: [10 / 200, 20 / 200], persMax: 25, persAmp: [3, 5] };
function newShift(kind, rnd){
  const a = kind === "pers" ? SALTI2.persAmp : SALTI2.amp, s0 = rnd() < 0.5 ? -1 : 1;
  const st = { kind, A: a[0] + rnd() * (a[1] - a[0]), H: SALTI2.half[0] + rnd() * (SALTI2.half[1] - SALTI2.half[0]), drift: 0, rate: 0 };
  st.v0 = s0 * st.A; st.v1 = -s0 * st.A; st.d = st.H; st.t = rnd() * st.d; // una sinusoide presa in un punto qualunque
  if (kind === "pers") st.rate = (rnd() < 0.5 ? -1 : 1) * (SALTI2.persRate[0] + rnd() * (SALTI2.persRate[1] - SALTI2.persRate[0]));
  return st;
}
function stepShift(st, dt, rnd, ruota = true){ // avanza di dt secondi; restituisce di quanti gradi il vento è girato rispetto al medio (+ = in senso orario); ruota = false: la rotazione persistente aspetta
  st.t += dt;
  if (st.t >= st.d){
    st.t -= st.d; st.v0 = st.v1; const j = () => 1 + (rnd() * 2 - 1) * SALTI2.jit;
    st.v1 = -Math.sign(st.v1 || 1) * st.A * j(); st.d = st.H * j();
  }
  if (st.kind === "pers" && ruota) st.drift = Math.max(-SALTI2.persMax, Math.min(SALTI2.persMax, st.drift + st.rate * dt));
  return st.drift + st.v0 + (st.v1 - st.v0) * (1 - Math.cos(Math.PI * Math.min(1, st.t / st.d))) / 2;
}
// 1.0.45: scarroccio dell'1b (docs/archivio/PROPOSTA-SCARROCCIO-1B.md): deriva e pala come ali, Day 2017 eq. 11-12 (F17) con le misure delle regole di
// classe (F37), barca dritta, scia della deriva sulla pala a zero: side = ½ρ·K·u·vl, K = 1,70 m² (deriva 1,176, pala 0,527 con l'acqua al 90%).
// Al posto di u si usa √(u² + u0²): u0 è ricavato perché da ferma la barca scarrocci come nell'1a (q·u0 = 0,4·foilK + 60 = 268; ipotesi).
const DERIVA2 = { q: 873, u0: 0.307 }; // q = ½·ρ·K (N·s/m²), u0 in m/s
function rud2Alpha(S, tiller){ // angolo effettivo della pala (gradi), stesso segno della barra
  return tiller * RUD2.maxRudder + Math.atan2(S.r * D2R * RUD2.xR, S.u) / D2R;
}

// 1.0.6: resistenza dello scafo dritto da una tabella misurata in vasca, al posto di k1·u + k2·u² + k4·u⁴ (docs/archivio/PROPOSTA-VELOCITA.md).
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
  let push = null; // boma spinto (1b): forza e momento della vela a collo, nel riferimento della barca (x avanti, y a dritta)
  if (C.push && S.lv === 2){
    if (!S.pushSide) S.pushSide = S.boomSide;
    const p = S.pushSide, b = BOMA2.angle * D2R, f = [-Math.cos(awa * D2R), -Math.sin(awa * D2R)]; // f: dove va l'aria
    let n = [p * Math.sin(b), Math.cos(b)]; // normale alla vela, girata dalla parte verso cui la spinge il vento
    const fn = f[0] * n[0] + f[1] * n[1]; if (fn < 0) n = [-n[0], -n[1]];
    const al = Math.asin(Math.min(1, Math.abs(fn))) / D2R, CN = CL(al) * Math.cos(al * D2R) + CD(al) * Math.sin(al * D2R);
    const Fx = q * CN * n[0], Fy = q * CN * n[1], xc = BOMA2.xMast - BOMA2.dCE * Math.cos(b), yc = p * BOMA2.dCE * Math.sin(b);
    push = { Fx, Fy, M: xc * Fy - yc * Fx }; // M > 0: la prua va a dritta
  } else if (S.pushSide) S.pushSide = 0;
  const drive = push ? push.Fx : L * Math.sin(A * D2R) - Dg * Math.cos(A * D2R);
  const side = push ? push.Fy * (awa >= 0 ? -1 : 1) : L * Math.cos(A * D2R) + Dg * Math.sin(A * D2R); // spinge sottovento (col boma spinto può essere negativa)
  const lv2 = S.lv === 2 && S.u >= RUD2.uMin && !push, a2 = lv2 ? rud2Alpha(S, C.tiller) : 0;
  const rud = lv2 ? 0 : C.tiller * BOAT.maxRudder; // 1b: la barra conta solo attraverso a2
  const res = hullDrag(S.u) * (S.u < 0 ? BOAT.backDrag : 1) +
              (lv2 ? RUD2.dragK * S.u * S.u * Math.sin(Math.abs(a2) * D2R) ** 2 :
              BOAT.rudderDragK * S.u * Math.abs(S.u) * Math.sin(Math.abs(rud) * D2R) ** 2);
  const heelDrag = 1 + Math.pow(Math.abs(S.heel || 0) / 30, 2) * 0.6;
  // 1.0.11: resistenza indotta, Delft (Day 2017, eq. 15) Ri = Fh² / (π·½ρ·V²·TE²), con u² + 0,4 come nello scarroccio: a bassa velocità la deriva non regge
  // la spinta laterale e la formula pura fermerebbe la barca (docs/archivio/PROPOSTA-BOLINA.md §3). TE costante: in Delft cala sbandando e cambia col Froude.
  const Ri = BOAT.TE > 0 ? side * side * S.u * Math.abs(S.u) / (Math.PI * 0.5 * BOAT.rhoW * BOAT.TE * BOAT.TE * (S.u * S.u + 0.4) ** 2) : 0;
  S.u += (drive - res * heelDrag - Ri) / BOAT.mass * dt;
  // 1.0.8: nessun tetto all'indietro (docs/archivio/PROPOSTA-RETROMARCIA.md): vela che sbatte contro la resistenza della tabella, la stessa della marcia avanti
  // scarroccio: la deriva resiste molto, meno a bassa velocità
  const leewardSign = awa >= 0 ? -1 : 1; // vento da dritta -> scarroccia verso sinistra
  const latTarget = leewardSign * side / (S.lv === 2 ? DERIVA2.q * Math.sqrt(S.u * S.u + DERIVA2.u0 * DERIVA2.u0) : BOAT.foilK * (S.u * S.u + 0.4) + 60);
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
  if (lv2){ // 1b: la forza della pala (che stalla oltre stallA) contro lo smorzamento dello scafo
    const F = Math.max(-RUD2.stallA, Math.min(RUD2.stallA, a2)) * D2R;
    const V2 = S.u * S.u + (S.r * D2R * RUD2.xR) ** 2;
    S.r += -RUD2.yawG * (V2 * F + S.u * RUD2.yawRho * S.r * D2R) * dt / D2R;
    // 1.0.46: barca orziera sbandando (docs/archivio/PROPOSTA-ORZIERA-1B.md): F4 eq. 6, la spinta applicata al centro velico spostato sottovento
    // di zCE·sin(sbandamento) fa girare verso il vento; nullo a barca dritta, sbandata sopravento poggia. Lo scafo che orza da solo è fuori (F4 non dà numeri).
    S.r += (awa >= 0 ? 1 : -1) * drive * BOAT.zCE * Math.sin(phi) / RUD2.Izz * dt / D2R;
    S.r /= 1 + RUD2.hullKq / RUD2.Izz * Math.abs(S.r * D2R) * dt; // forma che non inverte mai il verso della rotazione
    S.stall = Math.abs(a2) > RUD2.stallA;
  } else {
  if (S.lv === 2) S.stall = false;
  // virata: la barra a dritta porta la pala a sinistra -> la prua gira a sinistra
  let rTarget = -(S.u / BOAT.turnLen) * Math.sin(rud * D2R) / D2R; // gradi/s
  // barca ferma nel vento: la prua poggia da sola
  if (A < BOAT.ironsA && Math.abs(S.u) < BOAT.ironsU) rTarget += (awa >= 0 ? -1 : 1) * BOAT.ironsYaw * (1 - Math.abs(S.u) / BOAT.ironsU);
  if (push) rTarget += Math.sign(push.M) * Math.sqrt(Math.abs(push.M) / BOMA2.Kq) / D2R; // boma spinto: la vela fa girare la barca
  S.r += (rTarget - S.r) * Math.min(1, dt * BOAT.yawK);
  }
  S.h = norm360(S.h + S.r * dt);
  S.x += bv[0] * dt; S.y += bv[1] * dt;
  // 1.0.71 (docs/PROPOSTA-BOMA-IN-POPPA.md, osservazione 63): con il vento apparente quasi esattamente da poppa il segno di awa oscilla (onde, assetto) e il boma saltellava da un lato all'altro;
  // ora il lato cambia solo se il vento apparente è passato oltre BOOM_ISTERESI gradi da dietro. Il lato del boma non entra nelle forze (solo disegno, lato della scuffia, lato del peso dell'equipaggio).
  const latoBoma = awa >= 0 ? -1 : 1; // -1: boma a sinistra
  S.boomSide = push ? S.pushSide : (S.boomSide && latoBoma !== S.boomSide && A > 180 - BOOM_ISTERESI) ? S.boomSide : latoBoma;
  S.boom = push ? BOMA2.angle : boom;
  if (S.lv === 2) S.pushing = !!push;
  return { heel: S.heel, hike: S.hike, awa, aws, alpha, awFrom, drive, side, twa: norm180(E.twd - S.h), leeway: Math.atan2(S.vl, Math.max(0.3, Math.abs(S.u))) / D2R };
}
