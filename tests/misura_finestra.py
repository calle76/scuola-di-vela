# Soglia G della regola 16 (1.0.43, docs/PROPOSTA-REGOLE-PRECEDENZA-1B.md): quanto gira la prua, in T secondi, una barca dell'1b che ha la
# precedenza su un'altra vicina (entro 10 m) e non sta manovrando (stesse mure e niente virata in tutta la finestra). Non è un collaudo: non ha soglie.
# Regata dei salti di vento, semi a-b, principianti ed esperti, giocatore col pilota; campioni ogni 0,25 s. Esce il 95° percentile (la regola della proposta).
# Riga «da sola»: barche senza nessuna entro 30 m, dopo il via e oltre 20 m dalla boa, cioè le sole correzioni di rotta.
# Uso: python misura_finestra.py <primo seme> <ultimo seme> [T secondi, 5.2]
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent; BASE = (ROOT / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""
JS = """([seme, liv, T]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", 2]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, me = R.boats[0], bs = R.boats, dt = 1 / 60, n180 = v => ((v % 360) + 540) % 360 - 180, K = Math.round(T / 0.25);
  const storia = bs.map(() => []), out = [], sola = [];
  const tack = b => n180(sv.windAt(b.S.x, b.S.y).twd - b.S.h) < 0 ? -1 : 1;
  let passi = 0;
  const campione = () => {
    bs.forEach((b, i) => { storia[i].push({ h: b.S.h, m: tack(b), v: !!b.virando }); if (storia[i].length > K + 1) storia[i].shift(); });
    bs.forEach((A, i) => { const st = storia[i]; if (st.length <= K || A.fin !== null || A.dnf || A.S.capsized) return;
      if (st.some(c => c.m !== st[0].m || c.v)) return; // manovra nella finestra: non conta
      if (R.t > T && Math.hypot(A.S.x - R.mark.x, A.S.y - R.mark.y) > 20 && bs.every(B => B === A || Math.hypot(A.S.x - B.S.x, A.S.y - B.S.y) > 30))
        sola.push(Math.abs(n180(st[K].h - st[0].h))); // da sola, dopo il via e lontano dalla boa: solo le correzioni di rotta
      for (const B of bs){ if (B === A || B.fin !== null || B.dnf || B.S.capsized || Math.hypot(A.S.x - B.S.x, A.S.y - B.S.y) > 10) continue;
        if (sv.chiCede(A, B).cede === B){ const br = Math.atan2(B.S.x - A.S.x, -(B.S.y - A.S.y)) * 180 / Math.PI; // direzione in cui A vede B
          out.push([Math.abs(n180(st[K].h - st[0].h)), Math.abs(n180(br - st[K].h)) < Math.abs(n180(br - st[0].h)), R.t < 0]); break; } } });
  };
  const passo = () => { if (++passi % 15 === 0) campione(); };
  while (me.fin === null && !me.dnf && R.t < 900){ sv.pilota(dt); sv.run(dt, 1); passo(); }
  let k = 0; while (k++ < 60 * 300 && !bs.every(b => b.fin !== null || b.dnf)){ sv.run(dt, 1); passo(); }
  return [out, sola]; }"""
async def main():
    a, z = int(sys.argv[1]), int(sys.argv[2]); T = float(sys.argv[3]) if len(sys.argv) > 3 else 5.2
    async with async_playwright() as p:
        b = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch(); pg = await b.new_page(viewport={"width":1360,"height":650}); await pg.add_init_script(SEME)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_function("window.__sv")
        v = []; sola = []
        for seme in range(a, z + 1):
            for liv in ("principianti", "esperti"): r = await pg.evaluate(JS, [seme, liv, T]); v += r[0]; sola += r[1]
        def riga(nome, w):
            w = sorted(w); pc = lambda q: w[min(len(w) - 1, int(q * len(w)))]
            print(f"  {nome}: {len(w)} campioni; mediano {pc(0.5):.1f}°, 90° {pc(0.9):.1f}°, 95° {pc(0.95):.1f}°, 99° {pc(0.99):.1f}°, massimo {w[-1]:.1f}°" if w else f"  {nome}: 0 campioni")
        print(f"semi {a}-{z}, T {T} s, errori {errs[:2]}")
        riga("tutti", [c[0] for c in v]); riga("verso l'altra", [c[0] for c in v if c[1]]); riga("allontanandosi", [c[0] for c in v if not c[1]])
        riga("prima del via", [c[0] for c in v if c[2]]); riga("dopo il via", [c[0] for c in v if not c[2]]); riga("verso l'altra, dopo il via", [c[0] for c in v if c[1] and not c[2]])
        riga("da sola (nessuna entro 30 m, dopo il via, oltre 20 m dalla boa)", sola)
        await b.close()
asyncio.run(main())
