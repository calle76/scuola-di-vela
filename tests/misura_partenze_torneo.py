# Misura osservazioni 59-62 (28 ott 2026): partenza fuori dagli estremi e avversari alla boa 1, nel torneo dell'1b col pilota.
import asyncio, json, pathlib, sys, os, statistics
from playwright.async_api import async_playwright
BASE = (pathlib.Path("/home/callle/scuola-di-vela/index.html")).as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
RUN = """seme => {
  const sv = __sv, dt = 1 / 60; sv.simTime = 0; __seed(seme);
  document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], D = Math.PI / 180;
  const wf = (x, y) => { const a = sv.twd * D; return [x * Math.sin(a) - y * Math.cos(a), x * Math.cos(a) + y * Math.sin(a)]; }; // [su, q]
  const o = R.boats.slice(1), out = { tri: !!R.tri, gunQ: null, crossQ: {}, ocs: 0, lenti: {}, tmax: 0 };
  const prevUp = {}; let gun = false, n = 0;
  while (R.t < 1500 && me.fin === null && !me.dnf){
    sv.pilota(dt); sv.run(dt, 1); n++;
    if (!gun && R.t >= 0){ gun = true; out.gunQ = o.map(b => Math.round(wf(b.S.x, b.S.y)[1])); o.forEach(b => prevUp[b.name] = wf(b.S.x, b.S.y)[0]); }
    if (gun && R.t < 90){ for (const b of o){ const [u, q] = wf(b.S.x, b.S.y);
        if (!(b.name in out.crossQ) && prevUp[b.name] < 0 && u >= 0) out.crossQ[b.name] = Math.round(q);
        prevUp[b.name] = u; } }
    if (n % 6 === 0 && gun){ const m = R.marks[0];
      for (const b of o){ if (b.leg !== 1) continue; const d = Math.hypot(b.S.x - m.x, b.S.y - m.y); const v = Math.abs(b.S.u || 0) * 1.944;
        if (d < 25 && v < 1) out.lenti[b.name] = (out.lenti[b.name] || 0) + 0.1; } }
  }
  out.ocs = o.filter(b => b.ocs).length;
  out.wm = o.map(b => b.wrongMarks || 0); out.dnf = o.filter(b => b.dnf).length; out.fin = o.filter(b => b.fin !== null).length; out.pen = R.penList.length;
  out.title = R.brief.slice(0, 30);
  document.getElementById("rTor").click();
  return out;
}"""
async def main():
    seme_da, seme_a = int(sys.argv[1]), int(sys.argv[2])
    ris = []
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for t in range(seme_da, seme_a + 1):
            ctx = await b.new_context(viewport={"width": 1280, "height": 800}); await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(200)
            await pg.evaluate("([s, l]) => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; const e = document.getElementById('aiLevel'); e.value = l; e.dispatchEvent(new Event('change')); __sv.torApri(); }", [t, "principianti"])
            for k in range(4):
                r = await pg.evaluate(RUN, 5000 + 10 * t + k); r["seme"] = t; r["k"] = k + 1; ris.append(r)
            await ctx.close()
        await b.close()
    json.dump(ris, open(sys.argv[3], "w"))
asyncio.run(main())
