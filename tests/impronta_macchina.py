# Indagine del 21 novembre 2026: perché la stessa regata (stessi semi, stesso codice, stessa versione del browser) esce diversa sul PC di Ale
# (Xeon X5660, senza AVX né FMA) e sui computer di GitHub? Non è un collaudo: non boccia mai, stampa solo numeri da confrontare fra le due macchine.
#   1) la macchina (modello della CPU, se ci sono AVX2 e FMA), il browser e la sua versione;
#   2) l'impronta delle funzioni matematiche del browser (sin, cos, exp, pow, atan2…) su 2000 valori fissi: se differisce, la causa è lì;
#   3) la prima regata di un torneo lungo col pilota (seme 201), un'impronta di tutte le barche ogni 5 s di gioco per tutta la regata e i valori esatti
#      del giocatore a 10, 30 e 60 s: dove le due macchine cominciano a differire.
# Uso: python tests/impronta_macchina.py   (BROWSER=firefox per Firefox). Confrontare le uscite con diff, per esempio
#      grep -E "^(M|T|V) " uscita_pc.txt > a; grep -E "^(M|T|V) " uscita_github.txt > b; diff a b
import asyncio, os, pathlib, re
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BR = os.environ.get("BROWSER", "chromium")
MATEMATICA = """() => {
  const f64 = new Float64Array(1), u32 = new Uint32Array(f64.buffer), h = (x) => { f64[0] = x; return u32[0] ^ Math.imul(u32[1], 16777619); };
  const fn = { sin: Math.sin, cos: Math.cos, tan: Math.tan, atan2: (a) => Math.atan2(a, 1 - a / 3), exp: Math.exp, log: (a) => Math.log(a + 3), pow: (a) => Math.pow(a + 3, 1.7), sqrt: (a) => Math.sqrt(a + 3), tanh: Math.tanh, hypot: (a) => Math.hypot(a, 1 + a), atan: Math.atan, asin: (a) => Math.asin(a / 7), cbrt: Math.cbrt };
  const out = {};
  for (const k in fn){ let a = 0; for (let i = 0; i < 2000; i++) a = (Math.imul(a, 31) + h(fn[k]((i - 1000) * 0.0173))) | 0; out[k] = (a >>> 0).toString(16); }
  return out; }"""
REGATA = """() => {
  const sv = __sv, sel = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('change')); }, seme = 201;
  const semina = () => (s => { Math.random = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })(seme);
  sv.fast(0); sel('aiLevel', 'medio'); sel('cdSel', '60'); window.confirm = () => true; sv.lungo = true;
  semina(); sv.torApri(); document.getElementById('torGo').click(); sv.rot.spento = true; semina(); sv.simTime = 0; sv.openItem(["r", "t"]);
  const R = sv.R, dt = 1 / 60, out = { T: [], V: [] }, f64 = new Float64Array(1), u32 = new Uint32Array(f64.buffer);
  const h = (x) => { f64[0] = x; return u32[0] ^ Math.imul(u32[1], 16777619); };
  let n = 0, prossimo = 0; const vedi = { 10: 1, 30: 1, 60: 1 };
  const asinO = Math.asin; let aa = 0, na = 0; Math.asin = (x) => { const y = asinO(x); aa = (Math.imul(aa, 31) + h(y)) | 0; na++; return y; };
  while (R.t < 900 && R.boats.some(b => b.fin === null && !b.dnf)){
    sv.pilota(dt); sv.run(dt, 1); n++;
    if (R.t >= prossimo){ let a = 0; for (const b of R.boats){ a = (Math.imul(a, 31) + h(b.S.x)) | 0; a = (Math.imul(a, 31) + h(b.S.y)) | 0; a = (Math.imul(a, 31) + h(b.S.h)) | 0; }
      out.T.push(Math.round(R.t) + " " + (a >>> 0).toString(16) + " asin " + na + " " + (aa >>> 0).toString(16)); prossimo += 5; }
    const r = Math.round(R.t); if (vedi[r] && R.t >= r){ delete vedi[r]; const S = R.boats[0].S; out.V.push(r + " x " + S.x + " y " + S.y + " h " + S.h + " u " + S.u); }
  }
  return out; }"""
def cpu():
    try:
        t = pathlib.Path("/proc/cpuinfo").read_text(); m = re.search(r"model name\s*:\s*(.*)", t)
        return (m.group(1).strip() if m else "?") + " | avx2 " + ("sì" if " avx2" in t else "no") + " | fma " + ("sì" if " fma" in t else "no")
    except Exception as e: return "? " + str(e)
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); pg = await b.new_page(viewport={"width": 1360, "height": 650})
        await pg.goto((ROOT / "index.html").as_uri() + "#collaudo"); await pg.wait_for_timeout(400)
        print("macchina:", cpu()); print("browser:", BR, b.version, "| ua:", await pg.evaluate("navigator.userAgent"))
        for k, v in (await pg.evaluate(MATEMATICA)).items(): print("M", k, v)
        r = await pg.evaluate(REGATA)
        for x in r["T"]: print("T", x)
        for x in r["V"]: print("V", x)
        await b.close()
    print("ESITO: OK (solo numeri da confrontare)")
asyncio.run(main())
