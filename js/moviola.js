// Scuola di vela, moviola.js — «Rivedi»: spezzoni di regata registrati in memoria (tasto O o contatto) e riproduzione a fine gara (1.0.58).
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/archivio/PROPOSTA-DIVISIONE-CODICE.md.

  // ======================================================================
  // MOVIOLA (1.0.58, docs/PROPOSTA-COACH-REGISTRATORE.md, prima fetta)
  // Solo lettura sulla simulazione: durante la regata copia le posizioni di tutte le barche a 10 al secondo, non chiama Math.random e non
  // scrive nel gioco. Tiene gli ultimi 10 s in un buffer e, quando il giocatore preme M o c'è un contatto con penalità, ne fa uno spezzone
  // (10 s prima e 8 s dopo). A fine regata «Rivedi» riproduce gli spezzoni a gioco fermo, sostituendo per un attimo lo stato delle barche
  // (come drawOther) e rimettendolo a posto all'uscita. Costanti (ipotesi nostre): 10 campioni/s, 10 s prima, 8 s dopo, al massimo 12 spezzoni.
  // ======================================================================
  const RIV_DT = 0.1, RIV_PRIMA = 10, RIV_DOPO = 8, RIV_MAX = 12, RIV_AUTO_MAX = 6;
  const riv = { roll: [], pend: [], snips: [], acc: 0, nAuto: 0, nMan: 0, on: false, i: 0, pos: 0, speed: 1, playing: true, bk: null };
  const rivTempo = t => { const s = Math.max(0, Math.floor(t)); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); };
  const rivCount = () => riv.snips.length + riv.pend.length;

  // ---- registrazione ----
  function rivReset(){ riv.roll = []; riv.pend = []; riv.snips = []; riv.acc = 0; riv.nAuto = riv.nMan = 0; }
  function rivCapture(t, dt){ // a ogni passo della regata, dopo lo sparo e finché il giocatore non ha finito
    if (!R || R.phase !== "race" || t < 0) return;
    riv.acc += dt; if (riv.acc < RIV_DT) return; riv.acc = 0;
    const f = { t, b: R.boats.map(b => { const s = b.S; return [s.x, s.y, s.h, s.heel, s.u, s.dispBoom, s.boom, s.boomSide, s.capsized ? 1 : 0, s.hike || 0]; }) };
    riv.roll.push(f); while (f.t - riv.roll[0].t > RIV_PRIMA) riv.roll.shift();
    for (const p of riv.pend) p.frames.push(f);
    riv.pend = riv.pend.filter(p => { if (t < p.fine) return true; rivPush(p); return false; });
  }
  function rivPush(p){
    riv.snips.push(p);
    while (riv.snips.length > RIV_MAX){ const k = riv.snips.findIndex(s => s.auto); riv.snips.splice(k < 0 ? 0 : k, 1); }
    riv.snips.sort((a, b) => a.t - b.t);
  }
  function rivMark(label, auto){ // false se non si può (non in gara, troppo presto, troppi automatici)
    if (!R || R.phase !== "race" || riv.roll.length < 2) return false;
    if (auto){ if (riv.nAuto >= RIV_AUTO_MAX || riv.pend.length) return false; riv.nAuto++; } else riv.nMan++;
    riv.pend.push({ label, auto, t: R.t, fine: R.t + RIV_DOPO, frames: riv.roll.slice() });
    return true;
  }
  addEventListener("keydown", e => {
    if (riv.on || e.repeat || e.key.toLowerCase() !== "o" || e.ctrlKey || e.metaKey || e.altKey || mode !== "race" || sesTyping()) return;
    if (rivMark("Il tuo segno n. " + (riv.nMan + 1) + ", a " + rivTempo(R ? R.t : 0), false)) toast("Momento segnato: lo rivedi a fine regata");
  });

  // ---- riproduzione ----
  const rivSnip = () => riv.snips[riv.i], rivDur = () => { const f = rivSnip().frames; return f[f.length - 1].t - f[0].t; };
  function rivApri(){
    for (const p of riv.pend) rivPush(p); riv.pend = [];       // spezzoni rimasti aperti all'arrivo: si chiudono con quello che c'è
    if (!riv.snips.length || riv.on) return;
    const arrs = new Set(R.boats.map(b => b.wake).concat([wake]));
    riv.bk = { S: R.boats.map(b => Object.assign({}, b.S)), wake: new Map([...arrs].map(a => [a, a.splice(0)])) }; // scie nascoste: non coincidono con le posizioni registrate
    releaseKeys(); riv.on = true; riv.i = 0; riv.pos = 0; riv.playing = true;
    $("finOv").hidden = true; $("movBar").hidden = false; document.querySelector(".panel").classList.remove("fin");
    rivMostra(); $("movEsc").focus();
  }
  function rivChiudi(){
    if (!riv.on) return;
    R.boats.forEach((b, k) => Object.assign(b.S, riv.bk.S[k]));
    riv.bk.wake.forEach((items, a) => a.push(...items)); riv.bk = null;
    riv.on = false; $("movBar").hidden = true; releaseKeys(); finShow();
  }
  function rivApplica(){
    const sn = rivSnip(), fr = sn.frames, T = fr[0].t + clamp(riv.pos, 0, rivDur());
    let i = 0; while (i < fr.length - 2 && fr[i + 1].t < T) i++;
    const a = fr[i], b = fr[Math.min(i + 1, fr.length - 1)], f = b.t > a.t ? clamp((T - a.t) / (b.t - a.t), 0, 1) : 0;
    const L = (p, q) => p + (q - p) * f;
    R.boats.forEach((bt, k) => {
      const p = a.b[k], q = b.b[k], s = bt.S, n = f < 0.5 ? p : q;
      s.x = L(p[0], q[0]); s.y = L(p[1], q[1]); s.h = norm360(p[2] + norm180(q[2] - p[2]) * f); s.heel = L(p[3], q[3]); s.u = L(p[4], q[4]);
      s.dispBoom = L(p[5], q[5]); s.boom = L(p[6], q[6]); s.boomSide = n[7]; s.capsized = !!n[8]; s.hike = n[9];
    });
    $("movPos").value = Math.round(1000 * riv.pos / Math.max(0.1, rivDur()));
    $("movT").textContent = (T - sn.t >= 0 ? "+" : "−") + Math.abs(T - sn.t).toFixed(1) + " s";
  }
  function rivMostra(){
    const sn = rivSnip();
    $("movTit").textContent = "Momento " + (riv.i + 1) + " di " + riv.snips.length + " — " + sn.label;
    $("movPlay").textContent = riv.playing ? "Pausa" : "Riprendi"; $("movSpd").textContent = riv.speed === 1 ? "1×" : riv.speed === 0.5 ? "½×" : "¼×";
    $("movPrev").disabled = riv.i === 0; $("movNext").disabled = riv.i === riv.snips.length - 1;
    rivApplica();
  }
  function rivTick(dt){ // chiamata dal ciclo del gioco al posto della simulazione
    if (riv.playing){ riv.pos += dt * riv.speed; if (riv.pos > rivDur() + 1) riv.pos = 0; }
    rivApplica();
  }
  const rivVai = d => { const j = riv.i + d; if (j < 0 || j >= riv.snips.length) return; riv.i = j; riv.pos = 0; rivMostra(); };
  const rivPausa = () => { riv.playing = !riv.playing; rivMostra(); };
  const rivVel = v => { riv.speed = v; rivMostra(); };
  $("finRev").onclick = rivApri; $("movEsc").onclick = rivChiudi; $("movPrev").onclick = () => rivVai(-1); $("movNext").onclick = () => rivVai(1);
  $("movPlay").onclick = rivPausa; $("movSpd").onclick = () => rivVel(riv.speed === 1 ? 0.5 : riv.speed === 0.5 ? 0.25 : 1);
  $("movPos").oninput = e => { riv.playing = false; riv.pos = e.target.value / 1000 * rivDur(); rivMostra(); };
  addEventListener("keydown", e => { // durante la moviola i tasti sono solo suoi: la barca non si guida
    if (!riv.on) return;
    e.stopPropagation();
    const tag = e.target.tagName, fuoco = tag === "BUTTON" || tag === "INPUT";
    if (e.key === "Escape"){ e.preventDefault(); rivChiudi(); }
    else if (fuoco) return;
    else if (e.key === "ArrowLeft"){ e.preventDefault(); rivVai(-1); }
    else if (e.key === "ArrowRight"){ e.preventDefault(); rivVai(1); }
    else if (e.key === " "){ e.preventDefault(); rivPausa(); }
    else if (e.key === "1" || e.key === "2" || e.key === "3"){ rivVel([1, 0.5, 0.25][+e.key - 1]); }
    else if (e.key.toLowerCase() === "r"){ riv.pos = 0; rivMostra(); }
  }, true);
