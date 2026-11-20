# Misura della voce 66 (a), 1.3.27: passo delle isocrone della rotta ottimale nelle regate lunghe. Per ogni regata lunga del torneo (pilota sul giocatore):
# rotta del giocatore e in assoluto con passo 1, 1,5 e 2 s: tempo di calcolo (ms), tempo della rotta, differenza dal passo 1, giro della boa valido col metro
# di tests/misura_giro_boa.py (roundCheck su tratti divisi in 60 pezzi), rotta più lenta della barca vera (non deve succedere oltre 1%).
# Uso: python tests/misura_passo_rotta.py PRIMO ULTIMO
import asyncio, os, pathlib, statistics as st, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
GIRO = (ROOT / "tests" / "misura_giro_boa.py").read_text().split("  const SUB = 60;")[1].split("  const una =")[0]
JS = """([k, seme]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', 'medio'); sel('cdSel', '60'); window.confirm = () => true; sv.lungo = true;
  if (sv.tor){ sv.torApri(); const rit = document.getElementById('torRit'); if (rit) rit.click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push(T.av.concat([0]).map((x, i) => ({ fin: i + 1, pp: 0 })));
  sv.rot.spento = false; semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60; R.tor = false;
  while (R.t < 1500 && R.boats[0].fin === null){ sv.pilota(dt); sv.run(dt, 1); }
  const SUB = 60;""" + GIRO + """
  const out = { up: R.up, tri: !!R.tri, fin: R.boats[0].fin, taglio: sv.rot.barche[0].taglio ? sv.rot.barche[0].taglio.t : null, p: {} };
  for (const d of [1, 1.5, 2]){ sv.rot.dt = d;
    let t0 = performance.now(); const o = sv.rotCalcola(0), ms = performance.now() - t0;
    t0 = performance.now(); const a = sv.rotAssoluta(), msA = performance.now() - t0;
    out.p[d] = { ms, msA, tempo: o && o.tempo, tempoA: a && a.tempo, giro: o ? giro(o, R.marks.slice(sv.rot.barche[0].taglio.leg - 1)) : null, giroA: a ? giro(a, R.marks) : null }; }
  sv.rot.dt = 0; return out;
}"""
async def main(A, B):
    res = []
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(400)
        for seme in range(A, B + 1):
            for k in (0, 1):
                r = await pg.evaluate(JS, [k, seme]); res.append(r)
                print(seme, "triangolo" if r["tri"] else "bastone", {d: (round(v["ms"]), round(v["msA"]), v["tempo"] and round(v["tempo"], 1), v["giro"], v["giroA"]) for d, v in r["p"].items()}, "arrivo", r["fin"] and round(r["fin"], 1), flush=True)
        await br.close()
    for d in ("1.5", "2"):
        dif = [100 * (r["p"][d]["tempo"] - r["p"]["1"]["tempo"]) / r["p"]["1"]["tempo"] for r in res if r["p"][d]["tempo"] and r["p"]["1"]["tempo"]]
        ms = [r["p"][d]["ms"] / r["p"]["1"]["ms"] for r in res]; msA = [r["p"][d]["msA"] / r["p"]["1"]["msA"] for r in res]
        val = sum(1 for r in res if r["p"][d]["giro"] and all(s == 1 and n == 0 for s, n in r["p"][d]["giro"]))
        lenta = sum(1 for r in res if r["p"][d]["tempo"] and r["fin"] and r["p"][d]["tempo"] > r["fin"] * 1.01)
        print(f"passo {d}: tempo della rotta rispetto al passo 1 mediana {st.median(dif):+.2f}% (da {min(dif):+.2f} a {max(dif):+.2f}); calcolo {st.median(ms):.2f} volte, in assoluto {st.median(msA):.2f} volte; "
              f"giro valido {val} su {len(res)}; rotta più lenta della barca vera oltre 1%: {lenta}")
    print("tempi col passo 1: rotta", [round(r["p"]["1"]["ms"]) for r in res], "in assoluto", [round(r["p"]["1"]["msA"]) for r in res], "errori", errs[:2])
asyncio.run(main(int(sys.argv[1]), int(sys.argv[2])))
