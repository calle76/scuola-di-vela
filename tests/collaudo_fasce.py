# Taratura delle fasce di tempo delle prove.
# Un pilota automatico (logica di collaudo_giro_boa.py: bolina a 52°, vela sempre regolata, boe lasciate a sinistra;
# qui cazza solo quando sta per strambare, non per tutta la poppa)
# percorre ogni prova più volte con direzioni del vento diverse. La simulazione avanza a passi fissi di 1/60 s con __sv.run,
# quindi i tempi non dipendono dalla velocità del computer. Il pilota corregge barra e scotta ogni 0,1 s.
# Uso: python collaudo_fasce.py [ripetizioni] [prove, per esempio 125]
import asyncio, pathlib, sys, statistics
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
URL = BASE + "#collaudo"
GIUSTO = [60, 0, -60]
PIANI = [[], [], [], [[0, GIUSTO]], [[0, GIUSTO], [1, GIUSTO]]]
CORSA = """
(plan) => {
  const sv = __sv, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  const pts = [];
  for (const [k, angs] of plan) { const m = sv.marks[k];
    for (const a of angs) { const b = (m.out + a) * D; pts.push({ x: m.x + Math.sin(b) * 13, y: m.y - Math.cos(b) * 13 }); } }
  const last = sv.marks[sv.marks.length - 1]; pts.push({ x: last.x, y: last.y });
  let i = 0, side = 1, n = 0;
  sv.fast(0);
  while (!sv.S.finished && n < 60 * 900) {
    const S = sv.S;
    if (n % 6 === 0 && i < pts.length) {
      const p = pts[i]; if (Math.hypot(p.x - S.x, p.y - S.y) < 7) i++;
      const q = pts[Math.min(i, pts.length - 1)];
      const brg = Math.atan2(q.x - S.x, -(q.y - S.y)) / D, rel = n180(brg - sv.twd);
      let want = brg;
      if (Math.abs(rel) < 52) { if (Math.abs(rel) > 12) side = Math.sign(rel); want = sv.twd + side * 52; }
      const cur = n180(S.h - sv.twd);
      if (Math.abs(rel) > 168 && Math.abs(cur) > 90) want = sv.twd + Math.sign(cur || 1) * 168;   // in poppa resta sulle sue mure: niente strambate inutili
      if (Math.abs(cur) < 48 && S.u < 0.8) want = sv.twd + Math.sign(cur || 1) * 95;
      const err = n180(S.h - want);
      sv.ctl.tiller = Math.max(-1, Math.min(1, err / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1);
      const gybe = (Math.abs(cur) > 150 && Math.sign(n180(want - sv.twd)) !== Math.sign(cur)) || Math.abs(cur) > 174;   // sta per strambare, o è così in poppa che può strambare per sbaglio
      sv.ctl.sheet = gybe ? Math.min(sv.autoSheet(), 0.3) : sv.autoSheet();   // cazza solo prima di strambare
      if (S.capsized && !S.righting) dispatchEvent(new KeyboardEvent("keydown", { key: "r" }));
    }
    sv.run(1 / 60, 1); n++;
  }
  return [sv.S.finished, sv.S.time, JSON.parse(JSON.stringify(sv.reg))];
}
"""
async def main(n, quali):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1280, "height": 800})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        for idx in quali:
            tempi = []; note = []
            for k in range(n * (3 if idx == 4 else 1)):
                vento = (k * 45) % 360
                await pg.evaluate(f"__sv.openItem(['m',{idx}])"); await pg.evaluate(f"__sv.startMission({idx}, {vento})")
                fin, t, reg = await pg.evaluate(CORSA, PIANI[idx])
                if fin: tempi.append(t)
                else: note.append(f"non finita (vento {vento})")
                e = {a: v for a, v in reg.items() if v}
                if e: note.append(f"vento {vento}: {e}")
            print(f"prova {idx+1}: tempi {[round(x,1) for x in tempi]} | mediana {statistics.median(tempi):.1f} | min {min(tempi):.1f} | max {max(tempi):.1f} | {note}", flush=True)
        print("errori:", errs); await b.close()
asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 8, [int(c) - 1 for c in (sys.argv[2] if len(sys.argv) > 2 else "12345")]))
