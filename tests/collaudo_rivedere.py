# Lezione «da rivedere» dopo un ripasso con errori (1.3.25, voce 62; Ale 20 nov: «la scelta più semplice»). Criteri scritti prima:
#   V1 ripasso con almeno un errore → nel menu la lezione dice «Da rivedere» (gioco libero e carriera), e l'esito lo dice
#   V2 ripasso tutto giusto → niente «Da rivedere» (su una lezione che non lo era)
#   V3 rifatta la lezione fino all'ultimo passo → torna «Completata»; i punti dell'esperienza non cambiano in nessun momento
#   V4 pagina senza #collaudo, tutto a clic: ripasso sbagliato, menu con «Da rivedere»; 0 errori
# Uso: python tests/collaudo_rivedere.py   (BROWSER=firefox per Firefox)
import asyncio, os, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
BR = os.environ.get("BROWSER", "chromium")
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("OK   " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)
RISPONDI = """async giusta => { const b = document.getElementById('qzBody'); for (let k = 0; k < 60; k++){
    if (!document.getElementById('quiz').open || b.querySelector('#qzAgain')) break;
    const opts = [...b.querySelectorAll('.opt')], Q = qz.qs[qz.i], i = Q.opts.findIndex(o => o.ok === giusta);
    opts[i].click(); await new Promise(r => setTimeout(r, 30)); const av = [...b.querySelectorAll('#qzAfter button')].pop(); if (av) av.click(); await new Promise(r => setTimeout(r, 30)); }
  return b.textContent; }"""
STATO = """li => { const bt = [...document.querySelectorAll('#menu button.item[data-k]')].find(x => x.querySelector('.kind') && x.querySelector('.kind').textContent === LESSONS[li].name);
  return { st: bt ? bt.querySelector('.state').textContent : null, riv: !!(progress.rivedi && progress.rivedi['l' + li]), esp: meriti(progress).pt.esp, done: !!progress.done['l' + li] }; }"""
async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch(); errs = []
        for modo in ("libero", "carriera"):
            ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda e: errs.append(str(e)))
            await q.goto((ROOT / "index.html").as_uri() + "#collaudo")
            await q.evaluate("m => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', m); localStorage.setItem('scuolaVelaLivello', 'scuola'); }", modo); await q.reload(); await q.wait_for_timeout(300)
            await q.evaluate("() => { LESSONS.forEach((L, i) => { progress.done['l' + i] = true; }); saveProgress(); __sv.st.showMenu(); }")
            e0 = (await q.evaluate(STATO, 0))["esp"]
            await q.evaluate("() => openQuiz(0)"); fine = await q.evaluate(RISPONDI, False); await q.evaluate("() => closeQuiz()"); await q.wait_for_timeout(150)
            s = await q.evaluate(STATO, 0)
            chk("V1", s["st"] == "Da rivedere" and s["riv"] and "da rivedere" in fine and s["esp"] == e0, f"V1 {modo}: dopo un ripasso sbagliato {s}, esito dice «da rivedere» {'da rivedere' in fine}")
            await q.evaluate("() => openQuiz(1)"); await q.evaluate(RISPONDI, True); await q.evaluate("() => closeQuiz()"); await q.wait_for_timeout(150)
            s1 = await q.evaluate(STATO, 1)
            chk("V2", s1["st"] == "Completata" and not s1["riv"], f"V2 {modo}: ripasso tutto giusto {s1}")
            await q.evaluate("() => { startLesson(0); showStep(LESSONS[0].steps.length - 1); }"); await q.evaluate("() => __sv.st.showMenu()"); await q.wait_for_timeout(150)
            s = await q.evaluate(STATO, 0)
            chk("V3", s["st"] == "Completata" and not s["riv"] and s["esp"] == e0 > 0, f"V3 {modo}: lezione rifatta {s}, esperienza {e0} → {s['esp']}")
            await ctx.close()
        # V4: come un giocatore
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda e: errs.append(str(e)))
        await q.goto((ROOT / "index.html").as_uri()); await q.evaluate("() => localStorage.clear()"); await q.reload(); await q.wait_for_timeout(400)
        await q.click("#menu [data-q='0']"); await q.wait_for_timeout(200)
        for _ in range(60):
            if await q.locator("#qzAgain").count(): break
            ok = await q.evaluate("() => { const Q = qz.qs[qz.i]; return Q.opts.findIndex(o => !o.ok); }")
            await q.locator("#qzBody .opt").nth(ok).click(); await q.wait_for_timeout(40)
            av = q.locator("#qzAfter button")
            if await av.count(): await av.last.click(); await q.wait_for_timeout(40)
        await q.click("#qzClose"); await q.wait_for_timeout(250)
        st = await q.evaluate("() => [...document.querySelectorAll('#menu button.item[data-k] .state')].map(x => x.textContent)")
        sv = await q.evaluate("() => typeof window.__sv")
        chk("V4", "Da rivedere" in st and sv == "undefined", f"V4 pagina senza #collaudo: stati del menu {st[:4]}")
        await ctx.close(); await b.close()
        chk("V4", not errs, f"errori della pagina {errs[:3]}")
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("V1", "V2", "V3", "V4")): print("ESITO: NON VALIDA"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
