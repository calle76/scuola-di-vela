# Misura (non collaudo, 17 nov 2026, osservazione 134): quante rotte ottimali (la tua dal taglio, quella in assoluto, quelle delle altre barche) attraversano la
# semiretta della boa nel verso sbagliato almeno una volta (come roundCheck di js/gioco.js: per il gioco «sbagliato poi giusto» vale 0 = boa non girata).
# Uso: python tests/misura_lato_boa.py PRIMO_SEME ULTIMO_SEME VENTO[,VENTO...]   (SALVA=file.json per salvare le uscite; torneo, principianti, 10 e 12 nodi)
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
JS = """([seme, wind, tws]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', 'principianti'); sel('cdSel', '60'); window.confirm = () => true;
  if (sv.tor){ sv.torApri(); document.getElementById('torRit').click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; T.regate[0] = { tws, wind };
  sv.rot.spento = false; semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60; R.tor = false;
  while (R.t < 900 && R.boats.some(b => b.fin === null && !b.dnf)){ sv.pilota(dt); sv.run(dt, 1); }
  const lato = (punti, mk) => { let sba = 0, giu = 0, pa; for (const p of punti){ const d = Math.hypot(p.x - mk.x, p.y - mk.y); if (d < 1.5) continue;
      const a = sv.norm180(Math.atan2(p.x - mk.x, -(p.y - mk.y)) * 180 / Math.PI - mk.out);
      if (Math.abs(a) < 0.05) continue;
      if (pa !== undefined && Math.abs(a) <= 90 && Math.abs(pa) <= 90 && (pa > 0) !== (a > 0)){ if (pa < 0) sba++; else giu++; } pa = a; } return [giu, sba]; };
  const out = { fin0: R.boats[0].fin, marks: R.marks.length };
  const o = sv.rotCalcola(0); out.mia = o ? R.marks.map(mk => lato(o.punti, mk)) : null;
  const a = sv.rotAssoluta(); out.ass = a ? R.marks.map(mk => lato(a.punti, mk)) : null;
  // anche le altre barche: la rotta ottimale di ognuna dal suo taglio
  out.altre = R.boats.slice(1).map((b, i) => { const q = sv.rotCalcola(i + 1); return q ? R.marks.map(mk => lato(q.punti, mk)) : null; });
  return out;
}"""
async def main(A, B, winds):
    res = []
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={"width": 1360, "height": 650})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        for w in winds:
            for tws in (10, 12):
                for seme in range(A, B + 1):
                    r = await pg.evaluate(JS, [seme, w, tws]); r.update(w=w, tws=tws, seme=seme); res.append(r)
        await br.close()
    tot = {"mia": [0, 0, 0], "ass": [0, 0, 0], "altre": [0, 0, 0]}
    brutti = []
    for r in res:
        for k in ("mia", "ass"):
            v = r[k]
            if v is None: tot[k][2] += 1
            elif all(x[1] == 0 for x in v): tot[k][0] += 1
            else: tot[k][1] += 1; brutti.append((k, r["w"], r["tws"], r["seme"], v))
        for v in r["altre"]:
            if v is None: tot["altre"][2] += 1
            elif all(x[1] == 0 for x in v): tot["altre"][0] += 1
            else: tot["altre"][1] += 1; brutti.append(("altra", r["w"], r["tws"], r["seme"], v))
    print(len(res), "regate; errori pagina", errs[:2]); print("(senza attraversamento sbagliato, con, non calcolata)", tot); print(brutti[:12])
    if os.environ.get("SALVA"): pathlib.Path(os.environ["SALVA"]).write_text(json.dumps(res))
asyncio.run(main(int(sys.argv[1]), int(sys.argv[2]), [int(x) for x in sys.argv[3].split(",")]))
