# Prova 6 di Deriva, «I giri di penalità» (1.3.2, docs/PROPOSTA-DERIVA-CIRCUITI.md D9; medaglie in collaudo_medaglie.py --prove 6).
# Passi fissi di 1/60 s, pagina con #collaudo e Math.random a seme fisso, una pagina per corsa; il pilota è quello preciso di collaudo_medaglie.py.
#   P1 col pilota che fa i giri subito (barra tutta da una parte) e poi il percorso: completata 10 su 10, giri fatti 2 su 2, nessun secondo aggiunto
#   P2 a mani ferme: completata 0 su 10 (in 900 s)
#   P3 il pilota che non fa i giri: completata 10 su 10, ogni giro non fatto costa 15 s (tempo = tempo vero arrotondato + 30), senza stella, e la riga di fine prova lo dice;
#      con un giro solo fatto: + 15 s
#   P4 la prova non entra nei meriti della Scuola (meriti uguali con e senza un tempo d'oro salvato nella prova 6); sta nel menu di Deriva, non in quello della Scuola
#   P5 pagina senza #collaudo: dal menu di Deriva la prova si apre, la riga dei giri c'è, il pannello a 1360x650 non scorre; 0 errori
# Uso: python collaudo_prova_giri.py [--semi 1-10]   (browser con BROWSER=firefox)
import asyncio, os, pathlib, sys, types
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent
src = (ROOT / "collaudo_medaglie.py").read_text().replace("asyncio.run(main())", "")
M = types.ModuleType("medaglie"); M.__file__ = str(ROOT / "collaudo_medaglie.py"); sys.path.insert(0, str(ROOT)); exec(compile(src, M.__file__, "exec"), M.__dict__)
BASE = (ROOT.parent / "index.html").as_uri()
IDX = 5
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)

# una corsa: seme, apertura e guida nella stessa chiamata (come collaudo_medaglie.py); «giri»: quanti giri fa il pilota prima del percorso (None = mani ferme)
CORSA = """([plan, E, seme, idx, vento, giri]) => { __seed(seme); __sv.openItem(['m', idx]); __sv.startMission(idx, vento);
  const sv = __sv;
  if (giri === null){ sv.fast(0); for (let n = 0; n < 60 * 900 && !sv.S.finished; n++){ sv.ctl.tiller = 0; sv.run(1 / 60, 1); } }
  else {
    if (giri < 2){ sv.fast(0); const fine = () => sv.mg.done >= giri; for (let n = 0; n < 60 * 120 && !fine(); n++){ sv.ctl.tiller = 1; sv.ctl.sheet = sv.autoSheet(); sv.run(1 / 60, 1); } E = { ...E, senzaGiri: true }; }
    (""" + M.CORSA.strip() + """)([plan, E]);
  }
  return { fin: !!sv.S.finished, t: sv.S.time, fatti: sv.mg.done, dovuti: sv.mg.need, best: progress.best['m' + idx] ?? null, stella: !!progress.clean['m' + idx],
           testo: document.getElementById('doneText').textContent, riga: document.getElementById('mGiri').textContent };
}"""

async def corsa(b, seme, giri):
    pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    await pg.add_init_script(M.SEME); await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(200)
    await pg.evaluate("() => localStorage.clear()")
    r = await pg.evaluate(CORSA, [M.PIANI[IDX], M.PRECISO, seme, IDX, ((seme - 1) * 45) % 360, giri])
    await pg.close(); r["errs"] = errs
    return r

async def main():
    a = sys.argv[1:]
    x, y = (a[a.index("--semi") + 1] if "--semi" in a else "1-10").split("-"); semi = range(int(x), int(y) + 1); n = len(semi)
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch(); errori = []
        G = [await corsa(b, s, 2) for s in semi]
        for r in G: errori += r["errs"]
        print("P1 col pilota:", [(round(r["t"], 1), r["fatti"], r["best"]) for r in G])
        chk("P1", sum(r["fin"] and r["fatti"] == 2 for r in G) == n and all(r["best"] == round(r["t"]) for r in G),
            f"P1 completata con i giri fatti {sum(r['fin'] and r['fatti'] == 2 for r in G)} su {n}, tempo salvato = tempo vero in {sum(r['best'] == round(r['t']) for r in G)}")
        F = [await corsa(b, s, None) for s in semi]
        chk("P2", sum(r["fin"] for r in F) == 0 and len(F) == n, f"P2 a mani ferme completata {sum(r['fin'] for r in F)} su {n}")
        Z = [await corsa(b, s, 0) for s in semi]
        print("P3 senza giri:", [(round(r["t"], 1), r["fatti"], r["best"]) for r in Z])
        chk("P3", len(Z) == n and all(r["fin"] and r["fatti"] == 0 and r["best"] == round(r["t"]) + 30 and not r["stella"] and "Giri non fatti: 2, 30 s" in r["testo"] for r in Z),
            f"P3 senza giri: +30 s in {sum(r['best'] == round(r['t']) + 30 for r in Z)} su {n}, stella in {sum(r['stella'] for r in Z)}; «{Z[0]['testo']}»")
        U = [await corsa(b, s, 1) for s in list(semi)[:3]]
        chk("P3", all(r["fin"] and r["fatti"] == 1 and r["best"] == round(r["t"]) + 15 and "Giri non fatti: 1, 15 s" in r["testo"] for r in U),
            f"P3 un giro solo: {[(round(r['t'], 1), r['fatti'], r['best']) for r in U]}")
        for r in F + Z + U: errori += r["errs"]

        # P4 meriti e menu
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errori.append(str(e)))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(200)
        m = await pg.evaluate("""() => { const p = { done: { l0: true }, best: { m0: 70 }, clean: {} }, q = JSON.parse(JSON.stringify(p)); q.done.m5 = true; q.best.m5 = MISSIONS[5].bands[0]; q.clean.m5 = true;
            const a = meriti(p), b = meriti(q); return [JSON.stringify([a.pt, a.totale, a.sugg]) === JSON.stringify([b.pt, b.totale, b.sugg]), a.pt.abil, MISSIONS[5].bands]; }""")
        chk("P4", m[0] and m[2][0] < 999, f"P4 meriti uguali con e senza l'oro nella prova 6: {m[0]} (abilità {m[1]}); bande {m[2]}")
        menu = await pg.evaluate("""() => { localStorage.setItem('scuolaVelaLivello', 'scuola'); showMenu(); const s = [...document.querySelectorAll('#menu .item .title')].map(t => t.textContent);
            document.querySelector('#livSel [data-v=deriva]').click(); const d = [...document.querySelectorAll('#menu button.item[data-d]')].map(b => b.dataset.d + ' ' + b.querySelector('.kind').textContent + ' ' + b.querySelector('.title').textContent);
            return [s.includes(MISSIONS[5].title), d]; }""")
        chk("P4", not menu[0] and menu[1][-1] == "m5 Prova 6 I giri di penalità", f"P4 nel menu della Scuola: {menu[0]}; nel menu di Deriva: {menu[1]}")
        await pg.close()

        # P5 pagina senza #collaudo
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); pg.on("pageerror", lambda e: errori.append(str(e)))
        await pg.goto(BASE); await pg.evaluate("() => { localStorage.clear(); localStorage.setItem('scuolaVelaLivello', 'deriva'); }"); await pg.reload(); await pg.wait_for_timeout(300)
        await pg.click("#menu button.item[data-d='m5']"); await pg.wait_for_timeout(400)
        await pg.click("#bGo"); await pg.wait_for_timeout(1500)
        r = await pg.evaluate("""() => { const p = document.querySelector('.panel'); return { dove: document.getElementById('where').textContent, riga: document.getElementById('mGiri').textContent,
            vis: !document.getElementById('mGiri').hidden, ecc: p ? p.scrollHeight - p.clientHeight : null, pag: document.documentElement.scrollHeight - innerHeight }; }""")
        chk("P5", "Prova 6" in r["dove"] and r["vis"] and "Giri da fare: 2" in r["riga"] and r["ecc"] == 0 and r["pag"] <= 0, f"P5 senza #collaudo: {r}")
        chk("P5", await pg.evaluate("typeof window.__sv") == "undefined", "P5 senza #collaudo __sv non esiste")
        await pg.close()
        chk("P5", not errori, f"P5 errori della pagina: {errori[:3]}")
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("P1", "P2", "P3", "P4", "P5")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
