# Misura della voce 73, passo A (22 nov 2026, docs/PROPOSTA-BARCA-73.md §3): quanto spesso, nei tornei lunghi col pilota, un rivale si trova
# dove la scotta «con lasca» cambierebbe qualcosa. Non è un collaudo: nessuna soglia. Per ogni rivale, dal via al suo arrivo (o all'arrivo del pilota):
#   s12: secondi con sbandamento oltre 12° (solo lì la regola con lasca è diversa da quella di oggi), s12b: gli stessi solo di bolina (|twa| < 75°);
#   s16: secondi con vento locale oltre 16 nodi; vmax: vento locale massimo; scuffie; blocchi: virate seguite da almeno 5 s sotto 1 nodo nei 20 s dopo.
# Uso: python tests/misura_rivali_vento_forte.py PRIMO_SEME ULTIMO_SEME   (tornei lunghi, __sv.lungo = true; BROWSER=firefox per Firefox)
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
src = (pathlib.Path(__file__).resolve().parent / "collaudo_torneo.py").read_text()
SEME = src.split('SEME = """')[1].split('"""')[0]
CORRI = """() => {
  const sv = __sv, dt = 1 / 60, KN = 1.943844; document.getElementById("torGo").click();
  const R = sv.R, me = R.boats[0], av = R.boats.filter(b => !b.me), n180 = a => ((a + 540) % 360) - 180;
  const q = av.map(b => ({ nome: b.name, s12: 0, s12b: 0, s16: 0, vmax: 0, scuffie: 0, blocchi: 0, virate: 0, cap: false, tk: 0, dopo: -1, lento: 0, contato: false, tempo: 0 }));
  while (me.fin === null && !me.dnf && R.t < 1500){ sv.pilota(dt); sv.run(dt, 1);
    if (R.t < 0) continue;
    av.forEach((b, i) => { const s = b.S, x = q[i]; if (b.fin !== null || b.dnf) return;
      if (s.capsized){ if (!x.cap) x.scuffie++; x.cap = true; return; } x.cap = false; x.tempo += dt;
      const w = sv.windAt(s.x, s.y), kn = w.tws * KN, twa = n180(w.twd - s.h), tk = Math.sign(twa);
      x.vmax = Math.max(x.vmax, kn); if (kn > 16) x.s16 += dt;
      if (Math.abs(s.heel) > 12){ x.s12 += dt; if (Math.abs(twa) < 75) x.s12b += dt; }
      if (x.tk && tk && tk !== x.tk && Math.abs(twa) < 90){ x.virate++; x.dopo = 20; x.lento = 0; x.contato = false; }
      if (tk) x.tk = tk;
      if (x.dopo > 0){ x.dopo -= dt; if (s.u * KN < 1) x.lento += dt; else x.lento = 0; if (x.lento >= 5 && !x.contato){ x.blocchi++; x.contato = true; } } });
  }
  const out = { t: Math.round(R.t), vento: +(sv.envTws() * KN).toFixed(1), raffiche: sv.gustLevel(), salti: sv.salti(), q: q.map(x => { delete x.cap; delete x.tk; delete x.dopo; delete x.lento; delete x.contato;
    for (const k of ["s12", "s12b", "s16", "vmax", "tempo"]) x[k] = +x[k].toFixed(1); return x; }) };
  document.getElementById("rTor").click(); return out;
}"""
async def main():
    s0, s1 = int(sys.argv[1]), int(sys.argv[2]); tutte = []
    async with async_playwright() as p:
        b = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for seme in range(s0, s1 + 1):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); pg = await ctx.new_page(); await pg.add_init_script(SEME)
            pg.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await pg.goto(BASE + "#collaudo"); await pg.wait_for_timeout(150)
            await pg.evaluate("s => { __sv.lungo = true; __sv.fast(0); __seed(s); __sv.store = 'scuolaVelaSim.v1'; __sv.torApri(); }", seme)
            for k in range(3):
                r = await pg.evaluate(CORRI); r["seme"] = seme; r["regata"] = k + 1; tutte.append(r)
                print(json.dumps(r, ensure_ascii=False), flush=True)
            await ctx.close()
        await b.close()
    Q = [x for r in tutte for x in r["q"]]; T = sum(x["tempo"] for x in Q) or 1
    print(f"\n== riepilogo: {len(tutte)} regate, {len(Q)} rivali-regata, {T/60:.0f} minuti di regata dei rivali")
    print(f"sbandati oltre 12°: {sum(x['s12'] for x in Q):.0f} s ({100*sum(x['s12'] for x in Q)/T:.2f}%), di bolina {sum(x['s12b'] for x in Q):.0f} s; rivali-regata con almeno 1 s: {sum(1 for x in Q if x['s12'] >= 1)}")
    print(f"vento locale oltre 16 nodi: {sum(x['s16'] for x in Q):.0f} s ({100*sum(x['s16'] for x in Q)/T:.2f}%); massimo {max(x['vmax'] for x in Q):.1f} nodi")
    print(f"scuffie: {sum(x['scuffie'] for x in Q)}; virate: {sum(x['virate'] for x in Q)}; virate bloccate (5 s sotto 1 nodo): {sum(x['blocchi'] for x in Q)}")
asyncio.run(main())
