// Scuola di vela, disegno.js — Pannello laterale e disegno del mare, della barca e degli strumenti.
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/PROPOSTA-DIVISIONE-CODICE.md.
  // ======================================================================
  // PANNELLO
  // ======================================================================
  function panel(){
    const st = curStep(), I = readI();
    $("iSpd").textContent = (S.u * KN).toFixed(1) + " kn";
    $("iAnd").textContent = S.capsized ? "—" : andName(I.twa);
    $("iTw").textContent = Math.round(I.twa) + "° · " + (local.tws * KN).toFixed(0) + " kn";
    $("iAw").textContent = Math.round(Math.abs(info.awa)) + "° · " + (info.aws * KN).toFixed(1) + " kn";
    $("iHdg").textContent = deg3(S.h);
    const mk = mode === "free" ? curMarks[0] : goal(); // navigazione libera: boa 1, come prima della 0.19.2
    $("iBrg").textContent = mode === "lesson" || !mk ? "—" : deg3(bearingTo(S, mk));
    const kq = $("kQ"); kq.hidden = !viewOn(); // «Q vista» nella legenda solo se la riga non si taglia, altrimenti sul mare
    if (!kq.hidden && kq.parentNode.scrollWidth > kq.parentNode.clientWidth) kq.hidden = true;
    qOnSea = viewOn() && kq.hidden;
    $("iHeel").textContent = S.capsized ? "scuffia" : Math.round(Math.abs(S.heel)) + "°";
    $("iLee").textContent = Math.abs(info.leeway || 0).toFixed(0) + "°";
    const t = ctl.tiller;
    $("vTil").textContent = Math.abs(t) < 0.03 ? "al centro" : (t < 0 ? "a sinistra " : "a dritta ") + Math.round(Math.abs(t) * 100) + "%";
    $("vSh").textContent = "boma a " + Math.round(S.boom) + "°";
    if (!dragTiller) $("tiller").value = Math.round(ctl.tiller * 100);
    $("sheet").value = Math.round(ctl.sheet * 100);
    const noRight = !!(st && st.noRight); // lezione 6, «La scuffia»: niente raddrizzamento finché non si passa al passo dopo
    $("rightBtn").hidden = !S.capsized || S.righting > 0 || noRight;
    $("capOverlay").hidden = !S.capsized || S.righting > 0 || noRight;
    $("capText").textContent = S.capCause === "gybe"
      ? "Hai scuffiato per una strambata: il vento è passato dall'altro lato con la vela tutta aperta e il boma ha attraversato la barca di colpo. Per strambare senza rischi: prima cazza, poi poggia, poi lasca (lezione 5)."
      : "Hai scuffiato: la barca è rovesciata e i comandi non rispondono finché non la raddrizzi.";
    // suggerimento
    const kind = st ? (st.hintKind || "sail") : "tt";
    let cls = "good", msg = "";
    const ttMsg = { flog: ["bad", "Troppo vicino al vento: la vela sbatte. Poggia."], wind: ["bad", "Si agita il filetto sopravento: cazza, oppure poggia."],
                    lee: ["bad", "Si agita il filetto sottovento: lasca, oppure orza."], ok: ["good", "Filetti dritti: vela regolata."] }[I.tt];
    const sailMsg = { flog: ["bad", "La vela sbatte: sei nell'angolo morto."], wind: ["bad", "La vela sbatte: è troppo lascata."],
                      lee: ["bad", "La vela è in stallo: troppo cazzata."], ok: ["good", "Vela gonfia e regolata."] }[I.tt];
    [cls, msg] = kind === "sail" ? sailMsg : ttMsg;
    // oltre circa 112° di vento apparente nessuna posizione della randa dà i filetti dritti (boma al massimo a BOAT.maxBoom):
    // a scotta tutta lascata «lasca» e «troppo cazzata» sarebbero consigli sbagliati, e in poppa i filetti non si usano.
    if (I.tt === "lee" && I.sheet > 0.99){ cls = "good"; msg = "Vento da dietro: la vela è già tutta aperta. In poppa i filetti non servono."; }
    const to = (env.twd + 180) * D2R, ahead = windAt(S.x - Math.sin(to) * 22, S.y + Math.cos(to) * 22);
    let back = false; // 0.20.2: «all'indietro» si mostra anche nei passi a suggerimenti spenti, se il passo dà la barra
    if (S.capsized && noRight){ cls = "good"; msg = "Hai scuffiato: la barca resta rovesciata. Premi Avanti: nel passo dopo la raddrizzi."; }
    else if (S.capsized){ cls = "bad"; msg = S.righting ? "Stai raddrizzando la barca…" : (S.capCause === "gybe" ? "Hai scuffiato per una strambata con la vela aperta: il boma ha attraversato la barca di colpo. Premi Raddrizza (o A)." : "Hai scuffiato! Premi Raddrizza (o A)."); }
    // 1.0.9: dal traverso in giù (oltre 75°, confine fra bolina larga e traverso) in raffica si poggia, non si orza (docs/PROPOSTA-RAFFICHE-PORTANTI.md)
    else if (S.pushing){ cls = ""; msg = "Boma spinto: la barca va all'indietro e la prua gira verso il boma. Al traverso molla Z, centra la barra e cazza."; }
    else if (S.stall){ cls = "bad"; msg = "La pala del timone è in stallo: l'acqua non la segue più e la barca frena. Muovi la barra più dolcemente."; }
    else if (S.heel > 25){ cls = "bad"; const bol = I.twa < 75;
      msg = I.sheet > 0.99 ? "Sbandi troppo e la vela è già tutta lasca: " + (bol ? "prova a orzare un poco." : "poggia un poco.") : "Sbandi troppo: lasca la scotta" + (bol ? ", oppure orza di poco." : " e poggia un poco."); }
    else if (S.heel < -15){ cls = "bad"; msg = "La barca sbanda verso di te: il vento è calato. Cazza un po' o poggia."; }
    // 0.20.2, fasi di backCheck(): sotto IRONS_A (40°) la barra verso il boma, poi barra al centro e cazzare, poi lasciar prendere velocità
    else if (S.indietro === 1){ back = true; cls = "bad"; msg = "All'indietro la barra funziona al contrario: spostala verso il boma, poi centrala e cazza."; }
    else if (S.indietro === 2){ back = true; cls = "bad"; msg = "Stai andando all'indietro, ma la prua è fuori dall'angolo morto: centra la barra e cazza."; }
    else if (S.indietro === 3 && I.twa >= IRONS_A - 3){ back = true; cls = ""; msg = "Ora vai avanti piano: barra al centro, cazza e lascia prendere velocità."; }
    else if (gustLevel && ahead.tws > local.tws * 1.2){ cls = ""; msg = "Raffica in arrivo: sfruttala per accelerare. " + (I.twa < 75 ? "Se sbandi troppo, lasca o orza un poco." : I.twa < 135 ? "Se sbandi troppo, poggia e lasca un poco." : "Se poggi troppo rischi la strambata."); } // cls vuoto: colore normale del testo, non è un allarme
    if (mode === "lesson" && st.course && !S.capsized){
      const off = norm180(S.h - S.course);
      cls = Math.abs(off) < 6 ? "good" : "bad";
      msg = "Rotta da tenere " + deg3(S.course) + ", ora " + deg3(S.h) + (Math.abs(off) < 6 ? ": in rotta." : off > 0 ? ": la prua è troppo a dritta." : ": la prua è troppo a sinistra.");
    }
    if (mode === "lesson" && st.turnHint && !S.capsized && S.u > -0.05 && S.heel <= 25 && Math.abs(S.r) > 3){
      const a = norm180(local.twd - S.h), orza = Math.sign(a) === Math.sign(S.r);
      cls = "good"; msg = orza ? "Stai orzando: la prua va verso il vento." : "Stai poggiando: la prua si allontana dal vento.";
    }
    if (mode === "lesson" && kind === "none" && !S.capsized && !(back && st.tiller)) { $("hint").hidden = true; }
    else if (mode === "lesson" && !st.pause && st.hud) $("hint").hidden = false;
    // 1.0.2: a passo completato il suggerimento ripete quello che dice il testo di fine passo, e a 1360x650 il pannello non ci sta:
    // si nasconde, tranne se la barca è rovesciata, sbanda oltre 25° o arretra, o se il passo ha i pulsanti Cazza e Lasca (spostarli sotto il puntatore è il difetto della 0.18.1)
    if (mode === "lesson" && stepDone && !(st.sem && st.sem.length) && !S.capsized && S.heel <= 25 && !back) $("hint").hidden = true;
    $("hint").className = "hint " + cls; $("hint").textContent = msg;
    if (mode === "race") racePanel();
    if (mode === "mission" || mode === "race") regShow($("stErr"));
    if (mode === "lesson"){ $("lErr").hidden = !!st.pause; regShow($("lErr")); }
    if (mode === "mission"){
      const prev = progress.best[recK("m" + missionIdx)];
      const bd = MISSIONS[missionIdx].bands, k = bd.findIndex(v => S.time <= v);
      $("stClock").innerHTML = "Tempo " + fmtClock(S.time) + (prev ? " <span>· record " + fmtClock(prev) + "</span>" : "") +
        (k >= 0 && !S.finished ? " <span>· " + MEDALS[k] + " entro " + fmtClock(bd[k]) + "</span>" : "");
    }
  }

  // ======================================================================
  // DISEGNO
  // ======================================================================
  let W = 0, H = 0, dpr = 1, colors = {};
  function readColors(){
    const cs = getComputedStyle(document.documentElement);
    ["sea-a","sea-b","ripple","foam","hull","hull-edge","cockpit","sail","sail-shade","spar","sailor","tt-port","tt-stbd","true","app","label","accent","moto"]
      .forEach(k => colors[k] = cs.getPropertyValue("--" + k).trim());
  }
  readColors();
  try { matchMedia("(prefers-color-scheme: dark)").addEventListener("change", readColors); } catch(e){}
  function resize(){ const r = canvas.getBoundingClientRect(); dpr = Math.min(2, devicePixelRatio || 1); W = r.width; H = r.height; canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr); }
  addEventListener("resize", resize);
  const hash = (i, j, k) => { let n = i * 374761393 + j * 668265263 + k * 2147483647; n = (n ^ (n >> 13)) * 1274126177; return ((n ^ (n >> 16)) >>> 0) / 4294967295; };
  let rippleOff = [0, 0], ripplePh = [0, 0], wakeT = 0; // ripplePh: sfasamento del secondo strato dentro le raffiche (1.0.19)
  // ---- vista e telecamera ----
  // tasto vista (Q tenuto), «vista del percorso»: sposta la barca sullo schermo dalla parte opposta all'obiettivo e, se serve, allontana
  // l'inquadratura finché barca e obiettivo stanno sullo schermo con un margine (mai sotto ZMIN). Solo disegno: fisica e tempo non lo leggono.
  // Ipotesi nostre: 60% della mezza larghezza e della mezza altezza, barca fra il 20% e l'80% dello schermo, spostamento in circa 0,25 s,
  // allontanamento in circa 0,4 s (VIEW_ZK), margine VIEW_M px. Al rilascio tutto torna com'era: userZoom non si tocca.
  // Una futura vista tattica con pausa (livello 4) sarebbe una condizione in più in «paused» nel ciclo.
  const VIEW_SHIFT = 0.6, VIEW_K = 12, VIEW_ZK = 7.5, VIEW_M = 50; // VIEW_K, VIEW_ZK: 1/s, al 95% in 0,25 s e in 0,4 s
  let zoomQ = 1; // fattore di zoom del tasto vista (1 = nessun effetto)
  const RIP_Z0 = 0.35, RIP_Z1 = 0.5; // dissolvenza delle increspature fra questi due zoom (ipotesi nostra)
  let viewOff = [0, 0], qOnSea = false, fontsOk = false, rippleCells = 0;
  Promise.all(["600", "700"].map(w => document.fonts.load(w + ' 14px "Barlow Semi Condensed"'))).catch(() => {}).then(() => fontsOk = true);
  const font = (w, px) => `${w} ${px}px "Barlow Semi Condensed", sans-serif`; // caratteri del disegno sul mare
  const viewOn = () => mode === "mission" || mode === "race";
  function view(){
    const ppm = Math.min(W, H) / 48 * camZoom * zoomQ;
    const rot = opt.view === "prua" ? -S.h * D2R : 0;
    return { ppm, rot, cx: W / 2 + viewOff[0], cy: H * (opt.view === "prua" ? 0.6 : 0.5) + viewOff[1] };
  }
  function viewUpdate(dt){
    const v = { ...view(), cx: W / 2, cy: H * (opt.view === "prua" ? 0.6 : 0.5) }, g = viewOn() && keys.has("q") ? goal() : null;
    let tx = 0, ty = 0, tz = 1;
    if (g){
      const [gx, gy] = toScreen(v, g.x, g.y), dx = (gx - v.cx) / zoomQ, dy = (gy - v.cy) / zoomQ, d = Math.hypot(dx, dy); // dx, dy: senza l'effetto del tasto
      if (d > 1){
        const bx = clamp(v.cx - dx / d * VIEW_SHIFT * W / 2, 0.2 * W, 0.8 * W), by = clamp(v.cy - dy / d * VIEW_SHIFT * H / 2, 0.2 * H, 0.8 * H);
        tx = bx - v.cx; ty = by - v.cy;
        // fattore che porta l'obiettivo dentro lo schermo, a VIEW_M px dal bordo, con la barca nella posizione spostata
        const lim = (b, q, size) => q > 0 ? (size - VIEW_M - b) / q : q < 0 ? (b - VIEW_M) / -q : Infinity;
        tz = clamp(Math.min(1, lim(bx, dx, W), lim(by, dy, H)), ZMIN / camZoom, 1);
      }
    }
    const a = 1 - Math.exp(-VIEW_K * dt);
    viewOff[0] += (tx - viewOff[0]) * a; viewOff[1] += (ty - viewOff[1]) * a;
    zoomQ += (tz - zoomQ) * (1 - Math.exp(-VIEW_ZK * dt));
  }
  function toScreen(v, x, y){
    const dx = (x - S.x) * v.ppm, dy = (y - S.y) * v.ppm, c = Math.cos(v.rot), s = Math.sin(v.rot);
    return [v.cx + dx * c - dy * s, v.cy + dx * s + dy * c];
  }
  function localToWorld(lx, ly){ const h = S.h * D2R, c = Math.cos(h), s = Math.sin(h); return [S.x + lx * c - ly * s, S.y + lx * s + ly * c]; }

  // ---- quadro principale ----
  function draw(dt){
    const st = curStep();
    camZoom += ((st && st.zoom ? st.zoom : 1) * userZoom - camZoom) * Math.min(1, dt * 3);
    viewUpdate(dt);
    const v = view();
    const sh = S.shake > 0 ? S.shake * 14 : 0;
    ctx.setTransform(dpr, 0, 0, dpr, (Math.random() - 0.5) * sh * dpr, (Math.random() - 0.5) * sh * dpr);
    const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, colors["sea-a"]); g.addColorStop(1, colors["sea-b"]);
    ctx.fillStyle = g; ctx.fillRect(-20, -20, W + 40, H + 40);

    ctx.save();
    ctx.translate(v.cx, v.cy); ctx.rotate(v.rot); ctx.scale(v.ppm, v.ppm); ctx.translate(-S.x, -S.y);
    // increspature
    const to = (env.twd + 180) * D2R, wx = Math.sin(to), wy = -Math.cos(to);
    rippleOff[0] += wx * env.tws * 0.35 * dt; rippleOff[1] += wy * env.tws * 0.35 * dt;
    // 1.0.19 (docs/PROPOSTA-INCRESPATURE.md): dentro le chiazze un secondo strato di trattini, più fitti e con uno scorrimento proprio,
    // quello del vento della raffica più forte in acqua. Lo sfasamento sta dentro una cella, così i trattini restano sullo schermo.
    let kMax = 0; for (const gg of gusts) kMax = Math.max(kMax, gg.k * gg.life);
    ripplePh[0] = (ripplePh[0] + wx * env.tws * kMax * 0.35 * dt) % 7; ripplePh[1] = (ripplePh[1] + wy * env.tws * kMax * 0.35 * dt) % 7;
    // attorno al centro dello schermo (non alla barca): con la barca spostata (prua in alto, tasto vista) le celle restano le stesse
    const cell = 7, R = Math.hypot(W, H) / v.ppm / 2 + cell, sdx = W / 2 - v.cx, sdy = H / 2 - v.cy, vc = Math.cos(v.rot), vs = Math.sin(v.rot);
    const mx = S.x + (sdx * vc + sdy * vs) / v.ppm, my = S.y + (-sdx * vs + sdy * vc) / v.ppm;
    // sotto zoom 0,5 le increspature sfumano e sotto 0,35 non si disegnano (a zoom lontano sono migliaia di tratti illeggibili e rallentano)
    const ez = camZoom * zoomQ, ripA = clamp((ez - RIP_Z0) / (RIP_Z1 - RIP_Z0), 0, 1);
    ctx.strokeStyle = colors.ripple; ctx.lineCap = "round"; ctx.lineWidth = Math.max(0.04, 1.1 / v.ppm); ctx.globalAlpha = ripA;
    const x0 = Math.floor((mx - R - rippleOff[0]) / cell), x1 = Math.ceil((mx + R - rippleOff[0]) / cell);
    const y0 = Math.floor((my - R - rippleOff[1]) / cell), y1 = Math.ceil((my + R - rippleOff[1]) / cell);
    rippleCells = ripA > 0 ? (x1 - x0) * (y1 - y0) : 0;
    const px = -wy, py = wx, len = 0.35 + env.tws * 0.07;
    if (ripA > 0 && (x1 - x0) * (y1 - y0) < 2500){
      // tratti per cella da 4 a 1 allontanando (in proporzione all'area): sullo schermo la densità resta simile, e il costo non cresce
      const nk = clamp(Math.round(4 * ez * ez), 1, 4);
      for (let i = x0; i <= x1; i++) for (let j = y0; j <= y1; j++) for (let k = 0; k < nk; k++){
        const rx = (i + hash(i, j, k)) * cell + rippleOff[0], ry = (j + hash(j, i, k + 7)) * cell + rippleOff[1];
        let l = len * (0.5 + hash(i, k, j));
        const gk = gusts.length ? gustAt(rx, ry) : 0;
        if (gk > 0.04){
          l *= 1 + gk * 2;
          ctx.strokeStyle = `rgba(0,14,28,${Math.min(0.6, gk * 1.8).toFixed(3)})`;
          ctx.beginPath(); ctx.moveTo(rx - px * l + 0.6, ry - py * l + 0.4);
          ctx.quadraticCurveTo(rx + wx * l * 0.25 + 0.6, ry + wy * l * 0.25 + 0.4, rx + px * l + 0.6, ry + py * l + 0.4); ctx.stroke();
          ctx.strokeStyle = colors.ripple;
          // secondo strato: fino al doppio dei trattini nel cuore, sfumati a zero sul bordo della chiazza.
          // La forza si scala su 0,4, che è il massimo delle raffiche del gioco: con gk puro si aggiungeva un trattino solo, invisibile.
          const f = Math.min(1, gk / 0.4), extra = Math.round(nk * f);
          if (extra > 0){
            ctx.globalAlpha = ripA * f;
            for (let e = 0; e < extra; e++){
              const ex = (i + hash(i, j, k + 13 + e)) * cell + rippleOff[0] + ripplePh[0];
              const ey = (j + hash(j, i, k + 19 + e)) * cell + rippleOff[1] + ripplePh[1];
              const el = l * (0.5 + hash(i, k + e, j));
              ctx.beginPath(); ctx.moveTo(ex - px * el, ey - py * el);
              ctx.quadraticCurveTo(ex + wx * el * 0.25, ey + wy * el * 0.25, ex + px * el, ey + py * el); ctx.stroke();
            }
            ctx.globalAlpha = ripA;
          }
        }
        ctx.beginPath(); ctx.moveTo(rx - px * l, ry - py * l);
        ctx.quadraticCurveTo(rx + wx * l * 0.25, ry + wy * l * 0.25, rx + px * l, ry + py * l); ctx.stroke();
      }
    }
    ctx.globalAlpha = 1;
    // raffiche: chiazze scure a gradiente, disegnate sempre (non dipendono dalle increspature)
    for (const gg of gusts){
      ctx.save(); ctx.translate(gg.x, gg.y); ctx.rotate(to); ctx.scale(1, 1.4);
      const rg = ctx.createRadialGradient(0, 0, 0, 0, 0, gg.r);
      const a = Math.min(0.6, 0.55 * gg.life * Math.min(1.2, gg.k / 0.3));
      rg.addColorStop(0, `rgba(0,16,32,${Math.max(0, a).toFixed(3)})`); rg.addColorStop(0.65, `rgba(0,16,32,${Math.max(0, a * 0.6).toFixed(3)})`); rg.addColorStop(1, "rgba(0,16,32,0)");
      ctx.fillStyle = rg; ctx.beginPath(); ctx.arc(0, 0, gg.r, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    }
    drawWakeOf(wake, S.u, 8, 0.8); // scia
    // traccia (per le prove e il bordeggio)
    // boe
    const marks = (mode === "lesson" ? (S.lessonMark ? [S.lessonMark] : []) : curMarks);
    marks.forEach((m, i) => {
      const done = mode === "mission" ? i < S.markIdx : (mode === "lesson" && S.markReached);
      const active = mode === "mission" ? i === S.markIdx : !done;
      if (m.fin){ // linea d'arrivo: scacchi fra due boe piccole
        const ex = -m.ny * FIN_HALF, ey = m.nx * FIN_HALF;
        drawChecker({ x: m.x - ex, y: m.y - ey }, { x: m.x + ex, y: m.y + ey }, v.ppm, active ? 1 : 0.5);
        ctx.fillStyle = "#F28C1B"; for (const k of [-1, 1]){ ctx.beginPath(); ctx.arc(m.x + k * ex, m.y + k * ey, Math.max(0.7, 3 / v.ppm), 0, Math.PI * 2); ctx.fill(); }
        return;
      }
      ctx.fillStyle = done ? "#8FA3AF" : "#F28C1B"; ctx.beginPath(); ctx.arc(m.x, m.y, Math.max(0.7, 3 / v.ppm), 0, Math.PI * 2); ctx.fill(); // almeno 3 px di raggio
      if (active && m.round) drawRoundArrow(m, 7, "rgba(255,226,122,.9)");
      else if (active && mode !== "free"){ ctx.strokeStyle = "rgba(255,226,122,.8)"; ctx.lineWidth = 0.15; ctx.setLineDash([0.8, 0.8]); ctx.beginPath(); ctx.arc(m.x, m.y, 12, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]); }
      ctx.strokeStyle = "rgba(255,255,255,.5)"; ctx.lineWidth = 0.08; ctx.beginPath(); ctx.arc(m.x, m.y, 1 + 0.15 * Math.sin(simTime * 2), 0, Math.PI * 2); ctx.stroke();
    });
    if (mode === "race") drawRaceWorld(v);
    drawGhost();
    drawBoat();
    drawTurnHint();
    ctx.restore();
    if (4.2 * v.ppm < 14) boatMarker(v); // barca sotto 14 px: triangolo orientato come la prua, attorno alla barca

    // sopra il mondo, in coordinate schermo
    ctx.font = font(600, 13); ctx.fillStyle = "rgba(255,255,255,.9)"; ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    marks.forEach((m, i) => { if (m.fin) return; const [sx, sy] = toScreen(v, m.x, m.y); ctx.fillText(m.label + (m.round && mode === "mission" && i === S.markIdx ? " · lasciala a sinistra" : ""), sx + 10, sy - 8); });
    const act = mode === "race" ? null : goal(); // in regata la freccia la disegna drawRaceScreen, sopra l'orologio
    if (act) offscreenArrow(v, act);
    const fm = marks.find(m => m.fin);
    if (fm) linePill(v, { x: fm.x + fm.ny * FIN_HALF, y: fm.y - fm.nx * FIN_HALF }, { x: fm.x - fm.ny * FIN_HALF, y: fm.y + fm.nx * FIN_HALF }, fm.label, act === fm ? fm : null, 0, 0);
    if (st && st.rose) drawRose(v, st.maneuvers, st.target);
    if (opt.arrows && (!st || st.arrows || st.hud >= 2 || (!st.pause && st.hud))) drawWindArrows(v, mode === "lesson" && lessonIdx < 3); // il vento apparente si spiega nella lezione 4
    if (st && st.labels) drawLabels(v, st.labels);
    drawCompass(v);
    drawWindBox(v);
    drawVersionTag();
    const heelG = !st || st.hud >= 3;
    if (heelG) drawHeelGauge();
    // rosa dell'angolo morto (0.16): dove c'è lo sbandamento e nei passi pratici delle lezioni, tranne quando c'è già la rosa grande
    if (opt.dead && !(st && (st.pause || st.rose || !st.hud))) drawDeadRose(heelG ? 196 : 84);
    if (mode === "race") drawRaceScreen(v);
    drawHelmLegend();
    if (qOnSea && fontsOk){ // ripiego se la riga dei tasti nel pannello si taglierebbe: sopra i pulsanti + e −
      ctx.save(); ctx.font = font(700, 13); ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
      ctx.fillStyle = "rgba(255,255,255,.8)"; ctx.fillText("Q vista", W - 34, H - 108); ctx.restore();
    }
    if (S.toast) drawToast();
  }

  // ---- frecce fuori schermo, linee e scritte ----
  // posizione e angolo della freccia fuori schermo verso m; null se m è sullo schermo
  function arrowAt(v, m){
    const [sx, sy] = toScreen(v, m.x, m.y), pad = 30;
    if (sx > 0 && sx < W && sy > 0 && sy < H) return null;
    const ang = Math.atan2(sy - H / 2, sx - W / 2);
    const t = Math.min((W / 2 - pad) / Math.abs(Math.cos(ang) || 1e-6), (H / 2 - pad) / Math.abs(Math.sin(ang) || 1e-6));
    let ax = W / 2 + Math.cos(ang) * t, ay = H / 2 + Math.sin(ang) * t;
    if (mode === "race" && ay < 80 && Math.abs(ax - W / 2) < 170) ay = 80; // non coprire l'orologio della regata
    return [ax, ay, ang];
  }
  function offscreenArrow(v, m){
    const a = arrowAt(v, m); if (!a) return;
    ctx.save(); ctx.translate(a[0], a[1]); ctx.rotate(a[2]); ctx.fillStyle = "#F28C1B";
    ctx.beginPath(); ctx.moveTo(14, 0); ctx.lineTo(-8, -9); ctx.lineTo(-8, 9); ctx.closePath(); ctx.fill(); ctx.restore();
    if (!fontsOk) return;
    // distanza dalla barca, ai 5 m, verso l'interno dello schermo rispetto alla freccia
    const txt = Math.round(Math.hypot(m.x - S.x, m.y - S.y) / 5) * 5 + " m";
    ctx.save(); ctx.font = font(700, 13); ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillStyle = "rgba(255,255,255,.9)"; ctx.fillText(txt, a[0] - Math.cos(a[2]) * 30, a[1] - Math.sin(a[2]) * 22); ctx.restore();
  }
  function boatMarker(v){
    const [x, y] = toScreen(v, S.x, S.y);
    ctx.save(); ctx.translate(x, y); ctx.rotate(S.h * D2R + v.rot);
    ctx.strokeStyle = "rgba(255,255,255,.9)"; ctx.lineWidth = 1.5; ctx.lineJoin = "round";
    ctx.beginPath(); ctx.moveTo(0, -13); ctx.lineTo(8, 9); ctx.lineTo(-8, 9); ctx.closePath(); ctx.stroke(); ctx.restore();
  }
  // linea a scacchi bianchi e neri fra a e b (coordinate del mondo): due file di quadretti di 3 px sullo schermo a ogni zoom
  function drawChecker(a, b, ppm, alpha){
    const q = 3 / ppm, L = Math.hypot(b.x - a.x, b.y - a.y) || 1, nx = -(b.y - a.y) / L * q / 2, ny = (b.x - a.x) / L * q / 2;
    ctx.save(); ctx.globalAlpha = alpha; ctx.lineCap = "butt";
    ctx.strokeStyle = "#16191C"; ctx.lineWidth = 2 * q; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    ctx.strokeStyle = "#fff"; ctx.lineWidth = q; ctx.setLineDash([q, q]);
    for (const s of [1, -1]){ ctx.lineDashOffset = s > 0 ? 0 : q; ctx.beginPath(); ctx.moveTo(a.x + nx * s, a.y + ny * s); ctx.lineTo(b.x + nx * s, b.y + ny * s); ctx.stroke(); }
    ctx.restore();
  }
  // scritta di una linea («Arrivo», «Linea di partenza»): pillola a misura fissa sullo schermo accanto a una delle due boe
  // (quella verso cui punta la freccia fuori schermo, se punta alla linea, altrimenti la più vicina alla barca), mai sopra la barca o le boe.
  // aim: punto a cui punta la freccia, o null; padA, padB: ingombro in metri oltre la boa (0,8 m) attorno alle due estremità (la barca giuria)
  function linePill(v, A, B, text, aim, padA, padB){
    if (!fontsOk) return; // misure e disegno solo con i caratteri caricati
    const pa = toScreen(v, A.x, A.y), pb = toScreen(v, B.x, B.y), ar = aim && arrowAt(v, aim), ref = ar || [v.cx, v.cy];
    const useA = Math.hypot(pa[0] - ref[0], pa[1] - ref[1]) <= Math.hypot(pb[0] - ref[0], pb[1] - ref[1]);
    const [p, o] = useA ? [pa, pb] : [pb, pa], gap = 10 + (0.8 + (useA ? padA : padB)) * v.ppm, flag = text === "Arrivo";
    ctx.save(); ctx.font = font(700, 14); ctx.textAlign = "left"; ctx.textBaseline = "middle";
    const h = 24, w = ctx.measureText(text).width + (flag ? 38 : 22);
    const dl = Math.hypot(p[0] - o[0], p[1] - o[1]), ux = dl > 1 ? (p[0] - o[0]) / dl : 1, uy = dl > 1 ? (p[1] - o[1]) / dl : 0;
    const onS = p[0] >= 0 && p[0] <= W && p[1] >= 0 && p[1] <= H; // boa sullo schermo: la pillola resta dentro lo schermo
    const at = (dx, dy) => { const e = gap + Math.abs(dx) * w / 2 + Math.abs(dy) * h / 2, x = p[0] + dx * e - w / 2, y = p[1] + dy * e - h / 2;
      return onS ? [clamp(x, 4, W - w - 4), clamp(y, 4, H - h - 4)] : [x, y]; };
    const hits = (x, y, cx, cy, r) => Math.hypot(clamp(cx, x, x + w) - cx, clamp(cy, y, y + h) - cy) < r;
    const rb = Math.max(26, 3.5 * v.ppm), cand = [at(ux, uy), at(-uy, ux), at(uy, -ux)];
    const free = ([x, y]) => !hits(x, y, v.cx, v.cy, rb) && !hits(x, y, p[0], p[1], 4 + (0.8 + (useA ? padA : padB)) * v.ppm) && !hits(x, y, o[0], o[1], 8 + (0.8 + (useA ? padB : padA)) * v.ppm);
    const seen = ([x, y]) => x >= 0 && y >= 0 && x + w <= W && y + h <= H; // prima le posizioni tutte sullo schermo
    const [x, y] = cand.find(c => free(c) && seen(c)) || cand.find(free) || cand[0];
    ctx.fillStyle = "rgba(10,24,36,.72)"; ctx.beginPath(); ctx.roundRect(x, y, w, h, h / 2); ctx.fill();
    let tx = x + 11;
    if (flag){ // bandierina a scacchi: asta e 3 x 2 quadretti
      ctx.fillStyle = "#fff"; ctx.fillRect(tx, y + 5, 1.5, 14); ctx.fillRect(tx + 1.5, y + 5, 10.5, 7);
      ctx.fillStyle = "#16191C"; for (const [c, r] of [[1, 0], [0, 1], [2, 1]]) ctx.fillRect(tx + 1.5 + c * 3.5, y + 5 + r * 3.5, 3.5, 3.5);
      tx += 17;
    }
    ctx.fillStyle = "#fff"; ctx.fillText(text, tx, y + h / 2 + 0.5); ctx.restore();
  }

  function drawToast(){
    const a = Math.min(1, S.toast.t / 0.4);
    ctx.save(); ctx.globalAlpha = a; ctx.font = font(700, 20); ctx.textAlign = "center"; ctx.textBaseline = "middle";
    const w = ctx.measureText(S.toast.text).width + 28;
    const ty = mode === "race" ? 100 : 58;
    ctx.fillStyle = "rgba(10,24,36,.75)"; ctx.fillRect(W / 2 - w / 2, ty, w, 36);
    ctx.fillStyle = "#fff"; ctx.fillText(S.toast.text, W / 2, ty + 19); ctx.restore();
  }

  // ---- rosa delle andature ed etichette ----
  // cerchio delle andature, in coordinate schermo attorno alla barca
  function drawRose(v, showManeuvers, target){
    const [cx, cy] = toScreen(v, S.x, S.y), R = Math.min(W, H) * 0.3, r0 = R * 0.72, rotDeg = v.rot / D2R;
    const toCanvas = bearing => (bearing + rotDeg - 90) * D2R;
    const sectors = [[0,40],[40,55],[55,75],[75,105],[105,135],[135,165],[165,180]];
    const twaS = norm180(local.twd - S.h), twa = Math.abs(twaS);
    const curIdx = ANDATURE.findIndex(a => twa < a[0]), curSide = twaS >= 0 ? -1 : 1; // lato del settore in cui si trova la prua
    ctx.save();
    for (const side of [1, -1]){
      sectors.forEach(([a1, a2], k) => {
        const b1 = env.twd + side * a1, b2 = env.twd + side * a2;
        const s1 = Math.min(toCanvas(b1), toCanvas(b2)), s2 = Math.max(toCanvas(b1), toCanvas(b2));
        ctx.beginPath(); ctx.arc(cx, cy, R, s1, s2); ctx.arc(cx, cy, r0, s2, s1, true); ctx.closePath();
        const isCur = k === curIdx && (side === curSide || k === 0 || k === 6);
        ctx.globalAlpha = isCur ? 0.5 : (k === 0 ? 0.3 : (k % 2 ? 0.12 : 0.2));
        ctx.fillStyle = isCur ? colors.label : (k === 0 ? "#E0553A" : "#FFFFFF"); ctx.fill();
        ctx.globalAlpha = 0.35; ctx.strokeStyle = "#fff"; ctx.lineWidth = 1; ctx.stroke();
        if (target && target.includes(k) && (side === curSide || k === 0 || k === 6)){ ctx.globalAlpha = 1; ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.setLineDash([5, 4]); ctx.stroke(); ctx.setLineDash([]); }
      });
    }
    ctx.globalAlpha = 1;
    ctx.font = font(600, Math.round(clamp(R * 0.075, 12, 16))); ctx.textBaseline = "middle";
    const put = (bearing, text, cur) => {
      const a = toCanvas(bearing), x = cx + Math.cos(a) * (R + 8), y = cy + Math.sin(a) * (R + 8);
      ctx.textAlign = Math.cos(a) > 0.2 ? "left" : Math.cos(a) < -0.2 ? "right" : "center";
      const yy = y + (ctx.textAlign === "center" ? (Math.sin(a) > 0 ? 10 : -10) : 0);
      ctx.fillStyle = "rgba(0,0,0,.35)"; ctx.fillText(text, x + 1, yy + 1);
      ctx.fillStyle = cur ? colors.label : "#fff"; ctx.fillText(text, x, yy);
    };
    put(env.twd, "Angolo morto", curIdx === 0);
    put(env.twd + 180, "Poppa", curIdx === 6);
    ANDATURE.slice(1, 6).forEach((an, j) => { const [a1, a2] = sectors[j + 1]; put(env.twd + curSide * (a1 + a2) / 2, an[1], curIdx === j + 1); });
    const hA = toCanvas(S.h);
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5; ctx.setLineDash([5, 4]);
    ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(hA) * R, cy + Math.sin(hA) * R); ctx.stroke(); ctx.setLineDash([]);
    if (showManeuvers){
      const rm = (R + r0) / 2;
      const arc = (b1, b2, label) => {
        const a1 = toCanvas(b1), a2 = toCanvas(b2);
        ctx.strokeStyle = colors.label; ctx.fillStyle = colors.label; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(cx, cy, rm, a1, a2); ctx.stroke();
        for (const [a, dir] of [[a1, -1], [a2, 1]]){
          const x = cx + Math.cos(a) * rm, y = cy + Math.sin(a) * rm, tx = -Math.sin(a) * dir, ty = Math.cos(a) * dir;
          ctx.beginPath(); ctx.moveTo(x + tx * 10, y + ty * 10); ctx.lineTo(x - ty * 7, y + tx * 7); ctx.lineTo(x + ty * 7, y - tx * 7); ctx.closePath(); ctx.fill();
        }
        const am = toCanvas((b1 + b2) / 2);
        ctx.textAlign = "center"; ctx.font = font(700, 15);
        ctx.fillText(label, cx + Math.cos(am) * (r0 - 16), cy + Math.sin(am) * (r0 - 16));
      };
      arc(env.twd - 30, env.twd + 30, "virata");
      arc(env.twd + 150, env.twd + 210, "strambata");
    }
    ctx.restore();
  }

  // etichette delle parti della barca
  function drawLabels(v, names){
    if (!geo) return;
    const L = (lx, ly) => toScreen(v, ...localToWorld(lx, ly));
    const to = (env.twd + 180) * D2R;
    const P = {
      prua: L(0, -2.1), poppa: L(0, 2.1), dritta: L(0.62, 0.5), sinistra: L(-0.62, 0.5), albero: L(0, geo.mastY),
      boma: L(geo.ex * 0.75, geo.mastY + (geo.ey - geo.mastY) * 0.75), randa: L(geo.rx, geo.ry),
      timone: L(-Math.sin(geo.tau) * 0.45, 2.05 + Math.cos(geo.tau) * 0.45), barra: L(Math.sin(geo.tau) * 0.6, 2.05 - Math.cos(geo.tau) * 0.6),
      deriva: L(0, 0.28), filetti: L(geo.qx, geo.qy),
      sopravento: toScreen(v, S.x - Math.sin(to) * 2.2, S.y + Math.cos(to) * 2.2), sottovento: toScreen(v, S.x + Math.sin(to) * 2.2, S.y - Math.cos(to) * 2.2)
    };
    const [bx, by] = toScreen(v, S.x, S.y);
    const used = [];
    ctx.save(); ctx.font = font(700, 16); ctx.textBaseline = "middle";
    for (const n of names){
      const [x, y] = P[n];
      let a = Math.atan2(y - by, x - bx);
      if (Math.hypot(x - bx, y - by) < 6) a = -Math.PI * 0.75;
      if (n === "barra") a += 0.6; if (n === "timone") a -= 0.6; if (n === "deriva") a = Math.atan2(y - by, x - bx) + Math.PI / 2;
      if (n === "randa") a += 0.5;
      let d = 58;
      let ex = x + Math.cos(a) * d, ey = y + Math.sin(a) * d;
      for (const u of used) if (Math.hypot(ex - u[0], ey - u[1]) < 28){ d += 30; ex = x + Math.cos(a) * d; ey = y + Math.sin(a) * d; }
      used.push([ex, ey]);
      ctx.strokeStyle = colors.label; ctx.fillStyle = colors.label; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(ex, ey); ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y, 5, 0, Math.PI * 2); ctx.stroke();
      ctx.textAlign = Math.cos(a) > 0.3 ? "left" : Math.cos(a) < -0.3 ? "right" : "center";
      const tx = ex + (ctx.textAlign === "left" ? 6 : ctx.textAlign === "right" ? -6 : 0), ty = ey + (ctx.textAlign === "center" ? (Math.sin(a) > 0 ? 12 : -12) : 0);
      const w = ctx.measureText(n).width, bxx = ctx.textAlign === "left" ? tx : ctx.textAlign === "right" ? tx - w : tx - w / 2;
      ctx.fillStyle = "rgba(10,24,36,.75)"; ctx.fillRect(bxx - 5, ty - 12, w + 10, 24);
      ctx.fillStyle = colors.label; ctx.fillText(n, tx, ty);
    }
    ctx.restore();
  }

  // ---- barca ----
  // 1.0.23 (docs/PROPOSTA-MOTO-SUL-MARE.md): onda corta che scorre sottovento, SOLO DISEGNO (il motore non la vede). La barca prende la
  // pendenza dell'onda dove si trova: di prua beccheggia, di lato rolla; andando contro le onde la fase corre più in fretta (Doppler da solo).
  // ponytail: periodo e ampiezze sono ipotesi nostre senza fonte («carino da vedere, non perfetto», Ale); una misura da video le sostituirebbe
  const WAVE_DEG = 5, CARENA = "#B9C4CB"; // rollio disegnato con 15 nodi (il beccheggio è il 70%), colore della carena
  function waveTilt(x, y, h, u){
    const kn = env.tws * KN, T = clamp(1.5 + kn * 0.05, 1.5, 2.5);
    const amp = WAVE_DEG * Math.min(1.2, kn / 15) * (1 + Math.max(0, 1 - Math.abs(u) / 1.5)); // ferma balla fino al doppio: navigando la deriva e la vela piena la tengono (Ale, «da ferma si muove di più»)
    let roll = 0, pitch = 0, heave = 0;
    for (const [da, kl, ka] of [[0, 1, 1], [30, 0.6, 0.5]]){ // onda principale e una più corta di lato, perché il moto non sia regolare
      const Tk = T * Math.sqrt(kl), k = 2 * Math.PI / (9.81 * Tk * Tk / (2 * Math.PI)), w = 2 * Math.PI / Tk; // λ = gT²/2π, acqua profonda
      const d = (env.twd + 180 + da) * D2R, dx = Math.sin(d), dy = -Math.cos(d); // verso dove va l'onda: sottovento
      const ph = k * (x * dx + y * dy) - w * simTime, s = Math.cos(ph) * amp * ka;
      const rel = d - h * D2R; // onda rispetto alla prua
      pitch += s * 0.7 * Math.cos(rel); roll += s * Math.sin(rel); heave += Math.sin(ph) * ka;
    }
    return { roll, pitch, amp, heave: heave * 0.012 * Math.min(1, kn / 10) };
  }
  function drawBoat(){
    const t = simTime;
    ctx.save(); ctx.translate(S.x, S.y); ctx.rotate(S.h * D2R);
    if (S.capsized){ drawCapsized(t); ctx.restore(); return; }
    const wv = waveTilt(S.x, S.y, S.h, S.u);
    ctx.scale(1 + wv.heave, 1 + wv.heave); // sulla cresta la barca è un filo più vicina
    const lee = S.boomSide, sinH = Math.sin(Math.max(-40, Math.min(70, S.heel + lee * wv.roll)) * D2R); // lee: lato verso cui sbanda (se positivo)
    const hy = -Math.sin(wv.pitch * D2R) * 5.5; // beccheggio: la testa d'albero va avanti e indietro
    // ombra
    ctx.fillStyle = "rgba(0,0,0,.18)"; hullPath(0.12 + lee * sinH * 0.9, 0.18 - hy * 0.1); ctx.fill();
    // baffi d'acqua alla prua, più lunghi e chiari con la velocità, aperti di circa 20° dalla rotta (l'angolo di Kelvin delle scie), e uno
    // spruzzo quando la prua scende sull'onda (disegno, non calcolo)
    const sp = clamp((S.u - 0.3) / 2.5, 0, 1);
    if (sp > 0){
      ctx.strokeStyle = "rgba(255,255,255," + (0.3 + 0.4 * sp).toFixed(3) + ")"; ctx.lineCap = "round";
      for (const sd of [-1, 1]) for (const [o, w] of [[0, 0.09], [0.25, 0.05]]){
        const j = 0.04 * Math.sin(t * 9 + sd * 2 + o * 7); // la schiuma trema
        const len = 1.2 + 1.8 * sp; // metri dietro la prua
        ctx.lineWidth = w + 0.05 * sp; ctx.beginPath(); ctx.moveTo(sd * 0.03, -2.12);
        ctx.quadraticCurveTo(sd * (0.5 + o + j), -1.75 + o, sd * (0.62 + o + len * 0.36), -2.1 + len + o); ctx.stroke();
      }
      const sz = clamp(wv.amp > 0 ? wv.pitch / (0.7 * wv.amp) * 2 - 1 : 0, 0, 1) * sp;
      if (sz > 0){ ctx.fillStyle = "rgba(255,255,255," + (0.55 * sz).toFixed(3) + ")";
        for (const sd of [-1, 1]){ ctx.beginPath(); ctx.ellipse(sd * 0.35, -1.95, 0.25 + 0.35 * sz, 0.15 + 0.2 * sz, sd * 0.6, 0, Math.PI * 2); ctx.fill(); } }
    }
    // carena: sbandando, sopravento si vede il fondo dello scafo (lo stesso grigio della barca scuffiata)
    if (Math.abs(sinH) > 0.02){ ctx.save(); ctx.scale(1 - Math.abs(sinH) * 0.15, 1); ctx.fillStyle = CARENA; hullPath(-lee * sinH * 0.55, 0); ctx.fill(); ctx.restore(); }
    // scafo (sbandando, visto dall'alto appare più stretto)
    ctx.save(); ctx.scale(1 - Math.abs(sinH) * 0.35, 1);
    ctx.fillStyle = S.hullColor || colors.hull; ctx.strokeStyle = colors["hull-edge"]; ctx.lineWidth = 0.05; hullPath(0, 0); ctx.fill(); ctx.stroke();
    // pozzetto e scassa della deriva
    ctx.fillStyle = colors.cockpit;
    ctx.beginPath(); ctx.moveTo(-0.38, 0.35); ctx.lineTo(0.38, 0.35); ctx.lineTo(0.42, 1.55); ctx.lineTo(-0.42, 1.55); ctx.closePath(); ctx.fill();
    ctx.fillStyle = colors.spar; ctx.fillRect(-0.04, 0.05, 0.08, 0.45);
    ctx.restore();
    // timone: pala dietro lo specchio di poppa, barra in avanti
    const tau = ctl.tiller * (S.lv === 2 ? RUD2.maxRudder : BOAT.maxRudder) * D2R;
    ctx.strokeStyle = colors.spar; ctx.lineCap = "round";
    ctx.lineWidth = 0.09; ctx.beginPath(); ctx.moveTo(0, 2.05); ctx.lineTo(-Math.sin(tau) * 0.55, 2.05 + Math.cos(tau) * 0.55); ctx.stroke();
    ctx.lineWidth = 0.06; ctx.beginPath(); ctx.moveTo(0, 2.05); ctx.lineTo(Math.sin(tau) * 1.0, 2.05 - Math.cos(tau) * 1.0); ctx.stroke();
    // timoniere seduto sopravento (1.0.23): piedi nel pozzetto, sedere sul bordo, busto che esce fuori bordo quanto più si sporge,
    // braccio sulla prolunga del timone; dall'alto il busto dritto si vede corto, sdraiato fuori bordo si vede lungo
    const ws = -S.boomSide, hk = S.hike || 0; // lato sopravento: opposto al boma
    const hipX = ws * (0.5 + 0.14 * hk), shX = hipX + ws * (0.12 + 0.72 * hk), shY = 1.0 - 0.08 * hk;
    ctx.strokeStyle = S.sailorColor || colors.sailor; ctx.lineCap = "round";
    ctx.lineWidth = 0.14; ctx.beginPath(); ctx.moveTo(ws * 0.08, 1.3); ctx.lineTo(hipX, 1.12); ctx.stroke();   // gambe
    ctx.lineWidth = 0.3; ctx.beginPath(); ctx.moveTo(hipX, 1.12); ctx.lineTo(shX, shY); ctx.stroke();           // busto
    // prolunga del timone: dalla fine della barra alla mano, che sta a un braccio (45 cm) dalla spalla; il braccio non si allunga mai
    const tx0 = Math.sin(tau) * 1.0, ty0 = 2.05 - Math.cos(tau) * 1.0, dd = Math.hypot(tx0 - shX, ty0 - shY), arm = Math.min(0.45, dd);
    const hdX = shX + (tx0 - shX) / (dd || 1) * arm, hdY = shY + (ty0 - shY) / (dd || 1) * arm;
    ctx.strokeStyle = colors.spar; ctx.lineWidth = 0.035; ctx.beginPath(); ctx.moveTo(tx0, ty0); ctx.lineTo(hdX, hdY); ctx.stroke();
    ctx.strokeStyle = S.sailorColor || colors.sailor; ctx.lineWidth = 0.08; ctx.beginPath(); ctx.moveTo(shX, shY); ctx.lineTo(hdX, hdY); ctx.stroke(); // braccio
    ctx.fillStyle = "#F2D2B6"; ctx.beginPath(); ctx.arc(shX + ws * (0.08 + 0.1 * hk), shY - 0.04, 0.13, 0, Math.PI * 2); ctx.fill();
    // randa e boma
    const bs = S.dispBoom >= 0 ? 1 : -1; // lato su cui sta il boma (anche durante lo spostamento)
    const mastY = -0.95, boomLen = 2.75, b = S.dispBoom * D2R;
    const ex = Math.sin(b) * boomLen, ey = mastY + Math.cos(b) * boomLen;
    const st = ttState();
    const load = Math.min(1, CL(Math.max(0, info.alpha)) / 1.2);
    const nx = Math.cos(b) * bs, ny = -Math.sin(b) * bs; // normale verso sottovento
    // vista dall'alto: si vede la randa fra il boma (base) e il profilo alto, più svergolato sottovento
    let camber = 0.22 + 0.3 * load, twist = 0.35 + 0.25 * load;
    if (st === "flog"){ camber = Math.sin(t * 28) * 0.3; twist = 0.15 + Math.sin(t * 19) * 0.25; }
    else if (st === "wind"){ camber *= 0.55 + 0.45 * Math.sin(t * 22); }
    // sbandando, la parte alta della vela si sposta sottovento (proiezione dall'alto); punto e curva servono ai filetti, che restano dove erano
    const hs = lee * sinH * 2.6;
    const tx = ex + nx * twist + hs, ty = ey + ny * twist;
    const mx = tx / 2 + nx * camber * 2 + hs * 0.5, my = (mastY + ty) / 2 + ny * camber * 2;
    // contorno della randa: base sul boma, balumina dalla fine del boma alla penna, penna in testa d'albero (dove finisce l'albero disegnato)
    const hx = lee * sinH * 5.5, hY = mastY + hy; // testa d'albero, sottovento quando la barca sbanda (e avanti e indietro col beccheggio)
    const fx = ex / 2 + nx * camber * 0.5, fy = (mastY + ey) / 2 + ny * camber * 0.5; // base appena gonfia
    const bulge = camber * 1.6 + twist; // ponytail: gonfiore della balumina a occhio, nessuna fonte
    const lx = (ex + hx) / 2 + nx * bulge, ly = (ey + hY) / 2 + ny * bulge;
    const sg = ctx.createLinearGradient(0, mastY, ex + nx, ey + ny); sg.addColorStop(0, colors["sail-shade"]); sg.addColorStop(0.55, S.sailColor || colors.sail); sg.addColorStop(1, colors["sail-shade"]);
    ctx.fillStyle = sg; ctx.strokeStyle = "rgba(60,70,80,.6)"; ctx.lineWidth = 0.04;
    ctx.beginPath(); ctx.moveTo(0, mastY); ctx.quadraticCurveTo(fx, fy, ex, ey); ctx.quadraticCurveTo(lx, ly, hx, hY); ctx.lineTo(0, mastY); ctx.fill(); ctx.stroke();
    // stecche: dalla balumina verso l'albero
    ctx.strokeStyle = "rgba(60,70,80,.25)";
    for (const f of [0.3, 0.55, 0.8]){
      const px = (1 - f) * (1 - f) * ex + 2 * (1 - f) * f * lx + f * f * hx, py = (1 - f) * (1 - f) * ey + 2 * (1 - f) * f * ly + f * f * hY;
      const ax = f * hx, ay = mastY + f * hy;
      ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px + (ax - px) * 0.35, py + (ay - py) * 0.35); ctx.stroke();
    }
    // boma
    ctx.strokeStyle = colors.spar; ctx.lineWidth = 0.09; ctx.beginPath(); ctx.moveTo(0, mastY); ctx.lineTo(ex, ey); ctx.stroke();
    // filetti: vicino all'inferitura, uno per lato della vela
    const f = 0.3, qx = 2 * (1 - f) * f * mx + f * f * tx, qy = (1 - f) * (1 - f) * mastY + 2 * (1 - f) * f * my + f * f * ty;
    const cx = tx, cy = ty - mastY, cl = Math.hypot(cx, cy), ax = cx / cl, ay = cy / cl; // direzione verso la balumina
    for (const side of [-1, 1]){
      const isLee = side === bs; // lato sottovento della vela = lato del boma
      const col = side < 0 ? colors["tt-port"] : colors["tt-stbd"];
      const ox = qx + Math.cos(b) * side * 0.1, oy = qy - Math.sin(b) * side * 0.1;
      const bad = (st === "flog") || (st === "wind" && !isLee) || (st === "lee" && isLee);
      ctx.strokeStyle = col; ctx.lineWidth = 0.07; ctx.beginPath(); ctx.moveTo(ox, oy);
      const segs = 6, Lt = 0.65;
      for (let i = 1; i <= segs; i++){
        const u = i / segs;
        let wig = 0, curl = 0;
        if (bad){ wig = Math.sin(t * 25 + u * 6 + side) * 0.09 * u; curl = (isLee ? 0.25 : -0.25) * u * u * side * bs; }
        const px = ox + ax * Lt * u + (-ay) * (wig + curl), py = oy + ay * Lt * u + ax * (wig + curl);
        ctx.lineTo(px, py);
      }
      ctx.stroke();
    }
    // albero (visibile come linea quando la barca sbanda) e segnavento in testa d'albero
    const mastSeen = Math.hypot(hx, hy) > 0.25;
    if (mastSeen){ ctx.strokeStyle = colors.spar; ctx.lineWidth = 0.07; ctx.beginPath(); ctx.moveTo(0, mastY); ctx.lineTo(hx, hY); ctx.stroke(); }
    ctx.fillStyle = colors.spar; ctx.beginPath(); ctx.arc(0, mastY, 0.08, 0, Math.PI * 2); ctx.fill();
    const awRel = info.awa * D2R; // da dove arriva, rispetto alla prua (+ dritta)
    const vx = Math.sin(awRel), vy = -Math.cos(awRel);
    ctx.strokeStyle = colors.app; ctx.fillStyle = colors.app; ctx.lineWidth = 0.06;
    // 1.0.10: perno vicino alla punta, come una banderuola: la coda, più lunga, sta sottovento (docs/PROPOSTA-DISEGNO-VELA.md)
    ctx.beginPath(); ctx.moveTo(hx + vx * 0.3, hY + vy * 0.3); ctx.lineTo(hx - vx * 0.7, hY - vy * 0.7); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(hx + vx * 0.3, hY + vy * 0.3); ctx.lineTo(hx + vx * 0.05 - vy * 0.12, hY + vy * 0.05 + vx * 0.12); ctx.lineTo(hx + vx * 0.05 + vy * 0.12, hY + vy * 0.05 - vx * 0.12); ctx.closePath(); ctx.fill();
    if (mastSeen){ ctx.fillStyle = colors.spar; ctx.beginPath(); ctx.arc(hx, hY, 0.07, 0, Math.PI * 2); ctx.fill(); } // perno del segnavento in testa d'albero
    ctx.restore();
    geo = { mastY, ex, ey, rx: (hx + ex + lx) / 3, ry: (mastY + ey + ly) / 3, qx, qy, tau, hx, hY, sc: 1 + wv.heave }; // hx, hY: testa d'albero (collaudo_moto_mare.py)
  }
  function drawCapsized(t){
    const side = S.capSide || 1, prog = S.righting ? Math.min(1, S.righting / 3) : 0;
    // 1.0.23: nei primi 0,6 s dopo la scuffia l'albero finisce di cadere (prima la barca passava di colpo da sbandata a sdraiata)
    const fall = S.capAt === undefined ? 1 : Math.min(1, (t - S.capAt) / 0.6);
    const lie = (1 - prog) * (0.75 + 0.25 * (1 - (1 - fall) * (1 - fall))); // 1 = sdraiata, 0 = dritta
    if (fall < 1){ ctx.strokeStyle = "rgba(255,255,255," + (0.7 * (1 - fall)).toFixed(3) + ")"; ctx.lineWidth = 0.12; // spruzzo dove l'albero tocca l'acqua
      ctx.beginPath(); ctx.ellipse(side * 5, -1.1, 0.6 + 2.4 * fall, 0.4 + 1.4 * fall, 0, 0, Math.PI * 2); ctx.stroke(); }
    // scafo sul fianco: si vede la carena
    ctx.save(); ctx.scale(1 - 0.45 * lie, 1);
    ctx.fillStyle = lie > 0.5 ? CARENA : colors.hull; ctx.strokeStyle = colors["hull-edge"]; ctx.lineWidth = 0.05; hullPath(0, 0); ctx.fill(); ctx.stroke();
    ctx.restore();
    // albero e vela distesi sull'acqua
    const mastY = -0.95, L = 5.8 * lie;
    ctx.fillStyle = "rgba(251,251,247,.8)"; ctx.strokeStyle = "rgba(60,70,80,.6)"; ctx.lineWidth = 0.04;
    ctx.beginPath(); ctx.moveTo(0, mastY); ctx.lineTo(side * L, mastY - 0.2); ctx.lineTo(side * 0.4 * lie, mastY + 2.7); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.strokeStyle = colors.spar; ctx.lineWidth = 0.08; ctx.beginPath(); ctx.moveTo(0, mastY); ctx.lineTo(side * L, mastY - 0.2); ctx.stroke();
    // timoniere in acqua, sulla deriva per raddrizzare
    ctx.fillStyle = colors.sailor; ctx.beginPath(); ctx.arc(-side * (0.9 - 0.4 * prog), 0.4, 0.22, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,.5)"; ctx.lineWidth = 0.06;
    ctx.beginPath(); ctx.arc(-side * (0.9 - 0.4 * prog), 0.4, 0.35 + 0.1 * Math.sin(t * 3), 0, Math.PI * 2); ctx.stroke();
  }
  function hullPath(ox, oy){
    ctx.beginPath();
    ctx.moveTo(ox, -2.1 + oy);
    ctx.bezierCurveTo(0.55 + ox, -1.5 + oy, 0.72 + ox, -0.2 + oy, 0.68 + ox, 0.7 + oy);
    ctx.lineTo(0.56 + ox, 2.1 + oy); ctx.lineTo(-0.56 + ox, 2.1 + oy); ctx.lineTo(-0.68 + ox, 0.7 + oy);
    ctx.bezierCurveTo(-0.72 + ox, -0.2 + oy, -0.55 + ox, -1.5 + oy, ox, -2.1 + oy);
    ctx.closePath();
  }

  // ---- frecce del vento e strumenti a schermo ----
  function shaftHead(sx, sy, x, y, dx, dy){ // asta da (sx, sy) e punta in (x, y), direzione (dx, dy); colori e spessore già scelti
    ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(x - dx * 10, y - dy * 10); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - dx * 14 - dy * 7, y - dy * 14 + dx * 7); ctx.lineTo(x - dx * 14 + dy * 7, y - dy * 14 - dx * 7); ctx.closePath(); ctx.fill();
  }
  function arrow(x, y, ang, len, col, label){
    const dx = Math.sin(ang), dy = -Math.cos(ang);
    const sx = x - dx * len, sy = y - dy * len;
    ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = 3;
    shaftHead(sx, sy, x, y, dx, dy);
    ctx.font = font(700, 13); ctx.textAlign = "center";
    ctx.fillText(label, sx - dx * 12, sy - dy * 12 + 4);
  }
  // frecce che puntano verso la barca, dalla direzione da cui arriva ciascun vento
  function drawWindArrows(v, trueOnly){
    const [bx, by] = toScreen(v, S.x, S.y), rr = 2.9 * v.ppm + 10;
    const scr = d => (d + (v.rot / D2R)) * D2R; // direzione mondo -> schermo
    const tFrom = scr(local.twd), aFrom = scr(info.awFrom);
    const tl = 25 + local.tws * 5, al = 25 + info.aws * 5;
    arrow(bx + Math.sin(tFrom) * rr, by - Math.cos(tFrom) * rr, tFrom + Math.PI, tl, colors.true, "reale");
    if (!trueOnly) arrow(bx + Math.sin(aFrom) * (rr + 6), by - Math.cos(aFrom) * (rr + 6), aFrom + Math.PI, al, colors.app, "apparente");
    drawSpeedArrow(v, bx, by, rr);
  }
  // Freccia della velocità (0.16): dal centro della barca, nella direzione in cui la barca si muove davvero
  // (avanti più scarroccio; all'indietro esce dalla poppa), lunga in proporzione alla velocità, nascosta sotto 0,3 nodi.
  function drawSpeedArrow(v, bx, by, rr){
    const st = curStep(); if (S.capsized || (st && st.pause)) return; // nelle pause la scena è ferma: niente freccia
    const h = S.h * D2R, vx = Math.sin(h) * S.u + Math.cos(h) * S.vl, vy = -Math.cos(h) * S.u + Math.sin(h) * S.vl, sp = Math.hypot(vx, vy);
    if (sp * KN < 0.3) return;
    const ang = (Math.atan2(vx, -vy) / D2R + v.rot / D2R) * D2R, dx = Math.sin(ang), dy = -Math.cos(ang);
    const len = rr + 22 * sp, tx = bx + dx * len, ty = by + dy * len;
    ctx.save(); ctx.strokeStyle = ctx.fillStyle = colors.moto; ctx.lineWidth = 3;
    shaftHead(bx, by, tx, ty, dx, dy);
    // scritta di fianco alla punta, dal lato opposto a quello da cui arriva il vento: così non si sovrappone alle frecce del vento
    const wf = (local.twd + v.rot / D2R) * D2R; let nx = -dy, ny = dx;
    if (nx * Math.sin(wf) - ny * Math.cos(wf) > 0){ nx = -nx; ny = -ny; }
    const lx = tx - dx * 8 + nx * 10, ly = ty - dy * 8 + ny * 10;
    ctx.font = font(700, 13); ctx.textAlign = nx >= 0 ? "left" : "right"; ctx.textBaseline = "middle";
    ctx.fillStyle = "rgba(0,0,0,.35)"; ctx.fillText("velocità", lx + 1, ly + 1);
    ctx.fillStyle = colors.moto; ctx.fillText("velocità", lx, ly);
    ctx.restore();
  }
  function drawCompass(v){
    const r = 26, cx = W - r - 16, cy = r + 22, a = v.rot;
    ctx.save(); ctx.translate(cx, cy);
    ctx.fillStyle = "rgba(0,0,0,.22)"; ctx.beginPath(); ctx.arc(0, 0, r + 4, 0, Math.PI * 2); ctx.fill();
    ctx.rotate(a); ctx.strokeStyle = "rgba(255,255,255,.8)"; ctx.fillStyle = "#fff"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, -r + 5); ctx.lineTo(-5, 0); ctx.lineTo(5, 0); ctx.closePath(); ctx.fill();
    ctx.font = font(700, 12); ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("N", 0, -r - 9);
    ctx.restore();
  }
  function drawHeelGauge(){
    const r = 44, cx = 84, cy = H - 20;
    const heel = S.capsized ? 90 * (S.righting ? 1 - Math.min(1, S.righting / 3) : 1) : Math.max(-60, Math.min(90, S.heel));
    ctx.save(); ctx.translate(cx, cy);
    ctx.fillStyle = "rgba(0,0,0,.25)"; ctx.beginPath(); ctx.arc(0, 0, r + 8, Math.PI, 0); ctx.closePath(); ctx.fill();
    const zone = (a1, a2, col) => { ctx.strokeStyle = col; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(0, 0, r, -Math.PI / 2 + a1 * D2R, -Math.PI / 2 + a2 * D2R); ctx.stroke(); };
    zone(-60, -15, "#E8935A"); zone(-15, 20, "#5CC393"); zone(20, 35, "#F2C14E"); zone(35, 60, "#E0553A"); zone(60, 90, "#8E1F14");
    const a = -Math.PI / 2 + heel * D2R;
    ctx.strokeStyle = "#fff"; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * (r - 4), Math.sin(a) * (r - 4)); ctx.stroke();
    ctx.fillStyle = "#fff"; ctx.font = font(600, 12); ctx.textAlign = "center";
    ctx.fillText("sbandamento " + (S.capsized ? "— scuffia" : Math.round(Math.abs(S.heel)) + "°"), 0, -r - 12);
    ctx.restore();
  }
  // Rosa dell'angolo morto: il vento arriva sempre dall'alto; il settore rosso è l'angolo morto (IRONS_A per lato,
  // lo stesso limite della voce «Andatura» e del registro); la lancetta è la prua, rossa quando ci entra.
  function drawDeadRose(cx){
    const r = 34, cy = H - 44, rel = norm180(S.h - local.twd), inDead = Math.abs(rel) < IRONS_A && !S.capsized;
    ctx.save(); ctx.translate(cx, cy);
    ctx.fillStyle = "rgba(0,0,0,.25)"; ctx.beginPath(); ctx.arc(0, 0, r + 8, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,.35)"; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.stroke();
    ctx.strokeStyle = "#E0553A"; ctx.beginPath(); ctx.arc(0, 0, r, -Math.PI / 2 - IRONS_A * D2R, -Math.PI / 2 + IRONS_A * D2R); ctx.stroke();
    ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.moveTo(0, -r + 12); ctx.lineTo(-5, -r + 3); ctx.lineTo(5, -r + 3); ctx.closePath(); ctx.fill(); // il vento entra dall'alto
    const a = -Math.PI / 2 + rel * D2R;
    ctx.strokeStyle = inDead ? "#E0553A" : "#fff"; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * (r - 4), Math.sin(a) * (r - 4)); ctx.stroke();
    ctx.fillStyle = inDead ? "#E0553A" : "#fff"; ctx.beginPath(); ctx.arc(0, 0, 3, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = "#fff"; ctx.font = font(600, 12); ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
    ctx.fillText(inDead ? "nell'angolo morto" : "prua e vento", 0, -r - 12);
    ctx.restore();
  }
  function drawWindBox(v){
    ctx.save(); ctx.font = font(600, 14); ctx.fillStyle = "rgba(255,255,255,.9)"; ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    ctx.fillText("Vento reale da " + card(env.twd) + " (" + deg3(env.twd) + "), " + (env.tws * KN).toFixed(0) + " nodi", 16, 26);
    ctx.restore();
  }
  // sotto la bussola (in alto a destra), sopra i pulsanti dello zoom: unico punto libero a tutte le risoluzioni del pannello
  function drawVersionTag(){
    ctx.save(); ctx.font = font(600, 12); ctx.fillStyle = "rgba(255,255,255,.45)"; ctx.textAlign = "right"; ctx.textBaseline = "alphabetic";
    ctx.fillText("V. " + VERSIONE, W - 16, 96);
    ctx.restore();
  }



