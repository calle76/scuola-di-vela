// Scuola di vela, regate.js — Fantasma e regate: avversari, partenza, contatti, classifica, disegno della regata.
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/PROPOSTA-DIVISIONE-CODICE.md.
  // ======================================================================
  // FANTASMA E REGATE
  // ======================================================================
  // ---- fantasma ----
  let ghosts;
  const loadGhosts = () => { try { ghosts = JSON.parse(localStorage.getItem(GHOST_STORE) || "{}"); } catch(e){ ghosts = {}; } };
  loadGhosts();
  const saveGhosts = () => { try { localStorage.setItem(GHOST_STORE, JSON.stringify(ghosts)); } catch(e){} };
  if (OLD_M.some(k => progress.best[k] || progress.clean[k] || ghosts[k])){ OLD_M.forEach(k => { delete progress.best[k]; delete progress.clean[k]; delete ghosts[k]; }); saveProgress(); saveGhosts(); wipeNote = true; } // 0.19, nessuna migrazione
  // coordinate "del vento": il vento arriva sempre da -y; così il fantasma vale con qualsiasi direzione del vento
  const toWF = (x, y) => { const th = -env.twd * D2R; return [x * Math.cos(th) - y * Math.sin(th), x * Math.sin(th) + y * Math.cos(th)]; };
  const fromWF = (x, y) => { const th = env.twd * D2R; return [x * Math.cos(th) - y * Math.sin(th), x * Math.sin(th) + y * Math.cos(th)]; };
  const rec = { key: null, samples: [], t: 0, acc: 0 };
  function recStart(key){ rec.key = key; rec.samples = []; rec.acc = 1; }
  function recSample(t, dt){
    if (!rec.key) return;
    rec.acc += dt; if (rec.acc < 0.2) return; rec.acc = 0;
    const [wx, wy] = toWF(S.x, S.y);
    rec.samples.push([+t.toFixed(2), +wx.toFixed(1), +wy.toFixed(1), Math.round(norm360(S.h - env.twd)), Math.round(S.dispBoom), Math.round(S.capsized ? 0 : S.heel)]);
    if (rec.samples.length > 6000) rec.key = null; // oltre 20 minuti non si registra
  }
  function recSave(){ if (rec.key && rec.samples.length > 5){ ghosts[rec.key] = rec.samples; saveGhosts(); } }
  function ghostAt(key, t){
    const g = ghosts[key]; if (!g || !g.length || t < g[0][0] || t > g[g.length - 1][0] + 3) return null;
    let i = 0; while (i < g.length - 2 && g[i + 1][0] < t) i++;
    const a = g[i], b = g[Math.min(i + 1, g.length - 1)], f = b[0] > a[0] ? clamp((t - a[0]) / (b[0] - a[0]), 0, 1) : 0;
    const L = (p, q) => p + (q - p) * f, La = (p, q) => p + norm180(q - p) * f;
    const [x, y] = fromWF(L(a[1], b[1]), L(a[2], b[2]));
    const boom = L(a[4], b[4]);
    return { x, y, h: norm360(La(a[3], b[3]) + env.twd), heel: L(a[5], b[5]), hike: 0.5, boomSide: sgn(boom), dispBoom: boom, boom: Math.abs(boom), capsized: false };
  }

  // ---- altre barche: disegno e scia ----
  // disegna un'altra barca riusando drawBoat (scambia per un attimo lo stato globale)
  function drawOther(bs, inf, tiller, alpha){
    const s0 = S, i0 = info, t0 = ctl.tiller, g0 = geo;
    S = bs; info = inf; ctl.tiller = tiller;
    ctx.save(); ctx.globalAlpha = alpha;
    try { drawBoat(); } finally { ctx.restore(); S = s0; info = i0; ctl.tiller = t0; geo = g0; }
  }
  function drawWakeOf(wk, u, maxAge = 6, alpha = 0.6){ // la barca del giocatore: 8 s, più marcata
    ctx.lineWidth = 0.12;
    for (const side of [-1, 1]){
      ctx.beginPath(); let started = false;
      for (let i = wk.length - 1; i >= 0; i--){
        const w = wk[i], age = simTime - w.t; if (age > maxAge) break;
        const sp = 0.35 + age * 0.35, x = w.x + w.nx * sp * side, y = w.y + w.ny * sp * side;
        started ? ctx.lineTo(x, y) : ctx.moveTo(x, y); started = true;
      }
      ctx.strokeStyle = colors.foam; ctx.globalAlpha = Math.min(1, Math.abs(u) / 2) * alpha; ctx.stroke(); ctx.globalAlpha = 1;
    }
  }

  // ---------------- regate ----------------
  const RACES = [
    { title: "Regata a bastone", desc: "Tre avversari, vento costante: partenza, bolina, poppa, arrivo.", wind: 0, tws: 10, gusts: 0 },
    { title: "Regata nelle raffiche", desc: "Tre avversari e vento rafficato: chi legge meglio l'acqua vince.", wind: 225, tws: 12, gusts: 1 }
  ];
  const LINE_HALF = 35, MARK_UP = 140;
  const FLEET_LOOK = [
    { name: "Rossa", hull: "#E9E4DF", sail: "#F6D5D0", sailor: "#C7362F" },
    { name: "Verde", hull: "#E3EAE4", sail: "#D6EEDC", sailor: "#1F8A4C" },
    { name: "Blu",   hull: "#E1E6EE", sail: "#D5E2F6", sailor: "#2B5DB8" }
  ];
  let R = null, raceIdx = 0;

  function newBoat(x, y, h){
    const twa = norm180(env.twd - h);
    const b = { x, y, h, u: 1.2, vl: 0, r: 0, boomSide: twa >= 0 ? -1 : 1, boom: 30, heel: 0, heelRate: 0, hike: 0.3,
                capsized: false, capT: 0, capSide: 1, dispBoom: 0 };
    return b;
  }
  // Posizioni di partenza casuali dietro la linea. Prima erano fisse, e il giocatore nasceva a 18 m dalla Blu
  // con le prue una contro l'altra: contatto quasi garantito, e la penalità toccava sempre a lui (mure a sinistra).
  // Vincoli: almeno START_GAP fra due barche, e nessuna coppia che si avvicini sotto START_CPA entro 25 secondi.
  const START_GAP = 20, START_CPA = 14;
  const AGGRO_OFF = 15; // metri: sotto questa distanza l'aggressiva smette di stringere (spirito della regola 16)
  function startSpots(n){
    // in coordinate del vento una barca mure a sinistra (s = 1) avanza verso +x, una mure a dritta verso -x
    const ok = (a, c) => {
      const rx = c.x - a.x, ry = c.y - a.y;
      if (Math.hypot(rx, ry) < START_GAP) return false;
      const vx = c.s - a.s, vv = vx * vx;
      if (vv < 1e-6) return true;                                   // stesse mure: non si avvicinano
      const t = -(rx * vx) / vv;
      return t <= 0 || t > 25 || Math.hypot(rx + vx * t, ry) >= START_CPA;
    };
    // Dietro la linea, ma più vicini quando la preparazione è corta: risalendo si guadagna circa 1 m al secondo verso
    // la linea, e con un minuto chi nasceva lontano partiva con una ventina di secondi di ritardo contro i cinque di
    // chi nasceva vicino (misurato su 30 partenze). Le barche si piazzano una alla volta: con la banda corta quattro
    // barche a 20 m l'una dall'altra ci stanno appena, e sorteggiare tutto l'insieme in blocco riusciva troppo di rado.
    const vicino = opt.countdown <= 60, yMin = vicino ? 26 : 38, yMax = vicino ? 54 : 74;
    const estrai = () => ({ x: -30 + Math.random() * 60, y: yMin + Math.random() * (yMax - yMin), s: Math.random() < 0.5 ? 1 : -1 });
    for (let giro = 0; giro < 40; giro++){             // se una barca non trova posto si riparte da zero
      const P = [];
      for (let k = 0; k < n; k++){
        let p = null;
        for (let tries = 0; tries < 200 && !p; tries++){ const q = estrai(); if (P.every(o => ok(o, q))) p = q; }
        if (!p) break;
        P.push(p);
      }
      if (P.length === n) return P;
    }
    // ripiego: in fila a zigzag, distanze verificate per quattro barche (consecutive 24,4 m, alterne 40 m)
    return Array.from({ length: n }, (_, k) => ({ x: -30 + k * (60 / Math.max(1, n - 1)), y: yMin + (k % 2) * Math.min(14, yMax - yMin), s: k % 2 ? 1 : -1 }));
  }
  const CHAR_TEXT = { prudente: "prudente e sta alla larga", normale: "normale", aggressiva: "aggressiva in partenza" };

  function aiParams(level){
    const r = () => Math.random();
    return level === "esperti"
      ? { up: 45 + r() * 3, down: 150 + r() * 5, trim: (r() - 0.5) * 4, gain: 18, boardMin: 35, boardMax: 90, react: 5 }
      : { up: 49 + r() * 5, down: 142 + r() * 8, trim: (r() - 0.5) * 12, gain: 26, boardMin: 25, boardMax: 60, react: 3 };
  }
  function startRace(i, wind){
    mode = "race"; raceIdx = i; showCards("race"); regReset();
    const rc = RACES[i];
    setWhere("Regata: " + rc.title);
    env.twd = wind === undefined ? rc.wind : wind; env.tws = rc.tws / KN;
    curMarks = [];
    const spots = startSpots(opt.aiLevel === "nessuno" ? 1 : 1 + FLEET_LOOK.length);
    const [px, py] = fromWF(spots[0].x, spots[0].y);
    freshState(px, py, norm360(env.twd + spots[0].s * 90), 0.35);
    setGusts(rc.gusts);
    const [pinX, pinY] = fromWF(-LINE_HALF, 0), [cbX, cbY] = fromWF(LINE_HALF, 0), [mX, mY] = fromWF(0, -MARK_UP), [cX, cY] = fromWF(0, 0);
    R = { t: -opt.countdown, phase: "pre", pin: { x: pinX, y: pinY }, cb: { x: cbX, y: cbY }, mark: { x: mX, y: mY, out: env.twd }, center: { x: cX, y: cY },
          boats: [], contacts: {}, signals: new Set(), doneAt: null };
    const me = { me: true, name: "Tu", S, ctl, info: null, wake, leg: 0, ocs: false, pen: 0, fin: null, prevWY: spots[0].y };
    R.boats.push(me);
    const slots = [-24, 2, 24].sort(() => Math.random() - 0.5);
    // una sola aggressiva, e solo con gli esperti; le altre prudenti o normali
    const aggro = opt.aiLevel === "esperti" ? Math.floor(Math.random() * FLEET_LOOK.length) : -1;
    (opt.aiLevel === "nessuno" ? [] : FLEET_LOOK).forEach((look, k) => {
      const spot = spots[k + 1];
      const [x, y] = fromWF(spot.x, spot.y);
      const bs = newBoat(x, y, norm360(env.twd + spot.s * 90));
      Object.assign(bs, { hullColor: look.hull, sailColor: look.sail, sailorColor: look.sailor });
      const b = { me: false, name: look.name, S: bs, ctl: { sheet: 0.4, tiller: 0 }, info: null, wake: [], wakeT: 0, leg: 0, ocs: false, pen: 0, fin: null,
                  prevWY: spot.y, rOff: Math.random() * 6, ai: aiParams(opt.aiLevel), side: 1, boardT: 0, boardMax: 40, startX: slots[k] + (Math.random() - 0.5) * 6,
                  char: k === aggro ? "aggressiva" : (Math.random() < 0.5 ? "prudente" : "normale") };
      b.info = step(bs, b.ctl, env, 0); bs.dispBoom = bs.boomSide * bs.boom;
      R.boats.push(b);
    });
    recStart(recK("r" + i) + "b");
    $("rTitle").textContent = rc.title;
    R.brief = "Vento da " + cardName(env.twd) + ", " + rc.tws + " nodi" + (rc.gusts ? " con raffiche" : "") +
      ". Partenza tra la barca giuria e la boa arancione, girare la boa gialla di bolina lasciandola a sinistra e tornare a tagliare la stessa linea. Allo scadere del conto alla rovescia devi essere dietro la linea: l'ideale è tagliarla lanciato proprio allo zero." +
      (opt.aiLevel === "nessuno" ? " Sei da solo: dalla seconda regata gareggi contro il fantasma del tuo record."
        : " Ogni avversario ha il suo carattere: " + R.boats.filter(b => !b.me).map(b => "la " + b.name + " è " + CHAR_TEXT[b.char]).join(", ") +
          ". Le posizioni dietro la linea cambiano a ogni partenza.") + centerNote();
    $("rDone").hidden = true;
    setControls([], true, true); setHud(3); $("hint").hidden = !opt.hint;
    showBrief(rc.title, R.brief, true);
  }

  // obiettivo attuale della barca: lo usano la freccia fuori schermo, il rilevamento del pannello e il tasto vista
  function goal(){
    if (mode === "race") return R && R.boats[0].fin === null ? targetOf(R.boats[0]) : null;
    if (mode === "mission") return S.finished ? null : curMarks[S.markIdx];
    if (mode === "lesson") return S.lessonMark && !S.markReached ? S.lessonMark : null;
    return null; // navigazione libera: nessun obiettivo
  }
  // Cambia b.rp (punto di passaggio alla boa) e la chiamano anche classifica e disegno: i cambi dipendono solo dalla posizione,
  // quindi chiamarla più volte nello stesso istante non cambia la regata (misurato nella 1.0.1: 160 regate, stessi arrivi al bit).
  function targetOf(b){
    if (b.leg === 0 || b.ocs){
      if (b.ocs){ const [x, y] = fromWF(0, 20); return { x, y, kind: "line" }; }
      if (!b.me && R.t >= 0){ // dopo il segnale: un punto oltre la linea, davanti alla barca
        const bx = toWF(b.S.x, b.S.y)[0], [x, y] = fromWF(clamp(bx * 0.6, -LINE_HALF + 8, LINE_HALF - 8), -25); return { x, y, kind: "line" };
      }
      const [x, y] = fromWF(b.me ? 0 : b.startX, 0); return { x, y, kind: "line" };
    }
    if (b.leg === 1){
      if (b.me) return { ...R.mark, kind: "mark" };
      // avversari: tre punti di passaggio per lasciare la boa a sinistra (coordinate del vento, boa in (0, -MARK_UP))
      // 0: poco sotto e a destra della boa; 1: oltre la boa, verso sinistra (qui si attraversa la semiretta e la boa è girata);
      // 2: solo se la boa è stata girata male o mancata: si torna sotto e a sinistra, per riprovare dal punto 0 passando sotto la boa
      const [wx, wy] = toWF(b.S.x, b.S.y), o = b.rOff, P = [[9 + o, -MARK_UP - 3], [-16 - o, -MARK_UP - 10 - o * 0.5], [-10, -MARK_UP + 14]];
      const near = (k, r) => Math.hypot(wx - P[k][0], wy - P[k][1]) < r;
      // il punto 1 si punta solo da sopra la boa: da più in basso la bolina porterebbe la barca proprio sopra la boa
      if (!b.rp && (near(0, 4) || (wy < -MARK_UP - 2 && wx > 3))) b.rp = 1;
      else if (b.rp === 1 && ((wx < -8 && (b.rnd || 0) < 0) || near(1, 8))) b.rp = 2; // girata male, o passata sotto la boa: si riprova
      else if (b.rp === 2 && near(2, 8)) b.rp = 0;
      const [x, y] = fromWF(P[b.rp || 0][0], P[b.rp || 0][1]); return { x, y, kind: "mark" };
    }
    if (!b.me){ const [x, y] = fromWF(b.startX * 0.8, 0); return { x, y, kind: "finish" }; }
    return { ...R.center, kind: "finish" };
  }

  // ---- guida degli avversari ----
  function aiControl(b, dt){
    const s = b.S, w = windAt(s.x, s.y), twd = w.twd, twa = norm180(twd - s.h), side = sgn(twa), A = Math.abs(twa);
    const ai = b.ai;
    let desired, hold = false;
    const tgt = targetOf(b);
    let dest = tgt;
    // 0.21.4: dopo l'arrivo si va nella zona di sosta, fuori dalla linea (25 m oltre l'estremità dal proprio lato, 30 m dietro la linea),
    // e lì si resta quasi fermi con la vela che sbatte, come prima del via: prima l'avversario arrivato girava attorno al punto d'arrivo
    if (b.fin !== null){
      const [px, py] = fromWF((b.startX < 0 ? -1 : 1) * (LINE_HALF + 25), 30); dest = { x: px, y: py };
      if (Math.hypot(s.x - px, s.y - py) < 12) hold = true;
    }
    // prima della partenza: blocco a sé, senza la logica di bolina generale
    let pre = false;
    if (R.t < 0 && b.leg === 0){
      pre = true;
      const [bx, by] = toWF(s.x, s.y);
      // l'aggressiva attende dall'altro lato, così arriva alla linea mure a dritta: con la precedenza in mano
      const [hx, hy] = fromWF(b.startX + (b.char === "aggressiva" ? 55 : -55), 18), [lx, ly] = fromWF(b.startX, -10);
      const go = -R.t <= Math.hypot(s.x - lx, s.y - ly) / 1.9 + 5;
      const aim = p => { let d = bearingTo(s, p); const r = norm180(d - twd); if (Math.abs(r) < ai.up + 4) d = twd + (r >= 0 ? 1 : -1) * (ai.up + 4); return d; };
      if (go) b.preDesired = aim({ x: lx, y: ly });
      else if (Math.hypot(s.x - hx, s.y - hy) > 15) b.preDesired = aim({ x: hx, y: hy });
      else hold = true;
      if (by < 7 && Math.abs(bx) <= LINE_HALF + 5 && R.t < -1) hold = true; // davanti alla linea: non superarla prima dello zero. 7 m e non 4: con le posizioni casuali e la prudente che evita da 22 m, qualcuna scivolava oltre la linea prima del via
    }
    const brg = bearingTo(s, dest);
    const rel = norm180(brg - twd);
    b.boardT += dt;
    if (hold){ desired = twd + 62; } // in attesa: quasi di bolina con la vela che sbatte, la barca resta quasi ferma
    else if (pre){ desired = b.preDesired; }
    else if (Math.abs(rel) < ai.up){ // bolina: bordi alternati
      const near = Math.hypot(dest.x - s.x, dest.y - s.y) < 30;
      if (near){ // vicino al bersaglio: il bordo che punta più vicino
        const best = Math.abs(norm180(twd - ai.up - brg)) < Math.abs(norm180(twd + ai.up - brg)) ? 1 : -1;
        if (best !== b.side && b.boardT > 8){ b.side = best; b.boardT = 0; } // isteresi: niente virate a raffica
      } else if (b.boardT > b.boardMax){ b.side = -b.side; b.boardT = 0; b.boardMax = ai.boardMin + Math.random() * (ai.boardMax - ai.boardMin); }
      desired = twd - b.side * ai.up;
    } else if (Math.abs(rel) > 180 - (180 - ai.down)){ // bersaglio in poppa piena: lasco con abbattute
      if (b.boardT > b.boardMax){ b.side = -b.side; b.boardT = 0; b.boardMax = ai.boardMin + Math.random() * (ai.boardMax - ai.boardMin); }
      desired = twd - b.side * ai.down;
    } else {
      desired = brg; b.side = sgn(norm180(twd - brg)); b.boardT = Math.min(b.boardT, b.boardMax * 0.5);
      // bersaglio a proravia del traverso ma sull'altra mura: virare direttamente da un'andatura larga non riesce (manca l'abbrivio).
      // Come un timoniere: prima orza fino alla bolina, poi vira, poi poggia verso il bersaglio.
      const newSide = sgn(norm180(twd - brg));
      if (newSide !== side && Math.abs(rel) < 90) desired = A > ai.up + 12 ? twd - side * ai.up : twd - newSide * ai.up;
    }
    // mure a sinistra: lascia strada a chi è mure a dritta, passandogli di poppa
    if (side < 0 && !hold){
      for (const o of R.boats){
        if (o === b || o.S.capsized) continue;
        const d = Math.hypot(o.S.x - s.x, o.S.y - s.y); if (d > 30) continue;
        const oTwa = norm180(local.twd - o.S.h); if (oTwa < 0) continue;
        const ang = Math.abs(norm180(bearingTo(s, o.S) - s.h)); if (ang > 70) continue;
        desired -= side * 28; break;
      }
    }
    // carattere aggressivo: prima del via punta le barche mure a sinistra che ha vicine, per costringerle a manovrare.
    // Spirito delle regole 14 e 16: sotto AGGRO_OFF smette di stringere, così una manovra per evitarla esiste sempre,
    // e sotto il raggio del blocco qui sotto cerca comunque di non urtare. La colpa resta decisa solo da mure e sopravento.
    if (b.char === "aggressiva" && pre && !hold && side > 0){
      let prey = null, best = 1e9;
      for (const o of R.boats){
        if (o === b || o.S.capsized || o.fin !== null) continue;
        if (norm180(twd - o.S.h) >= 0) continue;                           // solo chi è mure a sinistra
        const d = Math.hypot(o.S.x - s.x, o.S.y - s.y);
        if (d < AGGRO_OFF || d > 40 || d >= best) continue;
        best = d; prey = o;
      }
      if (prey) desired = bearingTo(s, prey.S);
    }
    // evita qualsiasi barca vicina davanti (anche quando avrebbe diritto di rotta: meglio non urtare)
    // la prudente comincia da più lontano: è il suo carattere
    const avoidR = b.char === "prudente" ? 22 : 14;
    for (const o of R.boats){
      if (o === b || o.fin !== null) continue;
      const d = Math.hypot(o.S.x - s.x, o.S.y - s.y); if (d > avoidR) continue;
      const relB = norm180(bearingTo(s, o.S) - s.h); if (Math.abs(relB) > 60) continue;
      desired -= (relB >= 0 ? 1 : -1) * 35 * (1 - d / avoidR + 0.3); break;
    }
    // la prua desiderata non deve mai finire nell'angolo morto (tranne durante una virata voluta)
    const dTwa = norm180(twd - desired);
    const wantsTack = !hold && Math.abs(rel) < ai.up && sgn(dTwa) !== side;
    if (!wantsTack && Math.abs(dTwa) < ai.up - 2) desired = twd - (sgn(dTwa) || side) * (ai.up - 2);
    // se per arrivare alla rotta voluta bisogna attraversare il vento e manca velocità: prima poggia e prendi abbrivio
    const turn = norm180(desired - s.h), toWind = norm180(twd - s.h);
    // (vale solo prima di iniziare: a virata in corso la velocità cala per forza, e non va interrotta)
    // 0.21.3: stessa soglia della regola «piantata» qui sotto (era 44° fisso): in partenza, fra 40° e 44°, nessuna delle due agiva e una barca
    // lenta che voleva virare oscillava per minuti attorno a 40° senza partire (collaudo_regate.py, regata nelle raffiche, seme 17)
    const ironsA = b.leg === 0 && !b.ocs ? 40 : 44;
    if (sgn(turn) === sgn(toWind) && Math.abs(toWind) < Math.abs(turn) && Math.abs(toWind) >= ironsA && s.u < 1.1) desired = twd - side * 95;
    // piantata nell'angolo morto: poggia e lascia sbattere la vela finché riparte
    const irons = A < ironsA && s.u < 0.6; // 44°: tra 40° e 44° una barca ferma restava sospesa senza ripartire; in partenza resta 40° (con 44° poggia troppo presto vicino alla linea), salvo chi torna dietro la linea dopo una partenza anticipata
    if (irons) desired = twd - side * 80;
    const err = norm180(s.h - desired);
    const tTarget = clamp(err / ai.gain + s.r * 0.02, -1, 1) * (s.u < 0 ? -1 : 1);
    b.ctl.tiller += (tTarget - b.ctl.tiller) * Math.min(1, dt * ai.react);
    // scotta: regolata sul vento apparente, con l'errore tipico di questo avversario
    const aw = Math.abs(b.info ? b.info.awa : 60);
    let boomT = Math.max(BOAT.minBoom, aw - 17 + ai.trim);
    let sheet = clamp((boomT - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
    if (hold || irons) sheet = 1;
    if (A > 158) sheet = Math.min(sheet, 0.42); // abbattuta controllata
    if (s.heel > 22) sheet = Math.min(1, sheet + 0.2);
    b.ctl.sheet += (sheet - b.ctl.sheet) * Math.min(1, dt * 3);
  }

  function stepAI(b, dt){
    const s = b.S;
    if (s.capsized){
      s.capT += dt; s.u = 0;
      if (s.capT > 5){ s.capsized = false; s.capT = 0; s.heel = 0; s.heelRate = 0; s.h = norm360(env.twd + s.capSide * 60); b.ctl.sheet = 0.8; }
      return;
    }
    aiControl(b, dt);
    const w = windAt(s.x, s.y);
    for (let i = 0; i < 3; i++) b.info = step(s, b.ctl, w, dt / 3);
    if (s.heel > BOAT.capsizeAt || s.heel < -45){ s.capsized = true; s.capSide = s.heel > 0 ? s.boomSide : -s.boomSide; s.heel = 0; s.u = 0; }
    s.dispBoom += (s.boomSide * s.boom - s.dispBoom) * Math.min(1, dt * 6);
    b.wakeT += dt;
    if (b.wakeT > 0.1){ b.wakeT = 0; const h = s.h * D2R; b.wake.push({ x: s.x - Math.sin(h) * 2.1, y: s.y + Math.cos(h) * 2.1, nx: Math.cos(h), ny: Math.sin(h), t: simTime }); if (b.wake.length > 70) b.wake.shift(); }
  }

  // ---- svolgimento: lati, contatti, arrivo, classifica ----
  function raceLegs(b){
    const s = b.S, [wx, wy] = toWF(s.x, s.y), prev = b.prevWY; b.prevWY = wy;
    const onLine = Math.abs(wx) <= LINE_HALF;
    if (b.fin !== null) return;
    if (b.leg === 0){
      if (R.t >= 0){
        if (b.ocs){ if (wy > 0){ b.ocs = false; if (b.me) toast("Sei tornato dietro la linea: ora riparti"); } }
        else if (prev > 0 && wy <= 0 && onLine){ b.leg = 1; if (b.me) toast("Partito! Ora la boa di bolina"); }
        else if (prev > 0 && wy <= 0 && !onLine){ b.ocs = true; if (b.me) regAdd("outLine"); if (b.me) toast("Sei passato fuori dalla linea: torna dietro e passa tra giuria e boa"); }
        else if (wy < -5 && !b.ocs){ b.ocs = true; if (b.me) regAdd("outLine"); } // oltre la linea senza averla tagliata: deve tornare indietro
      }
    } else if (b.leg === 1){
      const k = roundCheck(b, s.x, s.y, R.mark);
      if (k < 0){ b.wrongMarks = (b.wrongMarks || 0) + 1; if (b.me) regAdd("wrongMarks"); }
      if (b.rnd >= 1){ b.leg = 2; if (b.me) toast("Boa girata: ora all'arrivo"); }
      else if (k < 0 && b.me) roundToast(-1);
      else if (k > 0 && b.me) toast("Hai rimediato: ora girala lasciandola a sinistra");
    } else if (b.leg === 2){
      if (prev < 0 && wy >= 0 && onLine){ b.fin = R.t + b.pen; if (b.me) toast("Arrivato!"); }
    }
  }

  function contacts(){
    const bs = R.boats;
    for (let i = 0; i < bs.length; i++) for (let j = i + 1; j < bs.length; j++){
      const A = bs[i], B = bs[j], key = i + "-" + j;
      if (A.fin !== null || B.fin !== null || A.S.capsized || B.S.capsized) continue;
      const d = Math.hypot(A.S.x - B.S.x, A.S.y - B.S.y);
      if (R.contacts[key]){ if (d > 8) delete R.contacts[key]; continue; } // stesso contatto finché non si separano
      if (d > 4.2) continue;
      R.contacts[key] = simTime;
      const tA = sgn(norm180(local.twd - A.S.h)), tB = sgn(norm180(local.twd - B.S.h));
      let guilty, why;
      if (tA !== tB) guilty = tA < 0 ? A : B;
      else { const ya = toWF(A.S.x, A.S.y)[1], yb = toWF(B.S.x, B.S.y)[1]; guilty = ya < yb ? A : B; }
      const v = (tu, lui) => guilty.me ? tu : lui; // 0.21.2: «tu eri… dovevi» al giocatore, terza persona per l'avversario
      why = tA !== tB ? v("eri", "era") + " mure a sinistra e " + v("dovevi", "doveva") + " lasciare strada a chi era mure a dritta"
                      : v("eri", "era") + " sopravento con le stesse mure e " + v("dovevi", "doveva") + " stare lontano";
      guilty.pen += 15;
      for (const o of [A, B]){ o.S.u *= 0.6; }
      const dx = (A.S.x - B.S.x) / (d || 1), dy = (A.S.y - B.S.y) / (d || 1);
      const push = (4.6 - d) / 2 + 0.3;
      A.S.x += dx * push; A.S.y += dy * push; B.S.x -= dx * push; B.S.y -= dy * push;
      if (A.me || B.me){
        regAdd("contacts"); if (guilty.me) regAdd("contactsPen");
        const other = A.me ? B : A;
        toast(guilty.me ? "Contatto! Penalità +15 s" : "Contatto: penalità a " + other.name);
        R.lastRule = (guilty.me ? "Contatto con " + other.name + ": tu " : "Contatto: " + guilty.name + " ") + why + ". Penalità di 15 secondi.";
      }
    }
  }

  function updateRace(dt){
    if (!R) return;
    const prevT = R.t; R.t += dt;
    // segnali di partenza (versione accorciata a un minuto)
    const sig = (at, text) => { if (prevT < at && R.t >= at && !R.signals.has(at)){ R.signals.add(at); toast(text); } };
    sig(-opt.countdown, "Segnale di avviso: partenza tra " + Math.round(opt.countdown / 60) + (opt.countdown >= 120 ? " minuti" : " minuto"));
    if (opt.countdown > 60) sig(-60, "Un minuto"); sig(-30, "30 secondi"); sig(-10, "10 secondi");
    if (prevT < 0 && R.t >= 0){
      R.phase = "race";
      for (const b of R.boats){ const wy = toWF(b.S.x, b.S.y)[1]; if (wy <= 0) b.ocs = true; }
      if (R.boats[0].ocs) regAdd("ocs");
      // 0.21.5: richiamo individuale anche per gli avversari (regola 29.1 del regolamento di regata: chi è oltre la linea allo sparo
      // deve tornare dietro e ripartire, e il ritorno è la penalità). Prima il messaggio parlava solo del giocatore
      const ant = R.boats.filter(b => !b.me && b.ocs).map(b => b.name), chi = ant.length > 1 ? ant.slice(0, -1).join(", ") + " e " + ant[ant.length - 1] : ant[0];
      if (R.boats[0].ocs) toast("Partenza anticipata! Torna dietro la linea" + (ant.length ? " (anche " + chi + ")" : ""), ant.length ? 4.5 : 2.6);
      else toast(ant.length ? "Partenza! Richiamo individuale: " + chi + (ant.length > 1 ? " devono" : " deve") + " tornare dietro la linea" : "Partenza!", ant.length ? 4.5 : 2.6);
    }
    for (const b of R.boats){ if (!b.me) stepAI(b, dt); raceLegs(b); }
    contacts();
    recSample(R.t, dt);
    const me = R.boats[0];
    if (me.fin !== null && R.phase !== "done"){
      R.phase = "done"; R.doneAt = R.t;
      const key = "r" + raceIdx, bk = recK(key), prev = progress.best[bk], tot = Math.round(me.fin);
      if (!prev || tot < prev){ progress.best[bk] = tot; recSave(); }
      progress.done[key] = true; if (regTotal() === 0) progress.clean[bk] = true; saveProgress();
      raceResults(prev, tot);
      // 0.21: piazzamento per livello degli avversari (solo con avversari); «pulita» si legge adesso, all'arrivo
      if (opt.aiLevel !== "nessuno") R.pend = { key: bk + ":" + opt.aiLevel, pulita: regTotal() === 0 };
    }
    // il piazzamento si salva quando è definitivo: chi taglia la linea da qui in poi ha fin = R.t + pen >= il mio.
    // Se il giocatore lascia la regata prima (menu, nuova regata, ricomincia), il dato si perde.
    if (R.pend && (R.boats.every(b => b.fin !== null) || R.t >= me.fin)){
      const v = { pos: ranking().indexOf(me) + 1, n: R.boats.length, pulita: R.pend.pulita };
      const pts = r => 5 - r.pos + (r.pulita ? 1 : 0); // 4/3/2/1 più 1 senza errori; ponytail: vale per 4 barche, da rivedere se la flotta cambia
      progress.race = progress.race || {};
      const old = progress.race[R.pend.key];
      if (!old || pts(v) > pts(old)){ progress.race[R.pend.key] = v; saveProgress(); }
      R.pend = null;
    }
  }
  function ranking(){
    const score = b => b.fin !== null ? 1e7 - b.fin : (b.ocs ? -1e6 : b.leg * 1e4 - Math.hypot(b.S.x - targetOf(b).x, b.S.y - targetOf(b).y));
    return [...R.boats].sort((a, b) => score(b) - score(a));
  }
  function raceResults(prev, tot){
    const rank = ranking(), pos = rank.indexOf(R.boats[0]) + 1;
    $("rDone").hidden = false;
    $("rDoneText").textContent = pos + "° su " + rank.length + " in " + fmtTime(tot) +
      (R.boats[0].pen ? " (penalità comprese: " + R.boats[0].pen + " s)" : "") + "." + (!prev ? "" : tot < prev ? " Nuovo record!" : " Record: " + fmtTime(prev) + ".") +
      (regTotal() === 0 ? (reg.contacts ? " " + regText() + ". ★ senza errori." : " Nessun errore: ★ senza errori.") : " " + regText() + ".");
  }
  function legName(b){
    if (b.fin !== null) return "arrivata · " + fmtTime(Math.round(b.fin));
    if (b.S.capsized) return "scuffiata!";
    if (b.ocs) return "partenza anticipata";
    if (b.leg === 1 && b.rnd < 0) return "boa girata dal lato sbagliato";
    return ["prima della partenza", "di bolina", "in poppa verso l'arrivo"][b.leg];
  }
  function racePanel(){
    if (!R) return;
    const rank = ranking();
    $("standings").innerHTML = rank.map(b => `<li class="${b.me ? "me" : ""}"><b>${b.name}</b> <span>${legName(b)}${b.pen ? " · +" + b.pen + " s" : ""}</span></li>`).join("");
    $("rRule").hidden = !R.lastRule; $("rRule").textContent = R.lastRule || "";
  }

  // ---- disegno della regata e aiuti a schermo ----
  function drawRaceWorld(v){
    if (!R) return;
    // linea di partenza (tratteggio) e, dopo il via, d'arrivo (scacchi)
    if (R.t < 0){
      ctx.strokeStyle = "rgba(255,255,255,.55)"; ctx.lineWidth = 0.18; ctx.setLineDash([1.2, 1.2]);
      ctx.beginPath(); ctx.moveTo(R.pin.x, R.pin.y); ctx.lineTo(R.cb.x, R.cb.y); ctx.stroke(); ctx.setLineDash([]);
    } else drawChecker(R.pin, R.cb, v.ppm, 1);
    // boa di partenza (arancione) e barca giuria
    ctx.fillStyle = "#F28C1B"; ctx.beginPath(); ctx.arc(R.pin.x, R.pin.y, Math.max(0.8, 3 / v.ppm), 0, Math.PI * 2); ctx.fill();
    ctx.save(); ctx.translate(R.cb.x, R.cb.y); ctx.rotate(env.twd * D2R);
    ctx.fillStyle = "#DADFE2"; ctx.strokeStyle = "#5E6A72"; ctx.lineWidth = 0.08;
    ctx.beginPath(); ctx.moveTo(0, -4); ctx.lineTo(1.6, -1.5); ctx.lineTo(1.5, 4); ctx.lineTo(-1.5, 4); ctx.lineTo(-1.6, -1.5); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#9AA7B0"; ctx.fillRect(-1, -0.5, 2, 2.4);
    ctx.fillStyle = R.t < 0 ? "#F2C14E" : "#2B5DB8"; ctx.fillRect(0.2, -3.2, 1.2, 0.8);
    ctx.restore();
    // boa di bolina
    ctx.fillStyle = "#F2D43C"; ctx.beginPath(); ctx.arc(R.mark.x, R.mark.y, Math.max(0.9, 3 / v.ppm), 0, Math.PI * 2); ctx.fill();
    drawRoundArrow(R.mark, 7, "rgba(255,226,122,.9)");
    // avversari
    for (const b of R.boats){ if (b.me) continue; drawWakeOf(b.wake, b.S.u); drawOther(b.S, b.info, b.ctl.tiller, 1); }
  }
  function drawRaceScreen(v){
    if (!R) return;
    ctx.save(); ctx.font = font(700, 13); ctx.textAlign = "center"; ctx.textBaseline = "middle";
    for (const b of R.boats){ if (b.me) continue; const [sx, sy] = toScreen(v, b.S.x, b.S.y); ctx.fillStyle = "rgba(10,24,36,.6)"; const w = ctx.measureText(b.name).width + 10; ctx.fillRect(sx - w / 2, sy - 58, w, 18); ctx.fillStyle = b.S.sailorColor; ctx.fillText(b.name, sx, sy - 49); }
    const [gx, gy] = toScreen(v, R.mark.x, R.mark.y); ctx.fillStyle = "#fff"; ctx.textAlign = "left"; ctx.fillText("Boa di bolina · lasciala a sinistra", gx + 10, gy - 10);
    // orologio e posizione
    const me = R.boats[0], rank = ranking(), pos = rank.indexOf(me) + 1;
    let big, small = "";
    if (R.t < 0){
      big = "Partenza tra " + fmtClock(Math.ceil(-R.t));
      const [wx, wy] = toWF(S.x, S.y), dLine = Math.max(0, wy);
      const h = (S.h - env.twd) * D2R, vUp = S.u * Math.cos(h); // velocità verso la linea (verso il vento)
      const tLine = vUp > 0.2 ? Math.round(dLine / vUp) : null;
      small = "Alla linea: " + Math.round(dLine) + " m" + (tLine !== null ? " · " + tLine + " s alla velocità attuale" : "") + (Math.abs(wx) > LINE_HALF ? " (fuori dagli estremi)" : "");
    }
    else { big = fmtClock(me.fin !== null ? me.fin : R.t); small = pos + "° su " + rank.length; }
    ctx.textAlign = "center"; ctx.font = font(700, 26);
    const w = Math.max(ctx.measureText(big).width, 90) + 30;
    ctx.font = font(600, 15); const w2 = small ? ctx.measureText(small).width + 30 : 0; ctx.font = font(700, 26);
    const bw = Math.max(w, w2);
    ctx.fillStyle = me.ocs ? "rgba(160,40,30,.85)" : "rgba(10,24,36,.7)"; ctx.fillRect(W / 2 - bw / 2, 10, bw, small ? 58 : 40);
    ctx.fillStyle = "#fff"; ctx.fillText(big, W / 2, 30);
    if (small){ ctx.font = font(600, 15); ctx.fillText(small, W / 2, 55); }
    if (R.t > -10 && R.t < 0){ ctx.font = font(700, 64); ctx.fillStyle = "rgba(255,255,255,.85)"; ctx.fillText(String(Math.ceil(-R.t)), W / 2, H * 0.3); }
    if (me.ocs){ ctx.font = font(700, 16); ctx.fillStyle = "#FFD447"; ctx.fillText(R.t < 0 || R.t < 3 ? "Partenza anticipata: torna dietro la linea" : "Non sei partito: torna dietro la linea e tagliala tra giuria e boa", W / 2, 88); }
    ctx.restore();
    const g = goal(); // dopo l'arrivo niente freccia
    if (g) offscreenArrow(v, g);
    linePill(v, R.pin, R.cb, R.t < 0 ? "Linea di partenza" : "Arrivo", g && g.kind !== "mark" ? g : null, 0, 4);
  }
  // freccia curva sulla prua: da che parte sta girando davvero la barca
  function drawTurnHint(){
    if (S.capsized || Math.abs(S.r) < 2.5) return;
    const st = curStep(); if (st && (st.pause || !st.hud)) return;
    const d = S.r > 0 ? 1 : -1, k = Math.min(1, Math.abs(S.r) / 20);
    ctx.save(); ctx.translate(S.x, S.y); ctx.rotate(S.h * D2R);
    ctx.strokeStyle = "rgba(255,212,71,.9)"; ctx.fillStyle = "rgba(255,212,71,.9)"; ctx.lineWidth = 0.18; ctx.lineCap = "round";
    const ex = d * (1.2 + 1.2 * k), ey = -3.2 - 0.6 * k;
    ctx.beginPath(); ctx.moveTo(0, -2.5); ctx.quadraticCurveTo(0, -3.6, ex, ey); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(ex + d * 0.45, ey); ctx.lineTo(ex - d * 0.15, ey - 0.4); ctx.lineTo(ex - d * 0.15, ey + 0.4); ctx.closePath(); ctx.fill();
    ctx.restore();
  }
  // scritta in basso: cosa fa la barra in questo momento
  function drawHelmLegend(){
    const st = curStep();
    if (S.capsized || (st && (st.pause || !st.tiller)) || Math.abs(ctl.tiller) < 0.12) return;
    const tl = ctl.tiller < 0 ? "a sinistra" : "a dritta";
    const turn = S.u < -0.05 ? (ctl.tiller < 0 ? "sinistra" : "dritta") : (ctl.tiller < 0 ? "dritta" : "sinistra");
    const txt = "Barra " + tl + " → la prua gira a " + turn + (S.u < -0.05 ? " (stai andando all'indietro)" : "");
    ctx.save(); ctx.font = font(600, 15); ctx.textAlign = "center"; ctx.textBaseline = "middle";
    const w = ctx.measureText(txt).width + 24, y = H - 70;
    ctx.fillStyle = "rgba(10,24,36,.7)"; ctx.fillRect(W / 2 - w / 2, y - 14, w, 28);
    ctx.fillStyle = "#FFD447"; ctx.fillText(txt, W / 2, y); ctx.restore();
  }
  function drawGhost(){
    if (!opt.ghost) return;
    let g = null;
    if (mode === "mission") g = ghostAt(recK("m" + missionIdx), S.time);
    if (mode === "race" && R) g = ghostAt(recK("r" + raceIdx) + "b", R.t);
    if (!g) return;
    drawOther(g, { alpha: 17, awa: -g.boomSide * 40 }, 0, 0.35);
  }

