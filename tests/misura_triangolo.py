# Misura del triangolo del torneo (T2, 1.0.55, docs/PROPOSTA-TORNEI-1B.md §8): corre la regata 2 del torneo (triangolo) col pilota sostitutivo
# a seme fisso, con il lato L dato, e scrive durata, arrivi e giri sbagliati. Per C8 (durata del pilota), C9 e T2g (giri sbagliati) senza la finestra d'arrivo.
# Condizione: seme % 3 = 0 vento costante, 1 raffiche, 2 salti di vento; direzione del vento (seme % 8) * 45°; avversari principianti.
# Uso: python tests/misura_triangolo.py L seme_da seme_a [file di uscita]
import asyncio, json, pathlib, statistics, sys
from playwright.async_api import async_playwright

BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
SEME = """(() => { let s = 1; Math.random = () => { s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  window.__seed = v => { s = v; }; })();"""
CORSA = """([seme, L]) => {
  const sv = __sv, dt = 1 / 60; sv.triL = L; sv.fast(0); __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = "principianti"; sel.dispatchEvent(new Event("change"));
  sv.torApri(); document.getElementById("torGo").click();            // regata 1 (bastone): serve solo a creare il torneo
  sv.tor.ris.push(sv.tor.ris.length ? [] : [{ fin: 1, pp: 0 }, { fin: 2, pp: 0 }, { fin: 3, pp: 0 }, { fin: 4, pp: 0 }]);
  sv.tor.regate[1] = { c: seme % 3, wind: (seme % 8) * 45 };
  __seed(seme); sv.simTime = 0; sv.openItem(["r", "t"]);              // regata 2: il triangolo
  const R = sv.R; R.tor = false;                                       // senza finestra d'arrivo (C9 si misura fuori dalla finestra)
  if (!R.tri) return { errore: "non è un triangolo" };
  while (R.t < 1500 && R.boats.some(b => b.fin === null)){ sv.pilota(dt); sv.run(dt, 1); }
  return { seme, L, t: Math.round(R.t), marks: R.marks.length, boats: R.boats.map(b => ({ n: b.name, fin: b.fin === null ? null : b.fin - b.pen, pen: b.pen, wm: b.wrongMarks || 0, leg: b.leg, ocs: !!b.ocs })) };
}"""

async def main(L, a, b, uscita):
    righe = []; errori = []
    async with async_playwright() as p:
        br = await getattr(p, __import__("os").environ.get("BROWSER", "chromium")).launch()
        for seme in range(a, b + 1):
            ctx = await br.new_context(viewport={"width": 1280, "height": 800}); await ctx.add_init_script(SEME)
            pg = await ctx.new_page(); pg.on("pageerror", lambda e: errori.append(str(e)))
            pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(200)
            righe.append(await pg.evaluate(CORSA, [seme, L])); await ctx.close()
        await br.close()
    if uscita: pathlib.Path(uscita).write_text("\n".join(json.dumps(r) for r in righe) + "\n")
    ok = [r for r in righe if "boats" in r]
    me = [r["boats"][0]["fin"] for r in ok if r["boats"][0]["fin"] is not None]
    barche = [x for r in ok for x in r["boats"]]; arr = [x for x in barche if x["fin"] is not None]
    wm = sum(x["wm"] for x in barche); giusti = 2 * len(arr)
    print(f"L {L} semi {a}-{b}: regate {len(ok)}, pilota arrivato {len(me)}, durata mediana {statistics.median(me) / 60:.2f} min (min {min(me) / 60:.2f}, max {max(me) / 60:.2f})" if me else "nessun arrivo",
          f"| barche {len(barche)}, arrivate {len(arr)} ({100 * len(arr) / max(1, len(barche)):.1f}%), giri sbagliati {wm} su {giusti + wm} passaggi ({100 * wm / max(1, giusti + wm):.1f}%)",
          f"| tutte e 4 arrivate in {sum(all(x['fin'] is not None for x in r['boats']) for r in ok)} regate | errori {errori[:2]} | non triangolo {len(righe) - len(ok)}")
asyncio.run(main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else None))
