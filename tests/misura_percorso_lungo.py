# Misura della voce 63 (docs/PROPOSTA-PERCORSO-LUNGO.md, criteri L1-L3 scritti prima): regate del torneo col pilota sul giocatore (__sv.pilota) e rivali,
# con le regate lunghe accese o spente (__sv.lungo, __sv.lati). Per regata: tempo all'arrivo del giocatore dal via, virate dopo il via, tempo di bolina in raffica
# (vento sulla barca almeno 2 nodi sopra quello impostato), durata delle raffiche sulla barca (tratti di fila), velocità di bolina dentro e fuori, rivali non arrivati.
# Uso: python tests/misura_percorso_lungo.py PRIMO ULTIMO [lungo 0|1] [BAS,TRI]   (SALVA=file.json; un campione al secondo di gioco)
import asyncio, json, os, pathlib, statistics as st, sys
from playwright.async_api import async_playwright
URL = (pathlib.Path(os.environ.get("RADICE") or pathlib.Path(__file__).resolve().parent.parent) / "index.html").as_uri() + "#collaudo"
A, B = int(sys.argv[1]), int(sys.argv[2]); LUNGO = len(sys.argv) > 3 and sys.argv[3] == "1"
LATI = [int(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else None
JS = """([k, seme, lungo, lati]) => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); };
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', 'medio'); sel('cdSel', '60'); window.confirm = () => true; sv.lungo = lungo; if (lati) sv.lati = lati;
  if (sv.tor){ sv.torApri(); const rit = document.getElementById('torRit'); if (rit) rit.click(); }
  semina(); sv.torApri(); document.getElementById('torGo').click();
  const T = sv.tor; T.ris.length = 0; for (let j = 0; j < k; j++) T.ris.push(T.av.concat([0]).map((x, i) => ({ fin: i + 1, pp: 0 })));
  sv.rot.spento = true; semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, S = sv.S, dt = 1 / 60, KN = 1.9438; R.tor = false; // senza finestra d'arrivo: si misura fino all'ultimo
  let acc = 0, lato = 0, vir = 0, nb = 0, nr = 0, cur = 0, fermi = 0, acc2 = 0; const dur = [], vin = [], vout = [];
  while (R.t < 1500 && R.boats.some(b => b.fin === null && !b.dnf)){
    sv.pilota(dt); sv.run(dt, 1);
    if (R.t > 10 && (acc2 += dt) >= 1){ acc2 = 0; for (const b of R.boats) if (!b.me && b.fin === null && !b.dnf && b.S.u * KN < 0.5) fermi++; }
    if (R.t < 0 || R.boats[0].fin !== null || (acc += dt) < 1) continue; acc = 0;
    const w = sv.windAt(S.x, S.y), rel = sv.norm180(w.twd - S.h), twa = Math.abs(rel);
    if (twa < 80){ const l = Math.sign(rel); if (lato && l && l !== lato) vir++; if (l) lato = l; }
    if (twa >= 30 && twa <= 60 && R.boats[0].leg >= 1){
      nb++; const raf = (w.tws - sv.envTws()) * KN >= 2;
      if (raf){ nr++; cur++; vin.push(S.u * KN); } else { if (cur) dur.push(cur); cur = 0; vout.push(S.u * KN); } }
  }
  if (cur) dur.push(cur);
  const med = a => a.length ? a.slice().sort((x, y) => x - y)[Math.floor(a.length / 2)] : null;
  return { k, tri: !!R.tri, up: R.up, fin: R.boats[0].fin, fine: R.t, vir, nb, nr, dur, vin: med(vin), vout: med(vout), nonArr: R.boats.filter(b => b.fin === null).length, pen: (R.penList || []).filter(x => !/scontata/.test(x)).length, fermi, durata: R.t };
}"""
async def main():
    res = []
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={"width": 1360, "height": 650})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        for seme in range(A, B + 1):
            for k in (0, 1):
                r = await pg.evaluate(JS, [k, seme, LUNGO, LATI]); r["seme"] = seme; res.append(r)
                print(f"seme {seme} {'triangolo' if r['tri'] else 'bastone'} lato {r['up']} m: arrivo {r['fin'] and round(r['fin'])} s, virate {r['vir']}, bolina in raffica {r['nr']}/{r['nb']} s, raffiche {r['dur']}, v dentro {r['vin'] and round(r['vin'], 2)} fuori {r['vout'] and round(r['vout'], 2)}, non arrivati {r['nonArr']}", flush=True)
        await br.close()
    for nome, t in (("bastone", False), ("triangolo", True)):
        R = [r for r in res if r["tri"] == t and r["fin"]]
        if not R: continue
        d = [x for r in R for x in r["dur"]]; dv = [r["vin"] - r["vout"] for r in R if r["vin"] and r["vout"]]
        print(f"\n{nome}: {len(R)} regate; arrivo mediana {st.median(r['fin'] for r in R) / 60:.1f} min (da {min(r['fin'] for r in R) / 60:.1f} a {max(r['fin'] for r in R) / 60:.1f}); "
              f"virate dopo il via mediana {st.median(r['vir'] for r in R)}; bolina in raffica {100 * sum(r['nr'] for r in R) / max(1, sum(r['nb'] for r in R)):.0f}%; "
              f"durata di una raffica sulla barca mediana {st.median(d) if d else 0} s ({len(d)} raffiche); velocità di bolina dentro meno fuori mediana {st.median(dv) if dv else 0:+.2f} nodi ({len(dv)} regate); "
              f"regate con barche non arrivate {sum(1 for r in R if r['nonArr'])}; penalità per 10 minuti {600 * sum(r['pen'] for r in R) / sum(r['durata'] for r in R):.2f}; secondi di rivali fermi per minuto {60 * sum(r['fermi'] for r in R) / sum(r['durata'] for r in R):.2f}")
    print("errori della pagina", errs[:2])
    if os.environ.get("SALVA"): pathlib.Path(os.environ["SALVA"]).write_text(json.dumps(res))
asyncio.run(main())
