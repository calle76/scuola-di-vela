// Scuola di vela, avvio.js — Ciclo del gioco, avvio e aggancio dei collaudi (#collaudo). Va caricato per ultimo.
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/archivio/PROPOSTA-DIVISIONE-CODICE.md.
  // ======================================================================
  // CICLO
  // ======================================================================
  let last = performance.now(), panelT = 0, lastErr = "", timeScale = 1;
  function frame(now){
    requestAnimationFrame(frame);
    try { tick(now); }
    catch (err){ if (String(err) !== lastErr){ lastErr = String(err); console.error(err); $("errBox").hidden = false; $("errBox").textContent = "Errore interno: " + lastErr + ". Il gioco prosegue; se qualcosa non risponde, torna al menu."; } }
  }
  function tick(now){
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (mode === "menu") return;
    if (riv.on){ rivTick(dt); draw(0.016); return; } // moviola: gioco fermo, né registratore né pannello
    const st = curStep(), paused = (st && st.pause) || briefing || $("gloss").open || $("quiz").open || $("setDlg").open || $("torDlg").open;
    if (!paused){ for (let k = 0; k < timeScale; k++){ simulate(dt, st); simTime += dt; } }
    else { if (st && st.pause) ctl.sheet = autoSheet(); info = step(S, ctl, local, 0); S.dispBoom = S.boomSide * S.boom; }
    draw(paused ? 0.016 : dt);
    sesTick(dt);
    panelT -= dt; if (panelT <= 0){ panel(); panelT = 0.1; }
  }
  env.twd = 0; freshState(0, 0, 90, 0.4);
  addEventListener("pagehide", () => { if (mode === "race") torEsci(); }); // 1.0.50: pagina chiusa o ricaricata a metà regata del torneo = ritiro
  showMenu();
  // aggancio per i collaudi automatici (attivo solo con #collaudo nell'indirizzo, o #collaudo-lab per il laboratorio)
  if (location.hash === "#collaudo" || location.hash === "#collaudo-lab"){ window.__sv = {
    // 0.21, pilota sostituto per collaudo_competizione.py: la guida degli avversari principianti (aiControl) sulla barca del giocatore,
    // con i campi che le mancano, la lettura istantanea e lo stesso bersaglio degli avversari (me.me falso solo durante la chiamata).
    // Raddrizza dopo 1 s di scuffia: ipotesi nostra, un giocatore che preme il tasto (gli avversari si raddrizzano da soli dopo 5 s).
    pilota: dt => { const me = R.boats[0];
      if (!me.ai) Object.assign(me, { ai: aiParams("principianti"), side: 1, boardT: 0, boardMax: 40, rOff: Math.random() * 6, char: "normale", startX: toWF(S.x, S.y)[0] * 0.5, capW: 0 });
      if (S.capsized){ me.capW += dt; if (me.capW >= 1) rightBoat(); return ctl.tiller; }
      me.capW = 0; me.info = info; me.me = false; aiControl(me, dt); me.me = true; return ctl.tiller; },
    openItem, chiCede, hullWorld, hullOverlap, estraiEsame, meriti, torPunti, torSerie, torChiudi, torEsci, torApri, get tor(){ return tor; }, set triL(v){ TRI_L = v; }, windAt, envTws: () => env.tws, showStep, setShifts, // setShifts(null): i collaudi del timone e del boma misurano senza salti di vento (1.0.28)
    completeStep, startMission, readI, get R(){ return R; }, ghosts: () => ghosts, fast: n => timeScale = n, kick: n => GYBE_KICK = n, rank: () => ranking().map(b => b.name + ":" + legName(b)), get S(){ return S; }, get stepDone(){ return stepDone; },
    ctl, autoSheet, opt, autoK: (h0, k) => { AUTO_HEEL0 = h0; AUTO_K = k; }, get marks(){ return curMarks; }, get toast(){ return S.toast ? S.toast.text : null; }, get riquadro(){ return R && R.segnali ? rqDati() : null; }, get rqRect(){ return R ? R.rqRect : null; }, get rqRect2(){ return R ? R.rqRect2 : null; }, get twd(){ return local.twd; }, get mode(){ return mode; }, get reg(){ return reg; }, set skipBrief(v){ briefSkip = v; }, get briefing(){ return briefing; }, hideBrief, panel, set simTime(v){ simTime = v; },
    run: (dt, n) => { for (let k = 0; k < n; k++){ simulate(dt, curStep()); simTime += dt; sesTick(dt, true); } }, ses,
    frame: dt => { simulate(dt, curStep()); simTime += dt; draw(dt); }, get viewOff(){ return viewOff; }, get zoomQ(){ return zoomQ; }, get camZoom(){ return camZoom; }, draw: dt => draw(dt), gusts: () => gusts.map(g => [g.x, g.y, g.r, g.k, g.sh, g.ttl]), get rippleCells(){ return rippleCells; }, goal, cam: () => { const v = view(); return { cx: v.cx, cy: v.cy, W, H }; } }; // avanza la simulazione a passi fissi, senza il ciclo del browser (taratura delle fasce); sesTick è il registratore, solo lettura
    briefSkip = true; // i collaudi guidano subito; __sv.skipBrief = false per collaudare il riquadro
  }
  requestAnimationFrame(frame);

