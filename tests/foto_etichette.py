# Fotografie E5: regata 3, seme 2304, esperti (la più affollata in E1). Con TEMPO=t si ferma a quell'istante; senza, al primo
# disegno in cui una scritta piena copre la barca del giocatore dopo 30 s prima del via, e stampa l'istante.
import asyncio, os, pathlib, sys
from playwright.async_api import async_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
RAD = pathlib.Path(os.environ["RADICE"]); URL = (RAD / "index.html").as_uri() + "#collaudo"
JS = """([k, liv, seme, tempo]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', liv); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push([0, 1, 2, 3].map(i => ({ fin: i + 1, pp: 0 })));
  semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60, P = CanvasRenderingContext2D.prototype, fr0 = P.fillRect; let cat = null;
  P.fillRect = function(x, y, w, h){ if (cat && h === 18 && this.globalAlpha === 1 && /^rgba\\(10, ?24, ?36, ?0?\\.6\\)$/.test(this.fillStyle)) cat.push([x, y, w, h]); return fr0.call(this, x, y, w, h); };
  const orig = window.drawRaceScreen; let colpo = false;
  window.drawRaceScreen = function(v){ cat = []; orig(v); const rr = cat; cat = null; colpo = false;
    const me = sv.hullWorld(R.boats[0].S).map(([x, y]) => toScreen(v, x, y));
    const inP = (P, qx, qy) => { let c = false; for (let a = 0, b = P.length - 1; a < P.length; b = a++){ const [xa, ya] = P[a], [xb, yb] = P[b]; if ((ya > qy) !== (yb > qy) && qx < (xb - xa) * (qy - ya) / (yb - ya) + xa) c = !c; } return c; };
    const tocca = ([x, y, w, h]) => { if (me.some(([px, py]) => px >= x && px <= x + w && py >= y && py <= y + h)) return true; for (let a = 0; a <= 4; a++) for (let b = 0; b <= 2; b++) if (inP(me, x + w * a / 4, y + h * b / 2)) return true; return false; };
    if (rr.some(tocca)) colpo = true; };
  let n = 0;
  while (R.t < 900){ if (R.boats[0].fin === null) sv.pilota(dt);
    if (++n % 6) sv.run(dt, 1); else { sv.frame(dt); if (tempo === null ? (colpo && R.t > -30) : R.t >= tempo) break; } }
  window.drawRaceScreen = orig; P.fillRect = fr0; sv.frame(0);
  return R.t; }"""
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        await pg.evaluate(JS, [0, "principianti", 2301, -1000])   # il gruppo dei rivali nasce dal primo torneo, come in misura_etichette.py
        for _ in range(int(os.environ.get("ZOOM") or 0)): await pg.keyboard.press("2")   # ZOOM=n: n volte il tasto 2 (vista allontanata)
        t = await pg.evaluate(JS, [2, "esperti", 2304, float(os.environ["TEMPO"]) if os.environ.get("TEMPO") else None])
        await pg.screenshot(path=sys.argv[1]); print(f"istante {t:.4f}; errori {errs}")
        await br.close()
asyncio.run(main())
