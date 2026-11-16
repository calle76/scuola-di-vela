# Varianti del Coach misurate senza toccare il gioco (16 novembre 2026, per docs/PROPOSTA-COACH-2.md).
# Corre le regate di misura_pilota_giocatore.py e, a regata finita, ricalcola le frasi del Coach con una coaClou di prova messa nella pagina:
#   aff0  come oggi: una finestra è «affollata» se per almeno un secondo c'è una barca entro 3 lunghezze o un cono
#   affV  i primi VIA secondi dopo il taglio della linea non contano come affollati
#   affS  la finestra è affollata solo se i secondi affollati sono almeno SEC su 60
#   affVS tutte e due
# e la frase «hai virato N volte vicino alla boa» da 3 virate in su (peso almeno COA_MIN) o da 2.
#   .venv-collaudi/bin/python tests/misura_coach_varianti.py --pilota vecchio|nuovo [--semi 2601-2605] [--via 15] [--sec 10]
# Strumento di misura, non collaudo del giro.
import asyncio, json, pathlib, re, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
PIL = arg("--pilota", "vecchio"); A, B = (int(x) for x in arg("--semi", "2601-2605").split("-")); VIA = float(arg("--via", "15")); SEC = int(arg("--sec", "10"))
src = (ROOT / "tests" / "misura_pilota_giocatore.py").read_text(encoding="utf-8"); CORSA = re.search(r'CORSA = """(.*?)"""', src, re.S).group(1)
PILOTA_JS = (ROOT / "tests" / "pilota_giocatore.js").read_text(encoding="utf-8")

# coaClou di prova: la stessa del gioco (js/rotta.js), con due numeri in più: via (secondi dopo il taglio che non contano) e sec (secondi affollati minimi nella finestra)
VARIANTI = """([via, sec]) => {
  const vera = coaClou;
  const prova = (viaS, secMin) => function(P, tu, lati){
    const me0 = rot.barche[0], M = R.marks.slice(me0.taglio.leg - 1).map(m => [m.x, m.y]).concat([[(R.pin.x + R.cb.x) / 2, (R.pin.y + R.cb.y) / 2]]);
    const dopo = M.map((m, k) => M.slice(k).reduce((a, q, n, A) => a + (n ? Math.hypot(q[0] - A[n - 1][0], q[1] - A[n - 1][1]) : 0), 0));
    const resto = (x, y, k) => k >= M.length ? 0 : Math.hypot(x - M[k][0], y - M[k][1]) + dopo[k];
    const latoDi = (t, fine) => { let k = 0; while (k < fine.length && t >= fine[k]) k++; return k; };
    const tuFine = me0.giri.map(g => g.t), g = [], fine = Math.min(P[P.length - 1].t, tu[tu.length - 1].t);
    for (let s = P[0].t; s <= fine; s += 1){ const q = rotIstante(P, s, q => [q.x, q.y]), f = rotIstante(tu, s, f => f.b[0]);
      if (q && f) g.push({ s, d: resto(f[0], f[1], latoDi(s, tuFine)) - resto(q[0], q[1], latoDi(s, lati)) }); }
    const aff = new Set();
    for (const f of tu){ const me = f.b[0]; if (f.t < me0.taglio.t + viaS) continue;
      if ((f.c && f.c[0] >= COA_COP) || f.b.some((b, k) => k && Math.hypot(b[0] - me[0], b[1] - me[1]) < COA_AFF)) aff.add(Math.floor(f.t)); }
    const vel = (t0, t1) => { const fr = tu.filter(f => f.t >= t0 && f.t <= t1); return fr.length ? fr.reduce((a, f) => a + f.b[0][4], 0) / fr.length : 1; };
    let best = null, tutto = null;
    for (let i = 0; i + COA_FIN < g.length; i++){
      const a = g[i], b = g[i + COA_FIN], w = { t0: a.s, t1: b.s, m: b.d - a.d };
      let n = 0; for (let s = Math.floor(a.s); s <= b.s; s++) if (aff.has(s)) n++;
      w.libero = n < secMin;
      if (!tutto || w.m > tutto.m) tutto = w;
      if (w.libero && (!best || w.m > best.m)) best = w;
    }
    for (const w of [best, tutto]) if (w) w.peso = w.m / Math.max(0.5, vel(w.t0, w.t1));
    return { best, tutto, g };
  };
  const r = rot.res, out = {}, corta = F => F.map(x => ({ tipo: x.tipo, peso: Math.round(x.peso * 10) / 10, t: x.t, n: x.n }));
  const conf = { aff0: [0, 1], affV: [via, 1], affS: [0, sec], affVS: [via, sec] };
  try { for (const k in conf){ coaClou = prova(conf[k][0], conf[k][1]); const F = coaFrasi(r.ott, r.sp); out[k] = { F: corta(F), umore: coaUmore(F) }; } }
  finally { coaClou = vera; }
  const F0 = coaFrasi(r.ott, r.sp); out.oggi = { F: corta(F0), umore: coaUmore(F0) };
  const L0 = r.sp.lati[0]; out.lay = L0 && L0.lay ? { oltre: L0.lay.oltre, vicine: L0.lay.vicine } : null; out.min = COA_MIN; out.tvir = T_VIR; out.n = COA_N;
  return out; }"""

def con_boa(F, lay, da, cmin, tvir, nmax, umore):   # la frase delle virate da «da» virate in su, col peso almeno cmin: rifà i primi nmax e l'umore
    if not lay or lay["oltre"] or lay["vicine"] < da or any(x["tipo"] == "boa" for x in F): return F, umore
    G = sorted([x for x in F if x["tipo"] != "bene"] + [{"tipo": "boa", "peso": max(cmin, (lay["vicine"] - 1) * tvir), "n": lay["vicine"]}], key=lambda x: -x["peso"])[:nmax]
    um = "arrabbiato" if any(x["tipo"] in ("penalita", "scuffia") for x in G) or umore == "arrabbiato" else "contento" if all(x["peso"] < 10 for x in G) else "serio"
    return G, um

async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={"width": 1360, "height": 650}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(500)
        if PIL == "nuovo": await pg.evaluate(PILOTA_JS, {})
        R = []
        for s in range(A, B + 1):
            for k in range(4):
                c = await pg.evaluate(CORSA, [k, s])
                await pg.evaluate("() => { if (riv.on) rivChiudi(); rotApri(); }"); await pg.wait_for_timeout(120)
                v = await pg.evaluate(VARIANTI, [VIA, SEC]); await pg.evaluate("() => { if (riv.on) rivChiudi(); }")
                v["seme"], v["k"], v["pos"] = s, k, c["pos"]; R.append(v); print(json.dumps(v, ensure_ascii=False), flush=True)
        n = len(R)
        print(f"\nRIEPILOGO pilota {PIL}, {n} regate, semi {A}-{B}; via = {VIA:.0f} s, sec = {SEC}")
        uguali = sum(1 for r in R if r["oggi"] == r["aff0"])
        print(f"riscontro: la coaClou di prova coi numeri di oggi dà le stesse frasi del gioco in {uguali} regate su {n}")
        def riga(nome, FF):
            tipi = [[x["tipo"] for x in F] for F, _ in FF]; um = [u for _, u in FF]
            print(f"{nome:34s} affollato {sum('affollato' in t for t in tipi):2d} | clou {sum('clou' in t for t in tipi):2d} | boa {sum('boa' in t for t in tipi):2d} | partenza {sum('partenza' in t for t in tipi):2d} | "
                  f"bene {sum('bene' in t for t in tipi):2d} | frasi in media {sum(len(t) for t in tipi) / n:.2f} | contento {um.count('contento'):2d}, serio {um.count('serio'):2d}, arrabbiato {um.count('arrabbiato'):2d}")
        for k, nome in (("aff0", "oggi"), ("affV", f"senza i primi {VIA:.0f} s dopo il via"), ("affS", f"almeno {SEC} s affollati su 60"), ("affVS", "tutte e due")):
            riga(nome, [(r[k]["F"], r[k]["umore"]) for r in R])
            for da in (3, 2):
                riga(f"  + virate alla boa da {da}", [con_boa(r[k]["F"], r["lay"], da, r["min"], r["tvir"], r["n"], r[k]["umore"]) for r in R])
        print("errori della pagina:", errs[:3]); await br.close()
asyncio.run(main())
