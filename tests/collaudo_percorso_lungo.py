# Regate lunghe di Deriva (1.3.26, voce 63, docs/PROPOSTA-PERCORSO-LUNGO.md; criteri L1-L3 scritti prima, soglie della proposta con la durata di Ale: 9-11 minuti).
#   P1 per chi gioca (pagina senza #collaudo) un torneo nuovo è lungo: 3 regate, bolina 560 m, triangolo 460 m; con #collaudo resta corto finché non lo si accende
#   P2 un torneo lungo intero, col pilota sul giocatore: finisce dopo 3 regate, nessuno scarto in classifica, testo «con tre regate niente scarto»
#   P3 un torneo corto già cominciato (salvato senza n né lungo) resta di 4 regate corte, con lo scarto
#   P4 (L1-L3) 5 semi × bastone e triangolo: durata mediana fra 9 e 11 minuti; virate dopo il via mediana almeno 4; bolina in raffica fra 20% e 40%.
#      Durata di una raffica sulla barca (soglia della proposta 20 s: 17-26 s secondo i semi) e velocità di bolina dentro meno fuori (soglia +0,6: +0,2/+0,6) si riportano
#      e basta: soglie della proposta non raggiunte sempre, detto nel CHANGELOG 1.3.26 (20 nov). Non sono diventate soglie più basse
#   P5 testi: lezione 21 e menu dicono tre regate
# Uso: python tests/collaudo_percorso_lungo.py   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib, statistics as st, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BR = os.environ.get("BROWSER", "chromium")
MIS = (ROOT / "tests" / "misura_percorso_lungo.py").read_text().split('JS = """')[1].split('"""')[0]
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("OK   " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)
TORNEO = """async seme => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); }, dt = 1 / 60;
  (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', 'medio'); sel('cdSel', '60'); window.confirm = () => true; sv.lungo = true; sv.rot.spento = true;
  if (sv.tor){ sv.torApri(); const r = document.getElementById('torRit'); if (r) r.click(); }
  sv.torApri(); document.getElementById('torGo').click(); const T = sv.tor, ups = [];
  for (let k = 0; k < 4 && !T.fine; k++){ sv.simTime = 0; sv.openItem(["r", "t"]); const R = sv.R; ups.push([R.up, !!R.tri]);
    while (R.t < 1500 && R.boats.some(b => b.fin === null && !b.dnf) && !(R.boats[0].fin !== null && R.t > R.boats[0].fin + 400)){ sv.pilota(dt); sv.run(dt, 1); }
    sv.torEsci(); if (!T.fine){ sv.torApri(); const go = document.getElementById('torGo'); if (go) go.click(); } }
  const cl = sv.torSerie(T.ris), leg = torTabella(T, ['Tu'].concat(T.av.map(a => a.nome)));
  return { n: T.n, regate: T.ris.length, fine: !!T.fine, ups, scarti: cl.map(x => x.sc), leg };
}"""
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []
        # P1 e P5: pagina come la carica un giocatore
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda e: errs.append(str(e) + " @ " + str(getattr(e, "stack", ""))[:300]))
        await q.goto((ROOT / "index.html").as_uri()); await q.wait_for_timeout(400)
        r = await q.evaluate("() => { const T = torNuovo(); return { n: T.n, lungo: T.lungo, reg: T.regate.length, sv: typeof window.__sv, lati: [LATO_BAS, LATO_TRI] }; }")
        chk("P1", r == {"n": 3, "lungo": True, "reg": 3, "sv": "undefined", "lati": [560, 460]}, f"P1 senza #collaudo: torneo nuovo {r}")
        t = await q.evaluate("() => [LESSONS.find(L => L.steps && L.steps[0] && L.steps[0].title === 'Una serie di regate').steps[0].text[0], document.getElementById('menu').textContent]")
        chk("P5", "tre regate" in t[0] and "quattro regate" not in t[1], f"P5 lezione 21: {t[0][:70]!r}; menu senza «quattro regate» {'quattro regate' not in t[1]}")
        await ctx.close()
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda e: errs.append(str(e) + " @ " + str(getattr(e, "stack", ""))[:300]))
        await q.goto((ROOT / "index.html").as_uri() + "#collaudo"); await q.wait_for_timeout(400)
        r = await q.evaluate("() => { const T = torNuovo(); return { n: T.n, lungo: T.lungo }; }")
        chk("P1", r == {"n": 4, "lungo": False}, f"P1 con #collaudo il torneo resta corto: {r}")
        # P3: torneo corto salvato prima
        r = await q.evaluate("""() => { const T = torNuovo(); delete T.n; delete T.lungo; tor = T; const rc = torRc(); const out = { n: torN(T), up: rc.up, lungo: rc.lungo, sc: torSerie([0, 1, 2, 3].map(() => [{ fin: 1, pp: 0 }, { fin: 2, pp: 0 }])).map(x => x.sc) }; tor = null; return out; }""")
        chk("P3", r["n"] == 4 and r["up"] is None and r["lungo"] is False and all(x >= 0 for x in r["sc"]), f"P3 torneo corto già cominciato: {r}")
        # P2: torneo lungo intero
        r = await q.evaluate(TORNEO, 4242)
        print("P2:", r, flush=True)
        chk("P2", r["n"] == 3 and r["regate"] == 3 and r["fine"] and all(x == -1 for x in r["scarti"]) and "niente scarto" in r["leg"] and [u for u, _ in r["ups"]] == [560, 460, 560],
            f"P2 torneo lungo: {r['regate']} regate, finito {r['fine']}, scarti {r['scarti']}, lati {r['ups']}")
        # P4: L1-L3
        R = []; await q.evaluate("() => { tor = null; delete progress.torneo; }")   # dopo P2: il torneo finito non deve restare in mezzo
        for seme in range(201, 206):
            for k in (0, 1): R.append(await q.evaluate(MIS, [k, seme, True, None]))
        for nome, tri in (("bastone", False), ("triangolo", True)):
            X = [x for x in R if x["tri"] == tri and x["fin"]]; d = [v for x in X for v in x["dur"]]
            dur = st.median(x["fin"] for x in X) / 60; vir = st.median(x["vir"] for x in X); raf = sum(x["nr"] for x in X) / max(1, sum(x["nb"] for x in X)); dr = st.median(d) if d else 0
            dv = [x["vin"] - x["vout"] for x in X if x["vin"] and x["vout"]]
            chk("P4", len(X) == 5 and 9 <= dur <= 11 and vir >= 4 and 0.2 <= raf <= 0.4,
                f"P4 {nome}: {len(X)} regate, durata mediana {dur:.1f} min, virate {vir}, bolina in raffica {100 * raf:.0f}%, raffica sulla barca {dr} s (solo riportata); velocità dentro meno fuori {st.median(dv) if dv else 0:+.2f} nodi (solo riportata)")
        await ctx.close(); await b.close()
        chk("P1", not errs, f"errori della pagina {errs[:3]}")
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("P1", "P2", "P3", "P4", "P5")): print("ESITO: NON VALIDA"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
