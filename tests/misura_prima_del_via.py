# Misura dei contatti prima del via (7 novembre 2026, base per la proposta sui contatti al via; V2 di PROPOSTA-AVVERSARI-DERIVA). Non è un collaudo: nessuna soglia.
# Ogni corsa si ferma allo sparo. La barca del giocatore: «pilota» (la guida degli avversari) oppure «lontano» (ferma a 600 m: restano i soli avversari).
# Per ogni contatto, dal passo prima: secondi al via, chi, regola, e per le due barche velocità, se è partita (goStart), se dichiara di cedere, e se è in attesa (sotto 1 m/s).
# Uso: python tests/misura_prima_del_via.py PRIMO_SEME ULTIMO_SEME [regate, es. 0,1,2]     BROWSER=firefox per l'altro browser
import asyncio, collections, json, os, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent)
CORSA = """([race, seme, liv, cd, modo]) => {
  const sv = __sv; sv.fast(0); sv.openItem(["r", race]);
  const c = document.getElementById("cdSel"); c.value = String(cd); c.dispatchEvent(new Event("change"));
  __seed(seme); sv.simTime = 0;
  const sel = document.getElementById("aiLevel"); sel.value = liv; sel.dispatchEvent(new Event("change"));
  const R = sv.R, dt = 1 / 60, me = R.boats[0], t0 = R.t;
  const foto = b => ({ nome: b.me ? "Tu" : b.name, u: b.S.u, part: !!b.goStart, cede: b.cedeA ? (b.cedeA.me ? "Tu" : b.cedeA.name) : null, x: b.S.x, y: b.S.y });
  const qx = me.S.x + 600, qy = me.S.y + 600, out = []; let n = 0, prima = R.boats.map(foto), dMin = {};
  while (R.t < 0){
    prima = R.boats.map(foto);
    if (modo === "lontano") Object.assign(me.S, { x: qx, y: qy, u: 0 }); else sv.pilota(dt);
    sv.run(dt, 1);
    while (n < R.penList.length){ const txt = R.penList[n++], m = txt.match(/^(Tu|La (\\w+)), contatto con (te|la (\\w+))/); if (!m) continue;
      const g = m[1] === "Tu" ? "Tu" : m[2], a = m[3] === "te" ? "Tu" : m[4], G = prima.find(p => p.nome === g), A = prima.find(p => p.nome === a);
      const st = p => p.part ? "partita" : p.u < 1 ? "attesa" : "avvicinamento";
      out.push({ t: +R.t.toFixed(1), colpa: g, altra: a, regola: +(txt.match(/regola ([\\d.]+)/) || [0, 0])[1], stati: [st(G), st(A)].sort().join("+"), cedeva: G.cede === a, altraCedeva: A.cede === g, uG: +G.u.toFixed(2), uA: +A.u.toFixed(2) }); }
  }
  return { t0, contatti: out }; }"""
async def main():
    a, z = int(sys.argv[1]), int(sys.argv[2]); reg = [int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "0,1,2").split(",")]
    SEME = (pathlib.Path(__file__).resolve().parent / "esplora.py").read_text().split('SEME = """')[1].split('"""')[0]
    righe, errs = [], []
    async with async_playwright() as p:
        br = await getattr(p, os.environ.get("BROWSER", "chromium")).launch()
        for cd in (60, 180):
            for modo in ("pilota", "lontano"):
                for race in reg:
                    for liv in ("principianti", "esperti"):
                        for seme in range(a, z + 1):
                            pg = await br.new_page(); pg.on("pageerror", lambda e: errs.append(str(e))); await pg.add_init_script(SEME)
                            await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(150)
                            r = await pg.evaluate(CORSA, [race, seme, liv, cd, modo]); await pg.close()
                            r.update(cd=cd, modo=modo, race=race, liv=liv, seme=seme); righe.append(r); print(json.dumps(r, ensure_ascii=False), flush=True)
        await br.close()
    print("errori della pagina:", errs[:2])
    for cd in (60, 180):
        for modo in ("pilota", "lontano"):
            rr = [r for r in righe if r["cd"] == cd and r["modo"] == modo]; C = [c for r in rr for c in r["contatti"]]
            t_ok = sorted(set(r["t0"] for r in rr))
            print(f"\n== preparazione {cd} s, {modo}: regate {len(rr)} (partenza del conto a {t_ok}), contatti {len(C)}, a regata {len(C) / max(len(rr), 1):.2f}; regate con almeno uno: {sum(bool(r['contatti']) for r in rr)}")
            print("  col giocatore:", sum("Tu" in (c["colpa"], c["altra"]) for c in C), "| colpa del giocatore:", sum(c["colpa"] == "Tu" for c in C))
            print("  regole:", dict(sorted(collections.Counter(c["regola"] for c in C).items())))
            print("  stati:", collections.Counter(c["stati"] for c in C).most_common())
            print("  fasce di 15 s dal via:", sorted(collections.Counter(int(-c["t"] // 15) * 15 for c in C).items()))
            print("  chi ha colpa dichiarava di cedere:", sum(c["cedeva"] for c in C), "| l'altra dichiarava di cedere:", sum(c["altraCedeva"] for c in C), "| nessuna delle due:", sum(not c["cedeva"] and not c["altraCedeva"] for c in C))
asyncio.run(main())
