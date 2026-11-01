# Collaudo di «Cambia vento» nelle regate (1.0.75, Ale 1 nov 2026): c'è nel pannello e nella schermata finale di ogni regata,
# non c'è mai nel torneo; un clic cambia il vento e ricomincia la regata. Esce con 1 se qualcosa non va.
# Uso: .venv-collaudi/bin/python tests/collaudo_cambia_vento.py   (BROWSER=firefox per Firefox)
import asyncio, os, sys, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(500)
        n = await pg.evaluate("() => { const r = []; for (let i = 0; i < 30; i++){ try { __sv.openItem(['r', i]); } catch(e){ break; } const R = __sv.R; if (!R) break; r.push(i); } return r.length; }")
        righe = []
        for i in range(n):
            r = await pg.evaluate("""i => { __sv.openItem(['r', i]); const R = __sv.R, w0 = __sv.envTws ? null : null;
                const h = id => document.getElementById(id).hidden;
                const tw0 = __sv.R ? __sv.R : null;
                return { i, tor: !!R.tor, rWind: h('rWind'), rRow: h('rRow'), titolo: document.getElementById('rTitle').textContent }; }""", i)
            righe.append(r)
        torneo = await pg.evaluate("() => { __sv.torApri(); document.getElementById('torGo').click(); const h = id => document.getElementById(id).hidden; return { tor: !!__sv.R.tor, rWind: h('rWind'), titolo: document.getElementById('rTitle').textContent }; }")
        # clic su Cambia vento in una regata: il vento cambia e la regata ricomincia
        cambio = await pg.evaluate("""() => { __sv.openItem(['r', 3]); const prima = __sv.R.boats[0] && document.getElementById('rTitle').textContent;
            const tw = () => (typeof env !== 'undefined' ? env.twd : null); const a = tw(); const R0 = __sv.R; document.getElementById('rWind').click(); return { prima: a, dopo: tw(), nuova: __sv.R !== R0 }; }""")
        # schermata finale: si fa finire la regata e si guarda finWind
        fine = await pg.evaluate("""async () => { const h = id => document.getElementById(id).hidden; const out = {};
            for (const [nome, apri] of [['regata', () => __sv.openItem(['r', 3])], ['torneo', () => { __sv.torApri(); document.getElementById('torGo').click(); }]]){
              apri(); const R = __sv.R, me = R.boats[0]; R.t = Math.max(R.t, 1); for (const b of R.boats){ b.fin = 100; } me.fin = 100;
              for (let k = 0; k < 120 && h('finOv'); k++){ __sv.run(1/60, 1); await new Promise(r => setTimeout(r, 5)); }
              out[nome] = { finOv: !h('finOv'), finWind: !h('finWind'), finRestart: !h('finRestart') };
              document.getElementById('finOv').hidden = true; }
            return out; }""")
        print("regate:", n)
        for r in righe: print("  ", r)
        print("torneo:", torneo); print("clic su Cambia vento:", cambio); print("schermata finale:", fine); print("errori:", errs)
        ok = all(r["rWind"] == r["tor"] for r in righe) and len(righe) >= 4 and cambio["nuova"] and cambio["dopo"] != cambio["prima"] and torneo["tor"] and torneo["rWind"] and fine["regata"]["finOv"] and fine["regata"]["finWind"] and fine["torneo"]["finOv"] and not fine["torneo"]["finWind"] and not errs
        print("ESITO:", "OK" if ok else "FALLITO"); await b.close(); sys.exit(0 if ok else 1)
asyncio.run(main())
