# Lezione 2, «Tenere la rotta»: a mani ferme il passo non deve completarsi mai; correggendo con piccoli colpi di barra deve completarsi.
# A passi fissi con __sv.run, perché il risultato non dipenda dal carico del computer (vedi COLLAUDI.md).
# Uso: python collaudo_rotta.py [tentativi a mani ferme] [tentativi con correzioni]
import asyncio, sys
from playwright.async_api import async_playwright
import pathlib
# percorsi relativi al repository: il gioco è ../index.html, le immagini vanno in tests/output/
BASE = (pathlib.Path(__file__).resolve().parent.parent / "index.html").as_uri()
OUT = pathlib.Path(__file__).resolve().parent / "output"; OUT.mkdir(exist_ok=True)
URL = BASE + "#collaudo"
FERMI = int(sys.argv[1]) if len(sys.argv) > 1 else 25
CORREZIONI = int(sys.argv[2]) if len(sys.argv) > 2 else 6
# prue di ingresso: il traverso con cui si apre la lezione e le andature larghe con cui si arriva dal passo precedente
PRUE = [90, 112, 120, 130, 140, 150]

# apre il passo «Tenere la rotta» con la prua indicata; la rotta da tenere viene fissata su quella prua
APRI = """(h) => {
  __sv.openItem(['l', 1]); __sv.showStep(4);
  __sv.S.h = h; __sv.S.u = 2.3; __sv.S.r = 0; __sv.S.vl = 0;
  __sv.showStep(5); __sv.ctl.tiller = 0;
}"""

FERMO = """(secs) => {            // mani ferme: solo onde e orziera
  const n = Math.round(secs * 60); let tenuta = 0, massimo = 0;
  for (let k = 0; k < n; k++){
    __sv.run(1/60, 1);
    const off = Math.abs(((__sv.S.h - __sv.S.course + 540) % 360) - 180);
    tenuta = (off < 6 && __sv.readI().kn > 2) ? tenuta + 1/60 : 0;
    massimo = Math.max(massimo, tenuta);
    if (__sv.stepDone) break;
  }
  return [__sv.stepDone, Math.round(massimo * 10) / 10];
}"""

PILOTA = """(secs) => {           // come una persona: piccoli colpi di barra, e non insiste se la prua sta già rientrando
  const n = Math.round(secs * 60);
  for (let k = 0; k < n; k++){
    const off = ((__sv.S.h - __sv.S.course + 540) % 360) - 180;   // >0: prua troppo a dritta
    if (k % 12 < 8){                                              // colpo di 8 fotogrammi, poi la barra si ricentra
      if (off > 2 && __sv.S.r > -3) __sv.ctl.tiller = 0.3;
      else if (off < -2 && __sv.S.r < 3) __sv.ctl.tiller = -0.3;
    }
    __sv.run(1/60, 1);
    if (__sv.stepDone) return [true, Math.round(k / 60 * 10) / 10];
  }
  return [false, secs];
}"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1280,"height":800})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(300)
        # a mani ferme: l'orziera di 3°/s deve vincere sulle spinte delle onde (3-6°/s per 0,8 s)
        fermi = 0; tenute = []
        for i in range(FERMI):
            h = PRUE[i % len(PRUE)]
            await pg.evaluate(APRI, h)
            done, tenuta = await pg.evaluate(FERMO, 30)
            fermi += 1 if done else 0; tenute.append(tenuta)
        print(f"senza correzioni: completati {fermi} su {FERMI} (atteso 0); secondi in rotta di fila, massimo {max(tenute)} su 8 richiesti")
        # con correzioni
        tempi = []
        for i in range(CORREZIONI):
            await pg.evaluate(APRI, PRUE[i % len(PRUE)])
            done, t = await pg.evaluate(PILOTA, 60)
            tempi.append(t if done else None)
        riusciti = [t for t in tempi if t is not None]
        print(f"con correzioni: completati {len(riusciti)} su {CORREZIONI}; tempi {tempi}" +
              (f"; mediana {sorted(riusciti)[len(riusciti)//2]} s" if riusciti else ""))
        print("suggerimento:", await pg.inner_text("#hint"))
        await pg.screenshot(path=str(OUT / "course.png"))
        print("errori:", errs)
        await b.close()
asyncio.run(main())
