# Aiuto «scarso / buono» in regata (1.3.42, voce 48, docs/PROPOSTA-AIUTO-SCARSO.md: soglie scritte il 16 nov, prima del codice).
#   S1 con l'aiuto acceso o spento la regata non cambia: regate del torneo identiche al bit (20 in Chromium, 5 in Firefox, come collaudo_campo_q), la pagina disegna
#   S2 il numero scritto è quello della lezione 11: regata nei salti di vento, pilota, 10 semi, un campione al secondo; vento sulla barca letto con windAt
#      nel punto e nell'istante in cui il passo lo legge (dopo lo spostamento delle raffiche, come local), 0 differenze con almeno 500 campioni scritti.
#      Prima stesura (22 nov): windAt prima del passo, cioè prima di updateGusts: 6 diversi su 2139, tutti di 1° all'arrotondamento (difetto del metro)
#   S3 compare solo dove deve: 0 volte nelle regate della Scuola, prima del via, fuori dalla bolina, nel torneo con «regate»; viste tutte e tre le forme.
#      Dalla 1.3.45 (voce 79) nella lezione 11 compare nell'esercizio «Vira sullo scarso» anche con l'opzione spenta, e non negli altri passi (S3e;
#      fino alla 1.3.44 S3e contava 0 scritte, ma la barca restava al traverso e la riga non poteva comparire comunque: il controllo non misurava)
#   S4 spazio: la scritta non tocca bussola, «N» e scritta del vento (rettangoli misurati nella pagina); il pannello e le Impostazioni: collaudo_pannello.py e collaudo_menu_livelli.py
# Uso: python tests/collaudo_aiuto_scarso.py   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = (ROOT / "index.html").as_uri() + "#collaudo"
BR = os.environ.get("BROWSER", "chromium")
N1 = 5 if BR == "firefox" else 20
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();
(() => { const f = CanvasRenderingContext2D.prototype.fillText; window.__scritte = [];
  CanvasRenderingContext2D.prototype.fillText = function(t, x, y, ...r){ if (/^(scarso|buono) \\d+°$|^nella media$/.test(t)) __scritte.push({ t, x, y, w: this.measureText(t).width }); return f.call(this, t, x, y, ...r); }; })();"""
bad = []
def chk(ok, m):
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
S1 = """([seme, on]) => { const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(seme); sv.opt.scarso = on ? "tutte" : "no"; sv.opt.countdown = 60; sv.store = 'scuolaVelaSim.v1';
  sv.torApri(); document.getElementById("torGo").click(); const R = sv.R, me = R.boats[0]; let k = 0;
  while (me.fin === null && !me.dnf && R.t < 1500){ sv.pilota(dt); sv.run(dt, 1); if (++k % 3 === 0) sv.draw(dt); }
  const f = R.boats.map(b => [b.fin, b.pp || 0, !!b.dnf, Math.round(b.S.x * 100), Math.round(b.S.y * 100)].join(',')).join('|'); const n = __scritte.length; document.getElementById("rTor").click(); return [f, n]; }"""
# un campione al secondo: scritta disegnata adesso contro il conto fatto qui
S2 = """([seme, gara, opz]) => { const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(seme); sv.opt.scarso = opz; sv.opt.countdown = 60; sv.simTime = 0;
  if (gara === "tor"){ sv.store = 'scuolaVelaSim.v1'; sv.torApri(); document.getElementById("torGo").click(); } else sv.openItem(["r", gara]);
  const R = sv.R, me = R.boats[0], out = []; let acc = 0;
  while (me.fin === null && !me.dnf && R.t < 900){ const x0 = sv.S.x, y0 = sv.S.y, t0 = simTime; sv.pilota(dt); sv.run(dt, 1);
    if ((acc += dt) >= 1){ const t1 = simTime; sv.simTime = t0; const w = sv.windAt(x0, y0); sv.simTime = t1; acc = 0; __scritte.length = 0; sv.draw(dt); const a = sv.norm180(w.twd - sv.S.h), sc = -Math.sign(a) * sv.norm180(w.twd - sv.envTwd());
      const atteso = sc >= 7 ? "scarso " + Math.round(sc) + "°" : sc <= -3 ? "buono " + (-Math.round(sc)) + "°" : "nella media";
      out.push({ t: R.t, a: Math.abs(a), leg: me.leg, cap: sv.S.capsized, salti: sv.salti(), scritto: __scritte.length ? __scritte[0].t : null, atteso }); } }
  return out; }"""
LEZ = """() => { const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(77); const li = LESSONS.findIndex(l => l.steps.some(s => s.title === "Vira sullo scarso"));
  sv.opt.scarso = "no"; const conta = titolo => { sv.openItem(["l", li]); const si = LESSONS[li].steps.findIndex(s => s.title === titolo); for (let k = 0; k < si; k++) document.getElementById("lNext").click();
    __scritte.length = 0; let n = 0; for (let k = 0; k < 3600; k++){ S.h = norm360(local.twd + 50); S.r = 0; sv.run(dt, 1); if (k % 30 === 0){ __scritte.length = 0; sv.draw(dt); n += __scritte.length; } } return [si, n]; };
  const v = conta("Vira sullo scarso"), r = conta("Riepilogo"); return [li, v[0], v[1], r[1], sv.salti()]; }"""
# rettangoli: scritta contro bussola (cerchio di fondo r + 4), «N» (a r + 9 dal centro, in qualunque verso) e scritta del vento
S4 = """() => { const sv = __sv, dt = 1 / 60; sv.fast(0); __seed(1530); sv.opt.scarso = "tutte"; sv.openItem(["r", 2]); const R = sv.R; let pegg = 1e9, n = 0;
  ctx.save(); ctx.font = font(600, 14); const tw = ctx.measureText(windTesto()).width, cx = W - 16 - tw / 2, cy = H - 18 - 16 - 26 - 4; ctx.restore();
  while (R.t < 400){ sv.pilota(dt); sv.run(dt, 1); if (R.t > 0 && Math.round(R.t * 60) % 30 === 0){ __scritte.length = 0; sv.draw(dt);
    for (const s of __scritte){ n++; const basso = s.y + 4, alto = s.y - 14, sinistra = s.x - s.w / 2, destra = s.x + s.w / 2;
      const daN = cy - 26 - 9 - 7, daFondo = cy - 30, venSu = H - 8 - 14;   /* 1.3.81: la scritta del vento sta 10 px più in basso */
      pegg = Math.min(pegg, daN - basso, daFondo - basso, venSu - basso); if (sinistra < 0 || destra > W) pegg = -1; } } }
  return [n, pegg]; }"""
SOLO = os.environ.get("SOLO", "")
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []
        async def pagina():
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.goto(BASE); await pg.wait_for_timeout(300); return ctx, pg
        async def corsa(js, arg):
            ctx, pg = await pagina(); r = await pg.evaluate(js, arg); await ctx.close(); return r
        # ---- S2 e S3 nella regata nei salti di vento (SOLO=S2: solo questa parte) ----
        campioni = scritti = diversi = 0; fuori = 0; forme = set(); es = []
        for seme in range(1521, 1531):
            for c in await corsa(S2, [seme, 2, "regate"]):
                campioni += 1; dove = c["salti"] and c["t"] >= 0 and c["leg"] >= 1 and not c["cap"] and 35 <= c["a"] <= 75
                if c["scritto"]:
                    scritti += 1; forme.add(c["scritto"].split(" ")[0])
                    if c["scritto"] != c["atteso"]: diversi += 1; es.append(c)
                    if not dove: fuori += 1
                elif dove: fuori += 1; es.append(c)
        chk(scritti >= 500 and diversi == 0, f"S2 numero scritto contro il conto (vento sulla barca, vento medio, prua): {diversi} diversi su {scritti} scritte ({campioni} campioni, 10 regate); esempi {es[:2]}")
        chk(fuori == 0, f"S3a regata nei salti: scritta dove non deve, o assente dove deve, {fuori} su {campioni} campioni (prima del via, fuori bolina, scuffiata, dopo l'arrivo)")
        chk(forme == {"scarso", "buono", "nella"}, f"S3b forme viste: {sorted(forme)} (servono scarso, buono, nella media)")
        if SOLO == "S2": await b.close(); print("casi sbagliati: " + ("nessuno" if not bad else str(len(bad)))); raise SystemExit(1 if bad else 0)
        n0 = 0
        for seme in range(1531, 1536):
            for gara in (0, 1): n0 += sum(1 for c in await corsa(S2, [seme, gara, "tutte"]) if c["scritto"])
        chk(n0 == 0, f"S3c regate della Scuola (bastone e raffiche, vento che non gira, opzione «anche torneo»): {n0} scritte in 10 regate")
        nt = [sum(1 for c in await corsa(S2, [seme, "tor", o]) if c["scritto"]) for seme in (1536, 1537) for o in ("regate", "tutte")]
        chk(nt[0] == 0 and nt[2] == 0 and nt[1] > 0 and nt[3] > 0, f"S3d torneo: con «regate» {nt[0]} e {nt[2]} scritte, con «anche torneo» {nt[1]} e {nt[3]}")
        ctx, pg = await pagina(); r = await pg.evaluate(LEZ); await ctx.close()
        chk(r[0] >= 0 and r[1] >= 0 and r[4] and r[2] > 50 and r[3] == 0, f"S3e lezione 11 (opzione spenta, barca tenuta di bolina, 60 s): «Vira sullo scarso» {r[2]} scritte su 120 disegni (dalla 1.3.45 ci deve essere), «Riepilogo» {r[3]} (0)")
        # ---- S4 ----
        ctx, pg = await pagina(); r = await pg.evaluate(S4); await ctx.close()
        chk(r[0] >= 50 and r[1] >= 2, f"S4 spazio: {r[0]} scritte misurate, margine minimo da «N», bussola e vento {r[1]:.1f} px (soglia 2)")
        # ---- S1 ----
        uguali = 0; disegnate = 0
        for seme in range(1501, 1501 + N1):
            a = await corsa(S1, [seme, True]); c = await corsa(S1, [seme, False]); uguali += a[0] == c[0]; disegnate += a[1]
        chk(uguali == N1 and disegnate > 0, f"S1 torneo identico al bit con l'aiuto acceso e spento: {uguali} su {N1}; scritte disegnate con l'aiuto acceso {disegnate}")
        chk(not errs, f"errori della pagina {errs[:2]}")
        await b.close()
    print(); print("casi sbagliati: " + ("nessuno" if not bad else str(len(bad))))
    raise SystemExit(1 if bad else 0)
asyncio.run(main())
