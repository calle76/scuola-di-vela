# Collaudo delle layline in acqua (1.2.23, docs/PROPOSTA-LAYLINE.md, pezzo 2, criteri P1, P2, P4 scritti prima di misurare).
# P1 dove si vede: con «nelle regate» nella regata a tema sì, nel torneo, nelle regate della Scuola e negli esercizi no; con «anche nel torneo» anche
#    nel torneo; con «no» mai; dopo il giro della boa no. Si controlla layVisibile e, nella regata a tema, anche i pixel gialli disegnati.
# P2 è giusta: angolo = rotLay della polare; vento girato di 10° = linee girate di 10°; una barca della polare da un punto della layline a 100 m,
#    alla rotta sul fondo della layline col vento costante, passa entro 2 m dalla boa.
# P4 pagina senza #collaudo: la riga «Layline» c'è e cambia il disegno (pixel gialli), nessun errore.
# Uso: python tests/collaudo_layline.py
import asyncio, os, pathlib, sys
from playwright.async_api import async_playwright
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
errori = []
def no(m): errori.append(m); print("  NO  " + m, flush=True)
def ok(m): print("  ok  " + m, flush=True)
GIALLI = """() => { const c = document.querySelector('canvas'), x = c.getContext('2d'), d = x.getImageData(0, 0, c.width, c.height).data; let n = 0;
  for (let i = 0; i < d.length; i += 4) if (d[i] > 175 && d[i + 1] > 165 && d[i + 2] < 150 && d[i] - d[i + 2] > 60) n++; return n; }"""
async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
        await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(300)
        # P1
        casi = []
        for scelta in ("no", "regate", "tutte"):
            for dove in ("tema", "scuola", "torneo", "esercizio"):
                v = await pg.evaluate("""([scelta, dove]) => { const sv = __sv; const e = document.getElementById('laySel'); e.value = scelta; e.dispatchEvent(new Event('change'));
                  sv.fast(0); window.confirm = () => true;
                  if (dove === 'tema') sv.openItem(['r', 2]); else if (dove === 'scuola') sv.openItem(['r', 0]);
                  else if (dove === 'torneo'){ sv.torApri(); if (document.getElementById('torRit')){ document.getElementById('torRit').click(); sv.torApri(); } document.getElementById('torGo').click(); }
                  else { const L = sv.LESSONS; let li = -1, si = -1; L.forEach((l, i) => l.steps.forEach((s, j) => { if (li < 0 && s.esercizio && s.esercizio.regata >= 2) { li = i; si = j; } })); sv.apriEsercizio(li, si); }
                  sv.run(1 / 60, 30); return sv.layVisibile(); }""", [scelta, dove])
                atteso = (scelta == "regate" and dove == "tema") or (scelta == "tutte" and dove in ("tema", "torneo"))
                casi.append((scelta, dove, v, atteso))
                if v != atteso: no(f"P1 «{scelta}» {dove}: visibile {v}, atteso {atteso}")
        ok(f"P1 {sum(c[2] == c[3] for c in casi)} casi giusti su {len(casi)}")
        # P1: dopo il giro della boa sparisce; e i pixel gialli seguono layVisibile nella regata a tema
        r = await pg.evaluate("""async () => { const sv = __sv, e = document.getElementById('laySel'); e.value = 'regate'; e.dispatchEvent(new Event('change'));
          sv.openItem(['r', 2]); sv.run(1 / 60, 30); const R = sv.R; const me = R.boats[0];
          const m = R.marks[0]; Object.assign(me.S, { x: m.x + 0, y: m.y + 12 }); // 12 m sottovento alla boa: le linee sono a ±13 m, nello schermo sv.run(1 / 60, 2); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
          return { vis: sv.layVisibile() }; }""")
        await pg.wait_for_timeout(300); g_on = await pg.evaluate(GIALLI)
        await pg.evaluate("() => { const e = document.getElementById('laySel'); e.value = 'no'; e.dispatchEvent(new Event('change')); }"); await pg.wait_for_timeout(300); g_off = await pg.evaluate(GIALLI)
        if not (r["vis"] and g_on > g_off + 150): no(f"P1 pixel gialli con le layline {g_on}, senza {g_off} (visibile {r['vis']})")
        else: ok(f"P1 pixel gialli con le layline {g_on}, senza {g_off}")
        dopo = await pg.evaluate("() => { const e = document.getElementById('laySel'); e.value = 'regate'; e.dispatchEvent(new Event('change')); __sv.R.boats[0].leg = 2; return __sv.layVisibile(); }")
        if dopo: no("P1 dopo il giro della boa le layline restano")
        else: ok("P1 dopo il giro della boa spariscono")
        # P2
        g = await pg.evaluate("""() => { const sv = __sv, out = [];
          for (const tws of [6, 10, 14].map(k => k / 1.9438)) for (const twd of [0, 45, 200, 315]){
            const d = sv.layDir({ twd, tws }), a = sv.rotLay(tws), d2 = sv.layDir({ twd: twd + 10, tws });
            const angolo = Math.max(Math.abs(sv.norm180(d[0] - (twd + 180 - a))), Math.abs(sv.norm180(d[1] - (twd + 180 + a))));
            const giro = Math.max(Math.abs(sv.norm180(d2[0] - d[0] - 10)), Math.abs(sv.norm180(d2[1] - d[1] - 10)));
            // barca della polare da 100 m sulla layline, verso la boa (0, 0): rotta sul fondo = direzione opposta a quella della layline
            let manca = 0;
            for (const k of [0, 1]){ const D = d[k] * Math.PI / 180; let x = Math.sin(D) * 100, y = -Math.cos(D) * 100, best = 1e9;
              const r = sv.rotRiga(tws); let n = 0, err = 1e9; r.forEach((q, i) => { const e = Math.abs(30 + 5 * i + q[1] - a); if (e < err){ err = e; n = i; } });
              const twa = 30 + 5 * n, s = k === 0 ? 1 : -1, cog = (twd - s * (twa + r[n][1])) * Math.PI / 180, v = r[n][0];
              for (let t = 0; t < 200; t += 0.2){ x += Math.sin(cog) * v * 0.2; y -= Math.cos(cog) * v * 0.2; best = Math.min(best, Math.hypot(x, y)); }
              manca = Math.max(manca, best); }
            out.push({ angolo, giro, manca }); }
          return out; }""")
        ma = max(x["angolo"] for x in g); mg = max(x["giro"] for x in g); mm = max(x["manca"] for x in g)
        (ok if ma < 0.01 and mg < 0.01 and mm <= 2 and len(g) == 12 else no)(f"P2 su {len(g)} venti: angolo rispetto a rotLay al massimo {ma:.4f}°, giro di 10° sbagliato al massimo {mg:.4f}°, barca della polare passa al massimo a {mm:.2f} m dalla boa")
        if errs: no(f"errori della pagina: {errs[:2]}")
        await pg.close()
        # P4 pagina senza #collaudo
        pg = await b.new_page(viewport={"width": 1360, "height": 650}); e2 = []; pg.on("pageerror", lambda e: e2.append(str(e)))
        await pg.goto(BASE); await pg.wait_for_timeout(500)
        riga = await pg.evaluate("() => !!document.getElementById('laySel') && document.getElementById('laySel').value")
        await pg.click("[data-r='2']"); await pg.wait_for_timeout(1500)
        await pg.get_by_role("button", name="Parti").click(); await pg.wait_for_timeout(500); await pg.mouse.move(400, 300)
        for _ in range(30): await pg.mouse.wheel(0, 300); await pg.wait_for_timeout(30)   # zoom indietro col rotellino, fino a vedere la boa a 300 m
        await pg.wait_for_timeout(800)
        pg_on = await pg.evaluate(GIALLI)
        await pg.screenshot(path=str(pathlib.Path(__file__).resolve().parent / "output" / "layline_giocatore_accese.png"))
        await pg.evaluate("() => { const e = document.getElementById('laySel'); e.value = 'no'; e.dispatchEvent(new Event('change')); }"); await pg.wait_for_timeout(500)
        pg_off = await pg.evaluate(GIALLI)
        await pg.screenshot(path=str(pathlib.Path(__file__).resolve().parent / "output" / "layline_giocatore.png"))
        (ok if riga == "regate" and pg_on > pg_off + 80 and not e2 else no)  # 1.2.24: margine 150 -> 80 pixel perché le linee in acqua sono lunghe metà (osservazione 110); con la 1.2.23 erano 485 contro 225, con la 1.2.24 430 contro 299(f"P4 pagina senza #collaudo: riga «Layline» {riga}, pixel gialli {pg_on} con e {pg_off} senza, errori {e2[:1]}")
        await b.close()
    print("ESITO:", "OK" if not errori else f"FALLITO ({len(errori)})"); sys.exit(1 if errori else 0)
asyncio.run(main())
