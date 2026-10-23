// Scuola di vela, regate.js — Fantasma e regate: avversari, partenza, contatti, classifica, disegno della regata.
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/PROPOSTA-DIVISIONE-CODICE.md.
  // ======================================================================
  // FANTASMA E REGATE
  // ======================================================================
  // ---- fantasma ----
  let ghosts;
  const loadGhosts = () => { try { ghosts = JSON.parse(localStorage.getItem(GHOST_STORE) || "{}"); } catch(e){ ghosts = {}; } };
  loadGhosts();
  const saveGhosts = () => { if (LAB) return; try { localStorage.setItem(GHOST_STORE, JSON.stringify(ghosts)); } catch(e){} };
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
    { title: "Regata nelle raffiche", desc: "Tre avversari e vento rafficato: chi legge meglio l'acqua vince.", wind: 225, tws: 12, gusts: 1 },
    // 1.0.28: livello 2 in prova (docs/PROPOSTA-SALTI-VENTO.md): barca del livello 2, bolina di 300 m, salti di vento; resta fuori da meriti e carriera
    { title: "Regata nei salti di vento", desc: "Barca del livello 2, bolina di 300 m e vento che gira: vira sugli scarsi, o va verso la rotazione.", wind: 0, tws: 10, gusts: 0, lv2: true, up: 300, shifts: true }
  ];
  const RACES1 = RACES.filter(rc => !rc.lv2); // le regate del livello 1 (stessi indici: quelle del livello 2, col campo lv2, stanno in fondo); carriera, meriti e record contano solo queste
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
  const HOLD_S = -1; // in partenza si aspetta e si parte mure a dritta (precedenza): virare da fermi al via non riesce, e puntando un punto dritto controvento la barca zigzagava
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
      ? { up: 45 + r() * 3, down: 150 + r() * 5, trim: (r() - 0.5) * 4, gain: 18, boardMin: 35, boardMax: 90, react: 5, startM: 0.5 + (r() - 0.5) * 1 }
      : { up: 49 + r() * 5, down: 142 + r() * 8, trim: (r() - 0.5) * 12, gain: 26, boardMin: 25, boardMax: 60, react: 3, startM: 1.5 + (r() - 0.5) * 3 };
  }
  function startRace(i, wind){
    mode = "race"; raceIdx = i; showCards("race"); regReset();
    const rc = i === "t" ? torRc() : RACES[i], liv = rc.tor ? tor.liv : opt.aiLevel; // "t": la regata del torneo in corso (torneo dell'1b)
    setWhere(rc.tor ? "Torneo dell'1b" : "Regata: " + rc.title);
    env.twd = wind === undefined ? rc.wind : wind; env.tws = rc.tws / KN;
    curMarks = [];
    const spots = startSpots(liv === "nessuno" ? 1 : 1 + FLEET_LOOK.length);
    const [px, py] = fromWF(spots[0].x, spots[0].y);
    freshState(px, py, norm360(env.twd + spots[0].s * 90), 0.35);
    setGusts(rc.gusts, !!rc.tor);
    if (rc.lv2) S.lv = 2;
    if (rc.shifts) setShifts(Math.random() < 1 / 3 ? "pers" : "osc"); // un salto persistente una regata su tre
    const up = rc.up || MARK_UP;
    const [pinX, pinY] = fromWF(-LINE_HALF, 0), [cbX, cbY] = fromWF(LINE_HALF, 0), [mX, mY] = fromWF(0, -up), [cX, cY] = fromWF(0, 0);
    R = { t: -opt.countdown, phase: "pre", up, lv2: !!rc.lv2, tor: !!rc.tor, pin: { x: pinX, y: pinY }, cb: { x: cbX, y: cbY }, mark: { x: mX, y: mY, out: env.twd }, center: { x: cX, y: cY },
          boats: [], contacts: {}, signals: new Set(), doneAt: null };
    const me = { me: true, name: "Tu", S, ctl, info: null, wake, leg: 0, ocs: false, pen: 0, fin: null, prevWY: spots[0].y };
    R.boats.push(me);
    const slots = [-24, 2, 24].sort(() => Math.random() - 0.5);
    // una sola aggressiva, e solo con gli esperti; le altre prudenti o normali
    const aggro = liv === "esperti" ? Math.floor(Math.random() * FLEET_LOOK.length) : -1;
    (liv === "nessuno" ? [] : FLEET_LOOK).forEach((look, k) => {
      const spot = spots[k + 1];
      const [x, y] = fromWF(spot.x, spot.y);
      const bs = newBoat(x, y, norm360(env.twd + spot.s * 90));
      if (rc.lv2) bs.lv = 2;
      Object.assign(bs, { hullColor: look.hull, sailColor: look.sail, sailorColor: look.sailor });
      const b = { me: false, name: look.name, S: bs, ctl: { sheet: 0.4, tiller: 0 }, info: null, wake: [], wakeT: 0, leg: 0, ocs: false, pen: 0, fin: null,
                  prevWY: spot.y, rOff: Math.random() * 6, ai: aiParams(liv), side: 1, boardT: 0, boardMax: 40, startX: slots[k] + (Math.random() - 0.5) * 6,
                  char: k === aggro ? "aggressiva" : (Math.random() < 0.5 ? "prudente" : "normale") };
      if (rc.tor) Object.assign(b, { ai: { ...tor.av[k].ai }, char: tor.av[k].char }); // nel torneo la flotta resta la stessa per tutta la serie
      b.info = step(bs, b.ctl, env, 0); bs.dispBoom = bs.boomSide * bs.boom;
      R.boats.push(b);
    });
    recStart(recK("r" + i) + "b");
    $("rTitle").textContent = rc.title;
    R.brief = (rc.tor ? torBrief() : "") + "Vento da " + cardName(env.twd) + ", " + rc.tws + " nodi" + (rc.gusts ? " con raffiche" : "") +
      (rc.tor ? (rc.shifts ? ", che gira: oscilla di una dozzina di gradi ogni due minuti circa, oppure ruota sempre dalla stessa parte" : "") : rc.lv2 ? ", che gira: oscilla di una dozzina di gradi ogni due minuti circa, oppure ruota sempre dalla stessa parte. Barca del livello 2, boa a 300 m" : "") +
      ". Partenza tra la barca giuria e la boa arancione, girare la boa gialla di bolina lasciandola a sinistra e tornare a tagliare la stessa linea. Allo scadere del conto alla rovescia devi essere dietro la linea: conviene aspettare vicino alla linea, quasi fermo con la vela lascata, e cazzare negli ultimi secondi per essere già veloce allo zero. Se tagli prima dello zero vieni richiamato: torna dietro la linea e riparti subito, senza attese." +
      (liv === "nessuno" ? " Sei da solo: dalla seconda regata gareggi contro il fantasma del tuo record."
        : " Ogni avversario ha il suo carattere: " + R.boats.filter(b => !b.me).map(b => "la " + b.name + " è " + CHAR_TEXT[b.char]).join(", ") +
          ". Le posizioni dietro la linea cambiano a ogni partenza.") + centerNote();
    $("rDone").hidden = true; $("rTor").hidden = true; finShow();
    $("rRestart").hidden = $("rWind").hidden = rc.tor; $("rRet").hidden = !rc.tor; $("aiLevel").parentElement.hidden = rc.tor;
    setControls([], true, true); setHud(3); $("hint").hidden = !opt.hint;
    showBrief(rc.title, R.brief, true);
  }

  // obiettivo attuale della barca: lo usano la freccia fuori schermo, il rilevamento del pannello e il tasto vista
  function goal(){
    if (mode === "race") return R && R.boats[0].fin === null && !R.boats[0].dnf ? targetOf(R.boats[0]) : null;
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
      // avversari: tre punti di passaggio per lasciare la boa a sinistra (coordinate del vento, boa in (0, -R.up))
      // 0: poco sotto e a destra della boa; 1: oltre la boa, verso sinistra (qui si attraversa la semiretta e la boa è girata);
      // 2: solo se la boa è stata girata male o mancata: si torna sotto e a sinistra, per riprovare dal punto 0 passando sotto la boa
      const [wx, wy] = toWF(b.S.x, b.S.y), o = b.rOff, P = [[9 + o, -R.up - 3], [-16 - o, -R.up - 10 - o * 0.5], [-10, -R.up + 14]];
      const near = (k, r) => Math.hypot(wx - P[k][0], wy - P[k][1]) < r;
      // il punto 1 si punta solo da sopra la boa: da più in basso la bolina porterebbe la barca proprio sopra la boa
      if (!b.rp && (near(0, 4) || (wy < -R.up - 2 && wx > 3))) b.rp = 1;
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
    // 1.0.16 (docs/PROPOSTA-PARTENZE.md): si aspetta quasi fermi da una a due lunghezze dietro la linea e si parte per essere a piena
    // velocità allo zero. Prima si partiva a una velocità stimata fissa (1,9 m/s) frenando a 7 m: dalla 1.0.6 la barca scivola 10-11 m
    // e l'83% era oltre la linea allo sparo. Il blocco vale anche dopo lo sparo, finché chi è già partito non ha tagliato: con la logica
    // di bolina generale virava subito prima della linea, perdendo metà della velocità. L'avvicinamento, invece, resta alla logica
    // generale, che sa fare i bordi: il punto d'attesa è controvento e puntandolo con una prua sola la barca scivolava fino a 90 m di
    // lato, fuori dagli estremi, dove il taglio non conta.
    // 1.0.28, solo livello 2: col vento girato la prua di partenza può portare fuori dall'estremo, e da lì non si rientrava più
    // (regata nei salti, seme 20): dopo il via chi è fuori dagli estremi usa la logica generale, che punta un punto dentro la linea
    const fuori = R.lv2 && R.t >= 0 && Math.abs(toWF(s.x, s.y)[0]) > LINE_HALF - 3;
    if (b.leg === 0 && !b.ocs && (R.t < 0 || b.goStart) && !fuori){ // chi è oltre la linea torna indietro con la logica generale, che punta la linea: tenendo la prua della partenza se ne andava di bolina e non partiva più
      const [bx, by] = toWF(s.x, s.y);
      const L = BOAT.length, lat = Math.tan((ai.up + 4) * D2R); // metri di lato per ogni metro guadagnato verso la linea, in bolina larga
      const lineAim = twd + HOLD_S * (ai.up + 4); // verso la linea in bolina larga
      const yW = 1.5 * L, yF = 6 * L; // il punto d'attesa (metà della fascia) e il punto dove si attende il proprio turno, abbastanza dietro perché la deriva non conti
      if (b.waitX === undefined) // attesa e ritrovo spostati di lato quanto la barca scivolerà (verso -x in coordinate del vento), così il taglio cade fra le boe
        b.waitX = clamp(b.startX + lat * yW, lat * yW - (LINE_HALF - 2), LINE_HALF - 2); // dentro gli estremi sia l'attesa sia il taglio
      const far = -R.t > 45; // l'avvicinamento comincia a 45 s dal via: più presto si aspetterebbe vicino alla linea per minuti, scivolando fuori dagli estremi
      const [px, py] = far ? fromWF(b.waitX + lat * (yF - yW), yF) : fromWF(b.waitX, yW);
      if (!b.goStart && -R.t <= 30){ // quattro volte al secondo simula la propria partenza con step() e parte quando serve
        b.simT = (b.simT || 0) - dt;
        if (b.simT <= 0){ b.simT = 0.25; const T = startTime(b, lineAim, w, -R.t + 2); // simula fin poco oltre lo zero: se non arriva in tempo, parte subito
          if (T === null || -R.t <= T - ai.startM - (b.char === "prudente" ? 1 : 0)) b.goStart = true; } // il margine fa arrivare dopo lo zero, mai prima
      }
      b.holdA = holdAngle(by);
      if (b.goStart){ pre = true; b.preDesired = lineAim; if (by < 1 && R.t < -1) hold = true; } // partita: se è in anticipo non supera la linea prima dello zero
      // ancora in avvicinamento, con la logica generale perché sa fare i bordi; si lasca quando lo scivolamento simulato finirebbe
      // dentro la fascia d'attesa, cioè quando è il momento di smettere di spingere per fermarsi lì
      else if (Math.hypot(s.x - px, s.y - py) > (far ? 8 : 6) && glideY(b, w) > 2 * L) dest = { x: px, y: py };
      else { pre = true; hold = true; } // in attesa: si frena su tutta la linea e sui prolungamenti, non solo vicino agli estremi
      if (pre) b.boardT = 0; // il timer dei bordi non deve scadere durante l'attesa, altrimenti si vira appena tagliata la linea
    }
    const brg = bearingTo(s, dest);
    const rel = norm180(brg - twd);
    b.boardT += dt;
    if (hold){ desired = twd + (pre ? HOLD_S * b.holdA : 62); } // in attesa: quasi di bolina con la vela che sbatte, la barca resta quasi ferma
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
        const oTwa = norm180((R.lv2 ? windAt(o.S.x, o.S.y).twd : local.twd) - o.S.h); if (oTwa < 0) continue; // 1b: le mure col vento dove sta l'altra barca
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
    // 1.0.17 (docs/PROPOSTA-PARTENZE.md §8): chi sta evitando può orzare anche dentro l'angolo morto. Prima lo scarto veniva riscritto
    // dalla regola qui sotto: annullato nel 39% degli istanti in cui una barca stava scartando, e presente in 83 contatti su 88.
    const avoidR = b.char === "prudente" ? 22 : 14;
    let avoiding = false;
    for (const o of R.boats){
      if (o === b || o.fin !== null) continue;
      const d = Math.hypot(o.S.x - s.x, o.S.y - s.y); if (d > avoidR) continue;
      const relB = norm180(bearingTo(s, o.S) - s.h); if (Math.abs(relB) > 90) continue; // 1.0.17: era 60°; i contatti misurati hanno le prue a 93°, cioè l'altra arriva di fianco
      desired -= (relB >= 0 ? 1 : -1) * 35 * (1 - d / avoidR + 0.3); avoiding = true; break;
    }
    // la prua desiderata non deve mai finire nell'angolo morto (tranne durante una virata voluta)
    const dTwa = norm180(twd - desired);
    const wantsTack = !hold && Math.abs(rel) < ai.up && sgn(dTwa) !== side;
    if (!wantsTack && !avoiding && Math.abs(dTwa) < ai.up - 2) desired = twd - (sgn(dTwa) || side) * (ai.up - 2); // 1.0.17: chi evita può orzare oltre, e perde velocità come nella realtà
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
    b.ctl.tiller += (tillerFor(s, desired, ai) - b.ctl.tiller) * Math.min(1, dt * ai.react);
    let sheet = sheetFor(b.info, ai);
    if (hold || irons) sheet = 1;
    if (A > 158) sheet = Math.min(sheet, 0.42); // abbattuta controllata
    if (s.heel > 22) sheet = Math.min(1, sheet + 0.2);
    b.ctl.sheet += (sheet - b.ctl.sheet) * Math.min(1, dt * 3);
  }

  // la guida dell'avversario, la stessa nella regata e nelle due simulazioni qui sotto (startTime, glideY): se divergessero, la
  // simulazione non sarebbe quella che succederà. Barra verso la prua d (al contrario andando all'indietro):
  function tillerFor(s, d, ai){ return clamp(norm180(s.h - d) / ai.gain + s.r * 0.02, -1, 1) * (s.u < 0 ? -1 : 1); }
  // scotta regolata sul vento apparente, con l'errore tipico di questo avversario
  function sheetFor(info, ai){
    const boomT = Math.max(BOAT.minBoom, Math.abs(info ? info.awa : 60) - 17 + ai.trim);
    return clamp((boomT - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
  }
  // prua d'attesa rispetto al vento, a y metri dalla linea: a 55° arretra appena senza scivolare di lato, a 45° arretra di più (misure in PROPOSTA-PARTENZE.md §2)
  function holdAngle(y){ return y < 0.5 * BOAT.length ? 45 : 55; }

  // 1.0.16: secondi per tagliare la linea partendo adesso (cazza e va verso la prua d), con lo stesso step(); null se non ci arriva entro tMax
  function startTime(b, d, w, tMax){
    const s = Object.assign({}, b.S), c = { sheet: b.ctl.sheet, tiller: b.ctl.tiller }, ai = b.ai, dt = 1 / 20;
    let info = b.info;
    for (let t = 0; t < tMax; t += dt){
      if (toWF(s.x, s.y)[1] <= 0) return t;
      c.tiller += (tillerFor(s, d, ai) - c.tiller) * Math.min(1, dt * ai.react);
      c.sheet += (sheetFor(info, ai) - c.sheet) * Math.min(1, dt * 3);
      for (let i = 0; i < 3; i++) info = step(s, c, w, dt / 3);
    }
    return null;
  }

  // 1.0.16: dove si fermerebbe lascando adesso (distanza dalla linea in coordinate del vento), con lo stesso step(); ricalcolata due volte al secondo
  function glideY(b, w){
    const by0 = toWF(b.S.x, b.S.y)[1];
    if (by0 > 20) return by0;                                  // più lontana dell'abbrivio (10-11 m): non serve simulare
    if (b.glAt !== undefined && R.t - b.glAt < 0.5) return b.glY;
    b.glAt = R.t;
    const s = Object.assign({}, b.S), c = { sheet: b.ctl.sheet, tiller: b.ctl.tiller }, ai = b.ai, dt = 1 / 20;
    for (let t = 0; t < 30; t += dt){
      const y = toWF(s.x, s.y)[1];
      if (y <= BOAT.length || s.u < 0.05) return b.glY = y; // si fermerebbe a meno di una lunghezza dalla linea, oppure è già ferma
      c.tiller += (tillerFor(s, w.twd + HOLD_S * holdAngle(y), ai) - c.tiller) * Math.min(1, dt * ai.react); // le stesse prue dell'attesa
      c.sheet += (1 - c.sheet) * Math.min(1, dt * 3);           // vela tutta lascata, come in attesa
      for (let i = 0; i < 3; i++) step(s, c, w, dt / 3);
    }
    return b.glY = toWF(s.x, s.y)[1];
  }

  function stepAI(b, dt){
    const s = b.S;
    if (s.capsized){
      s.capT += dt; s.u = 0;
      if (s.capT > (s.lv === 2 ? RADD2.tAI : 5)){ s.capsized = false; s.capT = 0; s.heel = 0; s.heelRate = 0; s.h = norm360((s.lv === 2 ? windAt(s.x, s.y).twd : env.twd) + s.capSide * (s.lv === 2 ? RADD2.twa : 60)); b.ctl.sheet = s.lv === 2 ? 1 : 0.8; } // 1.0.32: livello 2 più lenta e al traverso del vento vero (coi salti, env.twd è il medio)
      return;
    }
    aiControl(b, dt);
    const w = windAt(s.x, s.y);
    for (let i = 0; i < 3; i++) b.info = step(s, b.ctl, w, dt / 3);
    if (s.heel > BOAT.capsizeAt || s.heel < -45){ s.capsized = true; s.capAt = simTime; s.capSide = s.heel > 0 ? s.boomSide : -s.boomSide; s.heel = 0; s.u = 0; }
    s.dispBoom += (s.boomSide * s.boom - s.dispBoom) * Math.min(1, dt * 6);
    b.wakeT += dt;
    if (b.wakeT > 0.1){ b.wakeT = 0; const h = s.h * D2R; b.wake.push({ x: s.x - Math.sin(h) * 2.1, y: s.y + Math.cos(h) * 2.1, nx: Math.cos(h), ny: Math.sin(h), t: simTime }); if (b.wake.length > 70) b.wake.shift(); }
  }

  // ---- svolgimento: lati, contatti, arrivo, classifica ----
  function raceLegs(b){
    const s = b.S, [wx, wy] = toWF(s.x, s.y), prev = b.prevWY; b.prevWY = wy;
    const onLine = Math.abs(wx) <= LINE_HALF;
    if (b.fin !== null || b.dnf) return;
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
      if (A.fin !== null || B.fin !== null || A.dnf || B.dnf || A.S.capsized || B.S.capsized) continue;
      const d = Math.hypot(A.S.x - B.S.x, A.S.y - B.S.y);
      if (R.contacts[key]){ if (d > 8) delete R.contacts[key]; continue; } // stesso contatto finché non si separano
      if (d > 4.2) continue;
      R.contacts[key] = simTime;
      // mure di ciascuna col vento nel suo punto (1b; nell'1a, difetto noto dalla 1.0.1, col vento del giocatore)
      const twA = R.lv2 ? windAt(A.S.x, A.S.y).twd : local.twd, twB = R.lv2 ? windAt(B.S.x, B.S.y).twd : local.twd;
      const tA = sgn(norm180(twA - A.S.h)), tB = sgn(norm180(twB - B.S.h));
      let guilty, why;
      if (tA !== tB) guilty = tA < 0 ? A : B;
      else { const ya = toWF(A.S.x, A.S.y)[1], yb = toWF(B.S.x, B.S.y)[1]; guilty = ya < yb ? A : B; }
      const v = (tu, lui) => guilty.me ? tu : lui; // 0.21.2: «tu eri… dovevi» al giocatore, terza persona per l'avversario
      why = tA !== tB ? v("eri", "era") + " mure a sinistra e " + v("dovevi", "doveva") + " lasciare strada a chi era mure a dritta"
                      : v("eri", "era") + " sopravento con le stesse mure e " + v("dovevi", "doveva") + " stare lontano";
      if (R.tor) guilty.pp = (guilty.pp || 0) + 1; else guilty.pen += 15; // torneo: penalità sul punteggio (F15 44.3), non sul tempo
      for (const o of [A, B]){ o.S.u *= 0.6; }
      const dx = (A.S.x - B.S.x) / (d || 1), dy = (A.S.y - B.S.y) / (d || 1);
      const push = (4.6 - d) / 2 + 0.3;
      A.S.x += dx * push; A.S.y += dy * push; B.S.x -= dx * push; B.S.y -= dy * push;
      if (A.me || B.me){
        regAdd("contacts"); if (guilty.me) regAdd("contactsPen");
        const other = A.me ? B : A;
        toast(guilty.me ? "Contatto! Penalità " + (R.tor ? "+1 punto" : "+15 s") : "Contatto: penalità a " + other.name);
        R.lastRule = (guilty.me ? "Contatto con " + other.name + ": tu " : "Contatto: " + guilty.name + " ") + why + (R.tor ? ". Penalità di 1 punto sul punteggio della regata." : ". Penalità di 15 secondi.");
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
    if (R.t >= 0 && Math.floor(R.t * 2) !== Math.floor(prevT * 2)) for (const b of R.boats){ // strada fatta ogni 0,5 s, per i distacchi
      const p = b.fin === null ? strada(b) : null; if (p !== null) (b.hist = b.hist || []).push([R.t, p]); }
    recSample(R.t, dt);
    const me = R.boats[0];
    if (R.tor) torFinestra();
    if (R.tor && (me.fin !== null || me.dnf) && R.phase !== "done"){ R.phase = "done"; R.doneAt = R.t; torArrivo(); }
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
  // 1.0.33: distacchi in secondi (docs/PROPOSTA-DISTACCHI.md). Strada fatta in metri, nella direzione del vento medio (lo spostamento
  // di lato non conta, come nel tracciamento delle regate vere): di bolina i metri saliti dalla linea (al più R.up), in poppa R.up più
  // i metri scesi dalla boa; null prima della partenza (o richiamata). Prima della conferma era la distanza in linea d'aria da boa e
  // centro della linea: chi tagliava l'arrivo a 15 m dal centro sembrava indietro. Ogni barca se la ricorda ogni 0,5 s; il distacco è
  // da quanti secondi la barca davanti aveva la strada che ho fatto io: un tempo vero, senza le penalità.
  function strada(b){
    if (b.fin !== null) return 2 * R.up;
    if (b.leg === 0 || b.ocs) return null;
    const wy = toWF(b.S.x, b.S.y)[1];
    return b.leg === 1 ? Math.min(R.up, -wy) : 2 * R.up + Math.min(0, wy);
  }
  function quando(b, p){ // primo istante in cui la barca b ha avuto la strada p (interpolato), null se mai
    const h = b.hist || [];
    for (let i = 0; i < h.length; i++) if (h[i][1] >= p){
      if (!i) return h[0][0];
      const [t0, p0] = h[i - 1], [t1, p1] = h[i]; return t0 + (t1 - t0) * (p - p0) / (p1 - p0 || 1);
    }
    return null;
  }
  function distacco(b){ // secondi della barca b da me: positivi se è davanti, negativi se è dietro; null se non si sa
    const me = R.boats[0];
    if (b.me || R.t < 0 || b.dnf || me.dnf) return null;
    if (me.fin !== null) return b.fin !== null ? me.fin - b.fin : null; // dopo il mio arrivo: i tempi d'arrivo, con le penalità
    const pm = strada(me), pb = strada(b);
    if (pm === null || pb === null) return null;
    const t = pb >= pm ? quando(b, pm) : quando(me, pb);
    return t === null ? null : (pb >= pm ? 1 : -1) * (R.t - t);
  }
  function ranking(){
    const score = b => b.fin !== null ? 1e7 - b.fin : b.dnf ? -2e6 : (b.ocs ? -1e6 : b.leg * 1e4 - Math.hypot(b.S.x - targetOf(b).x, b.S.y - targetOf(b).y));
    return [...R.boats].sort((a, b) => score(b) - score(a));
  }
  function raceResults(prev, tot){
    const rank = ranking(), pos = rank.indexOf(R.boats[0]) + 1;
    $("rDone").hidden = false;
    $("rDoneText").textContent = pos + "° su " + rank.length + " in " + fmtTime(tot) +
      (R.boats[0].pen ? " (penalità comprese: " + R.boats[0].pen + " s)" : "") + arrivoDistacchi() + "." + (!prev ? "" : tot < prev ? " Nuovo record!" : " Record: " + fmtTime(prev) + ".") +
      (regTotal() === 0 ? (reg.contacts ? " " + regText() + ". ★ senza errori." : " Nessun errore: ★ senza errori.") : " " + regText() + ".");
  }
  function arrivoDistacchi(){ // 1.0.33: «, a 4 s dalla Rossa (prima)»; tempi d'arrivo con le penalità, come la classifica
    const me = R.boats[0], prima = R.boats.filter(b => !b.me && b.fin !== null && b.fin <= me.fin).sort((a, b) => a.fin - b.fin);
    if (!prima.length) return "";
    const dav = prima[prima.length - 1], s = b => Math.round(me.fin - b.fin) + " s dalla " + b.name;
    return ", a " + s(dav) + (prima.length === 1 ? " (prima)" : ", a " + s(prima[0]) + " (prima)");
  }
  function legName(b){
    if (b.fin !== null) return "arrivata · " + fmtTime(Math.round(b.fin));
    if (b.dnf) return b.me && b.ret ? "ritirata" : "non arrivata";
    if (b.S.capsized) return "scuffiata!";
    if (b.ocs) return "partenza anticipata";
    if (b.leg === 1 && b.rnd < 0) return "boa girata dal lato sbagliato";
    return ["prima della partenza", "di bolina", "in poppa verso l'arrivo"][b.leg];
  }
  function racePanel(){
    if (!R) return;
    const rank = ranking();
    const gap = b => { const s = distacco(b); return s === null ? "" : " · " + (Math.round(s) < 0 ? "−" + -Math.round(s) : Math.round(s)) + " s"; }; // 1.0.33
    $("standings").innerHTML = rank.map(b => `<li class="${b.me ? "me" : ""}"><b>${b.name}</b> <span>${legName(b)}${b.pen ? " · +" + b.pen + " s" : ""}${b.pp ? " · +" + b.pp + " pt" : ""}${gap(b)}</span></li>`).join("");
    $("rRule").hidden = !R.lastRule; $("rRule").textContent = R.lastRule || "";
    finShow();
  }
  // ---- schermata finale (1.0.36, docs/PROPOSTA-SCHERMATA-FINALE.md) ----
  // A regata finita il riepilogo e la classifica passano dal pannello a un riquadro sopra il mare: il pannello non sfora più.
  // I riquadri #rDone e #standings restano compilati (i collaudi li leggono), solo nascosti dalla classe .fin.
  function finShow(){
    const on = R.phase === "done" && !$("rDone").hidden;
    document.querySelector(".panel").classList.toggle("fin", on);
    if (!on) return void ($("finOv").hidden = true);
    $("finText").textContent = $("rDoneText").textContent; $("finList").innerHTML = $("standings").innerHTML;
    $("finTor").hidden = $("rTor").hidden; $("finRestart").hidden = $("finWind").hidden = $("rRestart").hidden;
    if ($("finOv").hidden){ $("finOv").hidden = false; releaseKeys(); setTimeout(() => (!$("finRestart").hidden ? $("finRestart") : $("finTor")).focus(), 0); }
  }
  $("finRestart").onclick = () => $("rRestart").click(); $("finWind").onclick = () => $("rWind").click(); $("finTor").onclick = () => $("rTor").click();

  // ---- torneo dell'1b (1.0.34, tappa T1 di docs/PROPOSTA-TORNEI-1B.md) ----
  // Serie di 4 regate a bastone con la barca dell'1b contro gli stessi tre avversari, con lo stesso carattere. Punteggio di F15,
  // appendice A: punti bassi (A4), chi non arriva o si ritira prende iscritti + 1 (A5.2), uno scarto (A2.1) dopo la quarta regata,
  // parità con A8; un contatto con colpa è una penalità sul punteggio (44.3(c)), non 15 s. Finestra d'arrivo (appendice S, 12.3):
  // chi non arriva entro TOR_FIN volte il tempo della prima non arriva. Il torneo si salva in progress.torneo dopo ogni regata;
  // la regata interrotta (pagina chiusa, menu) si ricorre da capo. Le altre regate restano con i 15 s.
  const TOR_N = 4, TOR_FIN = 0.5; // TOR_FIN: ipotesi nostra, la finestra la scrivono le istruzioni di regata
  const TOR_COND = [{ nome: "10 nodi costanti", tws: 10, gusts: 0 }, { nome: "raffiche", tws: 12, gusts: 1 }, { nome: "salti di vento", tws: 10, gusts: 0, shifts: true }];
  let tor = null; // il torneo in corso: lo stesso oggetto di progress.torneo
  const torNome = k => "regata " + (k + 1) + " di " + TOR_N + " (" + TOR_COND[tor.regate[k].c].nome + ")";
  const fmtPt = v => String(Math.round(v * 10) / 10).replace(".", ",");
  function torNuovo(){
    const liv = opt.aiLevel === "nessuno" ? "principianti" : opt.aiLevel, aggro = liv === "esperti" ? Math.floor(Math.random() * FLEET_LOOK.length) : -1;
    return { ver: VERSIONE, liv, regate: [0, 1, 2, Math.floor(Math.random() * 3)].map(c => ({ c, wind: Math.floor(Math.random() * 8) * 45 })), // la quarta sorteggiata fra le tre
             av: FLEET_LOOK.map((l, k) => ({ ai: aiParams(liv), char: k === aggro ? "aggressiva" : Math.random() < 0.5 ? "prudente" : "normale" })), ris: [] };
  }
  function torRc(){
    const k = tor.ris.length, g = tor.regate[k], c = TOR_COND[g.c];
    return { title: "Torneo, regata " + (k + 1) + " di " + TOR_N, wind: g.wind, tws: c.tws, gusts: c.gusts, shifts: c.shifts, lv2: true, tor: true };
  }
  const torBrief = () => "Torneo dell'1b, " + torNome(tor.ris.length) + ", con la barca completa dell'1b. Punti: 1 al primo, 2 al secondo e così via; chi non arriva o si ritira ne prende " +
    (FLEET_LOOK.length + 2) + ". Un contatto con colpa vale 1 punto in più in questa regata invece dei 15 s (penalità sul punteggio, regola 44.3). Chi non arriva entro metà del tempo della prima, dopo il suo arrivo, non arriva. ";
  // punti di una regata, nell'ordine delle barche: r = [{ fin, pp }], fin = tempo d'arrivo o null (non arrivata o ritirata), pp = penalità
  function torPunti(r){
    const dnf = r.length + 1, pen = Math.round(2 * dnf) / 10; // A5.2; 44.3(c): 20% dei punti di chi non arriva, al decimo
    // ponytail: due arrivi allo stesso tempo hanno lo stesso posto (A7 farebbe la media): con i decimi di secondo non capita
    return r.map(b => b.fin === null ? dnf : Math.min(dnf, 1 + r.filter(o => o.fin !== null && o.fin < b.fin).length + b.pp * pen));
  }
  // classifica della serie: [{ i, p, sc, tot }] dalla prima all'ultima; i = barca, p = punti per regata, sc = regata scartata (-1 se nessuna)
  function torSerie(ris){
    const P = ris.map(torPunti);
    const cl = (ris[0] || []).map((x, i) => {
      const p = P.map(r => r[i]), sc = p.length >= TOR_N ? p.indexOf(Math.max(...p)) : -1; // a parità di peggiore si scarta la più vecchia
      return { i, p, sc, tot: p.reduce((a, v, k) => k === sc ? a : a + v, 0) };
    });
    const tenuti = x => x.p.filter((v, k) => k !== x.sc).sort((u, v) => u - v);
    return cl.sort((a, b) => {
      if (Math.abs(a.tot - b.tot) > 1e-9) return a.tot - b.tot;
      const ta = tenuti(a), tb = tenuti(b);
      for (let k = 0; k < ta.length; k++) if (ta[k] !== tb[k]) return ta[k] - tb[k];  // A8.1, senza gli scarti
      for (let k = a.p.length - 1; k >= 0; k--) if (a.p[k] !== b.p[k]) return a.p[k] - b.p[k]; // A8.2, dall'ultima regata, scarti compresi
      return 0;
    });
  }
  function torFinestra(){
    const f = R.boats.filter(b => b.fin !== null).map(b => b.fin);
    if (!f.length) return;
    R.torLim = Math.min(...f) * (1 + TOR_FIN);
    if (R.t < R.torLim) return;
    for (const b of R.boats) if (b.fin === null && !b.dnf){ b.dnf = true; if (b.me) toast("Finestra d'arrivo chiusa: non sei arrivato"); }
  }
  function torArrivo(){ // il giocatore ha finito la sua regata: arrivato, ritirato o fuori dalla finestra
    const me = R.boats[0], pen = me.pp ? " Penalità sul punteggio: +" + me.pp + (me.pp > 1 ? " punti." : " punto.") : "";
    $("rDone").hidden = false; $("rTor").hidden = false; $("rRet").hidden = true; $("hint").hidden = true; // finita la regata il suggerimento non serve: fa posto al risultato
    $("rDoneText").textContent = (me.fin !== null ? "Arrivato " + (1 + R.boats.filter(b => b.fin !== null && b.fin < me.fin).length) + "° in " + fmtTime(Math.round(me.fin)) + "." + pen
      : (me.ret ? "Ti sei ritirato" : "Non sei arrivato entro la finestra d'arrivo") + ": " + (R.boats.length + 1) + " punti."); // gli errori sono già nella riga sopra
  }
  // chiude la regata del torneo: le barche che navigano ancora arrivano (simulazione accelerata, senza il giocatore) o restano
  // fuori dalla finestra; poi il risultato entra nel torneo e si salva
  function torChiudi(){
    if (!R || !R.tor || R.torOk || !tor) return;
    const dt = 1 / 60;
    for (let k = 0; k < 60 * 1800 && R.boats.some(b => b.fin === null && !b.dnf); k++){ updateGusts(dt); updateRace(dt); simTime += dt; }
    R.torOk = true;
    tor.ris.push(R.boats.map(b => ({ fin: b.fin !== null && b.fin <= R.torLim ? Math.round(b.fin * 10) / 10 : null, pp: b.pp || 0 })));
    if (tor.ris.length === TOR_N) torFine();
    saveProgress();
  }
  function torFine(){ // dopo la quarta regata: piazzamento finale, meriti di Competizione dell'1b (solo carriera), torneo chiuso
    const pos = torSerie(tor.ris).findIndex(x => x.i === 0) + 1, mer = modo === "carriera" ? [6, 4, 3, 2][pos - 1] + (tor.ris.every(r => !r[0].pp) ? 1 : 0) : 0;
    const old = progress.torneoFatto || { pos: 9, mer: 0 };
    progress.torneoFatto = { pos: Math.min(pos, old.pos), mer: Math.max(mer, old.mer) }; // il migliore di sempre, piazzamento e meriti
    tor.fine = { pos, mer }; delete progress.torneo;
  }
  function torApri(){ // dal menu
    let nota = "";
    if (progress.torneo && progress.torneo.ver !== VERSIONE){ nota = "Il gioco è cambiato dalla versione " + progress.torneo.ver + ": il torneo in corso è stato chiuso, senza punti."; delete progress.torneo; saveProgress(); }
    tor = progress.torneo || null;
    torMostra(nota);
  }
  function torMostra(nota){
    const T = tor || torNuovo(), k = T.ris.length, inGioco = mode === "race";
    const nomi = ["Tu", ...FLEET_LOOK.map(l => l.name)], car = T.av.map((a, i) => "la " + FLEET_LOOK[i].name + " è " + CHAR_TEXT[a.char]).join(", ");
    const tab = k ? (() => { const P = T.ris.map(torPunti), cl = torSerie(T.ris);
      return `<table class="tor"><thead><tr><th></th><th>Barca</th>${T.ris.map((r, j) => `<th>R${j + 1}</th>`).join("")}<th>Totale</th></tr></thead><tbody>${cl.map((x, n) =>
        `<tr class="${x.i ? "" : "me"}"><td>${n + 1}°</td><td>${nomi[x.i]}</td>${x.p.map((v, j) => { const c = fmtPt(v) + (T.ris[j][x.i].pp ? "*" : "") + (T.ris[j][x.i].fin === null ? "°" : "");
          return `<td>${j === x.sc ? "(" + c + ")" : c}</td>`; }).join("")}<td><b>${fmtPt(x.tot)}</b></td></tr>`).join("")}</tbody></table>
        <p class="tor-leg">* penalità sul punteggio · ° non arrivata o ritirata · fra parentesi lo scarto${k < TOR_N ? ", che conta dopo la quarta regata" : ""}</p>`; })() : "";
    const fine = T.fine ? `<p class="score">${T.fine.pos}° su ${nomi.length}</p><p>${modo === "carriera" ? "Meriti di Competizione dell'1b: " + T.fine.mer + "." : "Nel gioco libero il torneo non dà meriti."}</p>` : "";
    const testa = !k ? `<p>Quattro regate a bastone con la barca completa dell'1b, contro gli stessi tre avversari (${T.liv}): ${car}. Vento: ${T.regate.map((g, j) => (j + 1) + ") " + TOR_COND[g.c].nome).join(", ")}.</p>
      <p>Punti come nel regolamento di regata: 1 al primo, 2 al secondo e così via, ${nomi.length + 1} a chi non arriva o si ritira; dopo la quarta regata la peggiore si scarta. Vince chi ha meno punti. Un contatto con colpa vale 1 punto in più nella regata. Il torneo si salva dopo ogni regata: se chiudi la pagina, la regata interrotta si ricorre da capo.</p>`
      : T.fine ? "" : `<p>Prossima: ${torNome(k)}.</p>`;
    $("torBody").innerHTML = `<div class="qz-top"><h2 id="torTitle">Torneo dell'1b</h2><span>${T.fine ? "finito" : k ? "dopo la regata " + k + " di " + TOR_N : ""}</span></div>
      ${nota ? `<p class="manca">${nota}</p>` : ""}${fine}${testa}${tab}
      <div class="row">${T.fine ? `<button class="primary" id="torMenu">Torna al menu</button>`
        : `<button class="primary" id="torGo">${k ? "Corri la regata " + (k + 1) : "Inizia il torneo"}</button>${tor ? `<button id="torRit">Ritirati dal torneo</button>` : ""}<button id="torMenu">${inGioco ? "Menu" : "Chiudi"}</button>`}</div>`;
    const chiudi = () => $("torDlg").close();
    $("torMenu").onclick = () => { chiudi(); if (T.fine) tor = null; if (inGioco || T.fine) showMenu(); };
    if ($("torGo")) $("torGo").onclick = () => { if (!tor){ tor = progress.torneo = T; saveProgress(); } chiudi(); openItem(["r", "t"]); };
    if ($("torRit")) $("torRit").onclick = () => { if (!confirm("Ritirarti dal torneo? Il torneo non conta: niente punti e niente piazzamento.")) return;
      delete progress.torneo; tor = null; saveProgress(); chiudi(); showMenu(); };
    releaseKeys(); $("torDlg").showModal();
  }
  $("rTor").onclick = () => { torChiudi(); torMostra(); };
  $("rRet").onclick = () => { const me = R && R.boats[0];
    if (!me || !R.tor || R.phase === "done" || !confirm("Ritirarti da questa regata? Prendi " + (R.boats.length + 1) + " punti, come chi non arriva.")) return;
    me.dnf = me.ret = true; };

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
      const tLine = vUp > 0.2 && dLine / vUp < 60 ? Math.round(dLine / vUp) : null; // 1.0.16: sopra 60 s il numero non serve (con la barca quasi ferma veniva enorme)
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

