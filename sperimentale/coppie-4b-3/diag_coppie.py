# Diagnosi (23 nov): le coppie S8 dopo il via che restano con la voce 3 accesa; per ogni episodio, perché chi cede non si è liberata.
# Uso (con la patch applicata): python sperimentale/coppie-4b-3/diag_coppie.py c10 2201-2230
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]  # la radice del repository
src = (ROOT / "tests" / "misura_manovre.py").read_text()
ns = {"__file__": str(ROOT / "tests" / "misura_manovre.py")}
exec(src.replace("asyncio.run(main())", ""), ns)
CORSA = ns["CORSA"]
add = ("if (b.__cp === 10 && R.t >= 0){ window.__copDopo++; const s = b.S, tw = sv.windAt(s.x, s.y).twd, tk = x => Math.sign(((sv.windAt(x.S.x, x.S.y).twd - x.S.h) % 360 + 540) % 360 - 180);"
       " (window.__ep = window.__ep || []).push({ t: +R.t.toFixed(0), i, j: R.boats.indexOf(o), leg: b.leg, ramo: b.ramo, u: +s.u.toFixed(2), stesse: tk(b) === tk(o), twa: Math.round(((tw - s.h) % 360 + 540) % 360 - 180),"
       " lib: b.libMia === undefined ? null : +(R.t - b.libMia).toFixed(0), d: +Math.hypot(o.S.x - s.x, o.S.y - s.y).toFixed(1), oMe: !!o.me, vir: !!b.virando }); }")
CORSA = CORSA.replace("if (b.__cp === 10 && R.t >= 0) window.__copDopo++;", add).replace("copDopo: window.__copDopo,", "copDopo: window.__copDopo, ep: window.__ep || [],")
assert "__ep" in CORSA
async def main():
    conf = sys.argv[1]; js = ns["imposta"](conf) if "imposta" in ns else None
    a, b_ = sys.argv[2].split("-")
    async with async_playwright() as p:
        br = await p.chromium.launch(); tutti = []
        for s in range(int(a), int(b_) + 1):
            for k in range(4):
                pg = await br.new_page(viewport={"width": 1360, "height": 650})
                await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
                await pg.evaluate("() => { " + js + " }")
                r = await pg.evaluate(CORSA.replace("const sv = __sv,", "const sv = __sv,"), [k, s, 0]); await pg.close()
                for e in r["ep"]: e["seme"] = s; e["k"] = k; print(json.dumps(e), flush=True)
        await br.close()
asyncio.run(main())
