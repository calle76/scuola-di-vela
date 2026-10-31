# Collaudo del riquadro delle bandiere e delle penalità (1.0.70, docs/PROPOSTA-RIQUADRO-BANDIERE.md). Soglie scritte nella proposta prima di misurare.
# Uso: .venv-collaudi/bin/python tests/collaudo_riquadro_bandiere.py
# Il metro legge i PIXEL disegnati (tre punti per bandiera, che distinguono le quattro bandiere fra loro), non solo lo stato del gioco; ogni controllo conta i casi misurati
# e fallisce se ne ha visti troppo pochi. Parti:
#  Q1 bandiere nel riquadro = tabella indipendente (1, 3 e 5 minuti), visibili 10 s dopo ogni cambio, pixel giusti; Q2 la X: partenza anticipata vera sì, ritorno prima dello sparo no;
#  Q3 avviso «oltre la linea» (solo con i Suggerimenti), mai in contraddizione con la X; Q4 penalità: giri da fare, fatti, scontata, motivo del contatto, giro nel verso opposto;
#  Q5 sparisce; Q6 le altre regate identiche al bit e la regata dei giri identica nella fisica (alla 1.0.69); Q7 costo del disegno; Q8 posto a 1360x650 e 1360x768; Q9 pagina senza #collaudo.
import asyncio, pathlib, sys, os, subprocess, tempfile, statistics
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
RIF = "c90725d"  # 1.0.69, l'ultima versione senza riquadro
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# lettura dei pixel: tre punti per bandiera (centro, angolo in alto a sinistra, metà del lato alto); ogni tipo ha la sua terna di colori e il metro deve riconoscere ESATTAMENTE il tipo atteso
PIX = """const pixBandiere = (dati) => {
  const c = document.querySelector('canvas'), g = c.getContext('2d'), k = c.width / W, r = __sv.rqRect, out = [];
  if (!r) return out;
  const px = (x, y) => { const d = g.getImageData(Math.round(x * k), Math.round(y * k), 1, 1).data; return [d[0], d[1], d[2]]; };
  const blu = p => Math.abs(p[0] - 31) < 14 && Math.abs(p[1] - 79) < 14 && Math.abs(p[2] - 163) < 14, bia = p => p[0] > 235 && p[1] > 235 && p[2] > 235;
  dati.flag.forEach((t, i) => { const cx = r[0] + 10 + i * 54 + 22, cy = r[1] + 10 + 15, c0 = px(cx, cy), cc = px(cx - 18, cy - 11), ct = px(cx, cy - 12);
    const T = { classe: [blu(c0), bia(cc), bia(ct)], P: [bia(c0), blu(cc), blu(ct)], X: [blu(c0), bia(cc), blu(ct)], blu: [blu(c0), blu(cc), blu(ct)] };
    const quali = Object.keys(T).filter(n => T[n].every(Boolean)); out.push([t, quali.length === 1 && quali[0] === t]); });
  return out;
};"""
# scena: regata dei giri, senza avversari, la barca resta dove la mettiamo (wy = distanza dalla linea, + dietro, - oltre) secondo i piani [[t da cui vale, wy]]; campione ogni 0,1 s
SCENA = PIX + """
async ([cd, seme, hint, piani, tfine, disegna]) => {
  const sv = __sv, dt = 1 / 60; opt.hint = hint; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const sel = document.getElementById('cdSel'); sel.value = String(cd); sel.dispatchEvent(new Event('change')); __seed(seme);
  const R = sv.R, me = R.boats[0]; if (R.cd !== cd) return { errore: 'cd ' + R.cd };
  const out = []; let k = 0, wy = piani[0][1];
  while (R.t < tfine){ for (const [t0, w] of piani) if (R.t >= t0) wy = w; const [px, py] = fromWF(0, wy); sv.S.x = px; sv.S.y = py; sv.S.u = 0; sv.ctl.tiller = 0; sv.run(dt, 1);
    if (k++ % 6 === 0){ const d = sv.riquadro, f = bandiereR(); if (disegna || d) sv.draw(0.016);
      out.push({ t: R.t, vis: !!d, flag: d ? d.flag : [], righe: d ? d.righe.map(r => r[0]) : [], senso: d ? d.senso : null, X: f.X, ocs: me.ocs, wy, rect: !!sv.rqRect || !!sv.rqRect2, pix: d && d.flag.length ? pixBandiere(d) : [] }); } }
  return { out };
}"""
# penalità: pilota fino a 25 s, poi giriDebito() e timone tutto da una parte; si campiona ogni 0,5 s
PEN = """async ([caso, dir, seme]) => {
  const sv = __sv, dt = 1 / 60; opt.hint = true; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0]; while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); }
  giriDebito(); const t0 = R.t, out = []; let cap = false, k = 0, rot = 0, hp = sv.S.h, fase = 0, tOpp = null;
  const camp = () => { if (k++ % 30 === 0){ const d = sv.riquadro; out.push({ t: R.t - t0, righe: d ? d.righe.map(r => r[0]) : null, done: R.done, need: R.need }); } };
  const gira = d => { sv.ctl.tiller = d; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); if (sv.S.capsized) cap = true; camp(); };
  if (caso === 'due'){ while (R.t < t0 + 90 && R.done < R.need && !cap) gira(dir); for (let j = 0; j < 60 * 9; j++){ sv.pilota(dt); sv.run(dt, 1); camp(); } }
  else { while (R.t < t0 + 60 && R.done < 1 && !cap) gira(dir); hp = sv.S.h; while (R.t < t0 + 120 && Math.abs(rot) < 400 && !cap){ gira(-dir); rot += norm180(sv.S.h - hp); hp = sv.S.h; } }
  return { out, cap, done: R.done, need: R.need };
}"""
CONTATTO = """async ([lato, seme]) => {
  const sv = __sv, dt = 1 / 60; opt.hint = true; const lv = document.getElementById('aiLevel'); lv.value = 'principianti'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, me = R.boats[0], o = R.boats[1]; while (R.t < 30){ sv.pilota(dt); sv.run(dt, 1); }
  const need0 = R.need, deb0 = R.need - R.done; o.S.h = me.S.h; o.S.u = me.S.u; o.S.x = me.S.x + lato; o.S.y = me.S.y;
  for (let k = 0; k < 3; k++){ sv.pilota(dt); sv.run(dt, 1); }
  const d = sv.riquadro; return { inc: R.need - need0, deb0, righe: d ? d.righe.map(r => r[0]) : null };
}"""
ALTRE = """async ([n, seme0]) => {
  const sv = __sv, dt = 1 / 60, out = [];
  for (let j = 0; j < n; j++){
    __seed(seme0 + j); sv.simTime = 0; sv.fast(0); sv.openItem(["r", j % 4]);
    const R = sv.R, me = R.boats[0]; let np = 0;
    while (R.t < 1500 && me.fin === null && !me.dnf){ sv.pilota(dt); sv.run(dt, 1); np++; }
    out.push({ fin: R.boats.map(b => b.fin), pen: R.penList.length, pp: R.boats.map(b => b.pp || 0), fine: R.boats.map(b => [Math.round(b.S.x * 1000), Math.round(b.S.y * 1000), Math.round(b.S.h * 1000)]), passi: np });
  }
  return out;
}"""
SCHERMATA = """async ([idx, seme]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", idx]);
  const R = sv.R; while (R.t < -30){ sv.ctl.tiller = 0; sv.run(dt, 1); }
  sv.S.x = R.cb.x + 7; sv.S.y = R.cb.y + 9; sv.S.u = 0; sv.draw(0.016);
  return document.querySelector('canvas').toDataURL();
}"""
# costo: a blocchi alternati, riquadro visibile e nascosto (si nasconde mettendo l'ultimo cambio lontano nel tempo); tempo di sv.draw in ms
COSTO = """async () => {
  const sv = __sv, dt = 1 / 60; opt.hint = true; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(3); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const sel = document.getElementById('cdSel'); sel.value = '300'; sel.dispatchEvent(new Event('change')); __seed(3);
  const R = sv.R; const [px, py] = fromWF(0, -6); while (R.t < -280){ sv.S.x = px; sv.S.y = py; sv.S.u = 0; sv.run(dt, 1); }
  R.need = 3; R.done = 1; R.rqMotivo = 'contatto con la Rossa'; R.boats[0].sconta = true; for (let i = 0; i < 30; i++) sv.draw(0.016);
  const tvis = R.rqT, mis = { vis: [], nasc: [] };
  for (let b = 0; b < 12; b++){ const vis = b % 2 === 0; R.rqT = vis ? R.t : -1e9; R.rqScont = null; if (!vis){ R.need = 0; R.done = 0; R.boats[0].sconta = false; opt.hint = false; } else { R.need = 3; R.done = 1; R.boats[0].sconta = true; opt.hint = true; }
    if (vis){ R.rqT = R.t; }
    const t0 = performance.now(); for (let i = 0; i < 100; i++){ if (vis) R.rqT = R.t; sv.draw(0.016); } const dtm = (performance.now() - t0) / 100;
    if (vis !== (!!sv.rqRect || !!sv.rqRect2)) return { errore: 'blocco ' + b + ': visibilità ' + vis + ' rect ' + (!!sv.rqRect || !!sv.rqRect2) };
    mis[vis ? 'vis' : 'nasc'].push(dtm); }
  return mis;
}"""
# posto: due stati al caso peggiore (prima e dopo lo sparo), rettangoli letti dal disegno
POSTO = """async (hs) => {
  const sv = __sv, dt = 1 / 60; opt.hint = true; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(2); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const sel = document.getElementById('cdSel'); sel.value = '300'; sel.dispatchEvent(new Event('change')); __seed(2);
  const R = sv.R, out = {}; const [px, py] = fromWF(0, -6);
  while (R.t < -55){ sv.S.x = px; sv.S.y = py; sv.S.u = 0; sv.run(dt, 1); }
  R.need = 3; R.done = 1; R.rqMotivo = 'toccata la barca del comitato'; R.boats[0].sconta = true; sv.draw(0.016); out.pre = [sv.rqRect, sv.rqRect2];
  while (R.t < 2){ sv.S.x = px; sv.S.y = py; sv.S.u = 0; sv.run(dt, 1); } sv.draw(0.016); out.post = [sv.rqRect, sv.rqRect2];
  const c = document.querySelector('canvas'); out.W = W; out.H = H; out.cw = c.width; out.ch = c.height; return out;
}"""
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
def atteso(t, cd):  # tabella delle bandiere senza richiamo: (classe, P, X, blu); nessuna dipendenza dal codice del gioco
    return (-cd <= t < 0, cd >= 180 and -(cd - 60) <= t < -60, False, t >= 0)
def cambi(cd):  # istanti in cui la tabella cambia
    return [-cd] + ([-(cd - 60)] if cd >= 180 else []) + [-60 if cd >= 180 else None, 0]
async def pagina(b, base, hash_="#collaudo", vp=(1360, 650)):
    ctx = await b.new_context(viewport={"width": vp[0], "height": vp[1]}); await ctx.add_init_script(SEME)
    pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(pathlib.Path(base, "index.html").as_uri() + hash_); await pg.wait_for_timeout(250)
    return ctx, pg, errs
def solo_pezzi(r): return [x for x in r if x]
async def main():
    rif = pathlib.Path(tempfile.mkdtemp()); a = subprocess.run(["git", "-C", str(ROOT), "archive", RIF], capture_output=True)
    subprocess.run(["tar", "-x", "-C", str(rif)], input=a.stdout, check=True)
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx, pg, errs = await pagina(b, ROOT)
        # ---- Q1 ----
        n = nvis = nerr = npix = 0; tipi = set(); dett = []
        for cd in (60, 180, 300):
            camb = sorted({-cd, 0} | ({-(cd - 60), -60} if cd >= 180 else set()))
            for seme in (1, 2, 3):
                r = await pg.evaluate(SCENA, [cd, seme * 10, True, [[-1e9, 12]], 3, False])
                if "errore" in r: dett.append(r["errore"]); nerr += 1; continue
                for s in r["out"]:
                    t = s["t"]; esp = atteso(t, cd); n += 1; nomi = [nm for nm, v in zip(("classe", "P", "X", "blu"), esp) if v]
                    ult = max([c for c in camb if c <= t + 1e-6], default=None)   # ultimo cambio della tabella
                    # con la barca dietro la linea e senza debiti la sola ragione per vedere il riquadro sono le bandiere cambiate da meno di 10 s
                    if nomi and ult is not None and t - ult < 9.8:
                        nvis += 1
                        if not s["vis"] or s["flag"] != nomi or [x[0] for x in s["pix"]] != nomi or not all(x[1] for x in s["pix"]): nerr += 1; dett.append((cd, round(t, 2), nomi, s["flag"], s["pix"]))
                        else: npix += len(s["pix"]); tipi.update(nomi)
                    elif ult is None or t - ult > 10.3:
                        if s["vis"]: nerr += 1; dett.append((cd, round(t, 2), "riquadro dopo 10 s", s["righe"], s["flag"]))
        chk("Q1 le bandiere del riquadro sono quelle della tabella e i pixel dicono lo stesso (1, 3 e 5 minuti, 3 regate ciascuna): %d campioni, %d con riquadro, %d bandiere verificate sui pixel, errori %d" % (n, nvis, npix, nerr), nerr == 0 and nvis >= 300 and tipi == {"classe", "P", "blu"}, "tipi visti " + str(sorted(tipi)) + " " + str(dett[:3]))
        # ---- Q2 e Q3 ----
        errA = []; errB = []; errC = []; nA = nB = nAv = nAvSpento = 0
        for k in range(20):  # A: si passa la linea e si torna dietro PRIMA dello sparo (a -40...-30 s, e per 8 s)
            t_in = -40 + 0.5 * k; r = await pg.evaluate(SCENA, [60, 100 + k, True, [[-1e9, 12], [t_in, -6], [t_in + 8, 8]], 4, True]); nA += 1
            for s in r["out"]:
                if s["X"] or "X" in s["flag"]: errA.append((k, round(s["t"], 2), "X"))
                over = t_in <= s["t"] < t_in + 8
                av = any(x.startswith("Oltre la linea") for x in s["righe"]); nAv += over and s["t"] > -59
                if abs(s["t"] - t_in) > 0.2 and abs(s["t"] - t_in - 8) > 0.2 and s["t"] < -1 and av != over: errC.append((k, round(s["t"], 2), av, over))
            r2 = await pg.evaluate(SCENA, [60, 100 + k, False, [[-1e9, 12], [t_in, -6], [t_in + 8, 8]], 4, False]); nAvSpento += 1
            if any(any(x.startswith("Oltre la linea") for x in s["righe"]) for s in r2["out"]): errC.append((k, "avviso con i Suggerimenti spenti"))
        for k in range(20):  # B: si passa la linea a -9,5...-0,5 s e si resta oltre (partenza anticipata vera); a +12 s si torna dietro
            t_in = -9.5 + 0.45 * k; r = await pg.evaluate(SCENA, [60, 200 + k, True, [[-1e9, 12], [t_in, -6], [12, 8]], 18, True]); nB += 1
            dopo = [s for s in r["out"] if 0.3 <= s["t"] <= 11.7]; fuori = [s for s in r["out"] if s["t"] >= 12.6]
            if not dopo or not all(s["X"] and "X" in s["flag"] and all(x[1] for x in s["pix"]) and any(x.startswith("X: ") for x in s["righe"]) for s in dopo): errB.append((k, "X mancante dopo lo sparo"))
            if any(s["X"] or "X" in s["flag"] for s in fuori): errB.append((k, "X ancora su dopo il ritorno"))
            pre = [s for s in r["out"] if -1 < s["t"] < 0]
            if any(any(x.startswith("Oltre la linea") for x in s["righe"]) for s in r["out"] if s["t"] >= 0.2): errC.append((k, "avviso dopo lo sparo"))
            if any(s["t"] >= 0.3 and not s["ocs"] for s in dopo): errB.append((k, "ocs falso"))
        chk("Q2a passare la linea e tornare dietro prima dello sparo: nessuna X (20 regate, passaggio da -40 a -30 s)", nA == 20 and not errA, str(errA[:3]))
        chk("Q2b partenza anticipata vera (passaggio da -9,5 a -1 s, resta oltre): X nel riquadro con i pixel giusti in tutti i campioni dopo lo sparo e tolta dopo il ritorno (20 regate)", nB == 20 and not errB, str(errB[:3]))
        chk("Q3a l'avviso «oltre la linea» c'è quando la barca è oltre e non c'è quando è dietro (20 regate; %d campioni con barca oltre) e mai dopo lo sparo" % nAv, nAv >= 200 and not [e for e in errC if len(e) == 4 or e[1] == "avviso dopo lo sparo"], str(errC[:3]))
        chk("Q3b con i Suggerimenti spenti l'avviso non c'è mai (20 regate)", nAvSpento == 20 and not [e for e in errC if len(e) == 2 and e[1] != "avviso dopo lo sparo"], str(errC[:3]))
        # ---- Q4 ----
        ok4 = []; ris = {}
        for caso, dir_ in (("due", 1), ("due", -1), ("opposto", 1), ("opposto", -1)):
            for seme in (1, 2, 3):
                r = await pg.evaluate(PEN, [caso, dir_, seme]); ris[(caso, dir_, seme)] = r
        def testi(r): return [s for s in r["out"] if s["righe"]]
        due = [r for (c, d, s), r in ris.items() if c == "due"]; opp = [r for (c, d, s), r in ris.items() if c == "opposto"]
        primi = [any(x.startswith("Penalità: 2 giri da fare") for s in testi(r) for x in s["righe"]) for r in due if not r["cap"]]
        sec = [any(x.startswith("Penalità: 1 giro da fare · fatti 1") for s in testi(r) for x in s["righe"]) for r in due if not r["cap"]]
        scon = [any(x == "Penalità scontata" for s in testi(r) for x in s["righe"]) for r in due if not r["cap"]]
        dopo = [all(not any(x == "Penalità scontata" for x in (s["righe"] or [])) for s in r["out"] if s["t"] > r["out"][-1]["t"] - 2) for r in due if not r["cap"]]
        mai_scont = [not any(x == "Penalità scontata" for s in testi(r) for x in s["righe"]) for r in opp if not r["cap"]]
        chk("Q4a debito di due giri: il riquadro dice «2 giri da fare», poi «1 giro da fare · fatti 1», poi «Penalità scontata» (%d prove senza scuffia)" % len(primi), len(primi) >= 4 and all(primi) and all(sec) and all(scon), str((primi, sec, scon)))
        chk("Q4b la scritta «Penalità scontata» sparisce entro 6 s dopo averla mostrata (negli ultimi 2 s delle prove non c'è)", len(dopo) >= 4 and all(dopo))
        chk("Q4c un giro in un verso e una rotazione di 400° nell'altro: mai «Penalità scontata» (%d prove senza scuffia)" % len(mai_scont), len(mai_scont) >= 3 and all(mai_scont))
        mot = []
        for lato in (1.2, -1.2):
            for seme in range(1, 11):
                r = await pg.evaluate(CONTATTO, [lato, seme]); mot.append(r)
        conc = [r for r in mot if r["inc"] >= 1]
        chk("Q4d contatto con colpa del giocatore (debito di due giri): il riquadro dice il motivo «Per: contatto con la …» (%d casi con colpa su %d)" % (len(conc), len(mot)), len(conc) >= 2 and all(r["righe"] and any(x.startswith("Per: contatto con la ") for x in r["righe"]) for r in conc), str(mot[:2]))
        senza = [r for r in mot if r["inc"] == 0 and r["deb0"] == 0]
        chk("Q4e quando la colpa non è del giocatore e non c'è debito, il riquadro non parla di penalità (%d casi su %d; ne servono almeno 2, se no il metro non ha misurato)" % (len(senza), len(mot)), len(senza) >= 2 and all(not r["righe"] or not any(x.startswith("Penalità") for x in r["righe"]) for r in senza))
        # ---- Q5 ----
        r = await pg.evaluate(SCENA, [60, 7, True, [[-1e9, 12]], 30, True])
        dopo10 = [s for s in r["out"] if s["t"] > -60 + 10.4 and s["t"] < -0.5]; dopo10b = [s for s in r["out"] if s["t"] > 10.4]
        chk("Q5 senza novità né debiti il riquadro sparisce dopo 10 s (%d campioni, tutti senza riquadro e senza rettangoli disegnati)" % (len(dopo10) + len(dopo10b)), len(dopo10) > 100 and len(dopo10b) > 100 and not any(s["vis"] or s["rect"] for s in dopo10 + dopo10b))
        await ctx.close()
        # ---- Q6 ----
        async def altre(base):
            c, g, e = await pagina(b, base); o = await g.evaluate(ALTRE, [20, 100]); await c.close(); return o
        nuovo = await altre(ROOT); vecchio = await altre(rif)
        chk("Q6a 20 regate (1a, 1b, salti di vento e regata dei giri): arrivi, penalità e posizioni finali identici al bit alla 1.0.69", nuovo == vecchio and len(nuovo) == 20)
        async def schermate(base):
            o = {}
            for i in (0, 2):
                c, g, e = await pagina(b, base); o[i] = await g.evaluate(SCHERMATA, [i, 9]); await c.close()
            return o
        sn = await schermate(ROOT); sv_ = await schermate(rif)
        ctxp, pgp, _ = await pagina(b, ROOT)
        diff = await pgp.evaluate("""async ([a0, a2, b0, b2]) => {
          const carica = u => new Promise(r => { const i = new Image(); i.onload = () => { const c = document.createElement('canvas'); c.width = i.width; c.height = i.height; const g = c.getContext('2d'); g.drawImage(i, 0, 0); r(g.getImageData(0, 0, c.width, c.height)); }; i.src = u; });
          const conf = async (u, v) => { const A = await carica(u), B = await carica(v); let fuori = 0, dentro = 0; for (let y = 0; y < A.height; y++) for (let x = 0; x < A.width; x++){ const k = 4 * (y * A.width + x); if (A.data[k] !== B.data[k] || A.data[k + 1] !== B.data[k + 1] || A.data[k + 2] !== B.data[k + 2]){ const zona = (x > A.width - 330 && y > A.height - 50) || (x < 130 && y > 30 && y < 56) || (x > A.width - 260 && y > 80 && y < 104) || (Math.abs(x - A.width / 2) < 250 && y > 230 && y < 540); if (zona) dentro++; else fuori++; } } return [fuori, dentro]; };
          return [await conf(a0, b0), await conf(a2, b2)]; }""", [sn[0], sn[2], sv_[0], sv_[2]])
        await ctxp.close()
        chk("Q6b la schermata a -30 s della regata 1a e della 1b è identica al pixel alla 1.0.69 fuori dalle zone del vento (in basso a destra, dov'è ora; in alto a destra, dov'era), delle vecchie scritte «Q vista» e «1 / 2 zoom» della vecchia spia in alto a sinistra e dell'area attorno alla barca (frecce senza nomi, senza banderuola) (pixel diversi fuori / dentro quelle zone: 1a %s, 1b %s; il metro deve vedere almeno una differenza nelle zone)" % (diff[0], diff[1]), diff[0][0] == 0 and diff[1][0] == 0 and diff[0][1] > 0 and diff[1][1] > 0)
        # ---- Q7 ----
        ctx, pg, errs = await pagina(b, ROOT)
        c = await pg.evaluate(COSTO)
        if "errore" in c: chk("Q7 costo del disegno", False, c["errore"])
        else:
            mv, mn = statistics.median(c["vis"]), statistics.median(c["nasc"]); diff = mv - mn
            chk("Q7 costo del disegno con riquadro (mediana %.3f ms) contro senza (%.3f ms): differenza %.3f ms, %.1f%% (soglie: 0,2 ms e 3%%; 6 blocchi da 100 fotogrammi per parte, alternati)" % (mv, mn, diff, 100 * diff / mn if mn else 0), diff <= 0.2 or diff / mn <= 0.03, "(il rumore fra blocchi è %.3f ms)" % (max(c["vis"] + c["nasc"]) - min(c["vis"] + c["nasc"])))
        await ctx.close()
        # ---- Q8 ----
        for vp in ((1360, 650), (1360, 768)):
            ctx, pg, errs = await pagina(b, ROOT, vp=vp); pz = await pg.evaluate(POSTO, vp[1]); await ctx.close()
            Wc, Hc = pz["W"], pz["H"]; probl = []
            ostacoli = {"bussola": [Wc - 26 - 16 - 30, 18, 60, 62], "orologio (e la riga «non sei partito»)": [Wc / 2 - 250, 0, 500, 100], "messaggio al centro (fino a 500 px)": [Wc / 2 - 250, 100, 500, 36], "vento e R in basso a destra": [Wc - 260, Hc - 40, 260, 40], "indicatori in basso a sinistra": [0, Hc - 110, 260, 110]}
            for nome_s, rr in (("prima dello sparo", pz["pre"]), ("dopo lo sparo", pz["post"])):
                for rect in solo_pezzi(rr):
                    x, y, w, h = rect
                    if x < 0 or y < 0 or x + w > Wc or y + h > Hc: probl.append((nome_s, "fuori dal mare", rect))
                    for on, (ox, oy, ow, oh) in ostacoli.items():
                        if x < ox + ow and ox < x + w and y < oy + oh and oy < y + h: probl.append((nome_s, on, rect))
            chk("Q8 %dx%d: i due pezzi del riquadro (caso peggiore, prima e dopo lo sparo) stanno nel mare e non toccano bussola, orologio e messaggio, vento, indicatori (canvas %dx%d); rettangoli: %s" % (vp[0], vp[1], Wc, Hc, [ [round(v) for v in r] for r in solo_pezzi(pz["pre"]) + solo_pezzi(pz["post"])]), len(solo_pezzi(pz["pre"])) == 2 and len(solo_pezzi(pz["post"])) == 2 and not probl, str(probl[:3]))
        # ---- Q9 ----
        ctx, pg, errs = await pagina(b, ROOT, "")
        await pg.click("#menu [data-r='3']"); await pg.wait_for_timeout(300); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1500)
        h = await pg.evaluate("() => { const d = R && R.segnali ? rqDati() : null; return { flag: d ? d.flag : null, r: R ? R.rqRect : null }; }")
        chk("Q9 pagina senza #collaudo: la regata dei giri si apre e il riquadro mostra la bandiera di classe, disegnato", h["flag"] == ["classe"] and h["r"] is not None, str(h))
        await pg.wait_for_timeout(1000)
        chk("Q9b nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
