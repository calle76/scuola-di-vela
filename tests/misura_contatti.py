# Misura dei contatti fra le barche in regata (23 ottobre 2026, docs/PROPOSTA-CONTATTO-VERO.md). Non è un collaudo: non ha soglie.
# Uso: python misura_contatti.py <regata 0-2> <attuale|senza> <primo seme> <ultimo seme>   (una riga JSON per corsa, principianti ed esperti)
#  attuale: contatti con la regola di oggi (cerchio di 4,2 m fra i centri), con la distanza fra i contorni degli scafi (m) al passo prima del contatto
#  senza:   mondo senza regola di contatto (le barche si attraversano): conta gli episodi in cui i contorni degli scafi si sovrappongono davvero
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent; BASE = (ROOT / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
JS = """([race, seme, liv, senza]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, me = R.boats[0], dt = 1 / 60;
  const bez = (p0, p1, p2, p3, n) => { const o = []; for (let i = 1; i <= n; i++){ const t = i / n, u = 1 - t;
    o.push([u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0], u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]]); } return o; };
  const LOC = [[0, -2.1], ...bez([0, -2.1], [0.55, -1.5], [0.72, -0.2], [0.68, 0.7], 10), [0.56, 2.1], [-0.56, 2.1], [-0.68, 0.7], ...bez([-0.68, 0.7], [-0.72, -0.2], [-0.55, -1.5], [0, -2.1], 10)];
  const hull = S => { const h = S.h * Math.PI / 180, c = Math.cos(h), s = Math.sin(h); return LOC.map(([x, y]) => [S.x + x * c - y * s, S.y + x * s + y * c]); };
  const inside = (p, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++){ const [xi, yi] = poly[i], [xj, yj] = poly[j];
    if ((yi > p[1]) !== (yj > p[1]) && p[0] < (xj - xi) * (p[1] - yi) / (yj - yi) + xi) c = !c; } return c; };
  const segd = (p, a, b) => { const dx = b[0] - a[0], dy = b[1] - a[1], l = dx*dx + dy*dy; let t = l ? ((p[0]-a[0])*dx + (p[1]-a[1])*dy) / l : 0; t = Math.max(0, Math.min(1, t)); return Math.hypot(p[0] - a[0] - t*dx, p[1] - a[1] - t*dy); };
  const clear = (A, B) => { const pa = hull(A), pb = hull(B); if (pa.some(p => inside(p, pb)) || pb.some(p => inside(p, pa))) return 0;
    let m = 1e9; for (const p of pa) for (let i = 0; i < pb.length; i++) m = Math.min(m, segd(p, pb[i], pb[(i + 1) % pb.length]));
    for (const p of pb) for (let i = 0; i < pa.length; i++) m = Math.min(m, segd(p, pa[i], pa[(i + 1) % pa.length])); return m; };
  const out = { contatti: [], sovrapposizioni: 0, minCentri: 1e9, esposti: 0, passi: 0 }, vistiContatti = new Set(), ep = {};
  const passo = () => {
    const bs = R.boats;
    for (let i = 0; i < bs.length; i++) for (let j = i + 1; j < bs.length; j++){
      const A = bs[i], B = bs[j], key = i + "-" + j; if (A.fin !== null || B.fin !== null || A.dnf || B.dnf || A.S.capsized || B.S.capsized) continue;
      const d = Math.hypot(A.S.x - B.S.x, A.S.y - B.S.y);
      if (senza && !R.contacts[key]) R.contacts[key] = -1;   // mondo senza contatti: la regola attuale non scatta mai
      if (d < 8){ out.esposti++; const c = clear(A.S, B.S); out.minCentri = Math.min(out.minCentri, d);
        if (c <= 0){ if (!ep[key]){ ep[key] = 1; out.sovrapposizioni++; } } else if (c > 1) ep[key] = 0; }
    }
  };
  let prev = null; const salva = () => R.boats.map(b => ({ x: b.S.x, y: b.S.y, h: b.S.h }));
  const rileva = () => { if (senza) return; for (const key of Object.keys(R.contacts)){ const id = key + ":" + R.contacts[key]; if (vistiContatti.has(id)) continue; vistiContatti.add(id);
      const [i, j] = key.split("-").map(Number), A = prev[i], B = prev[j]; out.contatti.push([+Math.hypot(A.x - B.x, A.y - B.y).toFixed(2), +clear(A, B).toFixed(2), R.lv2 ? 1 : 0]); } };
  let n = 0; const T = () => me.fin === null && !me.dnf && R.t < 900;
  while (T()){ prev = salva(); sv.pilota(dt); sv.run(dt, 1); rileva(); if (++n % 6 === 0) passo(); }
  let k = 0; while (k < 60 * 300 && !R.boats.every(b => b.fin !== null || b.dnf)){ prev = salva(); sv.run(dt, 1); rileva(); if (++k % 6 === 0) passo(); }
  out.passi = n; return out; }"""
async def main():
    race, senza, a, b_ = int(sys.argv[1]), sys.argv[2] == "senza", int(sys.argv[3]), int(sys.argv[4])
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1360,"height":650}); await pg.add_init_script(SEME)
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
        for seme in range(a, b_ + 1):
            for liv in ("principianti", "esperti"):
                r = await pg.evaluate(JS, [race, seme, liv, senza]); r.update(race=race, senza=senza, seme=seme, liv=liv); print(json.dumps(r), flush=True)
        print("ERR", errs[:3]); await b.close()
asyncio.run(main())
