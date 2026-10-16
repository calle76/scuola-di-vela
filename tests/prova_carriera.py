# Prova a mano della carriera (0.24), senza dover giocare ore: apre il gioco in una finestra vera di Chromium, con una carriera
# preparata in cui i meriti sono già a posto (come il giocatore A di docs/PROPOSTA-ESAME-E-BREVETTO.md, §12) e manca solo l'esame.
# Si fa l'esame dal menu: superato, compare l'attestato; sbagliato apposta, compaiono i ripassi da fare.
# Usa un profilo del browser a parte, che si cancella alla chiusura: i salvataggi del tuo browser non si toccano.
# Non è un collaudo: non controlla niente. Si chiude chiudendo la finestra.
# Uso: .venv-collaudi/bin/python tests/prova_carriera.py
import asyncio, json, pathlib, re
from playwright.async_api import async_playwright
import sorgente
INDEX = pathlib.Path(__file__).resolve().parent.parent / "index.html"; SRC = sorgente.testo()   # dalla 1.0.3: index.html più js/
BANDS = [list(map(int, b)) for b in re.findall(r"bands: \[(\d+), (\d+), (\d+)\]", SRC)]
MK = ["m0.4", "m1.4", "m2.4", "m3.5", "m4.6"]

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(headless=False)
        ctx = await b.new_context(viewport=None); pg = await ctx.new_page()
        await pg.goto(INDEX.as_uri())
        nq = await pg.evaluate("s => new Function(s + ';return QUIZ')().map(q => q.length)", re.search(r"const QUIZ = \[.*?\n  \];", SRC, re.S).group(0))
        p = {"done": {f"l{i}": True for i in range(6)} | {f"m{i}": True for i in range(5)},
             "best": {MK[i]: BANDS[i][1] for i in range(5)}, "clean": {MK[0]: True, MK[1]: True},
             "quiz": {f"q{i}": nq[i] for i in range(4)},
             "race": {"r0.4:principianti": {"pos": 3, "n": 4, "pulita": False}, "r1.4:principianti": {"pos": 3, "n": 4, "pulita": False}}}
        await pg.evaluate("d => { localStorage.clear(); localStorage.setItem('scuolaVelaModo', 'carriera'); localStorage.setItem('scuolaVelaCarriera.v1', d); }", json.dumps(p))
        await pg.reload()
        print("Carriera pronta: manca solo l'esame (pulsante nel riquadro «Ripasso ed esame»). Chiudi la finestra per finire.", flush=True)
        await pg.wait_for_event("close", timeout=0)
        await b.close()
asyncio.run(main())
