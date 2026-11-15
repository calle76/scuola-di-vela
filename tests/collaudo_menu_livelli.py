# Menu a due livelli, «La scuola» e «Deriva» (1.3.0, docs/PROPOSTA-DERIVA-CIRCUITI.md, criteri D2 e D3 per la parte della 1.3.0).
# Pagina caricata come la carica un giocatore (senza #collaudo), nel browser di BROWSER (chromium o firefox).
#  M1 spazio: a 1360x650 e 1360x768, gioco libero e carriera, livello salvato «scuola» e «deriva», carriera vuota e con il libretto al massimo
#     (attestato, torneo aperto): pagina senza eccesso, né in altezza né in larghezza;
#  M2 al suo posto: nel gioco libero la Scuola ha le regate 0-1 e la navigazione libera, non il torneo; Deriva ha le regate 2-3 e il torneo;
#     in carriera (dalla 1.3.5) i due livelli: senza attestato Deriva è spenta e si resta nella Scuola; con l'attestato Deriva ha regate 2-3, torneo e libretto di Deriva;
#  M3 ogni voce si apre: dal menu, cliccando, ogni regata apre la sua (titolo), il torneo apre il suo riquadro, la navigazione libera parte;
#  M4 il livello scelto resta: dopo la ricarica della pagina, e tornando al menu da una regata di Deriva;
#  M5 0 errori della pagina.
# Esce con 1 se un controllo fallisce o se una parte non ha casi.
import asyncio, json, os, pathlib, sys
import metro   # controlli che cadono anche a zero casi (docs/PROPOSTA-TEST-DEI-TEST.md)
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    if not ok: fail.append(testo); print("FALLITO " + testo, flush=True)

# carriera col libretto al massimo e l'attestato (stesse chiavi di collaudo_libretto.py): il caso più alto del menu della carriera
PIENA = {"done": {**{f"l{i}": True for i in range(20)}, **{f"m{i}": True for i in range(5)}}, "best": {}, "clean": {}, "quiz": {},
         "race": {"r0.4:esperti": {"pos": 1, "n": 4, "pulita": True}, "r1.4:esperti": {"pos": 1, "n": 4, "pulita": True}},
         "exam": {"superato": True, "voto": 30, "n": 34, "ripasso": []}, "brevetto": {"data": "2026-11-15"}}

async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        errs = []
        async def pagina(H, modo, liv, salv=None):
            ctx = await b.new_context(viewport={"width": 1360, "height": H}); q = await ctx.new_page(); q.on("pageerror", lambda x: errs.append(str(x)))
            q.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
            await q.goto(BASE)
            await q.evaluate("([m, l, d]) => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', m); localStorage.setItem('scuolaVelaLivello', l); if (d) localStorage.setItem('scuolaVelaCarriera.v1', d); }",
                             [modo, liv, json.dumps(salv) if salv else None])
            await q.reload(); await q.wait_for_timeout(300); await q.evaluate("document.fonts.ready")
            return ctx, q
        stato = """() => ({ ecc: document.documentElement.scrollHeight - innerHeight, eccx: document.documentElement.scrollWidth - innerWidth,
            piede: document.querySelector('.menu-foot').getBoundingClientRect().bottom, H: innerHeight,
            sel: document.getElementById('livSel') ? document.querySelector('#livSel [aria-pressed=true]').dataset.v : null,
            r: [...document.querySelectorAll('#menu [data-r]')].map(x => +x.dataset.r), tor: !!document.getElementById('goTor'),
            free: !!document.getElementById('goFree'), lib: !!document.getElementById('libManca') })"""
        # M1, M2
        for H in (650, 768):
            for modo, salv in (("libero", None), ("carriera", None), ("carriera", PIENA)):
                for liv in ("scuola", "deriva"):
                    ctx, q = await pagina(H, modo, liv, salv); s = await q.evaluate(stato)
                    tag = f"1360x{H} {modo}{' col libretto pieno' if salv else ''}, livello salvato {liv}"
                    chk("M1", s["ecc"] <= 0 and s["eccx"] <= 0 and s["piede"] <= s["H"], f"M1 {tag}: eccesso {s['ecc']} px in altezza, {s['eccx']} in larghezza, piede a {s['piede']:.0f} su {s['H']}")
                    if modo == "libero":
                        att = ([0, 1], False, True) if liv == "scuola" else ([2, 3], True, False)
                        chk("M2", s["sel"] == liv and (s["r"], s["tor"], s["free"]) == att and not s["lib"], f"M2 {tag}: {s}")
                    else:
                        # 1.3.5: in carriera i due livelli; senza attestato si resta nella Scuola (Deriva spenta), con l'attestato il livello salvato
                        lv = liv if salv else "scuola"
                        att = ([0, 1], False, True, True) if lv == "scuola" else ([2, 3], True, False, False)
                        chk("M2", s["sel"] == lv and (s["r"], s["tor"], s["free"], s["lib"]) == att, f"M2 {tag}: {s}")
                    print(f"{tag}: eccesso {s['ecc']}/{s['eccx']} px, selettore {s['sel']}, regate {s['r']}, torneo {s['tor']}, navigazione {s['free']}", flush=True)
                    await ctx.close()
        # M3, M4: dal menu, cliccando come un giocatore
        ctx, q = await pagina(650, "libero", "scuola")
        for r in (0, 1, 2, 3):
            liv = "deriva" if r >= 2 else "scuola"
            await q.click(f"#livSel button[data-v='{liv}']"); await q.wait_for_timeout(100)
            atteso = await q.inner_text(f"#menu [data-r='{r}'] .title")
            await q.click(f"#menu [data-r='{r}']"); await q.wait_for_timeout(400)
            t = (await q.text_content("#rTitle") or "").strip()
            chk("M3", t == atteso and await q.is_visible("#game"), f"M3 regata {r}: si apre «{t}», attesa «{atteso}»")
            await q.keyboard.press("Enter"); await q.wait_for_timeout(300)
            await q.click("#toMenu"); await q.wait_for_timeout(300)
            s = await q.evaluate(stato)
            chk("M4", s["sel"] == liv, f"M4 tornando al menu dalla regata {r}: livello {s['sel']}, atteso {liv}")
        await q.click("#livSel button[data-v='deriva']"); await q.click("#goTor"); await q.wait_for_timeout(300)
        chk("M3", await q.is_visible("#torDlg"), "M3 il torneo apre il suo riquadro")
        await q.evaluate("document.getElementById('torDlg').close()")
        await q.reload(); await q.wait_for_timeout(300); s = await q.evaluate(stato)
        chk("M4", s["sel"] == "deriva" and s["r"] == [2, 3], f"M4 dopo la ricarica il livello resta Deriva: {s}")
        await q.click("#livSel button[data-v='scuola']"); await q.click("#goFree"); await q.wait_for_timeout(400)
        chk("M3", await q.is_visible("#game"), "M3 la navigazione libera parte")
        await q.reload(); await q.wait_for_timeout(300); s = await q.evaluate(stato)
        chk("M4", s["sel"] == "scuola", f"M4 dopo la ricarica il livello resta la Scuola: {s}")
        chk("M5", await q.evaluate("typeof window.__sv") == "undefined", "M5 senza #collaudo __sv non esiste")
        await ctx.close()
        chk("M5", not errs, f"M5 errori della pagina: {errs[:3]}")
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("M1", "M2", "M3", "M4", "M5")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
