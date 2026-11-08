# Collaudo dell'orologio dei giri di penalità (1.2.17, docs/PROPOSTA-OROLOGIO-GIRI.md). Soglie scritte nella proposta prima di implementare.
# Uso: .venv-collaudi/bin/python tests/collaudo_orologio_giri.py        (BROWSER=firefox per l'altro browser)
#  O1 l'orologio c'è se e solo se c'è un debito di giri (anche prima del via), letto da __sv.riquadro; O2 pixel dell'anello: rosso prima del giro, verde dove il giro è arrivato,
#  nel verso giusto (ore 3 e ore 6 per i giri a dritta, ore 9 e ore 6 per quelli a sinistra); O3 il numero al centro = giri contati dal collaudo / giri della penalità;
#  O5 il riquadro sta nella metà alta dello schermo (bussola e vento sono in basso a destra); O7 pagina senza #collaudo: dopo un debito l'anello si vede, rosso.
import asyncio, os, pathlib, sys
import metro
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
# colore di un punto del disegno: «rosso», «verde» o «altro» (rosso #D9443C, verde #7FD6A8)
PIX = """const colore = (x, y) => { const c = document.querySelector('canvas'), k = c.width / W, d = c.getContext('2d').getImageData(Math.round(x * k), Math.round(y * k), 1, 1).data;
  return d[0] > d[1] + 60 ? 'rosso' : d[1] > d[0] + 40 && d[1] > 150 ? 'verde' : 'altro'; };
const punti = () => { const o = R.rqOr; if (!o) return null; const [x, y, r] = o; return { su: colore(x, y - r), ore3: colore(x + r, y), ore6: colore(x, y + r), ore9: colore(x - r, y) }; };"""
GIRI = PIX + """
async ([dir, seme, prima]) => {
  const sv = __sv, dt = 1 / 60; const lv = document.getElementById('aiLevel'); lv.value = 'nessuno'; lv.dispatchEvent(new Event('change')); __seed(seme); sv.simTime = 0; sv.fast(0); sv.openItem(["r", 3]);
  const R = sv.R, out = []; let k = 0, cap = false, inc = 0, dp = 0;
  const camp = (fase) => { if (k++ % 15) return; sv.draw(0.016); const d = sv.riquadro, o = d && d.orologio;
    if (R.done > dp){ inc += R.done - dp; dp = R.done; }
    out.push({ t: +R.t.toFixed(2), fase, deb: R.need > R.done, oro: !!o, frac: o ? o.frac : null, verso: o ? o.verso : null, testo: o ? o.testo : null, atteso: inc + "/" + (R.need - R.base), pix: o ? punti() : null, rect: sv.rqRect2 }); };
  if (prima){ while (R.t < -60){ sv.pilota(dt); sv.run(dt, 1); camp('senza'); } giriDebito(); dp = R.done; for (let j = 0; j < 60 * 5; j++){ sv.pilota(dt); sv.run(dt, 1); camp('prima del via'); } return { out, cap }; }
  while (R.t < 25){ sv.pilota(dt); sv.run(dt, 1); camp('senza'); }
  giriDebito(); dp = R.done; const t0 = R.t;
  while (R.t < t0 + 90 && R.done < R.need && !cap){ sv.ctl.tiller = dir; sv.ctl.sheet = sv.autoSheet(); sv.run(dt, 1); if (sv.S.capsized) cap = true; camp('giri'); }
  for (let j = 0; j < 60 * 5; j++){ sv.pilota(dt); sv.run(dt, 1); camp('dopo'); }
  return { out, cap, done: R.done, need: R.need };
}"""
bad = []
def chk(nome, ok, extra=""):
    print(("OK   " if ok else "FALLITO ") + nome + (" " + extra if extra else ""), flush=True)
    if not ok: bad.append(nome)
async def main():
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); await ctx.add_init_script(SEME)
        pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(250)
        G = [await pg.evaluate(GIRI, [1 if k % 2 else -1, 3000 + k, False]) for k in range(1, 11)]
        P = [await pg.evaluate(GIRI, [1, 3100 + k, True]) for k in range(1, 4)]
        tutti = [s for r in G + P for s in r["out"]]
        chk("O1 l'orologio c'è se e solo se c'è un debito di giri (%d letture in 13 prove, di cui %d con debito, %d prima del via con debito)" % (len(tutti), sum(s["deb"] for s in tutti), sum(1 for r in P for s in r["out"] if s["deb"])),
            sum(s["deb"] for s in tutti) > 100 and sum(1 for r in P for s in r["out"] if s["deb"]) > 10 and metro.tutti(s["oro"] == s["deb"] for s in tutti))
        conPix = [s for s in tutti if s["oro"] and s["pix"]]
        def atteso(s):   # quali punti devono essere verdi; None = punto troppo vicino al bordo dell'arco per giudicare
            f, v = s["frac"], s["verso"]; e = {"su": None}
            if v == 0 or f == 0: return {"ore3": "rosso", "ore6": "rosso", "ore9": "rosso"}
            lato = "ore3" if v > 0 else "ore9"; altro = "ore9" if v > 0 else "ore3"
            e[lato] = "verde" if f >= 0.30 else "rosso" if f <= 0.20 else None
            e["ore6"] = "verde" if f >= 0.55 else "rosso" if f <= 0.45 else None
            e[altro] = "verde" if f >= 0.80 else "rosso" if f <= 0.70 else None
            return e
        giudicati = [(s, k, c) for s in conPix for k, c in atteso(s).items() if c is not None]
        giusti = [x for x in giudicati if x[0]["pix"][x[1]] == x[2]]
        verdi = sum(1 for x in giudicati if x[2] == "verde"); dx = sum(1 for x in giudicati if x[2] == "verde" and x[0]["verso"] > 0); sx = sum(1 for x in giudicati if x[2] == "verde" and x[0]["verso"] < 0)
        chk("O2 pixel dell'anello: rosso dove il giro non è arrivato, verde dove è arrivato, nel verso giusto (%d punti giudicati, %d verdi: %d a dritta, %d a sinistra)" % (len(giudicati), verdi, dx, sx),
            len(giudicati) > 200 and dx > 20 and sx > 20 and metro.tutti(x[0]["pix"][x[1]] == x[2] for x in giudicati), "giusti %d su %d; primi sbagliati: %s" % (len(giusti), len(giudicati), [(x[0]["t"], x[1], x[2], x[0]["pix"][x[1]], round(x[0]["frac"], 2)) for x in giudicati if x not in giusti][:4]))
        oro = [s for s in tutti if s["oro"]]
        chk("O3 il numero al centro è giri contati dal collaudo / giri della penalità (%d letture; testi visti %s)" % (len(oro), sorted({s["testo"] for s in oro})),
            len(oro) > 100 and {"0/2", "1/2"} <= {s["testo"] for s in oro} and metro.tutti(s["testo"] == s["atteso"] for s in oro))
        scontate = sum(1 for r in G if not r["cap"] and r["done"] >= r["need"])
        chk("O3b le penalità si scontano come prima (giri contati dal gioco: 2 su 2) in tutte le prove senza scuffia", scontate >= 8 and metro.tutti(r["done"] >= r["need"] for r in G if not r["cap"]), "scontate %d su 10" % scontate)
        basso = max((s["rect"][1] + s["rect"][3]) for s in tutti if s["rect"])
        chk("O5 il riquadro con l'orologio sta nella metà alta dello schermo (parte più bassa a y=%d, metà = 325)" % basso, basso < 325)
        chk("O0 nessun errore di pagina", not errs, str(errs[:2]))
        await ctx.close()
        # ---- O7: pagina come la carica un giocatore ----
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri()); await pg.wait_for_timeout(500)
        await pg.click("#menu [data-r='3']"); await pg.wait_for_timeout(300); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(1500)
        await pg.evaluate("() => giriDebito()"); await pg.wait_for_timeout(800)
        r = await pg.evaluate("() => { " + PIX + " return { sv: typeof window.__sv, or: R.rqOr, pix: punti() }; }")
        chk("O7 pagina senza #collaudo: dopo un debito l'anello si vede, rosso (e __sv non esiste)", r["sv"] == "undefined" and r["or"] is not None and r["pix"] and all(r["pix"][k] == "rosso" for k in ("ore3", "ore6", "ore9")), str(r))
        chk("O8 nessun errore di pagina senza #collaudo", not errs, str(errs[:2]))
        await b.close()
    print("\ncasi sbagliati:", "nessuno" if not bad else bad)
    sys.exit(1 if bad else 0)
asyncio.run(main())
