# Misura per PROPOSTA-ETICHETTE-BARCHE.md, criterio E1 di PROPOSTA-ETICHETTE-BARCHE.md: quante volte, oggi, la scritta sopra un avversario copre lo scafo di un'altra barca.
# 20 regate del torneo (4 regate x 5 semi 2301-2305, principianti nei semi dispari, esperti nei pari), pilota per il giocatore,
# un disegno ogni 6 passi di simulazione, da 60 s prima del via all'arrivo di tutti (o 900 s). Non tocca il gioco.
# Uso: python tests/misura_etichette.py [salva.json]   (BROWSER=firefox per Firefox)
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
JS = """([k, liv, seme]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', liv); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push([0, 1, 2, 3].map(i => ({ fin: i + 1, pp: 0 })));
  semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60;
  const P = CanvasRenderingContext2D.prototype, fr0 = P.fillRect; let cattura = null;
  P.fillRect = function(x, y, w, h){ if (cattura && h === 18 && /^rgba\\(10, ?24, ?36, ?0?\\.6\\)$/.test(this.fillStyle)) cattura.push([x, y, w, h]); return fr0.call(this, x, y, w, h); };
  const orig = window.drawRaceScreen; let disegni = 0, copre = 0, copreMe = 0, casi = 0, etichette = 0;
  const dentroPoli = (P, x, y) => { let c = false; for (let i = 0, j = P.length - 1; i < P.length; j = i++){ const [xi, yi] = P[i], [xj, yj] = P[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; } return c; };
  const tocca = (r, P) => { const [x, y, w, h] = r; if (P.some(([px, py]) => px >= x && px <= x + w && py >= y && py <= y + h)) return true;
    for (let a = 0; a <= 4; a++) for (let b = 0; b <= 2; b++) if (dentroPoli(P, x + w * a / 4, y + h * b / 2)) return true; return false; };
  window.drawRaceScreen = function(v){ cattura = []; orig(v); const rr = cattura; cattura = null; disegni++;
    const scafi = R.boats.map(b => sv.hullWorld(b.S).map(([x, y]) => toScreen(v, x, y)));
    const av = R.boats.map((b, i) => i).filter(i => !R.boats[i].me); etichette += rr.length;
    let f = false, fm = false;
    rr.forEach(r => { const cx = r[0] + r[2] / 2;
      const prop = av.reduce((m, i) => { const [sx] = toScreen(v, R.boats[i].S.x, R.boats[i].S.y); return Math.abs(sx - cx) < Math.abs(m[1] - cx) ? [i, sx] : m; }, [-1, 1e9])[0];
      R.boats.forEach((b, i) => { if (i !== prop && tocca(r, scafi[i])){ f = true; casi++; if (b.me) fm = true; } }); });
    if (f) copre++; if (fm) copreMe++; };
  let n = 0;
  while (R.t < 900 && R.boats.some(b => b.fin === null && !b.dnf)){ if (R.boats[0].fin === null) sv.pilota(dt); if (++n % 6) sv.run(dt, 1); else sv.frame(dt); }
  window.drawRaceScreen = orig; P.fillRect = fr0;
  return { disegni, copre, copreMe, casi, etichette, t: R.t };
}"""
async def main():
    out = []
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(500)
        for k in range(4):
            for seme in range(2301, 2306):
                liv = "principianti" if seme % 2 else "esperti"
                r = await pg.evaluate(JS, [k, liv, seme]); r.update(reg=k, seme=seme, liv=liv); out.append(r)
                print(f"  regata {k + 1} seme {seme} {liv}: disegni {r['disegni']}, con una scritta su uno scafo {r['copre']} (sul tuo {r['copreMe']}), scritte disegnate {r['etichette']}", flush=True)
        await br.close()
    D = sum(r["disegni"] for r in out); C = sum(r["copre"] for r in out); M = sum(r["copreMe"] for r in out); E = sum(r["etichette"] for r in out)
    print(f"TOTALE: {len(out)} regate, {D} disegni, scritte {E}; disegni con una scritta sopra uno scafo {C} ({100 * C / max(D, 1):.1f}%), sopra il tuo {M}; errori {errs[:3]}")
    if len(sys.argv) > 1: pathlib.Path(sys.argv[1]).write_text(json.dumps(out))
asyncio.run(main())
