# Medaglie delle prove (1.2.11, docs/PROPOSTA-MEDAGLIE-E-NOMI.md §3, soglie scritte prima).
# Il pilota preciso è quello di collaudo_fasce.py (decide ogni 0,1 s, bolina a 52°, vela regolata). Quello «con errori tipici» decide ogni 0,5 s,
# stringe a 60° e tiene la scotta 0,12 più lasca: tre ipotesi nostre, non misure di principianti veri. Passi fissi di 1/60 s, una pagina nuova per corsa.
#   M3a: pilota preciso, 30 corse su 30 finite, almeno 25 su 30 entro l'oro, in ogni prova
#   M3b: pilota con errori, almeno 25 su 30 entro il bronzo, in ogni prova
#   M3c: pilota con errori, oro al massimo in 5 su 30, in ogni prova (il metro deve distinguere)
#   M3d: a corsa finita il pallino del menu è quello calcolato dal tempo, uno per prova
# Le bande si leggono dal gioco. Uso: python collaudo_medaglie.py [--semi 101-130] [--prove 12345] [--scelta]
#   --scelta: non controlla niente, stampa cosa dà la regola (semi 1-30): oro = mediana ai 5 s superiori, poi +5 s finché 25 su 30; argento ×1,25, bronzo ×1,6 ai 5 s più vicini
import asyncio, os, pathlib, statistics, sys
import metro   # controlli che cadono anche a zero casi (docs/PROPOSTA-TEST-DEI-TEST.md)
from playwright.async_api import async_playwright
URL = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri() + "#collaudo"
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
GIUSTO = [60, 0, -60]
PIANI = [[], [], [], [[0, GIUSTO]], [[0, GIUSTO], [1, GIUSTO]]]   # gli stessi di collaudo_fasce.py: i punti attorno alle boe
PRECISO = {"passo": 6, "bolina": 52, "lasca": 0}; ERRORI = {"passo": 30, "bolina": 60, "lasca": 0.12}
N_CORSE = 30
CORSA = """
([plan, E]) => {
  const sv = __sv, D = Math.PI / 180, n180 = a => ((a + 180) % 360 + 360) % 360 - 180;
  const pts = [];
  for (const [k, angs] of plan) { const m = sv.marks[k];
    for (const a of angs) { const b = (m.out + a) * D; pts.push({ x: m.x + Math.sin(b) * 13, y: m.y - Math.cos(b) * 13 }); } }
  const last = sv.marks[sv.marks.length - 1]; pts.push({ x: last.x, y: last.y });
  let i = 0, side = 1, n = 0, tieni = false;
  sv.fast(0);
  while (!sv.S.finished && n < 60 * 900) {
    const S = sv.S;
    if (n % E.passo === 0 && i < pts.length) {
      const p = pts[i]; if (Math.hypot(p.x - S.x, p.y - S.y) < 7 && i < pts.length - 1) i++;
      const q = pts[Math.min(i, pts.length - 1)];
      const brg = Math.atan2(q.x - S.x, -(q.y - S.y)) / D, rel = n180(brg - sv.twd);
      let want = brg;
      if (Math.abs(rel) < E.bolina) { if (S.u > 1.7) tieni = false; if (Math.abs(rel) > 12 && !tieni) side = Math.sign(rel); want = sv.twd + side * E.bolina; }
      const cur = n180(S.h - sv.twd);
      if (Math.abs(rel) > 168 && Math.abs(cur) > 90) want = sv.twd + Math.sign(cur || 1) * 168;
      if (Math.abs(cur) < 48 && S.u < 0.8) { want = sv.twd + Math.sign(cur || 1) * 95; side = Math.sign(cur || 1); tieni = true; }
      const err = n180(S.h - want);
      sv.ctl.tiller = Math.max(-1, Math.min(1, err / 20 + S.r * 0.02)) * (S.u < 0 ? -1 : 1);
      const gybe = (Math.abs(cur) > 150 && Math.sign(n180(want - sv.twd)) !== Math.sign(cur)) || Math.abs(cur) > 174;
      sv.ctl.sheet = gybe ? Math.min(sv.autoSheet(), 0.3) : Math.min(1, sv.autoSheet() + E.lasca);
      if (S.capsized && !S.righting) dispatchEvent(new KeyboardEvent("keydown", { key: "a" }));
    }
    sv.run(1 / 60, 1); n++;
  }
  return [!!sv.S.finished, sv.S.time];
}
"""
bad = []
def chk(ok, m):
    print(("OK   " if ok else "FALLITO ") + m, flush=True)
    if not ok: bad.append(m)
async def corsa(b, idx, k, seme0, E, menu=False):
    pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.add_init_script(SEME); await pg.goto(URL); await pg.wait_for_timeout(200)
    await pg.evaluate(f"__seed({seme0 + k})")
    await pg.evaluate(f"__sv.openItem(['m',{idx}])"); await pg.evaluate(f"__sv.startMission({idx}, {(k * 45) % 360})")
    fin, t = await pg.evaluate(CORSA, [PIANI[idx], E])
    pallino = None
    if menu and fin:   # il giocatore torna al menu e legge il pallino sulla voce della prova
        await pg.evaluate("showMenu()")
        titolo = await pg.evaluate(f"MISSIONS[{idx}].title")
        for g in range(3):
            await pg.click(f"#schede button[data-g='{g}']")
            r = await pg.evaluate("""t => { const v = [...document.querySelectorAll('#menu button.item[data-k]')].find(b => b.querySelector('.title').textContent === t);
              if (!v) return null; const m = v.querySelector('.medal'); return m ? m.className : ""; }""", titolo)
            if r is not None: pallino = r; break
    bande = await pg.evaluate(f"MISSIONS[{idx}].bands")
    await pg.close()
    return fin, t, bande, pallino, errs
def regola(tempi):
    oro = 5 * ((int(statistics.median(tempi)) // 5) + 1)
    while sum(t <= oro for t in tempi) < 25: oro += 5
    piu_vicino = lambda v: int(v / 5 + 0.5) * 5
    return [oro, piu_vicino(oro * 1.25), piu_vicino(oro * 1.6)]
async def main():
    a = sys.argv[1:]; scelta = "--scelta" in a
    primo, ultimo = map(int, (a[a.index("--semi") + 1] if "--semi" in a else ("1-30" if scelta else "101-130")).split("-"))
    prove = [int(c) - 1 for c in (a[a.index("--prove") + 1] if "--prove" in a else "12345")]
    n = ultimo - primo + 1
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); errori = []
        print(f"semi {primo}-{ultimo}, {n} corse per prova e per pilota", flush=True)
        if n != N_CORSE and not scelta: chk(False, f"le soglie sono scritte per {N_CORSE} corse, qui {n}")
        for idx in prove:
            pr = []; er = []
            for k in range(n):
                fin, t, bande, _, e = await corsa(b, idx, k, primo, PRECISO); errori += e; pr.append((fin, t))
            ok_t = [t for f, t in pr if f]
            if scelta:
                print(f"prova {idx + 1}: finite {len(ok_t)} su {n}, mediana {statistics.median(ok_t):.1f}, min {min(ok_t):.1f}, max {max(ok_t):.1f}; oggi {bande}, la regola dà {regola(ok_t)}", flush=True); continue
            for k in range(n):
                fin, t, bande, _, e = await corsa(b, idx, k, primo, ERRORI); errori += e; er.append((fin, t))
            ok_e = [t for f, t in er if f]
            print(f"prova {idx + 1}: bande {bande}", flush=True)
            print(f"  preciso: finite {len(ok_t)}, mediana {statistics.median(ok_t):.1f}, min {min(ok_t):.1f}, max {max(ok_t):.1f}, oro {sum(t <= bande[0] for t in ok_t)}", flush=True)
            print(f"  con errori: finite {len(ok_e)}, mediana {statistics.median(ok_e) if ok_e else 0:.1f}, min {min(ok_e, default=0):.1f}, max {max(ok_e, default=0):.1f}, oro {sum(t <= bande[0] for t in ok_e)}, argento {sum(bande[0] < t <= bande[1] for t in ok_e)}, bronzo {sum(bande[1] < t <= bande[2] for t in ok_e)}, nessuna {n - sum(t <= bande[2] for t in ok_e)}", flush=True)
            oro = sum(t <= bande[0] for t in ok_t)
            chk(len(ok_t) == n and oro >= 25, f"M3a prova {idx + 1}: finite {len(ok_t)} su {n}, entro l'oro {oro} (almeno 25)")
            bronzo = sum(t <= bande[2] for t in ok_e)
            chk(bronzo >= 25, f"M3b prova {idx + 1}: con errori entro il bronzo {bronzo} su {n} (almeno 25)")
            oro_e = sum(t <= bande[0] for t in ok_e)
            chk(len(ok_e) >= 25 and oro_e <= 5, f"M3c prova {idx + 1}: con errori oro {oro_e} su {len(ok_e)} finite (al massimo 5)")
        if not scelta:
            casi = []
            for idx in prove:
                fin, t, bande, pallino, e = await corsa(b, idx, 0, primo, PRECISO, menu=True); errori += e
                att = next((k + 1 for k in range(3) if t <= bande[k]), 0)
                casi.append(fin and pallino is not None and (f"m{att}" in pallino if att else pallino == ""))
                print(f"  menu, prova {idx + 1}: {t:.1f} s, medaglia attesa {att}, pallino {pallino!r}", flush=True)
            chk(metro.tutti(casi, minimo=len(prove)), f"M3d: pallino del menu uguale a quello calcolato, {sum(casi)} su {len(prove)}")
        chk(metro.nessuno(errori, minimo=0), f"errori della pagina {errori[:3]}")
        await b.close()
    print("casi sbagliati:", bad or "nessuno"); print("ESITO: " + ("FALLITO" if bad else "OK"))
    sys.exit(1 if bad else 0)
asyncio.run(main())
