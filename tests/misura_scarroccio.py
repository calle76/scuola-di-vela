# Misura delle regate dell'1b per lo scarroccio (1.0.45, docs/archivio/PROPOSTA-SCARROCCIO-1B.md, criterio 5). Non è un collaudo: confronta due giri.
# Tornei del gioco libero guidati dal pilota (come C2 di collaudo_torneo.py), semi fissi: per ogni barca tempo d'arrivo, non arrivata, boe sbagliate.
# Uso: python misura_scarroccio.py <primo seme> <ultimo seme>   (una riga JSON per regata; in fondo il riepilogo)
# 1.0.46 (docs/archivio/PROPOSTA-ORZIERA-1B.md): conta anche penalità per contatto e scuffie; MISURA_INDEX=<percorso di index.html> misura un'altra copia del gioco.
import os
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright
BASE = pathlib.Path(os.environ.get("MISURA_INDEX") or pathlib.Path(__file__).resolve().parent.parent / "index.html").resolve().as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""

async def pagina(b):  # come collaudo_torneo.py (non si importa: all'import lancerebbe il collaudo intero)
    ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); await pg.add_init_script(SEME)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(150)
    return ctx, pg, errs

async def prepara(pg, seme):  # torneo del gioco libero
    await pg.evaluate("s => { __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); }", seme)

CORRI = """() => { const sv = __sv, dt = 1 / 60;
  document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], cap = R.boats.map(() => 0), giu = R.boats.map(() => false);
  while (me.fin === null && !me.dnf && R.t < 1500){ sv.pilota(dt); sv.run(dt, 1);
    R.boats.forEach((b, i) => { if (b.S.capsized && !giu[i]) cap[i]++; giu[i] = b.S.capsized; }); }
  const pil = { fin: me.fin, dnf: !!me.dnf };
  document.getElementById("rTor").click();
  return R.boats.map((b, i) => ({ fin: i ? b.fin : pil.fin, dnf: i ? !!b.dnf : pil.dnf, wm: b.wrongMarks || 0, pp: b.pp || 0, cap: cap[i] })); }"""

async def main():
    a, z = int(sys.argv[1]), int(sys.argv[2]); tempi = {"pilota": [], "avversari": []}; nonarr = wm = regate = pp = cap = 0
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        for seme in range(a, z + 1):
            ctx, pg, errs = await pagina(b); await prepara(pg, seme)
            for k in range(4):
                r = await pg.evaluate(CORRI); regate += 1
                print(json.dumps({"seme": seme, "regata": k + 1, "barche": r}), flush=True)
                for i, x in enumerate(r):
                    wm += x["wm"]; pp += x["pp"]; cap += x["cap"]
                    if x["fin"] is None: nonarr += 1
                    else: tempi["pilota" if i == 0 else "avversari"].append(x["fin"])
            if errs: print("ERRORE nella pagina:", errs[0])
            await ctx.close()
        await b.close()
    m = lambda v: sum(v) / len(v) if v else float("nan")
    print(f"RIEPILOGO semi {a}-{z}: regate {regate}; tempo medio pilota {m(tempi['pilota']):.1f} s ({len(tempi['pilota'])} arrivi), "
          f"avversari {m(tempi['avversari']):.1f} s ({len(tempi['avversari'])} arrivi); non arrivate {nonarr}; boe sbagliate {wm}; penalità per contatto {pp}; scuffie {cap}")

asyncio.run(main())
