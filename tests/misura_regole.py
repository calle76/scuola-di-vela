# Misura dell'effetto delle regole 12 e 13 sulle regate dell'1b (1.0.40, docs/PROPOSTA-REGOLE-PRECEDENZA-1B.md). Non è un collaudo: non ha soglie.
# Per ogni contatto (regata dei salti di vento, semi a-b, principianti ed esperti, giocatore col pilota) confronta chi cede con le regole di prima
# (10; stesse mure: la più sopravento in y) e con le nuove, e dice quali regole decidono. Uso: python misura_regole.py <primo seme> <ultimo seme>
import asyncio, json, pathlib, sys
from collections import Counter
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent; BASE = (ROOT / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
JS = """([seme, liv]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", 2]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, me = R.boats[0], dt = 1 / 60, bs = R.boats, visti = new Set(), out = { contatti: [], pen: bs.map(() => 0) };
  const vecchia = (A, B) => { const tA = Math.sign(sv.windAt(A.S.x, A.S.y).twd - A.S.h) , nA = (v) => ((v % 360) + 540) % 360 - 180;
    const a = nA(sv.windAt(A.S.x, A.S.y).twd - A.S.h) < 0 ? -1 : 1, b = nA(sv.windAt(B.S.x, B.S.y).twd - B.S.h) < 0 ? -1 : 1;
    if (a !== b) return a < 0 ? A : B; const th = -sv.twd * Math.PI / 180, wy = S => S.x * Math.sin(th) + S.y * Math.cos(th); return wy(A.S) < wy(B.S) ? A : B; };
  let prev = {};
  const passo = () => {
    for (const key of Object.keys(R.contacts)){ const id = key + ":" + R.contacts[key]; if (visti.has(id) || !prev[key]) continue; visti.add(id);
      const [i, j] = key.split("-").map(Number); out.contatti.push({ giocatore: i === 0 || j === 0, regola: prev[key].regola, nuova: prev[key].cede, vecchia: prev[key].vecchia, cambia: prev[key].cede !== prev[key].vecchia }); }
    prev = {}; for (let i = 0; i < bs.length; i++) for (let j = i + 1; j < bs.length; j++){ const A = bs[i], B = bs[j];
      if (A.fin !== null || B.fin !== null || A.dnf || B.dnf || A.S.capsized || B.S.capsized || Math.hypot(A.S.x - B.S.x, A.S.y - B.S.y) > 6) continue;
      const c = sv.chiCede(A, B); prev[i + "-" + j] = { regola: c.regola, cede: c.cede === A ? i : j, vecchia: vecchia(A, B) === A ? i : j }; }
  };
  while (me.fin === null && !me.dnf && R.t < 900){ sv.pilota(dt); sv.run(dt, 1); passo(); }
  let k = 0; while (k++ < 60 * 300 && !bs.every(b => b.fin !== null || b.dnf)){ sv.run(dt, 1); passo(); }
  out.pen = bs.map(b => (b.pen || 0)); return out; }"""
async def main():
    a, z = int(sys.argv[1]), int(sys.argv[2])
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch(); pg = await b.new_page(viewport={"width":1360,"height":650}); await pg.add_init_script(SEME)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_function("window.__sv")
        tot = Counter(); reg = Counter(); camb = Counter(); pen = [0, 0, 0, 0]; n = 0; vec = [0, 0, 0, 0]; nuo = [0, 0, 0, 0]
        for seme in range(a, z + 1):
            for liv in ("principianti", "esperti"):
                r = await pg.evaluate(JS, [seme, liv]); n += 1
                for c in r["contatti"]:
                    tot["contatti"] += 1; tot["giocatore"] += c["giocatore"]; reg[c["regola"]] += 1
                    vec[c["vecchia"]] += 1; nuo[c["nuova"]] += 1
                    if c["cambia"]: camb[c["regola"]] += 1; tot["cambia"] += 1
                pen = [x + y for x, y in zip(pen, r["pen"])]
        print(f"regata dei salti di vento, semi {a}-{z}: {n} corse, contatti {tot['contatti']} ({tot['contatti']/n:.2f} a regata), con il giocatore {tot['giocatore']}")
        print("  decisi dalla regola:", dict(sorted(reg.items())), "| colpevole diverso da prima:", tot["cambia"], "su", tot["contatti"], dict(sorted(camb.items())))
        print("  penalità per barca (giocatore, Rossa, Blu, Verde): con le regole di prima", vec, "con le nuove", nuo)
        print("  secondi di penalità per barca (giocatore, Rossa, Blu, Verde) in totale:", pen, "per regata:", [round(x / n, 1) for x in pen], "errori", errs[:2])
        await b.close()
asyncio.run(main())
