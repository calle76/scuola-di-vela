# Voce 86 (27 nov 2026, docs/PROPOSTA-STRAPOGGIO-86.md, criteri S2-S3): la barca tenuta in strapoggio nel gioco vero.
# Navigazione libera, vento da nord a 6, 10, 15 nodi, raffiche e salti spenti. Si arriva a 170° di poppa sulle mure di partenza, poi la prua si porta (a 3°/s)
# all'angolo di prova e si tiene 30 s con la vela aperta (scotta 1): 190° e 195° (10° e 15° in strapoggio) e 205° (25°). Per confronto le stesse prove a 170° e 165°.
# Misura: strambate contate dal gioco (gybesV + gybesC), cambi di lato del boma, velocità media degli ultimi 10 s.
# Uso: .venv-collaudi/bin/python tests/misura_strapoggio.py   (BROWSER=firefox, RADICE=copia)
import asyncio, os, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parents[1])
CORSA = """async ([kn, ang]) => {
  const sv = __sv, dt = 1 / 60; sv.fast(0); sv.openItem('free');
  for (const [id, v] of [['wSpd', String(kn)], ['gustSel', '0'], ['wDir', '0']]){ const e = document.getElementById(id); if (!e) continue; e.value = v; e.dispatchEvent(new Event('change')); }
  sv.openItem('free'); sv.setShifts(null);
  const S = sv.S, ctl = sv.ctl; S.u = 3; S.vl = 0; S.r = 0; ctl.tiller = 0;
  let h = (sv.twd + 170 + 360) % 360; const fine = (sv.twd + ang + 360) % 360;
  for (let t = 0; t < 20; t += dt){ S.h = h; ctl.sheet = 1; sv.run(dt, 1); }
  const g0 = S.gybesV + S.gybesC, b0 = S.boomSide; let cambi = 0, ult = S.boomSide, us = 0, n = 0;
  for (let t = 0; t < 40; t += dt){ const d = ((fine - h + 540) % 360) - 180; h = (h + Math.sign(d) * Math.min(Math.abs(d), 3 * dt) + 360) % 360;
    S.h = h; ctl.sheet = 1; sv.run(dt, 1); if (S.boomSide !== ult){ cambi++; ult = S.boomSide; } if (t > 30){ us += S.u; n++; } if (S.capsized) break; }
  return { strambate: S.gybesV + S.gybesC - g0, violente: S.gybesV, cambi, kn: +(us / Math.max(1, n) * 1.943844).toFixed(2), cap: !!S.capsized, lato: S.boomSide === b0 ? "suo" : "altro" };
}"""
async def main():
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for kn in (6, 10, 15):
            riga = []
            for ang in (165, 170, 190, 195, 205):
                pg = await br.new_page(viewport={"width": 1360, "height": 650})
                await pg.goto((ROOT / "index.html").resolve().as_uri() + "#collaudo"); await pg.wait_for_function("window.__sv")
                r = await pg.evaluate(CORSA, [kn, ang]); await pg.close()
                riga.append(f"{ang}°: {r['kn']} nodi, strambate {r['strambate']}, boma {r['lato']}" + (" SCUFFIA" if r["cap"] else ""))
            print(f"{kn:2} nodi | " + " | ".join(riga), flush=True)
        await br.close()
asyncio.run(main())
