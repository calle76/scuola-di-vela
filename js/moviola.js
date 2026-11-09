// Scuola di vela, moviola.js — «Rivedi»: tutta la regata registrata in memoria, con i segni (tasto O, contatti, boe), e riproduzione a fine gara (1.0.58; regata intera dalla 1.0.76).
// Dalla 1.0.3 il gioco è diviso in file caricati in ordine da index.html (script classici, variabili condivise): vedi docs/archivio/PROPOSTA-DIVISIONE-CODICE.md.

  // ======================================================================
  // MOVIOLA (1.0.58; dalla 1.0.76 tutta la regata, docs/PROPOSTA-MOVIOLA-INTERA.md)
  // Solo lettura sulla simulazione: dal conto alla rovescia all'arrivo (o al ritiro) del giocatore copia le posizioni di tutte le barche
  // a 10 al secondo, non chiama Math.random e non scrive nel gioco. Il tasto O, ogni contatto e ogni boa toccata mettono un SEGNO
  // (un orario e una scritta), anche prima del via. A fine regata «Rivedi» riproduce tutta la regata a gioco fermo, sostituendo per un
  // attimo lo stato delle barche (come drawOther) e rimettendolo a posto all'uscita. Costanti (ipotesi nostre): 10 campioni/s, al
  // massimo 60 minuti (oltre si tengono gli ultimi 60), 10 s prima del segno quando ci si salta, passo delle frecce 5 s.
  // Fino alla 1.0.75: spezzoni di 18 s (10 prima e 8 dopo il segno), al massimo 12, solo dopo lo sparo.
  // ======================================================================
  const RIV_DT = 0.1, RIV_MAX_F = 36000, RIV_PRIMA = 10, RIV_PASSO = 5, RIV_VEL = [1, 0.5, 0.25, 4, 8];
  const riv = { all: [], segni: [], acc: 0, nMan: 0, on: false, pos: 0, speed: 1, playing: true, bk: null, tagliata: false, fine: null };
  const rivTempo = t => { const s = Math.floor(Math.abs(t)); return (t < 0 ? "−" : "") + Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); };
  const rivCount = () => riv.all.length > 1 ? 1 : 0;   // per il pulsante Rivedi: c'è qualcosa da rivedere

  // ---- registrazione ----
  function rivReset(){ riv.all = []; riv.segni = []; riv.acc = 0; riv.nMan = 0; riv.tagliata = false; riv.fine = null; }
  function rivCapture(t, dt){ // a ogni passo della regata, dal conto alla rovescia finché il giocatore non ha finito (o si è ritirato)
    if (!R || (R.phase !== "pre" && R.phase !== "race")) return;
    if (riv.fine === R) return;   // dopo l'arrivo del giocatore non si copia più
    const me = R.boats[0], ultimo = me.fin !== null || me.dnf;
    riv.acc += dt; if (riv.acc < RIV_DT && !ultimo && riv.all.length) return; riv.acc = 0;
    riv.all.push({ t, b: R.boats.map(b => { const s = b.S; return [s.x, s.y, s.h, s.heel, s.u, s.dispBoom, s.boom, s.boomSide, s.capsized ? 1 : 0, s.hike || 0]; }) });
    if (riv.all.length > RIV_MAX_F){ riv.all.shift(); riv.tagliata = true; }
    if (ultimo) riv.fine = R;
  }
  function rivMark(label, auto){ // un segno sulla regata; false se non si può (non in regata, o già finita per il giocatore)
    if (!R || (R.phase !== "pre" && R.phase !== "race") || riv.fine === R) return false;
    if (!auto) riv.nMan++;
    riv.segni.push({ label, auto, t: R.t });
    return true;
  }
  addEventListener("keydown", e => {
    if (riv.on || e.repeat || e.key.toLowerCase() !== "o" || e.ctrlKey || e.metaKey || e.altKey || mode !== "race" || sesTyping()) return;
    if (rivMark("Il tuo segno n. " + (riv.nMan + 1) + ", a " + rivTempo(R ? R.t : 0), false)){ toast("Momento segnato: lo rivedi a fine regata"); if (ses.on) sesEv("segno_rivedi", String(riv.nMan)); } // 1.0.60: lo stesso numero sta nel file della registrazione
  });

  // ---- riproduzione ----
  const rivT0 = () => riv.all[0].t, rivDur = () => riv.all[riv.all.length - 1].t - riv.all[0].t;
  const rivPosDi = t => clamp(t - rivT0(), 0, rivDur());
  function rivApri(){
    if (riv.all.length < 2 || riv.on) return;
    const arrs = new Set(R.boats.map(b => b.wake).concat([wake]));
    riv.bk = { S: R.boats.map(b => Object.assign({}, b.S)), wake: new Map([...arrs].map(a => [a, a.splice(0)])) }; // scie nascoste: non coincidono con le posizioni registrate
    releaseKeys(); riv.on = true; riv.playing = true; riv.speed = 1;
    const primo = riv.segni.find(g => g.t >= rivT0());
    riv.pos = rivPosDi((primo ? primo.t : 0) - RIV_PRIMA);   // si parte 10 s prima del primo segno, o 10 s prima dello sparo
    $("finOv").hidden = true; $("movBar").hidden = false; document.querySelector(".panel").classList.remove("fin");
    rivTacche(); rivMostra(); $("movPlay").focus();   // 1.0.76: il fuoco su Pausa, così lo spazio mette in pausa (su «Chiudi» chiudeva)
  }
  function rivChiudi(){
    if (!riv.on) return;
    R.boats.forEach((b, k) => Object.assign(b.S, riv.bk.S[k]));
    riv.bk.wake.forEach((items, a) => a.push(...items)); riv.bk = null;
    riv.on = false; rot.on = false; $("movBar").hidden = true; releaseKeys(); finShow();
  }
  function rivTacche(){ // un segno = una tacca sul cursore
    const d = Math.max(0.1, rivDur());
    $("movSegni").innerHTML = riv.segni.filter(g => g.t >= rivT0()).map(g => `<i style="left:${(100 * rivPosDi(g.t) / d).toFixed(2)}%" title="${g.label.replace(/"/g, "&quot;")}"></i>`).join("");
  }
  function rivApplica(){
    const fr = riv.all, T = rivT0() + clamp(riv.pos, 0, rivDur());
    let lo = 0, hi = fr.length - 1; while (hi - lo > 1){ const m = (lo + hi) >> 1; if (fr[m].t <= T) lo = m; else hi = m; } // ricerca binaria: la regata intera ha migliaia di copie
    const a = fr[lo], b = fr[hi], f = b.t > a.t ? clamp((T - a.t) / (b.t - a.t), 0, 1) : 0;
    const L = (p, q) => p + (q - p) * f;
    R.boats.forEach((bt, k) => {
      const p = a.b[k], q = b.b[k], s = bt.S, n = f < 0.5 ? p : q;
      s.x = L(p[0], q[0]); s.y = L(p[1], q[1]); s.h = p[8] !== q[8] ? n[2] : norm360(p[2] + norm180(q[2] - p[2]) * f); // 1.2.22: alla scuffiata e alla raddrizzata la prua cambia di colpo, non si mescola (collaudo_moviola V1, 9,84° con la 1.2.21) s.heel = L(p[3], q[3]); s.u = L(p[4], q[4]);
      s.dispBoom = L(p[5], q[5]); s.boom = L(p[6], q[6]); s.boomSide = n[7]; s.capsized = !!n[8]; s.hike = n[9];
    });
    $("movPos").value = Math.round(1000 * riv.pos / Math.max(0.1, rivDur()));
    $("movT").textContent = rivTempo(T) + (riv.tagliata ? " (tenuti gli ultimi 60 minuti)" : "");
    const g = rivSegnoVicino(T);
    $("movTit").textContent = rot.on && rot.res ? rot.res.testo : g ? "Segno " + (riv.segni.indexOf(g) + 1) + " di " + riv.segni.length + " — " + g.label : "Tutta la regata" + (riv.segni.length ? " — " + riv.segni.length + (riv.segni.length === 1 ? " segno" : " segni") + ": ↑ ↓ per saltarci" : "");
    const T0 = T + 0.05;
    $("movPrev").disabled = !riv.segni.some(x => x.t - RIV_PRIMA < T - 0.5); $("movNext").disabled = !riv.segni.some(x => x.t - RIV_PRIMA > T0);
  }
  const rivSegnoVicino = T => { let best = null; for (const g of riv.segni) if (T >= g.t - RIV_PRIMA && T <= g.t + 8) best = g; return best; }; // il segno «in corso»: da 10 s prima a 8 s dopo
  function rivMostra(){
    $("movPlay").textContent = riv.playing ? "Pausa" : "Riprendi";
    $("movSpd").textContent = riv.speed === 0.5 ? "½×" : riv.speed === 0.25 ? "¼×" : riv.speed + "×";
    rivApplica();
  }
  function rivTick(dt){ // chiamata dal ciclo del gioco al posto della simulazione
    if (riv.playing){ riv.pos += dt * riv.speed; if (riv.pos >= rivDur()){ riv.pos = rivDur(); riv.playing = false; rivMostra(); return; } } // alla fine si ferma
    rivApplica();
  }
  const rivSposta = d => { riv.pos = clamp(riv.pos + d, 0, rivDur()); rivMostra(); };
  const rivSegno = d => { // al segno dopo (d = 1) o prima (d = −1), 10 s prima del segno
    const T = rivT0() + riv.pos, ok = riv.segni.filter(g => d > 0 ? g.t - RIV_PRIMA > T + 0.05 : g.t - RIV_PRIMA < T - 0.5);
    if (!ok.length) return; const g = d > 0 ? ok[0] : ok[ok.length - 1]; riv.pos = rivPosDi(g.t - RIV_PRIMA); riv.playing = true; rivMostra(); };
  const rivPausa = () => { if (!riv.playing && riv.pos >= rivDur()) riv.pos = 0; riv.playing = !riv.playing; rivMostra(); };
  const rivVel = v => { riv.speed = v; rivMostra(); };
  $("finRev").onclick = rivApri; $("movEsc").onclick = rivChiudi; $("movPrev").onclick = () => rivSegno(-1); $("movNext").onclick = () => rivSegno(1);
  $("movPlay").onclick = rivPausa; $("movSpd").onclick = () => rivVel(RIV_VEL[(RIV_VEL.indexOf(riv.speed) + 1) % RIV_VEL.length]);
  $("movPos").oninput = e => { if (!riv.on) return; /* 1.0.60: a moviola chiusa il cursore non fa niente (collaudo_ricarica lo sposta lo stesso) */ riv.playing = false; riv.pos = e.target.value / 1000 * rivDur(); rivMostra(); };
  addEventListener("keydown", e => { // durante la moviola i tasti sono solo suoi: la barca non si guida
    if (!riv.on) return;
    e.stopPropagation();
    const tag = e.target.tagName;
    if (e.key === "Escape"){ e.preventDefault(); rivChiudi(); }
    else if (tag === "INPUT" && (e.key === "ArrowLeft" || e.key === "ArrowRight")) return;   // sul cursore le frecce lo muovono da sole
    else if (tag === "BUTTON" && (e.key === " " || e.key === "Enter")) return;               // su un pulsante spazio e Invio lo premono
    else if (e.key === "ArrowLeft"){ e.preventDefault(); rivSposta(-RIV_PASSO); }
    else if (e.key === "ArrowRight"){ e.preventDefault(); rivSposta(RIV_PASSO); }
    else if (e.key === "ArrowUp"){ e.preventDefault(); rivSegno(-1); }
    else if (e.key === "ArrowDown"){ e.preventDefault(); rivSegno(1); }
    else if (e.key === " "){ e.preventDefault(); rivPausa(); }
    else if ("12345".includes(e.key) && e.key.length === 1){ rivVel(RIV_VEL[+e.key - 1]); }
    else if (e.key.toLowerCase() === "r"){ riv.pos = 0; rivMostra(); }
  }, true);
