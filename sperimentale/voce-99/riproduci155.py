# Riproduce oss. 155: ripassa Ale e Blu del file 14:34 (380-397,48 s) dentro aggiornaPrecedenze/chiCede1516, scena ruotata col vento a nord
# Uso: python sperimentale/voce-99/riproduci155.py  (BROWSER=firefox; FERMA=Ale|Blu TF=secondi: prua di quella barca tenuta ferma da TF, le controprove di docs/PROPOSTA-VOCE-99.md)
import asyncio, json, math, os, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(os.environ["RADICE"]).resolve() if os.environ.get("RADICE") else pathlib.Path(__file__).resolve().parents[2]
f = str(pathlib.Path(__file__).resolve().parents[2] / "registrazioni" / "regata-20261128-1434-intera.txt")  # il file sta fuori da git
T0, T1 = float(os.environ.get("T0", 380)), float(os.environ.get("T1", 397.48))
S, B = {}, {}
for r in open(f):
    p = r.split()
    if not p: continue
    if p[0] == "S" and len(p) > 8:
        t = float(p[1]);
        if T0 <= t <= T1: S[t] = [float(p[2]), float(p[3]), float(p[4]), float(p[5]), float(p[7])]
    if p[0] == "B" and len(p) > 7 and p[2] == "Blu":
        t = float(p[1])
        if T0 <= t <= T1: B[t] = [float(p[3]), float(p[4]), float(p[5]), float(p[6])]
snap = []; HA = HB = 0
for t in sorted(S):
    if t not in B: continue
    xa, ya, ha, ua, twa = S[t]; xb, yb, hb, ub = B[t]
    twd = ha + twa   # vento vero dal punto di Ale; si ruota tutto perché il vento venga da nord (0°)
    rot = math.radians(-twd); c, s = math.cos(rot), math.sin(rot)
    R = lambda x, y: (x * c - y * s, x * s + y * c)
    a = R(xa, ya); b = R(xb, yb)
    FZ = os.environ.get("FERMA"); TF = float(os.environ.get("TF", 0))
    if FZ == "Ale" and t >= TF: ha = HA
    if FZ == "Blu" and t >= TF: hb = HB
    if t < TF or not FZ: HA, HB = ha, hb
    snap.append([t, a[0], a[1], ha - twd, b[0], b[1], hb - twd, ua * 0.5144, ub * 0.5144])
JS = """(snap) => { const sv = __sv; sv.fast(0); sv.openItem(["r", 3]);
  const A = R.boats[0], B = R.boats[1]; R.boats.slice(2).forEach((b, k) => { b.S.x = 5000 + 300 * k; b.S.y = 5000; });
  R.prec = {}; R.phase = "race"; for (const b of R.boats){ delete b.storiaH; delete b.tkP; delete b.virP; delete b.sgV; b.virando = false; b.ocs = false; b.sconta = false; }
  const out = []; let prev = "", out16 = 0;
  for (const s of snap){ R.t = s[0]; Object.assign(A.S, { x: s[1], y: s[2], h: (s[3] + 720) % 360, u: s[7] }); Object.assign(B.S, { x: s[4], y: s[5], h: (s[6] + 720) % 360, u: s[8] });
    aggiornaVirate(); aggiornaPrecedenze();
    const c = chiCede1516(A, B), p = R.prec["0-1"], base = c.base || c;
    const nm = x => x === A ? "Ale" : x === B ? "Blu" : "-";
    const k = [nm(base.cede), base.regola, nm(c.cede), c.regola, p ? nm(p.autore) : "", p ? p.t : ""].join(" ");
    if (k !== prev) out.push(s[0].toFixed(2) + " base: cede " + nm(base.cede) + " (" + base.regola + ")  con 15-16: cede " + nm(c.cede) + " (" + c.regola + ")  cambio a " + (p ? p.t : "-") + " autore " + (p ? nm(p.autore) : "-") + "  mure A " + tackOf(A) + " B " + tackOf(B) + " dist " + Math.hypot(A.S.x-B.S.x, A.S.y-B.S.y).toFixed(1));
    prev = k;
    const ha = c.base ? (c.base.cede === A ? B : A) : (c.cede === A ? B : A), al = ha === A ? B : A, brg = bearingTo(ha.S, al.S); let w = null;
    for (const [t, h] of (ha.storiaH || [])) if (R.t - t <= T15 + 1e-9 && Math.abs(norm180(ha.S.h - h)) >= G16 && Math.abs(norm180(brg - ha.S.h)) < Math.abs(norm180(brg - h))) { w = [t, h]; break; }
    if (w && !out16) { out.push("   16 con tutta la finestra: " + nm(ha) + " a " + R.t.toFixed(2) + " (prua di " + w[0].toFixed(2) + ")"); out16 = 1; } else if (!w) out16 = 0; }
  return out; }"""
async def main():
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); pg = await br.new_page(viewport={"width": 1360, "height": 650})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
        for l in await pg.evaluate(JS, snap): print(l)
        print("passi", len(snap), "errori pagina", errs); await br.close()
asyncio.run(main())
