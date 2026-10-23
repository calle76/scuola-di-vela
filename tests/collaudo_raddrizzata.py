# Raddrizzata del livello 2 (1.0.32, docs/archivio/PROPOSTA-RADDRIZZATA.md). Pagina con #collaudo, passi di 1/60 s, tasti veri.
# Navigazione libera, 6/10/15/20 nodi, scuffiata da tutte e due le parti, livello 2 e livello 1 (confronto). Si preme A e si aspetta:
#  R1 livello 2: dritta dopo 10 s (non prima), a 90° ± 5° dal vento, ferma, scotta tutta lascata; livello 1: dopo 3 s a 60° come sempre;
#  R2 con la scotta lascata e la barra al centro la barca non riscuffia nei 10 s seguenti;
#  R3 poi si tiene ↑ (cazza) finché la scotta arriva alla regolazione giusta (autoSheet del gioco), si lascia, e si misura il tempo
#     fino a 2 nodi (riportato, nessuna soglia). Velocità e scotta di R1 si leggono nell'istante in cui la barca torna dritta.
# Avversari: nella «Regata nei salti di vento» un avversario fatto scuffiare apposta è ancora rovesciato a 14,5 s e dritto a 15,5 s,
# a 90° ± 5° dal vento locale nell'istante in cui torna dritto (livello 2); nella regata 1 (livello 1) è dritto dopo 5 s a 60°.
# Poi la pagina senza #collaudo: navigazione libera, nessun errore. Esce con 1 se un controllo fallisce.
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
falliti = []
def check(ok, testo):
    print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: falliti.append(testo)

APRI = """([kn, lv, lato]) => { const sv = __sv; sv.fast(0); sv.openItem('free');
  for (const [id, v] of [['wSpd', String(kn)], ['gustSel', '0'], ['wDir', '0'], ['boatLv', String(lv)]]){ const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); }
  sv.openItem('free'); if (sv.setShifts) sv.setShifts(null); const S = sv.S;
  Object.assign(S, { capsized: true, capSide: lato, u: 0, vl: 0, r: 0, heel: 90, heelRate: 0, righting: 0 }); sv.run(1 / 60, 30); return S.lv || 1; }"""
GIRA = """s => { const sv = __sv, S = sv.S; let tDritta = null;
  let u0 = null, sh0 = null;
  for (let i = 0; i < s * 60; i++){ sv.run(1 / 60, 1); if (tDritta === null && !S.capsized){ tDritta = (i + 1) / 60; u0 = S.u; sh0 = sv.ctl.sheet; } }
  return { tDritta, cap: S.capsized, twa: ((sv.twd - S.h + 540) % 360) - 180, u: u0, sheet: sh0 }; }"""
CAZZA = """() => { const sv = __sv; let i = 0; for (; i < 10 * 60 && sv.ctl.sheet > sv.autoSheet(); i++) sv.run(1 / 60, 1); return [sv.ctl.sheet, i / 60]; }"""
ATTENDI = """t0 => { const sv = __sv, S = sv.S; let t = t0; for (let i = 0; i < 30 * 60; i++){ sv.run(1 / 60, 1); t += 1 / 60; if (S.u * 1.944 >= 2) return t; if (S.capsized) return -1; } return null; }"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
        errori = []; pg.on("pageerror", lambda e: errori.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
        n = 0
        for lv in (2, 1):
            for kn in (6, 10, 15, 20):
                for lato in (1, -1):
                    lvv = await pg.evaluate(APRI, [kn, lv, lato]); n += 1
                    await pg.keyboard.press("a")
                    att = 10 if lv == 2 else 3
                    r = await pg.evaluate(GIRA, att + 0.5)
                    ang = 90 if lv == 2 else 60
                    ok1 = lvv == lv and r["tDritta"] is not None and abs(r["tDritta"] - att) < 0.2 and abs(abs(r["twa"]) - ang) <= 5 and \
                        (r["sheet"] == 1 and r["u"] < 0.05 if lv == 2 else True)
                    check(ok1, f"R1 livello {lv}, {kn} nodi, lato {lato:+d}: dritta dopo {r['tDritta']} s, {abs(r['twa']):.0f}° dal vento, "
                               f"{r['u'] * 1.944:.2f} nodi, scotta {r['sheet']:.2f}")
                    r2 = await pg.evaluate(GIRA, 10)
                    check(not r2["cap"], f"R2 livello {lv}, {kn} nodi, lato {lato:+d}: 10 s senza riscuffiare (ora {abs(r2['twa']):.0f}° dal vento)")
                    await pg.keyboard.down("ArrowUp"); sh, tc = await pg.evaluate(CAZZA); await pg.keyboard.up("ArrowUp")
                    t2 = await pg.evaluate(ATTENDI, tc)
                    print(f"  R3 livello {lv}, {kn} nodi, lato {lato:+d}: cazzata a {sh:.2f}, da ↑ a 2 nodi {t2 if t2 is None else round(t2, 1)} s")
        print(f"casi misurati: {n}")
        for regata, att, ang in ((2, 15, 90), (0, 5, 60)):
            r = await pg.evaluate("""([i, att]) => { const sv = __sv; sv.fast(0); sv.openItem(['r', i]); const R = sv.R;
              while (R.t < 20) sv.run(1 / 60, 1);
              const b = R.boats.find(b => b.ai), s = b.S; s.capsized = true; s.capT = 0; s.capSide = 1; s.u = 0;
              let prima = null, twa = null; for (let i = 0; i < (att + 0.5) * 60; i++){ const c = s.capsized; sv.run(1 / 60, 1); if (i === Math.round((att - 0.5) * 60)) prima = s.capsized;
                if (c && !s.capsized) twa = ((windAt(s.x, s.y).twd - s.h) % 360 + 540) % 360 - 180; }
              return { prima, dopo: s.capsized, twa: twa ?? 0, lv: s.lv || 1 }; }""", [regata, att])
            check(r["prima"] and not r["dopo"] and abs(abs(r["twa"]) - ang) <= 5,
                  f"avversario, livello {r['lv']}: rovesciato a {att - 0.5} s, dritto a {att + 0.5} s, {abs(r['twa']):.0f}° dal vento (atteso {ang})")
        await pg.goto("about:blank"); await pg.goto(BASE); await pg.wait_for_timeout(400)
        await pg.click("#goFree"); await pg.wait_for_timeout(300)
        check(not errori, f"nessun errore della pagina ({errori[:2]})")
        await b.close()
    print("ESITO: " + ("OK" if not falliti else f"FALLITO ({len(falliti)})")); sys.exit(1 if falliti else 0)

asyncio.run(main())
