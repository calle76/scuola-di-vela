# Lezione 18, passo «Stare fermi» (voce 27, 1.3.58; docs/PROPOSTA-LEZIONE-STARE-FERMI.md §4, soglie scritte prima).
#   F1 il pilota coi soli tasti della scotta (W e S veri) completa il passo in almeno 18 semi su 20. Il vento del passo è costante: i semi cambiano il giocatore
#      (reazione 0,15-0,4 s, colpo 0,08-0,3 s), che legge la velocità come nel pannello, arrotondata a un decimo di nodo.
#   F2 senza toccare la scotta il passo non si completa (almeno 18 su 20; qui il caso è uno solo, deterministico: si ripete per semi solo come controllo del metro).
#      In più, riportati e senza soglia: prua a 50° e 55° senza toccare la scotta (chi poggia un poco e non tocca la scotta).
#   F4 pannello a 1360x650 senza pixel di eccesso, prima e dopo il passo. F5 pagina senza #collaudo: il passo si apre, il cerchio c'è, l'errore no.
# Uso: python collaudo_stare_fermi.py [--semi 1-20]   (browser con BROWSER=firefox). L'esercizio della lezione 19 (F3) è in collaudo_esercizi_regata.py (C2).
import asyncio, os, pathlib, sys
import metro   # controlli che cadono anche a zero casi
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
APRI = """() => { const sv = __sv; sv.fast(0); sv.openItem(["l", 18]); const i = LESSONS[18].steps.findIndex(s => s.startFermo); sv.showStep(i); return [i, LESSONS[18].steps[i].title, FERMI_S, FERMI_R, FERMI_KN]; }"""
CORSA = """([seme, modo, prua]) => { const sv = __sv, dt = 1 / 60; let s = seme * 7919 + 1; const rnd = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  sv.showStep(LESSONS[18].steps.findIndex(x => x.startFermo)); S.h = norm360(env.twd - prua);
  const tasto = (t, k) => dispatchEvent(new KeyboardEvent(t, { key: k })); let giu = null;
  const rt = 0.15 + rnd() * 0.25; let t = 0, dMax = 0, uMax = 0, uscito = null, scMin = 2, scMax = -1;
  const passi = n => { for (let k = 0; k < n; k++){ sv.run(dt, 1); t += dt; const d = Math.hypot(S.x - S.cerchio.x, S.y - S.cerchio.y); if (!sv.stepDone && d > dMax) dMax = d; if (d > S.cerchio.r && uscito === null && !sv.stepDone) uscito = t;
    uMax = Math.max(uMax, Math.abs(S.u * KN)); if (t > 10){ scMin = Math.min(scMin, ctl.sheet); scMax = Math.max(scMax, ctl.sheet); } if (sv.stepDone) return true; } return false; };
  while (t < 90 && !sv.stepDone && S.cerchio){
    const v = Math.round(S.u * KN * 10) / 10;  // la velocità come si legge nel pannello
    if (modo === "scotta" && v){ const k = v < 0 ? "w" : "s"; tasto("keydown", k); passi(Math.round((0.08 + rnd() * 0.22) * 60)); tasto("keyup", k); }
    if (passi(Math.round(rt * 60))) break;
  }
  tasto("keyup", "w"); tasto("keyup", "s");
  return { ok: sv.stepDone, t: +t.toFixed(1), dMax: +dMax.toFixed(1), uMax: +uMax.toFixed(2), uscito, scMin: +scMin.toFixed(2), scMax: +scMax.toFixed(2) }; }"""
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + str(extra) if extra != "" else ""), flush=True)
    if not ok: bad.append(nome)
async def main():
    a = sys.argv[1:]; x, y = (a[a.index("--semi") + 1] if "--semi" in a else "1-20").split("-"); semi = list(range(int(x), int(y) + 1)); n = len(semi); soglia = 0.9 * n
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script("window.requestAnimationFrame = () => 0;")
        pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(300)
        print("passo:", await pg.evaluate(APRI))
        G = [await pg.evaluate(CORSA, [s, "scotta", 45]) for s in semi]; M = [await pg.evaluate(CORSA, [s, "mani", 45]) for s in semi]
        ok = sum(r["ok"] for r in G)
        chk("F1 pilota coi tasti della scotta: passo completato in almeno 18 semi su 20", metro.tutti(True for r in G) and ok >= soglia, f"{ok} su {n}; scarroccio massimo {max(r['dMax'] for r in G)} m, mediano {sorted(r['dMax'] for r in G)[n // 2]} m; tempo {min(r['t'] for r in G)}-{max(r['t'] for r in G)} s; velocità massima {max(r['uMax'] for r in G)} nodi; scotta dopo 10 s {min(r['scMin'] for r in G)}-{max(r['scMax'] for r in G)}")
        no = sum(not r["ok"] for r in M)
        chk("F2 senza toccare la scotta il passo non si completa", metro.tutti(True for r in M) and no >= soglia, f"{no} su {n}; esce dal cerchio dopo {M[0]['uscito']:.1f} s" if M[0]["uscito"] else f"{no} su {n}; mai uscito")
        chk("F2b il metro vede l'uscita dal cerchio", metro.tutti(r["uscito"] is not None for r in M if not r["ok"]))
        for q in (50, 55): r = await pg.evaluate(CORSA, [1, "mani", q]); print(f"     (riportato) prua a {q}° senza toccare la scotta: {'completato' if r['ok'] else 'non completato'}, {r}")
        ecc = []
        for fine in (False, True):
            await pg.evaluate(APRI)
            await pg.evaluate("f => { if (f) completeStep(); __sv.run(1/60, 2); __sv.panel(); }", fine)
            ecc.append(await pg.evaluate("() => { const p = document.querySelector('.panel'); return [p.scrollHeight - p.clientHeight, document.documentElement.scrollHeight - innerHeight]; }"))
        chk("F4 pannello a 1360x650 senza eccesso, prima e dopo il passo", metro.tutti(e[0] <= 0 and e[1] <= 0 for e in ecc), ecc)
        chk("A0 nessun errore di pagina", not errs, errs[:2]); await ctx.close()
        # ---- pagina come la carica un giocatore ----
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri()); await pg.wait_for_timeout(300)
        await pg.evaluate("() => openItem(['l', 18])"); await pg.wait_for_timeout(200); await pg.click("#lNext"); await pg.wait_for_timeout(200)
        v0 = await pg.evaluate("() => [document.getElementById('lTitle').textContent, document.getElementById('hint').hidden, document.getElementById('hint').textContent, !!S.cerchio]")
        await pg.keyboard.down("w"); await pg.wait_for_timeout(2000); await pg.keyboard.up("w"); await pg.wait_for_timeout(500)
        v1 = await pg.evaluate("() => [S.u * KN, ctl.sheet, holdT]")
        await pg.click("#lRetry"); await pg.wait_for_timeout(100); v2 = await pg.evaluate("() => [ctl.sheet, Math.hypot(S.x - S.cerchio.x, S.y - S.cerchio.y), Math.abs(norm180(env.twd - S.h))]")
        chk("F5 senza #collaudo: il passo si apre, W cazza, il conto va avanti e Ricomincia rimette la barca ferma a 45°", v0[0] == "Stare fermi" and not v0[1] and v0[3] and v1[1] < 0.7 and v1[2] > 1 and v2[0] > 0.9 and v2[1] < 0.3 and 40 < v2[2] < 50 and not errs, f"{v0} {v1} {v2} {errs[:1]}")
        await ctx.close(); await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad); sys.exit(1 if bad else 0)
asyncio.run(main())
