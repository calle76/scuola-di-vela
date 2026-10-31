// Scuola di vela, regate.js — Fantasma e regate: avversari, partenza, contatti, classifica, disegno della regata.
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/archivio/PROPOSTA-DIVISIONE-CODICE.md.
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
  function drawWakeOf(wk, u, maxAge = 6, alpha = 0.6){ // di default la scia degli avversari; il giocatore la chiede di 8 s e più marcata (js/disegno.js)
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

  // ---- regate: elenco, posizioni di partenza, avvio, boe da puntare ----
  const RACES = [
    { title: "Regata a bastone", desc: "Tre avversari, vento costante: partenza, bolina, poppa, arrivo.", wind: 0, tws: 10, gusts: 0 },
    { title: "Regata nelle raffiche", desc: "Tre avversari e vento rafficato: chi legge meglio l'acqua vince.", wind: 225, tws: 12, gusts: 1 },
    // 1.0.28 (docs/archivio/PROPOSTA-SALTI-VENTO.md): barca dell'1b, bolina di 300 m, salti di vento; resta fuori da meriti e carriera
    { title: "Regata nei salti di vento", where: "salti di vento", desc: "Barca dell'1b, bolina di 300 m e vento che gira: vira sugli scarsi, o va verso la rotazione.", wind: 0, tws: 10, gusts: 0, lv2: true, up: 300, shifts: true },
    // 1.0.61 (docs/PROPOSTA-LIVELLO-2A.md, fetta 1): livello 2a, due giri al posto dei 15 s per il giocatore; resta fuori da meriti e carriera
    { title: "Regata con i giri di penalità", where: "giri di penalità", desc: "Livello 2: due giri se lasci male la strada, uno se tocchi una boa; bandiere sulla giuria.", wind: 0, tws: 10, gusts: 0, lv2: true, giri: true, segnali: true }
  ];
  const RACES1 = RACES.filter(rc => !rc.lv2); // le regate dell'1a (stessi indici: quelle dell'1b, col campo lv2, stanno in fondo); carriera, meriti e record contano solo queste
  const LINE_HALF = 35, MARK_UP = 140;
  let TRI_L = 140; // 1.0.55: lato del triangolo del torneo, in metri: il più piccolo con la mediana del pilota fra 4 e 5,5 minuti (C8: 4,03 sui semi 1-20, 4,16 sui 61-80); __sv.triL serve alla misura
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
  // una sola aggressiva, e solo con gli esperti: quale barca (indice nella flotta), o -1; le altre prudenti o normali
  const sorteggiaAggressiva = liv => liv === "esperti" ? Math.floor(Math.random() * FLEET_LOOK.length) : -1;
  const carattere = (k, aggro) => k === aggro ? "aggressiva" : (Math.random() < 0.5 ? "prudente" : "normale");
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
    setWhere(rc.tor ? "Torneo dell'1b" : "Regata: " + (rc.where || rc.title)); // 1.0.48: titolo corto nel pannello, perché «Regata: Regata nei salti di vento» andava a capo (check di Ale)
    env.twd = wind === undefined ? rc.wind : wind; env.tws = rc.tws / KN;
    curMarks = [];
    const spots = startSpots(liv === "nessuno" ? 1 : 1 + FLEET_LOOK.length);
    const [px, py] = fromWF(spots[0].x, spots[0].y);
    freshState(px, py, norm360(env.twd + spots[0].s * 90), 0.35);
    setGusts(rc.gusts, !!rc.tor);
    if (rc.lv2) S.lv = 2;
    if (rc.shifts) setShifts(Math.random() < 1 / 3 ? "pers" : "osc"); // un salto persistente una regata su tre
    const up = rc.up || MARK_UP, tri = !!rc.tri; // tri: triangolo equilatero di lato up, due boe (1.0.55)
    const [pinX, pinY] = fromWF(-LINE_HALF, 0), [cbX, cbY] = fromWF(LINE_HALF, 0), [mX, mY] = fromWF(0, -up), [cX, cY] = fromWF(0, 0);
    R = { cd: opt.countdown, t: -opt.countdown, phase: "pre", up, tri, lv2: !!rc.lv2, tor: !!rc.tor, giri: !!rc.giri, segnali: !!rc.segnali, need: 0, done: 0, giro: null, giroDir: 0, pin: { x: pinX, y: pinY }, cb: { x: cbX, y: cbY }, mark: { x: mX, y: mY, out: env.twd }, center: { x: cX, y: cY },
          boats: [], contacts: {}, penList: [], signals: new Set(), doneAt: null };
    R.marks = [R.mark]; // le boe nell'ordine del giro, tutte da lasciare a sinistra; il bastone ne ha una
    if (tri){ const [m2x, m2y] = fromWF(-0.866 * up, -0.5 * up); R.marks.push({ x: m2x, y: m2y, out: norm360(env.twd - 90) }); } // a sinistra guardando il vento: i lati al lasco sono a 120° dal vento
    const me = { me: true, name: "Tu", S, ctl, info: null, wake, leg: 0, ocs: false, pen: 0, fin: null, prevWY: spots[0].y };
    R.boats.push(me);
    const slots = [-24, 2, 24].sort(() => Math.random() - 0.5);
    const aggro = sorteggiaAggressiva(liv);
    (liv === "nessuno" ? [] : FLEET_LOOK).forEach((look, k) => {
      const spot = spots[k + 1];
      const [x, y] = fromWF(spot.x, spot.y);
      const bs = newBoat(x, y, norm360(env.twd + spot.s * 90));
      if (rc.lv2) bs.lv = 2;
      Object.assign(bs, { hullColor: look.hull, sailColor: look.sail, sailorColor: look.sailor });
      const b = { me: false, name: look.name, S: bs, ctl: { sheet: 0.4, tiller: 0 }, info: null, wake: [], wakeT: 0, leg: 0, ocs: false, pen: 0, fin: null,
                  prevWY: spot.y, rOff: Math.random() * 6, ai: aiParams(liv), side: 1, boardT: 0, boardMax: 40, startX: slots[k] + (Math.random() - 0.5) * 6,
                  char: carattere(k, aggro) };
      if (rc.tor) Object.assign(b, { ai: { ...tor.av[k].ai }, char: tor.av[k].char }); // nel torneo la flotta resta la stessa per tutta la serie
      b.info = step(bs, b.ctl, env, 0); bs.dispBoom = bs.boomSide * bs.boom;
      R.boats.push(b);
    });
    recStart(recK("r" + i) + "b"); rivReset();
    $("rTitle").textContent = rc.title;
    R.brief = introRegata(rc, liv);
    $("rDone").hidden = true; $("rTor").hidden = true; finShow();
    $("rRestart").hidden = rc.tor; $("rRet").hidden = !rc.tor; $("aiLevel").parentElement.hidden = rc.tor;
    setControls([], true, true); setHud(3); $("hint").hidden = !opt.hint;
    showBrief(rc.title, R.brief, true);
  }

  // il testo che si legge prima della regata (dopo la creazione delle barche: dice i caratteri degli avversari)
  function introRegata(rc, liv){
    let t = (rc.tor ? torBrief() : "") + "Vento da " + cardName(env.twd) + ", " + rc.tws + " nodi" + (rc.gusts ? " con raffiche" : "") +
      (rc.tor ? (rc.shifts ? ", che gira: oscilla di una dozzina di gradi ogni due minuti circa, oppure ruota sempre dalla stessa parte" : "") : rc.lv2 ? ", che gira: oscilla di una dozzina di gradi ogni due minuti circa, oppure ruota sempre dalla stessa parte. Barca dell'1b, boa a 300 m" : "") +
      ". Partenza tra la barca giuria e la boa arancione, " + (rc.tri ? "girare la boa 1 e poi la boa 2, tutte e due lasciandole a sinistra, e tornare a tagliare la stessa linea" : "girare la boa gialla di bolina lasciandola a sinistra e tornare a tagliare la stessa linea") + ". Allo scadere del conto alla rovescia devi essere dietro la linea: conviene aspettare vicino alla linea, quasi fermo con la vela lascata, e cazzare negli ultimi secondi per essere già veloce allo zero. Se tagli prima dello zero vieni richiamato: torna dietro la linea e riparti subito, senza attese." +
      (liv === "nessuno" ? " Sei da solo: dalla seconda regata gareggi contro il fantasma del tuo record."
        : " Ogni avversario ha il suo carattere: " + R.boats.filter(b => !b.me).map(b => "la " + b.name + " è " + CHAR_TEXT[b.char]).join(", ") +
          ". Le posizioni dietro la linea cambiano a ogni partenza.") + centerNote();
    if (rc.segnali) t += " Sulla barca giuria le bandiere dicono a che punto è la partenza: la bandiera di classe è l'avviso, la P (blu con il quadrato bianco) è il preparatorio e si ammaina a un minuto dal via, la classe si ammaina alla partenza. Se qualcuno parte in anticipo sale la X (bianca con la croce blu) finché non è tornato dietro la linea; dopo il via c'è la bandiera blu, perché la linea è d'arrivo. Il gioco non ha suoni: i tempi contano sulle bandiere.";
    if (rc.lv2) t += " Da questo livello i contatti sono quelli veri, scafo contro scafo. Prima avevi imparato a stare lontano perché il contatto scattava prima del contatto vero." +
      " Chi non lascia strada paga la penalità. Cede: con mure diverse, la barca mure a sinistra; con le stesse mure, se sono affiancate la sopravento, se non lo sono quella che sta dietro; e chi sta virando cede a tutte finché non è di nuovo di bolina.";
    return t;
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
    if (b.leg <= R.marks.length){
      if (b.me) return { ...R.marks[b.leg - 1], kind: "mark" };
      // avversari: tre punti di passaggio per lasciare la boa a sinistra (coordinate del vento, boa in (0, -R.up))
      // 0: poco sotto e a destra della boa; 1: oltre la boa, verso sinistra (qui si attraversa la semiretta e la boa è girata);
      // 2: solo se la boa è stata girata male o mancata: si torna sotto e a sinistra, per riprovare dal punto 0 passando sotto la boa
      // alla boa 2 (1.0.55) gli stessi punti ruotati di 90° attorno alla boa: lo «sopra» della boa 1 diventa il lato esterno a sinistra (ipotesi nostra, §8.7 punto 4)
      const [wx, wy] = toWF(b.S.x, b.S.y), o = b.rOff, due = b.leg === 2, [mx, my] = due ? toWF(R.marks[1].x, R.marks[1].y) : [0, -R.up];
      const P = due ? [[-3, -9 - o], [-10 - o * 0.5, 16 + o], [14, 10]].map(([dx, dy]) => [mx + dx, my + dy])
                    : [[9 + o, -R.up - 3], [-16 - o, -R.up - 10 - o * 0.5], [-10, -R.up + 14]];
      const near = (k, r) => Math.hypot(wx - P[k][0], wy - P[k][1]) < r;
      // il punto 1 si punta solo da sopra la boa: da più in basso la bolina porterebbe la barca proprio sopra la boa
      const sopra = due ? wx - mx < -2 && wy - my < -3 : wy < -R.up - 2 && wx > 3, oltre = due ? wy - my > 8 : wx < -8;
      if (!b.rp && (near(0, 4) || sopra)) b.rp = 1;
      else if (b.rp === 1 && ((oltre && (b.rnd || 0) < 0) || near(1, 8))) b.rp = 2; // girata male, o passata sotto la boa: si riprova
      else if (b.rp === 2 && near(2, 8)) b.rp = 0;
      const [x, y] = fromWF(P[b.rp || 0][0], P[b.rp || 0][1]); return { x, y, kind: "mark" };
    }
    if (!b.me){ const [x, y] = fromWF(b.startX * 0.8, 0); return { x, y, kind: "finish" }; }
    return { ...R.center, kind: "finish" };
  }

  // ---- guida degli avversari ----
  function cambiaBordo(b, ai){ b.side = -b.side; b.boardT = 0; b.boardMax = ai.boardMin + Math.random() * (ai.boardMax - ai.boardMin); } // scade il tempo del bordo: si vira, e si sorteggia la durata del prossimo
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
    // 1.0.16 (docs/archivio/PROPOSTA-PARTENZE.md): si aspetta quasi fermi da una a due lunghezze dietro la linea e si parte per essere a piena
    // velocità allo zero (le misure sono nella proposta). Il blocco vale anche dopo lo sparo, finché chi è già partito non ha tagliato;
    // l'avvicinamento resta alla logica generale, che sa fare i bordi.
    // 1.0.28, solo 1b: col vento girato la prua di partenza può portare fuori dall'estremo, e da lì non si rientrava più
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
      } else if (b.boardT > b.boardMax) cambiaBordo(b, ai);
      desired = twd - b.side * ai.up;
    } else if (Math.abs(rel) > 180 - (180 - ai.down)){ // bersaglio in poppa piena: lasco con abbattute
      if (b.boardT > b.boardMax) cambiaBordo(b, ai);
      desired = twd - b.side * ai.down;
    } else {
      desired = brg; b.side = sgn(norm180(twd - brg)); b.boardT = Math.min(b.boardT, b.boardMax * 0.5);
      // bersaglio a proravia del traverso ma sull'altra mura: virare direttamente da un'andatura larga non riesce (manca l'abbrivio).
      // Come un timoniere: prima orza fino alla bolina, poi vira, poi poggia verso il bersaglio.
      const newSide = sgn(norm180(twd - brg));
      if (newSide !== side && Math.abs(rel) < 90) desired = A > ai.up + 12 ? twd - side * ai.up : twd - newSide * ai.up;
    }
    // mure a sinistra: lascia strada a chi è mure a dritta, passandogli di poppa (solo 1a; nell'1b chi cede lo decide cedeAvv1b, qui sotto)
    if (!R.lv2 && side < 0 && !hold){
      for (const o of R.boats){
        if (o === b || o.S.capsized) continue;
        const d = Math.hypot(o.S.x - s.x, o.S.y - s.y); if (d > 30) continue;
        const oTwa = norm180(windOf(o) - o.S.h); if (oTwa < 0) continue; // nell'1a windOf è il vento del giocatore (difetto noto dalla 1.0.1)
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
    // evita qualsiasi barca vicina davanti (anche quando avrebbe diritto di rotta: meglio non urtare); la prudente comincia da più lontano.
    // Solo 1a: nell'1b decide cedeAvv1b. 1.0.17 (docs/archivio/PROPOSTA-PARTENZE.md §8): chi sta evitando può orzare anche dentro l'angolo morto
    // (prima lo scarto veniva riscritto dalla regola qui sotto: annullato nel 39% degli istanti, presente in 83 contatti su 88).
    const avoidR = b.char === "prudente" ? 22 : 14;
    let avoiding = false;
    if (R.lv2){ if (!hold) desired = cedeAvv1b(b, desired, twd, side, ai); } // avoiding resta false: nell'1b la prua non entra mai nell'angolo morto
    else for (const o of R.boats){
      if (o === b || o.fin !== null) continue;
      const d = Math.hypot(o.S.x - s.x, o.S.y - s.y); if (d > avoidR) continue;
      const relB = norm180(bearingTo(s, o.S) - s.h); if (Math.abs(relB) > 90) continue; // 1.0.17: era 60°; i contatti misurati hanno le prue a 93°, cioè l'altra arriva di fianco
      desired -= (relB >= 0 ? 1 : -1) * 35 * (1 - d / avoidR + 0.3); avoiding = true; break;
    }
    // 1.0.67 (docs/PROPOSTA-GIRI-AVVERSARI.md): chi ha un debito di giri e la via libera segue la sequenza dei giri al posto della rotta; le tre regole qui sotto (angolo morto, abbrivio, piantata) non valgono
    const gm = R.giri ? giroAI(b, dt, twd, ai) : null;
    if (gm !== null) desired = gm;
    // la prua desiderata non deve mai finire nell'angolo morto (tranne durante una virata voluta)
    const dTwa = norm180(twd - desired);
    const wantsTack = !hold && Math.abs(rel) < ai.up && sgn(dTwa) !== side;
    if (gm === null && !wantsTack && !avoiding && Math.abs(dTwa) < ai.up - 2) desired = twd - (sgn(dTwa) || side) * (ai.up - 2); // 1.0.17: chi evita può orzare oltre, e perde velocità come nella realtà
    // se per arrivare alla rotta voluta bisogna attraversare il vento e manca velocità: prima poggia e prendi abbrivio
    const turn = norm180(desired - s.h), toWind = norm180(twd - s.h);
    // (vale solo prima di iniziare: a virata in corso la velocità cala per forza, e non va interrotta)
    // 0.21.3: stessa soglia della regola «piantata» qui sotto (era 44° fisso): in partenza, fra 40° e 44°, nessuna delle due agiva e una barca
    // lenta che voleva virare oscillava per minuti attorno a 40° senza partire (collaudo_regate.py, regata nelle raffiche, seme 17)
    const ironsA = b.leg === 0 && !b.ocs ? 40 : 44;
    if (gm === null && sgn(turn) === sgn(toWind) && Math.abs(toWind) < Math.abs(turn) && Math.abs(toWind) >= ironsA && s.u < 1.1) desired = twd - side * 95;
    // piantata nell'angolo morto: poggia e lascia sbattere la vela finché riparte
    const irons = A < ironsA && s.u < 0.6; // 44°: tra 40° e 44° una barca ferma restava sospesa senza ripartire; in partenza resta 40° (con 44° poggia troppo presto vicino alla linea), salvo chi torna dietro la linea dopo una partenza anticipata
    if (irons && gm === null) desired = twd - side * 80;
    muoviTimone(b.ctl, s, desired, ai, dt);
    let sheet = sheetFor(b.info, ai);
    if (hold || irons) sheet = 1;
    if (A > 158) sheet = Math.min(sheet, 0.42); // abbattuta controllata
    if (s.heel > 22) sheet = Math.min(1, sheet + 0.2);
    b.ctl.sheet += (sheet - b.ctl.sheet) * Math.min(1, dt * 3);
  }

  // 1.0.49 (docs/PROPOSTA-AVVERSARI-1B.md, punto A), solo 1b: chi deve cedere secondo chiCede si scosta, chi ha la precedenza tiene la
  // rotta e scarta solo all'ultimo; mai dentro l'angolo morto. Prima ogni avversario scartava qualsiasi barca davanti entro 14-22 m, anche
  // avendo la precedenza, orzando fin dentro l'angolo morto: 72 piantate su 124 avendo la precedenza (tests/misura_avversari.py, semi 1-20).
  const D_CEDE = 30, T_CEDE = 15, CEDE_A = 28, ULTIMO = 1.5; // ipotesi nostre: 30 m e 28° come la regola 10 degli avversari dell'1a; 15 s di preavviso
  function cedeAvv1b(b, desired, twd, side, ai){
    const s = b.S, L = BOAT.length, vx = Math.sin(s.h * D2R) * s.u, vy = -Math.cos(s.h * D2R) * s.u;
    if (b.virando) return desired; // a virata in corso la si finisce
    let best = null, bt = 1e9;
    for (const o of R.boats){ // la barca col contatto più vicino nel tempo: chi passa a meno di due lunghezze entro T_CEDE s
      if (o === b || o.fin !== null || o.dnf || o.S.capsized) continue;
      const rx = o.S.x - s.x, ry = o.S.y - s.y, d = Math.hypot(rx, ry); if (d > D_CEDE) continue;
      const wx = Math.sin(o.S.h * D2R) * o.S.u - vx, wy = -Math.cos(o.S.h * D2R) * o.S.u - vy, w2 = wx * wx + wy * wy;
      const t = w2 > 1e-6 ? Math.max(0, -(rx * wx + ry * wy) / w2) : 0; // fra quanti secondi si è più vicini
      if (t >= bt || t > T_CEDE || (Math.hypot(rx + wx * t, ry + wy * t) > 2 * L && !(o === b.cedeA && t > 0))) continue; // chi sta già cedendo continua finché non si allontanano: altrimenti appena poggiato la previsione dice «passi», torna su e urta
      bt = t; best = { o, d };
    }
    if (!best){ b.cedeA = null; return desired; }
    const o = best.o, devo = chiCede(b, o).cede === b; b.cedeA = devo ? o : null;
    if (!devo && best.d > ULTIMO * L) return desired; // ha la precedenza: tiene la rotta (regole 14 e 16) fino a ULTIMO lunghezze
    const relB = norm180(bearingTo(s, o.S) - s.h);
    const base = sgn(norm180(twd - desired)) === side ? desired : twd - side * ai.up; // se la guida chiede di virare (timer dei bordi), si cede sulle mure di adesso
    const nd = devo && tackOf(b) !== tackOf(o) ? base - side * CEDE_A // regola 10: poggia e passa di poppa
      : base - (relB >= 0 ? 1 : -1) * (devo ? CEDE_A : 35);          // stesse mure, o ultimo momento: si scosta dall'altra
    const t2 = norm180(twd - nd);
    if (sgn(t2) === side && Math.abs(t2) >= ai.up - 2) return nd;
    return devo && Math.abs(relB) < 60 ? base - side * CEDE_A : twd - side * (ai.up - 2); // mai nell'angolo morto né oltre il vento: chi deve cedere a una barca davanti, se non può orzare, poggia
  }

  // la guida dell'avversario, la stessa nella regata e nelle due simulazioni qui sotto (startTime, glideY): se divergessero, la
  // simulazione non sarebbe quella che succederà. Barra verso la prua d (al contrario andando all'indietro):
  function tillerFor(s, d, ai){ return clamp(norm180(s.h - d) / ai.gain + s.r * 0.02, -1, 1) * (s.u < 0 ? -1 : 1); }
  // la barra segue la prua d con la prontezza dell'avversario; una sola legge per la regata e per le due simulazioni
  function muoviTimone(c, s, d, ai, dt){ c.tiller += (tillerFor(s, d, ai) - c.tiller) * Math.min(1, dt * ai.react); }
  // scotta regolata sul vento apparente, con l'errore tipico di questo avversario
  function sheetFor(info, ai){
    const boomT = Math.max(BOAT.minBoom, Math.abs(info ? info.awa : 60) - 17 + ai.trim);
    return clamp((boomT - BOAT.minBoom) / (BOAT.maxBoom - BOAT.minBoom), 0, 1);
  }
  // prua d'attesa rispetto al vento, a y metri dalla linea: a 55° arretra appena senza scivolare di lato, a 45° arretra di più (misure in docs/archivio/PROPOSTA-PARTENZE.md §2)
  function holdAngle(y){ return y < 0.5 * BOAT.length ? 45 : 55; }

  // 1.0.16: secondi per tagliare la linea partendo adesso (cazza e va verso la prua d), con lo stesso step(); null se non ci arriva entro tMax
  function startTime(b, d, w, tMax){
    const s = Object.assign({}, b.S), c = { sheet: b.ctl.sheet, tiller: b.ctl.tiller }, ai = b.ai, dt = 1 / 20;
    let info = b.info;
    for (let t = 0; t < tMax; t += dt){
      if (toWF(s.x, s.y)[1] <= 0) return t;
      muoviTimone(c, s, d, ai, dt);
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
      muoviTimone(c, s, w.twd + HOLD_S * holdAngle(y), ai, dt); // le stesse prue dell'attesa
      c.sheet += (1 - c.sheet) * Math.min(1, dt * 3);           // vela tutta lascata, come in attesa
      for (let i = 0; i < 3; i++) step(s, c, w, dt / 3);
    }
    return b.glY = toWF(s.x, s.y)[1];
  }

  function stepAI(b, dt){
    const s = b.S;
    if (s.capsized){
      s.capT += dt; s.u = 0;
      if (R.giri){ b.gCum = null; b.sconta = false; } // 1.0.67: scuffia durante i giri: il giro in corso si perde, il debito resta
      const b1 = s.lv === 2; // 1.0.32: l'1b si raddrizza più lenta e al traverso del vento vero (coi salti, env.twd è il medio)
      if (s.capT > (b1 ? RADD2.tAI : 5)){
        s.capsized = false; s.capT = 0; s.heel = 0; s.heelRate = 0;
        s.h = norm360((b1 ? windAt(s.x, s.y).twd : env.twd) + s.capSide * (b1 ? RADD2.twa : 60)); b.ctl.sheet = b1 ? 1 : 0.8;
      }
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

  // ---- svolgimento: i lati della regata ----
  function raceLegs(b){
    const s = b.S, [wx, wy] = toWF(s.x, s.y), prev = b.prevWY; b.prevWY = wy;
    const onLine = Math.abs(wx) <= LINE_HALF;
    if (b.fin !== null || b.dnf) return;
    if (b.leg === 0){
      if (R.t >= 0){
        if (b.ocs){ if (wy > 0){ b.ocs = false; if (R.xSet) R.xSet = R.xSet.filter(o => o !== b); if (b.me) toast("Sei tornato dietro la linea: ora riparti"); } }
        else if (prev > 0 && wy <= 0 && onLine){ b.leg = 1; if (b.me) toast("Partito! Ora la boa di bolina"); }
        else if (prev > 0 && wy <= 0 && !onLine){ b.ocs = true; if (b.me) regAdd("outLine"); if (b.me) toast("Sei passato fuori dalla linea: torna dietro e passa tra giuria e boa"); }
        else if (wy < -5 && !b.ocs){ b.ocs = true; if (b.me) regAdd("outLine"); } // oltre la linea senza averla tagliata: deve tornare indietro
      }
    } else if (b.leg <= R.marks.length){ // 1.0.55: una boa (bastone) o due (triangolo); al cambio di lato il giro riparte da zero, come nelle prove (gioco.js)
      const k = roundCheck(b, s.x, s.y, R.marks[b.leg - 1]), ultima = b.leg === R.marks.length;
      if (k < 0){ b.wrongMarks = (b.wrongMarks || 0) + 1; if (b.me) regAdd("wrongMarks"); }
      if (b.rnd >= 1){
        if (b.me) toast(!R.tri ? "Boa girata: ora all'arrivo" : ultima ? "Boa 2 girata: ora all'arrivo" : "Boa 1 girata: ora la boa 2");
        b.leg++; b.rnd = 0; b.rndA = undefined; b.rp = 0;
      }
      else if (k < 0 && b.me) roundToast(-1);
      else if (k > 0 && b.me) toast("Hai rimediato: ora girala lasciandola a sinistra");
    } else if (b.leg === R.marks.length + 1){
      if (prev < 0 && wy >= 0 && onLine){ if (R.giri){ if (b.me) giriMancanti(b); else giriMancantiAI(b); } b.fin = R.t + b.pen; if (b.me) toast("Arrivato!"); }
    }
  }

  // ---- sagoma degli scafi (1.0.39) ----
  // 1.0.39 (docs/archivio/PROPOSTA-CONTATTO-VERO.md): nell'1b il contatto è fra i contorni degli scafi, non fra cerchi di 2,1 m attorno ai centri.
  // Poligono di 24 punti dagli stessi punti di hullPath (js/disegno.js): prua in (0, -2,1), poppa in y = 2,1; coordinate locali (x di lato, y verso poppa).
  const HULL_PTS = (() => {
    const bez = (p0, p1, p2, p3) => { const o = []; for (let i = 1; i <= 10; i++){ const t = i / 10, u = 1 - t;
      o.push([u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0], u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]]); } return o; };
    return [[0, -2.1], ...bez([0, -2.1], [0.55, -1.5], [0.72, -0.2], [0.68, 0.7]), [0.56, 2.1], [-0.56, 2.1], [-0.68, 0.7], ...bez([-0.68, 0.7], [-0.72, -0.2], [-0.55, -1.5], [0, -2.1])];
  })();
  const hullWorld = S => { const h = S.h * D2R, c = Math.cos(h), s = Math.sin(h); return HULL_PTS.map(([x, y]) => [S.x + x * c - y * s, S.y + x * s + y * c]); };
  // separazione di due poligoni convessi (assi separatori): { pen, nx, ny } con pen = sovrapposizione minima sugli assi (positiva se si toccano, negativa: la distanza è almeno -pen)
  // e la normale da B ad A orientata dai centri (ax, ay) e (bx, by)
  function polySep(pa, pb, ax, ay, bx, by){
    let best = null;
    for (const poly of [pa, pb]) for (let i = 0; i < poly.length; i++){
      const [x0, y0] = poly[i], [x1, y1] = poly[(i + 1) % poly.length], l = Math.hypot(x1 - x0, y1 - y0), nx = (y1 - y0) / l, ny = -(x1 - x0) / l;
      if (l < 1e-9) continue; // l'ultimo punto del contorno è uguale al primo: lato di lunghezza zero, senza asse
      let a0 = 1e9, a1 = -1e9, b0 = 1e9, b1 = -1e9;
      for (const [x, y] of pa){ const d = x * nx + y * ny; if (d < a0) a0 = d; if (d > a1) a1 = d; }
      for (const [x, y] of pb){ const d = x * nx + y * ny; if (d < b0) b0 = d; if (d > b1) b1 = d; }
      const pen = Math.min(a1, b1) - Math.max(a0, b0);
      if (!best || pen < best.pen) best = { pen, nx, ny };
    }
    if (best.nx * (ax - bx) + best.ny * (ay - by) < 0){ best.nx = -best.nx; best.ny = -best.ny; }
    return best;
  }
  // sovrapposizione dei contorni di due scafi: { pen, nx, ny } con la normale da B ad A, oppure null se non si toccano
  function hullOverlap(A, B){ const m = polySep(hullWorld(A), hullWorld(B), A.x, A.y, B.x, B.y); return m.pen > 0 ? m : null; }
  // ---- chi cede (1.0.40, docs/PROPOSTA-REGOLE-PRECEDENZA-1B.md) ----
  // Una sola funzione per penalità, testo di fine regata e semaforo. Nell'1a (!R.lv2) le regole sono quelle di sempre (10, e le stesse
  // mure col più sopravento in y), identiche al bit; nell'1b valgono 10, 11, 12 e 13 di F15, con le definizioni sui contorni degli scafi.
  const windOf = b => R.lv2 ? windAt(b.S.x, b.S.y).twd : local.twd;
  const tackOf = b => sgn(norm180(windOf(b) - b.S.h)); // -1 mure a sinistra, +1 mure a dritta
  // X è «dietro» a Y (clear astern) se tutto lo scafo di X sta dietro la linea al traverso dal punto più a poppa dello scafo di Y
  function dietroA(X, Y){
    const h = Y.h * D2R, fx = Math.sin(h), fy = -Math.cos(h), proj = p => p[0] * fx + p[1] * fy;
    return Math.max(...hullWorld(X).map(proj)) < Math.min(...hullWorld(Y).map(proj));
  }
  // la barca A è in virata finché non è di nuovo di bolina (regola 13); aggiornato a ogni passo per tutte le barche dell'1b
  const VIRATA_MIN = 42, VIRATA_MAX = 10; // gradi dal vento vero e secondi: ipotesi nostre (docs/PROPOSTA-REGOLE-PRECEDENZA-1B.md)
  function aggiornaVirate(){
    for (const b of R.boats){
      const a = norm180(windOf(b) - b.S.h), sg = sgn(a);
      if (b.sgV !== undefined && sg !== b.sgV && Math.abs(a) < 90){ b.virando = true; b.virT = R.t; } // la prua ha passato il vento
      if (b.virando && (Math.abs(a) >= VIRATA_MIN || R.t - b.virT > VIRATA_MAX)) b.virando = false;
      b.sgV = sg;
    }
  }
  // spostamento laterale di B rispetto alla prua di A (positivo a dritta della prua di A); la barca più sopravento è quella con y minore
  const latDi = (A, B) => { const h = A.S.h * D2R; return (B.S.x - A.S.x) * Math.cos(h) + (B.S.y - A.S.y) * Math.sin(h); };
  const piuSopravento = (A, B) => toWF(A.S.x, A.S.y)[1] < toWF(B.S.x, B.S.y)[1] ? A : B;
  // 21.2: sta scontando (solo il giocatore, giriPenalita); 21.1: dopo lo sparo è ancora oltre la linea e deve tornare (b.ocs). 0 se nessuna delle due
  const subordinata = b => b.sconta ? 21.2 : (R.t >= 0 && b.ocs && b.fin === null && !b.dnf) ? 21.1 : 0;
  // ritorna { cede: la barca che deve cedere, regola: 10-13, 21.1 o 21.2 }
  function chiCede(A, B){
    const tA = tackOf(A), tB = tackOf(B);
    if (!R.lv2){ // 1a: come prima della 1.0.40
      if (tA !== tB) return { cede: tA < 0 ? A : B, regola: 10 };
      return { cede: piuSopravento(A, B), regola: 11 };
    }
    if (R.giri){ // 1.0.66 (docs/PROPOSTA-REGOLA-21-2.md): 21.1 chi torna dietro la linea dopo la partenza anticipata e 21.2 chi sconta una penalità lasciano strada a chi non lo fa; fra le due la Sezione A non vale
      const sa = subordinata(A), sb = subordinata(B);
      if ((sa !== 0) !== (sb !== 0)) return { cede: sa ? A : B, regola: sa || sb };
    }
    if (A.virando !== B.virando) return { cede: A.virando ? A : B, regola: 13 };                 // 13: chi vira cede a chi non vira
    if (A.virando) return { cede: latDi(A, B) < 0 ? B : A, regola: 13 };                           // entrambe in virata: cede quella a sinistra dell'altra, o quella dietro
    if (tA !== tB) return { cede: tA < 0 ? A : B, regola: 10 };
    if (dietroA(A.S, B.S)) return { cede: A, regola: 12 };                                       // 12: stesse mure, non affiancate, cede quella dietro
    if (dietroA(B.S, A.S)) return { cede: B, regola: 12 };
    const lat = latDi(A, B);                                                                         // 11: affiancate, cede la sopravento
    if (lat === 0) return { cede: piuSopravento(A, B), regola: 11 };
    return { cede: lat * tA > 0 ? B : A, regola: 11 };                                             // B sta dal lato delle mure di A: B è sopravento
  }
  // ---- giri di penalità (livello 2a, 1.0.61, docs/PROPOSTA-LIVELLO-2A.md; F15 44.1 e 44.2) ----
  // Solo nelle regate con R.giri e solo per il giocatore. Ogni contatto con colpa dà un debito di due giri (R.need). Un giro è fatto quando, negli ultimi GIRO_MAX_S secondi,
  // la prua ha ruotato di almeno GIRO_GRADI nello stesso verso (senza tornare indietro di più di GIRO_VERSO gradi dal picco) e ci sono state almeno una virata e una strambata.
  // Un giro nel verso opposto al precedente fa ricominciare il conto (R.done = 1). All'arrivo ogni giro mancante costa GIRO_SEC secondi (ripiego dichiarato: niente squalifica).
  const GIRO_GRADI = 360, GIRO_VERSO = 20, GIRO_MAX_S = 20, GIRO_SEC = 15, GIRO_INIZIO = 120; // ipotesi nostre (GIRO_INIZIO, 1.0.66: gradi in GIRO_MAX_S secondi da cui si sta scontando la penalità, regola 21.2): isteresi del verso (disturbo delle onde), tempo massimo di un giro, ripiego per giro non fatto
  function giroVia(){ const S = R.boats[0].S; R.giro = { h: S.h, cum: 0, buf: [], last: -1e9 }; }
  function giriMsg(){ const m = R.need - R.done; R.lastRule = m <= 0 ? "Penalità scontata: i giri sono fatti." : "Penalità: " + (m === 1 ? "ti manca un giro" : "devi fare " + m + " giri") + ", nello stesso verso, ciascuno con una virata e una strambata."; }
  function giriDebito(n){ R.need += n === undefined ? 2 : n; giroVia(); giriMsg(); if (R.boats[0].sconta) R.boats[0].scontaT = R.t; } // la finestra riparte a ogni colpa: i giri contano dopo l'infrazione, non prima
  function giriPenalita(){
    const me = R.boats[0], S = me.S, g = R.giro;
    if (!g || R.need <= R.done || me.fin !== null || me.dnf){ me.sconta = false; return; }
    if (S.capsized){ giroVia(); me.sconta = false; return; }
    g.cum += norm180(S.h - g.h); g.h = S.h;
    const gy = S.gybesC + S.gybesV;
    if (R.t - g.last >= 0.5){ g.buf.push([R.t, g.cum, S.tacks, gy]); g.last = R.t; while (g.buf.length && R.t - g.buf[0][0] > GIRO_MAX_S) g.buf.shift(); }
    const o = g.buf[0], net = o ? g.cum - o[1] : 0;
    if (me.sconta){ if (R.t - me.scontaT > GIRO_MAX_S){ me.sconta = false; giroVia(); } } // 21.2: venti secondi senza finire un giro e non si sta più scontando
    else if (Math.abs(net) >= GIRO_INIZIO){ me.sconta = true; me.scontaT = R.t; }
    if (!o || Math.abs(net) < GIRO_GRADI || S.tacks <= o[2] || gy <= o[3]) return;
    const v = Math.sign(net); let pk = 0;
    for (const e of g.buf){ const x = (e[1] - o[1]) * v; if (x > pk) pk = x; else if (pk - x > GIRO_VERSO) return; } // il verso è cambiato
    if (pk - net * v > GIRO_VERSO) return;
    R.done = R.giroDir && v !== R.giroDir ? 1 : R.done + 1; R.giroDir = v;
    giroVia(); giriMsg(); me.scontaT = R.t; if (R.done >= R.need) me.sconta = false;
    toast(R.done >= R.need ? "Penalità scontata" : "Giro fatto: ne manca ancora " + (R.need - R.done));
    if (R.done >= R.need) R.penList.push("Tu, penalità scontata: " + R.need + (R.need === 1 ? " giro" : " giri") + ".");
  }
  function giriMancanti(b){ // il giocatore taglia l'arrivo con il debito aperto
    const m = R.need - R.done; if (m <= 0) return;
    b.pen += GIRO_SEC * m; R.done = R.need;
    R.penList.push("Tu, giri di penalità non fatti (" + m + "): +" + GIRO_SEC * m + " s al tempo.");
  }

  // ---- giri di penalità degli avversari (livello 2a, 1.0.67, docs/PROPOSTA-GIRI-AVVERSARI.md; F15 44.1 e 44.2) ----
  // Solo nelle regate con R.giri. Un avversario colpevole di un contatto ha un debito (b.gDebt, due giri). Dopo lo sparo, in regata e con nessuna barca a meno di GIRO_AI_VIA lunghezze
  // (e lontano da boe e linea d'arrivo) gira: la sequenza di prue sta in giroAI. Se una barca arriva a meno di GIRO_AI_STOP lunghezze il giro si sospende e riparte da zero. Mentre gira
  // b.sconta è vero, quindi vale per lui la 21.2 (chiCede). Un giro è fatto con 360° nello stesso verso, una virata e una strambata (come per il giocatore). Semplificazione dichiarata: i giri
  // cominciano solo dopo lo sparo (il regolamento li vuole «appena possibile», anche prima).
  const GIRO_AI_VIA = 4, GIRO_AI_STOP = 2, GIRO_AI_ERR = 12, GIRO_AI_LONTANO = 25, GIRO_AI_LARGA = 80, GIRO_AI_LENTA = 1.5; // lunghezze, lunghezze, gradi (anticipo sulla prua successiva), metri da boe e arrivo, gradi dal vento e m/s sotto i quali si poggia per prima: ipotesi nostre
  function giroLibero(b, lung){ // nessun'altra barca (ancora in regata, non scuffiata) entro lung lunghezze
    for (const o of R.boats) if (o !== b && o.fin === null && !o.dnf && !o.S.capsized && Math.hypot(o.S.x - b.S.x, o.S.y - b.S.y) < lung * BOAT.length) return false;
    return true;
  }
  function giroLontano(b){ // non vicino a una boa del percorso né, sull'ultimo lato, alla linea d'arrivo
    for (const m of R.marks) if (Math.hypot(m.x - b.S.x, m.y - b.S.y) < GIRO_AI_LONTANO) return false;
    return !(b.leg === R.marks.length + 1 && Math.abs(toWF(b.S.x, b.S.y)[1]) < GIRO_AI_LONTANO);
  }
  function giroAI(b, dt, twd, ai){ // la prua voluta per i giri, o null se la barca non sta girando
    const s = b.S;
    if (!(b.gDebt > 0) || b.fin !== null || b.dnf || R.t < 0 || b.leg < 1 || b.ocs){ if (b.gCum != null){ b.gCum = null; b.sconta = false; } return null; }
    if (b.gCum == null){ // non sta girando: comincia solo se la via è libera
      if (!giroLibero(b, GIRO_AI_VIA) || !giroLontano(b)) return null;
      const sd = sgn(norm180(twd - s.h)) || b.side; // 1.0.68: il verso lo sceglie la barca all'inizio e resta lo stesso per tutta la penalità (44.2 non dice quale): da un'andatura larga o con poca velocità poggia per prima (strambata, poi virata: prende velocità), altrimenti orza per prima (virata, poi strambata)
      b.gV = b.gV || (Math.abs(norm180(twd - s.h)) >= GIRO_AI_LARGA || s.u < GIRO_AI_LENTA ? -sd : sd);
      b.gCum = 0; b.gH = s.h; b.gTk = 0; b.gGy = 0; b.gS = sgn(norm180(twd - s.h)); b.sconta = true;
    } else if (!giroLibero(b, GIRO_AI_STOP)){ b.gCum = null; b.sconta = false; return null; }
    b.gCum += norm180(s.h - b.gH) * b.gV; b.gH = s.h;
    if (s.u < 0.6) return null; // 1.0.68: quasi ferma il timone non governa: la guida normale la fa ripartire, poi il giro riprende (visto in collaudo: 26 s fermi a 44° dal vento)
    const sg = sgn(norm180(twd - s.h)); // gli avversari non hanno i contatori di virate e strambate del giocatore: si contano qui, dal cambio di mura (con il vento davanti: virata, dietro: strambata)
    if (sg !== 0 && b.gS !== 0 && sg !== b.gS){ if (Math.abs(norm180(twd - s.h)) < 90) b.gTk++; else b.gGy++; }
    if (sg !== 0) b.gS = sg;
    if (b.gCum >= 360 && b.gTk > 0 && b.gGy > 0){ // un giro fatto
      b.gDebt--; b.gFatti = (b.gFatti || 0) + 1; b.gCum = 0; b.gTk = 0; b.gGy = 0;
      if (b.gDebt <= 0){ b.gCum = null; b.sconta = false; b.gV = 0; b.boardT = 0; R.penList.push("La " + b.name + ", penalità scontata: i giri sono fatti."); return null; }
    }
    // la sequenza, nel senso del giro: prua a 'U' dal vento, dall'altra parte del vento 'U', 'D' (poppa larga), dall'altra parte 'D' passando dalla poppa; q = angolo dal vento visto nel verso del giro
    const q = norm180(twd - s.h) * b.gV, U = ai.up, D = ai.down, x = q > D + GIRO_AI_ERR ? q - 360 : q;
    const t = x > U + GIRO_AI_ERR ? U : x > -U + GIRO_AI_ERR ? -U : x > -D + GIRO_AI_ERR ? -D : D - 360;
    return twd - b.gV * t;
  }
  function giriMancantiAI(b){ // un avversario taglia l'arrivo con il debito aperto: come il giocatore, +GIRO_SEC s per giro
    const m = b.gDebt; if (!(m > 0)) return;
    b.pen += GIRO_SEC * m; b.gDebt = 0; b.gCum = null; b.sconta = false;
    R.penList.push("La " + b.name + ", giri di penalità non fatti (" + m + "): +" + GIRO_SEC * m + " s al tempo.");
  }

  // ---- boa toccata (livello 2a, 1.0.62, docs/PROPOSTA-LIVELLO-2A.md fetta 2; F15 31 e 44.1) ----
  // Nelle regate con R.giri e solo per il giocatore: toccare una boa che conta ora costa UN giro (giriDebito(1)). Dalla 1.0.63 le boe sono anche ostacoli fermi (boeUrto).
  // Contano la linea (spillo e comitato) fino al via e sull'ultimo lato, la boa del lato in corso e, dal secondo lato, quella da cui il lato parte. Un tocco vale una volta
  // finché lo scafo non si allontana di BOA_LIBERA m dal bordo.
  const BOA_R = 0.9, BOA_LIBERA = 3; // m: raggio della boa come disegnata, distanza dal bordo per poter rifare un tocco; ipotesi nostre
  function distScafoPunto(S, px, py){ // distanza dal contorno dello scafo (convesso) a un punto; 0 se il punto è dentro
    const P = hullWorld(S); let dentro = true, best = 1e9;
    for (let i = 0; i < P.length; i++){
      const [x0, y0] = P[i], [x1, y1] = P[(i + 1) % P.length], ex = x1 - x0, ey = y1 - y0, l2 = ex * ex + ey * ey;
      if (ex * (py - y0) - ey * (px - x0) < 0) dentro = false;
      const t = l2 > 1e-12 ? Math.max(0, Math.min(1, ((px - x0) * ex + (py - y0) * ey) / l2)) : 0;
      best = Math.min(best, Math.hypot(px - x0 - t * ex, py - y0 - t * ey));
    }
    return dentro ? 0 : best;
  }
  function boeCheConta(me){
    const L = me.leg, out = [], linea = () => { out.push(["pin", R.pin, BOA_R]); out.push(["cb", R.cb, 0]); };
    if (L === 0) linea();
    else if (L <= R.marks.length) out.push(["m" + (L - 1), R.marks[L - 1], BOA_R]);
    else linea();
    if (L >= 2 && L <= R.marks.length + 1) out.push(["m" + (L - 2), R.marks[L - 2], BOA_R]);
    return out;
  }
  // 1.0.63 (fetta 2b): per il giocatore ogni oggetto del percorso (spillo, comitato, boe) è anche un ostacolo fermo: lo scafo che lo tocca viene spinto fuori
  // (a ogni passo, fino a 0,05 m oltre) e al primo passo del tocco perde il 40% della velocità, come nei contatti fra barche. La penalità spetta solo alle boe che contano ora
  // (boeCheConta). Gli avversari non si respingono. Spillo e boe sono cerchi; 1.0.64: la barca del comitato è il suo scafo, lo stesso poligono con cui è disegnata
  // (drawRace), perché con un cerchio di 2 m a prua e a poppa lo scafo disegnato si attraversava.
  const CB_PTS = [[0, -4], [1.6, -1.5], [1.5, 4], [-1.5, 4], [-1.6, -1.5]]; // gli stessi punti di drawRace, in metri attorno a R.cb, con la prua verso il vento
  const cbWorld = () => { const h = env.twd * D2R, c = Math.cos(h), s = Math.sin(h); return CB_PTS.map(([x, y]) => [R.cb.x + x * c - y * s, R.cb.y + x * s + y * c]); };
  // com'è messo lo scafo S rispetto all'oggetto: d = distanza dal bordo (0 se si toccano), tocca, urta (penetra), e la direzione per uscirne
  function statoOggetto(S, key, mk, r){
    if (key === "cb"){ const m = polySep(hullWorld(S), cbWorld(), S.x, S.y, R.cb.x, R.cb.y); return { d: m.pen > 0 ? 0 : -m.pen, tocca: m.pen > 0, urta: m.pen > 0, push: m.pen + 0.05, nx: m.nx, ny: m.ny }; }
    const d = distScafoPunto(S, mk.x, mk.y); let nx = S.x - mk.x, ny = S.y - mk.y; const l = Math.hypot(nx, ny);
    if (l < 1e-6){ const h = S.h * D2R; nx = -Math.sin(h); ny = Math.cos(h); } else { nx /= l; ny /= l; }
    return { d, tocca: d <= r, urta: d < r, push: Math.max(0.05, r + 0.05 - d), nx, ny };
  }
  function boeUrto(me, mk, r, key){
    const S = me.S; let st = statoOggetto(S, key, mk, r); if (!st.urta) return;
    R.boaUrto = R.boaUrto || {};
    if (!R.boaUrto[key]){ R.boaUrto[key] = true; S.u *= 0.6; }
    for (let k = 0; k < 12 && st.urta; k++){ S.x += st.nx * st.push; S.y += st.ny * st.push; st = statoOggetto(S, key, mk, r); }
  }
  function boeToccate(){
    const me = R.boats[0];
    if (me.fin !== null || me.dnf) return;
    R.boaTocc = R.boaTocc || {}; R.boaUrto = R.boaUrto || {};
    const contano = new Set(boeCheConta(me).map(e => e[0]));
    const tutte = [["pin", R.pin, BOA_R], ["cb", R.cb, 0], ...R.marks.map((mk, k) => ["m" + k, mk, BOA_R])]; // r = 0 per il comitato: ha la sua forma
    for (const [key, mk, r] of tutte){
      if (Math.hypot(me.S.x - mk.x, me.S.y - mk.y) > r + 8){ delete R.boaUrto[key]; delete R.boaTocc[key]; continue; } // lontano: nessun controllo, e il tocco si può rifare
      const st = statoOggetto(me.S, key, mk, r);
      if (R.boaUrto[key] && st.d > r + 0.3) delete R.boaUrto[key];
      if (R.boaTocc[key]){ if (st.d > r + BOA_LIBERA) delete R.boaTocc[key]; }
      else if (st.tocca && contano.has(key)){
        R.boaTocc[key] = R.t; R.nBoa = (R.nBoa || 0) + 1; giriDebito(1);
        const nome = key === "pin" ? "la boa dello spillo" : key === "cb" ? "la barca del comitato" : "la boa";
        R.rqMotivo = "toccata " + nome;
        R.penList.push("Tu, hai toccato " + nome + ": un giro di penalità (regola 31).");
        R.lastRule = "Hai toccato " + nome + " (regola 31): un giro di penalità, con una virata e una strambata. " + (R.need - R.done === 1 ? "Ti manca un giro." : "Ti mancano " + (R.need - R.done) + " giri.");
        toast("Hai toccato " + nome + "! Un giro di penalità");
        rivMark("Boa toccata a " + rivTempo(R.t) + ". " + R.penList[R.penList.length - 1], true);
      }
      boeUrto(me, mk, r, key);
    }
  }

  // ---- semaforo e contatti ----
  // semaforo di precedenza sullo scafo del giocatore (facoltativo, solo 1b): R.sem = "rosso" (devi lasciare strada), "verde" (hai la precedenza) o null.
  // Compare con un'altra barca (non finita né scuffiata) entro SEM_ON m che si avvicina; resta SEM_TENUTA s dopo l'ultimo avvicinamento, fino a SEM_OFF m.
  const SEM_ON = 8, SEM_OFF = 10, SEM_TENUTA = 2; // ipotesi nostre
  function semaforo(){
    const me = R.boats[0]; let best = null, bd = 1e9;
    for (const o of R.boats){
      if (o === me || o.fin !== null || o.dnf || o.S.capsized) continue;
      const d = Math.hypot(o.S.x - me.S.x, o.S.y - me.S.y);
      if (o.dSemT === undefined || R.t - o.dSemT >= 0.5){ // distanza confrontata ogni mezzo secondo: si avvicina di almeno 0,1 m
        if (o.dSem !== undefined && d < o.dSem - 0.1 && d < SEM_ON) R.semUntil = R.t + SEM_TENUTA;
        o.dSem = d; o.dSemT = R.t; }
      if (d < bd){ bd = d; best = o; }
    }
    R.semNome = best ? best.name : null; // per i collaudi: con quale barca è calcolato il colore
    R.sem = best && !me.S.capsized && me.fin === null && !me.dnf && R.t <= (R.semUntil || -1) && bd < SEM_OFF ? (chiCede(me, best).cede === me ? "rosso" : "verde") : null;
  }
  // il motivo della penalità: «tu eri… dovevi» al giocatore (0.21.2), terza persona per l'avversario; nell'1b con il numero della regola
  function motivoContatto(cc, guilty){
    const v = (tu, lui) => guilty.me ? tu : lui;
    return ({ 10: v("eri", "era") + " mure a sinistra e " + v("dovevi", "doveva") + " lasciare strada a chi era mure a dritta",
              11: v("eri", "era") + " sopravento con le stesse mure e " + v("dovevi", "doveva") + " stare lontano",
              12: v("eri", "era") + " dietro, con le stesse mure e senza essere affiancat" + v("o", "a") + ": " + v("dovevi", "doveva") + " lasciare strada a chi stava davanti",
              13: v("eri", "era") + " in virata: " + v("dovevi", "doveva") + " lasciare strada finché non " + v("eri", "era") + " di nuovo di bolina",
              21.1: v("stavi", "stava") + " tornando dietro la linea dopo una partenza anticipata e " + v("dovevi", "doveva") + " lasciare strada a chi non lo faceva",
              21.2: v("stavi", "stava") + " scontando una penalità e " + v("dovevi", "doveva") + " lasciare strada a chi non la scontava" })[cc.regola] + (R.lv2 ? " (regola " + cc.regola + ")" : "");
  }
  function contacts(){
    const bs = R.boats;
    for (let i = 0; i < bs.length; i++) for (let j = i + 1; j < bs.length; j++){
      const A = bs[i], B = bs[j], key = i + "-" + j;
      if (A.fin !== null || B.fin !== null || A.dnf || B.dnf || A.S.capsized || B.S.capsized) continue;
      const d = Math.hypot(A.S.x - B.S.x, A.S.y - B.S.y);
      if (R.contacts[key]){
        if (d > 8) delete R.contacts[key];
        else if (d <= 4.4){ // 1.0.41 (1b) e 1.0.42 (anche 1a, correzione di un difetto): gli scafi non si compenetrano; finché si toccano si spingono fuori ad ogni passo (la penalità resta una sola)
          const m = hullOverlap(A.S, B.S); if (m){ const p = m.pen / 2 + 0.02; A.S.x += m.nx * p; A.S.y += m.ny * p; B.S.x -= m.nx * p; B.S.y -= m.ny * p; } }
        continue; } // stesso contatto finché non si separano
      let mtv = null;
      if (R.lv2){ if (d > 4.4) continue; mtv = hullOverlap(A.S, B.S); if (!mtv) continue; } // 1b: scafo contro scafo; 4,4 m = due mezze lunghezze, oltre non si toccano
      else if (d > 4.2) continue;                                                          // 1a: cerchio di 4,2 m, la distanza di sicurezza dichiarata
      R.contacts[key] = simTime;
      // mure di ciascuna col vento nel suo punto (1b; nell'1a, difetto noto dalla 1.0.1, col vento del giocatore)
      const cc = chiCede(A, B), guilty = cc.cede;
      const why = motivoContatto(cc, guilty);
      if (R.tor) guilty.pp = (guilty.pp || 0) + 1; else if (R.giri){ if (guilty.me) giriDebito(); else guilty.gDebt = (guilty.gDebt || 0) + 2; } else guilty.pen += 15; // torneo: penalità sul punteggio (F15 44.3), non sul tempo; regata dei giri (1.0.61): il giocatore deve due giri
      for (const o of [A, B]){ o.S.u *= 0.6; }
      const dx = mtv ? mtv.nx : (A.S.x - B.S.x) / (d || 1), dy = mtv ? mtv.ny : (A.S.y - B.S.y) / (d || 1);
      const push = mtv ? mtv.pen / 2 + 0.15 : (4.6 - d) / 2 + 0.3; // 1b: si separano di 0,3 m fra gli scafi
      A.S.x += dx * push; A.S.y += dy * push; B.S.x -= dx * push; B.S.y -= dy * push;
      // 1.0.49 (docs/PROPOSTA-AVVERSARI-1B.md, punto C): ogni penalità col motivo, per l'elenco a fine regata; nell'1b anche un messaggio quando si toccano due avversari
      const altra = guilty === A ? B : A;
      R.penList.push((guilty.me ? "Tu" : "La " + guilty.name) + ", contatto con " + (altra.me ? "te" : "la " + altra.name) + ": " + why + ".");
      rivMark("Contatto a " + rivTempo(R.t) + ". " + R.penList[R.penList.length - 1], true);
      if (R.lv2 && !A.me && !B.me) toast("Contatto fra " + A.name + " e " + B.name + ": penalità alla " + guilty.name);
      if (A.me || B.me){
        regAdd("contacts"); if (guilty.me) regAdd("contactsPen");
        const other = A.me ? B : A;
        if (guilty.me) R.rqMotivo = "contatto con la " + other.name;
        toast(guilty.me ? "Contatto! Penalità " + (R.tor ? "+1 punto" : R.giri ? "due giri" : "+15 s") : "Contatto: penalità a " + other.name);
        R.lastRule = (guilty.me ? "Contatto con " + other.name + ": tu " : "Contatto: " + guilty.name + " ") + why + (R.tor ? ". Penalità di 1 punto sul punteggio della regata." : R.giri && guilty.me ? ". Penalità: due giri nello stesso verso, ciascuno con una virata e una strambata." : R.giri ? ". Penalità alla " + guilty.name + ": due giri." : ". Penalità di 15 secondi.");
      }
    }
  }

  // ---- bandiere della partenza (livello 2a, 1.0.65, docs/PROPOSTA-SEGNALI-PARTENZA.md, fetta 3; F15 26 e 29.1) ----
  // Solo nelle regate con R.segnali. Sequenza del regolamento con 5 minuti (classe a -300, P a -240, P giù a -60, classe giù al via); con 3 minuti la sequenza breve
  // (classe a -180, P a -120); con 1 minuto solo la classe (ipotesi nostre per 3 e 1). Dopo il via la linea è d'arrivo (blu). La X (richiamo individuale) sale allo sparo se una barca
  // è oltre la linea e resta finché quelle barche non sono tornate, al massimo X_MAX s.
  const X_MAX = 240; // s dallo sparo (F15 29.1)
  function bandiereAl(t, cd){ // classe, P e blu a un dato istante di regata (la X dipende dalle barche: bandiereR)
    const b = { classe: false, P: false, X: false, blu: false };
    if (t >= 0) b.blu = true;
    else { b.classe = t >= -cd; b.P = cd >= 180 && t >= -(cd - 60) && t < -60; }
    return b;
  }
  function bandiereR(){
    const b = bandiereAl(R.t, R.cd);
    b.X = R.t >= 0 && R.t < X_MAX && !!R.xSet && R.xSet.some(o => o.ocs && o.fin === null && !o.dnf);
    return b;
  }
  const BANDIERA_BLU = "#1F4FA3";
  function drawBandiera(tipo, cx, cy, w, h){ // 1.0.70: una bandiera (classe, P, X o blu) centrata in (cx, cy); la usano la barca giuria e il riquadro; spessore e colore del bordo li sceglie chi chiama
    ctx.fillStyle = tipo === "P" || tipo === "blu" ? BANDIERA_BLU : "#FFFFFF"; ctx.fillRect(cx - w / 2, cy - h / 2, w, h); ctx.strokeRect(cx - w / 2, cy - h / 2, w, h);
    ctx.fillStyle = BANDIERA_BLU;
    if (tipo === "classe"){ ctx.beginPath(); ctx.moveTo(cx, cy - h * 0.35); ctx.lineTo(cx + w * 0.25, cy + h * 0.35); ctx.lineTo(cx - w * 0.25, cy + h * 0.35); ctx.closePath(); ctx.fill(); }
    else if (tipo === "P"){ ctx.fillStyle = "#FFFFFF"; ctx.fillRect(cx - w * 0.25, cy - h * 0.25, w * 0.5, h * 0.5); }
    else if (tipo === "X"){ ctx.fillRect(cx - w * 0.07, cy - h / 2, w * 0.14, h); ctx.fillRect(cx - w / 2, cy - h * 0.09, w, h * 0.18); }
  }
  function drawBandiere(ppm){ // dentro il translate e il rotate della barca giuria; ogni bandiera nel suo posto (due file da due), con misura minima in pixel
    const f = bandiereR(), k = Math.min(1.1, Math.max(1, 12 / (1.5 * ppm))), w = 1.5 * k, h = 1.0 * k, yA = -0.7, yB = 0.6;
    ctx.lineWidth = 0.07; ctx.strokeStyle = "#33414A";
    if (f.classe) drawBandiera("classe", -0.8, yA, w, h);
    if (f.P) drawBandiera("P", 0.8, yA, w, h);
    if (f.X) drawBandiera("X", -0.8, yB, w, h);
    if (f.blu) drawBandiera("blu", 0.8, yB, w, h);
  }
  const bandiereTesto = f => ["classe", "P", "X", "blu"].filter(k => f[k]).join("+") || "nessuna";

  // ---- riquadro delle bandiere e delle penalità (livello 2a, 1.0.70, docs/PROPOSTA-RIQUADRO-BANDIERE.md) ----
  // Solo nelle regate con R.segnali. Due pezzi in alto ai lati del mare, dove prima c'erano la spia della registrazione (a sinistra) e il vento con la bussola (a destra); orologio e messaggio stanno al centro:
  // a sinistra le bandiere esposte in grande con una riga che dice cosa significano; a destra la X, le penalità e l'avviso «sei oltre la linea» (questo solo con i Suggerimenti
  // accesi; il test è quello che decide la X allo sparo: centro della barca oltre la linea). Le bandiere si vedono per RQ_PERM s dopo ogni cambio (la X finché c'è); a destra solo se c'è qualcosa da dire.
  const RQ_PERM = 10, RQ_SCONTATA = 6, RQ_LAMPO = 1.5, RQ_X = 16, RQ_BW = 44, RQ_BH = 30; // secondi e pixel: ipotesi nostre
  const RQ_NOMI = { classe: "Classe", P: "P", X: "X", blu: "Blu" }, rqMis = new Map();
  const RQ_YS = 10, RQ_YD = 10; // altezza dei due pezzi (la bussola e il vento stanno in basso a destra)
  function rqAggiorna(){ // a ogni passo: quando cambia l'insieme delle bandiere, e quando un debito di giri si chiude
    const k = bandiereTesto(bandiereR()); if (k !== R.rqKey){ R.rqKey = k; R.rqT = R.t; }
    const deb = R.need > R.done; if (R.rqDeb && !deb) R.rqScont = R.t; R.rqDeb = deb;
  }
  function rqDati(){ // { flag, senso (riga di significato o null), righe: [[testo, colore, peso, px]], lampo }; flag vuoto = niente pezzo di sinistra, righe vuote = niente pezzo di destra; null se non si vede nulla
    const me = R.boats[0], f = bandiereR(), flag = ["classe", "P", "X", "blu"].filter(k => f[k]), righe = [];
    const recente = R.rqT != null && R.t - R.rqT < RQ_PERM, deb = R.need > R.done, scont = R.rqScont != null && R.t - R.rqScont < RQ_SCONTATA;
    const oltre = opt.hint && R.t < 0 && me.fin === null && toWF(me.S.x, me.S.y)[1] <= 0;
    if (f.X) righe.push([me.ocs ? "X: torna dietro la linea" : "X: richiamo per altre barche", "#FFD447", 700, 14]);
    if (deb){
      const m = R.need - R.done;
      righe.push(["Penalità: " + m + (m === 1 ? " giro" : " giri") + " da fare" + (R.done ? " · fatti " + R.done : ""), "#FFFFFF", 700, 14]);
      if (R.rqMotivo) righe.push(["Per: " + R.rqMotivo, "rgba(255,255,255,.75)", 600, 12]);
      if (me.sconta) righe.push(["Stai scontando: lascia strada", "rgba(255,255,255,.75)", 600, 12]);
    } else if (scont) righe.push(["Penalità scontata", "#7FD6A8", 700, 14]);
    if (oltre) righe.push(["Oltre la linea: torna dietro", "#FFD447", 700, 14]);
    const vediF = flag.length && (recente || f.X);
    if (!vediF && !righe.length) return null;
    const senso = vediF ? (f.blu ? "Partito: la linea ora è d'arrivo" : f.P ? "Preparatorio: bandiera P alzata" : R.t >= -60 ? (R.cd >= 180 ? "Un minuto: la P è ammainata" : "Un minuto: resta la bandiera di classe") : "Avviso: bandiera di classe alzata") : null;
    return { flag: vediF ? flag : [], senso, righe, lampo: R.rqT != null && R.t - R.rqT < RQ_LAMPO };
  }
  function rqLarg(t, px, peso){ // la larghezza di un testo si misura una volta sola (e di nuovo quando i caratteri sono pronti)
    const k = (fontsOk ? "1" : "0") + peso + "|" + px + "|" + t; let w = rqMis.get(k);
    if (w === undefined){ ctx.font = font(peso, px); w = ctx.measureText(t).width; rqMis.set(k, w); }
    return w;
  }
  function rqSfondo(x, y, w, h, lampo){
    ctx.fillStyle = "rgba(10,24,36,.78)"; ctx.fillRect(x, y, w, h);
    ctx.lineWidth = lampo ? 3 : 1; ctx.strokeStyle = lampo ? "#FFD447" : "rgba(255,255,255,.4)"; ctx.strokeRect(x, y, w, h);
  }
  function drawRiquadro(){
    R.rqRect = null; R.rqRect2 = null; if (!R.segnali) return;
    const d = rqDati(); if (!d) return;
    const gap = 10, pad = 10; ctx.save(); ctx.textBaseline = "middle"; ctx.textAlign = "left";
    const nf = d.flag.length;
    if (nf){ // sinistra: le bandiere con il nome sotto e la riga di significato
      const fw = nf * RQ_BW + (nf - 1) * gap, w = Math.max(fw, rqLarg(d.senso, 13, 600)) + 2 * pad, h = 2 * pad + RQ_BH + 18 + 21;
      const y0 = RQ_YS; rqSfondo(RQ_X, y0, w, h, d.lampo);
      ctx.lineWidth = 1; ctx.strokeStyle = "#33414A";
      d.flag.forEach((k, i) => drawBandiera(k, RQ_X + pad + i * (RQ_BW + gap) + RQ_BW / 2, y0 + pad + RQ_BH / 2, RQ_BW, RQ_BH));
      ctx.font = font(600, 12); ctx.fillStyle = "rgba(255,255,255,.85)"; ctx.textAlign = "center";
      d.flag.forEach((k, i) => ctx.fillText(RQ_NOMI[k], RQ_X + pad + i * (RQ_BW + gap) + RQ_BW / 2, y0 + pad + RQ_BH + 9));
      ctx.textAlign = "left"; ctx.font = font(600, 13); ctx.fillStyle = "rgba(255,255,255,.9)"; ctx.fillText(d.senso, RQ_X + pad, y0 + pad + RQ_BH + 18 + 10);
      R.rqRect = [RQ_X, y0, w, h];
    }
    if (d.righe.length){ // destra: X, penalità, avviso
      let w = 0, h = 2 * pad; for (const [t, , peso, px] of d.righe){ w = Math.max(w, rqLarg(t, px, peso)); h += px + 8; }
      w += 2 * pad; const x = W - 16 - w, y0 = RQ_YD; rqSfondo(x, y0, w, h, false);
      let y = y0 + pad; for (const [t, col, peso, px] of d.righe){ ctx.font = font(peso, px); ctx.fillStyle = col; ctx.fillText(t, x + pad, y + (px + 8) / 2); y += px + 8; }
      R.rqRect2 = [x, y0, w, h];
    }
    ctx.restore();
  }

  // ---- svolgimento: updateRace, arrivo del giocatore e record ----
  function updateRace(dt){
    if (!R) return;
    const prevT = R.t; R.t += dt;
    if (R.segnali) rqAggiorna();
    // segnali di partenza (versione accorciata a un minuto)
    const sig = (at, text) => { if (prevT < at && R.t >= at && !R.signals.has(at)){ R.signals.add(at); toast(text); } };
    if (R.segnali){ // 1.0.65: i messaggi seguono le bandiere (le soglie con <=, perché il primo passo parte esattamente dal tempo dell'avviso)
      const sigB = (at, text) => { if (prevT <= at && R.t >= at && !R.signals.has(at)){ R.signals.add(at); toast(text); } };
      if (R.cd >= 180){
        sigB(-R.cd, "Avviso: alzata la bandiera di classe, partenza tra " + Math.round(R.cd / 60) + " minuti");
        sigB(-(R.cd - 60), "Preparatorio: alzata la bandiera P");
        sigB(-60, "Un minuto: ammainata la P");
      } else sigB(-R.cd, "Un minuto: resta la bandiera di classe, partenza tra un minuto");
    } else {
    sig(-opt.countdown, "Segnale di avviso: partenza tra " + Math.round(opt.countdown / 60) + (opt.countdown >= 120 ? " minuti" : " minuto"));
    if (opt.countdown > 60) sig(-60, "Un minuto");
    }
    sig(-30, "30 secondi");
    sig(-10, "10 secondi");
    if (prevT < 0 && R.t >= 0){
      R.phase = "race";
      for (const b of R.boats){ const wy = toWF(b.S.x, b.S.y)[1]; if (wy <= 0) b.ocs = true; }
      if (R.boats[0].ocs) regAdd("ocs");
      if (R.segnali) R.xSet = R.boats.filter(b => b.ocs); // richiamo individuale: la X sale per queste barche
      // 0.21.5: richiamo individuale anche per gli avversari (regola 29.1 del regolamento di regata: chi è oltre la linea allo sparo
      // deve tornare dietro e ripartire, e il ritorno è la penalità). Prima il messaggio parlava solo del giocatore
      const ant = R.boats.filter(b => !b.me && b.ocs).map(b => b.name), chi = ant.length > 1 ? ant.slice(0, -1).join(", ") + " e " + ant[ant.length - 1] : ant[0];
      if (R.boats[0].ocs) toast("Partenza anticipata! Torna dietro la linea" + (ant.length ? " (anche " + chi + ")" : ""), ant.length ? 4.5 : 2.6);
      else toast(ant.length ? "Partenza! Richiamo individuale: " + chi + (ant.length > 1 ? " devono" : " deve") + " tornare dietro la linea" : "Partenza!", ant.length ? 4.5 : 2.6);
    }
    for (const b of R.boats){ if (!b.me) stepAI(b, dt); raceLegs(b); }
    if (R.lv2) aggiornaVirate();
    contacts();
    if (R.giri){ boeToccate(); giriPenalita(); }
    if (R.lv2) semaforo();
    if (R.t >= 0 && Math.floor(R.t * 2) !== Math.floor(prevT * 2)) for (const b of R.boats){ // strada fatta ogni 0,5 s, per i distacchi
      const p = b.fin === null ? strada(b) : null; if (p !== null) (b.hist = b.hist || []).push([R.t, p]); }
    recSample(R.t, dt); rivCapture(R.t, dt);
    const me = R.boats[0];
    if (R.tor) torFinestra();
    if (R.tor && (me.fin !== null || me.dnf) && R.phase !== "done"){ R.phase = "done"; R.doneAt = R.t; torArrivo(); }
    if (me.fin !== null && R.phase !== "done") salvaArrivo(me);
    if (R.pend && (R.boats.every(b => b.fin !== null) || R.t >= me.fin)) salvaPiazzamento(me);
  }
  function salvaArrivo(me){ // il giocatore ha tagliato l'arrivo: record, regata fatta, risultato a schermo
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
  function salvaPiazzamento(me){
    const v = { pos: ranking().indexOf(me) + 1, n: R.boats.length, pulita: R.pend.pulita };
    const pts = r => 5 - r.pos + (r.pulita ? 1 : 0); // 4/3/2/1 più 1 senza errori; ponytail: vale per 4 barche, da rivedere se la flotta cambia
    progress.race = progress.race || {};
    const old = progress.race[R.pend.key];
    if (!old || pts(v) > pts(old)){ progress.race[R.pend.key] = v; saveProgress(); }
    R.pend = null;
  }
  // ---- distacchi e classifica ----
  // 1.0.33: distacchi in secondi (docs/archivio/PROPOSTA-DISTACCHI.md). Strada fatta in metri, nella direzione del vento medio (lo spostamento
  // di lato non conta, come nel tracciamento delle regate vere): di bolina i metri saliti dalla linea (al più R.up), in poppa R.up più
  // i metri scesi dalla boa; null prima della partenza (o richiamata). Prima della conferma era la distanza in linea d'aria da boa e
  // centro della linea: chi tagliava l'arrivo a 15 m dal centro sembrava indietro. Ogni barca se la ricorda ogni 0,5 s; il distacco è
  // da quanti secondi la barca davanti aveva la strada che ho fatto io: un tempo vero, senza le penalità.
  function strada(b){
    if (b.fin !== null) return (R.tri ? 3 : 2) * R.up;
    if (b.leg === 0 || b.ocs) return null;
    if (R.tri) return stradaTri(b);
    const wy = toWF(b.S.x, b.S.y)[1];
    return b.leg === 1 ? Math.min(R.up, -wy) : 2 * R.up + Math.min(0, wy);
  }
  // sul triangolo (1.0.55) la strada si misura lungo il lato, da 0 a L: la direzione del vento ne vedrebbe la metà sui lati al lasco (§8.7 punto 5).
  // L'ultimo lato no: la linea d'arrivo è orizzontale e il lato la taglia a 30°, quindi la proiezione sul lato arrivava a L fino a 8 s prima del traguardo
  // (D1 sul triangolo: 5 regate su 13 entro 3 s); lì conta la strada che manca alla linea in direzione del vento, portata a L (la linea vale esattamente L)
  function stradaTri(b){
    const [wx, wy] = toWF(b.S.x, b.S.y), L = R.up, c = 0.866, lato = [[0, 0, 0, -1], [0, -L, -c, 0.5]][b.leg - 1];
    if (b.leg === 3) return 2 * L + clamp(L + 2 * wy, 0, L);
    return (b.leg - 1) * L + clamp((wx - lato[0]) * lato[2] + (wy - lato[1]) * lato[3], 0, L);
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
    if (b.leg >= 1 && b.leg <= R.marks.length && b.rnd < 0) return "boa girata dal lato sbagliato";
    return (R.tri ? ["prima della partenza", "di bolina", "verso la boa 2", "verso l'arrivo"] : ["prima della partenza", "di bolina", "verso l'arrivo"])[b.leg];
  }
  function racePanel(){
    if (!R) return;
    const rank = ranking();
    const gap = b => { const s = distacco(b); if (s === null) return ""; const r = Math.round(s); return " · " + (r > 0 ? r + " s avanti" : r < 0 ? -r + " s dietro" : "alla pari"); }; // 1.0.33; 1.0.54: in parole invece del segno (check di Ale)
    $("standings").innerHTML = rank.map(b => `<li class="${b.me ? "me" : ""}"><b>${b.name}</b> <span>${legName(b)}${b.pen ? " · " + b.pen / 15 + " penalità (+" + b.pen + " s)" : ""}${b.pp ? " · " + b.pp + " penalità (+" + b.pp + " pt)" : ""}${gap(b)}</span></li>`).join("");
    $("rRule").hidden = !R.lastRule; $("rRule").textContent = R.lastRule || "";
    finShow();
  }
  // ---- schermata finale (1.0.36, docs/archivio/PROPOSTA-SCHERMATA-FINALE.md) ----
  // A regata finita il riepilogo e la classifica passano dal pannello a un riquadro sopra il mare: il pannello non sfora più.
  // I riquadri #rDone e #standings restano compilati (i collaudi li leggono), solo nascosti dalla classe .fin.
  function finShow(){
    const on = R.phase === "done" && !$("rDone").hidden;
    document.querySelector(".panel").classList.toggle("fin", on);
    if (!on) return void ($("finOv").hidden = true);
    $("finText").textContent = $("rDoneText").textContent; $("finList").innerHTML = $("standings").innerHTML;
    $("finPen").hidden = !R.penList.length; $("finPen").innerHTML = R.penList.length ? "<b>Penalità</b><br>" + R.penList.join("<br>") : ""; // 1.0.49: tutte le penalità col motivo (richiesta di Ale)
    $("finTor").hidden = $("rTor").hidden; $("finRev").hidden = !rivCount(); $("finRestart").hidden = $("rRestart").hidden;
    if ($("finOv").hidden){ $("finOv").hidden = false; releaseKeys(); setTimeout(() => (!$("finRestart").hidden ? $("finRestart") : $("finTor")).focus(), 0); }
  }
  $("finRestart").onclick = () => $("rRestart").click(); $("finTor").onclick = () => $("rTor").click();

  // ---- torneo dell'1b (1.0.34, tappa T1 di docs/PROPOSTA-TORNEI-1B.md) ----
  // Serie di 4 regate (1 e 3 a bastone, 2 e 4 a triangolo dalla 1.0.55) con la barca dell'1b contro gli stessi tre avversari, con lo stesso carattere. Punteggio di F15,
  // appendice A: punti bassi (A4), chi non arriva o si ritira prende iscritti + 1 (A5.2), uno scarto (A2.1) dopo la quarta regata,
  // parità con A8; un contatto con colpa è una penalità sul punteggio (44.3(c)), non 15 s. Finestra d'arrivo (appendice S, 12.3):
  // chi non arriva entro TOR_FIN volte il tempo della prima non arriva. Il torneo si salva in progress.torneo dopo ogni regata;
  // la regata lasciata a metà (pagina chiusa, menu) vale come ritiro (1.0.50). Le altre regate restano con i 15 s.
  const TOR_N = 4, TOR_FIN = 0.5; // TOR_FIN: ipotesi nostra, la finestra la scrivono le istruzioni di regata
  const TOR_COND = [{ nome: "10 nodi costanti", tws: 10, gusts: 0 }, { nome: "raffiche", tws: 12, gusts: 1 }, { nome: "salti di vento", tws: 10, gusts: 0, shifts: true }];
  let tor = null; // il torneo in corso: lo stesso oggetto di progress.torneo
  const torTri = k => k % 2 === 1; // percorsi misti (1.0.55, DECISIONI 27 ottobre 2026): dipende solo dal numero della regata, nessun numero a caso in più
  const torNome = k => "regata " + (k + 1) + " di " + TOR_N + " (" + TOR_COND[tor.regate[k].c].nome + (torTri(k) ? ", triangolo" : "") + ")";
  const fmtPt = v => String(Math.round(v * 10) / 10).replace(".", ",");
  function torNuovo(){
    const liv = opt.aiLevel === "nessuno" ? "principianti" : opt.aiLevel, aggro = sorteggiaAggressiva(liv);
    return { ver: VERSIONE, liv, regate: [0, 1, 2, Math.floor(Math.random() * 3)].map(c => ({ c, wind: Math.floor(Math.random() * 8) * 45 })), // la quarta sorteggiata fra le tre
             av: FLEET_LOOK.map((l, k) => ({ ai: aiParams(liv), char: carattere(k, aggro) })), ris: [] };
  }
  function torRc(){
    const k = tor.ris.length, g = tor.regate[k], c = TOR_COND[g.c];
    return { title: "Torneo, regata " + (k + 1) + " di " + TOR_N, wind: g.wind, tws: c.tws, gusts: c.gusts, shifts: c.shifts, lv2: true, tor: true, tri: torTri(k), up: torTri(k) ? TRI_L : undefined };
  }
  const torBrief = () => "Torneo dell'1b, " + torNome(tor.ris.length) + ", con la barca completa dell'1b. Punti: 1 al primo, 2 al secondo e così via; chi non arriva o si ritira ne prende " +
    (FLEET_LOOK.length + 2) + ". Un contatto con colpa vale 1 punto in più in questa regata invece dei 15 s (penalità sul punteggio, regola 44.3). Chi non arriva entro metà del tempo della prima, contato dal suo arrivo, non si classifica. ";
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
  // 1.0.50: lasciare la regata a metà (menu, pagina chiusa) è un ritiro, dal clic su «Corri la regata»; chi ha già finito resta com'è
  const torInCorso = () => !!(R && R.tor && tor && !R.torOk && R.phase !== "done");
  function torEsci(){
    if (!R || !R.tor || !tor || R.torOk) return;
    const me = R.boats[0];
    if (me.fin === null && !me.dnf) me.dnf = me.ret = true;
    torChiudi();
  }
  const torEsciOk = () => !torInCorso() || confirm("Uscire dalla regata? Conta come ritirata: prendi " + (R.boats.length + 1) + " punti, come chi non arriva.");
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
  function torTabella(T, nomi){ // la classifica della serie finora, come tabella
    const k = T.ris.length, cl = torSerie(T.ris);
    return `<table class="tor"><thead><tr><th></th><th>Barca</th>${T.ris.map((r, j) => `<th>R${j + 1}</th>`).join("")}<th>Totale</th></tr></thead><tbody>${cl.map((x, n) =>
        `<tr class="${x.i ? "" : "me"}"><td>${n + 1}°</td><td>${nomi[x.i]}</td>${x.p.map((v, j) => { const c = fmtPt(v) + (T.ris[j][x.i].pp ? "*" : "") + (T.ris[j][x.i].fin === null ? "°" : "");
          return `<td>${j === x.sc ? "(" + c + ")" : c}</td>`; }).join("")}<td><b>${fmtPt(x.tot)}</b></td></tr>`).join("")}</tbody></table>
        <p class="tor-leg">* penalità sul punteggio · ° non arrivata o ritirata · fra parentesi lo scarto${k < TOR_N ? ", che conta dopo la quarta regata" : ""}</p>`;
  }
  function torMostra(nota){
    const T = tor || torNuovo(), k = T.ris.length, inGioco = mode === "race";
    const nomi = ["Tu", ...FLEET_LOOK.map(l => l.name)], car = T.av.map((a, i) => "la " + FLEET_LOOK[i].name + " è " + CHAR_TEXT[a.char]).join(", ");
    const tab = k ? torTabella(T, nomi) : "";
    const fine = T.fine ? `<p class="score">${T.fine.pos}° su ${nomi.length}</p><p>${modo === "carriera" ? "Meriti di Competizione dell'1b: " + T.fine.mer + "." : "Nel gioco libero il torneo non dà meriti."}</p>` : "";
    const testa = !k ? `<p>Quattro regate, due a bastone e due a triangolo, con la barca completa dell'1b, contro gli stessi tre avversari (${T.liv}): ${car}. Vento: ${T.regate.map((g, j) => (j + 1) + ") " + TOR_COND[g.c].nome + (torTri(j) ? " (triangolo)" : " (bastone)")).join(", ")}.</p>
      <p>Punti come nel regolamento di regata: 1 al primo, 2 al secondo e così via, ${nomi.length + 1} a chi non arriva o si ritira; dopo la quarta regata la peggiore si scarta. Vince chi ha meno punti. Un contatto con colpa vale 1 punto in più nella regata. Il torneo si salva dopo ogni regata: se esci o chiudi la pagina a regata iniziata, quella regata vale come ritirata.</p>`
      : T.fine ? "" : `<p>Prossima: ${torNome(k)}.</p>`;
    $("torBody").innerHTML = `<div class="qz-top"><h2 id="torTitle">Torneo dell'1b</h2><span>${T.fine ? "finito" : k ? "dopo la regata " + k + " di " + TOR_N : ""}</span></div>
      ${nota ? `<p class="manca">${nota}</p>` : ""}${fine}${testa}${tab}
      <div class="row">${T.fine ? `<button class="primary" id="torMenu">Torna al menu</button>`
        : `<button class="primary" id="torGo">${k ? "Corri la regata " + (k + 1) : "Inizia il torneo"}</button>${tor ? `<button id="torRit">Ritirati dal torneo</button>` : ""}<button id="torMenu">${inGioco ? "Menu" : "Chiudi"}</button>`}</div>`;
    const chiudi = () => $("torDlg").close();
    $("torMenu").onclick = () => { if (inGioco && !torEsciOk()) return; chiudi(); if (T.fine) tor = null; if (inGioco || T.fine) showMenu(); };
    if ($("torGo")) $("torGo").onclick = () => { if (!tor){ tor = progress.torneo = T; saveProgress(); } chiudi(); openItem(["r", "t"]); };
    if ($("torRit")) $("torRit").onclick = () => { if (!confirm("Ritirarti dal torneo? Il torneo non conta: niente punti e niente piazzamento.")) return;
      delete progress.torneo; tor = null; saveProgress(); chiudi(); showMenu(); };
    releaseKeys(); $("torDlg").showModal();
  }
  $("rTor").onclick = () => { torChiudi(); torMostra(); };
  $("rRet").onclick = () => { const me = R && R.boats[0];
    if (!me || !R.tor || R.phase === "done" || !confirm("Ritirarti da questa regata? Prendi " + (R.boats.length + 1) + " punti, come chi non arriva.")) return;
    me.dnf = me.ret = true; };

  // ---- disegno della regata ----
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
    if (R.segnali) drawBandiere(v.ppm);
    else { ctx.fillStyle = R.t < 0 ? "#F2C14E" : "#2B5DB8"; ctx.fillRect(0.2, -3.2, 1.2, 0.8); }
    ctx.restore();
    // boa di bolina; sul triangolo due boe, e quella da girare ora ha un anello
    const next = R.tri ? R.boats[0].leg : 0;
    R.marks.forEach((mk, k) => {
      ctx.fillStyle = "#F2D43C"; ctx.beginPath(); ctx.arc(mk.x, mk.y, Math.max(0.9, 3 / v.ppm), 0, Math.PI * 2); ctx.fill();
      if (next === k + 1){ ctx.strokeStyle = "rgba(255,255,255,.9)"; ctx.lineWidth = 0.2; ctx.beginPath(); ctx.arc(mk.x, mk.y, Math.max(1.8, 6 / v.ppm), 0, Math.PI * 2); ctx.stroke(); }
      drawRoundArrow(mk, 7, "rgba(255,226,122,.9)");
    });
    // avversari
    for (const b of R.boats){ if (b.me) continue; drawWakeOf(b.wake, b.S.u); drawOther(b.S, b.info, b.ctl.tiller, 1); }
  }
  function drawOrologio(me, rank){ // il riquadro in alto: conto alla rovescia o tempo di gara, posizione, avvisi di partenza (dentro il save/restore del chiamante)
    const pos = rank.indexOf(me) + 1;
    ctx.textBaseline = "middle";
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
    if (me.ocs){ ctx.font = font(700, 16); ctx.fillStyle = "#FFD447"; ctx.fillText(R.t < 3 ? "Partenza anticipata: torna dietro la linea" : "Non sei partito: torna dietro la linea e tagliala tra giuria e boa", W / 2, 88); }
  }
  function drawRaceScreen(v){
    if (!R) return;
    ctx.save(); ctx.font = font(700, 13); ctx.textAlign = "center"; ctx.textBaseline = "middle";
    for (const b of R.boats){ if (b.me) continue; const [sx, sy] = toScreen(v, b.S.x, b.S.y); ctx.fillStyle = "rgba(10,24,36,.6)"; const w = ctx.measureText(b.name).width + 10; ctx.fillRect(sx - w / 2, sy - 58, w, 18); ctx.fillStyle = b.S.sailorColor; ctx.fillText(b.name, sx, sy - 49); }
    R.marks.forEach((mk, k) => { const [gx, gy] = toScreen(v, mk.x, mk.y); ctx.fillStyle = "#fff"; ctx.textAlign = "left"; ctx.fillText(R.tri ? "Boa " + (k + 1) + " · lasciala a sinistra" : "Boa di bolina · lasciala a sinistra", gx + 10, gy - 10); });
    drawOrologio(R.boats[0], ranking());
    ctx.restore();
    drawRiquadro();
    const g = goal(); // dopo l'arrivo niente freccia
    if (g) offscreenArrow(v, g);
    linePill(v, R.pin, R.cb, R.t < 0 ? "Linea di partenza" : "Arrivo", g && g.kind !== "mark" ? g : null, 0, 4);
  }
  // ---- aiuti a schermo e fantasma (valgono in tutte le modalità) ----
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

