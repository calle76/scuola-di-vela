# Regate a 6 barche (1.2.38, docs/PROPOSTA-NAZIONALE.md, passo 1; soglie scritte nella fermata 1 prima del codice).
#   N1 posizioni di partenza: 1000 partenze con 6 barche (500 con preparazione di 60 s, 500 con 180 s): distanze >= 20 m e nessuna rotta
#      di collisione sotto 14 m entro 25 s (ricontrollate QUI); ripiego al massimo nell'1%; il ripiego stesso rispetta le distanze.
#   N2 partenze pulite: 100 regate da 6 col pilota (25 tornei a 6, semi fissi): contatti nei primi 25 s dopo la nascita = 0.
#   N3 precedenze: le stesse 100 regate tutte finite (nessuna ferma fino a 1500 s); contatti per coppia di barche per regata al massimo
#      il doppio di quelli con 4 barche sugli stessi semi (100 regate da 4).
#   N4 velocità: tempo di calcolo di 600 passi con 6 barche al massimo 1,8 volte quello con 4, Chromium e Firefox (il migliore di 3 prove).
#   N6 pannello a 1360x650: pannello di regata con 6 barche, finestra del torneo a 6 righe dopo 4 regate, ognuna delle 5 schede.
#   (N5, scritte con 6 barche: misura_etichette.py con SEI=1. N7: impronta del guardiano, polare, raffiche, impronta1b, collaudi della stagione.)
# Uso: python collaudo_sei_barche.py [--tornei N] [--veloce]   (--veloce: solo N1, N4, N6 e un torneo a 6)
import asyncio, math, pathlib, sys
from playwright.async_api import async_playwright
QUI = pathlib.Path(__file__).resolve().parent
BASE = (QUI.parent / "index.html").as_uri()
NT = int(sys.argv[sys.argv.index("--tornei") + 1]) if "--tornei" in sys.argv else 25
VELOCE = "--veloce" in sys.argv
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
errori = []
def no(m): errori.append(m); print("  NO  " + m, flush=True)

async def pagina(bt, nome):
    ctx = await bt.new_context(viewport={"width": 1360, "height": 650})
    pg = await ctx.new_page(); await pg.add_init_script(SEME)
    pg.on("pageerror", lambda e: no(f"errore pagina {nome}: {e}"))
    pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
    await pg.evaluate("() => { __sv.fast(0); const e = document.getElementById('cdSel'); e.value = '60'; e.dispatchEvent(new Event('change')); }")
    return pg

def n1_ok(P):
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            a, c = P[i], P[j]; rx, ry = c["x"] - a["x"], c["y"] - a["y"]
            if math.hypot(rx, ry) < 20 - 1e-9: return False
            vx = c["s"] - a["s"]
            if vx * vx < 1e-6: continue
            t = -(rx * vx) / (vx * vx)
            if 0 < t <= 25 and math.hypot(rx + vx * t, ry) < 14: return False
    return True
def ripiego(P, cd):   # la forma del ripiego per n > 4 (startSpots): due file a 20 m
    n = len(P); yMin = 26 if cd <= 60 else 38
    att = [(-35 + (k // 2) * (70 / max(1, math.ceil(n / 2) - 1)) + (k % 2) * 17.5 - 8.75, yMin + (k % 2) * 20) for k in range(n)]
    return all(abs(p["x"] - x) < 1e-9 and abs(p["y"] - y) < 1e-9 for p, (x, y) in zip(P, att))

TORNEO = """([seme, sei]) => { const sv = __sv; __seed(seme); if (sv.tor){ sv.torApri(); const r = document.getElementById('torRit'); if (r) r.click(); }
  delete sv.progress.torneo; delete sv.progress.stagione; sv.torApri(); if (sei) document.getElementById('torN6').click(); return sv.tor ? -1 : document.querySelectorAll('#torBody .tor-sei').length; }"""
CORRI = """async (dt) => { const sv = __sv; dt = 1 / 60;
  document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], t0 = R.t; let n = 0, presto = 0, fino = 0;
  while (R.t < 1500 && R.boats.some(b => b.fin === null && !b.dnf)){ if (me.fin === null && !me.dnf) sv.pilota(dt); sv.run(dt, 1);
    for (; n < R.penList.length; n++) if (R.penList[n].includes("contatto con")){ fino++; if (R.t - t0 < 25) presto++; } }
  const ferma = R.t >= 1500; document.getElementById("rTor").click();
  return { barche: R.boats.length, contatti: fino, presto, ferma, t: R.t }; }"""
VELOC = """async (sei) => { const sv = __sv; __seed(4242); if (sv.tor){ sv.torApri(); const r = document.getElementById('torRit'); if (r) r.click(); }
  delete sv.progress.torneo; sv.torApri(); if (sei) document.getElementById('torN6').click(); document.getElementById('torGo').click();
  const R = sv.R; sv.run(1 / 60, 60 * 70); const t = [];
  for (let k = 0; k < 3; k++){ const a = performance.now(); sv.run(1 / 60, 600); t.push(performance.now() - a); }
  const n = R.boats.length; document.getElementById('torDlg').open || null; return { n, ms: Math.min(...t) }; }"""
PANNELLO = """() => { const d = document.getElementById('torDlg'), q = document.getElementById('torBody'), r = d.getBoundingClientRect();
  const btn = [...q.querySelectorAll('button')].map(b => b.getBoundingClientRect().bottom);
  return { aperto: d.open, dentro: r.top >= 0 && r.bottom <= innerHeight, scorreRiquadro: d.scrollHeight - d.clientHeight, scorreContenuto: q.scrollHeight - q.clientHeight,
           larg: Math.max(d.scrollWidth - d.clientWidth, q.scrollWidth - q.clientWidth), pulsanti: btn.length && btn.every(b => b <= r.bottom && b <= innerHeight) }; }"""
def pannello(o, cosa):
    print(f"  N6 {cosa}: {o}")
    if not o["aperto"] or not o["dentro"] or o["scorreRiquadro"] > 0 or o["scorreContenuto"] > 0 or o["larg"] > 0 or not o["pulsanti"]: no(f"N6 {cosa}: {o}")

async def main():
    async with async_playwright() as p:
        ch = await p.chromium.launch(); pg = await pagina(ch, "Chromium")
        # N1
        rip = bad = 0
        for k in range(1000):
            cd = 60 if k < 500 else 180
            P = await pg.evaluate("([s, cd]) => { __seed(s); return __sv.startSpots(6, cd); }", [70000 + k, cd])
            if not n1_ok(P): bad += 1; no(f"N1 partenza {k}: vincoli non rispettati")
            if ripiego(P, cd): rip += 1
        print(f"N1: 1000 partenze da 6, vincoli violati {bad}, ripiego {rip}")
        if rip > 10: no(f"N1: ripiego {rip} volte su 1000")
        # il ripiego da solo: costruito a mano con n = 5 e 6 e controllato
        for n in (5, 6):
            for cd in (60, 180):
                yMin = 26 if cd <= 60 else 38
                P = [{"x": -35 + (k // 2) * (70 / max(1, math.ceil(n / 2) - 1)) + (k % 2) * 17.5 - 8.75, "y": yMin + (k % 2) * 20, "s": 1 if k % 2 else -1} for k in range(n)]
                if not n1_ok(P): no(f"N1: il ripiego con {n} barche non rispetta i vincoli")
        # N4
        for nome, bt in (("Chromium", ch), ("Firefox", None)):
            if bt is None: ff = await p.firefox.launch(); q = await pagina(ff, "Firefox")
            else: q = pg
            v4 = await q.evaluate(VELOC, 0); v6 = await q.evaluate(VELOC, 1)
            rapp = v6["ms"] / v4["ms"]
            print(f"N4 {nome}: 600 passi con {v4['n']} barche {v4['ms']:.0f} ms, con {v6['n']} barche {v6['ms']:.0f} ms, rapporto {rapp:.2f}")
            if v6["n"] != 6 or v4["n"] != 4: no(f"N4 {nome}: barche {v4['n']} e {v6['n']}")
            if rapp > 1.8: no(f"N4 {nome}: rapporto {rapp:.2f} > 1,8")
            if bt is None: await ff.close()
        await pg.reload(); await pg.wait_for_timeout(300)
        await pg.evaluate("() => { __sv.fast(0); const e = document.getElementById('cdSel'); e.value = '60'; e.dispatchEvent(new Event('change')); }")
        # N6: pannello di regata con 6 barche, a 2 minuti dal via (torneo a parte, seme 999)
        await pg.evaluate(TORNEO, [999, 1])
        await pg.evaluate("() => { document.getElementById('torGo').click(); __sv.run(1 / 60, 60 * 180); __sv.panel && __sv.panel(); }"); await pg.wait_for_timeout(300)
        ph = await pg.evaluate("() => { const p = document.querySelector('.panel'); return [p.scrollHeight - p.clientHeight, document.documentElement.scrollHeight - innerHeight, __sv.R.boats.length]; }")
        print(f"  N6 pannello di regata con {ph[2]} barche: eccesso {ph[0]} px, pagina {ph[1]} px"); await pg.screenshot(path=str(QUI / "output" / "sei_barche_regata.png"))
        if ph[0] > 0 or ph[1] > 0 or ph[2] != 6: no(f"N6 pannello di regata: {ph}")
        await pg.reload(); await pg.wait_for_timeout(300)
        await pg.evaluate("() => { __sv.fast(0); const e = document.getElementById('cdSel'); e.value = '60'; e.dispatchEvent(new Event('change')); }")
        # N2, N3 (e N6 alla fine del primo torneo a 6)
        tot = {4: [0, 0, 0, 0], 6: [0, 0, 0, 0]}   # regate, contatti, presto, ferme
        for t in range(1 if VELOCE else NT):
            for sei in ((1,) if VELOCE else (0, 1)):
                b = await pg.evaluate(TORNEO, [880 + t, sei])
                if b != 1: no(f"torneo {t}: la scelta delle barche non c'è ({b})")
                for k in range(4):
                    await pg.evaluate("s => __seed(s)", (880 + t) * 100 + k)
                    r = await pg.evaluate(CORRI)
                    n = 6 if sei else 4
                    if r["barche"] != n: no(f"torneo {t} regata {k + 1}: {r['barche']} barche invece di {n}")
                    tot[n][0] += 1; tot[n][1] += r["contatti"]; tot[n][2] += r["presto"]; tot[n][3] += r["ferma"]
                    if r["presto"]: no(f"N2 torneo {t} ({n} barche) regata {k + 1}: {r['presto']} contatti nei primi 25 s")
                    if r["ferma"]: no(f"N3 torneo {t} ({n} barche) regata {k + 1}: regata ferma a {r['t']:.0f} s")
                if t == 0 and sei:
                    pannello(await pg.evaluate(PANNELLO), "torneo a 6 dopo 4 regate"); await pg.screenshot(path=str(QUI / "output" / "sei_barche_torneo.png"))
                    await pg.evaluate("() => document.getElementById('torRivali').click()")
                    for s in range(5):
                        await pg.evaluate("s => document.querySelectorAll('.tor-ling')[s].click()", s)
                        pannello(await pg.evaluate(PANNELLO), f"scheda {s + 1} di 5")
                    nl = await pg.evaluate("() => document.querySelectorAll('.tor-ling').length")
                    if nl != 5: no(f"N6: {nl} schede invece di 5")
                    await pg.screenshot(path=str(QUI / "output" / "sei_barche_scheda.png"))
                    await pg.evaluate("() => { document.getElementById('torIndietro').click(); document.getElementById('torMenu').click(); }")
            if (t + 1) % 5 == 0: print(f"  tornei {t + 1} fatti: {tot}", flush=True)
        for n in (4, 6):
            reg, c, presto, ferme = tot[n]
            if reg: print(f"N2/N3 {n} barche: {reg} regate, contatti {c} ({c / reg / (n * (n - 1) / 2):.3f} per coppia per regata), nei primi 25 s {presto}, regate ferme {ferme}")
        if not VELOCE and tot[4][0] and tot[6][0]:
            r4 = tot[4][1] / tot[4][0] / 6; r6 = tot[6][1] / tot[6][0] / 15
            print(f"N3: rapporto per coppia {r6 / r4 if r4 else float('inf'):.2f} (soglia 2)")
            if r4 == 0: no("N3: nessun contatto con 4 barche: il confronto non misura")
            elif r6 > 2 * r4: no(f"N3: {r6:.3f} contro {r4:.3f} per coppia")
        await ch.close()
    print("\nESITO:", "OK" if not errori else f"FALLITO ({len(errori)})")
if __name__ == "__main__": asyncio.run(main())
