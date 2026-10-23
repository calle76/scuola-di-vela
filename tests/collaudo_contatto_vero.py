# Contatto vero fra gli scafi nell'1b (1.0.39, docs/PROPOSTA-CONTATTO-VERO.md, parte A).
# Parte 1: coppie di barche messe a mano (stesso passo, nessun avversario che si muova): l'1a (regata 0) usa il cerchio di 4,2 m fra i
#   centri, l'1b (regata 2, «salti di vento») il contorno dello scafo. Ogni caso dice se il contatto deve esserci nei due livelli.
# Parte 2: regate intere col pilota (semi 1-3, principianti ed esperti, 1a e 1b), passi di 1/240 s:
#   criterio 3 (1.0.41), nell'1b dopo il contatto gli scafi non restano sovrapposti: al massimo 0,5 s a regata e 0,25 m di penetrazione (prima 9 s e 1,37 m);
#   criterio 1, nell'1b ogni contatto scatta con gli scafi a meno di 5 cm (al passo prima); criterio 2, nell'1b nessuna sovrapposizione senza
#   contatto; e il numero di contatti, riportato senza soglia. Il controllo deve aver visto contatti (n > 0) e coppie vicine, altrimenti è non valido.
# Uso: python collaudo_contatto_vero.py
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; window.__seed = v => { s = v; }; })();"""

# poligono dello scafo e distanza fra scafi: scritti qui per conto loro, non letti dal gioco (il metro non deve dipendere da ciò che si misura)
GEO = """
const bez = (p0, p1, p2, p3) => { const o = []; for (let i = 1; i <= 10; i++){ const t = i / 10, u = 1 - t;
  o.push([u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0], u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]]); } return o; };
const LOC = [[0, -2.1], ...bez([0, -2.1], [0.55, -1.5], [0.72, -0.2], [0.68, 0.7]), [0.56, 2.1], [-0.56, 2.1], [-0.68, 0.7], ...bez([-0.68, 0.7], [-0.72, -0.2], [-0.55, -1.5], [0, -2.1])];
const hull = S => { const h = S.h * Math.PI / 180, c = Math.cos(h), s = Math.sin(h); return LOC.map(([x, y]) => [S.x + x * c - y * s, S.y + x * s + y * c]); };
const inside = (p, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++){ const [xi, yi] = poly[i], [xj, yj] = poly[j];
  if ((yi > p[1]) !== (yj > p[1]) && p[0] < (xj - xi) * (p[1] - yi) / (yj - yi) + xi) c = !c; } return c; };
const segd = (p, a, b) => { const dx = b[0] - a[0], dy = b[1] - a[1], l = dx*dx + dy*dy; let t = l ? ((p[0]-a[0])*dx + (p[1]-a[1])*dy) / l : 0; t = Math.max(0, Math.min(1, t)); return Math.hypot(p[0] - a[0] - t*dx, p[1] - a[1] - t*dy); };
const clear = (A, B) => { const pa = hull(A), pb = hull(B); if (pa.some(p => inside(p, pb)) || pb.some(p => inside(p, pa))) return 0;
  let m = 1e9; for (const p of pa) for (let i = 0; i < pb.length; i++) m = Math.min(m, segd(p, pb[i], pb[(i + 1) % pb.length]));
  for (const p of pb) for (let i = 0; i < pa.length; i++) m = Math.min(m, segd(p, pa[i], pa[(i + 1) % pa.length])); return m; };
"""

# caso a mano: A in (0,0) con prua hA, B a (bx,by) con prua hB; si esegue un passo e si guarda se è nato un contatto
MANO = """([race, hA, hB, bx, by]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]); const R = sv.R, A = R.boats[1], B = R.boats[2];
  R.t = 30; for (const b of R.boats){ b.pen = 0; b.fin = null; b.S.capsized = false; }
  A.S.x = 0; A.S.y = 0; A.S.h = hA; B.S.h = hB; B.S.x = bx; B.S.y = by;
  R.boats[0].S.x = 500; R.boats[0].S.y = 500; R.boats[3].S.x = -500; R.boats[3].S.y = 500;
  R.contacts = {}; sv.run(1 / 600, 1);
  return Object.keys(R.contacts).length; }"""

# nome, prua A, prua B, B rispetto ad A (x, y), contatto nell'1a, contatto nell'1b
CASI = [
    ("affiancate a 3,0 m fra i centri (scafi a 1,6 m)", 45, 45, 3.0 * 0.7071, 3.0 * 0.7071, 1, 0),
    ("affiancate a 1,2 m fra i centri (scafi sovrapposti)", 45, 45, 1.2 * 0.7071, 1.2 * 0.7071, 1, 1),
    ("in fila a 3,5 m (si sovrappongono 0,7 m)", 45, 45, 3.5 * 0.7071, -3.5 * 0.7071, 1, 1),
    ("in fila a 4,3 m (separati)", 45, 45, 4.3 * 0.7071, -4.3 * 0.7071, 0, 0),
    ("in fila a 4,15 m (sovrapposti di 5 cm)", 45, 45, 4.15 * 0.7071, -4.15 * 0.7071, 1, 1),
    ("a T a 3,2 m (la poppa di B a 1,1 m dal fianco di A)", 0, 90, 3.2, 0, 1, 0),
    ("a T a 2,5 m (la poppa di B dentro il fianco di A)", 0, 90, 2.5, 0, 1, 1),
    ("lontane a 5 m", 0, 0, 5.0, 0, 0, 0),
]

SIM = """([race, seme, liv]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, me = R.boats[0], dt = 1 / 240;
""" + GEO + """
  const salva = () => R.boats.map(b => ({ x: b.S.x, y: b.S.y, h: b.S.h }));
  const out = { contatti: 0, maxDist: 0, sovrapposti: 0, vicine: 0, passi: 0, secSov: 0, maxPen: 0 }, visti = new Set();
  let prev = salva();
  const passo = () => {
    for (const key of Object.keys(R.contacts)){ const id = key + ":" + R.contacts[key]; if (visti.has(id)) continue; visti.add(id);
      const [i, j] = key.split("-").map(Number); out.contatti++; out.maxDist = Math.max(out.maxDist, clear(prev[i], prev[j])); }
    const bs = R.boats;
    for (let i = 0; i < bs.length; i++) for (let j = i + 1; j < bs.length; j++){
      const A = bs[i], B = bs[j]; if (A.fin !== null || B.fin !== null || A.dnf || B.dnf || A.S.capsized || B.S.capsized) continue;
      if (Math.hypot(A.S.x - B.S.x, A.S.y - B.S.y) > 5) continue;
      out.vicine++; if (clear(A.S, B.S) === 0 && !R.contacts[i + "-" + j]) out.sovrapposti++;
      const o = sv.hullOverlap(A.S, B.S); if (o){ out.secSov += dt; out.maxPen = Math.max(out.maxPen, o.pen); } }   // 1.0.41: scafi che restano sovrapposti dopo il contatto
  };
  let n = 0;
  while (me.fin === null && !me.dnf && R.t < 900){ prev = salva(); sv.pilota(dt); sv.run(dt, 1); passo(); n++; }
  let k = 0; while (k++ < 240 * 300 && !R.boats.every(b => b.fin !== null || b.dnf)){ prev = salva(); sv.run(dt, 1); passo(); n++; }
  out.passi = n; out.lv2 = R.lv2; return out; }"""

async def main():
    fail = []; casi = 0
    def chk(ok, msg):
        nonlocal casi
        casi += 1
        if not ok: fail.append(msg); print("FALLITO:", msg)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650}); await pg.add_init_script(SEME)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
        print("== parte 1: coppie a mano")
        for nome, hA, hB, bx, by, c1a, c1b in CASI:
            r1 = await pg.evaluate(MANO, [0, hA, hB, bx, by]); r2 = await pg.evaluate(MANO, [2, hA, hB, bx, by])
            print(f"  {nome:58s} 1a: {r1} (atteso {c1a})  1b: {r2} (atteso {c1b})")
            chk(r1 == c1a, f"1a, {nome}: contatti {r1}, attesi {c1a}"); chk(r2 == c1b, f"1b, {nome}: contatti {r2}, attesi {c1b}")
        print("== parte 2: regate intere (passi di 1/240 s)")
        tot = {0: [0, 0, 0, 0.0, 0, 0.0, 0.0], 2: [0, 0, 0, 0.0, 0, 0.0, 0.0]}  # contatti, sovrapposti, vicine, distanza max, corse, secondi sovrapposti, penetrazione max
        for race in (0, 2):
            for seme in (1, 2, 3):
                for liv in ("principianti", "esperti"):
                    r = await pg.evaluate(SIM, [race, seme, liv]); t = tot[race]
                    t[0] += r["contatti"]; t[1] += r["sovrapposti"]; t[2] += r["vicine"]; t[3] = max(t[3], r["maxDist"]); t[4] += 1; t[5] += r["secSov"]; t[6] = max(t[6], r["maxPen"])
        for race, nome in ((0, "1a (regata a bastone)"), (2, "1b (salti di vento)")):
            c, s_, v, d, n, ss, mp = tot[race]
            print(f"  {nome}: {n} corse, contatti {c} ({c / n:.1f} a regata), istanti con barche entro 5 m {v}, sovrapposizioni senza contatto {s_}, distanza massima fra scafi al contatto {d:.3f} m, scafi sovrapposti {ss / n:.2f} s a regata, penetrazione massima {mp:.2f} m")
        c, s_, v, d, n, ss, mp = tot[2]
        chk(ss / n <= 0.5 and mp <= 0.25, f"1b: scafi sovrapposti {ss / n:.2f} s a regata (atteso al massimo 0,5) e penetrazione massima {mp:.2f} m (attesa al massimo 0,25)")   # attese scritte il 24 ottobre, prima di vedere i numeri: prima della 1.0.41 erano 9 s e 1,37 m
        chk(v > 0 and c > 0, "1b: il controllo non ha misurato niente (nessuna coppia vicina o nessun contatto)")
        chk(s_ == 0, f"1b: {s_} istanti con scafi sovrapposti e nessun contatto")
        chk(d <= 0.05, f"1b: un contatto è scattato con gli scafi a {d:.3f} m al passo prima (soglia 0,05 m)")
        chk(tot[0][0] > 0, "1a: nessun contatto misurato")
        chk(not errs, f"errori della pagina: {errs[:3]}")
        await b.close()
    print(f"controlli: {casi}, falliti: {len(fail)}")
    print("ESITO:", "OK" if casi and not fail else "FALLITO"); sys.exit(1 if fail or not casi else 0)
asyncio.run(main())
