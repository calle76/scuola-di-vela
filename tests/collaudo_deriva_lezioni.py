# Lezioni di Deriva 21-23 (1.3.1, docs/PROPOSTA-DERIVA-CIRCUITI.md, criteri D3, D4 e D8; gli esercizi, D5, li guida collaudo_esercizi_regata.py, E22 ed E23).
#  D4 la Scuola resta com'è: esame di 34 domande con 28 per passare; nessuna domanda d'esame dalle lezioni di Deriva; «di 25 completate» nel menu della Scuola;
#     i meriti della carriera identici con e senza le lezioni e i ripassi di Deriva fatti (stesso salvataggio, 6 salvataggi diversi);
#  D8 niente doppioni: nessuna domanda dei ripassi di Deriva uguale a una della Scuola (ripassi ed esame); nessun termine del glossario ripetuto; le voci nuove ci sono;
#  D3 al suo posto: dal menu di Deriva (pagina senza #collaudo) ogni lezione si apre, ogni ripasso apre il suo quiz «Ripasso 21-23»; dall'ultimo passo «Prosegui» porta
#     alla lezione dopo di Deriva, dalla 23 si va alla prova 6 (1.3.2); 0 errori.
# Esce con 1 se un controllo fallisce o se una parte non ha casi.
import asyncio, json, os, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").as_uri()
BR = os.environ.get("BROWSER", "chromium")
fail, casi = [], {}
def chk(parte, ok, testo):
    casi[parte] = casi.get(parte, 0) + 1
    print(("ok      " if ok else "FALLITO ") + testo, flush=True)
    if not ok: fail.append(testo)

SCUOLA = """() => {
  const D = LESSONS.map((L, i) => i).filter(i => LESSONS[i].livello === "deriva");
  const testo = q => q[0].trim().toLowerCase();
  const scuola = new Set(); LESSONS.forEach((L, i) => { if (L.livello) return; (quizDi(i) || []).forEach(q => scuola.add(testo(q))); bancaEsame(i).forEach(q => scuola.add(q[1].trim().toLowerCase())); });
  const deriva = D.flatMap(i => quizDi(i).map(testo));
  const termini = GLOSS.map(g => g[0].toLowerCase());
  return { D, nomi: D.map(i => LESSONS[i].name + " · " + LESSONS[i].title), domande: domandeEsame(), soglia: sogliaEsame(), esameDa: lezioniEsame().filter(i => D.includes(i)).length,
    nDeriva: deriva.length, doppie: deriva.filter(t => scuola.has(t)), dentro: deriva.length - new Set(deriva).size, nScuola: scuola.size,
    termini: termini.length, ripetuti: termini.filter((t, k) => termini.indexOf(t) !== k), nuove: GLOSS.filter(g => D.some(i => LESSONS[i].name === g[2])).map(g => g[0]) };
}"""
MERITI = """(D) => {
  const salv = [{ done: {}, best: {}, clean: {} },
    { done: { l0: true, l1: true, l2: true }, best: {}, clean: {}, quiz: { q0: 4, q1: 3 } },
    { done: Object.fromEntries(LESSONS.map((L, i) => ["l" + i, true])), best: {}, clean: {}, quiz: Object.fromEntries(LESSONS.map((L, i) => ["q" + i, quizDi(i).length])) },
    { done: { l5: true }, best: {}, clean: {}, quiz: { q5: 1 }, race: { "r0.4:esperti": { pos: 1, n: 4, pulita: true } } },
    { done: Object.fromEntries([0, 1, 2, 3, 4].map(i => ["l" + i, true])), best: {}, clean: {}, quiz: { q2: 2, q3: 4 }, exam: { superato: true, voto: 30, n: 34, ripasso: [] } },
    { done: Object.fromEntries(LESSONS.map((L, i) => ["l" + i, i % 2 === 0])), best: {}, clean: {}, quiz: Object.fromEntries(LESSONS.map((L, i) => ["q" + i, i % 3])) }];
  return salv.map(p => {
    const senza = JSON.parse(JSON.stringify(p)); D.forEach(i => { delete senza.done["l" + i]; if (senza.quiz) delete senza.quiz["q" + i]; });
    const con = JSON.parse(JSON.stringify(senza)); D.forEach(i => { con.done["l" + i] = true; con.quiz = con.quiz || {}; con.quiz["q" + i] = quizDi(i).length; });
    const a = meriti(senza), b = meriti(con);
    return [JSON.stringify([a.pt, a.totale, a.superato, a.manca, a.sugg]) === JSON.stringify([b.pt, b.totale, b.superato, b.manca, b.sugg]), a.totale];
  });
}"""

async def main():
    async with async_playwright() as p:
        b = await getattr(p, BR).launch()
        errs = []
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda x: errs.append(str(x)))
        await q.goto(BASE + "#collaudo"); await q.wait_for_timeout(300)
        s = await q.evaluate(SCUOLA)
        print("lezioni di Deriva:", s["nomi"])
        chk("D4", len(s["D"]) == 4 and [n.split(" · ")[0] for n in s["nomi"]] == ["Lezione 21", "Lezione 22", "Lezione 23", "Lezione 24"], f"D4 quattro lezioni di Deriva, 21-24 (la 24 dalla 1.3.10): {s['nomi']}")
        chk("D4", s["domande"] == 34 and s["soglia"] == 28 and s["esameDa"] == 0, f"D4 esame: {s['domande']} domande, ne servono {s['soglia']}; lezioni di Deriva nell'esame {s['esameDa']}")
        chk("D8", s["nDeriva"] >= 12 and not s["doppie"] and not s["dentro"], f"D8 {s['nDeriva']} domande dei ripassi di Deriva confrontate con {s['nScuola']} della Scuola: uguali {s['doppie']}, ripetute fra loro {s['dentro']}")
        chk("D8", not s["ripetuti"] and len(s["nuove"]) >= 3, f"D8 glossario: {s['termini']} termini, ripetuti {s['ripetuti']}; voci delle lezioni di Deriva {s['nuove']}")
        m = await q.evaluate(MERITI, s["D"])
        chk("D4", len(m) == 6 and all(x[0] for x in m) and len({x[1] for x in m}) >= 3, f"D4 meriti uguali con e senza le lezioni e i ripassi di Deriva: {m}")
        await ctx.close()

        # D3 e D4 (menu): pagina come la carica un giocatore
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda x: errs.append(str(x)))
        await q.goto(BASE); await q.evaluate("() => { localStorage.clear(); localStorage.setItem('scuolaVelaLivello', 'scuola'); }"); await q.reload(); await q.wait_for_timeout(300)
        head = await q.inner_text(".tile .part-head")
        chk("D4", "di 25 completate" in head, f"D4 menu della Scuola: «{' '.join(head.split())}»")
        await q.click("#livSel button[data-v='deriva']")
        chk("D3", await q.locator("#menu button.item[data-d^='l']").count() == 4 and await q.locator("#menu [data-q]").count() == 4, "D3 nel menu di Deriva quattro lezioni e quattro ripassi")
        for k, li in enumerate(s["D"]):
            await q.click(f"#menu button.item[data-d='l{li}']"); await q.wait_for_timeout(200)
            nvis = await q.evaluate("() => !document.getElementById('game').hidden")
            chk("D3", nvis and f"{21 + k}" in (await q.inner_text("#where")), f"D3 la lezione {21 + k} si apre: «{(await q.inner_text('#where')).strip()}»")
            # fino all'ultimo passo (i passi con l'esercizio si saltano con l'apposito gancio: qui non si guida)
            for _ in range(20):
                if await q.is_visible("#lNext") and await q.is_enabled("#lNext"):
                    if "Prosegui" in await q.inner_text("#lNext") or "Torna al menu" in await q.inner_text("#lNext"): break
                    await q.click("#lNext"); await q.wait_for_timeout(80)
                else: break
            pros = (await q.inner_text("#lNext")).strip() if await q.is_visible("#lNext") else "(nascosto)"
            print(f"  lezione {21 + k}: pulsante in fondo «{pros}»")
            await q.click("#toMenu"); await q.wait_for_timeout(200)
        for k, li in enumerate(s["D"]):
            await q.click(f"#menu [data-q='{li}']"); await q.wait_for_timeout(200)
            t = await q.inner_text("#quiz") if await q.locator("#quiz").count() else ""
            chk("D3", f"Ripasso {21 + k}" in t, f"D3 il ripasso {21 + k} si apre: «{' '.join(t.split())[:80]}»")
            await q.keyboard.press("Escape"); await q.wait_for_timeout(150)
        chk("D3", await q.evaluate("typeof window.__sv") == "undefined", "D3 senza #collaudo __sv non esiste")
        await ctx.close()

        # D3: la scritta di «Prosegui» (la stessa che compare all'ultimo passo), col gancio
        ctx = await b.new_context(viewport={"width": 1360, "height": 650}); q = await ctx.new_page(); q.on("pageerror", lambda x: errs.append(str(x)))
        await q.goto(BASE + "#collaudo"); await q.wait_for_timeout(300)
        nx = await q.evaluate("(D) => D.map(li => { __sv.openItem(['l', li]); return nextLabel(); })", s["D"])
        chk("D3", nx == ["Prosegui: Lezione 22", "Prosegui: Lezione 23", "Prosegui: Lezione 24", "Prosegui: Prova 6"], f"D3 «Prosegui» dall'ultimo passo: {nx}")
        await ctx.close()
        chk("D3", not errs, f"D3 errori della pagina: {errs[:3]}")
        await b.close()
    print("casi per parte:", casi)
    if fail: print(f"ESITO: FALLITO ({len(fail)})"); sys.exit(1)
    if any(casi.get(k, 0) == 0 for k in ("D3", "D4", "D8")): print("ESITO: NON VALIDA (una parte senza casi)"); sys.exit(1)
    print("ESITO: OK"); sys.exit(0)
asyncio.run(main())
