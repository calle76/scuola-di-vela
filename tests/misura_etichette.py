# Misura per PROPOSTA-ETICHETTE-BARCHE.md, criterio E1: quante volte la scritta sopra un avversario copre lo scafo di un'altra barca.
# 20 regate del torneo (4 regate x 5 semi 2301-2305, principianti nei semi dispari, esperti nei pari), pilota per il giocatore,
# un disegno ogni 6 passi di simulazione, da 60 s prima del via all'arrivo di tutti (o 900 s). Non tocca il gioco.
# Conta solo le scritte piene (le trasparenti della 1.2.34 a parte) e, dalla 1.2.34, i cambi di posto sopra/sotto (E3).
# Uso: python tests/misura_etichette.py [salva.json]   (BROWSER=firefox per Firefox)
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
JS = """([k, liv, seme, zoom, sei]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', liv); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); if (sei) document.getElementById('torN6').click(); document.getElementById('torGo').click(); // SEI=1: torneo a 6 barche (1.2.38)
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push(Array.from({ length: T.av.length + 1 }, (_, i) => ({ fin: i + 1, pp: 0 })));
  semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  if (zoom){ userZoom = Math.max(0.1, Math.pow(1.25, -zoom)); camZoom = userZoom; } // ZOOM=n: come n volte il tasto 2 (seconda parte della proposta)
  const R = sv.R, dt = 1 / 60;
  const P = CanvasRenderingContext2D.prototype, fr0 = P.fillRect, ft0 = P.fillText; let cattura = null;
  P.fillRect = function(x, y, w, h){ if (cattura && h >= 14.5 && h <= 18.5 && /^rgba\\(10, ?24, ?36, ?0?\\.6\\)$/.test(this.fillStyle)) cattura.push([x, y, w, h, this.globalAlpha, null, null]); return fr0.call(this, x, y, w, h); };
  P.fillText = function(t, x, y){ const u = cattura && cattura[cattura.length - 1]; if (u && u[5] === null){ u[5] = t; const m = /([\\d.]+)px/.exec(this.font); u[6] = m ? +m[1] : null; } return ft0.apply(this, arguments); };
  const orig = window.drawRaceScreen; let disegni = 0, copre = 0, copreMe = 0, casi = 0, etichette = 0, trasp = 0, sotto = 0, cambi = 0, salti = 0, giuste = 0, lettMin = 1e9; const ultimo = {}, posto = {};
  const dentroPoli = (P, x, y) => { let c = false; for (let i = 0, j = P.length - 1; i < P.length; j = i++){ const [xi, yi] = P[i], [xj, yj] = P[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; } return c; };
  const tocca = (r, P) => { const [x, y, w, h] = r; if (P.some(([px, py]) => px >= x && px <= x + w && py >= y && py <= y + h)) return true;
    for (let a = 0; a <= 4; a++) for (let b = 0; b <= 2; b++) if (dentroPoli(P, x + w * a / 4, y + h * b / 2)) return true; return false; };
  window.drawRaceScreen = function(v){ cattura = []; orig(v); const rr = cattura; cattura = null; disegni++;
    const scafi = R.boats.map(b => sv.hullWorld(b.S).map(([x, y]) => toScreen(v, x, y)));
    const av = R.boats.map((b, i) => i).filter(i => !R.boats[i].me); etichette += rr.length;
    let f = false, fm = false;
    R.boats.forEach((b, i) => { if (!b.etq) return; if (i in posto && posto[i] !== b.etq.su){ cambi++; if (i in ultimo && R.t - ultimo[i] < 1 - 1e-6) salti++; ultimo[i] = R.t; } posto[i] = b.etq.su; if (!b.etq.su) sotto++; });
    const centri = R.boats.map(b => toScreen(v, b.S.x, b.S.y)), dRett = ([x, y, w, h], [px, py]) => Math.hypot(Math.max(x - px, 0, px - x - w), Math.max(y - py, 0, py - y - h));
    rr.forEach(r => { const prop = av.find(i => (R.boats[i].etich || R.boats[i].name) === r[5]); if (r[6] !== null) lettMin = Math.min(lettMin, r[6]);
      if (prop !== undefined){ const dP = dRett(r, centri[prop]); if (centri.every((c, j) => j === prop || dRett(r, c) > dP)) giuste++; }
      if (r[4] < 1){ trasp++; return; }
      R.boats.forEach((b, i) => { if (i !== prop && tocca(r, scafi[i])){ f = true; casi++; if (b.me) fm = true; } }); });
    if (f) copre++; if (fm) copreMe++; };
  let n = 0;
  while (R.t < 900 && R.boats.some(b => b.fin === null && !b.dnf)){ if (R.boats[0].fin === null) sv.pilota(dt); if (++n % 6) sv.run(dt, 1); else sv.frame(dt); }
  window.drawRaceScreen = orig; P.fillRect = fr0; P.fillText = ft0;
  return { disegni, copre, copreMe, casi, etichette, trasp, sotto, cambi, salti, giuste, lettMin, t: R.t };
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
                r = await pg.evaluate(JS, [k, liv, seme, int(os.environ.get("ZOOM") or 0), int(os.environ.get("SEI") or 0)]); r.update(reg=k, seme=seme, liv=liv); out.append(r)
                print(f"  regata {k + 1} seme {seme} {liv}: disegni {r['disegni']}, con una scritta su uno scafo {r['copre']} (sul tuo {r['copreMe']}), scritte disegnate {r['etichette']}, trasparenti {r['trasp']}, sotto {r['sotto']}, cambi di posto {r['cambi']} (sotto 1 s: {r['salti']}), della barca giusta {r['giuste']}, lettere min {r['lettMin']}", flush=True)
        await br.close()
    D = sum(r["disegni"] for r in out); C = sum(r["copre"] for r in out); M = sum(r["copreMe"] for r in out); E = sum(r["etichette"] for r in out)
    G = sum(r["giuste"] for r in out); LM = min(r["lettMin"] for r in out); T = sum(r["trasp"] for r in out); K = sum(r["cambi"] for r in out); X = sum(r["salti"] for r in out)
    print(f"TOTALE: {len(out)} regate, {D} disegni, scritte {E} (trasparenti {T}); disegni con una scritta piena sopra uno scafo {C} ({100 * C / max(D, 1):.1f}%), sopra il tuo {M}; cambi di posto {K}, di cui a meno di 1 s dal precedente {X}; scritte vicine alla barca giusta {G} ({100 * G / max(E, 1):.1f}%); lettere più piccole {LM} px; errori {errs[:3]}")
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"): pathlib.Path(sys.argv[1]).write_text(json.dumps(out))
    return {"giuste": G, "lettMin": LM, "regate": len(out), "disegni": D, "copre": C, "copreMe": M, "etichette": E, "trasp": T, "cambi": K, "salti": X, "errori": errs}
if __name__ == "__main__": asyncio.run(main())
